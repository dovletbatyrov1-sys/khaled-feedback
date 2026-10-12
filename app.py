import os
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# ===== SENIN BILGILERIN =====
BOT_TOKEN = "8681748088:AAEoZ2uJJmy-94oUQBA1MnXPxeZUSpRKgiM"
CHAT_ID = "-1003709911230"
# ============================

@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        img_b64 = request.form.get('base64_image', '')
        caption = request.form.get('caption', 'KHALED MOD WIN')
        
        if not img_b64:
            return jsonify({"status": False, "msg": "no image"}), 400
        
        if ',' in img_b64:
            img_b64 = img_b64.split(',')[1]
        
        img_bytes = base64.b64decode(img_b64)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': ('win.jpg', img_bytes, 'image/jpeg')}
        payload = {'chat_id': CHAT_ID, 'caption': caption, 'parse_mode': 'HTML'}
        
        r = requests.post(url, files=files, data=payload, timeout=30)
        
        if r.status_code == 200:
            return jsonify({"status": True, "msg": "sent"})
        else:
            return jsonify({"status": False, "msg": r.text}), 500
    except Exception as e:
        return jsonify({"status": False, "msg": str(e)}), 500

@app.route('/')
def home():
    return "KHALED Feedback Server Online"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)