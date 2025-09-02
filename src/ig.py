import hashlib
import hmac
import json
import logging
from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, HTTPException, Request

from .settings import settings
from .logic import make_reply

logger = logging.getLogger("ig")
router = APIRouter()

GRAPH_BASE = f"https://graph.facebook.com/{settings.GRAPH_API_VERSION}"


def _verify_signature(payload: bytes, signature_header: Optional[str]) -> bool:
    """
    Verifica X-Hub-Signature-256 si APP_SECRET está definido.
    Formato del header: 'sha256=<hex>'
    """
    if not settings.APP_SECRET:
        # Sin secreto => no verificamos (útil en desarrollo)
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    sent_sig = signature_header.split("=", 1)[1]
    mac = hmac.new(
        settings.APP_SECRET.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(mac, sent_sig)


async def _graph_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Llama POST a Graph con ?access_token=PAGE_TOKEN
    """
    url = f"{GRAPH_BASE}{path}"
    params = {"access_token": settings.IG_PAGE_TOKEN}
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, params=params, json=payload)
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Graph POST %s %s -> %s", url, payload, r.text)
            raise
        return r.json()


async def send_action(psid: str, action: str) -> None:
    """
    sender_action: typing_on | typing_off | mark_seen
    """
    payload = {"recipient": {"id": psid}, "sender_action": action}
    await _graph_post(f"/{settings.IG_USER_ID}/messages", payload)


async def send_text(psid: str, text: str) -> None:
    """
    Envía un mensaje de texto a un usuario (PSID).
    """
    payload = {"recipient": {"id": psid}, "message": {"text": text}}
    await _graph_post(f"/{settings.IG_USER_ID}/messages", payload)


@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Verificación inicial (webhook setup):
    GET /instagram/webhook?hub.mode=subscribe&hub.verify_token=...&hub.challenge=...
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.VERIFY_TOKEN and challenge is not None:
        # Devuelve el challenge como número si se puede
        try:
            return int(challenge)
        except Exception:
            return challenge

    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/webhook")
async def receive_webhook(request: Request):
    """
    Recibe eventos de Instagram (Messenger API for Instagram).
    """
    raw = await request.body()
    sig = request.headers.get("X-Hub-Signature-256")

    if not _verify_signature(raw, sig):
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Estructura: { object: 'instagram', entry: [ { messaging: [ ... ] } ] }
    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            sender = ((msg.get("sender") or {}).get("id"))  # PSID del usuario
            message = msg.get("message") or {}
            text = (message.get("text") or "").strip()

            # Ignora echos, postbacks u otros si no hay texto
            if not sender or not text:
                continue

            # Señales de "escribiendo..." y respuesta sencilla
            try:
                await send_action(sender, "typing_on")
            except Exception as e:
                logger.warning("typing_on failed: %s", e)

            # Lógica de respuesta
            reply = make_reply(text)

            try:
                await send_text(sender, reply)
            except Exception as e:
                logger.error("send_text error: %s", e)

            try:
                await send_action(sender, "typing_off")
                await send_action(sender, "mark_seen")
            except Exception as e:
                logger.warning("actions failed: %s", e)

    # Responder rápido 200 a Meta
    return {"status": "ok"}
