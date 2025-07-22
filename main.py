from flask import Flask
from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running..."

@app.route('/run')
def run_once():
    return run_bot()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
