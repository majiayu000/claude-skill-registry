---
name: esper:yolo
description: Implement all pending plans for the current phase automatically — commits at milestones, opens the phase PR when done. No stopping between plans.
---

You are running YOLO mode: automated sequential implementation of every pending plan in the current phase.

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Run `esperkit config get current_phase` to get the current phase.

Run `esperkit plan list --dir active --format json` to check for active plans. If the JSON contains any entries:
- Read the plan's `id`, `title`, `phase`, and `branch` from the JSON
- If `phase:` does not match `current_phase`: tell the user the active plan belongs to a different phase. Ask them to ship or suspend it first, then stop.
- If `phase:` matches: ask (using `AskUserQuestion`): "There is an active plan: [title]. Include it as the first plan in this YOLO run, or leave it alone and only run pending plans?"
  - **Include**: add it to the front of the queue (do not move — it is already active)
  - **Leave it**: do not include the active plan; process only pending plans

## Step 2: Load the phase queue

Run `esperkit plan list --dir pending --phase <current_phase> --format json` to get all pending plans for the current phase (already sorted by priority then id).

If the queue is empty (and no active plan was included from Step 1): print "No pending plans for phase [current_phase]." and suggest `/esper:plan` to add one. Stop.

Display the ordered queue:
```
YOLO queue for [current_phase]:
  1. #<id> — <title> (p<priority>)
  2. #<id> — <title> (p<priority>)
  ...
```

## Step 3: Confirm

Use `AskUserQuestion` to confirm: "YOLO will implement [N] plan(s) automatically — committing at milestones, no pauses between plans. Open the phase PR when all are done if the phase is complete. Proceed?"

If declined: stop gracefully.

## Step 4: Implement each plan (loop)

Repeat the following for each plan in the queue, in order.

Print a header at the start of each plan: `--- Plan #<id>: <title> ---`

### 4a. Branch

Read `branch:` from the plan frontmatter.

```bash
git checkout <branch>
```

If the branch does not exist, create it:
```bash
git checkout -b <branch>
```

If checkout fails for any other reason: stop the entire YOLO run and report the error. Do not continue to the next plan.

### 4b. Activate

If this plan came from `pending/` (not the pre-existing active plan from Step 1):
- Run `esperkit plan activate <filename>` to move it from `pending/` to `active/` and set `status: active`.

If the plan was already active (the one included from Step 1): skip the activation.

### 4c. Read context

Read:
- The active plan file (full content)
- `.esper/CONSTITUTION.md`
- `.esper/phases/<current_phase>.md`

### 4d. Generate todo list and implement with milestone commits

Before writing any code for this plan, use `TodoWrite` to generate a checklist of implementation steps from the plan's `## Approach` section. Convert each approach step into a concrete, actionable todo item. Do NOT enter plan mode (no EnterPlanMode/ExitPlanMode) — this is YOLO, no pauses.

Follow the plan's **Approach** section step by step.

Rules during implementation:
- Read each file before modifying it
- Follow existing code patterns
- Do not add features beyond what the plan describes
- Keep the plan file as a living document — update `## Approach` or `## Files to change` if something unexpected is found

**Milestone commits** — after each todo item is completed, commit immediately **without pausing for user approval**. This is YOLO mode:

```bash
git add <specific files changed in this milestone>
git commit -m "$(cat <<'EOF'
feat: <what was just implemented>

plan <id> — <title> (milestone)
EOF
)"
```

Stage only files related to the current plan's changes. Do not use `git add -A` or `git add .`.

If something unexpected is discovered that requires a significant change in approach (a missing dependency, a conflicting pattern):
- Update the plan file to reflect the revised approach
- Continue — do NOT stop to ask the user (YOLO mode)
- Document the deviation in the `## Progress` section

### 4e. Verify

After implementation is complete for this plan:

Run the verification steps from the plan's **Verification** section.

Also run `esperkit config get commands` to get the commands object. For each of `test`, `lint`, and `typecheck`:
- Skip it if the value is an empty string or missing
- Run it if non-empty and capture the exit code

