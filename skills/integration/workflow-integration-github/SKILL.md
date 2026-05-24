---
name: workflow-integration-github
description: PR review response workflow - fetch comments, triage, and respond to review feedback
allowed-tools: Read, Edit, Write, Bash(gh:*), Grep, Glob
---

# PR Workflow Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

Handles PR review comment workflows - fetching comments, triaging them, and generating appropriate responses.

## What This Skill Provides

### Workflows (Absorbs 2 Agents)

1. **Fetch Comments Workflow** - Retrieves PR review comments
   - Uses gh CLI to fetch structured comment data
   - Replaces: review-comment-fetcher agent

2. **Handle Review Workflow** - Processes and responds to comments
   - Triages each comment for appropriate action
   - Implements code changes or generates explanations
   - Replaces: review-comment-triager agent

## When to Activate This Skill

- Responding to PR review comments
- Processing review feedback
- Implementing reviewer-requested changes
- Generating explanations for reviewers

## Workflows

### Workflow 1: Fetch Comments

**Purpose:** Fetch all review comments for a PR.

**Input:** PR number (optional, defaults to current branch's PR)

**Steps:**

1. **Determine PR Number**
   ```bash
   gh pr view --json number --jq '.number'
   ```

2. **Fetch Comments**

   Script: `pm-workflow:workflow-integration-github`

   ```bash
   python3 .plan/execute-script.py pm-workflow:workflow-integration-github:pr fetch-comments [--pr {number}]
   ```

   Script outputs JSON:
   ```json
   {
     "pr_number": 123,
     "comments": [
       {
         "id": "...",
         "author": "...",
         "body": "...",
         "path": "...",
         "line": N,
         "resolved": false
       }
     ],
     "total_comments": N,
     "unresolved_count": N
   }
   ```

3. **Return Comment List**

**Output:** Structured list of comments for triage

---

### Workflow 2: Handle Review

**Purpose:** Process review comments and respond appropriately.

**Input:** PR number or comment list from Fetch workflow

**Steps:**

1. **Get Comments**
   If not provided, use Fetch Comments workflow first.

2. **Triage Each Comment**
   For each unresolved comment:

   Script: `pm-workflow:workflow-integration-github`

   ```bash
   python3 .plan/execute-script.py pm-workflow:workflow-integration-github:pr triage --comment '{json}'
   ```

   Script outputs decision:
   ```json
   {
     "comment_id": "...",
     "action": "code_change|explain|ignore",
     "reason": "...",
     "priority": "high|medium|low|none",
     "suggested_implementation": "..."
   }
   ```

3. **Process by Action Type**

   **For code_change:**
   - Read file at comment location
   - Implement suggested change using Edit tool
   - Reply to comment with commit reference

   **For explain:**
   - Generate explanation based on code context
   - Reply to comment using gh CLI:
     ```bash
     gh pr comment {pr} --body "..."
     ```

   **For ignore:**
   - No action required
   - Log as skipped

4. **Group by Priority**
   - Process high priority first
   - Then medium, then low

5. **Return Summary**

**Output:**
```json
{
  "pr_number": 123,
  "processed": {
    "code_changes": 3,
    "explanations": 1,
    "ignored": 1
  },
  "files_modified": ["..."],
  "status": "success"
}
```

---

## Scripts

Script: `pm-workflow:workflow-integration-github` → `pr.py`

### pr.py fetch-comments

**Purpose:** Fetch PR review comments from GitHub.

**Usage:**
```bash
python3 .plan/execute-script.py pm-workflow:workflow-integration-github:pr fetch-comments [--pr <number>]
```

**Requirements:** gh CLI installed and authenticated

**Output:** JSON with comments array

### pr.py triage

**Purpose:** Analyze a single comment and determine action.

**Usage:**
```bash
python3 .plan/execute-script.py pm-workflow:workflow-integration-github:pr triage --comment '{"id":"...", "body":"...", ...}'
```

**Output:** JSON with action decision

## References (Load On-Demand)

### Review Response Guide
```
Read references/review-response-guide.md
```

Provides:
- Comment classification patterns
- Response templates
- Best practices for reviewer communication

## Comment Classification

| Pattern | Action | Priority |
|---------|--------|----------|
| security, vulnerability, injection | code_change | high |
| bug, error, fix, broken | code_change | high |
| please add/remove/change | code_change | medium |
| rename, variable name, typo | code_change | low |
| why, explain, reasoning, ? | explain | low |
| lgtm, approved, looks good | ignore | none |

## Integration

### Commands Using This Skill
- **/pr-handle-pull-request** - Full PR workflow
- **/pr-respond-to-review-comments** - Comment response

### Related Skills
- **sonar-workflow** - Often used together in PR workflows
- **git-workflow** - Commits changes after responses

## Quality Verification

- [x] Self-contained with relative path pattern
- [x] Progressive disclosure (references loaded on-demand)
- [x] Scripts output JSON for machine processing
- [x] Both fetcher and triager agents absorbed
- [x] Clear workflow definitions
- [x] gh CLI integration documented

## References

- GitHub CLI: https://cli.github.com/
- Code Review Best Practices: https://google.github.io/eng-practices/review/
