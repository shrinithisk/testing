import os
import urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "SecureFlow AI Test Application running!"
    })

@app.route('/fetch')
def fetch_url():
    target = request.args.get('url', 'https://httpbin.org/get')
    # Vulnerable to SSRF/LFI if unvalidated
    try:
        response = urllib.request.urlopen(target)
        content = response.read().decode('utf-8')
        return jsonify({"url": target, "data": content[:200]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
