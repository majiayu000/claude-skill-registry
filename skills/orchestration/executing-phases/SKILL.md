---
name: executing-phases
description: Use this skill when executing all plans in a phase with wave-based parallelization, running phase execution, or completing phase work. Triggers include "execute phase", "run phase", "execute plans", "run the phase", and "phase execution".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
---

<user_command>/kata:execute-phase</user_command>


<objective>
Execute all plans in a phase using wave-based parallel execution.

Orchestrator stays lean: discover plans, analyze dependencies, group into waves, spawn subagents, collect results. Each subagent loads the full execute-plan context and handles its own plan.

Context budget: ~15% orchestrator, 100% fresh per subagent.
</objective>

<execution_context>
@./references/ui-brand.md
@./references/planning-config.md
@./references/phase-execute.md
</execution_context>

<context>
Phase: $ARGUMENTS

**Flags:**
- `--gaps-only` — Execute only gap closure plans (plans with `gap_closure: true` in frontmatter). Use after phase-verify creates fix plans.

@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<process>
0. **Resolve Model Profile**

   Read model profile for agent spawning:
   ```bash
   MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
   ```

   Default to "balanced" if not set.

   **Model lookup table:**

   | Agent              | quality | balanced | budget |
   | ------------------ | ------- | -------- | ------ |
   | kata-executor      | opus    | sonnet   | sonnet |
   | kata-verifier      | sonnet  | sonnet   | haiku  |
   | kata-code-reviewer | opus    | sonnet   | sonnet |
   | kata-*-analyzer    | sonnet  | sonnet   | haiku  |

   *Note: Review agents (kata-code-reviewer, kata-*-analyzer) are spawned by the kata-reviewing-pull-requests skill, which handles its own model selection based on the agents' frontmatter. The table above documents expected model usage for cost planning.*

   Store resolved models for use in Task calls below.

1. **Validate phase exists**
   - Find phase directory matching argument
   - Count PLAN.md files
   - Error if no plans found

1.5. **Create Phase Branch (pr_workflow only)**

   Read pr_workflow config:
   ```bash
   PR_WORKFLOW=$(cat .planning/config.json 2>/dev/null | grep -o '"pr_workflow"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
   ```

   **If PR_WORKFLOW=false:** Skip to step 2.

   **If PR_WORKFLOW=true:**
   1. Get milestone version from ROADMAP.md:
      ```bash
      MILESTONE=$(grep -oE 'v[0-9]+\.[0-9]+(\.[0-9]+)?' .planning/ROADMAP.md | head -1 | tr -d 'v')
      ```
   2. Get phase number and slug from PHASE_DIR:
      ```bash
      PHASE_NUM=$(basename "$PHASE_DIR" | sed -E 's/^([0-9]+)-.*/\1/')
      SLUG=$(basename "$PHASE_DIR" | sed -E 's/^[0-9]+-//')
      ```
   3. Infer branch type from phase goal (feat/fix/docs/refactor/chore, default feat):
      ```bash
      PHASE_GOAL=$(grep -A 5 "Phase ${PHASE_NUM}:" .planning/ROADMAP.md | grep "Goal:" | head -1 || echo "")
      if echo "$PHASE_GOAL" | grep -qi "fix\|bug\|patch"; then
        BRANCH_TYPE="fix"
      elif echo "$PHASE_GOAL" | grep -qi "doc\|readme\|comment"; then
        BRANCH_TYPE="docs"
      elif echo "$PHASE_GOAL" | grep -qi "refactor\|restructure\|reorganize"; then
        BRANCH_TYPE="refactor"
      elif echo "$PHASE_GOAL" | grep -qi "chore\|config\|setup"; then
        BRANCH_TYPE="chore"
      else
        BRANCH_TYPE="feat"
      fi
      ```
   4. Create branch with re-run protection:
      ```bash
      BRANCH="${BRANCH_TYPE}/v${MILESTONE}-${PHASE_NUM}-${SLUG}"
      if git show-ref --verify --quiet refs/heads/"$BRANCH"; then
        git checkout "$BRANCH"
        echo "Branch $BRANCH exists, resuming on it"
      else
        git checkout -b "$BRANCH"
        echo "Created branch $BRANCH"
      fi
      ```

   Store BRANCH variable for use in step 4.5 and step 10.5.

