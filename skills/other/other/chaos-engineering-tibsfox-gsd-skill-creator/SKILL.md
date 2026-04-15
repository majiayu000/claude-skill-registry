---
name: chaos-engineering
description: Provides chaos engineering best practices for resilience testing, fault injection, and game day planning. Use when designing resilience experiments, configuring chaos tools, planning game days, or when user mentions 'chaos engineering', 'resilience', 'litmus', 'game day', 'fault injection', 'chaos monkey', 'blast radius', 'steady state', 'failure mode'.
type: skill
category: ops
status: stable
origin: tibsfox
modified: false
first_seen: 2026-02-07
first_path: examples/chaos-engineering/SKILL.md
superseded_by: null
---
# Chaos Engineering

Best practices for systematically injecting failures to discover weaknesses before they cause outages, using steady-state hypotheses, controlled experiments, and progressive blast radius expansion.

## Chaos Engineering Principles

Chaos engineering is not random destruction. It is disciplined experimentation on distributed systems to build confidence in their resilience.

```
Define Steady State --> Form Hypothesis --> Design Experiment --> Control Blast Radius --> Run --> Analyze --> Fix --> Repeat
```

| Principle | Description | Why It Matters |
|-----------|-------------|----------------|
| Define steady state | Identify measurable normal behavior (latency, error rate, throughput) | Without a baseline, you cannot detect degradation |
| Hypothesize around steady state | Predict the system will maintain steady state during fault | Forces explicit thinking about expected behavior |
| Vary real-world events | Inject failures that actually happen (network, disk, process, dependency) | Simulated failures must map to real failure modes |
| Run in production | Test where real complexity exists (with safeguards) | Staging rarely matches production topology |
| Minimize blast radius | Start small, expand gradually, have kill switches | Chaos should reveal problems, not cause outages |
| Automate experiments | Repeatable experiments run in CI/CD or on schedule | Manual experiments don't scale and introduce bias |
| Build a hypothesis backlog | Track what you want to test and what you've learned | Systematic coverage prevents blind spots |

## Steady-State Hypothesis Template

Every chaos experiment begins with a hypothesis. This template ensures experiments are structured and measurable.

```yaml
# Steady-State Hypothesis Document
experiment:
  name: "Payment service database failover"
  id: "CHAOS-042"
  date: "2026-02-07"
  owner: "team-payments"
  reviewer: "sre-team"

steady_state:
  description: "Payment service processes transactions within SLO"
  metrics:
    - name: "p99 latency"
      source: "prometheus"
      query: 'histogram_quantile(0.99, rate(payment_request_duration_seconds_bucket[5m]))'
      threshold: "< 500ms"
    - name: "error rate"
      source: "prometheus"
      query: 'rate(payment_request_errors_total[5m]) / rate(payment_request_total[5m])'
      threshold: "< 0.1%"
    - name: "transaction throughput"
      source: "prometheus"
      query: 'rate(payment_transactions_total[5m])'
      threshold: "> 100 tx/s"

hypothesis: >
  When the primary database replica fails, the payment service will
  failover to the secondary replica within 30 seconds, maintaining
  p99 latency below 2 seconds and error rate below 1% during failover.

experiment_design:
  action: "Kill primary PostgreSQL pod in payment-db StatefulSet"
  duration: "5 minutes"
  blast_radius: "payment namespace only"
  rollback: "PostgreSQL operator will auto-recreate pod; manual failback if needed"

abort_conditions:
  - "Error rate exceeds 5% for more than 60 seconds"
  - "Total service outage detected (zero throughput for 30 seconds)"
  - "Cascading failures detected in upstream services"
  - "Any P1/P2 incident triggered by unrelated system"

expected_outcome:
  - "Failover completes within 30 seconds"
  - "p99 latency spikes to < 2s during failover, recovers to < 500ms"
  - "Error rate stays below 1%"
  - "No data loss or corruption"

actual_outcome: null  # Filled after experiment
findings: null
action_items: null
```

## Litmus Chaos Experiments

### LitmusChaos Engine Manifest

LitmusChaos is a CNCF project for Kubernetes-native chaos engineering. The ChaosEngine connects your application to chaos experiments.

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: payment-service-chaos
  namespace: payments
