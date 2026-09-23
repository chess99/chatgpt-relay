import unittest
from unittest.mock import patch

from relay import main


class MainTests(unittest.TestCase):
    def test_dispatch_calls_selected_provider(self):
        fake_spec = type("Spec", (), {"name": "test", "sender": lambda self, message: None})()
        with patch.object(main, "resolve_provider", return_value=fake_spec):
            self.assertEqual(main.dispatch("TEST", "hello"), "test")

    def test_unknown_provider_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported RELAY_PROVIDER"):
            main.dispatch("missing", "hello")

    def test_empty_message_rejected(self):
        with self.assertRaisesRegex(ValueError, "RELAY_MESSAGE"):
            main.dispatch("feishu", "  ")
