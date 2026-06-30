---
name: container-k8s-escape
description: Use when breaking out of a container or escalating inside Kubernetes — runc/BuildKit CVEs, privileged/capability/cgroup misconfig escapes, NVIDIA GPU toolkit escape, K8s RBAC abuse, kubelet RCE, ingress/admission-controller RCE, node-to-cluster pivot
metadata:
  type: offensive
  phase: exploit-install-actions
  tools: kubectl, crictl, runc, deepce, cdk, kube-hunter, peirates, amicontained, trufflehog, falco, kubeletctl, nsenter
  mitre: [T1611, T1610, T1613, T1552.001, T1552.007, T1078.001, T1068, T1496]
kill_chain:
  phase: [exploit, install, actions]
  step: [4, 5, 7]
  attck_tactics: [TA0002, TA0004, TA0005, TA0006, TA0008]
  attck_techniques: [T1611, T1610, T1613, T1609, T1552.001, T1552.007, T1078.001, T1068, T1496, T1610]
depends_on: [recon-osint, cloud-security, vulnerability-analysis]
feeds_into: [cloud-security, red-team-ops, privesc-linux, active-directory-attack]
inputs: [container_context, k8s_service_account, kubeconfig, node_access, registry_push_access]
outputs: [host_root_shell, node_compromise, stolen_sa_tokens, cluster_admin, attack_path, escape_finding]
references:
  - references/runtime-cve-escapes.md
  - references/privileged-misconfig-escape.md
  - references/nvidia-gpu-escape.md
  - references/k8s-rbac-escalation.md
  - references/ingress-admission-attacks.md
  - references/node-host-pivot.md
scripts:
  - scripts/escape_enum.sh
  - scripts/runc_cwd_escape.py
  - scripts/release_agent_escape.sh
  - scripts/nvidiascape_build.sh
  - scripts/k8s_rbac_audit.py
  - scripts/kubelet_exec.py
---

# Container Breakout & Kubernetes Escape

## When to Activate

- You have code execution inside a container/pod and want to break out to the host node
- Auditing a Kubernetes cluster for RBAC privilege-escalation and lateral-movement paths
- Assessing runc/containerd/BuildKit/Docker runtime versions against known escape CVEs
- A pod is privileged, has dangerous capabilities, hostPath/hostPID/hostNetwork, or a mounted docker.sock
- Attacking GPU/AI workloads using the NVIDIA Container Toolkit
- Testing ingress-nginx / admission-controller exposure for unauthenticated RCE
- Post-escape: pivoting from one node to full cluster takeover (kubelet, SA tokens, etcd, cloud IMDS)
- Building Falco/Sigma detections for container-escape behavior (defensive validation)

## Technique Map

