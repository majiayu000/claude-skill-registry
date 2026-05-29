---
skill_id: when-using-advanced-vector-search-use-agentdb-advanced
name: Advanced AgentDB Vector Search Implementation
version: 1.0.0
category: agentdb
subcategory: distributed-systems
trigger_pattern: "when-using-advanced-vector-search"
agents:
  - ml-developer
  - backend-dev
  - performance-analyzer
complexity: advanced
estimated_duration: 8-12 hours
prerequisites:
  - Basic AgentDB knowledge
  - Vector database concepts
  - Distributed systems understanding
  - TypeScript/Node.js proficiency
outputs:
  - Multi-database AgentDB cluster
  - QUIC synchronization system
  - Custom distance metrics
  - Hybrid search implementation
  - Performance benchmarks
validation_criteria:
  - 150x faster search vs baseline
  - Multi-DB synchronization working
  - Custom metrics functional
  - Hybrid search accurate
evidence_based_techniques:
  - Self-consistency validation
  - Program-of-thought decomposition
  - Chain-of-verification
  - Multi-agent consensus
metadata:
  author: claude-flow
  created: 2025-10-30
  updated: 2025-10-30
  tags:
    - agentdb
    - vector-search
    - distributed-systems
    - quic-sync
    - hybrid-search
---

# Advanced AgentDB Vector Search Implementation

## Overview

Master advanced AgentDB features including QUIC synchronization, multi-database management, custom distance metrics, hybrid search, and distributed systems integration for building distributed AI systems, multi-agent coordination, and advanced vector search applications.

## When to Use This Skill

Use this skill when you need to:
- Build distributed vector search systems
- Implement multi-agent coordination with shared memory
- Create custom similarity metrics for specialized domains
- Deploy hybrid search combining vector and traditional methods
- Scale AgentDB to production with high availability
- Synchronize multiple AgentDB instances in real-time

## SOP Framework: 5-Phase Advanced Vector Search Deployment

### Phase 1: Setup AgentDB Infrastructure (2-3 hours)

**Objective:** Initialize multi-database AgentDB infrastructure with proper configuration

**Agent:** backend-dev

**Steps:**

1. **Install AgentDB with advanced features**
```bash
npm install agentdb-advanced@latest
npm install @agentdb/quic-sync @agentdb/distributed
```

2. **Initialize primary database**
```typescript
import { AgentDB } from 'agentdb-advanced';
import { QUICSync } from '@agentdb/quic-sync';

const primaryDB = new AgentDB({
  name: 'primary-vector-db',
  dimensions: 1536, // OpenAI embedding size
  indexType: 'hnsw',
  distanceMetric: 'cosine',
  persistPath: './data/primary',
  advanced: {
    enableQUIC: true,
    multiDB: true,
    hybridSearch: true
  }
});

await primaryDB.initialize();
```

3. **Configure replica databases**
```typescript
const replicas = await Promise.all([
  AgentDB.createReplica('replica-1', {
    primary: primaryDB,
    syncMode: 'quic',
    persistPath: './data/replica-1'
  }),
  AgentDB.createReplica('replica-2', {
    primary: primaryDB,
    syncMode: 'quic',
    persistPath: './data/replica-2'
  })
]);
```

4. **Setup health monitoring**
```typescript
const monitor = primaryDB.createMonitor({
  checkInterval: 5000,
  metrics: ['latency', 'throughput', 'replication-lag'],
  alerts: {
    replicationLag: 1000, // ms
    errorRate: 0.01
  }
});

monitor.on('alert', (alert) => {
  console.error('Database alert:', alert);
});
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/infrastructure/config', {
  primary: primaryDB.id,
  replicas: replicas.map(r => r.id),
  syncMode: 'quic',
  timestamp: Date.now()
});
```

**Validation:**
- Primary database initialized
- Replicas connected and syncing
- Health monitor active
- Configuration stored in memory

**Evidence-Based Validation:**
```typescript
// Self-consistency check across replicas
const testVector = Array(1536).fill(0).map(() => Math.random());
await primaryDB.insert({ id: 'test-1', vector: testVector });

// Wait for sync
await new Promise(resolve => setTimeout(resolve, 100));

// Verify consistency
const checks = await Promise.all(
  replicas.map(r => r.get('test-1'))
);

const consistent = checks.every(c =>
  c && vectorEquals(c.vector, testVector)
);

console.log('Consistency check:', consistent ? 'PASS' : 'FAIL');
```

