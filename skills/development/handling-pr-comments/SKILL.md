---
name: handling-pr-comments
description: Use when addressing PR review feedback, after receiving review comments
  from CodeRabbit, Cursor, or human reviewers - ensures systematic responses to each
  comment thread with proper attribution and thread resolution.
---

# handling-pr-comments

Use when addressing PR review feedback, after receiving review comments from CodeRabbit, Cursor, or human reviewers - ensures systematic responses to each comment thread with proper attribution and thread resolution.

## When to Activate

Activate this skill when ANY of these conditions are true:

- User asks to "address PR comments" or "handle review feedback"
- User mentions CodeRabbit, Cursor bot, or reviewer comments
- User is working on fixes requested in a PR review
- User asks to "check PR comments" or "respond to reviewers"
- After making fixes to address review feedback

## CRITICAL: The Complete Workflow

**Most developers forget steps 4-6. This skill ensures they happen.**

### Phase 1: Discover and Filter Comments

First, run `gtg` to get a quick overview of PR status and actionable comments:

```bash
# Get PR status and actionable comments
OWNER=$(gh repo view --json owner -q .owner.login)
REPO=$(gh repo view --json name -q .name)

gtg "$PR_NUMBER" --repo "$OWNER/$REPO" --format json > /tmp/gtg-status.json

# Show status
echo "Status: $(jq -r '.status' /tmp/gtg-status.json)"
echo "Actionable comments: $(jq -r '.actionable_comments | length' /tmp/gtg-status.json)"
echo "Unresolved threads: $(jq -r '.threads.unresolved' /tmp/gtg-status.json)"

# List action items
echo "Action items:"
jq -r '.action_items[]' /tmp/gtg-status.json
```

For detailed filtering and categorization, also run the filtering script:

```bash
# Filter actionable vs non-actionable comments
bin/pr-comments-filter.sh <PR_NUMBER>
```

This script:

- Filters out non-actionable comments (confirmations, acknowledgments, fingerprinting)
- Categorizes actionable comments by priority (Critical → Low)
- Shows comment IDs and details for processing

### Phase 2: Triage Actionable Comments

The filter script categorizes by priority:

| Priority        | Marker                                                   | Action           |
| --------------- | -------------------------------------------------------- | ---------------- |
| 🔴 **CRITICAL** | `_⚠️ Potential issue_ \| _🔴 Critical_`                  | Fix immediately  |
| 🟠 **HIGH**     | `_⚠️ Potential issue_ \| _🟠 Major_`                     | Fix before merge |
| 🟡 **MEDIUM**   | `_🟡 Minor_` or `_🛠️ Refactor suggestion_ \| _🟠 Major_` | Should fix       |
| 🔵 **LOW**      | `_🔵 Trivial_` / `_🧹 Nitpick_`                          | Fix if quick     |
| 👤 **HUMAN**    | Non-bot comments                                         | Always process   |

For each actionable comment, further categorize as:

1. **Bug/Issue** - Must fix
2. **Enhancement** - Should fix
3. **Nitpick** - Nice to fix
4. **Question** - Needs clarification
5. **Intentional** - Decline with explanation
6. **Out-of-Scope** - See Phase 2b

### Phase 2b: Extract "Outside Diff Range" Comments from Review Bodies (CRITICAL)

**⚠️ COMMONLY MISSED**: CodeRabbit posts "Outside diff range" comments in the **review body**, not as inline threads. These are actionable feedback that MUST be addressed.

```bash
# Extract Outside diff range comments from review bodies
PR_NUMBER=<number>
OWNER=$(gh repo view --json owner -q .owner.login)
REPO_NAME=$(gh repo view --json name -q .name)

echo "=== OUTSIDE DIFF RANGE COMMENTS ==="
gh api "repos/$OWNER/$REPO_NAME/pulls/$PR_NUMBER/reviews" --paginate | \
  jq -r '.[] | select(.body | test("Outside diff range"; "i")) |
    "Review ID: \(.id)\n\(.body)\n---"'
```

**These comments are NOT in threads** - they cannot be replied to inline. You must:

1. Parse the file paths and line numbers from the review body
2. Address the feedback in your code
3. Commit and push
4. Leave a general PR comment acknowledging you addressed them

### Phase 2c: Handle Other Out-of-Scope Comments

Run the out-of-scope detection script:

