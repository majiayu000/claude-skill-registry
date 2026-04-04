---
name: Quick Query
description: Execute simple network status queries that require 1-2 commands. Use when user asks to "check device status", "show interface", "query routing table", "display BGP neighbors", or needs simple read-only information retrieval.
version: 1.0.0

# OLAV Extended Fields
intent: query
complexity: simple

# Output Configuration
output:
  format: markdown
  language: auto
  sections:
    - summary
---

# Quick Query

## Applicable Scenarios
- Query device interface status
- Query routing table
- Query ARP/MAC table
- Simple status checks

## Identification Signals
User questions contain: "check", "see", "status", "is it normal", "show", "display"

## Execution Strategy
1. **No write_todos needed**, execute directly
2. Parse device aliases from knowledge/aliases.md
3. Use search_capabilities to find suitable commands
4. Execute 1-2 commands
5. Keep results concise, return only key information

## Examples

### Interface Status Query
**Trigger**: "R1 Gi0/1 status", "show interface status"
**Command**: `show interfaces GigabitEthernet0/1` or `show interface brief`
**Extract**: up/down, speed, error counts

### IP/MAC Location
**Trigger**: "What port is 10.1.1.100 on", "Find this MAC"
**Process**:
1. `show arp | include 10.1.1.100` → Get MAC
2. `show mac address-table address <mac>` → Get port

### Version Information
**Trigger**: "Device version", "show version"
**Command**: `show version` or `display version`
**Extract**: Device model, software version, uptime

### CPU/Memory Query
**Trigger**: "CPU usage", "Memory status"
**Command**: `show processes cpu history`, `show memory statistics`
**Extract**: Current usage, trends

## Workflow
```
User query → Parse alias → search_capabilities → nornir_execute → Format output
```

## Output Format
Keep it concise, highlight key information:
```
R1 (10.1.1.1) - Interface Status
├─ Gi0/1: up, line protocol up
│  ├─ Input: 1000 Mbps, 0 errors
│  └─ Output: 1000 Mbps, 0 errors
├─ Gi0/2: administratively down
└─ Gi0/3: up, line protocol up
   └─ CRC errors: 0
```

## Notes
- Only execute read-only commands
- No configuration changes
- Output must be clear and concise
- If device doesn't exist, confirm with list_devices first
