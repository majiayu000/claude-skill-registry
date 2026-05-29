---
name: knowledge
description: Extracts knowledge from Amp threads and updates project docs. Use when asked to document recent work, sync docs after an epic, summarize what changed, or update AGENTS.md from thread history.
---

# Knowledge Extraction & Documentation Sync

Extracts knowledge from Amp threads and synchronizes project documentation.

## Pipeline

```
REQUEST → THREADS → TOPICS → CODE → DOCS
```

| Phase        | Action                     | Tools                  |
| ------------ | -------------------------- | ---------------------- |
| 1. Discover  | Find threads by query/time | `find_thread`          |
| 2. Extract   | Parallel topic extraction  | `Task` + `read_thread` |
| 3. Verify    | Ground topics in code      | `gkg`, `finder`        |
| 4. Map       | Find target docs           | `Read`, `Grep`         |
| 5. Reconcile | Compare all sources        | `Oracle`               |
| 6. Apply     | Surgical updates           | `edit_file`, `mermaid` |

## Phase 1: Discover Threads

Start from user request:

```bash
# "Document last 2 weeks"
find_thread after:2w

# "Summarize auth work"
find_thread "authentication"

# "What touched the SDK?"
find_thread file:packages/sdk

# Combined
find_thread "refactor" after:1w file:packages/api
```

## Phase 2: Extract Topics

Spawn parallel `Task` agents (2-3 threads each):

```
Task prompt:
"Read threads [T-xxx, T-yyy] using read_thread.
Goal: 'Extract topics, decisions, changes'

Return JSON:
{
  'topics': [{
    'name': 'topic name',
    'threads': ['T-xxx'],
    'summary': '1-2 sentences',
    'decisions': ['...'],
    'patterns': ['...'],
    'changes': ['...']
  }]
}"
```

Collect outputs → Oracle synthesizes:

```
Oracle: "Cluster these extractions. Deduplicate.
Latest thread wins conflicts. Output unified topic list."
```

See `reference/extraction-prompts.md` for full templates.

## Phase 3: Verify Against Code

For each topic, verify claims:

```
Topic: "Added retry logic to API client"

1. finder "retry logic API client"
   → finds src/api/client.ts

2. gkg__search_codebase_definitions "retry"
   → RetryPolicy class at L45

3. gkg__get_references "RetryPolicy"
   → 12 usages across 4 files

→ Confirmed: topic matches code
```

| Claim Type        | Verification                                |
| ----------------- | ------------------------------------------- |
| "Added X"         | `mcp__gkg__search_codebase_definitions "X"` |
| "Refactored Y"    | `finder "Y"` → `mcp__gkg__get_references`   |
| "Changed pattern" | `mcp__morph_mcp__warpgrep_codebase_search`  |
| "Updated config"  | `mcp__gkg__repo_map` on config paths        |

## Phase 4: Map to Docs

Discover existing documentation:

```bash
# Structure
gkg__repo_map on docs/, .claude/skills/, */AGENTS.md

# Find existing mentions
Grep "topic keyword" docs/
Grep "RetryPolicy" AGENTS.md
```

Read target files before updating:

```
Read docs/ARCHITECTURE.md
→ Note structure, sections, voice
→ Identify insertion point
```

See `reference/doc-mapping.md` for target file conventions.

## Phase 5: Reconcile

Oracle compares three sources:

```
Oracle prompt:
"Compare:
1. TOPICS: [extracted]
2. CODE: [verified state]
3. DOCS: [current content]

Output:
- GAPS: topics not in docs
- STALE: docs ≠ code
- UPDATES: [{file, section, change, rationale}]"
```

## Phase 6: Apply Updates

**Text updates**:

```
Read target → edit_file with precise changes
Preserve structure and voice
```

**Architecture diagrams**:

```
mermaid with citations:
{
  "code": "flowchart LR\n  A[Client] --> B[RetryPolicy]",
  "citations": {
    "Client": "file:///src/api/client.ts#L10",
    "RetryPolicy": "file:///src/api/retry.ts#L45"
  }
}
```

**Parallel updates**: Multiple unrelated files → spawn Task per file.

## Concrete Example

User: "Document the auth refactor from last week"

```
1. find_thread "auth" after:7d
   → [T-abc, T-def, T-ghi]

2. Task agents extract (parallel):
   Agent A: T-abc → {topics: [{name: "JWT migration"}]}
   Agent B: T-def, T-ghi → {topics: [{name: "session cleanup"}]}

3. Oracle clusters:
   → "Auth Refactor" with sub-topics

4. Verify:
   mcp__gkg__search_codebase_definitions "JWTService"
   → confirmed at packages/auth/jwt.ts

5. Map docs:
   Grep "authentication" AGENTS.md
   → Section exists at line 45

6. Oracle reconciles:
   → Gap: JWT migration not documented
   → Update: AGENTS.md auth section

7. Apply:
   edit_file AGENTS.md add JWT details
   mermaid auth flow diagram
```

## Tool Quick Reference

| Goal                | Tool                                                   |
| ------------------- | ------------------------------------------------------ |
| Find threads        | `find_thread query\|after:Xd\|file:path`               |
| Read thread         | `read_thread` with focused goal                        |
| Parallel extraction | `Task` (spawn multiple)                                |
| Find definitions    | `mcp__gkg__search_codebase_definitions`                |
| Find references     | `mcp__gkg__get_references`                             |
| Semantic search     | `finder` or `mcp__morph_mcp__warpgrep_codebase_search` |
| Area overview       | `mcp__gkg__repo_map`                                   |
| Synthesis           | `Oracle`                                               |
| Read doc            | `Read`                                                 |
| Search docs         | `Grep`                                                 |
| Update doc          | `edit_file`                                            |
| Diagram             | `mermaid` with citations                               |

## Quality Checklist

```
- [ ] Topics verified against code (GKG)
- [ ] Existing docs read before updating
- [ ] Changes surgical, not wholesale
- [ ] Mermaid diagrams have citations
- [ ] Terminology matches existing docs
```

## Troubleshooting

**Thread not found**: Try topic keywords, widen date range

**Too many threads**: Add `file:` filter, narrow dates

**Topic ≠ code**: Code is truth; note as "planned" or "historical"

**Doc structure unclear**: Read first, match existing patterns
