import os

from relay.http import request, request_json
from relay.text import chunk_text


def send(message: str) -> None:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if webhook_url:
        for chunk in chunk_text(message, 3900):
            status, body = request("POST", webhook_url, json_body={"text": chunk})
            if status != 200 or body.strip().lower() not in ("", "ok"):
                raise RuntimeError(f"Slack webhook rejected request: {body[:200]}")
        return

    token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
    channel_id = os.environ.get("SLACK_CHANNEL_ID", "").strip()
    if not token or not channel_id:
        raise RuntimeError(
            "Slack requires SLACK_WEBHOOK_URL, or SLACK_BOT_TOKEN + SLACK_CHANNEL_ID"
        )

    headers = {"Authorization": f"Bearer {token}"}
    for chunk in chunk_text(message, 3900):
        _, result = request_json(
            "POST",
            "https://slack.com/api/chat.postMessage",
            json_body={"channel": channel_id, "text": chunk},
            headers=headers,
        )
        if result.get("ok") is not True:
            raise RuntimeError(f"Slack rejected request: {result.get('error', 'unknown error')}")