### Phase 2: Configure Advanced Features (2-3 hours)

**Objective:** Setup QUIC synchronization, multi-DB coordination, and advanced routing

**Agent:** ml-developer

**Steps:**

1. **Configure QUIC synchronization**
```typescript
import { QUICConfig } from '@agentdb/quic-sync';

const quicSync = new QUICSync({
  primary: primaryDB,
  replicas: replicas,
  config: {
    maxStreams: 100,
    idleTimeout: 30000,
    keepAlive: 5000,
    congestionControl: 'cubic',
    prioritization: 'weighted-round-robin'
  }
});

await quicSync.start();

// Monitor sync performance
quicSync.on('sync-complete', (stats) => {
  console.log('Sync stats:', {
    duration: stats.duration,
    vectorsSynced: stats.count,
    throughput: stats.count / (stats.duration / 1000)
  });
});
```

2. **Implement multi-database router**
```typescript
import { MultiDBRouter } from '@agentdb/distributed';

const router = new MultiDBRouter({
  databases: [primaryDB, ...replicas],
  strategy: 'load-balanced', // or 'nearest', 'round-robin'
  healthCheck: {
    interval: 5000,
    timeout: 1000
  }
});

// Query routing
const searchResults = await router.search({
  vector: queryVector,
  topK: 10,
  strategy: 'fan-out-merge' // Query all, merge results
});
```

3. **Setup distributed coordination**
```typescript
import { DistributedCoordinator } from '@agentdb/distributed';

const coordinator = new DistributedCoordinator({
  databases: [primaryDB, ...replicas],
  consensus: 'raft', // or 'gossip', 'quorum'
  leaderElection: true
});

await coordinator.start();

// Handle leadership changes
coordinator.on('leader-elected', (leader) => {
  console.log('New leader:', leader.id);
  primaryDB = leader;
});
```

4. **Configure failover policies**
```typescript
const failoverPolicy = {
  maxRetries: 3,
  retryDelay: 1000,
  fallbackStrategy: 'replica-promotion',
  autoRecovery: true
};

router.setFailoverPolicy(failoverPolicy);
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/advanced/quic-config', {
  syncMode: 'quic',
  streams: quicSync.activeStreams,
  routingStrategy: 'load-balanced',
  coordinator: coordinator.id
});
```

**Validation:**
- QUIC sync operational
- Router distributing load
- Coordinator elected leader
- Failover tested

**Evidence-Based Validation:**
```typescript
// Program-of-thought: Test multi-DB coordination
async function validateCoordination() {
  // Step 1: Insert on primary
  const testId = 'coord-test-' + Date.now();
  await primaryDB.insert({ id: testId, vector: testVector });

  // Step 2: Wait for QUIC sync
  await quicSync.waitForSync(testId, { timeout: 2000 });

  // Step 3: Query through router
  const results = await router.search({
    vector: testVector,
    topK: 1,
    filter: { id: testId }
  });

  // Step 4: Verify result from any replica
  return results[0]?.id === testId;
}

const coordValid = await validateCoordination();
console.log('Coordination validation:', coordValid ? 'PASS' : 'FAIL');
```

### Phase 3: Implement Custom Distance Metrics (2-3 hours)

**Objective:** Create specialized distance functions for domain-specific similarity

**Agent:** ml-developer

**Steps:**

1. **Define custom metric interface**
```typescript
import { DistanceMetric } from 'agentdb-advanced';

interface CustomMetricConfig {
  name: string;
  weightedDimensions?: number[];
  transformFunction?: (vector: number[]) => number[];
  combineMetrics?: {
    metrics: string[];
    weights: number[];
  };
}
```

2. **Implement weighted Euclidean distance**
```typescript
const weightedEuclidean: DistanceMetric = {
  name: 'weighted-euclidean',
  compute: (a: number[], b: number[], weights?: number[]) => {
    if (!weights) weights = Array(a.length).fill(1);

    let sum = 0;
    for (let i = 0; i < a.length; i++) {
      sum += weights[i] * Math.pow(a[i] - b[i], 2);
    }
    return Math.sqrt(sum);
  },
  normalize: true
};

primaryDB.registerMetric(weightedEuclidean);
```

