---
name: memory-update
description: Scan agent's session-history transcripts for save-worthy signals (corrections, preferences, decisions, references), propose and write auto-memory files with valid frontmatter and MEMORY.md entry. Use when the user says "save this to memory", "remember that", or "scan this session for memories".
---

Scan session history, surface save-worthy moments, propose → confirm → write. Never fabricate — every proposal must cite a transcript turn.

## Scope

Creates or revises memory files in the agent's memory directory. Does not delete, merge-stale, or audit existing files (that is `memory-clean`). Does not redact or sanitize (that is `memory-sanitize`).

## Path resolution

```sh
SKILL_SCRIPTS="${MEMORY_UPDATE_SKILL_SCRIPTS:-$HOME/.claude/claude/skills/memory-update/scripts}"
MEMORY_DIR=$("$SKILL_SCRIPTS/resolve-paths.sh" memory_dir)
SESSION_HISTORY_GLOB=$("$SKILL_SCRIPTS/resolve-paths.sh" session_history_glob)
```

Abort on non-zero exit. Override `MEMORY_UPDATE_SKILL_SCRIPTS` if installed outside `$HOME/.claude`. Override `MEMORY_DIR` / `SESSION_HISTORY_GLOB` env vars to target a non-Claude-Code agent's layout.

## Memory types and required sections

Read `references/MEMORY-FRONTMATTER.md` for the full schema. Key rules:

| type | Required extra sections |
|---|---|
| `feedback` | `**Why:**` and `**How to apply:**` |
| `project` | `**Why:**` and `**How to apply:**` |
| `user` | none beyond frontmatter |
| `reference` | none beyond frontmatter |

Filename: `<type>_<slug>.md`. Slug: lowercase, hyphens only, ≤ 40 chars.

## Workflow

### 1. Resolve paths (above)

### 2. Scan session history for proposals

Run `scripts/scan-session.sh "$SESSION_HISTORY_GLOB"` → JSON array:

```json
[{ "type": "feedback", "slug": "prefer-foo", "evidence_turn_ids": ["uuid-123"],
   "draft_body": "...", "draft_index_entry": "- [Title](file.md) — hook" }, ...]
```

Read `references/SIGNAL-HEURISTICS.md` to understand which turns qualify. If the user triggered the skill with an explicit instruction ("remember that X"), synthesize a proposal from that instruction directly instead of scanning.

### 3. Present proposals and wait for confirmation

Render each proposal as:

```
Proposal N — type: feedback
Evidence: turn uuid-123 ("the user said 'stop doing X'")
Draft:
  ---
  name: …
  description: …
  type: feedback
  ---
  Rule text. **Why:** … **How to apply:** …
Index entry: - [Title](file.md) — hook (N chars)

Accept / Reject / Edit?
```

Wait for explicit user response per proposal. Never write without confirmation.

### 4. Check for near-duplicates before writing

```sh
rg -l -F "<key phrase from draft>" "$MEMORY_DIR"
```

`rg` works on any directory regardless of git worktree boundaries. If a hit exists, show the existing file's content and ask whether to merge into it or create new.

### 5. Write

- Write `"$MEMORY_DIR/<type>_<slug>.md"` with frontmatter + body.
- Append (or update) one-line entry in `"$MEMORY_DIR/MEMORY.md"` (≤ 150 chars).

### 6. Verify

Read back each written file; confirm frontmatter parses as YAML (key: value lines present, no tab-indentation errors). Report which files were written and their line counts.

## Anti-patterns (never do)

- Fabricate a memory without citing a transcript turn or explicit user statement.
- Write without per-proposal user confirmation.
- Store code patterns, fix recipes, git history, or ephemeral task state.
- Create MEMORY.md entries exceeding 150 chars.
