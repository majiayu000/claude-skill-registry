---
name: refine
version: 2.2.0
description: "[Project Management] Transform ideas into Product Backlog Items using BA best practices, hypothesis validation, and domain research. Use when converting ideas to PBIs, validating problem hypotheses, adding acceptance criteria, or refining requirements. Triggers on "create pbi", "refine idea", "convert to pbi", "acceptance criteria", "make actionable", "validate hypothesis"."
allowed-tools: Read, Write, Edit, Grep, Glob, TaskCreate, WebSearch, AskUserQuestion
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

- `docs/test-specs/` — Test specifications by module (read existing TCs for related features; recommend test spec generation for new PBIs)

## Quick Summary

**Goal:** Transform raw ideas into actionable Product Backlog Items using BA best practices, hypothesis validation, and domain research.

**Workflow:**

1. **Idea Intake** — Load artifact, detect project module
2. **Domain Research** — WebSearch for market/competitor context
3. **Problem Hypothesis** — Validate problem exists before building
4. **Elicitation** — Apply BABOK techniques to extract requirements
5. **Acceptance Criteria** — Write BDD GIVEN/WHEN/THEN scenarios (min 3)
6. **Prioritization** — Apply RICE/MoSCoW scoring
7. **Validation Interview** — MANDATORY user interview to confirm assumptions
8. **PBI Generation** — Save artifact to `team-artifacts/pbis/`

**Key Rules:**

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

- Never skip hypothesis validation for new features
- Validation interview is NOT optional — always ask 3-5 questions
- Use project domain-specific vocabulary when available
- MUST include `story_points` and `complexity` in PBI output (see `.claude/skills/shared/estimation-framework.md`)
- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- **MUST READ** `.claude/skills/shared/scaffold-production-readiness-protocol.md` — for Production Readiness Concerns table in PBI output
- **MUST READ** `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md` — for Authorization, Seed Data, Data Migration concerns in PBI output

## Greenfield Mode

> **Auto-detected:** If no existing codebase is found (no code directories like `src/`, `app/`, `lib/`, `server/`, `packages/`, etc., no manifest files like `package.json`/`*.sln`/`go.mod`, no populated `project-config.json`), this skill switches to greenfield mode automatically. Planning artifacts (docs/, plans/, .claude/) don't count — the project must have actual code directories with content.

**When greenfield is detected:**

1. Skip existing backlog item refinement (no backlog exists yet)
2. Enable DDD domain modeling: bounded contexts, aggregates, entities, value objects
3. Enable constraint capture: team skills, expected scale, hosting preferences, budget — as input signals for later tech stack research
4. Use WebSearch for market research and competitor analysis
5. Output domain model artifact alongside PBI artifact
6. Increase AskUserQuestion frequency — validate domain boundaries, entity relationships, business rules
7. **[CRITICAL] DO NOT ask about tech stack during refinement.** Tech stack is a research-driven decision that comes in a dedicated phase after business analysis. Capture team skills and scale expectations as input signals only.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Idea Refinement to PBI

Transform captured ideas into actionable Product Backlog Items using Business Analysis best practices, Hypothesis-Driven Development, and domain research.

## When to Use

- Idea artifact ready for refinement
- Need to validate problem hypothesis before building
- Converting concept to implementable item
- Adding acceptance criteria to requirements
- Researching domain/market context for new features

## Workflow Overview

| Phase | Name                | Key Activity                 | Output                 |
| ----- | ------------------- | ---------------------------- | ---------------------- |
| 1     | Idea Intake         | Load artifact, detect module | Context loaded         |
| 2     | Domain Research     | WebSearch market/competitors | Research summary       |
| 3     | Problem Hypothesis  | Validate problem exists      | Confirmed hypothesis   |
| 4     | Elicitation         | Apply BABOK techniques       | Requirements extracted |
| 5     | Acceptance Criteria | Write BDD scenarios          | GIVEN/WHEN/THEN        |
| 6     | Prioritization      | Apply RICE/MoSCoW            | Priority assigned      |
| 7     | Validation          | Interview user (MANDATORY)   | Assumptions confirmed  |
| 8     | PBI Generation      | Create artifact              | PBI file saved         |

