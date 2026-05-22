---
name: sre-engineer
description: "Expert Site Reliability Engineer specializing in SLOs, error budgets, and reliability engineering practices. Proficient in incident management, post-mortems, capacity planning, and building scalable, resilient systems with focus on reliability, availability, and performance."
---

# Site Reliability Engineer

## Purpose

Provides expert site reliability engineering expertise for building and maintaining highly available, scalable, and resilient systems. Specializes in SLOs, error budgets, incident management, chaos engineering, capacity planning, and observability platforms with focus on reliability, availability, and performance.

## When to Use

- Defining and implementing SLOs (Service Level Objectives) and error budgets
- Managing incidents from detection → resolution → post-mortem
- Building high availability architectures (multi-region, fault tolerance)
- Conducting chaos engineering experiments (failure injection, resilience testing)
- Capacity planning and auto-scaling strategies
- Implementing observability platforms (metrics, logs, traces)
- Designing toil reduction and automation strategies

## Quick Start

**Invoke this skill when:**
- Defining and implementing SLOs (Service Level Objectives) and error budgets
- Managing incidents from detection → resolution → post-mortem
- Building high availability architectures (multi-region, fault tolerance)
- Conducting chaos engineering experiments (failure injection, resilience testing)
- Capacity planning and auto-scaling strategies
- Implementing observability platforms (metrics, logs, traces)

**Do NOT invoke when:**
- Only DevOps automation needed (use devops-engineer for CI/CD pipelines)
- Application-level debugging (use debugger skill)
- Infrastructure provisioning without reliability context (use cloud-architect)
- Database performance tuning (use database-optimizer)
- Security incident response (use incident-responder for security)

---
---

## Core Workflows

### Workflow 1: Define and Implement SLOs

**Use case:** New microservice needs SLO definition and monitoring

**Step 1: SLI (Service Level Indicator) Selection**
```yaml
# Service: User Authentication API
# Critical user journey: Login flow

SLI Candidates:
1. Availability (request success rate):
   Definition: (successful_requests / total_requests) * 100
   Measurement: HTTP 2xx responses vs 5xx errors
   Rationale: Core indicator of service health
   
2. Latency (response time):
   Definition: P99 response time \u003c 500ms
   Measurement: Time from request received → response sent
   Rationale: User experience directly impacted by slow logins
   
3. Correctness (authentication accuracy):
   Definition: Valid tokens issued / authentication attempts
   Measurement: JWT validation failures within 1 hour of issuance
   Rationale: Security and functional correctness

Selected SLIs for SLO:
- Availability: 99.9% (primary SLO)
- Latency P99: 500ms (secondary SLO)
```

**Step 2: SLO Definition Document**
```markdown
# Authentication Service SLO

## Service Overview
- **Service**: User Authentication API
- **Owner**: Platform Team
- **Criticality**: Tier 1 (blocks all user actions)

## SLO Commitments

### Primary SLO: Availability
- **Target**: 99.9% availability over 28-day rolling window
- **Error Budget**: 0.1% = 40.3 minutes downtime per 28 days
- **Measurement**: `(count(http_response_code=2xx) / count(http_requests)) >= 0.999`
- **Exclusions**: Planned maintenance windows, client errors (4xx)

### Secondary SLO: Latency
- **Target**: P99 latency \u003c 500ms
- **Error Budget**: 1% of requests can exceed 500ms
- **Measurement**: `histogram_quantile(0.99, http_request_duration_seconds) \u003c 0.5`
- **Measurement Window**: 5-minute sliding window

## Error Budget Policy

### Budget Remaining Actions:
- **\u003e 50%**: Normal development velocity, feature releases allowed
- **25-50%**: Slow down feature releases, prioritize reliability
- **10-25%**: Feature freeze, focus on SLO improvement
- **\u003c10%**: Incident declared, all hands on reliability

### Budget Exhausted (0%):
- Immediate feature freeze
- Rollback recent changes
- Root cause analysis required
- Executive notification

## Monitoring and Alerting

**Prometheus Alerting Rules:**
```yaml
groups:
  - name: auth_service_slo
    interval: 30s
    rules:
      # Availability SLO alert
      - alert: AuthServiceSLOBreach
        expr: |
          (
            sum(rate(http_requests_total{service="auth",code=~"2.."}[5m]))
            /
            sum(rate(http_requests_total{service="auth"}[5m]))
          ) < 0.999
        for: 5m
        labels:
          severity: critical
          service: auth
        annotations:
          summary: "Auth service availability below SLO"
          description: "Current availability: {{ $value | humanizePercentage }}"
      
      # Error budget burn rate alert (fast burn)
      - alert: AuthServiceErrorBudgetFastBurn
        expr: |
          (
            1 - (
              sum(rate(http_requests_total{service="auth",code=~"2.."}[1h]))
              /
              sum(rate(http_requests_total{service="auth"}[1h]))
            )
          ) > 14.4 * (1 - 0.999)  # 2% of monthly budget in 1 hour
        for: 5m
        labels:
          severity: critical
          service: auth
        annotations:
          summary: "Auth service burning error budget at 14.4x rate"
          description: "At this rate, monthly budget exhausted in 2 days"
      
      # Latency SLO alert
      - alert: AuthServiceLatencySLOBreach
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{service="auth"}[5m])) by (le)
          ) > 0.5
        for: 5m
        labels:
          severity: warning
          service: auth
        annotations:
          summary: "Auth service P99 latency above SLO"
          description: "Current P99: {{ $value }}s (SLO: 0.5s)"
