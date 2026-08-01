---
name: phx-review
description: Review changed Elixir/Phoenix code read-only. Check requirements, cite
  evidence, deduplicate, and return a verdict.
---
# Review Elixir/Phoenix Code

Perform an evidence-based, read-only review of changed code. Find and explain
issues; do not edit files, create tasks, or fix findings.

## Usage

```text
$elixir-phoenix:phx-review
$elixir-phoenix:phx-review test
$elixir-phoenix:phx-review security
$elixir-phoenix:phx-review .claude/plans/auth/plan.md
$elixir-phoenix:phx-review --no-requirements
```

Treat the text after the skill name as a focus area, issue identifier, or path to
a plan/specification.

## Iron Laws

1. **Review is read-only** — inspect and report; never modify the worktree.
2. **Scope to changed code** — distinguish new defects from pre-existing issues.
3. **Every finding needs evidence** — cite a path and line, explain impact, and
   describe the concrete failure mode.
4. **Check requirements when available** — unmet requirements affect the verdict.
5. **Deduplicate and prioritize** — one root cause is one finding, with the
   highest justified severity.
6. **Do not require custom agents, hooks, MCP, or unavailable task APIs** — use
   optional runtime capabilities only when present.

## Workflow

### 1. Establish Scope

Determine the merge base or user-specified base, then inspect:

```bash
git status --short
git diff --name-only <base>...HEAD
git diff --stat <base>...HEAD
git diff <base>...HEAD -- <changed-files>
```

Do not assume `HEAD~5` is the correct base. Include uncommitted changes when the
user asks to review the current worktree. Record the chosen scope in the result.

### 2. Load Requirements

Unless `--no-requirements` is set, look for an explicit plan/spec path, current
conversation requirements, a branch or commit issue identifier, or the latest
relevant plan. Use available integrations or `gh issue view` when configured;
otherwise mark requirements `NOT AVAILABLE` and continue.

Read `references/requirements-detection.md` for detection order. Never let a
missing Linear, GitHub, hook, or MCP integration block code review.

### 3. Review by Concern

Select only concerns relevant to the diff:

- Elixir/Phoenix correctness and idioms;
- Ecto queries, changesets, transactions, migrations, and N+1 risks;
- LiveView lifecycle, reconnect, forms, streams, and assigns;
- authentication, authorization, secrets, and input handling;
- Oban idempotency, retries, uniqueness, and transaction boundaries;
- tests, regressions, and verification gaps;
- deployment/runtime configuration when those files changed.

Native Codex subagents may run independent read-only concern tracks in parallel.
Use generic subagents with the complete diff scope and return findings to this
session; do not depend on separately installed named agents. If subagents are
unavailable or unnecessary, run every selected concern sequentially here. A
sequential review is fully valid.

### 4. Verify Findings

For each candidate:

1. Confirm it is in changed code or label it `PRE-EXISTING`.
2. Trace the actual runtime or data-flow consequence.
3. Check nearby tests and requirements.
4. Remove style-only noise and speculative concerns.
5. Merge duplicates under the clearest root cause.

Run targeted read-only verification when it materially changes confidence. Do
not alter files or suppress failures. If a check cannot run, report that clearly.

### 5. Report a Verdict

Return one verdict:

- `PASS`
- `PASS WITH WARNINGS`
- `REQUIRES CHANGES`
- `BLOCKED`

List findings in descending severity as `BLOCKER`, `WARNING`, or `SUGGESTION`.
Each finding must include `path:line`, evidence, impact, and the smallest
appropriate correction. Add requirements coverage before findings; any `UNMET`
requirement requires `REQUIRES CHANGES`.

If there are no findings, say so explicitly and list residual risks or checks not
run. Stop after presenting the review. Suggest `$elixir-phoenix:phx-triage`, `$elixir-phoenix:phx-plan`, or
`$elixir-phoenix:phx-compound` as optional next steps without invoking them automatically.

## References

- `references/requirements-detection.md` — requirements source and coverage rules
- `references/agent-spawning.md` — Codex concern selection and optional parallelism