3. **Create hybrid metric (vector + scalar)**
```typescript
const hybridSimilarity: DistanceMetric = {
  name: 'hybrid-similarity',
  compute: (a: number[], b: number[], metadata?: any) => {
    // Vector similarity (cosine)
    const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
    const magA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
    const magB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
    const cosineSim = dotProduct / (magA * magB);

    // Scalar similarity (if metadata present)
    let scalarSim = 0;
    if (metadata) {
      scalarSim = 1 - Math.abs(metadata.timestamp - Date.now()) / 1e9;
    }

    // Combine (70% vector, 30% scalar)
    return 0.7 * (1 - cosineSim) + 0.3 * (1 - scalarSim);
  }
};

primaryDB.registerMetric(hybridSimilarity);
```

4. **Implement domain-specific metrics**
```typescript
// Example: Code similarity metric
const codeSimilarity: DistanceMetric = {
  name: 'code-similarity',
  compute: (a: number[], b: number[], metadata?: any) => {
    // Vector component
    const vectorDist = cosineDistance(a, b);

    // Syntactic similarity
    const syntaxSim = metadata?.ast_similarity || 0;

    // Semantic similarity
    const semanticSim = metadata?.semantic_similarity || 0;

    // Weighted combination
    return 0.5 * vectorDist + 0.3 * (1 - syntaxSim) + 0.2 * (1 - semanticSim);
  }
};

primaryDB.registerMetric(codeSimilarity);
```

5. **Benchmark custom metrics**
```typescript
async function benchmarkMetrics() {
  const testVectors = generateTestVectors(1000);
  const queryVector = testVectors[0];

  const metrics = ['cosine', 'euclidean', 'weighted-euclidean', 'hybrid-similarity'];
  const results: Record<string, any> = {};

  for (const metric of metrics) {
    const start = performance.now();
    const searchResults = await primaryDB.search({
      vector: queryVector,
      topK: 10,
      metric: metric
    });
    const duration = performance.now() - start;

    results[metric] = {
      duration,
      results: searchResults.length,
      accuracy: calculateAccuracy(searchResults)
    };
  }

  return results;
}

const benchmark = await benchmarkMetrics();
await agentDB.memory.store('agentdb/metrics/benchmark', benchmark);
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/custom-metrics/registry', {
  metrics: ['weighted-euclidean', 'hybrid-similarity', 'code-similarity'],
  benchmark: benchmark,
  recommended: 'hybrid-similarity'
});
```

**Validation:**
- Custom metrics registered
- Metrics produce valid distances
- Benchmark results collected
- Best metric identified

**Evidence-Based Validation:**
```typescript
// Chain-of-verification: Validate metric properties
async function verifyMetricProperties(metric: string) {
  const checks = {
    nonNegativity: true,
    symmetry: true,
    triangleInequality: true
  };

  const testVectors = [
    Array(1536).fill(0).map(() => Math.random()),
    Array(1536).fill(0).map(() => Math.random()),
    Array(1536).fill(0).map(() => Math.random())
  ];

  // Check non-negativity
  const d1 = await primaryDB.distance(testVectors[0], testVectors[1], metric);
  checks.nonNegativity = d1 >= 0;

  // Check symmetry: d(a,b) = d(b,a)
  const d2 = await primaryDB.distance(testVectors[1], testVectors[0], metric);
  checks.symmetry = Math.abs(d1 - d2) < 1e-6;

  // Check triangle inequality: d(a,c) <= d(a,b) + d(b,c)
  const dac = await primaryDB.distance(testVectors[0], testVectors[2], metric);
  const dbc = await primaryDB.distance(testVectors[1], testVectors[2], metric);
  checks.triangleInequality = dac <= d1 + dbc + 1e-6;

  return checks;
}

const metricValid = await verifyMetricProperties('hybrid-similarity');
console.log('Metric validation:', metricValid);
```

### Phase 4: Optimize Performance (2-3 hours)

**Objective:** Apply indexing, caching, and optimization techniques for production performance

**Agent:** performance-analyzer

**Steps:**

