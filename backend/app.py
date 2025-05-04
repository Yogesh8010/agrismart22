from flask import Flask, render_template, request
import os
import pickle
import numpy as np
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- Connect to MySQL Database ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="agrismart_db"
)
cursor = db.cursor()

# --- Load Chatbot Trained Dictionary ---
with open('chatbot_model/chatbot_model.pkl', 'rb') as f:
    chatbot_model = pickle.load(f)

# --- Flask Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    result = ""
    if request.method == "POST":
        try:
            crop = request.form.get("crop")
            ph = float(request.form.get("ph"))
            nitrogen = int(request.form.get("nitrogen"))
            phosphorus = int(request.form.get("phosphorus"))
            potassium = int(request.form.get("potassium"))
            season = request.form.get("season")
            yield_val = int(request.form.get("yield"))

            # Simple rule-based example logic
            suggestion = []

            if ph < 6.0:
                suggestion.append("Soil is acidic. Apply lime.")
            elif ph > 7.5:
                suggestion.append("Soil is alkaline. Consider adding sulfur.")
            else:
                suggestion.append("Soil pH is optimal.")

            if nitrogen < 40:
                suggestion.append("Add more nitrogen.")
            if phosphorus < 30:
                suggestion.append("Increase phosphorus levels.")
            if potassium < 30:
                suggestion.append("Apply potash fertilizer.")

            result = f"For crop <strong>{crop}</strong> in <strong>{season}</strong> season with previous yield of <strong>{yield_val} kg/acre</strong>:<br>" + "<br>".join(suggestion)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("recommend.html", result=result)


# ✅ Import prediction function from model.py

@app.route("/scanner", methods=["GET", "POST"])
def scanner():
    message = ""
    confidence = 0
    filename = ""
    if request.method == "POST":
        if "crop_image" not in request.files:
            message = "No image uploaded."
        else:
            image = request.files["crop_image"]
            if image.filename == "":
                message = "No image selected."
            else:
                filename = secure_filename(image.filename)
                upload_folder = os.path.join("backend", "uploads")
                os.makedirs(upload_folder, exist_ok=True)  # ✅ Auto-create folder if missing
                path = os.path.join(upload_folder, filename)
                image.save(path)

                # Load model and predict
                message, confidence = predict_image(path)

    return render_template("scanner.html", message=message, confidence=confidence, filename=filename)




@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    reply = ""
    user_query = ""
    if request.method == "POST":
        user_query = request.form["query"].lower()

        if "hello" in user_query or "hi" in user_query:
            reply = "Hello! How can I help you with your farm today?"
        elif "fertilizer" in user_query:
            reply = "Use NPK 10:26:26 for most crops during vegetative stage."
        elif "pesticide" in user_query:
            reply = "Neem oil is organic and effective for pest control."
        elif "ph" in user_query:
            reply = "Ideal soil pH is between 6.0 and 7.5."
        elif "irrigation" in user_query:
            reply = "Drip irrigation is efficient for water usage."
        elif "thank" in user_query:
            reply = "You're welcome! Happy farming 🌾"
        else:
            reply = "I'm still learning! Try asking about fertilizer, pH, pests, or irrigation."

    return render_template("chatbot.html", reply=reply, user_query=user_query)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
