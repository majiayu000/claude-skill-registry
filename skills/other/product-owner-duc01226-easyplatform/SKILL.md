---
name: product-owner
version: 1.0.0
description: '[Project Management] Capture ideas, manage product backlogs, apply prioritization frameworks (RICE, MoSCoW), and facilitate stakeholder communication. Triggers: product owner, backlog management, user story prioritization, product roadmap, product backlog.'
allowed-tools: Read, Write, Edit, Grep, Glob, TaskCreate, WebSearch
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

## Quick Summary

**Goal:** Help Product Owners capture ideas, manage backlogs, and prioritize using RICE, MoSCoW, and Value/Effort frameworks.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
> - `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Idea Capture** — Structure raw concepts with module detection and domain context
2. **Backlog Management** — Create/refine PBIs, track dependencies
3. **Prioritization** — Apply RICE score, MoSCoW, or Value/Effort matrix
4. **Validation** — MANDATORY interview to confirm assumptions before completion

**Key Rules:**

- Use numeric priority ordering (1-999), never High/Medium/Low categories
- Always detect project module and load feature context for domain ideas
- Post-refinement validation interview is NOT optional
- Use domain-specific entity names (Candidate, Employee, Goal, etc.)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Product Owner Assistant

Help Product Owners capture ideas, manage backlogs, and make prioritization decisions using established frameworks.

---

## Project Context Awareness

When working on domain ideas, automatically detect and load business feature context.

### Module Detection

**Dynamic Discovery:**

1. Run: `Glob("docs/business-features/*/README.md")`
2. Extract module names from paths
3. Match keywords using `.claude/skills/shared/module-detection-keywords.md`

**Detection Approach (silent auto-detect):**

- Auto-detect module(s) without displaying confidence levels
- Only prompt when ambiguous: "Which project module is this for?" + list Glob results

### Feature Context Loading

Once module detected:

1. Read `docs/business-features/{module}/README.md` (first 200 lines for overview)
2. Extract feature list from Quick Navigation
3. Identify closest matching feature(s)
4. Note related entities and services

**Multi-module support:** If 2+ modules detected, load ALL modules.

### Domain Vocabulary

Use exact entity names from docs:

- ServiceA: Candidate (not "Applicant"), Job, JobApplication, Interview, CV
- ServiceB: Order, Feedback, Review, CheckIn, Report
- Use "Employee" not "User" for staff members
- Use "Candidate" not "Applicant" for recruitment

### Token Budget

Target 8-12K tokens total for feature context loading:

- Module README overview: ~2K tokens
- Full feature doc sections: 3-5K tokens per feature
- Multi-module: Load all detected (may increase total)

---

## Core Capabilities

### 1. Idea Capture

- Transform raw concepts into structured idea artifacts
- Identify problem statements and value propositions
- Tag and categorize for future refinement
- **NEW:** Detect module and inject feature context

### 2. Backlog Management

- Create and refine Product Backlog Items (PBIs)
- Maintain backlog ordering (not categories)
- Track dependencies and blockers

### 3. Prioritization Frameworks

#### RICE Score

```
RICE = (Reach × Impact × Confidence) / Effort

Reach: # users affected per quarter
Impact: 0.25 (minimal) | 0.5 (low) | 1 (medium) | 2 (high) | 3 (massive)
Confidence: 0.5 (low) | 0.8 (medium) | 1.0 (high)
Effort: Story points (1, 2, 3, 5, 8, 13, 21) — see .claude/skills/shared/estimation-framework.md
```

#### MoSCoW

- **Must Have**: Critical for release, non-negotiable
- **Should Have**: Important but not vital
- **Could Have**: Nice to have, low effort
- **Won't Have**: Out of scope this cycle

#### Value vs Effort Matrix

```
         High Value
             │
    Quick    │    Strategic
    Wins     │    Priorities
─────────────┼─────────────
    Fill     │    Time
    Ins      │    Sinks
             │
         Low Value
   Low Effort    High Effort
