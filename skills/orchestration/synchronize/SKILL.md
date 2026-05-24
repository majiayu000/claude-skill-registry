---
name: synchronize
description: Merge outputs from multiple sources, resolve conflicts, and reconcile constraints into a unified result. Use when combining parallel agent outputs, merging data from different systems, or reconciling conflicting information.
argument-hint: "[sources] [strategy merge|replace|conflict_resolve] [conflict_rules]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Execute **synchronize** to merge data from multiple sources into a coherent, unified result with explicit conflict resolution.

**Success criteria:**
- All source data is accounted for (merged, replaced, or explicitly dropped)
- Conflicts are detected and resolved according to specified strategy
- Provenance is preserved for each merged element
- Output includes lineage trace for every change

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `sources` | Yes | array[string\|object] | List of data sources to synchronize (URIs, agent outputs, or inline data) |
| `strategy` | No | enum | Merge strategy: `merge` (combine), `replace` (latest wins), `conflict_resolve` (manual rules). Default: `merge` |
| `conflict_rules` | No | object | Rules for conflict resolution: priority order, field-level policies, or custom handlers |
| `target_schema` | No | string | Schema to validate merged output against |

## Procedure

1) **Inventory sources**: List all sources to synchronize
   - Record source type (agent output, file, API response)
   - Extract timestamp or version if available
   - Note source authority level (primary, secondary, derived)

2) **Normalize structures**: Transform all sources to comparable format
   - Identify common keys/fields across sources
   - Map equivalent fields with different names
   - Flag structural incompatibilities

3) **Detect conflicts**: Compare values for overlapping entities
   - Exact match: no conflict
   - Value difference: record as conflict with both values
   - Missing in one source: record as addition/deletion

4) **Apply resolution strategy**:
   - `merge`: Combine non-conflicting data; use conflict_rules for overlaps
   - `replace`: Use most recent or highest-priority source
   - `conflict_resolve`: Apply explicit rules; flag unresolvable for human review

5) **Ground claims**: Attach provenance to each merged element
   - Format: `source:<source_id>:<path>` or `conflict:<resolution_method>`
   - Track which source contributed each field

6) **Validate output**: Check merged result against target schema if provided

7) **Format output**: Structure results according to the output contract below

## Output Contract

Return a structured object:

```yaml
synchronization:
  sources: array[string]  # IDs of sources synchronized
  strategy: merge | replace | conflict_resolve
  timestamp: string  # ISO timestamp of sync operation
changes:
  - source: string  # Which source provided this change
    type: add | modify | delete
    entity: string  # Entity ID or path affected
    field: string | null  # Specific field if applicable
    value: object  # New/changed value
conflicts:
  - sources: array[string]  # Sources with conflicting values
    attribute: string  # Field/path in conflict
    values: array[object]  # Conflicting values from each source
    resolution: string | null  # How resolved, or null if unresolved
    resolution_rationale: string | null
result:
  synchronized: boolean  # True if all conflicts resolved
  entities_affected: integer  # Count of entities changed
  unresolved_conflicts: integer  # Count of conflicts needing human review
merged_data: object  # The synchronized result
confidence: number  # 0.0-1.0 based on conflict count and resolution quality
evidence_anchors: array[string]  # Source references for each claim
assumptions: array[string]  # Explicit assumptions made during sync
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `synchronization.sources` | array[string] | Identifiers for all sources included |
| `changes` | array[object] | Detailed log of every change made |
| `conflicts` | array[object] | All detected conflicts and their resolution |
| `result.synchronized` | boolean | Whether sync completed without unresolved conflicts |
| `merged_data` | object | The final synchronized output |
| `confidence` | number | Lower if many conflicts; higher if clean merge |

## Examples

### Example 1: Merging Two Agent Outputs

**Input:**
```yaml
sources:
  - agent_output_1:
      entity: "user_123"
      name: "Alice"
      role: "admin"
      last_seen: "2024-01-15"
  - agent_output_2:
      entity: "user_123"
      name: "Alice Smith"
      department: "Engineering"
      last_seen: "2024-01-16"
strategy: merge
conflict_rules:
  name: prefer_longer
  last_seen: prefer_newer
```

**Output:**
```yaml
synchronization:
  sources: ["agent_output_1", "agent_output_2"]
  strategy: merge
  timestamp: "2024-01-16T14:30:00Z"
