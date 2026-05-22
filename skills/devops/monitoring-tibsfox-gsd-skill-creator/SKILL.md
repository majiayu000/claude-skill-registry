---
name: openstack-monitoring
description: "OpenStack monitoring operations skill for deploying, configuring, and operating the cloud health monitoring stack. Covers Prometheus metric collection and scrape targets, Grafana dashboard provisioning and visualization, Alertmanager notification channels and routing, alerting rules for service health and resource exhaustion, service endpoint health checks, log aggregation strategies, SLA tracking with availability and response time percentiles, and capacity trend analysis from historical metrics. Use when deploying monitoring via Kolla-Ansible, configuring alert thresholds, troubleshooting blank dashboards, tuning noisy alerts, or analyzing cloud performance trends."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "monitoring"
          - "alerting"
          - "prometheus"
          - "grafana"
          - "metrics"
          - "dashboard"
          - "health check"
          - "SLA"
          - "uptime"
          - "log aggregation"
        contexts:
          - "monitoring openstack cloud"
          - "configuring alerts"
          - "troubleshooting monitoring"
          - "capacity trend analysis"
---

# OpenStack Monitoring Operations

Monitoring is the nervous system of a cloud deployment. Without it, operators fly blind -- problems are discovered by users instead of by automation. The monitoring stack provides continuous visibility into service health, resource utilization, and performance trends. When an operator asks "is the cloud healthy?" the answer comes from monitoring, not from guesswork.

The stack has three pillars: **Prometheus** collects and stores metrics (time-series data from every service, node, and container), **Grafana** visualizes those metrics (dashboards per service, alerting overview, capacity trends), and **Alertmanager** routes notifications when metrics cross thresholds (email, webhook, PagerDuty). Together they form a closed loop: collect, visualize, alert, act.

In NASA SE terms, monitoring maps to **Phase E (Operations & Sustainment)** -- continuous technical assessment through operational health monitoring, SLA tracking, and performance baseline comparison. The SURGEON agent is the primary consumer of this skill, using monitoring data for cloud health assessment. The GUARD agent consumes security-related metrics for posture evaluation.

## Deploy

### Kolla-Ansible Monitoring Deployment

**globals.yml settings:**

```yaml
# Enable monitoring stack
enable_prometheus: "yes"
enable_grafana: "yes"

# Optional: enable centralized logging
enable_central_logging: "yes"
enable_fluentd: "yes"

# Grafana admin credentials
grafana_admin_password: "{{ vault_grafana_admin_password }}"
```

**Deployment:**

```bash
# Deploy monitoring alongside other services
kolla-ansible -i inventory deploy --tags prometheus,grafana

# Or as part of full deployment
kolla-ansible -i inventory deploy
```

**Container verification:**

```bash
# Verify all monitoring containers are running
docker ps --filter "name=prometheus" --format "table {{.Names}}\t{{.Status}}"
docker ps --filter "name=grafana" --format "table {{.Names}}\t{{.Status}}"
docker ps --filter "name=alertmanager" --format "table {{.Names}}\t{{.Status}}"
docker ps --filter "name=node_exporter" --format "table {{.Names}}\t{{.Status}}"
# Expected: prometheus_server, grafana, alertmanager, node_exporter (all Up)

# Verify Prometheus is scraping targets
curl -s http://localhost:9090/api/v1/targets | python3 -m json.tool | head -20
# All targets should show "health": "up"
```

**Prometheus target configuration:**

Kolla-Ansible auto-configures scrape targets for deployed services. Verify the target list:

```bash
# Check active targets
curl -s http://localhost:9090/api/v1/targets | python3 -c "
import sys, json
data = json.load(sys.stdin)
for group in data['data']['activeTargets']:
    print(f\"{group['labels'].get('job','unknown'):30s} {group['health']:6s} {group['lastScrape']}\")
"
```

**Grafana data source setup:**

Kolla-Ansible registers Prometheus as the default Grafana data source. Verify:

```bash
# Check Grafana health
curl -s http://localhost:3000/api/health
# Expected: {"commit":"...","database":"ok","version":"..."}

# Check data source
curl -s -u admin:${GRAFANA_PASSWORD} http://localhost:3000/api/datasources
# Should list Prometheus data source
```

**Initial dashboard import:**

Kolla-Ansible ships default dashboards. For additional dashboards, use Grafana provisioning:

```bash
# Dashboards are stored in /etc/kolla/grafana/provisioning/dashboards/
# Add custom dashboards as JSON files to this directory
# Grafana auto-loads on container restart
docker restart grafana
```

