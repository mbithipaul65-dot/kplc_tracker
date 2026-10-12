import os
import africastalking
from meter_simulator import (
    get_meter_details,
    calculate_remaining_units,
    get_daily_consumption_rate,
    get_dynamic_threshold
)

# Africa's Talking Configuration
username = os.getenv("AT_USERNAME", "sandbox")
api_key = os.getenv("AT_API_KEY", "atsk_61335d944296dca8cc48d72912300887f40563b46a74dfa7c2698a5f7a708c6ec32b1992")  # Ensure your valid API key is set here

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def check_and_send_sms():
    """Checks power meter balance in units and sends KPLC alert if below threshold."""
    
    meter_info = get_meter_details()
    meter_number = meter_info["meter_number"]
    
    current_units = calculate_remaining_units()
    threshold_units = get_dynamic_threshold()
    daily_rate = get_daily_consumption_rate()
    
    # Calculate estimated time left in hours: (Remaining Units / Daily Consumption) * 24 Hours
    estimated_hours_left = (current_units / daily_rate) * 24 if daily_rate > 0 else 0
    
    if current_units < threshold_units:
        recipients = ["+254740395200"]  # Your phone number
        
        # Formatted SMS text using 'units'
        message = (
            f"KPLC Alert: Meter {meter_number} token balance is low ({current_units:.1f} units remaining). "
            f"Est time left: {estimated_hours_left:.1f} hours. Top up to avoid blackout."
        )
        
        try:
            response = sms.send(message, recipients)
            print("KPLC Low balance alert sent successfully:", response)
            return f"Alert sent for meter {meter_number}."
        except Exception as e:
            print("Error sending SMS:", str(e))
            return f"Failed to send SMS: {str(e)}"
    else:
        print(f"Balance OK for meter {meter_number}. Units: {current_units:.1f} units.")
        return f"Balance OK for meter {meter_number}."

if __name__ == "__main__":
    result = check_and_send_sms()
    print(result)