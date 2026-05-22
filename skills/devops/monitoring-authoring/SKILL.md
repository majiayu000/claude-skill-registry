---
name: monitoring-authoring
description: |
  Author monitoring resources: PrometheusRules, ServiceMonitors, PodMonitors,
  AlertmanagerConfig, Silence CRs, and canary-checker health checks.

  Use when: (1) Creating or modifying alert rules (PrometheusRule), (2) Adding scrape targets
  (ServiceMonitor/PodMonitor), (3) Configuring Alertmanager routing or silences,
  (4) Writing canary-checker health checks, (5) Creating recording rules,
  (6) Adding monitoring for a new application or platform component.

  Triggers: "create alert", "add alerting", "PrometheusRule", "ServiceMonitor", "PodMonitor",
  "AlertmanagerConfig", "silence alert", "canary check", "recording rule", "add monitoring",
  "scrape target", "alert rule", "prometheus rule", "health check canary"
user-invocable: false
---

# Monitoring Resource Authoring

This skill covers **creating and modifying** monitoring resources. For **querying** Prometheus
or investigating alerts, see the [prometheus skill](../prometheus/SKILL.md) and
[sre skill](../sre/SKILL.md).

## Resource Types Overview

| Resource | API Group | Purpose | CRD Provider |
|----------|-----------|---------|--------------|
| `PrometheusRule` | `monitoring.coreos.com/v1` | Alert rules and recording rules | kube-prometheus-stack |
| `ServiceMonitor` | `monitoring.coreos.com/v1` | Scrape metrics from Services | kube-prometheus-stack |
| `PodMonitor` | `monitoring.coreos.com/v1` | Scrape metrics from Pods directly | kube-prometheus-stack |
| `ScrapeConfig` | `monitoring.coreos.com/v1alpha1` | Advanced scrape configuration (relabeling, multi-target) | kube-prometheus-stack |
| `AlertmanagerConfig` | `monitoring.coreos.com/v1alpha1` | Routing, receivers, silencing | kube-prometheus-stack |
| `Silence` | `observability.giantswarm.io/v1alpha2` | Declarative Alertmanager silences | silence-operator |
| `Canary` | `canaries.flanksource.com/v1` | Synthetic health checks (HTTP, TCP, K8s) | canary-checker |

---

## File Placement

Monitoring resources go in different locations depending on scope:

| Scope | Path | When to Use |
|-------|------|-------------|
| Platform-wide alerts/monitors | `kubernetes/platform/config/monitoring/` | Alerts for platform components (Cilium, Istio, cert-manager, etc.) |
| Subsystem-specific alerts | `kubernetes/platform/config/<subsystem>/` | Alerts bundled with the subsystem they monitor (e.g., `dragonfly/prometheus-rules.yaml`) |
| Cluster-specific silences | `kubernetes/clusters/<cluster>/config/silences/` | Silences for known issues on specific clusters |
| Cluster-specific alerts | `kubernetes/clusters/<cluster>/config/` | Alerts that only apply to a specific cluster |
| Canary health checks | `kubernetes/platform/config/canary-checker/` | Platform-wide synthetic checks |

### File Naming Conventions

Observed patterns in the `config/monitoring/` directory:

| Pattern | Example | When |
|---------|---------|------|
| `<component>-alerts.yaml` | `cilium-alerts.yaml`, `grafana-alerts.yaml` | PrometheusRule files |
| `<component>-recording-rules.yaml` | `loki-mixin-recording-rules.yaml` | Recording rules |
| `<component>-servicemonitors.yaml` | `istio-servicemonitors.yaml` | ServiceMonitor/PodMonitor files |
| `<component>-canary.yaml` | `alertmanager-canary.yaml` | Canary health checks |
| `<component>-route.yaml` | `grafana-route.yaml` | HTTPRoute for gateway access |
| `<component>-secret.yaml` | `discord-secret.yaml` | ExternalSecrets for monitoring |
| `<component>-scrape.yaml` | `hardware-monitoring-scrape.yaml` | ScrapeConfig resources |

