---
name: qa-quarto
description: Adversarial Quarto-vs-Beamer parity QA. A critic agent compares the Quarto HTML render to the Beamer PDF benchmark for content/visual parity; a fixer agent applies fixes; loops until APPROVED (max 5 rounds). Use when user says "qa the quarto", "check parity", "does the html match the pdf?", "quarto matches beamer?", or after a translate-to-quarto run. Requires both the `.qmd` rendered and a `.pdf` benchmark.
argument-hint: "[LectureN]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
context: fork
---

# Adversarial Quarto vs Beamer QA Workflow

Compare Quarto HTML slides against their Beamer PDF benchmark using an iterative critic/fixer loop.

**Philosophy:** The Beamer PDF is the gold standard. The Quarto translation must be at least as good in every dimension.

---

## Workflow

```
Phase 0: Pre-flight → Phase 1: Critic audit → Phase 2: Fixer → Phase 3: Re-audit → Loop until APPROVED (max 5 rounds)
```

## Hard Gates (Non-Negotiable)

| Gate | Condition |
|------|-----------|
| **Overflow** | NO content cut off |
| **Plot Quality** | Interactive charts >= static plots |
| **Content Parity** | No missing slides/equations/text |
| **Visual Regression** | Quarto >= Beamer in all dimensions |
| **Slide Centering** | Content centered, no jumping |
| **Notation Fidelity** | All math verbatim from Beamer |

## Phase 0: Pre-flight

1. Locate Beamer (.tex/.pdf) and Quarto (.qmd/.html) files
2. Check freshness (re-render if QMD newer than HTML)
3. Verify TikZ SVGs if applicable

## Phase 1: Initial Audit

Launch the `quarto-critic` agent to compare Beamer vs Quarto comprehensively. Report saved to `quality_reports/[Lecture]_qa_critic_round1.md`.

## Phase 2: Fix Cycle

If not APPROVED, launch `quarto-fixer` agent to apply fixes (Critical → Major → Minor), re-render, and verify.

## Phase 3: Re-Audit

Re-launch critic to verify fixes. Loop back to Phase 2 if needed.

## Iteration Limits — loop-until-dry

This is the **loop-until-dry** primitive from [`orchestrator-protocol.md`](../../rules/orchestrator-protocol.md): the critic returns `FINDING`s (the hard-gate table is the CRITICAL roll-up, per [`orchestration-schemas.md`](../../references/orchestration-schemas.md)); the loop **converges when a round adds 0 new CRITICAL/MAJOR** findings (deduped on `location`+`finding`), not at a fixed round count.

- **Fallback cap:** 5 rounds bounds a non-converging loop, then escalate to the user with remaining issues.
- **Two-strikes:** the same gate failing in rounds N and N+2 is flagged for the user, not patched again ([`summary-parity.md`](../../rules/summary-parity.md)).
- APPROVED iff every hard gate passes (zero CRITICAL).

## Final Report

Save to `quality_reports/[Lecture]_qa_final.md` with hard gate status, iteration summary, and remaining issues.
