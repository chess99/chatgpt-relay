import os
import sys

from relay.providers import feishu


PROVIDERS = {
    "feishu": feishu.send,
}


def dispatch(provider_name: str, message: str) -> None:
    name = provider_name.strip().lower()
    if not name:
        raise ValueError("RELAY_PROVIDER must not be empty")
    if not message.strip():
        raise ValueError("RELAY_MESSAGE must not be empty")

    try:
        sender = PROVIDERS[name]
    except KeyError as exc:
        supported = ", ".join(sorted(PROVIDERS))
        raise ValueError(f"Unsupported RELAY_PROVIDER '{name}'. Supported: {supported}") from exc

    sender(message)


def main() -> int:
    provider_name = os.environ.get("RELAY_PROVIDER", "feishu")
    message = os.environ.get("RELAY_MESSAGE", "")

    try:
        dispatch(provider_name, message)
    except Exception as exc:
        print(f"Relay failed: {exc}", file=sys.stderr)
        return 1

    print(f"Relay delivered via provider '{provider_name.strip().lower()}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
