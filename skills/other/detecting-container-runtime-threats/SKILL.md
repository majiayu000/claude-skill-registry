<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-container-runtime-threats
description: >-
  Detect container runtime anomalies including shell spawning, file system
  tampering, network anomalies, privilege escalation, and cryptominer deployment
  using Falco rules, Tetragon tracing policies, and eBPF-based monitoring.
domain: cybersecurity
subdomain: cloud-native-security
tags:
  - falco
  - tetragon
  - ebpf
  - runtime-detection
  - container-escape
  - cryptominer
  - anomaly-detection
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1610"]
---

# Detecting Container Runtime Threats

## Overview

Container runtime threats include shell spawning in production containers,
sensitive file access, unexpected network connections, privilege escalation
attempts, and cryptominer deployment. This skill provides detection rules
for Falco and Tetragon to identify these behaviors in real time.

Mode: `[MODE: BLUE]` — Runtime threat detection. `[MODE: PURPLE]` — Detection engineering.

## Prerequisites

| Requirement | Details |
|---|---|
| Falco >= 0.37 or Tetragon >= 1.0 deployed | Required |
| Kubernetes audit logging enabled | Required |
| SIEM for alert aggregation | Required |

## Key Concepts

### Falco Rules for Container Threats

```yaml
# Detect shell spawned in container
- rule: Shell Spawned in Container
  desc: A shell was started in a running container
  condition: >
    spawned_process and container and
    proc.name in (bash, sh, zsh, dash, csh, ksh) and
    not proc.pname in (crond, sshd)
  output: >
    Shell spawned in container (user=%user.name container=%container.name
    shell=%proc.name parent=%proc.pname image=%container.image.repository
    cmdline=%proc.cmdline)
  priority: WARNING
  tags: [container, shell, mitre_execution, T1059]

# Detect sensitive mount
- rule: Sensitive Mount in Container
  desc: Container has sensitive host path mounted
  condition: >
    container and
    (ka.req.pod.volumes.hostpath intersects (/proc, /sys, /etc, /var/run/docker.sock))
  output: >
    Sensitive host mount detected (container=%container.name
    image=%container.image.repository mounts=%ka.req.pod.volumes.hostpath)
  priority: CRITICAL
  tags: [container, mount, mitre_privilege_escalation, T1611]

# Detect cryptominer network connections
- rule: Cryptominer Network Activity
  desc: Outbound connection to known mining pools
  condition: >
    outbound and container and
    fd.sip.name in (pool.minexmr.com, xmr.pool.minergate.com,
    pool.supportxmr.com, mining.oceanpool.org)
  output: >
    Cryptominer connection from container (container=%container.name
    image=%container.image.repository dest=%fd.sip.name:%fd.sport)
  priority: CRITICAL
  tags: [container, cryptominer, mitre_impact, T1496]

# Detect secret file reads
- rule: Read Sensitive File in Container
  desc: Sensitive file read from within container
  condition: >
    open_read and container and
    (fd.name startswith /etc/shadow or
     fd.name startswith /run/secrets or
     fd.name startswith /var/run/secrets/kubernetes.io)
  output: >
    Sensitive file read (file=%fd.name container=%container.name
    user=%user.name image=%container.image.repository)
  priority: WARNING
  tags: [container, credential_access, T1552]
```

### Tetragon Process Tracing

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: detect-privilege-escalation
spec:
  kprobes:
  - call: "__x64_sys_setuid"
    syscall: true
    args:
    - index: 0
      type: "int"
    selectors:
    - matchArgs:
      - index: 0
        operator: "Equal"
        values:
        - "0"
    - matchNamespaces:
      - namespace: Pid
        operator: NotIn
        values:
        - "host_ns"
```

## Workflow

```bash
# Deploy detection rules
node scripts/agent.js --action deploy --rules-dir ./falco-rules/

# Audit runtime alerts
node scripts/agent.js --action audit --output /tmp/runtime-threats.json

# Test detection with simulated threat
node scripts/agent.js --action test --simulate shell-spawn
```

## Detection

```yaml
title: Container Runtime Threats Detection
id: 70488ea8-4849-4170-987c-df5079ef57e0
status: experimental
description: Detects suspicious activity related to detecting container runtime threats techniques in cloud native security context
logsource:
  product: kubernetes
  service: audit
detection:
  selection:
    eventName: "*Unauthorized*"
  condition: selection
level: medium
tags:
  - attack.t1610
  - attack.privilege_escalation
falsepositives:
  - Kubernetes controller reconciliation loops during cluster updates
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Container Runtime Threats Detection | kubernetes | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1610 |

## Verification

- [ ] Shell spawning detected in all non-init containers
- [ ] Sensitive file access (shadow, secrets) generates alerts
- [ ] Cryptominer network connections blocked and alerted
- [ ] Container escape attempts (nsenter, mount) detected
- [ ] Privilege escalation (setuid 0) traced via Tetragon
- [ ] Alert pipeline to SIEM operational

## References

- [Falco Rules Reference](https://falco.org/docs/reference/rules/)
- [Tetragon TracingPolicy](https://tetragon.io/docs/concepts/tracing-policy/)
- [MITRE ATT&CK Containers Matrix](https://attack.mitre.org/matrices/enterprise/containers/)
