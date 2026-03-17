# 🚨 Skill: Alerting & Incident Management

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-alerting-incident-management` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `alerting`, `incident-management`, `pagerduty`, `opsgenie`, `oncall`, `runbooks` |
| **Referencia** | [Google SRE - On-Call](https://sre.google/workbook/on-call/), [PagerDuty](https://www.pagerduty.com/) |

## 🔑 Keywords para Invocación

- `alerting`
- `incident-management`
- `pagerduty`
- `opsgenie`
- `oncall`
- `runbooks`
- `incident-response`
- `@skill:alerting`

### Ejemplos de Prompts

```
Implementa alerting con PagerDuty y runbooks
```

```
Configura incident management y on-call rotation
```

```
Configura runbooks y on-call rotation
```

```
@skill:alerting - Sistema completo de alertas e incidentes
```

## 📖 Descripción

Alerting efectivo y gestión de incidentes es crítico para mantener servicios confiables. Este skill cubre diseño de alertas efectivas, on-call rotations, runbooks, e incident response workflows.

### ✅ Cuándo Usar Este Skill

- Servicios en producción
- Equipos on-call
- SLAs críticos
- Sistemas distribuidos
- Incidentes frecuentes
- Compliance requirements

### ❌ Cuándo NO Usar Este Skill

- Desarrollo local solo
- Servicios no críticos sin SLA
- Equipos sin capacidad on-call

## 🏗️ Arquitectura de Alerting

```
┌──────────────┐
│  Prometheus  │
│  (Metrics)   │
└──────┬───────┘
       │
       │ Alert Rules
       │
┌──────▼───────┐
│ Alertmanager │
└──────┬───────┘
       │
       ├──────────┬──────────┬──────────┐
       │          │          │          │
┌──────▼───┐ ┌───▼────┐ ┌───▼────┐ ┌──▼─────┐
│ PagerDuty│ │ Slack  │ │ Email  │ │ Webhook│
└──────────┘ └────────┘ └────────┘ └────────┘
       │
       │
┌──────▼──────────────┐
│ On-Call Engineer    │
│ (Incident Response) │
└─────────────────────┘
```

## 💻 Implementación

### 1. Alertmanager Configuration

```yaml
# alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
  # Critical alerts → PagerDuty immediately
  - match:
      severity: critical
    receiver: 'pagerduty-critical'
    continue: true

  # Warning alerts → Slack only
  - match:
      severity: warning
    receiver: 'slack-warnings'
    repeat_interval: 24h

  # Service-specific routes
  - match:
      service: payment-service
    receiver: 'payment-team'
    group_wait: 5s

inhibit_rules:
  # Inhibit warning if critical is firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster', 'service']

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_SERVICE_KEY'
        description: '{{ .GroupLabels.alertname }}: {{ .GroupLabels.service }}'
        severity: 'critical'
        client: 'Prometheus'
        client_url: 'http://prometheus:9090'

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts-warnings'
        title: 'Warning: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'payment-team'
    pagerduty_configs:
      - service_key: 'PAYMENT_TEAM_KEY'
        description: 'Payment Service Alert'
    slack_configs:
      - channel: '#payment-team'
```

### 2. Alert Rules (Prometheus)

```yaml
# prometheus/alerts/service-alerts.yml
groups:
  - name: service_alerts
    interval: 30s
    rules:
      # Error Budget Exhaustion
      - alert: ErrorBudgetExhaustion
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          ) > 0.001
          and
          (
            sum_over_time(
              (
                sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
                /
                sum(rate(http_requests_total[5m])) by (service)
              )[28d:]
            ) > 0.001
          )
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "Error budget exhausted for {{ $labels.service }}"
          description: |
            Service {{ $labels.service }} has exceeded error budget threshold.
            Current error rate: {{ $value | humanizePercentage }}
            Runbook: https://runbooks.example.com/error-budget

      # High Latency
      - alert: HighLatencyP99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1.0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High P99 latency in {{ $labels.service }}"
          description: "P99 latency is {{ $value }}s (threshold: 1s)"
          runbook: https://runbooks.example.com/high-latency

      # Service Down
      - alert: ServiceDown
        expr: up{job=~"app-.*"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Service has been unreachable for more than 2 minutes"
          runbook: https://runbooks.example.com/service-down

      # High Memory Usage
      - alert: HighMemoryUsage
        expr: |
          (
            container_memory_usage_bytes{pod=~".+"}
            /
            container_spec_memory_limit_bytes{pod=~".+"}
          ) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage in {{ $labels.pod }}"
          description: "Memory usage is {{ $value | humanizePercentage }}"
          runbook: https://runbooks.example.com/high-memory

      # Disk Space
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) < 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"

      # CPU Throttling
      - alert: CPUThrottling
        expr: |
          rate(container_cpu_cfs_throttled_seconds_total[5m]) > 0.1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "CPU throttling detected in {{ $labels.pod }}"
          description: "Container is being CPU throttled"

      # Connection Pool Exhaustion
      - alert: ConnectionPoolExhaustion
        expr: |
          (
            db_connections_active{service=~".+"}
            /
            db_connections_max{service=~".+"}
          ) > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Connection pool near exhaustion in {{ $labels.service }}"
          description: "{{ $value | humanizePercentage }} of connections in use"
