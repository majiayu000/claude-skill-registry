---
name: Failure Modes Analysis
description: Comprehensive guide to identifying, analyzing, and documenting failure modes in distributed systems
---

# Failure Modes Analysis

## Overview

Failure Modes Analysis is a systematic approach to identifying, categorizing, and mitigating potential failures in distributed systems. This skill teaches you how to anticipate system failures, understand their impact, and design resilient systems that gracefully handle various failure scenarios.

## 1. Understanding Failure Modes vs Failure Causes

### Failure Mode
**What the system does wrong** - the observable symptom or behavior when something fails.

Examples:
- Service returns 500 errors
- Database queries timeout
- Messages are lost
- Data becomes inconsistent

### Failure Cause
**Why the failure happened** - the root reason behind the failure mode.

Examples:
- Out of memory
- Network partition
- Disk full
- Bug in code

### The Relationship
```
Failure Cause → Failure Mode → Impact

Example:
Disk Full (cause) → Database writes fail (mode) → Users can't save data (impact)
```

## 2. Common Failure Modes in Distributed Systems

### 2.1 Network Partitions

**Description**: Network segments become isolated from each other, preventing communication.

**Characteristics**:
- Nodes can't communicate across partition boundary
- Each partition may continue operating independently
- Can lead to split-brain scenarios

**Example Scenario**:
```
Region A: [Service-1] [Service-2] [DB-Primary]
          |
          X  <-- Network partition
          |
Region B: [Service-3] [Service-4] [DB-Replica]

- Services in Region A can't reach Region B
- Both regions may elect their own leader
- Data divergence occurs
```

**Detection**:
- Heartbeat timeouts
- Consensus algorithm failures
- Cross-region request failures

### 2.2 Service Unavailability

**Description**: A service becomes completely unreachable or non-functional.

**Common Causes**:
- Process crash
- Container/pod termination
- Deployment failure
- Host failure

**Impact Patterns**:
```
Synchronous calls:  Request → [X Service Down] → Immediate failure
Asynchronous calls: Message → [Queue] → [X Service Down] → Delayed processing
```

### 2.3 Cascading Failures

**Description**: Failure in one component triggers failures in dependent components.

**Classic Pattern**:
```
1. Service A becomes slow (high latency)
2. Service B (depends on A) exhausts connection pool waiting
3. Service B becomes unavailable
4. Service C (depends on B) starts failing
5. System-wide outage
```

**Prevention**:
- Circuit breakers
- Timeouts
- Bulkheads
- Rate limiting

### 2.4 Resource Exhaustion

#### CPU Exhaustion
```
Symptoms:
- High CPU usage (>90%)
- Request latency increases
- Timeouts occur

Causes:
- Infinite loops
- Inefficient algorithms
- Traffic spike
- Crypto-mining malware
```

#### Memory Exhaustion
```
Symptoms:
- OOM (Out of Memory) errors
- Process crashes
- Swap thrashing
- GC pauses

Causes:
- Memory leaks
- Large object allocation
- Cache growth
- Connection leaks
```

#### Disk Exhaustion
```
Symptoms:
- Write failures
- Log rotation stops
- Database corruption
- Application crashes

Causes:
- Unbounded log growth
- Large file uploads
- Database growth
- Temp file accumulation
```

#### Connection Pool Exhaustion
```
Symptoms:
- "No available connections" errors
- Request queueing
- Timeouts
- Cascading failures

Causes:
- Connection leaks
- Slow queries holding connections
- Traffic spike
- Misconfigured pool size
```

### 2.5 Database Failures

**Primary Database Failure**:
```
Impact:
- Write operations fail immediately
- Read operations may succeed (if replicas exist)
- Failover time = downtime (typically 30s-5min)

Recovery:
1. Detect primary failure
2. Promote replica to primary
3. Update connection strings/DNS
4. Resume operations
```

**Replica Lag**:
```
Problem:
Primary: [Write at T=100] → Data committed
Replica: [Still at T=95]  → Stale data

Impact:
- Read-after-write inconsistency
- Users see old data
- Analytics reports incorrect data
```

### 2.6 Dependency Failures

**External API Failure**:
```typescript
// Payment service depends on Stripe API
async function processPayment(amount: number) {
  try {
    const result = await stripe.charges.create({ amount });
    return result;
  } catch (error) {
    // Stripe is down - what now?
    // - Retry?
    // - Queue for later?
    // - Fail the request?
    // - Use backup payment processor?
  }
}
```

