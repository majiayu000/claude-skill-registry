---
name: "V3 QE MCP Optimization"
description: "Optimized MCP server for QE with connection pooling, O(1) tool lookup, load balancing, and <100ms response times."
version: "3.0.0"
---

# V3 QE MCP Optimization

## Purpose

Guide the implementation of an optimized MCP server for QE operations with connection pooling, hash-indexed tool lookup (O(1)), load balancing for fleet operations, and <100ms p95 response time targets.

## Activation

- When optimizing MCP server performance
- When implementing connection pooling
- When adding load balancing for fleet operations
- When monitoring MCP performance metrics
- When reducing response latency

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                V3 QE MCP Optimized Server                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               Connection Pool                        │    │
│  │  • 50 max connections                               │    │
│  │  • 5 min pre-warmed                                 │    │
│  │  • 300s idle timeout                                │    │
│  │  • Health checks every 30s                          │    │
│  └─────────────────────────────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────┼──────────────────────────────┐    │
│  │               Fast Tool Registry                     │    │
│  │  • Hash index: O(1) lookup                          │    │
│  │  • Category index: domain grouping                  │    │
│  │  • LRU cache: 1000 entries                          │    │
│  │  • Fuzzy matcher: typo tolerance                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────┼──────────────────────────────┐    │
│  │               Load Balancer                          │    │
│  │  • Least-connections strategy                       │    │
│  │  • Response-time weighted                           │    │
│  │  • Agent capacity aware                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Start optimized MCP server
aqe-v3 mcp start --optimized --pool-size 50

# Check MCP performance metrics
aqe-v3 mcp metrics --dashboard

# Configure connection pool
aqe-v3 mcp pool --configure --min 5 --max 50 --idle-timeout 300

# Enable load balancing
aqe-v3 mcp balance --strategy least-connections --enable
```

## Agent Workflow

```typescript
// Optimize MCP for QE operations
Task("Configure optimized MCP", `
  Set up optimized MCP server:
  - Initialize connection pool (5 min, 50 max)
  - Build hash-indexed tool registry
  - Configure load balancer for fleet
  - Set up performance monitoring
`, "v3-qe-mcp-specialist")

// Monitor MCP performance
Task("Monitor MCP performance", `
  Track and analyze MCP metrics:
  - Measure p50/p95/p99 response times
  - Track pool hit rate (target >90%)
  - Monitor tool lookup times (<5ms)
  - Alert on threshold breaches
`, "v3-qe-metrics-optimizer")
```

## Optimized MCP Implementation

### 1. Connection Pool

```typescript
// v3/src/mcp/pool/ConnectionPool.ts
import { Connection, ConnectionConfig } from '@modelcontextprotocol/sdk';

export class QEConnectionPool {
  private readonly available: Connection[] = [];
  private readonly inUse: Map<string, Connection> = new Map();
  private readonly config: PoolConfig;
  private readonly healthChecker: HealthChecker;

  constructor(config: PoolConfig) {
    this.config = {
      maxConnections: config.maxConnections || 50,
      minConnections: config.minConnections || 5,
      idleTimeoutMs: config.idleTimeoutMs || 300000,
      healthCheckIntervalMs: config.healthCheckIntervalMs || 30000
    };

    this.healthChecker = new HealthChecker(this);
  }

  // Initialize pool with pre-warmed connections
  async initialize(): Promise<void> {
    const warmupPromises: Promise<void>[] = [];

    for (let i = 0; i < this.config.minConnections; i++) {
      warmupPromises.push(this.createConnection());
    }

    await Promise.all(warmupPromises);
    this.healthChecker.start();
  }

  // Acquire connection with timeout
  async acquire(timeoutMs: number = 5000): Promise<Connection> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
      // Try available connection
      const available = this.available.pop();
      if (available) {
        const id = crypto.randomUUID();
        this.inUse.set(id, available);
        return { ...available, poolId: id };
      }

      // Create new if under limit
      if (this.totalConnections < this.config.maxConnections) {
        return await this.createConnection();
      }

