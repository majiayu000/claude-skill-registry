---
name: documentation
description: Guide for maintaining documentation across the SAPPHIRE repository. Use when auditing docs, identifying gaps or redundancies, writing new documentation, updating stale content, or planning documentation improvements. References the existing documentation_improvement_plan.md for ongoing work.
---

# Documentation Management

Maintain clarity and coherence across the repository's documentation.

## Documentation Architecture

### SAPPHIRE Structure
```
README.md                    # Landing page: what is this, quick start
│
├── /doc                     # Comprehensive documentation
│   ├── index.md            # Documentation home (MkDocs)
│   ├── user_guide.md       # End-user workflows
│   ├── configuration.md    # Configuration reference
│   ├── deployment.md       # Deployment procedures
│   ├── development.md      # Developer setup & contribution
│   ├── workflows.md        # Pipeline workflow documentation
│   ├── dashboard.md        # Dashboard features & usage
│   ├── bulletin_template_tags.md  # Bulletin templating
│   │
│   ├── /luigi_daemon       # Luigi daemon operations
│   ├── /maintenance        # System maintenance docs
│   ├── /monitoring         # System monitoring docs
│   ├── /modules            # Module-specific docs (planned)
│   │
│   └── /plans              # Planning and issue tracking
│       ├── module_issues.md              # Issue index
│       ├── issues/                       # Detailed issue plans (gi_*.md)
│       ├── documentation_improvement_plan.md
│       └── *.md                          # Architecture/planning docs
│
└── /apps/<module>/         # Module-level READMEs
    └── README.md           # Quick overview, links to /doc/modules/
```

### Key Principles

1. **Single source of truth** — Each topic in one place, others link to it
2. **Progressive disclosure** — README → doc/index → specific guides → module READMEs
3. **Hybrid module docs** — Brief README in module, details in doc/modules/
4. **Flat by default** — Only nest when clearly necessary (operations, modules)

---

## Task 1: Documentation Audit

### 1.1 Inventory existing docs

| File | Location | Audience | Status |
|------|----------|----------|--------|
| README.md | root | all | current? |
| user_guide.md | /doc | users | current? |
| development.md | /doc | developers | current? |
| ... | ... | ... | ... |

### 1.2 Check against improvement plan

Read `doc/plans/documentation_improvement_plan.md` for:
- Completed items (✅)
- In-progress items
- Pending priorities

### 1.3 Identify issues

- **Orphaned docs** — Files not linked from anywhere
- **Gaps** — Missing docs for existing functionality
- **Redundancies** — Same info in multiple places
- **Stale content** — Docs that don't match current code
- **Misplaced docs** — Files in wrong location

---

## Task 2: Documentation Planning

### 2.1 Use existing roadmap

The `doc/plans/documentation_improvement_plan.md` contains:
- 7 phases of documentation work
- Priority-ordered tasks
- Status tracking

### 2.2 For new documentation needs

Use the **issue-planning** skill to:
1. Analyze what's needed
2. Plan the implementation
3. Create a well-structured issue or add to improvement plan

---

## Task 3: Writing & Updating Docs

### 3.1 Before writing, determine:

- **Audience**: end-user, developer, operator?
- **Location**: doc/ or module README?
- **Links**: What should link here? What should this link to?

### 3.2 Module README template

```markdown
# Module Name

Brief description (1-2 sentences).

## Purpose
Why this module exists.

## Quick Start
```bash
ieasyhydroforecast_env_file_path=/path/to/.env python script.py
```

## Inputs
- `input_file.csv` — description

## Outputs
- `output_file.csv` — description

## Full Documentation
See [module documentation](../../doc/modules/module_name.md)
```

### 3.3 Detailed doc template (for doc/modules/)

```markdown
# Module Name

## Overview
What this module does and who it's for.

## Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `VAR_NAME` | What it does | Yes/No |

## Data Formats
### Input
- Format specification

### Output
- Format specification

## Architecture
[Mermaid diagram if complex]

## Troubleshooting
Common issues and solutions.
```

### 3.4 Writing checklist

- [ ] Audience is defined
- [ ] Purpose clear in first paragraph
- [ ] Examples included
- [ ] Links to related docs added
- [ ] Placed in correct location
- [ ] Linked from parent doc
- [ ] No redundancy with existing docs

---

## Task 4: Maintenance Routines

### On code changes
- [ ] Does this change affect any documentation?
- [ ] Update relevant docs in same PR/commit
- [ ] If larger doc update needed, create separate issue

### Periodic review
- [ ] Check documentation_improvement_plan.md for pending items
- [ ] Verify quick start instructions still work
- [ ] Test links aren't broken

---

## Quick Commands

**Audit documentation:**
"Audit the documentation. Start by reading doc/plans/documentation_improvement_plan.md for context, then inventory current docs and identify gaps."

**Plan documentation improvements:**
"Review the documentation improvement plan and help me prioritize next steps."

**Write new module documentation:**
"Help me write documentation for the [module] module. Create both a brief README and detailed doc/modules/ entry."

**Check for doc impact:**
"I'm changing [describe change]. What documentation might need updating?"

---

## Related Skills

- **issue-planning**: For creating documentation improvement issues
- **software-architecture**: For understanding module structure when documenting
