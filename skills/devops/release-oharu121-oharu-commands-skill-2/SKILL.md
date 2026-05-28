---
name: release
description: Create a GitHub issue, commit, tag, and push a release. Detects repo type and runs mode-specific validation checks with user confirmation at every step.
user-invocable: true
---

# Release Skill

Orchestrate a full release: repo detection, validation, GitHub issue, commit, tag, push.

**IMPORTANT:** Every interaction with the user MUST go through `AskUserQuestion`. Never
prompt with plain text and wait for a reply — always use the tool.

## Path Variables

- `SKILLS_DIR` = `.claude/skills/release`
- `CONFIG_FILE` = `.claude/skills/release/config.json`

---

## Config File

Read `CONFIG_FILE` at startup if it exists:

```bash
cat .claude/skills/release/config.json 2>/dev/null
```

**Schema:**

```json
{
  "language": "en",
  "repo_mode": "skills-gems",
  "preflight_confirm": false
}
```

| Field | Effect when set |
|-------|----------------|
| `language` | Skip Step 1.5 — use this language directly |
| `repo_mode` | Skip detection — use this mode directly; validation still runs |
| `preflight_confirm: false` | Skip the confirmation gate — validation runs silently without asking "Proceed?" |

All fields are optional. Missing fields fall back to the interactive flow.

---

## Reusable Patterns

### Safe GitHub Body Write

When creating a GitHub issue or release with markdown body content, **never** pass the body
inline via `--body` with shell quoting — backticks, tables, and special characters will break.

Instead:

1. Write the markdown content to `.release-tmp/<filename>.md` using the Write tool
2. Pass `--body-file .release-tmp/<filename>.md` to `gh issue create` or `gh release create`
3. After creation, verify the body is not empty:

```bash
# For issues:
gh issue view <number> --json body --jq '.body | length'
# For releases:
gh release view v<version> --json body --jq '.body | length'
```

If the length is 0, stop the flow and report the error.

### Resume State

On startup (before Phase 0), check for an existing state file:

```bash
cat .release-tmp/state.json 2>/dev/null
```

**State schema:**

```json
{
  "schema_version": 1,
  "phase_completed": 2,
  "issue_number": 42,
  "issue_url": "https://github.com/...",
  "version": "v2.1.0",
  "title": "...",
  "mode": "skills-gems",
  "language": "en"
}
```

**If state file exists**, use AskUserQuestion:
- "Found release state from a previous run (phase \<N\> completed, issue #\<N\>). Resume?"
- Options: "Yes, resume from Phase \<N+1\>", "Start fresh"

If "Start fresh" is selected, use a follow-up AskUserQuestion:
- "Close the orphaned issue #\<N\> from the previous run?"
- Options: "Yes, close it", "No, leave it open"

Then delete `.release-tmp/state.json` and proceed from Phase 0.

**Save state** at the end of Phase 1 and Phase 2:

```bash
mkdir -p .release-tmp
# Write state.json via the Write tool with current progress
```

---

## Phase 0: Repo Detection

**If `repo_mode` is set in config:** skip detection, use the configured mode. State: "Using configured mode: `<mode>`."

**Otherwise**, run detection:

```bash
ls package.json pyproject.toml uv.lock skills/ 2>/dev/null
git status --short
```

Classify into one or more modes:

| Signal detected | Mode |
|-----------------|------|
| `skills/` directory exists AND changed files are under `skills/` | **skills-gems** |
| `package.json` exists | **npm** |
| `pyproject.toml` or `uv.lock` exists | **python** |
| Two or more of the above | **monorepo** |
| None of the above | **generic** |

**If `preflight_confirm` is `false` in config:** skip the confirmation gate, announce mode in plain text and proceed directly to Phase 1.

**Otherwise**, use AskUserQuestion to confirm:

> "Detected: **\<mode\>**. Validation will run: \<summary from pattern file\>. Proceed?"

Options:
- "Yes, proceed" (Recommended)
- "Skip validation"
- "Override mode" → follow-up AskUserQuestion: skills-gems / npm / python / monorepo / generic

---

## Phase 1: Validation

Read and follow `SKILLS_DIR/patterns/<mode>.md`.

Validation always runs for the configured/detected mode — `preflight_confirm: false` only
skips the confirmation gate, not the validation itself.

If validation passes, continue to Phase 2.
If validation fails, stop — do not continue until resolved.

---

## Phase 2: Issue Creation

### Step 1: Gather Context

From the session, identify:
- What feature/fix was implemented
- Which files were modified
- What the key changes were
- Any breaking changes

### Step 1.5: Ask for Language

Use AskUserQuestion:
- "What language should the issue, plan, and release notes be written in?"
- Options: "English", "Japanese (日本語)", "Other" (free text for any other language)

**Store the selected language.** Apply it to all generated content: plan file, issue title,
issue body, acceptance criteria, and release notes. Commit messages always stay in English
regardless of this setting (git convention).

### Step 2: Ask for Title

Use AskUserQuestion:
- 3 suggested titles (concise, action-oriented)
- "Other" option for free input

### Step 3: Ask for Labels

Use AskUserQuestion with multiSelect=true:
- Options: enhancement, bug, documentation, refactor
- "Other" for custom labels (comma-separated)

### Step 4: Ask for Version

```bash
git describe --tags --abbrev=0 2>/dev/null || echo "none"
```

Treat missing tags as v0.0.0. Use AskUserQuestion:
- patch: v{x}.{y}.{z+1}
- minor: v{x}.{y+1}.0
- major: v{x+1}.0.0
- Skip (no tag or release)

