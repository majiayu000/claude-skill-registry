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

```
Feature: {NNN}-{slug}
Branch: feature/{NNN}-{slug} (current: {actual-branch})
Status: Phase {N} - {phase-name} ({completed}/{total} tasks)
Next task: T{NNN} - {task-description}

Ready to continue work on this feature.
```

**Important:** Do NOT provide a detailed summary of the documents - they are already loaded into context. Confirm what was loaded and show the status summary only.
