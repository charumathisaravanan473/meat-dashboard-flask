from flask import Flask, jsonify, render_template
import random
from datetime import datetime
import joblib

app = Flask(__name__)

# -------------------------------
# LOAD ML MODEL
# -------------------------------
model = joblib.load("model.pkl")

# -------------------------------
# GENERATE SENSOR DATA
# -------------------------------
def get_data():
    return {
        "gas": random.randint(40, 250),
        "tds": random.randint(200, 1800),
        "temp": random.randint(5, 35),
        "hum": random.randint(40, 90)
    }

# -------------------------------
# ML PREDICTION FUNCTION
# -------------------------------
def predict(data):
    input_data = [[
        data["gas"],
        data["tds"],
        data["temp"],
        data["hum"]
    ]]

    pred = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    confidence = max(proba)

    if pred == 0:
        label = "Fresh"
    elif pred == 1:
        label = "Warning"
    else:
        label = "Spoiled"

    return label, round(confidence * 100, 2)

# -------------------------------
# ROUTES
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    d = get_data()

    label, confidence = predict(d)

    return jsonify({
        **d,
        "status": label,
        "confidence": confidence,
        "time": datetime.now().strftime("%H:%M:%S")
    })

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)