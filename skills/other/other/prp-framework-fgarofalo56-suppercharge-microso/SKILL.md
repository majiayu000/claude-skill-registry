---
name: prp-framework
description: "PRP (Product Requirement Prompt) methodology for one-pass implementation success. Provides context-rich development workflow with PRD creation, planning, implementation, and validation. Use when implementing features, fixing bugs, or creating comprehensive development plans. Triggers: prp, product requirement prompt, implementation plan, feature planning."
---

# PRP (Product Requirement Prompt) Framework

## What is PRP?

**PRP = PRD + curated codebase intelligence + agent/runbook**

The minimum viable packet an AI needs to ship production-ready code on the first pass.

A PRP supplies an AI coding agent with everything it needs to deliver a vertical slice of working software—no more, no less.

## How PRP Differs from Traditional PRD

A traditional PRD clarifies _what_ the product must do and _why_ customers need it, but deliberately avoids _how_ it will be built.

A PRP keeps the goal and justification sections of a PRD yet adds AI-critical layers:

- **Context**: Precise file paths, library versions, code snippet examples
- **Patterns**: Existing codebase conventions to follow
- **Validation**: Executable commands the AI can run to verify its work

---

## Core Methodology

### The PRP Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LARGE FEATURES                               │
│                                                                     │
│  1. PRD Creation (#prp-prd)                                        │
│     └─> Creates PRD with Implementation Phases                      │
│                                                                     │
│  2. Plan Creation (#prp-plan)                                       │
│     └─> Selects next phase, creates implementation plan             │
│                                                                     │
│  3. Implementation (#prp-implement)                                 │
│     └─> Executes plan with validation loops                         │
│                                                                     │
│  4. Review (#prp-review)                                            │
│     └─> Comprehensive code review                                   │
│                                                                     │
│  5. Repeat for each phase                                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       MEDIUM FEATURES                               │
│                                                                     │
│  1. Plan Creation (#prp-plan "feature description")                 │
│     └─> Creates implementation plan directly                        │
│                                                                     │
│  2. Implementation (#prp-implement)                                 │
│     └─> Executes plan with validation loops                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         BUG FIXES                                   │
│                                                                     │
│  1. Investigation (#prp-issue-investigate 123)                      │
│     └─> Analyzes issue, finds root cause                           │
│                                                                     │
│  2. Fix (#prp-issue-fix 123)                                        │
│     └─> Implements fix from investigation                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Principles

### 1. Context is King

Include ALL necessary information in the PRP:
- Documentation URLs with specific sections
- Code examples from the actual codebase
- Known gotchas and pitfalls
- File:line references for every pattern

**Anti-pattern**: Minimal context prompts that leave the AI guessing.

### 2. Validation Loops

Every PRP must include executable validation:
- Build commands
- Lint commands
- Test commands
- Integration verification

The AI should be able to run these and fix any failures.

**Anti-pattern**: PRPs without testable success criteria.

### 3. Information Dense

Use keywords and patterns from the codebase:
- Actual function names
- Real type definitions
- Existing error patterns
- Current naming conventions

**Anti-pattern**: Generic descriptions instead of specific references.

### 4. Bounded Scope

Each plan should be completable in one AI session:
- Clear start and end points
- Explicit out-of-scope items
- Dependencies listed and checked

**Anti-pattern**: Unbounded plans that grow during implementation.

---

## PRP Structure

### PRD Structure (for large features)

```markdown
# {Feature Name}

## Problem Statement
{Who has what problem, cost of not solving}

## Evidence
{Proof the problem exists}

## Proposed Solution
{What we're building and why}

## Key Hypothesis
We believe {capability} will {solve problem} for {users}.
We'll know we're right when {measurable outcome}.

## Implementation Phases
| # | Phase | Description | Status | Parallel | Depends |
|---|-------|-------------|--------|----------|---------|
| 1 | ... | ... | pending | - | - |
```

### Plan Structure (for implementation)

```markdown
# Feature: {Name}

## Summary
{What we're building}

## User Story
As a {user}, I want to {action}, so that {benefit}

## Patterns to Mirror
{Actual code snippets from codebase with file:line}

## Files to Change
| File | Action | Justification |
|------|--------|---------------|
| ... | CREATE/UPDATE | ... |

## Step-by-Step Tasks
### Task 1: {Description}
- ACTION: {what to do}
- MIRROR: {file:line to copy}
- VALIDATE: {command to run}

## Validation Commands
{Executable commands for each level}

## Acceptance Criteria
{Checkboxes for completion}
```

---

## Available Commands

| Command | Purpose | Input |
|---------|---------|-------|
| `#prp-prd` | Create PRD with phases | Feature description |
| `#prp-plan` | Create implementation plan | PRD path or description |
| `#prp-implement` | Execute plan | Plan path |
| `#prp-review` | Review code changes | Diff scope |
| `#prp-issue-investigate` | Analyze GitHub issue | Issue number |
| `#prp-issue-fix` | Fix from investigation | Issue number |
| `#prp-debug` | Root cause analysis | Problem description |

---

## Validation Levels

### Level 1: Static Analysis

**.NET/C#:**
```bash
dotnet build
dotnet format --verify-no-changes
```

**Python:**
```bash
ruff check . && mypy .
```

**TypeScript/React:**
```bash
npm run lint && npm run type-check
```

### Level 2: Unit Tests

**.NET/C#:**
```bash
dotnet test --filter "Category=Unit"
```

**Python:**
```bash
pytest tests/unit -v
```

**TypeScript/React:**
```bash
npm test -- --coverage
```

### Level 3: Full Suite

**.NET/C#:**
```bash
dotnet test && dotnet build --configuration Release
```

**Python:**
```bash
pytest && python -m build
```

**TypeScript/React:**
```bash
npm test && npm run build
```

---

## Artifacts Structure

```
PRPs/
├── prds/              # Product requirement documents
│   └── feature.prd.md
├── plans/             # Implementation plans
│   ├── feature.plan.md
│   └── completed/     # Archived completed plans
├── reports/           # Implementation reports
│   └── feature-report.md
├── issues/            # Issue investigations
│   ├── 123-investigation.md
│   └── completed/     # Archived investigations
└── templates/         # Reusable templates
    ├── prp-base.md
    └── prp-story.md
```

---

## Best Practices

### DO

- Start with codebase exploration before planning
- Include actual code snippets, not generic examples
- Define validation commands for every task
- Mark out-of-scope items explicitly
- Update PRD status after each phase

### DON'T

- Create plans without understanding existing patterns
- Skip validation steps
- Ignore the structured format
- Hardcode values that should be config
- Catch all exceptions without specific handling

---

## Success Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| First-Pass Success | > 80% | Plans implemented without replanning |
| Validation Pass Rate | > 95% | Implementations passing all checks |
| Context Completeness | 100% | All patterns documented with file:line |
| Test Coverage | > 80% | New code covered by tests |

---

## Quick Reference

### Starting a New Feature

1. Assess size: Large (needs PRD) or Medium (direct to plan)
2. Large: `#prp-prd "feature description"`
3. Medium: `#prp-plan "feature description"`
4. Review generated artifact
5. Implement: `#prp-implement {path}`

### Fixing a Bug

1. Investigate: `#prp-issue-investigate {number}`
2. Review investigation findings
3. Fix: `#prp-issue-fix {number}`
4. Create PR

### Debugging an Issue

1. Analyze: `#prp-debug "problem description"`
2. Review 5 Whys analysis
3. Use findings to create plan or fix
