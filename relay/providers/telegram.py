import os
from urllib.parse import quote

from relay.http import request_json
from relay.text import chunk_text


def send(message: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        raise RuntimeError("Telegram requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{quote(token, safe=':_-')}/sendMessage"
    for chunk in chunk_text(message, 4000):
        _, result = request_json(
            "POST",
            url,
            json_body={"chat_id": chat_id, "text": chunk, "disable_web_page_preview": False},
        )
        if result.get("ok") is not True:
            raise RuntimeError(
                f"Telegram rejected request: {result.get('description', 'unknown error')}"
            )
