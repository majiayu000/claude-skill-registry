---
name: skill-ecosystem-doctor
description: "Audit and safely remediate a cross-runtime Skill ecosystem spanning Codex, Claude Code, Loom, VibeGuard, Spellbook, and independent Git sources. Use when the user asks to inspect all local skills, resolve duplicate or divergent Skill copies, establish canonical sources and managed projections, retire obsolete skills without reinstall resurrection, scan Skill files for embedded credentials, quarantine unsafe automation, or prove Codex/Claude visibility with fresh checks. Do not use for invocation statistics alone; use skill-usage-stats for usage and zombie-skill evidence."
---

# Skill Ecosystem Doctor

Treat the local Skill collection as a governed software supply chain. Audit first,
plan repairs from evidence, apply only authorized changes, and finish with fresh
cross-runtime verification and a durable handoff.

This workflow is at `skill` maturity, not unattended `automation` maturity. Do
not schedule or silently apply repairs.

## Select the mode

| User intent | Mode | Routing |
|---|---|---|
| Inspect, review, inventory, or diagnose | `audit` | `execute_direct`; read-only |
| Explain what should change | `plan` | `plan_first`; no mutations |
| Fix, unify, quarantine, or retire | `repair` | `plan_first`; explicit scope and rollback |
| Recheck an existing governance file | `verify` | `execute_direct`; read-only |
| Rotate credentials, rewrite history, push, publish, or change remotes | external action | `clarify_first` unless the current request grants that exact action |

If the request mixes modes, run `audit` before `repair`. Do not infer repair
authorization from a request to inspect or diagnose.

## Operating Contract

- **Direct actions:** read-only discovery, deterministic audits, report drafts,
  and local validation.
- **Escalate before:** destructive changes, credential actions, history
  rewriting, remote publication, or any mutation not named by the current
  repair request.
- **Evidence-backed pushback:** challenge a proposed source, deletion, or
  completion claim only with paths, state queries, tests, ownership records, or
  a concrete data-loss or security risk.
- **Feedback loop:** promote repeated false positives, runtime-layout changes,
  and manual recovery steps into checks, fixtures, references, or evals.

## 1. Discover before creating

1. Search active roots and source repositories before creating a Skill,
   governance file, script, alias, or projection.
2. Locate every applicable `AGENTS.md` or equivalent before editing a source
   repository.
3. Read [runtime contracts](references/runtime-contracts.md) and classify each
   path as canonical source, managed projection, generated cache, or unknown.
4. Record the task goal, context, constraints, done-when conditions, dirty
   worktrees, runtime versions, and unavailable external permissions.
5. If work will span many files or sessions, use `flowguard` and keep the
   handoff outside parent context.

Common roots are discovery candidates, not declarations. Verify them on the
current machine; no data means unknown, not a guessed source relationship.

## 2. Run the deterministic audit

Use an existing governance file when one exists. Otherwise read
[the governance schema](references/governance-schema.md), adapt
[the example](assets/skill-governance.example.json) from discovered facts, and
show the proposed configuration before writing it.

From this Skill directory, run:

```bash
python3 scripts/ecosystem_doctor.py --governance ./skill-ecosystem-governance.json
python3 scripts/ecosystem_doctor.py --governance ./skill-ecosystem-governance.json --json
```

Use `--skip-loom` only when Loom is intentionally outside scope. A missing Loom
binary is an error when Loom validation is requested. Use `--fail-on-warn` for a
strict release gate.

The audit checks:

- broken roots, links, and local support-file references
- declared-name versus directory-name mismatches
- divergent active projections for the same declared name
- physical runtime copies without an exact source pin
- drift in pinned composite materializations
- active retired, quarantined, or projection-denied Skills
- active references to retired entry points
- high-confidence secret-like literals without printing their values
- Loom health, projection drift, and pending remote synchronization

Treat test-fixture secret patterns as visible warnings, not silent allowlists.

## 3. Classify findings

Order repairs by security, logic, data integrity, source lineage, and naming.
Separate facts from decisions:

- A digest conflict proves different content; it does not prove which copy is
  correct.
- A physical copy proves unmanaged materialization; it does not prove deletion
  is safe.
- A secret pattern proves local exposure risk; it does not prove account-side
  rotation occurred.
- A healthy projection proves installed consistency; it does not prove the
  upstream source is committed or remotely backed up.

Read [the remediation playbook](references/remediation-playbook.md) before
planning mutations.

## 4. Produce a repair plan

For every proposed action, record:

- finding and evidence
- owning source repository or unresolved owner
- exact writable files or paths
- authorization level
- reversible alternative and quarantine path
- repository-specific tests
- cross-runtime verification
- stop condition

Use disjoint file ownership for any parallel work. Do not let two agents edit a
shared registry, lockfile, manifest, or high-context file.

## 5. Apply only approved repairs

Safe direct actions are read-only inspection, report generation, local tests,
and drafting a plan. During an authorized `repair` run:

- prefer an independent clean Git worktree for source edits
- patch the canonical source, then regenerate managed outputs
- quarantine before removal and record original path plus digest
- preserve unrelated dirty worktree changes
- migrate genuinely neutral assets before retiring an entry point
- remove retired registrations, rules, references, projections, and installer
  sources without creating compatibility aliases
- update generated registries through their owning generator
- stop if the same hypothesis fails three times

Never print secrets, overwrite unknown user content, use force push, rewrite
history, or claim external credential rotation without direct evidence.

## 6. Verify and hand off

Run verification from the current session:

1. Run targeted tests for each changed source repository.
2. Run each repository's build and full test gate when applicable.
3. Re-run `ecosystem_doctor.py` and require zero errors.
4. Classify every remaining warning with evidence; do not suppress it merely to
   reach a clean count.
5. Confirm Codex and Claude resolve the intended source or exact pin.
6. For retired Skills, scan all active paths and test the relevant installer so
   reinstall does not restore them.
7. Run `git diff --check` in every changed Git worktree.
8. Fill [the remediation log template](assets/remediation-log-template.md).

Use [the eval cases](evals/evals.json) when forward-testing trigger boundaries,
read-only behavior, secret redaction, retirement, or dirty-worktree handling.

If commit, push, PR, merge, or landing is requested, prepare a review pack and
use `review-gate` unless the current request already grants that exact action.

## Done when

- canonical ownership is explicit for every in-scope active Skill
- active projections have no unresolved content conflicts or broken resources
- retired and denied names have no active path or invocation reference
- high-confidence embedded-secret findings are cleared or explicitly blocked
- every mutation has a rollback or quarantine record
- fresh source-specific tests and the ecosystem audit pass
- residual warnings and external actions are listed without overstating closure

## Gotchas, negative examples, and drift signals

- Do not choose the newest-looking fork automatically. Compare source history,
  contracts, tests, and ownership first.
- Do not turn a read-only audit into a bulk cleanup. Produce a repair plan.
- Do not replace quarantine with recursive deletion. Preserve a recoverable copy.
- Do not accept “should work” as verification. Run fresh commands.
- Do not automate this workflow after one successful machine repair. Promote
  only repeatedly stable, deterministic, read-only checks to scheduling.

Patch this Skill when the validator no longer understands an installed layout,
the same false positive recurs, a runtime changes projection semantics, or users
repeat the same safety correction.
