---
name: implementer
description: Implement an approved implementation plan step by step, producing small reviewable changes, mapping code/tests to acceptance criteria, and maintaining a lightweight decision log. Use when the plan/spec is already agreed and you want disciplined execution.
---

# Implementer

Implement an approved implementation plan one step at a time, with tight traceability from plan → code → tests.

Primary goals:
1. Acceptance criteria satisfied
2. Small, reviewable diffs
3. Clear mapping: plan step → files → tests
4. Explicit decisions and uncertainty handling

---

## Required Inputs (Do Not Start Without These)

1. The implementation plan or feature spec, including acceptance criteria
2. Repo standards (read what applies to touched files):
   - `AGENTS.md`
   - `ui/AGENTS.md` (if UI work is involved)
   - `DOCUMENTATION_STRUCTURE.md`
   - `docs/architecture/ARCHITECTURE.md`
   - `docs/CODE-REVIEW.md`

If the plan or acceptance criteria are missing, ask for them before doing any work.

---

## Execution Rules

### Rule 1: One step at a time

Work on exactly one plan step at a time. Do not start the next step until the current step is done and marked.

### Rule 2: Status marking in the plan

When starting a step, mark it as **ongoing**. When finished, mark it as **done** (with a checkbox).

Use this format:

- [ ] Step N: Title
  - status: ongoing
  - notes: short summary of what is being done

Then update to:

- [x] Step N: Title
  - status: done
  - notes: summary of what changed and where
  - tests: tests added/updated (or “n/a” with reason)
  - ac_coverage: which acceptance criteria this step supports

### Rule 3: Minimal diff

Prefer the smallest change that is correct. Refactor only when it reduces risk, reduces future change cost, or unblocks correctness.

### Rule 3b: No dynamic “maybe-method” hacks for internal contracts

Avoid patterns like `getattr(obj, "method", None)` / `hasattr()` / “if callable then call” for **internal** code paths that are part of the repo’s contracts.

- If the method/function “should always exist”, call it directly.
- If behavior is intentionally optional (plugin/provider boundary), detect capability **once at the boundary** and keep the rest of the code contract-driven.
- Telemetry/metrics must be best-effort: failures in tracking should never change prompts, retries, or request logic; they should degrade to “no metrics” with clear logs/tests.

### Rule 4: Tests map to acceptance criteria

For each acceptance criterion, ensure at least one of:
- unit tests
- integration tests
- UI tests

Or explicitly record why automation is not appropriate.

### Rule 5: Stop on impactful uncertainty

Stop and ask a question if any of these are unclear:
- acceptance criteria meaning/scope
- API contract behavior or backward compatibility
- data model invariants or migrations
- security/permission behavior
- error semantics and retryability
- cross-system integration expectations

If the uncertainty is not impactful, choose the simplest interpretation and record it in the Decision Log.

### Rule 7: Ask before deviating from repo standards

Before using patterns that deviate from `AGENTS.md` or other repo standards, **stop and ask for approval**. Common examples requiring approval:
- Imports inside functions (only allowed for: optional deps with graceful fallback, breaking circular imports, or expensive modules in rarely-used paths)
- Non-standard error handling patterns
- New dependencies or frameworks
- Architecture boundary violations

Do not assume an exception applies—ask first, then document the approved exception in the Decision Log.

### Rule 6: Record decisions (lightweight)

Maintain a Decision Log in the plan doc or PR description.

Make a decision entry when:
- there are multiple reasonable implementations
- user-visible behavior changes
- integrations/contracts could be affected
- tradeoffs were made that reviewers should know

Decision Log format:

- Decision: short title
  - context: why a decision was needed
  - options: 2–3 options considered
  - choice: what was chosen
  - rationale: why this choice
  - impact: what this affects
  - followups: planned cleanup/risks

---

## Implementation Process

### Step 0: Plan and repo alignment check

Confirm:
- acceptance criteria are present and testable
- plan steps are actionable and sequenced
- repo boundaries and standards are understood

### Step 1: Execute the current plan step

1. Mark the plan step as **ongoing**
2. Implement code changes for this step
3. Add/update tests for this step and its acceptance criteria
4. Update docs if required by `DOCUMENTATION_STRUCTURE.md`
5. Mark the plan step as **done** with brief notes/tests/ac coverage

### Step 2: Self review before moving on

Before starting the next step, verify:
- architecture boundaries are respected (`AGENTS.md`, `ui/AGENTS.md`, `ARCHITECTURE.md`, `UX_HIGH_LEVEL_IMPLEMENTATION_IDEA.md`)
- error handling matches existing patterns
- tests are deterministic and meaningful
- no secrets/sensitive data are logged or returned
- changes are minimal and reviewable