spec:
  appinfo:
    appns: payments
    applabel: "app=payment-service"
    appkind: deployment
  engineState: active
  chaosServiceAccount: litmus-admin
  monitoring: true

  # Steady-state checks before and after experiment
  components:
    runner:
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "200m"
          memory: "256Mi"

  experiments:
    - name: pod-delete
      spec:
        probe:
          # Steady-state verification probe
          - name: "payment-api-health"
            type: httpProbe
            mode: Continuous
            httpProbe/inputs:
              url: "http://payment-service.payments.svc:8080/health"
              insecureSkipVerify: false
              method:
                get:
                  criteria: "=="
                  responseCode: "200"
            runProperties:
              probeTimeout: 5s
              interval: 10s
              retry: 3
              probePollingInterval: 2s

          - name: "payment-latency-check"
            type: promProbe
            mode: Edge
            promProbe/inputs:
              endpoint: "http://prometheus.monitoring.svc:9090"
              query: 'histogram_quantile(0.99, rate(payment_request_duration_seconds_bucket{namespace="payments"}[1m]))'
              comparator:
                type: float
                criteria: "<="
                value: "2.0"
            runProperties:
              probeTimeout: 10s
              interval: 30s
              retry: 2

        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "120"
            - name: CHAOS_INTERVAL
              value: "30"
            - name: FORCE
              value: "true"
            - name: PODS_AFFECTED_PERC
              value: "50"
```

### Litmus Network Chaos Experiment

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: payment-network-chaos
  namespace: payments
spec:
  appinfo:
    appns: payments
    applabel: "app=payment-service"
    appkind: deployment
  engineState: active
  chaosServiceAccount: litmus-admin

  experiments:
    - name: pod-network-latency
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "180"
            - name: NETWORK_LATENCY
              value: "300"  # 300ms added latency
            - name: JITTER
              value: "100"  # 100ms jitter
            - name: NETWORK_INTERFACE
              value: "eth0"
            - name: DESTINATION_IPS
              value: "10.96.0.10"  # Target specific dependency (e.g., database)
            - name: CONTAINER_RUNTIME
              value: "containerd"
            - name: SOCKET_PATH
              value: "/run/containerd/containerd.sock"
        probe:
          - name: "transaction-success-rate"
            type: promProbe
            mode: Continuous
            promProbe/inputs:
              endpoint: "http://prometheus.monitoring.svc:9090"
              query: 'rate(payment_transactions_success_total{namespace="payments"}[1m]) / rate(payment_transactions_total{namespace="payments"}[1m]) * 100'
              comparator:
                type: float
                criteria: ">="
                value: "95.0"
            runProperties:
              probeTimeout: 10s
              interval: 15s
              retry: 3
```

## Chaos Monkey Configuration

Netflix's Chaos Monkey randomly terminates instances in production. Modern implementations support Kubernetes and use Spinnaker integration.

```yaml
# Chaos Monkey for Spring Boot (Simian Army successor)
# application.yml
chaos:
  monkey:
    enabled: true
    watcher:
      controller: true
      restController: true
      service: true
      repository: true
      component: false

    assaults:
      level: 5                    # 1 in 5 requests affected
      latencyActive: true
      latencyRangeStart: 1000     # 1 second
      latencyRangeEnd: 5000       # 5 seconds
      exceptionsActive: true
      exception:
        type: java.lang.RuntimeException
        arguments:
          - className: java.lang.String
            value: "Chaos Monkey - simulated failure"
      killApplicationActive: false  # DANGER: only enable in controlled tests
      memoryActive: false

    runtime:
      # Only active during business hours (safety net)
      scheduleEnabled: true
      scheduleExpression: "0 0 9-17 * * MON-FRI"

---
# Kube-monkey configuration (Kubernetes-native Chaos Monkey)
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-monkey-config
  namespace: kube-system
data:
  config.toml: |
    [kubemonkey]
    run_hour = 8
    start_hour = 10
    end_hour = 16
    grace_period_sec = 5
    cluster_dns_name = "cluster.local"
    whitelisted_namespaces = ["payments", "orders", "inventory"]
    blacklisted_namespaces = ["kube-system", "monitoring", "istio-system"]
    time_zone = "America/New_York"

    [debug]
    enabled = true
    schedule_immediate_kill = false
```

## Blast Radius Control Matrix

Controlling blast radius is the difference between chaos engineering and simply breaking things.

| Level | Scope | Example | Risk | When to Use |
|-------|-------|---------|------|-------------|
| 1 - Unit | Single container/process | Kill one pod replica | Minimal | Starting out, new experiments |
| 2 - Service | All replicas of one service | Delete all pods in deployment | Low | After Level 1 succeeds |
| 3 - Dependency | Degrade a dependency | Add latency to database connection | Medium | Testing circuit breakers, retries |
| 4 - Zone | Entire availability zone | Drain all nodes in one AZ | High | Quarterly DR exercises |
| 5 - Region | Full region failure | Redirect all traffic to secondary region | Critical | Annual DR exercises, game days |

