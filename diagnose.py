import pickle
import os
import sys

MODEL_DIR = "model"

try:
    with open("diagnose_output.txt", "w") as f:
        f.write(f"Loading from {os.path.abspath(MODEL_DIR)}\n")
        scaler = pickle.load(open(os.path.join(MODEL_DIR, "scaler.pkl"), "rb"))
        f.write(f"Scaler type: {type(scaler)}\n")
        if hasattr(scaler, "n_features_in_"):
            f.write(f"Scaler expects {scaler.n_features_in_} features.\n")
        
        encoders = pickle.load(open(os.path.join(MODEL_DIR, "encoders.pkl"), "rb"))
        f.write(f"Encoders keys ({len(encoders)}): {list(encoders.keys())}\n")

        model = pickle.load(open(os.path.join(MODEL_DIR, "churn_model.pkl"), "rb"))
        f.write(f"Model type: {type(model)}\n")
        if hasattr(model, "n_features_in_"):
            f.write(f"Model expects {model.n_features_in_} features.\n")
except Exception as e:
    with open("diagnose_output.txt", "w") as f:
        f.write(f"Error: {e}\n")
