---
name: knowledge-graph
description: "Manages persistent Knowledge Graph for specifications. Caches agent discoveries and codebase analysis to remember findings across sessions. Validates task dependencies, stores patterns, components, and APIs to avoid redundant exploration. Use when: you need to cache analysis results, remember findings, reuse previous discoveries, look up what we found, spec-to-tasks needs to persist codebase analysis, task-implementation needs to validate contracts, or any command needs to query existing patterns/components/APIs."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Knowledge Graph Skill

## Overview

Persistent JSON storage that caches agent discoveries and codebase analysis. Remember findings across sessions, validate task dependencies, query patterns/components/APIs, skip redundant exploration.

**Location**: `docs/specs/[ID-feature]/knowledge-graph.json`

---

## When to Use

1. **Cache results** - Before launching expensive codebase analysis, check if findings are already stored
2. **Remember findings** - After agent exploration, persist discoveries for future use
3. **Reuse discoveries** - Query existing context to maintain consistency across tasks
4. **Validate dependencies** - Check if required components/APIs exist before implementing
5. **Look up previous work** - Find what patterns, components, or APIs were already discovered

---

## Instructions

### read-knowledge-graph

Read existing Knowledge Graph or initialize empty structure:

```
Read file_path="docs/specs/001/knowledge-graph.json"
```

Returns full KG content. If file missing, returns empty structure and creates on first update.

---

### query-knowledge-graph

Query specific sections: `components`, `patterns`, `apis`, `integration-points`, `all`

```
Read file_path="docs/specs/001/knowledge-graph.json"
```

Filter results by section and process in-memory.

---

### update-knowledge-graph

```
# 1. Read existing
Read file_path="docs/specs/001/knowledge-graph.json"

# 2. Deep-merge updates (arrays append by ID, objects preserve existing)
# 3. Update timestamp
Write file_path="docs/specs/001/knowledge-graph.json" content="<merged JSON>"
```

**Deep-merge rules:**
- Arrays: append new items, deduplicate by `id` field
- Objects: preserve existing keys, add/update new keys
- Always update `metadata.updated_at` to current ISO timestamp

**Complete JSON example for update:**
```json
{
  "metadata": {
    "spec_id": "001-hotel-search",
    "created_at": "2026-03-14T10:30:00Z",
    "updated_at": "2026-03-23T10:00:00Z",
    "version": "1.0.0"
  },
  "patterns": {
    "architectural": [
      {
        "id": "pat-001",
        "name": "Repository Pattern",
        "convention": "Extend JpaRepository<Entity, ID>",
        "files": ["src/main/java/**/repository/*Repository.java"]
      }
    ]
  },
  "components": {
    "services": [
      {
        "id": "comp-svc-001",
        "name": "HotelService",
        "location": "src/main/java/com/example/hotel/service/HotelService.java",
        "type": "service",
        "methods": [{"name": "searchHotels", "returns": "List<HotelDTO>"}]
      }
    ]
  }
}
```

---

### validate-against-knowledge-graph

```
# 1. Read KG
Read file_path="docs/specs/001/knowledge-graph.json"

# 2. Check KG contains required IDs
# 3. Verify actual files exist
Grep pattern="src/**/HotelRepository.java"
```

Report satisfied dependencies and missing components.

---

### validate-contract

```
# 1. Read KG and task expectations
Read file_path="docs/specs/001/knowledge-graph.json"
Glob pattern="src/**/ExpectedFile.java"
Grep pattern="class ExpectedClass|interface ExpectedInterface"

# 2. Match expectations against KG.provides
# 3. Report satisfied/unsatisfied contracts
```

---

### extract-provides

```
# 1. Find implementation files
Glob pattern="src/**/*.java"

# 2. Extract symbols
Grep pattern="^(public|protected)? (class|interface|enum) " output_mode="content"

# 3. Classify by directory: /entity/ → entity, /service/ → service, /repository/ → repository
# 4. Update KG.provides with {task_id, file, symbols, type, implemented_at}
```

---

### aggregate-knowledge-graphs

```
# 1. Find all KG files
Glob pattern="docs/specs/*/knowledge-graph.json"

# 2. Read each, extract patterns.architectural and patterns.conventions
# 3. Write merged .global-knowledge-graph.json
Write file_path="docs/specs/.global-knowledge-graph.json" content="<aggregated>"
```

---

## Schema Structure