| Technique | ATT&CK | CWE | Reference | Script |
|-----------|--------|-----|-----------|--------|
| runc working-dir fd leak escape (Leaky Vessels, CVE-2024-21626) | T1611 | CWE-403 | references/runtime-cve-escapes.md | scripts/runc_cwd_escape.py |
| runc masked-path / `/dev/null` symlink escape (CVE-2025-31133) | T1611 | CWE-367 | references/runtime-cve-escapes.md | scripts/runc_cwd_escape.py |
| runc `/dev/console` bind-mount + LSM bypass (CVE-2025-52565/52881) | T1611 | CWE-363 | references/runtime-cve-escapes.md | scripts/escape_enum.sh |
| BuildKit cache/teardown symlink escape (CVE-2024-23651/52/53) | T1611 | CWE-59 | references/runtime-cve-escapes.md | scripts/escape_enum.sh |
| Privileged / `CAP_SYS_ADMIN` cgroup `release_agent` escape | T1611 | CWE-269 | references/privileged-misconfig-escape.md | scripts/release_agent_escape.sh |
| `core_pattern` host-side code exec on crash | T1611 | CWE-269 | references/privileged-misconfig-escape.md | scripts/release_agent_escape.sh |
| `hostPID` + `nsenter` into PID 1 namespace | T1611 | CWE-668 | references/privileged-misconfig-escape.md | scripts/escape_enum.sh |
| Mounted `docker.sock` / `containerd.sock` host takeover | T1610 | CWE-668 | references/privileged-misconfig-escape.md | scripts/escape_enum.sh |
| `hostPath` `/` mount → write host filesystem | T1611 | CWE-22 | references/privileged-misconfig-escape.md | scripts/escape_enum.sh |
| NVIDIAScape `LD_PRELOAD` OCI-hook escape (CVE-2025-23266) | T1611 | CWE-426 | references/nvidia-gpu-escape.md | scripts/nvidiascape_build.sh |
| NVIDIA CT TOCTOU mount escape (CVE-2024-0132 / CVE-2025-23359) | T1611 | CWE-367 | references/nvidia-gpu-escape.md | scripts/nvidiascape_build.sh |
| K8s RBAC privesc (verb/wildcard/escalate, SA token theft) | T1078.001 | CWE-269 | references/k8s-rbac-escalation.md | scripts/k8s_rbac_audit.py |
| `nodes/proxy` GET → kubelet WebSocket exec RCE | T1609 | CWE-863 | references/k8s-rbac-escalation.md | scripts/kubelet_exec.py |
| Anonymous/authed kubelet API exec on :10250 | T1609 | CWE-306 | references/k8s-rbac-escalation.md | scripts/kubelet_exec.py |
| IngressNightmare unauth RCE (CVE-2025-1974 + annotation chain) | T1190 | CWE-94 | references/ingress-admission-attacks.md | scripts/escape_enum.sh |
| Node → cluster pivot (etcd, IMDS, SA-token harvest) | T1613 | CWE-552 | references/node-host-pivot.md | scripts/escape_enum.sh |

## Quick Start

```bash
# 0. Enumerate the container/pod context: caps, mounts, sockets, runtime versions, K8s creds
bash scripts/escape_enum.sh                 # run INSIDE the target container

# 1. Runtime-CVE path: detect vulnerable runc/BuildKit and run the cwd-fd escape (CVE-2024-21626)
python3 scripts/runc_cwd_escape.py --probe                       # try fd 7,8,9 -> host /
python3 scripts/runc_cwd_escape.py --cmd 'id; cat /etc/shadow'   # via docker -w or k8s revshell

# 2. Misconfig path: privileged / CAP_SYS_ADMIN -> cgroup release_agent host code exec
bash scripts/release_agent_escape.sh -c 'id > /tmp/escape_out'   # reads host PID list / runs cmd

# 3. GPU path: build a malicious image for NVIDIAScape (CVE-2025-23266)
bash scripts/nvidiascape_build.sh --cmd 'id; cat /etc/shadow' --tag evil-gpu:latest

# 4. K8s RBAC: audit who can escalate / reach the kubelet (needs a kubeconfig or in-pod SA token)
python3 scripts/k8s_rbac_audit.py --kubeconfig ~/.kube/config --dangerous

# 5. nodes/proxy or open kubelet -> exec into any pod on the node
python3 scripts/kubelet_exec.py --node 10.0.0.5 --pod kube-system/etcd-master \
        --container etcd --cmd 'cat /var/lib/etcd/...' --token "$SA_TOKEN"
```

Recommended tooling: `deepce` / `cdk` / `amicontained` (in-container recon), `peirates` (K8s pivot),
`kube-hunter` (cluster scan), `kubeletctl` (kubelet API), `crictl` (post-escape node control),
`falco` (defensive validation of every technique below).

## OPSEC & Detection (summary)