### Registration

After creating a file in `config/monitoring/`, add it to the kustomization:

```yaml
# kubernetes/platform/config/monitoring/kustomization.yaml
resources:
  - ...existing resources...
  - my-new-alerts.yaml    # Add alphabetically by component
```

For subsystem-specific alerts (e.g., `config/dragonfly/prometheus-rules.yaml`), add to that
subsystem's `kustomization.yaml` instead.

---

## PrometheusRule Authoring

### Required Structure

Every PrometheusRule must include the `release: kube-prometheus-stack` label for Prometheus
to discover it. The YAML schema comment enables editor validation.

```yaml
---
# yaml-language-server: $schema=https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/monitoring.coreos.com/prometheusrule_v1.json
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: <component>-alerts
  labels:
    app.kubernetes.io/name: <component>
    release: kube-prometheus-stack    # REQUIRED - Prometheus selector
spec:
  groups:
    - name: <component>.rules        # or <component>-<subsystem> for sub-groups
      rules:
        - alert: AlertName
          expr: <PromQL expression>
          for: 5m
          labels:
            severity: critical        # critical | warning | info
          annotations:
            summary: "Short human-readable summary with {{ $labels.instance }}"
            description: >-
              Detailed explanation of what is happening, what it means,
              and what to investigate. Use template variables for context.
```

### Label Requirements

| Label | Required | Purpose |
|-------|----------|---------|
| `release: kube-prometheus-stack` | **Yes** | Prometheus discovery selector |
| `app.kubernetes.io/name: <component>` | Recommended | Organizational grouping |

Some files use additional labels like `prometheus: kube-prometheus-stack` (e.g., dragonfly),
but `release: kube-prometheus-stack` is the critical one for discovery.

### Severity Conventions

| Severity | `for` Duration | Use Case | Alertmanager Routing |
|----------|----------------|----------|---------------------|
| `critical` | 2m-5m | Service down, data loss risk, immediate action needed | Routed to Discord |
| `warning` | 5m-15m | Degraded performance, approaching limits, needs attention | Default receiver (Discord) |
| `info` | 10m-30m | Informational, capacity planning, non-urgent | Silenced by InfoInhibitor |

**Guidelines for `for` duration:**

- Shorter `for` = faster alert, more noise. Longer = quieter, slower response.
- `for: 0m` (immediate) only for truly instant failures (e.g., SMART health check fail).
- Most alerts: 5m is a good default.
- Flap-prone metrics (error rates, latency): 10m-15m to avoid false positives.
- Absence detection: 5m (metric may genuinely disappear briefly during restarts).

### Annotation Templates

Standard annotations used across this repository:

```yaml
annotations:
  summary: "Short title with {{ $labels.relevant_label }}"
  description: >-
    Multi-line description explaining what happened, the impact,
    and what to investigate. Reference threshold values and current
    values using template functions.
  runbook_url: "https://github.com/ionfury/homelab/blob/main/docs/runbooks/<runbook>.md"
```

The `runbook_url` annotation is optional but recommended for critical alerts that have
established recovery procedures.

### PromQL Template Functions

Functions available in `summary` and `description` annotations:

| Function | Input | Output | Example |
|----------|-------|--------|---------|
| `humanize` | Number | Human-readable number | `{{ $value \| humanize }}` -> "1.234k" |
| `humanizePercentage` | Float (0-1) | Percentage string | `{{ $value \| humanizePercentage }}` -> "45.6%" |
| `humanizeDuration` | Seconds | Duration string | `{{ $value \| humanizeDuration }}` -> "2h 30m" |
| `printf` | Format string | Formatted value | `{{ printf "%.2f" $value }}` -> "1.23" |

### Label Variables in Annotations

Access alert labels via `{{ $labels.<label_name> }}` and the expression value via `{{ $value }}`:

