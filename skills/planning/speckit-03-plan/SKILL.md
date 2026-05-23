---
name: speckit-03-plan
description: Create technical implementation plan from feature specification
---

# Spec-Kit Plan

Execute the implementation planning workflow using the plan template to generate design artifacts.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Constitution Loading (REQUIRED)

Before ANY action, load and internalize the project constitution:

1. Read constitution:
   ```bash
   cat .specify/memory/constitution.md 2>/dev/null || echo "NO_CONSTITUTION"
   ```

2. If file doesn't exist:
   ```
   ERROR: Project constitution not found at .specify/memory/constitution.md

   STOP - Cannot proceed without constitution.
   Run /speckit-00-constitution first to define project principles.
   ```

3. Parse all principles, constraints, and governance rules.

4. **Extract Enforcement Rules**:
   - Find all lines containing "MUST", "MUST NOT", "SHALL", "SHALL NOT", "REQUIRED", "NON-NEGOTIABLE"
   - Build an enforcement checklist from these rules
   - Example extraction:
     ```
     CONSTITUTION ENFORCEMENT RULES:
     [MUST] Use TDD - write tests before implementation
     [MUST NOT] Use external dependencies without justification
     [REQUIRED] All code must have error handling
     ```

5. **Validation commitment:** Every output will be validated against each principle before being written.

6. **Hard Gate Declaration**: State explicitly:
   ```
   CONSTITUTION GATE ACTIVE
   Extracted X enforcement rules
   ANY violation will HALT planning with explanation
   ```

## Prerequisites Check

1. Run setup script (choose based on platform):

   **Unix/macOS/Linux:**
   ```bash
   .specify/scripts/bash/setup-plan.sh --json
   ```

   **Windows (PowerShell):**
   ```powershell
   pwsh .specify/scripts/powershell/setup-plan.ps1 -Json
   ```

2. Parse JSON for:
   - `FEATURE_SPEC` - path to spec.md
   - `IMPL_PLAN` - path to plan.md
   - `SPECS_DIR` - feature directory
   - `BRANCH` - current branch name

3. If error or missing spec.md:
   ```
   ERROR: spec.md not found in feature directory.
   Run /speckit-01-specify first to create the feature specification.
   ```

## Smart Validation

**BEFORE proceeding to planning, perform semantic validation:**

### Spec Quality Gate

Read the spec.md and validate:

1. **Requirement Count Check**:
   - Count functional requirements (FR-XXX patterns)
   - WARN if fewer than 3 requirements: "Spec may be underspecified"
   - HALT if 0 requirements: "Cannot plan without requirements"

2. **Measurable Success Criteria Check**:
   - Scan Success Criteria section for numeric values, percentages, or time measurements
   - WARN if no measurable criteria found: "Success criteria should include metrics (e.g., 'under 3 seconds', '95% uptime')"

3. **Unresolved Clarification Check**:
   - Search for `[NEEDS CLARIFICATION]` markers
   - If found, list each one and ask: "Resolve these before planning, or proceed with assumptions?"
   - If user says proceed, document assumptions explicitly in plan.md

4. **User Story Coverage Check**:
   - Verify each user story has at least one acceptance scenario
   - WARN if any story lacks scenarios: "User Story X has no acceptance criteria"

5. **Cross-Reference Validation**:
   - Check that requirements reference user stories (or vice versa)
   - WARN if orphan requirements exist: "FR-XXX not linked to any user story"

### Quality Score Report

Calculate and display:
```
╭─────────────────────────────────────────────╮
│  SPEC QUALITY REPORT                        │
├─────────────────────────────────────────────┤
│  Requirements:     X found (min: 3)    [✓/✗]│
│  Success Criteria: X found (min: 3)    [✓/✗]│
│  User Stories:     X found (min: 1)    [✓/✗]│
│  Measurable:       X criteria have metrics  │
│  Clarifications:   X unresolved             │
│  Coverage:         X% requirements linked   │
├─────────────────────────────────────────────┤
│  OVERALL SCORE: X/10                        │
│  STATUS: [READY/NEEDS WORK]                 │
╰─────────────────────────────────────────────╯
```

**If score < 6**: Recommend running `/speckit-02-clarify` first
**If score >= 6**: Proceed with planning

## Execution Flow

### 1. Setup

- Run setup script to get paths and copy plan template
- Read `FEATURE_SPEC` and constitution
- Load `IMPL_PLAN` template

### 2. Execute Plan Workflow

Follow the structure in IMPL_PLAN template to:

1. **Fill Technical Context** (mark unknowns as "NEEDS CLARIFICATION"):
   - Language/Version
   - Primary Dependencies
   - Storage
   - Testing
   - Target Platform
   - Project Type
   - Performance Goals
   - Constraints
   - Scale/Scope

2. **Fill Constitution Check section** from constitution principles

3. **Evaluate gates** - ERROR if violations cannot be justified

### 3. Phase 0: Outline & Research

1. **Extract unknowns from Technical Context**:
   - For each NEEDS CLARIFICATION -> research task
   - For each dependency -> best practices task
   - For each integration -> patterns task

2. **Research each unknown** and document findings

3. **Consolidate findings** in `research.md`:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: `research.md` with all NEEDS CLARIFICATION resolved

### 4. Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** -> `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action -> endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Create quickstart.md** with test scenarios