changes:
  - source: "agent_output_1"
    type: add
    entity: "user_123"
    field: "role"
    value: "admin"
  - source: "agent_output_2"
    type: add
    entity: "user_123"
    field: "department"
    value: "Engineering"
  - source: "agent_output_2"
    type: modify
    entity: "user_123"
    field: "name"
    value: "Alice Smith"
  - source: "agent_output_2"
    type: modify
    entity: "user_123"
    field: "last_seen"
    value: "2024-01-16"
conflicts:
  - sources: ["agent_output_1", "agent_output_2"]
    attribute: "name"
    values: ["Alice", "Alice Smith"]
    resolution: "prefer_longer"
    resolution_rationale: "Longer name likely more complete"
  - sources: ["agent_output_1", "agent_output_2"]
    attribute: "last_seen"
    values: ["2024-01-15", "2024-01-16"]
    resolution: "prefer_newer"
    resolution_rationale: "More recent timestamp preferred"
result:
  synchronized: true
  entities_affected: 1
  unresolved_conflicts: 0
merged_data:
  entity: "user_123"
  name: "Alice Smith"
  role: "admin"
  department: "Engineering"
  last_seen: "2024-01-16"
confidence: 0.95
evidence_anchors:
  - "source:agent_output_1:role"
  - "source:agent_output_2:department"
  - "conflict:name:prefer_longer"
  - "conflict:last_seen:prefer_newer"
assumptions:
  - "Both sources refer to same user_123 entity"
  - "Longer name is more complete (not a different person)"
```

**Evidence pattern:** Each field in merged_data traced to originating source; conflicts logged with resolution method.

---

### Example 2: Unresolvable Conflict

**Input:**
```yaml
sources:
  - system_a: { price: 100, currency: "USD" }
  - system_b: { price: 150, currency: "USD" }
strategy: conflict_resolve
conflict_rules:
  price: require_human_review
```

**Output:**
```yaml
synchronization:
  sources: ["system_a", "system_b"]
  strategy: conflict_resolve
  timestamp: "2024-01-16T15:00:00Z"
changes: []
conflicts:
  - sources: ["system_a", "system_b"]
    attribute: "price"
    values: [100, 150]
    resolution: null
    resolution_rationale: "Price conflict requires human review per policy"
result:
  synchronized: false
  entities_affected: 0
  unresolved_conflicts: 1
merged_data: null
confidence: 0.3
evidence_anchors:
  - "source:system_a:price"
  - "source:system_b:price"
assumptions:
  - "Both prices refer to same product"
  - "50% price discrepancy exceeds auto-resolve threshold"
```

## Verification

- [ ] All source data accounted for in changes or conflicts
- [ ] Every conflict has resolution or is flagged unresolved
- [ ] merged_data passes target_schema validation (if provided)
- [ ] confidence reflects conflict severity and resolution quality
- [ ] evidence_anchors trace every merged field to source

**Verification tools:** Read (to validate source accessibility), Grep (to search for schema definitions)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Do not auto-resolve conflicts involving security-sensitive fields (credentials, permissions)
- Preserve original source data in evidence_anchors; never discard
- Flag confidence < 0.5 if more than 30% of fields have conflicts
- Stop and request clarification if sources have incompatible schemas

## Composition Patterns

**Commonly follows:**
- `retrieve` - Gathers raw data from multiple sources for synchronization
- `transform` - Normalizes data formats before merge
- `receive` - Ingests incoming events to synchronize with existing state
- `delegate` - Returns outputs from parallel agents to be merged

**Commonly precedes:**
- `world-state` - Synchronized data becomes canonical state snapshot
- `identity-resolution` - Merged entities may need identity reconciliation
- `persist` - Save synchronized result to durable storage
- `verify` - Validate merged output meets requirements

**Anti-patterns:**
- Never synchronize without `grounding` - merge requires evidence anchors (see ontology edge)
- Never synchronize without `provenance` - merge requires lineage trace (see ontology edge)
- Avoid synchronizing security-sensitive data without human review

**Workflow references:**
- See `reference/composition_patterns.md#digital-twin-sync-loop` for twin state synchronization
- See `reference/composition_patterns.md#enrichment-pipeline` for parallel data gathering
