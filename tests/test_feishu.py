import unittest

from relay.providers.feishu import build_payload, generate_sign


class FeishuTests(unittest.TestCase):
    def test_known_signature(self):
        self.assertEqual(
            generate_sign(1700000000, "test-secret"),
            "mbm4Y4oluIPQ00qlBIhX8vAZ0EKv3nw0LuTb91jPL84=",
        )

    def test_unsigned_payload(self):
        self.assertEqual(
            build_payload("hello"),
            {"msg_type": "text", "content": {"text": "hello"}},
        )

    def test_signed_payload(self):
        payload = build_payload("hello", "test-secret", timestamp=1700000000)
        self.assertEqual(payload["timestamp"], "1700000000")
        self.assertEqual(
            payload["sign"],
            "mbm4Y4oluIPQ00qlBIhX8vAZ0EKv3nw0LuTb91jPL84=",
        )

    def test_empty_message_rejected(self):
        with self.assertRaises(ValueError):
            build_payload("   ")
