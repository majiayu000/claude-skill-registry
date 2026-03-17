---
name: debug-thread-network
description: Debug and diagnose Thread mesh networks and OpenThread Border Routers. Use when troubleshooting Thread connectivity, analyzing Router Advertisements, testing IPv6 reachability to Thread devices, inspecting Thread Network Data, or diagnosing Border Router configuration issues.
---

# Debug Thread Network

Comprehensive toolkit for debugging Thread mesh networks and OpenThread Border Routers.

## Quick Start

Run the main diagnostic script to test connectivity and gather network information:

```bash
scripts/test_thread_connectivity.sh <border-router-ip>
```

Example:
```bash
scripts/test_thread_connectivity.sh 192.168.50.104
```

## Core Scripts

### 1. Thread Connectivity Test (`scripts/test_thread_connectivity.sh`)

**Purpose**: Comprehensive connectivity test for Thread Border Router

**Usage**:
```bash
scripts/test_thread_connectivity.sh <border-router-ip>
```

**What it tests**:
- ICMP reachability (ping)
- HTTP REST API accessibility
- IPv6 Router Advertisement reception
- Thread network status
- Border Router configuration

**Output**: Summary report with pass/fail status for each test

### 2. IPv6 Diagnostics (`scripts/ipv6_diagnostics.sh`)

**Purpose**: Gather complete IPv6 configuration and routing information

**Usage**:
```bash
scripts/ipv6_diagnostics.sh [interface]
```

**Collects**:
- IPv6 addresses on all interfaces
- IPv6 routing table
- Neighbor Discovery cache
- Router Advertisement prefixes
- Default routers

**Output**: Formatted diagnostic report

### 3. Border Router API Query (`scripts/query_otbr_api.sh`)

**Purpose**: Query OpenThread Border Router REST API endpoints

**Usage**:
```bash
scripts/query_otbr_api.sh <border-router-ip> [port]
```

**Endpoints queried**:
- `/get_properties` - Network properties
- `/node_information` - Node details
- `/topology` - Network topology
- `/diagnostics` - Full diagnostic info
- `/node/dataset/active` - Thread credentials

**Output**: JSON responses from each endpoint

### 4. Thread Network Data Decoder (`scripts/decode_thread_netdata.py`)

**Purpose**: Decode Thread Network Data hex string into human-readable format

**Usage**:
```bash
scripts/decode_thread_netdata.py <netdata-hex>
```

Or pipe from API:
```bash
curl -s http://192.168.50.104/diagnostics | \
  jq -r '.[0].NetworkData' | \
  scripts/decode_thread_netdata.py
```

**Decodes**:
- Prefix TLVs with IPv6 prefixes
- Border Router sub-TLVs with flags
- Has Route sub-TLVs
- Service TLVs

**Output**: Structured TLV analysis with prefix flags

### 5. RA Packet Analyzer (`scripts/analyze_ra_packet.sh`)

**Purpose**: Capture and analyze Router Advertisement packets

**Usage**:
```bash
sudo scripts/analyze_ra_packet.sh <interface>
```

**Captures**:
- Router Advertisement packets
- Prefix Information Options (PIO)
- Route Information Options (RIO)
- Router lifetime and flags

**Output**: Parsed RA packet details

## Common Workflows

### Workflow 1: Initial Border Router Discovery

When you know the network but not the border router IP:

```bash
# Scan for Thread Border Routers on network
scripts/scan_for_otbr.sh 192.168.1
```

### Workflow 2: Full Network Diagnostic

When troubleshooting connectivity issues:

```bash
# Step 1: Test connectivity
scripts/test_thread_connectivity.sh 192.168.50.104

# Step 2: Check IPv6 configuration
scripts/ipv6_diagnostics.sh en0

# Step 3: Query Border Router
scripts/query_otbr_api.sh 192.168.50.104

# Step 4: Analyze Router Advertisements
sudo scripts/analyze_ra_packet.sh en0
```

### Workflow 3: Decode Thread Network Configuration

When analyzing Thread network prefixes and routes:

```bash
# Get Network Data and decode
curl -s http://192.168.50.104/diagnostics | \
  jq -r '.[0].NetworkData' | \
  scripts/decode_thread_netdata.py
```

### Workflow 4: Test OMR Address Reachability

When verifying external connectivity to Thread devices:

```bash
# Get OMR addresses from border router
OMR_ADDR=$(curl -s http://192.168.50.104/diagnostics | \
  jq -r '.[0].IP6AddressList[] | select(startswith("fd03"))')

# Test connectivity
ping6 -c 3 $OMR_ADDR

# Test HTTP over IPv6
curl -s "http://[$OMR_ADDR]/get_properties" | jq
```

## Reference Documentation

### Thread Address Types

For detailed explanation of Thread IPv6 addressing, see [references/thread-addressing.md](references/thread-addressing.md)

### Router Advertisement Analysis

For RA packet structure and interpretation, see [references/router-advertisements.md](references/router-advertisements.md)

### OpenThread Border Router API

For complete API documentation, see [references/otbr-api.md](references/otbr-api.md)

## Troubleshooting Guide

### Border Router Not Responding

1. Check network connectivity: `ping <border-router-ip>`
2. Verify correct IP address
3. Check if REST API is enabled (ESP32 uses port 80, ot-br-posix uses 8081)
4. Verify firewall settings

### No IPv6 Connectivity to Thread Devices

1. Check if Router Advertisements are being received: `ndp -p`
2. Verify OMR prefix in routing table: `netstat -rn -f inet6 | grep fd`
3. Check if IPv6 forwarding is blocking RAs: `sysctl net.inet6.ip6.forwarding`
4. Verify border router is advertising routes

### Cannot Reach Mesh-Local Addresses

This is expected behavior. Mesh-local addresses (fd65::/64) are only reachable from within the Thread mesh. External devices must use OMR addresses instead.

### Router Advertisement Not Captured

1. Verify interface name: `ifconfig`
2. Check for sudo permissions
3. Wait longer (RAs sent every 30-300 seconds)
4. Use Wireshark filter: `icmpv6.type == 134`

## Platform-Specific Notes

### macOS

- Use `ndp` commands for neighbor discovery
- IPv6 forwarding check: `sysctl net.inet6.ip6.forwarding`
- Interface typically `en0` for Wi-Fi, `en1` for Ethernet

### Linux

- Use `ip -6` commands instead of `ndp`
- IPv6 forwarding check: `sysctl net.ipv6.conf.all.forwarding`
- Accept RA setting: `sysctl net.ipv6.conf.eth0.accept_ra`

## Best Practices

1. **Always start with connectivity test** - Run `test_thread_connectivity.sh` first
2. **Save diagnostic output** - Redirect script output to files for analysis
3. **Compare before/after** - Run diagnostics before and after configuration changes
4. **Check both sides** - Verify configuration on both infrastructure and Thread mesh
5. **Use IPv6 bracket notation** - When using IPv6 in URLs: `http://[fd03::1]/`