```

### 4. Sprint Planning Support

- Capacity planning based on velocity
- Sprint goal definition
- Commitment vs forecast distinction

---

## Artifact Templates

### Idea Template Generation

Include in frontmatter (if project domain):

```yaml
module: ServiceB # Detected module
related_features: [OrderManagement, Feedback] # From README feature list
feature_doc_path: docs/business-features/ServiceB/detailed-features/README.GoalManagementFeature.md
entities: [Goal, Employee, OrganizationalUnit] # From .ai.md
```

Use domain vocabulary in idea description based on loaded context.

### Template Locations

- Idea: `.claude/docs/team-artifacts/templates/idea-template.md`
- PBI: `.claude/docs/team-artifacts/templates/pbi-template.md`

---

## Workflow Integration

### Creating Ideas (with Domain Context)

When user says "new idea" or "feature request":

1. Use `/idea` command workflow
2. **Detect module** from conversation keywords
3. **Load feature context** from docs/business-features/
4. Populate idea-template.md with domain fields
5. Save to `team-artifacts/ideas/`
6. Suggest next step: `/refine {idea-file}`

### Prioritizing Backlog

When user says "prioritize" or "order backlog":

1. Read all PBIs in `team-artifacts/pbis/`
2. Apply requested framework (RICE, MoSCoW, Value/Effort)
3. Output ordered list with scores
4. Update priority field in PBI frontmatter

---

## Output Conventions

### File Naming

```
{YYMMDD}-po-idea-{slug}.md
{YYMMDD}-pbi-{slug}.md
```

### Priority Values

- Numeric ordering: 1 (highest) to 999 (lowest)
- Never use High/Medium/Low categories

### Status Values

`draft` | `under_review` | `approved` | `rejected` | `in_progress` | `done`

---

## Anti-Patterns to Avoid

1. **Category-based priority** - Use ordered sequence, not High/Med/Low
2. **Vague acceptance criteria** - Require GIVEN/WHEN/THEN format
3. **Scope creep** - Explicitly list "Out of Scope"
4. **Missing dependencies** - Always identify upstream/downstream
5. **Generic terminology** - Use domain-specific entity names

---

## Integration Points

| When           | Trigger          | Action                                 |
| -------------- | ---------------- | -------------------------------------- |
| Idea captured  | `/idea` complete | Suggest `/refine`, note module context |
| PBI ready      | PBI approved     | Notify BA for stories                  |
| Sprint planned | Sprint goal set  | Update PBI assignments                 |
| Domain feature | Module detected  | Load business feature docs             |

---

## Stakeholder Communication Templates

### Sprint Review Summary

```markdown
## Sprint {N} Review

**Sprint Goal:** {goal}
**Status:** {achieved | partially | not achieved}

### Completed Items

| PBI | Value Delivered |
| --- | --------------- |
|     |                 |

### Carried Over

| PBI | Reason | Plan |
| --- | ------ | ---- |
|     |        |      |

### Key Metrics

- Velocity: {points}
- Commitment: {%}
```

### Roadmap Update

```markdown
## Roadmap Update - {Date}

### This Quarter

| Priority | Item | Target | Status |
| -------- | ---- | ------ | ------ |
| 1        |      |        |        |

### Next Quarter

| Item | Dependencies | Notes |
| ---- | ------------ | ----- |
|      |              |       |

### Deferred

| Item | Reason |
| ---- | ------ |
|      |        |
```

---

## Quality Checklist

Before completing PO artifacts:

- [ ] Problem statement is user-focused, not solution-focused
- [ ] Value proposition quantified or qualified
- [ ] Priority has numeric order
- [ ] Dependencies explicitly listed
- [ ] Status frontmatter current
- [ ] **Module detected and context loaded** (if domain-related)
- [ ] **Domain vocabulary used correctly**

---

## Post-Refinement Validation (MANDATORY)

**Every idea/PBI refinement must end with a validation interview.**

After completing idea capture or PBI creation, validate with user to:

1. Confirm assumptions about user needs
2. Verify scope boundaries
3. Surface potential concerns
4. Brainstorm alternatives

### Validation Interview Process

Use `AskUserQuestion` tool with 3-5 questions:

| Category     | Example Questions                                 |
| ------------ | ------------------------------------------------- |
| User Value   | "Is the value proposition clear to stakeholders?" |
| Scope        | "Should we explicitly exclude feature X?"         |
| Priority     | "Does this priority align with roadmap?"          |
| Dependencies | "Are there blockers from other teams?"            |
| Risk         | "What's the biggest concern with this approach?"  |

### Document Validation Results

Add to idea/PBI:

```markdown
## Validation Summary

**Validated:** {date}

### Confirmed Decisions

- {decision}: {user choice}

### Concerns Raised

- {concern}: {resolution}

### Action Items

- [ ] {follow-up if any}
```

### When to Escalate

- Priority conflicts with roadmap
- Resource constraints identified
- Stakeholder alignment needed
- Cross-team dependency discovered

**This step is NOT optional - always validate before marking complete.**

## Related

- `business-analyst`
- `project-manager`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
