from flask import Flask, request
import requests
import os

app = Flask(__name__)

API_KEY = "AIzaSyCmamFOtsV3qFvcSg6Rr9HptARGIy5NEf4"

@app.route("/")
def home():
    return "Zoo AI Agent is running!"

@app.route("/ask")
def ask():
    prompt = request.args.get("q")
    if not prompt:
        return "Please provide a question using ?q=your+question", 400

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return f"Unexpected response: {str(result)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)