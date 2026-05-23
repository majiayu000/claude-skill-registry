---
name: chaos-engineer
description: Expert in resilience testing, fault injection, and building anti-fragile systems using controlled experiments.
---

# Chaos Engineer

## Purpose

Provides resilience testing and chaos engineering expertise specializing in fault injection, controlled experiments, and anti-fragile system design. Validates system resilience through controlled failure scenarios, failover testing, and game day exercises.

## When to Use

- Verifying system resilience before a major launch
- Testing failover mechanisms (Database, Region, Zone)
- Validating alert pipelines (Did PagerDuty fire?)
- Conducting "Game Days" with engineering teams
- Implementing automated chaos in CI/CD (Continuous Verification)
- Debugging elusive distributed system bugs (Race conditions, timeouts)

---
---

## 2. Decision Framework

### Experiment Design Matrix

```
What are we testing?
│
├─ **Infrastructure Layer**
│  ├─ Pods/Containers? → **Pod Kill / Container Crash**
│  ├─ Nodes? → **Node Drain / Reboot**
│  └─ Network? → **Latency / Packet Loss / Partition**
│
├─ **Application Layer**
│  ├─ Dependencies? → **Block Access to DB/Redis**
│  ├─ Resources? → **CPU/Memory Stress**
│  └─ Logic? → **Inject HTTP 500 / Delays**
│
└─ **Platform Layer**
   ├─ IAM? → **Revoke Keys**
   └─ DNS? → **Block DNS Resolution**
```

### Tool Selection

| Environment | Tool | Best For |
|-------------|------|----------|
| **Kubernetes** | **Chaos Mesh / Litmus** | Native K8s experiments (Network, Pod, IO). |
| **AWS/Cloud** | **AWS FIS / Gremlin** | Cloud-level faults (AZ outage, EC2 stop). |
| **Service Mesh** | **Istio Fault Injection** | Application level (HTTP errors, delays). |
| **Java/Spring** | **Chaos Monkey for Spring** | App-level logic attacks. |

### Blast Radius Control

| Level | Scope | Risk | Approval Needed |
|-------|-------|------|-----------------|
| **Local/Dev** | Single container | Low | None |
| **Staging** | Full cluster | Medium | QA Lead |
| **Production (Canary)** | 1% Traffic | High | Engineering Director |
| **Production (Full)** | All Traffic | Critical | VP/CTO (Game Day) |

**Red Flags → Escalate to `sre-engineer`:**
- No "Stop Button" mechanism available
- Observability gaps (Blind spots)
- Cascading failure risk identified without mitigation
- Lack of backups for stateful data experiments

---
---

## 4. Core Workflows

### Workflow 1: Kubernetes Pod Chaos (Chaos Mesh)

**Goal:** Verify that the frontend handles backend pod failures gracefully.

**Steps:**

1.  **Define Experiment (`backend-kill.yaml`)**
    ```yaml
    apiVersion: chaos-mesh.org/v1alpha1
    kind: PodChaos
    metadata:
      name: backend-kill
      namespace: chaos-testing
    spec:
      action: pod-kill
      mode: one
      selector:
        namespaces:
          - prod
        labelSelectors:
          app: backend-service
      duration: "30s"
      scheduler:
        cron: "@every 1m"
    ```

2.  **Define Hypothesis**
    -   *If* a backend pod dies, *then* Kubernetes will restart it within 5 seconds, *and* the frontend will retry 500s seamlessly ( < 1% error rate).

3.  **Execute & Monitor**
    -   Apply manifest.
    -   Watch Grafana dashboard: "HTTP 500 Rate" vs "Pod Restart Count".

4.  **Verification**
    -   Did the pod restart? Yes.
    -   Did users see errors? No (Retries worked).
    -   Result: **PASS**.

---
---

### Workflow 3: Zone Outage Simulation (Game Day)

**Goal:** Verify database failover to secondary region.

**Steps:**

1.  **Preparation**
    -   Notify on-call team (Game Day).
    -   Ensure primary DB writes are active.

2.  **Execution (AWS FIS / Manual)**
    -   Block network traffic to Zone A subnets.
    -   OR Stop RDS Primary instance (Simulate crash).

3.  **Measurement**
    -   Measure **RTO (Recovery Time Objective):** How long until Secondary becomes Primary? (Target: < 60s).
    -   Measure **RPO (Recovery Point Objective):** Any data lost? (Target: 0).

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Testing in Production First

**What it looks like:**
-   Running a "delete database" script in prod without testing in staging.

**Why it fails:**
-   Catastrophic data loss.
-   Resume Generating Event (RGE).

**Correct approach:**
-   Dev → Staging → Canary → Prod.
-   Verify hypothesis in lower environments first.

### ❌ Anti-Pattern 2: No Observability

**What it looks like:**
-   Running chaos without dashboards open.
-   "I think it worked, the app is slow."

**Why it fails:**
-   You don't know *why* it failed.
-   You can't prove resilience.

**Correct approach:**
-   **Observability First:** If you can't measure it, don't break it.

### ❌ Anti-Pattern 3: Random Chaos (Chaos Monkey Style)

**What it looks like:**
-   Killing random things constantly without purpose.

**Why it fails:**
-   Causes alert fatigue.
-   Doesn't test specific failure modes (e.g., network partition vs crash).

