---
name: faion-writing-design-docs
user-invocable: false
description: "SDD Framework: Creates, edits, or updates design.md with technical implementation. Use when user asks to create design, edit design, update design document, write technical design. Triggers on \"design.md\", \"design document\", \"technical design\"."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# SDD: Writing Design Documents

**Communication with user: User's language. Design content: English.**

---

## SDD Framework Overview

This skill is part of the **Spec-Driven Development (SDD)** framework.

### SDD Philosophy

**"Intent is the source of truth"** — specification is the main artifact, code is just its implementation.

### SDD Workflow

1. **SPECIFICATION** → faion-writing-specifications → spec.md (approved)
2. **DESIGN** ← YOU ARE HERE → Read spec + constitution → Research codebase → Write design.md
3. **TASK CREATION** → `faion-make-tasks` skill → TASK_*.md
4. **EXECUTION** → /faion-execute-task, /faion-do-all-tasks → Code + Tests

### SDD Directory Structure

```
aidocs/sdd/
├── CLAUDE.md                          # SDD overview
├── SDD_WORKFLOW.md                    # Detailed workflow
├── SPEC_TEMPLATE.md                   # spec.md template
├── DESIGN_TEMPLATE.md                 # design.md template ← use this!
├── CONSTITUTION_TEMPLATE.md           # constitution.md template
├── TASK_EXECUTION.md                  # Task execution process
└── {project}/                         # epass, billing, etc.
    ├── constitution.md                # Project principles ← read!
    └── features/
        └── {feature-name}/            # kebab-case
            ├── spec.md                # WHAT and WHY ← read!
            ├── design.md              # HOW ← creating here
            └── tasks/                 # Tasks
                ├── todo/
                ├── in_progress/
                └── done/
```

### Key SDD Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `constitution.md` | Project principles (WHAT) | READ before design |
| `contracts.md` | API contracts (HOW interfaces) | READ for API features |
| `spec.md` | WHAT and WHY | READ, must be approved |
| `design.md` | HOW to implement | CREATING with this skill |
| `TASK_*.md` | Atomic tasks | Created after design |

**contracts.md** is the single source of truth for all APIs. For features with API endpoints, design.md MUST reference contracts.md, not redefine endpoints.

---

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create design.md for a feature
- Edit/update/change/modify existing design document
- Write technical design based on spec
- Add architecture decisions to design

**Trigger phrases:** "create design", "edit design", "update design.md", "write design document"

---

## Purpose

Creates design.md for a feature based on:
1. Approved spec.md
2. Codebase analysis
3. Project constitution

## Input

- `feature_path` - path to feature directory (contains spec.md)

Or:
- `project` - project name
- `feature` - feature name

## Prerequisites

Before starting, verify:

```bash
SDD_BASE="aidocs/sdd"

# 1. spec.md exists with status approved
cat ${SDD_BASE}/{project}/features/{feature}/spec.md | grep -A1 "Status"

# 2. constitution.md exists
cat ${SDD_BASE}/{project}/constitution.md
```

**Required files:**
1. `spec.md` exists with status `approved`
2. Project `constitution.md` exists at `aidocs/sdd/{project}/constitution.md`
3. Project `contracts.md` exists at `aidocs/sdd/{project}/contracts.md` (for API features)

**If constitution.md doesn't exist:** Use skill `faion-writing-constitutions` to create it first.
**If contracts.md doesn't exist:** Use agent `faion-api-designer-agent` with MODE=init to create it.

## Workflow

### Phase 1: Read Specification

Read spec.md completely and extract:
- Problem Statement
- User Stories
- Functional Requirements
- API Contract (if present)
- Data Model (if present)
- Out of Scope

### Phase 2: Read Constitution

Read project principles from constitution.md and extract:
- Architecture patterns
- Code standards
- Testing requirements

### Phase 2.5: Read API Contracts (if API feature)

Read contracts.md and extract:
- Relevant endpoint definitions
- Request/response schemas
- Auth requirements
- Error format standard

**IMPORTANT:** Do NOT redefine API endpoints in design.md. Reference contracts.md instead:
```markdown
## API Endpoints

This feature implements endpoints from [contracts.md](../../contracts.md):
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
```

### Phase 3: Research Codebase

Use Grep and Glob tools to find related code:
- Similar models in `epass/app/applications/`
- Similar services (services.py files)
- Similar views (views.py files)
- Existing patterns

Determine:
- Which components can be reused
- Which patterns are in use
- Where to place new code

### Phase 4: Architecture Decisions

For each key decision:
1. Define context - what problem are we solving
2. List options - minimum 2 alternatives
3. Choose solution - which and why
4. Document rationale - reasoning behind choice

Typical decisions include:
- Business logic placement (new service vs existing)
- Model structure (new vs extend existing)
- Pattern selection
- Error handling approach

### Phase 5: Define Technical Approach

Define:
1. **Components** - new components, interactions, diagrams if complex
2. **Data Flow** - data path through system, validation points, error handling
3. **Files** - CREATE and MODIFY lists with scope

### Phase 6: Define Testing Strategy

Based on constitution:
1. Unit tests - isolated testing targets
2. Integration tests - flow coverage
3. Test data - required fixtures

### Phase 7: Identify Risks

For each risk document:
- Risk description
- Impact (High/Medium/Low)
- Mitigation strategy

### Phase 8: Review with User

Present key decisions:
1. Architecture Decisions - agreement check
2. Technical Approach - better alternatives
3. Risks - completeness check

### Phase 9: Agent Review

Before saving, call `faion-design-reviewer-agent` agent:

```
Task tool:
  subagent_type: "faion-design-reviewer-agent"
  prompt: "Review design for {project}/{feature}"
```

The agent checks:
- FR coverage (all requirements addressed)
- AD structure (context, options, rationale)
- Constitution compliance
- Files list completeness
- Technical correctness

If issues found → fix and re-review.
If approved → proceed to save.

### Phase 10: Save Design

Save design.md to feature directory: `{feature_path}/design.md`

## Architecture Decision Template

```
### AD-{N}: {Decision Name}

**Context:**
{Problem being solved and relevant context}

**Options:**
- **A: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}
- **B: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}

**Decision:** {Chosen solution}

**Rationale:** {Why this solution, influencing factors}

**Failed Attempts:** {Optional - approaches tried and rejected during analysis}
```

## Files Section Format

```
### Files

app/applications/{app}/models.py           # MODIFY - add {Model}
app/applications/{app}/services.py         # MODIFY - add {Service}
app/applications/{app}/views.py            # MODIFY - add {ViewSet}
app/applications/{app}/serializers.py      # MODIFY - add {Serializer}
app/applications/{app}/tests/test_{x}.py   # CREATE - tests for {x}
```

## Failed Attempts Section

Document approaches that were considered but rejected:

```
### Failed Attempts

1. **{Approach Name}** - {Why it was rejected}
2. **{Approach Name}** - {Why it was rejected}
```

This section helps future developers understand why certain paths were not taken.

## Output

File `design.md` at:
```
aidocs/sdd/{project}/features/{feature}/design.md
```

**Next step:** After approving design.md → use `faion-make-tasks` skill (via `/faion-net` → create tasks)

## Checklist Before Completion

- All FR from spec.md covered
- Architecture Decisions have rationale
- Files list is complete
- Testing strategy defined
- Risks identified
- Follows constitution
- API endpoints reference contracts.md (not redefined)
- User approved

## Sources

- Project spec.md
- Project constitution.md
- Project contracts.md (for API features)
- Template: `templates/DESIGN_TEMPLATE.md` (in this skill directory)