**Dependency Mapping**:
```
Your Service
├── Auth Service (critical)
├── Payment Service (critical)
├── Email Service (non-critical)
├── Analytics Service (non-critical)
└── Recommendation Service (non-critical)

Failure strategy:
- Critical: Circuit breaker + fallback
- Non-critical: Fail silently or degrade gracefully
```

### 2.7 Configuration Errors

**Bad Configuration Push**:
```
Scenario: Deploy new config with typo in database connection string

Impact:
- All instances restart
- All fail to connect to database
- Complete service outage

Prevention:
- Config validation
- Gradual rollout
- Automated rollback
- Canary deployments
```

### 2.8 Data Corruption

**Types**:
1. **Silent corruption**: Data is wrong but no error is raised
2. **Detected corruption**: Checksums fail, validation errors
3. **Partial corruption**: Some records are corrupted

**Example**:
```sql
-- Corrupted user record
{
  "id": 12345,
  "email": "user@example.com",
  "balance": null,  -- Should never be null!
  "created_at": "2024-13-45"  -- Invalid date
}
```

## 3. Failure Mode and Effects Analysis (FMEA)

### FMEA Template

| Component | Failure Mode | Failure Cause | Effect | Severity | Likelihood | Detection | RPN | Mitigation |
|-----------|--------------|---------------|--------|----------|------------|-----------|-----|------------|
| API Gateway | Returns 503 | Memory exhaustion | Users can't access system | SEV1 | Medium | Health checks | 120 | Add memory limits, auto-scaling |
| Database | Write timeout | Disk full | Data loss | SEV0 | Low | Disk monitoring | 80 | Disk alerts, auto-cleanup |
| Cache | Evicts all keys | Redis restart | Slow responses | SEV3 | Medium | Cache hit rate | 60 | Persistent cache, warm-up |

**RPN (Risk Priority Number)** = Severity × Likelihood × Detection Difficulty

### FMEA Process

```
1. Identify component
2. List potential failure modes
3. Determine effects of each failure
4. Assign severity rating (1-10)
5. Identify causes
6. Assign likelihood rating (1-10)
7. Identify detection methods
8. Assign detection rating (1-10)
9. Calculate RPN
10. Prioritize high RPN items
11. Design mitigations
```

## 4. Severity Classification

### SEV0 - Critical
```
Impact: Complete service outage, data loss, security breach
Response: Immediate all-hands response
Examples:
- Database deleted
- Security breach with data exfiltration
- Complete datacenter failure
- Payment processing completely down
```

### SEV1 - High
```
Impact: Major functionality unavailable, significant user impact
Response: Immediate response during business hours
Examples:
- Login system down
- Payment processing degraded
- API returning 50%+ errors
- Primary database down (with failover working)
```

### SEV2 - Medium
```
Impact: Partial functionality degraded, some users affected
Response: Response within hours
Examples:
- Search feature slow
- Email notifications delayed
- Admin dashboard unavailable
- Single region degraded
```

### SEV3 - Low
```
Impact: Minor functionality affected, workaround available
Response: Fix in next release
Examples:
- UI glitch
- Non-critical feature broken
- Slow analytics dashboard
- Cosmetic issues
```

### SEV4 - Minimal
```
Impact: No user impact, internal tooling only
Response: Fix when convenient
Examples:
- Internal monitoring dashboard slow
- Development environment issue
- Documentation typo
```

## 5. Detecting Failure Modes

### 5.1 Health Checks

```typescript
// Comprehensive health check
interface HealthCheck {
  status: 'healthy' | 'degraded' | 'unhealthy';
  checks: {
    database: CheckResult;
    cache: CheckResult;
    dependencies: CheckResult;
    resources: CheckResult;
  };
  timestamp: string;
}

async function performHealthCheck(): Promise<HealthCheck> {
  const checks = await Promise.all([
    checkDatabase(),
    checkCache(),
    checkDependencies(),
    checkResources()
  ]);

  const overallStatus = checks.every(c => c.healthy)
    ? 'healthy'
    : checks.some(c => c.critical && !c.healthy)
    ? 'unhealthy'
    : 'degraded';

  return {
    status: overallStatus,
    checks: {
      database: checks[0],
      cache: checks[1],
      dependencies: checks[2],
      resources: checks[3]
    },
    timestamp: new Date().toISOString()
  };
}

async function checkDatabase(): Promise<CheckResult> {
  try {
    const start = Date.now();
    await db.query('SELECT 1');
    const latency = Date.now() - start;

    return {
      healthy: latency < 100,
      critical: true,
      latency,
      message: latency < 100 ? 'OK' : 'High latency'
    };
  } catch (error) {
    return {
      healthy: false,
      critical: true,
      error: error.message,
      message: 'Database unreachable'
    };
  }
}
```