      // Wait for release
      await this.waitForRelease(100);
    }

    throw new Error('Connection pool timeout');
  }

  // Release connection back to pool
  release(connection: Connection): void {
    if (connection.poolId && this.inUse.has(connection.poolId)) {
      this.inUse.delete(connection.poolId);

      if (this.available.length < this.config.maxConnections) {
        connection.lastUsed = Date.now();
        this.available.push(connection);
      }
    }
  }

  // Get pool statistics
  getStats(): PoolStats {
    return {
      available: this.available.length,
      inUse: this.inUse.size,
      total: this.totalConnections,
      hitRate: this.calculateHitRate(),
      averageWaitTime: this.calculateAverageWaitTime()
    };
  }

  private get totalConnections(): number {
    return this.available.length + this.inUse.size;
  }

  private async createConnection(): Promise<Connection> {
    const connection = await Connection.create(this.config.connectionConfig);
    const id = crypto.randomUUID();
    this.inUse.set(id, connection);
    return { ...connection, poolId: id };
  }
}
```

### 2. Fast Tool Registry

```typescript
// v3/src/mcp/registry/FastToolRegistry.ts
export class FastToolRegistry {
  private readonly hashIndex: Map<string, ToolDefinition> = new Map();
  private readonly categoryIndex: Map<string, ToolDefinition[]> = new Map();
  private readonly lruCache: LRUCache<string, ToolDefinition>;
  private readonly fuzzyMatcher: FuzzyMatcher;

  constructor(config: RegistryConfig) {
    this.lruCache = new LRUCache({
      max: config.cacheSize || 1000
    });
    this.fuzzyMatcher = new FuzzyMatcher({ threshold: 0.8 });
  }

  // Register all QE tools
  registerTools(tools: ToolDefinition[]): void {
    for (const tool of tools) {
      // Hash index for O(1) lookup
      this.hashIndex.set(tool.name, tool);

      // Category index for domain grouping
      const category = tool.metadata?.category || 'general';
      const existing = this.categoryIndex.get(category) || [];
      existing.push(tool);
      this.categoryIndex.set(category, existing);
    }
  }

  // O(1) tool lookup with fuzzy fallback
  lookup(name: string): ToolDefinition | null {
    // 1. Check LRU cache
    const cached = this.lruCache.get(name);
    if (cached) return cached;

    // 2. Direct hash lookup (O(1))
    const exact = this.hashIndex.get(name);
    if (exact) {
      this.lruCache.set(name, exact);
      return exact;
    }

    // 3. Fuzzy match for typos
    const fuzzyMatch = this.fuzzyMatcher.findBest(
      name,
      Array.from(this.hashIndex.keys())
    );
    if (fuzzyMatch) {
      const tool = this.hashIndex.get(fuzzyMatch);
      if (tool) {
        this.lruCache.set(name, tool);
        return tool;
      }
    }

    return null;
  }

  // Get tools by category
  getByCategory(category: string): ToolDefinition[] {
    return this.categoryIndex.get(category) || [];
  }

  // Get lookup statistics
  getStats(): RegistryStats {
    return {
      totalTools: this.hashIndex.size,
      categories: Array.from(this.categoryIndex.keys()),
      cacheHitRate: this.lruCache.hitRate,
      fuzzyMatches: this.fuzzyMatcher.matchCount
    };
  }
}
```

### 3. Load Balancer

```typescript
// v3/src/mcp/balancer/LoadBalancer.ts
export class QELoadBalancer {
  private readonly agents: Map<string, AgentMetrics> = new Map();
  private readonly strategy: LoadBalancingStrategy;

  constructor(config: LoadBalancerConfig) {
    this.strategy = this.createStrategy(config.strategy || 'least-connections');
  }

