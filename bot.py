#!/usr/bin/env python3
"""
Telegram bot for РИТМ courier park.
Run as a separate process: python bot.py
Requires TELEGRAM_BOT_TOKEN and optionally TELEGRAM_ADMIN_CHAT_ID.
"""

import os
import sys
import logging
import time
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ritm.bot")

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SITE_URL = os.environ.get("SITE_URL", "https://example.com")
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_ADMIN_CHAT_ID")

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN is not set. Bot cannot start.")
    sys.exit(1)

try:
    import requests
except ImportError:
    logger.error("requests library is required")
    sys.exit(1)

API = f"https://api.telegram.org/bot{TOKEN}"


def api_call(method, **params):
    try:
        r = requests.post(f"{API}/{method}", json=params, timeout=30)
        data = r.json()
        if not data.get("ok"):
            logger.warning("API error: %s", data)
        return data
    except Exception as e:
        logger.exception("API call failed: %s", e)
        return None


def send_message(chat_id, text, reply_markup=None):
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_markup:
        params["reply_markup"] = reply_markup
    return api_call("sendMessage", **params)


def handle_start(chat_id, username=None):
    name = f", {username}" if username else ""
    text = (
        f"Здравствуйте{name}!\n\n"
        "Вы в боте курьерского парка <b>РИТМ</b>.\n\n"
        "«Твой город. Твой маршрут. Твой доход»\n\n"
        "Мы — независимый курьерский парк для пеших курьеров в Самаре.\n\n"
        "Чтобы оставить заявку, перейдите на сайт."
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "Открыть сайт", "url": SITE_URL}],
            [{"text": "Политика ПДн", "url": f"{SITE_URL}/privacy"}],
        ]
    }
    send_message(chat_id, text, reply_markup=keyboard)


def handle_help(chat_id):
    text = (
        "<b>Доступные команды:</b>\n\n"
        "/start — приветствие и ссылка на сайт\n"
        "/help — эта справка\n"
        "/privacy — политика обработки персональных данных\n\n"
        "Заявки принимаются только через сайт."
    )
    send_message(chat_id, text)


def handle_privacy(chat_id):
    text = (
        "Политика обработки персональных данных доступна на сайте:\n"
        f"{SITE_URL}/privacy"
    )
    send_message(chat_id, text)


def process_update(update):
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip()
    username = message.get("from", {}).get("first_name") or message.get("from", {}).get("username")

    if text.startswith("/start"):
        handle_start(chat_id, username)
    elif text.startswith("/help"):
        handle_help(chat_id)
    elif text.startswith("/privacy"):
        handle_privacy(chat_id)
    else:
        send_message(
            chat_id,
            "Используйте /start, /help или /privacy.\n"
            f"Заявки — на сайте: {SITE_URL}",
        )


def main():
    logger.info("Starting РИТМ Telegram bot...")
    offset = 0
    while True:
        try:
            data = api_call("getUpdates", offset=offset, timeout=30)
            if not data or not data.get("ok"):
                time.sleep(3)
                continue
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                try:
                    process_update(update)
                except Exception:
                    logger.exception("Error processing update")
        except KeyboardInterrupt:
            logger.info("Bot stopped")
            break
        except Exception:
            logger.exception("Polling error")
            time.sleep(5)


if __name__ == "__main__":
    main()
