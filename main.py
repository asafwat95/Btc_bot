from flask import Flask
from threading import Thread
from time import sleep
from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running..."

@app.route('/run')
def run_once():
    return run_bot()

# Looping thread
def auto_run():
    while True:
        run_bot()
        sleep(60)  # كل دقيقة

if __name__ == '__main__':
    Thread(target=auto_run, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