```

### 3. Runbook Template

```markdown
# Runbook: High Error Rate

## Alert Name
`HighErrorRate`

## Severity
Critical

## Description
Service error rate exceeds threshold (5% for 5 minutes)

## Symptoms
- High HTTP 5xx response rate
- User complaints
- Error logs increasing

## Immediate Actions

1. **Acknowledge Alert**
   - Acknowledge in PagerDuty/OpsGenie
   - Notify team in Slack

2. **Check Service Health**
   ```bash
   kubectl get pods -l app=service-name
   kubectl logs -l app=service-name --tail=100
   ```

3. **Check Metrics**
   - Grafana dashboard: `/d/service-overview`
   - Error rate graph
   - Latency graphs

4. **Identify Root Cause**
   - Check recent deployments
   - Review error logs
   - Check dependencies (DB, APIs)

## Resolution Steps

### If caused by code deployment:
```bash
# Rollback deployment
kubectl rollout undo deployment/service-name
```

### If caused by resource exhaustion:
```bash
# Scale up
kubectl scale deployment/service-name --replicas=5
```

### If caused by dependency failure:
1. Check dependency service status
2. Implement circuit breaker
3. Enable fallback mechanisms

## Post-Incident

- Document in incident log
- Update runbook if needed

## Escalation

- If not resolved in 15 min → Escalate to senior engineer
- If not resolved in 30 min → Escalate to engineering manager
- If service completely down → Escalate to CTO
```

### 4. On-Call Rotation (PagerDuty)

```yaml
# pagerduty/escalation-policies.yml
escalation_policies:
  - name: "Primary On-Call"
    description: "Primary escalation for production services"
    num_loops: 3
    escalation_rules:
      - escalation_delay_in_minutes: 0
        targets:
          - type: "user"
            id: "PXXXXXXXX"  # Primary on-call
      - escalation_delay_in_minutes: 15
        targets:
          - type: "user"
            id: "PYYYYYYYY"  # Secondary on-call
      - escalation_delay_in_minutes: 30
        targets:
          - type: "schedule"
            id: "PZZZZZZZZ"  # Manager on-call

  - name: "Critical Alerts Only"
    escalation_rules:
      - escalation_delay_in_minutes: 0
        targets:
          - type: "user_reference"
            id: "PXXXXXXXX"
      - escalation_delay_in_minutes: 10
        targets:
          - type: "escalation_policy_reference"
            id: "EPXXXXXXX"  # Manager escalation

schedules:
  - name: "Primary On-Call Schedule"
    time_zone: "America/New_York"
    layers:
      - name: "Layer 1"
        start: "2024-01-01T00:00:00"
        rotation_virtual_start: "2024-01-01T00:00:00"
        rotation_turn_length_seconds: 604800  # 1 week
        users:
          - user_id: "PXXXXXXXX"
          - user_id: "PYYYYYYYY"
          - user_id: "PZZZZZZZZ"
        restrictions:
          - type: "daily_restriction"
            start_time_of_day: "09:00:00"
            duration_seconds: 32400  # 9 hours
```

### 5. Incident Response Workflow

```python
# incident_response/workflow.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class IncidentSeverity(Enum):
    SEV1 = "critical"  # Service down
    SEV2 = "high"      # Major degradation
    SEV3 = "medium"    # Minor issues
    SEV4 = "low"       # Informational

