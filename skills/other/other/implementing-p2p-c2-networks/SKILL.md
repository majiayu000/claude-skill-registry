<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: implementing-p2p-c2-networks
description: >-
  Implement peer-to-peer C2 networks where compromised hosts relay commands without direct internet access, using SMB named pipes, TCP mesh, or custom P2P protocols.
domain: cybersecurity
subdomain: c2-frameworks
tags:
  - p2p-c2
  - smb-pipe
  - mesh
  - lateral-relay
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1090.003"]
  frameworks: ["MITRE ATT&CK"]
  tools: ["cobalt-strike", "havoc", "custom"]
---

# Implementing P2P C2 Networks

## Overview

Implement peer-to-peer C2 networks where compromised hosts relay commands without direct internet access, using SMB named pipes, TCP mesh, or custom P2P protocols.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `cobalt-strike` | Security tooling |
| `havoc` | Security tooling |
| `custom` | Security tooling |
| C2 framework with P2P support, internal network access, SMB connectivity | Environment requirement |

## Quick Reference

```bash
# Quick start commands
node scripts/agent.js --help
node scripts/agent.js configure --mode p2p --transport smb-pipe
```

## Workflow

### Step 1: Configure P2P Listener

```bash
node scripts/agent.js configure --mode p2p --transport smb-pipe
```

### Step 2: Link P2P Nodes

```bash
node scripts/agent.js link --parent beacon01 --child beacon02 --pipe c2pipe
```

### Step 3: Test Relay Chain

```bash
node scripts/agent.js test --chain beacon01,beacon02,beacon03
```

## Detection

```yaml
title: P2p C2 Networks Detection
id: ee9b7f30-57f1-475d-9483-42f8af05602a
status: experimental
description: Detects suspicious activity related to implementing p2p c2 networks techniques in c2 frameworks context
logsource:
  category: network_connection
  product: windows
detection:
  selection:
    DestinationPort: 443
    Initiated: "true"
  condition: selection
level: high
tags:
  - attack.t1090.003
  - attack.command_and_control
falsepositives:
  - Authorized penetration testing tools during scheduled assessments
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| P2p C2 Networks Detection | windows/network_connection | Sigma rule (high) |
| ATT&CK Coverage | MITRE ATT&CK | T1090.003 |

## Verification

- **Verify P2P mesh**: `node scripts/agent.js verify --mode p2p`
- **Confirm relay**: `node scripts/agent.js test --chain beacon01,beacon02,beacon03`

## References

- MITRE ATT&CK: T1090.003
- Frameworks: MITRE ATT&CK
- Tools: cobalt-strike, havoc, custom
