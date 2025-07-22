from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import whisper
import tempfile

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

# ==========================
# ✅ Root Route for Render Health Check
# ==========================
@app.route("/")
def home():
    return jsonify({"message": "Smart AI Chatbot is running!"})

# ✅ Ping Route for Frontend Health Check
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200

# ==========================
# 💬 Chat Endpoint
# ==========================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# 🎙️ Voice Input Endpoint
# ==========================
@app.route("/voice", methods=["POST"])
def voice():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        audio_file = request.files["audio"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            audio_path = temp_audio.name
            audio_file.save(audio_path)

        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        text = result["text"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        answer = response["choices"][0]["message"]["content"]

        os.remove(audio_path)
        return jsonify({"transcription": text, "response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# 🖼️ Image Input Endpoint
# ==========================
@app.route("/image", methods=["POST"])
def image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files["image"]
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)

        if not text.strip():
            return jsonify({"response": "No text found in image."})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"extracted": text, "response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# 🚀 Run App (for Render)
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