2. **Discover plans**
   - List all *-PLAN.md files in phase directory
   - Check which have *-SUMMARY.md (already complete)
   - If `--gaps-only`: filter to only plans with `gap_closure: true`
   - Build list of incomplete plans

3. **Group by wave**
   - Read `wave` from each plan's frontmatter
   - Group plans by wave number
   - Report wave structure to user

4. **Execute waves**
   For each wave in order:
   - Spawn `kata-executor` for each plan in wave (parallel Task calls)
   - Wait for completion (Task blocks)
   - Verify SUMMARYs created
   - **Update GitHub issue checkboxes (if enabled):**

     Build COMPLETED_PLANS_IN_WAVE from SUMMARY.md files created this wave:
     ```bash
     # Get plan numbers from SUMMARYs that exist after this wave
     COMPLETED_PLANS_IN_WAVE=""
     for summary in ${PHASE_DIR}/*-SUMMARY.md; do
       # Extract plan number from filename (e.g., 04-01-SUMMARY.md -> 01)
       plan_num=$(basename "$summary" | sed -E 's/^[0-9]+-([0-9]+)-SUMMARY\.md$/\1/')
       # Check if this plan was in the current wave (from frontmatter we read earlier)
       if echo "${WAVE_PLANS}" | grep -q "plan-${plan_num}"; then
         COMPLETED_PLANS_IN_WAVE="${COMPLETED_PLANS_IN_WAVE} ${plan_num}"
       fi
     done
     ```

     Check github.enabled and issueMode:
     ```bash
     GITHUB_ENABLED=$(cat .planning/config.json 2>/dev/null | grep -o '"enabled"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
     ISSUE_MODE=$(cat .planning/config.json 2>/dev/null | grep -o '"issueMode"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "never")
     ```

     **If `GITHUB_ENABLED != true` OR `ISSUE_MODE = never`:** Skip GitHub update.

     **Otherwise:**

     1. Find phase issue number:
     ```bash
     VERSION=$(grep -oE 'v[0-9]+\.[0-9]+(\.[0-9]+)?' .planning/ROADMAP.md | head -1 | tr -d 'v')
     ISSUE_NUMBER=$(gh issue list \
       --label "phase" \
       --milestone "v${VERSION}" \
       --json number,title \
       --jq ".[] | select(.title | startswith(\"Phase ${PHASE}:\")) | .number" \
       2>/dev/null)
     ```

     If issue not found: Warn and skip (non-blocking).

     2. Read current issue body:
     ```bash
     ISSUE_BODY=$(gh issue view "$ISSUE_NUMBER" --json body --jq '.body' 2>/dev/null)
     ```

     3. For each completed plan in this wave, update checkbox:
     ```bash
     for plan_num in ${COMPLETED_PLANS_IN_WAVE}; do
       # Format: Plan 01, Plan 02, etc.
       PLAN_ID="Plan $(printf "%02d" $plan_num):"
       # Update checkbox: - [ ] -> - [x]
       ISSUE_BODY=$(echo "$ISSUE_BODY" | sed "s/^- \[ \] ${PLAN_ID}/- [x] ${PLAN_ID}/")
     done
     ```

     4. Write and update:
     ```bash
     printf '%s\n' "$ISSUE_BODY" > /tmp/phase-issue-body.md
     gh issue edit "$ISSUE_NUMBER" --body-file /tmp/phase-issue-body.md 2>/dev/null \
       && echo "Updated issue #${ISSUE_NUMBER}: checked off Wave ${WAVE_NUM} plans" \
       || echo "Warning: Failed to update issue #${ISSUE_NUMBER}"
     ```

     This update happens ONCE per wave (after all plans in wave complete), not per-plan, avoiding race conditions.

   - **Open Draft PR (first wave only, pr_workflow only):**

     After first wave completion:
     ```bash
     if [ "$PR_WORKFLOW" = "true" ] && [ "$WAVE_NUM" = "1" ]; then
       # Check if PR already exists (re-run protection)
       EXISTING_PR=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number' 2>/dev/null)
       if [ -n "$EXISTING_PR" ]; then
         echo "PR #${EXISTING_PR} already exists, skipping creation"
         PR_NUMBER="$EXISTING_PR"
       else
         # Push branch and create draft PR
         git push -u origin "$BRANCH"

         # Get phase name from ROADMAP.md
         PHASE_NAME=$(grep -E "^Phase ${PHASE_NUM}:" .planning/ROADMAP.md | sed -E 's/^Phase [0-9]+: //' | cut -d'—' -f1 | xargs)

         # Build PR body
         PHASE_GOAL=$(grep -A 2 "^Phase ${PHASE_NUM}:" .planning/ROADMAP.md | grep "Goal:" | sed 's/.*Goal: //')

         # Get phase issue number for linking (if github.enabled)
         CLOSES_LINE=""
         if [ "$GITHUB_ENABLED" = "true" ] && [ "$ISSUE_MODE" != "never" ]; then
           PHASE_ISSUE=$(gh issue list --label phase --milestone "v${MILESTONE}" \
             --json number,title --jq ".[] | select(.title | startswith(\"Phase ${PHASE_NUM}:\")) | .number" 2>/dev/null)
           [ -n "$PHASE_ISSUE" ] && CLOSES_LINE="Closes #${PHASE_ISSUE}"
         fi

         # Build plans checklist (all unchecked initially)
         PLANS_CHECKLIST=""
         for plan in ${PHASE_DIR}/*-PLAN.md; do
           plan_name=$(grep -m1 "<name>" "$plan" | sed 's/.*<name>//;s/<\/name>.*//' || basename "$plan" | sed 's/-PLAN.md//')
           plan_num=$(basename "$plan" | sed -E 's/^[0-9]+-([0-9]+)-PLAN\.md$/\1/')
           PLANS_CHECKLIST="${PLANS_CHECKLIST}- [ ] Plan ${plan_num}: ${plan_name}\n"
         done

         cat > /tmp/pr-body.md << PR_EOF
## Phase Goal

${PHASE_GOAL}

## Plans

${PLANS_CHECKLIST}
${CLOSES_LINE}
PR_EOF

         # Create draft PR
         gh pr create --draft \
           --base main \
           --title "v${MILESTONE} Phase ${PHASE_NUM}: ${PHASE_NAME}" \
           --body-file /tmp/pr-body.md

         PR_NUMBER=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number')
         echo "Created draft PR #${PR_NUMBER}"
       fi
     fi
     ```

     Store PR_NUMBER for step 10.5.

     **Note:** PR body checklist items remain unchecked throughout execution. The PR body is static after creation — it does NOT update as plans complete. The GitHub issue (updated after each wave above) is the source of truth for plan progress during execution.

   - Proceed to next wave

