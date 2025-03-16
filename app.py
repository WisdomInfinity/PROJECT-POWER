from flask import Flask, request, jsonify
import requests
from sympy import symbols, Eq, solve

app = Flask(__name__)

#DEEPSEEK AND GOOGLE API
AI_API_KEY = "sk-75cdd1e921af455cb43ef7177bf14cce"
GOOGLE_SEARCH_ENGINE_ID = "AIzaSyDM_4QMdNSgZYUelR2jlqZd28onrlHEhXo"

#DEEPSEEK API CODE
def get_ai_response(user_message):
    headers = {"Authorization": f"Bearer {AI_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": user_message}]}
    response = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error")

#GOOGLE API CODE
def get_web_search_results(query):
    params = {"key": GOOGLE_SEARCH_API_KEY, "cx": GOOGLE_SEARCH_ENGINE_ID, "q": query}
    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params).json()
    return response.get("items", [{}])[0].get("snippet", "No relevant search results found.")


#Handle Incoming Requests
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()

    if "generate an image" in user_message:
        prompt = user_message.replace("generate an image of", "").strip()
        return jsonify({"reply": generate_image(prompt)})

    elif "solve" in user_message or "integrate" in user_message:
        return jsonify({"reply": get_math_solution(user_message)})

    elif "search" in user_message:
        return jsonify({"reply": get_web_search_results(user_message)})

    else:
        return jsonify({"reply": get_ai_response(user_message)})

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio_file = request.files["file"]
    return jsonify({"reply": transcribe_audio(audio_file)})

if __name__ == "__main__":
    app.run(debug=True)


    
