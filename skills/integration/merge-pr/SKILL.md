---
name: merge-pr
description: |
  Prepare PR for merge and guide human to merge via GitHub web UI. MUST BE USED when user wants to merge a PR.
  Verifies CI passing, verifies Beads issue already closed (from PR creation), and provides merge instructions.
  Issue closure happens at PR creation time (create-pull-request skill), NOT at merge time.
  Use when user says "merge the PR", "merge it", "merge this", "ready to merge", "merge to master",
  or when user mentions CI passing, approved reviews, ready-to-merge state, ready to ship,
  merge, deployment, PR completion, or shipping code.
tags: [workflow, pr, github, merge, deployment]
allowed-tools:
  - Bash(bd:*)
  - Bash(git:*)
  - Bash(gh:*)
  - Read
---

# Merge Pull Request

Prepare PR for human merge via GitHub web UI (<30 seconds prep).

## Purpose

Final step in V3 workflow: commit → create PR → fix PR → **merge PR**

**Philosophy:** AI prepares, human executes merge (trust + safety)

Handles:
- Verify CI passing (all checks green)
- Verify approvals (recommended but not required)
- Check working tree clean
- **Verify Beads issue already closed** (NOT close it - that happens at PR creation)
- Provide merge instructions for web UI
- Post-merge cleanup (switch to master, sync Beads, cache docs)

**Human responsibility:**
- Execute merge via GitHub web UI
- Delete remote branch (via web UI)

## When to Use This Skill

**Trigger phrases:**
- "merge the PR"
- "merge it"
- "merge this"
- "prepare to merge"
- "ready to merge"

**Automatically invoked when:**
- User asks to merge current branch's PR
- User says "merge" in context of an open PR

## Workflow

### 1. Get PR Context

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Extract FEATURE_KEY from feature-<KEY>
FEATURE_KEY=$(echo $BRANCH | sed 's/^feature-//')

# Get PR number and URL
gh pr view --json number,url -q '{number, url}'
```

### 2. Verify PR Status

**A. Check CI Status**
```bash
gh pr view --json statusCheckRollup -q '.statusCheckRollup[] | select(.status == "COMPLETED") | {name, conclusion}'
```

**Criteria:**
- ✅ All required checks passed → Proceed
- ⚠️ Some checks pending → Warn user, let them decide
- ❌ Failing checks → Block prep, suggest "fix the PR" first

**B. Check Approvals (Recommended)**
```bash
gh pr view --json reviewDecision -q '.reviewDecision'
```

**Criteria:**
- ✅ APPROVED → Ideal, proceed
- ⚠️ Empty (no reviews) → Warn but allow (solo dev OK)
- ❌ CHANGES_REQUESTED → Block prep, suggest addressing feedback first

**C. Check Merge Conflicts**
```bash
gh pr view --json mergeable -q '.mergeable'
```

**Criteria:**
- ✅ MERGEABLE → Proceed
- ❌ CONFLICTING → Block prep, suggest rebasing first

### 3. Check Working Tree

**CRITICAL: Must be clean before closing Beads**

```bash
git status --porcelain
```

**If dirty:**
- Ask user: "Working tree has uncommitted changes. Commit them first?"
- Options:
  - a) Commit changes now (with Feature-Key trailer)
  - b) Stash changes
  - c) Abort merge prep

**If clean:**
- Proceed to Beads verification

### 4. Verify Beads Issue Already Closed

**CRITICAL: Issue must be closed BEFORE merge (happens at PR creation)**

```bash
# Get current issue status
STATUS=$(bd show $FEATURE_KEY --json | jq -r '.status')

if [ "$STATUS" != "closed" ]; then
  echo "❌ Error: Beads issue must be closed BEFORE merge"
  echo ""
  echo "Current status: $STATUS"
  echo "Expected: closed"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Why this matters:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Issues should be closed at PR creation time, not merge time."
  echo "This ensures JSONL merges atomically with code (no post-merge mutations)."
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Recovery options:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Option 1: Close issue now (less ideal but works)"
  echo "  bd close $FEATURE_KEY --reason \"Closing before merge in PR #$PR_NUMBER\""
  echo "  bd sync && git push"
  echo "  # Then retry merge"
  echo ""
  echo "Option 2: Close and recreate PR (atomic pattern)"
  echo "  bd close $FEATURE_KEY --reason \"Work complete, ready for review\""
  echo "  bd sync && git push"
  echo "  gh pr close $PR_NUMBER"
  echo "  gh pr create  # Creates new PR with JSONL already closed"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Future prevention:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "When creating PRs, use create-pull-request skill which asks:"
  echo "  'Is work complete?' → YES closes issue BEFORE creating PR"
  echo ""
  exit 1