```bash
# Detect out-of-scope comments
bin/pr-comments-out-of-scope.sh <PR_NUMBER>
```

This script detects comments that:

- Reference lines NOT in the PR diff
- Are marked "outdated" by GitHub (GraphQL `isOutdated` flag)
- Are general PR discussion comments

**IMPORTANT**: Treat out-of-scope comments as **IN SCOPE** by default.

#### Evaluation Process

Use **ultrathink** to evaluate each out-of-scope comment:

```text
ultrathink: Analyze this out-of-scope review comment:
- What is the reviewer asking for?
- How complex is this change? (lines of code, files affected)
- Does it require refactoring other systems?
- Can I complete this in under 30 minutes?
- Are there any risks or dependencies?

Recommend: FIX_NOW or CREATE_ISSUE
```

#### Decision Matrix

| Criteria                                      | Action                                    |
| --------------------------------------------- | ----------------------------------------- |
| Simple fix (< 30 min, < 3 files, no refactor) | **FIX_NOW** - Make the change immediately |
| Medium complexity (unclear scope)             | **ASK_USER** - Present options            |
| Major refactor (multiple systems, risky)      | **CREATE_ISSUE** - Document for follow-up |

#### For FIX_NOW

1. Make the fix
2. Commit with descriptive message
3. Push to the PR branch
4. Reply: "Fixed in commit <hash>. This was outside the original PR scope but straightforward to address."
5. Resolve the thread

#### For CREATE_ISSUE

1. Create GitHub issue with context
2. Reply: "Created issue #<number> to track this."
3. Resolve the thread

### Phase 3: Make Fixes

Fix the actual code issues. Commit and push.

### Phase 4: RESPOND TO EACH THREAD (Often Forgotten!)

**After pushing fixes, respond to EACH comment thread individually:**

```bash
PR_NUMBER=<number>
OWNER=$(gh repo view --json owner -q .owner.login)
REPO_NAME=$(gh repo view --json name -q .name)
CURRENT_USER=$(gh api user -q '.login')
COMMENT_ID=<id-from-filter-script>

gh api "/repos/$OWNER/$REPO_NAME/pulls/$PR_NUMBER/comments/$COMMENT_ID/replies" \
  -X POST \
  -f body="Fixed in commit $(git rev-parse --short HEAD).

*(Response by Claude on behalf of @$CURRENT_USER)*"
```

### Phase 5: Resolve ALL Threads

**Every thread must be resolved after responding.** Use GraphQL to resolve:

```bash
THREAD_ID="PRRT_kwDOK-xA485..."  # From GraphQL query

gh api graphql -f query='mutation {
  resolveReviewThread(input: {threadId: "'"$THREAD_ID"'"}) {
    thread { id isResolved }
  }
}'
```

### Phase 6: Handle Threads That Can't Be Resolved

1. **Query the comment author** asking for specific follow-up
2. **Do NOT leave unresolved** - either resolve after responding, or ask for clarification
3. If waiting for author response, mark as needing user input

### Phase 7: Post-Push Iteration Check (MANDATORY)

**⚠️ THE #1 WORKFLOW FAILURE: Stopping after Phase 5-6 without checking for NEW comments.**

Automated reviewers (CodeRabbit, Cursor) analyze EVERY commit you push. They post NEW comments during/after their check runs.

```bash
# STEP 1: Wait for ALL CI/CD checks to complete
PR_NUMBER=<number>
echo "⏳ Waiting for CI/CD checks to complete..."
gh pr checks $PR_NUMBER --watch

# STEP 2: Check for NEW comments since your last response
OWNER=$(gh repo view --json owner -q .owner.login)
REPO_NAME=$(gh repo view --json name -q .name)
CURRENT_USER=$(gh api user -q '.login')

# Get timestamp of your last reply
LAST_REPLY=$(gh api "repos/$OWNER/$REPO_NAME/pulls/$PR_NUMBER/comments" --paginate | \
  jq -r "[.[] | select(.user.login == \"$CURRENT_USER\") | select(.in_reply_to_id)] | sort_by(.created_at) | last | .created_at")

# Handle case where user has no previous replies
if [ -z "$LAST_REPLY" ] || [ "$LAST_REPLY" = "null" ]; then
  echo "⚠️ No previous replies found - checking all comments as new"
  LAST_REPLY="1970-01-01T00:00:00Z"  # Unix epoch - treat all comments as new
fi

# Check for new comments after that time
NEW_COUNT=$(gh api "repos/$OWNER/$REPO_NAME/pulls/$PR_NUMBER/comments" --paginate | \
  jq -r --arg time "$LAST_REPLY" '[.[] | select(.in_reply_to_id == null) | select(.created_at > $time)] | length')

# STEP 3: Also check review bodies for new "Outside diff range" comments
NEW_REVIEWS=$(gh api "repos/$OWNER/$REPO_NAME/pulls/$PR_NUMBER/reviews" --paginate | \
  jq -r --arg time "$LAST_REPLY" '[.[] | select(.submitted_at > $time) | select(.body | test("Outside diff range"; "i"))] | length')

TOTAL_NEW=$((NEW_COUNT + NEW_REVIEWS))

if [ "$TOTAL_NEW" -gt 0 ]; then
  echo "🚨 $NEW_COUNT NEW INLINE COMMENT(S) + $NEW_REVIEWS NEW REVIEW BODY COMMENT(S) DETECTED"
  echo "ACTION: Return to Phase 1 and iterate"
else
  echo "✅ No new comments - safe to proceed to verification"
fi
```

