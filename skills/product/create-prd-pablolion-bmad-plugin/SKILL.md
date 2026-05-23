---
description:
  Create, validate, or edit product requirements documents. Tri-modal. Phase 2
  Planning
user-invocable: true
disable-model-invocation: true
---

# PRD Workflow (Tri-Modal)

**Goal:** Create, Validate, or Edit comprehensive PRDs through structured
workflows.

**Agent:** PM (John) **Phase:** 2 - Planning

**Modes:**

- **Create (-c):** Build new PRD from scratch through collaborative discovery
- **Validate (-v):** Quality check existing PRD against BMAD standards
- **Edit (-e):** Improve existing PRD based on validation feedback

---

## MODE DETERMINATION

### Detect Mode from Invocation

| Invocation                   | Mode     |
| ---------------------------- | -------- |
| `/bmad:create-prd` or `-c`   | Create   |
| `/bmad:validate-prd` or `-v` | Validate |
| `/bmad:edit-prd` or `-e`     | Edit     |

### If Mode Unclear

Present selection menu:

```text
**PRD Workflow - Select Mode:**

**[C] Create** - Create a new PRD from scratch
**[V] Validate** - Validate an existing PRD against BMAD standards
**[E] Edit** - Improve an existing PRD

Which mode would you like?
```

Wait for user selection before proceeding.

---

## WORKFLOW ARCHITECTURE

Same step-file architecture as other BMAD workflows:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only load current step file
- **Sequential Enforcement**: Complete steps in order
- **State Tracking**: Track progress in frontmatter `stepsCompleted`

### Critical Rules

- NEVER load multiple step files simultaneously
- ALWAYS read entire step file before execution
- NEVER skip steps or optimize sequence
- ALWAYS halt at menus and wait for user input

---

## MODE ROUTING

### Create Mode

**Entry Point:** `steps-c/step-01-init.md`

Create mode guides through 12 steps:

1. Initialization and discovery
2. Input document loading
3. Success criteria definition
4. User journeys
5. Domain model
6. Innovation opportunities
7. Project type specific requirements
8. Scoping
9. Functional requirements
10. Non-functional requirements
11. Polish and refinement
12. Completion and validation

### Validate Mode

**Entry Point:** `steps-v/step-v-01-discovery.md`

Validate mode performs 13 validation checks:

1. Discovery and PRD loading
2. Format detection
3. Density validation
4. Brief coverage validation
5. Measurability validation
6. Traceability validation
7. Implementation leakage validation
8. Domain compliance validation
9. Project type validation
10. SMART validation
11. Holistic quality validation
12. Completeness validation
13. Report generation

### Edit Mode

**Entry Point:** `steps-e/step-e-01-discovery.md`

Edit mode handles:

1. Discovery and PRD loading
2. Legacy conversion (if needed)
3. Targeted improvements

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load project config from `bmad/config.yaml`:

- `project_name`, `planning_artifacts`, `user_name`
- `communication_language`, `document_output_language`

### 2. Mode Detection

Check invocation for mode flags or keywords.

### 3. Route to Workflow

Based on mode, read and execute the appropriate entry step file:

**Create:** `${CLAUDE_PLUGIN_ROOT}/skills/prd/steps-c/step-01-init.md`
**Validate:** `${CLAUDE_PLUGIN_ROOT}/skills/prd/steps-v/step-v-01-discovery.md`
**Edit:** `${CLAUDE_PLUGIN_ROOT}/skills/prd/steps-e/step-e-01-discovery.md`

---

## OUTPUT

**Create Mode Output:** `planning-artifacts/prd-{project_name}-{date}.md`
**Validate Mode Output:** `planning-artifacts/prd-validation-report-{date}.md`
**Edit Mode Output:** Updates the specified PRD file in-place
