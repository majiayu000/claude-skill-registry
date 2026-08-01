---
name: analyzing-modbus-traffic
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: analyzing-modbus-traffic
description: >-
  Capture, decode, and analyze Modbus TCP/RTU traffic for unauthorized read/write operations,
  function code abuse, and anomalous register access patterns using Wireshark, Zeek, and
  Suricata ICS protocol dissectors.
domain: cybersecurity
subdomain: ot-ics-security
tags:
  - modbus
  - ics
  - protocol-analysis
  - wireshark
  - zeek
  - suricata
  - scada
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T0801", "T0831", "T0855"]
  nist-csf: ["DE.CM-1", "DE.AE-2"]
  iec-62443: ["SR 3.5", "SR 5.2"]
  uuid: a1b2c3d4-1001-4000-a001-000000000001
---

# Analyzing Modbus Traffic

## Overview

Modbus TCP (port 502) and Modbus RTU lack authentication, encryption, and integrity
checking by design. Any host with network access can read coils, write registers, and
manipulate physical processes. Traffic analysis identifies unauthorized operations,
reconnaissance sweeps, and exploitation attempts against PLCs and RTUs.

Mode: `[MODE: BLUE]` for monitoring; `[MODE: RED]` for protocol abuse testing.

## Prerequisites

| Requirement | Details |
|---|---|
| Wireshark 4.0+ with Modbus dissector enabled | Required |
| Zeek 6.0+ with `modbus.zeek` policy script | Required |
| Suricata 7.0+ with ICS rulesets (ET Open ICS) | Required |
| Network tap or SPAN port on OT VLAN carrying Modbus traffic | Required |
| Isolated lab for write-operation testing (NEVER on production) | Required |

## Key Concepts

### Modbus Function Codes

```yaml
# Read operations (reconnaissance)
FC 01: Read Coils              # Digital outputs
FC 02: Read Discrete Inputs    # Digital inputs
FC 03: Read Holding Registers  # Analog outputs / config
FC 04: Read Input Registers    # Analog inputs / measurements

# Write operations (manipulation — HIGH RISK)
FC 05: Write Single Coil       # Toggle digital output
FC 06: Write Single Register   # Set analog output
FC 15: Write Multiple Coils    # Bulk digital write
FC 16: Write Multiple Registers # Bulk analog write

# Diagnostic (recon / abuse)
FC 08: Diagnostics             # Device status / restart
FC 43: Read Device ID (MEI)    # Vendor, product, version
```

### Wireshark Capture and Filters

```bash
# Capture Modbus traffic on OT interface
tshark -i eth1 -f "tcp port 502" -w modbus_capture.pcap -b filesize:100000

# Display filter — all Modbus
wireshark -r modbus_capture.pcap -Y "modbus"

# Filter write operations only (high-risk)
tshark -r modbus_capture.pcap -Y "modbus.func_code == 5 || modbus.func_code == 6 || modbus.func_code == 15 || modbus.func_code == 16"

# Filter by unit ID (specific PLC)
tshark -r modbus_capture.pcap -Y "modbus.unit_id == 1"

# Extract register values from read responses
tshark -r modbus_capture.pcap -Y "modbus.func_code == 3" \
  -T fields -e ip.src -e ip.dst -e modbus.unit_id -e modbus.regval_uint16

# Detect exception responses (errors / scanning artifacts)
tshark -r modbus_capture.pcap -Y "modbus.exception_code"
```

### Zeek Modbus Analysis

```bash
# Process PCAP with Modbus analyzer
zeek -r modbus_capture.pcap modbus

# Parse Modbus log for unique function codes per source
cat modbus.log | zeek-cut ts id.orig_h id.resp_h func unit_id | sort -u

# Identify write operations
cat modbus.log | zeek-cut ts id.orig_h id.resp_h func | grep -E "WRITE|FORCE"

# Count function codes per source (detect scanning)
cat modbus.log | zeek-cut id.orig_h func | sort | uniq -c | sort -rn

# Detect register read sweeps
cat modbus.log | zeek-cut id.orig_h id.resp_h func quantity | \
  awk '$4 > 100 {print "LARGE READ:", $0}'
```

