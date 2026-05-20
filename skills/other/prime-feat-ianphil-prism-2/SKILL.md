---
name: prime-feat
description: This skill should be used when the user asks to "load feature context", "resume feature work", "prime feature N", "continue feature N", or wants to load all planning artifacts for a specific feature number.
---

# Prime Feature Context

Load all planning artifacts and context for feature {{feature_number}}.

## Artifact Locations

1. Find the feature folder: check `backlog/plans/{{feature_number}}-*/` first, then `backlog/plans/_completed/{{feature_number}}-*/`
2. Read all planning documents:
   - analysis.md
   - spec.md
   - research.md
   - plan.md
   - data-model.md
   - tasks.md
   - contracts/ (all files)
3. Read spec tests: `specs/tests/{{feature_number}}-*.md`
4. Check git branch status for `feature/{{feature_number}}-*`

## Workflow

1. Check `backlog/plans/` first for in-progress features, then `backlog/plans/_completed/` for completed ones
2. Use `ls backlog/plans/ backlog/plans/_completed/` to find the folder matching `{{feature_number}}-*`
3. Once found, extract the full feature ID (e.g., `001-mcp-integration`) and path
4. Read all files in `{feature-path}/`:
   - Start with `analysis.md`, `spec.md`, `plan.md` (core docs)
   - Then `data-model.md`, `tasks.md`, `research.md`
   - Finally list and read files in `contracts/` directory
5. Read `specs/tests/{feature-id}.md` if it exists
6. Run `git status` and `git branch --show-current` to check current branch
7. If not on the feature branch, suggest: `git checkout feature/{feature-id}`
8. Analyze `tasks.md` and summarize:
   - Total task count
   - Completed count (checked boxes)
   - Current phase based on task completion
   - Next uncompleted task

## Output Summary

Present a concise status report in this format:

```
┌─────────────────────────────────────────────────────────────┐
│ Feature {NNN}-{slug}                                        │
├─────────────────────────────────────────────────────────────┤
│ Branch: feature/{NNN}-{slug} ✓ (or ✗ if not on branch)     │
│ Progress: {completed}/{total} tasks ({percent}%)            │
├─────────────────────────────────────────────────────────────┤
│ Phase Progress:                                             │
│   Phase 1: {name} ████████████ {done}/{total} ✓            │
│   Phase 2: {name} ██████░░░░░░ {done}/{total} ← current    │
│   Phase 3: {name} ░░░░░░░░░░░░ {done}/{total}              │
│   ...                                                       │
├─────────────────────────────────────────────────────────────┤
│ Recently Completed:                                         │
│   • T{N} - {description}                                    │
│   • T{N} - {description}                                    │
├─────────────────────────────────────────────────────────────┤
│ Next Up:                                                    │
│   → T{N} - {description}  ← START HERE                      │
│     T{N} - {description}                                    │
│     T{N} - {description}                                    │
└─────────────────────────────────────────────────────────────┘
```

### Report Guidelines

1. **Phase Progress**: Show all phases with a visual progress bar (█ for done, ░ for remaining)
2. **Recently Completed**: Show last 2-3 completed tasks from the current phase
3. **Next Up**: Show next 3 uncompleted tasks, marking the first with "← START HERE"
4. **Keep it scannable**: Use consistent formatting, avoid prose

### Progress Bar Calculation

For each phase, calculate: `done / total * 12` filled blocks (█), remainder as empty (░)

**Important:** Do NOT provide a detailed summary of the documents - they are already loaded into context. The report replaces verbose explanations.
