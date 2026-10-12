def get_dynamic_threshold():
    """Calculates threshold based on average daily consumption (e.g., 2 days reserve)."""
    # Example logic: fetch average daily usage from database or simulation model
    average_daily_consumption = 3.5  # kWh per day (replace with your dynamic calculation)
    
    # Threshold = enough power to last for 2 days before total depletion
    reserve_days = 2
    dynamic_threshold = average_daily_consumption * reserve_days
    
    return dynamic_threshold