Always prefix with "v". **Store the selected version** for later steps.

### Step 5: Create Plan File

Read `SKILLS_DIR/templates/plan.md` for the template and rules.

Create `.plans/<slugified-title>.md` filled with real content from the session.
Write all narrative content (Context, Approach, Changes, Guard Rails, Verification)
in the language selected in Step 1.5. Section headings may stay in English for
template consistency, but all prose must be in the selected language.

### Step 6: Create GitHub Issue

#### 6a: Handle Milestone (if version selected)

```bash
gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.title == "<version>") | .title'
```

If missing:

```bash
gh api repos/{owner}/{repo}/milestones -f title="<version>" -f state="open"
```

#### 6b: Create the Issue

Read `SKILLS_DIR/templates/issue-body.md` for the body format.

Use the **Safe GitHub Body Write** pattern:

1. Write the issue body to `.release-tmp/issue-body.md` using the Write tool
2. Create the issue with `--body-file`:

```bash
mkdir -p .release-tmp
gh issue create \
  --title "<title>" \
  --label "<labels>" \
  --assignee "@me" \
  --milestone "<version>" \
  --body-file .release-tmp/issue-body.md
```

3. Verify the body is not empty:

```bash
gh issue view <number> --json body --jq '.body | length'
```

Omit `--milestone` if version was skipped.

### Step 7: Generate Commit Message

```
feat(<scope>): <description> (#<issue-number>)
```

Use `fix()` for bugs, `docs()` for documentation, `refactor()` for refactoring.

Output: `Issue created: <url> — proceeding with release automation...`

---

## Phase 3: Release Automation

### Step 8: Check Remote Status

```bash
git fetch
git rev-list --count HEAD..@{u}
```

If remote has new commits, use AskUserQuestion:
- "Remote has new commits. Pull with rebase before continuing?"
- Options: "Yes, pull --rebase", "No, continue anyway", "Cancel"

Pull: `git pull --rebase` — stop on merge conflicts.

### Step 8.5: Check README and CHANGELOG

Check whether `README.md` and `CHANGELOG.md` need updating based on the changes in this release:

**README.md — check for:**
- New skills or commands not yet listed in their respective tables
- Removed or renamed skills/commands still listed
- Installation instructions that reference outdated paths or file names

**CHANGELOG.md — check for:**
- Missing entry for the current version being released
- Entries for versions released since the last CHANGELOG update

If updates are needed, make them now before committing — so docs land in the same commit as the code. If README and CHANGELOG are already accurate, state so and continue.

### Step 9: Show Changes & Commit

```bash
git status --short
```

Use AskUserQuestion:
- "Commit these changes?" — show proposed commit message
- Options: "Yes, use this message", "No, use custom message", "Cancel"

If custom: use AskUserQuestion "Other" for free input.

```bash
git add <specific-files>
git commit -m "<message>"
```

**Important:** Do not use `git add .` — explicitly list the files that were changed as part
of this release to prevent accidentally staging unrelated files.

### Step 10: Tag Version

Skip if version was skipped. Otherwise:

```bash
git tag v<new-version>
```

### Step 11: Push to Remote

Use AskUserQuestion:
- "Push commits and tags to remote?"
- Options: "Yes, push now", "No, I'll push manually", "Cancel"

```bash
git push && git push --tags
```

On failure: show manual command.

### Step 12: Create GitHub Release

Skip if version was skipped.

Read `SKILLS_DIR/templates/release-notes.md` for the release notes format.

Use the **Safe GitHub Body Write** pattern:

1. Write release notes to `.release-tmp/release-notes.md` using the Write tool
2. Create the release with `--notes-file`:

```bash
gh release create v<version> \
  --title "<version> - <plan-title>" \
  --notes-file .release-tmp/release-notes.md
```

3. Verify the body is not empty:

```bash
gh release view v<version> --json body --jq '.body | length'
```

Write release notes in the language selected in Step 1.5.

### Step 13: Close Issue & Output

```bash
gh issue close <issue-number> --comment "Released in v<version>"
# or if skipped:
gh issue close <issue-number> --comment "Shipped in <commit-sha>"
```

**If config did not exist at startup**, use AskUserQuestion:
- "Save these preferences for future runs? (skips detection and language prompts)"
- Options: "Yes, save to `.claude/skills/release/config.json`", "No, ask me each time"

If yes, write `CONFIG_FILE` with the language and mode used this run, and `preflight_confirm: false`.

---

**If version was tagged**, output as plain markdown prose (not a fenced code block).
Use markdown link syntax so URLs are clickable in the IDE:

> Release complete!
>
> - **Issue:** `[#N](full-issue-url)`
> - **Version:** old → new
> - **Tag:** `vX.Y.Z`
> - **Release:** `[vX.Y.Z](full-release-url)`

**If version was skipped**, output as plain markdown prose:

> Changes committed and pushed!
>
> - **Issue:** `[#N](full-issue-url)`
> - **Commit:** `commit-message`
>
> No version tag or GitHub release (skipped).

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Remote fetch fails | Warn and continue |
| Pull conflicts | Stop, instruct to resolve manually |
| Validation fails | Stop, AskUserQuestion: skip or fix |
| Commit fails | Stop (likely pre-commit hook) |
| Tag already exists | Stop, AskUserQuestion with next version suggestion |
| Push fails | Warn, show manual command |
| gh not installed | Warn, provide manual release URL |
