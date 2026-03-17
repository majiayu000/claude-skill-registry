---
name: "V3 QE Memory Unification"
description: "Unified memory system for QE with AgentDB, HNSW indexing (150x-12,500x faster search), and SONA learning integration."
version: "3.0.0"
---

# V3 QE Memory Unification

## Purpose

Guide the implementation of a unified memory system for all QE domains using AgentDB with HNSW indexing, providing 150x-12,500x faster semantic search and cross-domain knowledge sharing.

## Activation

- When consolidating QE memory systems
- When implementing cross-domain knowledge sharing
- When migrating from legacy memory (SQLite, markdown, in-memory)
- When optimizing search performance
- When integrating SONA learning patterns

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 V3 QE Unified Memory                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ test-suites  │  │  coverage    │  │   defects    │       │
│  │   (HNSW)     │  │   (HNSW)     │  │   (HNSW)     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  quality     │  │  learning    │  │ coordination │       │
│  │   (HNSW)     │  │   (HNSW)     │  │   (HNSW)     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              AgentDB Core Engine                     │    │
│  │  • 1536-dimension embeddings                        │    │
│  │  • HNSW M=16, efConstruction=200                    │    │
│  │  • Hybrid persistence (SQLite + File)               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Initialize unified memory
aqe-v3 memory init --unified --hnsw

# Migrate from legacy systems
aqe-v3 memory migrate --source sqlite --domain coverage-analysis
aqe-v3 memory migrate --source markdown --domain defect-patterns

# Enable SONA integration
aqe-v3 memory sona --enable --mode real-time

# Search across all domains
aqe-v3 memory search --query "authentication test patterns" --domains all
```

## Agent Workflow

```typescript
// Spawn memory specialist for unified operations
Task("Initialize unified memory", `
  Set up QE unified memory system:
  - Create AgentDB with HNSW indexes per domain
  - Configure embedding dimensions (1536)
  - Set up cross-domain sharing protocols
  - Enable SONA learning integration
`, "v3-qe-memory-specialist")

// Migrate legacy data
Task("Migrate coverage data", `
  Migrate coverage analysis data to unified system:
  - Export from SQLite/in-memory sources
  - Generate embeddings for all entries
  - Index in HNSW for fast search
  - Validate migration integrity
`, "v3-qe-memory-specialist")
```

## Unified Memory Implementation

### 1. QE Unified Memory Service

```typescript
// v3/src/memory/QEUnifiedMemory.ts
import { AgentDB, HNSWIndex } from '@agentdb/core';

export class QEUnifiedMemory {
  private readonly db: AgentDB;
  private readonly indexes: Map<string, HNSWIndex>;

  constructor(config: QEMemoryConfig) {
    this.db = new AgentDB({
      storagePath: config.storagePath || '.agentic-qe/memory',
      embeddingDimensions: 1536,
      persistenceStrategy: 'hybrid'
    });

    this.indexes = new Map();
    this.initializeIndexes(config);
  }

  private initializeIndexes(config: QEMemoryConfig): void {
    // Domain-specific HNSW configurations
    const domainConfigs: Record<string, HNSWConfig> = {
      'defect-patterns': { M: 32, efConstruction: 400, efSearch: 200 },
      'coverage-analysis': { M: 16, efConstruction: 200, efSearch: 100 },
      'test-suites': { M: 8, efConstruction: 100, efSearch: 50 },
      'learning-patterns': { M: 24, efConstruction: 300, efSearch: 150 },
      'quality-metrics': { M: 16, efConstruction: 200, efSearch: 100 },
      'coordination': { M: 8, efConstruction: 100, efSearch: 50 }
    };

    for (const [domain, hnswConfig] of Object.entries(domainConfigs)) {
      this.indexes.set(domain, new HNSWIndex(hnswConfig));
    }
  }

  // Store with automatic embedding and indexing
  async store(entry: QEMemoryEntry): Promise<string> {
    // 1. Generate embedding
    const embedding = await this.generateEmbedding(entry.content);

    // 2. Store in AgentDB
    const id = await this.db.store({
      id: entry.id || crypto.randomUUID(),
      namespace: entry.domain,
      data: entry.content,
      embedding,
      metadata: entry.metadata,
      ttl: entry.ttl
    });

    // 3. Index in HNSW for fast search
    const index = this.indexes.get(entry.domain);
    if (index) {
      await index.add(id, embedding);
    }

    return id;
  }

