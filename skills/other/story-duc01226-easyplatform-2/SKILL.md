---
name: story
version: 1.1.1
description: "[Project Management] Break PBIs into user stories using vertical slicing, SPIDR splitting, and INVEST criteria. Use when creating user stories from PBIs, slicing features, or breaking down requirements. Triggers on keywords like "user story", "create stories", "slice pbi", "story breakdown", "vertical slice", "split story"."
allowed-tools: Read, Write, Edit, Grep, Glob, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Break Product Backlog Items into implementable user stories using vertical slicing, SPIDR splitting, and INVEST criteria.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Read PBI** — Load PBI artifact, acceptance criteria, and domain context
2. **Vertical Slice** — Identify end-to-end slices of functionality
3. **SPIDR Split** — Apply Spike/Paths/Interfaces/Data/Rules splitting if effort >5
4. **Write Stories** — INVEST-validated stories with min 3 GIVEN/WHEN/THEN scenarios each
5. **Validate** — Interview user to confirm slicing, acceptance criteria, and effort estimates

**Key Rules:**

- Stories with effort >8 MUST be split; >5 SHOULD be split
- Each story needs happy path, edge case, and error scenario (minimum)
- Use correct project domain vocabulary (Candidate not Applicant, Goal not Objective)

# User Story Creation

Break Product Backlog Items into implementable user stories using vertical slicing and SPIDR patterns.

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

| Module   | Correct Term   | Avoid               |
| -------- | -------------- | ------------------- |
| ServiceA | Candidate      | Applicant           |
| ServiceA | JobApplication | Application         |
| ServiceB | Goal           | Objective           |
| ServiceB | Employee       | User, Staff         |
| ServiceC | Survey         | Form, Questionnaire |

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

| Criterion       | Definition                       | Validation Question                 |
| --------------- | -------------------------------- | ----------------------------------- |
| **I**ndependent | No dependencies on other stories | Can this be developed in any order? |
| **N**egotiable  | Details can change               | Is the "how" open for discussion?   |
| **V**aluable    | Delivers user value              | Does user get observable benefit?   |
| **E**stimable   | Can estimate effort              | Can team size this?                 |
| **S**mall       | Completable in sprint            | Effort ≤8? (prefer ≤5)              |
| **T**estable    | Clear acceptance criteria        | Can we write pass/fail tests?       |

---

## SPIDR Splitting Checklist

**When to apply:** Story effort >8 MUST split. Effort >5 SHOULD split.

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
Effort 1-5:  ✅ Good size
Effort 6-8:  ⚠️ Consider splitting (apply SPIDR)
Effort >8:   ❌ MUST split (apply SPIDR, repeat until ≤8)
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

### Additional Scenario Types

**Security:** Unauthorized access attempt
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
effort: 1 | 2 | 3 | 5 | 8
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

## Dependencies

- **Upstream:** {What must be done first}
- **Downstream:** {What depends on this}

## Domain Context

**Module:** {module}
**Related Feature:** {feature doc path}
**Entities:** {Entity1}, {Entity2}
**Business Rules:** {BR-XXX references}

## Technical Notes

- {Implementation hints if needed}

## Validation Summary

**Validated:** {date}

### Confirmed

- {decision}: {user choice}

### Action Items

- [ ] {follow-up if any}

```

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

## Quality Checklist

Before completing user stories:

- [ ] Each story follows "As a... I want... So that..." format
- [ ] SPIDR splitting applied (effort ≤8, prefer ≤5)
- [ ] At least 3 scenarios per story: happy, edge, error
- [ ] All scenarios use GIVEN/WHEN/THEN format
- [ ] Effort estimated in Fibonacci (1, 2, 3, 5, 8)
- [ ] Stories independent (can develop in any order)
- [ ] Out of scope explicitly listed
- [ ] Dependencies identified (upstream/downstream)
- [ ] Parent PBI linked in frontmatter
- [ ] Domain vocabulary used correctly (if the project)
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
```
