---
name: pr-review
description: Review a pull request for spec alignment, architecture, tests, and docs. No code changes.
---

# PR Review

Review a PR against its linked issue and project constraints. Do not push fixes.

## Inputs

PR number or URL. Reviewer GitHub login (must not be PR author). Any custom concerns.

## Review-aware

Before starting: check if `<pr-slug>.findings.md` exists. If it does, incorporate prior findings into this review.

## Workflow

1. **Verify identity** — Run `gh api user --jq .login`. If reviewer == PR author, stop and request an identity switch.

   If you need a separate reviewer identity (e.g., work vs. personal account):
   ```bash
   # One-time setup for a reviewer account
   GH_CONFIG_DIR=~/.config/gh-reviewer gh auth login
   # Then prefix all gh commands with GH_CONFIG_DIR=~/.config/gh-reviewer
   GH_CONFIG_DIR=~/.config/gh-reviewer gh api user --jq .login
   ```

2. **Load PR + spec** — Run `gh pr view <n>` and `gh pr diff <n>`. Extract linked issue (`Fixes #X`) and read its full spec.

3. **Review** — Check:
   - Spec alignment (goals, scope, success criteria)
   - Architecture compliance (AGENTS.md invariants, authoritative systems)
   - Testing posture (new tests where appropriate; no unjustified test edits)
   - Docs drift or duplication
   - Git hygiene (commit structure, no debug leftovers)
   - If a check is red, compare against `main` and inspect the full PR commit range before classifying it. If the failure appears anywhere in the PR range, treat it as branch-owned regression and review it as part of the PR.

4. **Report findings** — Group by severity (Critical/Major/Minor) with `path:line` references. State a clear decision: approve / request changes / non-blocking.

5. **Submit** — Use `/findings` to write `<pr-slug>.findings.md`, OR submit via:
   ```
   gh pr review <n> --request-changes --body "..."
   ```
   Do not review as the PR author.
