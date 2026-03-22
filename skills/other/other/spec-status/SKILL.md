---
name: spec-status
description: Show pipeline overview of all specifications with status counts and stale detection
allowed-tools: Bash(find:*), Bash(grep:*), Bash(stat:*), Read, Glob
---

# Spec Status Skill

Display a pipeline overview of all specifications in the repository.

## Usage

```
/spec-status
```

## Output Format

```
Spec Pipeline:
  Draft:        2  001-valkey, 002-gpu-nodes
  Implementing: 1  003-queue
  Done:        15  (in docs/specs/done/)

Stale (>14 days unchanged):
  001-valkey (last modified: 2025-01-05)
```

## Workflow

### 1. Find Active Specs

```bash
# Find all spec.md files excluding done/ and templates/
find docs/specs -name "spec.md" \
  -not -path "*/done/*" \
  -not -path "*/templates/*" \
  -type f 2>/dev/null
```

### 2. Parse Status from Each Spec

For each spec file found:

```bash
# Extract status field from spec header
grep -oP '\*\*Status\*\*:\s*\K[^\s|]+' "$SPEC_FILE"
```

Valid statuses: `draft`, `in-review`, `approved`, `implementing`, `done`

### 3. Count Done Specs

```bash
# Count specs in done/ directory
find docs/specs/done -name "spec.md" -type f 2>/dev/null | wc -l
```

### 4. Detect Stale Specs

```bash
# Find specs not modified in 14+ days
find docs/specs -name "spec.md" \
  -not -path "*/done/*" \
  -not -path "*/templates/*" \
  -mtime +14 \
  -type f 2>/dev/null
```

### 5. Format Output

Group specs by status and display:
- **Draft**: Specs with `draft` or `in-review` status
- **Implementing**: Specs with `approved` or `implementing` status
- **Done**: Count of specs in `docs/specs/done/`
- **Stale**: Specs unchanged for 14+ days (needs attention)

## Status Categories

| Display | Spec Status Values |
|---------|-------------------|
| Draft | `draft`, `in-review` |
| Implementing | `approved`, `implementing` |
| Done | Located in `docs/specs/done/` |

## GitHub Issue Labels

This skill shows file-based status. For GitHub issue labels:

```bash
# List spec issues by label
gh issue list --label "spec:draft"
gh issue list --label "spec:implementing"
gh issue list --label "spec:done"
```

## Example Output

For a repository with:
- 2 specs in draft status
- 1 spec being implemented
- 15 archived specs
- 1 stale spec

```
╔════════════════════════════════════════════════════════════════╗
║  Spec Pipeline Status                                         ║
╚════════════════════════════════════════════════════════════════╝

  Stage          Count   Specs
  ─────────────────────────────────────────────────────────────
  Draft            2     001-valkey-caching, 002-gpu-node-pool
  Implementing     1     003-queue-composition
  Done            15     (archived in docs/specs/done/)

⚠️  Stale Specs (>14 days without changes):
  → 001-valkey-caching (last modified: 2025-01-05)
    Consider: Resume work or archive if abandoned
```

## Related Skills

- `/spec` - Create new specification
- `/clarify` - Resolve [NEEDS CLARIFICATION] markers
- `/create-pr` - Create PR (auto-references spec)
