import os

import africastalking
from flask import Flask

app = Flask(__name__)

# Initialize Africa's Talking SDK
username = os.getenv("AFRICASTALKING_USERNAME", "sandbox")
api_key = os.getenv("AFRICASTALKING_API_KEY")

africastalking.initialize(username, api_key)
sms = africastalking.SMS


def check_and_send_sms():
  """Your existing KPLC tracking logic goes here."""
  recipients = ["+2547XXXXXXXX"]  # Replace/retrieve your phone number
  message = "KPLC Tracker Alert: Power status updated!"

  try:
    response = sms.send(message, recipients)
    print("Africa's Talking Response:", response)
    return f"SMS Sent successfully! Response: {response}"
  except Exception as e:
    print("Error sending SMS:", str(e))
    return f"Failed to send SMS: {str(e)}"


@app.route("/")
def home():
  # Triggers the check whenever the web service URL is visited
  result = check_and_send_sms()
  return f"KPLC Tracker Web Service active. Status: {result}"


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)