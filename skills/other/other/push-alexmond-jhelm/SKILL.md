---
name: push
description: Create/update GitHub issue, branch, commit, PR, then continue implementing
argument-hint: [issue-number or description]
allowed-tools: Bash(gh *), Bash(git *)
---

## Push Workflow: Issue → Branch → PR → Continue

Argument `$ARGUMENTS` is either:
- An **existing issue number** (e.g. `42`) — update it and wire up the branch/PR
- A **short description** (e.g. `add retry logic for HTTP calls`) — create a new issue first

---

### Step 1: Resolve or create the GitHub issue

**If `$ARGUMENTS` is a number** — view the existing issue:
```bash
gh issue view $ARGUMENTS
```

**If `$ARGUMENTS` is a description** — create a new issue:
```bash
gh issue create \
  --title "$ARGUMENTS" \
  --body "## Context
<fill in context from current conversation / recent commits>

## Acceptance criteria
- [ ] <criterion 1>
- [ ] <criterion 2>"
```
Capture the new issue number from the output (e.g. `#59`).

---

### Step 1.5: Shortcut — skill-only changes go directly to main

If the **only** changed files are under `.claude/skills/` (skill updates, no source code changes):

```bash
git diff --stat
```

If all changed files are `.claude/skills/**` files:
1. Skip Steps 2–6 (no branch, no PR)
2. Commit directly on `main`:
   ```bash
   git add .claude/skills/<changed-file>
   git commit -m "$(cat <<'EOF'
   <imperative summary under 72 chars>

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   EOF
   )"
   git push
   ```
3. Report the commit SHA and stop. No CI wait needed for skill-only commits.

Otherwise continue with the full workflow below.

---

### Step 2: Ensure we're on main and up to date
```bash
git checkout main && git pull
```

---

### Step 3: Create a feature branch named after the issue
```bash
git checkout -b feature/<issue-number>-<short-slug>
```
Where `<short-slug>` is 2–4 words from the issue title, kebab-cased (e.g. `feature/59-retry-http-calls`).

If a matching branch already exists, check it out instead:
```bash
git checkout feature/<issue-number>-<short-slug>
```

---

### Step 4: Stage and commit any local changes (if present)

Check for uncommitted work first:
```bash
git status
git diff --stat
```

If there are changes to commit:
```bash
git add <changed-files>
git commit -m "$(cat <<'EOF'
<imperative summary under 72 chars>

Closes #<issue-number>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

If there are **no** changes yet, skip this step — implementation comes after the PR is open.

---

### Step 5: Push the branch
```bash
git push -u origin HEAD
```

---

### Step 6: Create the pull request (draft if no code yet)
```bash
gh pr create \
  --title "<concise title matching issue>" \
  --body "$(cat <<'EOF'
## Summary
- <bullet 1>
- <bullet 2>

## Test plan
- [ ] Run `./mvnw test -pl <module>`
- [ ] Verify <key behavior>

Closes #<issue-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" \
  --draft
```

Remove `--draft` if there are already commits with real code on the branch.

Report the PR URL to the user.

---

### Step 7: Continue implementing

Now implement the work described in the issue:
- Read the issue body for full requirements
- Follow project coding standards (Java 21, Lombok, tabs, spring-javaformat)
- Run `./mvnw test -pl <module>` after each meaningful change
- When done, mark the PR ready for review:
  ```bash
  gh pr ready
  ```