If any verification fails: **STOP the entire YOLO run**. Report clearly:
- Which plan failed
- Which command failed and what the output was
- What to do next (fix the issue, then run `/esper:continue` or `/esper:finish` to complete)

Do NOT proceed to the next plan if verification fails. Leave the current plan in `active/`.

### 4f. Update Progress

Add or update the `## Progress` section in the active plan file:

```markdown
## Progress
- Implemented [what was done, milestone by milestone]
- Modified: [list of files changed]
- Verification: [passed / failed with details]
```

### 4g. Archive

Run `esperkit plan finish <filename>` to move the plan from `active/` to `done/` and set `status: done` with `shipped_at`.

Commit the archive:
```bash
git add .esper/plans/done/<filename>
git add .esper/plans/active/<filename>   # stages the deletion
git commit -m "chore: archive plan <id> — <title>"
```

### 4g.5 Update phase file with shipped plan summary

Append a compact one-liner to the current phase file so future agents can read what was shipped without opening individual archived plan files.

1. From the archived plan file (now in `done/`), extract:
   - `id` and `title` from frontmatter
   - **First sentence** of the `## Approach` section (up to the first `.` or newline). If absent, skip.
   - **Filenames** from `## Files to change` (comma-separated bare filenames). If absent, skip.
2. Compose the one-liner:
   - With approach and files: `- Plan <id> — <title>: <first sentence>. Files: <filenames>`
   - With approach only: `- Plan <id> — <title>: <first sentence>.`
   - With neither: `- Plan <id> — <title>`
3. Read `.esper/phases/<current_phase>.md`:
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

### 4h. Continue

Move to the next plan in the queue. Repeat from 4a.

---

## Step 5: Push

After all plans in the queue are archived:

```bash
git push -u origin <branch>
```

If push fails (no remote, auth issue, etc.): report the error clearly and stop. Do not proceed to Step 6.

## Step 6: Phase check and PR

Run `esperkit plan list --dir pending --phase <current_phase> --format json`, `esperkit plan list --dir active --phase <current_phase> --format json`, and `esperkit plan list --dir done --phase <current_phase> --format json` to check plan status.

**If any plans remain in `pending/` or `active/`**: print how many remain and their titles. Skip PR creation — print: "Phase [N] not yet complete — [M] plan(s) remaining. Run `/esper:yolo` again or `/esper:apply` to continue."

**If all phase plans are in `done/`**: the phase is complete. Open ONE PR summarizing the entire phase:

Collect all plans with `type: "feature"` for the phase (fix-type plans already have their own PRs).

Read `.esper/phases/<current_phase>.md` for the phase title and acceptance criteria.

```bash
gh pr create \
  --title "Phase <N>: <phase title>" \
  --base main \
  --body "$(cat <<'EOF'
## Phase <N> — <phase title>

<phase goal, 1-2 sentences from the phase file>

## Shipped plans
- Plan <id> — <title>: <one-line approach summary>
...

## Acceptance criteria
<paste acceptance criteria checklist from phase file>

<if backlog_mode is "github" and the phase file has gh_issue set:>
Closes #<phase_gh_issue>
EOF
)"
```

Print the PR URL.

After the PR is opened, update each feature plan's `pr:` field in `done/` with the PR URL by running `esperkit plan set <filename> pr <PR URL>` for each. Then commit and push:
```bash
git add .esper/plans/done/
git commit -m "chore: record PR link for phase plans"
git push
```

## Step 7: Done

Print a summary:
- Plans shipped: N
- Phase PR: <URL> (or "not opened — phase not yet complete")

If the phase is complete, print: "Ready to plan the next phase? Run `/esper:phase` to define Phase <N+1>. Or use `/esper:plan` to add feature items and `/esper:fix` to log bugs."

Otherwise, suggest: "Run `/esper:yolo` again to continue with remaining plans, or `/esper:apply` to pick them up one at a time."