## Configure

### Prometheus Scrape Targets

Configure scrape jobs for all OpenStack service endpoints and infrastructure components:

**OpenStack API endpoints (per-service):**

| Service | Exporter/Endpoint | Default Port | Metrics |
|---------|-------------------|--------------|---------|
| Keystone | keystone_exporter or /healthcheck | 5000 | Auth latency, token issuance rate |
| Nova | nova_exporter or API /os-services | 8774 | Instance count, hypervisor stats |
| Neutron | neutron_exporter or API /v2.0/agents | 9696 | Agent status, network/subnet counts |
| Cinder | cinder_exporter or API /os-services | 8776 | Volume count, snapshot stats |
| Glance | API /healthcheck | 9292 | Image count, upload throughput |
| Swift | swift_exporter | 8080 | Object count, container stats |
| Heat | API /healthcheck | 8004 | Stack count, operation success rate |
| Horizon | HTTP probe | 443 | Dashboard availability, response time |

**Infrastructure exporters:**

| Component | Exporter | Default Port | Key Metrics |
|-----------|----------|--------------|-------------|
| HAProxy | haproxy_exporter | 9101 | Backend status, request rate, error rate |
| MariaDB | mysqld_exporter | 9104 | Connections, query rate, replication lag |
| RabbitMQ | rabbitmq_exporter | 9419 | Queue depth, message rate, consumer count |
| Node | node_exporter | 9100 | CPU, memory, disk, network per host |
| Container | cAdvisor | 8080 | Container CPU/memory/network per service |

### Grafana Dashboard Provisioning

Organize dashboards by service domain:

**Per-service dashboards:**
- **Nova Compute:** Hypervisor utilization, instance lifecycle states, API latency, scheduler placement
- **Neutron Networking:** Agent health, network/port counts, floating IP utilization, bandwidth
- **Cinder Storage:** Volume provisioned/used, snapshot counts, IOPS, backend capacity
- **Keystone Auth:** Token issuance rate, auth latency, failed auth attempts, active sessions

**Infrastructure dashboards:**
- **Node Overview:** CPU, memory, disk I/O, network throughput per host
- **HAProxy:** Backend health, active connections, error rates, response codes
- **MariaDB:** Query rate, slow queries, connections, buffer pool usage
- **RabbitMQ:** Queue depth, message throughput, consumer status, memory usage

### Alertmanager Configuration

**Notification channels:**

```yaml
# /etc/kolla/prometheus/alertmanager.yml
route:
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
    - match:
        severity: warning
      receiver: 'email-ops'

receivers:
  - name: 'default'
    email_configs:
      - to: 'ops-team@example.com'
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<pagerduty-integration-key>'
  - name: 'email-ops'
    email_configs:
      - to: 'ops-team@example.com'
        send_resolved: true
```

### Alert Rule Definitions

**Service health alerts:**

```yaml
# /etc/kolla/prometheus/rules/service-health.yml
groups:
  - name: openstack_services
    rules:
      - alert: ServiceDown
        expr: up{job=~"openstack-.*"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been unreachable for 2 minutes"

      - alert: HighAPILatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API latency on {{ $labels.job }}"

      - alert: ResourceExhaustion
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Disk space below 10% on {{ $labels.instance }}"

      - alert: CertificateExpiringSoon
        expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 30
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "TLS certificate expires within 30 days on {{ $labels.instance }}"
```

### Retention and Storage Sizing

**Prometheus retention:**

```yaml
# prometheus.yml or command-line flags
--storage.tsdb.retention.time=30d    # Keep 30 days of data
--storage.tsdb.retention.size=50GB   # Or cap at 50GB, whichever hits first
```

**Storage estimate:** ~2 bytes per sample. With 1000 time series at 15s scrape interval, expect ~350MB/day. For a typical OpenStack deployment with full exporters: plan 1-2GB/day.

## Operate

### Health Check Procedures

**Daily checks:**

```bash
# 1. Verify Prometheus is scraping all targets
curl -s http://localhost:9090/api/v1/targets | python3 -c "
import sys, json
data = json.load(sys.stdin)
down = [t for t in data['data']['activeTargets'] if t['health'] != 'up']
print(f'Targets down: {len(down)}')
for t in down: print(f'  - {t[\"labels\"].get(\"job\")}: {t[\"lastError\"]}')
"

# 2. Check Alertmanager for active alerts
curl -s http://localhost:9093/api/v2/alerts | python3 -c "
import sys, json
alerts = json.load(sys.stdin)
print(f'Active alerts: {len(alerts)}')
for a in alerts: print(f'  [{a[\"labels\"][\"severity\"]}] {a[\"labels\"][\"alertname\"]}: {a[\"annotations\"].get(\"summary\",\"\")}')
"

# 3. Verify Grafana is accessible
curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/api/health
# Expected: 200
```

