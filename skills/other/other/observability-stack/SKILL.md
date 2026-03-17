---
name: observability-stack
depth: full
description: >-
    Generates Pulumi TypeScript observability infrastructure for Grafana Alloy 1.13, Prometheus 3.5+, Grafana 12.3 across K8s/Docker. Use when deploying metrics stacks, provisioning alert rules/dashboards, or migrating cloud↔selfhosted observability.
---

# [H1][OBSERVABILITY-STACK]
>**Dictum:** *Infrastructure generation follows canonical deploy.ts patterns.*

<br>

Stack: Alloy -> Prometheus -> Grafana (metrics only). Logs/traces -> `otelcol.exporter.debug` (discarded).
Runtime: `OTEL_LOGS_EXPORTER=none`, `OTEL_TRACES_EXPORTER=none`, `OTEL_METRICS_EXPORTER=otlp` (deploy.ts:95-97).
Versions: Alloy 1.13.0 (OTel Collector v0.142.0), Prometheus 3.5.1+ (native histograms stable in 3.8+, flag no-op in 3.9+), Grafana 12.3.2.

| [INDEX] | [USE_THIS_SKILL]                       | [USE_OTHER_SKILL]                                          |
| :-----: | -------------------------------------- | ---------------------------------------------------------- |
|   [1]   | **Deploy observability via Pulumi.**   | **pulumi-k8s-generator**: Non-observability K8s resources. |
|   [2]   | **OTEL collector configs (Alloy).**    | **k8s-debug**: Debug deployed observability pods.          |
|   [3]   | **Scrape/alert rules, dashboards.**    | **pulumi-k8s-validator**: Audit existing infra code.       |
|   [4]   | **Mode migration cloud<->selfhosted.** | **promql-generator**: PromQL query construction.           |

**Tasks:**
1. Read all three `references/` files before generating.
2. Gather: mode (cloud/selfhosted), retention, HA, TLS via **AskUserQuestion** (ambiguous only).
3. Generate Pulumi TypeScript resources following `deploy.ts` patterns.
4. Validate: `pnpm exec nx run infrastructure:typecheck` then `pulumi preview --diff`.

---
## [1][CANONICAL_IMPLEMENTATION]
>**Dictum:** *deploy.ts is the single source of truth for resource patterns.*

<br>

Canonical: `infrastructure/src/deploy.ts` (207 LOC).

| [INDEX] | [LINES]     | [SYMBOL]                     | [PURPOSE]                                                       |
| :-----: | ----------- | ---------------------------- | --------------------------------------------------------------- |
|   [1]   | **14**      | `_CONFIG.images`             | Image tags (`:latest` -- pin for production).                   |
|   [2]   | **22**      | `_CONFIG.ports`              | alloyGrpc:4317, alloyHttp:4318, alloyMetrics:12345, prom:9090.  |
|   [3]   | **29-36**   | `_Ops.alloy(promUrl)`        | Alloy config: OTLP receiver, `prometheus.remote_write`, debug.  |
|   [4]   | **59**      | `_Ops.grafana(promUrl)`      | Prometheus datasource provisioning YAML.                        |
|   [5]   | **63**      | `_Ops.meta(ns,component,n?)` | Metadata factory with `stack: 'parametric'`, `tier: 'observe'`. |
|   [6]   | **71**      | `_Ops.prometheus(alloyHost)` | Scrape config: 15s interval, alloy:12345 + localhost:9090.      |
|   [7]   | **120-126** | `_k8sObserve(ns, items)`     | Array-driven factory: PVC + ConfigMap + Deployment + Service.   |

<br>

### [1.1][DATA_FLOW]

```
App (Effect OTEL) --OTLP--> Alloy(:4317/:4318) --remote_write--> Prometheus(:9090)
                                    |--debug sink--> (logs discarded)
                                    \--debug sink--> (traces discarded)
Grafana(:3000) --PromQL--> Prometheus(:9090)
```

---
## [2][GENERATION]
>**Dictum:** *Cloud and selfhosted share topology; differ in resource types.*

<br>

| [INDEX] | [MODE]           | [INFRASTRUCTURE]   | [LINES] | [USE_CASE]                  |
| :-----: | ---------------- | ------------------ | ------- | --------------------------- |
|   [1]   | **`cloud`**      | K8s (EKS/GKE/AKS). | 131-176 | Production, multi-node, HA. |
|   [2]   | **`selfhosted`** | Docker containers. | 178-194 | Dev, single-node, staging.  |

