---
name: prd
description: Generate Product Requirements Documents (PRDs) in Markdown format. Use when users want to create a PRD, spec out a feature, document requirements, or plan new functionality. Triggers on requests like "create a PRD", "write requirements for", "spec out this feature", or "document this feature idea".
---

# PRD Generator

Create clear, actionable Product Requirements Documents suitable for junior developers to understand and implement.

## Workflow

1. **Receive feature request** - User describes a feature or functionality
2. **Ask clarifying questions** - 3-5 essential questions with lettered options
3. **Generate PRD** - Create structured document based on answers
4. **Save PRD** - Write to `/tasks/prd-[feature-name].md`

**Important:** Do NOT implement the feature. Only create the PRD document.

## Step 1: Clarifying Questions

Ask only critical questions where the initial prompt is ambiguous. Skip questions when answers are reasonably inferable.

**Question areas:**

- Problem/Goal - "What problem does this solve?"
- Core Functionality - "What key actions should users perform?"
- Scope/Boundaries - "What should this NOT do?"
- Success Criteria - "How will we know it's successful?"

**Format requirements:**

- Number questions (1, 2, 3)
- Letter options (A, B, C, D) for each question
- Enable responses like "1A, 2C, 3B"

**Example:**

```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Generate additional revenue

2. Who is the target user?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only

3. What is the expected scope?
   A. MVP - minimal viable implementation
   B. Full feature - complete functionality
   C. Iteration - enhance existing feature
```

## Step 2: Generate PRD

After receiving answers, generate the PRD using the structure in [references/prd-template.md](references/prd-template.md).

**Writing guidelines:**

- Write for junior developers - explicit, unambiguous, avoid jargon
- Focus on "what" and "why", not "how"
- Number all functional requirements
- Keep requirements specific and testable

## Step 3: Save PRD

Save to `/tasks/prd-[feature-name].md`

Use kebab-case for feature name (e.g., `prd-user-authentication.md`, `prd-export-dashboard.md`).

Create the `/tasks/` directory if it doesn't exist.
