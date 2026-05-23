---
name: Bulkhead Patterns
description: Resource isolation strategies to prevent cascading failures and limit blast radius in distributed systems
---

# Bulkhead Patterns

## Overview

The Bulkhead pattern is a resilience design pattern that isolates resources to prevent failures in one part of a system from cascading to other parts. Named after the watertight compartments in ships that prevent the entire vessel from sinking if one compartment is breached.

**Core Principle**: "Isolate critical resources so that failure in one area doesn't sink the entire system."

---

## Core Concepts

### 1. Bulkhead Pattern Origin (Ship Compartments)

### The Titanic Lesson

```
Traditional Ship (No Bulkheads):
[=================================]
Hull breach → Entire ship floods → Ship sinks

Modern Ship (With Bulkheads):
[====|====|====|====|====|====|====]
Hull breach → One compartment floods → Ship stays afloat
```

### Software Analogy

```
Monolith Without Bulkheads:
[Thread Pool: 200 threads]
Slow API call uses all threads → Entire service hangs

Monolith With Bulkheads:
[API A: 50 threads] [API B: 50 threads] [API C: 50 threads] [Reserve: 50 threads]
Slow API A uses all its threads → APIs B and C continue working
```

## 2. Resource Isolation Principles

### Key Concepts

1. **Compartmentalization**: Divide resources into isolated pools
2. **Failure Containment**: Limit blast radius of failures
3. **Resource Guarantees**: Each component gets dedicated resources
4. **Graceful Degradation**: System continues operating with reduced capacity

### Benefits

```
✓ Prevents cascading failures
✓ Limits blast radius
✓ Improves fault isolation
✓ Enables independent scaling
✓ Protects critical paths
✓ Improves system observability
```

### Trade-offs

```
✗ Reduced resource efficiency (some pools may be underutilized)
✗ Increased complexity (managing multiple pools)
✗ Requires careful sizing
✗ May need more total resources
```

## 3. Types of Bulkheads

### 3.1 Thread Pool Bulkheads

**Concept**: Separate thread pools for different operations.

```typescript
// Without bulkheads - shared thread pool
class APIGateway {
  private threadPool = new ThreadPool(100); // Shared by all

  async handleRequest(req: Request) {
    return this.threadPool.execute(() => this.processRequest(req));
  }
}

// Problem: Slow endpoint consumes all threads, blocking all requests
```

```typescript
// With bulkheads - separate thread pools
class APIGateway {
  private pools = {
    critical: new ThreadPool(40),    // Critical endpoints
    standard: new ThreadPool(40),    // Standard endpoints
    batch: new ThreadPool(10),       // Batch operations
    reserve: new ThreadPool(10)      // Reserve capacity
  };

  async handleRequest(req: Request) {
    const pool = this.selectPool(req);
    return pool.execute(() => this.processRequest(req));
  }

  private selectPool(req: Request): ThreadPool {
    if (req.path.startsWith('/api/critical')) return this.pools.critical;
    if (req.path.startsWith('/api/batch')) return this.pools.batch;
    return this.pools.standard;
  }
}
```

**Node.js Implementation** (Worker Threads):

```typescript
import { Worker } from 'worker_threads';

class WorkerPool {
  private workers: Worker[] = [];
  private queue: Array<{ task: any; resolve: Function; reject: Function }> = [];
  private activeWorkers = 0;

  constructor(private poolSize: number, private workerScript: string) {
    for (let i = 0; i < poolSize; i++) {
      this.workers.push(new Worker(workerScript));
    }
  }

  async execute<T>(task: any): Promise<T> {
    return new Promise((resolve, reject) => {
      if (this.activeWorkers < this.poolSize) {
        this.runTask(task, resolve, reject);
      } else {
        this.queue.push({ task, resolve, reject });
      }
    });
  }

  private async runTask(task: any, resolve: Function, reject: Function) {
    const worker = this.workers[this.activeWorkers++];

    worker.once('message', (result) => {
      this.activeWorkers--;
      resolve(result);
      this.processQueue();
    });

    worker.once('error', (error) => {
      this.activeWorkers--;
      reject(error);
      this.processQueue();
    });

    worker.postMessage(task);
  }

  private processQueue() {
    if (this.queue.length > 0 && this.activeWorkers < this.poolSize) {
      const { task, resolve, reject } = this.queue.shift()!;
      this.runTask(task, resolve, reject);
    }
  }
}

// Usage: Separate pools for different workloads
const criticalPool = new WorkerPool(10, './critical-worker.js');
const standardPool = new WorkerPool(20, './standard-worker.js');
const batchPool = new WorkerPool(5, './batch-worker.js');

app.post('/api/critical/process', async (req, res) => {
  const result = await criticalPool.execute(req.body);
  res.json(result);
});

app.post('/api/standard/process', async (req, res) => {
  const result = await standardPool.execute(req.body);
  res.json(result);
});
```

