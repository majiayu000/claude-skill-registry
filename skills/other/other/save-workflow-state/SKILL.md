---
name: save-workflow-state
description: Save conductor workflow state to JSON file for smart resumption, tracking current phase, completed phases, issue context, and branch information
---

# Save Workflow State

## Purpose

Persist conductor workflow state after each phase completion to enable smart resumption across sessions, preventing duplicate work and allowing workflow recovery.

## When to Use

- After completing conductor Phase 1 (Issue Discovery and Planning)
- After completing conductor Phase 2 (Branch Setup and Implementation)
- After completing conductor Phase 3 (Quality Assurance)
- After completing conductor Phase 4 (PR Creation)
- After completing conductor Phase 5 (Gemini Review)
- After completing conductor Phase 6 (Final Report)

**Frequency**: 6 times per full-cycle workflow

## Instructions

### Step 1: Create State Directory

```bash
# Ensure state directory exists
mkdir -p .claude/state
```

### Step 2: Build State Object

Collect workflow metadata:

```bash
# Required fields with safe defaults
ISSUE_NUMBER=${1:-null}
ISSUE_TITLE=${2:-""}
CURRENT_PHASE=${3:-1}
BRANCH_NAME=${4:-""}

# Optional fields
PR_NUMBER=${5:-null}
AUDIT_SCORE=${6:-null}
ARCHITECTURE_PLAN=${7:-""}
IMPLEMENTATION_SUMMARY=${8:-""}

# Validate required fields
if [ "$ISSUE_NUMBER" = "null" ] || [ -z "$ISSUE_TITLE" ] || [ -z "$CURRENT_PHASE" ]; then
  echo "❌ Error: Missing required parameters"
  echo "Usage: save-workflow-state <issue_number> <issue_title> <current_phase> <branch_name> [pr_number] [audit_score] [architecture_plan] [implementation_summary]"
  exit 1
fi

# Get current timestamp
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Calculate completed phases
COMPLETED_PHASES="["
for i in $(seq 1 $((CURRENT_PHASE - 1))); do
  if [ $i -gt 1 ]; then
    COMPLETED_PHASES="$COMPLETED_PHASES,"
  fi
  COMPLETED_PHASES="$COMPLETED_PHASES$i"
done
COMPLETED_PHASES="$COMPLETED_PHASES]"
```

### Step 3: Write State File

```bash
STATE_FILE=".claude/state/conductor.json"

cat > "$STATE_FILE" << EOF
{
  "conductor_version": "1.0",
  "timestamp": "$TIMESTAMP",
  "workflow": "full-cycle",
  "issue": {
    "number": ${ISSUE_NUMBER},
    "title": "${ISSUE_TITLE}",
    "type": "feature",
    "hasAiAnalysis": true
  },
  "currentPhase": ${CURRENT_PHASE},
  "completedPhases": ${COMPLETED_PHASES},
  "context": {
    "branchName": "${BRANCH_NAME}",
    "filesChanged": [],
    "commitCount": 0,
    "prNumber": ${PR_NUMBER},
    "architecturePlan": "${ARCHITECTURE_PLAN}",
    "implementationNotes": "${IMPLEMENTATION_SUMMARY}"
  },
  "phases": {
    "1": {
      "name": "Issue Discovery and Planning",
      "status": "$([ ${CURRENT_PHASE} -gt 1 ] && echo 'completed' || echo 'in_progress')",
      "timestamp": "$TIMESTAMP",
      "outputs": {
        "issueSelected": ${ISSUE_NUMBER},
        "architectureValidated": true,
        "aiAnalysisUsed": true
      }
    },
    "2": {
      "name": "Branch Setup and Implementation",
      "status": "$([ $CURRENT_PHASE -gt 2 ] && echo 'completed' || [ $CURRENT_PHASE -eq 2 ] && echo 'in_progress' || echo 'pending')",
      "timestamp": "$([ $CURRENT_PHASE -ge 2 ] && echo $TIMESTAMP || echo '')",
      "outputs": {}
    },
    "3": {
      "name": "Quality Assurance",
      "status": "$([ $CURRENT_PHASE -gt 3 ] && echo 'completed' || [ $CURRENT_PHASE -eq 3 ] && echo 'in_progress' || echo 'pending')",
      "timestamp": "$([ $CURRENT_PHASE -ge 3 ] && echo $TIMESTAMP || echo '')",
      "outputs": {}
    },
    "4": {
      "name": "PR Creation",
      "status": "$([ $CURRENT_PHASE -gt 4 ] && echo 'completed' || [ $CURRENT_PHASE -eq 4 ] && echo 'in_progress' || echo 'pending')",
      "timestamp": "$([ $CURRENT_PHASE -ge 4 ] && echo $TIMESTAMP || echo '')",
      "outputs": {}
    },
    "5": {
      "name": "Gemini Review",
      "status": "$([ $CURRENT_PHASE -gt 5 ] && echo 'completed' || [ $CURRENT_PHASE -eq 5 ] && echo 'in_progress' || echo 'pending')",
      "timestamp": "$([ $CURRENT_PHASE -ge 5 ] && echo $TIMESTAMP || echo '')",
      "outputs": {}
    },
    "6": {
      "name": "Final Report",
      "status": "$([ $CURRENT_PHASE -gt 6 ] && echo 'completed' || [ $CURRENT_PHASE -eq 6 ] && echo 'in_progress' || echo 'pending')",
      "timestamp": "$([ $CURRENT_PHASE -ge 6 ] && echo $TIMESTAMP || echo '')",
      "outputs": {}
    }
  }
}
EOF
```

