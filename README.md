# Telegram Bot (Python)

Ein einfacher, erweiterbarer Telegram-Bot auf Basis von
[python-telegram-bot](https://docs.python-telegram-bot.org/).

## Funktionen

- `/start` – freundliche Begrüßung + Liste der Befehle
- `/help` – Hilfe mit Beispielen
- `/time` – aktuelle Uhrzeit
- `/reverse <text>` – kehrt deinen Text um
- **Smarte Antwort** – reagiert auf normale Textnachrichten (Begrüßung, Fragen, usw.)

## Projektstruktur

```
.
├── main.py            # Hauptcode des Bots
├── requirements.txt   # Python-Abhängigkeiten
├── .env.example       # Vorlage für den Bot-Token
├── .gitignore         # schützt u. a. die .env-Datei
└── README.md          # diese Anleitung
```

---

## 1. Bot bei Telegram erstellen (@BotFather)

1. Öffne Telegram und suche nach **@BotFather** (offizieller, blau verifizierter Account).
2. Starte den Chat mit `/start`.
3. Sende `/newbot`.
4. Wähle einen **Namen** (frei wählbar) und einen **Username** (muss auf `bot` enden, z. B. `mein_test_bot`).
5. Der BotFather gibt dir einen **Token** im Format `123456789:ABCdef...`.
6. **Diesen Token geheim halten** – er ist wie ein Passwort für deinen Bot.

> Optional: Mit `/setcommands` kannst du beim BotFather die Befehlsliste hinterlegen,
> damit sie im Telegram-Menü auftaucht.

---

## 2. Lokal einrichten und starten

### Voraussetzungen
- Python 3.10 oder neuer

### Schritte

```bash
# 1. Repository klonen
git clone <DEINE_REPO_URL>
cd <REPO_ORDNER>

# 2. (Empfohlen) virtuelle Umgebung anlegen
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Token eintragen
cp .env.example .env
# .env öffnen und TELEGRAM_BOT_TOKEN=... mit deinem echten Token füllen

# 5. Bot starten
python main.py
```

Wenn alles klappt, siehst du im Terminal `Bot startet …`.
Schreib deinem Bot in Telegram `/start` – er sollte antworten. 🎉

Beenden mit `Strg + C`.

---

## 3. Optional: Hosting

Der Bot nutzt standardmäßig **Polling** – das ist am einfachsten und braucht
keinen öffentlich erreichbaren Server.

### Variante A: Dauerhaft auf einem Server (Polling)
Lass `python main.py` z. B. auf einem kleinen VPS oder einer Plattform wie
[Railway](https://railway.app/), [Render](https://render.com/) oder
[Fly.io](https://fly.io/) laufen. Setze dort `TELEGRAM_BOT_TOKEN` als
**Umgebungsvariable** (nicht per Datei) in den Projekt-Einstellungen.

### Variante B: GitHub Actions (nur für Tests/kurze Läufe)
GitHub Actions eignet sich **nicht** für einen dauerhaft laufenden Bot
(Jobs haben ein Zeitlimit), ist aber gut, um z. B. Tests/Linting laufen zu
lassen. Den Token legst du dann unter
**Settings → Secrets and variables → Actions** als Secret `TELEGRAM_BOT_TOKEN` ab.

### Variante C: Webhooks (für Produktion mit eigenem Server)
Statt Polling kann der Bot auch per Webhook laufen. Dafür brauchst du eine
öffentlich erreichbare HTTPS-URL. In `main.py` würdest du dann
`app.run_webhook(...)` statt `app.run_polling(...)` verwenden. Für den Einstieg
reicht Polling völlig aus.

---

## Sicherheit

- Die echte **`.env`-Datei niemals committen** (ist in `.gitignore` ausgeschlossen).
- Wenn ein Token versehentlich öffentlich wurde: beim **@BotFather** mit
  `/revoke` einen neuen Token erzeugen.
