import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_telemetry(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: File not found at {csv_path}. Run generate_telemetry.py first.")
        return

    # Load dataset
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set visualization style
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

    # 1. Utilization Plot
    sns.lineplot(data=df, x='timestamp', y='utilization_pct', ax=axes[0], color='blue', label='Utilization (%)')
    axes[0].set_ylabel('Utilization (%)')
    axes[0].set_title('Air-Gapped Telemetry Simulation: Key Network Indicators Across Faults')

    # 2. Latency & Jitter Plot
    sns.lineplot(data=df, x='timestamp', y='latency_ms', ax=axes[1], color='red', label='Latency (ms)')
    sns.lineplot(data=df, x='timestamp', y='jitter_ms', ax=axes[1], color='orange', label='Jitter (ms)')
    axes[1].set_ylabel('Time (ms)')

    # 3. Packet Loss & Tunnel Health
    sns.lineplot(data=df, x='timestamp', y='packet_loss_pct', ax=axes[2], color='purple', label='Packet Loss (%)')
    sns.lineplot(data=df, x='timestamp', y='tunnel_health_pct', ax=axes[2], color='green', label='Tunnel Health (%)')
    axes[2].set_ylabel('Percentage (%)')

    # 4. Routing Events (BGP / OSPF)
    sns.lineplot(data=df, x='timestamp', y='bgp_flaps', ax=axes[3], color='magenta', label='BGP Flaps')
    sns.lineplot(data=df, x='timestamp', y='ospf_changes', ax=axes[3], color='brown', label='OSPF Changes')
    axes[3].set_ylabel('Event Count')
    axes[3].set_xlabel('Timestamp')

    plt.tight_layout()
    output_image = os.path.join("data", "telemetry_visualization.png")
    plt.savefig(output_image, dpi=300)
    print(f"Saved telemetry plot to: {output_image}")
    plt.show()

if __name__ == "__main__":
    plot_telemetry(os.path.join("data", "synthetic_telemetry.csv"))