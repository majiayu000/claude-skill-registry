---
name: retrieve
description: Fetch known facts or data from specified sources with citations and evidence pointers. Use when you know what you need and where to find it. Emphasizes provenance and verifiable references.
argument-hint: "[target] [source] [format]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Web
context: fork
agent: explore
---

## Intent

Execute **retrieve** to fetch specific, known information from specified sources. Unlike `search` (which explores under uncertainty), retrieve fetches identified items with full provenance tracking.

**Success criteria:**
- Requested data is fetched completely
- Source and timestamp are recorded
- Data integrity is verified where possible
- Citations enable re-retrieval
- Missing data is explicitly flagged

**World Modeling Context:**
Retrieve feeds into all world modeling layers by providing grounded observations for `world-state`, timestamps for `temporal-reasoning`, and evidence for `grounding`.

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `target` | Yes | string\|object | What to retrieve (path, URL, query, or identifier) |
| `source` | No | string | Where to retrieve from (file, api, database); default: infer |
| `format` | No | string | Expected format (json, text, binary); default: auto-detect |
| `constraints` | No | object | Filters, projections, version specifications |

## Procedure

1) **Identify target**: Determine exactly what to fetch
   - File path: Exact file location
   - URL: Web resource address
   - API endpoint: Service + parameters
   - Record: Database/system identifier

2) **Verify source accessibility**: Confirm retrieval is possible
   - Check permissions
   - Verify network access if remote
   - Confirm source exists

3) **Execute retrieval**: Fetch the data
   - For files: Read with line numbers preserved
   - For URLs: Fetch with timeout and retry
   - For APIs: Call with appropriate auth
   - Record exact timestamp of retrieval

4) **Validate retrieved data**: Check completeness and integrity
   - Verify format matches expected
   - Check for truncation or corruption
   - Validate against schema if available
   - Compute hash for integrity tracking

5) **Extract relevant portions**: If constraints specified
   - Apply filters to reduce data
   - Project specific fields
   - Slice by line numbers or sections

6) **Construct citation**: Build verifiable reference
   - Full path/URL
   - Timestamp of retrieval
   - Version/revision if available
   - Hash for integrity verification

7) **Document provenance**: Record retrieval metadata
   - Source authority
   - Freshness (how current)
   - Reliability (historical accuracy)

8) **Handle failures**: If retrieval fails
   - Record failure reason
   - Suggest alternatives if available
   - Note partial success if applicable

## Output Contract

Return a structured object:

```yaml
retrieved:
  target: string  # What was requested
  source: string  # Where it came from
  timestamp: string  # ISO 8601 retrieval time
  data: object | string | array  # The retrieved content
  format: string  # Data format (json, text, etc.)
  complete: boolean  # Was full content retrieved?
citation:
  reference: string  # Full citation for re-retrieval
  version: string | null  # Version/revision if applicable
  hash: string | null  # Content hash for integrity
  authority: low | medium | high
provenance:
  source_type: string  # file, api, database, web
  last_modified: string | null  # When source was last changed
  freshness: fresh | stale | unknown  # How current is this data
  reliability: string  # Assessment of source reliability
extraction:
  applied_filters: object | null
  original_size: integer | null
  returned_size: integer | null
  truncated: boolean
confidence: number  # 0.0-1.0
evidence_anchors: array[string]
assumptions: array[string]
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `retrieved.data` | any | The fetched content |
| `citation` | object | Verifiable reference to re-fetch |
| `provenance` | object | Source reliability and freshness |
| `extraction` | object | Filtering/processing applied |

## Examples

### Example 1: Retrieve Configuration File

**Input:**
```yaml
target: "config/database.yml"
source: file
```

**Output:**
```yaml
retrieved:
  target: "config/database.yml"
  source: "file:config/database.yml"
  timestamp: "2025-01-24T15:30:00Z"
  data:
    development:
      adapter: postgresql
      host: localhost
      database: myapp_dev
    production:
      adapter: postgresql
      host: "${DATABASE_HOST}"
      database: myapp_prod
      pool: 25
  format: yaml
  complete: true
citation:
  reference: "config/database.yml:1-15"
  version: "git:abc123"
  hash: "sha256:def456..."
  authority: high
