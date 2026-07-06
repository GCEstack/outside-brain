import unittest

from scripts.keyword_builder import build_keywords, tokenize


class TestKeywordBuilder(unittest.TestCase):
    def test_tokenize_filters_stop_words_and_punctuation(self):
        result = tokenize("The EC8 Edge Crew picks for today!")
        self.assertIn("ec8", result)
        self.assertIn("edge", result)
        self.assertIn("crew", result)
        self.assertIn("picks", result)
        self.assertNotIn("the", result)
        self.assertNotIn("for", result)

    def test_build_keywords_combines_sources(self):
        result = build_keywords(
            "EC8 Edge Crew",
            "- **Edge** (account1, 10 messages)\n- **Crew picks**",
            ["betting", "ec"],
        )

        self.assertIn("ec8", result)
        self.assertIn("edge", result)
        self.assertIn("crew", result)
        self.assertIn("betting", result)
        self.assertIn("ec", result)
        self.assertIn("picks", result)
