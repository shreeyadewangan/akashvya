import numpy as np

def calculate_risk_metrics(predicted_label, probability, telemetry_dict):
    """
    Translates prediction output and telemetry parameters into actionable Risk Level
    and Time-to-Impact (TTI) estimates.
    """
    confidence_pct = round(float(probability) * 100, 2)
    
    # Base risk score derived from prediction confidence
    if predicted_label == "Normal":
        risk_score = round(max(0, (1.0 - probability) * 40), 2)
    else:
        risk_score = round(probability * 70, 2)

    # Telemetry severity multipliers
    if telemetry_dict.get("packet_loss_pct", 0) > 5.0 or telemetry_dict.get("latency_ms", 0) > 150:
        risk_score += 15.0
    if telemetry_dict.get("bgp_flaps", 0) > 2 or telemetry_dict.get("interface_errors", 0) > 50:
        risk_score += 15.0

    risk_score = float(np.clip(risk_score, 0, 100))

    # Categorize Risk Level
    if risk_score < 30:
        risk_level = "LOW"
    elif risk_score < 60:
        risk_level = "MEDIUM"
    elif risk_score < 85:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    # Time-to-Impact Estimation Heuristic
    if predicted_label == "Normal":
        tti = "N/A (Operational)"
    elif predicted_label in ["Underlay Failure", "Policy Misconfiguration"]:
        tti = "0 - 5 Minutes (Immediate Impact)"
    elif predicted_label == "BGP Flapping":
        tti = "5 - 15 Minutes (Route Degradation Active)"
    elif predicted_label == "IPSec Degradation":
        tti = "15 - 30 Minutes (Security Overhead Degradation)"
    elif predicted_label == "Progressive Congestion":
        # Estimate TTI dynamically based on remaining buffer headroom
        utilization = telemetry_dict.get("utilization_pct", 50)
        remaining_headroom = max(1, 100 - utilization)
        estimated_minutes = max(5, int(remaining_headroom * 0.8))
        tti = f"{estimated_minutes} - {estimated_minutes + 15} Minutes (Impending Saturation)"
    else:
        tti = "10 - 20 Minutes"

    return {
        "predicted_issue": predicted_label,
        "confidence": f"{confidence_pct}%",
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "time_to_impact": tti
    }