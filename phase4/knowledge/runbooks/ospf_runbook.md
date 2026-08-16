# OSPF Adjacency Troubleshooting Runbook
Document ID: RB-OSPF-003

## Problem: OSPF Neighbor Adjacency Changes
- **Symptoms**: OSPF neighbor state dropping from FULL to INIT or DOWN, loss of internal routes.
- **Immediate Resolution Steps**:
  1. Verify hello and dead timer consistency across adjacent routers: `show ip ospf interface`.
  2. Check for unicast/multicast traffic blocking caused by firewall or ACL misconfigurations.
  3. Inspect interface errors and packet loss on the interconnecting link.