### Blast Radius Escalation Protocol

```
Level 1: Single pod kill
  |
  +-- Pass? --> Level 2: Full service disruption
  |               |
  |               +-- Pass? --> Level 3: Dependency failure
  |               |               |
  |               |               +-- Pass? --> Level 4: Zone failure (game day)
  |               |               |               |
  |               |               |               +-- Pass? --> Level 5: Region failover (annual)
  |               |               |
  |               |               +-- Fail --> Fix, retest Level 3
  |               |
  |               +-- Fail --> Fix, retest Level 2
  |
  +-- Fail --> Fix, retest Level 1
```

## Game Day Runbook Template

Game days are structured chaos engineering exercises involving multiple teams. They test both technical resilience and human response.

```markdown
# Game Day Runbook: [Scenario Name]

## Metadata
- **Date:** YYYY-MM-DD
- **Time Window:** HH:MM - HH:MM (timezone)
- **Game Master:** [name]
- **Participants:** [teams]
- **Communication Channel:** #gameday-YYYY-MM-DD

## Pre-Game Checklist
- [ ] All participating teams briefed (do NOT reveal exact failure scenario)
- [ ] Monitoring dashboards open and shared
- [ ] Rollback procedures documented and tested
- [ ] Customer communication templates prepared
- [ ] Stakeholders notified of game day window
- [ ] On-call engineers aware and standing by
- [ ] Kill switch tested and ready

## Scenario
**Narrative:** [Real-world scenario description]
**Technical Action:** [Exact fault injection steps]
**Expected Impact:** [What should happen if systems are resilient]
**Worst Case:** [What happens if resilience mechanisms fail]

## Timeline
| Time | Action | Owner |
|------|--------|-------|
| T-30m | Final go/no-go check | Game Master |
| T-15m | Verify steady state metrics | SRE |
| T-0 | Inject failure | Game Master |
| T+5m | Observe initial response | All teams |
| T+15m | Check: has system self-healed? | SRE |
| T+30m | Decision: continue or abort | Game Master |
| T+60m | End experiment, begin recovery | Game Master |
| T+90m | Verify full recovery | SRE |
| T+120m | Hot debrief | All participants |

## Observation Checklist
- [ ] Did alerts fire within expected time?
- [ ] Did on-call respond within SLO?
- [ ] Did failover mechanisms activate?
- [ ] Were customers impacted? For how long?
- [ ] Did runbooks match actual recovery steps?
- [ ] Were any cascading failures observed?
- [ ] Did communication flow correctly?

## Post-Game
- [ ] Write-up completed within 48 hours
- [ ] Action items created with owners and deadlines
- [ ] Findings shared with engineering org
- [ ] Next game day scenario identified
```

## Progressive Chaos Maturity Levels

| Level | Name | Practices | Experiments | Frequency |
|-------|------|-----------|-------------|-----------|
| 0 | None | No chaos practice | None | Never |
| 1 | Exploratory | Ad-hoc experiments in staging | Pod kills, restarts | Quarterly |
| 2 | Systematic | Hypothesis-driven, documented | Network faults, dependency failures | Monthly |
| 3 | Automated | Chaos in CI/CD, scheduled experiments | Multi-service scenarios, zone failures | Weekly |
| 4 | Advanced | Production chaos, game days, culture of resilience | Region failover, data plane chaos | Continuous |

## Chaos in CI/CD Pipelines

Integrate chaos experiments as quality gates in your deployment pipeline.

### GitHub Actions Chaos Workflow