**Cloud (deploy.ts:147-154):**
- Alloy: ConfigMap + DaemonSet + Service (3 ports: grpc:4317, http:4318, metrics:12345). Resources: `200m/256Mi` limits, `100m/128Mi` requests.
- `_k8sObserve` array: prometheus (cmd flags, 9090, PVC) + grafana (datasource provisioning, 3000, PVC).

**Selfhosted (deploy.ts:187-189):**
- 3 `docker.Container` resources with `uploads` (config) + named volumes via `_Ops.dockerVol`.
- Grafana: `GF_SECURITY_ADMIN_PASSWORD` from `_Ops.secret()`. Shared network via `_Ops.dockerNets(networkId)`.

All resources: Pulumi TypeScript. Never raw YAML, Helm, or docker-compose.

---
## [3][VALIDATION]
>**Dictum:** *Validation gates prevent broken observability pipelines.*

<br>

| [INDEX] | [CHECK]                                 | [SCOPE]       |
| :-----: | --------------------------------------- | ------------- |
|   [1]   | **Alloy OTLP ports 4317/4318 exposed.** | All.          |
|   [2]   | **Alloy metrics port 12345 exposed.**   | All.          |
|   [3]   | **Prometheus scrapes all components.**  | All.          |
|   [4]   | **Grafana datasource provisioned.**     | All.          |
|   [5]   | **Resource requests/limits set.**       | Cloud.        |
|   [6]   | **Named volumes for stateful data.**    | Selfhosted.   |
|   [7]   | **TLS for inter-component traffic.**    | Cloud (prod). |

---
## [4][PRODUCTION]
>**Dictum:** *Production gaps require explicit acknowledgment.*

<br>

| [INDEX] | [CONCERN]             | [STATUS]                  | [RECOMMENDATION]                                       |
| :-----: | --------------------- | ------------------------- | ------------------------------------------------------ |
|   [1]   | **TLS**               | Not configured.           | cert-manager or AWS ACM for inter-component comms.     |
|   [2]   | **Security contexts** | Missing on observe pods.  | `runAsNonRoot: true`, `readOnlyRootFilesystem: true`.  |
|   [3]   | **Image tags**        | `:latest` (deploy.ts:14). | Pin to specific versions for production.               |
|   [4]   | **NetworkPolicies**   | Not defined.              | Restrict Alloy<-App, Prometheus<-Alloy, Grafana->Prom. |
|   [5]   | **Resource limits**   | Alloy only.               | Add to Prometheus/Grafana via `_k8sObserve` extension. |

---
## [5][DEPRECATIONS]
>**Dictum:** *Deprecated components require migration paths.*

<br>

| [INDEX] | [DEPRECATED]                  | [REPLACEMENT]                 | [STATUS]             |
| :-----: | ----------------------------- | ----------------------------- | -------------------- |
|   [1]   | **Promtail**                  | Alloy.                        | EOL March 2, 2026.   |
|   [2]   | **`lokiexporter`**            | `otlphttp`.                   | Removed OTEL 0.140+. |
|   [3]   | **Standalone OTEL Collector** | Alloy (includes v0.142.0).    | Superseded.          |
|   [4]   | **River syntax (name)**       | "Alloy configuration syntax". | Renamed Alloy 1.8+.  |

---
## [6][EXTENSION_LOKI_TEMPO]
>**Dictum:** *Full 3-signal integration extends the metrics-only default.*

<br>

| [INDEX] | [SIGNAL]           | [IMAGE]                | [ALLOY_CHANGE]                   | [RUNTIME_ENV]                |
| :-----: | ------------------ | ---------------------- | -------------------------------- | ---------------------------- |
|   [1]   | **Logs (Loki)**    | `grafana/loki:3.6.x`.  | debug -> loki exporter.          | `OTEL_LOGS_EXPORTER=otlp`.   |
|   [2]   | **Traces (Tempo)** | `grafana/tempo:2.7.x`. | debug -> otlp exporter to Tempo. | `OTEL_TRACES_EXPORTER=otlp`. |

[REFERENCE] `references/stack_architecture.md#extension-adding-loki--tempo`.

---
## [7][REFERENCES]
>**Dictum:** *Reference files provide detailed implementation patterns.*

<br>

- `references/stack_architecture.md` -- Topology, sizing, Prometheus version matrix, Loki/Tempo extension.
- `references/alert_rules.md` -- Alert templates, recording rules (classic + native), ConfigMap provisioning.
- `references/grafana_dashboards.md` -- Dashboard panels (Grafana 12.3+, schema v2), native histogram heatmap.
