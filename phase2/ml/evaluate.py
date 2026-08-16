import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from preprocessing import load_and_preprocess_data

def evaluate_pipeline():
    """Evaluates ML model performance across standard metrics and FPR."""
    # Load dataset & saved model
    X_train, X_test, y_train, y_test, label_encoder, _ = load_and_preprocess_data()
    model = joblib.load("models/rf_model.joblib")

    # Generate predictions
    y_pred = model.predict(X_test)
    class_names = label_encoder.classes_

    print("\n" + "="*60)
    print("               MODEL PERFORMANCE REPORT               ")
    print("="*60 + "\n")

    # Detailed Classification Report (Precision, Recall, F1-Score)
    report = classification_report(y_test, y_pred, target_names=class_names)
    print(report)

    # Calculate False Positive Rate (FPR) per class
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
    print(cm_df)

    print("\nFalse Positive Rates (FPR) Per Category:")
    for i, category in enumerate(class_names):
        fp = cm[:, i].sum() - cm[i, i]
        tn = cm.sum() - (cm[i, :].sum() + cm[:, i].sum() - cm[i, i])
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        print(f" - {category}: {fpr:.4f} ({fpr*100:.2f}%)")
    print("="*60)

if __name__ == "__main__":
    evaluate_pipeline()