### 5.2 Circuit Breakers

```typescript
class CircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private lastFailureTime?: number;

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000,
    private resetTimeout: number = 30000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime! > this.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    if (this.state === 'HALF_OPEN') {
      this.state = 'CLOSED';
    }
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }

  getState() {
    return this.state;
  }
}
```

### 5.3 Timeouts

```typescript
// Timeout configuration by operation type
const TIMEOUTS = {
  database: {
    connect: 5000,
    query: 10000,
    transaction: 30000
  },
  http: {
    connect: 3000,
    read: 10000,
    total: 15000
  },
  cache: {
    get: 100,
    set: 200
  }
};

// Timeout wrapper
async function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  operation: string
): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(
      () => reject(new Error(`${operation} timeout after ${timeoutMs}ms`)),
      timeoutMs
    )
  );

  return Promise.race([promise, timeout]);
}

// Usage
const user = await withTimeout(
  db.query('SELECT * FROM users WHERE id = $1', [userId]),
  TIMEOUTS.database.query,
  'Database query'
);
```

### 5.4 Error Rates

```typescript
// Error rate monitoring
class ErrorRateMonitor {
  private requests: { timestamp: number; success: boolean }[] = [];
  private windowMs = 60000; // 1 minute

  recordRequest(success: boolean) {
    this.requests.push({ timestamp: Date.now(), success });
    this.cleanup();
  }

  getErrorRate(): number {
    this.cleanup();
    if (this.requests.length === 0) return 0;

    const errors = this.requests.filter(r => !r.success).length;
    return errors / this.requests.length;
  }

  isHealthy(threshold: number = 0.05): boolean {
    return this.getErrorRate() < threshold;
  }

  private cleanup() {
    const cutoff = Date.now() - this.windowMs;
    this.requests = this.requests.filter(r => r.timestamp > cutoff);
  }
}
```

## 6. Failure Mode Documentation

### Failure Mode Document Template

```markdown
# Failure Mode: [Name]

## Identification
- **ID**: FM-001
- **Component**: API Gateway
- **Subsystem**: Request Routing
- **Discovered**: 2024-01-15
- **Severity**: SEV1

## Description
Brief description of what goes wrong when this failure occurs.

## Symptoms
Observable signs that this failure is occurring:
- High error rate on /api/v1/* endpoints
- 503 Service Unavailable responses
- Request queue depth > 1000

## Root Causes
Known causes that trigger this failure mode:
1. Memory leak in routing module
2. Sudden traffic spike (>10x normal)
3. Downstream service timeout

## Impact
- **User Impact**: Users cannot access API
- **Business Impact**: Revenue loss, SLA breach
- **Blast Radius**: All API consumers
- **Data Impact**: No data loss

## Detection
- **Automated**: Health check fails, error rate alert
- **Manual**: User reports, monitoring dashboard
- **MTTD**: ~2 minutes (Mean Time To Detect)

## Mitigation
Immediate actions to reduce impact:
1. Scale up API Gateway instances
2. Enable rate limiting
3. Failover to backup region

## Prevention
Long-term fixes to prevent recurrence:
1. Fix memory leak
2. Implement auto-scaling
3. Add circuit breakers for downstream services

## Runbook
Link to operational runbook: [Runbook-001](./runbooks/api-gateway-overload.md)

## Related Incidents
- INC-2024-001: API Gateway outage on 2024-01-10
- INC-2024-015: Partial degradation on 2024-01-12
```

## 7. Single Points of Failure (SPOF) Identification

### SPOF Analysis Checklist

```
Infrastructure Layer:
□ Single load balancer
□ Single database instance
□ Single cache instance
□ Single message queue
□ Single DNS server
□ Single network path

Application Layer:
□ Single API gateway
□ Single authentication service
□ Single payment processor
□ Shared session store
□ Centralized configuration service

Data Layer:
□ Single data center
□ Single backup location
□ Single replication stream
□ Master-only writes

External Dependencies:
□ Single cloud provider
□ Single CDN
□ Single payment gateway
□ Single email provider
```

