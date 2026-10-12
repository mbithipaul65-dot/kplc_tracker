from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "KPLC Tracker Web Service active."

@app.route('/trigger-sms', methods=['GET', 'POST'])
def trigger_sms():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)