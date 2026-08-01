---
name: performing-tls-analysis
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-tls-analysis
description: >-
  Analyze TLS/SSL configurations, certificates, cipher suites, and handshakes for security weaknesses, expired certificates, and malicious C2 indicators using sslyze, testssl.sh, and Wireshark.
domain: cybersecurity
subdomain: network-security
tags:
  - tls
  - ssl
  - certificate
  - cipher-suite
  - sslyze
  - testssl
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1573", "T1071.001"]
  nist-csf: ["PR.DS-2", "DE.CM-1"]
  uuid: 9b84b272-ea07-46f5-8961-35cde834eb88
---

# Performing TLS Analysis

## Overview

TLS analysis is critical for both offensive and defensive security. Defensively, it identifies
weak configurations, expired certificates, and protocol downgrade risks. For threat hunting,
TLS metadata (JA3/JA3S fingerprints, certificate anomalies, SNI mismatches) reveals C2 channels
and malicious infrastructure without decrypting traffic.

Mode: `[MODE: BLUE]` for configuration audit; `[MODE: INCIDENT]` for threat hunting via TLS metadata.

## Prerequisites

| Requirement | Details |
|---|---|
| sslyze or testssl.sh for active scanning | Required |
| Wireshark/tshark for passive TLS analysis | Required |
| Zeek for JA3/JA3S fingerprint extraction | Required |
| OpenSSL CLI for certificate inspection | Required |
| Network tap or PCAP for passive analysis | Required |

## Key Concepts

### TLS Configuration Audit

```bash
# sslyze comprehensive scan
sslyze --regular target.com:443

# testssl.sh — detailed TLS analysis
testssl.sh --wide --color 3 target.com:443

# OpenSSL manual checks
# Check certificate chain
openssl s_client -connect target.com:443 -showcerts </dev/null 2>/dev/null

# Check specific protocol support
openssl s_client -connect target.com:443 -tls1_2 </dev/null 2>/dev/null
openssl s_client -connect target.com:443 -tls1_3 </dev/null 2>/dev/null

# Check cipher suites
nmap --script ssl-enum-ciphers -p 443 target.com
```

### JA3/JA3S Fingerprinting

```bash
# JA3 — TLS client fingerprint (identifies malware families)
# Computed from: TLS version, cipher suites, extensions, elliptic curves, EC point formats

# Zeek JA3 extraction
zeek -r traffic.pcap /opt/zeek/share/zeek/policy/protocols/ssl/ja3.zeek
cat ssl.log | zeek-cut ja3 ja3s server_name

# Known malicious JA3 hashes:
# Cobalt Strike: a0e9f5d64349fb13191bc781f81f42e1
# Metasploit Meterpreter: 5d65ea3fb1d4aa7d826733d2f2bf4e48
# Trickbot: 6734f37431670b3ab4292b8f60f29984
```

### Wireshark TLS Filters

```
# TLS handshake analysis
tls.handshake.type == 1          # Client Hello
tls.handshake.type == 2          # Server Hello
tls.handshake.type == 11         # Certificate
tls.handshake.type == 12         # Server Key Exchange

# Weak cipher detection
tls.handshake.ciphersuite == 0x000a  # TLS_RSA_WITH_3DES_EDE_CBC_SHA
tls.handshake.ciphersuite == 0x002f  # TLS_RSA_WITH_AES_128_CBC_SHA

# Certificate analysis
x509sat.CountryName == ""        # Missing country (self-signed indicator)
tls.handshake.extensions.supported_version == 0x0301  # TLS 1.0

# SNI inspection
tls.handshake.extensions_server_name contains "suspicious"
```

### Suricata TLS Rules

```yaml
# Detect self-signed certificate (C2 indicator)
alert tls any any -> any any (msg:"Self-signed TLS certificate"; \
  tls.cert_subject; tls.cert_issuer; \
  pcre:"/^(.+)$/S"; pcre:"/^\1$/I"; \
  sid:4000001; rev:1;)

# Detect expired certificate
alert tls any any -> any any (msg:"Expired TLS certificate in use"; \
  tls.cert_invalid; \
  sid:4000002; rev:1;)

# Known malicious JA3 (Cobalt Strike default)
alert tls any any -> any any (msg:"Cobalt Strike default JA3"; \
  ja3.hash; content:"a0e9f5d64349fb13191bc781f81f42e1"; \
  sid:4000003; rev:1;)
```

## Workflow

### Step 1: Active TLS Audit

```bash
# Scan all public-facing services
sslyze --json_out=tls_audit.json target.com:443 mail.target.com:993
```

### Step 2: Passive TLS Monitoring

```bash
# Extract TLS metadata from network tap
zeek -r traffic.pcap /opt/zeek/share/zeek/policy/protocols/ssl/ja3.zeek local
cat ssl.log | zeek-cut ts server_name ja3 ja3s issuer subject
```

### Step 3: Certificate Inventory

```bash
# Extract all certificates from PCAP
tshark -r traffic.pcap -Y "tls.handshake.type==11" \
  -T fields -e x509sat.printableString -e x509ce.dNSName \
  -e x509af.utcTime
```

### Step 4: Threat Hunt via JA3

```bash
# Compare JA3 hashes against threat intel
cat ssl.log | zeek-cut ja3 | sort | uniq -c | sort -rn | head -20
# Cross-reference with ja3er.com or abuse.ch
```

## Detection

```yaml
title: Tls Analysis Detection
id: 84e8ff2a-ed93-4b03-b441-5e7ab6b958a3
status: experimental
description: Detects suspicious activity related to performing tls analysis techniques in network security context
logsource:
  category: firewall
  product: linux
detection:
  selection:
    Action: blocked
  condition: selection
level: medium
tags:
  - attack.t1573
  - attack.t1071.001
  - attack.command_and_control
falsepositives:
  - Network monitoring tools performing scheduled connectivity checks
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Tls Analysis Detection | linux/firewall | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1573, T1071.001 |

## Verification

- [ ] No TLS 1.0/1.1 in use (TLS 1.2+ only, prefer 1.3)
- [ ] No weak cipher suites (RC4, DES, 3DES, export ciphers)
- [ ] All certificates valid (not expired, not self-signed in production)
- [ ] Certificate chains complete (no missing intermediates)
- [ ] HSTS headers present on web services
- [ ] JA3 monitoring deployed for known malicious fingerprints
- [ ] Certificate transparency logs monitored

## References

- [sslyze Documentation](https://nabla-c0d3.github.io/sslyze/documentation/)
- [JA3 Fingerprinting](https://github.com/salesforce/ja3)
- [testssl.sh](https://testssl.sh/)
- Mozilla SSL Configuration Generator
- NIST SP 800-52 Rev 2: TLS Implementation Guidelines