### 3.2 Connection Pool Bulkheads

**Concept**: Separate database connection pools for different services/tenants.

```typescript
// Database connection bulkheads
import { Pool } from 'pg';

class DatabaseBulkheads {
  private pools = {
    readWrite: new Pool({
      host: 'primary.db.example.com',
      max: 20,  // 20 connections for read-write operations
      idleTimeoutMillis: 30000
    }),
    readOnly: new Pool({
      host: 'replica.db.example.com',
      max: 50,  // 50 connections for read-only operations
      idleTimeoutMillis: 30000
    }),
    analytics: new Pool({
      host: 'analytics.db.example.com',
      max: 10,  // 10 connections for analytics queries
      idleTimeoutMillis: 60000
    })
  };

  async executeWrite(query: string, params: any[]) {
    const client = await this.pools.readWrite.connect();
    try {
      return await client.query(query, params);
    } finally {
      client.release();
    }
  }

  async executeRead(query: string, params: any[]) {
    const client = await this.pools.readOnly.connect();
    try {
      return await client.query(query, params);
    } finally {
      client.release();
    }
  }

  async executeAnalytics(query: string, params: any[]) {
    const client = await this.pools.analytics.connect();
    try {
      return await client.query(query, params);
    } finally {
      client.release();
    }
  }
}

// Usage
const db = new DatabaseBulkheads();

// Critical user-facing queries use readWrite pool
app.post('/api/users', async (req, res) => {
  const result = await db.executeWrite(
    'INSERT INTO users (name, email) VALUES ($1, $2)',
    [req.body.name, req.body.email]
  );
  res.json(result.rows[0]);
});

// Analytics queries use separate pool
app.get('/api/analytics/report', async (req, res) => {
  const result = await db.executeAnalytics(
    'SELECT date, COUNT(*) FROM events GROUP BY date',
    []
  );
  res.json(result.rows);
});
```

### 3.3 Semaphore Bulkheads

**Concept**: Limit concurrent operations using semaphores.

```typescript
class Semaphore {
  private permits: number;
  private queue: Array<() => void> = [];

  constructor(permits: number) {
    this.permits = permits;
  }

  async acquire(): Promise<void> {
    if (this.permits > 0) {
      this.permits--;
      return Promise.resolve();
    }

    return new Promise((resolve) => {
      this.queue.push(resolve);
    });
  }

  release(): void {
    this.permits++;
    const resolve = this.queue.shift();
    if (resolve) {
      this.permits--;
      resolve();
    }
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    await this.acquire();
    try {
      return await fn();
    } finally {
      this.release();
    }
  }
}

// Bulkheads using semaphores
class SemaphoreBulkheads {
  private semaphores = {
    externalAPI: new Semaphore(10),   // Max 10 concurrent external API calls
    database: new Semaphore(20),       // Max 20 concurrent DB queries
    fileSystem: new Semaphore(5)       // Max 5 concurrent file operations
  };

  async callExternalAPI(url: string) {
    return this.semaphores.externalAPI.execute(async () => {
      return await fetch(url);
    });
  }

  async queryDatabase(query: string) {
    return this.semaphores.database.execute(async () => {
      return await db.query(query);
    });
  }

  async readFile(path: string) {
    return this.semaphores.fileSystem.execute(async () => {
      return await fs.readFile(path);
    });
  }
}
```

### 3.4 Process Isolation

**Concept**: Run different workloads in separate processes.

