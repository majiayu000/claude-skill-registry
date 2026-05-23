---
name: verifying-work
description: Use this skill when validating built features through conversational testing, running UAT, user acceptance testing, checking if features work, or verifying implementation. Triggers include "verify work", "test features", "UAT", "user testing", "check if it works", and "validate features".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
---

<user_command>/kata:verify-work</user_command>


<objective>
Validate built features through conversational testing with persistent state.

Purpose: Confirm what Claude built actually works from user's perspective. One test at a time, plain text responses, no interrogation. When issues are found, automatically diagnose, plan fixes, and prepare for execution.

Output: {phase}-UAT.md tracking all test results. If issues found: diagnosed gaps, verified fix plans ready for /kata:execute-phase
</objective>

<execution_context>
@./references/verify-work.md
@./references/UAT-template.md
</execution_context>

<context>
Phase: $ARGUMENTS (optional)
- If provided: Test specific phase (e.g., "4")
- If not provided: Check for active sessions or prompt for phase

@.planning/STATE.md
@.planning/ROADMAP.md
</context>

<process>
1. Check for active UAT sessions (resume or start new)
2. Find SUMMARY.md files for the phase
3. Extract testable deliverables (user-observable outcomes)
4. Create {phase}-UAT.md with test list
5. Present tests one at a time:
   - Show expected behavior
   - Wait for plain text response
   - "yes/y/next" = pass, anything else = issue (severity inferred)
6. Update UAT.md after each response
7. On completion: commit UAT.md
7.5. Finalize changes (pr_workflow only) — commit fixes, push, mark PR ready
7.6. Run PR review (pr_workflow only, optional) — offer automated review
7.7. Handle review findings — fix issues or add to backlog
8. If issues found:
   - Spawn parallel debug agents to diagnose root causes
   - Spawn kata-planner in --gaps mode to create fix plans
   - Spawn kata-plan-checker to verify fix plans
   - Iterate planner ↔ checker until plans pass (max 3)
   - Present ready status with `/clear` then `/kata:execute-phase`
</process>

<step_7_5_pr_workflow>
## 7.5. Finalize Changes (pr_workflow only)

Read pr_workflow config:
```bash
PR_WORKFLOW=$(cat .planning/config.json 2>/dev/null | grep -o '"pr_workflow"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
```

**If PR_WORKFLOW=false:** Skip to offer_next.

**If PR_WORKFLOW=true:**

1. Check for uncommitted changes:
   ```bash
   git status --porcelain
   ```

2. If changes exist, stage and commit them:
   ```bash
   git add -u
   git commit -m "fix({phase}): UAT fixes"
   ```

3. Push to branch:
   ```bash
   BRANCH=$(git branch --show-current)
   git push origin "$BRANCH"
   ```

4. Check if PR exists:
   ```bash
   PR_NUMBER=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number' 2>/dev/null)
   ```

5. If PR exists, mark ready (if still draft):
   ```bash
   gh pr ready "$PR_NUMBER" 2>/dev/null || true
   PR_URL=$(gh pr view --json url --jq '.url')
   ```

Store PR_NUMBER and PR_URL for offer_next.
</step_7_5_pr_workflow>

<step_7_6_pr_review>
## 7.6. Run PR Review (pr_workflow only, optional)

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
3. **STOP and ask what to do with findings** (see step 7.7)

**If user chooses "Skip":**
Continue to offer_next without review.
</step_7_6_pr_review>

<step_7_7_handle_findings>
## 7.7. Handle Review Findings (required after review completes)

**STOP here. Do not proceed to offer_next until user chooses an action.**

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
3. Commit and push fixes
4. Continue to offer_next

**Path B: "Fix critical & important"**
1. Fix each critical and important issue
2. If suggestions remain, ask: "Add {N} suggestions to backlog?"
   - "Yes" → Create todos, store TODOS_CREATED count
   - "No" → Continue
3. Commit and push fixes
4. Continue to offer_next

**Path C: "Fix all issues"**
1. Fix all critical, important, and suggestion issues
2. Commit and push fixes
3. Continue to offer_next

**Path D: "Add to backlog"**
1. Create todos for all issues using `/kata:add-todo`
2. Store TODOS_CREATED count
3. Continue to offer_next

**Path E: "Ignore and continue"**
1. Continue to offer_next

Store REVIEW_SUMMARY and TODOS_CREATED for offer_next output.
</step_7_7_handle_findings>