### SPOF Mitigation Strategies

```
1. Redundancy
   - Active-Active: Multiple instances serving traffic
   - Active-Passive: Standby ready to take over
   - N+1: One extra instance beyond minimum needed

2. Geographic Distribution
   - Multi-region deployment
   - Cross-datacenter replication
   - Edge caching

3. Failover Mechanisms
   - Automatic failover (DNS, load balancer)
   - Manual failover (controlled switchover)
   - Gradual failover (traffic shifting)

4. Dependency Alternatives
   - Multiple payment processors
   - Multiple cloud providers
   - Multiple CDNs
```

## 8. Blast Radius Analysis

### Blast Radius Definition
The maximum scope of impact if a component fails completely.

### Blast Radius Calculation

```
Component: User Authentication Service

Direct Impact:
- All login attempts fail
- All authenticated API calls fail
- Session validation fails

Indirect Impact:
- New user signups blocked
- Password resets unavailable
- OAuth flows broken

Affected Users:
- Total users: 1,000,000
- Active users (hourly): 50,000
- Blast radius: 100% of active users

Affected Services:
- Web application (critical)
- Mobile app (critical)
- Admin dashboard (critical)
- Public API (critical)
- Blast radius: 4/4 services (100%)

Business Impact:
- Revenue: $10,000/hour
- SLA credits: $50,000 if >1 hour
- Reputation: High
```

### Blast Radius Reduction

```typescript
// Strategy 1: Graceful degradation
async function authenticateUser(token: string) {
  try {
    return await authService.validate(token);
  } catch (error) {
    // Fallback to cached authentication
    return await cachedAuth.validate(token);
  }
}

// Strategy 2: Bulkheads (isolation)
// Separate thread pools for different tenants
const tenantPools = {
  'tenant-premium': new ThreadPool(100),
  'tenant-standard': new ThreadPool(50),
  'tenant-free': new ThreadPool(10)
};

// Strategy 3: Rate limiting per client
const rateLimiter = new RateLimiter({
  perClient: 100, // requests per minute
  global: 10000   // total requests per minute
});
```

## 9. Common Failure Patterns

### 9.1 Split-Brain Scenarios

```
Problem: Network partition causes two nodes to both think they're the leader

Scenario:
Node A (Region 1): "I'm the leader, accepting writes"
Node B (Region 2): "I'm the leader, accepting writes"

Result: Data divergence, conflicts, inconsistency

Prevention:
- Quorum-based consensus (Raft, Paxos)
- Fencing tokens
- Witness nodes in third location
```

### 9.2 Thundering Herd

```
Problem: Many clients simultaneously retry after a failure

Scenario:
1. Service goes down
2. 10,000 clients detect failure
3. All clients retry at same time
4. Service comes back up
5. Service immediately overwhelmed by 10,000 requests
6. Service goes down again
7. Repeat

Prevention:
- Exponential backoff with jitter
- Circuit breakers
- Rate limiting
- Gradual traffic ramp-up
```

```typescript
// Jittered exponential backoff
function calculateBackoff(attempt: number): number {
  const baseDelay = 1000; // 1 second
  const maxDelay = 60000; // 60 seconds
  const exponentialDelay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
  const jitter = Math.random() * exponentialDelay * 0.3; // ±30% jitter
  return exponentialDelay + jitter;
}
```

### 9.3 Retry Storms

```
Problem: Cascading retries amplify load

Scenario:
Client → Service A → Service B → Service C

Service C fails:
- Service B retries 3 times
- Service A retries 3 times
- Client retries 3 times
- Total requests to C: 1 × 3 × 3 × 3 = 27x amplification!

Prevention:
- Retry budgets
- End-to-end request deadlines
- Circuit breakers at each layer
```

### 9.4 Poison Pill Messages

```
Problem: A message that always causes processing to fail

Scenario:
1. Message arrives in queue
2. Consumer processes message
3. Message causes crash (malformed data, bug trigger)
4. Consumer restarts
5. Picks up same message
6. Crashes again
7. Infinite crash loop

Prevention:
- Dead letter queues (DLQ)
- Max retry count
- Message validation before processing
- Poison pill detection
```