```yaml
summary: "Cilium agent down on {{ $labels.instance }}"
description: >-
  BPF map {{ $labels.map_name }} on {{ $labels.instance }} is at
  {{ $value | humanizePercentage }}.
```

### Common Alert Patterns

**Target down (availability):**
```yaml
- alert: <Component>Down
  expr: up{job="<job-name>"} == 0
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "<Component> is down on {{ $labels.instance }}"
```

**Absence detection (component disappeared entirely):**
```yaml
- alert: <Component>Down
  expr: absent(up{job="<job-name>"} == 1)
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "<Component> is unavailable"
```

**Error rate (ratio):**
```yaml
- alert: <Component>HighErrorRate
  expr: |
    (
      sum(rate(http_requests_total{job="<job>",status=~"5.."}[5m]))
      /
      sum(rate(http_requests_total{job="<job>"}[5m]))
    ) > 0.05
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "<Component> error rate above 5%"
    description: "Error rate is {{ $value | humanizePercentage }}"
```

**Latency (histogram quantile):**
```yaml
- alert: <Component>HighLatency
  expr: |
    histogram_quantile(0.99,
      sum(rate(http_request_duration_seconds_bucket{job="<job>"}[5m])) by (le)
    ) > 1
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "<Component> p99 latency above 1s"
    description: "P99 latency is {{ $value | humanizeDuration }}"
```

**Resource pressure (capacity):**
```yaml
- alert: <Component>ResourcePressure
  expr: <resource_used> / <resource_total> > 0.9
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "<Component> at {{ $value | humanizePercentage }} capacity"
```

**PVC space low:**
```yaml
- alert: <Component>PVCLow
  expr: |
    kubelet_volume_stats_available_bytes{persistentvolumeclaim=~".*<component>.*"}
    /
    kubelet_volume_stats_capacity_bytes{persistentvolumeclaim=~".*<component>.*"}
    < 0.15
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "PVC {{ $labels.persistentvolumeclaim }} running low"
    description: "{{ $value | humanizePercentage }} free space remaining"
```

### Alert Grouping

Group related alerts in named rule groups. The `name` field groups alerts in the Prometheus
UI and affects evaluation order:

```yaml
spec:
  groups:
    - name: cilium-agent       # Agent availability and health
      rules: [...]
    - name: cilium-bpf         # BPF subsystem alerts
      rules: [...]
    - name: cilium-policy      # Network policy alerts
      rules: [...]
    - name: cilium-network     # General networking alerts
      rules: [...]
```

---

## Recording Rules

Recording rules pre-compute expensive queries for dashboard performance. Place them alongside
alerts in the same PrometheusRule file or in a dedicated `*-recording-rules.yaml` file.

```yaml
spec:
  groups:
    - name: <component>-recording-rules
      rules:
        - record: <namespace>:<metric>:<aggregation>
          expr: |
            <PromQL aggregation query>
```

### Naming Convention

Recording rule names follow the pattern `level:metric:operations`:

```
loki:request_duration_seconds:p99
loki:requests_total:rate5m
loki:requests_error_rate:ratio5m
```

### When to Create Recording Rules

- Dashboard queries that aggregate across many series (e.g., sum/rate across all pods)
- Queries used by multiple alerts (avoids redundant computation)
- Complex multi-step computations that are hard to read inline

### Example: Loki Recording Rules

```yaml
- record: loki:request_duration_seconds:p99
  expr: |
    histogram_quantile(0.99,
      sum(rate(loki_request_duration_seconds_bucket[5m])) by (le, job, namespace)
    )

- record: loki:requests_error_rate:ratio5m
  expr: |
    sum(rate(loki_request_duration_seconds_count{status_code=~"5.."}[5m])) by (job, namespace)
    /
    sum(rate(loki_request_duration_seconds_count[5m])) by (job, namespace)
```

---

## ServiceMonitor and PodMonitor

