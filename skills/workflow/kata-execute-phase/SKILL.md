---
name: kata-execute-phase
description: Execute all plans in a phase with wave-based parallelization, running phase execution, or completing phase work. Triggers include "execute phase", "run phase", "execute plans", "run the phase", and "phase execution".
metadata:
  version: "0.1.0"
allowed-tools: Read Write Bash
---
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

   | Agent                       | quality | balanced | budget |
   | --------------------------- | ------- | -------- | ------ |
   | general-purpose (executor)  | opus    | sonnet   | sonnet |
   | kata-verifier      | sonnet  | sonnet   | haiku  |
   | kata-code-reviewer | opus    | sonnet   | sonnet |
   | kata-*-analyzer    | sonnet  | sonnet   | haiku  |

   *Note: Review agents (kata-code-reviewer, kata-*-analyzer) are spawned by the kata-review-pull-requests skill, which handles its own model selection based on the agents' frontmatter. The table above documents expected model usage for cost planning.*

   Store resolved models for use in Task calls below.

1. **Validate phase exists**
   Find phase directory using the discovery script:
   ```bash
   bash "${SKILL_BASE_DIR}/scripts/find-phase.sh" "$PHASE_ARG"
   ```
   Outputs `PHASE_DIR`, `PLAN_COUNT`, and `PHASE_STATE` as key=value pairs. Exit code 1 = not found, 2 = no plans. Parse the output to set these variables for subsequent steps.

1.25. **Move phase to active (state transition)**

   ```bash
   # Move from pending to active when execution begins
   # PHASE_STATE is from find-phase.sh output (step 1)
   if [ "$PHASE_STATE" = "pending" ]; then
     DIR_NAME=$(basename "$PHASE_DIR")
     mkdir -p ".planning/phases/active"
     mv "$PHASE_DIR" ".planning/phases/active/${DIR_NAME}"
     PHASE_DIR=".planning/phases/active/${DIR_NAME}"
     echo "Phase moved to active/"
   fi
   ```

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

3.5. **Display execution banner**

   Display stage banner and wave structure:

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Kata ► EXECUTING PHASE {X}: {Phase Name}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   **{N} plans, {M} waves:**

   | Wave | Plans | Description |
   |------|-------|-------------|
   | 1    | 01, 02 | {plan names from frontmatter} |
   | 2    | 03    | {plan name} |

   **Model profile:** {profile} (executor → {model})

