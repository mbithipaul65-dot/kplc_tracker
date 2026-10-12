from flask import Flask, jsonify

# Import your actual SMS or meter reading function here
# from your_sms_module import send_meter_sms  

app = Flask(__name__)

@app.route('/')
def home():
    return "KPLC Tracker Web Service active."

@app.route('/trigger-sms', methods=['GET', 'POST'])
def trigger_sms():
    try:
        # Call your SMS dispatch/simulation function here:
        # send_meter_sms()
        
        return jsonify({"status": "OK", "message": "SMS triggered successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)