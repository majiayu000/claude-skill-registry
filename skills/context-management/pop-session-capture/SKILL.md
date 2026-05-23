---
name: session-capture
description: "Saves complete session state to STATUS.json for seamless continuation across conversations. Captures git context, in-progress tasks, service status, focus area, and next actions. Use at the end of work sessions, before context limits, or when switching to a different task. Do NOT use mid-task or for quick questions - the overhead is only worthwhile when you actually need to resume later."
hooks:
  Stop:
    - script: "${CLAUDE_PLUGIN_ROOT}/../../shared-py/hooks/auto-save-state.py"
      once: true
---

# Session Capture

## Overview

Save current session state to STATUS.json for seamless continuation in future sessions.

**Core principle:** Future Claude should have everything needed to continue without asking.

**Trigger:** End of work session, major milestones, before context limits

## STATUS.json Schema

```json
{
  "lastUpdate": "2025-01-15T10:30:00Z",
  "project": "project-name",
  "sessionType": "Fresh | Resume | Continuation",
  "git": {
    "branch": "feature/current-work",
    "lastCommit": "abc123 - feat: add feature X",
    "uncommittedFiles": 3,
    "stagedFiles": 1
  },
  "tasks": {
    "inProgress": ["Task being worked on"],
    "completed": ["Recently completed task"],
    "blocked": ["Task blocked by X"]
  },
  "services": {
    "devServer": { "running": true, "port": 3000 },
    "database": { "running": true, "port": 5432 }
  },
  "context": {
    "focusArea": "Working on authentication flow",
    "blocker": "Waiting for API response format clarification",
    "nextAction": "Implement token refresh logic",
    "keyDecisions": ["Using JWT for auth", "Session expiry: 1 hour"]
  },
  "projectData": {
    "testStatus": "47 passing, 2 failing",
    "buildStatus": "passing",
    "lintErrors": 0
  }
}
```

## Capture Process

### Step 1: Gather Git State

```bash
# Get current branch
git branch --show-current

# Get last commit
git log -1 --format="%h - %s"

# Count uncommitted changes
git status --porcelain | wc -l

# Get staged files
git diff --cached --name-only | wc -l
```

### Step 2: Gather Task State

From TodoWrite:

- Tasks marked as in_progress
- Recently completed tasks (last 3)
- Any blocked tasks with reasons

### Step 3: Check Services

```bash
# Check if dev server is running
curl -s http://localhost:3000/health || echo "not running"

# Check database
pg_isready -h localhost -p 5432 || echo "not running"
```

### Step 4: Document Context

Capture:

- What area of code you're focused on
- Any blockers or decisions made
- What should happen next
- Key decisions made during session

### Step 5: Run Project Checks

```bash
# Run tests
npm test 2>&1 | tail -1

# Check build
npm run build 2>&1 | tail -1

# Run lint
npm run lint 2>&1 | tail -1
```

### Step 6: Write STATUS.json

Write to `.claude/STATUS.json` (or project root if no .claude directory)

## When to Capture

**Automatic triggers:**

- End of conversation (if hooks enabled)
- Before Claude Code closes
- After major milestone completion

**Manual triggers:**

- Before switching to different work
- When hitting context limits
- Before complex operations

## Example Output

```json
{
  "lastUpdate": "2025-01-15T14:30:00Z",
  "project": "my-app",
  "sessionType": "Resume",
  "git": {
    "branch": "feature/user-auth",
    "lastCommit": "a7f3c2e - feat: add login form component",
    "uncommittedFiles": 2,
    "stagedFiles": 0
  },
  "tasks": {
    "inProgress": ["Implement password reset flow"],
    "completed": ["Create login form", "Add form validation"],
    "blocked": []
  },
  "services": {
    "devServer": { "running": true, "port": 3000 },
    "database": { "running": true, "port": 5432 }
  },
  "context": {
    "focusArea": "Authentication system",
    "blocker": null,
    "nextAction": "Add forgot password email template",
    "keyDecisions": ["Using nodemailer for emails", "Password reset expires in 1 hour"]
  },
  "projectData": {
    "testStatus": "45 passing, 0 failing",
    "buildStatus": "passing",
    "lintErrors": 0
  }
}
```

## Integration

**Pairs with:**

- **session-resume** - Reads STATUS.json on startup
- **context-restore** - Loads previous context into working memory

**Hook integration:**

- Can be triggered by session-end hook
- Runs before Claude Code closes
