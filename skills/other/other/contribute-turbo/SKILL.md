---
name: contribute-turbo
description: "Submit turbo skill improvements back to the upstream repo. Adapts to repo mode: fork mode creates a PR, source mode pushes directly. Use when the user asks to \"contribute to turbo\", \"submit turbo changes\", \"PR my skill changes\", \"contribute back\", or \"upstream my changes\"."
---

# Contribute Turbo

Submit staged turbo skill improvements from `~/.turbo/repo/` back to the upstream repo. The workflow adapts based on `repoMode` in `~/.turbo/config.json`.

## Step 1: Verify Contributor Status

Read `~/.turbo/config.json` and check `repoMode`:

- `"fork"` or `"source"` — proceed
- `"clone"` — tell the user that contributions require a fork. Offer to help convert their clone to a fork (add their fork as origin, rename current origin to upstream). Stop.
- Missing config or repo — tell the user to run the Turbo setup first. Stop.

Verify the repo exists and has the expected remotes:

```bash
git -C ~/.turbo/repo remote -v
```

## Step 2: Mirror Installed Skill Changes

Port session corrections from `~/.agents/skills/<name>/` (where edits land first) into `~/.turbo/repo/codex/skills/<name>/` (the basis for the contribution), leaving any persistent local customizations in the installed copy untouched.

Detect drifted skills:

```bash
for skill in ~/.agents/skills/*/; do
  name=$(basename "$skill")
  repo_dir=~/.turbo/repo/codex/skills/"$name"
  [ -d "$repo_dir" ] || continue
  diff -rq "$skill" "$repo_dir" >/dev/null 2>&1 && continue
  echo "$name"
done
```

For each drifted skill, first check whether the repo copy already has unstaged changes for it (`git -C ~/.turbo/repo status --porcelain codex/skills/<name>/`). If it does, use `request_user_input` to ask the user how to proceed before mirroring — those changes will conflate with mirrored corrections in Step 3 if not resolved.

Then read both versions of every changed file and classify each hunk:

- **Correction** — a session edit meant to improve the skill upstream. For modified files and new files, mirror the change into the repo copy with `apply_patch`. For files deleted from the installed copy, remove the repo copy with `rm`.
- **Customization** — a persistent local addition that does not belong upstream (extra workflow steps, personal paths, machine-specific notes, internal references). Leave it in the installed copy; do not propagate.
- **Ambiguous** — use `request_user_input` to confirm classification before applying.

## Step 3: Check Cross-Edition Sync

Before staging, check whether the Codex paths drifted in Step 2 have parallel files in the Claude edition that should be updated alongside them:

- `codex/skills/<name>/` ↔ `claude/skills/<name>/`
- `codex/SKILL-CONVENTIONS.md` ↔ `claude/SKILL-CONVENTIONS.md`
- `codex/ADDITIONS.md` ↔ `claude/ADDITIONS.md`
- `codex/SETUP.md` ↔ `claude/SETUP.md`
- `codex/UPDATE.md` ↔ `claude/UPDATE.md`
- `codex/MIGRATION.md` ↔ `claude/MIGRATION.md`

For each Codex path with pending changes, check whether the Claude sibling exists in `~/.turbo/repo/claude/` and whether the local repo already has matching changes for it (`git -C ~/.turbo/repo status --porcelain claude/<path>`). If a Claude sibling exists but has no matching changes, use `request_user_input`:

> The change to `codex/<path>` touches the Codex edition, but `claude/<path>` exists and has no matching change. Does the Claude sibling need the same update?

Options:

- **Yes, I need to update the Claude sibling** — Stop. The user manually edits `~/.turbo/repo/claude/<path>` (vocabulary differs; only behavioral parity is required) and re-runs this skill.
- **No, this is Codex-specific** — Continue.

If any sibling-update answer is "Yes", stop the workflow. Nothing has been staged yet, so there is no state to clean up before re-running.

## Step 4: Review Pending Changes

Check what changes exist in the local repo:

```bash
git -C ~/.turbo/repo diff --name-only
git -C ~/.turbo/repo diff --cached --name-only
```

If there are unstaged changes to skill files, stage the specific skill directories that changed (both editions, when sibling updates landed in Step 3):

