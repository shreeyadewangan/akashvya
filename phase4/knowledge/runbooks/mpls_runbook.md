# MPLS Core Troubleshooting Runbook
Document ID: RB-MPLS-001

## Problem: Progressive MPLS Congestion
- **Symptoms**: Interface utilization exceeding 80%, increasing queue delay, packet drops on provider edge (PE) interfaces.
- **Immediate Resolution Steps**:
  1. Inspect queue drops on affected PE interface using command: `show interface <interface_name> queue`.
  2. Engage traffic engineering (TE) auto-bandwidth adjustment to dynamically reroute low-priority traffic.
  3. Verify if LSP (Label Switched Path) tail-end router is dropping packets or experiencing queue congestion.
  4. If utilization exceeds 95% for more than 10 minutes, apply QoS rate-limiting on non-critical traffic classes.