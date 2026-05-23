---
name: research
description: 'Deep codebase exploration with multi-angle analysis for Codex agents. Output: .agents/research/*.md. Triggers: "research", "investigate", "explore codebase", "how does X work".'
---

# $research — Codebase Exploration (Codex Tailoring)

This override captures the Codex-native execution model for research tasks.

## Codex-Native Flow

### Step 1: Setup

```bash
ao codex ensure-start 2>/dev/null || true
mkdir -p .agents/research
```

### Step 2: Check Prior Art

```bash
ao lookup --query "<topic>" --limit 5 2>/dev/null || true
ao search "<topic>" 2>/dev/null || true
```

Search all local knowledge directories by content:

```bash
for dir in research learnings knowledge patterns retros plans brainstorm; do
  grep -r -l -i "<topic>" .agents/${dir}/ 2>/dev/null
done
```

Read matched files before proceeding to avoid redundant investigation.

### Step 3: Explore the Codebase

Use `spawn_agent(agent_type="explorer", ...)` for parallel exploration branches. Each explorer gets a focused sub-question:

```
spawn_agent(
  agent_type="explorer",
  prompt="Investigate: <sub-question>. Search in <directory>. Report file:line citations."
)
```

For inline exploration (no sub-agents), use iterative retrieval:

1. Start broad with `grep -r` and `find` scoped to specific directories
2. Score results by relevance (0-1)
3. Extract new search terms from high-relevance files
4. Repeat for up to 3 refinement cycles

Discovery tiers (execute in order):
- **Code-Map**: read `docs/code-map/README.md` → find category → read feature file
- **Scoped Search**: `grep -r "<topic>" <specific-dir>/` — always scope to a directory
- **Source Code**: Read files identified by prior tiers
- **Prior Knowledge**: Search `.agents/` directories
- **External Docs**: Web search as last resort

### Step 4: Synthesize Findings

Write to `.agents/research/YYYY-MM-DD-<topic-slug>.md`:

```markdown
---
id: research-YYYY-MM-DD-<topic-slug>
type: research
date: YYYY-MM-DD
---

# Research: <Topic>

**Scope:** <what was investigated>

## Summary
<2-3 sentence overview>

## Key Files
| File | Purpose |
|------|---------|
| path/to/file | Description |

## Findings
<detailed findings with file:line citations>

## Recommendations
<next steps or actions>
```

### Step 5: Report Completion

Tell the user what was found, where it's saved, and suggest `/plan` as the next step.

## Constraints

1. Always scope searches to specific directories — never grep the full repo unscoped.
2. Cite specific `file:line` references for all claims.
3. Use `spawn_agent(agent_type="explorer")` for parallel exploration; otherwise explore inline.
4. Write output to `.agents/research/` — research must produce a file artifact.
