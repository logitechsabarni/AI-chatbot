import os, base64
from flask import Flask, request, render_template, session
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
openai.api_key = os.getenv("OPENAI_API_KEY")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = [{"role": "system", "content": "You are a helpful assistant."}]

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        uploaded_file = request.files.get("image")

        print("🔹 Received user_input:", user_input)
        if uploaded_file and allowed_file(uploaded_file.filename):
            file_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
            base64_image = f"data:image/jpeg;base64,{file_data}"
            session["messages"].append({"role": "user", "content": "[Image uploaded]"})

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": "Describe this image."},
                            {"type": "image_url", "image_url": {"url": base64_image}}
                        ]}
                    ],
                    max_tokens=500
                ).choices[0].message["content"]
                session["messages"].append({"role": "assistant", "content": response})
                print("🔹 Bot reply (image):", response)
            except Exception as e:
                response = f"Error with image input: {e}"
                session["messages"].append({"role": "assistant", "content": response})
                print("❗️OpenAI error:", e)
        elif user_input:
            session["messages"].append({"role": "user", "content": user_input})
            try:
                bot_reply = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=session["messages"]
                ).choices[0].message["content"]
                session["messages"].append({"role": "assistant", "content": bot_reply})
                print("🔹 Bot reply (text):", bot_reply)
            except Exception as e:
                bot_reply = f"Error with text input: {e}"
                session["messages"].append({"role": "assistant", "content": bot_reply})
                print("❗️OpenAI error:", e)

    return render_template("index.html", messages=session["messages"])

@app.route("/reset")
def reset():
    session.clear()
    return "Chat history cleared!"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
