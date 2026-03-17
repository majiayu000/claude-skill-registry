---
name: kata-complete-milestone
description: Archive a completed milestone, preparing for the next version, marking a milestone complete, shipping a version, or wrapping up milestone work. Triggers include "complete milestone", "finish milestone", "archive milestone", "ship version", "mark milestone done", "milestone complete", "release version", "create release", and "ship milestone".
metadata:
  version: "0.1.0"
allowed-tools: Read Write Bash
---
<objective>
Mark milestone {{version}} complete, archive to milestones/, and update ROADMAP.md and REQUIREMENTS.md.

Purpose: Create historical record of shipped version, archive milestone artifacts (roadmap + requirements), and prepare for next milestone.
Output: Milestone archived (roadmap + requirements), PROJECT.md evolved, git tagged.
</objective>

<execution_context>
**Load these files NOW (before proceeding):**

- @./references/milestone-complete.md (main workflow)
- @./references/milestone-archive-template.md (archive template)
- @./references/version-detector.md (version detection functions)
- @./references/changelog-generator.md (changelog generation functions)
  </execution_context>

<context>
**Project files:**
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `.planning/STATE.md`
- `.planning/PROJECT.md`

**User input:**

- Version: {{version}} (e.g., "1.0", "1.1", "2.0")
  </context>

<process>

**Follow milestone-complete.md workflow:**

0. **CRITICAL: Branch setup (if pr_workflow=true)**

   **Check pr_workflow config FIRST before any other work:**

   ```bash
   PR_WORKFLOW=$(cat .planning/config.json 2>/dev/null | grep -o '"pr_workflow"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
   CURRENT_BRANCH=$(git branch --show-current)
   ```

   **If `PR_WORKFLOW=true` AND on `main`:**

   You MUST create a release branch BEFORE proceeding. All milestone completion work goes on that branch.

   ```bash
   # Determine version from user input or detect from project files
   # (version-detector.md handles detection across project types)
   VERSION="X.Y.Z"  # Set from user input or detection

   # Create release branch
   git checkout -b release/v$VERSION

   echo "Created release branch: release/v$VERSION"
   echo "All milestone completion work will be committed here."
   ```

   Display:
   ```
   ⚠ pr_workflow is enabled — creating release branch first.

   Branch: release/v$VERSION

   All milestone completion commits will go to this branch.
   After completion, a PR will be created to merge to main.
   ```

   **If `PR_WORKFLOW=false` OR already on a non-main branch:**

   Proceed with current branch (commits go to main or current branch).

   **GATE: Do NOT proceed until branch is correct:**
   - If pr_workflow=true, you must be on release/vX.Y.Z branch
   - If pr_workflow=false, main branch is OK

0.1. **Generate release artifacts:**

   Proactively generate changelog and version bump. Follow the release_workflow step in milestone-complete.md (loads version-detector.md and changelog-generator.md) to:
   1. Detect version bump type from conventional commits
   2. Calculate next version
   3. Generate changelog entry
   4. Bump version in all project version files detected by version-detector.md
   5. Insert changelog entry into CHANGELOG.md

   Present all proposed changes for review:
   ```
   ## Release Preview

   **Current version:** $CURRENT_VERSION
   **Bump type:** $BUMP_TYPE
   **Next version:** $NEXT_VERSION

   **Changelog entry:**
   ## [$NEXT_VERSION] - $DATE

   ### Added
   [feat commits formatted]

   ### Fixed
   [fix commits formatted]

   ### Changed
   [docs/refactor/perf commits formatted]

   **Files updated:**
   [list each version file detected and updated]
   - CHANGELOG.md → new entry prepended
   ```

   Use AskUserQuestion:
   - header: "Release Changes"
   - question: "Review the release changes above. Approve?"
   - options:
     - "Approve" — Keep changes and proceed to verify readiness
     - "Edit changelog first" — Pause for user edits, then confirm
     - "Revert and skip release" — Undo release file changes, proceed to verify readiness without release artifacts

