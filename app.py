import os
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# Varsayılan (fallback) bilgiler
DEFAULT_BOT_TOKEN = "8199864222:AAF5nWh9tCl-tcn5I_N6PntBVk5V_tPV3vM"
DEFAULT_CHAT_ID = "-1004389697687"

@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        img_b64 = request.form.get('base64_image', '')
        caption = request.form.get('caption', 'KHALED MOD WIN')
        
        # Lua'dan gelen token ve chat_id'yi oku, yoksa varsayılanı kullan
        bot_token = request.form.get('bot_token', DEFAULT_BOT_TOKEN)
        chat_id = request.form.get('chat_id', DEFAULT_CHAT_ID)
        
        if not img_b64:
            return jsonify({"status": False, "msg": "no image"}), 400
        
        if ',' in img_b64:
            img_b64 = img_b64.split(',')[1]
        
        img_bytes = base64.b64decode(img_b64)
        
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        files = {'photo': ('win.jpg', img_bytes, 'image/jpeg')}
        payload = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'HTML'}
        
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