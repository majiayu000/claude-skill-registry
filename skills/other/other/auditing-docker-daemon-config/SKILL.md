<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: auditing-docker-daemon-config
description: >-
  Audit Docker daemon configuration for security misconfigurations including
  exposed APIs, insecure registries, missing user namespace remapping, excessive
  logging, and non-compliant CIS Docker Benchmark settings.
domain: cybersecurity
subdomain: container-security
tags:
  - docker
  - daemon
  - cis-benchmark
  - hardening
  - configuration-audit
  - docker-socket
  - user-namespaces
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1610"]
---

# Auditing Docker Daemon Config

## Overview

Docker daemon misconfigurations are a primary attack vector for container escape
and host compromise. This skill audits `/etc/docker/daemon.json`, systemd unit
files, Docker socket permissions, and runtime settings against the CIS Docker
Benchmark to identify insecure defaults, exposed TCP APIs, missing TLS, disabled
user namespace remapping, and excessive container capabilities.

Mode: `[MODE: BLUE]` — Defensive configuration audit.

## Prerequisites

| Requirement | Details |
|---|---|
| Root or docker group access on target host | Required |
| Docker >= 20.10 installed | Required |
| `docker info` and `docker system info` accessible | Required |
| CIS Docker Benchmark v1.6+ reference | Required |
| Optional | `docker-bench-security` for automated scanning |

## Key Concepts

### Daemon Configuration File

```bash
# Check daemon.json
cat /etc/docker/daemon.json

# Critical settings to verify
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "live-restore": true,
  "userland-proxy": false,
  "log-driver": "json-file",
  "log-opts": {"max-size": "10m", "max-file": "3"},
  "storage-driver": "overlay2",
  "default-ulimits": {"nofile": {"Name": "nofile", "Hard": 64000, "Soft": 64000}}
}
```

### Docker Socket Security

```bash
# Check socket permissions
ls -la /var/run/docker.sock
# Should be: srw-rw---- root docker

# Check if TCP API is exposed
ss -tlnp | grep 2375
ss -tlnp | grep 2376

# Check for exposed API without TLS (CRITICAL)
curl -s http://localhost:2375/version 2>/dev/null && echo "EXPOSED WITHOUT TLS"

# Verify TLS configuration
docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem \
  -H=tcp://HOST:2376 version
```

### CIS Docker Benchmark Checks

```bash
# Run docker-bench-security
docker run --rm --net host --pid host \
  --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  docker/docker-bench-security

# Manual checks
# CIS 2.1: Restrict network traffic between containers
docker network ls --filter driver=bridge -q | xargs -I {} \
  docker network inspect {} --format '{{.Options}}'

# CIS 2.5: Ensure auditd is configured for Docker files
auditctl -l | grep -E '/usr/bin/docker|/var/lib/docker|/etc/docker'

# CIS 2.8: Enable user namespace support
docker info --format '{{.SecurityOptions}}' | grep userns
```

### User Namespace Remapping

```bash
# Check current remapping status
docker info --format '{{.SecurityOptions}}'

# Configure user namespace remapping
# In /etc/docker/daemon.json:
# { "userns-remap": "default" }

# Verify subordinate UID/GID mappings
cat /etc/subuid
cat /etc/subgid
```

## Workflow

### Step 1: Collect Configuration

```bash
docker info --format json > /tmp/docker-info.json
cat /etc/docker/daemon.json > /tmp/daemon.json 2>/dev/null || echo "{}" > /tmp/daemon.json
```

### Step 2: Run Audit

```bash
node scripts/agent.js --daemon-config /tmp/daemon.json --docker-info /tmp/docker-info.json --output /tmp/docker-audit.json
```

### Step 3: Review Findings

```bash
cat /tmp/docker-audit.json | jq '.findings[] | select(.severity == "critical" or .severity == "high")'
```

## Detection

```yaml
title: Auditing Docker Daemon Config Detection
id: 558df9c1-a8ce-4914-b5ae-bc3552351399
status: experimental
description: Detects suspicious activity related to auditing docker daemon config techniques in container security context
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
  - attack.execution
falsepositives:
  - Container orchestration platform performing routine health checks
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Auditing Docker Daemon Config Detection | kubernetes | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1610 |

## Verification

- [ ] Docker TCP API not exposed on port 2375 (unencrypted)
- [ ] TLS enabled if TCP API required (port 2376)
- [ ] Inter-container communication disabled (`icc: false`)
- [ ] User namespace remapping enabled
- [ ] `no-new-privileges` set to true
- [ ] Docker socket permissions restricted to root:docker
- [ ] Content trust enabled (`DOCKER_CONTENT_TRUST=1`)
- [ ] Audit rules configured for Docker files and directories
- [ ] Log driver configured with size limits

## References

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Docker Daemon Configuration](https://docs.docker.com/engine/reference/commandline/dockerd/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [NIST SP 800-190 — Container Security](https://csrc.nist.gov/publications/detail/sp/800-190/final)
