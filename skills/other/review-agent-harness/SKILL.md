---
name: review-agent-harness
description: Review whether a repository's coding-agent harness can reliably carry work from intent through controlled execution, verification, delivery, and learning. Use when asked to assess agent readiness, repeated agent failures, Rules/Skills/Hooks/Memory effectiveness, missing validation or recovery loops, or whether a harness repair improved later outcomes. Do not use for code-only audits, AGENTS-only audits, individual skill reliability reviews, or executing the task itself.
---

# Review Agent Harness

Review the operating system around coding agents, not only its files. Separate
declared assets, reachable routes, observed task use, and later outcomes.

## Route And Scope

Resolve the directory containing this `SKILL.md` before running its scripts.
Select one mode:

- `static`: inspect the target repository only. Use by default.
- `episode`: add explicitly authorized Codex or Claude Code JSONL sources.
- `longitudinal`: compare a validated report with the existing ledger.

Default to inline, read-only output. Write a durable report under the target
only when the user explicitly requests an artifact or historical tracking.
Never discover user-home Sessions, read Memory bodies, or inspect another
provider merely because its files are available.

Use adjacent skills instead when their narrower owner is sufficient:

- `codebase-audit` for code defects and architecture health;
- `repo-agent-context-audit` for AGENTS, Skills, and Specs alone;
- `skill-lifeguard` for one Skill's reliable contract;
- `flowguard` for running a long task;
- `review-gate` before landing an agent-generated diff.

## Step 1: Freeze The Evidence Boundary

Record target, mode, provider, locale, decision, acceptance boundary, output
mode, included sources, excluded sources, and unavailable evidence. Treat a
missing required source as `unobserved`; do not substitute a broader directory,
another provider, or remembered results.

Resolve the target before interpreting assets or assigning scores. The collector
classifies it as `exact_git_root`, `inside_git_worktree`,
`contains_nested_git_root`, or `non_git_directory`. If the supplied directory
contains a nested Git root, stop and retarget that exact repository; do not
score the parent as though it were the project. For a Git target, the collector
uses Git's tracked and untracked inventory and excludes ignored worktrees and
prior review output from repository evidence.

Run static collection from the installed Skill directory:

```bash
python3 scripts/collect_evidence.py \
  --target /absolute/target \
  --mode static \
  --locale zh-CN \
  --decision "assess agent-harness readiness" \
  --acceptance-boundary "resolve all five dimensions" \
  --output-mode inline \
  --output /temporary/evidence.json
```

For Session-informed review, require the user to authorize exact files or an
exact root. Use one provider per evidence envelope:

```bash
python3 scripts/collect_evidence.py \
  --target /absolute/target \
  --mode episode \
  --provider codex \
  --session-file /explicit/session.jsonl \
  --locale zh-CN \
  --decision "explain the observed verification gap" \
  --acceptance-boundary "separate configured and exercised routes" \
  --output-mode inline \
  --output /temporary/evidence.json
```

Use `--session-root` only when that exact recursive scope was authorized. Add
`--include-request-summaries` only when sanitized request summaries are needed
for the decision. Read [Privacy Boundary](references/privacy-boundary.md) and
[Session Adapters](references/session-adapters.md) before Session-informed work.

Omit `--output` to stream evidence to stdout. Inline means no target writes;
environment-owned scratch remains allowed. `validate_findings.py --input -`
accepts findings JSON from stdin when the caller already has a stream.

Checkpoint: collection must return `agent-harness-evidence`; every stage must
be `available`, `constrained`, `not_authorized`, `not_applicable`, `unavailable`,
or `unobserved`. A depth-limited scan is `constrained`, never silently complete.
Stop on malformed output or an unexplained missing stage.

Copy the collector-owned `scope.target_id` and complete `scope.snapshot`
(`baseline`, `target_relation`, and `id`) into the findings document. Never
author these values manually. The renderer and ledger updater recompute the
binding from `--target` and reject a different local directory or any target
state that changed after collection. A previous report, ledger row, branch
name, or remembered result is a historical lead only. Recheck any retained
claim against the frozen current snapshot and label genuinely historical
evidence as such.