### Suricata ICS Rules

```yaml
# Alert on any Modbus write to PLC network
alert tcp any any -> $ICS_NET 502 ( \
  msg:"MODBUS - Write Single Coil (FC05)"; \
  flow:established,to_server; \
  content:"|00 00|"; offset:2; depth:2; \
  content:"|05|"; offset:7; depth:1; \
  classtype:protocol-command-decode; \
  sid:4000001; rev:1; \
  metadata:mitre_attack_technique T0831;)

# Alert on Modbus device identification scan
alert tcp any any -> $ICS_NET 502 ( \
  msg:"MODBUS - Read Device ID (FC43/MEI)"; \
  flow:established,to_server; \
  content:"|00 00|"; offset:2; depth:2; \
  content:"|2b|"; offset:7; depth:1; \
  threshold:type both, track by_src, count 3, seconds 60; \
  sid:4000002; rev:1;)

# Alert on Modbus exception flood (scan indicator)
alert tcp $ICS_NET 502 -> any any ( \
  msg:"MODBUS - Exception Response Flood"; \
  flow:established,to_client; \
  content:"|80|"; offset:7; depth:1; \
  byte_test:1,>=,0x80,7; \
  threshold:type both, track by_dst, count 10, seconds 30; \
  sid:4000003; rev:1;)
```

## Workflow

### Step 1: Baseline Normal Traffic

```bash
# Capture 24h of normal operations
tcpdump -i eth1 -f "tcp port 502" -w baseline_modbus.pcap -G 86400 -W 1

# Generate baseline profile
zeek -r baseline_modbus.pcap modbus
cat modbus.log | zeek-cut id.orig_h id.resp_h func unit_id | sort -u > baseline_pairs.txt

# Document expected function codes per source
echo "=== Baseline Modbus Communication Pairs ==="
cat baseline_pairs.txt
```

### Step 2: Detect Anomalies

```bash
# Compare live traffic against baseline
zeek -r live_capture.pcap modbus
cat modbus.log | zeek-cut id.orig_h id.resp_h func unit_id | sort -u > current_pairs.txt
diff baseline_pairs.txt current_pairs.txt

# Flag new sources communicating with PLCs
comm -13 <(cut -f1 baseline_pairs.txt | sort -u) \
         <(cut -f1 current_pairs.txt | sort -u)
```

### Step 3: Investigate Write Operations

```bash
# Extract all write commands with timestamps
tshark -r suspect_capture.pcap \
  -Y "modbus.func_code >= 5 && modbus.func_code <= 16" \
  -T fields -e frame.time -e ip.src -e ip.dst \
  -e modbus.func_code -e modbus.reference_num -e modbus.regval_uint16
```

## Verification

- [ ] Modbus traffic captured from correct SPAN/tap point
- [ ] Baseline communication pairs documented
- [ ] Write operations monitored and alerted
- [ ] Suricata ICS rules deployed and tested against PCAP
- [ ] Zeek modbus.log integrated into SIEM
- [ ] Exception response patterns analyzed for scanning activity
- [ ] Unauthorized source IPs flagged for investigation

## Detection Opportunities

- New Modbus sources not in baseline → unauthorized device or lateral movement
- Write function codes from HMI/historian (should be read-only) → compromised system
- Rapid sequential reads across register ranges → reconnaissance sweep
- Exception response floods → active scanning with invalid unit IDs
- Register value changes outside process thresholds → process manipulation

```yaml
title: Modbus Traffic Detection
id: 810f2018-9111-4709-8ef2-43c2594f5d31
status: experimental
description: Detects suspicious activity related to analyzing modbus traffic techniques in ot ics security context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*analyzing*modbus*"
  condition: selection
level: medium
tags:
  - attack.t0801
  - attack.t0831
  - attack.t0855
  - attack.lateral_movement
falsepositives:
  - Industrial control system maintenance by authorized engineering staff
```

## References

- Modbus Application Protocol Specification v1.1b3
- [Wireshark Modbus Dissector](https://wiki.wireshark.org/Modbus)
- NIST SP 800-82 Rev 3: Guide to OT Security
- IEC 62443-3-3 SR 3.5: Input Validation
