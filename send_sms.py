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
api_key = os.getenv("AT_API_KEY", "your_api_key_here")

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def check_and_send_sms():
    """Checks power meter balance in units and sends SMS alert if low."""
    meter_info = get_meter_details()
    meter_number = meter_info["meter_number"]
    phone_number = meter_info.get("phone_number", "+254712345678")
    
    current_units = calculate_remaining_units()
    threshold_units = get_dynamic_threshold()
    daily_rate = get_daily_consumption_rate()
    
    # Calculate estimated time remaining in hours
    hours_left = (current_units / daily_rate) * 24 if daily_rate > 0 else 0

    if current_units <= threshold_units:
        # Original exact message format
        message = (
            f"KPLC Alert: Meter {meter_number} token balance is low "
            f"({current_units:.1f} units remaining). "
            f"Est time left: {hours_left:.1f} hours. "
            f"Top up to avoid blackout."
        )

        try:
            response = sms.send(message, [phone_number])
            print(f"KPLC Low balance alert sent successfully: {response}")
            print(f"Alert sent for meter {meter_number}.")
        except Exception as e:
            print(f"Error sending SMS: {e}")
    else:
        print(f"Meter balance normal ({current_units:.1f} units). No alert required.")

if __name__ == "__main__":
    check_and_send_sms()