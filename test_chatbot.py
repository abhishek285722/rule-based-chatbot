"""
test_chatbot.py - Unit tests for Rule-Based Chatbot Engine
Validates preprocessing, pattern matching, dynamic intents, and fallback handling.
"""

import unittest
from chatbot import preprocess_text, match_intent, get_response_with_intent, get_response


class TestChatbot(unittest.TestCase):

    def test_preprocessing(self):
        """Tests that text is lowercased, punctuation stripped, and spacing normalized."""
        self.assertEqual(preprocess_text("  Hello, WORLD!!!  "), "hello world")
        self.assertEqual(preprocess_text("What's up?!"), "whats up")
        self.assertEqual(preprocess_text("25 + 10 = ?"), "25 + 10")
        self.assertEqual(preprocess_text(""), "")

    def test_word_boundary_avoidance(self):
        """Ensures substring words don't trigger false positive matches."""
        # 'this' contains 'hi', but should NOT trigger 'greeting'
        self.assertNotEqual(match_intent("this is a cool project"), "greeting")
        # 'white' contains 'hi', should NOT trigger 'greeting'
        self.assertNotEqual(match_intent("the snow is white"), "greeting")
        # 'shift' contains 'hi', should NOT trigger 'greeting'
        self.assertNotEqual(match_intent("night shift"), "greeting")

    def test_greetings_and_farewells(self):
        """Tests standard greetings and farewells."""
        self.assertEqual(match_intent("hello"), "greeting")
        self.assertEqual(match_intent("hi there!"), "greeting")
        self.assertEqual(match_intent("good morning my friend"), "greeting")
        self.assertEqual(match_intent("goodbye!"), "farewell")
        self.assertEqual(match_intent("see you later"), "farewell")

    def test_identity_and_creator(self):
        """Tests questions about bot identity and creator."""
        self.assertEqual(match_intent("who are you?"), "name")
        self.assertEqual(match_intent("what is your name"), "name")
        self.assertEqual(match_intent("who made you?"), "creator")
        self.assertEqual(match_intent("who built you"), "creator")

    def test_dynamic_time_and_date(self):
        """Tests time and date dynamic response generation."""
        resp_time, intent_time = get_response_with_intent("what time is it?")
        self.assertEqual(intent_time, "time")
        self.assertIn("The current time is", resp_time)

        resp_date, intent_date = get_response_with_intent("what is today's date?")
        self.assertEqual(intent_date, "date")
        self.assertIn("Today is", resp_date)

    def test_simple_math(self):
        """Tests arithmetic calculations."""
        resp, intent = get_response_with_intent("what is 25 * 4")
        self.assertEqual(intent, "math")
        self.assertIn("100", resp)

        resp_div, _ = get_response_with_intent("calculate 10 / 0")
        self.assertIn("zero is undefined", resp_div)

    def test_jokes_and_quotes(self):
        """Tests humor and inspirational quotes."""
        self.assertEqual(match_intent("tell me a joke"), "joke")
        self.assertEqual(match_intent("inspire me with a quote"), "quote")

    def test_help_and_thanks(self):
        """Tests help and appreciation intents."""
        self.assertEqual(match_intent("help"), "help")
        self.assertEqual(match_intent("what can you do?"), "help")
        self.assertEqual(match_intent("thank you so much!"), "thanks")

    def test_unknown_fallback(self):
        """Tests unrecognized phrases trigger the fallback intent."""
        resp, intent = get_response_with_intent("asdkjhfasdjkflh1293871239")
        self.assertEqual(intent, "unknown")
        self.assertTrue(len(resp) > 0)


if __name__ == "__main__":
    unittest.main()
