---
name: ralph-ify
description: Transform any workflow, skill, or process into a RALPH-style iterative architecture with quality gates and state persistence
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task, AskUserQuestion
user_invocable: true
argument-hint: <input> [--name SKILL_NAME]
---

# RALPH-ify: Transform Workflows into Iterative Architecture

## Overview

RALPH-ify is a meta-skill that transforms any workflow, existing skill, or business process into a RALPH-style iterative architecture. It generates complete, ready-to-run skills with:

- Three-phase execution (Planning → Iterative Execution → Assembly)
- Quality gates with specific feedback for refinement
- State persistence for resumability
- Audit logging for transparency

## Invocation

```bash
/ralph-ify <input> [--name SKILL_NAME]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<input>` | Yes | Workflow description, file path, or existing skill path |
| `--name` | No | Name for the generated skill (auto-generated if not provided) |

### Input Formats

The skill accepts multiple input formats:

1. **Text description**: `"Process invoices and send payment reminders"`
2. **File path**: `/path/to/workflow-description.md`
3. **Existing skill**: `.claude/skills/document-studio` (to upgrade a non-RALPH skill)
4. **Meeting transcript**: Path to a transcript file describing a process

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PHASE 1: ANALYSIS                           │
├─────────────────────────────────────────────────────────────────┤
│  1. Parse input (detect format: text/file/skill)                │
│  2. Extract workflow structure                                   │
│  3. Identify discrete work units                                 │
│  4. Map dependencies between units                               │
│  5. Present analysis summary                                     │
│  6. ──► CHECKPOINT: Get user approval ◄──                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PHASE 2: DESIGN                             │
├─────────────────────────────────────────────────────────────────┤
│  1. Generate atomic work units with sizing                       │
│  2. Create PRD schema structure                                  │
│  3. Design quality gates (4-8 per item type)                    │
│  4. Define state file structure                                  │
│  5. Present design summary                                       │
│  6. ──► CHECKPOINT: Get user approval ◄──                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 3: SCAFFOLD                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Generate SKILL.md with three-phase architecture             │
│  2. Create prd-schema.json                                       │
│  3. Create quality-gates.md                                      │
│  4. Create state directory template                              │
│  5. Write all files to .claude/skills/{skill-name}/             │
│  6. Present completion summary                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Analysis

### Step 1.1: Detect Input Format

Parse the input to determine its type:

```
IF input starts with "." or "/" AND is a directory:
    → Existing skill (upgrade mode)
ELSE IF input is a valid file path:
    → File-based workflow description
ELSE:
    → Free-form text description
```

### Step 1.2: Extract Workflow Structure

Read the referenced prompt template: `.claude/skills/ralph-ify/prompts/analysis.md`

Run the analysis prompt against the input to extract:
- **Workflow name**: What is this process called?
- **Workflow steps**: What are the sequential/parallel steps?
- **Work units**: What are the discrete, atomic tasks?
- **Dependencies**: Which units depend on others?
- **Success criteria**: What does "done" look like for each unit?
- **Failure modes**: What can go wrong?

### Step 1.3: Present Analysis Summary

Present findings to the user in this format:

```markdown
## Workflow Analysis: {workflow_name}

### Identified Work Units ({count})

| ID | Unit Name | Dependencies | Est. Complexity |
|----|-----------|--------------|-----------------|
| 1  | ...       | None         | Low             |
| 2  | ...       | [1]          | Medium          |

### Success Criteria
- Unit 1: [criteria]
- Unit 2: [criteria]

### Potential Failure Modes
- [failure mode 1]
- [failure mode 2]
```

### Step 1.4: User Approval Checkpoint

Use `AskUserQuestion` to confirm:
- Are the work units correctly identified?
- Are there any missing steps?
- Should any units be split or merged?

---

## Phase 2: Design

### Step 2.1: Generate Atomic Work Units

For each identified work unit, ensure it:
- Can be completed in one context window
- Has clear input/output boundaries
- Has measurable success criteria

### Step 2.2: Create PRD Schema

Read the template: `.claude/skills/ralph-ify/templates/prd-template.json`

Generate a PRD schema specific to this workflow:

```json
{
  "version": "1.0",
  "skill": "{skill-name}",
  "config": {
    "maxIterations": {recommended},
    "maxFailuresPerItem": 3
  },
  "items": [
    {
      "id": "{ITEM_TYPE}-001",
      "title": "...",
      "description": "...",
      "priority": 1,
      "status": "pending",
      "dependsOn": []
    }
  ]
}
```

