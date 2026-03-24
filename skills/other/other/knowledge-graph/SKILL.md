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

---

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

---

## Instructions

### 1. read-knowledge-graph

**Purpose**: Load and parse the Knowledge Graph for a specification.

**Usage:**
```
/knowledge-graph read [spec-folder]
```

**Parameters:**
- `spec-folder`: Path to spec folder (e.g., `docs/specs/001-feature/`)

**Behavior:**
- Looks for `knowledge-graph.json` in the spec folder
- Parses and validates JSON structure
- Returns empty KG structure if file doesn't exist
- Raises error if JSON is invalid

**Example:**
```
Input: docs/specs/001-hotel-search/
Output: {
  metadata: { spec_id: "001-hotel-search", version: "1.0" },
  patterns: { architectural: [...], conventions: [...] },
  components: { controllers: [...], services: [...], repositories: [...] }
}
```

**Implementation Steps:**
1. Parse spec folder path
2. Check if `knowledge-graph.json` exists
3. If exists: Read file, parse JSON, validate structure
4. If not exists: Return empty KG with metadata
5. Return parsed KG object

---

### 2. query-knowledge-graph

**Purpose**: Query specific sections of the Knowledge Graph.

**Usage:**
```
/knowledge-graph query [spec-folder] [query-type] [filters]
```

**Parameters:**
- `spec-folder`: Path to spec folder
- `query-type`: One of: `components`, `patterns`, `apis`, `integration-points`, `all`
- `filters`: Optional JSON filters (e.g., `{"category": "services"}`)

**Behavior:**
- Loads KG from spec folder
- Filters by query type
- Applies optional filters
- Returns matching results

**Example Queries:**

```
# Find all services
/knowledge-graph query docs/specs/001-hotel-search/ components {"category": "services"}
→ Returns: [{ id: "comp-svc-001", name: "HotelService", ... }]

# Find architectural patterns
/knowledge-graph query docs/specs/001-hotel-search/ patterns {"category": "architectural"}
→ Returns: [{ name: "Repository Pattern", convention: "..." }]

# Find REST endpoints
/knowledge-graph query docs/specs/001-hotel-search/ apis {"type": "internal"}
→ Returns: [{ path: "/api/v1/hotels", method: "GET" }]
```

**Implementation Steps:**
1. Call `read-knowledge-graph` to load KG
2. Navigate to requested section (e.g., `kg.components`)
3. Apply filters if provided
4. Return filtered results

---

### 3. update-knowledge-graph

**Purpose**: Update the Knowledge Graph with new discoveries from agents or analysis.

**Usage:**
```
/knowledge-graph update [spec-folder] [updates] [source]
```

**Parameters:**
- `spec-folder`: Path to spec folder
- `updates`: Partial KG object with new findings
- `source`: Description of what provided updates (e.g., "general-code-explorer agent")

**Behavior:**
- Loads existing KG (or creates new)
- Deep merges updates into existing KG
- Updates `metadata.updated_at` timestamp
- Adds entry to `metadata.analysis_sources`
- Writes updated KG back to file

**Example:**

```
Input:
  spec-folder: docs/specs/001-hotel-search/
  updates: {
    patterns: {
      architectural: [
        { name: "Service Locator Pattern", convention: "..." }
      ]
    }
  }
  source: "general-software-architect agent"

Behavior:
1. Load existing docs/specs/001-hotel-search/knowledge-graph.json
2. Merge new pattern into patterns.architectural array
3. Update metadata.updated_at to current timestamp
4. Add { agent: "general-software-architect", timestamp: "..." } to analysis_sources
5. Write back to file
```

**Merge Logic:**
- **Arrays**: Append new items (check for duplicates by ID)
- **Objects**: Deep merge, preserve existing keys
- **Metadata**: Always update timestamps and sources

**Implementation Steps:**
1. Call `read-knowledge-graph` to load existing KG
2. Parse `updates` parameter
3. Deep merge updates into KG (preserve existing, add new)
4. Update `metadata.updated_at` to current ISO timestamp
5. Add entry to `metadata.analysis_sources`
6. Write updated KG to `docs/specs/[ID]/knowledge-graph.json`
7. Log summary of changes (e.g., "Added 2 patterns, 1 component")

