---
name: resilient-storage
description: Multi-backend storage layer with automatic failover between Redis, database, and memory backends. Includes circuit breakers per backend and health-aware routing for high availability.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: resilience
  time: 6h
  source: drift-masterguide
---

# Resilient Storage Layer

Multi-backend storage with automatic failover. Redis primary, database secondary, memory fallback. Circuit breakers per backend. Health-aware routing.

## When to Use This Skill

- Building systems that can't afford storage downtime
- Need graceful degradation when Redis or database is unavailable
- Implementing distributed locks that must work even during partial outages
- Any caching layer that needs high availability

## Core Concepts

The resilient storage layer provides:
- Multiple storage backends with priority ordering
- Automatic failover when a backend fails
- Circuit breakers to prevent cascading failures
- Health checks to detect and recover from outages
- Memory fallback that's always available

Architecture:
```
Backend Selection (FAILOVER | ROUND_ROBIN | PRIORITY)
         │
    ┌────┼────┐
    ▼    ▼    ▼
  Redis  DB  Memory
  (P:1) (P:2) (P:999)
    │    │    │
    └────┴────┘
         │
   Health Monitor
```

## Implementation

### TypeScript

```typescript
export enum StorageBackendType {
  REDIS = 'redis',
  SUPABASE = 'supabase',
  MEMORY = 'memory',
}

export enum BackendHealth {
  HEALTHY = 'healthy',
  DEGRADED = 'degraded',
  UNHEALTHY = 'unhealthy',
}

export interface IStorageBackend {
  name: string;
  type: StorageBackendType;
  
  initialize(): Promise<void>;
  shutdown(): Promise<void>;
  healthCheck(): Promise<BackendHealth>;
  
  get(key: string): Promise<string | null>;
  set(key: string, value: string, ttlSeconds?: number): Promise<boolean>;
  delete(key: string): Promise<boolean>;
  
  acquireLock(name: string, holderId: string, ttlSeconds: number): Promise<LockResult>;
  releaseLock(name: string, holderId: string): Promise<boolean>;
}

interface BackendState {
  backend: IStorageBackend;
  priority: number;
  health: BackendHealth;
  circuitOpen: boolean;
  circuitOpenedAt?: Date;
  consecutiveFailures: number;
}

export class ResilientStorage {
  private backends: BackendState[] = [];
  private healthCheckInterval: NodeJS.Timeout | null = null;
  
  constructor(
    private config: {
      healthCheckIntervalMs: number;
      circuitBreakerThreshold: number;
      circuitBreakerResetMs: number;
    }
  ) {}
  
  async initialize(backendConfigs: Array<{
    backend: IStorageBackend;
    priority: number;
    enabled: boolean;
  }>): Promise<void> {
    for (const config of backendConfigs) {
      if (!config.enabled) continue;
      
      try {
        await config.backend.initialize();
        this.backends.push({
          backend: config.backend,
          priority: config.priority,
          health: BackendHealth.HEALTHY,
          circuitOpen: false,
          consecutiveFailures: 0,
        });
      } catch (error) {
        console.warn(`Failed to initialize ${config.backend.name}:`, error);
      }
    }
    
    // Always add memory fallback
    if (!this.backends.some(b => b.backend.type === StorageBackendType.MEMORY)) {
      const memoryBackend = new MemoryBackend();
      await memoryBackend.initialize();
      this.backends.push({
        backend: memoryBackend,
        priority: 999,
        health: BackendHealth.HEALTHY,
        circuitOpen: false,
        consecutiveFailures: 0,
      });
    }
    
    // Sort by priority
    this.backends.sort((a, b) => a.priority - b.priority);
    
    // Start health checks
    this.healthCheckInterval = setInterval(
      () => this.runHealthChecks(),
      this.config.healthCheckIntervalMs
    );
  }
  
  private async executeWithFailover<T>(
    operation: string,
    fn: (backend: IStorageBackend) => Promise<T>,
    isSuccess: (result: T) => boolean = () => true
  ): Promise<T> {
    const triedBackends = new Set<string>();
    
    while (triedBackends.size < this.backends.length) {
      const state = this.selectBackend(triedBackends);
      if (!state) break;
      
      triedBackends.add(state.backend.name);
      
      try {
        const result = await fn(state.backend);
        if (isSuccess(result)) {
          this.recordSuccess(state);
          return result;
        }
        this.recordFailure(state);
      } catch (error) {
        console.warn(`${operation} failed on ${state.backend.name}:`, error);
        this.recordFailure(state);
      }
    }
    
    throw new Error(`All backends failed for: ${operation}`);
  }
  
  private selectBackend(exclude: Set<string>): BackendState | null {
    const available = this.backends.filter(
      b => !exclude.has(b.backend.name) &&
           b.health !== BackendHealth.UNHEALTHY &&
           !b.circuitOpen
    );
    
    if (available.length === 0) {
      // Try memory fallback even if excluded
      return this.backends.find(
        b => b.backend.type === StorageBackendType.MEMORY
      ) || null;
    }
    
    return available[0];
  }
  
  private recordSuccess(state: BackendState): void {
    state.consecutiveFailures = 0;
    if (state.circuitOpen) {
      state.circuitOpen = false;
      console.log(`Circuit closed for ${state.backend.name}`);
    }
  }
  
  private recordFailure(state: BackendState): void {
    state.consecutiveFailures++;
    
    if (state.consecutiveFailures >= this.config.circuitBreakerThreshold) {
      if (!state.circuitOpen) {
        state.circuitOpen = true;
        state.circuitOpenedAt = new Date();
        console.warn(`Circuit opened for ${state.backend.name}`);
      }
    }
  }
  
  // Public API
  async get(key: string): Promise<string | null> {
    return this.executeWithFailover('get', b => b.get(key));
  }
  
  async set(key: string, value: string, ttlSeconds?: number): Promise<boolean> {
    return this.executeWithFailover('set', b => b.set(key, value, ttlSeconds), r => r);
  }
  
  async acquireLock(
    name: string,
    holderId: string,
    ttlSeconds: number
  ): Promise<LockResult> {
    return this.executeWithFailover(
      'acquireLock',
      b => b.acquireLock(name, holderId, ttlSeconds),
      r => r.acquired || !r.error
    );
  }
}
```