fi

echo "✅ Beads issue already closed (status: $STATUS)"
echo "   → JSONL will merge atomically with code"
echo ""
```

**Why verify instead of close:**
- **Structural fix:** Issues closed at PR creation (create-pull-request skill)
- **Atomic merge:** JSONL already on feature branch when PR created
- **No post-merge mutations:** Never need to modify JSONL on master
- **Prevents hook conflicts:** All Beads state changes on feature branch
- **Clear workflow:** Closed = "ready to ship", Open = "work in progress"

### 5. Present Merge Instructions to User (MANDATORY)

**This confirmation is REQUIRED. Provide web UI link and clear instructions.**

```
✅ PR #156 Ready to Merge

Feature: GUARD_SKILL_ACTIVATION
Branch: feature-GUARD_SKILL_ACTIVATION
Beads: bd-pso (closed ✅)

Status:
✅ CI: All checks passed
✅ Beads: Closed and committed to feature branch
✅ Conflicts: None
✅ Working tree: Clean

📝 Merge Instructions:

1. Open PR in GitHub web UI:
   https://github.com/fengning-starsend/prime-radiant-ai/pull/156

2. Click "Squash and merge" button

3. Verify squash commit message includes:
   - Feature title
   - PR number
   - All commits squashed

4. Check "Delete branch" checkbox ✅

5. Confirm merge

After you merge, say "cleanup" and I'll switch to master and pull latest.
```

**Why human merges:**
- GitHub web UI handles squash reliably
- User sees final commit message before merge
- No risk of `gh pr merge` local cleanup failures
- User controls exact timing of merge
- Web UI provides visual confirmation

### 6. Wait for Human to Merge

**Do not proceed automatically. Wait for:**
- User confirmation: "merged" / "done" / "cleanup"
- User explicitly asks to verify merge succeeded

### 7. Post-Merge Cleanup (After User Confirms)

```bash
# Verify PR actually merged
STATE=$(gh pr view $PR_NUMBER --json state -q .state)

if [ "$STATE" != "MERGED" ]; then
  echo "⚠️ PR not merged yet. Waiting for merge..."
  exit 1
fi

# Get merge commit hash
MERGE_COMMIT=$(gh pr view $PR_NUMBER --json mergeCommit -q '.mergeCommit.oid' | cut -c1-7)

# Switch to master
git checkout master

# Pull latest (includes merge)
git pull origin master

# Verify merge commit is on master (search recent 20 commits, not just HEAD)
git log --oneline -20 | grep -q "$MERGE_COMMIT"

# Delete local feature branch (remote already deleted via web UI)
git branch -d feature-$FEATURE_KEY 2>/dev/null || echo "Branch already deleted"

# Sync Beads (imports closure from git)
bd sync
```

### 7.5. Auto-Cache Docs to Serena (If Docs Exist)

**After successful merge, cache docs for searchability:**

```bash
DOC_DIR="docs/$FEATURE_KEY"

if [ -d "$DOC_DIR" ]; then
  echo "💾 Caching docs to Serena..."

  # Get issue details
  ISSUE_JSON=$(bd show $FEATURE_KEY --json)
  ISSUE_TITLE=$(echo "$ISSUE_JSON" | jq -r '.title')
  ISSUE_TYPE=$(echo "$ISSUE_JSON" | jq -r '.type')

  # Combine all markdown files into cache
  CACHE_CONTENT="# $FEATURE_KEY: $ISSUE_TITLE

