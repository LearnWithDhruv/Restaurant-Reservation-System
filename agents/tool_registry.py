# agents/tool_registry.py

from datetime import datetime  # Add this import
from tools.reservation_tools import make_reservation
from tools.recommendation_tools import recommend_restaurant
from tools.query_tools import query_restaurant
from services.data_service import DataService
from config import RESTAURANTS_FILE, RESERVATIONS_FILE

print(f"ToolRegistry: datetime = {datetime}, has strptime = {hasattr(datetime, 'strptime')}")
# Initialize DataService to access restaurant data
data_service = DataService(RESTAURANTS_FILE, RESERVATIONS_FILE)

# Registry of available tools with intent keywords and weights
TOOLS = {
    "make_reservation": {
        "function": make_reservation,
        "description": "Books a reservation at a restaurant.",
        "parameters": ["restaurant_name", "date_time", "party_size"],
        "keywords": ["book", "reserve", "table"],
        "weight": 1.0
    },
    "recommend_restaurant": {
        "function": recommend_restaurant,
        "description": "Recommends a restaurant based on user preferences.",
        "parameters": ["cuisine", "party_size", "date_time"],
        "keywords": ["recommend", "suggest", "find"],
        "weight": 0.8
    },
    "query_restaurant": {
        "function": query_restaurant,
        "description": "Queries details about a restaurant.",
        "parameters": ["restaurant_name"],
        "keywords": ["query", "details", "info"],
        "weight": 0.6
    }
}

def detect_intent(user_input):
    """
    Detects user intent based on input using a scoring mechanism.
    Returns the tool name and extracted parameters.
    """
    user_input = user_input.lower().strip()
    restaurants = data_service.load_restaurants()
    restaurant_names = [r["name"].lower() for r in restaurants]

    # Extract fields
    potential_restaurant = extract_field(user_input, "restaurant")
    cuisine = extract_field(user_input, "cuisine")
    date_time = extract_field(user_input, "time")
    party_size = extract_field(user_input, "people")

    # Initialize scores for each intent
    intent_scores = {intent: 0.0 for intent in TOOLS}

    # Score intents based on keywords
    for intent, tool in TOOLS.items():
        for keyword in tool["keywords"]:
            if keyword in user_input:
                intent_scores[intent] += tool["weight"]

    # Boost scores based on extracted fields
    if potential_restaurant and potential_restaurant.lower() in restaurant_names:
        intent_scores["make_reservation"] += 0.5
        intent_scores["query_restaurant"] += 0.7  # Higher boost for query since it's more likely
    if cuisine:
        intent_scores["recommend_restaurant"] += 0.6
    if date_time and party_size:
        intent_scores["make_reservation"] += 0.4
        intent_scores["recommend_restaurant"] += 0.3

    # Select the intent with the highest score
    best_intent = max(intent_scores, key=intent_scores.get)
    if intent_scores[best_intent] == 0.0:  # No intent detected
        return None, {}

    # Prepare parameters based on the selected intent
    params = {}
    if best_intent == "make_reservation":
        params = {
            "restaurant_name": potential_restaurant,
            "date_time": date_time or "2025-05-17 18:00",
            "party_size": party_size or "2"
        }
    elif best_intent == "recommend_restaurant":
        params = {
            "cuisine": cuisine or "Italian",
            "party_size": party_size or "2",
            "date_time": date_time or "2025-05-17 18:00"
        }
    elif best_intent == "query_restaurant":
        params = {
            "restaurant_name": potential_restaurant
        }

    return best_intent, params

def extract_field(user_input, field):
    """
    Extracts a field from user input dynamically.
    """
    user_input = user_input.lower()

    if field == "restaurant":
        restaurants = data_service.load_restaurants()
        restaurant_names = [r["name"].lower() for r in restaurants]
        for name in restaurant_names:
            if name in user_input:
                for r in restaurants:
                    if r["name"].lower() == name:
                        return r["name"]
        return None

    elif field == "cuisine":
        restaurants = data_service.load_restaurants()
        cuisines = set(r["cuisine"].lower() for r in restaurants)
        for cuisine in cuisines:
            if cuisine in user_input:
                return cuisine.capitalize()
        return None

    elif field == "time":
        words = user_input.split()
        for i, word in enumerate(words):
            if word in ["at", "on"] and i + 1 < len(words):
                # Look for "YYYY-MM-DD HH:MM", "YYYY-MM-DD HH:MM:SS", or "YYYY-MM-DD HHMM"
                potential_time = " ".join(words[i + 1:i + 3])  # Start with "YYYY-MM-DD HH:MM"
                if potential_time:
                    # Check if it matches any supported format
                    formats = ['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H%M']
                    for fmt in formats:
                        try:
                            datetime.strptime(potential_time, fmt)
                            return potential_time
                        except ValueError:
                            continue
                # If the first attempt fails, try including seconds
                potential_time = " ".join(words[i + 1:i + 4])  # Include possible seconds
                if potential_time:
                    for fmt in formats:
                        try:
                            datetime.strptime(potential_time, fmt)
                            return potential_time
                        except ValueError:
                            continue
        return None

    elif field == "people":
        words = user_input.split()
        for i, word in enumerate(words):
            if word in ["for"] and i + 1 < len(words):
                try:
                    num = int(words[i + 1])
                    return str(num)
                except ValueError:
                    continue
        return None

    return None