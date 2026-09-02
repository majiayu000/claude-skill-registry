---
name: autoship
description: 'Use when the user says release this, publish this package, or cut a release for a changesets-based npm package. Not for non-npm packages or releases without a changesets workflow.'
disable-model-invocation: true
---

# Autoship

## Contract

| Field | Bound contract |
|---|---|
| Trigger | release this, publish this package, autoship, cut a release, npm release flow |
| Authority | Human-only. Invoking autoship is standing consent for the full release flow; gate risky steps on objective preconditions instead of pausing mid-flow. Force-push, history rewrites, and destructive git operations require explicit confirmation. |
| Side effect | Writes a changeset file, runs quality-gate fixers, commits and pushes, merges the bot-opened Version Packages PR, and publishes to npm. Restricted to VCS-tracked targets and the npm registry. |
| Done | New version is published on npm and confirmed by `npm view <package> version` matching the merged `package.json`. |

## Inputs

- A changesets-based npm package with a release workflow in `.github/workflows/` using `changesets/action`.
- Optional bump level: defaults to `patch`; `minor` or `major` only on explicit user instruction.
- No new changeset is required if one already exists on the default branch and the intent is to watch or merge only.

## Procedure

The release workflow runs twice. First, push a commit carrying a pending `.changeset/*.md` file. The workflow runs `changeset version` in CI and opens a "Version Packages" PR on branch `changeset-release/main`. Merge that PR; the workflow runs again and, with no pending changesets left, runs `changeset publish`. The local job ends at pushing the changeset file. CI owns versioning and publishing; anything versioned locally breaks the loop.

1. Create the changeset. Check for pending changesets (`ls .changeset/*.md` excluding `README.md`). If any exist, ask whether to add another or skip. Write the file directly because `npm run changeset` needs a TTY:
   ```
   cat > .changeset/<short-id>.md << 'EOF'
   ---
   "<package-name>": patch
   ---
   <one or two sentences of user-facing change>
   EOF
   ```
   Generate the short id with `node -e "console.log(Math.random().toString(36).slice(2,10))"`. The description ships verbatim in `CHANGELOG.md` and is the only thing consumers read about this version. Done when: the changeset file is written with a valid package bump and user-facing description.

2. Fix quality gates. Discover scripts from `package.json` (`jq '.scripts | keys[]' -r`); in non-npm repos check `Makefile`, `Cargo.toml`, `pyproject.toml`, `go.mod`. Run gates in order: lint, typecheck, test, format. Scope auto-fixers (`lint --fix`, `format`) to changed files where supported; after any fixer check `git status` and `git restore` unrelated churn (MDX is a frequent casualty). On failure, parse output for file, line, code, and message; fix syntax errors first, then type errors, then lint errors, one root cause at a time when errors cascade. Re-run every gate from the start after any code change, not just the failed one, because a type fix routinely breaks lint and a lint autofix can break a test. Retry each gate up to 5 fix iterations, reporting the gate, remaining error count, and last error output on exhaustion. Done when: every gate passes or the retry budget is exhausted with the failure reported.

3. Commit and push the changeset. Stage the changeset file and in-scope fixes only with explicit paths — never `git add -A`, which silently commits pre-commit-hook artifacts such as a root `schema.gql`. Sweep `git status --porcelain` for stray generated artifacts and unrelated fixer churn before committing. Commit `chore: add <type> changeset for <package>` and push. Do NOT run `npx changeset version` locally: it consumes the `.changeset/*.md` file, the pushed commit loses its pending changeset, the "Changeset Status" check fails, and no Version Packages PR opens. Do NOT run `npm publish` directly or hand-edit `CHANGELOG.md` or `package.json` `version`; CI generates both in the Version Packages PR and local edits create conflicts that make the bot PR unmergeable. Done when: the changeset commit is pushed and no local version or publish command ran.

4. Monitor CI and merge the Version Packages PR. Start a background watch scoped to the pushed commit SHA (not branch, so older pushes do not bleed in), emitting state changes and a `TERMINAL:` line when every workflow run completes. Do not stop on an idle first poll; runs take time to queue. Keep `sleep` at 30s or more to avoid burning the GitHub API rate limit:
   ```
   SHA=$(git rev-parse HEAD); LAST=""
   while true; do
     CUR=$(gh run list --commit "$SHA" --limit 20 \
       --json status,conclusion,workflowName,databaseId \
       --jq 'map("\(.databaseId)|\(.workflowName)|\(.status)|\(.conclusion // \"\")")|.[]')
     [ "$CUR" != "$LAST" ] && { echo "---"; echo "$CUR"; LAST="$CUR"; }
     [ -z "$CUR" ] && { sleep 30; continue; }
     echo "$CUR" | grep -qv '|completed|' && { sleep 30; continue; }
     echo "$CUR" | grep -qv '|success$' && echo "TERMINAL: failure" || echo "TERMINAL: success"
     exit 0
   done
   ```
   Any non-`success` conclusion (`failure`, `cancelled`, `timed_out`, `action_required`, `neutral`, `skipped`, `stale`) is a failure. On failure, classify via `gh run view <id> --log-failed`: flaky or infrastructure failures get `gh run rerun <id> --failed` up to 3 times; real failures get a fix, commit, push, and a fresh watch. Once green, find the open PR titled "Version Packages" on branch `changeset-release/main` (`gh pr list --search "Version Packages" --state open --json number,headRefName`; the valid JSON field is `headRefName`, not `headBranch`). If absent, watch for it capped at 10 minutes. Verify every merge precondition before merging: the PR title is exactly "Version Packages" or the head branch is `changeset-release/main` — never merge any other PR. Confirm all required checks pass. Merge the PR. Done when: the Version Packages PR is merged with all preconditions verified.

5. Watch the publish run and verify on npm. Merging triggers the same workflow again, which publishes. Identify the workflow file in `.github/workflows/` (commonly `release.yml`, `npm-publish.yml`, `publish.yml`) and watch its latest run on the default branch for a `TERMINAL:` line. On failure, report with logs and stop — never auto-retry; publish failures are real (npm auth, registry, OIDC/provenance, tag conflict). On success, verify `npm view <package> version` against the merged `package.json`, stop all background watches, and report the version. The `npm view` output is the completion evidence; never report success without it. Done when: `npm view <package> version` matches the merged `package.json` and all watches are stopped.

## Failure and recovery
- Quality gate still failing after 5 iterations: stop, report the gate, remaining error count, and last error output.
- CI fails after the changeset push: classify flaky or infrastructure (rerun `--failed`, max 3) versus real (fix, push, fresh watch).
- "Changeset Status" check fails: missing changeset → add one (Step 1); consumed state from a local `changeset version` → revert the version bump and `CHANGELOG.md` edit, re-add the changeset file, and force-push. Rerunning CI cannot fix consumed state.
- Version Packages PR absent after 10 minutes: check that pending changesets exist on the default branch, the workflow file exists, and the action ran (`gh run list`).
- Merge precondition fails: stop and report; never override failing checks or resolve conflicts in the bot PR.
- Publish run fails: never auto-retry; report with logs.
- Partial-result rule: a failure at any step leaves the release half-shipped (changeset pushed, PR open, or publish pending). Report the exact state and the next human action rather than widening scope or pretending the done predicate holds. Rollback is version control: revert the changeset commit or close the Version Packages PR; never rewrite published registry state.

## Output
The published version string from `npm view <package> version` confirmed against the merged `package.json`, plus a one-line release summary — on any blocked or non-converged state, a report naming the failed step, remaining error count or failing check, and next human action.
