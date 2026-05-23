---
name: esper:finish
description: Complete the active plan — run verification, commit any remaining changes, and archive to done/. Run this when implementation is complete.
---

You are finalizing the active backlog item.

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Run `esperkit plan list --dir active --format json`. If the list is empty, stop: "No active plan to finish. Run `/esper:apply` to start one."

The JSON output includes the frontmatter fields (`id`, `title`, `branch`, `type`, `phase`). Also read the active plan file's full content from `.esper/plans/active/<filename>` for the body sections.

## Step 2: Run verification

Run `esperkit config get commands` to get the commands object as JSON. For each of `test`, `lint`, and `typecheck`:
- Skip it entirely if the value is an empty string or the key is missing
- Run it if non-empty and capture the exit code

If all three commands are empty or missing, print: "No verification commands configured — skipping." Then continue.

If any non-empty command fails, stop and report the failures clearly. Do NOT proceed. Fix the failures before running `/esper:finish` again.

## Step 3: Commit remaining changes

Run `git status --porcelain` to check for uncommitted changes.

**If there are uncommitted changes:**
1. Run `git diff HEAD` to see what changed
2. Stage the files related to this plan (including the plan file itself):
   ```bash
   git add <relevant files>
   ```
3. Draft a commit message:
   ```
   <feat|fix|chore>: <concise description tied to plan title>

   <1-3 sentences on what changed and why>

   plan <id> — <title>
   ```
4. Show the draft to the user and wait for approval (use `AskUserQuestion`)
5. Once approved:
   ```bash
   git commit -m "$(cat <<'EOF'
   <approved message>
   EOF
   )"
   ```

**If the working tree is clean:** Print "Nothing to commit — archiving plan as-is." and continue to Step 4.

## Step 4: Archive the plan

Run `esperkit plan finish <filename>` — this moves the file from `active/` to `done/`, sets `status: done` and `shipped_at: <today's date>` in the frontmatter.

Do NOT add a `pr:` field — that is added by `/esper:ship` when the PR is opened.

Commit the archive:
```bash
git add .esper/plans/done/<filename>
git add .esper/plans/active/<filename>   # stages the deletion
git commit -m "chore: archive plan <id> — <title>"
```

## Step 4.5: Update phase file with shipped plan summary

Append a compact one-liner to the current phase file so future agents can read what was shipped without opening individual archived plan files.

1. Run `esperkit config get current_phase` to get the phase name.
2. From the archived plan file (now in `done/`), extract:
   - `id` and `title` from frontmatter
   - **First sentence** of the `## Approach` section (up to the first `.` or newline). If the section is absent, skip this part.
   - **Filenames** from `## Files to change` (comma-separated bare filenames, e.g. `cli.js, plan.js`). If the section is absent, skip this part.
3. Compose the one-liner:
   - With approach and files: `- Plan <id> — <title>: <first sentence>. Files: <filenames>`
   - With approach only: `- Plan <id> — <title>: <first sentence>.`
   - With neither: `- Plan <id> — <title>`
4. Read `.esper/phases/<current_phase>.md`:
   - If the file is **missing**: print "Warning: phase file not found — skipping Shipped Plans update." and continue.
   - If a `## Shipped Plans` section **exists**: append the one-liner as a new bullet under it.
   - If it **does not exist**: append the following block to the end of the file:
     ```

     ## Shipped Plans
     - Plan <id> — <title>: ...
     ```

Commit the phase file update:
```bash
git add .esper/phases/<current_phase>.md
git commit -m "chore: update <current_phase> Shipped Plans index"
```

## Step 5: Summary

Print: "Plan <id> — <title> finished and archived to `done/`."

**If `type: "feature"`:**
- Run `esperkit plan list --dir pending --phase <phase> --format json` and count the entries
- Print: "Feature plan archived. [N] plan(s) remaining in [current_phase]."
- Next: "Run `/esper:apply` to continue with the next plan. The phase PR opens via `/esper:ship` when all plans are done."

**If `type: "fix"` (or type is missing):**
- Print: "Fix plan archived. Next: run `/esper:ship` to push and open a PR for this fix."
