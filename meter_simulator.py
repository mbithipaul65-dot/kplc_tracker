def get_meter_details():
    """Returns the registered KPLC meter details."""
    return {
        "meter_number": "37192840192"  # Replace with your actual meter number
    }

def calculate_remaining_units():
    """Calculates or returns the current remaining power in units."""
    return 2.2  # Example: 2.2 units remaining

def get_daily_consumption_rate():
    """Returns average daily consumption in units per day."""
    return 3.5  # Example: 3.5 units used per day

def get_dynamic_threshold():
    """Calculates low-power threshold based on 2 days of reserve power."""
    return get_daily_consumption_rate() * 2  # Dynamic threshold = 7.0 units