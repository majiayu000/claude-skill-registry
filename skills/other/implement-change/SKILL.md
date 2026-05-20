---
name: implement-change
description: >-
  Execute code changes from an implementation plan. Use when someone says "implement this",
  "build this", "code this", "start building", "let's implement", "execute the plan",
  "make the changes", "do the work", or has an approved implementation plan ready for coding.
  Takes implementation plans and produces working code, phase by phase with verification.
---

# Implement Change

Execute an implementation plan phase by phase, producing working code with verification at each step.

## Design Philosophy

While implementing, consult [references/software-design-philosophy.md](references/software-design-philosophy.md) for code-level design principles. Watch for red flags: shallow modules, information leakage, pass-through methods, temporal decomposition.

## Principles

- **Understand before coding** — read all relevant files thoroughly first
- **Phase by phase** — complete one phase before starting the next
- **Verify as you go** — run checks after each phase, fix issues before proceeding
- **Adapt to reality** — plans are guides, not rigid scripts; handle mismatches thoughtfully
- **Track progress** — keep todos updated, check off items as completed

## Input

This skill expects an implementation plan (from `/dev-skills:implementation-planning`). If no plan exists, create one first — don't start coding without a plan.

## Process

### 1. Understand the Work

Read the plan completely. Read all files mentioned or related. Create a todo list tracking each phase.

If the plan has checkboxes, check for existing `[x]` marks — resume from first unchecked item.

### 2. Implement Phase by Phase

For each phase:

1. **Implement** — make the code changes
2. **Verify** — run the specified checks (tests, typecheck, lint)
3. **Fix** — address any failures before moving on
4. **Update** — mark todos complete, check boxes in plan file

### 3. Handle Mismatches

When reality differs from the plan, surface it:

- What the plan says vs what you found
- Why it matters
- How you suggest proceeding

Don't silently deviate — get guidance.

### 4. Final Verification

After all phases complete:
- Run full test suite
- Run typecheck and lint
- Verify the original acceptance criteria are met

## Working Guidelines

**Do:**
- Read files thoroughly — full files for small ones, targeted sections for large ones
- Follow existing code patterns in the codebase
- Keep changes focused on the plan scope
- Update progress frequently

**Don't:**
- Make unrelated "improvements"
- Skip verification steps
- Proceed past failures without fixing them
- Assume — ask when unclear

## Progress Tracking

Use todos to track each phase, verification steps, and blockers.

Update the plan file checkboxes as you complete items:
```markdown
- [x] Completed item
- [ ] Pending item
```

## Resuming Work

If picking up existing work:
- Check for `[x]` marks in the plan
- Trust completed work unless something seems wrong
- Start from first unchecked item
- Verify previous work only if you hit unexpected issues

## Handoffs

- After all phases pass verification → suggest `/dev-skills:qa-test` for browser verification
- If acceptance criteria need revision during implementation → flag it, don't modify them
