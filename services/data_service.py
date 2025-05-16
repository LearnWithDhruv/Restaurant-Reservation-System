# services/data_service.py

import json
import os
from datetime import datetime  # Add this import

class DataService:
    def __init__(self, restaurants_file, reservations_file):
        self.restaurants_file = restaurants_file
        self.reservations_file = reservations_file
        self._initialize_data()

    def _initialize_data(self):
        """Initialize restaurant and reservation data if they don't exist or are invalid."""
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.restaurants_file), exist_ok=True)

        # Initialize restaurants.json
        if not os.path.exists(self.restaurants_file) or os.path.getsize(self.restaurants_file) == 0:
            restaurants = self._generate_restaurant_data()
            with open(self.restaurants_file, 'w') as f:
                json.dump(restaurants, f, indent=4)

        # Initialize reservations.json
        if not os.path.exists(self.reservations_file) or os.path.getsize(self.reservations_file) == 0:
            with open(self.reservations_file, 'w') as f:
                json.dump([], f, indent=4)

    def _generate_restaurant_data(self):
        """Generate 20 restaurant entries programmatically."""
        locations = ["Downtown", "Midtown", "Uptown", "Eastside", "Westside"]
        cuisines = ["Italian", "Japanese", "Mexican", "Chinese", "Indian"]
        restaurants = []
        for i in range(20):
            name = f"Restaurant {chr(65 + i)}"  # Restaurant A, B, ..., T
            location = locations[i % len(locations)]
            cuisine = cuisines[i % len(cuisines)]
            seating_capacity = (i % 3 + 1) * 20  # 20, 40, 60
            restaurants.append({
                "name": name,
                "location": location,
                "cuisine": cuisine,
                "seating_capacity": seating_capacity,
                "available_slots": {
                    "2025-05-17 18:00": seating_capacity
                }
            })
        return restaurants

    def load_restaurants(self):
        """Load restaurant data from file with error handling."""
        try:
            with open(self.restaurants_file, 'r') as f:
                content = f.read().strip()
                if not content:  # If file is empty, reinitialize
                    restaurants = self._generate_restaurant_data()
                    with open(self.restaurants_file, 'w') as f_write:
                        json.dump(restaurants, f_write, indent=4)
                    return restaurants
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # Reinitialize the file if there's an error
            restaurants = self._generate_restaurant_data()
            with open(self.restaurants_file, 'w') as f:
                json.dump(restaurants, f, indent=4)
            return restaurants

    def load_reservations(self):
        """Load reservation data from file with error handling."""
        try:
            with open(self.reservations_file, 'r') as f:
                content = f.read().strip()
                if not content:  # If file is empty, reinitialize
                    with open(self.reservations_file, 'w') as f_write:
                        json.dump([], f_write, indent=4)
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # Reinitialize the file if there's an error
            with open(self.reservations_file, 'w') as f:
                json.dump([], f, indent=4)
            return []

    def save_reservation(self, reservation):
        """Save a new reservation to file."""
        reservations = self.load_reservations()
        reservations.append(reservation)
        with open(self.reservations_file, 'w') as f:
            json.dump(reservations, f, indent=4)

    def update_availability(self, restaurant_name, date_time, party_size):
        """Update restaurant availability after a reservation."""
        restaurants = self.load_restaurants()
        for restaurant in restaurants:
            if restaurant["name"] == restaurant_name:
                if date_time not in restaurant["available_slots"]:
                    restaurant["available_slots"][date_time] = restaurant["seating_capacity"]
                available = restaurant["available_slots"][date_time]
                if available < int(party_size):
                    return False
                restaurant["available_slots"][date_time] -= int(party_size)
                break
        with open(self.restaurants_file, 'w') as f:
            json.dump(restaurants, f, indent=4)
        return True