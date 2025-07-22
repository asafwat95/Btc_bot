from flask import Flask
from main import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Hopper bot is running."

@app.route('/run')
def run():
    result = run_bot()
    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