  // Semantic search across domains (O(log n) via HNSW)
  async search(query: string, options: SearchOptions = {}): Promise<SearchResult[]> {
    const queryEmbedding = await this.generateEmbedding(query);
    const domains = options.domains || Array.from(this.indexes.keys());
    const results: SearchResult[] = [];

    for (const domain of domains) {
      const index = this.indexes.get(domain);
      if (!index) continue;

      // O(log n) search via HNSW
      const candidates = await index.search(queryEmbedding, options.limit || 10);

      for (const { id, distance } of candidates) {
        const entry = await this.db.get(id);
        if (entry && distance < (options.threshold || 0.5)) {
          results.push({
            id,
            domain,
            content: entry.data,
            similarity: 1 - distance,
            metadata: entry.metadata
          });
        }
      }
    }

    return results
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, options.limit || 10);
  }

  // Cross-domain knowledge sharing
  async shareKnowledge(
    sourceDomain: string,
    targetDomains: string[],
    query: string
  ): Promise<void> {
    const sourceResults = await this.search(query, { domains: [sourceDomain] });

    for (const result of sourceResults) {
      for (const targetDomain of targetDomains) {
        await this.store({
          domain: targetDomain,
          content: result.content,
          metadata: {
            ...result.metadata,
            sharedFrom: sourceDomain,
            sharedAt: new Date().toISOString()
          }
        });
      }
    }
  }
}
```

### 2. Domain Migration Service

```typescript
// v3/src/memory/migration/QEMigrationService.ts
export class QEMigrationService {
  constructor(
    private readonly unifiedMemory: QEUnifiedMemory,
    private readonly embeddingProvider: EmbeddingProvider
  ) {}

  // Migrate from SQLite
  async migrateSQLite(config: SQLiteMigrationConfig): Promise<MigrationResult> {
    const { source, domain, preserveIds } = config;
    const sqlite = new SQLiteReader(source);
    const entries = await sqlite.readAll();

    let migrated = 0;
    let failed = 0;

    for (const entry of entries) {
      try {
        await this.unifiedMemory.store({
          id: preserveIds ? entry.id : undefined,
          domain,
          content: entry.data,
          metadata: {
            migratedFrom: 'sqlite',
            originalId: entry.id,
            migratedAt: new Date().toISOString()
          }
        });
        migrated++;
      } catch (error) {
        failed++;
        console.error(`Failed to migrate entry ${entry.id}:`, error);
      }
    }

    return { migrated, failed, total: entries.length };
  }

  // Migrate from markdown files
  async migrateMarkdown(config: MarkdownMigrationConfig): Promise<MigrationResult> {
    const { pattern, domain } = config;
    const files = await glob(pattern);

    let migrated = 0;
    let failed = 0;

    for (const file of files) {
      try {
        const content = await readFile(file, 'utf-8');
        const parsed = this.parseMarkdown(content);

        await this.unifiedMemory.store({
          domain,
          content: parsed,
          metadata: {
            migratedFrom: 'markdown',
            sourceFile: file,
            migratedAt: new Date().toISOString()
          }
        });
        migrated++;
      } catch (error) {
        failed++;
      }
    }

    return { migrated, failed, total: files.length };
  }

  // Migrate in-memory data
  async migrateInMemory(
    data: Map<string, unknown>,
    domain: string
  ): Promise<MigrationResult> {
    let migrated = 0;
    let failed = 0;

    for (const [key, value] of data.entries()) {
      try {
        await this.unifiedMemory.store({
          id: key,
          domain,
          content: value,
          metadata: {
            migratedFrom: 'in-memory',
            migratedAt: new Date().toISOString()
          }
        });
        migrated++;
      } catch (error) {
        failed++;
      }
    }

    return { migrated, failed, total: data.size };
  }
}
```

### 3. SONA Integration

```typescript
// v3/src/memory/sona/QESONAMemory.ts
export class QESONAMemory {
  constructor(
    private readonly unifiedMemory: QEUnifiedMemory,
    private readonly sonaProvider: SONAProvider
  ) {}