4. **Agent context update** (choose based on platform):

   **Unix/macOS/Linux:**
   ```bash
   .specify/scripts/bash/update-agent-context.sh claude
   ```

   **Windows (PowerShell):**
   ```powershell
   pwsh .specify/scripts/powershell/update-agent-context.ps1 -AgentType claude
   ```

   This updates CLAUDE.md with the new technology stack.

**Output**: `data-model.md`, `/contracts/*`, `quickstart.md`, updated agent file

### 5. Constitution Check (Post-Design)

Re-evaluate the Constitution Check after design phase:

- Verify all technical decisions align with principles
- If ANY violation detected:
  - STOP immediately
  - State: "CONSTITUTION VIOLATION: [Principle Name]"
  - Explain what specifically violates the principle
  - Suggest compliant alternative approach
  - DO NOT proceed with "best effort" or workarounds

### 6. Phase Separation Validation (REQUIRED)

Before finalizing, scan the draft plan for governance content that belongs in `/speckit-00-constitution`:

**Check for violations - plan MUST NOT contain:**
- Project governance principles or "laws"
- Non-negotiable development rules (e.g., "always use TDD", "code review required")
- Quality standards that apply project-wide (e.g., "100% test coverage")
- Amendment procedures or versioning policies
- Compliance or audit requirements
- Team workflow rules (e.g., "PRs must be approved by 2 reviewers")
- Coding standards that aren't technology-specific

**Plan SHOULD contain** (these are appropriate here):
- Technology stack decisions (languages, frameworks, databases)
- Architecture patterns for THIS feature
- Implementation approach and rationale
- Data models and API contracts
- Performance targets for THIS feature
- Technology-specific best practices

**If violations found:**
```
╭─────────────────────────────────────────────────────────────────╮
│  PHASE SEPARATION VIOLATION DETECTED                           │
├─────────────────────────────────────────────────────────────────┤
│  Plan contains governance content:                             │
│  - [list each violation]                                       │
│                                                                 │
│  Governance principles belong in /speckit-00-constitution.     │
│  Plan defines HOW to implement THIS feature, not project laws. │
├─────────────────────────────────────────────────────────────────┤
│  ACTION: Moving governance content to constitution reference...│
╰─────────────────────────────────────────────────────────────────╯
```

**Auto-fix:** Replace governance statements with constitution references:
- "Always use TDD" → "Per constitution: [reference TDD principle]"
- "Code must have 100% coverage" → "Coverage target per constitution"
- "All PRs require review" → (remove - this is workflow, not implementation)

Re-validate after fixes until no violations remain.

## Output Validation (REQUIRED)

Before writing ANY artifact:

1. Review output against EACH constitutional principle
2. If ANY violation detected:
   - STOP immediately
   - State: "CONSTITUTION VIOLATION: [Principle Name]"
   - Explain: What specifically violates the principle
   - Suggest: Compliant alternative approach
3. If compliant, proceed and note: "Validated against constitution v[VERSION]"

## Key Rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
- Command ends after Phase 1 design is complete

## Report

Output:
- Branch name
- IMPL_PLAN path
- Generated artifacts list:
  - research.md
  - data-model.md
  - contracts/*
  - quickstart.md
- Agent file update status

## Semantic Diff on Re-run

**If plan.md already exists with content**, perform semantic diff before overwriting:

### 1. Detect and Parse Existing Plan

If plan.md exists and has Technical Context filled in:

1. **Extract semantic elements**:
   - Language/Version
   - Primary Dependencies
   - Storage choice
   - Project structure decisions

2. **Compare with new content**:
   ```
   ╭─────────────────────────────────────────────────────╮
   │  SEMANTIC DIFF: plan.md                             │
   ├─────────────────────────────────────────────────────┤
   │  Tech Stack:                                        │
   │    ~ Language: Python 3.11 → Python 3.12            │
   │    + Added: Redis for caching                       │
   │    - Removed: None                                  │
   │                                                     │
   │  Architecture:                                      │
   │    ~ Changed: Switched from REST to GraphQL         │
   │    + Added: Event sourcing pattern                  │
   ├─────────────────────────────────────────────────────┤
   │  DOWNSTREAM IMPACT:                                 │
   │  ⚠ tasks.md MUST be regenerated (architecture change)│
   │  ⚠ contracts/ need updates (API change)            │
   │  ⚠ data-model.md may need updates                  │
   ╰─────────────────────────────────────────────────────╯
   ```

3. **Flag breaking changes**:
   - Language change → ALL tasks affected
   - Framework change → Most tasks affected
   - Storage change → Data layer tasks affected

### 2. Automatic Downstream Invalidation

If significant changes detected:
```
WARNING: Plan changes detected that invalidate downstream artifacts.
Recommend re-running:
- /speckit-05-tasks (REQUIRED - architecture changed)
- /speckit-06-analyze (RECOMMENDED - verify consistency)
```

## Next Steps

After completing the plan:

1. **Recommended**: Run `/speckit-04-checklist` to create domain-specific quality checklists
   - Generates "unit tests for English" to validate requirements quality
   - Helps catch requirement gaps before implementation
   - Required to reach 100% before `/speckit-07-implement`

2. **Required**: Run `/speckit-05-tasks` to generate the task breakdown

Suggest to user:
```
Plan complete! Next steps:
- /speckit-04-checklist - (Recommended) Generate quality checklists for requirements validation
- /speckit-05-tasks - Generate task breakdown from plan
```
