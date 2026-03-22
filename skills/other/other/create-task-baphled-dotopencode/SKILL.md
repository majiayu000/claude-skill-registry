---
name: create-task
description: Create well-structured development tasks with clear acceptance criteria
category: Workflow Orchestration
---

# Skill: create-task

## What I do

I structure development tasks with clear scope, acceptance criteria, and estimation. Good tasks are completable in one session, testable, and unambiguous about what "done" means.

## When to use me

- Breaking down a feature into implementable units
- Creating GitHub issues for development work
- Writing acceptance criteria for stories
- Estimating complexity and effort
- Planning sprint or iteration work

## Core principles

1. **One session rule** - A task should be completable in 1-4 hours
2. **Testable criteria** - Every criterion can be verified with a test
3. **Unambiguous done** - No debate about whether it's finished
4. **Right-sized** - Too big = split, too small = merge
5. **Independent** - Minimise dependencies on other incomplete tasks

## Task template

```markdown
## Title: [Verb] [what] [where/context]

### Description
One paragraph explaining what needs to be done and why.

### Acceptance criteria
- [ ] [Observable behaviour when condition]
- [ ] [Observable behaviour when other condition]
- [ ] [Error case handled]
- [ ] Tests written and passing
- [ ] Coverage >= 95% on new code

### Technical notes
- Key files: [files likely to change]
- Pattern to follow: [reference existing similar code]
- Dependencies: [external libs, other tasks]

### Estimation
- Complexity: S/M/L
- Effort: [1-4 hours]
```

## Patterns & examples

**Good acceptance criteria (testable):**
```markdown
- [ ] Timeline screen displays events sorted by date descending
- [ ] Empty timeline shows "No events yet" message
- [ ] Selecting an event navigates to detail screen
- [ ] Error loading events shows error message with retry option
```

**Bad acceptance criteria (vague):**
```markdown
- [ ] Timeline works properly          # What does "properly" mean?
- [ ] Good user experience             # Subjective
- [ ] Handle all edge cases            # Which ones?
- [ ] Clean code                       # Not measurable
```

**Complexity estimation:**
```
SMALL (1-2 hours)
  Single file change, clear pattern to follow
  Example: "Add date field to event detail screen"

MEDIUM (2-4 hours)
  Multiple files, known pattern, some decisions
  Example: "Add CSV export to timeline feature"

LARGE (4+ hours → SPLIT IT)
  Multiple layers, new patterns, unknowns
  Example: "Implement full search functionality"
  → Split into: search service, search UI, search indexing
```

**Splitting large tasks:**
```
TOO BIG: "Implement timeline feature"

SPLIT INTO:
1. Create Event domain model and repository
2. Create TimelineService with list/filter
3. Create timeline list screen
4. Create timeline detail screen
5. Create browsetimeline intent (wire it together)
6. Add E2E tests for timeline workflow
```

**Creating via GitHub CLI:**
```bash
gh issue create \
  --title "Add CSV export to timeline" \
  --body "$(cat <<'EOF'
## Description
Users need to export their timeline events as CSV for
use in spreadsheets and external tools.

## Acceptance criteria
- [ ] Export button visible on timeline list screen
- [ ] CSV contains: date, title, company, description
- [ ] CSV uses UTF-8 encoding with BOM for Excel compatibility
- [ ] Empty timeline exports header row only
- [ ] Tests cover all criteria above

## Technical notes
- New ExportService in internal/service/
- Follow existing service patterns
- Use encoding/csv stdlib

## Estimation
- Complexity: M
- Effort: ~3 hours
EOF
)" \
  --label "feature,medium"
```

## Anti-patterns to avoid

- ❌ Tasks that take more than a day (split them)
- ❌ Vague acceptance criteria ("it should work well")
- ❌ No estimation (blocks planning and prioritisation)
- ❌ Missing technical context (new contributor can't start)
- ❌ Dependent tasks without explicit ordering

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Create Task.md`

## Related skills

- `create-bug` - Bug-specific task structure
- `estimation` - Deeper estimation techniques
- `bdd-workflow` - Acceptance criteria become BDD specs
- `scope-management` - Preventing scope creep in tasks
- `create-pr` - PR that implements the task