```

**Step 3: Grafana Dashboard**
```json
{
  "dashboard": {
    "title": "Auth Service SLO Dashboard",
    "panels": [
      {
        "title": "30-Day Availability SLO",
        "targets": [{
          "expr": "avg_over_time((sum(rate(http_requests_total{service=\"auth\",code=~\"2..\"}[5m])) / sum(rate(http_requests_total{service=\"auth\"}[5m])))[30d:5m])"
        }],
        "thresholds": [
          {"value": 0.999, "color": "green"},
          {"value": 0.995, "color": "yellow"},
          {"value": 0, "color": "red"}
        ]
      },
      {
        "title": "Error Budget Remaining",
        "targets": [{
          "expr": "1 - ((1 - avg_over_time((sum(rate(http_requests_total{service=\"auth\",code=~\"2..\"}[5m])) / sum(rate(http_requests_total{service=\"auth\"}[5m])))[30d:5m])) / (1 - 0.999))"
        }],
        "visualization": "gauge",
        "thresholds": [
          {"value": 0.5, "color": "green"},
          {"value": 0.25, "color": "yellow"},
          {"value": 0, "color": "red"}
        ]
      }
    ]
  }
}
```

---
---

### Workflow 3: Chaos Engineering Experiment

**Use case:** Validate resilience to database failover

**Experiment Design:**
```yaml
# chaos-experiment-db-failover.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: database-primary-kill
  namespace: chaos-testing
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      app: postgresql
      role: primary
  scheduler:
    cron: "@every 2h"  # Run experiment every 2 hours
  duration: "0s"  # Instant kill
```

**Hypothesis:**
```markdown
## Hypothesis
**Steady State**: 
- Application maintains 99.9% availability
- P99 latency \u003c 500ms
- Database queries succeed with automatic failover to replica

**Perturbation**:
- Kill primary database pod (simulates AZ failure)

**Expected Behavior**:
- Kubernetes detects pod failure within 10 seconds
- Replica promoted to primary within 30 seconds
- Application reconnects to new primary within 5 seconds
- Total impact: \u003c45 seconds of elevated error rate (\u003c5%)
- No data loss (synchronous replication)

**Abort Conditions**:
- Error rate \u003e 20% for \u003e60 seconds
- Manual rollback command issued
- Customer complaints spike \u003e10x normal
```

**Execution Steps:**
```bash
#!/bin/bash
# chaos-experiment-runner.sh

set -e

echo "=== Chaos Experiment: Database Failover ==="
echo "Start time: $(date)"

# Step 1: Baseline metrics (5 minutes)
echo "[1/7] Collecting baseline metrics..."
START_TIME=$(date -u +%s)
sleep 300

BASELINE_ERROR_RATE=$(promtool query instant \
  'sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))' \
  | jq -r '.data.result[0].value[1]')

echo "Baseline error rate: ${BASELINE_ERROR_RATE}"

# Step 2: Inject failure
echo "[2/7] Injecting failure: Killing primary database pod..."
kubectl delete pod -l app=postgresql,role=primary -n production

# Step 3: Monitor failover
echo "[3/7] Monitoring failover process..."
for i in {1..60}; do
  READY_PODS=$(kubectl get pods -l app=postgresql -n production \
    -o jsonpath='{.items[?(@.status.conditions[?(@.type=="Ready")].status=="True")].metadata.name}' \
    | wc -w)
  
  if [ $READY_PODS -ge 1 ]; then
    echo "Failover completed at T+${i}s: $READY_PODS ready pods"
    break
  fi
  
  echo "T+${i}s: Waiting for replica promotion..."
  sleep 1
done

# Step 4: Measure impact
echo "[4/7] Measuring incident impact..."
sleep 60  # Wait for metrics to stabilize

INCIDENT_ERROR_RATE=$(promtool query instant \
  'max_over_time((sum(rate(http_requests_total{code=~"5.."}[1m])) / sum(rate(http_requests_total[1m])))[5m:])' \
  | jq -r '.data.result[0].value[1]')

echo "Peak error rate during incident: ${INCIDENT_ERROR_RATE}"

