---
name: project-memory
description: Set up and maintain a structured project memory system in docs/project_notes/ that tracks bugs with solutions, architectural decisions, key project facts, and work history. Use this skill when asked to "set up project memory", "track our decisions", "log a bug fix", "update project memory", or "initialize memory system". Configures both CLAUDE.md and AGENTS.md to maintain memory awareness across different AI coding tools.
---

# Project Memory

## Table of Contents

- [Overview](#overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Core Capabilities](#core-capabilities)
  - [1. Initial Setup - Create Memory Infrastructure](#1-initial-setup---create-memory-infrastructure)
  - [2. Configure CLAUDE.md - Memory-Aware Behavior](#2-configure-claudemd---memory-aware-behavior)
  - [3. Configure AGENTS.md - Multi-Tool Support](#3-configure-agentsmd---multi-tool-support)
  - [4. Searching Memory Files](#4-searching-memory-files)
  - [5. Updating Memory Files](#5-updating-memory-files)
  - [6. Memory File Maintenance](#6-memory-file-maintenance)
- [Templates and References](#templates-and-references)
- [Example Workflows](#example-workflows)
- [Integration with Other Skills](#integration-with-other-skills)
- [Success Criteria](#success-criteria)

## Overview

Maintain institutional knowledge for projects by establishing a structured memory system in `docs/project_notes/`. This skill sets up four key memory files (bugs, decisions, key facts, issues) and configures CLAUDE.md and AGENTS.md to automatically reference and maintain them. The result is a project that remembers past decisions, solutions to problems, and important configuration details across coding sessions and across different AI tools.

## When to Use This Skill

Invoke this skill when:

- Starting a new project that will accumulate knowledge over time
- The project already has recurring bugs or decisions that should be documented
- The user asks to "set up project memory" or "track our decisions"
- The user wants to log a bug fix, architectural decision, or completed work
- Encountering a problem that feels familiar ("didn't we solve this before?")
- Before proposing an architectural change (check existing decisions first)
- Working on projects with multiple developers or AI tools (Claude Code, Cursor, etc.)

## Core Capabilities

### 1. Initial Setup - Create Memory Infrastructure

When invoked for the first time in a project, create the following structure:

```
docs/
└── project_notes/
    ├── bugs.md         # Bug log with solutions
    ├── decisions.md    # Architectural Decision Records
    ├── key_facts.md    # Project configuration and constants
    └── issues.md       # Work log with ticket references
```

**Directory naming rationale:** Using `docs/project_notes/` instead of `memory/` makes it look like standard engineering organization, not AI-specific tooling. This increases adoption and maintenance by human developers.

**Initial file content:** Copy templates from the `references/` directory in this skill:
- Use `references/bugs_template.md` for initial `bugs.md`
- Use `references/decisions_template.md` for initial `decisions.md`
- Use `references/key_facts_template.md` for initial `key_facts.md`
- Use `references/issues_template.md` for initial `issues.md`

Each template includes format examples and usage tips.

### 2. Configure CLAUDE.md - Memory-Aware Behavior

Add or update the following section in the project's `CLAUDE.md` file:

```markdown
## Project Memory System

This project maintains institutional knowledge in `docs/project_notes/` for consistency across sessions.

### Memory Files

- **bugs.md** - Bug log with dates, solutions, and prevention notes
- **decisions.md** - Architectural Decision Records (ADRs) with context and trade-offs
- **key_facts.md** - Project configuration, credentials, ports, important URLs
- **issues.md** - Work log with ticket IDs, descriptions, and URLs

### Memory-Aware Protocols

**Before proposing architectural changes:**
- Check `docs/project_notes/decisions.md` for existing decisions
- Verify the proposed approach doesn't conflict with past choices
- If it does conflict, acknowledge the existing decision and explain why a change is warranted

**When encountering errors or bugs:**
- Search `docs/project_notes/bugs.md` for similar issues
- Apply known solutions if found
- Document new bugs and solutions when resolved

**When looking up project configuration:**
- Check `docs/project_notes/key_facts.md` for credentials, ports, URLs, service accounts
- Prefer documented facts over assumptions

**When completing work on tickets:**
- Log completed work in `docs/project_notes/issues.md`
- Include ticket ID, date, brief description, and URL

**When user requests memory updates:**
- Update the appropriate memory file (bugs, decisions, key_facts, or issues)
- Follow the established format and style (bullet lists, dates, concise entries)

### Style Guidelines for Memory Files

- **Prefer bullet lists over tables** for simplicity and ease of editing
- **Keep entries concise** (1-3 lines for descriptions)
- **Always include dates** for temporal context
- **Include URLs** for tickets, documentation, monitoring dashboards
- **Manual cleanup** of old entries is expected (not automated)
```

### 3. Configure AGENTS.md - Multi-Tool Support

If the project has an `AGENTS.md` file (used for agent workflows or multi-tool projects), add the same memory protocols. This ensures consistency whether using Claude Code, Cursor, GitHub Copilot, or other AI tools.

**If AGENTS.md exists:** Add the same "Project Memory System" section as above.

**If AGENTS.md doesn't exist:** Ask the user if they want to create it. Many projects use multiple AI tools and benefit from shared memory protocols.

### 4. Searching Memory Files

When encountering problems or making decisions, proactively search memory files:

**Search bugs.md:**
```bash
# Look for similar errors
grep -i "connection refused" docs/project_notes/bugs.md

# Find bugs by date range
grep "2025-01" docs/project_notes/bugs.md
```

**Search decisions.md:**
```bash
# Check for decisions about a technology
grep -i "database" docs/project_notes/decisions.md

# Find all ADRs
grep "^### ADR-" docs/project_notes/decisions.md
```

**Search key_facts.md:**
```bash
# Find database connection info
grep -A 5 "Database" docs/project_notes/key_facts.md

# Look up service accounts
grep -i "service account" docs/project_notes/key_facts.md
```

**Use Grep tool for more complex searches:**
- Search across all memory files: `Grep(pattern="oauth", path="docs/project_notes/")`
- Context-aware search: `Grep(pattern="bug", path="docs/project_notes/bugs.md", -A=3, -B=3)`

### 5. Updating Memory Files

When the user requests updates or when documenting resolved issues, update the appropriate memory file:

**Adding a bug entry:**
```markdown
### YYYY-MM-DD - Brief Bug Description
- **Issue**: What went wrong
- **Root Cause**: Why it happened
- **Solution**: How it was fixed
- **Prevention**: How to avoid it in the future
```

**Adding a decision:**
```markdown
### ADR-XXX: Decision Title (YYYY-MM-DD)

**Context:**
- Why the decision was needed
- What problem it solves

**Decision:**
- What was chosen

**Alternatives Considered:**
- Option 1 -> Why rejected
- Option 2 -> Why rejected

**Consequences:**
- Benefits
- Trade-offs
```

**Adding key facts:**
- Organize by category (GCP Project, Database, API, Local Development, etc.)
- Use bullet lists for clarity
- Include both production and development details
- Add URLs for easy navigation
- See `references/key_facts_template.md` for security guidelines on what NOT to store

**Adding work log entry:**
```markdown
### YYYY-MM-DD - TICKET-ID: Brief Description
- **Status**: Completed / In Progress / Blocked
- **Description**: 1-2 line summary
- **URL**: https://jira.company.com/browse/TICKET-ID
- **Notes**: Any important context
```

### 6. Memory File Maintenance

**Periodically clean old entries:**
- User is responsible for manual cleanup (no automation)
- Remove very old bug entries (6+ months) that are no longer relevant
- Archive completed work from issues.md (3+ months old)
- Keep all decisions (they're lightweight and provide historical context)
- Update key_facts.md when project configuration changes

**Conflict resolution:**
- If proposing something that conflicts with decisions.md, explain why revisiting the decision is warranted
- Update the decision entry if the choice changes
- Add date of revision to show evolution

## Templates and References

This skill includes template files in `references/` that demonstrate proper formatting:

- **references/bugs_template.md** - Bug entry format with examples
- **references/decisions_template.md** - ADR format with examples
- **references/key_facts_template.md** - Key facts organization with examples (includes security guidelines)
- **references/issues_template.md** - Work log format with examples

When creating initial memory files, copy these templates to `docs/project_notes/` and customize them for the project.

## Example Workflows

### Scenario 1: Encountering a Familiar Bug

```
User: "I'm getting a 'connection refused' error from the database"
-> Search docs/project_notes/bugs.md for "connection"
-> Find previous solution: "Use AlloyDB Auth Proxy on port 5432"
-> Apply known fix
```

### Scenario 2: Proposing an Architectural Change

```
Internal: "User might benefit from using SQLAlchemy for migrations"
-> Check docs/project_notes/decisions.md
-> Find ADR-002: Already decided to use Alembic
-> Use Alembic instead, maintaining consistency
```

### Scenario 3: User Requests Memory Update

```
User: "Add that CORS fix to our bug log"
-> Read docs/project_notes/bugs.md
-> Add new entry with date, issue, solution, prevention
-> Confirm addition to user
```

### Scenario 4: Looking Up Project Configuration

```
Internal: "Need to connect to database"
-> Check docs/project_notes/key_facts.md
-> Find Database Configuration section
-> Use documented connection string and credentials
```

## Tips for Effective Memory Management

1. **Be proactive**: Check memory files before proposing solutions
2. **Be concise**: Keep entries brief (1-3 lines for descriptions)
3. **Be dated**: Always include dates for temporal context
4. **Be linked**: Include URLs to tickets, docs, monitoring dashboards
5. **Be selective**: Focus on recurring or instructive issues, not every bug

## Integration with Other Skills

The project-memory skill complements other skills:

- **requirements-documenter**: Requirements -> Decisions (ADRs reference requirements)
- **root-cause-debugger**: Bug diagnosis -> Bug log (document solutions after fixes)
- **code-quality-reviewer**: Quality issues -> Decisions (document quality standards)
- **docs-sync-editor**: Code changes -> Key facts (update when config changes)

When using these skills together, consider updating memory files as a follow-up action.

## Success Criteria

This skill is successfully deployed when:

- `docs/project_notes/` directory exists with all four memory files
- CLAUDE.md includes "Project Memory System" section with protocols
- AGENTS.md includes the same protocols (if file exists or user requested)
- Memory files follow template format and style guidelines
- AI assistant checks memory files before proposing changes
- User can easily request memory updates ("add this to bugs.md")
- Memory files look like standard engineering documentation, not AI artifacts