```typescript
// Master process
import { fork } from 'child_process';

class ProcessBulkhead {
  private workers: Map<string, any> = new Map();

  constructor() {
    // Spawn separate processes for different workloads
    this.workers.set('api', fork('./workers/api-worker.js'));
    this.workers.set('batch', fork('./workers/batch-worker.js'));
    this.workers.set('analytics', fork('./workers/analytics-worker.js'));
  }

  async execute(workload: string, task: any): Promise<any> {
    const worker = this.workers.get(workload);
    if (!worker) throw new Error(`Unknown workload: ${workload}`);

    return new Promise((resolve, reject) => {
      worker.once('message', resolve);
      worker.once('error', reject);
      worker.send(task);
    });
  }
}

// Usage
const bulkhead = new ProcessBulkhead();

app.post('/api/process', async (req, res) => {
  const result = await bulkhead.execute('api', req.body);
  res.json(result);
});

app.post('/batch/process', async (req, res) => {
  const result = await bulkhead.execute('batch', req.body);
  res.json(result);
});
```

### 3.5 Service Isolation (Microservices)

**Concept**: Separate services for different domains.

```
Monolith:
[User Service + Order Service + Payment Service + Analytics]
Payment service fails → Entire monolith affected

Microservices:
[User Service] [Order Service] [Payment Service] [Analytics Service]
Payment service fails → Other services continue operating
```

## 4. When to Use Bulkheads

### Use Cases

```
✓ Multi-tenant systems
  - Isolate tenants to prevent noisy neighbor problems

✓ Mixed workload systems
  - Separate critical and non-critical operations

✓ External dependency management
  - Isolate slow/unreliable external services

✓ Rate limiting
  - Limit resources per client/tenant

✓ Priority-based processing
  - Guarantee resources for high-priority requests
```

### Decision Matrix

| Scenario | Bulkhead Type | Reason |
|----------|---------------|--------|
| Multiple external APIs | Thread Pool | Prevent slow API from blocking others |
| Multi-tenant database | Connection Pool | Isolate tenant queries |
| CPU-intensive tasks | Process Isolation | Prevent blocking event loop |
| File uploads | Semaphore | Limit concurrent I/O operations |
| Microservices | Service Isolation | Complete failure isolation |

## 5. Implementation Patterns

### Pattern 1: Priority-Based Bulkheads

```typescript
class PriorityBulkhead {
  private pools = {
    critical: new Semaphore(50),   // 50% capacity
    high: new Semaphore(30),       // 30% capacity
    medium: new Semaphore(15),     // 15% capacity
    low: new Semaphore(5)          // 5% capacity
  };

  async execute<T>(
    priority: 'critical' | 'high' | 'medium' | 'low',
    fn: () => Promise<T>
  ): Promise<T> {
    const pool = this.pools[priority];
    return pool.execute(fn);
  }
}

// Usage
const bulkhead = new PriorityBulkhead();

// Critical: User authentication
app.post('/auth/login', async (req, res) => {
  const result = await bulkhead.execute('critical', async () => {
    return await authenticateUser(req.body);
  });
  res.json(result);
});

// Low: Analytics tracking
app.post('/analytics/track', async (req, res) => {
  bulkhead.execute('low', async () => {
    await trackEvent(req.body);
  }).catch(err => console.error('Analytics failed:', err));
  res.status(202).send(); // Accept immediately
});
```

### Pattern 2: Tenant-Based Bulkheads

```typescript
class TenantBulkhead {
  private pools = new Map<string, Semaphore>();
  private defaultPoolSize = 10;
  private premiumPoolSize = 50;

  getPool(tenantId: string, tier: 'free' | 'premium'): Semaphore {
    if (!this.pools.has(tenantId)) {
      const size = tier === 'premium' ? this.premiumPoolSize : this.defaultPoolSize;
      this.pools.set(tenantId, new Semaphore(size));
    }
    return this.pools.get(tenantId)!;
  }

  async execute<T>(
    tenantId: string,
    tier: 'free' | 'premium',
    fn: () => Promise<T>
  ): Promise<T> {
    const pool = this.getPool(tenantId, tier);
    return pool.execute(fn);
  }
}

// Usage
const tenantBulkhead = new TenantBulkhead();

app.post('/api/process', async (req, res) => {
  const tenantId = req.headers['x-tenant-id'] as string;
  const tier = await getTenantTier(tenantId);

  const result = await tenantBulkhead.execute(tenantId, tier, async () => {
    return await processRequest(req.body);
  });

  res.json(result);
});
```

