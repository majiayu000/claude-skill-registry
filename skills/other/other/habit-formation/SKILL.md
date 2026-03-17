---
name: habit-formation
description: |
  Learns from your work patterns across sessions. Detects repeated corrections,
  preferences, and workflows, then automatically applies them in future sessions.
  Use when you want Claude to remember your preferences without manually editing CLAUDE.md.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
---

# Habit Formation

Learn and apply user patterns across sessions automatically.

---

## Quick Start

1. **Work normally for one session.** The skill detects corrections, preferences, and repeated workflows in the background. No setup required.
2. **Run `/habit-formation save` at the end.** Patterns get written to `~/.claude/skills/habit-formation/state/patterns.json`. Anything observed 2+ times becomes a rule.
3. **Start a new session.** Rules load automatically from `state/rules.json`. The skill tells you how many rules it loaded, then stays out of the way.

That is it. After two sessions the skill starts paying for itself.

---

## Overview

This skill observes how you work and builds a persistent memory of your preferences, corrections, and workflows. It runs in two modes:

1. **Passive** (during session): Watches for corrections and repeated patterns silently
2. **Active** (on command): Saves, loads, or analyzes patterns on demand

---

## State Files

All state persists in `~/.claude/skills/habit-formation/state/`:

| File | Purpose |
|------|---------|
| `patterns.json` | Raw detected patterns with occurrence counts |
| `rules.json` | Promoted rules (patterns that crossed the threshold) |
| `session-log.json` | Summary of the last session |

---

## Commands

### `/habit-formation` or `/habit-formation status`

Show current session's detected patterns and active rules.

### `/habit-formation save`

End-of-session save. Does the following:

1. Summarize all patterns detected in the current session
2. Read existing `state/patterns.json` and merge (increment counts)
3. Promote any pattern with count >= threshold to `state/rules.json`
4. Show a summary of what was saved and promoted
5. Suggest CLAUDE.md additions for confirmed rules

### `/habit-formation load`

Explicitly load rules from `state/rules.json` and apply them as context.

### `/habit-formation analyze`

Run deep cross-session analysis using `scripts/analyze.py`:

```
!python ~/.claude/skills/habit-formation/scripts/analyze.py
```

Shows statistics across all conversation logs and recommendations.

### `/habit-formation reset`

Clear all state files and start fresh. Ask for confirmation first.

---

## Session Start Behavior

At the beginning of every session where this skill is active:

1. Check if `~/.claude/skills/habit-formation/state/rules.json` exists
2. If it exists and is non-empty, read it
3. Apply each rule as a behavioral constraint for the session
4. Briefly acknowledge: "Loaded X habit rules from previous sessions."

---

## Pattern Detection (During Session)

Watch for these patterns silently. Do NOT interrupt the user. Track internally.

### 1. User Corrections

**Detection**: User messages containing correction signals after an assistant response.

**Keywords** (English):
- "no", "not like that", "wrong", "actually", "instead", "I said", "I meant",
  "don't do that", "stop", "that's not what I", "please don't", "I prefer"

**Keywords** (Korean):
- "아니", "그게 아니라", "잘못", "틀렸", "다시", "이렇게 말고", "그렇게 하지 말고"

**Action**: Record what was corrected and what the user wanted instead.

**Threshold**: 2+ occurrences of similar corrections -> promote to rule.

### 2. Tone/Style Preferences

**Detection**: Explicit or implicit tone requests.

**Keywords**: "formal", "casual", "brief", "detailed", "concise", "verbose",
"shorter", "more detail", "too long", "반말", "존댓말", "짧게", "자세하게"

**Action**: Record the preference direction.

**Threshold**: 2+ times -> promote to rule.

### 3. Repeated Request Categories

**Detection**: Categorize user requests and track frequency.

**Categories**:
| Category | Signal Keywords |
|----------|----------------|
| File operations | create, write, edit, modify, rename, delete, move |
| Debugging | error, bug, fix, broken, doesn't work, why |
| Testing | test, spec, coverage, assert, expect |
| Documentation | docs, readme, comment, explain, document |
| Refactoring | refactor, clean up, simplify, extract, rename |
| Git operations | commit, push, branch, merge, rebase, PR |

**Threshold**: 5+ requests in a category -> note as primary workflow.

### 4. Tool Workflow Sequences

**Detection**: Track sequences of tool calls made by the assistant.

**Examples**:
- Read -> Edit -> Bash(test) = "edit and verify" pattern
- Grep -> Read -> Edit = "search and fix" pattern
- Read -> Read -> Read -> Write = "research then create" pattern

**Threshold**: 3+ identical sequences -> note as preferred workflow.

### 5. File Type Focus

**Detection**: Count edits per file extension.

**Threshold**: 10+ edits to same extension -> note primary language/framework.

### 6. Code Style Preferences

**Detection**: Observe formatting choices in user-provided code or user corrections to generated code.

**Tracked preferences**:

| Preference | Variants | Detection Signal |
|---|---|---|
| Quotes | single `'` vs double `"` | User rewrites string quotes, or eslint config specifies |
| Semicolons | always vs never (ASI) | User adds/removes semicolons after generation |
| Trailing commas | always vs never vs es5 | User edits trailing commas in arrays/objects |
| Import ordering | grouped (built-in, external, internal) vs alphabetical vs ungrouped | User rearranges import blocks |
| Import style | named `import { x }` vs default `import x` vs namespace `import * as x` | User corrects import form |
| Indentation | tabs vs spaces, indent width (2 or 4) | User reformats indentation |
| Bracket style | same-line `{` vs new-line `{` | User moves brackets |