provenance:
  source_type: file
  last_modified: "2025-01-20T10:00:00Z"
  freshness: fresh
  reliability: "Version controlled, reviewed configuration"
extraction:
  applied_filters: null
  original_size: 450
  returned_size: 450
  truncated: false
confidence: 1.0
evidence_anchors:
  - "config/database.yml:1-15"
assumptions:
  - "File contents reflect deployed configuration"
```

**Evidence pattern:** Read file directly, computed hash, tracked git version.

---

### Example 2: Retrieve API Documentation

**Input:**
```yaml
target: "https://api.example.com/docs/v2/endpoints"
source: web
format: json
```

**Output:**
```yaml
retrieved:
  target: "https://api.example.com/docs/v2/endpoints"
  source: "web:api.example.com"
  timestamp: "2025-01-24T15:35:00Z"
  data:
    version: "2.0.0"
    endpoints:
      - path: "/users"
        methods: ["GET", "POST"]
        auth_required: true
      - path: "/users/{id}"
        methods: ["GET", "PUT", "DELETE"]
        auth_required: true
  format: json
  complete: true
citation:
  reference: "https://api.example.com/docs/v2/endpoints"
  version: "v2.0.0"
  hash: "sha256:789abc..."
  authority: high
provenance:
  source_type: web
  last_modified: "2025-01-15T00:00:00Z"
  freshness: fresh
  reliability: "Official API documentation"
extraction:
  applied_filters: null
  original_size: 2500
  returned_size: 2500
  truncated: false
confidence: 0.95
evidence_anchors:
  - "url:https://api.example.com/docs/v2/endpoints"
assumptions:
  - "API documentation reflects actual API behavior"
```

---

### Example 3: Retrieve with Filtering

**Input:**
```yaml
target: "src/models/user.ts"
source: file
constraints:
  lines: "1-50"
  sections: ["interface", "class"]
```

**Output:**
```yaml
retrieved:
  target: "src/models/user.ts"
  source: "file:src/models/user.ts"
  timestamp: "2025-01-24T15:40:00Z"
  data: |
    interface UserAttributes {
      id: string;
      email: string;
      name: string;
      createdAt: Date;
    }

    class User implements UserAttributes {
      id: string;
      email: string;
      name: string;
      createdAt: Date;

      constructor(attrs: UserAttributes) {
        Object.assign(this, attrs);
      }
    }
  format: text
  complete: false
citation:
  reference: "src/models/user.ts:1-50"
  version: "git:abc123"
  hash: null
  authority: high
provenance:
  source_type: file
  last_modified: "2025-01-22T09:00:00Z"
  freshness: fresh
  reliability: "Source code"
extraction:
  applied_filters:
    lines: "1-50"
    sections: ["interface", "class"]
  original_size: 5000
  returned_size: 500
  truncated: true
confidence: 0.95
evidence_anchors:
  - "src/models/user.ts:1-20"
  - "src/models/user.ts:22-35"
assumptions:
  - "Extracted sections are complete within specified lines"
```

## Verification

- [ ] Retrieved data matches expected format
- [ ] Citation enables exact re-retrieval
- [ ] Hash validates data integrity (when available)
- [ ] Truncation is explicitly flagged
- [ ] Timestamp is accurate

**Verification tools:** Hash verification, re-retrieval test

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Do not retrieve from paths marked as sensitive
- Respect rate limits on remote sources
- Flag stale data (>24h old for volatile sources)
- Never fabricate retrieved content

## Composition Patterns

**Commonly follows:**
- `search` - After finding, retrieve full content
- `inspect` - Retrieve specific files discovered during inspection

**Commonly precedes:**
- `world-state` - Retrieved data becomes observations
- `grounding` - Retrieved content provides evidence
- `provenance` - Retrieval is a step in provenance chain
- `integrate` - Retrieved data feeds integration

**Anti-patterns:**
- Avoid retrieving without tracking provenance
- Never assume retrieval succeeded without checking `complete`

**Workflow references:**
- See `reference/composition_patterns.md#world-model-build` for retrieval in model construction
- See `reference/composition_patterns.md#digital-twin-sync-loop` for ongoing data retrieval
