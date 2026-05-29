/*============================================================================*/
/* ADVANCED AGENTDB VECTOR SEARCH IMPLEMENTATION SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: Advanced AgentDB Vector Search Implementation
version: 1.0.0
description: |
  [assert|neutral] Advanced AgentDB Vector Search Implementation skill for agentdb workflows [ground:given] [conf:0.95] [state:confirmed]
category: agentdb
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute Advanced AgentDB Vector Search Implementation workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic agentdb processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "Advanced AgentDB Vector Search Implementation",
  category: "agentdb",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["Advanced AgentDB Vector Search Implementation", "agentdb", "workflow"],
  context: "user needs Advanced AgentDB Vector Search Implementation capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Advanced AgentDB Vector Search Implementation

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



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

2. **Implement m

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/agentdb/Advanced AgentDB Vector Search Implementation/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "Advanced AgentDB Vector Search Implementation-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>ADVANCED AGENTDB VECTOR SEARCH IMPLEMENTATION_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
