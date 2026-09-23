import unittest

from relay.text import chunk_text


class ChunkTextTests(unittest.TestCase):
    def test_short_text(self):
        self.assertEqual(chunk_text("hello", 10), ["hello"])

    def test_prefers_newline(self):
        self.assertEqual(chunk_text("abc\ndef", 4), ["abc", "def"])

    def test_hard_split(self):
        self.assertEqual(chunk_text("abcdef", 3), ["abc", "def"])

    def test_invalid_limit(self):
        with self.assertRaises(ValueError):
            chunk_text("hello", 0)
