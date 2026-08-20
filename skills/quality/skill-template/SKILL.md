---
name: prd-vXX-skill-name
description: >
  [1-2 sentence description of what this skill does].
  Triggers on [specific phrases/contexts that should activate this skill].
  Outputs [what the skill produces].
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# [Skill Name]

[One sentence summary of the skill's purpose.]

## Workflow Overview

1. **Step 1** → Brief description
2. **Step 2** → Brief description
3. **Step 3** → Brief description

## Core Output Template

[Define the primary output structure this skill produces]

| Element | Definition | Evidence |
|---------|------------|----------|
| **Field 1** | What this captures | How to validate |
| **Field 2** | What this captures | How to validate |

See `assets/output-template.md` for copy-paste template.

## Step 1: [First Major Step]

[Detailed instructions for this step]

### Checklist
- [ ] Item 1
- [ ] Item 2

## Step 2: [Second Major Step]

[Detailed instructions for this step]

## Step 3: [Third Major Step]

[Detailed instructions for this step]

## Quality Gates

### Pass Checklist
- [ ] Gate 1: [Specific, measurable criterion]
- [ ] Gate 2: [Specific, measurable criterion]
- [ ] Gate 3: [Specific, measurable criterion]

### Testability Check
- [ ] Can this output be validated?
- [ ] Does it reference IDs from SoT/?

> **How this is evaluated**: This skill's output is scored by `scripts/readiness.py` (a deterministic, $0, no-LLM proxy). Clearing a gate is permission to advance, not the goal — the goal is evidence. Padding inputs to move the score without moving the evidence is a *frozen-replay defect*. See [`PRINCIPLES.md` P7](../PRINCIPLES.md).

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Bad pattern 1 | "Example" | → "Better approach" |
| Bad pattern 2 | "Example" | → "Better approach" |
| Evidence fabrication | Back-filling confidence/evidence to clear a gate | → Cite a real source or mark the gap; never invent to pass (P4 anti-leakage, P7) |

## Bundled Resources

- **`references/[file].md`** — [Description of when to use]
- **`assets/[template].md`** — [Description of template purpose]

## Handoff

[What happens after this skill completes? What stage/skill comes next?]
