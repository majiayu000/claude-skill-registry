---
name: spec-validate
description: Validation loop for speccing. Clarifies requirements through structured questioning before document creation.
---

# Spec Validate Skill

Validate requirements through structured clarification. Produces validation data for spec-create.

> **Reference:** See [reference/issue-types.md](reference/issue-types.md) for type definitions, [reference/question-taxonomy.md](reference/question-taxonomy.md) for question templates, and [reference/sdd-gates.md](reference/sdd-gates.md) for pre-implementation gate definitions.

---

## When to Use

**Use for:**
- New features before implementation
- Unclear requirements needing refinement
- Complex changes needing design exploration
- When multiple approaches seem viable

**Don't use for:**
- Simple bug fixes
- Well-specified changes
- Clear mechanical tasks (use Claude's native planning)

---

## Workflow

### Step 0: Check Native Plan Context

Before starting validation, check if the user has existing context from Claude's native `/plan`:

1. **Check for context:** Ask if `/plan` was used or if there's existing plan context
2. **If present:** Extract key elements:
   - Goal/objective → Seeds **Scope** taxonomy area
   - Approach/strategy → Seeds **Integration/Architecture** areas
   - Open questions → Become priority clarification targets
3. **If absent:** Proceed directly to Step 1

This step bridges native Claude planning with structured validation.

### Step 0.5: Constitution Check (Initiatives Only)

For Initiative-type work, verify alignment with constitution before proceeding:

1. Read `.claude/constitution.md`
2. Check if proposed work aligns with core principles
3. If conflict detected:
   - Flag the conflict
   - Ask user to resolve or justify exception
   - Document exception in validation data

**Skip for:** Features, Tasks (constitution checked during task-dispatch for Initiatives)

### Step 1: Issue Type Selection

**FIRST QUESTION (Always)** - Use AskUserQuestion:

```
Header: Work type
Question: What type of work is this?
multiSelect: false
Options:
- Initiative: Strategic coordination (months) - Multiple features toward business goal
- Feature: User-facing capability (weeks) - Deliverable value, multiple tasks
- Task: Implementation item (days) - Single concrete deliverable
- Exploratory: Not sure yet - Gather context first, then classify
```

This selection determines:
- **Question limit:** Tasks get 3, Features/Initiatives get 5
- **Taxonomy areas:** Tasks get minimal (3), Features/Initiatives get full (7)

**If Exploratory:** Gather context, ask 3 questions to understand scope, present classification recommendation, restart with correct type.

### Step 2: Gather Context

1. Examine relevant files, docs, recent commits
2. Understand existing patterns and constraints
3. Initialize taxonomy tracking based on issue type

**Taxonomy by type:**

| Type | Areas to Cover |
|------|----------------|
| Initiative | Scope, Behavior, Data Model, Constraints, Edge Cases, Integration, Terminology |
| Feature | Scope, Behavior, Data Model, Constraints, Edge Cases, Integration, Terminology |
| Task | Scope, Behavior, Integration |

### Step 2.5: Ambiguity Scan

Automatically scan gathered context for specification gaps across taxonomy areas.

**Process:**

1. For each taxonomy area (based on issue type), evaluate:
   - **clear**: Fully specified, no questions needed
   - **partial**: Some information present, gaps remain
   - **missing**: Not addressed at all

2. Populate `ambiguity_scan` section in validation data:
   ```yaml
   ambiguity_scan:
     scope:
       status: clear | partial | missing
       gaps: ["gap description if partial/missing"]
     behavior:
       status: clear | partial | missing
       gaps: []
     # ... remaining areas
   ```

3. Route based on scan results:
   - **No gaps (all clear):** Proceed silently to Step 4 (skip validation loop)
   - **Gaps found:** Areas with `partial` or `missing` status become priority candidates for clarification questions in Step 3

**Evaluation criteria per area:**

| Area | Clear | Partial | Missing |
|------|-------|---------|---------|
| Scope | Goals, boundaries, success criteria defined | Some elements unclear | No scope information |
| Behavior | User flows, system responses specified | Some paths undefined | No behavior described |
| Data Model | Entities, relationships, formats clear | Schema gaps exist | No data model |
| Constraints | Performance, security, compatibility stated | Some constraints unclear | No constraints |
| Edge Cases | Error handling, limits documented | Some cases unaddressed | No edge cases |
| Integration | Dependencies, APIs, interfaces identified | Some touchpoints unclear | No integration info |
| Terminology | Domain terms defined consistently | Some ambiguous terms | No definitions |

### Step 3: Validation Loop

Ask clarifying questions in taxonomy-based batches, with re-evaluation between rounds.

**Process:**
1. Identify uncovered taxonomy areas
2. Prioritize areas by (Impact × Uncertainty)
3. Group questions by taxonomy area into batches
4. Use AskUserQuestion with multiple questions from the same area
5. Receive answers
6. Re-evaluate remaining questions for relevance (skip questions invalidated by answers)
7. Update taxonomy coverage
8. Repeat with next taxonomy area until limit reached or all Primary areas covered

**Batch format:**

```
AskUserQuestion with questions array (1-4 questions per batch):

Question 1:
  Header: [Area, max 12 chars]
  Question: [Clear question ending with ?]
  multiSelect: false
  Options: [2-4 options with implications]

Question 2:
  Header: [Same area]
  Question: [Related question]
  ...
```

**Single question format (when only one question in area):**

```
Header: [Area, max 12 chars]
Question: [Clear question ending with ?]
multiSelect: false
Options:
- Option A: [choice] - [implication]
- Option B: [choice] - [implication]
- Option C: [choice] - [implication]
- None: [default/skip]
```

**Batching rules:**
- One batch per taxonomy area (questions grouped by area)
- Multiple trigger fields within a batch combine with OR (any match)

**Batch counts:**
- Tasks: up to 3 batches (Scope, Behavior, Integration)
- Features/Initiatives: up to 7 batches (all taxonomy areas)
- Plus: additional clarification batches if "Other" answers need follow-up

**Batch size limits:**
- Tasks: up to 3 questions per batch
- Features/Initiatives: up to 4 questions per batch (AskUserQuestion max)

**Re-evaluation between batches:**
- After receiving answers, check if pending questions are still relevant
- Skip questions invalidated by previous answers
- If user provides ambiguous "Other" answer spanning areas, add follow-up to next batch

### Step 3.5: Initiative-Specific Validation (Initiatives Only)

For Initiatives, ask about user story prioritization and implementation strategy:

```
Header: User Stories
Question: How should user stories be prioritized?
multiSelect: false
Options:
- MVP First (Recommended): P1 stories deliver standalone value, P2/P3 are incremental
- Parallel Tracks: Stories can be developed independently by different teams
- Sequential: Stories have strict dependencies, must complete in order
```

```
Header: Strategy
Question: What implementation approach fits best?
multiSelect: false
Options:
- MVP First (Recommended): Ship P1, iterate on P2/P3 based on feedback
- Incremental: Each phase adds value, all planned upfront
- Parallel Team: Multiple workstreams, integration points defined
```

Track selections in validation data for spec-create (populates Implementation Strategy section).

### Step 3.6: SDD Section Opt-ins (Features Only)

For Features, offer opt-in for detailed SDD sections:

```
Header: SDD sections
Question: Which detailed sections do you want in the spec?
multiSelect: true
Options:
- Tech Decisions: Document technology choices and rationale
- API Contract: Define API endpoints and schemas
- Data Model: Document entities and relationships
- None: Keep spec lightweight
```

Track selections in validation data for spec-create.

### Step 4: Propose Approaches

Use AskUserQuestion to present options:

```
Header: Approach
Question: Which approach should we take?
multiSelect: false
Options:
- Approach A: [brief] - Trade-off: [X]
- Approach B: [brief] - Trade-off: [Y] (Recommended)
- Approach C: [brief] - Trade-off: [Z]
```

Lead with your recommendation. Apply YAGNI ruthlessly.

### Step 5: Generate Validation Data

Compile validation data for spec-create:

- **Issue type:** Selected in Step 1
- **Ambiguity scan:** Status per area (clear / partial / missing) with gap descriptions
- **Questions used:** N / limit
- **Taxonomy coverage:** Status per area (Covered / Gap / N/A)
- **Clarification log:** Question → Answer → Integration point
- **Approach selected:** From Step 4
- **SDD opt-ins:** Which sections selected (Features only)
- **Gates status:** For Initiatives: run gate checks; for Features/Tasks: mark n/a
- **Markers:** Any unresolved items identified during validation

This data passes to spec-create for validation.yaml.

---

## Key Principles

| Principle | Why |
|-----------|-----|
| **Issue type first** | Branches workflow, sets question limit |
| **Ambiguity scan** | Identifies gaps early, skips validation if all clear |
| **MultiSelect always** | Structured options, faster iteration |
| **Question limits** | Forces prioritization |
| **Taxonomy tracking** | Ensures coverage of important areas |
| **YAGNI ruthlessly** | Remove unnecessary features |

---

## Output

This skill produces **validation data**, not documents. The data flows to `spec-create` which generates:
- spec.md, context.md, tasks.md, dependencies.yaml, validation.yaml

---

## Integration

**Invoked by:** `/spec.create` command (default behavior)

**Standalone use:** Can be invoked directly via `spec-validate` skill for validation without document creation.
