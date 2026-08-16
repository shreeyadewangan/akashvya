# Core Network Topology Overview
Document ID: TOP-001

## Node Architecture
- **Site NYC-HQ**:
  - Device: `Core-PE-Router-01`
  - Interfaces: `GigabitEthernet0/0/1` (Primary MPLS Trunk to Service Provider), `GigabitEthernet0/0/2` (Secondary IPSec Backup WAN).
  - SLA Thresholds: Max Latency = 50ms, Max Packet Loss = 1.0%, Max Utilization = 85%.