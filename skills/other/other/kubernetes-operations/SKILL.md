---
name: kubernetes-operations
description: Kubernetes cluster operations on minikube including observability (Grafana, Prometheus, Alertmanager, Loki, Tempo), debugging (kubectl debug, ephemeral containers), and cluster management (ArgoCD). Use when working with cluster/manifests/, Kubernetes workloads, pods, deployments, operators, controllers, or cluster components.
context: fork
keywords: kubernetes, k8s, minikube, grafana, prometheus, loki, tempo, argocd, pod, クラスタ, 監視, kubectl, deployment
---

* Access Grafana at `https://grafana.minikube.127.0.0.1.nip.io`
* Disable ArgoCD selfHeal before manual changes, re-enable after

## Debugging

| Investigating | Tool | Entry Point                                 |
|---------------|------|---------------------------------------------|
| Traces, metrics, logs, profiles | Grafana | `https://grafana.minikube.127.0.0.1.nip.io` |
| Pod startup failures, events | kubectl | `kubectl get events -n <namespace>`         |
| In-container process/network | kubectl debug | Ephemeral container                         |

### Observability Investigation (via Grafana)

Use Grafana for all observability signals. Do NOT query backends (Tempo, Mimir, Loki) directly.

1. **Get query parameters** - Check `cluster/manifests/<app>/` for namespace, labels, `OTEL_SERVICE_NAME` (see [Queries](reference/queries.md) for parameter locations)
2. **Open Grafana** - Access `https://grafana.minikube.127.0.0.1.nip.io` in browser
3. **Select datasource and query** - Use appropriate signal:

| Signal | Backend | Datasource | Query Language | Use Case |
|--------|---------|------------|----------------|----------|
| Traces | Tempo | Tempo | TraceQL | Request flow, latency, access destinations |
| Metrics | Mimir (Prometheus) | Mimir | PromQL | Resource usage, HTTP rates, alerting |
| Logs | Loki | Loki | LogQL | Error investigation, audit |
| Profiles | Pyroscope | Pyroscope | Flamegraph UI | CPU/memory hotspots |
| Probes | Blackbox Exporter | Mimir | PromQL | Endpoint reachability |

| Symptom | Signal | Query Approach |
|---------|--------|----------------|
| Errors in logs | Loki → Tempo | Extract traceid from logs, trace in Tempo |
| Latency/5xx | Tempo | Search traces with `status = error` |
| Unknown outbound dependencies | Tempo | Search traces, inspect spans for outbound calls |
| Resource saturation | Mimir | Query CPU/memory metrics |
| High CPU/memory | Pyroscope | Check flamegraphs |

### Pod Direct Investigation (via kubectl)

Use kubectl when Grafana cannot answer the question (e.g., pod not starting, container-level inspection).

| Symptom | Action |
|---------|--------|
| Pod not starting | `kubectl get events -n <namespace>` |
| CrashLoopBackOff | `kubectl logs <pod> -n <namespace> --previous` |
| Network connectivity | `kubectl debug` with ephemeral container |
| Process inspection | `kubectl debug` with ephemeral container |

#### Ephemeral Container

```bash
kubectl debug <pod-name> -n <namespace> \
  --profile=restricted \
  --image=ghcr.io/hippocampus-dev/hippocampus/ephemeral-container:main \
  --target=<container-name> \
  -- <command>
```

Note: Do not use `-it` flag when executing commands. It causes output streaming issues.

## Manual Changes

Required when directly modifying live cluster resources (e.g., `kubectl apply`, `kubectl patch`, `kubectl delete`) outside of the GitOps workflow.

| Operation | Requires Manual Changes |
|-----------|------------------------|
| `kubectl apply/patch/delete` | Yes |
| Debugging (read-only: logs, events, debug) | No |
| Grafana queries | No |
| Editing manifests in repo | No (ArgoCD syncs automatically) |

### ArgoCD selfHeal Control

ArgoCD reverts manual changes unless selfHeal is disabled first. Always re-enable after.

```bash
# Disable selfHeal
kubectl patch application <app-name> -n argocd --type=merge \
  -p '{"spec":{"syncPolicy":{"selfHeal":false}}}'

# Re-enable selfHeal (after work is complete)
kubectl patch application <app-name> -n argocd --type=merge \
  -p '{"spec":{"syncPolicy":{"selfHeal":true}}}'
```

## Observability Stack Manifests

| Component | Path |
|-----------|------|
| Grafana | `cluster/manifests/grafana/` |
| Tempo | `cluster/manifests/tempo/` |
| Mimir | `cluster/manifests/mimir/` |
| Loki | `cluster/manifests/loki/` |
| Pyroscope | `cluster/manifests/pyroscope/` |
| Prometheus | `cluster/manifests/prometheus/` |
| Fluentd | `cluster/manifests/fluentd/` |
| OpenTelemetry | `cluster/manifests/otel-agent/`, `cluster/manifests/otel-collector/` |

## Reference

If writing observability queries:
  See [Queries](reference/queries.md)
