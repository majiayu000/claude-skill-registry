---
name: next-github-issue
description: Fetch the oldest open GitHub issue and implement it. Automatically delegates to /feature based on issue scope.
allowed-tools: Task, TodoWrite, TaskOutput, Skill
---

# Next GitHub Issue Skill - Orchestrator

**Orchestrator ONLY spawns Opus subagents and collects summaries. ALL work is delegated.**

## Critical Rules

1. **NEVER run bash commands** - subagents run commands
2. **NEVER read files** - subagents read files
3. Orchestrator only: spawns agents, tracks todos, reports summaries

---

## Phase 1: Fetch Issues Subagent

Spawn a single subagent to fetch and select the oldest issue:

```
Task(general-purpose, model: opus):

Fetch open GitHub issues and select the oldest.

---

## Tasks

1. **Fetch issues**:
   ```bash
   gh issue list --state open --json number,title,createdAt,labels,url --jq 'sort_by(.createdAt)'
   ```

2. **Skip issues with labels**: blocked, wontfix, duplicate

3. **Select the oldest non-blocked issue**

4. **Fetch full issue details**:
   ```bash
   gh issue view <number> --json number,title,body,labels,createdAt,author,comments
   ```

---

## Output Format

```yaml
---
ALL_ISSUES:
  - number: 42
    title: "Add blog section"
    age_days: 14
    labels: [enhancement]
  - number: 15
    title: "Fix animation flicker"
    age_days: 12
    labels: [bug]

SELECTED_ISSUE:
  number: 42
  title: "Add blog section"
  url: "https://github.com/.../issues/42"
  body: "[full issue body]"
  comments: "[any comments]"
  labels: [enhancement]
  created_at: "2025-01-01"
  author: "username"

NO_ISSUES_FOUND: false
---
```
```

**If NO_ISSUES_FOUND: true** → Report to user and exit.

---

## Phase 2: Compose User Story

Based on the selected issue, compose a user story for `/feature`:

```yaml
USER_STORY:
  title: "[derive from issue title]"
  description: |
    ## User Story

    **As a** visitor to wouterwisse.com
    **I want** [derive from issue title]
    **So that** [derive from issue description]

    ## GitHub Issue

    - Issue: #[number]
    - URL: [url]

    ## Description

    [full issue body]

    ## Acceptance Criteria

    [convert issue requirements to checkboxes]
    - [ ] [criterion 1]
    - [ ] [criterion 2]
    - [ ] Closes GitHub issue #[number]

    ## Comments

    [any discussion from issue]
```

---

## Phase 3: Invoke /feature Skill

Invoke the skill directly to implement the user story:

```
Skill(feature)
```

Pass the composed user story as input. The /feature skill will handle the full implementation workflow including:
- Research and planning
- Implementation via /task skill
- Verification and PR creation

**Important:** Ensure the PR body includes "Fixes #[number]" to auto-close the issue.

Wait for /feature to complete, then collect the PR URL from its output.

---

## Phase 4: Link Issue Subagent

After `/feature` completes, spawn subagent to link issue:

```
Task(general-purpose, model: opus):

Link GitHub issue to the created PR.

---

## Context

ISSUE_NUMBER: [number]
PR_URL: [from Phase 3]

---

## Tasks

1. Comment on the issue with PR link:
   ```bash
   gh issue comment <number> --body "Implemented in PR #<pr_number>

   The PR will auto-close this issue when merged."
   ```

---

## Output Format

```yaml
---
ISSUE_LINKED: true | false
COMMENT_ADDED: true | false
---
```
```

---

## Phase 5: Report to User

Summarize all results:

```markdown
## GitHub Issue Implemented

### Issue
- **Issue**: #42 - Add blog section
- **URL**: https://github.com/.../issues/42

### Implementation
Delegated to `/feature` workflow.

### PR Created
- PR: https://github.com/.../pull/123

### Issue Linked
Comment added linking to PR

### Next Steps
1. Review the PR
2. Run `/fix-pr` to address review comments
3. Merge PR → Issue auto-closes
```

---

## Progress Tracking

Use TodoWrite throughout:

```yaml
todos:
  - content: "Fetch issues"
    status: completed
  - content: "Select oldest issue"
    status: completed
  - content: "Compose user story"
    status: completed
  - content: "Delegate to /feature"
    status: in_progress
  - content: "Link issue to PR"
    status: pending
```

---

## Key Principles

1. **Orchestrator is minimal** - only spawns agents, invokes skills, and collects results
2. **Issue fetching is delegated** - subagent runs gh commands
3. **Skill invocation by orchestrator** - only orchestrator can invoke Skill tool
4. **Implementation via /feature** - full workflow delegation
5. **Issue linking is delegated** - subagent posts comment
6. **Auto-close setup** - PR body includes "Fixes #X"
