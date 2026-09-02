---
name: ci-fix
description: 'Use when the user says "CI is red", "fix the checks", or "make CI green" on a PR or branch. Diagnoses failing GitHub Actions checks, fixes the root cause, and re-verifies to green. Interactive mode applies a local fix; autonomous mode pushes to a fix branch. Not for deploys, credentials, permission-widening, or rerun-as-fix; non-CI bugs use strike-the-root.'
---

# CI fix

Repair failing CI on a PR or branch. Two modes: interactive (default, reversible local) and autonomous (remote push, entered only on an explicit user ask). Never widen workflow permissions, never add `pull_request_target`, never offer a rerun in place of a code fix. Merge conflicts route to `resolve-merge-conflicts`; non-CI bugs route to `strike-the-root`.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Interactive: user asks to diagnose or repair failing CI on a PR or branch. Autonomous: user explicitly asks for the fix to be pushed. |
| Authority | Interactive: reversible local — write only named source files after plan approval; no remote mutation. Autonomous: the only remote mutation is creating or updating `ci-fix/<original-branch>` on the same remote; never opens a PR. |
| Side effect | Interactive: local source files are edited and a local-equivalent check passes; remote CI is unchanged. Autonomous: a fix branch is pushed with the approved change set and a new CI run is observed. |
| Done | Interactive: failing checks identified, the approved local fix is applied, and every local equivalent passes; return `local-fix-ready` because remote CI is unchanged. Autonomous: a new run on `ci-fix/<original-branch>` is green and the ordered root-cause record is delivered. `checks-pass` is claimed only after a green remote run is observed. |

## Inputs

- `repo`: path inside the repo (default `.`). Must be a Git repository.
- Target: PR number or URL, original branch name, or run ID; defaults to the current branch's PR. A working tree already carrying the in-progress fix is fine.
- `gh` authenticated for the repo host with workflow/repo scopes; an unauthenticated CLI stops the skill before any change.
- Optional: a specific job ID for full-log inspection, or an artifact download when logs alone do not identify the cause.

## Procedure — interactive (spine)

1. Verify gh authentication: `gh auth status`. If unauthenticated, stop and ask the user to run `gh auth login`; no mutation before this. Done when: an authenticated identity is confirmed by `gh auth status` output, or the handoff is asked and no mutation has occurred.
2. Resolve the failing run. PR: `gh pr view --json number,url`. Non-PR branch or supplied run ID: `gh run list --branch <branch> --status failure --limit 5`, then `gh run view <run-id>`. Done when: one failing run is identified by its run ID and branch name from command output.
3. Inspect failing checks (GitHub Actions only). Prefer the bundled script, which handles gh field drift, run-id/job-id extraction, failure-snippet extraction, and exits non-zero while failures remain:
   - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"` (`--json` for machine output).
   - Manual fallback: `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`; rerun with the fields `gh` accepts if one is rejected. Extract the run id from `detailsUrl`, then `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha` and `gh run view <run_id> --log`; for one failing job use `gh run view <run-id> --log --job <job-id>`; for evidence logs cannot supply, `gh run download <run-id> -D .artifacts/<run-id>`. If a run log is still in progress, fetch job logs via `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs"`.
   - A check whose `detailsUrl` is not a GitHub Actions run is external: report the URL only; do not attempt Buildkite or other providers.
   Done when: every failing check has a name, URL, and a log snippet from command output — or an explicit `log_pending`/`log_unavailable` marker; never a fabricated snippet.
4. Triage every failing check: classify each as a root cause or a downstream symptom of another failure. A single root cause may surface as several failing checks. Order the work so root causes are fixed before the symptoms they produce. Done when: every failing check is classified as root cause or symptom in a written list, and the work order places root causes before their symptoms.
5. For each root-cause failure, read the failure log and the relevant source to determine the smallest deterministic fix for that cause; prefer a code change over workflow plumbing; for a flaky test, fix the nondeterminism instead of rerunning. Request approval before editing any file. Done when: the plan is approved in writing with the file paths and change described, or refused — then report the plan and wait without editing.
6. Implement the approved plan and summarize diffs and tests. Keep the change set inside the failing job/step where possible. Done when: `git diff --name-only` lists only the approved file paths and the diff summary matches the approved plan.
7. Run the local equivalent of each failing CI check to confirm the fix before any push. Done when: the local check command exits 0 with its output captured, confirming the fix reproduces green locally.
8. Capture the current remote status with `gh pr checks <pr>`. Interactive mode has not pushed, so report `local-fix-ready` with the local proof and the observed red or pending remote checks; never imply that local edits changed CI. If the remote checks are already green because another actor updated the branch, report the observed green state without attributing it to the local patch. Done when: the current `gh pr checks` output is captured and the result is `local-fix-ready` with remote status quoted, or an independently updated remote run is observed green with its output quoted.

