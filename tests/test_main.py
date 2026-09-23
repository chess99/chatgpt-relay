import unittest
from unittest.mock import patch

from relay import main


class MainTests(unittest.TestCase):
    def test_dispatch_calls_selected_provider(self):
        calls = []
        with patch.dict(main.PROVIDERS, {"test": calls.append}, clear=True):
            main.dispatch("TEST", "hello")
        self.assertEqual(calls, ["hello"])

    def test_unknown_provider_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported RELAY_PROVIDER"):
            main.dispatch("missing", "hello")

    def test_empty_message_rejected(self):
        with self.assertRaisesRegex(ValueError, "RELAY_MESSAGE"):
            main.dispatch("feishu", "  ")
