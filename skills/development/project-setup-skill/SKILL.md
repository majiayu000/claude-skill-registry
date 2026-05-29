---
document_name: "project-setup.skill.md"
location: ".claude/skills/project-setup.skill.md"
codebook_id: "CB-SKILL-SETUP-001"
version: "1.0.0"
date_created: "2026-01-03"
date_last_edited: "2026-01-03"
document_type: "skill"
purpose: "Comprehensive skill for initializing new projects with all required fundamentals"
category: "skills"
subcategory: "project-management"
skill_metadata:
  category: "project-management"
  complexity: "intermediate"
  estimated_time: "15-30 minutes"
  prerequisites:
    - "Access to repository"
    - "Understanding of project type"
related_docs:
  - "CLAUDE.md"
  - "templates/documents/preamble.template.md"
imports:
  - path: "templates/_templates-index.md"
    alias: "TEMPLATES"
maintainers:
  - "head-cook"
status: "active"
tags:
  - "skill"
  - "setup"
  - "initialization"
  - "project"
ai_parser_instructions: |
  This skill is for project initialization.
  Run this BEFORE any coding begins on a new project.
  Section markers: === SECTION ===
  Procedure markers: <!-- PROCEDURE:name:START/END -->
  Checklist markers: - [ ] item
---

# Project Setup Skill

[!FIXED!]
## Purpose

This skill initializes new projects with all required fundamentals. Run this skill BEFORE any coding begins to ensure the kitchen is ready.

**When to use:**
- Starting a new project
- Pre-flight checklist failures
- Onboarding codebook to existing project
[!FIXED!]

---

=== PREREQUISITES ===
<!-- AI:PREREQUISITES:START -->

Before running this skill:

- [ ] Access to the repository
- [ ] Understanding of project type (web app, library, CLI, etc.)
- [ ] Knowledge of tech stack being used
- [ ] Authority to create files and directories

<!-- AI:PREREQUISITES:END -->

---

=== PROCEDURE: FULL INITIALIZATION ===
<!-- PROCEDURE:full-init:START -->

### Step 1: Core Files

Create these files if they don't exist:

#### 1.1 .gitignore
```bash
# Check if exists
ls -la .gitignore

# If not, create appropriate gitignore for project type
# Reference: templates/project/gitignore.template
```

#### 1.2 README.md
```markdown
# Project Name

## Overview
Brief description of the project.

## Setup
Instructions for getting started.

## Development
How to run locally.

## Contributing
How to contribute.
```

#### 1.3 CHANGELOG.md
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
```

### Step 2: CLAUDE.md

Copy and customize from codebook:
1. Copy CLAUDE.md from codebook to project root
2. Update project-specific sections
3. Adjust pre-flight checklist for project type

### Step 3: Directory Structure

Create essential directories:

```bash
mkdir -p .claude/skills
mkdir -p agentdocs/templates
mkdir -p devdocs/architecture
mkdir -p devdocs/business
mkdir -p devdocs/data
mkdir -p devdocs/ui
mkdir -p buildlogs/$(date +%Y)/templates
mkdir -p standards
mkdir -p templates
mkdir -p workflows
mkdir -p guides
```

### Step 4: Index Files

Create index files for each directory:

```markdown
# _<directory>-index.md

---
document_name: "_<directory>-index.md"
location: "<path>/_<directory>-index.md"
codebook_id: "CB-<CATEGORY>-INDEX"
# ... standard preamble
---

# <Directory> Index

=== REGISTERED ITEMS ===

