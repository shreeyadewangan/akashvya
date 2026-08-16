# BGP Route Instability Runbook
Document ID: RB-BGP-002

## Problem: BGP Route Flapping
- **Symptoms**: Frequent BGP state transitions between ESTABLISHED and IDLE, high CPU usage on route processor, packet loss during convergence.
- **Immediate Resolution Steps**:
  1. Check BGP neighbor state and flap history: `show ip bgp summary`.
  2. Inspect underlying physical link error counters (CRC, drops) to rule out physical layer instability.
  3. Verify MTU size mismatch across peering interfaces.
  4. Enable BGP Route Flap Dampening if external peer flaps repeatedly (>3 flaps within 10 minutes).