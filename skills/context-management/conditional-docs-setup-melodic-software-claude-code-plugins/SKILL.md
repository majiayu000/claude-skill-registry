---
name: conditional-docs-setup
description: Set up conditional documentation loading to prevent context pollution. Use when organizing project docs, implementing progressive disclosure, or reducing CLAUDE.md token consumption with on-demand loading.
allowed-tools: Read, Write
---

# Conditional Docs Setup Skill

Set up conditional documentation loading to prevent context pollution.

## When to Use

- Setting up documentation for a new project
- Reducing context pollution in existing projects
- Creating just-in-time documentation loading
- Optimizing agent context usage

## Core Concept

Load documentation only when conditions match the current task.

> "IMPORTANT: Only read the documentation if any one of the conditions match your task."

## Setup Workflow

### Step 1: Inventory Documentation

List all documentation files in the project:

```bash
# Find documentation files
find . -name "*.md" -path "*/docs/*"
find . -name "README*"
find . -name "CONTRIBUTING*"
```

### Step 2: Categorize by Purpose

Group documentation by what it helps with:

| Category | Examples |
| --- | --- |
| Setup | README, INSTALL, CONTRIBUTING |
| API | api-reference, endpoints, schemas |
| Architecture | design-docs, system-overview |
| Features | feature-specific guides |
| Testing | test-patterns, fixtures |

### Step 3: Define Loading Conditions

For each document, identify when it's relevant:

```markdown
- docs/api-reference.md
  - Conditions:
    - When working with API endpoints
    - When adding new routes
    - When modifying request/response formats

- docs/database-schema.md
  - Conditions:
    - When modifying database tables
    - When adding new models
    - When writing migrations
```

### Step 4: Create Conditional Docs File

Create the conditional documentation manifest:

```markdown
# Conditional Documentation

This helps determine what documentation to read based on
the specific changes you need to make in the codebase.

IMPORTANT: Only read documentation if conditions match your task.

---

- README.md
  - Conditions:
    - When first understanding the project
    - When setting up the development environment

- docs/api/endpoints.md
  - Conditions:
    - When working with REST endpoints
    - When adding new API routes

- docs/database/schema.md
  - Conditions:
    - When modifying database tables
    - When creating migrations

- docs/testing/patterns.md
  - Conditions:
    - When writing new tests
    - When debugging test failures
```

### Step 5: Integrate with Commands

Add conditional docs check to planning commands:

```markdown
## Relevant Documentation

Read `.claude/commands/conditional_docs.md` to check if your task
requires additional documentation. If your task matches any conditions
listed, include those documentation files.
```

## Condition Writing Guidelines

### Be Specific

```markdown
# Good - Specific conditions
- When adding a new API endpoint
- When modifying user authentication

# Bad - Vague conditions
- When doing backend work
- When coding
```

### Cover Common Scenarios

```markdown
- docs/auth.md
  - Conditions:
    - When implementing login/logout
    - When adding new permissions
    - When debugging auth issues
    - When integrating OAuth
    - When working with sessions
```

### Avoid Overlap

Each document should have distinct conditions:

```markdown
# Good - Distinct conditions
- api-reference.md → API endpoints
- database-schema.md → Database tables

# Bad - Overlapping conditions
- api-reference.md → When doing backend work
- database-schema.md → When doing backend work
```

## Maintenance Workflow

### When Documentation is Added

1. Create the new documentation file
2. Add entry to conditional_docs.md
3. Define appropriate loading conditions

### When Documentation is Updated

1. Review existing conditions
2. Add/remove conditions as needed
3. Update documentation content

### When Documentation is Removed

1. Delete the documentation file
2. Remove entry from conditional_docs.md

## Template: Conditional Docs File

```markdown
# Conditional Documentation

This helps determine what documentation to read based on
the specific changes you need to make in the codebase.

IMPORTANT: Only read documentation if conditions match your task.
Excessive documentation loading wastes context and reduces focus.

---

## Project Setup

- README.md
  - Conditions:
    - When first understanding the project
    - When setting up development environment
    - When learning available commands

## Backend

- docs/api/reference.md
  - Conditions:
    - When working with API endpoints
    - When adding new routes

- docs/database/schema.md
  - Conditions:
    - When modifying database tables
    - When writing migrations

## Frontend

- docs/components/guide.md
  - Conditions:
    - When creating new components
    - When modifying UI patterns

## Testing

- docs/testing/patterns.md
  - Conditions:
    - When writing tests
    - When debugging test failures
```

## Memory References

- @conditional-docs-pattern.md - Full pattern documentation
- @minimum-context-principle.md - Why this matters
- @one-agent-one-purpose.md - Context affects focus

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
