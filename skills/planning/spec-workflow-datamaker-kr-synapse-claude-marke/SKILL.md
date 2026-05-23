---
name: spec-workflow
description: "Orchestrates the complete specify→clarify→plan→tasks→implement workflow. Use when starting a new feature from scratch or when the user wants end-to-end guided development."
allowed-tools: Skill, Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Task, WebSearch, WebFetch
user-invocable: true
---

# Spec Workflow Agent

## Agent Type

This is an **orchestrator agent** that coordinates all speckit-helper skills to manage the
full specification-to-implementation lifecycle. Unlike worker skills that perform specific
tasks, this agent manages the entire workflow and coordinates other skills.

## Coordinated Skills

- **spec-authoring**: Specification writing, requirement structuring, quality criteria
- **task-decomposition**: Phase-based task ordering, dependency graph, traceability
- **consistency-analysis**: Cross-document gap detection, conflict identification
- **checklist-generation**: Domain-specific quality checklists, requirement testing

## Purpose

This agent orchestrates the complete specification-driven development workflow from a
feature idea to implemented code. It invokes each skill in sequence, manages transitions
between phases, and ensures quality gates are met before proceeding.

## Architecture

### Orchestrator Pattern

```
spec-workflow (Orchestrator)
├── Phase 1: Specification
│   └── Invokes spec-authoring → Generate spec.md
├── Phase 2: Clarification
│   └── AskUserQuestion → Resolve ambiguities in spec
├── Phase 3: Planning
│   └── Generate research.md, plan.md, data-model.md, contracts/
├── Phase 4: Task Decomposition
│   └── Invokes task-decomposition → Generate tasks.md
├── Phase 5: Quality Gate
│   ├── Invokes consistency-analysis → Detect issues
│   └── Invokes checklist-generation → Generate checklists
├── Phase 6: Review & Approval
│   └── Present findings, wait for user go/no-go
└── Phase 7: Implementation
    └── Execute tasks in dependency order
```

## When to Activate

This agent activates when:
- User wants to start a new feature from scratch
- User asks for "end-to-end" or "full workflow" development
- User explicitly invokes the spec-workflow agent
- User says "guide me through building this feature"

## Orchestration Workflow

### Step 1: Gather Feature Description

**Ask the user** for a feature description if not provided.

If the user provides a description directly, proceed. Otherwise:
- Use AskUserQuestion: "What feature would you like to build? Describe it in 1-3 sentences."

### Step 2: Generate Specification

**Invoke the specify command workflow**:

1. Detect project type from existing files (package.json, pyproject.toml, etc.).
2. Create `.speckit/<feature-slug>/` directory.
3. Generate `spec.md` with structured sections:
   - Feature Overview
   - User Stories with priorities (P1/P2/P3)
   - Functional Requirements (FR-001, FR-002, ...)
   - Non-Functional Requirements (NFR-001, ...)
   - Key Entities
   - Success Criteria (SC-001, ...)
   - Assumptions & Constraints
   - Open Questions
4. Generate initial `checklists/requirements.md`.

**Present to user**: Summary of generated spec with key stats (number of user stories,
requirements, entities).

### Step 3: Clarify Ambiguities

**Invoke the clarify workflow**:

1. Read the generated `spec.md`.
2. Identify unclear, ambiguous, or underspecified areas.
3. Generate up to 5 targeted clarification questions using AskUserQuestion.
4. Update `spec.md` with the user's answers.
5. Mark resolved questions in the Open Questions section.

**Decision point**: After clarification, ask the user:
- "The specification looks solid. Shall I proceed to planning, or do you want to
  refine any requirements first?"

If the user wants to refine:
- Invoke the refine workflow to apply changes.
- Return to clarification (loop up to 2 times to avoid scope creep).

### Step 4: Check Constitution

**Check for existing constitution**:

1. Look for `.speckit/constitution.md`.
2. If it exists, read it and validate the spec against stated principles.
3. If it does not exist and the project seems to have implicit standards:
   - Suggest running `/speckit-helper:constitution` first.
   - If the user declines, proceed without constitution checks.

### Step 5: Generate Plan and Tasks

**Invoke the plan workflow**:

1. Read `spec.md` and project context.
2. Generate `research.md` with technology decisions.
3. Generate `plan.md` with architecture and component design.
4. Generate `data-model.md` if entities are defined.
5. Generate API contracts in `contracts/` if endpoints are defined.
6. Generate `quickstart.md` with setup steps.

**Invoke the tasks workflow**:

1. Read all generated documents.
2. Generate `tasks.md` with phase-ordered, dependency-aware tasks.
3. Validate coverage: every requirement maps to at least one task.
4. Flag gaps with `[Gap]` markers.

**Present to user**: Task summary — number of phases, tasks per phase, estimated
complexity distribution.

### Step 6: Quality Gate

