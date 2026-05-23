---
name: nightly
description: "End-of-day cleanup and maintenance routine. Calculates Sleep Score (0-100) based on uncommitted work, branch cleanup, issue updates, CI status, and service shutdown. Automatically captures session state to STATUS.json. Use at end of work day before closing Claude Code."
---

# Nightly Routine

## Overview

Automated end-of-day maintenance that ensures clean project state before leaving for the day.

**Core principle:** Leave the codebase in a clean, resumable state with zero manual overhead.

**Trigger:** End of work day, before closing Claude Code

**Duration:** ~10-15 seconds (vs. ~60 seconds manual)

## Sleep Score (0-100)

Comprehensive health check across 6 dimensions:

| Check                  | Points | Criteria                            |
| ---------------------- | ------ | ----------------------------------- |
| Uncommitted work saved | 25     | No uncommitted changes OR committed |
| Branches cleaned       | 20     | No stale merged branches            |
| Issues updated         | 20     | Today's issues have status updates  |
| CI passing             | 15     | Latest CI run successful            |
| Services stopped       | 10     | No dev services running             |
| Logs archived          | 10     | Session logs saved                  |

**Score Interpretation:**

- **90-100**: Perfect shutdown - ready for tomorrow
- **70-89**: Good - minor cleanup needed
- **50-69**: Fair - some uncommitted work or failed CI
- **0-49**: Poor - significant cleanup required

## Workflow Steps

### 1. Collect Project State

Using `capture_state.py` utility:

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
- Uncommitted files (count and list)
- Stashed changes count
- Last commit info
- Merged branches count

**GitHub Analysis:**

- Open issues (last 5)
- Recent issue updates
- Latest CI run status

**Service Analysis:**

- Running dev services (node, npm, pnpm, redis, postgres, supabase)
- Session log files to archive

### 2. Calculate Sleep Score

Using `sleep_score.py` module:

```python
from pop_nightly.scripts.sleep_score import calculate_sleep_score

score, breakdown = calculate_sleep_score(state)
# score: 0-100
# breakdown: {
#   'uncommitted_work_saved': {'points': 0, 'max': 25, 'reason': '...'},
#   'branches_cleaned': {'points': 20, 'max': 20, 'reason': '...'},
#   ...
# }
```

### 3. Generate Nightly Report

Using `report_generator.py` module:

```python
from pop_nightly.scripts.report_generator import generate_nightly_report

report = generate_nightly_report(score, breakdown, state)
# Returns formatted markdown report with:
# - Sleep Score headline
# - Score breakdown table
# - Uncommitted changes (if any)
# - Recommendations before leaving
# - Next session actions
```

### 4. Capture Session State

Invoke `pop-session-capture` skill to update STATUS.json:

```python
# This happens automatically via Skill tool invocation
# Updates STATUS.json with:
# - Nightly routine execution timestamp
# - Sleep score
# - Git status
# - In-progress work
# - Recommendations
```

### 5. Present Report to User

Display nightly report with:

- **Sleep Score** (0-100) with visual indicator
- **Score Breakdown** - What contributed to the score
- **Uncommitted Changes** - Files that need attention
- **Recommendations** - Actions before leaving
- **Next Steps** - What to do tomorrow morning

## Data Collection Commands

### Git Commands (Consolidated)

Single command to gather all git data:

```bash
{
  echo "=== BRANCH ==="
  git rev-parse --abbrev-ref HEAD
  echo "=== COMMIT ==="
  git log -1 --format="%h - %s"
  echo "=== STATUS ==="
  git status --porcelain
  echo "=== STASHES ==="
  git stash list | wc -l
  echo "=== MERGED ==="
  git branch --merged main | grep -v "^\*" | grep -v "main" | wc -l
} | python -c "
import sys
sections = sys.stdin.read().split('===')
data = {}
for section in sections:
    if 'BRANCH' in section:
        data['branch'] = section.split('===')[1].strip()
    # ... parse other sections
print(json.dumps(data))
"
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

**Sleep Score Impact:**

If on protected branch with uncommitted work:

- **Warning:** Include ⚠️ PROTECTED indicator in output
- **Recommendation:** "Create feature branch and move uncommitted work before committing"
- **Option Priority:** Prioritize "Create feature branch" over "Commit and push"

### GitHub Commands (Consolidated)

```bash
{
  gh issue list --state open --limit 5 --json number,title,updatedAt
  echo "---SEPARATOR---"
  gh run list --limit 1 --json conclusion,status,createdAt
} > /tmp/gh_data.json
```

### Service Check (Consolidated)

```bash
{
  ps aux | grep -E "(node|npm|pnpm|redis|postgres|supabase)" | grep -v grep
  echo "---SEPARATOR---"
  ls ~/.claude/logs/*.log 2>/dev/null | wc -l
} > /tmp/service_data.txt
```

## Integration with Existing Utilities

### capture_state.py

Located: `packages/shared-py/popkit_shared/utils/capture_state.py`

```python
def capture_project_state() -> dict:
    """Capture complete project state for nightly routine."""
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
- Saves to `.claude/popkit/measurements/nightly-<timestamp>.json`

### routine_cache.py

Located: `packages/shared-py/popkit_shared/utils/routine_cache.py`

Caching strategy:

- **Never cache**: Git status (changes frequently)
- **Cache 15 min**: CI status
- **Cache 1 hour**: GitHub issue list

## Output Format

```markdown
# 🌙 Nightly Routine Report

**Date**: 2025-12-28
**Sleep Score**: 60/100 ⚠️

## Score Breakdown

| Check                  | Points | Status                  |
| ---------------------- | ------ | ----------------------- |
| Uncommitted work saved | 0/25   | ❌ 3 uncommitted files  |
| Branches cleaned       | 20/20  | ✅ No stale branches    |
| Issues updated         | 20/20  | ✅ All issues current   |
| CI passing             | 0/15   | ❌ Latest run skipped   |
| Services stopped       | 10/10  | ✅ All services stopped |
| Logs archived          | 10/10  | ✅ No logs to archive   |

## Uncommitted Changes (3 files)

- `apps/popkit/packages/websitebuild-popkit-test-beta.txt` (deleted)
- `pnpm-lock.yaml` (modified)
- `.npmrc` (untracked)

## 📋 Recommendations

**Before Leaving:**

- Commit or stash uncommitted changes
- Review 8 stashes: `git stash list`
- Check why CI was skipped

**Next Morning:**

- Run `/popkit:routine morning` to check overnight changes
- Review and test pending PRs
- Clear stash backlog

---

STATUS.json updated ✅
Session state captured for tomorrow's resume.

## 🎯 Next Actions (The PopKit Way)

**CRITICAL**: Always end with AskUserQuestion to keep PopKit in control.

Use AskUserQuestion tool with context-aware options based on nightly report:

**Option 1: If uncommitted work exists (Score < 70)**
```

What would you like to do before ending the day?
├─ Commit and push all changes (Recommended)
│ └─ Save all uncommitted work
├─ Stash changes for tomorrow
├─ Review uncommitted files
└─ Other

```

**Option 2: If clean working directory (Score >= 70)**
```

Ready to wrap up! What's your last action?
├─ Review tomorrow's priorities
├─ Check overnight CI status
├─ End session (all clean)
└─ Other

```

**Option 3: If services still running**
```

Dev services are still running. What would you like to do?
├─ Stop all dev services (Recommended)
├─ Leave services running
├─ Check which services are running
└─ Other

```

**Option 4: If CI failing**
```

Latest CI run failed. What would you like to do?
├─ Investigate CI failure now
├─ Note for morning review
├─ Check CI logs
└─ Other

````

### Implementation

After generating the nightly report, invoke AskUserQuestion based on score and context:

```python
# After generating report
questions = generate_next_action_questions(score, breakdown, state)
# Returns AskUserQuestion tool invocation

# Example output to Claude:
{
    "type": "ask_user_question",
    "questions": [{
        "question": "What would you like to do before ending the day?",
        "header": "Next Action",
        "multiSelect": false,
        "options": [
            {
                "label": "Commit and push all changes (Recommended)",
                "description": "Save 5 uncommitted files"
            },
            {
                "label": "Stash changes for tomorrow",
                "description": "Keep work-in-progress safe"
            },
            {
                "label": "Stop dev services",
                "description": "3 services still running: redis, postgres, node"
            }
        ]
    }]
}
````

**Why This Matters (The PopKit Way):**

- ✅ Keeps PopKit in control of the workflow
- ✅ Prevents "forgot to commit" situations
- ✅ Enables graceful session shutdown
- ✅ Prevents "report dump and done" anti-pattern
- ✅ Maintains workflow continuity for tomorrow

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
# If they fail, assume services are stopped (safe default)
```

## Optimization Features

### Tool Call Reduction

- **Baseline**: 11 tool calls (manual)
- **Optimized**: 4 tool calls (automated)
- **Reduction**: 64%

### Execution Time

- **Baseline**: ~60 seconds (manual, with thinking)
- **Optimized**: ~10-15 seconds (automated)
- **Improvement**: 75-83%

### Caching

With `--optimized` flag:

- Uses `routine_cache.py` for GitHub data
- Reduces redundant API calls
- 40-96% token reduction (per routine.md)

## Usage Examples

### Basic Usage

```bash
/popkit:routine nightly
# → Runs default nightly routine
# → Calculates Sleep Score
# → Updates STATUS.json
# → Shows report
```

### With Measurement

```bash
/popkit:routine nightly --measure
# → Runs nightly routine
# → Tracks performance metrics
# → Saves to .claude/popkit/measurements/
```

### Quick Summary

```bash
/popkit:routine nightly quick
# → Shows one-line summary
# → Sleep Score: 60/100 - 3 uncommitted files, CI skipped
```

### With Optimization

```bash
/popkit:routine nightly --optimized
# → Uses caching for GitHub data
# → Reduces token usage by 40-96%
```

## Files Modified

1. **STATUS.json** - Session state updated with:
   - Sleep score
   - Git context
   - Nightly routine timestamp
   - Recommendations

2. **.claude/popkit/measurements/** (if --measure used)
   - Performance metrics
   - Tool call breakdown
   - Duration and token usage

## Related Skills

- **pop-session-capture**: Updates STATUS.json (invoked automatically)
- **pop-morning**: Morning counterpart with Ready to Code score
- **pop-routine-optimized**: Optimized execution with caching

## Related Commands

- **/popkit:routine nightly**: Main entry point
- **/popkit:routine morning**: Morning routine
- **/popkit:next**: Context-aware next action recommendations

## Success Criteria

✅ Sleep Score accurately reflects project state
✅ STATUS.json always updated correctly
✅ Completes in <20 seconds
✅ Provides actionable recommendations
✅ Reduces manual workflow by 64%

---

**Skill Type**: Automated Routine
**Category**: Workflow Automation
**Tier**: Core (Always Available)
**Version**: 1.0.0
