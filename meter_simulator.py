def get_meter_details():
    """Returns the registered KPLC meter details."""
    return {
        "meter_number": "37192840192"  # Replace with your actual KPLC meter number
    }

def calculate_remaining_units():
    """Calculates or returns the current remaining power units in kWh."""
    return 4.2  # Example: 4.2 kWh remaining (replace with DB query when ready)

def get_daily_consumption_rate():
    """Returns average daily consumption in kWh/day."""
    return 3.5  # Example: 3.5 kWh used per day

def get_dynamic_threshold():
    """Calculates low-power threshold based on 2 days of reserve power."""
    return get_daily_consumption_rate() * 2  # Alert threshold = 7.0 kWh