```typescript
async function processMessage(message: Message) {
  const retryCount = message.attributes.retryCount || 0;
  const maxRetries = 3;

  try {
    await handleMessage(message);
    await message.ack();
  } catch (error) {
    if (retryCount >= maxRetries) {
      // Move to dead letter queue
      await dlq.send(message);
      await message.ack();
      logger.error('Poison pill detected', { message, error });
    } else {
      // Retry with backoff
      await message.nack({
        retryCount: retryCount + 1,
        delay: calculateBackoff(retryCount)
      });
    }
  }
}
```

## 10. Byzantine Failures

### Definition
Failures where components behave arbitrarily or maliciously, providing incorrect or inconsistent information.

### Examples

```
1. Corrupted Data
   Node returns valid-looking but incorrect data
   
2. Inconsistent Responses
   Node returns different answers to different requesters
   
3. Timing Attacks
   Node delays responses strategically
   
4. Malicious Behavior
   Compromised node actively tries to disrupt system
```

### Byzantine Fault Tolerance

```
Requirements:
- Need 3f + 1 nodes to tolerate f Byzantine failures
- Example: To tolerate 1 Byzantine node, need 4 total nodes

Algorithms:
- PBFT (Practical Byzantine Fault Tolerance)
- Blockchain consensus (Proof of Work, Proof of Stake)
- Tendermint
```

## 11. Gray Failures (Partial Failures)

### Definition
Failures that are not complete outages but cause degraded performance or intermittent errors.

### Characteristics

```
- Hard to detect (not clearly up or down)
- May pass health checks
- Affect only some requests
- Often timing-dependent
- Can be worse than complete failures (no clear failover)
```

### Examples

```
1. Slow Disk
   - 95% of requests succeed normally
   - 5% of requests timeout
   - Health checks pass (they're in the 95%)

2. Network Flakiness
   - Packets dropped intermittently
   - Some connections succeed, others fail
   - Retries sometimes work

3. Memory Pressure
   - GC pauses cause intermittent slowness
   - Most requests fine, some timeout
   - Gradually gets worse

4. Partial Database Corruption
   - Most queries work
   - Specific rows/tables corrupted
   - Affects only certain users
```

### Detection

```typescript
// Percentile-based health checks
class GrayFailureDetector {
  private latencies: number[] = [];

  recordLatency(latency: number) {
    this.latencies.push(latency);
    if (this.latencies.length > 1000) {
      this.latencies.shift();
    }
  }

  isHealthy(): boolean {
    if (this.latencies.length < 100) return true;

    const sorted = [...this.latencies].sort((a, b) => a - b);
    const p50 = sorted[Math.floor(sorted.length * 0.5)];
    const p99 = sorted[Math.floor(sorted.length * 0.99)];

    // Healthy if p99 < 2x p50 (low variance)
    // Gray failure if p99 >> p50 (high variance)
    return p99 < p50 * 2;
  }
}
```

## 12. Testing Failure Modes (Chaos Engineering Preview)

### Basic Failure Injection

```typescript
// Simulate random failures
class ChaosMiddleware {
  constructor(
    private failureRate: number = 0.01, // 1% failure rate
    private enabled: boolean = false
  ) {}

  async handle(req: Request, res: Response, next: NextFunction) {
    if (!this.enabled) {
      return next();
    }

    if (Math.random() < this.failureRate) {
      const chaos = this.selectChaos();
      return chaos(req, res);
    }

    next();
  }

  private selectChaos() {
    const scenarios = [
      this.injectLatency,
      this.injectError,
      this.injectTimeout
    ];
    return scenarios[Math.floor(Math.random() * scenarios.length)];
  }

  private injectLatency(req: Request, res: Response) {
    const delay = Math.random() * 5000; // 0-5 seconds
    setTimeout(() => {
      res.status(200).json({ chaos: 'latency', delay });
    }, delay);
  }

  private injectError(req: Request, res: Response) {
    res.status(500).json({ chaos: 'error', message: 'Simulated failure' });
  }

  private injectTimeout(req: Request, res: Response) {
    // Never respond (simulate timeout)
  }
}
```

## 13. Real-World Failure Case Studies

### Case Study 1: AWS S3 Outage (2017)

```
Incident: S3 US-EAST-1 outage on February 28, 2017

Failure Mode: Service unavailability

Root Cause:
- Engineer ran debug command to remove small number of servers
- Typo in command removed large number of servers
- Removal process took longer than expected
- Subsystems had to be restarted in specific order

Impact:
- 4-hour outage
- Affected thousands of websites and services
- $150M+ in economic impact

Lessons:
1. Command-line tools need better safeguards
2. Removal processes should have rate limits
3. Subsystems should restart independently
4. Need better tooling for large-scale operations
```

