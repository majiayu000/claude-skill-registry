---
name: openspec-workflow
description: Use OpenSpec for specification-driven development. Apply when planning features, implementing changes, or managing project deliverables.
---

# OpenSpec Workflow - Specification-Driven Development

OpenSpec ensures AI agents build what was planned, not what they invented.

## Directory Structure

```
project/
└── openspec/
    ├── specs/           # Source of truth (what IS built)
    ├── changes/         # Proposals & WIP (what SHOULD change)
    ├── ideas/           # Quick-capture for later
    └── project.md       # Project conventions
```

## The Three-Stage Workflow

### Stage 1: Proposal
Create a change proposal before implementing anything significant.

```
openspec/changes/add-feature-x/
├── proposal.md     # What and why
├── tasks.md        # Numbered implementation steps
├── design.md       # Technical approach
└── specs/          # Delta specs (what will change)
```

### Stage 2: Implementation
Work through tasks.md sequentially. Keep specs in sync with code.

### Stage 3: Archive
When complete: `openspec archive <change-id>`
Specs merge to source of truth. Change moves to archive.

## CLI Commands

```bash
# List all changes
openspec list

# Show specific change details
openspec show <change-id>

# Validate a change
openspec validate <change-id> --strict

# Archive completed change
openspec archive <change-id> --yes

# List specs
openspec spec list --long
```

## Creating a Proposal

**proposal.md format:**
```markdown
# Feature Name

## Summary
One paragraph: what this change does.

## Motivation
Why we need this. What problem it solves.

## Scope
- What's included
- What's explicitly NOT included

## Dependencies
- Other changes this depends on
- External requirements
```

**tasks.md format:**
```markdown
# Implementation Tasks

## Phase 1: Foundation
- [ ] Task 1.1: Description
- [ ] Task 1.2: Description

## Phase 2: Core Implementation
- [ ] Task 2.1: Description
...
```

## Rules

1. **Proposal before code** - For anything non-trivial, write proposal.md first
2. **Tasks are sequential** - Complete in order unless explicitly parallel
3. **Validate before archive** - `openspec validate --strict` must pass
4. **Specs are truth** - Code follows specs, not vice versa
5. **Ideas are cheap** - Capture in ideas/ freely, promote to changes/ when ready

## When to Use OpenSpec

**YES - Use OpenSpec for:**
- New features (more than a few files)
- Architectural changes
- Multi-step implementations
- Anything that needs review

**NO - Skip OpenSpec for:**
- Bug fixes (unless complex)
- Typo corrections
- Single-file changes
- Exploratory work

## Integration with megg

OpenSpec tracks WHAT gets built.
megg tracks WHY decisions were made.

Use both:
- OpenSpec for implementation specs
- megg for decision rationale and context

## Validation Checklist

Before marking a change complete:
- [ ] All tasks.md items checked
- [ ] `openspec validate --strict` passes
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Specs match implementation