<anti_patterns>
- Don't use AskUserQuestion for test responses — plain text conversation
- Don't ask severity — infer from description
- Don't present full checklist upfront — one test at a time
- Don't run automated tests — this is manual user validation
- Don't fix issues during testing — log as gaps, diagnose after all tests complete
</anti_patterns>

<offer_next>
Output this markdown directly (not as a code block). Route based on UAT results:

| Status                          | Route                         |
| ------------------------------- | ----------------------------- |
| All tests pass + more phases    | Route A (next phase)          |
| All tests pass + last phase     | Route B (milestone complete)  |
| Issues found + fix plans ready  | Route C (execute fixes)       |
| Issues found + planning blocked | Route D (manual intervention) |

---

**Route A: All tests pass, more phases remain**

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
 Kata ► PHASE {Z} VERIFIED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

{N}/{N} tests passed
UAT complete ✓
{If PR_WORKFLOW and MERGED: PR: #{pr_number} — merged ✓}
{If PR_WORKFLOW and not MERGED: PR: #{pr_number} ({pr_url}) — ready for review}
{If REVIEW_SUMMARY: PR Review: {summary_stats}}
{If TODOS_CREATED: Backlog: {N} todos created from review suggestions}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

/kata:discuss-phase {Z+1} — gather context and clarify approach

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- /kata:plan-phase {Z+1} — skip discussion, plan directly
- /kata:execute-phase {Z+1} — skip to execution (if already planned)
{If PR_WORKFLOW and not MERGED: - `gh pr view --web` — review PR in browser before next phase}

───────────────────────────────────────────────────────────────

---

**Route B: All tests pass, milestone complete**

**Step 1: If PR_WORKFLOW=true, STOP and ask about merge BEFORE showing completion output.**

Use AskUserQuestion:
- header: "PR Ready for Merge"
- question: "PR #{pr_number} is ready. Merge before completing milestone?"
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
 Kata ► PHASE {Z} VERIFIED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

{N}/{N} tests passed
Final phase verified ✓
{If PR_WORKFLOW and MERGED: PR: #{pr_number} — merged ✓}
{If PR_WORKFLOW and not MERGED: PR: #{pr_number} ({pr_url}) — ready for review}
{If REVIEW_SUMMARY: PR Review: {summary_stats}}
{If TODOS_CREATED: Backlog: {N} todos created from review suggestions}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Audit milestone** — verify requirements, cross-phase integration, E2E flows

/kata:audit-milestone

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- /kata:complete-milestone — skip audit, archive directly
{If PR_WORKFLOW and not MERGED: - `gh pr view --web` — review PR in browser before audit}

───────────────────────────────────────────────────────────────

---

**Route C: Issues found, fix plans ready**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PHASE {Z} ISSUES FOUND ⚠
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

{N}/{M} tests passed
{X} issues diagnosed
Fix plans verified ✓

### Issues Found

{List issues with severity from UAT.md}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Execute fix plans** — run diagnosed fixes

/kata:execute-phase {Z} --gaps-only

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- cat .planning/phases/{phase_dir}/*-PLAN.md — review fix plans
- /kata:plan-phase {Z} --gaps — regenerate fix plans

───────────────────────────────────────────────────────────────

---

**Route D: Issues found, planning blocked**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PHASE {Z} BLOCKED ✗
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

{N}/{M} tests passed
Fix planning blocked after {X} iterations

### Unresolved Issues

{List blocking issues from planner/checker output}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Manual intervention required**

Review the issues above and either:
1. Provide guidance for fix planning
2. Manually address blockers
3. Accept current state and continue

───────────────────────────────────────────────────────────────

**Options:**
- /kata:plan-phase {Z} --gaps — retry fix planning with guidance
- /kata:discuss-phase {Z} — gather more context before replanning

───────────────────────────────────────────────────────────────
</offer_next>

<success_criteria>
- [ ] UAT.md created with tests from SUMMARY.md
- [ ] Tests presented one at a time with expected behavior
- [ ] Plain text responses (no structured forms)
- [ ] Severity inferred, never asked
- [ ] Batched writes: on issue, every 5 passes, or completion
- [ ] Committed on completion
- [ ] If issues: parallel debug agents diagnose root causes
- [ ] If issues: kata-planner creates fix plans from diagnosed gaps
- [ ] If issues: kata-plan-checker verifies fix plans (max 3 iterations)
- [ ] Ready for `/kata:execute-phase` when complete
</success_criteria>
