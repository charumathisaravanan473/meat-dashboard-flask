import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# -------------------------------
# STEP 1: Generate Synthetic Data
# -------------------------------
data = []

for _ in range(1000):
    gas = np.random.randint(30, 300)
    tds = np.random.randint(200, 1800)
    temp = np.random.randint(5, 35)
    hum = np.random.randint(40, 90)

    # Label logic
    if gas < 80 and tds < 500:
        label = 0   # Fresh
    elif gas < 150:
        label = 1   # Warning
    else:
        label = 2   # Spoiled

    data.append([gas, tds, temp, hum, label])

df = pd.DataFrame(data, columns=["gas", "tds", "temp", "hum", "label"])

# -------------------------------
# STEP 2: Prepare Data
# -------------------------------
X = df[["gas", "tds", "temp", "hum"]]
y = df["label"]

# -------------------------------
# STEP 3: Train Model
# -------------------------------
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

print("Model trained successfully!")

# -------------------------------
# STEP 4: Save Model
# -------------------------------
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")