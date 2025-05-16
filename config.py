# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESTAURANTS_FILE = os.path.join(BASE_DIR, "data", "restaurants.json")
RESERVATIONS_FILE = os.path.join(BASE_DIR, "data", "reservations.json")