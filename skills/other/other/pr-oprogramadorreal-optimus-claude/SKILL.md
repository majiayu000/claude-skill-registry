---
description: Creates or updates a pull request (GitHub) or merge request (GitLab) for the current branch using the Conventional PR format — structured summary, changes, rationale, and test plan. Use when a branch is ready for review, or to update an existing PR/MR description.
disable-model-invocation: true
---

# Pull Request / Merge Request

Create or update a PR (GitHub) or MR (GitLab) for the current branch using the Conventional PR format. Detects the hosting platform, checks for an existing PR/MR, and either creates a new one or offers to update the existing one. New PRs target the repository's default branch; updates to existing PRs use the PR's current target branch. PRs/MRs are created as ready to merge (not draft).

## Step 1: Pre-flight

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, run the multi-repo selection procedure below. Otherwise, skip to **Verify git state**.

### Multi-repo selection

1. For each child repo, check:
   - Current branch: `git -C <repo-path> rev-parse --abbrev-ref HEAD`
   - Default branch: use the algorithm from `$CLAUDE_PLUGIN_ROOT/skills/pr/references/default-branch-detection.md` (run inside the repo)
   - Whether it has commits ahead of default: `git -C <repo-path> log --oneline origin/<default-branch>..HEAD 2>/dev/null | head -1`
2. If default branch detection fails for a repo, warn the user (e.g., "Could not detect default branch for `<repo>` — skipping") and exclude it from the candidates list
3. Filter to repos that are on a non-default branch AND have commits ahead of the default branch
4. If **no repos** have changes → inform the user: "No repositories in this workspace have branches with changes ready for a PR." Stop.
5. If **one repo** has changes → inform the user which repo was detected and proceed to run Steps 2–8 inside that repo's directory
6. If **multiple repos** have changes → present the list and use `AskUserQuestion` — header "Multi-Repo PRs", question "Multiple repositories have changes ready for PRs:". Options:
   - **All** — "Create PRs for all repos with changes (one at a time)"
   - Each individual repo name — "Create PR for `<repo>` only"
7. If the user selects a specific repo, proceed to run Steps 2–8 inside that repo's directory
8. If the user selects **All**, process each repo with changes through Steps 2–8 sequentially. For each repo: run all commands inside that repo's directory, complete Steps 2–7 fully (including the per-repo report in Step 7), then **continue to the next repo**. After the last repo, show the combined summary from Step 8

### Verify git state

1. Confirm the current directory is inside a git repository: `git rev-parse --is-inside-work-tree`. If not → inform the user and stop.
2. Get the current branch: `git rev-parse --abbrev-ref HEAD`.
3. Check that the current branch is not the default branch. Detect the default branch using the algorithm in `$CLAUDE_PLUGIN_ROOT/skills/pr/references/default-branch-detection.md`. If no default branch can be determined → inform the user: "Could not detect the default branch. Ensure `origin` is configured and has been fetched." Stop. If on the default branch → inform the user: "You're on the default branch (`<branch>`). Switch to a feature branch first." Stop.

## Step 2: Platform Detection

When processing multiple repos, show a heading (e.g., `## repo-name`) before starting this step for each repo.

Read `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md` and use the **Platform Detection Algorithm** section. If platform is unknown → inform the user that the hosting platform could not be determined and stop.

## Step 3: CLI Availability

Read `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md` and use the **CLI Verification** section to check availability and authentication. If the CLI is not installed, use the **CLI Installation** section — offer to install via `AskUserQuestion` (header "Install CLI", question "The [GitHub CLI (`gh`) / GitLab CLI (`glab`)] is required but not installed. Install it now?"):
- **Install** — "Install automatically (requires [package manager])"
- **Cancel** — "I'll install it manually"

If the user chooses **Cancel** → provide manual installation instructions and stop.
If installation fails → provide manual installation instructions and stop.
If installed but auth fails → inform the user: "CLI installed. Run `[gh/glab] auth login` to authenticate, then re-run `/optimus:pr`." Stop.

## Step 4: Branch and Existing PR/MR Check

### Push branch if needed

Check if the branch has been pushed: `git ls-remote --heads origin <branch> 2>/dev/null`

If the branch is not on the remote:
1. Check for commits: `git log --oneline HEAD --not --remotes 2>/dev/null | head -1`. If no commits → inform the user: "No commits on this branch yet. Commit your changes first." Stop.
2. Push: `git push -u origin <branch>`

If the branch is on the remote but has unpushed commits (`git log origin/<branch>..HEAD --oneline`), push them: `git push origin <branch>`

### Check for existing PR/MR

- **GitHub:** `gh pr view --json number,state,title,body,url,baseRefName 2>/dev/null`
  - If a PR exists and is **open** → save the `baseRefName` as the PR's **target branch**, then go to Step 6 (Update Flow)
  - If a PR exists but is **closed/merged** → treat as no PR (create a new one)
  - If no PR exists → go to Step 5 (Create Flow)

- **GitLab:** `glab mr view --output json 2>/dev/null`
  - If an MR exists and is **opened** → save the `target_branch` from the JSON as the MR's **target branch**, then go to Step 6 (Update Flow)
  - If an MR exists but is **closed/merged** → treat as no MR
  - If no MR exists → go to Step 5 (Create Flow)

## Step 5: Create Flow

### Detect default branch

- **GitHub:** `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`
- **GitLab:** use the default branch detected in Step 1, or `git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`

