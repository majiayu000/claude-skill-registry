---
name: ship
description: Automates the full code release pipeline — branch, commit, push, PR, wait for CI, merge, version bump, release, cleanup.
argument-hint: 'conventional commit message, e.g. "feat: add new feature"'
model: claude-sonnet-4-6
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
  - Glob
---

## Your Task

Automate the complete release pipeline for this plugin using the conventional commit message provided.

**Input**: `$ARGUMENTS`

This is a conventional commit message (e.g., `feat: streaming URL management tools`).

---

# Ship — Automated Code Release Pipeline

You automate the entire release workflow from uncommitted changes on `main` to a published GitHub Release with version bump.

**Pipeline**:
```
[uncommitted changes on main]
  → create feature branch
  → commit with conventional commit message
  → push + create PR
  → poll CI checks until all pass (or fail)
  → merge PR
  → pull main
  → determine version bump from commit prefix
  → update plugin.json + marketplace.json + CHANGELOG + README badges
  → commit "chore: release 0.x.0"
  → push to main (triggers auto-release.yml → GitHub Release)
  → delete local feature branch
```

---

## Step 0: Parse Input

Extract from `$ARGUMENTS`:

1. **Full commit message** — the entire string (e.g., `feat: streaming URL management tools`)
2. **Prefix** — the conventional commit type before the colon: `feat:`, `fix:`, `feat!:`, `docs:`, `chore:`
3. **Description** — everything after the prefix (e.g., `streaming URL management tools`)
4. **Branch name** — derived from the message: lowercase, spaces to hyphens, prefix becomes the branch prefix
   - `feat: streaming URL management tools` → `feat/streaming-url-management-tools`
   - `fix: correct audio path` → `fix/correct-audio-path`
   - `feat!: breaking change` → `feat/breaking-change`
   - `docs: update README` → `docs/update-readme`
   - `chore: cleanup` → `chore/cleanup`
5. **Version bump type**:
   - `feat:` → MINOR (0.57.0 → 0.58.0)
   - `fix:` → PATCH (0.57.0 → 0.57.1)
   - `feat!:` → MAJOR (0.57.0 → 1.0.0)
   - `docs:` or `chore:` → **none** (skip version bump and release steps)

If `$ARGUMENTS` is empty or doesn't match a conventional commit pattern, **stop** and ask the user for a commit message.

---

## Step 1: Pre-flight Checks

Run these checks. If ANY fail, **stop immediately** with a clear error message.

1. **On main branch?**
   ```bash
   git branch --show-current
   ```
   Must be `main`. If not: "Switch to main first: `git checkout main && git pull`"

2. **Uncommitted changes exist?**
   ```bash
   git status --porcelain
   ```
   Must have output. If empty: "No changes to ship. Make some changes first."

3. **GitHub CLI authenticated?**
   ```bash
   gh auth status
   ```
   Must succeed. If not: "Run `gh auth login` first."

4. **Read current version** from `.claude-plugin/plugin.json`:
   ```bash
   jq -r '.version' .claude-plugin/plugin.json
   ```
   Store as `CURRENT_VERSION`.

Report: "Pre-flight passed. Current version: {CURRENT_VERSION}. Shipping: {commit message}"

---

## Step 2: Branch + Commit + Push

1. **Create feature branch**:
   ```bash
   git checkout -b {branch-name}
   ```

2. **Stage files** — use `git status` to identify changed files. Stage them by name. **Never** stage `.env`, `credentials`, or secret files. Prefer specific filenames over `git add -A`.

3. **Commit** with the conventional commit message + co-author:
   ```bash
   git commit -m "$(cat <<'EOF'
   {full commit message}

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```

4. **Push**:
   ```bash
   git push -u origin {branch-name}
   ```

---

## Step 3: Create PR

Create a pull request using the commit message as the title:

```bash
gh pr create --title "{full commit message}" --body "$(cat <<'EOF'
## Summary
{1-3 bullet points summarizing what changed}

## Test plan
- [ ] CI checks pass (automated)
- [ ] Version sync validates (automated)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Capture the PR number from the output for subsequent steps.

---

## Step 4: Wait for CI Checks

Poll CI using `gh pr checks` with the `--watch` flag:

```bash
gh pr checks {pr-number} --watch --fail-level all
```

This blocks until all checks complete. Use a 10-minute timeout.

**If any check fails**:
- Report which check(s) failed
- Print the failing check URL(s) if available
- **Stop the pipeline** — leave the PR open for the user to investigate
- Say: "CI failed. Fix the issues, push to the branch, and re-run `/bitwize-music:ship` or merge manually."
- **Do NOT proceed to merge.**

**If all checks pass**: Report "All CI checks passed." and continue.

---

## Step 5: Merge PR

1. **Merge the PR** (merge commit, delete remote branch):
   ```bash
   gh pr merge {pr-number} --merge --delete-branch
   ```

2. **Switch back to main and pull**:
   ```bash
   git checkout main && git pull origin main
   ```

---

## Step 6: Version Bump

**Skip this entire step if the prefix is `docs:` or `chore:`.**

### 6a: Calculate new version

From `CURRENT_VERSION` and the bump type:
- MINOR: increment middle number, reset patch to 0 (e.g., 0.57.0 → 0.58.0)
- PATCH: increment last number (e.g., 0.57.0 → 0.57.1)
- MAJOR: increment first number, reset others to 0 (e.g., 0.57.0 → 1.0.0)

Store as `NEW_VERSION`.

### 6b: Update `.claude-plugin/plugin.json`

Change `"version": "{CURRENT_VERSION}"` → `"version": "{NEW_VERSION}"`

### 6c: Update `.claude-plugin/marketplace.json`

Change `"version": "{CURRENT_VERSION}"` → `"version": "{NEW_VERSION}"`

### 6d: Update `CHANGELOG.md`

1. Find the current `## [Unreleased]` section content
2. Insert a new versioned section between `[Unreleased]` and the previous version:
   - Empty `## [Unreleased]` section at top
   - Then `## [{NEW_VERSION}] - {YYYY-MM-DD}` with the content that was under Unreleased
3. The date is today's date

### 6e: Update README.md badges

Update these badge lines:
- Version badge: `![Version](https://img.shields.io/badge/version-{NEW_VERSION}-blue)`
- Skills count badge: count directories in `skills/*/` and update `![Skills](https://img.shields.io/badge/skills-{COUNT}-green)`
- Test count badge: run `pytest --co -q 2>/dev/null | tail -1` to get the count, update `![Tests](https://img.shields.io/badge/tests-{COUNT}-brightgreen)`

### 6f: Update README "What's New" table (for `feat:` and `feat!:` only)

If the commit is a `feat:` or `feat!:`:
- Read the CHANGELOG entry for this version
- Add a row to the "What's New" table in README.md at the top (below the header row)
- Format: `| **{MINOR_VERSION}** | {brief highlight} |`
- Example: `| **0.58** | Ship skill for automated code release pipeline |`

### 6g: Update README skill count text

If a new skill was added, update the "collection of **N specialized skills**" text in README.md to match the badge count.

---

## Step 7: Release Commit + Push

**Skip if `docs:` or `chore:` prefix (no version bump happened).**

1. **Stage the version files**:
   ```bash
   git add .claude-plugin/plugin.json .claude-plugin/marketplace.json CHANGELOG.md README.md
   ```

2. **Commit**:
   ```bash
   git commit -m "$(cat <<'EOF'
   chore: release {NEW_VERSION}

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```

3. **Push to main** — this triggers `auto-release.yml` which creates the GitHub Release:
   ```bash
   git push origin main
   ```

---

## Step 8: Cleanup

1. **Delete local feature branch** (it was already deleted from remote by `--delete-branch`):
   ```bash
   git branch -d {branch-name}
   ```

2. **Report success**:
   ```
   Ship complete!

   Commit: {full commit message}
   Version: {CURRENT_VERSION} → {NEW_VERSION}
   PR: {PR URL}
   Release: auto-release.yml will create GitHub Release for v{NEW_VERSION}

   Branch {branch-name} cleaned up (local + remote).
   ```

   For `docs:`/`chore:` (no version bump):
   ```
   Ship complete!

   Commit: {full commit message}
   Version: unchanged ({CURRENT_VERSION})
   PR: {PR URL}

   No version bump for {prefix} commits.
   Branch {branch-name} cleaned up (local + remote).
   ```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Not on `main` | Stop. Tell user to `git checkout main && git pull`. |
| No uncommitted changes | Stop. "Nothing to ship." |
| `gh` not authenticated | Stop. Suggest `gh auth login`. |
| CI check fails | Stop. Report failure details. Leave PR open. |
| Merge conflict | Stop. Report conflict. Let user resolve. |
| Push rejected | Stop. Report error. Suggest `git pull --rebase`. |
| Invalid commit message | Stop. Show expected format with examples. |

**Never force-push. Never skip CI. Never auto-close a failed PR.**

---

## Remember

1. **Parse the commit message first** — everything flows from the prefix
2. **Pre-flight is non-negotiable** — stop if any check fails
3. **Stage files by name** — never `git add -A` or `git add .`
4. **CI must pass** — never merge with failing checks
5. **Version bump follows conventional commits** — `feat:` = MINOR, `fix:` = PATCH, `feat!:` = MAJOR
6. **Both JSON files must match** — plugin.json and marketplace.json versions stay in sync
7. **CHANGELOG gets the content** — move Unreleased to versioned section
8. **Badges must match** — version, skills count, test count in README
9. **`chore: release` commit triggers auto-release.yml** — which creates the GitHub Release
10. **Clean up branches** — delete local and remote after merge

**Your deliverable**: Changes shipped from uncommitted code to published GitHub Release in one automated pipeline.