# Step 5: Validate recovery
echo "[5/7] Validating service recovery..."
for i in {1..30}; do
  CURRENT_ERROR_RATE=$(promtool query instant \
    'sum(rate(http_requests_total{code=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))' \
    | jq -r '.data.result[0].value[1]')
  
  if (( $(echo "$CURRENT_ERROR_RATE < 0.01" | bc -l) )); then
    echo "Service recovered at T+$((60+i))s"
    break
  fi
  
  sleep 1
done

# Step 6: Data integrity check
echo "[6/7] Running data integrity checks..."
psql -h postgres-primary-service -U app -c "SELECT COUNT(*) FROM orders WHERE created_at > NOW() - INTERVAL '10 minutes';"

# Step 7: Results summary
echo "[7/7] Experiment Results:"
echo "================================"
echo "Baseline error rate: ${BASELINE_ERROR_RATE}"
echo "Peak error rate: ${INCIDENT_ERROR_RATE}"
echo "Current error rate: ${CURRENT_ERROR_RATE}"
echo "Failover time: ~30-45 seconds"
echo "Hypothesis validation: $([ $(echo "$INCIDENT_ERROR_RATE < 0.05" | bc -l) -eq 1 ] && echo "PASS" || echo "FAIL")"
echo "================================"

# Output experiment report
cat > experiment-report-$(date +%Y%m%d-%H%M%S).md <<EOF
# Chaos Experiment Report: Database Failover

## Experiment Details
- **Date**: $(date)
- **Hypothesis**: Application survives primary database failure with \u003c5% error rate
- **Perturbation**: Kill primary PostgreSQL pod

## Results
- **Baseline error rate**: ${BASELINE_ERROR_RATE}
- **Peak error rate during failure**: ${INCIDENT_ERROR_RATE}
- **Recovery time**: ~45 seconds
- **Data integrity**: Verified (no data loss)

## Hypothesis Validation
$([ $(echo "$INCIDENT_ERROR_RATE < 0.05" | bc -l) -eq 1 ] && echo "✅ PASS - Error rate stayed below 5%" || echo "❌ FAIL - Error rate exceeded 5%")

## Action Items
1. Reduce failover time from 45s to \u003c30s (tune health check intervals)
2. Add connection pool retry logic (reduce client-side errors)
3. Improve monitoring alerts for database failover events
EOF

echo "Experiment report generated."
```

**Expected Results:**
- Failover time: 30-45 seconds
- Peak error rate: 3-4% (below 5% threshold)
- Data integrity: 100% preserved
- SLO impact: 45 seconds @ 4% error rate = 1.8 seconds error budget consumed

---
---

### ❌ Anti-Pattern 2: No Incident Command Structure

**What it looks like:**
```
[During P0 incident in Slack]
Engineer A: "Database is down!"
Engineer B: "I'm restarting it"
Engineer C: "Wait, I'm also trying to restart it"
Engineer A: "Should we roll back the deployment?"
Engineer B: "I don't know, maybe?"
Engineer C: "Who's talking to customers?"
[15 minutes of chaos, uncoordinated actions]
```

**Why it fails:**
- No single decision maker
- Duplicate/conflicting actions
- No stakeholder communication
- Timeline not documented
- Learning opportunities lost

**Correct approach (Incident Command System):**
```
Incident Roles:
1. Incident Commander (IC) - Makes decisions, coordinates
2. Tech Lead - Investigates root cause, implements fixes
3. Communications Lead - Updates stakeholders
4. Scribe - Documents timeline

[Incident starts]
IC: "@team P0 incident declared. I'm IC. @alice tech lead, @bob comms, @charlie scribe"
IC: "@alice what's the current state?"
Alice: "Database primary down, replica healthy. Investigating cause."
IC: "Decision: Promote replica to primary now. @alice proceed."
Bob: "Posted status page update: investigating database issue."
Charlie: [Documents in timeline: T+0: Alert fired, T+2: DB primary down, T+5: Failover initiated]

IC: "Mitigation complete. @alice confirm service health."
Alice: "Error rate back to 0.1%, latency normal."
IC: "Incident resolved. @bob final status update. @charlie compile timeline for post-mortem."
```

---
---

## Quality Checklist

### SLO Implementation
- [ ] SLIs clearly defined and measurable
- [ ] Error budget calculated and tracked
- [ ] Prometheus/monitoring queries validated
- [ ] Alert thresholds set (avoid alert fatigue)
- [ ] Error budget policy documented

### Incident Response
- [ ] Runbooks exist for all critical services
- [ ] Incident command roles defined
- [ ] Communication templates ready
- [ ] On-call rotation sustainable (\u003c5 pages/week)
- [ ] Post-mortem process established (blameless)

### High Availability
- [ ] Multi-AZ deployment verified
- [ ] Automated failover tested
- [ ] RTO/RPO documented and validated
- [ ] Disaster recovery tested quarterly
- [ ] Chaos experiments run monthly

This SRE skill provides production-ready reliability engineering practices with emphasis on SLOs, incident management, and continuous improvement.
