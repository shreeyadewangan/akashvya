import os
import joblib
import pandas as pd
from risk_engine import calculate_risk_metrics

# Determine absolute path to the directory containing this script (phase2/ml)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

def predict_single_sample(telemetry_dict):
    """
    Generates inference and risk estimates for an incoming telemetry observation.
    Uses dynamic file paths to find model artifacts regardless of working directory.
    """
    model_path = os.path.join(MODEL_DIR, "rf_model.joblib")
    encoder_path = os.path.join(MODEL_DIR, "label_encoder.joblib")
    features_path = os.path.join(MODEL_DIR, "feature_names.joblib")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Train the model in phase2/ml first.")

    model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)
    feature_names = joblib.load(features_path)

    # Convert telemetry dictionary into DataFrame with aligned feature order
    input_df = pd.DataFrame([telemetry_dict])[feature_names]

    # Model inference
    probabilities = model.predict_proba(input_df)[0]
    predicted_class_idx = probabilities.argmax()
    predicted_label = label_encoder.inverse_transform([predicted_class_idx])[0]
    confidence_score = probabilities[predicted_class_idx]

    # Pass through risk engine
    result = calculate_risk_metrics(predicted_label, confidence_score, telemetry_dict)
    return result

if __name__ == "__main__":
    sample_telemetry = {
        "utilization_pct": 88.5,
        "latency_ms": 142.0,
        "jitter_ms": 18.2,
        "packet_loss_pct": 4.5,
        "interface_errors": 12,
        "bgp_flaps": 0,
        "ospf_changes": 0,
        "tunnel_health_pct": 100.0,
        "traffic_mbps": 885.0
    }

    prediction = predict_single_sample(sample_telemetry)
    print("\nSample Network Telemetry Prediction:")
    for k, v in prediction.items():
        print(f" - {k.replace('_', ' ').title()}: {v}")