### Step 2.3: Design Quality Gates

Read the prompt: `.claude/skills/ralph-ify/prompts/quality-gates.md`

For each item type, generate 4-8 quality checks:

```markdown
## Quality Gate: {item_type}

| Check | Criteria | Pass Threshold | Failure Suggestion |
|-------|----------|----------------|-------------------|
| check_1 | ... | ... | "To fix: ..." |
| check_2 | ... | ... | "To fix: ..." |

**Pass Threshold**: 70% of checks must pass
**Critical Failures**: [checks that auto-fail the gate]
```

### Step 2.4: Define State Structure

Design the state directory:

```
.{skill-name}/
├── prd.json              # Source of truth for items
├── progress.txt          # Human-readable log
├── segments/             # Per-item outputs (if applicable)
└── output/               # Final assembled outputs
```

### Step 2.5: User Approval Checkpoint

Present the complete design and use `AskUserQuestion` to confirm:
- Is the PRD structure correct?
- Are the quality gates appropriate?
- Should any gates be added/removed?

---

## Phase 3: Scaffold

### Step 3.1: Generate SKILL.md

Read the template: `.claude/skills/ralph-ify/templates/skill-template.md`

Generate a complete SKILL.md with:
- Frontmatter (name, description, tools, invocation)
- Overview section
- Three-phase execution flow
- Detailed instructions for each phase
- Quality gates section
- State files documentation
- Troubleshooting section

### Step 3.2: Create Supporting Files

Generate all supporting files:

1. **prd-schema.json**: The designed PRD structure
2. **quality-gates.md**: All quality gate definitions
3. **State directory template**: Empty directories with README

### Step 3.3: Write Files

Write all files to `.claude/skills/{skill-name}/`:

```
.claude/skills/{skill-name}/
├── SKILL.md
├── prd-schema.json
├── quality-gates.md
└── state-template/
    ├── .gitkeep
    └── README.md
```

### Step 3.4: Completion Summary

Present a summary:

```markdown
## RALPH-ified Skill Created

**Skill Name**: {skill-name}
**Location**: .claude/skills/{skill-name}/

### Files Created
- SKILL.md (main skill definition)
- prd-schema.json (PRD structure)
- quality-gates.md (validation criteria)
- state-template/ (state directory)

### Next Steps
1. Review the generated SKILL.md
2. Test with: `/{skill-name} <test-input>`
3. Iterate on quality gates as needed
```

---

## Quality Gates (for RALPH-ify itself)

### Gate 1: Decomposition Quality

| Check | Criteria |
|-------|----------|
| atomic_units | Each unit can be completed in one context window |
| clear_boundaries | Units have defined inputs and outputs |
| no_overlap | Units don't duplicate work |
| complete_coverage | All workflow steps are covered |

### Gate 2: Quality Gate Coverage

| Check | Criteria |
|-------|----------|
| gate_count | Each item type has 4-8 validation checks |
| specific_suggestions | Each failure has actionable suggestions |
| measurable_criteria | Criteria are objective, not subjective |
| threshold_defined | Pass threshold is explicitly set |

### Gate 3: State Schema Validity

| Check | Criteria |
|-------|----------|
| valid_json | PRD schema is valid JSON |
| required_fields | Has id, status, priority, title |
| status_enum | Status uses standard values (pending/in_progress/passed/failed/blocked) |
| dependency_refs | Dependencies reference valid IDs |

### Gate 4: Skill Definition Completeness

| Check | Criteria |
|-------|----------|
| has_frontmatter | Skill has valid YAML frontmatter |
| has_overview | Overview section explains purpose |
| has_phases | All three phases documented |
| has_state_docs | State files are documented |

---

## State Files

This skill does not maintain persistent state. Each invocation is independent.

---

## Troubleshooting

### "Input not recognized"
- Ensure the input is either a valid file path or text description
- For existing skills, provide the full path to the skill directory

### "Workflow too complex"
- Break the workflow into smaller sub-workflows
- Run RALPH-ify on each sub-workflow separately

### "Quality gates seem wrong"
- Quality gates are generated heuristically; edit them manually after generation
- Focus on measurable, objective criteria

---

## Examples

See `.claude/skills/ralph-ify/examples/` for example transformations.
