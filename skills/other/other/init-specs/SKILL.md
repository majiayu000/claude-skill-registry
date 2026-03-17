---
name: init-specs
description: Initialize spec documents (requirements, specs, plans) for a new task. Creates scaffolded markdown files in specs/ directory. Use when user wants to start a new task specification.
allowed-tools: Read, Write, Glob, Bash
user-invocable: true
---

# Init Specs

## Skill Info

Part of the **spec-manager** agent. This skill scaffolds the initial spec documents for a new task.

## Input

The user provides a task title as arguments: $ARGUMENTS

Arguments may optionally include a ticket ID prefix. Supported formats:
- `/init-specs SYN-1234 User Authentication Flow` — ticket ID + title
- `/init-specs User Authentication Flow` — title only (ticket ID asked later)

If no task title is provided, ask the user for a task title before proceeding.

## Process

### Step 0: Collect Ticket ID

1. Check if the first argument matches a ticket ID pattern (e.g., `SYN-1234`, `PROJ-99`, `#123`). If so, extract it as the ticket ID and use the remaining text as the task title.
2. If no ticket ID was found in the arguments, ask the user for a ticket ID using AskUserQuestion. Provide options:
   - **Skip** — No ticket ID for this task
   - **Other** — Let the user type a ticket ID
3. The ticket ID will be used for:
   - The git branch name
   - The `Ticket` field in the requirements template

### Step 1: Slug the Task Title

Convert the task title to a URL-friendly slug:
- Lowercase all characters
- Replace spaces and special characters with hyphens
- Remove consecutive hyphens
- Trim leading/trailing hyphens

**Example**: "User Authentication Flow" -> `user-authentication-flow`

### Step 2: Create Git Branch

Create and checkout a new git branch for this task:

1. **Build branch name**:
   - If ticket ID exists: `{ticket-id}-{slug}` (e.g., `syn-1234-user-authentication-flow`)
   - If no ticket ID: `feat-{slug}` (e.g., `feat-user-authentication-flow`)
   - Entire branch name should be lowercased

2. **Check current git state**:
   - Run `git status` to check for uncommitted changes
   - If there are uncommitted changes, warn the user and ask whether to proceed (changes will carry over to the new branch) or abort

3. **Create and checkout the branch**:
   - Run `git checkout -b {branch-name}`
   - If the branch already exists, warn the user and ask whether to:
     - Switch to the existing branch (`git checkout {branch-name}`)
     - Choose a different name
     - Abort

4. **Report**: Confirm the branch was created and checked out

### Step 3: Check for Existing Directory

Check if a directory already exists at `specs/{slug}/`. If it does, warn the user and ask whether to overwrite or choose a different title.

### Step 4: Create Spec Files

Create the `specs/{slug}/` directory and the following three files inside it:

#### 1. `specs/{slug}/requirements.md`

```markdown
# Requirements: {Original Task Title}

> Created: {YYYY-MM-DD}
> Status: Draft
> Ticket: {ticket-id or "N/A"}

## Overview

<!-- Describe the task/feature at a high level. What problem does it solve? -->

## Goals

<!-- What are the primary goals of this task? -->

- [ ] Goal 1
- [ ] Goal 2

## Functional Requirements

<!-- Describe what the system should DO. Be specific and measurable. -->

### FR-1: {Requirement Name}

- **Description**:
- **Acceptance Criteria**:
  - [ ]

### FR-2: {Requirement Name}

- **Description**:
- **Acceptance Criteria**:
  - [ ]

## Non-Functional Requirements

<!-- Performance, security, scalability, maintainability, etc. -->

- **Performance**:
- **Security**:
- **Scalability**:

## Constraints

<!-- Technical constraints, time constraints, dependencies, etc. -->

-

## Out of Scope

<!-- Explicitly state what is NOT included in this task -->

-

## References

<!-- Links to related documents, designs, APIs, etc. -->

-
```

#### 2. `specs/{slug}/specs.md`

```markdown
# Specs: {Original Task Title}

> Created: {YYYY-MM-DD}
> Status: Pending (waiting for requirements)
> Requirements: [requirements.md](./requirements.md)

## Overview

<!-- This document will be generated from requirements. Run /specify-with-requirements after completing requirements. -->

## Technical Specifications

<!-- Auto-generated from requirements analysis -->

## Architecture

<!-- Component design, data flow, integrations -->

## API / Interface Design

<!-- Endpoints, function signatures, data models -->

## Error Handling

<!-- Error scenarios and handling strategies -->

## Dependencies

<!-- External and internal dependencies -->

## Open Questions

<!-- Unresolved questions to clarify -->

-
```

#### 3. `specs/{slug}/plans.md`

```markdown
# Plans: {Original Task Title}

> Created: {YYYY-MM-DD}
> Status: Pending (waiting for specs)
> Specs: [specs.md](./specs.md)

## Overview

<!-- This document will be generated from specs. Run /plan-with-specs after specs are finalized. -->

## Implementation Steps

<!-- Auto-generated from specs analysis -->

## Task Breakdown

<!-- Ordered list of implementation tasks -->

## Testing Strategy

<!-- Test plan for verification -->

## Rollback Plan

<!-- How to undo changes if needed -->

## Progress Tracking

| Step | Status | Notes |
|------|--------|-------|
|      |        |       |
```

### Step 5: Report Completion

After creating all three files, display a summary:

```
Spec documents initialized for: "{Original Task Title}"

Branch: {branch-name}
Ticket: {ticket-id or "N/A"}

Created files:
  - specs/{slug}/requirements.md  <- Write your requirements here
  - specs/{slug}/specs.md         <- Generated after /specify-with-requirements
  - specs/{slug}/plans.md         <- Generated after /plan-with-specs

Next step: Edit specs/{slug}/requirements.md with your requirements, then run:
  /specify-with-requirements {slug}
```

## Important

- Always create the `specs/` directory if it doesn't exist
- Use the actual current date for the "Created" field
- Preserve the original task title (with proper casing) in document headers
- Use the slugged version only for file names and cross-references