5. **Aggregate results**
   - Collect summaries from all plans
   - Report phase completion status

6. **Commit any orchestrator corrections**
   Check for uncommitted changes before verification:
   ```bash
   git status --porcelain
   ```

   **If changes exist:** Orchestrator made corrections between executor completions. Commit them:
   ```bash
   git add -u && git commit -m "fix({phase}): orchestrator corrections"
   ```

   **If clean:** Continue to verification.

7. **Verify phase goal**
   Check config: `WORKFLOW_VERIFIER=$(cat .planning/config.json 2>/dev/null | grep -o '"verifier"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")`

   **If `workflow.verifier` is `false`:** Skip to step 8 (treat as passed).

   **Otherwise:**
   - Spawn `kata-verifier` subagent with phase directory and goal
   - Verifier checks must_haves against actual codebase (not SUMMARY claims)
   - Creates VERIFICATION.md with detailed report
   - Route by status:
     - `passed` → continue to step 8
     - `human_needed` → present items, get approval or feedback
     - `gaps_found` → present gaps, offer `/kata:plan-phase {X} --gaps`

8. **Update roadmap and state**
   - Update ROADMAP.md, STATE.md

9. **Update requirements**
   Mark phase requirements as Complete:
   - Read ROADMAP.md, find this phase's `Requirements:` line (e.g., "AUTH-01, AUTH-02")
   - Read REQUIREMENTS.md traceability table
   - For each REQ-ID in this phase: change Status from "Pending" to "Complete"
   - Write updated REQUIREMENTS.md
   - Skip if: REQUIREMENTS.md doesn't exist, or phase has no Requirements line