```
knowledge-graph.json
├── metadata (spec_id, created_at, updated_at, version, analysis_sources)
├── codebase_context (project_structure, technology_stack)
├── patterns (architectural[], conventions[])
├── components (controllers[], services[], repositories[], entities[], dtos[])
├── provides[] ({ task_id, file, symbols[], type, implemented_at })
├── apis (internal[], external[])
└── integration_points[]
```

**Complete schema with field definitions:** See `references/schema.md`

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| File not found | Return empty KG; creates on first update |
| Invalid JSON | Raise error; offer to recreate from analysis |
| Merge conflicts | Deep-merge preserves existing, adds new with timestamps |
| Write failure | Log error; continue without caching (non-blocking) |

**Update workflow:**
1. Read: `Read` → `docs/specs/[ID]/knowledge-graph.json`
2. Validate update JSON structure
3. Deep-merge updates into KG object
4. Write: `Write` → same path
5. Verify write succeeded

---

## Best Practices

**Before expensive operations:**
- Query KG first to check for cached analysis
- If fresh (< 7 days), skip redundant exploration
- Offer user choice: use cached or re-explore

**After discoveries:**
- Update KG immediately after agent analysis completes
- Include source agent/timestamp in metadata
- Batch similar updates, avoid per-operation writes

**Freshness guidelines:**
- < 7 days: Fresh, safe to use
- 7-30 days: Consider regenerating
- > 30 days: Stale, re-analysis recommended

---

## Examples

### Cache Agent Discoveries (Complete Workflow)

```
# Step 1: Check existing KG
Read file_path="docs/specs/001/knowledge-graph.json"

# Step 2: Analyze codebase (agent task)
Glob pattern="src/main/java/**/*.java"
Grep pattern="public (class|interface) " output_mode="content"

# Step 3: Build update with discoveries
Write file_path="docs/specs/001/knowledge-graph.json" content="{
  \"metadata\": {
    \"spec_id\": \"001-hotel-search\",
    \"created_at\": \"2026-03-14T10:30:00Z\",
    \"updated_at\": \"2026-03-23T10:00:00Z\",
    \"version\": \"1.0.0\",
    \"analysis_sources\": [{\"agent\": \"general-code-explorer\", \"timestamp\": \"2026-03-23T10:00:00Z\"}]
  },
  \"patterns\": {
    \"architectural\": [{
      \"id\": \"pat-001\",
      \"name\": \"Repository Pattern\",
      \"convention\": \"Extend JpaRepository<Entity, ID>\"
    }]
  },
  \"components\": {
    \"services\": [{
      \"id\": \"comp-svc-001\",
      \"name\": \"HotelService\",
      \"location\": \"src/main/java/com/example/hotel/service/HotelService.java\",
      \"type\": \"service\"
    }],
    \"repositories\": [{
      \"id\": \"comp-repo-001\",
      \"name\": \"HotelRepository\",
      \"location\": \"src/main/java/com/example/hotel/repository/HotelRepository.java\",
      \"type\": \"repository\"
    }]
  }
}"
```

### Validate Task Dependencies

```
# Read KG and task requirements
Read file_path="docs/specs/001/knowledge-graph.json"

# Verify components exist in codebase
Grep pattern="src/main/java/com/example/hotel/repository/HotelRepository.java"
Grep pattern="src/main/java/com/example/hotel/service/HotelService.java"

# Report validation result
# If all found: "All dependencies satisfied, proceed with implementation"
# If missing: "Warning: HotelService not found. Create it first?"
```

### Query for Context Before Task Generation

```
# Load KG to get cached context
Read file_path="docs/specs/001/knowledge-graph.json"

# Present summary to user:
# "Found cached analysis (2 days old):
#  - Patterns: Repository Pattern, Service Layer
#  - Components: HotelService, HotelController
#  - Conventions: naming with *Controller/*Service/*Repository
#  Use cached context for task generation?"
```

**More examples:** See `references/query-examples.md`

---

## Constraints and Warnings

**Critical Constraints:**
- Read-only on source code; only creates/updates `knowledge-graph.json`
- Only reads/writes KG files from `docs/specs/[ID]/` paths
- Does NOT generate implementation code automatically

**Limitations:**
- Validation checks KG only; cannot verify actual codebase if KG outdated
- KG accuracy depends on freshness; re-explore if > 7 days old
- Cross-spec learning only via `aggregate` operation

**Warnings:**
- KG > 30 days old may not reflect current codebase state
- Validator may report false negatives if KG predates implementation
- Merge strategy preserves existing values; explicit overwrite required to replace

---

## See Also

- `references/schema.md` - Complete JSON schema with field definitions
- `references/query-examples.md` - Query patterns and integration examples
- `references/integration-patterns.md` - Command integration details