### Pattern 3: Adaptive Bulkheads

```typescript
class AdaptiveBulkhead {
  private permits: number;
  private maxPermits: number;
  private minPermits: number;
  private successCount = 0;
  private failureCount = 0;

  constructor(initial: number, min: number, max: number) {
    this.permits = initial;
    this.minPermits = min;
    this.maxPermits = max;
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.permits <= 0) {
      throw new Error('Bulkhead full');
    }

    this.permits--;

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    } finally {
      this.permits++;
    }
  }

  private onSuccess() {
    this.successCount++;
    if (this.successCount >= 10) {
      this.increaseCapacity();
      this.successCount = 0;
    }
  }

  private onFailure() {
    this.failureCount++;
    if (this.failureCount >= 5) {
      this.decreaseCapacity();
      this.failureCount = 0;
    }
  }

  private increaseCapacity() {
    if (this.permits < this.maxPermits) {
      this.permits = Math.min(this.permits + 5, this.maxPermits);
      console.log(`Increased capacity to ${this.permits}`);
    }
  }

  private decreaseCapacity() {
    if (this.permits > this.minPermits) {
      this.permits = Math.max(this.permits - 5, this.minPermits);
      console.log(`Decreased capacity to ${this.permits}`);
    }
  }
}
```

## 6. Bulkhead Sizing (Thread Pool Math)

### Little's Law

```
L = λ × W

Where:
L = Number of requests in system (pool size)
λ = Arrival rate (requests per second)
W = Average time in system (seconds)

Example:
- Arrival rate: 100 req/s
- Average processing time: 0.5s
- Pool size needed: 100 × 0.5 = 50 threads
```

### Sizing Formula

```typescript
interface WorkloadCharacteristics {
  requestsPerSecond: number;
  avgProcessingTimeMs: number;
  p99ProcessingTimeMs: number;
  targetUtilization: number; // 0.7 = 70%
}

function calculatePoolSize(workload: WorkloadCharacteristics): number {
  // Use p99 latency for safety
  const avgTimeSeconds = workload.p99ProcessingTimeMs / 1000;
  
  // Little's Law
  const baseSize = workload.requestsPerSecond * avgTimeSeconds;
  
  // Add buffer for target utilization
  const sizeWithBuffer = baseSize / workload.targetUtilization;
  
  return Math.ceil(sizeWithBuffer);
}

// Example
const apiWorkload: WorkloadCharacteristics = {
  requestsPerSecond: 100,
  avgProcessingTimeMs: 200,
  p99ProcessingTimeMs: 500,
  targetUtilization: 0.7
};

const poolSize = calculatePoolSize(apiWorkload);
console.log(`Recommended pool size: ${poolSize}`); // ~72 threads
```

### Multi-Pool Sizing

```typescript
interface SystemCapacity {
  totalThreads: number;
  workloads: {
    name: string;
    priority: number; // 1-10
    requestsPerSecond: number;
    avgProcessingTimeMs: number;
  }[];
}

function allocatePoolSizes(system: SystemCapacity): Map<string, number> {
  const totalPriority = system.workloads.reduce((sum, w) => sum + w.priority, 0);
  const allocation = new Map<string, number>();

  for (const workload of system.workloads) {
    // Allocate based on priority
    const share = (workload.priority / totalPriority) * system.totalThreads;
    
    // Verify it meets demand
    const demand = (workload.requestsPerSecond * workload.avgProcessingTimeMs) / 1000;
    
    // Use max of priority-based and demand-based
    const poolSize = Math.max(Math.ceil(share), Math.ceil(demand * 1.5));
    
    allocation.set(workload.name, poolSize);
  }

  return allocation;
}

// Example
const system: SystemCapacity = {
  totalThreads: 100,
  workloads: [
    { name: 'critical', priority: 10, requestsPerSecond: 50, avgProcessingTimeMs: 200 },
    { name: 'standard', priority: 5, requestsPerSecond: 100, avgProcessingTimeMs: 100 },
    { name: 'batch', priority: 2, requestsPerSecond: 10, avgProcessingTimeMs: 1000 }
  ]
};

const allocation = allocatePoolSizes(system);
// critical: 50 threads
// standard: 31 threads
// batch: 15 threads
```

