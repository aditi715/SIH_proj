from flask import Flask, render_template, request, jsonify
import json
from deep_translator import GoogleTranslator
def translate_text(text, src_lang, dest_lang):
    try:
        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"

app = Flask(__name__)

# Load dataset
with open("data/groundwater.json", "r", encoding="utf-8") as f:
    groundwater_data = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    lang = data.get("lang", "en")

    # Translate input if not English
    if lang != "en":
        user_message = translator.translate(user_message, src=lang, dest="en").text

    # Dummy intelligent query handling
    response = "Sorry, I could not understand. Try asking about recharge, extraction or status."

    if "status" in user_message.lower():
        response = "Groundwater status: Semi-Critical in 2023 for selected block."
    elif "recharge" in user_message.lower():
        response = "Annual recharge is 120 MCM, extraction 80 MCM."
    elif "historical" in user_message.lower():
        response = "Historical data (2015-2023) shows extraction increased by 15%."

    # Translate response back
    if lang != "en":
        response = translator.translate(response, src="en", dest=lang).text

    return jsonify({"reply": response})

@app.route("/api/data")
def get_data():
    return jsonify(groundwater_data)

if __name__ == "__main__":
    app.run(debug=True)