**Correct approach:**
-   **Thoughtful Experiments:** Design targeted scenarios (e.g., "What if Redis is slow?"). Random chaos is for *maintenance*, targeted chaos is for *verification*.

---
---

## 7. Quality Checklist

**Planning:**
-   [ ] **Hypothesis:** Clearly defined ("If X happens, Y should occur").
-   [ ] **Blast Radius:** Limited (e.g., 1 zone, 1% users).
-   [ ] **Approval:** Stakeholders notified (or scheduled Game Day).

**Safety:**
-   [ ] **Stop Button:** Automated abort script ready.
-   [ ] **Rollback:** Plan to restore state if needed.
-   [ ] **Backup:** Data backed up before stateful experiments.

**Execution:**
-   [ ] **Monitoring:** Dashboards visible during experiment.
-   [ ] **Logging:** Experiment start/end times logged for correlation.

**Review:**
-   [ ] **Fix:** Action items assigned (Jira).
-   [ ] **Report:** Findings shared with engineering team.

## Examples

### Example 1: Kubernetes Pod Failure Recovery

**Scenario:** A microservices platform needs to verify that their cart service handles pod failures gracefully without impacting user checkout flow.

**Experiment Design:**
1. **Hypothesis**: If a cart-service pod is killed, Kubernetes will reschedule within 5 seconds, and users will see less than 0.1% error rate
2. **Chaos Injection**: Use Chaos Mesh to kill random pods in the production namespace
3. **Monitoring**: Track error rates, pod restart times, and user-facing failures

**Execution Results:**
- Pod restart time: 3.2 seconds average (within SLA)
- Error rate during experiment: 0.02% (below 0.1% threshold)
- Circuit breakers prevented cascading failures
- Users experienced seamless failover

**Lessons Learned:**
- Retry logic was working but needed exponential backoff
- Added fallback response for stale cart data
- Created runbook for pod failure scenarios

### Example 2: Database Failover Validation

**Scenario:** A financial services company needs to verify their multi-region database failover meets RTO of 30 seconds and RPO of zero data loss.

**Game Day Setup:**
1. **Preparation**: Notified all stakeholders, backed up current state
2. **Primary Zone Blockage**: Used AWS FIS to simulate zone failure
3. **Failover Trigger**: Automated failover initiated when health checks failed
4. **Measurement**: Tracked RTO, RPO, and application recovery

**Measured Results:**
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| RTO | < 30s | 18s | ✅ PASS |
| RPO | 0 data | 0 data | ✅ PASS |
| Application recovery | < 60s | 42s | ✅ PASS |
| Data consistency | 100% | 100% | ✅ PASS |

**Improvements Identified:**
- DNS TTL was too high (5 minutes), reduced to 30 seconds
- Application connection pooling needed pre-warming
- Added health check for database replication lag

### Example 3: Third-Party API Dependency Testing

**Scenario:** A SaaS platform depends on a payment processor API and needs to verify graceful degradation when the API is slow or unavailable.

**Fault Injection Strategy:**
1. **Delay Injection**: Using Istio to add 5-10 second delays to payment API calls
2. **Timeout Validation**: Verify circuit breakers open within configured timeouts
3. **Fallback Testing**: Ensure users see appropriate error messages

**Test Scenarios:**
- 50% of requests delayed 10s: Circuit breaker opens, fallback shown
- 100% delay: System degrades gracefully with queue-based processing
- Recovery: System reconnects properly after fault cleared

**Results:**
- Circuit breaker threshold: 5 consecutive failures (needed adjustment)
- Fallback UI: 94% of users completed purchase via alternative method
- Alert tuning: Reduced false positives by tuning latency thresholds

## Best Practices

### Experiment Design

- **Start with Hypothesis**: Define what you expect to happen before running experiments
- **Limit Blast Radius**: Always start with small scope and expand gradually
- **Measure Steady State**: Establish baseline metrics before introducing chaos
- **Document Everything**: Record experiment parameters, expectations, and outcomes
- **Iterate and Evolve**: Use findings to design more comprehensive experiments

### Safety and Controls

- **Always Have a Stop Button**: Can you abort the experiment immediately?
- **Define Rollback Plan**: How do you restore normal operations?
- **Communication**: Notify stakeholders before and during experiments
- **Timing**: Avoid experiments during critical business periods
- **Escalation Path**: Know when to stop and call for help

### Tool Selection

- **Match Tool to Environment**: Kubernetes → Chaos Mesh/Litmus, AWS → FIS
- **Service Mesh Integration**: Use Istio/Linkerd for application-level faults
- **Cloud-Native Tools**: Leverage managed chaos services where available
- **Custom Tools**: Build application-specific chaos when needed
- **Multi-Cloud**: Consider tools that work across cloud providers

### Observability Integration

- **Pre-Experiment Validation**: Ensure dashboards and alerts are working
- **Metrics Collection**: Capture before/during/after metrics
- **Log Analysis**: Review logs for unexpected behavior
- **Distributed Tracing**: Use traces to understand failure propagation
- **Alert Validation**: Verify alerts fire as expected during experiments

### Cultural Aspects

- **Blame-Free Post-Mortems**: Focus on system improvement, not finger-pointing
- **Regular Game Days**: Schedule chaos exercises as routine team activities
- **Cross-Team Participation**: Include on-call, developers, and operations
- **Share Learnings**: Document and share experiment results broadly
- **Reward Resilience**: Recognize teams that build resilient systems
