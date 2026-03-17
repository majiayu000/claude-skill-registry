---
name: review-skill
description: Review a skill document using specialized reviewers. Each reviewer finds specific issue types.
---

# Review Skill

Run specialized reviewers against a skill document to find correctness, clarity, and conformance issues.

## Core Philosophy

**Every issue demands a document change:** real issue → fix it; false positive → add clarifying text.

---

## Reviewers

**Correctness** — will this do the wrong thing?
| Reviewer | Question | Finds |
|----------|----------|-------|
| execution | "Would this cause wrong behavior?" | Logic errors, missing steps, broken flows (all treated equally; no severity levels) |
| contradictions | "Does A contradict B?" | Conflicting instructions |
| coverage | "Is every option/branch handled?" | Unhandled branches, missing handlers |

**Clarity** — will this be misunderstood?
| Reviewer | Question | Finds |
|----------|----------|-------|
| adversarial | "Where might an LLM misinterpret this?" | Fixable ambiguities, missing info |
| terminology | "Is term X used consistently?" | Naming inconsistencies |
| conciseness | "Is everything here necessary?" | Verbosity, redundancy, over-explanation |

**Conformance** — does this follow conventions?
| Reviewer | Question | Finds |
|----------|----------|-------|
| checklist | "Do these specific checks pass?" | Structural issues, missing sections |
| portability | "Would this break on other LLM providers?" | Provider-specific assumptions |

---

## Phases

`@lib/...` references are expanded inline by the skill loader.

@lib/001_INITIALIZE.md
@lib/002_FAN_OUT.md
@lib/003_COLLECT.md
@lib/004_SYNTHESIZE.md
@lib/005_TRIAGE.md
@lib/006_HIL_PLAN_APPROVAL.md
@lib/007_ADDRESS.md
@lib/008_VERIFY.md
@lib/009_HIL_CHANGE_CONFIRMATION.md
@lib/010_STAGE.md
@lib/011_COMMIT.md
@lib/012_LOOP_GATE.md
@lib/013_EPILOGUE.md

---

## Quick Reference

| Phase                    | Purpose                           |
| ------------------------ | --------------------------------- |
| Initialize               | Parse args, validate target       |
| Fan Out                  | Launch all reviewers in parallel  |
| Collect                  | Gather and merge results          |
| Synthesize               | Group into themes                 |
| Triage                   | Propose fixes                     |
| HIL: Plan Approval       | User approves proposed fixes      |
| Address                  | Make edits                        |
| Verify                   | Confirm changes                   |
| HIL: Change Confirmation | User confirms edits               |
| Stage                    | Review and stage changes          |
| Commit                   | Create commit with proper message |
| Loop Gate                | Check pass count, loop or exit    |
| Epilogue                 | Report and end                    |

## Flags

| Flag                    | Behavior                                                      |
| ----------------------- | ------------------------------------------------------------- |
| `--auto`                | Skip HIL checkpoints (still displays plan/summary)            |
| `-n N`                  | Do N passes (default: 1)                                      |
| `--reviewer <category>` | Run only `correctness`, `clarity`, or `conformance` reviewers |

---
