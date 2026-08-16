from llm_copilot import generate_noc_report

def run_tests():
    topology = {
        "site": "NYC-HQ",
        "device": "Core-PE-Router-01",
        "interface": "GigabitEthernet0/0/1"
    }

    # Scenario A: BGP Route Instability
    bgp_telemetry = {
        "utilization_pct": 42.0,
        "latency_ms": 65.0,
        "jitter_ms": 12.0,
        "packet_loss_pct": 2.1,
        "interface_errors": 0,
        "bgp_flaps": 5,
        "ospf_changes": 1,
        "tunnel_health_pct": 95.0,
        "traffic_mbps": 420.0
    }

    print("\n" + "="*70)
    print(" SCENARIO A: TESTING BGP ROUTE INSTABILITY TELEMETRY ")
    print("="*70)
    report_a = generate_noc_report(bgp_telemetry, topology)
    print(report_a)

    # Scenario B: High Congestion Event
    congestion_telemetry = {
        "utilization_pct": 94.5,
        "latency_ms": 155.0,
        "jitter_ms": 28.0,
        "packet_loss_pct": 6.8,
        "interface_errors": 45,
        "bgp_flaps": 0,
        "ospf_changes": 0,
        "tunnel_health_pct": 100.0,
        "traffic_mbps": 945.0
    }

    print("\n" + "="*70)
    print(" SCENARIO B: TESTING PROGRESSIVE CONGESTION TELEMETRY ")
    print("="*70)
    report_b = generate_noc_report(congestion_telemetry, topology)
    print(report_b)

if __name__ == "__main__":
    run_tests()