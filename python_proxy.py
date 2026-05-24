"""
VidGen — Local Python Proxy
Run this if the browser gives a CORS error.
It acts as a local middleman between your browser and the Gemini API.

Requirements:
  pip install flask flask-cors requests

Run:
  python python_proxy.py

Then open:  http://localhost:5000
"""

from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import requests, os, io

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/proxy/generate', methods=['POST'])
def proxy_generate():
    key   = request.args.get('key', '')
    model = request.json.get('model', 'veo-2.0-generate-001')
    url   = f"{GEMINI_BASE}/models/{model}:generateVideo?key={key}"
    r     = requests.post(url, json=request.json, timeout=60)
    return Response(r.content, status=r.status_code, content_type='application/json')

@app.route('/proxy/operation', methods=['GET'])
def proxy_operation():
    key  = request.args.get('key', '')
    name = request.args.get('name', '')
    url  = f"{GEMINI_BASE}/{name}?key={key}"
    r    = requests.get(url, timeout=30)
    return Response(r.content, status=r.status_code, content_type='application/json')

@app.route('/proxy/file', methods=['GET'])
def proxy_file():
    key = request.args.get('key', '')
    uri = request.args.get('uri', '')
    sep = '&' if '?' in uri else '?'
    r   = requests.get(f"{uri}{sep}key={key}", timeout=60)
    return Response(r.content, status=r.status_code,
                    content_type=r.headers.get('Content-Type','video/mp4'))

if __name__ == '__main__':
    print("\n✅ VidGen proxy running → open http://localhost:5000\n")
    app.run(debug=False, port=5000)
