<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: analyzing-dotnet-assemblies
description: >-
  Analyze .NET assemblies to decompile IL code, inspect metadata, extract embedded resources, and identify malicious functionality.
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - dotnet
  - csharp
  - il-code
  - dnspy
  - decompilation
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1027", "T1059.001"]
  cwe: ["CWE-506"]
  tools: ["dnSpy", "ILSpy", "de4dot", "monodis", "dotPeek"]
---

# Analyzing Dotnet Assemblies

## Overview

Analyze .NET assemblies to decompile IL code, inspect metadata, extract embedded resources, and identify malicious functionality.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `dnSpy` | Security tooling |
| `ILSpy` | Security tooling |
| `de4dot` | Security tooling |
| `monodis` | Security tooling |
| `dotPeek` | Security tooling |
| Isolated lab environment for testing | Environment requirement |
| Authorization and signed Rules of Engagement (RoE) | Environment requirement |
| Relevant target samples or systems acquired through authorized channels | Environment requirement |

## Quick Reference

```bash
# Decompile with ILSpy CLI
ilspycmd ./target.dll -o ./decompiled/

# Inspect assembly metadata
monodis --typedef ./target.dll
monodis --method ./target.dll

# Deobfuscate .NET
de4dot ./target.exe -o ./cleaned.exe

# Extract embedded resources
python3 -c "
import dnfile
pe = dnfile.dnPE('./target.dll')
for r in pe.net.resources:
    print(f'{r.name}: {r.size} bytes')
"
```

## Workflow

### Step 1: Preparation and Reconnaissance

```bash
# Identify target and gather initial intelligence
file ./target_sample
dnspy --version 2>/dev/null || echo "Install dnSpy"

# Set up working directory
mkdir -p /tmp/analyzing-dotnet-assemblies/{output,logs,artifacts}
```

### Step 2: Primary Analysis

```bash
# Execute primary analysis with dnSpy
# Refer to Quick Reference above for detailed commands
echo "[*] Running Analyzing Dotnet Assemblies with dnSpy..."

# Log all operations
script -q /tmp/analyzing-dotnet-assemblies/logs/session.log
```

### Step 3: Deep Investigation

```bash
# Apply ILSpy for secondary analysis
echo "[*] Deep investigation with ILSpy..."

# Cross-reference findings
diff /tmp/analyzing-dotnet-assemblies/output/primary.json /tmp/analyzing-dotnet-assemblies/output/secondary.json
```

### Step 4: Documentation and Reporting

```bash
# Generate structured findings report
cat <<'EOF' > /tmp/analyzing-dotnet-assemblies/output/report.json
{
  "technique": "analyzing-dotnet-assemblies",
  "domain": "reverse-engineering",
  "tools_used": ["dnSpy", "ILSpy"],
  "findings": [],
  "recommendations": []
}
EOF
```

## Detection

```yaml
title: Dotnet Assemblies Detection
id: df17ae97-986d-41f9-96af-ac65538ebd02
status: experimental
description: Detects suspicious activity related to analyzing dotnet assemblies techniques in reverse engineering context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*analyzing*dotnet*"
  condition: selection
level: medium
tags:
  - attack.t1027
  - attack.t1059.001
  - attack.defense_evasion
falsepositives:
  - Malware analysis sandbox performing automated binary inspection
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Dotnet Assemblies Detection | windows/process_creation | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1027, T1059.001 |

## Verification

- [ ] Environment and tools verified and operational
- [ ] Target samples acquired through authorized channels
- [ ] Primary analysis completed with findings documented
- [ ] Secondary validation performed with independent tooling
- [ ] All artifacts preserved in structured output directory
- [ ] Detection opportunities documented for blue team

## References

- [MITRE ATT&CK T1027](https://attack.mitre.org/techniques/T1027) — Related technique
- [dnSpy Documentation](https://dnspy.org/) — Primary tooling
- [ILSpy Reference](https://ilspy.org/) — Secondary tooling
