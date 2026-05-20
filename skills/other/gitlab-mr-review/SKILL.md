---
name: Gitlab MR Review
description: Gitlab MR Review
category: general
---

---
name: gitlab-mr-review
description: Use when asked to review a GitLab merge request URL - efficiently checks out code with wtm, gathers context from GitLab and Asana, and performs deep code review using the requesting-code-review skill
---

# GitLab Merge Request Review

## Overview

Efficient workflow for reviewing GitLab merge requests: extract MR number, gather context in parallel (glab + Asana if linked), checkout code with wtm, and perform deep review using code-review skill.

## When to Use

- User provides a GitLab MR URL like `https://gitlab.com/org/repo/-/merge_requests/1234`
- User asks to "review MR 1234" for tracktile project
- Need to understand and review code changes with full context

## Workflow

### Step 1: Extract MR Number

```bash
# From URL: https://gitlab.com/sharokenstudio/tracktile/tracktile/-/merge_requests/3386
# MR number is: 3386
```

### Step 2: Get MR Metadata First

```bash
cd ~/tracktile/prerelease && glab mr view 3386
```

**Extract from output:**
- Source branch name (e.g., `feature/new-auth-flow`)
- MR title and description
- Check description for Asana links (e.g., `https://app.asana.com/0/1234567890/9876543210`)

### Step 3: Checkout Code & Get Asana Context (PARALLEL)

**CRITICAL: Run these in parallel in a SINGLE message with multiple tool calls:**

**Parallel Task 1 - Checkout or update branch:**

**Check if worktree already exists:**
```bash
if [ -d ~/tracktile/feature/new-auth-flow ]; then
  cd ~/tracktile/feature/new-auth-flow && git pull
else
  cd ~/tracktile && wtm checkout feature/new-auth-flow
fi
```

**Logic:**
- If worktree exists: `cd` into it and `git pull` to update
- If worktree doesn't exist: Use `wtm checkout BRANCH_NAME` to create it

**Exact wtm command syntax:**
- ✅ CORRECT: `wtm checkout BRANCH_NAME`
- ❌ WRONG: `wtm BRANCH_NAME`
- ❌ WRONG: `wtm add BRANCH_NAME`
- ❌ WRONG: `wtm list`

**What wtm does (when creating new worktree):**
- Creates worktree at `~/tracktile/BRANCH_NAME/`
- Auto-installs node_modules (via post_create hook)
- Auto-sets up .env files (via post_create hook)
- Example path: `~/tracktile/feature/new-auth-flow/`

**Parallel Task 2 - Get Asana context (if link found in Step 2):**

While wtm runs, use Asana MCP in parallel:
- Extract task ID from URL `https://app.asana.com/0/1234567890/9876543210` → `9876543210`
- Call `mcp__asana__asana_get_task` with `task_id: "9876543210"`
- Get requirements, acceptance criteria, context

**Wait for both tasks to complete** before proceeding to Step 4.

### Step 4: Switch to Worktree Directory

```bash
cd ~/tracktile/feature/new-auth-flow/
```

**Critical:**
- Path format is `~/tracktile/BRANCH_NAME/` (note the trailing slash)
- Example: if branch is `feature/new-auth-flow`, path is `~/tracktile/feature/new-auth-flow/`
- You MUST cd into this directory before code review

### Step 5: Deep Code Review

**MANDATORY:** Invoke `superpowers:requesting-code-review` skill using Skill tool.

**Pass this context to the skill:**
- MR description and intent from glab
- Asana task requirements (if applicable)
- Discussion comments from glab

**Do NOT:**
- Create manual review checklist
- Run additional git commands (`git diff`, `git log`) - skill handles this
- Read files manually - skill does this
- Invoke wrong skill names like `code-review` or `superpowers:code-reviewer`

**The requesting-code-review skill handles:**
- Finding and reading all changed files
- Code quality analysis
- Security review
- Test coverage
- Architecture patterns
- Performance concerns

## Quick Reference

| Step | Command | Purpose |
| ---- | ------- | ------- |
| 1 | Extract MR number from URL | Get "3386" |
| 2a | `glab mr view 3386` | Get metadata + branch name + check for Asana |
| 2b | `wtm checkout BRANCH` | Setup worktree (auto-installs deps) |
| 2c | Get Asana task (if linked) | Get requirements context |
| 3 | `cd ~/tracktile/BRANCH` | Switch to worktree |
| 4 | Invoke code-review skill | Deep review with context |

## Common Mistakes

❌ **Running commands sequentially**
- Don't wait for glab to finish before starting wtm
- Start gathering context while wtm installs deps

❌ **Not checking if worktree already exists**
- Always check if `~/tracktile/BRANCH_NAME/` exists
- If exists: `cd` into it and `git pull` to update
- If doesn't exist: Use `wtm checkout BRANCH_NAME`

❌ **Forgetting to switch to worktree directory**
- After `wtm checkout feature-branch`, you MUST `cd ~/tracktile/feature-branch/`
- Code review must happen in the worktree, not main directory

❌ **Skipping Asana context**
- Always check MR description for Asana links
- Requirements and acceptance criteria live in Asana
- Missing this means reviewing code without knowing what it should do

❌ **Manual review instead of using code-review skill**
- Don't create your own checklist
- The code-review skill has comprehensive methodology
- Use it with all the context you gathered

❌ **Using wrong repository path**
- Commands assume `~/tracktile` for tracktile project (bare repo setup)
- Worktrees are at `~/tracktile/BRANCH_NAME/`

## Example: Complete Flow

```
User: "Review this MR: https://gitlab.com/sharokenstudio/tracktile/tracktile/-/merge_requests/3386"

You:
1. Extract MR number: 3386
2. Run in parallel:
   - glab mr view 3386 → Get branch name "feature/new-auth" + check description
   - Found Asana link in description → Get task context
   - wtm checkout feature/new-auth → Setup worktree
3. cd ~/tracktile/feature/new-auth
4. Use code-review skill with context:
   - MR intent: "Implements new auth flow"
   - Asana requirements: [acceptance criteria from task]
   - Discussion: [any comments from glab]
```

## Real-World Impact

- Parallel execution saves 2-3 minutes per review
- Asana context prevents missing requirements
- wtm auto-setup eliminates manual dependency installation
- code-review skill ensures consistent, thorough reviews
