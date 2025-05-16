# app.py

import streamlit as st
from agents.tool_registry import detect_intent, TOOLS
from agents.prompt_templates import WELCOME_MESSAGE, ERROR_INVALID_INPUT, DYNAMIC_GUIDANCE, GUIDANCE_SUGGESTIONS
from services.data_service import DataService
from config import RESTAURANTS_FILE, RESERVATIONS_FILE

# Initialize data service
data_service = DataService(RESTAURANTS_FILE, RESERVATIONS_FILE)

# Streamlit app
st.title("FoodieSpot Reservation System 🍽️")
st.markdown(WELCOME_MESSAGE)

# User input
user_input = st.text_input("Enter your request:")

if user_input:
    # Detect intent and call the appropriate tool
    intent, params = detect_intent(user_input)
    if intent and intent in TOOLS:
        tool = TOOLS[intent]["function"]
        response = tool(params, data_service)
        st.markdown(response)
    else:
        # Determine possible intent based on input
        user_input_lower = user_input.lower()
        restaurants = data_service.load_restaurants()
        restaurant_names = [r["name"].lower() for r in restaurants]
        possible_action = "something else"
        suggestion = "Please provide more details or try a different request."

        # Check if a restaurant name is mentioned
        for name in restaurant_names:
            if name in user_input_lower:
                possible_action = "querying restaurant details or making a reservation"
                suggestion = GUIDANCE_SUGGESTIONS["query_restaurant"] + " Or, " + GUIDANCE_SUGGESTIONS["make_reservation"]
                break

        # Check if a cuisine is mentioned
        cuisines = set(r["cuisine"].lower() for r in restaurants)
        for cuisine in cuisines:
            if cuisine in user_input_lower:
                possible_action = "finding a restaurant recommendation"
                suggestion = GUIDANCE_SUGGESTIONS["recommend_restaurant"]
                break

        # Display dynamic guidance
        error_message = ERROR_INVALID_INPUT + "\n" + DYNAMIC_GUIDANCE.format(
            possible_action=possible_action,
            suggestion=suggestion
        )
        st.markdown(error_message)

# Display restaurant list
if st.checkbox("Show available restaurants"):
    restaurants = data_service.load_restaurants()
    st.write("Available Restaurants:")
    for restaurant in restaurants:
        st.write(f"- {restaurant['name']} ({restaurant['cuisine']}) - {restaurant['location']}")