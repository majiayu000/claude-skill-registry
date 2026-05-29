---
name: feature-plan
description: "[Skill] Create detailed implementation plans for features. Asks clarifying questions, suggests solutions, proposes architecture, and outputs a structured plan document. Use when user wants to plan a feature before coding."
argument-hint: [feature description or requirements]
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion
---

Create a comprehensive implementation plan for $ARGUMENTS. This skill helps transform vague requirements into actionable, detailed plans before any code is written.

## Planning Process

### Phase 1: Understand & Clarify

First, analyze the provided requirements and identify:
- **Missing information**: What critical details are not specified?
- **Ambiguous points**: What could be interpreted multiple ways?
- **Assumptions**: What are you assuming that should be confirmed?
- **Dependencies**: What existing systems/code does this interact with?

Use `AskUserQuestion` to clarify ALL unclear points before proceeding. Group related questions together. Examples:
- "Should this feature be accessible to all users or specific roles?"
- "What's the expected data volume/scale?"
- "Are there existing patterns in the codebase to follow?"
- "What's the error handling strategy?"

**Do NOT proceed until you have enough clarity to propose solutions.**

### Phase 2: Explore Codebase

Before suggesting solutions, explore the existing codebase to understand:
- Current architecture and patterns
- Related existing implementations
- Available utilities, hooks, and shared components
- Database schema / API structure (if relevant)
- Testing patterns in use

### Phase 3: Suggest Solutions

Present 2-3 distinct approaches with trade-offs:

```
## Proposed Solutions

### Option A: [Name]
**Approach**: Brief description
**Pros**: List benefits
**Cons**: List drawbacks
**Best for**: When this option is ideal

### Option B: [Name]
**Approach**: Brief description
**Pros**: List benefits
**Cons**: List drawbacks
**Best for**: When this option is ideal
```

Use `AskUserQuestion` to let the user pick their preferred approach. Include a recommendation if one option is clearly better for their context.

### Phase 4: Gather Resources

Ask the user for any helpful resources:
- Documentation links
- Design files / mockups
- Example implementations to reference
- API specifications
- Related PRs or issues

### Phase 5: Create Detailed Plan

After user confirms the approach, create the full plan document.

## Output Format

Save the plan to `.plans/<index>--<plan-name>--<date>.md`

**Naming rules:**
- `<index>`: 3-digit sequential number (001, 002, etc.) - check existing files in `.plans/`
- `<plan-name>`: kebab-case summary (e.g., `user-authentication-flow`, `product-gallery-redesign`)
- `<date>`: Format `MM-DD-YYYY`

**Document structure:**

```markdown
# [Plan Title]

> **Created**: [Date]
> **Status**: Draft | Ready | In Progress | Completed

---

## Original Prompt

[Paste the exact user input/requirements here]

---

## Summary

[2-3 sentence overview of what this plan covers]

---

## Requirements

### Functional Requirements
- [ ] FR1: Description
- [ ] FR2: Description

### Non-Functional Requirements
- [ ] NFR1: Performance, security, accessibility, etc.

### Out of Scope
- Item 1 (explicitly excluded)

---

## Technical Approach

### Solution Overview
[Describe the chosen approach in 1-2 paragraphs]

### Architecture Diagram (if applicable)
[ASCII diagram or description of component relationships]

---

## Implementation Structure

### Files to Create
| File | Purpose |
|------|---------|
| `path/to/file.ts` | Description |

### Files to Modify
| File | Changes |
|------|---------|
| `path/to/existing.ts` | What changes |

### Folder Structure
```plaintext
src/
├── features/
│   └── [feature-name]/
│       ├── components/
│       ├── hooks/
│       ├── utils/
│       ├── types.ts
│       └── index.ts
```

---

## Instructions

1. **Read the requirements** carefully from $ARGUMENTS
2. **Ask clarifying questions** - do not skip this step
3. **Explore the codebase** to understand existing patterns
4. **Present solution options** with clear trade-offs
5. **Let user choose** their preferred approach
6. **Ask for resources** they want to reference
7. **Generate the plan** with all sections
8. **Save to `.plans/` folder** with proper naming
9. **Keep it under 500 lines** - be concise, use tables, avoid verbose explanations

## Important Notes

- Always save the original prompt at the top of the document
- Check `.plans/` folder for existing files to determine the next index
- Create the `.plans/` folder if it doesn't exist
- Focus on actionable items, not theoretical discussions
- Include code structure and type definitions
- Be specific about file paths relative to project root
- The plan should be self-contained - anyone should understand it without extra context
