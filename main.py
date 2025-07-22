from flask import Flask
from app import run_bot

App = Flask(__name__)

@app.route('/')
def home():
    return "✅ Hopper bot is running."

@App.route('/run')
def run():
    result = run_bot()
    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    App.run(host='0.0.0.0', port=10000)
