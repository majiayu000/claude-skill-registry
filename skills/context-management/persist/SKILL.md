---
name: persist
description: Write stable learnings, decisions, and patterns to durable storage like CLAUDE.md or knowledge files. Use when saving project decisions, recording patterns, or updating long-term memory.
argument-hint: "[content] [destination CLAUDE.md|file] [section]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Edit
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: prompt
          prompt: |
            PERSIST DATA VALIDATION CHECK

            Target file: {{tool_input.file_path}}
            Content to write: {{tool_input.new_string}}

            Verify before persisting:
            1. NO credentials, API keys, or secrets in content
            2. NO personally identifiable information (PII)
            3. NO executable code that could be malicious
            4. File is within project scope (not system files)
            5. Content is stable knowledge (not ephemeral data)

            Also check:
            - Is this a duplicate of existing content?
            - Does this contradict existing persisted facts?

            Reply ALLOW if content is safe to persist.
            Reply BLOCK with specific reason if validation fails.
          once: false
        - type: command
          command: |
            # Validate target file is not a sensitive system file
            TARGET="{{tool_input.file_path}}"
            # Block writes to system directories
            if echo "$TARGET" | grep -qE "^(/etc/|/usr/|/bin/|/sbin/|~/.ssh/|~/.aws/|~/.config/)"; then
              echo "BLOCK: Cannot persist to system or credential directories"
              exit 1
            fi
            # Block writes to credential files
            if echo "$TARGET" | grep -qiE "(\.env|credentials|secrets|password|\.pem|\.key)$"; then
              echo "BLOCK: Cannot persist to credential files"
              exit 1
            fi
            exit 0
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: |
            echo "[PERSIST] $(date -u +%Y-%m-%dT%H:%M:%SZ) | File: {{tool_input.file_path}} | Success" >> .audit/persist-operations.log 2>/dev/null || true
---

## Intent

Execute **persist** to write stable learnings, decisions, and patterns to durable storage for future recall and consistency.

**Success criteria:**
- Content is written to the correct destination
- Existing content is preserved or properly merged
- New content follows established structure/format
- Metadata (timestamp, source) is recorded
- Write is verified successfully

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `content` | Yes | string\|object | What to persist: decision, pattern, fact, or structured knowledge |
| `destination` | No | string | Where to write: `CLAUDE.md`, file path, or `auto` (determine best location). Default: `CLAUDE.md` |
| `section` | No | string | Section within destination to write to (e.g., "Decisions", "Patterns", "Facts") |
| `content_type` | No | enum | Type of content: `decision`, `pattern`, `fact`, `context`. Default: auto-detect |
| `merge_strategy` | No | enum | How to handle existing content: `append`, `replace`, `merge`. Default: `append` |

## Procedure

1) **Validate content**: Ensure content is appropriate for persistence
   - Check content is non-empty and meaningful
   - Verify content type classification
   - Ensure no sensitive data (credentials, PII) is being persisted
   - Validate content structure if object

2) **Determine destination**: Select where to write
   - `CLAUDE.md`: Project-level decisions and patterns
   - Specific file: Domain or feature-specific knowledge
   - `auto`: Choose based on content type and scope

3) **Read existing content**: Load current state of destination
   - Parse structure and sections
   - Identify target section for new content
   - Note existing entries to avoid duplicates

4) **Check for duplicates/conflicts**: Compare new vs existing
   - Exact duplicate: Skip or update timestamp only
   - Similar content: Flag for review
   - Contradiction: Stop and request clarification

5) **Format new content**: Structure for persistence
   - Add timestamp and source metadata
   - Format according to destination conventions
   - Include rationale if decision/pattern

6) **Apply merge strategy**:
   - `append`: Add to end of section
   - `replace`: Overwrite matching existing entry
   - `merge`: Intelligently combine with existing

7) **Write to destination**: Execute the write operation
   - Use Edit tool for file modifications
   - Preserve file formatting and structure
   - Add section headers if needed

8) **Verify write**: Confirm content was persisted correctly
   - Re-read destination file
   - Confirm new content present
   - Validate structure integrity

## Output Contract

Return a structured object:

```yaml
persisted:
  content_type: decision | pattern | fact | context
  content_id: string  # Unique identifier for this persisted item
  destination: string  # File path where content was written
  section: string | null  # Section within file
  timestamp: string  # ISO timestamp of persistence
write_operation:
  strategy: append | replace | merge
  bytes_written: integer
  lines_added: integer
  lines_modified: integer
verification:
  write_confirmed: boolean
  content_present: boolean
  structure_valid: boolean
metadata:
  source: string  # Where this knowledge came from
  related_entries: array[string]  # IDs of related persisted items
  expiry: string | null  # When this knowledge should be reviewed
duplicates_found:
  - existing_id: string
    similarity: number
    action_taken: skipped | updated | merged
confidence: number  # 0.0-1.0 based on write verification
evidence_anchors: array[string]  # References to verification
assumptions: array[string]  # Explicit assumptions
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `persisted.content_id` | string | Unique ID for retrieval with `recall` |
| `persisted.destination` | string | File path of storage location |
| `write_operation` | object | Details of the write performed |
| `verification.write_confirmed` | boolean | Whether write was verified |
| `duplicates_found` | array | Any duplicate/similar entries detected |
| `confidence` | number | 1.0 if verified; lower if issues |

## Examples

### Example 1: Persisting a Project Decision

**Input:**
```yaml
content:
  decision: "Use PostgreSQL for all persistent storage"
  rationale: "Strong ACID guarantees, mature ecosystem, team familiarity"
  context: "Evaluated PostgreSQL, MySQL, and MongoDB for new backend service"
  constraints:
    - "Must support complex queries"
    - "Team has PostgreSQL experience"
