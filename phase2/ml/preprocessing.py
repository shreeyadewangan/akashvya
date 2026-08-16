import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

FEATURE_COLUMNS = [
    "utilization_pct", "latency_ms", "jitter_ms", "packet_loss_pct",
    "interface_errors", "bgp_flaps", "ospf_changes", "tunnel_health_pct", "traffic_mbps"
]

TARGET_COLUMN = "fault_label"

def load_and_preprocess_data(csv_path="../../phase1/data/synthetic_telemetry.csv"):
    """
    Loads raw network telemetry, drops non-predictive metadata (data leakage prevention),
    encodes labels, and splits into train/test sets.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Telemetry dataset not found at {csv_path}. Complete Phase 1 first.")

    df = pd.read_csv(csv_path)

    # Features (X) and Target (y)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # Encode categorical text labels into integer IDs
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Train/Test Split (80% train, 20% test) with stratification to preserve class ratios
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
    )

    return X_train, X_test, y_train, y_test, label_encoder, FEATURE_COLUMNS

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, encoder, features = load_and_preprocess_data()
    print("Dataset successfully preprocessed without data leakage.")
    print(f"Features utilized ({len(features)}): {features}")
    print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")