@dataclass
class Incident:
    id: str
    title: str
    severity: IncidentSeverity
    status: str  # open, investigating, mitigated, resolved
    created_at: datetime
    resolved_at: Optional[datetime]
    assigned_to: str
    affected_services: List[str]
    description: str
    root_cause: Optional[str] = None
    resolution: Optional[str] = None

class IncidentResponseWorkflow:
    def __init__(self):
        self.incidents = []

    def create_incident(
        self,
        title: str,
        severity: IncidentSeverity,
        affected_services: List[str],
        description: str
    ) -> Incident:
        incident = Incident(
            id=f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            title=title,
            severity=severity,
            status="open",
            created_at=datetime.now(),
            resolved_at=None,
            assigned_to=self._assign_oncall(),
            affected_services=affected_services,
            description=description
        )
        
        self.incidents.append(incident)
        self._notify_team(incident)
        self._create_incident_channel(incident)
        
        return incident

    def _assign_oncall(self) -> str:
        # Logic to assign to current on-call engineer
        return "engineer@example.com"

    def _notify_team(self, incident: Incident):
        # Send notifications via PagerDuty, Slack, etc.
        pass

    def _create_incident_channel(self, incident: Incident):
        # Create dedicated Slack channel for incident
        channel_name = f"incident-{incident.id.lower()}"
        # Create channel logic
        pass

    def update_status(self, incident_id: str, status: str, notes: str):
        incident = self._find_incident(incident_id)
        if incident:
            incident.status = status
            if status == "resolved":
                incident.resolved_at = datetime.now()

    def _find_incident(self, incident_id: str) -> Optional[Incident]:
        return next((i for i in self.incidents if i.id == incident_id), None)
```

### 6. Alert Fatigue Prevention

```yaml
# alertmanager/alert-fatigue-prevention.yml
# Strategies to prevent alert fatigue

# 1. Alert Grouping
route:
  group_by: ['alertname', 'service']
  group_wait: 10s      # Wait before sending initial notification
  group_interval: 5m   # Wait before sending updated notification
  repeat_interval: 12h # Minimum time between notifications

# 2. Alert Inhibition
inhibit_rules:
  # Don't alert on warning if critical is firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['service']

  # Don't alert on individual instance if all instances are down
  - source_match:
      alertname: 'AllInstancesDown'
    target_match_re:
      alertname: '.*InstanceDown'

# 3. Alert Suppression (Silence Rules)
# Use Alertmanager UI or API to create silences for known issues

# 4. Threshold Tuning
# Use error budgets and SLOs to set meaningful thresholds
# Example: Alert only when error budget is at risk

# 5. Alert Classification
# Only page on actionable alerts
# Use different channels for different severities
```

## 🎯 Mejores Prácticas

### 1. Alert Design

✅ **DO:**
- Alert on symptoms, not causes
- Make alerts actionable
- Include runbook links
- Use appropriate severity levels
- Test alerts regularly

❌ **DON'T:**
- Alert on every metric
- Create alerts that require investigation to understand
- Alert on things you can't fix
- Duplicate alerts across systems

### 2. On-Call

✅ **DO:**
- Maintain clear rotation schedules
- Provide context in handoffs
- Limit on-call duration (max 1 week)
- Compensate on-call time
- Track on-call load

❌ **DON'T:**
- Have people on-call 24/7
- Make on-call mandatory without compensation
- Skip handoffs between rotations

### 3. Incident Response

✅ **DO:**
- Follow runbooks
- Communicate frequently
- Document decisions
- Implement action items

❌ **DON'T:**
- Skip incident documentation
- Point fingers
- Ignore post-mortem action items

## 🚨 Troubleshooting

### Too Many Alerts

1. Review alert rules
2. Increase thresholds where appropriate
3. Implement better grouping
4. Use alert inhibition

### Alerts Not Firing

1. Check Prometheus query syntax
2. Verify alert rule evaluation
3. Check Alertmanager configuration
4. Verify notification channel configs

### On-Call Burnout

1. Review alert volume
2. Reduce non-actionable alerts
3. Improve runbooks
4. Rotate more frequently

## 📚 Recursos Adicionales

- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Google SRE - On-Call Handbook](https://sre.google/workbook/on-call/)
- [Incident Response Guide](https://response.pagerduty.com/)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

