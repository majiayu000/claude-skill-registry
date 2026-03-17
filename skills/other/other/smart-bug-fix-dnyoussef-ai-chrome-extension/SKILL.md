---
name: smart-bug-fix
description: Intelligent bug fixing workflow combining root cause analysis, multi-model reasoning, Codex auto-fix, and comprehensive testing. Uses RCA agent, Codex iteration, and validation to systematically fix bugs.
tags: [debugging, rca, codex, testing, essential, tier-1]
version: 1.0.0
---

# Smart Bug Fix

## Purpose

Systematically debug and fix bugs using root cause analysis, multi-model reasoning, and automated testing.

## Specialist Agent

I am a debugging specialist using systematic problem-solving methodology.

**Methodology** (Root Cause + Fix + Validate Pattern):
1. Deep root cause analysis (5 Whys, inverse reasoning)
2. Multi-model reasoning for fix approaches
3. Codex auto-fix in isolated sandbox
4. Comprehensive testing with iteration
5. Regression validation
6. Performance impact analysis

**Models Used**:
- **Claude (RCA)**: Deep root cause analysis
- **Codex (Fix)**: Rapid fix implementation
- **Claude (Validation)**: Comprehensive testing
- **Gemini (Context)**: Large codebase analysis if needed

**Output**: Fixed code with test validation and impact analysis

## Input Contract

```yaml
input:
  bug_description: string (required)
  context_path: string (directory or file, required)
  reproduction_steps: string (optional)
  error_logs: string (optional)
  depth: enum[shallow, normal, deep] (default: deep)
```

## Output Contract

```yaml
output:
  root_cause: object
    identified: string
    contributing_factors: array[string]
    evidence: array[string]
  fix_applied: object
    changes: array[file_change]
    reasoning: string
    alternatives_considered: array[string]
  validation: object
    tests_passed: boolean
    regression_check: boolean
    performance_impact: string
  confidence: number (0-1)
```

## Execution Flow

```bash
#!/bin/bash
set -e

BUG_DESC="$1"
CONTEXT_PATH="$2"

echo "=== Smart Bug Fix Workflow ==="

# PHASE 1: Root Cause Analysis
echo "[1/6] Performing deep root cause analysis..."
npx claude-flow agent-rca "$BUG_DESC" \
  --context "$CONTEXT_PATH" \
  --depth deep \
  --output rca-report.md

# PHASE 2: Context Analysis (if large codebase)
LOC=$(find "$CONTEXT_PATH" -name "*.js" -o -name "*.ts" | xargs wc -l | tail -1 | awk '{print $1}')
if [ "$LOC" -gt 10000 ]; then
  echo "[2/6] Large codebase detected - analyzing with Gemini MegaContext..."
  gemini "Analyze patterns related to: $BUG_DESC" \
    --files "$CONTEXT_PATH" \
    --model gemini-2.0-flash \
    --output context-analysis.md
else
  echo "[2/6] Standard codebase - skipping mega-context analysis"
fi

# PHASE 3: Alternative Solutions (multi-model reasoning)
echo "[3/6] Generating fix approaches..."
# Claude approach (from RCA)
CLAUDE_FIX=$(cat rca-report.md | grep "Solution" -A 10)

# Codex alternative approach
codex --reasoning-mode "Alternative approaches to fix: $BUG_DESC" \
  --context rca-report.md \
  --output codex-alternatives.md

# PHASE 4: Implement Fix with Codex Auto
echo "[4/6] Implementing fix with Codex Auto..."
codex --full-auto "Fix bug: $BUG_DESC based on RCA findings" \
  --context rca-report.md \
  --context "$CONTEXT_PATH" \
  --sandbox true \
  --network-disabled \
  --output fix-implementation/

# PHASE 5: Comprehensive Testing with Iteration
echo "[5/6] Testing fix with Codex iteration..."
npx claude-flow functionality-audit fix-implementation/ \
  --model codex-auto \
  --max-iterations 5 \
  --sandbox true \
  --regression-check true \
  --output test-results.json

# Check if tests passed
TESTS_PASSED=$(cat test-results.json | jq '.all_passed')
if [ "$TESTS_PASSED" != "true" ]; then
  echo "⚠️ Tests failed after 5 iterations - escalating to user"
  exit 1
fi

# PHASE 6: Performance Impact Analysis
echo "[6/6] Analyzing performance impact..."
npx claude-flow analysis performance-report \
  --compare-before-after \
  --export performance-impact.json

# Display summary
echo ""
echo "================================================================"
echo "Bug Fix Complete!"
echo "================================================================"
echo ""
echo "Root Cause: $(cat rca-report.md | grep 'Primary Root Cause' -A 2 | tail -1)"
echo "Tests: ✓ All passing"
echo "Regression: ✓ No regressions detected"
echo "Performance Impact: $(cat performance-impact.json | jq '.impact_summary')"
echo ""
echo "Files changed:"
find fix-implementation/ -name "*.js" -o -name "*.ts" | head -10
echo ""
```

## Integration Points

### Cascades
- Part of `/bug-triage-workflow` cascade
- Used by `/production-incident-response` cascade
- Invoked by `/fix-bug` command

### Commands
- Uses: `/agent-rca`, `/gemini-megacontext`, `/codex-auto`, `/functionality-audit`
- Chains with: `/style-audit`, `/performance-report`

### Other Skills
- Input to `regression-validator` skill
- Used by `incident-response` skill
- Integrates with `code-review-assistant`

## Advanced Features

### Automatic RCA Depth Selection

```javascript
function selectRCADepth(bugDescription, errorLogs) {
  if (errorLogs.includes("intermittent") || errorLogs.includes("race condition")) {
    return "deep"; // Complex issues need deep analysis
  } else if (errorLogs.includes("TypeError") || errorLogs.includes("undefined")) {
    return "normal"; // Common errors need normal analysis
  } else {
    return "shallow"; // Simple issues
  }
}
```

### Multi-Model Fix Approach

```yaml
fix_strategy:
  1. Claude RCA → Deep understanding
  2. Codex alternatives → Multiple approaches
  3. Codex auto-fix → Rapid implementation
  4. Claude validation → Comprehensive testing
```

### Codex Iteration Loop

```
Test → FAIL → Codex fix → Test → FAIL → Codex fix → Test → PASS → Apply
↑                                                                    ↓
└────────────────── Max 5 iterations ──────────────────────────────┘
```

## Usage Example

```bash
# Fix bug with description
smart-bug-fix "API timeout under load" src/api/

# Fix with reproduction steps
smart-bug-fix "Login fails on Firefox" src/auth/ \
  --reproduction-steps "1. Open Firefox 2. Try login 3. See error"

# Fix with error logs
smart-bug-fix "Database connection fails" src/db/ \
  --error-logs "logs/error.log"
```

## Failure Modes

- **RCA inconclusive**: Request more context, run additional diagnostics
- **Codex fix fails tests**: Try alternative approach, escalate if max iterations reached
- **Regression detected**: Rollback fix, analyze conflicting requirements
- **Performance degradation**: Optimize fix, consider alternative approach