| Codebook ID | Name | File | Status |
|-------------|------|------|--------|
| | | | |
```

### Step 5: First Buildlog

Create the first buildlog:

1. Determine current week number
2. Copy template from `buildlogs/templates/weekly.buildlog.template.md`
3. Create as `buildlogs/<YEAR>/week-<NN>.buildlog.md`
4. Fill in dates and initial entry:

```markdown
| Time | Tag | Entry | Related |
|------|-----|-------|---------|
| HH:MM | #micro-decision | Project initialized using project-setup skill | CB-SKILL-SETUP-001 |
```

### Step 6: Basic Standards

Create minimal standards files:

- `standards/naming-conventions.md` - How to name things
- `standards/code-patterns.md` - Coding patterns to follow (or reference)

### Step 7: Verification

Run the pre-flight checklist from CLAUDE.md:
- All checks should pass
- If any fail, address immediately

<!-- PROCEDURE:full-init:END -->

---

=== PROCEDURE: QUICK SETUP ===
<!-- PROCEDURE:quick-setup:START -->

For minimal viable setup (when time is critical):

1. **Create .gitignore** (essential for any git project)
2. **Create CLAUDE.md** (copy from codebook, minimal customization)
3. **Create buildlogs directory and first log** (mandatory)
4. **Create README.md** (basic project info)

Note: Full setup should be completed as soon as possible.

<!-- PROCEDURE:quick-setup:END -->

---

=== PROCEDURE: ONBOARDING EXISTING PROJECT ===
<!-- PROCEDURE:onboard:START -->

When adding codebook to an existing project:

### Step 1: Assess Current State

- [ ] What documentation exists?
- [ ] What patterns are in use?
- [ ] What standards are established?

### Step 2: Create Codebook Structure

- [ ] Create `.claude/skills/` directory
- [ ] Create `agentdocs/` directory
- [ ] Create `buildlogs/` directory
- [ ] Copy CLAUDE.md and customize

### Step 3: Migrate Existing Docs

- [ ] Move existing docs to `devdocs/` if appropriate
- [ ] Add YAML preambles to existing files
- [ ] Assign Codebook IDs
- [ ] Create index files

### Step 4: Document Current State

- [ ] Document existing patterns in `standards/`
- [ ] Note gaps in buildlog with `#gap-identified`
- [ ] Plan for completing documentation

### Step 5: Establish Baseline

- [ ] Create first buildlog with current state
- [ ] Run pre-flight checklist
- [ ] Note any failures for future resolution

<!-- PROCEDURE:onboard:END -->

---

=== TEMPLATES USED ===
<!-- AI:TEMPLATES:START -->

| Template | Purpose | Location |
|----------|---------|----------|
| preamble.template.md | Standard YAML preamble | templates/documents/ |
| weekly.buildlog.template.md | Weekly buildlog | buildlogs/templates/ |
| gitignore.template | .gitignore starter | templates/project/ |

<!-- AI:TEMPLATES:END -->

---

=== VERIFICATION CHECKLIST ===
<!-- AI:VERIFICATION:START -->

After running this skill, verify:

### Core Files
- [ ] .gitignore exists and is appropriate
- [ ] README.md has project overview
- [ ] CHANGELOG.md exists
- [ ] CLAUDE.md is customized for project

### Directory Structure
- [ ] .claude/skills/ exists
- [ ] agentdocs/ exists
- [ ] devdocs/ exists with subdirectories
- [ ] buildlogs/ exists with current week log
- [ ] standards/ exists

### Index Files
- [ ] _skill-index.md exists
- [ ] _agent-index.md exists
- [ ] _devdocs-index.md exists
- [ ] _buildlog-index.md exists

### Buildlog
- [ ] Current week's buildlog exists
- [ ] At least one entry (initialization)
- [ ] Dates are correct

### Pre-Flight
- [ ] CLAUDE.md pre-flight checklist passes

<!-- AI:VERIFICATION:END -->

---

=== COMMON ISSUES ===
<!-- AI:ISSUES:START -->

### Wrong Week Number
**Issue:** Buildlog has incorrect week
**Fix:** Check ISO 8601 week calculation; Week 01 contains first Thursday

### Existing Structure Conflicts
**Issue:** Project has existing structure that conflicts
**Fix:** Adapt codebook structure to fit; document deviations

### Permission Issues
**Issue:** Can't create files/directories
**Fix:** Check file permissions; may need manual intervention

### Missing Tech-Specific Content
**Issue:** Standards don't cover project's tech stack
**Fix:** Create tech-specific standards; note as `#gap-identified`

<!-- AI:ISSUES:END -->

---

=== RELATED SKILLS ===
<!-- AI:RELATED:START -->

| Skill | Relationship |
|-------|--------------|
| @skill(git-workflow) | Use after setup for version control |
| @skill(agent-creation) | Use when complexity requires agents |
| @skill(documentation) | Use for creating devdocs |

<!-- AI:RELATED:END -->
