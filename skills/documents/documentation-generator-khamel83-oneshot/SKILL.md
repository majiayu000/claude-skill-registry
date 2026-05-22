---
name: documentation-generator
description: "Generate and update project documentation including README, LLM-OVERVIEW, and ADRs. Ensures docs match current code state. Use when user says 'update docs', 'write README', 'generate documentation', or 'ADR'."
allowed-tools: Read, Write, Edit, Glob
---

# Documentation Generator

You are an expert at creating clear, useful project documentation.

## When To Use

- After major feature / milestone completion
- User asks "Update docs for this"
- User asks "Write the README / ADR / API docs"
- Before handing off to another engineer/agent

## Inputs

- Current codebase
- Existing docs (if any)
- PRD + feature plan(s)

## Outputs

Updated:
- `README.md` (Quick Start, features, limitations)
- `LLM-OVERVIEW.md` (architecture, current state)
- Optional new ADR(s) for decisions

## Workflow

### 1. Scan Project

- Identify main entry points
- List main modules and responsibilities
- Note current state vs documented state

### 2. Update README

Ensure README has:
- One-line description
- Problem / solution
- Quick Start (≤5 commands)
- Storage choice & upgrade trigger
- Known limitations

### 3. Update LLM-OVERVIEW

Ensure reality matches code:
- Status
- Current state
- Architecture decisions
- Recent changes

### 4. ADRs for Major Decisions

For each big decision, write ADR using template.

## README Template

```markdown
# [Project Name] - [One-line description]

**Status**: [In Development / Alpha / Beta / Production]
**Current Tier**: [Storage tier / Deployment tier]
**Upgrade Trigger**: [When to upgrade]

## What This Does
[Problem → Solution in 2-3 sentences]

## Quick Start
\`\`\`bash
git clone [repo]
cd [project]
./scripts/setup.sh
./scripts/start.sh
\`\`\`

## Features
- [Feature 1]
- [Feature 2]

## Configuration
[Environment variables or config files]

## Known Limitations
- [Limitation 1]
- [Limitation 2]
```

## LLM-OVERVIEW Template

```markdown
# LLM-OVERVIEW: [Project Name]

> Complete context for any LLM to understand this project.
> **Last Updated**: [DATE]
> **ONE_SHOT Version**: 3.1

## 1. WHAT IS THIS PROJECT?
### One-Line Description
[A tool that does X for Y people]

### The Problem It Solves
[What's painful without this?]

### Current State
- **Status**: [In Development / Alpha / Beta / Production]
- **Version**: [X.Y.Z]
- **Last Milestone**: [What was accomplished]
- **Next Milestone**: [What's being worked on]

## 2. ARCHITECTURE OVERVIEW
### Tech Stack
Language: [Python 3.11 / Node 20 / etc.]
Framework: [FastAPI / Express / etc.]
Database: [SQLite / PostgreSQL / etc.]
Deployment: [Local / systemd / Docker]

### Key Components
| Component | Purpose | Location |
|-----------|---------|----------|
| [Component] | [What it does] | [path] |

## 3. KEY FILES
- `src/main.py` - Entry point
- `src/models.py` - Data models
- `scripts/` - Automation scripts

## 4. CURRENT STATE
### What Works
- [Feature 1]

### What's In Progress
- [Feature 2 - 50%]

### What's Broken
- [Issue 1 - workaround]

## 5. HOW TO WORK ON THIS PROJECT
\`\`\`bash
./scripts/setup.sh
./scripts/start.sh
pytest tests/
\`\`\`
```

## ADR Template (Nygard Format)

```markdown
# ADR-[NUMBER]: [Title]

**Date**: YYYY-MM-DD
**Status**: [Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue we're facing?]

## Decision
[What is the change we're proposing?]

## Rationale
[Why is this the best approach?]

## Consequences

### Positive
- [Benefit 1]

### Negative
- [Trade-off 1]

## Alternatives Considered
- Alternative 1: [Description] - Rejected because [reason]
```

## Anti-Patterns

- Generating generic docs that don't match the code
- Duplicating content instead of pointing to canonical sections
- Outdated Quick Start commands
- Missing version/status information

## Keywords

docs, documentation, README, LLM-OVERVIEW, ADR, generate docs, update docs
