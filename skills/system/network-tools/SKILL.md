---
name: network-tools
description: Linux network tools and diagnostics
version: 1.0.0
author: terminal-skills
tags: [linux, network, diagnosis, netstat, ss, curl]
---

# Network Tools and Diagnostics

## Overview
Linux network diagnostics, port scanning, traffic analysis and other tool usage skills.

## Network Configuration

### View Configuration
```bash
# IP address
ip addr
ip a
ifconfig                            # Legacy command

# Routing table
ip route
route -n
netstat -rn

# DNS configuration
cat /etc/resolv.conf
systemd-resolve --status
```

### Configure Network
```bash
# Temporary IP configuration
ip addr add 192.168.1.100/24 dev eth0
ip addr del 192.168.1.100/24 dev eth0

# Enable/Disable interface
ip link set eth0 up
ip link set eth0 down

# Add route
ip route add 10.0.0.0/8 via 192.168.1.1
ip route del 10.0.0.0/8
```

## Connectivity Testing

### ping
```bash
ping hostname
ping -c 4 hostname                  # Send 4 packets
ping -i 0.2 hostname                # 0.2 second interval
ping -s 1000 hostname               # Specify packet size
```

### traceroute
```bash
traceroute hostname
traceroute -n hostname              # Don't resolve hostnames
traceroute -T hostname              # Use TCP
mtr hostname                        # Real-time trace
```

### DNS Query
```bash
nslookup hostname
dig hostname
dig +short hostname
dig @8.8.8.8 hostname               # Specify DNS server
host hostname
```

## Ports and Connections

### ss Command (Recommended)
```bash
# Listening ports
ss -tlnp                            # TCP listening
ss -ulnp                            # UDP listening
ss -tlnp | grep :80

# All connections
ss -tanp                            # TCP connections
ss -s                               # Statistics

# Filter
ss -t state established
ss -t dst 192.168.1.1
ss -t sport = :80
```

### netstat Command
```bash
netstat -tlnp                       # TCP listening
netstat -ulnp                       # UDP listening
netstat -anp                        # All connections
netstat -s                          # Statistics
```

### lsof Network
```bash
lsof -i                             # All network connections
lsof -i :80                         # Specific port
lsof -i tcp                         # TCP connections
lsof -i @192.168.1.1                # Specific host
```

## HTTP Tools

### curl
```bash
# Basic request
curl http://example.com
curl -I http://example.com          # Headers only
curl -v http://example.com          # Verbose output

# POST request
curl -X POST -d "data=value" http://example.com
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://example.com

# Download
curl -O http://example.com/file.zip
curl -o output.zip http://example.com/file.zip

# Authentication
curl -u user:pass http://example.com
curl -H "Authorization: Bearer token" http://example.com
```

### wget
```bash
wget http://example.com/file.zip
wget -c http://example.com/file.zip # Resume download
wget -r http://example.com          # Recursive download
wget --mirror http://example.com    # Mirror site
```

## Packet Capture

### tcpdump
```bash
# Basic capture
tcpdump -i eth0
tcpdump -i any

# Filter
tcpdump -i eth0 port 80
tcpdump -i eth0 host 192.168.1.1
tcpdump -i eth0 'tcp port 80 and host 192.168.1.1'

# Save/Read
tcpdump -i eth0 -w capture.pcap
tcpdump -r capture.pcap

# Display content
tcpdump -i eth0 -A port 80          # ASCII
tcpdump -i eth0 -X port 80          # Hexadecimal
```

### Traffic Monitoring
```bash
# Real-time traffic
iftop
iftop -i eth0

# By process
nethogs
nethogs eth0

# Bandwidth test
iperf3 -s                           # Server
iperf3 -c server_ip                 # Client
```

## Common Scenarios

### Scenario 1: Troubleshoot Port Usage
```bash
# Check port usage
ss -tlnp | grep :8080
lsof -i :8080

# Find process and handle
kill -9 PID
# Or
fuser -k 8080/tcp
```

### Scenario 2: Test Service Connectivity
```bash
# TCP port test
nc -zv hostname 80
telnet hostname 80

# HTTP service test
curl -I http://hostname
curl -w "HTTP Code: %{http_code}\nTime: %{time_total}s\n" -o /dev/null -s http://hostname
```

### Scenario 3: Network Performance Diagnosis
```bash
# Latency test
ping -c 100 hostname | tail -1

# Route analysis
mtr --report hostname

# Bandwidth test
iperf3 -c server -t 30
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Network unreachable | `ping`, `traceroute`, check routing |
| DNS resolution failed | `dig`, `nslookup`, check resolv.conf |
| Port unreachable | `ss -tlnp`, check firewall |
| Connection timeout | `mtr`, `tcpdump` packet capture |
| Insufficient bandwidth | `iftop`, `iperf3` test |