### Gather change data

Collect information about the changes on the branch:

```bash
# Commit list
git log --oneline origin/<default-branch>..HEAD

# Changed files summary
git diff --stat origin/<default-branch>..HEAD

# Full diff for analysis
git diff origin/<default-branch>..HEAD
```

If there are no commits ahead of the default branch → inform the user: "This branch has no changes compared to `<default-branch>`." Stop.

### Generate PR content

Read the Conventional PR template: `$CLAUDE_PLUGIN_ROOT/skills/pr/references/pr-template.md`

Generate a title and body following the template. When filling in the sections:
- Synthesize the **Summary** from commit messages, changed files, and the diff
- Use `git diff --stat` output as a starting point for **Changes**, then describe what each file change accomplishes
- For the **Test plan**, look for: test files in the diff → "Run `<test command>` to verify"; CI configuration → "CI pipeline will run automatically"; manual verification → describe what to check

### Preview and confirm

Present the generated title and body to the user (in a multi-repo workspace, include the repo name in the header):

```
## PR Preview [— repo-name]

**Title:** <title>

---

<body>
```

Use `AskUserQuestion` — header "PR preview", question "Review the PR/MR title and description above. Proceed or adjust?":
- **Create PR** — "Looks good — create the PR/MR"
- **Adjust** — "I want to modify the title or description"

If the user chooses **Adjust**, ask what to change, apply modifications, and preview again.

### Create PR/MR

Write the body to a secure temp file: `TMPFILE=$(mktemp "${TMPDIR:-/tmp}/pr-body-XXXXXX.md")`. Clean up after the creation attempt: `rm -f "$TMPFILE"`.

- **GitHub:** `gh pr create --title "<title>" --body-file "$TMPFILE" --base <default-branch>`
- **GitLab:** `glab mr create --title "<title>" --description "$(cat "$TMPFILE")" --target-branch <default-branch>`

Proceed to Step 7.

## Step 6: Update Flow

### Show current PR/MR

Display the current title and body to the user:

```
## Existing PR/MR

**#<number>:** <title>
**URL:** <url>

---

<current body>
```

### Ask what to update

Use `AskUserQuestion` — header "Update PR", question "A PR/MR already exists for this branch. What would you like to do?":
- **Regenerate title and description** — "Regenerate both using the Conventional PR format based on current branch changes"
- **Regenerate description only** — "Keep the current title, regenerate the description"
- **Cancel** — "Keep the current PR/MR as-is"

If the user chooses **Cancel** → report the existing PR/MR URL and stop.

### Regenerate content

#### Phase 1 — Generate fresh content

Gather change data using the existing PR/MR's **target branch** (saved in Step 4) as the base for diffs — use it in place of `<default-branch>` in the `git log`, `git diff --stat`, and `git diff` commands from Step 5. Generate new content following the Conventional PR template. This is the authoritative content. Do not present yet.

#### Phase 2 — Scan existing content for non-diff information

Review the existing PR/MR title and body (saved from Step 4) for information that **cannot be derived from code changes**. Examples: issue/ticket references (`#45`, `JIRA-123`), deployment instructions, external links, reviewer-directed notes, or follow-up tasks. Discard anything that is outdated, factually wrong based on current diffs, or already covered by the freshly generated content. If useful non-diff information is found:

1. **Standard sections**: Integrate at a natural position within the matching section of the new content (e.g., issue references in Summary, manual verification steps in Test plan).
2. **Non-standard sections**: If the existing body has sections outside the four standard ones (e.g., `## Deployment notes`, `## Related issues`) that contain non-diff information still relevant, preserve them after `## Test plan`.
3. **Title**: Only when regenerating the title — if the existing title contains an issue reference or similar non-diff context, incorporate it into the new title while keeping Conventional Commit format.

#### Phase 3 — Preview

Present the final content for preview. If any non-diff information was carried over from the existing PR/MR, add a brief note above the preview: "Note: some manually-added content from the existing PR/MR was carried over (issue references, deployment notes, etc.)."

Use `AskUserQuestion` — header "Update preview", question "Review the updated PR/MR. Proceed or adjust?":
- **Update** — "Apply changes to the PR/MR"
- **Adjust** — "I want to modify before updating"

### Apply update

Write the body to a secure temp file (same pattern as Step 5). Clean up after the update attempt.

- **GitHub:** `gh pr edit <number> --title "<title>" --body-file "$TMPFILE"`  (or `--body-file` only if keeping the title)
- **GitLab:** `glab mr update <number> --title "<title>" --description "$(cat "$TMPFILE")"`

Proceed to Step 7.

## Step 7: Per-Repo Report

```
## PR/MR [Created / Updated] [— repo-name]

- URL: [PR/MR URL]
- Title: [title]
- Target: [target-branch]
- Status: Ready to merge
```

If processing multiple repos, **continue to the next repo** — go back to Step 2 for the next repo in the list. Do NOT show next-step recommendations or the fresh-conversation tip until all repos are done. After the last repo (or if processing a single repo), proceed to Step 8.

## Step 8: Final Summary

In a multi-repo workspace where multiple repos were processed, show a combined summary across all repos:

```
## All PRs/MRs Created

| Repo | PR/MR | URL |
|------|-------|-----|
| `repo-name` | title | URL |
```

Recommend running `/optimus:verify` to prove the feature works, then `/optimus:code-review` for static quality review before merging.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