destination: CLAUDE.md
section: "Architecture Decisions"
content_type: decision
```

**Output:**
```yaml
persisted:
  content_type: decision
  content_id: "decision_db_20240116"
  destination: "CLAUDE.md"
  section: "Architecture Decisions"
  timestamp: "2024-01-16T10:00:00Z"
write_operation:
  strategy: append
  bytes_written: 256
  lines_added: 8
  lines_modified: 0
verification:
  write_confirmed: true
  content_present: true
  structure_valid: true
metadata:
  source: "conversation:conv_abc123"
  related_entries: []
  expiry: null
duplicates_found: []
confidence: 1.0
evidence_anchors:
  - "CLAUDE.md:45-52"
  - "verification:re-read:success"
assumptions:
  - "CLAUDE.md is the correct location for architecture decisions"
  - "No conflicting database decisions exist"
```

**What was written to CLAUDE.md:**
```markdown
### Architecture Decisions

#### Database: PostgreSQL [2024-01-16]

**Decision:** Use PostgreSQL for all persistent storage

**Rationale:** Strong ACID guarantees, mature ecosystem, team familiarity

**Context:** Evaluated PostgreSQL, MySQL, and MongoDB for new backend service

**Constraints:**
- Must support complex queries
- Team has PostgreSQL experience
```

---

### Example 2: Detecting Duplicate

**Input:**
```yaml
content:
  pattern: "Wrap external API errors with domain-specific error types"
  rationale: "Prevents leaking implementation details"
destination: CLAUDE.md
section: "Patterns"
content_type: pattern
```

**Output:**
```yaml
persisted:
  content_type: pattern
  content_id: null
  destination: "CLAUDE.md"
  section: "Patterns"
  timestamp: "2024-01-16T11:00:00Z"
write_operation:
  strategy: append
  bytes_written: 0
  lines_added: 0
  lines_modified: 0
verification:
  write_confirmed: false
  content_present: true
  structure_valid: true
metadata:
  source: "conversation:conv_def456"
  related_entries: ["pattern_err_001"]
  expiry: null
duplicates_found:
  - existing_id: "pattern_err_001"
    similarity: 0.95
    action_taken: skipped
confidence: 0.9
evidence_anchors:
  - "CLAUDE.md:134"
assumptions:
  - "High similarity indicates same pattern"
  - "Skipping to avoid duplicate"
next_actions:
  - "Consider updating existing pattern if new rationale is better"
```

---

### Example 3: Merging with Existing Content

**Input:**
```yaml
content:
  fact: "API rate limit is 1000 requests per minute"
  source: "API documentation v2.3"
destination: "docs/api-notes.md"
section: "Rate Limits"
content_type: fact
merge_strategy: merge
```

**Output:**
```yaml
persisted:
  content_type: fact
  content_id: "fact_rate_limit_20240116"
  destination: "docs/api-notes.md"
  section: "Rate Limits"
  timestamp: "2024-01-16T12:00:00Z"
write_operation:
  strategy: merge
  bytes_written: 64
  lines_added: 1
  lines_modified: 1
verification:
  write_confirmed: true
  content_present: true
  structure_valid: true
metadata:
  source: "API documentation v2.3"
  related_entries: ["fact_rate_limit_20231201"]
  expiry: "2024-07-16"
duplicates_found:
  - existing_id: "fact_rate_limit_20231201"
    similarity: 0.8
    action_taken: merged
confidence: 1.0
evidence_anchors:
  - "docs/api-notes.md:23"
  - "source:API documentation v2.3"
assumptions:
  - "New rate limit supersedes previous"
  - "6-month expiry for review"
```

## Verification

- [ ] Content validated for appropriateness (no secrets/PII)
- [ ] Destination file exists or can be created
- [ ] Write operation completed without error
- [ ] Content present in destination after write
- [ ] File structure/formatting preserved

**Verification tools:** Read (to verify write), Edit (to perform write)

## Safety Constraints

- `mutation`: true
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: medium

**Capability-specific rules:**
- NEVER persist credentials, API keys, or secrets
- NEVER persist PII without explicit user consent
- Validate content does not contain executable code
- Preserve existing file structure and formatting
- Create backup before replacing existing content
- Stop if destination is a system or configuration file

## Composition Patterns

**Commonly follows:**
- `decide` - Persist decisions for future reference
- `discover` - Save discovered patterns or relationships
- `recall` - Update existing memories with new context
- `summarize` - Save summary as durable knowledge

**Commonly precedes:**
- `recall` - Persisted content becomes available for recall
- `verify` - Verify persisted content is correct
- `audit` - Record what was persisted for compliance

**Anti-patterns:**
- Never persist without checking for duplicates
- Never persist contradictory information without flagging
- Never persist to files outside project scope without approval
- Avoid persisting ephemeral/temporary information

**Workflow references:**
- Pairs with `recall` for the remember/recall cycle
- Final step in many learning workflows
