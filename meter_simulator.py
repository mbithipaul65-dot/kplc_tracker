import random
from send_sms import send_sms_alert
# Uncomment or adjust the import below based on how your Africa's Talking SMS function is named
# from app import send_sms_alert 

class MeterSimulator:
    def __init__(self, meter_number="01928374650", initial_units=15.0):
        self.meter_number = meter_number
        self.units = float(initial_units)
        self.is_connected = True
        self.threshold = 5.0  # Low balance warning threshold in kWh

    def simulate_consumption(self):
        """
        Simulates hourly power consumption, decrements token units,
        and checks if a low-balance alert needs to be sent.
        """
        if not self.is_connected:
            return f"Meter {self.meter_number} is currently disconnected (Outage)."

        # Simulate random hourly power consumption (e.g., between 0.2 and 0.8 kWh)
        consumed = round(random.uniform(0.2, 0.8), 2)
        self.units = max(0.0, round(self.units - consumed, 2))

        status_message = f"Meter {self.meter_number} | Units Remaining: {self.units} kWh"

        # Check if units have dropped below or equal to the threshold
        if self.units <= self.threshold and self.units > 0:
            alert_text = f"KPLC Alert: Low balance! Meter {self.meter_number} has {self.units} kWh remaining."
          send_sms_alert(alert_text)
            # send_sms_alert(alert_text)
            status_message += " | LOW BALANCE WARNING SENT!"
        elif self.units == 0.0:
            status_message = f"KPLC Alert: Meter {self.meter_number} has run out of tokens (0 kWh)!"
           send_sms_alert(status_message)

        return status_message

# Global simulator instance to be imported into app.py
meter = MeterSimulator()