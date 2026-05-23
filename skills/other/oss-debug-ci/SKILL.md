---
name: oss-debug-ci
description: |
  Debug CI failures in unfamiliar repo pipelines. Reads CI configs, fetches failure
  logs, classifies the failure type, and guides the user through diagnosing and fixing
  the issue. Use when CI fails on your PR in an OSS repo, when you don't understand
  a CI error, or when debugging GitHub Actions/CircleCI/other CI systems. Not for
  setting up CI from scratch — this is for debugging existing pipelines.
---

# Debug CI

CI failed on someone else's repo and the error makes no sense. This skill teaches you to read CI pipelines, classify failures, and fix them — instead of pushing blind patches and hoping.

## Purpose

CI failures in unfamiliar repos are disorienting. The error might come from a linter you've never configured, a test runner with custom settings, or a platform-specific incompatibility. Most contributors respond by pushing random fixes until green. This skill teaches you to read the pipeline, understand what failed and why, determine if it's your fault, and fix it systematically.

## When to Use

- CI fails on your PR and you don't understand the error
- CI failure is in a tool/system you haven't used before
- You suspect the failure is pre-existing (flaky test, broken main)
- You need to reproduce a CI failure locally
- **NOT** when setting up CI for a new project — that's infrastructure work
- **NOT** when CI passes but the code is wrong — that's `oss-contribute`

## Prerequisites

- A PR submitted to an OSS repo (from `oss-submit-pr`)
- `gh` CLI authenticated
- Access to the CI logs (public repo or you have permissions)

## Process

### 1. Identify the CI system and read the config

Before looking at logs, understand the pipeline structure.

```bash
# Find CI configuration files
ls -la .github/workflows/ 2>/dev/null
ls -la .circleci/ 2>/dev/null
ls -la .travis.yml Jenkinsfile .gitlab-ci.yml .buildkite/ azure-pipelines.yml 2>/dev/null

# Read the relevant workflow
cat .github/workflows/ci.yml  # or whatever the CI config is
```

Map the pipeline:
- What jobs exist? (build, test, lint, typecheck, etc.)
- What order do they run in? (parallel or sequential?)
- What OS/container do they run on? (ubuntu, macos, windows, custom image?)
- What language/tool versions are pinned? (node 20, python 3.12, go 1.22?)
- What caching is used? (dependency caching, build caching?)

### 2. Fetch the failure logs

```bash
# List recent CI runs for your PR
gh run list --branch $(git branch --show-current) --limit 5

# View the failed run
gh run view {run-id}

# Get the specific failure logs
gh run view {run-id} --log-failed

# If you need the full log for a specific job
gh run view {run-id} --log --job {job-id}
```

Isolate the actual error from surrounding noise. CI logs are verbose — most of the output is setup and teardown. The failure is usually in the last 20-50 lines of a failed step.

### 3. Classify the failure

Determine what kind of failure you're dealing with. This determines your fix strategy.

| Failure Type | Signals | Fix Strategy |
|-------------|---------|--------------|
| **Build error** | Compilation failed, import not found, type error | Your code has a syntax or type issue. Fix locally. |
| **Test failure** | Assertion failed, expected X got Y | Your changes broke a test. Read the test to understand what it expects. |
| **Lint/format failure** | Style violation, unused import, formatting diff | Run the repo's formatter/linter locally. Often auto-fixable. |
| **Dependency resolution** | Package not found, version conflict, lockfile mismatch | You changed deps or the lockfile is stale. Regenerate it. |
| **Environment mismatch** | Works locally, fails in CI | Different OS, different tool version, missing env var. |
| **Flaky test** | Test passes sometimes, fails sometimes. Same code. | Not your fault. Check if this test fails on main too. |
| **Pre-existing failure** | Main branch has the same failure | Not your fault. Comment on PR noting pre-existing failure. |
| **Timeout** | Job exceeded time limit | Your changes might be slow, or CI is under load. Check if it's reproducible. |
| **Permission/secret issue** | Auth failed, secret not found | Fork PRs can't access repo secrets. Check if the job needs secrets. |

### 4. Determine if the failure is yours

This is the critical question. Don't fix what isn't broken.

```bash
# Check if the same job fails on main
gh run list --branch main --limit 5 --workflow {workflow-name}
gh run view {latest-main-run-id} --log-failed

# Check if this test is known to be flaky
gh issue list -R {owner}/{repo} --search "flaky {test-name}" --state open
gh issue list -R {owner}/{repo} --label "flaky" --state open

# Try rebasing onto latest main — maybe the failure was already fixed
git fetch origin main
git rebase origin/main
```

