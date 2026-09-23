import base64
import json
import urllib.error
import urllib.parse
import urllib.request


def request(
    method: str,
    url: str,
    *,
    json_body: dict | list | None = None,
    form_body: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    basic_auth: tuple[str, str] | None = None,
    timeout: int = 20,
) -> tuple[int, str]:
    if json_body is not None and form_body is not None:
        raise ValueError("json_body and form_body are mutually exclusive")

    body: bytes | None = None
    final_headers = dict(headers or {})
    if json_body is not None:
        body = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        final_headers.setdefault("Content-Type", "application/json; charset=utf-8")
    elif form_body is not None:
        body = urllib.parse.urlencode(form_body).encode("utf-8")
        final_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")

    if basic_auth is not None:
        username, password = basic_auth
        raw = f"{username}:{password}".encode("utf-8")
        token = base64.b64encode(raw).decode("ascii")
        final_headers["Authorization"] = f"Basic {token}"

    req = urllib.request.Request(url, data=body, headers=final_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {response_body[:300]}") from exc


def request_json(*args, **kwargs) -> tuple[int, dict]:
    status, body = request(*args, **kwargs)
    if not body.strip():
        return status, {}
    try:
        return status, json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON response, got: {body[:300]}") from exc