---

### 4. validate-against-knowledge-graph

**Purpose**: Validate task requirements against actual codebase state stored in KG.

**Usage:**
```
/knowledge-graph validate [spec-folder] [requirements]
```

**Parameters:**
- `spec-folder`: Path to spec folder
- `requirements`: Object with task dependencies (components, APIs, patterns)

**Behavior:**
- Loads KG from spec folder
- Checks if required components/APIs exist
- Compares pattern usage against KG conventions
- Returns validation report with errors and warnings

**Example:**

```
Input:
  spec-folder: docs/specs/001-hotel-search/
  requirements: {
    components: ["comp-repo-001", "comp-svc-missing"],
    apis: ["api-int-001"],
    patterns: [{ name: "Repository Pattern" }]
  }

Output:
  {
    errors: [
      "Component comp-svc-missing not found in codebase"
    ],
    warnings: [
      "API api-int-001 not found, may need implementation"
    ],
    valid: false
  }
```

**Validation Rules:**

| Check | Severity | Message |
|-------|----------|---------|
| Component missing | Error | "Component {id} not found" |
| API missing | Warning | "API {id} not found, may need implementation" |
| Pattern mismatch | Warning | "Pattern {name} differs from convention" |
| Convention violated | Warning | "Naming convention violation: {component}" |

**Implementation Steps:**
1. Call `read-knowledge-graph` to load KG
2. Parse `requirements` parameter
3. Check each required component exists in `kg.components`
4. Check each required API exists in `kg.apis`
5. Check pattern usage matches `kg.patterns`
6. Return validation report with errors/warnings

---

### 5. validate-contract (NEW)

**Purpose**: Validate that task expectations (expects) are satisfied by completed dependencies (provides).

**Usage:**
```
/knowledge-graph validate-contract [spec-folder] [expects] [completed-dependencies]
```

**Parameters:**
- `spec-folder`: Path to spec folder
- `expects`: Array of expected items (files + symbols)
- `completed-dependencies`: Array of task IDs that are completed, each with their provides

**Behavior:**
- Checks if expected files exist
- Verifies expected symbols are declared in those files
- Validates that completed dependencies provide what's expected
- Returns validation report with satisfied/unsatisfied expectations

**Example:**

```
Input:
  spec-folder: docs/specs/001-hotel-search/
  expects: [
    { file: "src/main/java/com/hotels/search/domain/entity/Search.java", symbols: ["Search", "SearchStatus"] },
    { file: "src/main/java/com/hotels/search/domain/valueobject/SearchId.java", symbols: ["SearchId"] }
  ]
  completed-dependencies: [
    { task_id: "TASK-001", provides: [
      { file: "src/main/java/com/hotels/search/domain/entity/Search.java", symbols: ["Search", "SearchStatus", "SearchCriteria"] }
    ]}
  ]

Output:
  {
    satisfied: [
      { expectation: "Search entity with symbols [Search, SearchStatus]", provided_by: "TASK-001" }
    ],
    unsatisfied: [
      { expectation: "SearchId value object", provided_by: "None", reason: "No completed dependency provides SearchId" }
    ],
    valid: false
  }
```

**Implementation Steps:**
1. For each expectation in `expects`:
   a. Check if file exists (using Glob or Read)
   b. Check if symbols are declared (using Grep to find class/interface declarations)
2. Match expectations against provides from completed dependencies
3. Build satisfied/unsatisfied arrays
4. Return validation report

**Error Messages:**
| Scenario | Message |
|----------|---------|
| File not found | "Expected file {path} does not exist" |
| Symbol not found | "Expected symbol {symbol} not found in {file}" |
| No provider | "No completed dependency provides {item}" |
| Contract satisfied | "Expectation satisfied by {task_id}" |

---

### 6. extract-provides (NEW)

**Purpose**: Extract actual provides from implemented files by analyzing source code.