1. **Check for audit:**

   - Look for `.planning/v{{version}}-MILESTONE-AUDIT.md`
   - If missing or stale: recommend `/kata-audit-milestone` first
   - If audit status is `gaps_found`: recommend `/kata-plan-milestone-gaps` first
   - If audit status is `passed`: proceed to step 1

   ```markdown
   ## Pre-flight Check

   {If no v{{version}}-MILESTONE-AUDIT.md:}
   ⚠ No milestone audit found. Run `/kata-audit-milestone` first to verify
   requirements coverage, cross-phase integration, and E2E flows.

   {If audit has gaps:}
   ⚠ Milestone audit found gaps. Run `/kata-plan-milestone-gaps` to create
   phases that close the gaps, or proceed anyway to accept as tech debt.

   {If audit passed:}
   ✓ Milestone audit passed. Proceeding with completion.
   ```

1. **Verify readiness:**

   - Check all phases in milestone have completed plans (SUMMARY.md exists)
   - Present milestone scope and stats
   - Wait for confirmation

2. **Gather stats:**

   - Count phases, plans, tasks
   - Calculate git range, file changes, LOC
   - Extract timeline from git log
   - Present summary, confirm

3. **Extract accomplishments:**

   - Read all phase SUMMARY.md files in milestone range
   - Extract 4-6 key accomplishments
   - Present for approval

4. **Archive milestone:**

   - Create `.planning/milestones/v{{version}}-ROADMAP.md`
   - Extract full phase details from ROADMAP.md
   - Fill milestone-archive.md template
   - Update ROADMAP.md to one-line summary with link

5. **Archive requirements:**

   - Create `.planning/milestones/v{{version}}-REQUIREMENTS.md`
   - Mark all v1 requirements as complete (checkboxes checked)
   - Note requirement outcomes (validated, adjusted, dropped)
   - Delete `.planning/REQUIREMENTS.md` (fresh one created for next milestone)

6. **Update PROJECT.md:**

   - Add "Current State" section with shipped version
   - Add "Next Milestone Goals" section
   - Archive previous content in `<details>` (if v1.1+)

6.5. **Review Documentation (Non-blocking):**

   Before committing, offer final README review:

   Use AskUserQuestion:
   - header: "Final README Review"
   - question: "Revise README before completing milestone v{{version}}?"
   - options:
     - "Yes, draft an update for my review" — Revise README and present to the user for approval
     - "No, I'll make the edits myself" — Pause for user review, wait for "continue"
     - "Skip for now" — Proceed directly to commit

   **If "Yes, I'll review now":**
   ```
   Review README.md for the complete v{{version}} milestone.
   Ensure all shipped features are documented.
   Say "continue" when ready to proceed.
   ```

   **If "Show README":**
   Display README.md, then use AskUserQuestion:
   - header: "README Accuracy"
   - question: "Does this look accurate for v{{version}}?"
   - options:
     - "Yes, looks good" — Proceed to Step 7
     - "Needs updates" — Pause for user edits, wait for "continue"

   **If "Skip" or review complete:** Proceed to Step 7.

   *Non-blocking: milestone completion continues regardless of choice.*

6.7. **Close GitHub Milestone:**

   If github.enabled, close the GitHub Milestone for this version.
   See milestone-complete.md `close_github_milestone` step for details.

