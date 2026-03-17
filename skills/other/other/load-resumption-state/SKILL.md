---
name: load-resumption-state
description: Load conductor workflow state from previous session and determine resumption point by analyzing git state and saved JSON state file
---

# Load Resumption State

## Purpose

Analyze previous conductor workflow state from both `.claude/state/conductor.json` file and current git state to determine the correct resumption point, preventing duplicate work.

## When to Use

- At start of conductor workflow
- When resuming interrupted workflow
- Before Phase 1 (to check if already in progress)
- When user explicitly requests resumption

## Instructions

### Step 1: Check for State File

```bash
STATE_FILE=".claude/state/conductor.json"

if [ -f "$STATE_FILE" ]; then
  echo "📋 Found previous conductor session"

  # Validate JSON
  if ! jq empty "$STATE_FILE" 2>/dev/null; then
    echo "⚠️ State file corrupted - using git-only resumption"
    STATE_FOUND=false
  else
    STATE_FOUND=true

    # Load state
    SAVED_ISSUE=$(jq -r '.issue.number' "$STATE_FILE")
    SAVED_PHASE=$(jq -r '.currentPhase' "$STATE_FILE")
    SAVED_BRANCH=$(jq -r '.context.branchName' "$STATE_FILE")
    SAVED_PR=$(jq -r '.context.prNumber' "$STATE_FILE")
    SAVED_TIMESTAMP=$(jq -r '.timestamp' "$STATE_FILE")

    echo "   Issue: #$SAVED_ISSUE"
    echo "   Phase: $SAVED_PHASE"
    echo "   Branch: $SAVED_BRANCH"
    echo "   Last updated: $SAVED_TIMESTAMP"
  fi
else
  echo "ℹ️ No previous state file found - checking git state only"
  STATE_FOUND=false
fi
```

### Step 2: Analyze Git State

```bash
# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if on feature branch
if [[ "$CURRENT_BRANCH" =~ ^feature/issue-([0-9]+) ]]; then
  # Extract issue number from branch name
  BRANCH_ISSUE="${BASH_REMATCH[1]}"

  echo "🌿 Found feature branch: $CURRENT_BRANCH"
  echo "   Issue from branch: #$BRANCH_ISSUE"

  # Count commits on this branch
  COMMIT_COUNT=$(git rev-list --count development..HEAD 2>/dev/null || echo "0")
  echo "   Commits: $COMMIT_COUNT"

  # Check for uncommitted changes
  if [ -n "$(git status --porcelain)" ]; then
    HAS_CHANGES=true
    echo "   Uncommitted changes: Yes"
  else
    HAS_CHANGES=false
    echo "   Uncommitted changes: No"
  fi

  # Check if PR exists
  PR_NUMBER=$(gh pr list --head "$CURRENT_BRANCH" --json number --jq '.[0].number' 2>/dev/null)

  if [ -n "$PR_NUMBER" ] && [ "$PR_NUMBER" != "null" ]; then
    HAS_PR=true
    echo "   PR: #$PR_NUMBER"
  else
    HAS_PR=false
    echo "   PR: None"
  fi

  FEATURE_BRANCH_EXISTS=true
else
  echo "ℹ️ Not on feature branch (current: $CURRENT_BRANCH)"
  FEATURE_BRANCH_EXISTS=false
fi
```

### Step 3: Determine Resumption Point

```bash
RESUME_PHASE=1
RESUME_STEP=""

if [ "$FEATURE_BRANCH_EXISTS" = true ]; then
  if [ "$HAS_PR" = true ]; then
    # PR exists → Resume from Phase 5 (Gemini Review)
    RESUME_PHASE=5
    RESUME_STEP="Monitor CI and Gemini review"
    SKIP_PHASES="1, 2, 3, 4"

  elif [ "$COMMIT_COUNT" -gt 0 ]; then
    # Commits exist but no PR → Resume from Phase 4 (PR Creation)
    # But first verify Phase 3 quality gates passed
    RESUME_PHASE=4
    RESUME_STEP="Create pull request"
    SKIP_PHASES="1, 2, 3"
    VERIFY_QUALITY=true

  elif [ "$HAS_CHANGES" = true ]; then
    # Uncommitted changes → Resume from Phase 3 (Quality Assurance)
    RESUME_PHASE=3
    RESUME_STEP="Run quality gates"
    SKIP_PHASES="1, 2 (partial)"

  else
    # Branch exists but no commits → Resume from Phase 2 Step 3 (Implementation)
    RESUME_PHASE=2
    RESUME_STEP="Implementation (branch already created)"
    SKIP_PHASES="1, 2 (steps 1-2)"
  fi
else
  # No feature branch → Start from Phase 1
  RESUME_PHASE=1
  RESUME_STEP="Issue discovery and planning"
  SKIP_PHASES="None"
fi

# Override with state file if more recent
if [ "$STATE_FOUND" = true ] && [ "$SAVED_PHASE" -gt "$RESUME_PHASE" ]; then
  RESUME_PHASE=$SAVED_PHASE
  echo "⚠️ State file indicates later phase - using Phase $SAVED_PHASE"
fi
```

### Step 4: Validate Resumption