```bash
git -C ~/.turbo/repo add codex/skills/<name>/
git -C ~/.turbo/repo add claude/skills/<name>/   # if a sibling was updated
```

If there are no changes at all, tell the user there is nothing to contribute and stop.

Present the changes in a summary table:

```
| # | Skill | Change Summary |
|---|-------|----------------|
| 1 | $evaluate-findings | Added handling for security-default findings |
| 2 | $self-improve | Clarified routing for trusted reviewer feedback |
```

Use `request_user_input` to confirm which changes to include. If the user deselects some, unstage those files.

## Step 5: Validate Skill Quality

Read `~/.turbo/repo/codex/SKILL-CONVENTIONS.md` for the turbo project's skill conventions. These conventions supplement `$create-skill`'s general best practices with turbo-specific patterns.

For each confirmed skill, if `$create-skill` has not been invoked for it in this session, run `$create-skill` to review and refine the skill. Any improvements from the review become part of the contribution.

## Step 6: Craft Contribution Context

For each change, construct a "why" explanation. The goal: the turbo maintainer should understand what happened and why the existing instructions were insufficient, without learning anything about the contributor's project.

Use this template:

> During [general workflow description], the skill's instructions [what was missing or wrong]. This caused [what happened]. The change [what it does] so that [benefit].

**Example:**

> During a code review session, the evaluate-findings skill encountered a finding with `security-default` severity. The existing instructions only handled `critical`, `high`, `medium`, and `low` severities, causing the finding to be silently dropped. The change adds `security-default` to the severity handling table so these findings are properly triaged.

### Privacy Filter

Before finalizing, verify each "why" description contains none of the following:

- Project or repo names
- File paths from the user's project
- Company or product names
- API keys, URLs, or credentials
- Business logic or domain-specific terminology that identifies the project
- User names beyond the contributor's GitHub handle

Output the drafted context as text. Then use `request_user_input` for approval. The user must approve the contribution message before proceeding.

## Step 7: Commit Rules

Run `$commit-rules` to load commit message rules and technical constraints.

## Step 8: Create Branch and Commit

When multiple skills were changed, batch related changes into a single branch and commit. Create separate branches only when changes are independent and unrelated.

### Fork mode

Create a feature branch:

```bash
git -C ~/.turbo/repo checkout -b improve/<skill-name>-<short-desc>
```

Commit with a message matching the turbo repo style (check `git -C ~/.turbo/repo log -n 10 --oneline`). Incorporate the "why" context in the commit message.

### Source mode

Stay on main. Commit directly with the same message style.

## Step 9: Push

### Fork mode

Run `$github-voice` to load writing style rules.

Push and create a PR:

```bash
git -C ~/.turbo/repo push -u origin improve/<skill-name>-<short-desc>
```

Create the PR against the upstream repo:

```bash
gh pr create --repo tobihagemann/turbo --head <user>:improve/<skill-name>-<short-desc> --title "..." --body "..."
```

PR body format:

```markdown
## Summary
- [1-3 bullet points]

## Context
[The crafted "why" explanation from Step 6]
```

Return to main after creating the PR:

```bash
git -C ~/.turbo/repo checkout main
```

Report the PR URL.

### Source mode

Pull and rebase before pushing to incorporate any upstream changes:

```bash
git -C ~/.turbo/repo pull --rebase origin main
```

If the rebase pulled in new commits, run `$update-turbo` to apply upstream changes (skill updates, migrations, config changes) to the local installation before pushing.

Then push:

```bash
git -C ~/.turbo/repo push origin main
```

Report the pushed commit hash.

## Step 10: Update Config

In source mode, update `~/.turbo/config.json` so the next `$update-turbo` does not re-surface the just-pushed changes:

1. Read `~/.turbo/config.json`
2. Set `codex.lastUpdateHead` (creating the `codex` object or key if missing) to the current HEAD: `git -C ~/.turbo/repo rev-parse HEAD`
3. Write the updated config back

Report that the contribution is complete.

Skip this step in fork mode (the upstream has not changed until the PR is merged).

Then update or check the active plan and proceed to any remaining task.
