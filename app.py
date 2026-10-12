from flask import Flask, render_template, request, jsonify
# import other modules (like your database or SMS sender)

# 1. Initialize Flask FIRST
app = Flask(__name__)

# 2. THEN define your routes using @app.route
@app.route('/trigger-sms', methods=['GET', 'POST'])
def trigger_sms():
    # Your trigger logic here
    return {"status": "success", "message": "Cron check completed"}, 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)