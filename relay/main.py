import os
import sys

from relay.providers import resolve_provider


def dispatch(provider_name: str, message: str) -> str:
    if not message.strip():
        raise ValueError("RELAY_MESSAGE must not be empty")
    spec = resolve_provider(provider_name)
    spec.sender(message)
    return spec.name


def main() -> int:
    provider_name = os.environ.get("RELAY_PROVIDER", "feishu")
    message = os.environ.get("RELAY_MESSAGE", "")

    try:
        delivered_by = dispatch(provider_name, message)
    except Exception as exc:
        print(f"Relay failed: {exc}", file=sys.stderr)
        return 1

    print(f"Relay delivered via provider '{delivered_by}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