If the failure exists on main: **it's not your problem**. Comment on your PR:
```
CI failure in `{job-name}` appears to be pre-existing — the same test fails on main ([run link]). Happy to help fix separately if useful.
```

### 5. Reproduce locally

If the failure IS from your changes, reproduce it before fixing blindly.

```bash
# Run the exact command CI runs (read it from the CI config)
# Don't guess — copy the exact command from the workflow file

# Common examples:
npm run test          # not just "npm test" if the script is different
pytest -x             # might need specific flags
make lint             # might include multiple linters
cargo clippy -- -D warnings  # might treat warnings as errors
```

If it passes locally but fails in CI:
- Check tool versions: `node --version`, `python --version`, etc. vs CI config
- Check for OS-specific behavior (path separators, line endings, case sensitivity)
- Check for missing environment variables (CI might set `CI=true` which changes behavior)
- Check for timing issues (CI machines are slower, timeouts may differ)

### 6. Thinking gate — user explains the failure

> "Now that you've seen the logs and classified the failure:
> 1. What type of failure is this? (Use the classification table above)
> 2. Is it caused by your changes or pre-existing?
> 3. What do you think the fix is? (Be specific — what file, what change)"

Wait for their answer. If they say "I don't know," point them to the specific log line and CI config step that failed. Don't hand them the answer.

### 7. Fix and verify

The user fixes the issue based on their diagnosis. The LLM helps with:
- Explaining unfamiliar CI tools or configurations
- Finding the right commands to reproduce locally
- Pointing to CI documentation when needed

```bash
# After fixing, run the failing command locally
# {exact command from CI config}

# Push the fix
git add {changed-files}
git commit -m "{descriptive message about the CI fix}"
git push
```

### 8. Monitor the re-run

```bash
# Watch the new CI run
gh run list --branch $(git branch --show-current) --limit 1
gh run watch {new-run-id}
```

If it fails again with a DIFFERENT error: go back to step 2. CI pipelines are sequential — fixing one failure may reveal the next.

If it fails with the SAME error: your fix didn't work. Re-read the logs more carefully. The error message might be misleading — look at the lines above and below it for context.

## Related Skills

- **Previous step**: ← `oss-submit-pr` — CI runs after you submit
- **Previous step**: ← `oss-post-pr` — reviewer may ask you to fix CI
- **If code changes needed**: → `oss-contribute` — if the fix requires significant code changes
- **Return to**: → `oss-post-pr` — after CI is green, continue with review

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I'll just push a fix and see if CI goes green" | Blind pushing wastes CI minutes (a shared resource), clutters your commit history, and tells maintainers you don't understand the codebase. Diagnose first. |
| "It passes locally so CI must be wrong" | CI is usually right. It uses pinned versions, clean state, and different OS. If it fails in CI and passes locally, YOU have the wrong environment. |
| "I'll just skip this CI check" | You can't skip CI on someone else's repo. Even if you could, the maintainer will notice and reject your PR. |
| "I'll ask the maintainer to re-run CI, it's probably flaky" | Check if it's flaky first (step 4). Asking maintainers to re-run without evidence wastes their time and makes you look like you didn't try. |
| "I'll copy the fix from another PR that had the same error" | Same error message doesn't mean same root cause. Understand YOUR failure before applying someone else's fix. |

## Red Flags

- User pushes 3+ "fix CI" commits without reading the logs — they're guessing, not debugging
- Failure is in a job unrelated to the user's changes (e.g., docs build fails on a code PR) — likely pre-existing
- User wants to modify CI config files — that's almost never the right fix for a contributor PR
- Same failure type keeps recurring across multiple pushes — the diagnosis is wrong

## Verification Checklist

- [ ] CI system and pipeline structure understood (step 1)
- [ ] Failure classified by type (step 3)
- [ ] Determined whether failure is from user's changes or pre-existing (step 4)
- [ ] Failure reproduced locally (step 5, if applicable)
- [ ] User explained the failure type, cause, and fix (step 6)
- [ ] Fix pushed and CI passes (step 7-8)
- [ ] No unnecessary "fix CI" commits cluttering the history

## Anti-patterns

- **DO NOT** push blind fixes without reading the logs — diagnose first, fix second
- **DO NOT** modify CI configuration files in a contributor PR — fix your code, not the pipeline
- **DO NOT** assume "works locally" means CI is wrong — CI has the authoritative environment
- **DO NOT** ask maintainers to re-run without checking if the failure is pre-existing first
- **DO NOT** let the user skip classification — knowing the failure TYPE determines the fix strategy