1. **Configure HNSW indexing**
```typescript
await primaryDB.createIndex({
  type: 'hnsw',
  params: {
    M: 16, // Number of connections per layer
    efConstruction: 200, // Construction time accuracy
    efSearch: 100, // Search time accuracy
    maxElements: 1000000
  }
});

// Enable index for all replicas
await Promise.all(
  replicas.map(r => r.syncIndex(primaryDB))
);
```

2. **Implement query caching**
```typescript
import { QueryCache } from '@agentdb/optimization';

const cache = new QueryCache({
  maxSize: 10000,
  ttl: 3600000, // 1 hour
  strategy: 'lru',
  hashFunction: 'xxhash64'
});

primaryDB.setCache(cache);

// Cache hit monitoring
cache.on('hit', (key, entry) => {
  console.log('Cache hit:', { key, age: Date.now() - entry.timestamp });
});
```

3. **Enable quantization**
```typescript
import { Quantization } from '@agentdb/optimization';

const quantizer = new Quantization({
  method: 'product-quantization',
  codebookSize: 256,
  subvectors: 8,
  compressionRatio: 4 // 4x memory reduction
});

await primaryDB.applyQuantization(quantizer);

// Verify accuracy after quantization
const accuracyTest = await benchmarkAccuracy(primaryDB, testQueries);
console.log('Post-quantization accuracy:', accuracyTest);
```

4. **Batch operations**
```typescript
import { BatchProcessor } from '@agentdb/optimization';

const batchProcessor = new BatchProcessor({
  batchSize: 1000,
  flushInterval: 5000,
  parallelBatches: 4
});

// Batch inserts
const vectors = generateVectors(10000);
await batchProcessor.insertBatch(primaryDB, vectors);

// Batch searches
const queries = generateQueries(100);
const results = await batchProcessor.searchBatch(primaryDB, queries, {
  topK: 10,
  parallel: true
});
```

5. **Performance benchmarking**
```typescript
async function comprehensiveBenchmark() {
  const benchmark = {
    insertThroughput: 0,
    searchLatency: 0,
    searchThroughput: 0,
    memoryUsage: 0,
    cacheHitRate: 0
  };

  // Insert throughput
  const insertStart = performance.now();
  await batchProcessor.insertBatch(primaryDB, generateVectors(10000));
  benchmark.insertThroughput = 10000 / ((performance.now() - insertStart) / 1000);

  // Search latency (p50, p95, p99)
  const latencies: number[] = [];
  for (let i = 0; i < 1000; i++) {
    const start = performance.now();
    await primaryDB.search({ vector: generateQuery(), topK: 10 });
    latencies.push(performance.now() - start);
  }
  latencies.sort((a, b) => a - b);
  benchmark.searchLatency = {
    p50: latencies[Math.floor(latencies.length * 0.5)],
    p95: latencies[Math.floor(latencies.length * 0.95)],
    p99: latencies[Math.floor(latencies.length * 0.99)]
  };

  // Memory usage
  benchmark.memoryUsage = await primaryDB.getMemoryUsage();

  // Cache hit rate
  const cacheStats = cache.getStats();
  benchmark.cacheHitRate = cacheStats.hits / (cacheStats.hits + cacheStats.misses);

  return benchmark;
}

const perfResults = await comprehensiveBenchmark();
await agentDB.memory.store('agentdb/optimization/benchmark', perfResults);
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/optimization/config', {
  indexing: { type: 'hnsw', params: {...} },
  caching: { enabled: true, hitRate: perfResults.cacheHitRate },
  quantization: { method: 'product-quantization', ratio: 4 },
  performance: perfResults
});
```

**Validation:**
- HNSW index built and synced
- Cache operational with good hit rate
- Quantization maintains accuracy
- Performance meets targets (>150x improvement)

**Evidence-Based Validation:**
```typescript
// Multi-agent consensus on performance targets
async function validatePerformanceTargets() {
  const targets = {
    searchLatencyP95: 10, // ms
    insertThroughput: 50000, // vectors/sec
    memoryEfficiency: 4, // compression ratio
    cacheHitRate: 0.7 // 70%
  };

  const results = await comprehensiveBenchmark();

  const validations = {
    latency: results.searchLatency.p95 <= targets.searchLatencyP95,
    throughput: results.insertThroughput >= targets.insertThroughput,
    memory: results.memoryUsage.compressionRatio >= targets.memoryEfficiency,
    cache: results.cacheHitRate >= targets.cacheHitRate
  };

  const allPass = Object.values(validations).every(v => v);

  return { validations, allPass, results };
}

const perfValidation = await validatePerformanceTargets();
console.log('Performance validation:', perfValidation);
```

