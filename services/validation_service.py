# services/validation_service.py

from datetime import datetime
import pytz  # Add pytz for timezone handling

class ValidationService:
    @staticmethod
    def validate_date_time(date_time_str):
        """Validate date-time format (e.g., '2025-05-17 18:00')."""
        if not date_time_str:
            return False

        # Clean the input: remove extra spaces
        date_time_str = date_time_str.strip()

        # Supported formats
        formats = [
            '%Y-%m-%d %H:%M',      # 2025-05-16 19:00
            '%Y-%m-%d %H:%M:%S',   # 2025-05-16 19:00:00
            '%Y-%m-%d %H%M'        # 2025-05-16 1900
        ]

        parsed_time = None
        for fmt in formats:
            try:
                parsed_time = datetime.strptime(date_time_str, fmt)
                break
            except ValueError:
                continue

        if parsed_time is None:
            print(f"Date-time validation failed for '{date_time_str}'")  # Debug
            return False

        # Convert parsed time to UTC (assume input is in IST)
        ist = pytz.timezone("Asia/Kolkata")
        parsed_time = ist.localize(parsed_time).astimezone(pytz.UTC)

        # Get current time in UTC
        current_time = datetime.now(pytz.UTC)

        # Ensure the date-time is in the future
        if parsed_time <= current_time:
            print(f"Date-time '{date_time_str}' is in the past: {parsed_time} <= {current_time}")  # Debug
            return False

        return True

    @staticmethod
    def validate_party_size(party_size):
        """Validate party size is a positive integer."""
        try:
            size = int(party_size)
            return size > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_restaurant_name(restaurant_name, restaurants):
        """Validate restaurant name exists."""
        return any(r["name"] == restaurant_name for r in restaurants)

    @staticmethod
    def validate_cuisine(cuisine, restaurants):
        """Validate cuisine exists."""
        return any(r["cuisine"] == cuisine for r in restaurants)