## 7. Monitoring Bulkhead Health

```typescript
class MonitoredBulkhead {
  private semaphore: Semaphore;
  private metrics = {
    totalRequests: 0,
    activeRequests: 0,
    queuedRequests: 0,
    rejectedRequests: 0,
    avgWaitTime: 0,
    maxWaitTime: 0
  };

  constructor(permits: number) {
    this.semaphore = new Semaphore(permits);
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    this.metrics.totalRequests++;
    const startWait = Date.now();

    try {
      await this.semaphore.acquire();
      const waitTime = Date.now() - startWait;
      this.updateWaitTimeMetrics(waitTime);

      this.metrics.activeRequests++;
      return await fn();
    } catch (error) {
      this.metrics.rejectedRequests++;
      throw error;
    } finally {
      this.metrics.activeRequests--;
      this.semaphore.release();
    }
  }

  private updateWaitTimeMetrics(waitTime: number) {
    this.metrics.maxWaitTime = Math.max(this.metrics.maxWaitTime, waitTime);
    this.metrics.avgWaitTime =
      (this.metrics.avgWaitTime * (this.metrics.totalRequests - 1) + waitTime) /
      this.metrics.totalRequests;
  }

  getMetrics() {
    return {
      ...this.metrics,
      utilization: this.metrics.activeRequests / this.semaphore['permits'],
      rejectionRate: this.metrics.rejectedRequests / this.metrics.totalRequests
    };
  }
}

// Export metrics
app.get('/metrics/bulkheads', (req, res) => {
  const metrics = {
    critical: criticalBulkhead.getMetrics(),
    standard: standardBulkhead.getMetrics(),
    batch: batchBulkhead.getMetrics()
  };
  res.json(metrics);
});
```

## 8. Bulkheads in Different Architectures

### Monoliths

```typescript
// Bulkheads within a monolith
class MonolithWithBulkheads {
  private pools = {
    userService: new Semaphore(30),
    orderService: new Semaphore(30),
    paymentService: new Semaphore(20),
    analyticsService: new Semaphore(10),
    reserve: new Semaphore(10)
  };

  async handleUserRequest(req: Request) {
    return this.pools.userService.execute(() => this.processUserRequest(req));
  }

  async handleOrderRequest(req: Request) {
    return this.pools.orderService.execute(() => this.processOrderRequest(req));
  }

  async handlePaymentRequest(req: Request) {
    return this.pools.paymentService.execute(() => this.processPaymentRequest(req));
  }
}
```

### Microservices

```
Service-level bulkheads (natural isolation):

[User Service]     [Order Service]    [Payment Service]
  - 10 instances     - 15 instances      - 5 instances
  - 2 CPU each       - 2 CPU each        - 4 CPU each
  - 4GB RAM each     - 4GB RAM each      - 8GB RAM each

Payment service failure doesn't affect User or Order services
```

### Serverless

```typescript
// Lambda concurrency limits as bulkheads
// AWS Lambda: Reserved concurrency per function

// Critical function: 100 reserved concurrent executions
// Standard function: 50 reserved concurrent executions
// Batch function: 20 reserved concurrent executions

// CloudFormation example:
Resources:
  CriticalFunction:
    Type: AWS::Lambda::Function
    Properties:
      ReservedConcurrentExecutions: 100

  StandardFunction:
    Type: AWS::Lambda::Function
    Properties:
      ReservedConcurrentExecutions: 50
```

## 9. Trade-offs: Isolation vs Resource Efficiency

### Without Bulkheads (Shared Pool)

```
Pros:
✓ Maximum resource efficiency
✓ Simple to manage
✓ Flexible resource allocation

Cons:
✗ No failure isolation
✗ Noisy neighbor problems
✗ Cascading failures
✗ Difficult to prioritize workloads
```

### With Bulkheads (Isolated Pools)

```
Pros:
✓ Failure isolation
✓ Predictable performance
✓ Priority enforcement
✓ Better observability

Cons:
✗ Lower resource efficiency
✗ More complex management
✗ Requires careful sizing
✗ May need more total resources
```

### Finding the Balance

