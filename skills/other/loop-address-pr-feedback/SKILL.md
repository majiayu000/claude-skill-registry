---
name: loop-address-pr-feedback
description: Systematically address AI and human review feedback on PR stacks. Triage issues, fix valid ones, respond to comments, restack, and request re-reviews until all reviewers are satisfied.
---

# Loop: Address PR Feedback

You are a PR author addressing review feedback. **Reviewers give feedback, you fix and respond.**

## Core Concept

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  AI/Human       │────▶│  Claude fixes   │────▶│  Reply & push   │
│  reviews PR     │     │  valid issues   │     │  request re-rev │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                               │
         └─────────────── loop ──────────────────────────┘
```

**The loop:**

1. **Gather** — Collect review comments from all sources
2. **Triage** — Valid → fix, invalid → explain, unclear → ask
3. **Fix** — Make changes, commit, restack dependent PRs
4. **Respond** — Reply with fix SHA or rationale, resolve threads
5. **Summon** — Tag reviewers for re-review
6. **Loop** — Until all threads resolved and approvals obtained

## Relationship to loop-codex-review

| Aspect          | loop-codex-review  | loop-address-pr-feedback |
| --------------- | ------------------ | ------------------------ |
| **When**        | Pre-PR (local)     | Post-PR (remote)         |
| **Reviewer**    | `codex review` CLI | GitHub bots + humans     |
| **Trigger**     | You run it         | Reviews arrive async     |
| **Interface**   | stdout parsing     | GitHub API               |
| **Scope**       | Single diff        | Stack of PRs             |
| **Fixed point** | 3 clean at xhigh   | All threads resolved     |

Same decision procedure, different interface.

## Phase: Initialize

**Detect the PR stack and get full context.**

1. Get stack overview with full context:

   ```bash
   gt log          # Full detail (recommended)
   gt ls           # Short form (just branch names)
   gt log -s       # Current stack only (if multiple stacks)
   ```

   `gt log` shows everything in one shot:
   - PR numbers, titles, and status (Draft, Needs approvals, Approved)
   - Local changes needing submit
   - Commit history per branch
   - Graphite links

2. If not using Graphite, fall back to:

   ```bash
   gh pr list --author "@me" --state open --json number,headRefName,reviewDecision
   ```

3. Determine review order — address base PRs before children (changes propagate down via restack)

**Args:**

```bash
/loop-address-pr-feedback              # All PRs in current stack
/loop-address-pr-feedback --pr 123     # Single PR only
/loop-address-pr-feedback --skip 456   # Skip a PR (e.g., deferred)
```

## Phase: Gather

**Fetch all review feedback for each PR.**

GitHub has three places reviews live:

| Type            | API                      | Use                    |
| --------------- | ------------------------ | ---------------------- |
| Issue comments  | `/issues/{num}/comments` | General PR feedback    |
| Review comments | `/pulls/{num}/comments`  | Line-specific feedback |
| Review threads  | GraphQL `reviewThreads`  | Resolution status      |

```bash
# Issue comments
gh api repos/{owner}/{repo}/issues/{num}/comments \
  --jq '.[] | {id, user: .user.login, body}'

# Review comments
gh api repos/{owner}/{repo}/pulls/{num}/comments \
  --jq '.[] | {id, user: .user.login, path, line, body}'

# Review threads (for resolution status)
gh api graphql -f query='
  query($owner: String!, $repo: String!, $num: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $num) {
        reviewThreads(first: 50) {
          nodes { id isResolved comments(first: 1) { nodes { body } } }
        }
      }
    }
  }' -f owner=OWNER -f repo=REPO -F num=NUM
