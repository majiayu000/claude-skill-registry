---
name: plan-feature
description: Plan a new feature before writing code. Explores the codebase, creates a structured plan with verification criteria, and only implements after approval.
disable-model-invocation: true
argument-hint: [feature description]
---

# Plan Feature

Create a structured implementation plan before writing any code. Based on the principle that **planning before coding** prevents wasted work and produces better results.

## Usage

`/plan-feature <description of the feature>`

## Procedure

### Step 1: Understand the Request

Parse `$ARGUMENTS` to understand what feature the user wants. If the description is ambiguous, ask clarifying questions:
- What is the expected behavior?
- Are there any constraints (performance, compatibility, etc.)?
- Should this follow an existing pattern in the codebase?

### Step 2: Explore the Codebase

Before planning, understand the existing architecture. Use the Explore agent or read files directly:

1. **Find related code**: Search for files related to the feature (e.g., if adding auth, search for existing auth/user code)
2. **Understand patterns**: How does the codebase structure similar features? (routing, services, models, tests)
3. **Identify dependencies**: What existing modules will this feature interact with?
4. **Check for conventions**: Read CLAUDE.md for project-specific conventions

### Step 3: Create the Plan

Write a structured plan with these sections:

```markdown
# Feature Plan: [Feature Name]

## Scope
What this feature does and does NOT do. Explicit boundaries.

## Affected Files
- `path/to/file1.ts` — What changes and why
- `path/to/file2.ts` — What changes and why
- `path/to/new-file.ts` — NEW: What this file does

## Approach
Step-by-step implementation order:
1. First, ... (because this establishes the foundation)
2. Then, ... (because this depends on step 1)
3. Finally, ... (integration and wiring)

## Risks & Edge Cases
- Risk: [description] → Mitigation: [approach]
- Edge case: [description] → Handling: [approach]

## Verification Criteria
How to confirm the feature works:
- [ ] Unit tests pass: `[specific test command]`
- [ ] Integration test: [describe manual or automated check]
- [ ] Edge case covered: [specific scenario]
- [ ] No regressions: `[full test suite command]`
```

### Step 4: Save the Plan

Save the plan to a local file:
- Path: `.claude/plans/<feature-slug>.md`
- Create the `.claude/plans/` directory if it doesn't exist

### Step 5: Present for Approval

Show the plan to the user and ask for approval:

> "Here's the implementation plan. Should I proceed, or would you like to adjust anything?"

**Do NOT write any implementation code until the user approves the plan.**

### Step 6: Execute (After Approval)

Once approved:
1. Follow the plan step-by-step
2. After each step, verify it works before moving to the next
3. Run the verification criteria at the end
4. Report completion with a summary of what was done

If you discover the plan needs adjustment during implementation, stop and consult the user before deviating.
