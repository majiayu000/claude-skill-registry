---
name: morning
description: "Start-of-day setup and readiness routine. Calculates Ready to Code Score (0-100) based on session restoration, service health, dependency updates, branch sync, PR reviews, and issue triage. Automatically captures session state to STATUS.json. Use at start of work day after opening Claude Code."
---

# Morning Routine

## Overview

Automated start-of-day setup that ensures optimal development environment before starting work.

**Core principle:** Validate readiness to code and restore previous session context with zero manual overhead.

**Trigger:** Start of work day, after opening Claude Code

**Duration:** ~15-20 seconds (vs. ~90 seconds manual)

## Ready to Code Score (0-100)

Comprehensive readiness check across 6 dimensions:

| Check                | Points | Criteria                                           |
| -------------------- | ------ | -------------------------------------------------- |
| Session Restored     | 20     | Previous session context restored from STATUS.json |
| Services Healthy     | 20     | All required dev services running                  |
| Dependencies Updated | 15     | Package dependencies up to date                    |
| Branches Synced      | 15     | Local branch synced with remote                    |
| PRs Reviewed         | 15     | No PRs waiting for review                          |
| Issues Triaged       | 15     | All issues assigned/prioritized                    |

**Branch Protection Penalty (Issue #142):**

If on protected branch (`main`, `master`, `develop`, `production`) with uncommitted changes:

- **Penalty:** -10 points from Branches Synced score
- **Indicator:** Show ⚠️ PROTECTED warning in Current State table
- **Recommendation:** Create feature branch before starting work

**Score Interpretation:**

- **90-100**: Excellent - Fully ready to code
- **80-89**: Very Good - Almost ready, minor setup
- **70-79**: Good - Ready with minor issues
- **60-69**: Fair - 10-15 minutes setup needed
- **50-59**: Poor - Significant setup required
- **0-49**: Not Ready - Focus on environment setup

## Workflow Steps

### 1. Restore Previous Session

Load context from STATUS.json:

```python
from pathlib import Path
import json

status_file = Path('STATUS.json')
if status_file.exists():
    status = json.loads(status_file.read_text())

    # Extract session context
    last_nightly = status.get('last_nightly_routine', {})
    git_status = status.get('git_status', {})

    session_data = {
        'restored': True,
        'last_nightly_score': last_nightly.get('sleep_score'),
        'last_work_summary': git_status.get('action_required'),
        'previous_branch': git_status.get('current_branch'),
        'stashed_count': git_status.get('stashes', 0)
    }
```

**Restored Context Includes:**

- Last nightly routine Sleep Score
- Previous work summary
- Git branch and uncommitted work
- Stashed changes count

### 2. Check Dev Environment

Using `capture_state.py` utility with morning-specific checks:

```python
from popkit_shared.utils.capture_state import capture_project_state

state = capture_project_state()
# Returns: {
#   'git': {...},
#   'github': {...},
#   'services': {...}
# }
```

**Git Analysis:**

- Current branch
- Commits behind remote (after git fetch)
- Uncommitted files
- Stashed changes

**GitHub Analysis:**

- PRs needing review (no review decision or changes requested)
- Issues needing triage (no assignee or labels)
- Latest CI status

**Service Analysis:**

- Running dev services (node, npm, pnpm, redis, postgres, supabase)
- Required services vs. running services

**Dependency Analysis:**

- Outdated package count
- Major/minor updates available

### 3. Calculate Ready to Code Score

Using `ready_to_code_score.py` module:

```python
from pop_morning.scripts.ready_to_code_score import calculate_ready_to_code_score

score, breakdown = calculate_ready_to_code_score(state)
# score: 0-100
# breakdown: {
#   'session_restored': {'points': 20, 'max': 20, 'reason': '...'},
#   'services_healthy': {'points': 10, 'max': 20, 'reason': '...'},
#   ...
# }
```

### 4. Generate Morning Report

Using `morning_report_generator.py` module:

```python
from pop_morning.scripts.morning_report_generator import generate_morning_report

report = generate_morning_report(score, breakdown, state)
# Returns formatted markdown report with:
# - Ready to Code Score headline
# - Score breakdown table
# - Service status (if not all running)
# - Setup recommendations
# - Today's focus items
```

### 5. Capture Session State

Update STATUS.json with morning routine data:

```python
# This happens automatically via direct STATUS.json update
# Updates STATUS.json with:
# - Morning routine execution timestamp
# - Ready to Code score
# - Session restoration status
# - Dev environment state
# - Recommendations
```

### 6. Present Report to User

Display morning report with:

- **Ready to Code Score** (0-100) with visual indicator
- **Score Breakdown** - What contributed to the score
- **Setup Issues** - Services down, sync needed, outdated deps
- **Recommendations** - Actions before coding
- **Today's Focus** - PRs to review, issues to triage

## Data Collection Commands

### Git Commands (Consolidated)

Single command to gather all git data:

```bash
{
  git fetch --quiet
  echo "=== BRANCH ==="
  git rev-parse --abbrev-ref HEAD
  echo "=== BEHIND ==="
  git rev-list --count HEAD..origin/$(git rev-parse --abbrev-ref HEAD)
  echo "=== STATUS ==="
  git status --porcelain
  echo "=== STASHES ==="
  git stash list | wc -l
}
```

**Branch Protection Detection (Issue #142):**

After collecting branch name, check if it's a protected branch:

```python
from popkit_shared.utils.session_recorder import is_recording_enabled, record_reasoning

# Get current branch
current_branch = git_output['branch']

# Protected branches
PROTECTED_BRANCHES = ["main", "master", "develop", "production"]
is_protected = current_branch in PROTECTED_BRANCHES

# Record if on protected branch
if is_recording_enabled():
    record_reasoning(
        step="Check branch protection",
        reasoning=f"Branch '{current_branch}' is {'PROTECTED' if is_protected else 'not protected'}",
        data={
            "current_branch": current_branch,
            "is_protected": is_protected
        }
    )
```

### GitHub Commands (Consolidated)

```bash
{
  gh pr list --state open --json number,title,reviewDecision
  echo "---SEPARATOR---"
  gh issue list --state open --json number,title,assignees,labels
} > /tmp/gh_morning_data.json
```

### Service Check (Consolidated)

```bash
{
  ps aux | grep -E "(node|npm|pnpm|redis|postgres|supabase)" | grep -v grep
  echo "---SEPARATOR---"
  pnpm outdated --json 2>/dev/null || echo "{}"
} > /tmp/service_morning_data.txt
```

## Integration with Existing Utilities

### capture_state.py

Located: `packages/shared-py/popkit_shared/utils/capture_state.py`

```python
def capture_project_state() -> dict:
    """Capture complete project state for morning routine."""
    return {
        'git': capture_git_state(),
        'github': capture_github_state(),
        'services': capture_service_state(),
        'timestamp': datetime.now().isoformat()
    }
```

### routine_measurement.py

Located: `packages/shared-py/popkit_shared/utils/routine_measurement.py`

When invoked with `--measure` flag:

- Tracks tool call count
- Measures duration
- Calculates token usage
- Saves to `.claude/popkit/measurements/morning-<timestamp>.json`

### routine_cache.py

Located: `packages/shared-py/popkit_shared/utils/routine_cache.py`

Caching strategy:

- **Never cache**: Git status (changes frequently)
- **Cache 5 min**: Service status, dependency checks
- **Cache 15 min**: GitHub PR/issue data

## Output Format

```markdown
# ☀️ Morning Routine Report

**Date**: 2025-12-28 09:30
**Ready to Code Score**: 75/100 👍
**Grade**: B - Good - Ready with minor issues

## Score Breakdown

| Check                | Points | Status                               |
| -------------------- | ------ | ------------------------------------ |
| Session Restored     | 20/20  | ✅ Previous session context restored |
| Services Healthy     | 10/20  | ⚠️ Missing: redis                    |
| Dependencies Updated | 15/15  | ✅ All dependencies up to date       |
| Branches Synced      | 10/15  | ⚠️ 3 commits behind remote           |
| PRs Reviewed         | 15/15  | ✅ No PRs pending review             |
| Issues Triaged       | 10/15  | ⚠️ 2 issues need triage              |

## 🔧 Dev Services Status

**Required**: 2 services
**Running**: 1 services

**Not Running:**

- redis

## 🔄 Branch Sync Status

**Current Branch**: fix/critical-build-blockers
**Commits Behind Remote**: 3

Run `git pull` to sync with remote.

## 📋 Recommendations

**Before Starting Work:**

- Start dev services: redis
- Sync with remote: git pull (behind by 3 commits)

**Today's Focus:**

- Triage 2 open issues
- Review overnight commits and CI results
- Continue: Fix critical build blockers

---

STATUS.json updated ✅
Morning session initialized. Ready to code!

## 🎯 Next Actions (The PopKit Way)

**CRITICAL**: Always end with AskUserQuestion to keep PopKit in control.

Use AskUserQuestion tool with context-aware options based on morning report:

**Option 1: If services are down or sync needed (Score < 80)**
```

What would you like to do next?
├─ Fix environment issues (Recommended)
│ └─ Start redis, pull 3 commits, etc.
├─ Start work anyway (skip setup)
├─ Review what changed overnight
└─ Other

```

**Option 2: If environment is healthy (Score >= 80)**
```

Ready to code! What's your focus today?
├─ Work on highest priority issue
├─ Review open PRs (X pending)
├─ Continue yesterday's work: [last task]
└─ Other

```

**Option 3: If issues need triage**
```

You have X issues needing attention. What would you like to do?
├─ Triage issues now (Recommended)
├─ Review issue #Y (highest priority)
├─ Skip triage, start coding
└─ Other

````

### Implementation

After generating the morning report, invoke AskUserQuestion based on score and context:

```python
# After generating report
questions = generate_next_action_questions(score, breakdown, state)
# Returns AskUserQuestion tool invocation

# Example output to Claude:
{
    "type": "ask_user_question",
    "questions": [{
        "question": "What would you like to do next?",
        "header": "Next Action",
        "multiSelect": false,
        "options": [
            {
                "label": "Fix environment issues (Recommended)",
                "description": "Start redis, sync with remote (3 commits behind)"
            },
            {
                "label": "Work on #42: Fix critical build blockers",
                "description": "Continue yesterday's work (highest priority)"
            },
            {
                "label": "Review open PRs",
                "description": "2 PRs waiting for review"
            }
        ]
    }]
}
````

**Why This Matters (The PopKit Way):**

- ✅ Keeps PopKit in control of the workflow
- ✅ Forces intentional user decisions
- ✅ Enables context-aware next actions
- ✅ Prevents "report dump and done" anti-pattern
- ✅ Maintains continuous workflow loop

**Never just show a report and end the session!**

````

## Error Handling

### Git Not Available

```python
try:
    git_state = capture_git_state()
except GitNotFoundError:
    print("[WARN] Git not available - skipping git checks")
    # Continue with partial score
````

### GitHub CLI Not Available

```python
try:
    github_state = capture_github_state()
except GhNotFoundError:
    print("[WARN] GitHub CLI not available - skipping GitHub checks")
    # Continue with partial score
```

### Service Check Failures

```python
# Service checks are best-effort
# If they fail, provide recommendations but don't block
```

### Session Restore Failures

```python
try:
    session_data = restore_session()
except Exception:
    print("[WARN] Could not restore session - starting fresh")
    session_data = {'restored': False}
```

## Optimization Features

### Tool Call Reduction

- **Estimated Baseline**: ~15 tool calls (manual)
- **Optimized**: ~5 tool calls (automated)
- **Reduction**: ~67%

### Execution Time

- **Estimated Baseline**: ~90 seconds (manual, with thinking)
- **Optimized**: ~15-20 seconds (automated)
- **Improvement**: 78-83%

### Caching

With `--optimized` flag:

- Uses `routine_cache.py` for GitHub/service data
- Reduces redundant API calls
- 40-96% token reduction (per routine.md)

## Usage Examples

### Basic Usage

```bash
/popkit:routine morning
# → Runs default morning routine
# → Calculates Ready to Code Score
# → Updates STATUS.json
# → Shows report
```

### With Measurement

```bash
/popkit:routine morning --measure
# → Runs morning routine
# → Tracks performance metrics
# → Saves to .claude/popkit/measurements/
```

### Quick Summary

```bash
/popkit:routine morning quick
# → Shows one-line summary
# → Ready to Code Score: 75/100 👍 - redis down, 3 commits behind
```

### With Optimization

```bash
/popkit:routine morning --optimized
# → Uses caching for GitHub/service data
# → Reduces token usage by 40-96%
```

## Files Modified

1. **STATUS.json** - Session state updated with:
   - Ready to Code score
   - Session restoration status
   - Dev environment state
   - Morning routine timestamp
   - Recommendations

2. **.claude/popkit/measurements/** (if --measure used)
   - Performance metrics
   - Tool call breakdown
   - Duration and token usage

## Related Skills

- **pop-session-resume**: Restores session context (invoked automatically)
- **pop-nightly**: Evening counterpart with Sleep Score
- **pop-routine-optimized**: Optimized execution with caching

## Related Commands

- **/popkit:routine morning**: Main entry point
- **/popkit:routine nightly**: Nightly routine
- **/popkit:next**: Context-aware next action recommendations

## Success Criteria

✅ Ready to Code Score accurately reflects environment state
✅ STATUS.json always updated correctly
✅ Completes in <25 seconds
✅ Provides actionable recommendations
✅ Session context successfully restored
✅ Reduces manual workflow by 67%

---

**Skill Type**: Automated Routine
**Category**: Workflow Automation
**Tier**: Core (Always Available)
**Version**: 1.0.0