7. **Commit and finalize:**

   - Stage: MILESTONES.md, PROJECT.md, ROADMAP.md, STATE.md, archive files
   - Commit: `chore: complete v{{version}} milestone`

   **PR workflow handling (branch was created in step 0):**

   ```bash
   PR_WORKFLOW=$(cat .planning/config.json 2>/dev/null | grep -o '"pr_workflow"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
   CURRENT_BRANCH=$(git branch --show-current)
   ```

   **If `PR_WORKFLOW=true` (on release/vX.Y.Z branch):**

   Push branch and create PR:

   ```bash
   # Push branch
   git push -u origin "$CURRENT_BRANCH"

   # Collect all phase issues for this milestone
   GITHUB_ENABLED=$(cat .planning/config.json 2>/dev/null | grep -o '"enabled"[[:space:]]*:[[:space:]]*[^,}]*' | head -1 | grep -o 'true\|false' || echo "false")
   ISSUE_MODE=$(cat .planning/config.json 2>/dev/null | grep -o '"issueMode"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "never")

   CLOSES_LINES=""
   if [ "$GITHUB_ENABLED" = "true" ] && [ "$ISSUE_MODE" != "never" ]; then
     # Get all phase issue numbers for this milestone
     # --state all includes already-closed issues (GitHub ignores redundant Closes #X,
     # but including them ensures PR body reflects all related work)
     PHASE_ISSUES=$(gh issue list --label phase --milestone "v{{version}}" \
       --state all --json number --jq '.[].number' 2>/dev/null)

     if [ -z "$PHASE_ISSUES" ]; then
       echo "Note: No phase issues found for milestone v{{version}}. This is expected for milestones without GitHub issues."
     fi

     # Build multi-line closes section
     for num in ${PHASE_ISSUES}; do
       CLOSES_LINES="${CLOSES_LINES}Closes #${num}
   "
     done
   fi

   # Create PR
   gh pr create \
     --title "v{{version}}: [Milestone Name]" \
     --body "$(cat <<EOF
   ## Summary

   Completes milestone v{{version}}.

   **Key accomplishments:**
   - [accomplishment 1]
   - [accomplishment 2]
   - [accomplishment 3]

   ## Release Files

   [list version files that were updated]
   - `CHANGELOG.md` — v{{version}} entry added

   ## After Merge

   Create GitHub Release with tag `v{{version}}`.

   ## Closes

   ${CLOSES_LINES}
   EOF
   )"
   ```

   Display:
   ```
   ✓ PR created: [PR URL]

   After merge:
   → Create GitHub Release with tag v{{version}}
   ```

   **If `PR_WORKFLOW=false` (on main):**

   Create tag locally:
   - Tag: `git tag -a v{{version}} -m "[milestone summary]"`
   - Ask about pushing tag

2. **Post-release verification:**

   After the release PR is merged (or tag is pushed), prompt for verification:

   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    POST-RELEASE CHECKLIST
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Before moving on, verify the release:

   ☐ CI/CD pipeline passed (if configured)
   ☐ Release artifacts published successfully
   ☐ Quick smoke test confirms basic functionality

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

   Use AskUserQuestion:
   - header: "Verification"
   - question: "Release verification complete?"
   - options:
     - "Yes, verified" — Continue to completion
     - "Something failed" — Stop and investigate
     - "Skip" — Continue without verifying

   **If "Something failed":** Stop and help debug the issue.
   **If "Yes" or "Skip":** Continue to step 9.

3. **Offer next steps:**
   - `/kata-add-milestone` — start next milestone (questioning → research → requirements → roadmap)

</process>

<success_criteria>

- Milestone archived to `.planning/milestones/v{{version}}-ROADMAP.md`
- Requirements archived to `.planning/milestones/v{{version}}-REQUIREMENTS.md`
- `.planning/REQUIREMENTS.md` deleted (fresh for next milestone)
- ROADMAP.md collapsed to one-line entry
- PROJECT.md updated with current state
- Git tag v{{version}} created (if pr_workflow=false) OR PR created/instructions given (if pr_workflow=true)
- GitHub Milestone v{{version}} closed (if github.enabled)
- Commit successful
- User knows next steps (including need for fresh requirements)

**If release workflow was run:**
- CHANGELOG.md updated with v{{version}} entry (reviewed and approved)
- Version bumped in all detected project version files
- GitHub Release created (if pr_workflow=false) OR instructions provided (if pr_workflow=true)
  </success_criteria>

<critical_rules>

- **Load workflow first:** Read milestone-complete.md before executing
- **Verify completion:** All phases must have SUMMARY.md files
- **User confirmation:** Wait for approval at verification gates
- **Archive before deleting:** Always create archive files before updating/deleting originals
- **One-line summary:** Collapsed milestone in ROADMAP.md should be single line with link
- **Context efficiency:** Archive keeps ROADMAP.md and REQUIREMENTS.md constant size per milestone
- **Fresh requirements:** Next milestone starts with `/kata-add-milestone` which includes requirements definition
  </critical_rules>
