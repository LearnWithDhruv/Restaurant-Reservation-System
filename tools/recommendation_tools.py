# tools/recommendation_tools.py

from agents.prompt_templates import RESPONSE_RECOMMENDATION

def recommend_restaurant(params, data_service):
    """Recommends up to 3 restaurants based on user preferences with ranking."""
    cuisine = params.get("cuisine")
    party_size = params.get("party_size")
    date_time = params.get("date_time")
    restaurants = data_service.load_restaurants()

    # List to store matching restaurants with scores
    candidates = []

    # Simulated user location for scoring (for demonstration; in a real system, this would come from user input)
    user_location = "Downtown"  # Assume the user is in Downtown

    # Evaluate each restaurant
    for restaurant in restaurants:
        # Check cuisine match
        if restaurant["cuisine"].lower() != cuisine.lower():
            continue

        # Check availability
        available = restaurant["available_slots"].get(date_time, restaurant["seating_capacity"])
        if available < int(party_size):
            continue

        # Calculate a score for ranking
        score = 0.0

        # Factor 1: Cuisine match (already filtered, but could add partial matches in the future)
        score += 1.0

        # Factor 2: Availability (prefer restaurants with capacity closer to party size)
        capacity_ratio = available / int(party_size)
        if 1.0 <= capacity_ratio <= 2.0:  # Ideal fit: capacity is 1x to 2x the party size
            score += 0.5
        elif capacity_ratio > 2.0:  # Too much capacity (less cozy)
            score += 0.3

        # Factor 3: Location proximity (simplified scoring)
        if restaurant["location"] == user_location:
            score += 0.4
        elif restaurant["location"] in ["Midtown", "Uptown"]:  # Nearby locations
            score += 0.2

        # Add to candidates with score
        candidates.append({
            "restaurant": restaurant,
            "score": score,
            "reason": f"Matches your cuisine preference ({cuisine}) and has enough seating for {party_size} people."
        })

    # Sort candidates by score (descending)
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Return up to 3 recommendations
    if not candidates:
        return "No suitable restaurants found."

    # Format response for multiple recommendations
    response = "Here are my top recommendations:\n"
    for i, candidate in enumerate(candidates[:3], 1):  # Limit to 3 recommendations
        restaurant = candidate["restaurant"]
        response += f"{i}. **{restaurant['name']}** ({restaurant['cuisine']}) - {restaurant['location']}\n"
        response += f"   - {candidate['reason']}\n"
        response += "   - Would you like to book a reservation here?\n"

    return response