10. **Commit phase completion**
    Check `COMMIT_PLANNING_DOCS` from config.json (default: true).
    If false: Skip git operations for .planning/ files.
    If true: Bundle all phase metadata updates in one commit:
    - Stage: `git add .planning/ROADMAP.md .planning/STATE.md`
    - Stage REQUIREMENTS.md if updated: `git add .planning/REQUIREMENTS.md`
    - Commit: `docs({phase}): complete {phase-name} phase`

10.25. **Review Documentation (Non-blocking, pr_workflow only)**

    If PR_WORKFLOW=true, before marking PR ready, offer README review:

    Use AskUserQuestion:
    - header: "README Review"
    - question: "This phase may have added user-facing features. Review README before marking PR ready?"
    - options:
      - "Yes, I'll update README" — Pause for user edits, wait for "continue"
      - "Skip" — Proceed to mark PR ready
      - "Show README" — Display current README, then ask if updates needed

    **If user chooses "Yes, I'll update README":**
    ```
    Update README.md with any documentation for this phase's features.
    Say "continue" when ready to mark the PR ready.
    ```

    **If user chooses "Show README":**
    Display README.md content, then use AskUserQuestion:
    - header: "README Updates"
    - question: "Does the README need updates for this phase?"
    - options:
      - "Yes, I'll update now" — Pause for user edits, wait for "continue"
      - "No, looks good" — Proceed to mark PR ready

    After README updates (if any), stage and commit:
    ```bash
    # Only if README was modified
    if git diff --quiet README.md; then
      echo "No README changes"
    else
      git add README.md
      git commit -m "docs({phase}): update README for phase features"
    fi
    ```

    *Non-blocking: phase completion continues regardless of choice.*

10.5. **Mark PR Ready (pr_workflow only)**

    After phase completion commit:
    ```bash
    if [ "$PR_WORKFLOW" = "true" ]; then
      # Push final commits
      git push origin "$BRANCH"

      # Mark PR ready for review
      gh pr ready

      PR_URL=$(gh pr view --json url --jq '.url')
      echo "PR marked ready: $PR_URL"
    fi
    ```

    Store PR_URL for offer_next output.

10.6. **Run PR Review (pr_workflow only, optional)**

    After marking PR ready, offer to run automated review:

    Use AskUserQuestion:
    - header: "PR Review"
    - question: "Run automated PR review before team review?"
    - options:
      - "Yes, run full review" — Run kata-reviewing-pull-requests with all aspects
      - "Quick review (code only)" — Run kata-reviewing-pull-requests with "code" aspect only
      - "Skip" — Proceed without review

    **If user chooses review:**
    1. Invoke skill: `Skill("kata:reviewing-pull-requests", "<aspect>")`
    2. Display review summary with counts: {N} critical, {M} important, {P} suggestions
    3. **STOP and ask what to do with findings** (see below)

    **If user chooses "Skip":**
    Continue to step 11 without review.

