---
name: delivery-checklist
description: Pre-delivery acceptance checklist and reusable mini-prompts for common tasks. Use when (1) Preparing to mark story as Delivered, (2) Final PR review before merge, (3) Need quick prompt templates for classification/TDD/refactoring/PR composition, (4) Verifying completeness of implementation. Includes default loop (Plan → Implement → Artifacts → PR → Verify → Deliver) and acceptance criteria.
---

# Delivery Checklist & Mini-Prompts

## Default Loop

**Plan → Implement (Red→Green→Refactor) → Produce Artifacts → PR → Verify CI → Deliver**

Always respond in this order:
1. **Plan** (checklist)
2. **Actions & Artifacts** (logs, screenshots, test output)
3. **Findings**
4. **Code Diffs** (unified `---/+++` patches)
5. **Tests Added/Updated**
6. **PR Description** (summary, risks, rollout)
7. **Next Steps**

## Acceptance Checklist (before marking Delivered)

* [ ] Story type + estimate stated; branch follows convention
* [ ] Red→Green→Refactor commits present (incl. WIP + EOD)
* [ ] Tests added/updated and passing locally & in CI
* [ ] Security/a11y/responsive considerations addressed (if UI)
* [ ] PR description complete with evidence and rollback plan
* [ ] Staging deploy verified or verification plan included

## Reusable Mini-Prompts

* **Classify story:** "Classify as feature/bug/chore and justify. Provide estimate (0/1/2/3/5/8) with rationale."
* **TDD kickstart:** "Generate minimal failing tests for {behavior}, given/when/then, then outline the smallest implementation."
* **Refactor pass:** "With tests green, propose safe refactors that reduce complexity and keep public API stable."
* **PR composer:** "Summarize commits into a PR description using Problem/Solution/Test Plan/Risk/Story Link."

## Reference Files

See `references/acceptance-criteria.md` for expanded checklist with examples and verification steps.

See `references/mini-prompts.md` for detailed mini-prompt templates with usage examples.
