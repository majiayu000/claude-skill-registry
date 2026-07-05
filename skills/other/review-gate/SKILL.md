---
name: review-gate
description: "Use before an agent-produced diff is committed, pushed, opened as a PR, merged, landed, or applied to user files when explicit implementation approval is missing. Trigger for review gate, review pack, approve before landing, diff first then land, human approval, merge gate, commit gate, push gate, or PR readiness. Produces a concise review pack, records risks and verification, and blocks landing until a human explicitly approves or approves with required fixes."
---

# Review Gate

Use this skill as the last-mile safety checkpoint for agent-generated changes.
It complements PR review tools; it does not replace code review, CI, or human
approval.

Use `assets/review-pack-template.md` when the user needs a reusable review pack
shape.

## When To Run

Run before any of these actions when an agent-generated diff is involved:

- commit
- push
- open or update a PR
- merge or land
- apply a generated patch to user files when the user has not already approved
  that exact implementation path

Read-only review, planning, issue triage, and local exploration do not require
this gate unless the next step would land or publish changes.

## Operating Contract

- Direct actions: inspect diffs, collect verification evidence, and draft the
  review pack.
- Escalate before: commit, push, PR creation, merge, branch deletion, or
  applying a generated patch when the user has not approved that exact action.
- Evidence-backed pushback: block landing when verification is stale, sensitive
  surfaces lack review, or approval is ambiguous.
- Feedback loop: convert repeated review findings into new checklist items,
  verification commands, or Review Pack risk prompts.

## Gate States

| State | Meaning | Allowed next action |
| --- | --- | --- |
| `draft_pack` | Review pack is being assembled. | Inspect diff and verification only. |
| `needs_fixes` | Blocking risks or missing evidence exist. | Patch and rerun the gate. |
| `awaiting_human` | Pack is complete but no human approval exists. | Stop before commit, push, PR, merge, or apply. |
| `approved` | Human explicitly approved the pack in the current thread. | Proceed with the named action only. |
| `approved_with_fixes` | Human approved after specific fixes. | Apply fixes, verify, and record evidence before landing. |

Agents must not self-approve. Prior CI success, a reviewer lane, or a green
local test is evidence for the pack, not approval.

## Gotchas

- Approval is action-specific. "Commit it" does not mean "merge it."
- A reviewer lane is independent evidence, not human approval.
- If a fix changes the diff after approval, refresh verification and update the
  pack before landing.

## Review Pack

Produce this compact pack:

```text
review_gate:
- intent:
- diff_summary:
- files_changed:
- driving_skill_or_issue:
- risks:
- missing_tests_or_verification:
- commands_run:
- evidence:
- open_questions:
- approval_needed_for:
- decision:
```

Keep findings ranked by severity. Include exact file paths, PR numbers, issue
numbers, command names, and current head SHA when available.

## Decision Rules

- If verification is stale, missing, or tied to a different head SHA, set
  `needs_fixes`.
- If the diff touches auth, payments, secrets, permissions, `innerHTML`, `eval`,
  shell execution, generated registry, hooks, or high-context files, call that
  out explicitly.
- If user approval is ambiguous, set `awaiting_human` and ask for the named
  action only.
- If the user approves, do exactly the approved action. A commit approval is not
  automatically a merge approval.
- If a required fix changes the diff, rerun the relevant verification and update
  the pack before landing.

## Integration Points

`flowguard` should call this gate at landing checkpoints. Queue skills may use a
reviewer lane for independent findings, but the Review Gate still records the
human-facing pack and approval state.

For GitHub PRs, combine this gate with current remote truth:

- PR head SHA
- check rollup
- merge state
- GraphQL reviewThreads
- linked issue intent

## Verification

For Spellbook changes, the pack usually cites:

```bash
git diff --check
python3 ./scripts/validate_skills.py --check
python3 ./scripts/audit_skill_quality.py skill-name
```

Use project-specific tests for code changes. If a command cannot run, report the
precondition and keep the decision out of `approved`.
