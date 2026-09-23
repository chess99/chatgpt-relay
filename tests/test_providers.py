import os
import unittest
from unittest.mock import patch

from relay.providers import discord, googlechat, line, slack, telegram, twilio, wecom
from relay.providers import canonical_provider_names, resolve_provider


class RegistryTests(unittest.TestCase):
    def test_expected_providers_registered(self):
        self.assertEqual(
            canonical_provider_names(),
            ("feishu", "telegram", "discord", "slack", "googlechat", "line", "wecom", "twilio"),
        )

    def test_aliases(self):
        self.assertEqual(resolve_provider("lark").name, "feishu")
        self.assertEqual(resolve_provider("sms").name, "twilio")
        self.assertEqual(resolve_provider("gchat").name, "googlechat")


class ProviderTests(unittest.TestCase):
    def test_telegram_payload(self):
        env = {"TELEGRAM_BOT_TOKEN": "token", "TELEGRAM_CHAT_ID": "123"}
        with patch.dict(os.environ, env, clear=True), patch.object(
            telegram, "request_json", return_value=(200, {"ok": True})
        ) as request:
            telegram.send("hello")
        payload = request.call_args.kwargs["json_body"]
        self.assertEqual(payload["chat_id"], "123")
        self.assertEqual(payload["text"], "hello")

    def test_discord_webhook(self):
        with patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": "https://example.invalid"}, clear=True), patch.object(
            discord, "request", return_value=(204, "")
        ) as request:
            discord.send("hello")
        self.assertEqual(request.call_args.kwargs["json_body"], {"content": "hello"})

    def test_slack_webhook(self):
        with patch.dict(os.environ, {"SLACK_WEBHOOK_URL": "https://example.invalid"}, clear=True), patch.object(
            slack, "request", return_value=(200, "ok")
        ) as request:
            slack.send("hello")
        self.assertEqual(request.call_args.kwargs["json_body"], {"text": "hello"})

    def test_google_chat_webhook(self):
        with patch.dict(os.environ, {"GOOGLE_CHAT_WEBHOOK_URL": "https://example.invalid"}, clear=True), patch.object(
            googlechat, "request_json", return_value=(200, {"name": "spaces/x/messages/y"})
        ) as request:
            googlechat.send("hello")
        self.assertEqual(request.call_args.kwargs["json_body"], {"text": "hello"})

    def test_line_push(self):
        env = {"LINE_CHANNEL_ACCESS_TOKEN": "token", "LINE_TO_ID": "U123"}
        with patch.dict(os.environ, env, clear=True), patch.object(
            line, "request_json", return_value=(200, {})
        ) as request:
            line.send("hello")
        self.assertEqual(request.call_args.kwargs["json_body"]["to"], "U123")

    def test_wecom_webhook(self):
        with patch.dict(os.environ, {"WECOM_WEBHOOK_URL": "https://example.invalid"}, clear=True), patch.object(
            wecom, "request_json", return_value=(200, {"errcode": 0, "errmsg": "ok"})
        ) as request:
            wecom.send("hello")
        self.assertEqual(request.call_args.kwargs["json_body"]["msgtype"], "text")

    def test_twilio_form(self):
        env = {
            "TWILIO_ACCOUNT_SID": "AC123",
            "TWILIO_AUTH_TOKEN": "secret",
            "TWILIO_FROM": "+10000000001",
            "TWILIO_TO": "+10000000002",
        }
        with patch.dict(os.environ, env, clear=True), patch.object(
            twilio, "request_json", return_value=(201, {"sid": "SM123"})
        ) as request:
            twilio.send("hello")
        self.assertEqual(request.call_args.kwargs["form_body"]["Body"], "hello")
        self.assertEqual(request.call_args.kwargs["basic_auth"], ("AC123", "secret"))
