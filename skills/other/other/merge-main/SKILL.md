---
name: merge-main
description: >
  Use when all feature work is merged to `develop` and the batch is ready to
  ship to `main`. Handles the full release workflow: NEWS.md update, version
  bump, develop → main PR, CI monitoring, merge, tagging, and post-release
  dev version bump. Trigger when the user says "merge to main", "release time",
  "prepare release", "ship this", "release vX.Y.Z", or "merge develop to main".
  CRITICAL: This skill only edits NEWS.md and DESCRIPTION. It does NOT write
  or edit R source files, test files, or any other source code.
---

# Merge-Main Skill

## HARD CONSTRAINT — READ THIS FIRST

**YOU ARE A RELEASE AGENT.**

You CANNOT write, edit, or create:
- `.R` source files
- `.R` test files
- Any other source code

**The ONLY files you may create or edit:**
- `NEWS.md` — the user-facing changelog
- `DESCRIPTION` — version field only

If you find yourself about to use the Edit or Write tool on a `.R` file,
**stop immediately**. Report what you found and ask the user whether to
address it before proceeding with the release.

---

## Session Recovery — Check This Before Starting

Call `TaskList` first. If a "Release:" task already exists `in_progress`:

| Task state | What to do |
|---|---|
| Release task `in_progress`, no PR yet | Resume from Step 3 |
| Release task `in_progress`, PR exists, CI pending | Resume CI monitoring (Step 6) |
| Release task `in_progress`, PR merged, not tagged | Resume from Step 7 |
| Release task `completed` | Report that the release is done — nothing to do |
| No tasks | Fresh start — proceed to Step 1 |

---

## Step 1: Pre-flight

Run these first:

```bash
git branch --show-current
git status
```

**If not on `develop`: STOP.** Tell the user to `git checkout develop` first.

**Check GitHub merge settings:** The repo must have "Allow merge commits" enabled
(GitHub → Settings → General → Pull Requests). Both squash and regular merge can be
active simultaneously. If only squash is enabled, the `--merge` flag in Step 8 will
fail — ask the user to enable merge commits before proceeding.

**If working tree is not clean:** report what's uncommitted. Ask the user
whether to stash or commit the changes before proceeding.

Confirm the release version with the user:

> "What version is this release? (Current DESCRIPTION version: X.Y.Z.9000)"

The release version is `X.Y.Z` (drop the `.9000`). Confirm with the user
before proceeding — do not infer it.

Find the last release tag on `main`:

```bash
git describe --tags --abbrev=0 origin/main
```

Show the user what's changed since that tag:

```bash
git log <last-tag>..develop --oneline
```

Create the main tracking task:

```
TaskCreate:
  subject:    "Release: vX.Y.Z"
  description: "Full release workflow for vX.Y.Z."
  activeForm: "Preparing release vX.Y.Z"

TaskUpdate:
  status: in_progress
```

---

## Step 2: Draft NEWS.md

### Find the changelog files

Identify all changelog files added to `develop` since the last release tag:

```bash
git diff <last-tag>..develop --name-only | grep "^changelog/"
```

Read each file. These are the source material for the NEWS.md section.

### Draft the new section

Write a draft NEWS.md section following the format in `refs/news-format.md`.

**Show the draft to the user and ask for approval.** Do not write to NEWS.md
until the user approves the content. Revise if requested.

---

## Step 3: Write NEWS.md and Bump DESCRIPTION

Once the user approves the draft:

### Write NEWS.md

Insert the new section at the very top of `NEWS.md`, above any existing
`# surveycore` header.

Verify the file structure looks correct after writing: new section at top,
previous version's section immediately below.

### Bump DESCRIPTION

Edit `DESCRIPTION`: change `Version: X.Y.Z.9000` to `Version: X.Y.Z`.

---

## Step 4: Run devtools::check()

```bash
Rscript -e "devtools::check()"
```

**Required:** 0 errors, 0 warnings, ≤2 notes.

