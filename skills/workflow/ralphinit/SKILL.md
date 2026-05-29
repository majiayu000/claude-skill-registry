---
description: Start a ralph style looping session
allowed-tools: Bash(git:*), Bash(codex:*), Bash(cat:*), Bash(wc:*)
---

# Initialize Project Documentation from System Plan

You are initializing a new project for agent-driven development. The user has provided a `current_SYSTEM-PLAN.md` file in the current working directory that describes the system architecture and goals.

## Your Task

Read `current_SYSTEM-PLAN.md` and create two companion documents:

1. **current_PRD.md** - A comprehensive Product Requirements Document
2. **current_PROGRESS.md** - A progress tracking journal

These three `current_*` files will serve as the foundation for an automated agent that works in a continuous development loop, picking up tasks and making progress incrementally.

---

## Step 1: Read the System Plan

First, read `current_SYSTEM-PLAN.md` in the current directory to understand:
- Project goals and context
- Architecture and components
- Design decisions
- Development stages/phases
- Success criteria
- Any constraints or scope limitations

---

## Step 2: Create current_PRD.md

Write a comprehensive PRD with **testable requirements** extracted from the system plan. Structure it as:

```markdown
# [Project Name] - Product Requirements Document

**Last Updated:** [today's date]

---

## Requirements

```json
[
  {
    "category": "functional|integration|architecture|performance|usability|maintainability|milestone|constraint",
    "description": "Clear, testable requirement statement",
    "steps": [
      "Step 1 to verify this requirement",
      "Step 2...",
      "Step 3...",
      "Step 4...",
      "Step 5..."
    ],
    "passes": false
  },
  ...
]
```

## Summary Statistics

| Category | Count |
|----------|-------|
| Functional | X |
| Integration | X |
| ... | ... |
| **Total** | **X** |

## Development Stages Mapping

Map requirements to development stages from the system plan.

## Open Questions

List any ambiguities or decisions that need user input.
```

### PRD Guidelines:

- **Extract ALL testable requirements** from the system plan - be thorough
- Each requirement must have 4-6 concrete verification steps
- Start all requirements with `"passes": false`
- Use categories: `functional`, `integration`, `architecture`, `performance`, `usability`, `maintainability`, `milestone`, `constraint`
- Functional requirements should cover every component mentioned in the architecture
- Include milestone requirements that map to the plan's success criteria
- Aim for 40-100 requirements depending on project complexity
- Requirements should be specific enough that pass/fail is unambiguous

---

## Step 3: Create current_PROGRESS.md

Write a progress journal structured for continuous agent development:

```markdown
# [Project Name] Progress Journal

**Purpose:** Track progress on implementation. Useful for context continuity between sessions.

**Last Updated:** [today's date]

---

## Current Status: [STAGE NAME] NOT STARTED

Brief description of where we are.

---

## Project Context Quick Reference

### What We Have
- Key existing assets (data, models, infrastructure)

### Key Files
- List important files and their purposes

### Core Design Decisions (from plan)
1. Decision 1
2. Decision 2
...

---

## Development Stages Checklist

### Stage 1: [Name]
**Goal:** [from system plan]

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Validation:** [how to know this stage is complete]

---

### Stage 2: [Name]
...

---

## Session Log

### [Date] - Session 1
**Work Done:**
- (empty - will be filled as work progresses)

**Next Session Should:**
- Start with first task from Stage 1

---

## Architecture Quick Reference

[Include a simplified architecture diagram or component list from the system plan]

---

## Key Interfaces (for quick reference)

[Extract key interfaces/APIs from the system plan that the agent will need to implement]

---

## Notes & Decisions Log

*Add notes here as implementation decisions are made*

---

## Open Questions

[Copy from system plan or identify new ones]
```

### Progress Guidelines:

- Structure should make it easy for an agent to:
  - Quickly understand current state
  - Find the next task to work on
  - Record what was done
  - Track which PRD requirements have been satisfied
- Include enough architecture context that the agent doesn't need to re-read the full system plan every session
- Checklist items should map to PRD requirements where possible
- Leave session log empty - it will be filled as work progresses

---

## Step 4: Verify and Report

After creating both files:
1. Confirm both files were written successfully
2. Report the total number of requirements in the PRD
3. Report the number of development stages identified
4. List any open questions or ambiguities that need user clarification

---

## Important Notes

- The system plan is the source of truth - don't invent requirements not implied by the plan
- Be comprehensive - the agent will rely on these documents to know what to build
- Keep formatting consistent - these files will be read programmatically
- Use the exact filenames: `current_PRD.md` and `current_PROGRESS.md`
- All three files should be in the current working directory
