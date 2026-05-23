---
name: thunderdome
description: AI scrum master for GitHub team collaboration. Use at session start, for status checks, debriefing, or team coordination. Triggers on "thunderdome", "run scrum", "status", "debrief", "session start".
user-invocable: true
argument-hint: "[status|debrief|scores|agents]"
---

# Protocol Thunderdome

> "Two devs enter. One codebase."

AI-powered scrum master for GitHub team collaboration. Provides session management, multi-agent coordination, gamified contribution tracking, and automated status reporting.

## Commands

| Command | Description |
|---------|-------------|
| `/thunderdome` | Full status report |
| `/thunderdome status` | Same as above |
| `/thunderdome debrief` | End-of-session checklist |
| `/thunderdome scores` | Gamification leaderboard |
| `/thunderdome agents` | Multi-agent coordination status |

## Status Report Workflow

When invoked, generate a comprehensive status report:

### 1. Git State

```bash
# Fetch latest
git fetch origin --quiet

# Check uncommitted files
git status --porcelain
```

**Report:**
- CRITICAL: X uncommitted files (list first 5)
- WARNING: X unpushed commits
- OK: Working directory clean
- INFO: Current branch

### 2. GitHub State

```bash
# Recent commits
gh api repos/{owner}/{repo}/commits --jq '.[:5] | .[] | "\(.sha[0:7]) \(.author.login): \(.commit.message | split("\n")[0])"'

# Open PRs
gh api repos/{owner}/{repo}/pulls --jq '.[] | "PR #\(.number): \(.title)"'

# Open issues (excluding PRs)
gh api repos/{owner}/{repo}/issues --jq '.[] | select(.pull_request == null) | "#\(.number) \(.title)"'

# Branches
gh api repos/{owner}/{repo}/branches --jq '.[].name'
```

**Report:**
- X open PRs awaiting review (list them)
- X issues in backlog
- Recent commits by contributor
- Branch inventory

### 3. Test Status

Detect and run project tests:
- `package.json` → `npm test`
- `Makefile` → `make test`
- `swift` project → `swift test`
- `pytest` → `pytest`

**Report:**
- Tests: X passed, Y failed
- CRITICAL if any failures

### 4. Contributor Stats

For each contributor, count:
- Commits today
- Commits this week
- Calculate gamification score

### 5. Summary

End with assessment:
- **ALL CLEAR** - Ready for battle
- **WARNINGS** - List items needing attention
- **CRITICAL** - Blockers that must be resolved

---

## Debrief Protocol

Before ending a session, verify:

### 1. Tests Pass (MANDATORY)

Run full test suite. **DO NOT proceed if tests fail.**

- Fix failures, OR
- Document as known issue in session log

### 2. No Uncommitted Changes

```bash
git status --porcelain | wc -l
```

If changes exist:
```bash
git add -A
git commit -m "Session: <brief description>"
```

### 3. Changes Pushed

```bash
git log origin/main..HEAD --oneline
```

Push any unpushed commits:
```bash
git push origin main
```

### 4. Documentation Current

Check if key docs need updates:
- README.md
- CLAUDE.md (if exists)
- Any docs describing changed behavior

### 5. Issues Synced

- Close completed issues
- Create issues for discovered bugs
- Update labels (in-progress, done)

### 6. Final Checklist

Output verification:
- [ ] All tests passing
- [ ] All changes committed
- [ ] All commits pushed
- [ ] Documentation updated
- [ ] Issues synced

Only report **SAFE TO CLOSE** when all items checked.

---

## Gamification System

Track contributions with competitive scoring:

### Scoring Rules

| Action | Points |
|--------|--------|
| Commit with tests | +50 |
| Small commit (<50 lines) | +10 |
| PR merged | +100 |
| Bug fix | +25 |
| Review submitted | +15 |
| **Breaking CI** | **-100** |
| Untested code dump (>300 lines) | -75 |
| Lazy commit message (<10 chars) | -15 |
| Force push to main | -50 |

### Titles (Score-Based)

| Score | Title |
|-------|-------|
| 0-99 | Keyboard Polisher |
| 100-299 | Bug Whisperer |
| 300-499 | Commit Crusader |
| 500-999 | Merge Master |
| 1000-1999 | Pull Request Paladin |
| 2000-3999 | Refactor Ronin |
| 4000-7499 | Test Titan |
| 7500-14999 | Pipeline Pharaoh |
| 15000+ | Code Demigod |

### Shame Titles

Awarded for consistent bad behavior:
- **Build Breaker** - 3+ CI failures in a week
- **YOLO Developer** - No tests in 5+ consecutive commits
- **Benchwarmer** - Lowest weekly score among active contributors

---

## Multi-Agent Coordination

When multiple Claude Code instances work on the same repo:

### Intent Broadcasting

Before starting work:
1. Check if other agents are registered
2. Declare what you're working on
3. Check for file conflicts

### Safe Parallel Zones

These can be edited simultaneously WITHOUT coordination:
- Different views/components
- Backend vs frontend directories
- Tests vs implementation (different files)
- Separate documentation files

### Conflict Resolution Priority

1. **First registered wins** - Agent who declared first has priority
2. **Critical path wins** - Bug fixes > features > refactoring
3. **Ask the human** - When priority unclear

### Agent Coordination File

If `.thunderdome/agents.json` exists, use it:

```json
{
  "agents": [
    {
      "id": "session-abc123",
      "task": "Implementing feature X",
      "files": ["src/feature.ts", "src/feature.test.ts"],
      "started": "2026-01-28T10:00:00Z"
    }
  ]
}
```

Register your task, check for conflicts, deregister when done.

---

## PR/Code Review Workflow

AI manages code review when asked:

### Creating PRs

```bash
gh pr create --title "Feature: description" --body "## Summary
- Change 1
- Change 2

## Test Plan
- Verified X
- Tested Y"
```

### Reviewing PRs

```bash
# View diff
gh pr diff <number>

# Approve
gh pr review <number> --approve --body "LGTM - tests pass, code clean"

# Request changes
gh pr review <number> --request-changes --body "Please fix: ..."
```

### Review Checklist

- [ ] Code compiles/builds
- [ ] Tests pass
- [ ] No secrets committed
- [ ] Commit messages descriptive
- [ ] Related issue linked
- [ ] No unnecessary changes

### Merging

```bash
# Merge with commit (preserves history)
gh pr merge <number> --merge --delete-branch

# Or squash (cleaner history)
gh pr merge <number> --squash --delete-branch
```

---

## Configuration

Create `.thunderdome/config.json` for project-specific settings:

```json
{
  "contributors": ["username1", "username2"],
  "gamification": true,
  "testCommand": "npm test",
  "criticalFiles": ["src/models/*", "src/services/*"],
  "coordinationEnabled": true
}
```

---

## Philosophy

Thunderdome treats collaborative development as a competitive-cooperative sport:

- **Compete** on contribution quality (tests, atomic commits, clean code)
- **Cooperate** on shared goals (shipping features, maintaining quality)
- **Coordinate** through visibility (everyone sees the same state)

The gamification incentivizes good practices:
- Tests with code (+50) beats untested dumps (-75)
- Small atomic commits (+10) beat monolithic changes
- Passing CI beats breaking the build (-100)

May your commits be atomic and your tests green.