### Output

- **Path:** `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`
- **ID Pattern:** `PBI-{YYMMDD}-{NNN}`

---

## Phase 0: Locate Active Plan (if in workflow)

If running within a workflow (big-feature, greenfield-init, etc.):

1. **Search for active plan** — Glob `plans/*/plan.md` sorted by modification time, or check `TaskList` for plan context
2. **Read `plan.md`** — understand project scope, goals, architecture decisions, domain model
3. **Read existing research** — `{plan-dir}/research/*.md` for business evaluation, domain analysis, architecture design
4. **Read `docs/project-reference/domain-entities-reference.md`** (if exists) — understand existing domain entities
5. Use plan context to inform PBI refinement (don't re-ask questions already answered in prior steps)

## Phase 1: Idea Intake & Context Loading

1. Read idea artifact from path or find by ID in `team-artifacts/ideas/`
2. Extract: problem statement, value proposition, target users, scope
3. Check `module` field for project domain; if absent, detect via keywords or prompt user

---

## Phase 2: Domain Research

**Trigger:** New domain, unclear competitors, `--research` flag.
**Skip:** Internal tooling, well-understood domain, time-constrained.

Use WebSearch with domain terms. Summarize in max 3 bullets (market context, competitors, best practices).

---

## Phase 3: Problem Hypothesis Validation

Draft and validate hypothesis with user via AskUserQuestion. 42% of startups fail due to no market need - validate before building.

**Skip:** `--skip-hypothesis`, validated hypothesis exists, bug fix/tech debt.

### Problem Hypothesis Template

```markdown
**We believe** [target users/persona]
**Experience** [specific problem]
**Because** [root cause]
**We'll know this is true when** [validation metric/evidence]
```

### Value Hypothesis Template

```markdown
**We believe** [feature/solution]
**Will deliver** [value/benefit]
**To** [target users]
**We'll know we're right when** [success metric]
```

### Validation Process

1. Draft hypothesis from idea content
2. Use AskUserQuestion to validate:
    - "Is this the core problem we're solving?"
    - "Who exactly experiences this? How often?"
    - "What evidence do we have this problem exists?"
3. If validated, proceed to elicitation
4. If invalidated, return idea for clarification

---

## Phase 4: Requirements Elicitation (BABOK Core 5)

Select technique based on context:

### 1. Interviews

**When:** Deep individual insights needed, stakeholder perspectives vary
**Process:** Prepare open-ended questions (why, how, what-if) → active listening → follow-up on unexpected answers → document verbatim quotes
**Output:** Stakeholder needs, pain points, constraints

### 2. Workshops

**When:** Group consensus needed, complex requirements, multiple stakeholders
**Process:** Define agenda + timebox (90 min max) → neutral facilitator → capture all voices (round-robin, silent voting) → document decisions and dissent
**Output:** Prioritized requirements, consensus decisions

### 3. Document Analysis

**When:** Existing systems/processes to understand, regulatory requirements
**Process:** Gather artifacts (specs, manuals, code) → extract implicit requirements → note gaps → cross-reference with stakeholder input
**Output:** As-is state, compliance requirements, gaps

### 4. Observation (Job Shadowing)

**When:** Understand real workflow, users can't articulate needs
**Process:** Shadow users → note workarounds/pain points → don't interrupt → ask clarifying questions afterward
**Output:** Actual vs stated workflow, hidden requirements

### 5. Prototyping

**When:** Visual validation needed, UI/UX requirements unclear
**Process:** Start low-fidelity (sketches, wireframes) → iterate on feedback → increase fidelity as requirements stabilize → document design decisions
**Output:** Validated UI requirements, interaction patterns

---

## Phase 5: Acceptance Criteria (BDD Format)

Write GIVEN/WHEN/THEN scenarios. Minimum 3: happy path, edge case, error case.

### Standard BDD Format

```gherkin
Scenario: {Descriptive title}
  Given {precondition/context}
    And {additional context}
  When {action/trigger}
    And {additional action}
  Then {expected outcome}
    And {additional verification}
```

### Best Practices

| Practice                  | Description                       |
| ------------------------- | --------------------------------- |
| Single trigger            | "When" clause has ONE action      |
| 3 scenarios minimum       | Happy path, edge case, error case |
| No implementation details | Focus on behavior, not how        |
| Testable outcomes         | "Then" must be verifiable         |
| Stakeholder language      | No technical jargon               |

### Example Scenarios

```gherkin
Scenario: Employee creates goal with valid data
  Given employee has permission to create goals
    And employee is on the goal creation page
  When employee submits goal form with all required fields
  Then goal is created with status "Draft"
    And goal appears in employee's goal list

Scenario: Goal creation fails with missing required field
  Given employee is on the goal creation page
  When employee submits form without title
  Then validation error "Title is required" is displayed
    And goal is not created

Scenario: Manager reviews subordinate goal
  Given manager has direct reports
    And subordinate has submitted goal for review
  When manager opens goal review page
  Then subordinate's goal is visible with "Pending Review" status
```

### Project Test Case Format

- **Format:** `TC-{FEATURE}-{NNN}` (e.g., TC-GM-001)
- **Evidence:** `file:line` format
- See `business-analyst` skill for detailed patterns

---

### Phase 5.5: Testability Assessment

Use `AskUserQuestion` with 2-3 questions:

1. "Which testing approach fits this PBI?"
    - TDD-first: Write test specs before implementation (Recommended for complex features)
    - Implement-first: Build feature, then create test specs
    - Parallel: Spec and implement simultaneously

2. "What test levels are needed?"
    - Integration tests only (Recommended for backend CQRS)
    - Integration + E2E
    - Unit + Integration + E2E

For EACH acceptance criterion, generate a corresponding test case outline:

| AC                         | Test Outline                                            | Priority |
| -------------------------- | ------------------------------------------------------- | -------- |
| AC-1: User can create goal | TC: Create goal with valid data → verify persisted      | P0       |
| AC-2: Goal requires title  | TC: Create goal without title → verify validation error | P1       |

This table becomes the seed for `/tdd-spec` if the user chooses TDD-first.

Document in PBI under `## Testability Assessment`.

---

## Phase 6: Prioritization & Estimation

> **MUST READ** `.claude/skills/shared/estimation-framework.md` for story point scale and complexity definitions.

Apply RICE score or MoSCoW for priority. Estimate using **Story Points (Modified Fibonacci 1-21)** for complexity measurement.

### Story Points (Primary Estimation)

See `shared/estimation-framework.md` for SP reference table.

### Quick RICE Score

```
Score = (Reach x Impact x Confidence) / Effort

Reach: Users affected per quarter (100, 500, 1000+)
Impact: 0.25 (minimal) | 0.5 (low) | 1 (medium) | 2 (high) | 3 (massive)
Confidence: 0.5 (low) | 0.8 (medium) | 1.0 (high)
Effort: Story points (1, 2, 3, 5, 8, 13, 21)
```

### MoSCoW Categories

| Category        | Meaning                  | Action              |
| --------------- | ------------------------ | ------------------- |
| **Must Have**   | Critical, non-negotiable | Include in MVP      |
| **Should Have** | Important but not vital  | Plan for release    |
| **Could Have**  | Nice to have, low effort | If time permits     |
| **Won't Have**  | Out of scope this cycle  | Document for future |

---

## Phase 7: Validation Interview (MANDATORY)

Generate 3-5 questions covering assumptions, scope, dependencies, edge cases. Use AskUserQuestion. Document in PBI. This step is NOT optional.

### Question Categories

| Category            | Example Question                                                            |
| ------------------- | --------------------------------------------------------------------------- |
| **Assumptions**     | "We assume X is true. Correct?"                                             |
| **Scope**           | "Should Y be included or explicitly excluded?"                              |
| **Dependencies**    | "This requires Z. Is that available?"                                       |
| **Edge Cases**      | "What happens when data is empty/null?"                                     |
| **Business Impact** | "Will this affect existing reports/workflows?"                              |
| **Entities**        | "Create new entity or extend existing X?"                                   |
| **Prod Readiness**  | "Does this feature need linting, error handling, loading, or Docker setup?" |
| **Authorization**   | "Who can perform this action? What roles/permissions are needed?"           |
| **Seed Data**       | "Does this feature need reference/lookup data to function?"                 |
| **Data Migration**  | "Does this change entity schema? Is data transformation needed?"            |

### Process

1. Generate 3-5 questions from assumptions, scope, dependencies
2. Use `AskUserQuestion` tool to interview
3. Document in PBI under `## Validation Summary`
4. Update PBI based on answers

### Validation Output Format

```markdown
## Validation Summary

**Validated:** {date}

### Confirmed Decisions

- {decision}: {user choice}

### Assumptions Confirmed

- {assumption}: Confirmed/Modified

### Open Items

- [ ] {follow-up items}
```

---

## Phase 8: PBI Artifact Generation

Save to `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`.

### PBI Template

```markdown
---
id: PBI-{YYMMDD}-{NNN}
title: '{Brief descriptive title}'
module: '{ModuleName — detect from project-config.json modules[]}'
priority: Must Have | Should Have | Could Have | Won't Have
story_points: 1 | 2 | 3 | 5 | 8 | 13 | 21
complexity: Low | Medium | High | Very High
status: draft | refined | ready | in_progress | done
rice_score: { calculated }
created: '{YYYY-MM-DD}'
source_idea: '{idea artifact path or ID}'
---

# {PBI Title}

## Description

**As a** {user role}
**I want** {capability}
**So that** {business value}

## Business Value

- {Quantified benefit 1}
- {Quantified benefit 2}

## Problem Hypothesis

**We believe** {target users}
**Experience** {specific problem}
**Because** {root cause}
**We'll know this is true when** {validation metric}

## Business Rules

- BR-{MOD}-XXX: {Rule description}

## Acceptance Criteria

### AC-1: {Title}

Scenario: {Happy path}
Given {context}
When {action}
Then {outcome}

### AC-2: {Title}

Scenario: {Edge case}
Given {edge state}
When {action}
Then {handling}

### AC-3: {Title}

Scenario: {Error case}
Given {context}
When {invalid action}
Then error "{message}"

## Testability Assessment

| AC   | Test Outline       | Priority |
| ---- | ------------------ | -------- |
| AC-1 | {test description} | P0       |
| AC-2 | {test description} | P1       |

## Out of Scope

- {Explicitly excluded item 1}
- {Explicitly excluded item 2}

## Dependencies

| Dependency            | Type         | Description                    |
| --------------------- | ------------ | ------------------------------ |
| {PBI/service/feature} | must-before  | {Why this must be done first}  |
| {PBI/service/feature} | can-parallel | {Why this can run in parallel} |
| {PBI/service/feature} | blocked-by   | {What blocks this PBI}         |
| -                     | independent  | {No dependencies — first item} |

## Production Readiness Concerns

> Ref: `.claude/skills/shared/scaffold-production-readiness-protocol.md`

| Concern                | Required        | Notes                                   |
| ---------------------- | --------------- | --------------------------------------- |
| Code linting/analyzers | Yes/No/Existing | {tool preference or "scaffold default"} |
| Error handling setup   | Yes/No/Existing | {pattern: toast/inline/error-page}      |
| Loading indicators     | Yes/No/Existing | {pattern: spinner/skeleton/progress}    |
| Docker integration     | Yes/No/Existing | {scope: infra-only/full/none}           |
| CI/CD quality gates    | Yes/No/Existing | {coverage threshold, lint enforcement}  |
| Security scanning      | Yes/No/Existing | {dependency audit, SAST}                |

## Authorization & Access Control

> Ref: `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md`

| Role   | Can Create | Can Read | Can Update | Can Delete | Notes         |
| ------ | ---------- | -------- | ---------- | ---------- | ------------- |
| {Role} | ✅/❌      | ✅/❌    | ✅/❌      | ✅/❌      | {scope notes} |

**New permissions needed:** {Yes/No — list if yes}
**Multi-tenant isolation:** {Yes/No}

## Seed Data Requirements

> Ref: `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md`

| Data Type          | Description                          | Owner        | Required |
| ------------------ | ------------------------------------ | ------------ | -------- |
| Reference data     | {lookups, statuses, types}           | Application  | Yes/No   |
| Configuration data | {default settings}                   | Application  | Yes/No   |
| Test seed data     | {entities for integration tests}     | Test project | Yes/No   |
| Performance data   | {large-volume data for load testing} | Test tooling | Yes/No   |

> If no seed data needed: `N/A — no seed data required for this feature.`

## Data Migration

> Ref: `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md`

| Change                      | Type                                   | Backward Compatible | Reversible |
| --------------------------- | -------------------------------------- | ------------------- | ---------- |
| {schema change description} | Add field / Remove field / Type change | Yes/No              | Yes/No     |

> If no schema changes: `N/A — no schema changes required.`

## Domain Context

**Entities:** {Entity1}, {Entity2}
**Related Features:** {feature doc paths}

## UI Layout

> **MUST READ:** `.claude/skills/shared/ui-wireframe-protocol.md`

### Wireframe

{ASCII wireframe using box-drawing characters — see ui-wireframe-protocol.md}

**Layout:** {description with approximate proportions/dimensions}

### Components

- **{ComponentName}** — {behavior description} _(tier: common | domain-shared | page/app)_

> Classify per **Component Hierarchy** in `ui-wireframe-protocol.md` — search existing libs before proposing new components.

### States

| State   | Behavior                   |
| ------- | -------------------------- |
| Default | {what user sees initially} |
| Loading | {spinner/skeleton}         |
| Empty   | {empty state message}      |
| Error   | {error handling}           |

> If backend-only: `## UI Layout` → `N/A — Backend-only change. No UI affected.`

## Validation Summary

**Validated:** {date}

### Confirmed Decisions

- {decision}: {user choice}

### Assumptions Confirmed

- {assumption}: Confirmed/Modified

### Open Items

- [ ] {follow-up items}
```

---

## Anti-Patterns to Avoid

| Anti-Pattern                   | Better Approach                     |
| ------------------------------ | ----------------------------------- |
| Refining vague ideas           | Return to `/idea` for clarification |
| Skipping hypothesis validation | Always run Phase 3 for new features |
| Solution-first thinking        | Start with problem, not solution    |
| Generic acceptance criteria    | Use GIVEN/WHEN/THEN with specifics  |
| Ignoring domain context        | Load project docs if applicable     |
| Too large PBI (XL+)            | Break into smaller items            |
| Missing "Out of Scope"         | Explicitly list exclusions          |
| Assuming instead of asking     | Run validation interview            |

---

## Key Rules

- **Every PBI MUST include a Dependencies table** — with types: `must-before`, `can-parallel`, `blocked-by`, `independent`. This enables `/prioritize` and `/plan` to respect ordering.
- **No vague dependency descriptions** — Each dependency must specify the concrete PBI, service, or feature and WHY the relationship exists.

## Definition of Ready (INVEST)

| Criterion           | Check                        |
| ------------------- | ---------------------------- |
| **I**ndependent     | No blocking dependencies     |
| **N**egotiable      | Details can be refined       |
| **V**aluable        | Clear user/business value    |
| **E**stimable       | Team can estimate (XS-XL)    |
| **S**mall           | Single sprint                |
| **T**estable        | 3+ GIVEN/WHEN/THEN scenarios |
| Problem Validated   | Hypothesis confirmed         |
| Domain Context      | BR/entity context loaded     |
| Stakeholder Aligned | Validation interview done    |
| Prod Readiness      | Concerns documented          |

---

## Project Integration

For domain PBIs: detect module (ref: `.claude/skills/shared/module-detection-keywords.md`), extract business rules from `docs/business-features/{module}/`, load entity context from `.ai.md`. Target 8-12K tokens for feature context.

---

## Related

- **Role Skill:** `business-analyst` (detailed patterns)
- **Input:** `/idea` output
- **Next Step:** `/story`, `/tdd-spec` (Recommended for TDD), `/test-spec`, `/design-spec`
- **Prioritization:** `/prioritize`

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/story (Recommended)"** — Break PBI into implementable user stories
- **"/tdd-spec"** — If using TDD approach
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