10.7. **Handle Review Findings (required after review completes)**

    **STOP here. Do not proceed to step 11 until user chooses an action.**

    Use AskUserQuestion with options based on what was found:
    - header: "Review Findings"
    - question: "How do you want to handle the review findings?"
    - options (show only applicable ones):
      - "Fix critical issues" — (if critical > 0) Fix critical, then offer to add remaining to backlog
      - "Fix critical & important" — (if critical + important > 0) Fix both, then offer to add suggestions to backlog
      - "Fix all issues" — (if any issues) Fix everything
      - "Add to backlog" — Create todos for all issues without fixing
      - "Ignore and continue" — Skip all issues

    **After user chooses:**

    **Path A: "Fix critical issues"**
    1. Fix each critical issue
    2. If important or suggestions remain, ask: "Add remaining {N} issues to backlog?"
       - "Yes" → Create todos, store TODOS_CREATED count
       - "No" → Continue
    3. Continue to step 11

    **Path B: "Fix critical & important"**
    1. Fix each critical and important issue
    2. If suggestions remain, ask: "Add {N} suggestions to backlog?"
       - "Yes" → Create todos, store TODOS_CREATED count
       - "No" → Continue
    3. Continue to step 11

    **Path C: "Fix all issues"**
    1. Fix all critical, important, and suggestion issues
    2. Continue to step 11

    **Path D: "Add to backlog"**
    1. Create todos for all issues using `/kata:add-todo`
    2. Store TODOS_CREATED count
    3. Continue to step 11

    **Path E: "Ignore and continue"**
    1. Continue to step 11

    Store REVIEW_SUMMARY and TODOS_CREATED for offer_next output.

11. **Offer next steps**
    - Route to next action (see `<offer_next>`)
</process>

<offer_next>
Output this markdown directly (not as a code block). Route based on status:

| Status                 | Route                                              |
| ---------------------- | -------------------------------------------------- |
| `gaps_found`           | Route C (gap closure)                              |
| `human_needed`         | Present checklist, then re-route based on approval |
| `passed` + more phases | Route A (next phase)                               |
| `passed` + last phase  | Route B (milestone complete)                       |

---

**Route A: Phase verified, more phases remain**

**Step 1: If PR_WORKFLOW=true, STOP and ask about merge BEFORE showing completion output.**

Use AskUserQuestion:
- header: "PR Ready for Merge"
- question: "PR #{pr_number} is ready. Merge before continuing to next phase?"
- options:
  - "Yes, merge now" — merge PR, then show completion
  - "No, continue without merging" — show completion with PR status

**Step 2: Handle merge response (if PR_WORKFLOW=true)**

If user chose "Yes, merge now":
```bash
gh pr merge "$PR_NUMBER" --squash --delete-branch
git checkout main && git pull
```
Set MERGED=true for output below.

**Step 3: Show completion output**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PHASE {Z} COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

