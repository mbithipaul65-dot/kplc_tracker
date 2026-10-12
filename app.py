@app.route('/trigger-sms', methods=['GET', 'POST'])
def trigger_sms():
    # Execute your alert logic / SMS check function here
    # send_low_balance_alerts()
    
    # Return a short, lightweight JSON response
    return {"status": "success", "message": "Cron check completed"}, 200