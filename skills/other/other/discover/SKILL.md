---
name: discover
description: Read project docs, clarify requirements, and help create Docs/PRODUCT.md.
version: 1.1.0
tags: [discovery, docs, requirements]
owner: orchestration
status: active
---

# Discover Skill

Read Docs/ folder, understand the project, and help create PRODUCT.md.

## Overview

This skill guides the discovery phase where you:
1. Read all documents in the Docs/ folder (recursively)
2. Understand the project vision and context
3. Ask clarifying questions
4. Help the user create a well-structured Docs/PRODUCT.md

## Usage

```
/discover
```

## Prerequisites

- Access to project documentation (`Docs/` or fallback locations).

## Purpose

**Human-guided discovery** - Don't assume, ask questions.

The goal is to build shared understanding before any code is written. By the end of this phase, both you and the user should have a clear picture of:

- What problem we're solving
- What success looks like
- Key constraints and requirements
- Technical approach (high-level)

## Workflow Steps

### Step 1: Find and Read Documents

Look for documentation in these locations (in order of priority):

**Primary (preferred):**
- `Docs/` folder - Primary documentation folder

**Fallbacks (legacy):**
- `Documents/` folder - Legacy naming convention
- `docs/` folder - Lowercase alternative
- `README.md` - If no docs folder exists
- Any `.md` files in the root

**Flexible Structure:**
The Docs/ folder can have ANY structure. The only requirement is that `PRODUCT.md`
exists somewhere in Docs/ (usually at the root). All other documentation can be
organized however makes sense for the project.

**How to search:**
```
Glob: Docs/**/*.md
```

This finds all `.md` files in Docs/ and all subfolders, regardless of structure.

If Docs/ doesn't exist, check fallback locations. List all found documents and read each one.

### Step 2: Summarize Understanding

After reading, present a summary:

```markdown
## What I Understand

### Project Purpose
[Brief summary of what the project does]

### Current State
[Is this greenfield or existing code? What exists?]

### Feature/Goal
[What we're trying to build or achieve]

### Key Constraints
[Technical, timeline, compatibility requirements]

### Stakeholders
[Who will use this? Who needs to approve?]
```

### Step 3: Ask Clarifying Questions

Present 3-5 targeted questions. Examples:

- "What's the MVP scope vs. nice-to-haves?"
- "Are there existing patterns I should follow?"
- "What's the testing strategy preference?"
- "Are there any hard deadlines?"
- "Who needs to review before merge?"

**Important**: Wait for answers before proceeding.

### Step 4: Capture Context

Create or update `CONTEXT.md` with:
- Decisions made during discussion
- User preferences
- Constraints confirmed
- Out-of-scope items

### Step 5: Draft Docs/PRODUCT.md

When ready, propose a Docs/PRODUCT.md draft:

```markdown
# Feature Name
[Clear, specific name]

## Summary
[50-500 characters describing what it does]

## Problem Statement
[Why this feature is needed - minimum 100 characters]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
[Minimum 3 criteria]

## Example Inputs/Outputs

### Example 1
```
// Input
{example input}
// Output
{expected output}
```

### Example 2
```
// Input
{example input}
// Output
{expected output}
```

## Technical Constraints
[Performance, security, compatibility requirements]

## Testing Strategy
[How to test this feature]

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No security issues
```

### Step 6: Get Approval

Ask: "Should I save this as Docs/PRODUCT.md?"

Only save after user confirms. Create the Docs/ folder if it doesn't exist.

## Key Behaviors

### DO
- Read ALL available documents before asking questions
- Present your understanding for validation
- Ask targeted, specific questions
- Wait for answers before proceeding
- Offer to create PRODUCT.md when ready
- Be explicit about what you don't know

### DON'T
- Assume requirements not explicitly stated
- Skip to planning without understanding
- Create PRODUCT.md without approval
- Make architectural decisions without discussion
- Rush through discovery

## Document Locations

Check these paths (in priority order):
1. `Docs/` - Primary documentation folder (preferred)
2. `Documents/` - Legacy documentation folder (fallback)
3. `docs/` - Lowercase alternative (fallback)
4. `README.md` - Project readme (minimal fallback)
5. `./*.md` - Any markdown files in root (last resort)

## Output Files

| File | Purpose |
|------|---------|
| `CONTEXT.md` | Decisions and preferences from discussion |
| `Docs/PRODUCT.md` | Feature specification (after approval) |

**Note:** PRODUCT.md should be created inside Docs/ folder, not in project root.

## State Update

After completing discovery:
- Create/update `workflow_state` in SurrealDB
- Set `phase_status.discussion = "completed"`
- Set `current_phase = 1` (ready for planning)

## Transition

When Docs/PRODUCT.md is created and approved:

```
Discovery complete! Docs/PRODUCT.md created.

Next steps:
  /plan - Create task breakdown from this specification

Or if you want to review the spec again:
  Read Docs/PRODUCT.md and let me know any changes needed.
```

## Example Session

```
User: /discover

Claude: I'll explore your project documentation to understand what we're building.

Let me check for documents...

Searching: Docs/**/*.md

Found:
  - Docs/product-vision.md
  - Docs/design/overview.md
  - Docs/design/api-design.md

Reading each document...

## What I Understand

### Project Purpose
This is a task management API that allows teams to track work items with assignments, priorities, and due dates.

### Current State
Greenfield project. No existing code yet. Using TypeScript + Express + PostgreSQL stack.

### Feature/Goal
Building the core task CRUD operations with user assignment.

### Key Constraints
- REST API design (from Docs/architecture/api-design.md)
- Must support bulk operations
- Auth handled separately (OAuth assumed)

## Questions

1. Should tasks support subtasks, or keep it flat for MVP?
2. What's the priority model - numeric (1-5) or labels (high/medium/low)?
3. Are there any rate limiting requirements?
4. Who will be calling this API - web app, mobile, or both?

User: Keep flat for MVP. Use labels. No rate limits yet. Web app only for now.

Claude: Got it. Let me capture that in CONTEXT.md...

Based on our discussion, here's a draft Docs/PRODUCT.md:

[Shows draft]

Should I save this as Docs/PRODUCT.md?

User: Yes, looks good.

Claude: Created Docs/PRODUCT.md

Discovery complete! You can now:
  /plan - Create task breakdown from this specification
```

## Outputs

- `Docs/PRODUCT.md` created or updated with validated structure.

## Error Handling

- If required documentation is missing, stop and request sources before drafting PRODUCT.md.

## Related Skills

- `/plan` - Next step after discovery
- `/status` - Check current progress
- `/orchestrate` - Full automated workflow (alternative)