{Y} plans executed
Goal verified ✓
{If github.enabled: GitHub Issue: #{issue_number} ({checked}/{total} plans checked off)}
{If PR_WORKFLOW and MERGED: PR: #{pr_number} — merged ✓}
{If PR_WORKFLOW and not MERGED: PR: #{pr_number} ({pr_url}) — ready for review}
{If REVIEW_SUMMARY: PR Review: {summary_stats}}
{If TODOS_CREATED: Backlog: {N} todos created from review suggestions}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

`/kata:discuss-phase {Z+1}` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- `/kata:plan-phase {Z+1}` — skip discussion, plan directly
- `/kata:verify-work {Z}` — manual acceptance testing before continuing
{If PR_WORKFLOW and not MERGED: - `gh pr view --web` — review PR in browser before next phase}

───────────────────────────────────────────────────────────────

---

**Route B: Phase verified, milestone complete**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► MILESTONE COMPLETE 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**v1.0**

{N} phases completed
All phase goals verified ✓
{If pr_workflow: Phase PRs ready — merge to prepare for release}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Audit milestone** — verify requirements, cross-phase integration, E2E flows

/kata:audit-milestone

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- /kata:verify-work — manual acceptance testing
- /kata:complete-milestone — skip audit, archive directly

───────────────────────────────────────────────────────────────

---

**Route C: Gaps found — need additional planning**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PHASE {Z} GAPS FOUND ⚠
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

Score: {N}/{M} must-haves verified
Report: .planning/phases/{phase_dir}/{phase}-VERIFICATION.md

### What's Missing

{Extract gap summaries from VERIFICATION.md}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Plan gap closure** — create additional plans to complete the phase

/kata:plan-phase {Z} --gaps

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- cat .planning/phases/{phase_dir}/{phase}-VERIFICATION.md — see full report
- /kata:verify-work {Z} — manual testing before planning

───────────────────────────────────────────────────────────────

---

After user runs /kata:plan-phase {Z} --gaps:
1. Planner reads VERIFICATION.md gaps
2. Creates plans 04, 05, etc. to close gaps
3. User runs /kata:execute-phase {Z} again
4. phase-execute runs incomplete plans (04, 05...)
5. Verifier runs again → loop until passed
</offer_next>

<wave_execution>
**Parallel spawning:**

Before spawning, read file contents using Read tool. The `@` syntax does not work across Task() boundaries - content must be inlined in the Task prompt.

**Read these files:**
- Each plan file in the wave (e.g., `{plan_01_path}`, `{plan_02_path}`, etc.)
- `.planning/STATE.md`

Spawn all plans in a wave with a single message containing multiple Task calls, with inlined content:

```
Task(prompt="Execute plan at {plan_01_path}\n\n<plan>\n{plan_01_content}\n</plan>\n\n<project_state>\n{state_content}\n</project_state>", subagent_type="kata-executor", model="{executor_model}")
Task(prompt="Execute plan at {plan_02_path}\n\n<plan>\n{plan_02_content}\n</plan>\n\n<project_state>\n{state_content}\n</project_state>", subagent_type="kata-executor", model="{executor_model}")
Task(prompt="Execute plan at {plan_03_path}\n\n<plan>\n{plan_03_content}\n</plan>\n\n<project_state>\n{state_content}\n</project_state>", subagent_type="kata-executor", model="{executor_model}")
```

All three run in parallel. Task tool blocks until all complete.

**No polling.** No background agents. No TaskOutput loops.
</wave_execution>

<checkpoint_handling>
Plans with `autonomous: false` have checkpoints. The phase-execute.md workflow handles the full checkpoint flow:
- Subagent pauses at checkpoint, returns structured state
- Orchestrator presents to user, collects response
- Spawns fresh continuation agent (not resume)

See `@./references/phase-execute.md` step `checkpoint_handling` for complete details.
</checkpoint_handling>

<deviation_rules>
During execution, handle discoveries automatically:

1. **Auto-fix bugs** - Fix immediately, document in Summary
2. **Auto-add critical** - Security/correctness gaps, add and document
3. **Auto-fix blockers** - Can't proceed without fix, do it and document
4. **Ask about architectural** - Major structural changes, stop and ask user

Only rule 4 requires user intervention.
</deviation_rules>

<commit_rules>
**Per-Task Commits:**

After each task completes:
1. Stage only files modified by that task
2. Commit with format: `{type}({phase}-{plan}): {task-name}`
3. Types: feat, fix, test, refactor, perf, chore
4. Record commit hash for SUMMARY.md

**Plan Metadata Commit:**

After all tasks in a plan complete:
1. Stage plan artifacts only: PLAN.md, SUMMARY.md
2. Commit with format: `docs({phase}-{plan}): complete [plan-name] plan`
3. NO code files (already committed per-task)

**Phase Completion Commit:**

After all plans in phase complete (step 7):
1. Stage: ROADMAP.md, STATE.md, REQUIREMENTS.md (if updated), VERIFICATION.md
2. Commit with format: `docs({phase}): complete {phase-name} phase`
3. Bundles all phase-level state updates in one commit

**NEVER use:**
- `git add .`
- `git add -A`
- `git add src/` or any broad directory

**Always stage files individually.**
</commit_rules>

<success_criteria>
- [ ] All incomplete plans in phase executed
- [ ] Each plan has SUMMARY.md
- [ ] Phase goal verified (must_haves checked against codebase)
- [ ] VERIFICATION.md created in phase directory
- [ ] STATE.md reflects phase completion
- [ ] ROADMAP.md updated
- [ ] REQUIREMENTS.md updated (phase requirements marked Complete)
- [ ] GitHub issue checkboxes updated per wave (if github.enabled)
- [ ] User informed of next steps
</success_criteria>
