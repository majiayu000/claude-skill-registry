---
name: runbooks-troubleshooting-guides
description: Use when creating troubleshooting guides and diagnostic procedures for operational issues. Covers problem diagnosis, root cause analysis, and systematic debugging.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Runbooks - Troubleshooting Guides

Creating effective troubleshooting guides for diagnosing and resolving operational issues.

## Troubleshooting Framework

### The 5-Step Method

1. **Observe** - Gather symptoms and data
2. **Hypothesize** - Form theories about root cause
3. **Test** - Validate hypotheses with experiments
4. **Fix** - Apply solution
5. **Verify** - Confirm resolution

## Basic Troubleshooting Guide

```markdown
# Troubleshooting: [Problem Statement]

## Symptoms

What the user/system is experiencing:
- API returning 503 errors
- Response time > 10 seconds
- High CPU usage alerts

## Quick Checks (< 2 minutes)

### 1. Is the service running?
```bash
kubectl get pods -n production | grep api-server
```

**Expected:** STATUS = Running

### 2. Are recent deploys the cause?

```bash
kubectl rollout history deployment/api-server
```

**Check:** Did we deploy in the last 30 minutes?

### 3. Is this affecting all users?

Check error rate in Datadog:

- If < 5%: Isolated issue, may be client-specific
- If > 50%: Widespread issue, likely infrastructure

## Common Causes

| Symptom | Likely Cause | Quick Fix |
|---------|-------------|-----------|
| 503 errors | Pod crashlooping | Restart deployment |
| Slow responses | Database connection pool | Increase pool size |
| High memory | Memory leak | Restart pods |

## Detailed Diagnosis

### Hypothesis 1: Database Connection Issues

**Test:**

```bash
# Check database connections
kubectl exec -it api-server-abc -- psql -h $DB_HOST -c "SELECT count(*) FROM pg_stat_activity"
```

**If connections > 90:** Pool is saturated.
**Next step:** Increase pool size or investigate slow queries.

### Hypothesis 2: High Traffic Spike

**Test:**

```bash
# Check request rate
curl -H "Authorization: Bearer $DD_API_KEY" \
  "https://api.datadoghq.com/api/v1/query?query=sum:nginx.requests{*}"
```

**If requests 3x normal:** Traffic spike.
**Next step:** Scale up pods or enable rate limiting.

### Hypothesis 3: External Service Degradation

**Test:**

```bash
# Check third-party API
curl -w "@curl-format.txt" https://api.stripe.com/v1/charges
```

**If response time > 2s:** External service slow.
**Next step:** Implement circuit breaker or increase timeouts.

## Resolution Steps

### Solution A: Immediate (< 5 minutes)

Restart affected pods:

```bash
kubectl rollout restart deployment/api-server -n production
```

**When to use:** Quick mitigation while investigating root cause.

### Solution B: Short-term (< 30 minutes)

Scale up resources:

```bash
kubectl scale deployment/api-server --replicas=10 -n production
```

**When to use:** Traffic spike or resource exhaustion.

### Solution C: Long-term (< 2 hours)

Fix root cause:

1. Identify slow database query
2. Add database index
3. Deploy code optimization

**When to use:** After immediate pressure is relieved.

## Validation

- [ ] Error rate < 1%
- [ ] Response time p95 < 200ms
- [ ] CPU usage < 70%
- [ ] No active alerts

## Prevention

How to prevent this issue in the future:

- Add monitoring alert for connection pool saturation
- Implement auto-scaling based on request rate
- Set up load testing to find capacity limits

```

## Decision Tree Format

```markdown
# Troubleshooting: Slow API Responses

## Start Here

```

                    Check response time
                           |
            ┌──────────────┴──────────────┐
            │                             │
        < 500ms                       > 500ms
            │                             │
       NOT THIS RUNBOOK            Continue below

