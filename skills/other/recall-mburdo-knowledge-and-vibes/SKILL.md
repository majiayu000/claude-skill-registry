---
name: recall
description: Retrieve context from past sessions before implementing. Use for learned patterns, past solutions, anti-patterns, session history, or when the user mentions "recall", "memory", "history", "cass", "cm", or "what do we know about".
---

# Recall — Session Memory

Retrieve relevant history, rules, and anti-patterns from past sessions. Direct execution.

> **Design rationale:** This skill executes directly rather than spawning subagents because memory retrieval is a simple command sequence (~200 tokens), not substantial analytical work. Per Lita research: "Simple agents achieve 97% of complex system performance with 15x less code."

## When This Applies

| Signal | Action |
|--------|--------|
| Starting non-trivial task | Distilled context |
| "What do we know about X?" | Distilled context |
| "How did we do this before?" | Session search |
| Looking for patterns/anti-patterns | Distilled context |
| Stuck on a problem | Deep dive |
| User says "/recall" | Full protocol |

**Default: Retrieve context before any non-trivial implementation.**

---

## Tool Reference

### Commands
| Command | Purpose |
|---------|---------|
| `cm context "task" --json` | Distilled rules + anti-patterns |
| `cm doctor` | Health check |
| `cass search "query" --robot` | Raw session search |
| `cass view /path.jsonl --json` | View full session |
| `cass expand /path -n LINE -C 3 --json` | Expand with context |
| `cass timeline --today --json` | Today's sessions |
| `cass index --full` | Rebuild index |

### Critical Rule

**Always use `--robot` or `--json`. Never run bare `cass`.**

Bare `cass` launches a TUI that will hang AI agents.

---

## Execution Flow

Execute these steps directly. No subagents needed.

### Step 1: Distilled Context (Always Start Here)

```bash
cm context "{task_description}" --json
```

**Returns:**
- **Rules** — Distilled patterns from past sessions
- **Anti-patterns** — What NOT to do (and why)
- **Suggested searches** — Specific CASS queries for more detail
- **Historical context** — Related past work

**Example:**
```bash
cm context "implement OAuth login" --json
cm context "add new database migration" --json
cm context "refactor the payment module" --json
```

---

### Step 2: Review and Extract

From `cm context` output, extract:

| Category | What to Note |
|----------|--------------|
| **Must-follow rules** | "Always use X", "Never do Y" |
| **Anti-patterns** | Past failures to avoid |
| **Relevant sessions** | Sessions to dig into |
| **Unknowns** | Gaps that need grounding |

---

### Step 3: Deep Dive (If Needed)

If `cm context` suggests searches or you need more detail:

**Search for specific patterns:**
```bash
cass search "{pattern}" --robot --fields minimal --limit 5
```

**View a specific session:**
```bash
cass view /path/to/session.jsonl --json
```

**Expand around a match:**
```bash
cass expand /path -n {line} -C 3 --json
```

---

### Step 4: Apply Context

Before implementing:

- [ ] Rules noted and will be followed
- [ ] Anti-patterns noted and will be avoided
- [ ] Prior solutions reviewed for reuse
- [ ] Gaps identified for grounding

---

## Search Patterns

### Task-based
```bash
cm context "implement user authentication" --json
cm context "fix pagination bug" --json
cm context "add API endpoint for X" --json
```

### Pattern-based
```bash
cm context "error handling in API routes" --json
cm context "database transaction patterns" --json
cm context "form validation" --json
```

### Problem-based
```bash
cm context "timeout errors in background jobs" --json
cm context "memory leak in long-running process" --json
```

---

## CASS Search Reference

### Basic Search
```bash
cass search "query" --robot --limit 5
```

### Lean Output (fewer tokens)
```bash
cass search "query" --robot --fields minimal --limit 5
```

### With Summary
```bash
cass search "query" --robot --fields summary
```

### Token-Budgeted
```bash
cass search "query" --robot --max-tokens 2000
```

### Workspace-Specific
```bash
cass search "query" --workspace "/path/to/project" --robot
```

### By Time Range
```bash
cass search "query" --robot --since 7d
```

---

## Timeline Commands

```bash
# Today's sessions
cass timeline --today --json

# Last week
cass timeline --since 7d --json

# Recent activity
cass timeline --days 7 --json --limit 10
```

---

## Output Interpretation

### Rules (high signal)
```json
{
  "rules": [
    {"pattern": "auth", "rule": "Always use bcrypt cost >= 12"}
  ]
}
```
**Follow these.** They're distilled from successful sessions.

### Anti-patterns (high signal)
```json
{
  "antipatterns": [
    "Don't use localStorage for tokens - session abc failed"
  ]
}
```
**Avoid these.** They caused failures before.

### Suggested searches (medium signal)
```json
{
  "suggested_searches": [
    "cass search 'jwt refresh' --robot"
  ]
}
```
**Run these** if you need more detail on a specific aspect.

---

## Output Formats

```bash
--robot              # Default structured output
--robot-format jsonl # Streaming format
--robot-format compact # Minimal single-line JSON
--fields minimal     # Reduce output size
--fields summary     # Just summaries
```

---

## Query Tips

| Query Type | Example |
|------------|---------|
| Exact phrase | `"error handling"` |
| Wildcard | `auth*` |
| Multiple terms | `database migration` |
| Recent | Add `--since 7d` |

---

## Search Refinement

| If results are... | Try... |
|-------------------|--------|
| Too broad | Add specific terms, use quotes |
| Too narrow | Remove terms, try synonyms |
| Wrong domain | Add project/feature qualifiers |
| Too old | Use `--since` flag |

---

## Integration with Workflow

### At session start (via /prime)
```bash
cm context "{project_name}" --json
```

### After claiming a bead (via /advance)
```bash
cm context "{bead_title}" --json
```

### Before implementation
```bash
cm context "{what_you're_about_to_build}" --json
```

### When stuck
```bash
cm context "{problem_description}" --json
cass search "{error_message}" --robot
```

---

## Troubleshooting

### Search returns nothing
```bash
# Rebuild index
cass index --full

# Health check
cass health
cm doctor
```

### Export for reference
```bash
cass export /path/session.jsonl --format markdown -o reference.md
cass export /path/session.jsonl --format json
```

---

## When to Use /recall vs Other Tools

| Need | Use |
|------|-----|
| Learned patterns/rules | `/recall` (cm context) |
| Past session content | `/recall` (cass search) |
| Current codebase | `/explore` (warp-grep) |
| External documentation | `/ground` (exa) |
| Task graph | bv commands |

---

## Quick Reference

```bash
# Distilled context (always start here)
cm context "task description" --json

# Health check
cm doctor

# Search sessions
cass search "query" --robot --limit 5
cass search "query" --robot --fields minimal

# View session
cass view /path.jsonl --json

# Expand with context
cass expand /path -n 42 -C 3 --json

# Timeline
cass timeline --today --json
cass timeline --since 7d --json

# Index
cass index --full
```

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Run bare `cass` | TUI hangs agents | Always `--robot` or `--json` |
| Skip cm context | Miss learned patterns | Always check before non-trivial work |
| Use raw search for rules | Less relevant results | Use cm context first |
| Ignore anti-patterns | Repeat past mistakes | Note and avoid them |
| Skip suggested searches | Miss important history | Run if cm suggests them |

---

## See Also

- `/prime` — Session startup (includes recall)
- `/advance` — Bead workflow (includes recall after claiming)
- `/ground` — External documentation search