**Action**: On first detection, record the preference with an example. On second detection of the same preference, promote to rule.

**Priority**: If the project has an `.editorconfig`, `.prettierrc`, or `eslint` config, read those first and pre-populate rules. User corrections still override config-file defaults.

---

## Pattern Storage Format

### patterns.json

```json
{
  "version": 1,
  "updated_at": "2026-02-10T12:00:00Z",
  "patterns": [
    {
      "id": "p001",
      "type": "correction",
      "description": "User prefers tabs over spaces",
      "count": 3,
      "first_seen": "2026-02-08",
      "last_seen": "2026-02-10",
      "examples": [
        "No, use tabs not spaces",
        "Switch to tabs please"
      ],
      "promoted": true
    }
  ]
}
```

### rules.json

```json
{
  "version": 1,
  "updated_at": "2026-02-10T12:00:00Z",
  "rules": [
    {
      "id": "r001",
      "source_pattern": "p001",
      "rule": "Always use tabs for indentation, never spaces",
      "category": "code_style",
      "promoted_at": "2026-02-10",
      "applied_count": 5
    }
  ]
}
```

### session-log.json

```json
{
  "session_date": "2026-02-10",
  "patterns_detected": 3,
  "patterns_promoted": 1,
  "corrections_observed": 2,
  "primary_activities": ["debugging", "file_operations"],
  "files_edited": {".tsx": 12, ".py": 3},
  "summary": "Focused on React component debugging. User prefers concise responses."
}
```

---

## CLAUDE.md Suggestion Format

When a rule has been confirmed (count >= threshold), suggest adding it to CLAUDE.md:

```
I noticed a recurring pattern that might be worth adding to your CLAUDE.md:

**Pattern**: [description]
**Observed**: [count] times across [N] sessions
**Suggested addition**:

### [Date] [Category]
- [Rule description]

Would you like me to add this to your CLAUDE.md's "Recent Learning" section?
```

Only suggest for high-confidence patterns. Do not spam suggestions.

---

## Thresholds

| Pattern Type | Count to Promote | Notes |
|---|---|---|
| User corrections | 2 | High signal, low threshold |
| Tone preferences | 2 | Usually explicit |
| Repeated requests | 5 | Need higher volume |
| Tool sequences | 3 | Same exact sequence |
| File type focus | 10 | Cumulative across sessions |

---

## Important Constraints

- **Never interrupt the user** to report pattern detection. Track silently.
- **Never auto-modify CLAUDE.md**. Always suggest and wait for approval.
- **Merge, don't overwrite** patterns.json on save. Increment counts for existing patterns.
- **State files are user-owned**. The user can edit or delete them at any time.
- **Privacy first**: Pattern data stays local. Never transmit or log externally.
- **Graceful degradation**: If state files don't exist or are corrupt, start fresh silently.

---

## Pattern Conflicts

Patterns can contradict each other, especially when you work across multiple projects. For example: Project A uses tabs, Project B uses spaces. Or you prefer terse commit messages in personal projects but detailed ones at work.

### Resolution: Project-Scoped State Directories

By default, state lives in `~/.claude/skills/habit-formation/state/`. To scope patterns per project, set a different state directory based on the project root:

```
~/.claude/skills/habit-formation/state/           # global (default)
~/.claude/skills/habit-formation/state/project-a/  # project-scoped
~/.claude/skills/habit-formation/state/project-b/  # project-scoped
```

**How scoping works**:

1. On session start, check if a project-scoped directory exists for the current working directory (matched by the directory name or a `.habit-scope` marker file in the project root).
2. If a project scope exists, load rules from that scope. Global rules still apply but project-scoped rules take precedence on conflict.
3. If no project scope exists, use global state only.
4. When promoting a pattern, ask: "This conflicts with a global rule. Save as project-specific override?" if a conflict is detected.

**Conflict priority** (highest wins):
1. Project-scoped rule
2. Global rule
3. Config file inference (`.prettierrc`, `.editorconfig`)

### When Two Rules Directly Contradict

If two rules within the same scope contradict (e.g., one session you said "use semicolons," another session you said "no semicolons"), do the following:

1. Flag the conflict in `/habit-formation status` output
2. Do not auto-apply either rule
3. Ask the user once: "I have conflicting rules about semicolons. Which should I keep?"
4. Demote the loser back to a pattern with count reset to 0

---

## Migration

### Between Machines

Copy the state directory to the same path on the target machine:

```bash
# On source machine
tar czf habit-state.tar.gz ~/.claude/skills/habit-formation/state/

# On target machine
tar xzf habit-state.tar.gz -C ~/
```

Rules and patterns transfer directly because they are plain JSON with no machine-specific paths.

### Between Projects

To seed a new project's state from an existing project:

```bash
cp -r ~/.claude/skills/habit-formation/state/project-a/ \
      ~/.claude/skills/habit-formation/state/project-b/
```

Then run `/habit-formation status` in the new project to review the imported rules. Remove any that do not apply (different framework, different conventions).

### Selective Export

To share only your code style rules (not workflow patterns) with a teammate:

```bash
# Extract code_style rules only
python3 -c "
import json
with open('state/rules.json') as f:
    data = json.load(f)
data['rules'] = [r for r in data['rules'] if r['category'] == 'code_style']
print(json.dumps(data, indent=2))
" > code-style-rules.json
```

Your teammate can then place this file as their `rules.json` or merge it into their existing one.

---

## References

See `references/pattern-guide.md` for detailed pattern detection algorithms and examples.