```bash
# If resuming from Phase 4+, verify quality gates passed
if [ "$RESUME_PHASE" -ge 4 ] && [ "$VERIFY_QUALITY" = true ]; then
  echo ""
  echo "⚠️ Resuming after implementation - validating quality gates..."

  # Quick validation checks
  VALIDATION_PASSED=true

  # Check if tests exist
  if ! npm run test --dry-run &>/dev/null; then
    echo "   ⚠️ Warning: No test script found"
  fi

  # Check for TypeScript errors
  if command -v tsc &>/dev/null; then
    if ! tsc --noEmit &>/dev/null; then
      echo "   ❌ TypeScript errors detected"
      VALIDATION_PASSED=false
    fi
  fi

  if [ "$VALIDATION_PASSED" = false ]; then
    echo ""
    echo "❌ Quality validation failed - resuming from Phase 3 instead"
    RESUME_PHASE=3
    RESUME_STEP="Re-run quality gates"
  fi
fi
```

### Step 5: Return Resumption Data

```json
{
  "resumption": {
    "detected": true,
    "phase": 4,
    "step": "Create pull request",
    "skipPhases": [1, 2, 3]
  },
  "state": {
    "source": "git+state_file",
    "stateFile": {
      "found": true,
      "issue": 137,
      "savedPhase": 3,
      "timestamp": "2025-10-21T..."
    },
    "git": {
      "branch": "feature/issue-137-dark-mode",
      "issue": 137,
      "commits": 5,
      "hasChanges": false,
      "hasPR": false
    }
  },
  "recommendation": {
    "action": "resume",
    "phase": 4,
    "reason": "Branch exists with commits but no PR - ready for PR creation",
    "validation": {
      "qualityGates": "not_verified",
      "recommendation": "Run Phase 3 validation before proceeding"
    }
  }
}
```

## Output Format

### Resume from Phase 1 (Fresh Start)

```json
{
  "resumption": {
    "detected": false,
    "phase": 1,
    "step": "Issue discovery and planning",
    "skipPhases": []
  },
  "state": {
    "source": "none",
    "branch": "development"
  }
}
```

### Resume from Phase 3 (Quality Gates)

```json
{
  "resumption": {
    "detected": true,
    "phase": 3,
    "step": "Run quality gates",
    "skipPhases": [1, 2]
  },
  "state": {
    "source": "git",
    "git": {
      "branch": "feature/issue-137-dark-mode",
      "issue": 137,
      "commits": 0,
      "hasChanges": true
    }
  }
}
```

### Resume from Phase 5 (Gemini Review)

```json
{
  "resumption": {
    "detected": true,
    "phase": 5,
    "step": "Monitor CI and Gemini review",
    "skipPhases": [1, 2, 3, 4]
  },
  "state": {
    "source": "git+pr",
    "git": {
      "branch": "feature/issue-137-dark-mode",
      "issue": 137,
      "commits": 5,
      "hasPR": true,
      "prNumber": 45
    }
  }
}
```

## Integration with Conductor

Used at the start of conductor workflow:

```markdown
### BEFORE STARTING ANY WORKFLOW:

**Step 1: Check for Resumption**

Use `load-resumption-state` skill to analyze previous work:

Result: {
  "resumption": {
    "detected": true,
    "phase": 3,
    "skipPhases": [1, 2]
  }
}

**OUTPUT TO USER:**
```
🔄 RESUMPTION DETECTED

Current State:
  Branch: feature/issue-137-dark-mode
  Issue: #137
  Commits: 5
  PR: None

Detected Work:
  ✅ Phase 1: Planning
  ✅ Phase 2: Implementation
  → Phase 3: Quality Assurance

Resume from Phase 3? This will:
  - Skip completed phases
  - Continue with Quality Assurance
  - Preserve existing commits
```

**If user confirms**: Jump to Phase 3
**If user declines**: Start fresh from Phase 1
```

## Resumption Decision Matrix

| Git State | State File | Resume Phase | Skip Phases |
|-----------|------------|--------------|-------------|
| No feature branch | None | 1 | None |
| Feature branch, no commits | Phase 2 | 2 (Step 3) | 1, 2 (partial) |
| Feature branch + commits | Phase 3 | 3 | 1, 2 |
| Feature branch + commits + changes | None | 3 | 1, 2 |
| Feature branch + PR | Phase 5 | 5 | 1, 2, 3, 4 |
| Feature branch + PR + CI passed | Phase 6 | 6 | 1, 2, 3, 4, 5 |

## Related Skills

- `save-workflow-state` - Save state after each phase
- `determine-resumption-phase` - Advanced decision logic
- `clear-workflow-state` - Clean up after workflow completion

## Error Handling

### Corrupted State File

```json
{
  "resumption": {
    "detected": true,
    "phase": 2,
    "warning": "State file corrupted - using git-only resumption"
  }
}
```

### Conflicting State

```json
{
  "resumption": {
    "detected": true,
    "phase": 3,
    "warning": "State file (Phase 2) conflicts with git (Phase 3) - using git state"
  }
}
```

## Best Practices

1. **Always check state before starting** - Prevents duplicate work
2. **Trust git state over state file** - More reliable source of truth
3. **Validate quality gates** - When resuming Phase 4+
4. **Inform user of resumption** - Let them confirm before skipping phases
5. **Log resumption decision** - Include reasoning for debugging

## Notes

- State file is supplemental - git is source of truth
- Resumption saves significant time on interrupted workflows
- User should always confirm resumption point
- Quality gates should be re-validated when resuming late phases