**Status:** closed (merged in PR #$PR_NUMBER)
**Type:** $ISSUE_TYPE
**Merged:** $(date +%Y-%m-%d)
**Source:** $DOC_DIR/

**[CACHE]** This is a searchable cache. Source of truth: git ($DOC_DIR/)

---

"

  # Append all markdown files
  find "$DOC_DIR" -name "*.md" -type f | while read file; do
    echo "## $(basename $file .md)" >> /tmp/cache_${FEATURE_KEY}.tmp
    echo "" >> /tmp/cache_${FEATURE_KEY}.tmp
    cat "$file" >> /tmp/cache_${FEATURE_KEY}.tmp
    echo "" >> /tmp/cache_${FEATURE_KEY}.tmp
    echo "---" >> /tmp/cache_${FEATURE_KEY}.tmp
    echo "" >> /tmp/cache_${FEATURE_KEY}.tmp
  done

  CACHE_CONTENT+=$(cat /tmp/cache_${FEATURE_KEY}.tmp)
  rm /tmp/cache_${FEATURE_KEY}.tmp

  # Write to Serena using MCP tool
  mcp__serena__write_memory(
    memory_file_name="${FEATURE_KEY}_merged",
    content="$CACHE_CONTENT"
  )

  echo "✅ Cached to Serena: ${FEATURE_KEY}_merged"
  echo "   Search with: /search '@serena ${FEATURE_KEY}'"
else
  echo "ℹ️  No docs to cache (Beads only)"
fi
```

**Why auto-cache:**
- Merged work becomes searchable via Serena
- Clearly marked as [CACHE] (not source of truth)
- Enables fast cross-feature references
- No manual step required
- Only happens after successful merge

**Verification:**
- ✅ On master branch
- ✅ Latest merge pulled
- ✅ Local feature branch deleted
- ✅ Beads synced
- ✅ Docs cached to Serena (if exist)

### 8. Confirm Completion

```
✅ Merge Complete

Merged: GUARD_SKILL_ACTIVATION → master
Commit: a1b2c3d (squashed 50 commits)
Beads: bd-pso (closed, synced to master)

Workspace:
✅ On master branch
✅ Pulled latest changes
✅ Local branch deleted
✅ Beads state synced

Ready for next feature.
```

## Integration Points

### With Beads
- **Verifies issue already closed** (closed at PR creation time by create-pull-request skill)
- **JSONL already in PR** (merged atomically with code)
- **Syncs after merge** (imports from master)
- **No post-merge mutations** (prevents hook conflicts on master)

### With create-pull-request
- **Completes lifecycle:** create-pull-request → fix-pr-feedback → merge-pr
- **Same PR** (no new PRs)
- **Bidirectional linking** (PR → Beads, Beads → PR)

### With GitHub Web UI
- **Human control** (user decides when to merge)
- **Visual confirmation** (see commit message before merging)
- **Reliable squash** (GitHub handles it)
- **Branch cleanup** (delete via checkbox)

## Safety Guardrails

**Before preparing:**
- ✅ Verify CI passing (block if failing)
- ✅ Verify no conflicts (block if conflicting)
- ⚠️ Check approvals (warn if missing, allow for solo dev)
- ✅ Verify working tree clean (block if dirty)

**Auto-prep allowed:**
- All checks passed
- No conflicts
- Working tree clean

**Require user approval:**
- Checks pending (ask if they want to wait)
- No approvals yet (warn but allow)
- CHANGES_REQUESTED (block, suggest fix-pr-feedback)

**Never auto-prep:**
- Failing CI checks
- Merge conflicts
- Dirty working tree
- User hasn't confirmed

## Best Practices

1. **Verify issue already closed** - Should be closed at PR creation time
2. **Clean working tree** - No uncommitted changes before verification
3. **Human merges** - Trust web UI reliability
4. **Wait for confirmation** - Don't assume merge happened
5. **Verify merge** - Check PR state before cleanup
6. **Sync Beads after** - Import closure from master
7. **Atomic merge pattern** - JSONL merges with code (no post-merge mutations)

## What This Skill Does

✅ Verify PR merge-readiness (CI, approvals, conflicts)
✅ Check working tree clean (block if dirty)
✅ **Verify Beads issue already closed** (error if not)
✅ Provide merge instructions with web UI link
✅ Wait for human to merge
✅ Clean up local workspace after merge
✅ Sync Beads state from master
✅ Auto-cache docs to Serena (if exist)

## What This Skill DOESN'T Do

❌ Merge PR automatically (human does via web UI)
❌ Delete remote branch (human does via web UI checkbox)
❌ Skip user confirmation (always waits for "merged" confirmation)
❌ **Close Beads issue** (already closed at PR creation time by create-pull-request skill)
❌ Push to master (never, pre-push hook blocks)
❌ Modify JSONL on master (never - atomic merge pattern prevents this)

## Anti-Patterns

❌ Closing Beads at merge time (should be closed at PR creation)
❌ Committing to master directly (pre-push hook blocks this)
❌ Auto-merging without human confirmation
❌ Skipping working tree check
❌ Not verifying merge succeeded before cleanup
❌ Modifying JSONL on master (causes hook conflicts)

## Example Scenarios

### Scenario 1: Clean Merge (Issue Already Closed)

```
User: "merge the PR"

AI:
1. Checks PR #156: CI passed ✅, No conflicts ✅
2. Checks working tree: Clean ✅
3. Verifies bd-pso status: closed ✅ (closed at PR creation)
4. Presents merge instructions with web UI link
5. Waits...

User: [Merges via web UI, deletes branch]

User: "merged"

AI:
6. Verifies PR state = MERGED
7. Switches to master, pulls
8. Deletes local branch
9. Syncs Beads
10. Caches docs to Serena
11. Confirms: "✅ Merge complete, workspace clean"
```

### Scenario 2: Dirty Working Tree

```
User: "merge the PR"

AI:
1. Checks PR status: ✅ Ready
2. Checks working tree: ❌ Dirty (.beads/beads.left.meta.json modified)
3. Asks: "Working tree has uncommitted changes. Options:
   a) Commit changes now
   b) Stash changes
   c) Abort merge prep"

