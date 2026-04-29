---
name: triage-issue
description: Investigate a reported bug to root cause, then emit a TDD-shaped fix plan as an issue artifact. Trigger when the user reports a bug, says "triage", asks for issue investigation, or wants a fix plan before code changes.
---

Investigate, find root cause, emit a fix plan shaped as RED-GREEN cycles. Mostly hands-off — minimize user prompts.

## Process

### 1. Capture the problem (one prompt max)

If the user has not already described the bug, ask exactly one question: "What's the problem you're seeing?" Then start investigating. No follow-ups yet.

### 2. Explore and diagnose

Dispatch an Explore agent. Find:
- **Where** the bug manifests (entry points, UI, API responses)
- **What** code path executes (trace the flow)
- **Why** it fails (root cause, not just symptom)
- **Related** code (similar patterns, adjacent modules, existing tests)

Use `git --no-pager grep -n -C 3 <pattern>` and `ast-grep run -p '<pattern>' -l <lang> -C 3` for structural traces.

### 3. Identify the fix shape

From the investigation, lock:
- Minimal change targeting root cause
- Affected modules and their interface contracts
- Behaviors needing test coverage
- Classification: regression / missing feature / design flaw

### 4. Design the TDD fix plan

Ordered list of RED-GREEN cycles. Each cycle is a vertical slice through public interfaces.

**Rules:**
- Tests assert on **observable behavior** through public interfaces, never internal state.
- One test at a time. Vertical slicing — never "all tests first, then all code".
- Each test must survive radical internal refactors.
- Include a final REFACTOR step if cleanup is warranted.
- **Durability gate:** the plan reads like a spec, not a patch. No file paths, no line numbers, no internal struct names.

### 5. Emit the issue

`gh issue create --title "<bug summary>" --body-file <tmp>` using the template below. Do NOT ask the user to review first — file it, then share the URL and a one-line root-cause summary.

## Template

```
## Problem
- Actual: what happens
- Expected: what should happen
- Repro: numbered steps (or "non-deterministic; observed in <context>")

## Root Cause Analysis
- Code path involved (described by module + behavior, not file paths)
- Why current code fails (the contract violation, not the line)
- Contributing factors

## TDD Fix Plan
1. **RED:** Write a test asserting <observable behavior>.
   **GREEN:** Minimal change to make it pass.
2. **RED:** Write a test asserting <next observable behavior>.
   **GREEN:** Minimal change to make it pass.
**REFACTOR:** Cleanup after green (extract, rename, deduplicate). Optional.

## Acceptance Criteria
- [ ] Behavior X visible from public interface
- [ ] Behavior Y visible from public interface
- [ ] All new tests pass
- [ ] Existing tests still pass
```

## RED-GREEN Examples Across Stacks

**Python (pytest):**
1. **RED:** `test_balance_returns_zero_for_new_account` asserts `account_service.balance(new_id) == Decimal("0")`.
   **GREEN:** Initialize default balance in account constructor.

**Rust (cargo test):**
1. **RED:** `#[test] fn balance_returns_zero_for_new_account` asserts `service.balance(id)? == Decimal::ZERO`.
   **GREEN:** Initialize default balance in `Account::new`.

## ODIN integration

The issue artifact produced here is the **input contract** for `odin:debug` (executes investigation extension if needed) and `odin:test-driven` (drives the RED→GREEN→REFACTOR cycles). Hand off the issue URL explicitly.
