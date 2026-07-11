---
name: 051-design-two-steps-methods
description: Use when a complex or risky code change should be split into Kent Beck's two-step method by first making the change easy through behavior-preserving preparatory refactoring, then making the intended behavior change once the design supports it. This should trigger for requests such as Apply two-step change; Make this risky change safer; Refactor before changing behavior; Separate preparation from behavior change. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# Two-Step Change Method

Guide Java developers through complex or risky changes by keeping design preparation separate from behavior modification. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Clarifying the intended behavior change before editing
- Identifying design obstacles that make the change difficult or risky
- Step 1: behavior-preserving preparatory refactoring that makes the change easy
- Validation that Step 1 preserves existing behavior
- Step 2: the smallest intended behavior change after the design supports it
- Verification that Step 2 delivers the intended behavior
- Handoff to focused Java, framework, persistence, messaging, API, or testing skills while preserving the two-step sequence

## Constraints

Separate behavior-preserving preparation from behavior-changing work, and validate after each step.

- **MUST**: State the intended behavior change before proposing preparatory refactoring
- **MUST**: Keep Step 1 behavior-preserving; do not mix broad refactoring with the intended behavior change
- **MUST**: Verify existing behavior after Step 1 using the project-appropriate tests, build, characterization tests, or manual checks
- **MUST**: Make Step 2 only after the design has been prepared and validated
- **MUST**: Verify the intended behavior after Step 2 with focused tests and relevant build checks
- **MUST**: Record assumptions and risks when preparation cannot be fully separated from behavior change

## When to use this skill

- Apply two-step change
- Make this risky change safer
- Refactor before changing behavior
- Separate preparation from behavior change
- Make the change easy, then make the easy change

## Workflow

1. **Define the intended change**

Read `references/051-design-two-steps-methods.md`, inspect the relevant code and tests, and state the exact behavior or capability that must change. Identify why the current design makes the change complex, risky, or hard to verify.

2. **Plan preparatory refactoring**

Choose the smallest behavior-preserving refactoring that reduces the obstacle: extract method or class, clarify names, isolate dependencies, add seams for testing, move responsibilities, improve types, or add characterization tests before touching behavior.

3. **Make the change easy**

Apply Step 1 as focused preparatory refactoring only. Keep commits, notes, or task boundaries clear enough that reviewers can see no intended behavior change is included.

4. **Validate preserved behavior**

Run the relevant existing tests, build checks, characterization tests, or manual verification. If behavior changes unexpectedly, fix or revert the preparation before proceeding.

5. **Make the easy behavior change**

Apply the smallest intended behavior change now that the design supports it. Use focused Java, framework, persistence, messaging, API, or testing skills when detailed implementation guidance is needed.

6. **Verify and report the outcome**

Verify the intended behavior with targeted tests and relevant project validation. Report what was preparation, what changed behavior, what was verified after each step, and any remaining risks.

## Reference

For detailed guidance, examples, and constraints, see [references/051-design-two-steps-methods.md](references/051-design-two-steps-methods.md).
