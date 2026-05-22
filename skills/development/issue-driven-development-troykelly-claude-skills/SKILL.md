---
name: issue-driven-development
description: Use for any development work - the master 13-step coding process that orchestrates all other skills, ensuring GitHub issue tracking, proper branching, TDD, code review, and CI verification
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Task
  - mcp__github__*
  - mcp__git__*
  - mcp__memory__*
model: opus
---

# Issue-Driven Development

## Overview

The master coding process. Every step references specific skills. Follow in order.

**Core principle:** No work without an issue. No shortcuts. No exceptions.

**Announce at start:** "I'm using issue-driven-development to implement this work."

## Before Starting

Create TodoWrite items for each step you'll execute. This is not optional.

## The 13-Step Process

### Step 1: Issue Check

**Question:** Am I working on a clearly defined GitHub issue that is tracked in the project board?

**Actions:**
- If no issue exists → Create one using `issue-prerequisite` skill
- If issue is vague → Ask questions, UPDATE the issue, then proceed
- **VERIFY** issue is in GitHub Project with correct fields (not assumed - verified)

**Verification (MANDATORY) - uses cached data:**

```bash
# Verify issue is in project board (0 API calls - uses cache)
ITEM_ID=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == [ISSUE_NUMBER]) | .id")

if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
  echo "BLOCKED: Issue not in project board. Add it before proceeding."
  # Add to project (1 API call) and refresh cache (1 API call)
  gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --url "$(gh issue view [ISSUE_NUMBER] --json url -q .url)"
  export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)
  ITEM_ID=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == [ISSUE_NUMBER]) | .id")
fi

# Verify Status field is set (0 API calls - uses cache)
STATUS=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.id == \"$ITEM_ID\") | .status.name")

if [ -z "$STATUS" ] || [ "$STATUS" = "null" ]; then
  echo "BLOCKED: Issue has no Status in project. Set Status before proceeding."
fi
```

**Skill:** `issue-prerequisite`, `project-board-enforcement`

**Gate:** Do not proceed unless:
1. GitHub issue URL exists
2. Issue is verified in GitHub Project (ITEM_ID obtained)
3. Status field is set (Ready, Backlog, or In Progress)

---

### Step 2: Read Comments

**Question:** Are there comments on the issue I need to read?

**Actions:**
- Read all comments on the issue
- Note any decisions, clarifications, or context
- Check for linked issues or PRs

**Skill:** `issue-lifecycle`

---

### Step 3: Size Check

**Question:** Is this issue too large for a single task?

**Indicators of too-large:**
- More than 5 acceptance criteria
- Touches more than 3 unrelated areas
- Estimated > 1 context window of work
- Multiple independent deliverables

**If too large:**
1. Break into sub-issues using `issue-decomposition`
2. Link sub-issues to parent
3. Update parent issue as `parent` label
4. Loop back to Step 1 with first sub-issue

**Skill:** `issue-decomposition`

---

### Step 4: Memory Search

**Question:** Is there previous work on this issue or related issues?

**Actions:**
- Search `episodic-memory` for issue number, feature name, related terms
- Search `mcp__memory` knowledge graph for related entities
- Note any relevant context, decisions, or gotchas

**Skill:** `memory-integration`

---

### Step 5: Research

**Question:** Do I need to perform research to complete this task?

**Research types:**
1. **Repository documentation** - README, CONTRIBUTING, docs/
2. **Existing codebase** - Similar patterns, related code
3. **Online resources** - API docs, library references, Stack Overflow

**Actions:**
- Conduct necessary research
- Document findings in issue comment if significant
- Note any blockers or concerns

**Skill:** `pre-work-research`

---

### Step 6: Branch Check & Status Update

**Question:** Am I on the correct branch AND has the project status been updated?

**Rules:**
- NEVER work on `main`
- Create feature branch if needed
- Branch from correct base (usually `main`, sometimes existing feature branch)

**Naming:** `feature/issue-123-short-description` or `fix/issue-456-bug-name`

**Project Status Update (MANDATORY) - uses cached IDs:**

When starting work, update project board Status to "In Progress":

```bash
# Use cached IDs (0 API calls for lookups)
# GH_PROJECT_ID, GH_STATUS_FIELD_ID, GH_STATUS_IN_PROGRESS_ID set by session-start

# Update status to In Progress (1 API call)
gh project item-edit --project-id "$GH_PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$GH_STATUS_FIELD_ID" --single-select-option-id "$GH_STATUS_IN_PROGRESS_ID"

# Refresh cache and verify (1 API call)
export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)
NEW_STATUS=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.id == \"$ITEM_ID\") | .status.name")

if [ "$NEW_STATUS" != "In Progress" ]; then
  echo "ERROR: Failed to update project status. Cannot proceed."
  exit 1
fi
```

