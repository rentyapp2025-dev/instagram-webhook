import re


def make_reply(user_text: str) -> str:
    """
    Lógica mínima de respuestas.
    Ajusta a tu gusto: aquí solo un eco con saludos.
    """
    t = user_text.strip().lower()

    if re.search(r"\b(hola|hello|hey|buenas)\b", t):
        return (
            "¡Hola! 👋 Soy tu asistente de Instagram.\n"
            "Puedo responderte y hacer eco de tu mensaje. "
            "Escríbeme algo o di *menu* para más info."
        )

    if t == "menu":
        return (
            "Menú rápido:\n"
            "• Escribe *hola* para saludar\n"
            "• Escribe cualquier texto y te lo repito\n"
            "• Pronto: botones, quick replies, imágenes 🤖"
        )

    # Fallback: eco
    return f"Me dijiste: “{user_text}”. ¿Necesitas algo más?"