**Usage:**
```
/knowledge-graph extract-provides [files]
```

**Parameters:**
- `files`: Array of file paths to analyze

**Behavior:**
- For each file, parse to find declared symbols
- Classify symbols by type (entity, value-object, service, repository, etc.)
- Return array of provides with file, symbols, and inferred type

**Example:**

```
Input:
  files: [
    "src/main/java/com/hotels/search/domain/entity/Search.java",
    "src/main/java/com/hotels/search/domain/valueobject/SearchId.java"
  ]

Output:
  provides: [
    {
      file: "src/main/java/com/hotels/search/domain/entity/Search.java",
      symbols: ["Search", "SearchStatus"],
      type: "entity"
    },
    {
      file: "src/main/java/com/hotels/search/domain/valueobject/SearchId.java",
      symbols: ["SearchId"],
      type: "value-object"
    }
  ]
```

**Symbol Detection by Language:**

| Language | Symbol Types | Detection Method |
|----------|-------------|------------------|
| Java | class, interface, enum | Grep for `^(public\|protected)? (class\|interface\|enum) ` |
| TypeScript | class, interface, function, const | Grep for `^(export )?(class\|interface\|function\|const) ` |
| Python | class, function | Grep for `^(class\|def) ` |
| Go | struct, func, interface | Grep for `^(type\|func) ` |

**Implementation Steps:**
1. For each file:
   a. Detect language from extension
   b. Use appropriate Grep pattern to find declarations
   c. Infer type from directory structure (e.g., `/domain/entity/` → entity)
   d. Extract symbol names
2. Build provides array
3. Return extracted provides

---


### 7. aggregate-knowledge-graphs (NEW)

**Purpose**: Merge patterns and conventions from all spec KGs into a project-level summary for cross-spec learning.

**Usage**:
```
/knowledge-graph aggregate [project-root]
```

**Parameters**:
- `project-root`: Path to project root containing docs/specs/ directory

**Behavior**:
- Scan all `docs/specs/*/knowledge-graph.json` files
- Extract `patterns.architectural` and `patterns.conventions` from each KG
- Deduplicate by pattern name
- Write to `docs/specs/.global-knowledge-graph.json`
- Include metadata: which specs contributed, last aggregation date

**Output**: `docs/specs/.global-knowledge-graph.json`

**Global KG Schema**:
```json
{
  "metadata": {
    "aggregated_at": "[ISO timestamp]",
    "project_root": "[path]",
    "contributing_specs": ["spec-id-1", "spec-id-2"],
    "total_patterns": N
  },
  "patterns": {
    "architectural": [
      {
        "name": "[Pattern Name]",
        "sources": ["spec-id-1", "spec-id-2"],
        "frequency": 2,
        "first_seen": "[date]",
        "convention": "[detailed convention]"
      }
    ],
    "conventions": [
      {
        "name": "[Convention Name]",
        "sources": ["spec-id-1"],
        "frequency": 1,
        "examples": ["[brief example]"]
      }
    ]
  }
}
```

**Implementation Steps**:
1. Scan docs/specs/ for all subdirectories containing knowledge-graph.json
2. For each KG found:
   a. Extract all patterns.architectural entries
   b. Extract all patterns.conventions entries
   c. Track which spec contributed each pattern
3. Deduplicate by pattern.name (keep most detailed version)
4. Build global KG with deduplicated patterns
5. Update metadata with aggregation timestamp and contributing specs
6. Write to docs/specs/.global-knowledge-graph.json
7. Return summary: "Aggregated N architectural patterns and M conventions from X specs"
## KG Schema Reference

The Knowledge Graph follows this structure:

```
knowledge-graph.json
├── metadata
│   ├── spec_id (string)
│   ├── feature_name (string)
│   ├── created_at (ISO timestamp)
│   ├── updated_at (ISO timestamp)
│   ├── version (string)
│   └── analysis_sources (array of {agent, timestamp, focus})
├── codebase_context
│   ├── project_structure
│   └── technology_stack
├── patterns
│   ├── architectural (array)
│   └── conventions (array)
├── components
│   ├── controllers (array)
│   ├── services (array)
│   ├── repositories (array)
│   ├── entities (array)
│   └── dtos (array)
├── provides (array) [NEW]
│   └── { task_id, file, symbols: [], type, implemented_at }
├── apis
│   ├── internal (array)
│   └── external (array)
└── integration_points (array)
```

