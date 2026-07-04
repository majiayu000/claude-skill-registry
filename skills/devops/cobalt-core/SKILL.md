---
name: cobalt-core
description: "Cobalt Core infrastructure knowledge: KVM exporters, hypervisor tooling, OpenStack compute."
agent: kubernetes-helm-engineer
user-invocable: true
argument-hint: "<cobaltcore topic or repo name>"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Agent
  - Edit
  - Write
routing:
  triggers:
    - "cobalt core"
    - "cobaltcore"
    - "kvm-exporter"
    - "kvm exporter"
    - "hypervisor metrics"
    - "libvirt exporter"
    - "cloud hypervisor"
  category: infrastructure
  pairs_with:
    - go-patterns
    - prometheus-grafana-engineer
    - kubernetes-helm-engineer
---

# Cobalt Core

Domain skill for the [cobaltcore-dev](https://github.com/cobaltcore-dev) project family — SAP Converged Cloud infrastructure components for KVM hypervisor management, metrics collection, and compute-node tooling.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| kvm-exporter, metrics, prometheus, libvirt, hypervisor, collector, scrape, steal time, NUMA, cgroups, cloud hypervisor | `references/kvm-exporter.md` | ~800 lines |
| goroutine, concurrency, semaphore, TryLock, sync.Map, race condition, socket exhaustion, scrape overlap, ClearScrapeCache | `references/concurrency-patterns.md` | ~200 lines |
| test, mock, moq, unit test, E2E, Kind cluster, race detector, interface_mock_gen, test-metrics.sh | `references/testing-patterns.md` | ~200 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.

---

## Phase 1: IDENTIFY

Determine which cobaltcore component the user is asking about.

| Component | Repository | Reference |
|-----------|-----------|-----------|
| KVM Exporter | `cobaltcore-dev/kvm-exporter` | `references/kvm-exporter.md` |

If the component is not listed, tell the user no reference exists yet and offer to analyze the repo.

**Gate**: Component identified. Reference loaded. Proceed to Phase 2.

---

## Phase 2: RESPOND

Use loaded reference knowledge to answer the user's question. The references contain:
- Architecture and data flow diagrams
- Complete metric catalogs with types, labels, and descriptions
- Configuration options and environment variables
- Deployment models (Helm, DaemonSet, container specs)
- Code patterns (concurrency, caching, error handling)
- Testing strategies (unit mocks, E2E with Kind clusters)
- Alerting rules and operational concerns

For implementation questions involving Go code, pair with the `go-patterns` skill for language-specific patterns. For Prometheus/Grafana questions, pair with `prometheus-grafana-engineer`. For Kubernetes deployment questions, pair with `kubernetes-helm-engineer`.

**Gate**: Question answered with reference-backed specifics, not generic advice.

---

## Phase 3: EXTEND

When the user wants to add a new cobaltcore repo:
1. Analyze the repo systematically (README, go.mod, key source files, Dockerfile, Helm chart)
2. Create a new reference file at `references/{repo-name}.md`
3. Update the Reference Loading Table in this SKILL.md
4. Update the component table in Phase 1

Follow the structure established in `references/kvm-exporter.md` for consistency.