**Skill:** `branch-discipline`, `project-board-enforcement`

**Gate:** Do not proceed if:
1. On `main` branch
2. Project Status not updated to "In Progress"

---

### Step 7: TDD Development

**Process:** RED → GREEN → REFACTOR

**Standards to apply simultaneously:**
- `tdd-full-coverage` - Write test first, watch fail, minimal code to pass
- `strict-typing` - No `any` types, full typing
- `inline-documentation` - JSDoc/docstrings for all public APIs
- `inclusive-language` - Respectful terminology
- `no-deferred-work` - No TODOs, do it now

**Actions:**
- Write failing test for first acceptance criterion
- Implement minimal code to pass
- Refactor if needed
- Repeat for each criterion

**Skills:** `tdd-full-coverage`, `strict-typing`, `inline-documentation`, `inclusive-language`, `no-deferred-work`

---

### Step 8: Verification Loop

**Question:** Did I succeed in delivering what is documented in the issue?

**Actions:**
- Run all tests
- Check each acceptance criterion
- If any failure → Return to Step 7
- If 2 consecutive failures → Trigger `research-after-failure`

**Skill:** `acceptance-criteria-verification`, `research-after-failure`

---

### Step 9: Code Review (MANDATORY GATE)

**Question:** Minor change or major change?

**Minor change (Step 9.1):**
- Review only new tests and generated code
- Use `comprehensive-review` checklist

**Major change (Step 9.2):**
- Identify all impacted code
- Review new AND impacted tests and code
- Use `comprehensive-review` checklist

**7 Review Criteria:**
1. Blindspots - What am I missing?
2. Clarity/Consistency - Is code readable and consistent?
3. Maintainability - Can this be maintained?
4. Security - Any vulnerabilities?
5. Performance - Any bottlenecks?
6. Documentation - Adequate docs?
7. Style - Follows style guide?

**Security-Sensitive Check:**

```bash
# Check if any changed files are security-sensitive
git diff --name-only HEAD~1 | grep -E '(auth|security|middleware|api|password|token|secret|session|routes|\.sql)'
```

If matches found:
1. Invoke `security-reviewer` subagent OR perform `security-review` skill
2. Mark "Security-Sensitive: YES" in review artifact
3. Include security findings in artifact

**HARD REQUIREMENT:** Post review artifact to issue comment:

```markdown
<!-- REVIEW:START -->
## Code Review Complete

| Property | Value |
|----------|-------|
| Issue | #[ISSUE] |
| Scope | [MINOR|MAJOR] |
| Security-Sensitive | [YES|NO] |
| Reviewed | [ISO_TIMESTAMP] |

[... full artifact per comprehensive-review skill ...]

**Review Status:** ✅ COMPLETE
<!-- REVIEW:END -->
```

**Gate:** PR creation will be BLOCKED by hooks if artifact not found.

**Skills:** `review-scope`, `comprehensive-review`, `security-review`, `review-gate`

---

### Step 10: Implement Findings (ABSOLUTE REQUIREMENT)

**Rule:** Implement ALL recommendations from code review, regardless how minor.

**ABSOLUTE:** Every finding must result in ONE of:
1. **Fixed in this PR** - Code changed, tests pass, verified
2. **Tracking issue created** - Using `deferred-finding` skill

There is NO third option. "Won't fix without tracking" is NOT permitted.

**Actions:**
- Address each finding from review
- For findings that cannot be fixed now:
  1. Use `deferred-finding` skill to create tracking issue
  2. Add `review-finding` and `spawned-from:#ISSUE` labels
  3. Link tracking issue in review artifact
- Re-run affected tests
- Update review artifact to show:
  - All FIXED findings marked ✅
  - All DEFERRED findings with tracking issue #
  - "Unaddressed: 0"

**Gate:** Review artifact must show "Unaddressed: 0" before proceeding.

**Skills:** `apply-all-findings`, `deferred-finding`

---

### Step 11: Run Full Tests

**Actions:**
- Run full relevant test suite (not just new tests)
- Verify no regressions
- Check test coverage if available

**Skill:** `tdd-full-coverage`

---

### Step 12: Raise PR (GATED)

