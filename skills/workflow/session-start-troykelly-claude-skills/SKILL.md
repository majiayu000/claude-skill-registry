---
name: session-start
description: Use at the beginning of every work session - establishes context by checking GitHub project state, reading memory, verifying environment, and orienting before starting work
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - mcp__github__*
  - mcp__memory__*
model: opus
---

# Session Start

## Overview

Get your bearings before doing any work. Every session starts here.

**Core principle:** Understand the current state before taking action.

**Announce at start:** "I'm using session-start to get oriented before beginning work."

## The Protocol

Execute these steps in order at the start of every session:

### Step 1: Environment Check

Verify required tools and environment variables are available.

```bash
# Check GitHub CLI authentication
gh auth status

# Check git is available
git --version

# Verify GITHUB_PROJECT is set
echo $GITHUB_PROJECT
```

**If any check fails:** Report to user before proceeding.

**Skill:** `environment-bootstrap`

---

### Step 1.5: Development Services

Check for available development services (docker-compose).

```bash
# Detect compose services
if [ -f "docker-compose.yml" ] || [ -f ".devcontainer/docker-compose.yml" ]; then
    docker-compose config --services
    docker-compose ps
fi
```

**Key questions:**
- What services are available (postgres, redis, etc.)?
- Which are currently running?
- Do any need to be started for this work?

**If services are available but not running:**
```bash
# Start all services
docker-compose up -d

# Or start specific service
docker-compose up -d postgres
```

**Skill:** `local-service-testing`

---

### Step 2: Repository State

Understand the current state of the repository.

```bash
# Current branch
git branch --show-current

# Working directory status
git status

# Recent commits
git log --oneline -5

# Any stashed changes?
git stash list
```

**Key questions:**
- Am I on a feature branch or main?
- Are there uncommitted changes?
- Is there work in progress?

---

### Step 3: GitHub Project State (Source of Truth)

Check the current state of work via the **GitHub Project Board** (the source of truth).

**CRITICAL: Use `github-api-cache` to minimize API calls.**

```bash
# === CACHE INITIALIZATION (3 API calls total) ===
# This replaces 20+ individual API calls

echo "Initializing GitHub API cache..."

# CALL 1: Cache all project fields
export GH_CACHE_FIELDS=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)

# CALL 2: Cache all project items
export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)

# CALL 3: Get project ID
export GH_PROJECT_ID=$(gh project list --owner "$GH_PROJECT_OWNER" --format json --limit 100 | \
  jq -r ".projects[] | select(.number == $GITHUB_PROJECT_NUM) | .id")

# Extract field IDs from cache (NO API CALLS)
export GH_STATUS_FIELD_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .id')
export GH_STATUS_IN_PROGRESS_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "In Progress") | .id')
export GH_STATUS_DONE_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Done") | .id')

echo "Cached $(echo "$GH_CACHE_ITEMS" | jq '.items | length') project items"
```

**Query from cache (NO API CALLS):**

```bash
# Get all project items with their status (from cache)
echo "$GH_CACHE_ITEMS" | jq '.items[] | {number: .content.number, title: .content.title, status: .status.name}'

# Get Ready issues (from cache)
echo "$GH_CACHE_ITEMS" | jq -r '.items[] | select(.status.name == "Ready") | .content.number'

# Get In Progress issues (from cache)
echo "$GH_CACHE_ITEMS" | jq -r '.items[] | select(.status.name == "In Progress") | .content.number'

# Get Blocked issues (from cache)
echo "$GH_CACHE_ITEMS" | jq -r '.items[] | select(.status.name == "Blocked") | .content.number'
```

**Key questions:**
- What issues have Status = "In Progress"?
- What issues have Status = "Ready" (pending work)?
- Are there any Status = "Blocked" items?
- What's the highest priority Ready item?

**Skill:** `github-api-cache`

---

### Step 3.5: Project Board Sync Verification

**MANDATORY:** Verify project board state matches actual work state.

**Uses cached data from Step 3 - NO additional API calls for project queries.**

```bash
# Check for sync issues between project board and reality
# ALL project queries use GH_CACHE_ITEMS (cached in Step 3)

echo "## Project Board Sync Check"
echo ""

# 1. Issues marked "In Progress" should have active branches (0 API calls)
echo "### Checking: In Progress issues have branches"
for issue in $(echo "$GH_CACHE_ITEMS" | jq -r '.items[] | select(.status.name == "In Progress") | .content.number'); do
  branch=$(git branch -r 2>/dev/null | grep -E "feature/$issue-" | head -1)
  if [ -z "$branch" ]; then
    echo "⚠️ Issue #$issue is 'In Progress' but has no branch"
  fi
done

# 2. Active branches should have issues marked "In Progress" (0 API calls)
echo ""
echo "### Checking: Active branches have In Progress issues"
for branch in $(git branch -r 2>/dev/null | grep -E 'origin/feature/[0-9]+' | sed 's/.*feature\///' | cut -d- -f1 | sort -u); do
  status=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $branch) | .status.name")

  if [ "$status" != "In Progress" ] && [ "$status" != "In Review" ]; then
    echo "⚠️ Branch for #$branch exists but project Status='$status' (expected: In Progress or In Review)"
  fi
done

# 3. Open PRs should have issues marked "In Review" (1 API call for PR list - REST API)
echo ""
echo "### Checking: Open PRs have In Review issues"
for pr in $(gh pr list --json number,body --jq '.[] | select(.body | contains("Closes #")) | .body' 2>/dev/null | grep -oE 'Closes #[0-9]+' | grep -oE '[0-9]+'); do
  # Use cached items, not API call
  status=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $pr) | .status.name")

  if [ "$status" != "In Review" ]; then
    echo "⚠️ Issue #$pr has open PR but project Status='$status' (expected: In Review)"
  fi
done

echo ""
echo "Sync check complete."
```

