# tests/test_agent.py

import unittest
from agents.tool_registry import detect_intent

class TestAgent(unittest.TestCase):
    def test_detect_reservation_intent(self):
        user_input = "book a table at Restaurant A for 2 people at 2025-05-17 18:00"
        intent, params = detect_intent(user_input)
        self.assertEqual(intent, "make_reservation")
        self.assertEqual(params["restaurant_name"], "Restaurant A")
        self.assertEqual(params["party_size"], "2")

    def test_detect_recommendation_intent(self):
        user_input = "recommend a restaurant with Italian cuisine for 4 people"
        intent, params = detect_intent(user_input)
        self.assertEqual(intent, "recommend_restaurant")
        self.assertEqual(params["cuisine"], "Italian")
        self.assertEqual(params["party_size"], "4")

if __name__ == "__main__":
    unittest.main()