### Memory Backend (Fallback)

```typescript
export class MemoryBackend implements IStorageBackend {
  name = 'memory';
  type = StorageBackendType.MEMORY;
  
  private store = new Map<string, { value: string; expiresAt?: number }>();
  private locks = new Map<string, { holderId: string; expiresAt: number }>();
  
  async initialize(): Promise<void> {
    setInterval(() => this.cleanup(), 60000);
  }
  
  async shutdown(): Promise<void> {
    this.store.clear();
    this.locks.clear();
  }
  
  async healthCheck(): Promise<BackendHealth> {
    return BackendHealth.HEALTHY; // Memory is always healthy
  }
  
  async get(key: string): Promise<string | null> {
    const entry = this.store.get(key);
    if (!entry) return null;
    if (entry.expiresAt && Date.now() > entry.expiresAt) {
      this.store.delete(key);
      return null;
    }
    return entry.value;
  }
  
  async set(key: string, value: string, ttlSeconds?: number): Promise<boolean> {
    this.store.set(key, {
      value,
      expiresAt: ttlSeconds ? Date.now() + ttlSeconds * 1000 : undefined,
    });
    return true;
  }
  
  async delete(key: string): Promise<boolean> {
    return this.store.delete(key);
  }
  
  async acquireLock(
    name: string,
    holderId: string,
    ttlSeconds: number
  ): Promise<LockResult> {
    const existing = this.locks.get(name);
    const now = Date.now();
    
    if (existing && existing.expiresAt > now && existing.holderId !== holderId) {
      return { acquired: false, error: 'Lock held by another process' };
    }
    
    this.locks.set(name, {
      holderId,
      expiresAt: now + ttlSeconds * 1000,
    });
    
    return { acquired: true };
  }
  
  async releaseLock(name: string, holderId: string): Promise<boolean> {
    const lock = this.locks.get(name);
    if (!lock || lock.holderId !== holderId) return false;
    this.locks.delete(name);
    return true;
  }
  
  private cleanup(): void {
    const now = Date.now();
    for (const [key, entry] of this.store) {
      if (entry.expiresAt && entry.expiresAt < now) {
        this.store.delete(key);
      }
    }
    for (const [name, lock] of this.locks) {
      if (lock.expiresAt < now) {
        this.locks.delete(name);
      }
    }
  }
}
```

## Usage Examples

### Initialization

```typescript
const storage = new ResilientStorage({
  healthCheckIntervalMs: 30000,
  circuitBreakerThreshold: 5,
  circuitBreakerResetMs: 60000,
});

await storage.initialize([
  { backend: new RedisBackend(process.env.REDIS_URL), priority: 1, enabled: true },
  { backend: new SupabaseBackend(), priority: 2, enabled: true },
  { backend: new MemoryBackend(), priority: 999, enabled: true },
]);

// Operations automatically failover
await storage.set('key', 'value', 3600);
const value = await storage.get('key');

// Locks work across backends
const lock = await storage.acquireLock('job:123', 'worker-1', 30);
```

### Health Endpoint

```typescript
// GET /api/health/storage
export async function GET() {
  const status = storage.getHealthStatus();
  
  const allHealthy = Object.values(status).every(
    s => s.health === 'healthy' && !s.circuitOpen
  );
  
  return Response.json({
    status: allHealthy ? 'healthy' : 'degraded',
    activeBackend: storage.getActiveBackend(),
    backends: status,
  }, {
    status: allHealthy ? 200 : 503,
  });
}
```

## Best Practices

1. Always include memory fallback - it's your last line of defense
2. Set appropriate circuit breaker thresholds based on your SLAs
3. Monitor backend switches - frequent switches indicate instability
4. Use health checks to detect issues before they cause failures
5. Log all failover events for debugging and alerting

## Common Mistakes

- Not including a memory fallback backend
- Setting circuit breaker thresholds too low (causes flapping)
- Forgetting to handle the case where all backends fail
- Not monitoring health check results
- Using the same TTL for all backends (memory may need shorter TTLs)

## Related Patterns

- circuit-breaker - Prevent cascading failures
- distributed-lock - Distributed locking implementation
- leader-election - Leader election using locks
- graceful-degradation - Graceful degradation strategies