**Weekly checks:**
- Review alert history for false positives; adjust thresholds as needed
- Check Prometheus storage usage: `curl -s http://localhost:9090/api/v1/status/tsdb`
- Verify all Grafana dashboards load without errors
- Review SLA metrics against targets

**Monthly checks:**
- Validate retention policy is enforcing correctly (oldest data purged)
- Review and update alert rules for any new services or changed thresholds
- Export SLA report for stakeholders
- Compare current baselines against previous month for trend analysis

### SLA Reporting

```bash
# API availability (percentage of time each endpoint returns 2xx/3xx)
# Query Prometheus for service uptime over 30 days
curl -s "http://localhost:9090/api/v1/query?query=avg_over_time(up{job=~'openstack-.*'}[30d])*100"

# Response time percentiles (95th percentile over 30 days)
curl -s "http://localhost:9090/api/v1/query?query=histogram_quantile(0.95,rate(http_request_duration_seconds_bucket{job=~'openstack-.*'}[30d]))"
```

### Alert Tuning

**Reducing noise:**
- Increase `for` duration on flapping services (e.g., 2m to 5m)
- Use `group_wait` and `group_interval` to batch related alerts
- Add `inhibit_rules` to suppress downstream alerts when root cause is firing
- Use recording rules to pre-compute expensive queries

**Adjusting thresholds:**
- Review 7-day metric history before changing thresholds
- Use Grafana annotations to correlate threshold changes with alert volume

### Prometheus Rule Reloading

```bash
# After editing rules files, reload without restart
curl -X POST http://localhost:9090/-/reload
# Verify: curl -s http://localhost:9090/api/v1/rules | python3 -m json.tool | head
```

### Capacity Trend Analysis

Use Prometheus historical data for forward-looking capacity planning:

```promql
# Disk usage growth rate (GB/day) over past 30 days
deriv(node_filesystem_avail_bytes{mountpoint="/"}[30d]) / (1024^3) * 86400

# Memory utilization trend
predict_linear(node_memory_MemAvailable_bytes[30d], 86400*90)
# Predicts memory availability 90 days from now

# Instance density trend
deriv(openstack_nova_running_vms[30d]) * 86400
# VMs added per day
```

## Troubleshoot

### 1. Prometheus Scrape Failures

**Symptoms:** Targets show "down" in Prometheus UI. Gaps in metric graphs.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Target unreachable | `curl -v http://<target>:<port>/metrics` -- connection refused or timeout | Verify container running: `docker ps`; check port binding; verify network connectivity |
| TLS certificate mismatch | Prometheus logs: `tls: bad certificate` or `x509: certificate signed by unknown authority` | Add CA cert to Prometheus config: `tls_config.ca_file`; or set `insecure_skip_verify: true` for internal |
| Firewall rules blocking | `iptables -L -n` or `firewall-cmd --list-all` -- exporter port not open | Open port: `firewall-cmd --add-port=9100/tcp --permanent && firewall-cmd --reload` |
| Authentication required | HTTP 401 in Prometheus logs | Add `basic_auth` to scrape config with correct credentials |
| Scrape timeout | Prometheus logs: `context deadline exceeded` | Increase `scrape_timeout` in job config (default 10s) |

### 2. Grafana Dashboard Blank / No Data

**Symptoms:** Dashboard panels show "No data" or "N/A". Time series graphs are empty.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Data source misconfigured | Grafana > Settings > Data Sources > Test | Correct Prometheus URL (typically `http://prometheus:9090`) |
| Prometheus not running | `docker ps --filter name=prometheus` | `docker restart prometheus_server` |
| Time range mismatch | Dashboard time picker shows future or very old range | Set to "Last 1 hour" and verify data exists |
| Metric name changed | Query editor shows red error | Check available metrics: Explore > Metrics browser; update query |
| Dashboard variable empty | Template variables at top show "---" | Edit variable query; ensure label values exist |

### 3. Alert Storms (Excessive Notifications)