### Phase 5: Deploy and Monitor (2-3 hours)

**Objective:** Deploy to production with monitoring, alerting, and operational procedures

**Agent:** backend-dev

**Steps:**

1. **Setup production configuration**
```typescript
const productionConfig = {
  cluster: {
    primary: {
      host: process.env.PRIMARY_HOST,
      port: parseInt(process.env.PRIMARY_PORT),
      replicas: 2
    },
    replicas: [
      { host: process.env.REPLICA1_HOST, port: parseInt(process.env.REPLICA1_PORT) },
      { host: process.env.REPLICA2_HOST, port: parseInt(process.env.REPLICA2_PORT) }
    ]
  },
  monitoring: {
    enabled: true,
    exporters: ['prometheus', 'cloudwatch'],
    alerts: {
      replicationLag: 1000,
      errorRate: 0.01,
      latencyP95: 50
    }
  },
  backup: {
    enabled: true,
    interval: 3600000, // 1 hour
    retention: 7 // days
  }
};

await deployCluster(productionConfig);
```

2. **Implement monitoring dashboards**
```typescript
import { MetricsExporter } from '@agentdb/monitoring';

const exporter = new MetricsExporter({
  exporters: [
    {
      type: 'prometheus',
      port: 9090,
      metrics: [
        'agentdb_search_latency',
        'agentdb_insert_throughput',
        'agentdb_replication_lag',
        'agentdb_cache_hit_rate',
        'agentdb_memory_usage'
      ]
    },
    {
      type: 'cloudwatch',
      namespace: 'AgentDB/Production',
      region: 'us-east-1'
    }
  ]
});

await exporter.start();

// Custom metrics
exporter.registerMetric('agentdb_custom_queries', 'counter',
  'Custom metric queries executed'
);
```

3. **Configure alerting**
```typescript
import { AlertManager } from '@agentdb/monitoring';

const alertManager = new AlertManager({
  channels: [
    { type: 'email', recipients: ['ops@company.com'] },
    { type: 'slack', webhook: process.env.SLACK_WEBHOOK },
    { type: 'pagerduty', apiKey: process.env.PAGERDUTY_KEY }
  ],
  rules: [
    {
      metric: 'agentdb_replication_lag',
      condition: '> 1000',
      severity: 'critical',
      message: 'Replication lag exceeds 1 second'
    },
    {
      metric: 'agentdb_search_latency_p95',
      condition: '> 50',
      severity: 'warning',
      message: 'Search latency P95 exceeds 50ms'
    },
    {
      metric: 'agentdb_error_rate',
      condition: '> 0.01',
      severity: 'critical',
      message: 'Error rate exceeds 1%'
    }
  ]
});

await alertManager.start();
```

4. **Implement health checks**
```typescript
import express from 'express';

const healthApp = express();

healthApp.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: Date.now(),
    databases: await Promise.all([
      primaryDB.healthCheck(),
      ...replicas.map(r => r.healthCheck())
    ]),
    quic: quicSync.isHealthy(),
    coordinator: coordinator.getStatus()
  };

  const allHealthy = health.databases.every(db => db.status === 'healthy');

  res.status(allHealthy ? 200 : 503).json(health);
});

healthApp.get('/metrics', async (req, res) => {
  const metrics = await exporter.getMetrics();
  res.set('Content-Type', 'text/plain');
  res.send(metrics);
});

healthApp.listen(8080);
```