```

## Phase: Triage

**Categorize each issue before acting.**

| Assessment     | Action                                            |
| -------------- | ------------------------------------------------- |
| Valid bug      | React 👍, fix, commit, reply with SHA, resolve    |
| Valid style    | React 👍, fix, commit, reply with SHA, resolve    |
| False positive | React 👎, reply explaining why, resolve           |
| Outdated       | React 👎, reply noting already addressed, resolve |
| Unclear        | Reply asking for clarification (don't resolve)    |
| Won't fix      | Reply with rationale (may or may not resolve)     |

**Considerations:**

- Verify before fixing — especially AI reviews
- False positives signal unclear code — consider adding comments
- Check if later commits already addressed the issue
- Some "issues" are intentional design tradeoffs

## Phase: Fix

**Spawn agents to fix valid issues.**

```
Task(
  description: "Fix: <issue summary>",
  prompt: "Fix the issue found by code review: ...",
  subagent_type: "general-purpose",
  run_in_background: true
)
```

Group by file or PR. Parallelize independent fixes.

## Phase: Commit

```bash
git add -A && git commit -m "$(cat <<'EOF'
Address review feedback

- Fixed <issue 1>
- Fixed <issue 2>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Phase: Restack

**If you modified a base PR, child PRs need restacking.**

```bash
gt restack
```

Handle conflicts:

- If conflicts occur in skipped/deferred PRs, abort and push what succeeded
- Push each branch individually: `git push origin <branch> --force-with-lease`

## Phase: Respond

**Reply, react, and resolve.**

```bash
# Reply to issue comment
gh api repos/{owner}/{repo}/issues/{num}/comments \
  -X POST -f body="Fixed in {sha}."

# Reply to review thread
gh api graphql -f query='
  mutation($threadId: ID!, $body: String!) {
    addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
      comment { id }
    }
  }' -f threadId="PRRT_..." -f body="Fixed in {sha}."

# React to comment (👍 valid, 👎 invalid)
gh api repos/{owner}/{repo}/pulls/comments/{id}/reactions \
  -X POST -f content="+1"

# Resolve thread
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { isResolved }
    }
  }' -f threadId="PRRT_..."
```

## Phase: Summon

**Request re-review by tagging the reviewer.**

```bash
gh api repos/{owner}/{repo}/issues/{num}/comments \
  -X POST -f body="@{reviewer} Please re-review. Addressed:
- Fixed X
- Fixed Y"
```

Be specific — reviewers should know what to verify.

## Phase: Wait

Reviews arrive asynchronously. Either:

1. **Exit** — Tell user to re-invoke when reviews arrive
2. **Poll** — Check for new comments periodically

```
Addressed all current feedback. Requested re-reviews.
Run /loop-address-pr-feedback again when new reviews arrive.
```

## Fixed Point

**A PR is done when:**

- All review threads resolved
- No pending comments
- Required approvals obtained
- CI passing

**A stack is done when all PRs are done.**

```
┌───────────────────────────────────────────┐
│  STACK COMPLETE                           │
├───────────────────────────────────────────┤
│  PR #1: ✓ resolved, approved              │
│  PR #2: ✓ resolved, approved              │
│  PR #3: ⏸ skipped                         │
├───────────────────────────────────────────┤
│  Ready for merge queue: #1, #2            │
└───────────────────────────────────────────┘
```

## State Tracking

Persist in task descriptions for compaction survival:

```yaml
prs:
  - num: 1
    branch: feature-a
    status: done # addressing | waiting | done | skipped
  - num: 2
    branch: feature-b
    status: addressing
iteration: 1
```

## Anti-patterns

- Fixing before triaging (some issues are false positives)
- Ignoring false positives (they signal unclear code)
- Responding without fixing (empty acknowledgment)
- Pushing without restacking (breaks child PRs)
- Resolving without replying (no audit trail)
- Summoning without summary (reviewer doesn't know what changed)
- Addressing children before parents (causes conflicts)

## Resumption

After compaction:

1. `TaskList` — find tracking task
2. Read task description for state
3. `gt ls` — check stack state
4. Resume from appropriate phase

---

Enter loop-address-pr-feedback mode. Detect PR stack, gather feedback, triage, fix, respond, summon. Address base PRs first.
