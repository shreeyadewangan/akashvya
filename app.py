import sys
import os
import streamlit as st
import pandas as pd
import numpy as np

# Dynamically add phase subdirectories to Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, "phase2", "ml"))
sys.path.append(os.path.join(ROOT_DIR, "phase3"))
sys.path.append(os.path.join(ROOT_DIR, "phase4"))

# Imports from individual phase packages
from predict import predict_single_sample
from rag_engine import generate_grounded_noc_report

# Streamlit Setup
st.set_page_config(
    page_title="Air-Gapped MPLS NOC Copilot",
    page_icon="📡",
    layout="wide"
)

st.markdown("""
    <style>
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SIDEBAR CONTROLLER
# -------------------------------------------------------------------
st.sidebar.title("NOC Control Center")
st.sidebar.subheader("Fault Injection Simulator")

fault_scenario = st.sidebar.selectbox(
    "Select Operating State / Fault Scenario:",
    [
        "Normal Operations",
        "Progressive Congestion",
        "BGP Route Flapping",
        "IPSec Tunnel Degradation",
        "Underlay Failure",
        "Policy Misconfiguration"
    ]
)

st.sidebar.divider()
st.sidebar.caption("🔒 **Air-Gap Status**: Active (Local Inference Only)")
st.sidebar.caption("🤖 **Engine**: Ollama (`llama3.2`)")
st.sidebar.caption("🧠 **ML Model**: Random Forest (Phase 2)")

# -------------------------------------------------------------------
# TELEMETRY GENERATION
# -------------------------------------------------------------------
def get_telemetry_for_scenario(scenario):
    np.random.seed(42)
    noise = np.random.normal(0, 0.5)
    
    if scenario == "Normal Operations":
        return {
            "utilization_pct": round(32.5 + noise, 2),
            "latency_ms": round(12.4 + noise, 2),
            "jitter_ms": round(1.2 + noise, 2),
            "packet_loss_pct": 0.0,
            "interface_errors": 0,
            "bgp_flaps": 0,
            "ospf_changes": 0,
            "tunnel_health_pct": 100.0,
            "traffic_mbps": round(325.0 + noise * 10, 2)
        }
    elif scenario == "Progressive Congestion":
        return {
            "utilization_pct": round(91.8 + noise, 2),
            "latency_ms": round(142.0 + noise * 2, 2),
            "jitter_ms": round(21.5 + noise, 2),
            "packet_loss_pct": round(5.2 + max(0, noise), 2),
            "interface_errors": int(15 + noise * 2),
            "bgp_flaps": 0,
            "ospf_changes": 0,
            "tunnel_health_pct": 100.0,
            "traffic_mbps": round(918.0 + noise * 5, 2)
        }
    elif scenario == "BGP Route Flapping":
        return {
            "utilization_pct": round(44.0 + noise, 2),
            "latency_ms": round(58.0 + noise * 3, 2),
            "jitter_ms": round(14.0 + noise, 2),
            "packet_loss_pct": round(2.1 + max(0, noise), 2),
            "interface_errors": 0,
            "bgp_flaps": 6,
            "ospf_changes": 2,
            "tunnel_health_pct": 92.0,
            "traffic_mbps": 440.0
        }
    elif scenario == "IPSec Tunnel Degradation":
        return {
            "utilization_pct": round(38.0 + noise, 2),
            "latency_ms": round(165.0 + noise * 5, 2),
            "jitter_ms": round(42.0 + noise * 2, 2),
            "packet_loss_pct": round(11.5 + max(0, noise), 2),
            "interface_errors": int(6 + noise),
            "bgp_flaps": 0,
            "ospf_changes": 0,
            "tunnel_health_pct": 28.0,
            "traffic_mbps": 304.0
        }
    elif scenario == "Underlay Failure":
        return {
            "utilization_pct": 5.0,
            "latency_ms": 350.0,
            "jitter_ms": 78.0,
            "packet_loss_pct": 65.0,
            "interface_errors": 180,
            "bgp_flaps": 4,
            "ospf_changes": 5,
            "tunnel_health_pct": 10.0,
            "traffic_mbps": 50.0
        }
    else:  # Policy Misconfiguration
        return {
            "utilization_pct": 99.5,
            "latency_ms": round(95.0 + noise, 2),
            "jitter_ms": round(18.0 + noise, 2),
            "packet_loss_pct": round(4.2 + max(0, noise), 2),
            "interface_errors": int(112 + noise * 5),
            "bgp_flaps": 0,
            "ospf_changes": 0,
            "tunnel_health_pct": 100.0,
            "traffic_mbps": 1194.0
        }

telemetry = get_telemetry_for_scenario(fault_scenario)
topology_info = {
    "site": "NYC-HQ",
    "device": "Core-PE-Router-01",
    "interface": "GigabitEthernet0/0/1"
}

# Run Phase 2 ML Prediction Pipeline
ml_prediction = predict_single_sample(telemetry)

# -------------------------------------------------------------------
# HEADER & EXECUTIVE METRICS
# -------------------------------------------------------------------
st.title("📡 Air-Gapped Predictive NOC Copilot")
st.caption("Integrated Operations Center | Phase 1 Telemetry → Phase 2 ML → Phase 4 Local RAG → Ollama")

if ml_prediction["risk_level"] == "LOW":
    st.success("🟢 **SYSTEM HEALTH NORMAL**: All signals within threshold limits.")
elif ml_prediction["risk_level"] in ["MEDIUM", "HIGH"]:
    st.warning(f"⚠️ **ELEVATED RISK**: Impending failure predicted ({ml_prediction['predicted_issue']}).")
else:
    st.error(f"🚨 **CRITICAL ALERT**: Immediate action needed for {ml_prediction['predicted_issue']}.")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Predicted Issue", ml_prediction["predicted_issue"])
m2.metric("ML Confidence", ml_prediction["confidence"])
m3.metric("Risk Score", f"{ml_prediction['risk_score']} / 100")
m4.metric("Risk Level", ml_prediction["risk_level"])
m5.metric("Time-to-Impact", ml_prediction["time_to_impact"])

st.divider()

# -------------------------------------------------------------------
# TELEMETRY CHARTS
# -------------------------------------------------------------------
st.subheader("📈 Real-Time Telemetry Signals")

chart_length = 30
time_index = pd.date_range(end=pd.Timestamp.now(), periods=chart_length, freq="1min")

base_util = np.linspace(30, telemetry["utilization_pct"], chart_length)
base_lat = np.linspace(15, telemetry["latency_ms"], chart_length)
base_loss = np.linspace(0, telemetry["packet_loss_pct"], chart_length)
base_tunnel = np.linspace(100, telemetry["tunnel_health_pct"], chart_length)

c1, c2 = st.columns(2)

with c1:
    st.markdown("**Interface Utilization (%)**")
    st.line_chart(pd.DataFrame({"Utilization (%)": base_util + np.random.normal(0, 1, chart_length)}, index=time_index))

    st.markdown("**Latency (ms)**")
    st.line_chart(pd.DataFrame({"Latency (ms)": base_lat + np.random.normal(0, 1.5, chart_length)}, index=time_index))

with c2:
    st.markdown("**Packet Loss Rate (%)**")
    st.line_chart(pd.DataFrame({"Packet Loss (%)": np.clip(base_loss + np.random.normal(0, 0.2, chart_length), 0, 100)}, index=time_index))

    st.markdown("**IPSec Tunnel Health Score (%)**")
    st.line_chart(pd.DataFrame({"Tunnel Health (%)": np.clip(base_tunnel + np.random.normal(0, 0.5, chart_length), 0, 100)}, index=time_index))

st.divider()

# -------------------------------------------------------------------
# LOCAL RAG + OLLAMA COPILOT
# -------------------------------------------------------------------
st.subheader("🤖 Local AI NOC Copilot Incident Analysis")

if st.button("🔍 Generate Grounded Copilot Diagnosis", type="primary"):
    with st.spinner("Executing Phase 4 vector search & Ollama inference..."):
        report, sources = generate_grounded_noc_report(ml_prediction, telemetry, topology_info)
        
        col_report, col_sources = st.columns([3, 1])
        
        with col_report:
            st.markdown("### Copilot Incident Report")
            st.info(report)
            
        with col_sources:
            st.markdown("### Retrieved Runbooks")
            for src in sources:
                st.success(f"📄 `{src}`")
            st.markdown("**Target Device:**")
            st.write(f"- Site: `{topology_info['site']}`")
            st.write(f"- Device: `{topology_info['device']}`")
            st.write(f"- Interface: `{topology_info['interface']}`")