5. **Create operational runbook**
```typescript
const runbook = {
  deployment: {
    steps: [
      '1. Verify configuration in production.env',
      '2. Deploy primary database first',
      '3. Deploy replicas with QUIC sync enabled',
      '4. Verify replication lag < 100ms',
      '5. Enable monitoring and alerting',
      '6. Run smoke tests',
      '7. Gradually increase traffic'
    ]
  },
  troubleshooting: {
    'High replication lag': [
      'Check network connectivity between nodes',
      'Verify QUIC streams are not saturated',
      'Consider increasing QUIC maxStreams',
      'Check primary database load'
    ],
    'Slow search queries': [
      'Verify HNSW index is built',
      'Check cache hit rate',
      'Review query patterns',
      'Consider adjusting efSearch parameter'
    ],
    'Leader election failure': [
      'Check coordinator logs',
      'Verify quorum availability',
      'Check network partitions',
      'Manually trigger election if needed'
    ]
  },
  backup: {
    schedule: 'Hourly incremental, daily full',
    retention: '7 days',
    restore: [
      '1. Stop affected database instance',
      '2. Download backup from S3',
      '3. Restore data directory',
      '4. Start database with --recovery flag',
      '5. Verify data integrity',
      '6. Rejoin cluster'
    ]
  }
};

await agentDB.memory.store('agentdb/production/runbook', runbook);
```

**Memory Pattern:**
```typescript
await agentDB.memory.store('agentdb/production/deployment', {
  config: productionConfig,
  deployed: Date.now(),
  monitoring: {
    dashboards: ['prometheus:3000', 'grafana:3001'],
    alerts: alertManager.getRules()
  },
  runbook: runbook
});
```

**Validation:**
- Production cluster deployed
- Monitoring active and exporting metrics
- Alerts configured and tested
- Health checks returning 200
- Runbook documented

**Evidence-Based Validation:**
```typescript
// Self-consistency check: Production readiness
async function validateProductionReadiness() {
  const checks = {
    deployment: false,
    monitoring: false,
    alerting: false,
    healthChecks: false,
    backup: false,
    documentation: false
  };

  // Check deployment
  const clusterStatus = await coordinator.getClusterStatus();
  checks.deployment = clusterStatus.healthy && clusterStatus.nodes.length >= 3;

  // Check monitoring
  const metrics = await exporter.getMetrics();
  checks.monitoring = metrics.length > 0;

  // Check alerting
  const alertStatus = await alertManager.getStatus();
  checks.alerting = alertStatus.active && alertStatus.channels.length > 0;

  // Check health endpoint
  const healthResponse = await fetch('http://localhost:8080/health');
  checks.healthChecks = healthResponse.status === 200;

  // Check backup configuration
  const backupStatus = await checkBackupStatus();
  checks.backup = backupStatus.enabled && backupStatus.lastBackup !== null;

  // Check documentation
  const docs = await agentDB.memory.retrieve('agentdb/production/runbook');
  checks.documentation = docs !== null;

  const readiness = Object.values(checks).every(c => c);

  return { checks, readiness };
}

const prodReadiness = await validateProductionReadiness();
console.log('Production readiness:', prodReadiness);
```

## Integration Scripts

### Complete Deployment Script

```bash
#!/bin/bash
# deploy-advanced-agentdb.sh

set -e

echo "Advanced AgentDB Deployment Script"
echo "==================================="

# Phase 1: Infrastructure Setup
echo "Phase 1: Setting up infrastructure..."
npm install agentdb-advanced @agentdb/quic-sync @agentdb/distributed @agentdb/optimization @agentdb/monitoring

# Phase 2: Initialize databases
echo "Phase 2: Initializing databases..."
node -e "
const { AgentDB } = require('agentdb-advanced');
const primary = new AgentDB({
  name: 'primary',
  dimensions: 1536,
  advanced: { enableQUIC: true, multiDB: true }
});
await primary.initialize();
console.log('Primary database initialized');
"

# Phase 3: Deploy replicas
echo "Phase 3: Deploying replicas..."
for i in 1 2; do
  node -e "
  const { AgentDB } = require('agentdb-advanced');
  const replica = await AgentDB.createReplica('replica-$i', {
    syncMode: 'quic'
  });
  console.log('Replica $i deployed');
  "
done

# Phase 4: Configure monitoring
echo "Phase 4: Configuring monitoring..."
node -e "
const { MetricsExporter } = require('@agentdb/monitoring');
const exporter = new MetricsExporter({
  exporters: [{ type: 'prometheus', port: 9090 }]
});
await exporter.start();
console.log('Monitoring configured');
"

# Phase 5: Run validation
echo "Phase 5: Running validation..."
npm run test:integration

echo "Deployment complete!"
```

### Quick Start Script

