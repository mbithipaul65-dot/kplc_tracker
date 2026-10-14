from db_manager import get_latest_meter_data

def get_meter_details():
    """Returns the registered KPLC meter details."""
    return {
        "meter_number": "37192840192",
        "phone_number": "+254740395206"  # <--- Add your phone number here
    }

def calculate_remaining_units():
    """Fetches the current remaining token units from the database."""
    data = get_latest_meter_data()
    return data.get("current_units", 2.2)

def get_daily_consumption_rate():
    """Fetches average daily consumption from the database."""
    data = get_latest_meter_data()
    return data.get("daily_consumption", 3.5)

def get_dynamic_threshold():
    """Calculates low-power threshold based on 2 days of reserve power."""
    return get_daily_consumption_rate() * 2