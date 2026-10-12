import africastalking
from meter_simulator import calculate_remaining_units, get_dynamic_threshold

# Africa's Talking Configuration
username = "sandbox"  
api_key = "atsk_61335d944296dca8cc48d72912300887f40563b46a74dfa7c2698a5f7a708c6ec32b1992"    
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def check_and_send_sms():
    """Checks power meter balance against a dynamic daily-consumption threshold and alerts if low."""
    
    current_units = calculate_remaining_units()     # e.g., current kWh remaining
    threshold_units = get_dynamic_threshold()       # Dynamically calculated based on daily usage
    
    # Check if units fall below the individualized daily-consumption threshold
    if current_units < threshold_units:
        recipients = ["+254740395200"]  # Your phone number
        
        message = (
            f"KPLC ALERT: Low balance ({current_units:.1f} kWh left). "
            f"Based on your daily usage, your power may run out soon. Please top up!"
        )
        
        try:
            response = sms.send(message, recipients)
            print("Dynamic low balance alert sent:", response)
            return f"Alert sent. Units: {current_units:.1f}, Threshold: {threshold_units:.1f}"
        except Exception as e:
            print("Error sending SMS:", str(e))
            return f"Failed to send SMS: {str(e)}"
    else:
        print(f"Balance OK. Current: {current_units:.1f} kWh, Threshold: {threshold_units:.1f} kWh.")
        return f"Balance OK. No SMS needed."