| Technique | Telemetry / IOC | Detection (Sigma/EDR/Falco) | OPSEC note |
|-----------|-----------------|------------------------------|------------|
| runc cwd-fd escape (CVE-2024-21626) | container process cwd under `/proc/self/fd/N`; `getcwd` ENOENT errors; host-path access from pid1 | Falco `Container Drift`/unexpected host-fs read; alert on runtime < runc 1.1.12 | No new files needed; works via `-w`/cwd only — very quiet, but lands on real host fs |
| runc 2025 trio (masked-path/console) | symlink swap of `/dev/null` or `/dev/pts/N`; RW open of `/proc/sysrq-trigger`/`core_pattern` | Falco "Write below /proc/sys"/sysrq; mount race anomalies | Symlink swap is a timing race; on failure may crash host (sysrq) — loud |
| release_agent / core_pattern | mount of cgroup/cgroup2; write to `*/release_agent` or `/proc/sys/kernel/core_pattern` | Falco `Detect release_agent File Container Escapes`; Sigma on write to core_pattern | Requires CAP_SYS_ADMIN+mount; release_agent is cgroup-v1 only |
| nsenter / hostPID | `nsenter --target 1`; process entering host mount/pid ns | Falco "nsenter" / `proc.name=nsenter` in container; ATT&CK T1611 | hostPID is visible in pod spec; nsenter is a strong IOC |
| docker.sock abuse | `/var/run/docker.sock` mounted; `curl --unix-socket` create privileged container | Falco "Docker socket access by unexpected proc"; new privileged container event | Spawns a *new* privileged container — visible to docker/containerd events |
| NVIDIAScape (CVE-2025-23266) | image `ENV LD_PRELOAD=/proc/self/cwd/*.so`; nvidia hook loads .so from container fs | Falco shared-lib load by `nvidia-ctk`/hook from container path | Needs only image push + run; no kernel bug — image scan catches the ENV |
| nodes/proxy → kubelet exec | WebSocket GET to kubelet `/exec`/`/run` on :10250; **no API-server audit entry** | Runtime/L7 only — invisible to API audit & GuardDuty; monitor kubelet access log | Bypasses API-server audit & admission entirely — extremely stealthy |
| K8s RBAC privesc / SA-token theft | read of `/var/run/secrets/.../token`; `can-i` probes; bind to cluster-admin | API audit `create rolebindings`/`escalate`; Falco `Read SA token` | `kubectl auth can-i` probing is logged at API server |
| IngressNightmare (CVE-2025-1974) | AdmissionReview with injected NGINX directive; `.so` loaded from `/proc/<pid>/fd` | Sysdig/Falco "IngressNightmare"; shared-lib load from /proc in nginx | Code runs during `nginx -t` validation; controller SA grabs all-namespace secrets |

## Deep Dives

- references/runtime-cve-escapes.md — runc CVE-2024-21626 (working-dir fd leak), the Nov-2025 runc trio (CVE-2025-31133/52565/52881 masked-path & `/dev/console`), and the BuildKit Leaky Vessels CVEs, with full PoCs and version matrices.
- references/privileged-misconfig-escape.md — `--privileged`/capability escapes: cgroup-v1 `release_agent`, `core_pattern`, `hostPID`+`nsenter`, mounted docker/containerd sockets, and `hostPath`/`/` mounts, with complete scripts.
- references/nvidia-gpu-escape.md — NVIDIAScape (CVE-2025-23266 `LD_PRELOAD` OCI-hook) and the CVE-2024-0132 / CVE-2025-23359 TOCTOU mount escapes in the NVIDIA Container Toolkit; build-and-run PoCs.
- references/k8s-rbac-escalation.md — RBAC privilege escalation (wildcards, `escalate`/`bind`, `pods/exec`, impersonation), SA-token harvest, the `nodes/proxy` GET → kubelet WebSocket exec RCE, and open kubelet :10250.
- references/ingress-admission-attacks.md — IngressNightmare (CVE-2025-1974 + the annotation-injection chain), admission-webhook abuse, and how a controller SA leads to cluster-wide secret theft.
- references/node-host-pivot.md — post-escape playbook: from one node to the whole cluster — etcd looting, kubelet/crictl, SA-token mining across pods, cloud IMDS role theft, and the defensive counterweight.
