import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Meat Quality Dashboard", layout="wide")

# ------------------ UI STYLE ------------------
st.markdown("""
<style>
.stMetric {
    background-color: #111;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("🥩 Smart Meat Quality Monitoring Dashboard")

# ------------------ SIDEBAR ------------------
st.sidebar.header("System Status")
status = st.sidebar.selectbox("Device Status", ["Online", "Offline"])

# ------------------ SENSOR DATA ------------------
def get_sensor_data():
    return {
        "MQ135 (Gas ppm)": random.randint(40, 250),
        "VOC Index": round(random.uniform(0.2, 1.0), 2),
        "TDS (ppm)": random.randint(200, 1800),
        "Temperature (°C)": random.randint(5, 35),
        "Humidity (%)": random.randint(40, 90),
        "Color Index": round(random.uniform(0.5, 3.5), 2)
    }

# ------------------ CLASSIFICATION ------------------
def classify(data):
    if data["MQ135 (Gas ppm)"] < 80 and data["TDS (ppm)"] < 500:
        return "Fresh"
    elif data["MQ135 (Gas ppm)"] < 150:
        return "Warning"
    else:
        return "Spoiled"

# ------------------ GET DATA ------------------
data = get_sensor_data()
label = classify(data)

# ------------------ METRICS ------------------
st.markdown("## 📊 Sensor Readings")

col1, col2, col3 = st.columns(3)
col1.metric("Gas (MQ135)", data["MQ135 (Gas ppm)"])
col2.metric("TDS", data["TDS (ppm)"])
col3.metric("Temperature", data["Temperature (°C)"])

col4, col5, col6 = st.columns(3)
col4.metric("VOC Index", data["VOC Index"])
col5.metric("Humidity", data["Humidity (%)"])
col6.metric("Color Index", data["Color Index"])

# ------------------ STATUS ------------------
st.markdown("## 🔍 Meat Quality Status")

if label == "Fresh":
    st.success("✅ Fresh Meat")
elif label == "Warning":
    st.warning("⚠️ Warning Condition")
else:
    st.error("🚨 Spoiled Meat Detected!")

# ------------------ RISK SCORE ------------------
risk_score = int((data["MQ135 (Gas ppm)"] / 300) * 100)

st.markdown("## 🎯 Risk Score")
st.progress(risk_score)
st.write(f"Risk Level: {risk_score}%")

# ------------------ AI EXPLANATION ------------------
st.markdown("## 🧠 AI Explanation")

if label == "Fresh":
    st.info("Low gas levels and low TDS indicate fresh meat.")
elif label == "Warning":
    st.warning("Moderate gas and TDS levels suggest early spoilage.")
else:
    st.error("High gas concentration and TDS indicate advanced spoilage.")

# ------------------ SPOILAGE PREDICTION ------------------
st.markdown("## 🔮 Spoilage Prediction")

if label == "Fresh":
    st.success("Estimated spoilage in 24-36 hours")
elif label == "Warning":
    st.warning("Estimated spoilage in 6-12 hours")
else:
    st.error("Already spoiled!")

# ------------------ SAFETY ZONE ------------------
st.markdown("## 🌡️ Safety Indicator")

if risk_score < 40:
    st.success("Safe Zone")
elif risk_score < 70:
    st.warning("Caution Zone")
else:
    st.error("Danger Zone")

# ------------------ SENSOR CONTRIBUTION ------------------
st.markdown("## 📊 Sensor Contribution")

importance = {
    "Gas (MQ135)": 31,
    "VOC": 25,
    "TDS": 18,
    "Color": 15,
    "Temp": 7,
    "Humidity": 4
}

st.bar_chart(importance)

# ------------------ TIMESTAMP ------------------
st.markdown("## ⏱️ Last Updated")
st.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ------------------ DEVICE INFO ------------------
st.markdown("## 📍 Device Info")
st.write("Device ID: ESP32-001")
st.write("Location: Cold Storage Unit A")

# ------------------ IMAGE ------------------
st.markdown("## 📷 Live Meat Image")
st.image("https://via.placeholder.com/500", caption="ESP32-CAM Feed (Replace later)")

# ------------------ GRAPH ------------------
st.markdown("## 📈 Sensor Trends")

history = [get_sensor_data() for _ in range(10)]
df = pd.DataFrame(history)

st.line_chart(df)

# ------------------ INDIVIDUAL GRAPHS ------------------
st.markdown("## 📊 Individual Sensor Graphs")

colA, colB = st.columns(2)

with colA:
    st.line_chart(df[["MQ135 (Gas ppm)"]])
    st.line_chart(df[["TDS (ppm)"]])

with colB:
    st.line_chart(df[["Temperature (°C)"]])
    st.line_chart(df[["Humidity (%)"]])

# ------------------ HISTORICAL ANALYSIS ------------------
st.markdown("## 📊 Historical Summary")
st.write(df.describe())

# ------------------ DOWNLOAD ------------------
st.markdown("## 📥 Download Data")

current_df = pd.DataFrame([data])

st.download_button(
    label="Download Latest Data",
    data=current_df.to_csv(index=False),
    file_name="sensor_data.csv",
    mime="text/csv"
)

# ------------------ SOS ALERT ------------------
if label == "Spoiled":
    st.error("🚨 SOS ALERT SENT TO AUTHORITY (Simulated)")

# ------------------ AUTO REFRESH ------------------
time.sleep(2)
st.rerun()