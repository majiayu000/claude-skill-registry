---
name: ce-adr-gap-analyzer
description: >
  Analyze ADR compliance by interpreting the ADR's intent, verifying that
  implementation and RTD satisfy every decision, and producing a dated gap
  report with only unresolved items.
---

# CE ADR Gap Analyzer

You are verifying that the **intent and decisions** of a given ADR are fully
realized in code and documentation. Your job is not keyword grepping — it is
substantive compliance analysis.

---

## Inputs

- ADR identifier (e.g. `ADR-004`), or `all` to sweep every ADR in the appendix.
- Repository files (source code, tests, docs) accessible in workspace.

---

## Phase 1 — Understand the ADR intent

1. **Read the full ADR text** (`docs/improvement/adrs/ADR-XXX-*.md`). Extract:
   - **Decisions** — what the ADR mandates, forbids, or constrains.
   - **Requirements** — concrete deliverables (APIs, contracts, invariants,
     enforcement mechanisms, documentation, tests).
   - **Rationale** — why these decisions were made. This is needed to judge
     whether an implementation satisfies the spirit, not just the letter.
   - **Scope** — which modules, subsystems, or surfaces the ADR governs.
2. Build a **checklist of required outcomes** from the decisions. Each outcome
   is a testable statement, e.g.:
   - "Plugin trust flags must be immutable after registration."
   - "RTD must document the fallback chain."
   - "CI must enforce the two-release deprecation window."

## Phase 2 — Verify implementation against intent

3. For each required outcome, **search and read the codebase** (`src/`,
   `tests/`, configuration files):
   - Read the relevant source files. Understand what the code actually does
     and whether it satisfies the ADR requirement.
   - Check for invariant enforcement (assertions, validators, guards) where
     the ADR requires them.
   - Check for correct API surfaces, signatures, and contracts where the ADR
     specifies them.
   - Check for tests that exercise the required behavior.
4. For each required outcome, **check RTD and documentation** (`docs/`) when
   the ADR has documentation requirements:
   - Verify that docs describe the behavior accurately and consistently with
     the implementation.
   - Flag docs that contradict the code or the ADR text.
   - Flag missing documentation for ADR-mandated surfaces.

## Phase 3 — Classify and score gaps

5. For each required outcome that is **not fully satisfied**, record a gap:
   - Violation impact (1–5): how seriously the gap violates the ADR intent.
   - Code scope (1–5): breadth of code affected.
   - Unified severity = impact × scope.
   - One-line recommendation with file/line pointers where evidence was found
     (or expected but missing).
6. Mark outcomes that **are fully satisfied** as completed — these will be
   purged from the output (see Phase 4).

## Phase 4 — Update the ADR status appendix

The output format and rules are defined in the **ADR status appendix** heading
of `docs/improvement/RELEASE_PLAN_v1.md`. The appendix states:

> This appendix lists only unresolved gaps per ADR. ADRs with no open gaps
> show a clear compliance verification line (date-stamped). Tables use the
> project's severity axes: Violation impact (1–5) × Code scope (1–5) =
> Unified severity.

Follow these rules exactly when writing or updating appendix sections:

7. **Purge completed gaps.** When updating an existing appendix section:
   - **Remove every row whose gap is resolved.** Do not keep completed rows
     with zeroed-out scores — delete them entirely.
   - If a table mixes completed and open rows, rewrite it with **only the
     remaining open rows**, ranks renumbered from 1.
   - If **all** rows are completed, **replace the entire table** (header,
     separator, data rows) with a single compliance verification line.
8. **Only unresolved gaps appear.** Never list completed, resolved, or
   zeroed-out rows in the table.
9. **Date stamp — mandatory on every update.** Every time the appendix is
   updated (single ADR or full sweep), stamp today's date:
   - Compliance lines use format:
     `**Compliance verification (YYYY-MM-DD):** Reviewed code and RTD — no ADR-XXX gaps found; ADR-XXX is fully compliant. No further action required.`
   - Gap tables: add `_Last gap analysis: YYYY-MM-DD_` immediately above
     the table.
10. **If NO gaps remain** the compliance verification line must be
    unambiguous — it replaces the entire table and makes clear that no
    further action is required.

---

## Key principles

- **Intent over keywords.** Do not rely on grepping for `TODO` or `COMPLETED`.
  Read the ADR decisions, understand what they require, and verify that code
  and docs deliver. A missing `TODO` does not mean compliance; present code
  does not mean the ADR intent is satisfied.
- **Substance over ceremony.** A gap exists when implementation diverges from
  what the ADR decided — not when a keyword is absent. A gap is closed when
  code and docs genuinely satisfy the requirement — not when someone wrote
  `COMPLETED` next to it.
- **Conservative severity.** Prefer conservative estimates when evidence is
  ambiguous.
- **Evidence-based.** Every gap claim must cite specific files and lines (or
  their absence). Every compliance claim must cite the evidence that satisfies
  the ADR requirement.
- **Keep ADR status appendix tidy.** Status reports must be placed correctly in the order under the correct header in the ADR status appendix. No duplicate entries per ADR allowed.

---

## Files to read

```
docs/improvement/adrs/ADR-XXX-*.md     ← the ADR itself (primary source of intent)
docs/improvement/RELEASE_PLAN_v1.md    ← appendix to update with gap results
src/                                   ← implementation evidence
tests/                                 ← test coverage of ADR requirements
docs/                                  ← RTD evidence (when ADR has doc requirements)
```

---

## Notes and constraints

- This skill is an evidence-gathering assistant, not an authoritative arbiter.
  Impact/scope ratings are suggestions for ADR owner review.
- The date is always stamped — there is no opt-out.
- When sweeping all ADRs, process each section independently and apply the
  same four phases to every one.
