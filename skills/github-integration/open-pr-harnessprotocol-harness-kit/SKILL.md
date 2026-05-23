---
name: open-pr
description: Use when wrapping up a development task and getting a PR ready — runs local tests, creates a PR (if one doesn't exist) with a structured description template, conducts a code review via the review skill, and checks CI status with quick fixes. Trigger when the user says they're done with a feature, want to open a PR, wrap up, finalize their work, or push their branch for review. Also invoke proactively after completing all tasks in an implementation plan. Does NOT merge — suggests /merge-pr when the PR is ready to land.
---

# Open PR

A structured PR preparation workflow: tests → create PR → code review → CI → hand off to merge.

**Announce at start:** "I'm using the open-pr skill to get this PR ready."

---

## Step 1: Pre-flight — Run Local Tests

Run the test suite before touching anything else. Detect the right command from project files:

| Indicator | Command |
|-----------|---------|
| CLAUDE.md test command | Use that (takes precedence over all below) |
| `go.mod` | `go test ./...` |
| `package.json` | `npm test` or `yarn test` |
| `pyproject.toml` / `setup.py` | `pytest` |
| `Cargo.toml` | `cargo test` |

If **tests fail:** Stop. Show the failures clearly. Don't proceed — fix them or ask the user how to handle. Do not skip or bypass test hooks.

If **tests pass:** Continue.

---

## Step 2: Check for Existing PR

```bash
gh pr view --json number,url,state 2>/dev/null
```

- **PR already open:** Skip to [Step 4 — Code Review](#step-4-code-review).
- **No PR:** Continue to Step 3.

---

## Step 3: Create the PR

### Push the branch

```bash
git push -u origin $(git branch --show-current)
```

### Title

Use the most meaningful commit message as a starting point, cleaned up to be concise. Follow conventional commit format (`feat:`, `fix:`, `refactor:`, etc.) if the repo uses it — check recent commits with `git log --oneline -10`.

### Auto-detect labels

Infer labels from the branch name and commits — apply with `--label` if the label exists in the repo:

| Pattern | Label |
|---------|-------|
| `fix/`, `bug/`, "fix" in commits | `bug` |
| `feat/`, `feature/` | `enhancement` |
| `refactor/`, `chore/` | `refactor` |
| `docs/` | `documentation` |

Skip labels that don't exist in the repo rather than erroring.

### PR description template

Fill in every section based on the actual changes — no unfilled placeholders:

```
## Summary
<!-- What this PR does and why — 2-4 sentences. Lead with intent, not implementation. -->

## Changes
<!-- Key changes. Be specific — not "updated code" but what and why. -->
-

## Test Plan
<!-- How this was verified -->
- [ ] Local tests pass
- [ ] CI checks pass
- [ ] <any manual or integration steps>

## Notes
<!-- Edge cases, follow-ups, known limitations, or anything a reviewer should know -->
```

### Create

```bash
gh pr create \
  --title "<title>" \
  --body "$(cat <<'EOF'
<filled-template>
EOF
)"
```

Leave `--reviewer` and `--assignee` unset.

---

## Step 4: Code Review

Invoke the `review` skill (use the Skill tool) to review all changes in this PR.

The review should cover:
- **Baseline:** correctness, security, error handling, performance, naming clarity
- **Test coverage:** flag any new functionality that lacks tests
- **Codebase-specific:** scan CLAUDE.md for any `## Code Review`, `## Standards`, or `## Gotchas` sections and incorporate those requirements

After the review, present a clear report:

```
Code Review Report
──────────────────
[MUST FIX] <issue> — <file>:<line>
[SUGGESTION] <issue>
No blocking issues found.
```

**If MUST FIX items:** Address them, commit, push. Once resolved, continue to Step 5.

**If only suggestions:** Note them for the user to follow up post-merge at their discretion.

---

## Step 5: CI Status

```bash
gh pr checks
```

**All passing:** Continue.

**Failing:**
1. Read the failure output — identify root cause
2. **Quick fix** (lint, formatting, import, typo): Fix it, commit, push, wait for CI to rerun, then continue
3. **Complex failure** (logic error, architecture issue, flaky infra): Stop and report clearly:
   > "CI is failing due to [X]. This needs a dedicated fix before merging — let's plan it out."

Never proceed to merge with failing CI.

---

## Step 6: Report and Hand Off

Once tests, review, and CI are all green, report the PR status and suggest the next step:

```
PR #<N> is ready to merge.
──────────────────────────
Title:  <title>
Branch: <branch> → <base>
URL:    <url>

✓ Local tests pass
✓ Code review clean (or: N suggestions noted for follow-up)
✓ CI passing

Run /merge-pr to squash merge and clean up.
```

Do not merge, rebase, or push anything further. Hand off cleanly.

---

## Quick Reference

| Step | Action | Block on failure? |
|------|--------|-------------------|
| 1. Local tests | Run test suite | Yes — fix first |
| 2. PR check | Exists? | Skip to review |
| 3. Create PR | Push + `gh pr create` | — |
| 4. Code review | `review` skill | Yes for MUST FIX |
| 5. CI | `gh pr checks` | Yes — fix or stop |
| 6. Report | PR summary + `/merge-pr` suggestion | — |

## Rules

**Never:**
- Proceed with failing tests or CI
- Merge, rebase, or force-push anything
- Use `--no-verify` to bypass hooks
- Leave PR template sections unfilled
- Set reviewer or assignee

**Always:**
- Address MUST FIX review items before handing off
- Suggest `/merge-pr` at the end
