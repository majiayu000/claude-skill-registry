---
name: sk
description: "How to use the repo-scoped sk CLI to manage Claude Skills in this codebase."
---

# Using the `sk` CLI

`sk` is the repo-scoped Skills manager that installs, audits, and syncs Claude Skills listed in `skills.lock.json`. Treat it like Cargo for skills: installs live under `./skills`, while the cache stays in `~/.cache/sk/repos`.

## When to reach for this skill
- You need to install or upgrade a skill from the canonical skills repo (`https://github.com/lambdamechanic/skills`).
- You want to verify the working tree is clean (`sk doctor --status`, `sk doctor --summary`).
- You are preparing to sync edits back to the upstream skills repository (`sk sync-back <install>`).

## Core workflow
1. **Refresh the cache** (optional but fast):
   ```bash
   target/debug/sk cache refresh
   ```
2. **Install or upgrade a skill** (alias keeps folder names stable):
   ```bash
   target/debug/sk install https://github.com/lambdamechanic/skills testing-patterns --alias testing
   target/debug/sk upgrade testing
   ```
3. **Audit local installs** before landing work:
   ```bash
   target/debug/sk doctor --status --json   # detect dirty trees vs lockfile
   target/debug/sk doctor --summary --json  # shows pending upgrades or cache drift
   ```
4. **Sync edits upstream** after modifying a skill under `./skills/<name>`:
   ```bash
   target/debug/sk sync-back <name> --message "Describe the change"
   ```
   Once `sk config set default_repo <repo>` is configured, `sk sync-back <name>` automatically targets that repo, uses `<name>` for the skill-path, and generates `sk/sync/<name>/<timestamp>` branches so the quickstart `-m` flag is the only required argument. Supply `--repo` / `--skill-path` only when you need to override the defaults.

   This creates a temp branch in the cached repo, copies your edited skill directory, commits, and pushes. On success `sk` runs `gh` for you: it auto-opens a PR, enables auto-merge when GitHub reports the branch is clean, and prints the PR URL (or a conflict warning) so you can follow up if automation gets blocked. If the GitHub CLI is missing or the repo isn’t reachable via GitHub, you’ll see a warning plus manual PR instructions and can run `gh pr create` yourself once available.

   **PR automation tips**

   - Run `gh auth status` once per machine to ensure the GitHub CLI is logged in; `sk` will reuse your credentials.
   - Missing `rsync` prints a warning and falls back to a recursive copy before committing; install `rsync` to keep large skills fast.
   - After the push, watch the terminal output:
     - `Opened PR …` (or `Reusing PR …`) links to the branch that was just published.
     - `Auto-merge armed…` means GitHub will land it once checks pass; otherwise you’ll see `Auto-merge blocked…` with a link to fix conflicts manually.
     - `Auto-merge skipped…` appears when checks can’t be armed (e.g., required approvals disabled); click through and finish by hand.
   - When `gh` is missing or unauthenticated you’ll see “Skipping PR automation …”; install/auth and rerun `sk sync-back` to finish the upload.
   - Automation currently uses GitHub’s standard `--merge` strategy; if your repo enforces `--squash`/`--rebase`, turn off auto-merge in the UI and land it manually after review.
   - If your PR output says `enablePullRequestAutoMerge`, run `gh repo edit <owner>/<repo> --enable-auto-merge` (or visit the repo’s Settings → General page) once to flip the toggle.
5. **Publish a brand-new skill** that doesn’t exist upstream yet:
   ```bash
   target/debug/sk sync-back <name> \
     --repo https://github.com/lambdamechanic/skills \
     --skill-path <subdir> \
     --message "Add <name> skill"
   ```
   Provide `--repo` / `--skill-path` only if you need something other than the configured defaults. `sk` clones that repo, branches from the default tip (or your custom `--branch`), copies your local folder, pushes, and rewrites `skills.lock.json` with the exact commit SHA/digest so status checks stay clean. You will always see the temporary branch name in the CLI output, e.g. `Pushed branch 'sk/sync/<name>/<timestamp>' …`, even though that branch is meant to be merged and deleted once the upstream PR lands.

### Example: publishing `sk`

```bash
cd /path/to/sk-decisions
target/debug/sk sync-back sk \
  --repo https://github.com/lambdamechanic/skills \
  --skill-path sk \
  --branch sk/add-sk-skill-doc \
  --message "Add sk skill doc"
```

What happens:
- `sk` prints both the temporary branch name and the upstream repo it pushed to, so you can follow up on GitHub immediately.
- The branch only needs to live long enough for you (or automation) to open a PR; the lockfile entry pins the pushed commit hash, so it’s safe to delete the branch once merged.
- `skills.lock.json` gains a new entry for `sk` with the push timestamp, digest, and commit ID; subsequent `sk doctor --status` runs stay green because the on-disk tree matches that digest.

## Guardrails
- Always run `bd update` / `bd close` so `.beads/issues.jsonl` matches any skill changes.
- Never edit `skills.lock.json` by hand. Let `sk install`, `sk upgrade`, or `sk remove` update it; commit the lockfile alongside the skill changes.
- If `sk doctor --status` reports `dirty`, fix the local tree before running `sk upgrade` or `sk sync-back` to avoid partial syncs.
- `sk upgrade --all` skips skills with local edits and prints reminders to `sk sync-back <name>`; treat that as a temporary state and clean them up promptly so future upgrades stay automatic.
- When creating a new skill, always specify the upstream repo/path so `sk` can register it and refresh the lockfile automatically.
- Use `sk precommit` (once implemented) to block local-only sources such as `file://` entries.

## Debug tips
- `target/debug/sk doctor --apply` rebuilds missing installs or cache entries.
- `target/debug/sk where <name>` prints the absolute path of an installed skill and its cached repo clone.
- Set `SK_TRACE=1` to surface extra logging when diagnosing cache fetches or rsync failures.
