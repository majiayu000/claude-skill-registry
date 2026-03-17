---
name: new-plan
description: Create a new planning document and register it in the project CLAUDE.md. Use when starting multi-script or multi-session work that needs tracking, or when the user invokes /new-plan.
user-invocable: true
---

# Create a New Planning Document

When the user invokes `/new-plan`, create a structured planning document and register it in the project's document registry.

## 1. Gather Information

Ask the user:
- **Topic**: What is this plan for? (e.g., "transcriptomics volcano plots", "book chapter revision", "API redesign")
- **Category**: Planning doc (tracks status of ongoing work) or Data doc (describes datasets, file formats, schemas)?
- **Style**: Data science (numbered scripts, inputs/outputs tracking) or General (tasks, milestones, components)?
- **Task tracking** (planning docs only): Checkboxes (simple open/completed lists) or Status table (phased rows with status column)?

If the user provides the topic directly as an argument (e.g., `/new-plan thermal proteome profiling`), use that and still ask the remaining questions.

Streamline the questions — if the answers are obvious from context, propose defaults and let the user confirm. For example, a data science project asking about "volcano plots" likely wants data science style with status table.

## 2. Create the Document

Create a new `.md` file in the project's `.claude/` directory.

### Naming convention
- Use `SCREAMING_SNAKE_CASE` matching existing docs
- Planning docs: `{TOPIC}_PLAN.md` (e.g., `THERMAL_PROTEOME_PLAN.md`)
- Data docs: `{TOPIC}_DATA.md` (e.g., `SECRETOMICS_DATA.md`)

---

## Planning Document Templates

### General planning doc (checkbox style)

For general projects (books, tools, infrastructure) with simple task tracking.

```markdown
# {Topic} Plan

> Last updated: {today}

## Overview

{Brief description of what this plan covers}

## Goals

- [ ] Goal 1
- [ ] Goal 2

## Open Tasks

{Group tasks by category if there are many}

- [ ] Task 1
- [ ] Task 2

## Key Files

- (list key files and components as they become relevant)

## Completed

- [x] (move completed items here)
```

### General planning doc (status table style)

For general projects that benefit from phased tracking.

```markdown
# {Topic} Plan

> Last updated: {today}

## Overview

{Brief description of what this plan covers}

## Goals

- [ ] Goal 1
- [ ] Goal 2

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | {First phase} | Not started |

## Key Files

- (list key files and components as they become relevant)
```

### Data science planning doc

For analysis projects with numbered scripts, data pipelines, and input/output tracking.

```markdown
# {Topic} Plan

> Last updated: {today}

## Overview

{Brief description of what this plan covers}

## Goals

- [ ] Goal 1
- [ ] Goal 2

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | {First phase} | Not started |

## Key Files

### Inputs
- (list input files as they become relevant)

### Outputs
- (list output files as they are created)

### Scripts

Track all scripts here. When a script is superseded, move it to the Legacy section.

#### Active
| Script | Purpose | Status |
|--------|---------|--------|
| (add scripts as they are created) | | |

#### Legacy / Inactive
| Script | Replaced by | Notes |
|--------|-------------|-------|
| (move superseded scripts here) | | |
```

---

## Data Document Templates

### General data doc

For documenting APIs, schemas, configuration formats, or any structured reference material.

```markdown
# {Topic} Data

## Overview

{Brief description of what this document covers}

## Purpose

{Why this data/schema/format exists and how it's used}

## Key Files

| File | Description |
|------|-------------|
| | |

## Structure / Schema

{Describe the structure, format, or schema of the key files}

## Notes

{Any important notes about usage, edge cases, or conventions}
```

### Data science data doc

For documenting experimental datasets with biological/scientific context.

```markdown
# {Topic} Data

## Overview

{Brief description of the dataset}

## Experimental Design

{Describe the experiment that generated this data}

## Key Files

| File | Description |
|------|-------------|
| | |

## Column Descriptions

{For key files, describe important columns}

## Processing Notes

{Any important notes about how data was processed or should be used}
```

---

## Maintaining Plans Over Time

### Collapse completed phases

When a phase is marked complete, collapse its detailed content to a **3-5 line summary**. Keep the phase heading and a brief record of what was done and any key outcomes, but remove per-item audit results, checklists, and working notes that are no longer needed for active work. This prevents plans from growing monotonically as work progresses.

**Before collapsing, check:** Does any information in this phase feed into a future phase that hasn't started yet? If so, ensure that information is already captured in the future phase's section (or the "Next Session" section) before removing it from the completed phase. Only collapse what is truly historical.

Example — before collapsing:
```markdown
## Phase 2: Dependency Audit ✓ COMPLETE

### Per-script summary
(60 lines of detailed per-script audit results...)

### Critical issues
(30 lines of issue details, all resolved...)
```

After collapsing:
```markdown
## Phase 2: Dependency Audit ✓ COMPLETE

Audited 21 scripts. Found 3 critical issues (all resolved in Phase 4): missing `theme_paper()` definition, hardcoded paths in 2 scripts, undeclared dependency on `datasets_for_plotting/conditions.csv`. Full audit preserved in git history.
```

---

## 3. Register in Project CLAUDE.md

After creating the document, add it to the **Project Document Registry** in the project's `.claude/CLAUDE.md`:

1. Read `.claude/CLAUDE.md` and find the "Project Document Registry" section
2. Add a new row to the appropriate table (Planning Documents or Data Documents)
3. Include the document name, topic, and whether it has a status table

If no registry exists, create the registry section first (following the format in the `/done` skill documentation).

## 4. Confirm

Tell the user:
- What file was created and where
- That it was registered in the project CLAUDE.md
- Suggest they start filling in the details or that you can help plan the work
