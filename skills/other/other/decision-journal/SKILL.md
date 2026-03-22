---
name: vibe-decision-journal
description: Extracts and records architectural decisions from diffs, conversation context, and explicit choices. Supports automatic extraction from staged changes, deduplication against prior decisions, and persistent ADR-format logging with spec traceability.
user-invocable: true
---

# vibe-decision-journal

Decisions happen whether you document them or not. This skill makes sure they don't vanish into git history.

## When to Use This Skill

- After making any significant design, architecture, or behavioral choice
- Before committing — extract implicit decisions from staged diffs
- When you realize "we keep coming back to this question"
- After a session where multiple design choices were made without explicit recording

## When NOT to Use This Skill

- Trivial implementation choices (variable naming, formatting, import order)
- Decisions already captured and reviewed
- Temporary/reversible choices (which test to run first)

## Modes

### Mode 1: Automatic Extraction (from staged diffs)

Use when committing or when the user says "what decisions did we make?"

1. **Read the staged diff**:
   ```
   git diff --cached
   ```

2. **Analyze for implicit decisions** — Look for changes that represent choices:
   - New abstractions, patterns, or data structures introduced
   - API contracts defined or changed
   - Caching/storage/retry strategies chosen
   - Error handling approaches selected
   - Behavioral changes (not just refactors)
   - Configuration or default values set

3. **Filter out non-decisions**:
   - Process/workflow choices ("commit now", "run tests")
   - Tooling setup ("install package X")
   - Pure refactors with no behavioral change
   - Diagnostic observations ("X causes Y")
   - Trivial changes (formatting, imports, variable renames)

4. **Deduplicate against existing decisions**:
   - Read existing decisions from `docs/decisions/` or project decision log
   - Skip exact matches (same question + same decision)
   - Flag potential conflicts (same topic, different conclusion) — present both to user
   - If a new decision countermands an old one, mark the old one as `Superseded by: [new decision]`

5. **Present each extracted decision** to the user for review using `AskUserQuestion`:
   - **Accept** — record as-is
   - **Accept with edits** — user refines the wording
   - **Not a decision** — discard (it was a refactor, not a choice)
   - **Already captured** — skip

### Mode 2: Explicit Recording (manual)

Use when the user explicitly states a decision.

1. **Capture the decision** directly from the conversation.

### Mode 3: Session Sweep

Use at end of session or when user says "what did we decide this session?"

1. **Review the work done this session** — files changed, features built, bugs fixed
2. **Extract decisions** from the pattern of changes (not just the latest diff)
3. **Present consolidated list** for review

## Decision Format

```markdown
## DEC-[NNNN]: [Short title]
**Date**: [Today]
**Status**: Accepted | Superseded | Rejected
**Supersedes**: DEC-[NNNN] (if applicable)

### Context
[1-2 sentences: what situation prompted this decision]

### Decision
[What was decided. Be specific enough to reconstruct the choice.]

### Alternatives Considered
1. [Alternative A] — Rejected because [reason]

### Consequences
- [What this enables or constrains going forward]

### Affected Files
- [path/to/file.ext]

### Spec Sections (if applicable)
- [Which spec sections this decision affects]
```

## Storage

Decisions are stored in `docs/decisions/decisions.jsonl` (append-only, one JSON object per line):

```json
{
  "id": "DEC-0001",
  "title": "Use Redis for session caching",
  "status": "accepted",
  "date": "2026-03-07",
  "context": "Need sub-10ms session lookups at 10k req/s",
  "decision": "Use Redis with 24h TTL for session data",
  "alternatives": ["In-memory dict (no persistence)", "DynamoDB (too expensive at scale)"],
  "consequences": ["Adds Redis as infrastructure dependency", "Enables horizontal scaling"],
  "affected_files": ["src/cache.py", "config/redis.yml"],
  "spec_sections": ["## Session Management"],
  "supersedes": null,
  "extracted_from": "diff"
}
```

Also render a human-readable markdown version in `docs/decisions/` as `DEC-NNNN-[slug].md`.

**ID assignment**: Read existing decisions, find the highest DEC-NNNN, increment by 1.

## Deduplication Rules

When extracting decisions automatically:

1. **Exact match**: Same question/topic AND same conclusion → skip
2. **Same topic, different conclusion**: Present both to user — ask if this supersedes the prior decision
3. **Semantic overlap**: If two extracted decisions from the same diff describe the same choice in different words, merge into one and present the clearer version

## Output Format

### Decisions Extracted: [N]

| # | Decision | Source | Status |
|---|----------|--------|--------|
| 1 | Use Redis for session caching | diff: src/cache.py | Accepted |
| 2 | 24h TTL for all cached data | diff: config/redis.yml | Accepted |
| 3 | Retry with exponential backoff | explicit | Already captured (DEC-0012) |

### New Decisions Recorded
- DEC-0045: Use Redis for session caching
- DEC-0046: 24h TTL for all cached data

### Superseded Decisions
- DEC-0008: "Use in-memory caching" → Superseded by DEC-0045