### Step 4: Verify State Written

```bash
if [ -f "$STATE_FILE" ]; then
  echo "✅ Workflow state saved: Phase $CURRENT_PHASE"

  # Validate JSON
  if jq empty "$STATE_FILE" 2>/dev/null; then
    echo "✅ State file is valid JSON"
  else
    echo "❌ State file has invalid JSON - workflow resumption may fail"
  fi
else
  echo "❌ Failed to save workflow state"
fi
```

## State Schema

```typescript
interface ConductorState {
  conductor_version: string;
  timestamp: string;
  workflow: "full-cycle" | "implementation-only" | "quality-gate";
  issue: {
    number: number;
    title: string;
    type: "feature" | "bug" | "refactor" | "research-heavy";
    hasAiAnalysis: boolean;
  };
  currentPhase: 1 | 2 | 3 | 4 | 5 | 6;
  completedPhases: number[];
  context: {
    branchName: string;
    filesChanged: string[];
    commitCount: number;
    prNumber: number | null;
    architecturePlan: string;
    implementationNotes: string;
  };
  phases: {
    [key: string]: {
      name: string;
      status: "pending" | "in_progress" | "completed";
      timestamp: string;
      outputs: Record<string, any>;
    };
  };
}
```

## Usage Examples

### After Phase 1 Completion

```bash
# Save state after Phase 1
save-workflow-state \
  137 \
  "Add user dark mode preference toggle" \
  1 \
  "feature/issue-137-dark-mode" \
  null \
  null \
  "VSA compliant, no violations found"
```

### After Phase 3 Completion

```bash
# Save state after Phase 3 with quality metrics
save-workflow-state \
  137 \
  "Add user dark mode preference toggle" \
  3 \
  "feature/issue-137-dark-mode" \
  null \
  8.5 \
  "VSA compliant" \
  "Implemented dark mode toggle with state management"
```

### After Phase 4 Completion

```bash
# Save state after PR creation
save-workflow-state \
  137 \
  "Add user dark mode preference toggle" \
  4 \
  "feature/issue-137-dark-mode" \
  45 \
  8.5 \
  "VSA compliant" \
  "Implemented dark mode toggle"
```

## Integration with Conductor

Used after each phase in conductor workflow:

```markdown
### Phase 1: Issue Discovery and Planning

... [phase work] ...

**ACTION: Save state after Phase 1 completion:**

Use `save-workflow-state` skill:
- issue_number: $ISSUE_NUMBER
- issue_title: $ISSUE_TITLE
- current_phase: 1
- branch_name: $BRANCH_NAME (if created)
- architecture_plan: Summary from architect agent

→ Proceed to Phase 2
```

## Related Skills

- `load-resumption-state` - Load saved state for workflow resumption
- `determine-resumption-phase` - Analyze state to determine restart point
- `clear-workflow-state` - Clean up state after workflow completion

## State File Location

- **Path**: `.claude/state/conductor.json`
- **Git**: Should be in `.gitignore` (session-specific)
- **Persistence**: Survives across Claude Code restarts
- **Cleanup**: Manually delete or use `clear-workflow-state` skill

## Best Practices

1. **Save after each phase** - Don't batch multiple phases
2. **Include phase outputs** - Save key metrics and decisions
3. **Validate JSON** - Use `jq` to verify valid JSON
4. **Update completedPhases** - Accurately track completed work
5. **Timestamp everything** - Helps debug resumption issues
6. **Don't commit state** - Add to `.gitignore`

## Error Handling

### Directory Creation Fails

```bash
if ! mkdir -p .claude/state; then
  echo "❌ Cannot create state directory"
  return 1
fi
```

### Write Permission Denied

```bash
if [ ! -w .claude/state ]; then
  echo "❌ No write permission for state directory"
  return 1
fi
```

### Invalid JSON Generated

```bash
if ! jq empty "$STATE_FILE" 2>/dev/null; then
  echo "⚠️ Invalid JSON in state file - resumption may fail"
  echo "State file location: $STATE_FILE"
fi
```

## Notes

- State file enables smart resumption across sessions
- Should be created in `.claude/state/` directory
- Not committed to git (session-specific)
- Used by `load-resumption-state` skill for workflow recovery
- Critical for long-running workflows spanning multiple sessions