4. **Execute waves**
   For each wave in order:
   - Spawn `general-purpose` executor for each plan in wave (parallel Task calls)
   - Wait for completion (Task blocks)
   - Verify SUMMARYs created
   - **Update GitHub issue checkboxes (if enabled):**

     Build COMPLETED_PLANS_IN_WAVE from SUMMARY.md files created this wave:
     ```bash
     # Get plan numbers from SUMMARYs that exist after this wave
     COMPLETED_PLANS_IN_WAVE=""
     for summary in $(find "${PHASE_DIR}" -maxdepth 1 -name "*-SUMMARY.md" 2>/dev/null); do
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

     After first wave completion (orchestrator provides PHASE_ARG):
     ```bash
     # Re-read config (bash blocks don't share state)
     PR_WORKFLOW=$(cat .planning/config.json 2>/dev/null | grep -o '"pr_workflow"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
     GITHUB_ENABLED=$(cat .planning/config.json 2>/dev/null | grep -o '"enabled"[[:space:]]*:[[:space:]]*[^,}]*' | head -1 | grep -o 'true\|false' || echo "false")
     ISSUE_MODE=$(cat .planning/config.json 2>/dev/null | grep -o '"issueMode"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "never")
     MILESTONE=$(grep -E "^\- \[.\] \*\*Phase|^### v" .planning/ROADMAP.md | grep -E "In Progress" | grep -oE "v[0-9]+\.[0-9]+(\.[0-9]+)?" | head -1 | tr -d 'v')
     [ -z "$MILESTONE" ] && MILESTONE=$(grep -oE 'v[0-9]+\.[0-9]+(\.[0-9]+)?' .planning/ROADMAP.md | head -1 | tr -d 'v')
     # PHASE_DIR already set by universal discovery in step 1
     PHASE_NUM=$(basename "$PHASE_DIR" | sed -E 's/^([0-9]+)-.*/\1/')
     BRANCH=$(git branch --show-current)

     if [ "$PR_WORKFLOW" = "true" ]; then
       # Check if PR already exists (re-run protection - also handles wave > 1)
       EXISTING_PR=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number' 2>/dev/null)
       if [ -n "$EXISTING_PR" ]; then
         echo "PR #${EXISTING_PR} already exists, skipping creation"
         PR_NUMBER="$EXISTING_PR"
       else
         # Push branch and create draft PR
         git push -u origin "$BRANCH"

         # Get phase name from ROADMAP.md (format: #### Phase N: Name)
         PHASE_NAME=$(grep -E "^#### Phase ${PHASE_NUM}:" .planning/ROADMAP.md | sed -E 's/^#### Phase [0-9]+: //' | xargs)

         # Build PR body (Goal is on next line after phase header)
         PHASE_GOAL=$(grep -A 3 "^#### Phase ${PHASE_NUM}:" .planning/ROADMAP.md | grep "Goal:" | sed 's/.*Goal:[[:space:]]*//')

         # Get phase issue number for linking (if github.enabled)
         CLOSES_LINE=""
         if [ "$GITHUB_ENABLED" = "true" ] && [ "$ISSUE_MODE" != "never" ]; then
           PHASE_ISSUE=$(gh issue list --label phase --milestone "v${MILESTONE}" \
             --json number,title --jq ".[] | select(.title | startswith(\"Phase ${PHASE_NUM}:\")) | .number" 2>/dev/null)
           [ -n "$PHASE_ISSUE" ] && CLOSES_LINE="Closes #${PHASE_ISSUE}"
           # Store PHASE_ISSUE for use in step 10.6 merge path
         fi

         # Build plans checklist (all unchecked initially)
         PLANS_CHECKLIST=""
         for plan in $(find "${PHASE_DIR}" -maxdepth 1 -name "*-PLAN.md" 2>/dev/null); do
           plan_name=$(grep -m1 "<name>" "$plan" | sed 's/.*<name>//;s/<\/name>.*//' || basename "$plan" | sed 's/-PLAN.md//')
           plan_num=$(basename "$plan" | sed -E 's/^[0-9]+-([0-9]+)-PLAN\.md$/\1/')
           PLANS_CHECKLIST="${PLANS_CHECKLIST}- [ ] Plan ${plan_num}: ${plan_name}\n"
         done

         # Collect source_issue references from all plans
         SOURCE_ISSUES=""
         for plan in $(find "${PHASE_DIR}" -maxdepth 1 -name "*-PLAN.md" 2>/dev/null); do
           source_issue=$(grep -m1 "^source_issue:" "$plan" | cut -d':' -f2- | xargs)
           if echo "$source_issue" | grep -q "^github:#"; then
             issue_num=$(echo "$source_issue" | grep -oE '#[0-9]+')
             [ -n "$issue_num" ] && SOURCE_ISSUES="${SOURCE_ISSUES}Closes ${issue_num}\n"
           fi
         done
         SOURCE_ISSUES=$(echo "$SOURCE_ISSUES" | sed '/^$/d')  # Remove empty lines

         cat > /tmp/pr-body.md << PR_EOF
## Phase Goal

${PHASE_GOAL}

## Plans

${PLANS_CHECKLIST}
${CLOSES_LINE}
${SOURCE_ISSUES:+
## Source Issues

${SOURCE_ISSUES}}
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

   **If clean:** Continue to test suite.

6.5. **Run project test suite**

   Before verification, run the project's test suite to catch regressions early:

   ```bash
   TEST_SCRIPT=$(cat package.json 2>/dev/null | grep -o '"test"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1)
   ```

   **If package.json has a test script:**
   - Run `npm test`
   - If tests pass: proceed to step 7
   - If tests fail: report test failures, still proceed to step 7

   **If no test script detected:**
   - Skip this step, proceed to step 7

   **Skip for gap phases:** If mode is `gap_closure`, skip test suite

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
     - `gaps_found` → present gaps, offer `/kata-plan-phase {X} --gaps`

7.5. **Validate completion and move to completed**

   After verification passes, validate completion artifacts before moving phase to completed:

   ```bash
   # Validate completion artifacts
   PLAN_COUNT=$(find "$PHASE_DIR" -maxdepth 1 -name "*-PLAN.md" 2>/dev/null | wc -l | tr -d ' ')
   MISSING=""
   if [ "$PLAN_COUNT" -eq 0 ]; then
     MISSING="${MISSING}\n- No PLAN.md files found"
   fi
   for plan in $(find "$PHASE_DIR" -maxdepth 1 -name "*-PLAN.md" 2>/dev/null); do
     plan_id=$(basename "$plan" | sed 's/-PLAN\.md$//')
     [ ! -f "$PHASE_DIR/${plan_id}-SUMMARY.md" ] && MISSING="${MISSING}\n- Missing SUMMARY.md for ${plan_id}"
   done
   # Non-gap phases require VERIFICATION.md
   IS_GAP=$(find "$PHASE_DIR" -maxdepth 1 -name "*-PLAN.md" -exec grep -l "gap_closure: true" {} + 2>/dev/null | head -1)
   if [ -z "$IS_GAP" ] && ! find "$PHASE_DIR" -maxdepth 1 -name "*-VERIFICATION.md" 2>/dev/null | grep -q .; then
     MISSING="${MISSING}\n- Missing VERIFICATION.md (required for non-gap phases)"
   fi

   if [ -z "$MISSING" ]; then
     DIR_NAME=$(basename "$PHASE_DIR")
     mkdir -p ".planning/phases/completed"
     mv "$PHASE_DIR" ".planning/phases/completed/${DIR_NAME}"
     PHASE_DIR=".planning/phases/completed/${DIR_NAME}"
     echo "Phase validated and moved to completed/"
   else
     echo "Warning: Phase incomplete:${MISSING}"
   fi
   ```

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

10.6. **Post-Verification Checkpoint (REQUIRED — Loop until user chooses "Skip to completion")**

    After PR is ready (or after phase commits if pr_workflow=false), present the user with post-verification options. This is the decision point before proceeding to completion output.

    **Control flow:**
    - UAT → returns here after completion
    - PR review → step 10.7 → returns here
    - Merge → executes merge → returns here
    - Skip → proceeds to step 11

    **IMPORTANT:** Do NOT skip this step. Do NOT proceed directly to step 11. The user must choose how to proceed.

    Use AskUserQuestion:
    - header: "Phase Complete"
    - question: "Phase {X} execution complete. What would you like to do?"
    - options:
      - "Run UAT (Recommended)" — Walk through deliverables for manual acceptance testing
      - "Run PR review" — 6 specialized agents review code quality
      - "Merge PR" — (if pr_workflow=true) Merge to main
      - "Skip to completion" — Trust automated verification, proceed to next phase/milestone

    **Note:** Show "Merge PR" option only if `pr_workflow=true` AND PR exists AND not already merged.

    **If user chooses "Run UAT":**
    1. Invoke skill: `Skill("kata:kata-verify-work", "{phase}")`
    2. UAT skill handles the walkthrough and any issues found
    3. After UAT completes, return to this step to ask again (user may want PR review or merge)

    **If user chooses "Run PR review":**
    4. Invoke skill: `Skill("kata:review-pull-requests")`
    5. Display review summary with counts: {N} critical, {M} important, {P} suggestions
    6. **STOP and ask what to do with findings** (see step 10.7)
    7. After findings handled, return to this step

    **If user chooses "Merge PR":**
    8. Execute merge:
       ```bash
       gh pr merge "$PR_NUMBER" --merge --delete-branch
       git checkout main && git pull

       # Explicitly close the phase issue (backup in case Closes #X didn't trigger)
       if [ -n "$PHASE_ISSUE" ]; then
         gh issue close "$PHASE_ISSUE" --comment "Closed by PR #${PR_NUMBER} merge" 2>/dev/null \
           && echo "Closed issue #${PHASE_ISSUE}" \
           || echo "Note: Issue #${PHASE_ISSUE} may already be closed"
       fi

       # Close source issues from plans (backup in case Closes #X didn't trigger)
       for plan in $(find "${PHASE_DIR}" -maxdepth 1 -name "*-PLAN.md" 2>/dev/null); do
         source_issue=$(grep -m1 "^source_issue:" "$plan" | cut -d':' -f2- | xargs)
         if echo "$source_issue" | grep -q "^github:#"; then
           issue_num=$(echo "$source_issue" | grep -oE '[0-9]+')
           gh issue close "$issue_num" --comment "Closed by PR #${PR_NUMBER} merge (source issue for plan)" 2>/dev/null || true
         fi
       done
       ```
    9. Set MERGED=true
    10. Return to this step to ask if user wants UAT or review before continuing

    **If user chooses "Skip to completion":**
    Continue to step 11.

10.7. **Handle Review Findings (required after PR review completes)**

    **STOP here. Do not proceed until user chooses an action.**

    Use AskUserQuestion with options based on what was found:
    - header: "Review Findings"
    - question: "How do you want to handle the review findings?"
    - options (show only applicable ones):
      - "Fix critical issues" — (if critical > 0) Fix critical, then offer to add remaining to backlog
      - "Fix critical & important" — (if critical + important > 0) Fix both, then offer to add suggestions to backlog
      - "Fix all issues" — (if any issues) Fix everything
      - "Add to backlog" — Create issues for all findings without fixing
      - "Ignore and continue" — Skip all issues

    **After user chooses:**

    **Path A: "Fix critical issues"**
    1. Fix each critical issue
    2. If important or suggestions remain, ask: "Add remaining {N} issues to backlog?"
       - "Yes" → Create issues, store TODOS_CREATED count
       - "No" → Continue
    3. Return to step 10.6 checkpoint

    **Path B: "Fix critical & important"**
    1. Fix each critical and important issue
    2. If suggestions remain, ask: "Add {N} suggestions to backlog?"
       - "Yes" → Create issues, store TODOS_CREATED count
       - "No" → Continue
    3. Return to step 10.6 checkpoint

    **Path C: "Fix all issues"**
    1. Fix all critical, important, and suggestion issues
    2. Return to step 10.6 checkpoint

    **Path D: "Add to backlog"**
    1. Create issues for all findings using `/kata-add-issue`
    2. Store TODOS_CREATED count
    3. Return to step 10.6 checkpoint

    **Path E: "Ignore and continue"**
    1. Return to step 10.6 checkpoint

    Store REVIEW_SUMMARY and TODOS_CREATED for offer_next output.

    **Note:** After handling findings, return to step 10.6 so user can choose UAT, merge, or skip. The checkpoint loop continues until user explicitly chooses "Skip to completion".

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

(Merge status already determined in step 10.6)

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
{If TODOS_CREATED: Backlog: {N} issues created from review suggestions}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

`/kata-discuss-phase {Z+1}` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- `/kata-plan-phase {Z+1}` — skip discussion, plan directly
- `/kata-verify-work {Z}` — manual acceptance testing before continuing
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
{If PR_WORKFLOW and MERGED: All phase PRs merged ✓}
{If PR_WORKFLOW and not MERGED: Phase PRs ready — merge to prepare for release}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Audit milestone** — verify requirements, cross-phase integration, E2E flows

/kata-audit-milestone

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- /kata-verify-work — manual acceptance testing
- /kata-complete-milestone — skip audit, archive directly

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

/kata-plan-phase {Z} --gaps

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- cat .planning/phases/{phase_dir}/{phase}-VERIFICATION.md — see full report
- /kata-verify-work {Z} — manual testing before planning

───────────────────────────────────────────────────────────────

---

After user runs /kata-plan-phase {Z} --gaps:
1. Planner reads VERIFICATION.md gaps
2. Creates plans 04, 05, etc. to close gaps
3. User runs /kata-execute-phase {Z} again
4. phase-execute runs incomplete plans (04, 05...)
5. Verifier runs again → loop until passed
</offer_next>

<wave_execution>
**Parallel spawning:**

Before spawning, read file contents using Read tool. The `@` syntax does not work across Task() boundaries - content must be inlined in the Task prompt.

**Read these files:**
- Each plan file in the wave (e.g., `{plan_01_path}`, `{plan_02_path}`, etc.)
- `.planning/STATE.md`
- `references/executor-instructions.md` (relative to skill base directory) — store as `executor_instructions_content`

Spawn all plans in a wave with a single message containing multiple Task calls, with inlined content:

```
Task(prompt="<agent-instructions>\n{executor_instructions_content}\n</agent-instructions>\n\nExecute plan at {plan_01_path}\n\n<plan>\n{plan_01_content}\n</plan>\n\n<project_state>\n{state_content}\n</project_state>", subagent_type="general-purpose", model="{executor_model}")
Task(prompt="<agent-instructions>\n{executor_instructions_content}\n</agent-instructions>\n\nExecute plan at {plan_02_path}\n\n<plan>\n{plan_02_content}\n</plan>\n\n<project_state>\n{state_content}\n</project_state>", subagent_type="general-purpose", model="{executor_model}")
Task(prompt="<agent-instructions>\n{executor_instructions_content}\n</agent-instructions>\n\nExecute plan at {plan_03_path}\n\n<plan>\n{plan_03_content}\n</plan>\n\n<project_state>\n{state_content}\n</project_state>", subagent_type="general-purpose", model="{executor_model}")
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
