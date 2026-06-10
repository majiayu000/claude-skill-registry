---
name: codebase-report
description: >-
  Produce reusable technical architecture documents from codebase exploration.
  Use when onboarding, "write up what this does", architecture docs, or handoff.
practices:
- pragmatic-programmer
skill_api_version: 1
hexagonal_role: supporting
consumes: []
produces:
- codebase-report
context:
  window: fork
metadata:
  tier: knowledge
  stability: stable
  dependencies: []
user-invocable: true
---

<!-- TOC: Core | Prompt | Quick Start | Modes | Anti-Patterns | Subagent | References -->

# Codebase Report

> **Core Insight:** Understanding is ephemeral. Documents survive context compaction.

## The Problem

You explore a codebase, build a mental model, then context compacts. This skill produces **reusable artifacts** that survive.

**Differs from codebase-archaeology:** Archaeology = understanding. This = producing a document.

---

## THE EXACT PROMPT

```
Produce a Comprehensive Technical Architecture Report for this codebase:

1. Executive summary (what is it, key stats)
2. Entry points (main, routes, handlers)
3. Key types (3-5 core domain objects)
4. Data flow (input → processing → output)
5. External dependencies (DBs, APIs, critical libs)
6. Configuration (env, files, CLI, precedence)
7. Test infrastructure

Include file:line references. Output as markdown I can reference later.
```

---

## Quick Start

```bash
# Option 1: Auto-scaffold (fills what it can detect)
./scripts/scaffold-report.py /path/to/project > ARCHITECTURE.md

# Option 2: Manual exploration
cat README.md AGENTS.md 2>/dev/null | head -200
ls src/ lib/ cmd/ pkg/ 2>/dev/null
rg "fn main|func main|if __name__" --type-add 'all:*.*' -l | head -5

# Then fill template from references/TEMPLATE.md
```

---

## Report Modes

| Mode | Time | Depth | Use When |
|------|------|-------|----------|
| **Quick Scan** | 10 min | Entry + types + flow | Orientation, PR context |
| **Standard** | 30 min | Full template | Onboarding, docs |
| **Deep Dive** | 1+ hr | + diagrams, all paths | Audits, major decisions |

### Quick Scan (Minimal)

```
Quick architecture overview:
- What is it? (1 sentence)
- Entry points (list)
- 3 key types
- Main data flow (1 diagram)
Keep under 150 lines.
```

---

## Output Structure

```markdown
# [Project] - Technical Architecture Report

## Executive Summary
[What + stats in 3 lines]

## Entry Points
| Entry | Location | Purpose |
|-------|----------|---------|

## Key Types
| Type | Location | Purpose |
|------|----------|---------|

## Data Flow
[ASCII diagram + 2-sentence description]

## External Dependencies
| Dependency | Purpose | Critical? |
|------------|---------|-----------|

## Configuration
| Source | Priority | Example |
|--------|----------|---------|

## Test Infrastructure
| Type | Location | Count |
|------|----------|-------|
```

Full template: [TEMPLATE.md](references/TEMPLATE.md)

---

## Delegation Pattern

For large codebases, delegate exploration:

```
Use the codebase-explorer subagent to explore this codebase.
Return structured findings, then I'll compile the final report.
```

The subagent explores in read-only mode and returns findings in report-ready format.

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Stop at understanding | Always produce artifact |
| Vague descriptions | Include `file:line` refs |
| Skip data flow | Trace end-to-end |
| One giant report | Match depth to purpose |
| Assume knowledge persists | Write it down now |

---

## Integration

### With Hooks

Auto-generate report stub on new project:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "if echo \"$TOOL_INPUT\" | grep -q 'git clone'; then ./scripts/scaffold-report.py . > ARCHITECTURE.md; fi"
      }]
    }]
  }
}
```

### With Other Skills

| After using... | Consider... |
|----------------|-------------|
| codebase-archaeology | Producing this report to persist findings |
| multi-pass-bug-hunting | Adding "Known Issues" section |
| codebase-pattern-extraction | Noting patterns in "Notes & Gotchas" |

---

## References

| Topic | File |
|-------|------|
| Full template | [TEMPLATE.md](references/TEMPLATE.md) |
| Real examples | [EXAMPLES.md](references/EXAMPLES.md) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/scaffold-report.py` | Auto-generate report skeleton |

## Subagents

| Subagent | Purpose |
|----------|---------|
| `subagents/explorer.md` | Parallel exploration for large codebases |