### Case Study 2: GitLab Database Incident (2017)

```
Incident: Accidental database deletion on January 31, 2017

Failure Mode: Data loss

Root Cause:
- Production database under heavy load
- Engineer tried to remove directory on wrong server
- Removed production database instead of staging
- Backup systems had failed (silently)

Impact:
- 6 hours of data lost
- 18 hours to recover
- 5,000 projects affected

Lessons:
1. Test backups regularly
2. Monitor backup systems
3. Require confirmation for destructive operations
4. Use infrastructure as code
5. Implement better access controls
```

### Case Study 3: Knight Capital Trading Error (2012)

```
Incident: $440 million loss in 45 minutes

Failure Mode: Incorrect behavior (Byzantine failure)

Root Cause:
- Deployed new code to 7 of 8 servers
- 8th server had old code with repurposed flag
- Old code activated, started buying at ask, selling at bid
- Lost $10M per minute

Impact:
- $440M loss
- Company nearly bankrupted
- Acquired by competitor

Lessons:
1. Ensure atomic deployments
2. Verify all servers updated
3. Have kill switches for automated systems
4. Monitor for anomalous behavior
5. Implement position limits
```

## 14. Failure Mode Prevention Strategies

### 1. Defense in Depth

```
Layer 1: Prevent failures
- Code reviews
- Testing (unit, integration, chaos)
- Static analysis
- Deployment safeguards

Layer 2: Detect failures quickly
- Monitoring
- Alerting
- Health checks
- Anomaly detection

Layer 3: Limit blast radius
- Circuit breakers
- Bulkheads
- Rate limiting
- Graceful degradation

Layer 4: Recover quickly
- Automated failover
- Auto-scaling
- Self-healing
- Runbooks

Layer 5: Learn from failures
- Postmortems
- Incident reviews
- Failure mode documentation
- Continuous improvement
```

### 2. Chaos Engineering

```
Proactively inject failures to:
- Verify failure detection works
- Test recovery procedures
- Build confidence in system resilience
- Identify unknown failure modes

See: 40-system-resilience/chaos-engineering/SKILL.md
```

### 3. Observability

```
Three Pillars:
1. Metrics: What is happening (error rate, latency, throughput)
2. Logs: Why it's happening (error messages, stack traces)
3. Traces: Where it's happening (distributed request flow)

Failure Detection:
- Error rate > threshold
- Latency p99 > threshold
- Throughput < threshold
- Resource utilization > threshold
```

### 4. Redundancy and Replication

```
Redundancy Types:
- Active-Active: All instances serve traffic
- Active-Passive: Standby ready to take over
- N+1: One spare beyond minimum needed
- N+2: Two spares (for maintenance + failure)

Replication:
- Synchronous: Strong consistency, higher latency
- Asynchronous: Eventual consistency, lower latency
- Semi-synchronous: Hybrid approach
```

### 5. Graceful Degradation

```
Priority Levels:
P0 (Critical): Must work (authentication, payment)
P1 (Important): Should work (search, recommendations)
P2 (Nice-to-have): Can fail (analytics, tracking)

Degradation Strategy:
if (authService.isDown()) {
  // P0: Use cached credentials
}

if (searchService.isDown()) {
  // P1: Return cached results
}

if (analyticsService.isDown()) {
  // P2: Silently fail
}
```

## Summary

Failure Modes Analysis is essential for building resilient distributed systems. Key takeaways:

1. **Understand the difference** between failure modes (symptoms) and failure causes (root reasons)
2. **Document common failure modes** in your system and how to detect them
3. **Use FMEA** to systematically analyze and prioritize failure risks
4. **Implement detection mechanisms**: health checks, circuit breakers, timeouts, error rate monitoring
5. **Identify and eliminate SPOFs** (Single Points of Failure)
6. **Analyze blast radius** to understand failure impact
7. **Learn from real-world incidents** to avoid repeating mistakes
8. **Test failure modes** proactively through chaos engineering
9. **Build defense in depth** with multiple layers of protection
10. **Document everything** so your team can respond effectively

## Related Skills

- `40-system-resilience/chaos-engineering` - Proactive failure testing
- `40-system-resilience/retry-timeout-strategies` - Handling transient failures
- `40-system-resilience/disaster-recovery` - Recovering from catastrophic failures
- `40-system-resilience/postmortem-analysis` - Learning from incidents
