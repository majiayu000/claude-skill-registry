---
name: Device Inspection
description: Execute comprehensive L1-L4 network device inspection. Use when user asks to "inspect all devices", "run comprehensive health check", "full network audit", or needs systematic L1-L4 analysis across multiple devices.
version: 1.0.0

# OLAV Extended Fields
intent: inspect
complexity: medium

# Output Configuration
output:
  format: markdown
  language: auto
  sections:
    - summary
    - details
    - recommendations
---

# Device Inspection - Comprehensive L1-L4

## Applicable Scenarios
- Comprehensive network health assessment (all test devices)
- Full stack network inspection (L1-L4)
- Network baseline establishment and verification
- Pre-maintenance complete audit

## Identification Signals
User questions contain: "inspect", "comprehensive", "full check", "all devices", "L1-L4"

## Execution Strategy
1. **List all devices in 'test' group** using list_devices(group="test")
2. **For each device, execute comprehensive inspection** covering L1 (Physical), L2 (Data Link), L3 (Network), L4 (Transport)
3. **Generate consolidated report** with device-by-device status
4. **Flag anomalies** across all layers

## Comprehensive Inspection Template (L1-L4)

### L1 - Physical Layer
- [ ] `show version` (Device model, serial, uptime)
- [ ] `show inventory` (Hardware modules, power supplies, fans)
- [ ] `show environment all` (Temperature, power status, fan status)
- [ ] `show interfaces` (Physical port states, media types)

### L2 - Data Link Layer
- [ ] `show vlan brief` (VLAN configuration and status)
- [ ] `show spanning-tree summary` (STP topology, root bridge)
- [ ] `show spanning-tree detail` (Port states, costs)
- [ ] `show cdp neighbors` (CDP neighbor discovery)
- [ ] `show mac address-table` (MAC table status, count)

### L3 - Network Layer
- [ ] `show ip route summary` (Route count and protocol summary)
- [ ] `show ip ospf neighbor` (OSPF neighbor status)
- [ ] `show ip ospf interface brief` (OSPF interface states)
- [ ] `show ip bgp summary` (BGP neighbor status)
- [ ] `show ip bgp vpnv4 all summary` (VPNv4 status if applicable)

### L4 - Transport Layer & Services
- [ ] `show tcp brief` (TCP session count)
- [ ] `show processes cpu` (CPU utilization and process breakdown)
- [ ] `show memory statistics` (Memory usage across memory pools)
- [ ] `show interfaces counters errors` (Error counters on all interfaces)
- [ ] `show interfaces counters dropped` (Dropped packet counters)

## Report Format

### Executive Summary
```
📋 test Network Comprehensive Inspection Report
Inspection Time: 2026-01-08 14:30:00
Total Devices: 8
Overall Status: 2 devices OK, 5 devices WARNING, 1 device CRITICAL

Device Summary:
├─ R1 (10.1.1.1) ✅ OK - L1:✅ L2:✅ L3:✅ L4:✅
├─ R2 (10.1.1.2) ⚠️ WARNING - L1:⚠️ L2:✅ L3:✅ L4:✅
├─ R3 (10.1.1.3) ⚠️ WARNING - L1:✅ L2:✅ L3:✅ L4:⚠️
├─ R4 (10.1.1.4) ⚠️ WARNING - L1:⚠️ L2:✅ L3:✅ L4:✅
├─ S1 (10.2.1.1) ✅ OK - L1:✅ L2:✅ L3:✅ L4:✅
├─ S2 (10.2.1.2) ⚠️ WARNING - L1:✅ L2:⚠️ L3:✅ L4:✅
├─ A1 (10.3.1.1) ⚠️ WARNING - L1:✅ L2:✅ L3:⚠️ L4:✅
└─ A2 (10.3.1.2) ❌ CRITICAL - L1:❌ L2:✅ L3:✅ L4:⚠️
```

### Device-by-Device Detailed Results
Each device gets a full L1-L4 report:
```
╔══════════════════════════════════════════════════════╗
║ Device: R1 (10.1.1.1) - Core Router                 ║
║ Platform: Cisco IOS XE                              ║
║ Status: ✅ ALL SYSTEMS OK                           ║
╚══════════════════════════════════════════════════════╝

Layer 1 (Physical):
  CPU Utilization: 15% (5min avg) ✅
  Memory Usage: 62% (avaitestle: 8.2GB) ✅
  Temperature: 42°C (threshold: 70°C) ✅
  Power Supplies: 2/2 ACTIVE ✅
  Fans: 6/6 SPINNING ✅

Layer 2 (Data Link):
  VLAN Count: 45 ✅
  Active Ports: 48/48 UP ✅
  STP Root: YES (Priority: 24576) ✅
  LLDP Neighbors: 4 discovered ✅

Layer 3 (Network):
  IPv4 Routes: 2,847 routes ✅
  OSPF Neighbors: 3 FULL ✅
  BGP Neighbors: 2 ESTABLISHED ✅
  Routing Errors: 0 ✅

Layer 4 (Transport):
  Interface Errors: 0 (24h avg) ✅
  Dropped Packets: 0 (24h avg) ✅
  TCP Sessions: 45 active ✅
  UDP Flows: 128 active ✅
```

### Anomaly Details & Recommendations
```
⚠️ WARNING: R2 - Temperature trending high
Current: 58°C | Trend: +2°C/hour | Threshold: 70°C
Recommendation: Monitor closely, ensure adequate airflow

❌ CRITICAL: A2 - Power supply #1 degraded
Status: FAILED | Uptime before failure: 847 days
Recommendation: Replace PSU immediately before other PSU fails
```

### Consolidated Findings
```
Critical Issues (Immediate Action):
1. A2 Power Supply Failure - Replace PSU
2. A1 BGP Neighbor Flapping - Check link stability

Warnings (Monitor):
1. R2 Temperature trending up - Check cooling
2. S2 STP Bridge Priority - May need rebalancing
3. R3 Interface FCS Errors increasing - Check optics

Informational (Good Status):
- All core devices operating normally
- test network stable and well-managed
```

## Multi-Device Inspection Process

1. **Device Collection**: Query all devices in 'test' group
2. **Parallel Execution**: Execute inspection template on each device
3. **Data Aggregation**: Collect and normalize results
4. **Analysis**: Compare against health baselines
5. **Reporting**: Generate comprehensive multi-device report with:
   - Overall network health score
   - Device-by-device status
   - Cross-layer dependency analysis
   - Consolidated recommendations

## Output Artifact
```
reports/test-comprehensive-inspection-20260108-143000.md
├─ Executive Summary Dashboard
├─ Device Status Matrix
├─ Layer-by-Layer Details (8 devices × 4 layers = 32 sections)
├─ Anomaly Analysis
├─ Historical Comparison (vs. previous inspection)
└─ Recommendations & Actions
```
