---
name: skill-lifeguard
description: "Use when a skill is brittle, drifting, repeatedly failing, or needs a Reliable Skill Contract. Trigger for phrases like skill lifeguard, reliable skill, self-maintaining skill, negative examples, verification checkpoints, drift signals, replay hooks, or failure log to skill patch. Audits or patches skills so high-value workflows include explicit forbidden behaviors, checkpoints, machine-checkable done conditions, replay or smoke hooks, and drift detection."
---

# Skill Lifeguard

Use this skill to make an existing or new skill self-maintaining enough for real
agent work. It complements `skill-audit` and `skill-creator`: use this skill for
the reliability contract, then use those skills for library fit and authoring.

Read `references/examples.md` when you need example contract wording. Use
`assets/reliable-contract-template.md` when drafting a reusable section.

## Reliable Skill Contract

Every high-value workflow skill should either include these five elements or
record why an element is intentionally deferred:

| Element | Required Evidence |
| --- | --- |
| Explicit negative examples | Named forbidden behaviors and concrete alternatives. |
| Verification checkpoints | Pass/fail checks after important phases, not only at the end. |
| Machine-checkable done conditions | Commands, assertions, artifacts, or state queries from the current session. |
| Replay or smoke hooks | A small way to rerun or sample the workflow, plus a log-to-patch loop. |
| Drift signal detection | Observable signs that the skill is stale, undertriggering, overtriggering, or producing false success. |

## Workflow

1. Search before creating or moving skill files.
2. Read the target skill and nearby docs that define its expected workflow.
3. Classify the skill maturity:
   - `manual`: workflow still needs human validation.
   - `skill`: manually validated and packaged as reusable instructions.
   - `automation`: repeatedly reliable and safe enough for scheduled or hook-driven use.
4. Score the five contract elements as `present`, `partial`, `missing`, or `deferred`.
5. Patch the smallest durable home: `SKILL.md` for routing and boundaries,
   `references/` for long examples, `scripts/` for deterministic checks,
   `assets/` or `templates/` for reusable report shapes.
6. Run repository validation and any skill-specific smoke check.

## Operating Contract

- Direct actions: audit skill files, draft contract gaps, patch local skill
  instructions, and run local validation.
- Escalate before: publishing skills, installing into user runtime directories,
  deleting user files, changing secrets, or promoting manual workflows into
  scheduled automation.
- Evidence-backed pushback: refuse reliability claims that lack fresh
  verification, replay hooks, or drift signals.
- Feedback loop: turn repeated corrections, false-success signals, or failed
  smoke runs into a skill patch and rerun validation.

## Gotchas

- A checklist without pass/fail evidence is not a checkpoint.
- A warning-only fallback can hide missing data; fail loud when output would be
  incomplete or misleading.
- A one-time successful manual run is not automation maturity.

## Output

For audits, lead with findings:

```text
reliable_skill_contract:
- target:
- maturity:
- score:
  negative_examples:
  verification_checkpoints:
  machine_done_conditions:
  replay_or_smoke_hooks:
  drift_signals:
- blocking_gaps:
- patch_plan:
- verification:
```

For edits, keep the patch scoped to the missing contract elements. Do not
rewrite the skill's domain behavior unless the reliability gap requires it.

## Negative Examples

Reject these patterns and name the safer alternative:

- "Verify by saying it should work." Use a fresh command, fixture, or state
  query instead.
- "Swallow a failed helper and continue with a generic fallback." Surface the
  failure or mark the workflow blocked.
- "Add a broad reminder to be careful." Add a concrete forbidden behavior and
  an allowed replacement.
- "Automate a workflow that has never passed manually." Keep it in `manual`
  maturity and add smoke checks first.

## Checkpoints

Place checkpoints where a future agent could otherwise drift:

- after startup discovery and applicable instructions are read
- before edits that touch high-context files or generated metadata
- after each deterministic verification command
- before commit, push, PR, merge, or automation
- after a failure log produces a skill patch

## Drift Signals

Treat these as evidence to patch the skill:

- users repeat the same correction
- the skill triggers for the wrong task boundary
- the skill fails to trigger for its primary phrase
- the expected verification command no longer exists
- output format changes without downstream docs or examples changing
- a silent fallback hides missing data, auth, files, or external state

## Verification

For Spellbook skills, run:

```bash
python3 ./scripts/validate_skills.py --check
python3 ./scripts/audit_skill_quality.py skill-name
```

If the skill owns scripts, also run the relevant syntax check or fixture. Report
missing prerequisites instead of marking the contract complete.
