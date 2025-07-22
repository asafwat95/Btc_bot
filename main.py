from flask import Flask
from bot import run_bot, send_last_id_telegram

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running..."

@app.route('/run')
def run_once():
    return run_bot()

@app.route('/send_last_id')
def send_last_id():
    send_last_id_telegram()
    return "✅ last_id sent to Telegram!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
