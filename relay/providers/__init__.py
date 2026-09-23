from dataclasses import dataclass
from typing import Callable

from relay.providers import discord, feishu, googlechat, line, slack, telegram, twilio, wecom


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    label: str
    sender: Callable[[str], None]
    aliases: tuple[str, ...] = ()


_SPECS = (
    ProviderSpec("feishu", "Feishu / Lark", feishu.send, ("lark",)),
    ProviderSpec("telegram", "Telegram", telegram.send),
    ProviderSpec("discord", "Discord", discord.send),
    ProviderSpec("slack", "Slack", slack.send),
    ProviderSpec("googlechat", "Google Chat", googlechat.send, ("google-chat", "gchat")),
    ProviderSpec("line", "LINE", line.send),
    ProviderSpec("wecom", "WeCom / 企业微信", wecom.send, ("wechat-work", "work-wechat")),
    ProviderSpec("twilio", "Twilio SMS", twilio.send, ("sms",)),
)

_BY_NAME: dict[str, ProviderSpec] = {}
for spec in _SPECS:
    _BY_NAME[spec.name] = spec
    for alias in spec.aliases:
        _BY_NAME[alias] = spec


def resolve_provider(name: str) -> ProviderSpec:
    normalized = name.strip().lower()
    try:
        return _BY_NAME[normalized]
    except KeyError as exc:
        supported = ", ".join(spec.name for spec in _SPECS)
        raise ValueError(
            f"Unsupported RELAY_PROVIDER '{normalized}'. Supported: {supported}"
        ) from exc


def canonical_provider_names() -> tuple[str, ...]:
    return tuple(spec.name for spec in _SPECS)
