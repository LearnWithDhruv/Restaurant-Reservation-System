# tools/reservation_tools.py

from agents.prompt_templates import RESPONSE_RESERVATION_SUCCESS, ERROR_NO_AVAILABILITY
from services.validation_service import ValidationService
from datetime import datetime

print(f"ReservationTools: datetime = {datetime}, has strptime = {hasattr(datetime, 'strptime')}")

def make_reservation(params, data_service):
    """Makes a reservation at a restaurant."""
    restaurant_name = params.get("restaurant_name")
    date_time = params.get("date_time")
    party_size = params.get("party_size")
    
    print(f"Validating date_time: '{date_time}'")
    # Validate inputs
    validation_service = ValidationService()
    restaurants = data_service.load_restaurants()

    if not validation_service.validate_restaurant_name(restaurant_name, restaurants):
        return "Invalid restaurant name."
    if not validation_service.validate_date_time(date_time):
        # Check if the date-time is in the past
        try:
            parsed_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
            if parsed_time <= datetime.now():
                return "The date and time must be in the future. Please choose a later time."
        except ValueError:
            pass
        return "Invalid date-time format. Use YYYY-MM-DD HH:MM (e.g., 2025-05-17 18:00)."
    if not validation_service.validate_party_size(party_size):
        return "Invalid party size. Must be a positive number."

    # Check availability and update
    if data_service.update_availability(restaurant_name, date_time, party_size):
        reservation = {
            "restaurant_name": restaurant_name,
            "date_time": date_time,
            "party_size": int(party_size)
        }
        data_service.save_reservation(reservation)
        return RESPONSE_RESERVATION_SUCCESS.format(
            restaurant_name=restaurant_name,
            date_time=date_time,
            party_size=party_size
        )
    return ERROR_NO_AVAILABILITY