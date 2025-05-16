# FoodieSpot Reservation System

## Overview
This project implements a conversational AI reservation system for FoodieSpot, a restaurant chain. It includes a frontend (Streamlit), recommendation capabilities, and a tool-calling architecture.

## Business Strategy (40%)
### Use Case
- **Problem**: FoodieSpot needs to streamline reservation management across multiple locations.
- **Solution**: A conversational AI agent that handles reservations, recommendations, and queries.
- **Success Metrics**:
  - 50% reduction in manual reservation handling time.
  - 20% increase in customer satisfaction (via surveys).
  - 10% increase in bookings through recommendations.
- **Vertical Expansion**:
  - Adaptable for other restaurant chains by updating `restaurants.json`.
  - Extendable to adjacent industries like event venues or hotels.
- **Competitive Advantages**:
  - Dynamic intent detection without hardcoding.
  - Recommendation system based on user preferences.
  - Scalable data management with JSON.

## Technical Implementation (60%)
- **Frontend**: Streamlit (`app.py`).
- **Data**: Stored in `restaurants.json` and `reservations.json`.
- **Tool Calling**: Implemented in `tool_registry.py` with rule-based intent detection.
- **Recommendation**: Logic in `recommendation_tools.py`.
- **Error Handling**: Input validation in `validation_service.py`.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`

## File Structure
- `agents/`: Intent detection and prompt templates.
- `data/`: Restaurant and reservation data.
- `services/`: Business logic for data and validation.
- `static/`: CSS styles.
- `tests/`: Unit tests.
- `tools/`: Reservation, recommendation, and query tools.
- `app.py`: Main Streamlit app.
- `config.py`: Configuration settings.