<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: network-security
description: >-
  Network security including firewall management, IDS/IPS configuration (Suricata/Snort),
  network segmentation and micro-segmentation, VPN security, DNS security (DoH/DoT/DNSSEC),
  zero trust network access (ZTNA), network traffic analysis, DDoS mitigation,
  Wi-Fi security assessment, and network forensics.
domain: cybersecurity
subdomain: network-security
tags:
  - firewall
  - ids-ips
  - suricata
  - network-segmentation
  - vpn
  - dns-security
  - ztna
  - ddos
  - pcap-analysis
  - zeek
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1046", "T1090", "T1095", "T1571", "T1572"]
  nist-csf: ["PR.AC-5", "PR.DS-2", "PR.PT-4", "DE.CM-1"]
  frameworks: ["CIS Controls v8 12-13", "NIST SP 800-41", "NIST SP 800-207"]
---

# Network Security

## When to Use

Activate when the operator asks about firewall rules, IDS/IPS, network segmentation,
VPN hardening, DNS security, ZTNA, network monitoring, DDoS mitigation, PCAP analysis,
or Zeek/Suricata deployment.

Mode: `[MODE: BLUE]` for network defense; `[MODE: ARCHITECT]` for network design; `[MODE: INCIDENT]` for network forensics.

## Quick Reference

| Control | Tool / Command | Purpose |
|---------|---------------|---------|
| Firewall audit | `iptables -L -n -v --line-numbers` | Rule review |
| Suricata test | `suricata -T -c /etc/suricata/suricata.yaml` | Config validation |
| PCAP analysis | `zeek -r capture.pcap local` | Protocol analysis |
| DNS monitoring | `zeek -r capture.pcap dns.zeek \| zeek-cut query answers` | DNS logging |
| Network scan | `nmap -sS -sV -O -A -p- target` | Asset discovery |
| Bandwidth monitor | `vnstat -i eth0 -l` | Traffic baseline |
| TLS inspection | `sslyze --regular target.com:443` | Certificate audit |
| WiFi audit | `airodump-ng wlan0mon` | Wireless survey |

## Workflow

### 1. Network Segmentation Design

```
Zone Architecture:
├── DMZ (public-facing services)
│   ├── Web servers, reverse proxies, WAF
│   └── Rules: Internet → DMZ (443/80 only), DMZ → Internal (specific APIs)
├── Internal/Corporate
│   ├── User workstations, corporate apps
│   └── Rules: Internal → Internet via proxy, Internal → DMZ limited
├── Server/Data Center
│   ├── Databases, application servers, file servers
│   └── Rules: No direct internet, accessed from Internal via specific ports
├── Management
│   ├── Jump hosts, SIEM, backup, patch management
│   └── Rules: Mgmt → All (SSH/RDP/SNMP), No inbound except from PAW
├── OT/SCADA (if applicable)
│   ├── PLCs, HMIs, historians
│   └── Rules: Air-gapped or data diode from IT
└── Guest/IoT
    ├── Guest Wi-Fi, IoT devices, BYOD
    └── Rules: Internet only, no access to any internal zone

Micro-segmentation:
├── Label-based policies (Cilium, Calico for K8s)
├── Per-workload firewall rules
├── East-west traffic inspection
└── Default deny between all workloads
```

### 2. IDS/IPS (Suricata)

```yaml
# /etc/suricata/suricata.yaml key settings
af-packet:
  - interface: eth0
    threads: auto
    cluster-type: cluster_flow

rule-files:
  - suricata.rules
  - /var/lib/suricata/rules/et-open/*.rules

outputs:
  - eve-log:
      enabled: yes
      types:
        - alert
        - dns
        - http
        - tls
        - flow

# Custom rule examples:
# Detect reverse shell
alert tcp $HOME_NET any -> $EXTERNAL_NET any (msg:"Reverse shell detected"; flow:established,to_server; content:"/bin/sh"; content:"-i"; sid:1000001; rev:1;)

# Detect DNS tunneling
alert dns any any -> any any (msg:"DNS tunneling - high entropy query"; dns.query; content:"|00|"; pcre:"/^[a-z0-9]{30,}\./i"; sid:1000002; rev:1;)

# Detect Cobalt Strike default cert
alert tls any any -> any any (msg:"Cobalt Strike default TLS cert"; tls.cert_subject; content:"Major Cobalt Strike"; sid:1000003; rev:1;)
```

### 3. DNS Security

```bash
# DNSSEC validation check
dig @8.8.8.8 example.com +dnssec +short
delv @8.8.8.8 example.com

# DNS-over-HTTPS (DoH) configuration
# Unbound resolver with DoH upstream
server:
  tls-cert-bundle: /etc/ssl/certs/ca-certificates.crt
forward-zone:
  name: "."
  forward-tls-upstream: yes
  forward-addr: 1.1.1.1@853#cloudflare-dns.com
  forward-addr: 1.0.0.1@853#cloudflare-dns.com

# DNS sinkholing for threat intel
# Add malicious domains to DNS blackhole
echo "local-zone: \"malware-c2.com\" redirect" >> /etc/unbound/unbound.conf
echo "local-data: \"malware-c2.com A 0.0.0.0\"" >> /etc/unbound/unbound.conf

# DNS query logging for threat hunting
# Zeek dns.log analysis
cat dns.log | zeek-cut query | sort | uniq -c | sort -rn | head -50
# Look for: high frequency queries, long domain names, TXT record abuse
```

### 4. Zero Trust Network Access (ZTNA)

```
ZTNA principles:
├── No implicit trust based on network location
├── Every access request authenticated + authorized + encrypted
├── Micro-perimeter around each application (not network segment)
├── Continuous verification (not just at connection time)
└── Least privilege access per session

Components:
├── Identity-aware proxy (BeyondCorp model)
├── Software-defined perimeter (SDP)
├── Device trust posture (compliance, patch level, EDR status)
├── Application-level access (not network-level VPN)
└── Continuous risk assessment during session

Migration from VPN to ZTNA:
1. Inventory all applications accessed via VPN
2. Deploy identity-aware proxy for web applications first
3. Implement device trust verification
4. Migrate non-web apps to SDP/ZTNA broker
5. Decommission traditional VPN (last)
```

### 5. Network Forensics

```bash
# PCAP capture for investigation
tcpdump -i eth0 -w evidence.pcap -C 100M -Z root host $SUSPECT_IP

# Zeek analysis
zeek -r evidence.pcap local
# Review: conn.log, dns.log, http.log, ssl.log, files.log

# Extract files from PCAP
zeek -r evidence.pcap extract-all-files.zeek
# Files saved to extract_files/ directory

# Network flow analysis
nfdump -r nfcapd.* -s srcip/bytes -n 20  # Top talkers
nfdump -r nfcapd.* -s dstport/flows -n 20  # Top destination ports

# TLS certificate analysis
zeek-cut -d ts id.orig_h id.resp_h server_name < ssl.log | sort -u
```

## Verification

- [ ] Network segmentation enforced (DMZ, internal, management zones)
- [ ] IDS/IPS deployed on critical network boundaries
- [ ] Default deny firewall policies on all zones
- [ ] DNS security configured (DNSSEC validation, DoH/DoT)
- [ ] VPN/ZTNA with MFA for all remote access
- [ ] Network traffic logging centralized to SIEM
- [ ] DDoS mitigation plan tested
- [ ] Wireless networks audited (WPA3, rogue AP detection)
