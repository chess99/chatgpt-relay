import os
import unittest
from unittest.mock import patch

from relay.providers import feishu


class FeishuTests(unittest.TestCase):
    def test_known_signature(self):
        self.assertEqual(
            feishu.generate_sign(1700000000, "test-secret"),
            "mbm4Y4oluIPQ00qlBIhX8vAZ0EKv3nw0LuTb91jPL84=",
        )

    def test_unsigned_payload(self):
        self.assertEqual(
            feishu.build_webhook_payload("hello"),
            {"msg_type": "text", "content": {"text": "hello"}},
        )

    def test_signed_payload(self):
        payload = feishu.build_webhook_payload("hello", "test-secret", timestamp=1700000000)
        self.assertEqual(payload["timestamp"], "1700000000")
        self.assertEqual(
            payload["sign"],
            "mbm4Y4oluIPQ00qlBIhX8vAZ0EKv3nw0LuTb91jPL84=",
        )

    def test_empty_message_rejected(self):
        with self.assertRaises(ValueError):
            feishu.build_webhook_payload("   ")

    def test_webhook_mode_has_priority(self):
        env = {
            "FEISHU_WEBHOOK_URL": "https://example.invalid/webhook",
            "FEISHU_WEBHOOK_SECRET": "secret",
            "FEISHU_APP_ID": "app-id",
            "FEISHU_APP_SECRET": "app-secret",
            "FEISHU_CHAT_ID": "chat-id",
        }
        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(feishu, "send_webhook") as webhook,
            patch.object(feishu, "send_app_message") as app,
        ):
            feishu.send("hello")
        webhook.assert_called_once_with(
            "hello", env["FEISHU_WEBHOOK_URL"], env["FEISHU_WEBHOOK_SECRET"]
        )
        app.assert_not_called()

    def test_app_mode_when_no_webhook(self):
        env = {
            "FEISHU_APP_ID": "app-id",
            "FEISHU_APP_SECRET": "app-secret",
            "FEISHU_CHAT_ID": "chat-id",
        }
        with patch.dict(os.environ, env, clear=True), patch.object(
            feishu, "send_app_message"
        ) as app:
            feishu.send("hello")
        app.assert_called_once_with("hello", "app-id", "app-secret", "chat-id")

    def test_missing_config_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "not configured"):
                feishu.send("hello")
