---
name: knowledge-graph
description: "Manage persistent Knowledge Graph for specifications. Provides read, query, update, and validation capabilities for codebase analysis caching. Use when: spec-to-tasks needs to cache/reuse codebase analysis, task-implementation needs to validate task dependencies or contracts, spec-quality needs to synchronize provides, or any command needs to query existing patterns/components/APIs. Reduces redundant codebase exploration by caching agent discoveries."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Knowledge Graph Skill

## Overview

The Knowledge Graph (KG) is a persistent JSON file that stores discoveries from codebase analysis, eliminating redundant exploration and enabling task validation.

**Location**: `docs/specs/[ID-feature]/knowledge-graph.json`

**Key Benefits:**
- ✅ Avoid re-exploring already-analyzed codebases
- ✅ Validate task dependencies against actual codebase state
- ✅ Share discoveries across team members
- ✅ Accelerate task generation with cached context

## When to Use

Use this skill when:

1. **spec-to-tasks needs to cache/reuse codebase analysis** - Store agent discoveries for future reuse
2. **task-implementation needs to validate task dependencies and contracts** - Check if required components exist before implementing
3. **Any command needs to query existing patterns/components/APIs** - Retrieve cached codebase context
4. **Reducing redundant codebase exploration** - Avoid re-analyzing already-explored code

**Trigger phrases:**
- "Load knowledge graph"
- "Query knowledge graph"
- "Update knowledge graph"
- "Validate against knowledge graph"
- "Check if component exists"
- "Find existing patterns"

## Instructions

### Available Operations

**1. read-knowledge-graph** - Load and parse KG for a specification
- **Input**: Path to spec folder (e.g., `docs/specs/001-feature/`)
- **Output**: KG object with metadata, patterns, components, APIs

**2. query-knowledge-graph** - Query specific sections (components, patterns, APIs)
- **Input**: Spec folder, query type, optional filters
- **Output**: Filtered results matching criteria

**3. update-knowledge-graph** - Update KG with new discoveries
- **Input**: Spec folder, updates (partial KG), source description
- **Output**: Merged KG with new findings

**4. validate-against-knowledge-graph** - Validate task dependencies against KG
- **Input**: Spec folder, requirements (components, APIs, patterns)
- **Output**: Validation report with errors/warnings

**5. validate-contract** - Validate provides/expects between tasks
- **Input**: Spec folder, expects (files + symbols), completed dependencies
- **Output**: Satisfied/unsatisfied expectations report

**6. extract-provides** - Extract symbols from implemented files
- **Input**: Array of file paths
- **Output**: Array of provides with file, symbols, type

**7. aggregate-knowledge-graphs** - Merge patterns from all specs
- **Input**: Project root path
- **Output**: Global KG with deduplicated patterns

See [references/query-examples.md](references/query-examples.md) for detailed usage examples.

## Examples

### Input/Output Examples

**Read Knowledge Graph:**
```
Input: /knowledge-graph read docs/specs/001-hotel-search/
Output: {
  metadata: { spec_id: "001-hotel-search", version: "1.0" },
  patterns: { architectural: [...], conventions: [...] },
  components: { controllers: [...], services: [...]}
}
```

**Query Components:**
```
Input: /knowledge-graph query docs/specs/001-hotel-search/ components {"category": "services"}
Output: [{ id: "comp-svc-001", name: "HotelSearchService", type: "service"}]
```

**Update Knowledge Graph:**
```
Input: /knowledge-graph update docs/specs/001-hotel-search/ {
  patterns: { architectural: [{ name: "Repository Pattern"}] }
}
Output: "Added 1 pattern to knowledge graph"
```

**Validate Dependencies:**
```
Input: /knowledge-graph validate docs/specs/001-hotel-search/ {
  components: ["comp-repo-001"]
}
Output: { valid: true, errors: [], warnings: [] }
```

See [references/examples.md](references/examples.md) for comprehensive workflow examples.

## KG Schema Reference

See [references/schema.md](references/schema.md) for complete JSON schema with examples.

## Integration Patterns

See [references/integration-patterns.md](references/integration-patterns.md) for detailed integration with Developer Kit commands.

## Error Handling

See [references/error-handling.md](references/error-handling.md) for comprehensive error handling strategies and recovery procedures.

## Performance Considerations

See [references/performance.md](references/performance.md) for optimization strategies and performance characteristics.

## Security

See [references/security.md](references/security.md) for security considerations, threat mitigation, and best practices.

## Best Practices

**When to Query KG**: Before codebase analysis, task generation, dependency validation

**When to Update KG**: After agent discoveries, component implementation, pattern discovery

**KG Freshness**:
- < 7 days: Fresh
- 7-30 days: Stale, warn user
- > 30 days: Very stale, offer regeneration

See [references/performance.md](references/performance.md) and [references/security.md](references/security.md) for detailed best practices.

## Constraints and Warnings

### Critical Constraints

- **Source-Code Safe Operations**: Does NOT modify source code files. Only creates/updates `knowledge-graph.json` files.
- **Path Validation**: Only reads/writes KG files from `docs/specs/[ID]/` paths.
- **No Automatic Code Generation**: Caches analysis results, does NOT generate implementation code.

### Limitations

- **Validation Scope**: Checks components exist in KG, but cannot verify if they exist in actual codebase if KG is outdated
- **Freshness Dependency**: KG accuracy depends on how recently it was updated
- **Single-Spec First**: Each KG is primarily specific to a single specification
- **File Size**: KG files can grow large (>1MB) for complex specifications

See [references/error-handling.md](references/error-handling.md) and [references/security.md](references/security.md) for complete constraints and warnings.

## Reference Files

- [schema.md](references/schema.md) - Complete JSON schema
- [query-examples.md](references/query-examples.md) - Query patterns
- [integration-patterns.md](references/integration-patterns.md) - Command integration
- [error-handling.md](references/error-handling.md) - Error handling guide
- [performance.md](references/performance.md) - Performance optimization
- [security.md](references/security.md) - Security considerations
- [examples.md](references/examples.md) - Practical examples
