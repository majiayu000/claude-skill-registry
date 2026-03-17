---
name: root-cause-analysis
description: Conduct systematic root cause analysis to identify underlying problems. Use structured methodologies to prevent recurring issues and drive improvements.
---

# Root Cause Analysis

## Overview

Root cause analysis (RCA) identifies underlying reasons for failures, enabling permanent solutions rather than temporary fixes.

## When to Use

- Production incidents
- Customer-impacting issues
- Repeated problems
- Unexpected failures
- Performance degradation

## Instructions

### 1. **The 5 Whys Technique**

```yaml
Example: Website Down

Symptom: Website returned 503 Service Unavailable

Why 1: Why was website down?
  Answer: Database connection pool exhausted

Why 2: Why was connection pool exhausted?
  Answer: Queries taking too long, connections not released

Why 3: Why were queries slow?
  Answer: Missing index on frequently queried column

Why 4: Why was index missing?
  Answer: Performance testing didn't use production-like data volume

Why 5: Why wasn't production-like data used?
  Answer: Load testing environment doesn't mirror production

Root Cause: Load testing environment under-provisioned

Solution: Update load testing environment with production-like data

Prevention: Establish environment parity requirements
```

### 2. **Systematic RCA Process**

```yaml
Step 1: Gather Facts
  - When did issue occur?
  - Who detected it?
  - How many users affected?
  - What error messages?
  - What system changes deployed?
  - Check logs, metrics, alerts
  - Determine impact scope

Step 2: Reproduce
  - Can we reproduce consistently?
  - What are the exact steps?
  - What environment (prod, staging)?
  - Can we isolate to component?
  - Set up test case

Step 3: Identify Contributing Factors
  - Direct cause
  - Indirect/enabling factors
  - System vulnerabilities
  - Procedural gaps
  - Knowledge gaps

Step 4: Determine Root Cause
  - Use 5 Whys technique
  - Ask "why did this control fail?"
  - Look for systemic issues
  - Separate root cause from symptoms

Step 5: Develop Solutions
  - Immediate: Fix the symptom
  - Short-term: Prevent recurrence
  - Long-term: Systemic fix
  - Prioritize by impact/effort

Step 6: Implement & Verify
  - Implement solutions
  - Test in staging
  - Deploy carefully
  - Verify improvement
  - Monitor metrics

Step 7: Document & Share
  - Write RCA report
  - Document lesson learned
  - Share with team
  - Update procedures
  - Training if needed
```

### 3. **RCA Report Template**

```yaml
RCA Report:

Incident: Database connection failure (2024-01-15, 14:30-15:15)

Impact:
  - Duration: 45 minutes
  - Users affected: 5,000 (10% of user base)
  - Revenue lost: ~$2,000
  - Severity: P1 (Critical)

Timeline:
  14:30: Automated monitoring alert: High error rate (20%)
  14:32: On-call engineer notified
  14:35: Identified database connection error in logs
  14:40: Restarted database connection pool
  14:42: Service recovered, error rate returned to 0.1%
  14:50: Incident declared resolved
  15:15: Full recovery verified

Root Cause:
  Poorly optimized query introduced in release 2.5.0 caused
  queries to take 10x longer. Connection pool exhausted as
  connections weren't released quickly.

Contributing Factors:
  1. No query performance testing pre-deployment
  2. Load testing environment doesn't match production volume
  3. No alerting on query duration
  4. Connection pool timeout set too high

Solutions:
  Immediate (Done):
    - Rolled back problematic query optimization

  Short-term (1 week):
    - Added query performance alerts (>1s)
    - Added index for slow query
    - Set query timeout to 5 seconds

  Long-term (1 month):
    - Updated load testing with production-like data
    - Implement performance benchmarks in CI/CD
    - Improve monitoring for connection pool health
    - Training on query optimization

Prevention:
  - Query performance regression tests
  - Load testing with production data
  - Connection pool metrics monitoring
  - Code review of database changes
```

### 4. **Root Cause Analysis Techniques**

```yaml
Fishbone Diagram:

Main problem: Slow API Response

Branches:

  Code:
    - Inefficient algorithm
    - Missing cache
    - Unnecessary queries

  Data:
    - Large dataset
    - Missing index
    - Slow database

  Infrastructure:
    - Low CPU capacity
    - Slow network
    - Disk I/O bottleneck

  Process:
    - No monitoring
    - No load testing
    - Manual deployments

  People:
    - Lack of knowledge
    - Lack of tools
    - No peer review

---

Systemic vs. Individual Causes:

Individual: "Developer used inefficient code"
  Fix: Training
  Risk: Happens again with different person

Systemic: "No code review process"
  Fix: Implement mandatory code review
  Risk: Prevents similar issues

Prefer systemic solutions for prevention
```

### 5. **Follow-Up & Prevention**

```yaml
After RCA:

1. Track Action Items
  - Assign owner
  - Set deadline
  - Follow up in retrospective

2. Prevent Recurrence
  - Automated tests
  - Monitoring/alerts
  - Procedural changes
  - Training

3. Monitor Metrics
  - Track similar incidents
  - Verify fix effectiveness
  - Monitor preventive measures
  - Catch early warnings

4. Share Learnings
  - Document incident
  - Share with team
  - Industry sharing if relevant
  - Update procedures

---

Checklist:

[ ] Incident details documented
[ ] Timeline established
[ ] Logs reviewed
[ ] Metrics analyzed
[ ] Root cause identified (via 5 Whys)
[ ] Contributing factors listed
[ ] Immediate actions completed
[ ] Short-term solutions planned
[ ] Long-term solutions identified
[ ] Solutions prioritized
[ ] RCA report written
[ ] Team debriefing scheduled
[ ] Action items assigned
[ ] Prevention measures planned
[ ] Follow-up scheduled
```

## Key Points

- Distinguish symptom from root cause
- Use 5 Whys technique systematically
- Look for systemic issues, not individual blame
- Focus on prevention, not just fixing
- Document thoroughly for team learning
- Assign clear ownership for solutions
- Follow up to verify effectiveness
- Use RCA to drive improvements
