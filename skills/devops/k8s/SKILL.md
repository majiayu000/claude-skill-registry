---
name: k8s
description: Kubernetes ops skill for deploying, operating, and troubleshooting services on Kubernetes. Use for tasks like writing manifests/Helm, configuring deployments/services/ingress, autoscaling, observability, RBAC, secrets/configmaps, rollout/rollback, incident debugging, and production readiness checks.
---

# k8s

Use this skill for Kubernetes 运维与发布相关工作。

## Defaults / assumptions to confirm

- Cluster type: managed (EKS/GKE/ACK) vs self-hosted
- Packaging: raw YAML vs Helm vs Kustomize
- Ingress: NGINX/ALB/APISIX/Istio
- Observability stack: Prometheus/Grafana, Loki/ELK, tracing

## Workflow

1) Understand service requirements
- Ports, protocols, health checks, resources (CPU/mem), storage needs.
- SLOs: latency, availability, RPO/RTO.
- Dependencies: DB, cache, MQ, external APIs.

2) Deployment design
- Use `Deployment` for stateless; `StatefulSet` for stable identities/storage.
- Define `readinessProbe` and `livenessProbe` (and `startupProbe` if needed).
- Set `resources.requests/limits` and choose appropriate QoS.
- Use `PodDisruptionBudget` for availability during maintenance.

3) Config & secrets
- Config: `ConfigMap` (non-sensitive), mounted or env.
- Secrets: `Secret` (sensitive) + external secret manager if available.
- Never commit plaintext secrets; prefer sealed/external secrets.

4) Networking
- `Service` types and DNS.
- `Ingress`/Gateway routing, TLS termination, timeouts.
- NetworkPolicy if cluster enforces it.

5) Scaling & resilience
- `HPA` based on CPU/memory/custom metrics.
- Graceful shutdown (`preStop`, terminationGracePeriodSeconds).
- Retry/backoff at client; avoid retry storms.

6) Observability
- Standard logs with correlation IDs.
- Metrics: RPS, p95 latency, error rate, saturation.
- Alerts and dashboards; runbook links.

7) Release operations
- Rolling updates, canary/blue-green if needed.
- `kubectl rollout status` + rollback plan.
- Post-deploy verification checks and smoke tests.

8) Troubleshooting checklist
- `kubectl get/describe` pods, events, and `logs`.
- Check probes, image pull, env/config, DNS, network, and resource throttling.
- For performance: node pressure, HPA behavior, GC/heap, connection pool limits.

## Output expectations when making changes

- Provide manifests (or Helm values/templates) + brief deployment notes.
- Include resource sizing rationale and probe settings.
- Include rollback instructions and verification steps.