**If it fails:** STOP. Report the failure. Do not proceed to committing.
If the failure is in R source code, tell the user and ask them to fix it
(this skill cannot edit `.R` files). Re-run after the fix is confirmed.

---

## Step 5: Commit and Push to develop

Stage only `NEWS.md` and `DESCRIPTION`:

```bash
git add NEWS.md DESCRIPTION
git status   # verify only those two files are staged
```

Commit:

```bash
git commit -m "$(cat <<'EOF'
chore(release): bump version to X.Y.Z

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"

git push origin develop
```

---

## Step 6: Create PR develop → main

### Check for existing PR

```bash
gh pr list --base main --head develop
```

If one already exists: report its URL and skip to Step 7 (Monitor CI).

### Draft the PR

PR title: `chore(release): bump version to X.Y.Z`

PR body — use the template in `refs/release-pr-template.md`, filling
in the NEWS.md section content for "What's in this release".

**Show the draft to the user before creating.** Ask for approval. Do NOT
create the PR until the user approves.

### Create the PR

```bash
gh pr create \
  --base main \
  --title "chore(release): bump version to X.Y.Z" \
  --body "$(cat <<'EOF'
<approved-body>
EOF
)"
```

Store the PR URL:

```
TaskUpdate:
  metadata: { prUrl: "<url>", prNumber: <N> }
```

Report the PR URL to the user.

---

## Step 7: Monitor CI

Create a CI tracking task:

```
TaskCreate:
  subject:    "CI: release vX.Y.Z"
  description: "Monitoring CI for release PR #N"
  activeForm: "Monitoring CI for release vX.Y.Z"

TaskUpdate:
  status: in_progress
```

Wait for the run to appear, then watch it:

```bash
gh run list --branch develop --limit 3

gh run watch <run-id> --exit-status > /dev/null 2>&1
echo "CI exit: $?"
```

**If CI fails:** analyze the failure:

```bash
gh run view <run-id> --log-failed 2>&1 | tail -40
```

Report the failure to the user. If the fix requires editing `.R` files,
tell the user to fix the code and re-push to `develop` — this skill cannot
do that. After the fix is pushed and CI is re-triggered, resume monitoring.

**If CI passes:** proceed to Step 8.

---

## Step 8: Merge the PR

**Confirmation gate** — ask the user explicitly before merging:

> "CI passed. Ready to merge `develop` → `main` and release vX.Y.Z?
> This will merge PR #N and tag the release."

Wait for confirmation. Do not merge without it.

On confirmation:

```bash
gh pr merge <pr-number> --merge
```

Mark the CI task complete:

```
TaskUpdate (CI task):
  status: completed
  metadata: { status: "passed" }
```

---

## Step 9: Tag on main

```bash
git fetch origin main
git checkout main
git pull
```

Confirm the tag message with the user. Suggested format:

> `Phase N complete: <one-line summary of what this release adds>`

Create and push the tag:

```bash
git tag -a vX.Y.Z -m "<confirmed-tag-message>"
git push origin vX.Y.Z
```

Report the tag URL:

```
https://github.com/<owner>/surveycore/releases/tag/vX.Y.Z
```

Tell the user: go to that URL to create a GitHub Release with the NEWS.md
section as the release body (optional but recommended).

---

## Step 10: Post-release Dev Bump

Switch back to `develop` and bump the version:

```bash
git checkout develop
git pull
```

Edit `DESCRIPTION`: change `Version: X.Y.Z` to `Version: X.Y.Z.9000`.

Commit:

```bash
git add DESCRIPTION
git commit -m "$(cat <<'EOF'
chore(post-release): bump version to X.Y.Z.9000

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"

git push origin develop
```

---

## Step 11: Done

Mark the release task complete:

```
TaskUpdate (release task):
  status: completed
```

Report:

> "Release vX.Y.Z complete.
>
> - PR #N merged to `main`
> - Tag `vX.Y.Z` pushed
> - `develop` bumped to `X.Y.Z.9000`
>
> Consider creating a GitHub Release at: https://github.com/<owner>/surveycore/releases/tag/vX.Y.Z"

