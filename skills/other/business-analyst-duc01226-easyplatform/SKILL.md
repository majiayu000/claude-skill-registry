---
name: business-analyst
version: 1.0.0
description: "[Project Management] Assist Business Analysts with requirements refinement, user story writing, acceptance criteria in BDD format, and gap analysis. Use when creating user stories, writing acceptance criteria, analyzing requirements, or mapping business processes. Triggers on keywords like "requirements", "user story", "acceptance criteria", "BDD", "GIVEN WHEN THEN", "gap analysis", "process flow", "business rules"."
allowed-tools: Read, Write, Edit, Grep, Glob, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Refine requirements into actionable user stories with BDD acceptance criteria and business rule traceability.

**Workflow:**

1. **Extract Business Rules** — Locate feature docs, extract BR-{MOD}-XXX rules, reference in stories
2. **Investigate Entities** — Load .ai.md companion files, extract domain model and query patterns
3. **Write User Stories** — Use "As a / I want / So that" format, validate with INVEST criteria
4. **Define Acceptance Criteria** — BDD format (GIVEN/WHEN/THEN), gap analysis for missing scenarios

**Key Rules:**

- Always reference existing business rules from `docs/business-features/` before creating new ones
- User stories must pass INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Include entity context and related domain model in every story

# Business Analyst Assistant

Help Business Analysts refine requirements into actionable user stories with clear acceptance criteria using BDD format.

---

## Business Rules Extraction (Project Domain)

When refining domain-related PBIs, automatically extract and reference existing business rules.

### Step 1: Locate Related Feature Docs

**Dynamic Discovery:**

1. Run: `Glob("docs/business-features/{module}/detailed-features/*.md")` for feature docs
2. Or: `Glob("docs/business-features/{module}/detailed-features/**/*.md")` for nested features
3. For AI companion files: `Glob("docs/business-features/{module}/detailed-features/*.ai.md")`

From PBI frontmatter or module detection:

1. Check `module` field
2. Identify related feature from `related_features` list
3. Read discovered feature documentation

### Step 2: Extract Existing Business Rules

From feature doc "Business Rules" section:

- Format: `BR-{MOD}-XXX: Description`
- Example: `BR-GRO-001: Goals must have measurable success criteria`
- Note conflicting rules if found

### Step 3: Add to User Story

Include section:

```markdown
## Related Business Rules

**From Feature Docs:**

- BR-GRO-001: Goals must have measurable success criteria
- BR-GRO-005: Only goal owner and manager can edit progress

**New Business Rules (if applicable):**

- BR-GRO-042: {New rule description}

**Conflicts/Clarifications:**

- {Note any conflicts with existing rules}
```

### Token Budget

Target 8-12K tokens total (validated decision: prefer completeness):

- Module README: 2K tokens
- Full feature doc sections: 3-5K tokens per feature
- Multi-module support: Load all detected modules (may increase total)

---

## Entity Domain Investigation

When refining domain-related PBIs, investigate related entities using .ai.md files.

### Step 1: Load AI Companion File

```
Glob("docs/business-features/{module}/detailed-features/*.ai.md")
```

Select file matching feature from PBI context.

### Step 2: Extract Domain Model

From `## Domain Model` section:

- Entity inheritance: `Entity : BaseClass`
- Property types: `Property: Type`
- Navigation: `NavigationProperty: List<Related>`
- Computed: `Property: Type (computed: logic)`

### Step 3: Correlate with Codebase

From `## File Locations` section:

1. Read entity source file
2. Verify properties match documentation
3. Note any undocumented properties (flag for doc update)

### Step 4: Identify Query Patterns

From `## Key Expressions` section:

- Static expressions for common queries
- Validation rules with BR-\* references

### Step 5: Add to User Story

Include entity context:

```markdown
## Entity Context

**Primary:** {Entity} - {description}
**Related:** {Entity1}, {Entity2}
**Key Queries:** {ExpressionName}
**Source:** {path}
```

This ensures implementation uses correct entities and patterns.

---

## Core Capabilities

### 1. Requirements Refinement

- Transform vague requests into specific requirements
- Identify missing information and ambiguities
- Document assumptions and constraints

### 2. User Story Writing

#### Format

```
As a {user role/persona}
I want {goal/desire}
So that {benefit/value}
```

#### INVEST Criteria

- **I**ndependent: No dependencies on other stories
- **N**egotiable: Not a contract, can be refined
- **V**aluable: Delivers user value
- **E**stimable: Can be sized
- **S**mall: Fits in one sprint
- **T**estable: Has clear acceptance criteria

### 3. Acceptance Criteria (BDD Format)

```gherkin
Scenario: {Descriptive title}
  Given {precondition/context}
    And {additional context}
  When {action/trigger}
    And {additional action}
  Then {expected outcome}
    And {additional verification}
```

**For Project Domain:**

1. Reference existing test case patterns from feature docs
2. Use TC-{MOD}-{FEATURE}-XXX format (e.g., TC-GRO-GOAL-001)
3. Include Evidence field: `file:line` format
4. Example from GoalManagement feature:
    ```
    TC-GRO-GOAL-001: Create goal with valid data
    GIVEN employee has permission to create goals
    WHEN employee submits goal form with all required fields
    THEN goal is created and appears in goal list
    Evidence: goal.service.ts:87, goal.component.ts:142
    ```

### 4. Business Rules Documentation

#### Rule Format

