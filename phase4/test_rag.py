import sys
import os

# Include Phase 2 ML path
sys.path.append(os.path.abspath("../phase2/ml"))
from predict import predict_single_sample
from rag_engine import generate_grounded_noc_report

def run_rag_test():
    topology = {
        "site": "NYC-HQ",
        "device": "Core-PE-Router-01",
        "interface": "GigabitEthernet0/0/1"
    }

    # High Congestion Scenario
    telemetry_input = {
        "utilization_pct": 91.2,
        "latency_ms": 138.5,
        "jitter_ms": 22.0,
        "packet_loss_pct": 5.4,
        "interface_errors": 18,
        "bgp_flaps": 0,
        "ospf_changes": 0,
        "tunnel_health_pct": 100.0,
        "traffic_mbps": 912.0
    }

    print("Step 1: Running Local ML Prediction...")
    ml_output = predict_single_sample(telemetry_input)
    print(f" -> ML Prediction: {ml_output['predicted_issue']} ({ml_output['confidence']})")

    print("\nStep 2: Performing Local RAG Retrieval + Ollama Generation...")
    report, sources = generate_grounded_noc_report(ml_output, telemetry_input, topology)

    print("\n" + "="*70)
    print(" GROUNDED NOC COPILOT REPORT (LOCAL RAG ENABLED) ")
    print("="*70)
    print(report)
    print("="*70)
    print(f"Retrieved Document Sources: {sources}")

if __name__ == "__main__":
    run_rag_test()