### Via Helm Values (Preferred)

Most charts support enabling ServiceMonitor through values. Always prefer this over manual resources:

```yaml
# kubernetes/platform/charts/<app-name>.yaml
serviceMonitor:
  enabled: true
  interval: 30s
  scrapeTimeout: 10s
```

### Manual ServiceMonitor

When a chart does not support ServiceMonitor creation, create one manually. The resource
lives in the `monitoring` namespace and uses `namespaceSelector` to reach across namespaces.

```yaml
---
# yaml-language-server: $schema=https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/monitoring.coreos.com/servicemonitor_v1.json
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: <component>
  namespace: monitoring
  labels:
    release: kube-prometheus-stack    # REQUIRED for discovery
spec:
  namespaceSelector:
    matchNames:
      - <target-namespace>            # Namespace where the service lives
  selector:
    matchLabels:
      app.kubernetes.io/name: <component>   # Must match service labels
  endpoints:
    - port: http-monitoring           # Must match service port name
      path: /metrics
      interval: 30s
```

### Manual PodMonitor

Use PodMonitor when pods expose metrics but don't have a Service (e.g., DaemonSets, sidecars):

```yaml
---
# yaml-language-server: $schema=https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/monitoring.coreos.com/podmonitor_v1.json
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: <component>
  namespace: monitoring
  labels:
    release: kube-prometheus-stack    # REQUIRED for discovery
spec:
  namespaceSelector:
    matchNames:
      - <target-namespace>
  selector:
    matchLabels:
      app: <component>
  podMetricsEndpoints:
    - port: "15020"                   # Port name or number (quoted if numeric)
      path: /stats/prometheus
      interval: 30s
```

### Cross-Namespace Pattern

All ServiceMonitors and PodMonitors in this repo live in the `monitoring` namespace and use
`namespaceSelector` to reach pods in other namespaces. This centralizes monitoring configuration
and avoids needing `release: kube-prometheus-stack` labels on resources in app namespaces.

### Advanced: matchExpressions

For selecting multiple pod labels (e.g., all Flux controllers):

```yaml
selector:
  matchExpressions:
    - key: app
      operator: In
      values:
        - helm-controller
        - source-controller
        - kustomize-controller
```

---

## AlertmanagerConfig

The platform Alertmanager configuration lives in `config/monitoring/alertmanager-config.yaml`.
It defines routing and receivers for the entire platform.

### Current Routing Architecture

```
All alerts
  ├── InfoInhibitor → null receiver (silenced)
  ├── Watchdog → heartbeat receiver (webhook to healthchecks.io, every 2m)
  └── severity=critical → discord receiver
  └── (default) → discord receiver
```

### Receivers

| Receiver | Type | Purpose |
|----------|------|---------|
| `"null"` | None | Silences matched alerts (e.g., InfoInhibitor) |
| `heartbeat` | Webhook | Sends Watchdog heartbeat to healthchecks.io |
| `discord` | Discord webhook | Sends alerts to Discord channel |

### Adding a New Route

To route specific alerts differently (e.g., to a different channel or receiver), add a route
entry in the `alertmanager-config.yaml`:

```yaml
routes:
  - receiver: "<receiver-name>"
    matchers:
      - name: alertname
        value: "<AlertName>"
        matchType: =
```

### Secrets for Alertmanager

| Secret | Source | File |
|--------|--------|------|
| `alertmanager-discord-webhook` | ExternalSecret (AWS SSM) | `discord-secret.yaml` |
| `alertmanager-heartbeat-ping-url` | Replicated from `kube-system` | `heartbeat-secret.yaml` |

---

## Silence CRs (silence-operator)

Silences suppress known alerts declaratively. They are **per-cluster resources** because
different clusters have different expected alert profiles.

### Placement

```
kubernetes/clusters/<cluster>/config/silences/
  ├── kustomization.yaml
  └── <descriptive-name>.yaml
```

