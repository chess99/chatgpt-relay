import os

from relay.http import request_json
from relay.text import chunk_text


def send(message: str) -> None:
    webhook_url = os.environ.get("GOOGLE_CHAT_WEBHOOK_URL", "").strip()
    if not webhook_url:
        raise RuntimeError("Google Chat requires GOOGLE_CHAT_WEBHOOK_URL")

    for chunk in chunk_text(message, 3900):
        _, result = request_json("POST", webhook_url, json_body={"text": chunk})
        if result and "name" not in result:
            raise RuntimeError("Google Chat webhook returned an unexpected response")
