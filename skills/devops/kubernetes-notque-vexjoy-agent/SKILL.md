---
name: kubernetes
description: "Kubernetes operations: debugging, security, RBAC, and infrastructure tooling."
user-invocable: false
context: fork
agent: kubernetes-helm-engineer
routing:
  triggers:
    # from kubernetes-debugging
    - "kubernetes debug"
    - "pod failure"
    - "pod crashloop"
    - "kubectl logs"
    - "OOMKilled"
    - "pod pending"
    # from kubernetes-security
    - "kubernetes security"
    - "k8s RBAC"
    - "RBAC setup"
    - "pod security policy"
    - "network policy"
    # from cobalt-core
    - "cobalt core"
    - "cobaltcore"
    - "kvm-exporter"
    - "kvm exporter"
    - "hypervisor metrics"
    - "libvirt exporter"
    - "cloud hypervisor"
  category: kubernetes
  pairs_with:
    - service-health-check
    - go-patterns
    - prometheus-grafana-engineer
---

# Kubernetes Skill

Kubernetes debugging, security hardening, and infrastructure tooling. Covers pod triage, RBAC, network policies, and cobaltcore hypervisor components.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| CrashLoopBackOff, OOMKilled, config error, health check, liveness probe, ImagePullBackOff, Pending, FailedScheduling | `references/crash-diagnosis.md` | ~140 lines |
| service resolution, DNS, CoreDNS, port-forward, NetworkPolicy ingress/egress | `references/network-debugging.md` | ~50 lines |
| CPU throttling, memory limit, OOMKill, ephemeral storage, DiskPressure, debug container | `references/resource-debugging.md` | ~100 lines |
| RBAC, Role, RoleBinding, ClusterRole, ServiceAccount, least-privilege | `references/rbac-patterns.md` | ~60 lines |
| PodSecurity, SecurityContext, runAsNonRoot, readOnlyRootFilesystem, restricted, baseline | `references/pod-security.md` | ~90 lines |
| NetworkPolicy, default-deny, allow-list, namespace isolation | `references/network-policies.md` | ~70 lines |
| cosign, Kyverno, OPA, admission controller, Sealed Secrets, External Secrets | `references/supply-chain.md` | ~120 lines |
| kvm-exporter, libvirt, hypervisor, collector, scrape, steal time, NUMA | `references/kvm-exporter.md` | ~800 lines |
| cobaltcore concurrency, goroutine, semaphore, TryLock | `references/cobalt-concurrency-patterns.md` | ~200 lines |
| cobaltcore testing, mock, moq, Kind cluster | `references/cobalt-testing-patterns.md` | ~200 lines |
| kubernetes debugging process, triage flow, diagnosis routing | `references/kubernetes-debugging.md` | ~50 lines |
| kubernetes security process, RBAC + pod security + network hardening | `references/kubernetes-security.md` | ~50 lines |
| cobaltcore overview, KVM exporter architecture, component identification | `references/cobalt-core.md` | ~50 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.

---

## Phase 1: TRIAGE

Determine which Kubernetes domain the request targets:

| Domain | Load references | Action |
|--------|----------------|--------|
| Pod failure, CrashLoop, OOM | crash-diagnosis, resource-debugging | Triage flow |
| Network, DNS, service resolution | network-debugging, network-policies | Connectivity diagnosis |
| RBAC, permissions, roles | rbac-patterns | Access control |
| Pod hardening, container security | pod-security | Security posture |
| Image signing, secrets, admission | supply-chain | Supply chain |
| Cobaltcore / KVM exporter | kvm-exporter + cobalt refs | Component-specific |

Always specify `-n <namespace>` explicitly in every kubectl command.

**Gate**: Domain identified and relevant references loaded.

---

## Phase 2: DIAGNOSE / RESPOND

For debugging: follow the triage flow — describe, logs, events, exec. Use read-only commands to gather evidence before proposing changes.

For security: provide concrete YAML manifests and specific configurations. Answer with reference-backed specifics, not generic advice.

For cobaltcore: use component-specific reference knowledge for architecture, metrics, configuration, and deployment details.

**Gate**: Specific, reference-backed diagnosis or response provided.

---

## Phase 3: VERIFY

For debugging: confirm the fix resolves the symptom.
For security: validate against the misconfiguration table in supply-chain.md.
For cobaltcore: verify against component test patterns.
