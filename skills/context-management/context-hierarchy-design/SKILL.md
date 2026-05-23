---
name: context-hierarchy-design
description: Design memory hierarchy with progressive loading for optimal context management. Use when organizing CLAUDE.md imports, implementing just-in-time context loading, or designing priming hierarchies for agents.
allowed-tools: Read, Grep, Glob
---

# Context Hierarchy Design Skill

Design a memory hierarchy that loads context progressively based on task needs.

## Purpose

Not all context is needed all the time. A well-designed hierarchy ensures agents get exactly the context they need without bloat.

## When to Use

- Setting up a new project's context infrastructure
- Refactoring bloated CLAUDE.md files
- Creating task-specific context loading
- Optimizing agent startup time
- Scaling context for multiple task types

## The Three-Tier Memory Strategy

```text
Tier 1: CLAUDE.md (minimal, always loaded)
        |
        v
Tier 2: Priming Commands (task-specific, on-demand)
        |
        v
Tier 3: File Reads (just-in-time, as needed)
```

## Design Process

### Step 1: Audit Current State

Analyze existing context infrastructure:

1. Measure CLAUDE.md size
2. Count imports and their sizes
3. Review command coverage
4. Identify task types

```text
Checklist:
- [ ] CLAUDE.md token count
- [ ] Import count and total
- [ ] Task types identified
- [ ] Command coverage mapped
```

### Step 2: Categorize Context

For each piece of existing context, ask:

| Question | If Yes -> |
| --- | --- |
| Needed for EVERY task? | Tier 1 (CLAUDE.md) |
| Needed for task TYPE? | Tier 2 (Priming) |
| Needed for specific work? | Tier 3 (On-demand) |

### Step 3: Design Tier 1 (CLAUDE.md)

Minimal essentials only:

```markdown
# Project Name

## Context
One-sentence project description.

## Tooling
- Language: X
- Runtime: Y
- Package Manager: Z

## Key Commands
- `cmd test` - Run tests
- `cmd build` - Build project

## Critical Rules
1. Most important rule
2. Second most important
3. Third most important (max 5)
```

Target size: less than 2KB.

### Step 4: Design Tier 2 (Priming Commands)

Create commands for each task type:

| Task Type | Command | Context Loaded |
| --- | --- | --- |
| General | /prime | README, git status |
| Bug Fix | /prime-bug | Recent commits, test files |
| Feature | /prime-feature | Architecture, API patterns |
| Review | /prime-review | Style guide, PR diff |
| Docs | /prime-docs | Existing docs, API surface |

**Priming Command Template:**

```markdown
# Prime: [Task Type]

## Run
[Discovery commands for current state]

## Read
[Essential files for this task type]

## Report
[Summary prompt for understanding]
```

### Step 5: Design Tier 3 (On-Demand)

Identify files loaded during work:

| Category | Loading Strategy |
| --- | --- |
| Source files | Read specific file when editing |
| Test files | Read when running tests |
| Configs | Read when configuring |
| Dependencies | Read when debugging deps |

**Principle:** Never pre-load what can be loaded on-demand.

## Output Format

Design document structure:

```markdown
# Context Hierarchy Design: [Project]

## Tier 1: CLAUDE.md (Always Loaded)

**Target Size:** <2KB
**Content:**
- Project context (1 sentence)
- Tooling (language, runtime, PM)
- Key commands (3-5)
- Critical rules (3-5)

## Tier 2: Priming Commands (Task-Specific)

### /prime
**Purpose:** General codebase understanding
**Loads:** README, git status, project structure

### /prime-bug
**Purpose:** Bug fixing context
**Loads:** Recent commits, test patterns, error logs

### /prime-feature
**Purpose:** Feature development context
**Loads:** Architecture, API patterns, similar features

## Tier 3: On-Demand (Just-in-Time)

**Strategy:** Load during execution, not pre-emptively
- Source files: Read when editing
- Tests: Read when testing
- Configs: Read when configuring

## Migration Plan

1. [ ] Backup current CLAUDE.md
2. [ ] Create minimal CLAUDE.md
3. [ ] Create priming commands
4. [ ] Test with common task types
5. [ ] Iterate based on usage
```

## Design Patterns

### Pattern: Import Hierarchy

```text
CLAUDE.md (always)
  -> imports/core.md (always, if large)
  -> imports/tooling.md (conditional)
  -> imports/workflows.md (conditional)
```

### Pattern: Directory-Scoped Memory

```text
/project
  CLAUDE.md (project-wide)
  /frontend
    CLAUDE.md (frontend-specific)
  /backend
    CLAUDE.md (backend-specific)
```

### Pattern: Task-Type Priming

```text
/prime -> Base context
/prime-{type} -> Type-specific context
```

## Validation Criteria

After design, verify:

- [ ] CLAUDE.md under 2KB
- [ ] Every task type has priming command
- [ ] No "just in case" loading
- [ ] Progressive disclosure works
- [ ] Common workflows smooth

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Everything in CLAUDE.md | Bloat | Move to priming |
| No priming commands | Static context | Add task-type priming |
| Import everything | Wasted tokens | Conditional imports |
| Directory CLAUDE.md bloat | Compounding | Keep scoped minimal |

## Key Quote

> "Use context priming over CLAUDE.md or similar auto-loading memory files. Engineering work constantly changes, but memory files only grow."

## Cross-References

- @context-priming-patterns.md - Priming command patterns
- @rd-framework.md - Reduce unnecessary context
- @context-layers.md - What loads into context
- @minimum-context-principle.md - Include only what's necessary

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