```yaml
name: Resilience Tests

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 10 * * 1'  # Every Monday at 10:00 UTC

permissions:
  contents: read

jobs:
  chaos-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - name: Set up test cluster
        uses: helm/kind-action@v1
        with:
          cluster_name: chaos-test
          config: test/kind-config.yaml

      - name: Deploy application
        run: |
          kubectl apply -f k8s/namespace.yaml
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
          kubectl wait --for=condition=available deployment/payment-service \
            -n payments --timeout=120s

      - name: Install LitmusChaos
        run: |
          kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-v3.0.0.yaml
          kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=litmus \
            -n litmus --timeout=120s

      - name: Verify steady state
        run: |
          # Check application health before chaos
          kubectl exec -n payments deploy/payment-service -- \
            curl -sf http://localhost:8080/health || exit 1

      - name: Run chaos experiment
        run: |
          kubectl apply -f chaos/pod-delete-experiment.yaml
          # Wait for experiment to complete
          kubectl wait --for=jsonpath='{.status.engineStatus}'=completed \
            chaosengine/payment-chaos -n payments --timeout=300s

      - name: Verify resilience
        run: |
          # Check experiment verdict
          VERDICT=$(kubectl get chaosresult payment-chaos-pod-delete \
            -n payments -o jsonpath='{.status.experimentStatus.verdict}')
          echo "Experiment verdict: $VERDICT"
          if [ "$VERDICT" != "Pass" ]; then
            echo "CHAOS TEST FAILED: System did not maintain steady state"
            kubectl logs -n payments -l app=payment-service --tail=100
            exit 1
          fi

      - name: Collect results
        if: always()
        run: |
          kubectl get chaosresult -n payments -o yaml > chaos-results.yaml

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: chaos-results
          path: chaos-results.yaml
          retention-days: 30
```

## Common Failure Modes to Test

| Failure Mode | Tool/Method | What It Validates |
|-------------|-------------|-------------------|
| Pod termination | LitmusChaos pod-delete | Auto-scaling, health checks, restart policies |
| Network latency | tc netem / LitmusChaos | Timeouts, circuit breakers, retry logic |
| Network partition | iptables / LitmusChaos | Split-brain handling, quorum mechanisms |
| DNS failure | CoreDNS manipulation | DNS caching, fallback resolution |
| CPU stress | stress-ng / LitmusChaos | Autoscaling triggers, throttling behavior |
| Memory pressure | stress-ng / LitmusChaos | OOM handling, graceful degradation |
| Disk I/O saturation | fio / LitmusChaos | Write-ahead log performance, disk alerts |
| Dependency unavailable | Network block / mock | Circuit breakers, fallback responses, bulkheads |
| Clock skew | chrony manipulation | Certificate validation, token expiry, cron jobs |
| Configuration drift | Mutate ConfigMap/Secret | Config reload, graceful failure on bad config |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Chaos without hypothesis | Random destruction teaches nothing | Always write a hypothesis before injecting failures |
| Testing only in staging | Staging rarely matches production complexity | Graduate to production chaos with proper safeguards |
| No abort criteria | Experiments can escalate into real outages | Define and automate kill switches before every experiment |
| Big bang experiments | Starting with region-level failures on day one | Follow blast radius levels: pod -> service -> zone -> region |
| Chaos as punishment | Using chaos to blame teams for failures | Frame chaos as learning; celebrate finding weaknesses |
| No follow-through | Running experiments but never fixing findings | Track action items with owners and deadlines; re-test fixes |
| Manual-only experiments | Experiments that depend on one person to run | Automate experiments, integrate into CI/CD pipeline |
| Ignoring human factors | Only testing technical resilience | Game days should test alerting, communication, and runbooks too |
| Secret chaos | Running experiments without telling anyone | Communicate schedules; surprise chaos erodes trust |
| Skipping steady-state verification | No baseline to compare against | Always measure before, during, and after injection |
| Chaos without observability | Cannot measure impact of experiments | Instrument first, then inject chaos; monitoring is prerequisite |
| One-and-done experiments | Running an experiment once and declaring success | Systems change; re-run experiments regularly to catch regressions |

## Chaos Engineering Readiness Checklist

- [ ] Observability in place (metrics, logs, traces) for target services
- [ ] Steady-state metrics identified and baselined for target services
- [ ] Chaos tooling installed and configured (LitmusChaos, Gremlin, or equivalent)
- [ ] Service account and RBAC configured for chaos operator
- [ ] Abort criteria defined and kill switch mechanism tested
- [ ] First hypothesis document written and reviewed
- [ ] Blast radius limited to single pod/container for initial experiments
- [ ] Monitoring dashboards prepared for experiment observation
- [ ] On-call team briefed and aware of experiment schedule
- [ ] Rollback procedures documented and tested independently
- [ ] Communication channel established for experiment coordination
- [ ] First experiment successfully run in non-production environment
- [ ] Results documented with findings and action items
- [ ] Leadership briefed on chaos engineering program and value
- [ ] Game day planned within 90 days of first successful experiment
- [ ] Chaos experiments integrated into CI/CD pipeline (or plan to do so)
- [ ] Resilience scorecard created for tracked services