  // Select best agent for request
  selectAgent(request: MCPRequest): string {
    const availableAgents = Array.from(this.agents.entries())
      .filter(([_, metrics]) => metrics.status === 'available')
      .map(([id, metrics]) => ({ id, metrics }));

    if (availableAgents.length === 0) {
      throw new Error('No available agents');
    }

    return this.strategy.select(availableAgents, request);
  }

  // Update agent metrics
  updateMetrics(agentId: string, metrics: Partial<AgentMetrics>): void {
    const existing = this.agents.get(agentId) || this.createDefaultMetrics();
    this.agents.set(agentId, { ...existing, ...metrics });
  }

  // Record request completion
  recordCompletion(agentId: string, responseTimeMs: number): void {
    const metrics = this.agents.get(agentId);
    if (metrics) {
      metrics.activeConnections--;
      metrics.responseTimeHistory.push(responseTimeMs);
      if (metrics.responseTimeHistory.length > 100) {
        metrics.responseTimeHistory.shift();
      }
      metrics.averageResponseTime = this.calculateAverage(metrics.responseTimeHistory);
    }
  }

  private createStrategy(name: string): LoadBalancingStrategy {
    switch (name) {
      case 'least-connections':
        return new LeastConnectionsStrategy();
      case 'response-time':
        return new ResponseTimeWeightedStrategy();
      case 'round-robin':
        return new RoundRobinStrategy();
      default:
        return new LeastConnectionsStrategy();
    }
  }
}

// Least-connections strategy
class LeastConnectionsStrategy implements LoadBalancingStrategy {
  select(agents: AgentWithMetrics[]): string {
    return agents.sort((a, b) =>
      a.metrics.activeConnections - b.metrics.activeConnections
    )[0].id;
  }
}

// Response-time weighted strategy
class ResponseTimeWeightedStrategy implements LoadBalancingStrategy {
  select(agents: AgentWithMetrics[]): string {
    // Weight inversely by response time
    const weights = agents.map(a => ({
      id: a.id,
      weight: 1 / (a.metrics.averageResponseTime || 1)
    }));

    const totalWeight = weights.reduce((sum, w) => sum + w.weight, 0);
    let random = Math.random() * totalWeight;

    for (const w of weights) {
      random -= w.weight;
      if (random <= 0) return w.id;
    }

    return agents[0].id;
  }
}
```

### 4. Performance Monitoring

```typescript
// v3/src/mcp/monitoring/MCPMonitor.ts
export class MCPMonitor {
  private readonly metrics: MCPMetrics;
  private readonly alerts: AlertManager;

  constructor(config: MonitorConfig) {
    this.metrics = new MCPMetrics();
    this.alerts = new AlertManager(config.alerts);
  }

  // Record request metrics
  recordRequest(request: MCPRequest, responseTimeMs: number): void {
    this.metrics.record('request_latency', responseTimeMs);
    this.metrics.increment('total_requests');

    // Check alert thresholds
    if (responseTimeMs > this.config.alertThresholds.p95) {
      this.alerts.trigger('high_latency', { responseTimeMs });
    }
  }

  // Record pool metrics
  recordPoolMetrics(stats: PoolStats): void {
    this.metrics.gauge('pool_available', stats.available);
    this.metrics.gauge('pool_in_use', stats.inUse);
    this.metrics.gauge('pool_hit_rate', stats.hitRate);

    if (stats.hitRate < 0.7) {
      this.alerts.trigger('low_pool_hit_rate', stats);
    }
  }

