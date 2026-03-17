---
name: refine
version: 2.1.0
description: "[Project Management] Transform ideas into Product Backlog Items using BA best practices, hypothesis validation, and domain research. Use when converting ideas to PBIs, validating problem hypotheses, adding acceptance criteria, or refining requirements. Triggers on "create pbi", "refine idea", "convert to pbi", "acceptance criteria", "make actionable", "validate hypothesis"."
allowed-tools: Read, Write, Edit, Grep, Glob, TaskCreate, WebSearch, AskUserQuestion
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

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

- Never skip hypothesis validation for new features
- Validation interview is NOT optional — always ask 3-5 questions
- Use domain-specific vocabulary (Candidate not Applicant, Employee not User)

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

- **Format:** `TC-{MOD}-{FEATURE}-XXX` (e.g., TC-GRO-GOAL-001)
- **Evidence:** `file:line` format
- See `business-analyst` skill for detailed patterns

---

## Phase 6: Prioritization & Estimation

Apply RICE score or MoSCoW. Estimate effort using T-shirt sizing (XS-XL).

### Quick RICE Score

```
Score = (Reach x Impact x Confidence) / Effort

Reach: Users affected per quarter (100, 500, 1000+)
Impact: 0.25 (minimal) | 0.5 (low) | 1 (medium) | 2 (high) | 3 (massive)
Confidence: 0.5 (low) | 0.8 (medium) | 1.0 (high)
Effort: Person-days (1, 3, 5, 10, 20)
```

### MoSCoW Categories

| Category        | Meaning                  | Action              |
| --------------- | ------------------------ | ------------------- |
| **Must Have**   | Critical, non-negotiable | Include in MVP      |
| **Should Have** | Important but not vital  | Plan for release    |
| **Could Have**  | Nice to have, low effort | If time permits     |
| **Won't Have**  | Out of scope this cycle  | Document for future |

### Effort Estimation

| T-Shirt | Days  | When to Use                        |
| ------- | ----- | ---------------------------------- |
| XS      | 0.5-1 | Config change, simple fix          |
| S       | 1-2   | Single component, clear scope      |
| M       | 3-5   | Multiple components, some unknowns |
| L       | 5-10  | Cross-cutting, integration needed  |
| XL      | 10+   | Epic - break down further          |

---

## Phase 7: Validation Interview (MANDATORY)

Generate 3-5 questions covering assumptions, scope, dependencies, edge cases. Use AskUserQuestion. Document in PBI. This step is NOT optional.

### Question Categories

| Category            | Example Question                               |
| ------------------- | ---------------------------------------------- |
| **Assumptions**     | "We assume X is true. Correct?"                |
| **Scope**           | "Should Y be included or explicitly excluded?" |
| **Dependencies**    | "This requires Z. Is that available?"          |
| **Edge Cases**      | "What happens when data is empty/null?"        |
| **Business Impact** | "Will this affect existing reports/workflows?" |
| **Entities**        | "Create new entity or extend existing X?"      |

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

Save to `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`. Template: `team-artifacts/templates/pbi-template.md`.

Required sections: Frontmatter, Description, Business Value, Problem Hypothesis, Business Rules, Acceptance Criteria, Out of Scope, Dependencies, Validation Summary.

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

---

## Project Integration

For domain PBIs: detect module (ref: `.claude/skills/shared/module-detection-keywords.md`), extract business rules from `docs/business-features/{module}/`, load entity context from `.ai.md`. Target 8-12K tokens for feature context.

---

## Related

- **Role Skill:** `business-analyst` (detailed patterns)
- **Input:** `/idea` output
- **Next Step:** `/story`, `/test-spec`, `/design-spec`
- **Prioritization:** `/prioritize`

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
