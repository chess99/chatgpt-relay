import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.request


def generate_sign(timestamp: int, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(string_to_sign, digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_payload(message: str, secret: str = "", timestamp: int | None = None) -> dict:
    if not message.strip():
        raise ValueError("message must not be empty")

    payload = {
        "msg_type": "text",
        "content": {"text": message},
    }

    if secret:
        ts = int(time.time()) if timestamp is None else int(timestamp)
        payload["timestamp"] = str(ts)
        payload["sign"] = generate_sign(ts, secret)

    return payload


def send(message: str) -> None:
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
    secret = os.environ.get("FEISHU_WEBHOOK_SECRET", "").strip()

    if not webhook_url:
        raise RuntimeError("FEISHU_WEBHOOK_URL is required for provider 'feishu'")

    data = json.dumps(build_payload(message, secret), ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu webhook HTTP {exc.code}: {body[:300]}") from exc

    result = json.loads(body or "{}")
    code = result.get("code", result.get("StatusCode", 0))
    if code not in (0, None):
        detail = result.get("msg", result.get("StatusMessage", "unknown error"))
        raise RuntimeError(f"Feishu webhook rejected request: code={code}, msg={detail}")
