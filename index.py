import os
from flask import Flask
from tele_info import get_info

app = Flask(__name__)

@app.route('/')
def home():
    return "بوت تيليجرام يعمل بنجاح!"

# إذا أردت إضافة نقطة لتفعيل البوت
@app.route('/start')
def start_bot():
    os.system("python3 tele_info.py &")  # تشغيل كود tele_info.py
    return "تم تشغيل البوت بنجاح."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
