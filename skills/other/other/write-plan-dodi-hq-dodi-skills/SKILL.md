---
name: write-plan
description: Use when you have a spec or requirements and need to create a step-by-step implementation plan before coding
---

# Write Plan

Create implementation plans with enough detail that an engineer with zero codebase context can execute them. Exact file paths, complete code, exact commands, bite-sized steps.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Scope Check

If the spec covers multiple independent subsystems, break into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each is responsible for.

- Each file: one clear responsibility, well-defined interface
- Files that change together should live together
- Follow established codebase patterns
- Prefer smaller focused files over large ones

## Plan Document Header

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use dodi-dev:implement to execute this plan.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [Key technologies]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts:123-145`
- Test: `tests/exact/path/to/test.ts`

- [ ] **Step 1:** [Specific action]

```typescript
// Complete code, not "add validation"
```

- [ ] **Step 2:** Verify

Run: `exact command`
Expected: [exact output]

- [ ] **Step 3:** Commit

```bash
git add [files]
git commit -m "feat: specific change"
```
````

## Guidelines

- Exact file paths always
- Complete code in plan (not "add validation" or "similar to X")
- Exact commands with expected output
- Write tests where they add value — skip tests for trivial getters/setters/CRUD
- DRY, YAGNI, frequent commits

## Plan Review Loop

After completing each chunk (≤1000 lines):

1. Dispatch plan-reviewer subagent (see plan-reviewer-prompt.md)
2. Fix issues, re-dispatch until approved (max 5 iterations)

## Execution Handoff

**"Plan saved to `docs/plans/<filename>.md`. Ready to execute?"**

When ready, invoke `dodi-dev:implement`.
