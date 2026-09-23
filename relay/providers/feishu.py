import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request


TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"


def generate_sign(timestamp: int, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(string_to_sign, digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_webhook_payload(message: str, secret: str = "", timestamp: int | None = None) -> dict:
    if not message.strip():
        raise ValueError("message must not be empty")

    payload = {"msg_type": "text", "content": {"text": message}}
    if secret:
        ts = int(time.time()) if timestamp is None else int(timestamp)
        payload["timestamp"] = str(ts)
        payload["sign"] = generate_sign(ts, secret)
    return payload


def _request_json(request: urllib.request.Request, *, timeout: int = 15) -> dict:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu HTTP {exc.code}: {body[:300]}") from exc
    return json.loads(body or "{}")


def send_webhook(message: str, webhook_url: str, secret: str = "") -> None:
    data = json.dumps(build_webhook_payload(message, secret), ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    result = _request_json(request)
    code = result.get("code", result.get("StatusCode", 0))
    if code not in (0, None):
        detail = result.get("msg", result.get("StatusMessage", "unknown error"))
        raise RuntimeError(f"Feishu webhook rejected request: code={code}, msg={detail}")


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    request = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    result = _request_json(request)
    if result.get("code", 0) != 0:
        raise RuntimeError(
            f"Feishu token request failed: code={result.get('code')}, "
            f"msg={result.get('msg', 'unknown error')}"
        )
    token = result.get("tenant_access_token", "")
    if not token:
        raise RuntimeError("Feishu token response did not include tenant_access_token")
    return token


def send_app_message(message: str, app_id: str, app_secret: str, chat_id: str) -> None:
    token = get_tenant_access_token(app_id, app_secret)
    query = urllib.parse.urlencode({"receive_id_type": "chat_id"})
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": message}, ensure_ascii=False),
    }
    request = urllib.request.Request(
        f"{MESSAGE_URL}?{query}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    result = _request_json(request)
    if result.get("code", 0) != 0:
        raise RuntimeError(
            f"Feishu message rejected: code={result.get('code')}, "
            f"msg={result.get('msg', 'unknown error')}"
        )


def send(message: str) -> None:
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
    webhook_secret = os.environ.get("FEISHU_WEBHOOK_SECRET", "").strip()
    if webhook_url:
        send_webhook(message, webhook_url, webhook_secret)
        return

    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    chat_id = os.environ.get("FEISHU_CHAT_ID", "").strip()
    if app_id and app_secret and chat_id:
        send_app_message(message, app_id, app_secret, chat_id)
        return

    raise RuntimeError(
        "Feishu provider is not configured. Set FEISHU_WEBHOOK_URL, or set "
        "FEISHU_APP_ID + FEISHU_APP_SECRET + FEISHU_CHAT_ID."
    )
