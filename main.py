"""
Telegram-Bot – Hauptdatei.

Ein einfacher, aber erweiterbarer Bot auf Basis von python-telegram-bot (v21+).
Er stellt die Befehle /start und /help bereit und beantwortet normale
Textnachrichten mit einer kleinen, cleveren Logik (Zeit, Text umkehren,
humorvoller Kommentar).
"""

import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# .env laden (TELEGRAM_BOT_TOKEN usw.)
load_dotenv()

# Logging einrichten, damit man im Terminal sieht, was passiert.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
# httpx ist sehr gesprächig – auf WARNING drosseln.
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
# Befehls-Handler
# --------------------------------------------------------------------------- #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Begrüßt den Nutzer und listet die verfügbaren Befehle auf."""
    user = update.effective_user
    name = user.first_name if user else "da"
    text = (
        f"👋 Hallo {name}! Willkommen beim Bot.\n\n"
        "Ich kann folgendes:\n"
        "• /start – diese Begrüßung anzeigen\n"
        "• /help – Hilfe und Beispiele\n"
        "• /time – aktuelle Uhrzeit ausgeben\n"
        "• /reverse <text> – deinen Text rückwärts ausgeben\n\n"
        "Oder schreib mir einfach eine Nachricht – ich antworte dir! 🙂"
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Zeigt eine kurze Hilfe mit Beispielen."""
    text = (
        "ℹ️ *Hilfe*\n\n"
        "*Befehle:*\n"
        "• /start – Begrüßung\n"
        "• /help – diese Hilfe\n"
        "• /time – aktuelle Uhrzeit\n"
        "• /reverse <text> – Text umkehren\n\n"
        "*Freier Chat:*\n"
        "Schreib mir irgendeinen Text. Ich reagiere je nach Inhalt – "
        "z. B. auf eine Begrüßung, eine Frage oder eine Nachricht mit einem "
        "Fragezeichen.\n\n"
        "_Beispiel:_ schick mir `Hallo` oder `/reverse Telegram`"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gibt die aktuelle Server-Uhrzeit aus."""
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await update.message.reply_text(f"🕒 Aktuelle Uhrzeit (Server): {now}")


async def reverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kehrt den übergebenen Text um. Nutzung: /reverse <text>"""
    if not context.args:
        await update.message.reply_text(
            "Bitte gib einen Text an, z. B.: /reverse Hallo Welt"
        )
        return
    original = " ".join(context.args)
    await update.message.reply_text(f"🔁 {original[::-1]}")


# --------------------------------------------------------------------------- #
# Smarte Antwort auf normale Textnachrichten
# --------------------------------------------------------------------------- #
async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Beantwortet normale Textnachrichten mit einer kleinen Logik.

    Platzhalter / Beispiel-Logik:
    - Begrüßung erkennen
    - Fragen (mit "?") erkennen
    - sonst: Text humorvoll kommentieren und Länge zurückgeben
    """
    text = (update.message.text or "").strip()
    lower = text.lower()

    greetings = {"hallo", "hi", "hey", "servus", "moin", "guten tag"}

    if lower in greetings:
        reply = "👋 Hallo! Wie kann ich dir helfen? Tippe /help für alle Optionen."
    elif text.endswith("?"):
        reply = (
            "🤔 Eine gute Frage! Ich bin noch ein einfacher Bot, aber hier "
            "könntest du echte Logik (z. B. eine API oder ein KI-Modell) "
            "anbinden."
        )
    elif lower in {"danke", "dankeschön", "thx", "thanks"}:
        reply = "😊 Gern geschehen!"
    else:
        reply = (
            f'Du hast geschrieben: "{text}"\n'
            f"Das sind {len(text)} Zeichen. "
            "Mit /reverse kann ich den Text auch umkehren 🙂"
        )

    await update.message.reply_text(reply)


# --------------------------------------------------------------------------- #
# Fehlerbehandlung
# --------------------------------------------------------------------------- #
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Loggt Fehler, damit der Bot nicht still abstürzt."""
    logger.error("Fehler beim Verarbeiten eines Updates:", exc_info=context.error)


# --------------------------------------------------------------------------- #
# Einstiegspunkt
# --------------------------------------------------------------------------- #
def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN ist nicht gesetzt. "
            "Lege eine .env-Datei an (siehe .env.example) oder setze die "
            "Umgebungsvariable."
        )

    app = ApplicationBuilder().token(token).build()

    # Befehle registrieren
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(CommandHandler("reverse", reverse_command))

    # Normale Textnachrichten (keine Befehle) an die smarte Antwort schicken
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply)
    )

    # Fehler-Handler
    app.add_error_handler(error_handler)

    logger.info("Bot startet … (Beenden mit Strg+C)")
    # Polling: einfachste Methode, kein öffentlicher Server nötig.
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
