# agents/prompt_templates.py

# Templates for user interaction and responses
WELCOME_MESSAGE = """
Welcome to FoodieSpot Reservation System! 🍽️
I can help you:
- Book a reservation
- Find a restaurant recommendation
- Query restaurant details
What would you like to do?
"""

ASK_RESERVATION_DETAILS = """
Please provide the following details to make a reservation:
- Restaurant name
- Date and time (e.g., 2025-05-17 18:00)
- Number of people
"""

ASK_RECOMMENDATION_DETAILS = """
To recommend a restaurant, please tell me:
- Preferred cuisine (e.g., Italian, Chinese)
- Number of people
- Date and time (e.g., 2025-05-17 18:00)
"""

RESPONSE_RESERVATION_SUCCESS = """
Reservation successful! 🎉
Details:
- Restaurant: {restaurant_name}
- Date and Time: {date_time}
- Party Size: {party_size}
"""

RESPONSE_RECOMMENDATION = """
Based on your preferences, I recommend:
- Restaurant: {restaurant_name}
- Cuisine: {cuisine}
- Location: {location}
Would you like to book a reservation here?
"""

ERROR_INVALID_INPUT = """
Sorry, I couldn’t understand your request.
"""

DYNAMIC_GUIDANCE = """
It looks like you might be interested in {possible_action}. {suggestion}
"""

GUIDANCE_SUGGESTIONS = {
    "make_reservation": "Try saying something like: 'Book a table at Restaurant A for 2 people at 2025-05-17 18:00'.",
    "recommend_restaurant": "Try saying something like: 'Recommend an Italian restaurant for 4 people'.",
    "query_restaurant": "Try saying something like: 'Tell me about Restaurant B'."
}

ERROR_NO_AVAILABILITY = """
Sorry, the restaurant is fully booked at that time. Please try a different time or restaurant.
"""