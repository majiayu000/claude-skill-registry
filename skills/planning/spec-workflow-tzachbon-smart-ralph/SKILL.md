---
name: spec-workflow
description: This skill should be used when the user asks to "build a feature", "create a spec", "start spec-driven development", "run research phase", "generate requirements", "create design", "plan tasks", "implement spec", "check spec status", "triage a feature", "create an epic", "decompose a large feature", or needs guidance on spec-driven development workflow, phase ordering, or epic orchestration.
version: 0.2.0
---

# Spec Workflow

Spec-driven development transforms feature requests into structured specs through sequential phases, then executes them task-by-task.

## Decision Tree: Where to Start

| Situation | Command |
|-----------|---------|
| New feature, want guidance | `/ralph-specum:start <name> <goal>` |
| New feature, skip interviews | `/ralph-specum:start <name> <goal> --quick` |
| Large feature needing decomposition | `/ralph-specum:triage <goal>` |
| Resume existing spec | `/ralph-specum:start` (auto-detects) |
| Jump to specific phase | `/ralph-specum:<phase>` |

## Single Spec Flow

```
start/new -> research -> requirements -> design -> tasks -> implement
```

Each phase produces a markdown artifact in `./specs/<name>/`. Normal mode pauses for approval between phases. Quick mode runs all phases then auto-starts execution.

### Phase Commands

| Command | Agent | Output | Purpose |
|---------|-------|--------|---------|
| `/ralph-specum:research` | research-analyst | research.md | Explore feasibility, patterns, context |
| `/ralph-specum:requirements` | product-manager | requirements.md | User stories, acceptance criteria |
| `/ralph-specum:design` | architect-reviewer | design.md | Architecture, components, interfaces |
| `/ralph-specum:tasks` | task-planner | tasks.md | POC-first task breakdown |
| `/ralph-specum:implement` | spec-executor | commits | Autonomous task-by-task execution |

## Epic Flow (Multi-Spec)

For features too large for a single spec, use epic triage to decompose into dependency-aware specs.

```
triage -> [spec-1, spec-2, spec-3...] -> implement each in order
```

**Entry points:**
- `/ralph-specum:triage <goal>` -- create or resume an epic
- `/ralph-specum:start` -- detects active epics, suggests next unblocked spec

**File structure:**
```
specs/
  _epics/<epic-name>/
    epic.md            # Triage output (vision, specs, dependency graph)
    research.md        # Exploration + validation research
    .epic-state.json   # Progress tracking across specs
    .progress.md       # Learnings and decisions
```

## Management Commands

| Command | Purpose |
|---------|---------|
| `/ralph-specum:status` | Show all specs and progress |
| `/ralph-specum:switch <name>` | Change active spec |
| `/ralph-specum:cancel` | Cancel active execution |
| `/ralph-specum:refactor` | Update spec files after execution |

## Common Workflows

### Quick prototype
```bash
/ralph-specum:start my-feature "Build X" --quick
# Runs all phases automatically, starts execution
```

### Guided development
```bash
/ralph-specum:start my-feature "Build X"
# Interactive interviews at each phase
# Review and approve each artifact
/ralph-specum:implement
```

### Large feature
```bash
/ralph-specum:triage "Build entire auth system"
# Decomposes into: auth-core, auth-oauth, auth-rbac
/ralph-specum:start  # Picks next unblocked spec
```

## References

- **`references/phase-transitions.md`** -- Detailed phase flow, state transitions, quick mode behavior, phase skipping