### Template

```yaml
---
# <Comment explaining WHY this alert is silenced>
apiVersion: observability.giantswarm.io/v1alpha2
kind: Silence
metadata:
  name: <descriptive-name>
  namespace: monitoring
spec:
  matchers:
    - name: alertname
      matchType: "=~"           # "=" exact, "=~" regex, "!=" negation, "!~" regex negation
      value: "Alert1|Alert2"
    - name: namespace
      matchType: "="
      value: <target-namespace>
```

### Matcher Reference

| matchType | Meaning | Example |
|-----------|---------|---------|
| `=` | Exact match | `value: "KubePodCrashLooping"` |
| `!=` | Not equal | `value: "Watchdog"` |
| `=~` | Regex match | `value: "KubePod.*\|TargetDown"` |
| `!~` | Regex negation | `value: "Info.*"` |

### Requirements

- **Always include a comment** explaining why the silence exists (architectural limitation, expected behavior, etc.)
- Every cluster must maintain a **zero firing alerts baseline** (excluding Watchdog)
- **Silences are a LAST RESORT** — every effort must be made to fix the root cause before resorting to a silence. Only silence when the alert genuinely cannot be fixed: architectural limitations (e.g., single-node Spegel), expected environmental behavior, or confirmed upstream bugs
- **Never leave alerts firing without action** — either fix the cause or create a Silence CR. An ignored alert degrades trust in the entire monitoring system and leads to alert fatigue where real incidents get missed

### Adding a Silence to a Cluster

1. Create `config/silences/` directory if it does not exist
2. Add the Silence YAML file
3. Create or update `config/silences/kustomization.yaml`:
   ```yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   resources:
     - <silence-name>.yaml
   ```
4. Reference `silences` in `config/kustomization.yaml`

---

## Canary Health Checks