```typescript
// Hybrid approach: Shared pool with limits
class HybridBulkhead {
  private globalPool = new Semaphore(100);
  private perServiceLimits = {
    serviceA: new Semaphore(40),
    serviceB: new Semaphore(40),
    serviceC: new Semaphore(30)
  };

  async execute<T>(service: string, fn: () => Promise<T>): Promise<T> {
    const serviceLimit = this.perServiceLimits[service];
    
    // Acquire both global and service-specific permits
    await Promise.all([
      this.globalPool.acquire(),
      serviceLimit.acquire()
    ]);

    try {
      return await fn();
    } finally {
      this.globalPool.release();
      serviceLimit.release();
    }
  }
}
```

## 10. Bulkheads in Popular Libraries

### Resilience4j (Java)

```java
import io.github.resilience4j.bulkhead.Bulkhead;
import io.github.resilience4j.bulkhead.BulkheadConfig;

// Create bulkhead
BulkheadConfig config = BulkheadConfig.custom()
    .maxConcurrentCalls(10)
    .maxWaitDuration(Duration.ofMillis(500))
    .build();

Bulkhead bulkhead = Bulkhead.of("externalAPI", config);

// Use bulkhead
Supplier<String> decoratedSupplier = Bulkhead
    .decorateSupplier(bulkhead, () -> callExternalAPI());

String result = decoratedSupplier.get();
```

### Polly (.NET)

```csharp
using Polly;
using Polly.Bulkhead;

// Create bulkhead policy
var bulkheadPolicy = Policy
    .BulkheadAsync(
        maxParallelization: 10,
        maxQueuingActions: 20,
        onBulkheadRejectedAsync: context =>
        {
            Console.WriteLine("Bulkhead rejected");
            return Task.CompletedTask;
        });

// Use bulkhead
var result = await bulkheadPolicy.ExecuteAsync(async () =>
{
    return await CallExternalAPIAsync();
});
```

### Hystrix (Deprecated but Educational)

```java
import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;
import com.netflix.hystrix.HystrixThreadPoolKey;

public class ExternalAPICommand extends HystrixCommand<String> {
    public ExternalAPICommand() {
        super(Setter
            .withGroupKey(HystrixCommandGroupKey.Factory.asKey("ExternalAPI"))
            .andThreadPoolKey(HystrixThreadPoolKey.Factory.asKey("ExternalAPIPool"))
            .andThreadPoolPropertiesDefaults(
                HystrixThreadPoolProperties.Setter()
                    .withCoreSize(10)
                    .withMaxQueueSize(20)
            ));
    }

    @Override
    protected String run() {
        return callExternalAPI();
    }
}
```

## 11. Kubernetes Resource Limits as Bulkheads

```yaml
# Pod resource limits
apiVersion: v1
kind: Pod
metadata:
  name: api-service
spec:
  containers:
  - name: api
    image: api:latest
    resources:
      requests:
        memory: "256Mi"
        cpu: "500m"      # 0.5 CPU
      limits:
        memory: "512Mi"
        cpu: "1000m"     # 1 CPU

---
# Namespace resource quotas (bulkhead per namespace)
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    pods: "100"

---
# LimitRange (default limits)
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
  - max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "250m"
      memory: "256Mi"
    type: Container
```

## 12. Database Connection Pooling as Bulkhead

```typescript
// PostgreSQL connection pool bulkheads
import { Pool } from 'pg';

class DatabaseConnectionBulkheads {
  private pools: Map<string, Pool> = new Map();

  constructor() {
    // Tenant-specific pools
    this.createPool('tenant-premium', {
      max: 20,
      min: 5,
      idleTimeoutMillis: 30000
    });

    this.createPool('tenant-standard', {
      max: 10,
      min: 2,
      idleTimeoutMillis: 30000
    });

    this.createPool('tenant-free', {
      max: 5,
      min: 1,
      idleTimeoutMillis: 10000
    });
  }

  private createPool(name: string, config: any) {
    this.pools.set(name, new Pool({
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      ...config
    }));
  }

  getPool(tenantTier: string): Pool {
    const poolName = `tenant-${tenantTier}`;
    return this.pools.get(poolName) || this.pools.get('tenant-free')!;
  }

  async query(tenantTier: string, sql: string, params: any[]) {
    const pool = this.getPool(tenantTier);
    return pool.query(sql, params);
  }
}
```