```

## Step 1: Locate the Slowness

```bash
# Check which service is slow
curl -w "@timing.txt" https://api.example.com/users
```

**Decision:**

- Time to first byte > 2s → Database slow (go to Step 2)
- Time to first byte < 100ms → Network slow (go to Step 3)
- Timeout → Service down (go to Step 4)

## Step 2: Database Diagnosis

```bash
# Check active queries
psql -c "SELECT query, state, query_start FROM pg_stat_activity WHERE state != 'idle'"
```

**Decision:**

- Query running > 5s → Slow query (Solution A)
- Many idle in transaction → Connection leak (Solution B)
- High connection count → Pool exhausted (Solution C)

### Solution A: Optimize Slow Query

1. Identify slow query from above
2. Run EXPLAIN ANALYZE
3. Add missing index or optimize query

### Solution B: Fix Connection Leak

1. Restart application pods
2. Review code for unclosed connections
3. Add connection timeout

### Solution C: Increase Connection Pool

1. Edit database config
2. Increase max_connections
3. Update application pool size

## Step 3: Network Diagnosis

... (continue with network troubleshooting)

```

## Layered Troubleshooting

### Layer 1: Application

```markdown
## Application Layer Issues

### Check Application Health

1. **Health endpoint:**
   ```bash
   curl https://api.example.com/health
   ```

1. **Application logs:**

   ```bash
   kubectl logs deployment/api-server --tail=100 | grep ERROR
   ```

2. **Application metrics:**
   - Request rate
   - Error rate
   - Response time percentiles

### Common Application Issues

**Memory Leak**

- **Symptom:** Memory usage climbing over time
- **Test:** Check memory metrics in Datadog
- **Fix:** Restart pods, investigate with heap dump

**Thread Starvation**

- **Symptom:** Slow responses, high CPU
- **Test:** Thread dump analysis
- **Fix:** Increase thread pool size

**Code Bug**

- **Symptom:** Specific endpoints fail
- **Test:** Review recent deploys
- **Fix:** Rollback or hotfix

```

### Layer 2: Infrastructure

```markdown
## Infrastructure Layer Issues

### Check Infrastructure Health

1. **Node resources:**
   ```bash
   kubectl top nodes
   ```

1. **Pod resources:**

   ```bash
   kubectl top pods -n production
   ```

2. **Network connectivity:**

   ```bash
   kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- ping database.internal
   ```

### Common Infrastructure Issues

**Node Under Pressure**

- **Symptom:** Pods evicted, slow scheduling
- **Test:** `kubectl describe node` for pressure conditions
- **Fix:** Scale node pool or add nodes

**Network Partition**

- **Symptom:** Intermittent timeouts
- **Test:** MTR between pods and destination
- **Fix:** Check security groups, routing tables

**Disk I/O Saturation**

- **Symptom:** Slow database, high latency
- **Test:** Check IOPS metrics in CloudWatch
- **Fix:** Increase provisioned IOPS

```

### Layer 3: External Dependencies

```markdown
## External Dependencies Issues

### Check External Services

1. **Third-party APIs:**
   ```bash
   curl -w "@timing.txt" https://api.stripe.com/health
   ```

1. **Status pages:**
   - Check status.stripe.com
   - Check status.aws.amazon.com

2. **DNS resolution:**

   ```bash
   nslookup api.stripe.com
   dig api.stripe.com
   ```

### Common External Issues

**API Rate Limiting**

- **Symptom:** 429 responses from external service
- **Test:** Check rate limit headers
- **Fix:** Implement backoff, cache responses

**Service Degradation**

- **Symptom:** Slow external API responses
- **Test:** Check their status page
- **Fix:** Implement circuit breaker, use fallback

**DNS Failure**

- **Symptom:** Cannot resolve hostname
- **Test:** DNS queries
- **Fix:** Check DNS config, try alternative resolver

```

## Systematic Debugging

### Use the Scientific Method

