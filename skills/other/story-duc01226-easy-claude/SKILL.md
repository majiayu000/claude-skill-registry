---
name: story
version: 1.2.0
description: "[Project Management] Break PBIs into user stories using vertical slicing, SPIDR splitting, and INVEST criteria. Use when creating user stories from PBIs, slicing features, or breaking down requirements. Triggers on keywords like "user story", "create stories", "slice pbi", "story breakdown", "vertical slice", "split story"."
allowed-tools: Read, Write, Edit, Grep, Glob, TaskCreate, AskUserQuestion
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Break Product Backlog Items into implementable user stories using vertical slicing, SPIDR splitting, and INVEST criteria.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference docs:
>
> - `project-structure-reference.md` -- project patterns and structure
> - `.claude/skills/shared/estimation-framework.md` -- story points, complexity, splitting rules
> - `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
> - `docs/test-specs/` — Test specifications by module (read existing TCs for related features; include test story/acceptance criteria for new stories)
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Read PBI** — Load PBI artifact, acceptance criteria, and domain context
2. **Vertical Slice** — Identify end-to-end slices of functionality
3. **SPIDR Split** — Apply Spike/Paths/Interfaces/Data/Rules splitting if effort >5
4. **Write Stories** — INVEST-validated stories with min 3 GIVEN/WHEN/THEN scenarios each
5. **Validate** — Interview user to confirm slicing, acceptance criteria, and effort estimates

**Key Rules:**

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

- Stories with SP >8 MUST be split; >5 SHOULD be split (see estimation-framework.md)
- All stories MUST include `story_points` and `complexity` fields

## Greenfield Mode

> **Auto-detected:** If no existing codebase is found (no code directories like `src/`, `app/`, `lib/`, `server/`, `packages/`, etc., no manifest files like `package.json`/`*.sln`/`go.mod`, no populated `project-config.json`), this skill switches to greenfield mode automatically. Planning artifacts (docs/, plans/, .claude/) don't count — the project must have actual code directories with content.

**When greenfield is detected:**

1. Generate **foundation PBIs** instead of feature stories: infrastructure setup, project scaffold, CI/CD pipeline, first feature vertical slice
2. Add dependency ordering: infrastructure stories BEFORE feature stories
3. Skip "MUST READ project-structure-reference.md" (won't exist)
4. Include setup stories: dev environment, build tooling, deployment pipeline, monitoring
5. Priority order: infra → scaffold → first feature → remaining features
6. **[CRITICAL] Architecture Scaffolding Story:** FIRST story = "Architecture Scaffolding" — all OOP/SOLID base abstract classes, generic interfaces, infrastructure abstractions per chosen tech stack. AI self-investigates what base classes the project needs. All feature stories depend on this.
7. Scaffolding acceptance criteria: all base classes compile/type-check, DI/IoC registrations resolve, smoke test passes
8. **UI System Foundation Story:** If the project has a frontend, generate a "UI System Foundation" story (Sprint 0) with these sub-stories:

    | Sub-Story                                                                 | SP  | Priority  | Depends On               |
    | ------------------------------------------------------------------------- | --- | --------- | ------------------------ |
    | "Set up design token system"                                              | 2-3 | Must Have | Architecture Scaffolding |
    | "Create base layout and responsive grid"                                  | 2-3 | Must Have | Design tokens            |
    | "Create core UI components (loading, error, empty, toast, button, input)" | 3-5 | Must Have | Design tokens + layout   |

    **Dependency rule:** All UI feature stories MUST depend on "UI System Foundation" stories.

- Each story needs happy path, edge case, and error scenario (minimum)
- Use correct project domain vocabulary when available (check project docs for terminology)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# User Story Creation

Break Product Backlog Items into implementable user stories using vertical slicing and SPIDR patterns.

---

## Step 0: Locate Active Plan (if in workflow)

If running within a workflow (big-feature, greenfield-init, etc.):

1. **Search for active plan** — Glob `plans/*/plan.md` sorted by modification time, or check `TaskList` for plan context
2. **Read `plan.md`** — understand project scope, architecture decisions, domain model, implementation plan
3. **Read existing research** — `{plan-dir}/research/*.md` and `{plan-dir}/phase-*.md` for domain model, tech stack, architecture
4. **Read `docs/project-reference/domain-entities-reference.md`** (if exists) — understand existing domain entities for accurate story scoping
5. Use plan context to inform story slicing (architecture decisions affect how stories are split)

---

## When to Use

- PBI ready for story breakdown
- Feature needs vertical slicing
- Creating sprint-ready work items
- Story too large (effort >8)

---

## Quick Reference

### Workflow

1. Read PBI artifact and acceptance criteria
2. **Load domain context** (if project module detected)
3. Identify vertical slices (end-to-end functionality)
4. **Apply SPIDR splitting** if stories too large
5. Apply INVEST criteria to each story
6. Create user stories with GIVEN/WHEN/THEN (min 3 scenarios)
7. Save to `team-artifacts/pbis/stories/`
8. **Validate stories** (MANDATORY) - Interview user to confirm slicing, acceptance criteria, and effort
9. Suggest next: `/test-spec` or `/design-spec`

### Output

- **Path:** `team-artifacts/pbis/stories/{YYMMDD}-us-{pbi-slug}.md`
- **Format:** Single file with all stories (use ## headers per story)

---

## Project Domain Context Loading

When slicing domain-related PBIs, automatically load business context.

### Step 1: Detect Module

**From PBI frontmatter:**

1. Check `module` field
2. If missing, detect from keywords (ref: `.claude/skills/shared/module-detection-keywords.md`)

### Step 2: Load Feature Context

```
Glob("docs/business-features/{module}/detailed-features/*.md")
```

1. Read module README (first 200 lines)
2. Identify related feature from `related_features` list
3. Extract existing business rules (BR-{MOD}-XXX)
4. Note entity names from feature docs

### Step 3: Apply Domain Vocabulary

Read `docs/project-config.json` modules[] and `docs/business-features/` to detect domain vocabulary per module. Use entity names from feature docs — avoid ambiguous synonyms.

### Step 4: Include in Story

```markdown
## Domain Context

**Module:** {detected module}
**Feature:** {related feature}
**Entities:** {Entity1}, {Entity2}
**Business Rules:** BR-{MOD}-XXX (from feature docs)
```

---

## INVEST Criteria

| Criterion       | Definition                       | Validation Question                  |
| --------------- | -------------------------------- | ------------------------------------ |
| **I**ndependent | No dependencies on other stories | Can this be developed in any order?  |
| **N**egotiable  | Details can change               | Is the "how" open for discussion?    |
| **V**aluable    | Delivers user value              | Does user get observable benefit?    |
| **E**stimable   | Can estimate story points        | Can team size this? (Fibonacci 1-21) |
| **S**mall       | Completable in sprint            | SP ≤8? (prefer ≤5)                   |
| **T**estable    | Clear acceptance criteria        | Can we write pass/fail tests?        |

---

## SPIDR Splitting Checklist

**When to apply:** Story SP >8 MUST split. SP >5 SHOULD split. SP 13 = SHOULD split into 2-3 stories. SP 21 = MUST split (epic-level).

| Pattern        | Question                     | Split Strategy                            |
| -------------- | ---------------------------- | ----------------------------------------- |
| **S**pike      | Unknown complexity?          | Create research spike first, then stories |
| **P**aths      | Multiple workflow branches?  | One story per path/choice                 |
| **I**nterfaces | Multiple UIs or APIs?        | One story per interface                   |
| **D**ata       | Multiple data formats/types? | One story per data variation              |
| **R**ules      | Multiple business rules?     | One story per rule variation              |

### Splitting Examples

**Paths:** "User can pay by card OR PayPal" → Story A: Card payment, Story B: PayPal payment

**Data:** "Import CSV, Excel, JSON" → Story A: CSV import, Story B: Excel import, Story C: JSON import

**Rules:** "Different approval flows by amount" → Story A: <$1000 auto-approve, Story B: >$1000 manager approval

### Size Validation

```
SP 1-5:   ✅ Good size
SP 6-8:   ⚠️ Consider splitting (apply SPIDR)
SP 13:    ❌ SHOULD split into 2-3 stories
SP 21:    ❌ MUST split — epic-level, not sprint-ready
```

---

## Scenario Templates

### Minimum 3 scenarios per story:

### 1. Happy Path (Positive)

```gherkin
Scenario: User successfully {completes action}
  Given {user has required permissions/state}
  And {required data exists}
  When user {performs valid action}
  Then {primary expected outcome}
  And {secondary verification if needed}
```

### 2. Edge Case (Boundary)

```gherkin
Scenario: System handles {boundary condition}
  Given {edge state: empty list, max items, zero value}
  When user {attempts action at boundary}
  Then {appropriate handling: pagination, warning, default}
```

### 3. Error Case (Negative)

```gherkin
Scenario: System prevents {invalid action}
  Given {precondition}
  When user {provides invalid input OR unauthorized action}
  Then error message "{specific error message}"
  And {system remains in valid state}
  And {no partial changes saved}
```

### 4. Authorization (MANDATORY per story)

```gherkin
Scenario: Unauthorized user cannot {perform action}
  Given user has role {unauthorized role}
  When user attempts to {action}
  Then system rejects with "Forbidden" or "Unauthorized"
  And no data is modified
```

> Ref: `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md` §1

### Additional Scenario Types

**Performance:** Response time under load
**Concurrency:** Simultaneous user actions
**Integration:** External service unavailable

---

## Story Artifact Template

````markdown
---
id: US-{YYMMDD}-{NNN}
parent_pbi: '{PBI-ID}'
title: '{Brief story title}'
persona: '{User persona}'
priority: P1 | P2 | P3
story_points: 1 | 2 | 3 | 5 | 8 | 13
complexity: Low | Medium | High | Very High
sprint: 0 | 1 | 2 | ...
status: draft | ready | in_progress | done
module: '{ServiceA | ServiceB | ServiceC | ServiceD}'
---

# User Stories for {PBI Title}

## Story 1: {Title}

**As a** {user role}
**I want** {goal}
**So that** {benefit}

### Acceptance Criteria

#### Scenario 1: {Happy path title}

```gherkin
Given {context}
When {action}
Then {outcome}
```
````

#### Scenario 2: {Edge case title}

```gherkin
Given {edge state}
When {action}
Then {handling}
```

#### Scenario 3: {Error case title}

```gherkin
Given {context}
When {invalid action}
Then error "{message}"
```

---

## Story 2: {Title}

{Repeat structure...}

---

## Out of Scope

- {Explicitly excluded items}

## Story Dependencies

| Story    | Depends On | Type         | Reason                            |
| -------- | ---------- | ------------ | --------------------------------- |
| US-{NNN} | -          | independent  | First slice, no dependencies      |
| US-{NNN} | US-{NNN}   | must-after   | Needs entity/API from prior story |
| US-{NNN} | US-{NNN}   | can-parallel | Independent feature slice         |
| US-{NNN} | US-{NNN}   | blocked-by   | Requires external service/infra   |

## Domain Context

**Module:** {module}
**Related Feature:** {feature doc path}
**Entities:** {Entity1}, {Entity2}
**Business Rules:** {BR-XXX references}

## UI Wireframe

> **MUST READ:** `.claude/skills/shared/ui-wireframe-protocol.md`

### Layout

{ASCII wireframe showing this story's UI slice — see ui-wireframe-protocol.md}

### Components

- **{ComponentName}** — {behavior for this story} _(tier: common | domain-shared | page/app)_

> Classify per **Component Hierarchy** in `ui-wireframe-protocol.md` — search existing libs before proposing new components.

### Interaction Flow

1. User {action} on {component}
2. System {response/feedback}
3. UI updates to show {result}

### States

| State   | Behavior                   |
| ------- | -------------------------- |
| Default | {what user sees initially} |
| Loading | {spinner/skeleton}         |
| Empty   | {empty state message}      |
| Error   | {error handling}           |

> If backend-only: `## UI Wireframe` → `N/A — Backend-only change. No UI affected.`

## Technical Notes

- {Implementation hints if needed}

## Validation Summary

**Validated:** {date}

### Confirmed

- {decision}: {user choice}

### Action Items

- [ ] {follow-up if any}

````

---

## Sprint 0 / Foundation Stories (Production Readiness)

> Ref: `.claude/skills/shared/scaffold-production-readiness-protocol.md`

When the PBI includes a "Production Readiness Concerns" table with "Required" items, automatically generate Sprint 0 / foundation stories for each concern:

| PBI Concern | Story Title | Story Points | Priority |
|-------------|-------------|-------------|----------|
| Code linting/analyzers = Required | "Set up code linting and formatting" | 1-2 SP | Must Have |
| Error handling setup = Required | "Set up error handling foundation" | 2-3 SP | Must Have |
| Loading indicators = Required | "Set up loading indicator infrastructure" | 1-2 SP | Must Have |
| Docker integration = Required | "Set up Docker development environment" | 2-3 SP | Must Have |
| CI/CD quality gates = Required | "Set up CI/CD quality gates" | 2-3 SP | Must Have |
| Seed data = Required | "Set up seed data / data seeder" | 2-3 SP | Must Have |
| Data migration = Required | "Create data migration for schema changes" | 1-3 SP | Must Have |

> Ref: `.claude/skills/shared/cross-cutting-quality-concerns-protocol.md` §2, §5

### Rules
- Foundation stories MUST be completed before feature stories begin
- Mark as `sprint: 0` or `sprint: foundation` in story metadata
- Each foundation story references the specific protocol section for implementation guidance
- If PBI concern = "Existing", skip story generation (already set up)
- If PBI concern = "No", skip story generation (explicitly opted out)

---

## Anti-Patterns to Avoid

| Anti-Pattern       | Problem                                           | Correct Approach                              |
| ------------------ | ------------------------------------------------- | --------------------------------------------- |
| Horizontal slicing | "Backend story" + "Frontend story" = delays value | Vertical slice: thin end-to-end functionality |
| Single scenario    | Missing edge/error cases                          | Minimum 3 scenarios: happy, edge, error       |
| Vague criteria     | "Fast", "user-friendly" untestable                | Quantify: "< 200ms", "≤ 3 clicks"             |
| Solution-speak     | "Use Redis cache" constrains team                 | Outcome: "Results return within 200ms"        |
| Effort >8          | Won't fit sprint, hard to estimate                | Apply SPIDR, split until ≤8                   |
| No error scenario  | Missing negative test coverage                    | Always include invalid input handling         |
| Generic persona    | "As a user" too vague                             | Specific: "As a hiring manager"               |

---

## Key Rules

- **Every story set MUST include a Story Dependencies table** — with types: `must-after`, `can-parallel`, `blocked-by`, `independent`. This enables `/prioritize` and `/plan` to respect implementation ordering.
- **SPIDR splits MUST include dependency chains** — When splitting a story, declare which split stories depend on others.
- **No orphan stories** — Every story must appear in the dependency table, even if independent.

## Quality Checklist

Before completing user stories:

- [ ] Each story follows "As a... I want... So that..." format
- [ ] SPIDR splitting applied (effort ≤8, prefer ≤5)
- [ ] At least 3 scenarios per story: happy, edge, error
- [ ] All scenarios use GIVEN/WHEN/THEN format
- [ ] Effort estimated in Fibonacci (1, 2, 3, 5, 8)
- [ ] Stories independent (can develop in any order)
- [ ] Out of scope explicitly listed
- [ ] Story Dependencies table included with all stories listed
- [ ] Dependency types correct (must-after, can-parallel, blocked-by, independent)
- [ ] Parent PBI linked in frontmatter
- [ ] Domain vocabulary used correctly (if the project)
- [ ] Authorization scenario included per story (unauthorized access rejection)
- [ ] Seed data story included if PBI has seed data requirements
- [ ] Data migration story included if PBI has schema changes
- [ ] Validation interview completed

---

## Validation Step (MANDATORY)

After creating user stories, validate with user.

### Question Categories

| Category         | Example Question                                    |
| ---------------- | --------------------------------------------------- |
| **Slicing**      | "Are the story slices independent enough?"          |
| **Size**         | "Any story >8 effort that needs further splitting?" |
| **Scenarios**    | "Any acceptance criteria missing for edge cases?"   |
| **Dependencies** | "Are there hidden dependencies between stories?"    |
| **Scope**        | "Should anything be explicitly excluded?"           |

### Process

1. Generate 2-4 questions focused on slicing quality, scenarios, and dependencies
2. Use `AskUserQuestion` tool to interview
3. Document in story artifact under `## Validation Summary`
4. Update stories based on answers (split if needed)

**This step is NOT optional.**

---

## Related

| Type           | Reference                                   |
| -------------- | ------------------------------------------- |
| **Role Skill** | `business-analyst`                          |
| **Command**    | `/story`                                    |
| **Input**      | `/refine` output (PBI)                      |
| **Next Steps** | `/test-spec`, `/design-spec`, `/prioritize` |

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## MANDATORY: Systematic Task Breakdown for Stories

**MANDATORY IMPORTANT MUST** break down ALL stories into small, systematic todo tasks using `TaskCreate` BEFORE starting implementation. Each story MUST have its own set of tasks that cover:

1. **Read & understand story** — Load story artifact, acceptance criteria, domain context
2. **Identify vertical slice layers** — Backend entity/command/query, frontend component/store/API, integration points
3. **Create implementation subtasks per layer** — One task per file or logical unit (entity, command handler, DTO, component, service, test)
4. **Include spec tasks** — Each story MUST have corresponding test specifications (unit, integration, or E2E as appropriate)
5. **Include validation task** — Verify story against acceptance criteria GIVEN/WHEN/THEN after implementation
6. **Include review task** — Final quality check per story

### Task Naming Convention

```

[Story US-{ID}] {Layer}: {Description}

```

Example for a "Create Goal" story:
```

[Story US-001] Entity: Create Goal entity with validation rules
[Story US-001] Command: CreateGoalCommand + Handler
[Story US-001] DTO: GoalDto with mapping
[Story US-001] API: POST /api/goals endpoint
[Story US-001] Component: GoalCreateFormComponent
[Story US-001] Store: GoalVmStore with create action
[Story US-001] Test: Integration test for CreateGoalCommand
[Story US-001] Test: E2E test for goal creation flow
[Story US-001] Review: Verify against AC scenarios

```

**Why:** Without systematic task breakdown, stories become monolithic — leading to missed edge cases, incomplete specs, and context loss during implementation.

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:
- **"/tdd-spec (Recommended)"** — Generate test specifications from stories
- **"/plan-validate"** — If stories need validation against plan
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
````
