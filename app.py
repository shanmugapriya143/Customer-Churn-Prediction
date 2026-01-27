from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
import random

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../model")  # Corrected for deployment

class MockModel:
    def predict_proba(self, features):
        val = abs(np.sum(features)) % 1
        return [[1-val, val]]

class MockScaler:
    def transform(self, features):
        return features


try:
    model = pickle.load(open(os.path.join(MODEL_DIR, "churn_model.pkl"), "rb"))
    scaler = pickle.load(open(os.path.join(MODEL_DIR, "scaler.pkl"), "rb"))
    encoders = pickle.load(open(os.path.join(MODEL_DIR, "encoders.pkl"), "rb"))
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}. Using Mock Model.")
    model = MockModel()
    scaler = MockScaler()
    encoders = {}


@app.route("/")
def home():
    return "Customer Churn Prediction API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        result = _predict_single(data)
        return jsonify(result)
    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if file:
            import pandas as pd
            df = pd.read_csv(file)
            results = []
            for index, row in df.iterrows():
                data = row.to_dict()
                processed_row = _predict_single(data)
                processed_row['customer_id'] = str(data.get('customerID') or data.get('customer_id') or f"Row-{index+1}")
                results.append(processed_row)
            
            
            results.sort(key=lambda x: x['probability'], reverse=True)
            return jsonify(results)
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def _predict_single(data):
    try:
        norm_data = {k.lower(): v for k, v in data.items()}
        
        tenure = float(data.get("tenure") or norm_data.get("tenure") or 0)
        monthly_charges = float(data.get("MonthlyCharges") or norm_data.get("monthlycharges") or 0)
        total_charges = float(data.get("TotalCharges") or norm_data.get("totalcharges") or 0)
        senior_citizen = int(data.get("SeniorCitizen") or norm_data.get("seniorcitizen") or 0)

        numeric = [tenure, monthly_charges, total_charges, senior_citizen]
        
        categorical = []
        if encoders:
            for col, encoder in encoders.items():
                if col == "Churn": continue
                val = data.get(col) or norm_data.get(col.lower()) or "No"
                try:
                    categorical.append(encoder.transform([str(val)])[0])
                except:
                    categorical.append(0)
        
        features = np.array([numeric + categorical])
        
        if hasattr(scaler, 'transform'):
            features = scaler.transform(features)
        
        if isinstance(model, MockModel) or not hasattr(model, 'predict_proba'):
            # Heuristic for Mock
            score = 0
            if tenure < 12: score += 30
            if monthly_charges > 80: score += 20
            contract = data.get("Contract") or norm_data.get("contract") or "Month-to-month"
            if contract == "Month-to-month": score += 30
            internet = data.get("InternetService") or norm_data.get("internetservice") or "Fiber optic"
            if internet == "Fiber optic": score += 10
            
            probability = min(max(score + random.randint(-5, 5), 5), 95)
        else:
            probability = round(model.predict_proba(features)[0][1] * 100, 2)

    except Exception as e:
        print(f"Prediction logic error: {e}")
        probability = 50 

  
    reasons = []
    if float(data.get("tenure") or 0) < 6: reasons.append("New customer (Low Tenure)")
    if float(data.get("MonthlyCharges") or 0) > 70: reasons.append("High Monthly Charges")
    contract = data.get("Contract") or norm_data.get("contract") or "Month-to-month"
    if contract == "Month-to-month": reasons.append("Month-to-month Contract Risk")
    if not reasons:
        reasons.append("Macro-economic factors")

    if probability >= 70:
        risk = "Critical"
        suggestion = "Offer 20% Discount for 1-year commitment."
        tip = "Immediate account review required."
    elif probability >= 40:
        risk = "Medium"
        suggestion = "Suggest an upgrade to a better value plan."
        tip = "Send personalized satisfaction survey."
    else:
        risk = "Low"
        suggestion = "Recommend accessories or add-ons."
        tip = "Keep engaged with newsletter."

    return {
        "probability": probability,
        "risk": risk,
        "reasons": reasons,
        "suggestion": suggestion,
        "tip": tip
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