**Symptoms:** Hundreds of alerts in minutes. Ops team overwhelmed with notifications.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Threshold too sensitive | Alert history shows constant firing/resolving cycle | Increase `for` duration (2m to 10m); widen threshold band |
| Service flapping | Up/down oscillation in metrics graph | Investigate root cause (resource starvation, network instability); add hysteresis |
| Missing inhibition rules | Root cause + all downstream alerts fire simultaneously | Add `inhibit_rules` in alertmanager.yml to suppress child alerts |
| Group settings too aggressive | `group_wait: 0s` sends individual alerts | Set `group_wait: 30s`, `group_interval: 5m` |

### 4. High Cardinality Metric Explosion

**Symptoms:** Prometheus memory usage spiking. Queries timing out. TSDB compaction errors.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Unbounded labels (user IDs, request IDs) | `prometheus_tsdb_head_series` count growing rapidly | Remove high-cardinality labels from metrics; use `metric_relabel_configs` to drop |
| Too many scrape targets | Target count in UI vastly exceeds expected | Consolidate exporters; reduce scrape frequency for low-priority targets |
| Recording rules generating series | `prometheus_rule_group_rules` count high | Audit recording rules; remove unused aggregations |

### 5. Node Exporter Not Reporting

**Symptoms:** Host-level metrics missing (CPU, memory, disk). Node dashboard empty.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Container not running | `docker ps --filter name=node_exporter` empty | `docker restart node_exporter` or redeploy: `kolla-ansible deploy --tags prometheus` |
| Port conflict | `ss -tlnp | grep 9100` shows different process | Change node_exporter port or stop conflicting process |
| Wrong network namespace | Exporter running but Prometheus cannot reach it | Verify exporter is on management network; check docker network settings |

### 6. Missing Metrics After Upgrade

**Symptoms:** Dashboards break after OpenStack or monitoring stack upgrade. Queries return empty.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Scrape config drift | Compare pre/post upgrade Prometheus config | Regenerate config: `kolla-ansible reconfigure --tags prometheus` |
| Renamed metrics | Old metric names return empty; new names available in Explore | Update dashboard queries to new metric names; use `metric_relabel_configs` for aliases |
| Exporter version mismatch | Exporter changelog shows breaking changes | Update dashboards to match new exporter version; import compatible dashboard JSON |

## Integration Points

Monitoring connects to every layer of the cloud operations stack:

**Core OpenStack services:** Monitors all 8 service endpoints for health (up/down), latency (request duration histograms), and error rates (4xx/5xx response codes). Each service has dedicated scrape targets and dashboard panels.

**Security skill:** Security event alerting -- failed authentication spikes, certificate expiry countdown, unauthorized API access patterns. Certificate monitoring feeds GUARD agent security posture assessment.

**Capacity skill:** Resource utilization metrics (CPU, memory, disk, network per host and per instance) feed capacity planning models. Prometheus `predict_linear()` enables forward-looking capacity projections.

**Backup skill:** Monitors backup job execution -- success/failure status, duration, storage consumption. Alerts on backup failures or missed backup windows.

**Networking-debug skill:** Network metric collection (interface throughput, packet drops, OVS flow counts) provides data for SDN troubleshooting. Neutron agent health monitoring detects network control plane issues.

**Kolla-ansible-ops skill:** Monitors deployment and reconfigure operations -- container restart counts, deployment duration, configuration drift detection.

**SURGEON agent:** Primary consumer. SURGEON queries Prometheus for cloud health assessment: "Are all services up? Any active critical alerts? Any trending toward resource exhaustion?" Monitoring data is SURGEON's primary diagnostic input.

**GUARD agent:** Consumes security-related metrics for posture evaluation: failed auth rates, certificate status, API error patterns, unauthorized access attempts.

## NASA SE Cross-References

| SE Phase | Monitoring Activity | Reference |
|----------|---------------------|-----------|
| Phase D (Integration & Test) | Establish performance baseline metrics during integration testing; record initial scrape target health as verification evidence | SP-6105 SS 5.2-5.3 |
| Phase E (Operations & Sustainment) | Continuous operational health monitoring, SLA tracking against MOPs/MOEs, alert management, capacity trend analysis | SP-6105 SS 5.4-5.5, NPR 7123.1 SS 5.4 |
| Phase E (Technical Assessment) | Life-cycle health review using monitoring dashboards; compare current performance against established baselines | SP-6105 SS 6.7 |
| Phase F (Closeout) | Archive monitoring data (Prometheus snapshots) as operational record; export SLA reports for mission retrospective | SP-6105 SS 6.1 |
