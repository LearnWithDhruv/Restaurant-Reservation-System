# tools/query_tools.py

def query_restaurant(params, data_service):
    """Queries details about a restaurant."""
    restaurant_name = params.get("restaurant_name")
    restaurants = data_service.load_restaurants()

    for restaurant in restaurants:
        if restaurant["name"] == restaurant_name:
            return f"""
Restaurant Details:
- Name: {restaurant['name']}
- Location: {restaurant['location']}
- Cuisine: {restaurant['cuisine']}
- Seating Capacity: {restaurant['seating_capacity']}
"""
    return "Restaurant not found."