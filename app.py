from flask import Flask, jsonify
from send_sms import check_and_send_sms  # or your main execution function

app = Flask(__name__)

@app.route('/trigger-sms', methods=['GET', 'POST'])
def trigger_sms():
    try:
        # Execute your core logic (SMS / Telegram check)
        check_and_send_sms()
        
        # Return a minimal, lightweight JSON response (< 100 bytes)
        return jsonify({
            "status": "success",
            "message": "Cron execution completed."
        }), 200

    except Exception as e:
        # Return a concise error payload if something breaks
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500