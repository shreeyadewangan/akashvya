# QoS and Policy Misconfiguration Runbook
Document ID: RB-QOS-005

## Problem: Policy Misconfiguration & Traffic Drops
- **Symptoms**: Sudden saturation across all interfaces, high interface errors, dropping real-time voice/video traffic.
- **Immediate Resolution Steps**:
  1. Verify active service-policy configuration: `show policy-map interface`.
  2. Ensure strict priority queues (LLQ) are not over-subscribed or policing legitimate control plane packets.
  3. Roll back recent policy commits if configuration drift occurred within the last hour.