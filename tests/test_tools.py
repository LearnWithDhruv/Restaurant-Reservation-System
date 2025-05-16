# tests/test_tools.py

import unittest
from tools.reservation_tools import make_reservation
from services.data_service import DataService
from config import RESTAURANTS_FILE, RESERVATIONS_FILE

class TestTools(unittest.TestCase):
    def setUp(self):
        self.data_service = DataService(RESTAURANTS_FILE, RESERVATIONS_FILE)

    def test_make_reservation(self):
        params = {
            "restaurant_name": "Restaurant A",
            "date_time": "2025-05-17 18:00",
            "party_size": "2"
        }
        result = make_reservation(params, self.data_service)
        self.assertTrue("Reservation successful" in result)

if __name__ == "__main__":
    unittest.main()