  // Get dashboard data
  getDashboard(): MCPDashboard {
    return {
      latency: {
        p50: this.metrics.percentile('request_latency', 50),
        p95: this.metrics.percentile('request_latency', 95),
        p99: this.metrics.percentile('request_latency', 99)
      },
      pool: {
        hitRate: this.metrics.get('pool_hit_rate'),
        utilization: this.metrics.get('pool_in_use') / this.config.maxConnections
      },
      toolLookup: {
        averageTimeMs: this.metrics.average('tool_lookup_time'),
        cacheHitRate: this.metrics.get('tool_cache_hit_rate')
      },
      requests: {
        total: this.metrics.get('total_requests'),
        perSecond: this.metrics.rate('total_requests', 60)
      },
      errors: {
        rate: this.metrics.rate('errors', 60),
        recent: this.alerts.getRecentAlerts(10)
      }
    };
  }
}
```

## QE MCP Tools (Optimized)

| Tool | Category | Target Latency |
|------|----------|----------------|
| qe_test_generate | test-generation | <500ms |
| qe_coverage_analyze | coverage-analysis | <200ms |
| qe_coverage_gaps | coverage-analysis | <100ms |
| qe_quality_gate | quality-assessment | <100ms |
| qe_quality_metrics | quality-assessment | <50ms |
| qe_fleet_init | coordination | <200ms |
| qe_fleet_status | coordination | <50ms |
| qe_agent_spawn | coordination | <100ms |
| qe_task_orchestrate | coordination | <150ms |
| qe_memory_store | memory | <20ms |
| qe_memory_retrieve | memory | <10ms |
| qe_memory_search | memory | <50ms |
| qe_learn_pattern | learning | <100ms |
| qe_learn_status | learning | <30ms |

## Performance Configuration

```typescript
const QE_MCP_CONFIG: OptimizedMCPConfig = {
  // Connection pooling
  pool: {
    maxConnections: 50,
    minConnections: 5,
    idleTimeoutMs: 300000, // 5 minutes
    healthCheckIntervalMs: 30000
  },

  // Tool registry
  registry: {
    cacheEnabled: true,
    cacheSize: 1000,
    indexType: 'hash',
    fuzzyMatchEnabled: true
  },

  // Load balancing
  balancer: {
    strategy: 'least-connections',
    healthCheckIntervalMs: 10000,
    capacityAware: true
  },

  // Performance targets
  targets: {
    p95ResponseTime: 100, // ms
    poolHitRate: 0.9,
    toolLookupTime: 5 // ms
  },

  // Monitoring
  monitoring: {
    enabled: true,
    dashboardIntervalMs: 1000,
    alertThresholds: {
      p95ResponseTime: 200,
      errorRate: 0.05,
      poolHitRate: 0.7
    }
  }
};
```

## Performance Targets

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| p95 Response Time | ~250ms | <100ms | 2.5x |
| Tool Lookup | ~15ms (linear) | <5ms (hash) | 3x |
| Pool Hit Rate | 0% (no pool) | >90% | ∞ |
| Startup Time | ~1.8s | <400ms | 4.5x |
| Memory Usage | ~150MB | ~75MB | 50% |

## CLI Commands

```bash
# Start optimized server
aqe-v3 mcp start --optimized
aqe-v3 mcp start --pool-size 50 --strategy least-connections

# Pool management
aqe-v3 mcp pool status
aqe-v3 mcp pool configure --min 5 --max 50
aqe-v3 mcp pool drain  # Graceful shutdown

# Registry operations
aqe-v3 mcp tools list
aqe-v3 mcp tools lookup qe_test_generate
aqe-v3 mcp tools stats

# Load balancer
aqe-v3 mcp balance status
aqe-v3 mcp balance configure --strategy response-time
aqe-v3 mcp balance agents

# Monitoring
aqe-v3 mcp metrics
aqe-v3 mcp metrics --dashboard
aqe-v3 mcp metrics --export prometheus
aqe-v3 mcp alerts list
```

## Implementation Checklist

- [ ] Implement connection pool with pre-warming
- [ ] Create hash-indexed tool registry
- [ ] Add fuzzy matching for typos
- [ ] Implement load balancer strategies
- [ ] Add performance monitoring
- [ ] Create dashboard endpoint
- [ ] Set up alerting
- [ ] Write performance benchmarks
- [ ] Add CLI commands

## Related Skills

- v3-qe-mcp - Basic MCP implementation
- v3-qe-fleet-coordination - Agent orchestration
- v3-mcp-optimization (claude-flow) - Reference implementation

## Related ADRs

- ADR-039: V3 QE MCP Optimization
