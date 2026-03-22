<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-dns-tunneling
description: >-
  Detect and analyze DNS-based data exfiltration and command-and-control tunneling
  using Zeek DNS analytics, Suricata rules, entropy analysis, and frequency-based
  anomaly detection on query patterns.
domain: cybersecurity
subdomain: network-security
tags:
  - dns
  - tunneling
  - exfiltration
  - c2
  - zeek
  - suricata
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1071.004", "T1048.003", "T1572"]
  nist-csf: ["DE.CM-1", "DE.AE-3", "DE.AE-5"]
  uuid: a1b2c3d4-1002-4a00-b002-f00d00000002
---

# Detecting DNS Tunneling

## Overview

DNS tunneling encodes arbitrary data in DNS queries and responses to bypass firewalls
and exfiltrate data. Detection relies on identifying statistical anomalies in query
length, entropy, subdomain depth, query volume per domain, and TXT record abuse.
This skill covers passive detection with Zeek, active detection with Suricata, and
entropy-based analysis techniques.

Mode: `[MODE: BLUE]` for detection; `[MODE: PURPLE]` for coverage validation.

## Prerequisites

| Requirement | Details |
|---|---|
| Zeek 6.0+ with DNS protocol analyzer | Required |
| Suricata 7.0+ with DNS app-layer parser | Required |
| DNS logs (passive DNS or tap on recursive resolver) | Required |
| Python 3.10+ with `math` and `collections` for entropy analysis | Required |
| Known DNS tunnel tools for testing | iodine, dnscat2, dns2tcp |

## Key Concepts

### DNS Tunnel Indicators

```yaml
# Statistical indicators of DNS tunneling
high_entropy_subdomain: >3.5 bits per character in subdomain labels
long_query_names: >50 characters total FQDN length
deep_subdomains: >4 label levels (a.b.c.d.evil.com)
high_txt_volume: Abnormal TXT record query/response ratio
single_domain_volume: >100 queries/min to single domain
non_standard_types: NULL, PRIVATE, or TXT heavy query mix
```

### Suricata DNS Tunnel Detection Rules

```
# Detect long DNS queries (possible tunneling)
alert dns $HOME_NET any -> any any ( \
  msg:"DNS Tunnel - excessively long query name"; \
  dns.query; content:"."; offset:50; \
  threshold:type both, track by_src, count 10, seconds 60; \
  classtype:bad-unknown; \
  sid:3001001; rev:1; \
  metadata:mitre_attack_technique T1071.004;)

# Detect high volume TXT queries to single domain
alert dns $HOME_NET any -> any any ( \
  msg:"DNS Tunnel - high volume TXT queries"; \
  dns.query; content:"."; \
  dns.opcode:0; \
  threshold:type both, track by_src, count 50, seconds 300; \
  classtype:bad-unknown; \
  sid:3001002; rev:1;)

# Detect known DNS tunnel tool signatures
alert dns $HOME_NET any -> any any ( \
  msg:"DNS Tunnel - iodine handshake detected"; \
  dns.query; content:"."; \
  content:"v"; offset:0; depth:1; \
  pcre:"/^v[0-9a-f]{4}\./"; \
  sid:3001003; rev:1;)
```

### Zeek DNS Entropy Analysis

```zeek
# dns-tunnel-detect.zeek — entropy-based DNS tunnel detection
@load base/protocols/dns

module DNSTunnel;

export {
    redef enum Notice::Type += {
        DNS_Tunnel_Suspected,
        DNS_Tunnel_High_Volume,
    };

    const entropy_threshold = 3.5 &redef;
    const query_len_threshold = 52 &redef;
}

function calc_entropy(s: string): double {
    local freq: table[string] of count = {};
    local n = |s|;
    for ( i in s ) {
        if ( s[i] !in freq )
            freq[s[i]] = 0;
        ++freq[s[i]];
    }
    local ent = 0.0;
    for ( c, cnt in freq ) {
        local p = cnt * 1.0 / n;
        ent -= p * log2(p);
    }
    return ent;
}

event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count) {
    if ( |query| > query_len_threshold ) {
        local ent = calc_entropy(query);
        if ( ent > entropy_threshold ) {
            NOTICE([$note=DNS_Tunnel_Suspected,
                    $msg=fmt("High entropy DNS query: %s (entropy=%.2f)", query, ent),
                    $conn=c,
                    $identifier=cat(c$id$orig_h, query)]);
        }
    }
}
```

### Command-Line Analysis

```bash
# Extract DNS queries from Zeek logs and compute statistics
zeek-cut query < dns.log | awk '{print length, $0}' | sort -rn | head -20

# Find domains with highest query volume
zeek-cut query < dns.log | rev | cut -d. -f1-2 | rev | sort | uniq -c | sort -rn | head -20

# Identify TXT record abuse
zeek-cut qtype_name query < dns.log | grep "TXT" | cut -f2 | sort | uniq -c | sort -rn

# Capture DNS traffic for offline analysis
tcpdump -i eth0 -w dns_capture.pcap 'port 53'
suricata -r dns_capture.pcap -S /etc/suricata/rules/dns-tunnel.rules -l /tmp/dns_test/
```

## Workflow

### Step 1: Baseline Normal DNS Behavior

Establish query length distribution, entropy baseline, and per-domain volume for your network.

### Step 2: Deploy Detection Rules

Load Suricata rules and Zeek scripts targeting tunnel indicators.

### Step 3: Analyze Anomalies

```bash
# Check Suricata alerts for DNS tunnel signatures
cat /var/log/suricata/eve.json | \
  jq 'select(.event_type=="alert" and .alert.signature | contains("DNS Tunnel"))'

# Review Zeek notices
cat notice.log | zeek-cut note msg
```

### Step 4: Validate with Known Tools

```bash
# Test with iodine (lab only)
iodine -f -r 10.0.0.53 tunnel.lab.local

# Test with dnscat2
dnscat2 --dns server=10.0.0.53,domain=tunnel.lab.local
```

### Step 5: Tune and Suppress

Whitelist legitimate long-query services (CDNs, DKIM, SPF lookups) in suppress lists.

## Detection

```yaml
title: Dns Tunneling Detection
id: 27bfd9b7-a2a5-4337-86dd-59a521d14642
status: experimental
description: Detects suspicious activity related to detecting dns tunneling techniques in network security context
logsource:
  category: firewall
  product: linux
detection:
  selection:
    Action: blocked
  condition: selection
level: medium
tags:
  - attack.t1071.004
  - attack.t1048.003
  - attack.t1572
  - attack.command_and_control
falsepositives:
  - Network monitoring tools performing scheduled connectivity checks
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Dns Tunneling Detection | linux/firewall | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1071.004, T1048.003, T1572 |

## Verification

- [ ] Entropy threshold detects iodine/dnscat2 traffic
- [ ] Query length rule fires on tunnel payloads
- [ ] TXT volume rule catches data exfil patterns
- [ ] Legitimate CDN/DKIM queries do not trigger false positives
- [ ] Detection latency under 60 seconds for active tunnels
- [ ] Alerts forwarded to SIEM with source IP context

## References

- [Zeek DNS Protocol Analyzer](https://docs.zeek.org/en/current/scripts/base/protocols/dns/)
- SANS ISC: Detecting DNS Tunneling
- MITRE ATT&CK T1071.004 — Application Layer Protocol: DNS
- [Suricata DNS Keywords](https://docs.suricata.io/en/latest/rules/dns-keywords.html)