Canary resources provide synthetic monitoring using [Flanksource canary-checker](https://canarychecker.io/).
They live in `config/canary-checker/` for platform checks or alongside app config for app-specific checks.

### HTTP Health Check

```yaml
---
# yaml-language-server: $schema=https://kubernetes-schemas.pages.dev/canaries.flanksource.com/canary_v1.json
apiVersion: canaries.flanksource.com/v1
kind: Canary
metadata:
  name: http-check-<component>
spec:
  schedule: "@every 1m"
  http:
    - name: <component>-health
      url: https://<component>.${internal_domain}/health
      responseCodes: [200]
      maxSSLExpiry: 7           # Alert if TLS cert expires within 7 days
      thresholdMillis: 5000     # Fail if response takes >5s
```

### TCP Port Check

```yaml
spec:
  schedule: "@every 1m"
  tcp:
    - name: <component>-port
      host: <service>.<namespace>.svc.cluster.local
      port: 8080
      timeout: 5000
```

### Kubernetes Resource Check with CEL

Test that pods are actually healthy using CEL expressions (preferred over `ready: true`
because the built-in flag penalizes pods with restart history):

```yaml
spec:
  interval: 60
  kubernetes:
    - name: <component>-pods-healthy
      kind: Pod
      namespaceSelector:
        name: <namespace>
      resource:
        labelSelector: app.kubernetes.io/name=<component>
      test:
        expr: >
          dyn(results).all(pod,
            pod.Object.status.phase == "Running" &&
            pod.Object.status.conditions.exists(c, c.type == "Ready" && c.status == "True")
          )
```

### Canary Metrics and Alerting

canary-checker exposes metrics that are already monitored by the platform:

- `canary_check == 1` triggers `CanaryCheckFailure` (critical, 2m)
- High failure rates trigger `CanaryCheckHighFailureRate` (warning, 5m)

These alerts are defined in `config/canary-checker/prometheus-rules.yaml` -- you do not
need to create separate alerts for each canary.

---

## Workflow: Adding Monitoring for a New Component

### Step 1: Determine What Exists

Check if the Helm chart already provides monitoring:

```bash
# Search chart values for monitoring options
kubesearch <chart-name> serviceMonitor
kubesearch <chart-name> prometheusRule
```

Enable via Helm values if available (see [deploy-app skill](../deploy-app/SKILL.md)).

### Step 2: Create Missing Resources

If the chart does not provide monitoring, create resources manually:

1. **ServiceMonitor** or **PodMonitor** for metrics scraping
2. **PrometheusRule** for alert rules
3. **Canary** for synthetic health checks (HTTP/TCP)

### Step 3: Place Files Correctly

- If the component has its own config subsystem (`config/<component>/`), add monitoring
  resources there alongside other config
- If it is a standalone monitoring addition, add to `config/monitoring/`

### Step 4: Register in Kustomization

Add new files to the appropriate `kustomization.yaml`.

### Step 5: Validate

```bash
task k8s:validate
```

### Step 6: Verify After Deployment

Prometheus is behind OAuth2 Proxy — use `kubectl exec` or port-forward for API queries:

```bash
# Check ServiceMonitor is discovered
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/targets' | \
  jq '.data.activeTargets[] | select(.labels.job | contains("<component>"))'

# Check alert rules are loaded
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/rules' | \
  jq '.data.groups[] | select(.name | contains("<component>"))'

# Check canary status
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get canaries -A | grep <component>
```

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing `release: kube-prometheus-stack` label | Prometheus ignores the resource | Add the label to metadata.labels |
| PrometheusRule in wrong namespace without namespaceSelector | Prometheus does not discover it | Place in `monitoring` namespace or ensure Prometheus watches the target namespace |
| ServiceMonitor selector does not match any service | No metrics scraped, no error raised | Verify labels match with `kubectl get svc -n <ns> --show-labels` |
| Using `ready: true` in canary-checker Kubernetes checks | False negatives after pod restarts | Use CEL `test.expr` instead |
| Hardcoding domains in canary URLs | Breaks across clusters | Use `${internal_domain}` substitution variable |
| Very short `for` duration on flappy metrics | Alert noise | Use 10m+ for error rates and latencies |
| Creating alerts for metrics that do not exist yet | Alert permanently in "pending" state | Verify metrics exist in Prometheus before writing rules |

---

## Reference: Existing Alert Files

| File | Component | Alert Count | Subsystem |
|------|-----------|-------------|-----------|
| `monitoring/cilium-alerts.yaml` | Cilium | 14 | Agent, BPF, Policy, Network |
| `monitoring/istio-alerts.yaml` | Istio | ~10 | Control plane, mTLS, Gateway |
| `monitoring/cert-manager-alerts.yaml` | cert-manager | 5 | Expiry, Renewal, Issuance |
| `monitoring/network-policy-alerts.yaml` | Network Policy | 2 | Enforcement escape hatch |
| `monitoring/external-secrets-alerts.yaml` | External Secrets | 3 | Sync, Ready, Store health |
| `monitoring/grafana-alerts.yaml` | Grafana | 4 | Datasource, Errors, Plugins, Down |
| `monitoring/loki-mixin-alerts.yaml` | Loki | ~5 | Requests, Latency, Ingester |
| `monitoring/alloy-alerts.yaml` | Alloy | 3 | Dropped entries, Errors, Lag |
| `monitoring/hardware-monitoring-alerts.yaml` | Hardware | 7 | Temperature, Fans, Disks, Power |
| `dragonfly/prometheus-rules.yaml` | Dragonfly | 2+ | Down, Memory |
| `canary-checker/prometheus-rules.yaml` | canary-checker | 2 | Check failure, High failure rate |

---

## Keywords

PrometheusRule, ServiceMonitor, PodMonitor, ScrapeConfig, AlertmanagerConfig, Silence,
silence-operator, canary-checker, Canary, recording rules, alert rules, monitoring,
observability, scrape targets, prometheus, alertmanager, discord, heartbeat
