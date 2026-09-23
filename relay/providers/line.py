import os

from relay.http import request_json
from relay.text import chunk_text


def send(message: str) -> None:
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
    target = os.environ.get("LINE_TO_ID", "").strip()
    if not token or not target:
        raise RuntimeError("LINE requires LINE_CHANNEL_ACCESS_TOKEN and LINE_TO_ID")

    headers = {"Authorization": f"Bearer {token}"}
    for chunk in chunk_text(message, 4800):
        _, result = request_json(
            "POST",
            "https://api.line.me/v2/bot/message/push",
            json_body={"to": target, "messages": [{"type": "text", "text": chunk}]},
            headers=headers,
        )
        if result:
            raise RuntimeError(f"LINE returned an unexpected response: {str(result)[:200]}")