## 13. Real Examples

### Netflix Hystrix

```
Hystrix uses bulkheads to isolate dependencies:

[User Service]
  ├─ [Thread Pool: Recommendations] (10 threads)
  ├─ [Thread Pool: Personalization] (10 threads)
  ├─ [Thread Pool: Ratings] (5 threads)
  └─ [Thread Pool: Reviews] (5 threads)

If Recommendations service is slow:
- Only its 10 threads are affected
- Other services continue with their dedicated threads
```

### AWS Lambda Concurrency Limits

```
AWS Lambda uses reserved concurrency as bulkheads:

Account limit: 1000 concurrent executions

Function allocation:
- Critical API: 400 reserved
- Standard API: 300 reserved
- Batch processing: 200 reserved
- Unreserved pool: 100

Critical API can always use its 400, even if others are busy
```

## 14. Testing Bulkhead Effectiveness

```typescript
// Load test to verify bulkhead isolation
import { performance } from 'perf_hooks';

async function testBulkheadIsolation() {
  const results = {
    criticalLatencies: [] as number[],
    standardLatencies: [] as number[]
  };

  // Overload standard endpoint
  const standardPromises = Array(100).fill(0).map(async () => {
    const start = performance.now();
    try {
      await fetch('http://localhost:3000/api/standard/slow');
    } catch (error) {}
    results.standardLatencies.push(performance.now() - start);
  });

  // Meanwhile, test critical endpoint
  await new Promise(resolve => setTimeout(resolve, 100));

  const criticalPromises = Array(10).fill(0).map(async () => {
    const start = performance.now();
    try {
      await fetch('http://localhost:3000/api/critical/fast');
    } catch (error) {}
    results.criticalLatencies.push(performance.now() - start);
  });

  await Promise.all([...standardPromises, ...criticalPromises]);

  // Verify critical endpoint not affected by standard overload
  const avgCritical = results.criticalLatencies.reduce((a, b) => a + b) / results.criticalLatencies.length;
  const avgStandard = results.standardLatencies.reduce((a, b) => a + b) / results.standardLatencies.length;

  console.log(`Critical avg latency: ${avgCritical}ms`);
  console.log(`Standard avg latency: ${avgStandard}ms`);
  console.log(`Isolation effective: ${avgCritical < avgStandard * 0.5}`);
}
```

## Summary

Key takeaways for Bulkhead Patterns:

1. **Isolate resources** - Prevent failures from cascading
2. **Size appropriately** - Use Little's Law and workload characteristics
3. **Monitor utilization** - Track pool usage and wait times
4. **Balance efficiency vs isolation** - Find the right trade-off
5. **Use multiple bulkhead types** - Thread pools, connection pools, semaphores, processes
6. **Implement priority-based allocation** - Protect critical paths
7. **Test isolation** - Verify bulkheads work under load
8. **Adapt to workload** - Adjust pool sizes based on metrics
9. **Combine with circuit breakers** - Fail fast when bulkhead is full
10. **Document pool sizes** - Explain sizing decisions

---

## Quick Start

### Basic Thread Pool Bulkhead

```python
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import threading

# Create isolated thread pools
critical_pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="critical")
normal_pool = ThreadPoolExecutor(max_workers=20, thread_name_prefix="normal")
background_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="background")

def with_bulkhead(pool):
    """Decorator to execute function in specific thread pool"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            future = pool.submit(func, *args, **kwargs)
            return future.result()
        return wrapper
    return decorator

# Use bulkheads
@with_bulkhead(critical_pool)
def process_payment(order_id):
    # Critical operation - isolated pool
    return payment_service.charge(order_id)

@with_bulkhead(normal_pool)
def process_order(order_id):
    # Normal operation - separate pool
    return order_service.create(order_id)

@with_bulkhead(background_pool)
def send_email(user_id):
    # Background task - separate pool
    return email_service.send(user_id)
```

### Connection Pool Bulkhead

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Separate connection pools for different workloads
critical_db = create_engine(
    "postgresql://...",
    poolclass=QueuePool,
    pool_size=10,  # Small, dedicated pool
    max_overflow=5
)

