---
name: architecture-review
description: |
  Architecture evaluation criteria and technology standards for the homelab.
  Preloaded into the designer agent to ground design decisions in established
  patterns and principles.

  Use when: (1) Evaluating a proposed technology addition, (2) Reviewing architecture decisions,
  (3) Assessing stack fit for a new component, (4) Comparing implementation approaches.

  Triggers: "architecture review", "evaluate technology", "stack fit", "should we use",
  "technology comparison", "design review", "architecture decision"
user-invocable: false
---

# Architecture Evaluation Framework

## Current Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **OS** | Talos Linux | Immutable, API-driven Kubernetes OS |
| **GitOps** | Flux + ResourceSets | Declarative cluster state reconciliation |
| **CNI/Network** | Cilium | eBPF networking, network policies, Hubble observability |
| **Storage** | Longhorn | Distributed block storage with S3 backup |
| **Object Storage** | Garage | S3-compatible distributed object storage |
| **Database** | CNPG (CloudNativePG) | PostgreSQL operator with HA and backups |
| **Cache/KV** | Dragonfly | Redis-compatible in-memory store |
| **Monitoring** | kube-prometheus-stack | Prometheus + Grafana + Alertmanager |
| **Logging** | Alloy → Loki | Log collection pipeline |
| **Certificates** | cert-manager | Automated TLS certificate management |
| **Secrets** | ESO + AWS SSM | External Secrets Operator with Parameter Store |
| **Upgrades** | Tuppr | Declarative Talos/Kubernetes/Cilium upgrades |
| **Infrastructure** | Terragrunt + OpenTofu | Infrastructure as Code for bare-metal provisioning |
| **CI/CD** | GitHub Actions + OCI | Artifact-based promotion pipeline |

## Evaluation Criteria

When evaluating any proposed technology addition or architecture change, assess against these criteria:

### 1. Principle Alignment

Score the proposal against each core principle (Strong/Weak/Neutral):
- **Enterprise at Home**: Does it reflect production-grade patterns?
- **Everything as Code**: Can it be fully represented in git?
- **Automation is Key**: Does it reduce or increase manual toil?
- **Learning First**: Does it teach valuable enterprise skills?
- **DRY and Code Reuse**: Does it leverage existing patterns or create duplication?
- **Continuous Improvement**: Does it make the system more maintainable?

### 2. Stack Fit

- Does this overlap with existing tools? (e.g., adding Redis when Dragonfly exists)
- Does it integrate with the GitOps workflow? (Must be Flux-deployable)
- Does it work on bare-metal? (No cloud-only services)
- Does it support the multi-cluster model? (dev → integration → live)

### 3. Operational Cost

- How is it monitored? (Must integrate with kube-prometheus-stack)
- How is it backed up? (Must have a recovery story)
- How does it handle upgrades? (Must be declarative, ideally via Renovate)
- What's the failure blast radius? (Isolated > cluster-wide)

### 4. Complexity Budget

- Is the complexity justified by the learning value?
- Could a simpler existing tool solve the same problem?
- What's the maintenance burden over 12 months?

### 5. Alternative Analysis

- What existing stack components could solve this? (Always check first)
- What are the top 2-3 alternatives in the ecosystem?
- What do other production homelabs use? (kubesearch research)

### 6. Failure Modes

- What happens when this component is unavailable?
- How does it interact with network policies? (Default deny)
- What's the recovery procedure? (Must be documented in a runbook)
- Can it self-heal? (Strong preference for self-healing)

## Common Design Patterns

### New Application
1. HelmRelease via ResourceSet (flux-gitops pattern)
2. Namespace with network-policy profile label
3. ExternalSecret for credentials
4. ServiceMonitor + PrometheusRule for observability
5. GarageBucketClaim if S3 storage needed
6. CNPG Cluster if database needed

### New Infrastructure Component
1. OpenTofu module in `infrastructure/modules/`
2. Unit in appropriate stack under `infrastructure/units/`
3. Test coverage in `.tftest.hcl` files
4. Version pinned in `versions.env` if applicable

### New Secret
1. Store in AWS SSM Parameter Store
2. Reference via ExternalSecret CR
3. Never commit to git, not even encrypted

### New Storage
1. Longhorn PVC for block storage (default)
2. GarageBucketClaim for object storage (S3-compatible)
3. Never use hostPath or emptyDir for persistent data

### New Database
1. CNPG Cluster CR for PostgreSQL
2. Automated backups to Garage S3
3. Connection pooling via PgBouncer (CNPG-managed)

### New Network Exposure
1. HTTPRoute for HTTP/HTTPS traffic (Gateway API)
2. Appropriate network-policy profile label
3. cert-manager Certificate for TLS
4. Internal gateway for internal-only services

## Anti-Patterns to Challenge

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|------------------|
| "Just run a container" without monitoring | Invisible failures, no alerting | ServiceMonitor + PrometheusRule required |
| Adding a new tool when existing ones suffice | Stack bloat, maintenance burden | Evaluate existing stack first |
| Skipping observability "for now" | Technical debt that never gets paid | Monitoring is day-1, not day-2 |
| Manual operational steps | Drift, inconsistency, bus factor | Everything declarative via GitOps |
| Cloud-only services | Vendor lock-in, can't run on bare-metal | Self-hosted alternatives preferred |
| Single-instance without HA story | Single point of failure | At minimum, document recovery procedure |
| Storing state outside git | Shadow configuration, drift | Git is the source of truth |
