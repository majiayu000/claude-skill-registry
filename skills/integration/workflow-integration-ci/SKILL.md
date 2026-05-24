---
name: workflow-integration-ci
description: PR review response workflow - fetch comments, triage, and respond to review feedback (GitHub and GitLab)
user-invocable: false
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# PR Workflow Skill (Provider-Agnostic)

Handles PR review comment workflows - fetching comments, triaging them, and generating appropriate responses. Works with both GitHub and GitLab via the unified `tools-integration-ci` abstraction.

## What This Skill Provides

### Workflows (Absorbs 2 Agents)

1. **Fetch Comments Workflow** - Retrieves PR review comments
   - Uses `tools-integration-ci` abstraction (GitHub or GitLab)
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

1. **Get PR Comments via CI Integration**

   Use the `pr-comments` command from marshal.json (provider-agnostic):

   ```bash
   # Resolve command from config
   COMMAND=$(jq -r '.ci.commands["pr-comments"]' .plan/marshal.json)
   eval "$COMMAND --pr-number {number} [--unresolved-only]"
   ```

   Or use the workflow script for additional processing:

   ```bash
   python3 .plan/execute-script.py pm-workflow:workflow-integration-ci:pr fetch-comments [--pr {number}]
   ```

   Output (TOON format):
   ```toon
   status: success
   operation: pr_comments
   provider: github|gitlab
   pr_number: 123
   total: N
   unresolved: N

   comments[N]{id,author,body,path,line,resolved,created_at}:
   c1	alice	Fix security issue	src/Auth.java	42	false	2025-01-15T10:30:00Z
   ```

2. **Return Comment List**

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

   Script: `pm-workflow:workflow-integration-ci`

   ```bash
   python3 .plan/execute-script.py pm-workflow:workflow-integration-ci:pr triage --comment '{json}'
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

Script: `pm-workflow:workflow-integration-ci` → `pr.py`

### pr.py fetch-comments

**Purpose:** Fetch PR review comments from GitHub.

**Usage:**
```bash
python3 .plan/execute-script.py pm-workflow:workflow-integration-ci:pr fetch-comments [--pr <number>]
```

**Requirements:** gh CLI installed and authenticated

**Output:** JSON with comments array

### pr.py triage

**Purpose:** Analyze a single comment and determine action.

**Usage:**
```bash
python3 .plan/execute-script.py pm-workflow:workflow-integration-ci:pr triage --comment '{"id":"...", "body":"...", ...}'
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
- [x] Scripts output TOON/JSON for machine processing
- [x] Both fetcher and triager agents absorbed
- [x] Clear workflow definitions
- [x] Provider-agnostic via tools-integration-ci

## References

- tools-integration-ci: `plan-marshall:tools-integration-ci` skill
- GitHub CLI: https://cli.github.com/
- GitLab CLI: https://gitlab.com/gitlab-org/cli
- Code Review Best Practices: https://google.github.io/eng-practices/review/