```markdown
# Debugging: Database Connection Failures

## 1. Observation

**What we know:**
- Error: "connection refused" in logs
- Started: 2025-01-15 14:30 UTC
- Frequency: Every database query fails
- Scope: All pods affected

## 2. Hypothesis

**Possible causes:**
1. Database instance is down
2. Security group blocking traffic
3. Network partition
4. Wrong credentials

## 3. Test Each Hypothesis

### Test 1: Database instance status

```bash
aws rds describe-db-instances --db-instance-identifier prod-db | jq '.DBInstances[0].DBInstanceStatus'
```

**Result:** "available"
**Conclusion:** Database is running ✗ Hypothesis 1 rejected

### Test 2: Security group rules

```bash
aws ec2 describe-security-groups --group-ids sg-abc123 | jq '.SecurityGroups[0].IpPermissions'
```

**Result:** Port 5432 open only to 10.0.0.0/16
**Pod IP:** 10.1.0.5
**Conclusion:** Pod IP not in allowed range ✓ **ROOT CAUSE FOUND**

## 4. Fix

Update security group:

```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-abc123 \
  --protocol tcp \
  --port 5432 \
  --cidr 10.1.0.0/16
```

## 5. Verify

Test connection from pod:

```bash
kubectl exec -it api-server-abc -- psql -h prod-db.rds.amazonaws.com -c "SELECT 1"
```

**Result:** Success ✓

```

## Time-Boxed Investigation

```markdown
# Troubleshooting: Production Outage

**Time Box:** Spend MAX 15 minutes investigating before escalating.

## First 5 Minutes: Quick Wins

- [ ] Check pod status
- [ ] Check recent deploys
- [ ] Check external status pages
- [ ] Review monitoring dashboards

**If issue persists:** Continue to next phase.

## Minutes 5-10: Common Causes

- [ ] Restart pods (quick mitigation)
- [ ] Check database connectivity
- [ ] Review application logs
- [ ] Check resource limits

**If issue persists:** Continue to next phase.

## Minutes 10-15: Deep Dive

- [ ] Enable debug logging
- [ ] Capture thread dump
- [ ] Check for memory leaks
- [ ] Review network traces

**If issue persists:** ESCALATE to senior engineer.

## Escalation

**Escalate to:** Platform Team Lead
**Provide:**
- Timeline of issue
- Tests performed
- Current error rate
- Mitigation attempts
```

## Common Troubleshooting Patterns

### Binary Search

```markdown
## Finding Which Service is Slow

Using binary search to narrow down the problem:

1. **Check full request:** 5000ms total
2. **Check first half (API → Database):** 4900ms
   → Problem is in database query
3. **Check database:** Query takes 4800ms
4. **Check query plan:** Sequential scan on large table
5. **Root cause:** Missing index

**Fix:** Add index on frequently queried column.
```

### Correlation Analysis

```markdown
## Finding Related Events

Look for patterns and correlations:

**Timeline:**
- 14:25 - Deploy completed
- 14:30 - Error rate spike
- 14:35 - Database CPU at 100%
- 14:40 - Requests timing out

**Correlation:** Deploy introduced N+1 query.

**Evidence:**
- No config changes
- No infrastructure changes
- Only code deploy
- Error coincides with deploy

**Action:** Rollback deploy.
```

## Anti-Patterns

### Don't Skip Obvious Checks

```markdown
# Bad: Jump to complex solutions
## Database Slow

Must be a query optimization issue. Let's analyze query plans...

# Good: Check basics first
## Database Slow

1. Is the database actually running?
2. Can we connect to it?
3. Are there any locks?
4. What does the slow query log show?
```

### Don't Guess Randomly

```markdown
# Bad: Random changes
## API Errors

Let's try:
- Restarting the database
- Scaling to 100 pods
- Changing the load balancer config
- Updating the kernel

# Good: Systematic approach
## API Errors

1. What is the actual error message?
2. When did it start?
3. What changed before it started?
4. Can we reproduce it?
```

### Don't Skip Documentation

```markdown
# Bad: No notes
## Fixed It

I restarted some pods and now it works.

# Good: Document findings
## Resolution

**Root Cause:** Memory leak in worker process
**Evidence:** Pod memory climbing linearly over 6 hours
**Temporary Fix:** Restarted pods
**Long-term Fix:** PR #1234 fixes memory leak
**Prevention:** Added memory usage alerts
```

## Related Skills

- **runbook-structure**: Organizing operational documentation
- **incident-response**: Handling production incidents