## Autonomous mode (explicit user ask only)

Gate: enter only when the user asks for the fix to be pushed (for example "push the fix" or "land it on a fix branch"); never self-initiated. Before any mutation, preview the failing job, the exact change set, and the target branch `ci-fix/<original-branch>` — the plan approval from spine step 5 doubles as the push approval once the preview is acknowledged.

1. Run spine steps 1–5 (auth, locate, evidence, triage, plan). Done when: plan is approved in writing and the push preview (target branch, change set, failing job) is acknowledged by the user.
2. If workflow files must change: keep existing `permissions:` minimal, never broaden token access, no `pull_request_target` unless the user explicitly requested it. Done when: `git diff` on workflow files touches no permission key outside the previewed set.
3. Create or update the branch. New: `git checkout -b ci-fix/<original-branch>`. Existing: show its current commits, confirm reuse with the user, `git checkout ci-fix/<original-branch>`, then `git pull origin <original-branch>`. Done when: the branch is checked out and `git log --oneline -1` shows it carries only the previewed change.
4. Stage only the exact paths in the approved preview with `git add -- <paths>`, then inspect the staged path list and patch. Stop if the staged set contains any extra path. Commit `fix: resolve CI failure in <job-name>`, then push `git push -u origin ci-fix/<original-branch>` (plain `git push` once upstream is set). Done when: `git diff --cached --name-only` lists only the approved paths and `git push` succeeds with the remote branch at the pushed SHA confirmed by `git rev-parse origin/ci-fix/<original-branch>`.
5. Watch: `gh run list --branch ci-fix/<original-branch> --limit 1` for the new run id, then `gh run watch <new-run-id> --exit-status`. Re-trigger only failed jobs with `gh run rerun <new-run-id> --failed` when the evidence is infrastructure or a confirmed flake and the user approves; a rerun never substitutes for a deterministic fix. Done when: `gh run view <new-run-id> --json conclusion` reports `success`, or the failure classification below applies.
6. If new failures appear, repeat from spine step 4 treating the new failures as the current set. Stop only when every check in the set is green.

## Failure and recovery

- gh unauthenticated, or no failing run found for the supplied PR/branch/run ID: stop and report; nothing committed or pushed.
- Logs do not identify a root cause (insufficient logs, unreproducible secret or environment failure): report the evidence found; no guessed fix; in autonomous mode push nothing.
- The smallest fix requires widening scope beyond the failing job/step or broadening workflow permissions: stop and report why; never expand permissions to make tests pass.
- Local check does not reproduce the CI failure: do not push. Report the reproduction gap and attach the CI log as the blocked state.
- A fix resolves one check but breaks another: if not yet pushed, amend or discard the fix; if pushed, revert it. Re-triage treating the new break as a root cause.
- Interactive non-convergence: report remaining failures and the diff applied; roll back edited files via VCS when the user requests it.
- Autonomous run still red: diagnose the new failure and apply one further in-scope fix; still failing with no new actionable cause → blocked, with the failing-run link, analysis so far, and the exact failing job. Leave the branch and runs in place; never delete or force-push to hide a failure unless the user asks.
- Push or watch interrupted: the remote branch state is authoritative — re-run `gh run list --branch ci-fix/<original-branch> --limit 1` and resume watching; never re-push blindly.
- Push rejected (protected branch, conflict, permission): do not force-push. Report the rejection reason as the blocked state.
- Non-convergent: after repeated fix cycles, new failures keep appearing in the fix's own code. Stop. Report the non-convergent state with the failure chain; do not claim green or that the done predicate holds.

## Output

Interactive: failing-check report (check name, run URL, log snippet, missing-log notes), then the ordered root-cause record (per root cause: check name, root cause, changed paths), applied diff, local-check results, and the observed current `gh pr checks` status; terminal `local-fix-ready`, `blocked` with the exact reason, or `non-converged`. Autonomous: the ordered root-cause record plus a summary in fixed order — failing run (link or ID), root cause, fix (what changed), verification (new run link showing green); terminal `checks-pass`, `blocked` (exact reason), or `non-passing` (link and analysis).