```
BR-{MOD}-{NNN}: {Rule name}
IF {condition}
THEN {action/result}
ELSE {alternative}
Evidence: {file}:{line}
```

### 5. Gap Analysis

- Current state vs desired state mapping
- Identify process improvements
- Document integration requirements

---

## Context Validation (Project Domain)

Before finalizing user story:

### Cross-Reference Check

- [ ] Business rules don't conflict with existing BR-{MOD}-XXX rules
- [ ] Test case format matches existing TC-{MOD}-{FEATURE}-XXX patterns
- [ ] Entity names match those in .ai.md files
- [ ] Evidence format follows file:line convention

### Documentation Links

Add to user story:

```markdown
## Reference Documentation

- Feature Doc: `docs/business-features/{module}/detailed-features/{feature}.md`
- Related Entities: `docs/business-features/{module}/*.ai.md`
- Existing Test Cases: See feature doc Section 15 (Test Cases & Scenarios)
```

If conflicts found, note in "Unresolved Questions" section.

---

## Workflow Integration

### Refining Ideas to PBIs

When user runs `/refine {idea-file}`:

1. Read idea artifact
2. **Check for module field** in frontmatter
3. **Load business feature context** if domain-related
4. Extract requirements
5. **Extract existing BRs** from feature docs
6. Identify acceptance criteria using TC patterns
7. Create PBI with GIVEN/WHEN/THEN format
8. Save to `team-artifacts/pbis/`

### Creating User Stories

When user runs `/story {pbi-file}`:

1. Read PBI
2. Break into vertical slices
3. Write user stories with AC
4. Ensure INVEST criteria met
5. **Include related BRs**
6. Save to `team-artifacts/pbis/stories/`

---

## Templates

### User Story Template

````markdown
---
id: US-{YYMMDD}-{NNN}
parent_pbi: '{PBI-ID}'
persona: '{Persona name}'
priority: P1 | P2 | P3
effort: 1 | 2 | 3 | 5 | 8 | 13
status: draft | ready | in_progress | done
module: '' # Project module (if applicable)
---

# User Story

**As a** {user role}
**I want** {goal}
**So that** {benefit}

## Acceptance Criteria

### Scenario 1: {Happy path title}

```gherkin
Given {context}
When {action}
Then {outcome}
```
````

### Scenario 2: {Edge case title}

```gherkin
Given {context}
When {action}
Then {outcome}
```

### Scenario 3: {Error case title}

```gherkin
Given {context}
When {invalid action}
Then {error handling}
```

## Related Business Rules

<!-- Auto-extracted from feature docs -->

- BR-{MOD}-XXX: {Description}

## Out of Scope

- {Explicitly excluded item}

## Notes

- {Implementation guidance}

```

---

## Elicitation Techniques

### 5 Whys
1. Why? → {answer}
2. Why? → {answer}
3. Why? → {answer}
4. Why? → {answer}
5. Why? → {root cause}

### SMART Criteria for Requirements
- **S**pecific: Clear and unambiguous
- **M**easurable: Can verify completion
- **A**chievable: Technically feasible
- **R**elevant: Aligned with business goals
- **T**ime-bound: Has a deadline or sprint

---

## Output Conventions

### File Naming
```

{YYMMDD}-ba-story-{slug}.md
{YYMMDD}-ba-requirements-{slug}.md

````

### Requirement IDs
- Functional: `FR-{MOD}-{NNN}` (e.g., FR-GROW-001)
- Non-Functional: `NFR-{MOD}-{NNN}`
- Business Rule: `BR-{MOD}-{NNN}`

### AC IDs
- `AC-{NNN}` per story/PBI

### Test Case IDs (Project)
- `TC-{MOD}-{FEATURE}-{NNN}` (e.g., TC-GRO-GOAL-001)

---

## Quality Checklist

Before completing BA artifacts:
- [ ] User story follows "As a... I want... So that..." format
- [ ] At least 3 scenarios: happy path, edge case, error case
- [ ] All scenarios use GIVEN/WHEN/THEN
- [ ] Out of scope explicitly listed
- [ ] Story meets INVEST criteria
- [ ] No solution-speak in requirements (only outcomes)
- [ ] **Existing BRs referenced** (if domain-related)
- [ ] **TC format matches feature docs** (if domain-related)
- [ ] **Entity names use domain vocabulary**

---

## Post-Refinement Validation (MANDATORY)

**Every refinement must end with a validation interview.**

After completing user story or PBI refinement, conduct validation to:

1. Surface hidden assumptions
2. Confirm critical decisions
3. Identify potential concerns
4. Brainstorm with user on alternatives

### Validation Interview Process

Use `AskUserQuestion` tool with 3-5 questions:

| Category        | Example Questions                       |
| --------------- | --------------------------------------- |
| Assumptions     | "We assume X. Is this correct?"         |
| Scope           | "Should Y be explicitly excluded?"      |
| Dependencies    | "Does this depend on Z being ready?"    |
| Edge Cases      | "What happens when data is empty/null?" |
| Business Impact | "Will this affect existing reports?"    |

### Document Validation Results

Add to user story/PBI:

```markdown
## Validation Summary

**Validated:** {date}

### Confirmed Decisions
- {decision}: {user choice}

### Concerns Raised
- {concern}: {resolution}

### Action Items
- [ ] {follow-up if any}
````

### When to Flag for Stakeholder Review

- Decision impacts other teams
- Scope change requested
- Technical risk identified
- Business rule conflict detected

**This step is NOT optional - always validate before marking refinement complete.**

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