**If sync issues found:**

1. Report discrepancies to user before proceeding
2. Fix critical discrepancies (In Progress with no branch = stale state)
3. Document any unresolved sync issues

**Skill:** `project-board-enforcement`

---

### Step 3.6: Active Orchestration Detection

**CRITICAL:** Check if autonomous orchestration was running and needs to resume.

```bash
# Check MCP Memory for active orchestration marker
ACTIVE_ORCH=$(mcp__memory__open_nodes({"names": ["ActiveOrchestration"]}))
```

**If ActiveOrchestration entity exists:**

```markdown
## ⚠️ ACTIVE ORCHESTRATION DETECTED

**Status:** [from entity]
**Scope:** [from entity]
**Tracking Issue:** #[from entity]
**Last Loop:** [from entity]
**Repository:** [from entity]

### Action Required

Context was compacted mid-orchestration. Resuming now.

1. Verify tracking issue still exists
2. Resume orchestration via `autonomous-orchestration` skill
3. Continue from current phase (BOOTSTRAP or MAIN_LOOP)
```

**Resume orchestration immediately** - do not wait for user input. The original request for autonomous operation is still the active consent.

**If no ActiveOrchestration entity:** Continue to Step 4.

---

### Step 4: Memory Recall

Search for relevant context from previous sessions.

**Episodic Memory:**
- Search for current issue number
- Search for feature/project name
- Search for recent work in this repository

**Knowledge Graph (mcp__memory):**
- Check for entities related to this project
- Look for documented decisions or patterns

**Skill:** `memory-integration`

---

### Step 5: Active Work Detection

Determine if there's work in progress to resume.

**Indicators of active work:**
- Branch is not main
- Uncommitted changes exist
- Issue marked "In Progress" in project
- Previous session notes reference ongoing work

**If active work detected:**
1. Read the associated issue
2. Check last commit message for context
3. Review any verification reports
4. Determine current step in `issue-driven-development` process

---

### Step 6: Environment Bootstrap

If starting fresh or environment needs setup:

```bash
# Run init script if it exists
if [ -f scripts/init.sh ]; then
    ./scripts/init.sh
fi

# Or common alternatives
pnpm install --frozen-lockfile  # Node projects
pip install                     # Python projects
```

**Verify basic functionality works before starting new work.**

**Skill:** `environment-bootstrap`

---

### Step 7: Orient and Report

Summarize current state to user:

```markdown
## Session State

**Repository:** [owner/repo]
**Branch:** [current branch]
**Working Directory:** [clean/dirty]

**Active Work:**
- Issue: #[number] - [title]
- Status: [project status]
- Progress: [what's been done]

**Environment:**
- [tool versions]
- [any issues detected]

**Development Services:**
- postgres: [running/stopped] @ localhost:5432
- redis: [running/stopped] @ localhost:6379
- [other services from docker-compose]

**Ready to:** [resume work on X / start new issue / await instructions]
```

---

## Decision Tree

```
Start Session
     │
     ▼
┌─────────────────┐
│ Environment OK? │──No──► Report issues, await fix
└────────┬────────┘
         │ Yes
         ▼
┌─────────────────┐
│ On main branch? │──Yes──► Ready for new work
└────────┬────────┘
         │ No
         ▼
┌─────────────────┐
│ Uncommitted     │──Yes──► Resume in-progress work
│ changes exist?  │
└────────┬────────┘
         │ No
         ▼
┌─────────────────┐
│ Issue marked    │──Yes──► Resume in-progress work
│ In Progress?    │
└────────┬────────┘
         │ No
         ▼
Ready for new work
```

## Resuming In-Progress Work

If resuming work from a previous session:

1. **Read the issue** - Full description and all comments
2. **Check last commit** - What was the last completed step?
3. **Run tests** - Is the codebase in a working state?
4. **Review verification** - What criteria are already met?
5. **Determine next step** - Map to `issue-driven-development` steps

Then continue from the appropriate step in `issue-driven-development`.

## Starting New Work

If no work in progress:

1. Check GitHub Project for highest priority "Ready" item
2. Or await user instructions for which issue to work on
3. Begin `issue-driven-development` from Step 1

## Common Issues

| Issue | Resolution |
|-------|------------|
| GITHUB_PROJECT not set | Ask user for project URL |
| Not authenticated to gh | Run `gh auth login` |
| Dirty working directory on main | Stash or discard before proceeding |
| Issue "In Progress" but branch deleted | Reset issue status, start fresh |

## Checklist

Before proceeding to work:

- [ ] Environment verified (gh, git, env vars)
- [ ] **GITHUB_PROJECT_NUM and GH_PROJECT_OWNER set**
- [ ] **GitHub API cache initialized (GH_CACHE_ITEMS, GH_CACHE_FIELDS set)**
- [ ] Development services detected and status reported
- [ ] Repository state understood
- [ ] **GitHub Project state checked (via cached data, not repeated API calls)**
- [ ] **Project board sync verified (Step 3.5) using cached data**
- [ ] **Sync discrepancies reported/fixed**
- [ ] **Active orchestration checked (Step 3.6)** - Resume if found
- [ ] Memory searched for context
- [ ] Active work detected or new work identified
- [ ] Environment bootstrapped if needed
- [ ] Required services started (if applicable)
- [ ] State reported to user

**Skills:** `github-api-cache`, `project-board-enforcement`

## Integration

After session-start completes, proceed to either:

- **Resume:** Continue from current step in `issue-driven-development`
- **New work:** Begin `issue-driven-development` from Step 1

Always operate under `autonomous-operation` mode.