```typescript
// quickstart-advanced.ts
import { setupAdvancedAgentDB } from './setup';

async function quickStart() {
  console.log('Starting Advanced AgentDB Quick Setup...');

  // 1. Setup infrastructure
  const { primary, replicas, router } = await setupAdvancedAgentDB({
    dimensions: 1536,
    replicaCount: 2,
    enableQUIC: true
  });

  // 2. Load sample data
  console.log('Loading sample data...');
  const vectors = generateSampleVectors(10000);
  await router.insertBatch(vectors);

  // 3. Test searches
  console.log('Testing searches...');
  const query = vectors[0];
  const results = await router.search({
    vector: query,
    topK: 10,
    metric: 'cosine'
  });
  console.log('Search results:', results.length);

  // 4. Verify replication
  console.log('Verifying replication...');
  const syncStatus = await router.getSyncStatus();
  console.log('Replication lag:', syncStatus.lag, 'ms');

  console.log('Quick setup complete!');
}

quickStart().catch(console.error);
```

## Memory Coordination Patterns

```typescript
// Store cluster configuration
await memory.store('agentdb/cluster/config', {
  topology: 'distributed',
  nodes: [primary, ...replicas],
  syncMode: 'quic',
  timestamp: Date.now()
});

// Store performance metrics
await memory.store('agentdb/metrics/latest', {
  searchLatency: perfResults.searchLatency,
  throughput: perfResults.insertThroughput,
  cacheHitRate: perfResults.cacheHitRate
});

// Store custom metrics registry
await memory.store('agentdb/metrics/custom', {
  registered: ['weighted-euclidean', 'hybrid-similarity'],
  active: 'hybrid-similarity',
  benchmarks: benchmark
});

// Store operational state
await memory.store('agentdb/operations/state', {
  deployed: true,
  healthy: true,
  leader: coordinator.getLeader(),
  lastBackup: backupTimestamp
});
```

## Evidence-Based Success Criteria

1. **Multi-Database Consistency (Self-Consistency)**
   - All replicas return identical results for same query
   - Replication lag < 100ms
   - Zero data loss during failover

2. **Performance Targets (Benchmarking)**
   - Search latency P95 < 10ms
   - Insert throughput > 50,000 vectors/sec
   - Memory efficiency 4x compression
   - Cache hit rate > 70%

3. **Custom Metrics Validity (Chain-of-Verification)**
   - Metrics satisfy mathematical properties
   - Metrics improve domain-specific accuracy
   - Metrics perform within latency budget

4. **Production Readiness (Multi-Agent Consensus)**
   - Monitoring exports all required metrics
   - Alerts fire correctly in test scenarios
   - Health checks pass consistently
   - Runbook covers common failure modes

## Troubleshooting Guide

**Issue: High replication lag**
```typescript
// Diagnose
const diagnostics = await quicSync.diagnose();
console.log('QUIC diagnostics:', diagnostics);

// Fix: Increase stream capacity
await quicSync.reconfigure({
  maxStreams: 200,
  congestionControl: 'bbr'
});
```

**Issue: Slow queries after quantization**
```typescript
// Check accuracy loss
const accuracy = await benchmarkAccuracy(primaryDB, testQueries);
if (accuracy < 0.95) {
  // Adjust quantization parameters
  await primaryDB.applyQuantization({
    method: 'product-quantization',
    compressionRatio: 2 // Reduce compression
  });
}
```

**Issue: Cache thrashing**
```typescript
// Analyze cache patterns
const cacheStats = cache.getDetailedStats();
console.log('Cache stats:', cacheStats);

// Adjust cache size or TTL
cache.reconfigure({
  maxSize: 20000, // Increase size
  ttl: 7200000 // Increase TTL to 2 hours
});
```

## Success Metrics

- 150x faster search vs baseline
- 4-32x memory reduction with quantization
- Multi-database synchronization < 100ms lag
- Custom metrics improve accuracy by 15-30%
- 99.9% uptime in production
- Health checks pass continuously

## Additional Resources

- AgentDB Advanced Documentation: https://agentdb.dev/docs/advanced
- QUIC Synchronization Guide: https://agentdb.dev/docs/quic
- Custom Metrics Tutorial: https://agentdb.dev/docs/metrics
- Production Deployment Best Practices: https://agentdb.dev/docs/production
