import pandas as pd
import numpy as np
import os

# Set random seed for deterministic, reproducible telemetry generation
np.random.seed(42)

def generate_synthetic_telemetry(num_minutes=600):
    """
    Generates time-series network telemetry spanning 6 operational scenarios:
    1. Normal Operations
    2. Progressive MPLS Congestion
    3. BGP Route Instability / Flapping
    4. IPSec Tunnel Degradation
    5. Intermittent MPLS Underlay Failure
    6. Controller/Policy Misconfiguration
    """
    # 1. Setup timestamps (1-minute intervals)
    timestamps = pd.date_range(start="2026-08-16 00:00:00", periods=num_minutes, freq="1min")
    
    # 2. Divide timeline into 6 equal windows (100 minutes each)
    window_size = num_minutes // 6
    
    # Pre-allocate feature arrays
    sites = ["NYC-HQ"] * num_minutes
    devices = ["Edge-Router-01"] * num_minutes
    interfaces = ["GigabitEthernet0/0/1"] * num_minutes
    
    utilization = np.zeros(num_minutes)
    latency = np.zeros(num_minutes)
    jitter = np.zeros(num_minutes)
    packet_loss = np.zeros(num_minutes)
    interface_errors = np.zeros(num_minutes, dtype=int)
    bgp_flaps = np.zeros(num_minutes, dtype=int)
    ospf_changes = np.zeros(num_minutes, dtype=int)
    tunnel_health = np.zeros(num_minutes)
    traffic_volume = np.zeros(num_minutes)
    fault_labels = []

    for i in range(num_minutes):
        # Base gaussian noise values for realistic fluctuation
        noise = np.random.normal(0, 1)

        # SCENARIO 1: Normal Operation (Minutes 0 - 99)
        if i < window_size:
            utilization[i] = np.clip(30 + noise * 3, 10, 50)
            latency[i] = np.clip(12 + noise * 1.5, 8, 20)
            jitter[i] = np.clip(1.5 + noise * 0.3, 0.5, 3.0)
            packet_loss[i] = 0.0
            interface_errors[i] = 0
            bgp_flaps[i] = 0
            ospf_changes[i] = 0
            tunnel_health[i] = 100.0
            traffic_volume[i] = utilization[i] * 10
            fault_labels.append("Normal")

        # SCENARIO 2: Progressive MPLS Congestion (Minutes 100 - 199)
        elif i < window_size * 2:
            progress = (i - window_size) / window_size  # Linear scale 0 to 1
            utilization[i] = np.clip(40 + (progress * 55) + noise * 2, 40, 99)
            latency[i] = np.clip(15 + (progress * 120) + noise * 5, 15, 160)
            jitter[i] = np.clip(2 + (progress * 20) + noise * 2, 2, 30)
            packet_loss[i] = np.clip((progress * 6.0) + max(0, noise * 0.5), 0, 10)
            interface_errors[i] = int(np.clip(progress * 15 + noise, 0, 30))
            bgp_flaps[i] = 0
            ospf_changes[i] = 0
            tunnel_health[i] = 100.0
            traffic_volume[i] = utilization[i] * 10
            fault_labels.append("Progressive Congestion")

        # SCENARIO 3: BGP Route Flapping (Minutes 200 - 299)
        elif i < window_size * 3:
            utilization[i] = np.clip(45 + noise * 5, 30, 60)
            latency[i] = np.clip(25 + noise * 8, 15, 75)
            jitter[i] = np.clip(5 + noise * 2, 1, 15)
            packet_loss[i] = np.clip(1.5 + max(0, noise), 0, 5)
            interface_errors[i] = 0
            bgp_flaps[i] = np.random.choice([0, 1, 2, 4, 6], p=[0.3, 0.3, 0.2, 0.1, 0.1])
            ospf_changes[i] = np.random.choice([0, 1], p=[0.8, 0.2])
            tunnel_health[i] = 95.0
            traffic_volume[i] = utilization[i] * 10
            fault_labels.append("BGP Flapping")

        # SCENARIO 4: IPSec Tunnel Degradation (Minutes 300 - 399)
        elif i < window_size * 4:
            progress = (i - window_size * 3) / window_size
            utilization[i] = np.clip(35 + noise * 4, 20, 50)
            latency[i] = np.clip(40 + (progress * 90) + noise * 10, 30, 180)
            jitter[i] = np.clip(10 + (progress * 35) + noise * 4, 5, 50)
            packet_loss[i] = np.clip((progress * 12.0) + max(0, noise), 0, 20)
            interface_errors[i] = int(np.clip(progress * 5, 0, 10))
            bgp_flaps[i] = 0
            ospf_changes[i] = 0
            tunnel_health[i] = np.clip(100 - (progress * 75) + noise * 2, 15, 100)
            traffic_volume[i] = utilization[i] * 8
            fault_labels.append("IPSec Degradation")

        # SCENARIO 5: Intermittent MPLS Underlay Failure (Minutes 400 - 499)
        elif i < window_size * 5:
            # Simulate sharp periodic outages
            is_outage = (i % 15 < 5)
            utilization[i] = 5.0 if is_outage else np.clip(50 + noise * 5, 30, 70)
            latency[i] = 350.0 if is_outage else np.clip(20 + noise * 3, 15, 35)
            jitter[i] = 80.0 if is_outage else np.clip(3 + noise, 1, 6)
            packet_loss[i] = np.random.uniform(40.0, 90.0) if is_outage else 0.5
            interface_errors[i] = np.random.randint(50, 200) if is_outage else 0
            bgp_flaps[i] = np.random.randint(1, 4) if is_outage else 0
            ospf_changes[i] = np.random.randint(2, 6) if is_outage else 0
            tunnel_health[i] = 20.0 if is_outage else 90.0
            traffic_volume[i] = utilization[i] * 10
            fault_labels.append("Underlay Failure")

        # SCENARIO 6: Controller / Policy Misconfiguration (Minutes 500 - 599)
        else:
            utilization[i] = np.clip(98.0 + noise * 0.5, 95.0, 100.0)
            latency[i] = np.clip(85 + noise * 10, 60, 120)
            jitter[i] = np.clip(15 + noise * 3, 8, 25)
            packet_loss[i] = np.clip(3.5 + max(0, noise), 1.0, 8.0)
            interface_errors[i] = int(np.clip(100 + noise * 10, 50, 150))
            bgp_flaps[i] = 0
            ospf_changes[i] = 0
            tunnel_health[i] = 100.0
            traffic_volume[i] = utilization[i] * 12
            fault_labels.append("Policy Misconfiguration")

    # 3. Construct DataFrame
    df = pd.DataFrame({
        "timestamp": timestamps,
        "site": sites,
        "device": devices,
        "interface": interfaces,
        "utilization_pct": np.round(utilization, 2),
        "latency_ms": np.round(latency, 2),
        "jitter_ms": np.round(jitter, 2),
        "packet_loss_pct": np.round(packet_loss, 2),
        "interface_errors": interface_errors,
        "bgp_flaps": bgp_flaps,
        "ospf_changes": ospf_changes,
        "tunnel_health_pct": np.round(tunnel_health, 2),
        "traffic_mbps": np.round(traffic_volume, 2),
        "fault_label": fault_labels
    })
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_telemetry()
    
    # Define output directory and file path
    output_dir = "data"
    output_path = os.path.join(output_dir, "synthetic_telemetry.csv")
    
    # Automatically create the 'data' directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Successfully generated telemetry data: {output_path}")
    print(f"Dataset shape: {df.shape} (rows, columns)")
    print("\nClass Distribution:")
    print(df["fault_label"].value_counts())