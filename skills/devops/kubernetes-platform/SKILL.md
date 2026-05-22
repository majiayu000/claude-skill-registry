---
name: Kubernetes Platform Engineering
description: Production Kubernetes platform patterns covering cluster architecture, security, GitOps, observability, autoscaling, and operational guardrails
---

# Kubernetes Platform Engineering

## Overview

Platform engineering on Kubernetes is about making the “golden path” easy: secure-by-default workloads, consistent delivery via GitOps, and predictable operations (capacity, upgrades, incident response).

## Why This Matters

- **Reliability**: self-healing + controlled rollouts reduce incidents
- **Security**: least privilege and isolation by default
- **Developer velocity**: standard templates + paved roads
- **Cost control**: right-sizing and autoscaling without surprises

---

## Core Concepts

### 1. Cluster Architecture

- Separate node pools by workload class (stateless, stateful, GPU, batch, system).
- Define upgrade strategy (surge capacity, maintenance windows, version skew policy).
- Decide multi-cluster approach (per env/region/tenant) and shared services (ingress, monitoring, secrets).

### 2. Workload Patterns

- **Deployment** for stateless services; use `PodDisruptionBudget`, `readinessProbe`, and `topologySpreadConstraints`.
- **StatefulSet** for stable identity/storage (databases, queues) with explicit backup/restore.
- **Job/CronJob** for batch; enforce concurrency policies and deadlines.
- **DaemonSet** for node-level agents (logging, CNI, security).

### 3. Networking

- Use `Ingress`/Gateway with TLS termination and standardized auth/rate limiting at the edge.
- Apply **NetworkPolicies** (default-deny + explicit allow) for zero-trust inside the cluster.
- Consider service mesh only when you need it (mTLS, traffic shifting, retries, L7 telemetry); keep complexity intentional.

### 4. Storage

- Standardize `StorageClass` per tier (fast SSD, standard, archival) and backup policies.
- For stateful apps: set anti-affinity/zone spread; verify recovery time objectives (RTO/RPO).
- Avoid “pet” PVs by having a documented restore path and regular restore drills.

### 5. Security Baseline

- Enforce Pod Security (restricted baseline): non-root, read-only root filesystem, drop capabilities.
- RBAC least privilege: namespace-scoped roles, separate human vs automation identities.
- Secrets: prefer external secret managers (e.g., External Secrets + AWS/GCP/Azure secret store); avoid long-lived static secrets in Git.
- Admission policies: Kyverno / Gatekeeper for guardrails (image registries, resource limits, required labels).

### 6. Observability & Ops

- Metrics: Prometheus + dashboards per service (latency, errors, saturation, restarts).
- Logs: structured JSON with trace IDs; centralized retention policies.
- Traces: OpenTelemetry for request graphs across services.
- SLOs: define error budgets and link alerts to user impact.

### 7. GitOps & Delivery

- Git is source of truth: Argo CD / Flux reconciles desired state.
- Use Helm/Kustomize overlays per environment; keep secrets out-of-band.
- Progressive delivery: canary/blue-green via Argo Rollouts / Flagger (or mesh-based traffic shifting).

### 8. Cost & Capacity Management

- Require resource requests/limits; use VPA recommendations carefully (watch for restarts).
- Use HPA/KEDA for demand-based scaling; use cluster autoscaler/Karpenter for nodes.
- Separate spot/preemptible pools for tolerant workloads; enforce pod placement policies.

## Quick Start (Minimal “Production-ish” Deployment)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxUnavailable: 0, maxSurge: 1 }
  selector: { matchLabels: { app: app } }
  template:
    metadata: { labels: { app: app } }
    spec:
      securityContext: { runAsNonRoot: true }
      containers:
        - name: app
          image: your-registry/app:1.0.0
          ports: [{ containerPort: 3000 }]
          resources:
            requests: { cpu: "100m", memory: "256Mi" }
            limits: { cpu: "500m", memory: "512Mi" }
          readinessProbe:
            httpGet: { path: /readyz, port: 3000 }
            initialDelaySeconds: 5
          livenessProbe:
            httpGet: { path: /healthz, port: 3000 }
            initialDelaySeconds: 10
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app
spec:
  minAvailable: 1
  selector: { matchLabels: { app: app } }
```

## Production Checklist

- [ ] Requests/limits set; namespaces have `LimitRange`/`ResourceQuota`
- [ ] `readinessProbe` + `livenessProbe` + graceful shutdown configured
- [ ] PDB + topology spread/anti-affinity to survive node/zone events
- [ ] NetworkPolicies enforce default-deny and least access
- [ ] RBAC least privilege; service accounts scoped per app
- [ ] Metrics/logs/traces exported; alerts tied to SLOs
- [ ] Backup/restore drills for stateful components
- [ ] Upgrade playbook exists (cluster + addons + workload compatibility)

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| Argo CD / Flux | GitOps continuous delivery |
| Helm / Kustomize | Packaging and environment overlays |
| Prometheus + Grafana | Metrics + dashboards |
| Loki/ELK | Central logging |
| OpenTelemetry | Distributed tracing |
| External Secrets | Secret manager integration |
| Kyverno / Gatekeeper | Policy enforcement |

## Anti-patterns

1. **No requests/limits**: unpredictable scheduling and noisy-neighbor incidents
2. **Hand-applied changes**: `kubectl apply` drift instead of GitOps reconciliation
3. **Flat network**: no NetworkPolicies; lateral movement is trivial
4. **Single replica**: planned/unplanned disruption becomes downtime

## Real-World Examples

### Example: Progressive Delivery (Canary)

- Deploy new version at 5% traffic; watch SLOs; ramp to 25/50/100%; auto-rollback on regressions.

### Example: Autoscaling

- HPA on CPU/requests-per-second + cluster autoscaler for nodes; cap max replicas to protect dependencies.

### Example: Zero-Trust Networking

- Default-deny in each namespace; only allow traffic from ingress controller to app and app to explicit dependencies.

## Common Mistakes

1. Missing readiness probes (traffic hits pods before they’re ready)
2. Running containers as root (wider blast radius on compromise)
3. Unbounded egress (data exfiltration paths and surprise costs)
4. Treating the cluster as the product (no SLOs, no runbooks, no ownership)

## Integration Points

- CI (image build, SBOM, scanning, signing)
- CD (GitOps reconciler + progressive delivery)
- Cloud provider (EKS/GKE/AKS, IAM, load balancers, DNS)
- Observability + incident management (paging, runbooks, postmortems)

## Further Reading

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Production Best Practices](https://learnk8s.io/production-best-practices)
- [Kubernetes Patterns](https://k8spatterns.io/)
