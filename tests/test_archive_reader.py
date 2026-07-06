import json
import tempfile
import unittest
from pathlib import Path

from scripts.archive_reader import extract_user_messages, read_chat


class TestArchiveReader(unittest.TestCase):
    def test_read_chat(self):
        with tempfile.TemporaryDirectory() as tmp:
            chat_path = Path(tmp) / "chat.json"
            chat_path.write_text(
                json.dumps({
                    "id": "chat-1",
                    "title": "Edge",
                    "created_at": "2026-07-03T02:42:08Z",
                    "messages": [
                        {"role": "user", "content": "Edge crew odds today"},
                        {"role": "assistant", "content": "Here are the picks"},
                    ],
                }),
                encoding="utf-8",
            )

            result = read_chat(chat_path)

            self.assertEqual(result["title"], "Edge")
            self.assertEqual(result["created_at"], "2026-07-03T02:42:08Z")
            self.assertEqual(len(result["messages"]), 2)

    def test_extract_user_messages(self):
        chat = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi"},
                {"role": "user", "content": "World"},
            ]
        }

        result = extract_user_messages(chat)

        self.assertEqual(result, ["Hello", "World"])