## Step 2: Run Three Isolated Evidence Passes

Keep the passes logically independent even when one agent runs them in
sequence:

1. **Task pass**: use the current goal, corrections, acceptance boundary, and
   authorized Episode facts. Do not infer repository mechanisms.
2. **Project pass**: use static startup, commands, tests, CI, Git, delivery, and
   recovery evidence. Do not infer Session behavior.
3. **Agent-assets pass**: use project Rules, Skills, Hooks, settings, and other
   configured surfaces. Presence and counts are navigation facts only.

Do not launch parallel agents by default. If the user explicitly requests
threads, use `threads` with read-only lanes and bounded evidence packets. A
specialist proposes candidates; it does not assign final severity or claim
effectiveness.

Read [Review Model](references/review-model.md) before classifying the five
dimensions. Use `present -> reachable -> exercised -> outcome_supported` only
when each stronger state has direct evidence.

Resolve all 15 stable checks, three per dimension. Assign a score to each
dimension only after resolving its checks. The score is an evidence-bounded
summary, not a finding: `present` caps a dimension at 74, `reachable` at 84,
`exercised` at 94, and `outcome_supported` at 100; `missing` or `unobserved`
caps it at 59. Use the lowest applicable check ceiling and retain a short score
rationale. Do not compute an overall score.

## Step 3: Reconcile Findings

Retain each distinct eligible candidate. Merge only when consequence, root
cause, owner, and verifier are the same. The lead alone assigns severity,
confidence, primary dimension, verification state, and priority.

Read [Finding Contract](references/finding-contract.md). Every finding needs:

- an observed consequence or exact governing requirement;
- a bounded evidence reference;
- a cause chain and smallest owner;
- an executable repair route;
- a machine-checkable verifier.

Counts, file absence without a requirement, similarity, theoretical risk,
score, or unavailable evidence never create a finding. Critical and High
findings require an adversarial check; retain an unavailable check as
`unverified` instead of presenting it as confirmed.

Record each executed verifier in `verification_runs` with a stable id, purpose,
result, exit code, final-state flag, and bounded summary. A confirmed Critical
or High finding must cite a final-state `candidate_refutation` or
`targeted_reproduction` run that supports the claim. Inspect aggregate exit
semantics: a child syntax error or failed subcheck paired with aggregate exit 0
is evidence of a false-green verifier, not a passing check.

Author one `agent-harness-findings` JSON object in environment-owned scratch
space, then validate it:

```bash
python3 scripts/validate_findings.py --input /temporary/findings.json --strict --json
```

Fix the findings data, not the validator. Stop if validation does not pass.

## Step 4: Report Or Track History

For inline review, render the overview, frozen snapshot, five-dimension
scorecard, all 15 checks, structured verification runs, findings, evidence
boundary, and at most three priority moves in the response. Do not write to the
target.

When durable output is explicitly requested, render atomically:

```bash
python3 scripts/render_report.py \
  --findings /temporary/findings.json \
  --evidence /temporary/evidence.json \
  --target /absolute/target \
  --out /absolute/target/.agent-harness-review \
  --json
```

The renderer refuses to replace an existing run and writes only validated
`findings.json`, privacy-safe `evidence.json`, and derived `report.md`.

For longitudinal mode, update the ledger after a fresh review:

```bash
python3 scripts/update_ledger.py \
  --findings /temporary/findings.json \
  --target /absolute/target \
  --ledger /absolute/target/.agent-harness-review/ledger.json \
  --json
```

An absent prior finding remains open with `recheck_required` until a targeted
spot-check produces an `agent-harness-resolution-confirmations` document. Each
confirmation must retain the finding id, verifier, and one bounded
`evidence_ref`. Pass it with
`--resolution-confirmations /temporary/confirmations.json`. Never resolve from
finder absence or an id-only assertion.

## Step 5: Repair And Later Effect

Read [Repair Loop](references/repair-loop.md) for follow-up. This review does
not authorize fixes. Route a selected finding to its owner in a separate task,
run its verifier on the final state, and update `repair_state` only.