  // Enable SONA for pattern learning
  async enableSONAIntegration(config: SONAConfig): Promise<void> {
    await this.sonaProvider.initialize({
      mode: config.mode || 'real-time',
      adaptationTimeMs: config.adaptationTimeMs || 0.05,
      patternStorage: true
    });

    // Subscribe to memory events for pattern learning
    this.unifiedMemory.on('stored', async (entry) => {
      await this.learnFromEntry(entry);
    });

    this.unifiedMemory.on('searched', async (query, results) => {
      await this.learnFromSearch(query, results);
    });
  }

  private async learnFromEntry(entry: QEMemoryEntry): Promise<void> {
    if (entry.domain === 'learning-patterns') {
      await this.sonaProvider.adaptPattern({
        pattern: entry.content,
        source: entry.domain,
        timestamp: new Date()
      });
    }
  }

  private async learnFromSearch(
    query: string,
    results: SearchResult[]
  ): Promise<void> {
    if (results.length > 0) {
      await this.sonaProvider.reinforcePattern({
        query,
        topResults: results.slice(0, 3),
        timestamp: new Date()
      });
    }
  }

  // Get pattern recommendations
  async getRecommendations(context: string): Promise<PatternRecommendation[]> {
    const sonaPatterns = await this.sonaProvider.predictPatterns(context);
    const memoryPatterns = await this.unifiedMemory.search(context, {
      domains: ['learning-patterns'],
      limit: 5
    });

    return this.mergeRecommendations(sonaPatterns, memoryPatterns);
  }
}
```

## HNSW Configuration Reference

| Domain | M | efConstruction | efSearch | Use Case |
|--------|---|----------------|----------|----------|
| defect-patterns | 32 | 400 | 200 | High precision for prediction |
| coverage-analysis | 16 | 200 | 100 | Balanced for gap detection |
| test-suites | 8 | 100 | 50 | Fast lookup |
| learning-patterns | 24 | 300 | 150 | High recall for transfer |
| quality-metrics | 16 | 200 | 100 | Balanced |
| coordination | 8 | 100 | 50 | Fast agent state lookup |

## Performance Targets

| Operation | Target | Achieved Via |
|-----------|--------|--------------|
| Semantic search (10K entries) | <1ms | HNSW O(log n) |
| Semantic search (100K entries) | <2ms | HNSW O(log n) |
| Semantic search (1M entries) | <5ms | HNSW O(log n) |
| Memory usage | 50-75% reduction | Quantization |
| Cross-agent sharing | Real-time | Event-driven sync |
| Pattern adaptation | <0.05ms | SONA integration |

## CLI Commands

```bash
# Initialize unified memory
aqe-v3 memory init --unified --hnsw
aqe-v3 memory init --config memory-config.yaml

# Migration commands
aqe-v3 memory migrate --source sqlite --path ./data/coverage.db --domain coverage-analysis
aqe-v3 memory migrate --source markdown --pattern "docs/**/*.md" --domain defect-patterns
aqe-v3 memory migrate --source memory --domain test-suites

# Search operations
aqe-v3 memory search --query "authentication test patterns"
aqe-v3 memory search --query "sql injection vulnerabilities" --domains security-compliance
aqe-v3 memory search --query "flaky tests" --limit 20 --threshold 0.7

# SONA operations
aqe-v3 memory sona --enable --mode real-time
aqe-v3 memory sona --status
aqe-v3 memory sona --patterns --domain defect-patterns

# Cross-domain sharing
aqe-v3 memory share --from learning-patterns --to test-generation,coverage-analysis
aqe-v3 memory share --query "best practices" --targets all

# Statistics
aqe-v3 memory stats
aqe-v3 memory stats --domain coverage-analysis --detailed
```

## Implementation Checklist

- [ ] Implement QEUnifiedMemory with AgentDB
- [ ] Configure HNSW indexes per domain
- [ ] Create SQLite migration service
- [ ] Create markdown migration service
- [ ] Implement SONA integration
- [ ] Add cross-domain knowledge sharing
- [ ] Implement quantization for memory reduction
- [ ] Write performance benchmarks
- [ ] Add CLI commands

## Related Skills

- v3-qe-memory-system - Basic memory operations
- v3-qe-learning-optimization - Pattern learning
- v3-qe-agentic-flow-integration - SONA integration
- v3-memory-unification (claude-flow) - Reference implementation

## Related ADRs

- ADR-038: V3 QE Memory System Unification
- ADR-006: Unified Memory Service (claude-flow)
- ADR-009: Hybrid Memory Backend (claude-flow)
