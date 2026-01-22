from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# =========================
# LOAD MODEL FILES
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

model = pickle.load(open(os.path.join(MODEL_DIR, "churn_model.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(MODEL_DIR, "scaler.pkl"), "rb"))
encoders = pickle.load(open(os.path.join(MODEL_DIR, "encoders.pkl"), "rb"))

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return "Customer Churn Prediction API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Encode categorical values
    encoded = []
    for col, le in encoders.items():
        value = data[col]
        encoded.append(le.transform([value])[0])

    # Numeric values
    numeric = [
        data["tenure"],
        data["MonthlyCharges"],
        data["TotalCharges"],
        data["SeniorCitizen"]
    ]

    features = np.array([numeric + encoded])
    features = scaler.transform(features)

    prob = model.predict_proba(features)[0][1] * 100
    prob = round(prob, 2)

    # =========================
    # BUSINESS LOGIC
    # =========================
    reasons = []
    if data["tenure"] < 6:
        reasons.append("Customer is new with low tenure")
    if data["MonthlyCharges"] > 70:
        reasons.append("High monthly charges")
    if data["Contract"] == "Month-to-month":
        reasons.append("No long-term contract")

    if prob >= 70:
        suggestion = "Offer 20% discount & convert to yearly plan"
        tip = "High-risk customer – immediate retention needed"
    elif prob >= 40:
        suggestion = "Provide loyalty rewards"
        tip = "Medium risk – engage with offers"
    else:
        suggestion = "Upsell premium services"
        tip = "Customer is stable"

    return jsonify({
        "probability": prob,
        "reasons": reasons,
        "suggestion": suggestion,
        "tip": tip
    })

if __name__ == "__main__":
    app.run(debug=True)