Do not upgrade `learning-retention` from same-window repair evidence. For a
tool-backed route, collect the later Episode with `--mechanism-category edit`
or `validation`, `--episode-role later`, and an explicit `--comparison-basis`;
collect the baseline with the same basis and `--episode-role baseline`. The
adapter count shows only that coarse mechanism was exercised. Use bounded file
or policy evidence to map the category to the repaired route. Separately require
target-owned command or artifact references showing the result improved and
guardrails still passed. Adapter counts, collection time, or a request summary
alone never prove later effect.

When claiming `outcome_supported`, pass both collector envelopes to every gate:
`validate_findings.py --evidence baseline.json --evidence later.json`, and use
the same repeated `--evidence` flags with `render_report.py` or
`update_ledger.py`. The claim is rejected without exactly one bound baseline
and one bound later envelope.

## Operating Contract

Direct actions:

- inspect the authorized repository read-only;
- run bounded local collectors and validators;
- produce inline findings;
- write report artifacts only when durable output was requested.

Escalate before:

- reading stored Sessions, Memory bodies, or user-home assets outside an exact
  authorization;
- editing Rules, Skills, Hooks, settings, source, tests, or generated files;
- installing automation, publishing, committing, pushing, or changing remote
  state.

Evidence-backed pushback: reject a requested score or conclusion when the
target is not the exact repository, the relevant evidence is unavailable, an
aggregate verifier hides a failed subcheck, or a historical claim was not
rechecked on the frozen snapshot. State the concrete boundary and the smallest
next command that could resolve it.

Feedback loop: replay the closest case in `evals/evals.json` after a miss or
false positive, add one focused regression test, and patch the smallest durable
owner in the collector, validator, renderer, or written contract.

## Negative Examples And Gotchas

- Do not turn “five Skills installed” into “Skills are effective.” Require
  task-linked use and a result.
- Do not turn “no Session access” into “no failures.” Mark behavior
  `unobserved` and continue only with static mechanisms.
- Do not treat a test run before the final edit as verification closure. Run
  the mapped check on the final state.
- Do not mark a missing previous finding resolved because a finder omitted it.
  Spot-check and confirm the id.
- Do not copy raw prompts, commands, paths, secrets, or stable Session ids into
  findings or reports. Keep only adapter-produced facts.
- Do not use a numeric score as evidence or average the dimensions into an
  overall score. Scores summarize the 15 evidence-bounded checks only.
- Do not inherit a finding from an older report. Treat it as a lead and rerun
  its mapped check on the frozen snapshot.
- Do not redirect durable output to a sibling directory. The renderer accepts
  only `/absolute/target/.agent-harness-review`, and the ledger updater accepts
  only its `ledger.json` below that directory.
- Do not attribute a generated or aggregate failure to the nearest file. Trace
  the caller, configuration, and output owner before choosing the smallest
  repair owner.

## Done When And Drift Loop

Finish only when:

- all five dimensions appear exactly once with evidence or an explicit
  `unobserved` / `not_applicable` boundary;
- all 15 stable checks appear exactly once and each dimension score stays below
  its weakest applicable evidence ceiling;
- every finding passes `validate_findings.py --strict`;
- durable reports, when requested, are renderer-produced and paths are exact;
- unavailable stages and unverified high-severity candidates remain visible;
- no target mutation occurred outside explicit authority.

Use `evals/evals.json` and the repository tests as the replay surface. Patch the
smallest durable owner when the Skill over-triggers, misses a primary request,
accepts private data, treats configuration as use, resolves from absence, or
claims later effectiveness from same-window checks.

## Resources

- `scripts/collect_evidence.py`: static collector and Session adapter facade.
- `scripts/validate_findings.py`: findings, evidence-state, and privacy gate.
- `scripts/render_report.py`: atomic durable Markdown renderer.
- `scripts/update_ledger.py`: conservative longitudinal ledger.
- `references/review-model.md`: dimensions and evidence semantics.
- `references/finding-contract.md`: authoring and reconciliation contract.
- `references/privacy-boundary.md`: authorization and redaction rules.
- `references/session-adapters.md`: Codex and Claude Code input boundaries.
- `references/repair-loop.md`: repair progress versus later effectiveness.