User: "commit them"

AI:
4. Commits changes with Feature-Key trailer
5. Pushes to feature branch
6. Proceeds with Beads verification
7. Verifies issue closed ✅
8. Presents merge instructions
```

### Scenario 3: Failing CI

```
User: "merge the PR"

AI:
1. Checks CI: ❌ 2 checks failing (lint, test)
2. Blocks merge prep
3. Suggests: "❌ Cannot prepare merge: CI checks failing

   Failing checks:
   - lint: Line too long
   - test: AssertionError in test_foo

   Suggestion: Use 'fix the PR' to address failures first."
```

### Scenario 4: Issue Not Closed (Structural Problem)

```
User: "merge the PR"

AI:
1. Checks PR #200: CI passed ✅, No conflicts ✅
2. Checks working tree: Clean ✅
3. Checks Beads status: ❌ in_progress (NOT closed!)
4. Errors with recovery options:
   "❌ Error: Beads issue must be closed BEFORE merge

   Current status: in_progress
   Expected: closed

   Why this matters:
   Issues should be closed at PR creation time, not merge time.
   This ensures JSONL merges atomically with code.

   Recovery options:

   Option 1: Close issue now (less ideal but works)
     bd close bd-xyz --reason 'Closing before merge in PR #200'
     bd sync && git push
     # Then retry merge

   Option 2: Close and recreate PR (atomic pattern)
     bd close bd-xyz --reason 'Work complete, ready for review'
     bd sync && git push
     gh pr close 200
     gh pr create  # Creates new PR with JSONL already closed

   Future prevention:
   When creating PRs, use create-pull-request skill which asks:
     'Is work complete?' → YES closes issue BEFORE creating PR"
```

### Scenario 5: User Merges Before Confirmation

```
User: "merge the PR"

AI:
1. Prepares merge (closes Beads, commits, pushes)
2. Presents merge instructions
3. Waits for confirmation...

User: [Merges immediately without saying anything]

User: "check if it merged"

AI:
4. Checks PR state: MERGED ✅
5. Proceeds with cleanup
6. Confirms completion
```

## Troubleshooting

### "Working tree dirty" error
**Cause:** Uncommitted changes in working tree
**Fix:** Commit or stash changes, then retry

### "PR not found" error
**Cause:** Not on a feature branch, or PR doesn't exist
**Fix:** Switch to feature branch with open PR

### "CI checks failing" error
**Cause:** Required checks not passing
**Fix:** Use fix-pr-feedback skill to address failures

### "Merge conflicts" error
**Cause:** Branch conflicts with master
**Fix:** Rebase on master: `git fetch origin master && git rebase origin/master`

### "bd close failed" error
**Cause:** Beads issue doesn't exist or already closed
**Fix:** Verify issue ID matches branch name

## Future Enhancements

1. **Auto-wait for CI** - Poll until checks complete
2. **Conflict auto-resolution** - Attempt automatic rebase
3. **Smart approval** - Request review if needed
4. **Post-merge validation** - Verify deployment succeeded
5. **Rollback support** - Quick revert if issues found

---

**Last Updated:** 2025-11-13
**Related Skills:** create-pull-request, fix-pr-feedback, sync-feature-branch
**Helper Scripts:** scripts/bd-link-pr
**References:**
- PR workflow: AGENTS.md
- Beads integration: .claude/skills/beads-workflow/SKILL.md

**Changelog:**
- 2025-11-13: Initial creation with CI verification, approval checking, mandatory user confirmation
- 2025-11-13: **BREAKING** - Changed to human-merge workflow (Option A). AI prepares (closes Beads on feature branch), human merges via web UI, AI cleans up after confirmation. Fixes gh pr merge local cleanup failures.
