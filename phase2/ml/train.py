import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from preprocessing import load_and_preprocess_data

def train_model():
    """Trains Random Forest Classifier and persists model artifacts."""
    print("Loading preprocessed telemetry...")
    X_train, X_test, y_train, y_test, label_encoder, features = load_and_preprocess_data()

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    # Create directory for models
    os.makedirs("models", exist_ok=True)
    
    # Save artifacts
    joblib.dump(model, "models/rf_model.joblib")
    joblib.dump(label_encoder, "models/label_encoder.joblib")
    joblib.dump(features, "models/feature_names.joblib")

    print("Model training complete. Persisted artifacts to 'ml/models/'.")

if __name__ == "__main__":
    train_model()