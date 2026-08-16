# IPSec Security Tunnel Runbook
Document ID: RB-SEC-004

## Problem: IPSec Tunnel Degradation / High Latency
- **Symptoms**: IPSec tunnel health score drops below 50%, increased packet loss over encrypted WAN links, crypto engine queue buildup.
- **Immediate Resolution Steps**:
  1. Check Security Association (SA) lifetime and rekeying status: `show crypto ipsec sa`.
  2. Verify WAN underlay latency and packet loss using outer header ICMP probes.
  3. Check router crypto engine CPU usage; clear stale SAs if memory exhaustion occurs: `clear crypto sa`.