**Prerequisites (verified by hooks):**
- Review artifact posted to issue (Step 9)
- All findings addressed (Step 10) - "Unaddressed: 0"
- Review status is COMPLETE
- Full tests pass (Step 11)

**Actions:**
- Commit with descriptive message
- Push branch
- Create PR with complete documentation:
  - Summary of changes
  - Link to issue
  - Link to review artifact in issue
  - Verification report
  - Screenshots if UI changes

**CRITICAL:** The `PreToolUse` hook will BLOCK `gh pr create` if:
- No review artifact found in issue comments
- Review status is not COMPLETE
- Unaddressed findings > 0

If blocked, return to Step 9 or Step 10.

**Skills:** `clean-commits`, `pr-creation`, `review-gate`

---

### Step 13: CI Monitoring → Merge → Continue

**Actions:**
- Wait for CI to run
- If failure → Fix and push
- Repeat until green or truly unresolvable
- If unresolvable → Document in issue, mark as blocked

**When CI is green (MANDATORY):**
1. **Merge the PR immediately**: `gh pr merge [PR_NUMBER] --squash --delete-branch`
2. **Update project board Status to Done** (verify it updated)
3. **Continue to next issue** (in autonomous mode, do NOT stop and report)

```bash
# When CI passes
gh pr merge [PR_NUMBER] --squash --delete-branch

# Update project status to Done
# ... project board update commands ...

# Continue to next issue (do not stop)
```

**Do NOT:**
- Report "CI is green, ready for review/merge" and wait
- Summarize completed work and ask what to do next
- Stop after a single issue when more work remains

**Skills:** `ci-monitoring`

---

## Throughout the Process

**Issue AND project board updates happen CONTINUOUSLY, not as a separate step.**

### Mandatory Project Board Updates

These updates are NOT optional. They are gates.

| Moment | Project Status | Verification |
|--------|----------------|--------------|
| Starting work (Step 6) | → In Progress | Verify status changed |
| PR created (Step 12) | → In Review | Verify status changed |
| Work complete | → Done | Verify status changed |
| Blocked | → Blocked | Verify status changed |

### Issue Comment Updates

At minimum, update the issue:
- When starting work (Status → In Progress)
- When hitting blockers
- When making significant decisions
- When completing verification
- When raising PR

### Project Board Query (NOT Labels)

Use cached project data (`GH_CACHE_ITEMS`) for state queries. Never use labels for state. See `project-board-enforcement` skill.

## Error Handling

On failure: Assess severity → Preserve evidence → Attempt recovery → If unrecoverable, set status to Blocked. See `error-recovery` skill.

## Completion Criteria

Work is complete when:

- [ ] All acceptance criteria verified (PASS)
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Code review completed (comprehensive-review)
- [ ] Security review completed (if security-sensitive files)
- [ ] Review artifact posted to issue
- [ ] All review findings addressed (Unaddressed: 0)
- [ ] Deferred findings have tracking issues
- [ ] PR created with complete documentation
- [ ] CI is green
- [ ] Issue status updated
- [ ] **GitHub Project Status → Done (VERIFIED)**
- [ ] **Project board update confirmed (not assumed)**

## Quick Reference

| Step | Skill(s) | Gate |
|------|----------|------|
| 1 | issue-prerequisite, **project-board-enforcement** | Must have issue **IN PROJECT BOARD** |
| 2 | issue-lifecycle | - |
| 3 | issue-decomposition | - |
| 4 | memory-integration | - |
| 5 | pre-work-research | - |
| 6 | branch-discipline, **project-board-enforcement** | Must not be on main, **Status → In Progress** |
| 7 | tdd-full-coverage, strict-typing, inline-documentation, inclusive-language, no-deferred-work | - |
| 8 | acceptance-criteria-verification, research-after-failure | - |
| 9 | review-scope, comprehensive-review, security-review, review-gate | **Review artifact required** |
| 10 | apply-all-findings, deferred-finding | **Unaddressed: 0 required** |
| 11 | tdd-full-coverage | - |
| 12 | clean-commits, pr-creation, review-gate, **project-board-enforcement** | **Hook blocks without artifact**, **Status → In Review** |
| 13 | ci-monitoring, verification-before-merge | Must be green, **Status → Done on merge** |

## Enforcement

Hooks enforce:
- **PR creation** blocked without review artifact
- **PR merge** blocked without green CI
- **Stop** blocked if review incomplete
- **Project board** status must match work state

Gate failures require fixing before proceeding. See `project-board-enforcement` skill.