**provides Schema (NEW):**
```json
"provides": [
  {
    "task_id": "TASK-001",
    "file": "src/main/java/com/example/Domain.java",
    "symbols": ["EntityName", "Status"],
    "type": "entity|value-object|service|repository|controller|function|module",
    "implemented_at": "2026-03-14T10:30:00Z"
  }
]
```

For detailed schema with examples, see `references/schema.md`.

---

## Integration Patterns

The Knowledge Graph integrates with Developer Kit commands through specific phases in the spec-to-tasks, task-implementation, and spec-quality workflows.

**Key Integration Points:**

- **spec-to-tasks Phase 2.5**: Check/load cached analysis before exploring
- **spec-to-tasks Phase 3.5**: Persist agent discoveries after analysis
- **task-implementation T-3.5**: Knowledge Graph validation for existing components/APIs
- **task-implementation T-3.6**: Contract validation for provides/expects between tasks
- **task-implementation T-6.5**: Trigger `spec-quality` to persist provides after task completion
- **spec-quality Phase 4**: Merge extracted provides into the KG

For detailed integration patterns, data flows, and examples, see `references/integration-patterns.md`.

---

## Error Handling

### File Not Found
- **Behavior**: Return empty KG structure
- **Message**: "No existing knowledge graph, will create new"
- **Action**: Continue with empty KG, will be created on first update

### Invalid JSON
- **Behavior**: Raise error
- **Message**: "Knowledge graph corrupted at {path}"
- **Action**: Ask user: "Recreate from codebase analysis?"

### Merge Conflicts
- **Behavior**: Preserve existing values, add new with timestamps
- **Message**: "Merged X new findings into existing knowledge graph"

### Write Failure
- **Behavior**: Log error, continue without caching
- **Message**: "Cannot write knowledge graph, continuing without cache"

---

## Performance Considerations

- **Lazy loading**: Only load KG when explicitly requested
- **Incremental updates**: Merge changes, don't rewrite entire file
- **Cache invalidation**: Check timestamp, re-explore if KG > 7 days old
- **File size**: Monitor KG size; if > 1MB, suggest splitting by feature

---

## Security

- **Path validation**: Only read KG from `docs/specs/[ID]/` paths
- **JSON injection**: Validate all updates before merging
- **Secrets exclusion**: KG should NOT contain passwords, API keys, tokens
- **Git safety**: KG files can be committed (no sensitive data by design)

---

## Best Practices

### When to Query KG
- ✅ Before launching expensive codebase analysis
- ✅ When generating tasks to enrich technical context
- ✅ When validating task dependencies
- ✅ When checking if patterns/components exist

### When to Update KG
- ✅ After agent analysis completes (new discoveries)
- ✅ After implementing new components (add to graph)
- ✅ After discovering new patterns (document conventions)
- ❌ NOT during every operation (update in batches)

### KG Freshness
- **7 days**: Consider KG fresh, use cached analysis
- **30 days**: KG getting stale, warn user
- **Never updated**: Offer to regenerate from codebase

---

## Examples

### Example 1: Cache Agent Discoveries

```
# spec-to-tasks Phase 3.5
Agent output: "Found Repository Pattern with JpaRepository convention"

Update KG:
/knowledge-graph update docs/specs/001-feature/ {
  patterns: {
    architectural: [
      {
        id: "pat-001",
        name: "Repository Pattern",
        convention: "All repositories extend JpaRepository"
      }
    ]
  }
} "general-software-architect agent"

Result: knowledge-graph.json updated with pattern discovery
```

### Example 2: Validate Task Dependencies