**Invoke consistency analysis**:

1. Run all 8 analysis checks across documents.
2. Classify findings by severity.
3. Generate analysis report.

**Invoke checklist generation**:

1. Auto-detect applicable domains.
2. Generate checklists for each domain.

**Present findings to user**:

```
--- Quality Gate Results ---

Analysis:
  CRITICAL: X findings
  HIGH: Y findings
  MEDIUM: Z findings
  LOW: W findings

Checklists generated: N domains, M total questions

[If CRITICAL or HIGH findings exist:]
  Recommendation: Address the following issues before implementation:
  1. [Finding description]
  2. [Finding description]

  Options:
  a) Fix these issues now (I'll update the spec and re-run quality checks)
  b) Proceed to implementation anyway (issues will be noted but not blocking)
  c) Stop here and review manually
```

**Decision point**: Wait for user decision before proceeding.

- If user chooses (a): apply fixes, re-run quality gate, and present again.
- If user chooses (b): proceed with warnings.
- If user chooses (c): stop and provide a summary of the current state.

### Step 7: Implementation

**Only proceed if the user approved implementation** in Step 6.

**Invoke the implement workflow**:

1. Execute tasks in dependency order, phase by phase.
2. For each task:
   - Read relevant spec context.
   - Implement the change.
   - Run tests if available.
   - Mark complete in `tasks.md`.
3. Report progress after each phase.
4. Handle test failures with retries.

**After each phase**, provide a checkpoint:
- "Phase N complete: X tasks done, Y remaining. Continue?"

This allows the user to pause between phases, review progress, and make adjustments.

### Step 8: Completion Summary

After all tasks are implemented (or the user stops):

```
--- Spec Workflow Complete ---

Feature:      <feature-slug>
Spec:         .speckit/<slug>/spec.md
Tasks:        X completed / Y total
Quality:      CRITICAL: 0, HIGH: 0 (or list remaining)
Phases:       N completed

Generated artifacts:
  .speckit/<slug>/spec.md
  .speckit/<slug>/research.md
  .speckit/<slug>/plan.md
  .speckit/<slug>/data-model.md
  .speckit/<slug>/tasks.md
  .speckit/<slug>/checklists/*.md

Optional next steps:
  /speckit-helper:tasks-to-issues <slug>    Create GitHub Issues
  /speckit-helper:analyze <slug>            Re-run quality analysis
```

---

## Guidelines

### Do:
- Always invoke spec-authoring skill before task-decomposition
- Present findings and wait for user approval at each decision point
- Run quality gate before starting implementation
- Provide progress checkpoints between phases
- Keep the user informed of what is happening at each step
- Respect the user's decisions (skip, proceed, stop)

### Don't:
- Skip the specification phase and jump to implementation
- Auto-proceed past quality gate findings without user approval
- Implement code before tasks.md exists
- Generate tasks before plan.md exists
- Loop clarification more than 2 times without user request
- Make assumptions about user preferences without asking
- Modify files outside the `.speckit/` directory during planning phases

## Integration with Commands

This agent orchestrates the following commands in sequence:
- `/speckit-helper:specify` — Phase 1
- `/speckit-helper:clarify` — Phase 2
- `/speckit-helper:refine` — Phase 2 (conditional)
- `/speckit-helper:constitution` — Phase 3 (conditional)
- `/speckit-helper:plan` — Phase 4
- `/speckit-helper:tasks` — Phase 4
- `/speckit-helper:analyze` — Phase 5
- `/speckit-helper:checklist` — Phase 5
- `/speckit-helper:implement` — Phase 6

## Example Interaction

**User**: "I want to add user authentication with email/password and OAuth2 support"

**spec-workflow**:

1. **Specify**: Generates `.speckit/user-authentication/spec.md` with 6 user stories,
   12 functional requirements, 4 NFRs, and 3 entities.

2. **Clarify**: Asks 4 questions:
   - "Should password reset be included?"
   - "Which OAuth2 providers? (Google, GitHub, both?)"
   - "Should session management be token-based (JWT) or cookie-based?"
   - "Is email verification required for new accounts?"

3. **Plan**: Generates research.md (comparing Passport.js vs Auth.js), plan.md
   (architecture with middleware pattern), data-model.md (User, Session, OAuthToken).

4. **Tasks**: Generates 18 tasks across 5 phases:
   - Setup (3 tasks), Foundation (4 tasks), P1 Stories (6 tasks),
     Integration (3 tasks), Finalization (2 tasks).

5. **Quality Gate**: Reports 0 CRITICAL, 1 HIGH (missing rate limiting task),
   2 MEDIUM. User approves fix → spec updated → re-analysis passes.

6. **Implement**: Executes tasks phase by phase with checkpoints.

7. **Done**: All 18 tasks complete, user prompted for GitHub Issues creation.
