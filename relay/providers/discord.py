import os
import urllib.parse

from relay.http import request, request_json
from relay.text import chunk_text


def send(message: str) -> None:
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if webhook_url:
        for chunk in chunk_text(message, 1900):
            status, _ = request("POST", webhook_url, json_body={"content": chunk})
            if status not in (200, 204):
                raise RuntimeError(f"Discord webhook returned HTTP {status}")
        return

    token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    channel_id = os.environ.get("DISCORD_CHANNEL_ID", "").strip()
    if not token or not channel_id:
        raise RuntimeError(
            "Discord requires DISCORD_WEBHOOK_URL, or DISCORD_BOT_TOKEN + DISCORD_CHANNEL_ID"
        )

    channel = urllib.parse.quote(channel_id, safe="")
    url = f"https://discord.com/api/v10/channels/{channel}/messages"
    headers = {"Authorization": f"Bot {token}"}
    for chunk in chunk_text(message, 1900):
        _, result = request_json("POST", url, json_body={"content": chunk}, headers=headers)
        if "id" not in result:
            raise RuntimeError("Discord bot API returned no message id")