analytics_db = create_engine(
    "postgresql://...",
    poolclass=QueuePool,
    pool_size=50,  # Larger pool for analytics
    max_overflow=20
)
```

---

## Production Checklist

- [ ] **Identify Critical Paths**: Identify operations that must not be blocked
- [ ] **Resource Isolation**: Isolate thread pools, connection pools, memory
- [ ] **Pool Sizing**: Size pools based on workload analysis (not just max capacity)
- [ ] **Monitoring**: Track pool utilization, queue depth, rejections
- [ ] **Circuit Breakers**: Combine with circuit breakers for fail-fast behavior
- [ ] **Priority Queues**: Use priority queues within bulkheads
- [ ] **Testing**: Test isolation under load and failure scenarios
- [ ] **Documentation**: Document pool sizes and rationale
- [ ] **Alerting**: Alert when pools are near capacity
- [ ] **Graceful Degradation**: Define behavior when bulkhead is full
- [ ] **Resource Limits**: Set hard limits to prevent resource exhaustion
- [ ] **Review Regularly**: Review and adjust pool sizes based on metrics

---

## Anti-patterns

### ❌ Don't: Shared Resource Pools

```python
# ❌ Bad - All operations share same pool
shared_pool = ThreadPoolExecutor(max_workers=100)

def process_payment(order_id):
    return shared_pool.submit(payment_service.charge, order_id)  # Can be blocked by analytics!

def run_analytics():
    return shared_pool.submit(heavy_analytics)  # Can block payments!
```

```python
# ✅ Good - Isolated pools
payment_pool = ThreadPoolExecutor(max_workers=10)
analytics_pool = ThreadPoolExecutor(max_workers=50)

def process_payment(order_id):
    return payment_pool.submit(payment_service.charge, order_id)  # Isolated

def run_analytics():
    return analytics_pool.submit(heavy_analytics)  # Can't block payments
```

### ❌ Don't: Oversized Pools

```python
# ❌ Bad - Too many threads
pool = ThreadPoolExecutor(max_workers=1000)  # Context switching overhead!
```

```python
# ✅ Good - Sized appropriately
# Formula: pool_size = (CPU cores * 2) + I/O wait factor
pool = ThreadPoolExecutor(max_workers=20)  # Based on actual needs
```

### ❌ Don't: No Monitoring

```python
# ❌ Bad - No visibility
pool = ThreadPoolExecutor(max_workers=10)
# No way to know if pool is exhausted
```

```python
# ✅ Good - Monitor pool health
from prometheus_client import Gauge

pool_size = Gauge('thread_pool_size', 'Thread pool size')
pool_active = Gauge('thread_pool_active', 'Active threads')

def submit_with_metrics(pool, func):
    pool_size.set(pool._max_workers)
    pool_active.inc()
    try:
        return pool.submit(func)
    finally:
        pool_active.dec()
```

### ❌ Don't: No Graceful Degradation

```python
# ❌ Bad - Fails when pool is full
def process_request(data):
    future = pool.submit(process, data)
    return future.result()  # Blocks or fails if pool full
```

```python
# ✅ Good - Graceful degradation
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def process_request(data):
    try:
        future = pool.submit(process, data)
        return future.result(timeout=5)
    except TimeoutError:
        # Fallback to simpler processing
        return simple_process(data)
```

---

## Integration Points

- **Failure Modes** (`40-system-resilience/failure-modes/`) - Understanding what to isolate
- **Retry Strategies** (`40-system-resilience/retry-timeout-strategies/`) - Handling failures within bulkheads
- **Graceful Degradation** (`40-system-resilience/graceful-degradation/`) - Fallback when bulkhead is full
- **Chaos Engineering** (`40-system-resilience/chaos-engineering/`) - Testing bulkhead effectiveness
- **Circuit Breaker** (`40-system-resilience/graceful-degradation/`) - Fail-fast when bulkhead exhausted

---

## Further Reading

- [Bulkhead Pattern (Microsoft)](https://docs.microsoft.com/en-us/azure/architecture/patterns/bulkhead)
- [Resilience4j Bulkhead](https://resilience4j.readme.io/docs/bulkhead)
- [Hystrix Thread Pool Isolation](https://github.com/Netflix/Hystrix/wiki/How-it-Works#thread-isolation)