```
# task-implementation Task Mode
Task: "Use HotelRepository to search hotels"

Validate:
/knowledge-graph validate docs/specs/001-hotel-search/ {
  components: ["comp-repo-001"]
}

Result:
{
  valid: true,
  errors: [],
  warnings: []
}

→ Task validated, proceed with implementation
```

### Example 3: Query for Context

```
# spec-to-tasks Phase 4
Need to generate tasks for "Add booking feature"

Query KG:
/knowledge-graph query docs/specs/001-hotel-search/ patterns

Result:
[
  { name: "Repository Pattern", convention: "Extend JpaRepository" },
  { name: "Service Layer", convention: "@Service classes" }
]

→ Generate tasks following discovered patterns
```

---

## Constraints and Warnings

### Critical Constraints

- **Source-Code Safe Operations**: The knowledge-graph skill does NOT modify source code files. It only creates or updates `knowledge-graph.json` files and related KG artifacts.
- **Path Validation**: The skill only reads/writes KG files from `docs/specs/[ID]/` paths. It will NOT access files outside this structure.
- **No Automatic Code Generation**: This skill caches analysis results, it does NOT generate implementation code automatically.

### Limitations

- **Validation Scope**: The `validate-against-knowledge-graph` function checks if components exist in the KG, but cannot verify if they exist in the actual codebase if the KG is outdated.
- **Freshness Dependency**: KG accuracy depends on how recently it was updated. A KG older than 7 days may be stale.
- **Single-Spec First**: Each KG is primarily specific to a single specification (`docs/specs/[ID]/`). Cross-spec learning is available only through the optional `aggregate` operation and `.global-knowledge-graph.json`.
- **File Size**: KG files can grow large (>1MB) for complex specifications. Monitor size and consider splitting if needed.

### Warnings

- **Stale Knowledge**: If KG `updated_at` is >30 days old, the analysis may not reflect current codebase state. Consider re-running codebase analysis.
- **Validation False Positives**: The validator may report "component not found" if the KG was created before the component was implemented. Always verify with actual codebase.
- **Merge Conflicts**: If KG is under version control, merge conflicts may occur. The skill uses deep-merge strategy to preserve existing data.
- **Manual Edits**: Manual edits to `knowledge-graph.json` are supported but may be overwritten if agents update the file. Document manual changes clearly.

### Security Considerations

- **No Secrets Storage**: KG should NOT contain passwords, API keys, tokens, or other sensitive data. It only stores structural information (patterns, components, APIs).
- **Git Safe**: KG files are designed to be committed to git (no sensitive data by design).
- **Path Traversal Protection**: All file operations are restricted to `docs/specs/` subdirectories to prevent path traversal attacks.
- **JSON Injection Prevention**: All updates are validated as proper JSON before merging into KG.

### Performance Considerations

- **Lazy Loading**: KG is only loaded when explicitly requested (not automatically on every operation).
- **Incremental Updates**: Updates use deep-merge to preserve existing data, not full rewrites.
- **Cache Invalidation**: Check `metadata.updated_at` before using KG; re-explore if >7 days old.
- **File Size Monitoring**: Monitor KG file size; if >1MB, consider splitting by feature area.

### Best Practices

- **Update Regularly**: Refresh KG after significant codebase changes or new feature implementations.
- **Validate First**: Always use `validate-against-knowledge-graph` before implementing tasks that depend on specific components.
- **Review Before Use**: Check KG age and contents before relying on cached analysis for critical decisions.
- **Document Discoveries**: Add clear descriptions when updating KG to help future users understand findings.
- **Team Coordination**: Communicate with team when updating KG to avoid conflicting updates.

---

## See Also

- `references/schema.md` - Complete JSON schema with examples
- `references/query-examples.md` - Query patterns and examples

For integration with commands, see:
- `/plugins/developer-kit-core/commands/specs/devkit.spec-to-tasks.md` (Phase 2.5, 3.5)
- `/plugins/developer-kit-core/commands/specs/devkit.task-implementation.md` (T-3.5, T-3.6, T-6.5)
- `/plugins/developer-kit-core/commands/specs/devkit.spec-quality.md` (Phase 4)