**If NEW comments found**: Return to Phase 1. DO NOT proceed to verification.

**Iteration Loop**:

```text
REPEAT:
  Phase 1: Discover comments
  Phase 2: Triage
  Phase 3: Fix
  Phase 4: Respond
  Phase 5: Resolve threads
  Phase 6: Handle unclear threads
  Phase 7: Check for NEW comments after push

  IF new comments found → GO TO Phase 1
  IF no new comments → proceed to verification
```

## Response Templates

### For Fixes Made

```text
Fixed in commit <hash>.

*(Response by Claude on behalf of @username)*
```

### For Acknowledged Nitpicks

```text
Acknowledged - this is a valid suggestion. Deferring to a future cleanup PR to keep this PR focused.

*(Response by Claude on behalf of @username)*
```

### For Intentional Decisions

```text
This is intentional because [reason]. The [thing] is designed to [explanation].

*(Response by Claude on behalf of @username)*
```

## Mandatory Pre-Completion Check

**⚠️ BLOCKING: You MUST run this script and show its output before declaring ANY PR ready:**

```bash
bin/pr-comments-check.sh <PR_NUMBER>
```

This script:

- Returns exit code 0 if all comments addressed
- Returns exit code 1 if ANY unaddressed comments exist
- Shows ✅/❌ status for each comment

**If the script shows ANY ❌, you are NOT done.** Address each unaddressed comment:

1. If actionable → Fix it and reply confirming the fix
2. If out-of-scope → Reply explaining deferral (create issue if needed)
3. If disagree → Reply with reasoning
4. **NEVER ignore silently**

**You must show the script output in your response** as proof that all comments are addressed. Example:

```
🔍 Checking PR #908 for unaddressed comments...

=== Inline Code Review Comments ===
✅ Comment 123 by cursor[bot] - 1 reply(s)
✅ Comment 456 by coderabbitai[bot] - 1 reply(s)

=== General PR Discussion Comments ===
ℹ️  coderabbitai[bot]: <!-- summary -->...

✅ All inline review comments have been addressed
```

A PR is NOT ready until this script returns ✅.

## Verification Checklist

Before declaring PR comments handled:

- [ ] Ran `bin/pr-comments-filter.sh <PR>` to identify actionable comments
- [ ] **⚠️ CRITICAL**: Extracted "Outside diff range" comments from review bodies (Phase 2b)
- [ ] Ran `bin/pr-comments-out-of-scope.sh <PR>` to find other out-of-scope feedback
- [ ] Code fixes have been made and pushed
- [ ] Each comment thread has a response posted
- [ ] "Outside diff range" comments addressed with a general PR comment
- [ ] **⚠️ POST-PUSH CHECK**: Waited for CI/CD to complete, checked for NEW comments
- [ ] **NO new comments found** after the post-push check (iterate if found)
- [ ] **ALL threads have been resolved** (no unresolved threads remaining)
- [ ] All responses include proper attribution
- [ ] Out-of-scope comments have been either fixed OR have GitHub issues created

**⚠️ DO NOT skip the "Outside diff range" check (Phase 2b) - this is the #2 cause of incomplete PR handling.**

## Reference

For the complete detailed workflow with all edge cases and troubleshooting, see:
`.claude/commands/handle-pr-comments.md`
