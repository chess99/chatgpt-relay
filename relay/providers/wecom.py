import os

from relay.http import request_json
from relay.text import chunk_text


def send(message: str) -> None:
    webhook_url = os.environ.get("WECOM_WEBHOOK_URL", "").strip()
    if not webhook_url:
        raise RuntimeError("WeCom requires WECOM_WEBHOOK_URL")

    for chunk in chunk_text(message, 1900):
        _, result = request_json(
            "POST",
            webhook_url,
            json_body={"msgtype": "text", "text": {"content": chunk}},
        )
        if result.get("errcode", 0) != 0:
            raise RuntimeError(
                f"WeCom rejected request: errcode={result.get('errcode')}, "
                f"errmsg={result.get('errmsg', 'unknown error')}"
            )
