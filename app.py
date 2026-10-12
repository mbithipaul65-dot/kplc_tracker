from flask import Flask, jsonify
from send_sms import send_meter_sms  # Imports your actual SMS function

app = Flask(__name__)

@app.route('/')
def home():
    return "KPLC Tracker Web Service active."

@app.route('/trigger-sms', methods=['GET', 'POST'])
def trigger_sms():
    try:
        # Calls your actual SMS dispatch function
        send_meter_sms()
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)