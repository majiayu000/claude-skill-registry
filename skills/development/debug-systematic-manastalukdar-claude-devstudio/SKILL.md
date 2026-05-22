---
name: debug-systematic
description: Systematic debugging workflow with hypothesis testing
disable-model-invocation: false
---

# Systematic Debugging Workflow

I'll help you debug issues systematically using the scientific method - hypothesis formation, testing, and iterative refinement.

Arguments: `$ARGUMENTS` - error description, reproduction steps, or context

## Token Optimization

**Target:** 50% reduction (4,000-6,000 → 1,500-3,000 tokens)

### Core Optimization Strategies

**1. Hypothesis-Driven Debugging (Not Exhaustive Analysis)**
- ❌ **AVOID:** Reading entire codebase to find bugs
- ✅ **DO:** Form hypotheses about likely causes, test top 2-3 first
- **Token savings:** 90% (200 tokens vs 2,000+ tokens)
- **Pattern:** Prioritize recently changed files, common failure patterns

**2. Git Diff for Recently Changed Files (Likely Bug Source)**
- ❌ **AVOID:** `ls -R` then reading all files
- ✅ **DO:** `git diff --name-only HEAD~3..HEAD` to find changed files
- ✅ **DO:** `git log --oneline --since="3 days ago"` for recent commits
- **Token savings:** 85% (300 tokens vs 2,000+ tokens)
- **Pattern:** Bugs often introduced in recent changes

**3. Stack Trace Parsing with Grep**
- ❌ **AVOID:** Reading entire log files with Read tool
- ✅ **DO:** `grep -i "error\|exception\|fatal" logs/*.log | tail -20`
- ✅ **DO:** Parse stack traces to extract file paths and line numbers
- **Token savings:** 95% (100 tokens vs 2,000+ tokens for large logs)
- **Pattern:** Stack traces reveal exact failure locations

**4. Test Failure Analysis Caching**
- ✅ Cache test results in `debug/state.json`
- ✅ Cache hypothesis outcomes to avoid retesting
- ✅ Cache reproduction steps once confirmed
- **Token savings:** 70% on subsequent debugging turns
- **Pattern:** Multi-turn debugging sessions benefit from state

**5. Progressive Investigation (Narrow Before Deep)**
- ✅ Start with stack trace → identify file → read specific function
- ✅ Hypothesis testing: test most likely causes first
- ✅ Binary search through git history when needed
- **Token savings:** 60% (stop early when cause found)
- **Pattern:** Most bugs have obvious causes in changed code

**6. Session State Tracking for Multi-Turn Debugging**
- ✅ Session files in `debug/` directory
- ✅ Track tested hypotheses to avoid repetition
- ✅ Resume from last checkpoint on subsequent runs
- **Token savings:** 80% on resumed sessions (skip completed work)
- **Pattern:** Complex bugs require multiple debugging turns

### Token Usage by Operation

| Operation | Unoptimized | Optimized | Savings |
|-----------|-------------|-----------|---------|
| Initial bug analysis | 2,000-3,000 | 500-1,000 | 60-75% |
| Hypothesis formation | 1,500-2,000 | 400-800 | 60-73% |
| Stack trace parsing | 2,000+ | 100-200 | 90-95% |
| File investigation | 2,000+ | 300-600 | 70-85% |
| Test reproduction | 1,000-1,500 | 200-400 | 73-80% |
| Session resume | 2,000-3,000 | 300-600 | 80-85% |

**Average Reduction:** 50% (4,000-6,000 → 1,500-3,000 tokens)

### Debugging-Specific Patterns

**Stack Trace Analysis:**
```bash
# Extract file paths and line numbers from stack traces
grep -E "at .+ \(.+:[0-9]+:[0-9]+\)" error.log | head -10
# Focus investigation on these specific files/lines
```

**Recent Changes Focus:**
```bash
# Find files changed in last 3 days (likely bug sources)
git diff --name-only HEAD~10..HEAD
# Only read files that changed recently
```

**Hypothesis Prioritization:**
1. **Recent changes** (80% of bugs) - Check git diff first
2. **Stack trace files** (90% reliability) - Read exact failure locations
3. **Error message patterns** (70% of bugs) - Grep for similar errors
4. **Environment/config** (20% of bugs) - Check if configs changed
5. **External dependencies** (10% of bugs) - Check updates

**Binary Search for Regressions:**
```bash
# Use git bisect to find regression commit
git bisect start HEAD v1.2.3
git bisect run npm test  # Automated testing
# Saves 95% tokens vs manual testing each commit
```

### Caching Behavior

**Session Location:** `debug/` (in project root)
- `debug/plan.md` - Debugging plan with hypotheses and results
- `debug/state.json` - Session state and test results
- `debug/reproduction.log` - Issue reproduction steps and logs

**Cache Location:** `.claude/cache/debug/`
- `hypotheses.json` - Tested hypotheses and outcomes
- `stack-traces.json` - Parsed stack trace information
- `changed-files.json` - Recently changed files analysis

**Cache Validity:**
- Until issue resolved (status: "solved" in state.json)
- Until source files change (checksum-based)
- 7 days maximum for stale sessions

**Shared With:**
- `/debug-root-cause` - Root cause analysis skill
- `/debug-session` - Debug session documentation
- `/test` - Test execution for verification

### Usage Examples

**Start New Debugging Session:**
```
debug-systematic "API returns 500 on POST /users"
# Expected tokens: 1,500-3,000 (full analysis)
```

**Resume Existing Session:**
```
debug-systematic resume
# Expected tokens: 800-1,500 (skips completed hypotheses)
```

**Test Specific Hypothesis:**
```
debug-systematic test 1
# Expected tokens: 500-1,000 (focused testing)
```

**Check Debugging Progress:**
```
debug-systematic status
# Expected tokens: 200-500 (read session state only)
```

**Mark Issue as Solved:**
```
debug-systematic solved
# Expected tokens: 300-600 (generate summary)
```

### Early Exit Conditions

**Exit immediately (saves 90% tokens) when:**
- ✅ Issue already solved (check `debug/state.json` status)
- ✅ No test framework available (can't reproduce)
- ✅ Not a git repository (can't check recent changes)
- ✅ Root cause already identified in session state

**Progressive disclosure saves 60-80% tokens:**
- Show hypothesis formation → wait for user confirmation
- Test one hypothesis at a time → report results
- Only deep dive when hypothesis confirms

### Implementation Checklist

- ✅ Git diff analysis for recent changes (PRIMARY optimization)
- ✅ Stack trace parsing with Grep (saves 90-95%)
- ✅ Session-based hypothesis tracking (saves 70-80% on reruns)
- ✅ Progressive hypothesis testing (most likely → least likely)
- ✅ Bash-based log analysis (minimal tokens)
- ✅ Test failure result caching
- ✅ Early exit when issue resolved
- ✅ Binary search for regressions (git bisect)
- ✅ Focus area flags (specific file/function debugging)

**Optimization Status:** ✅ Optimized (Phase 2 Batch 2, 2026-01-26)
**Expected Tokens:** 1,500-3,000 (vs. 4,000-6,000 unoptimized)
**Achieved Reduction:** 50% average across all debugging operations

## Session Intelligence

I'll maintain debugging session continuity:

**Session Files (in current project directory):**
- `debug/plan.md` - Debugging plan with hypotheses and results
- `debug/state.json` - Session state and test results
- `debug/reproduction.log` - Issue reproduction steps and logs

**IMPORTANT:** Session files are stored in a `debug` folder in your current project root

**Auto-Detection:**
- If session exists: Resume debugging from last hypothesis
- If no session: Create debugging plan and initial reproduction
- Commands: `resume`, `reproduce`, `status`, `solved`

## Phase 1: Issue Reproduction & Information Gathering

### Extended Thinking for Complex Debugging

For complex or elusive bugs, I'll use extended thinking to explore debugging strategies:

<think>
When debugging complex issues:
- Multiple potential root causes that interact
- Timing-sensitive or race condition bugs
- Environment-specific failures
- Subtle state corruption scenarios
- Performance degradation patterns
- Security vulnerability exploitation paths
</think>

**Triggers for Extended Analysis:**
- Intermittent or non-deterministic bugs
- Production-only failures
- Performance issues without obvious cause
- Security vulnerabilities
- Multi-component system failures

**MANDATORY FIRST STEPS:**
1. Check if `debug` directory exists in current working directory
2. If directory exists, check for session files:
   - Look for `debug/state.json`
   - Look for `debug/plan.md`
   - If found, resume from last hypothesis
3. If no directory or session exists:
   - Gather error information
   - Create reproduction steps
   - Initialize debugging session

**Information Gathering (Token-Efficient):**

```bash
#!/bin/bash
# Systematic Debugging - Information Gathering

gather_debug_info() {
    echo "=== Issue Reproduction Information ==="
    echo ""

    # 1. Error logs (use Grep, not cat)
    echo "Recent error logs:"
    if [ -d "logs" ]; then
        grep -i "error\|exception\|fatal" logs/*.log 2>/dev/null | tail -20 || echo "  No errors in logs"
    fi

    # 2. Git status (what changed recently)
    echo ""
    echo "Recent changes:"
    git log --oneline --since="3 days ago" | head -10 || echo "  Not a git repository"

    # 3. Environment info
    echo ""
    echo "Environment:"
    if [ -f "package.json" ]; then
        echo "  Node: $(node --version 2>/dev/null || echo 'not installed')"
        echo "  NPM: $(npm --version 2>/dev/null || echo 'not installed')"
    elif [ -f "requirements.txt" ]; then
        echo "  Python: $(python --version 2>/dev/null || echo 'not installed')"
    fi

    # 4. System resources
    echo ""
    echo "System resources:"
    echo "  Memory: $(free -h 2>/dev/null | grep Mem | awk '{print $3 "/" $2}' || echo 'N/A')"
    echo "  Disk: $(df -h . 2>/dev/null | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}' || echo 'N/A')"

    # 5. Running processes (if server issue)
    echo ""
    echo "Relevant processes:"
    ps aux | grep -E "node|python|java" | grep -v grep | head -5 || echo "  No relevant processes"
}

gather_debug_info > debug/initial-state.log
cat debug/initial-state.log
```

**Reproduction Steps:**

```bash
#!/bin/bash
# Create reproducible test case

create_reproduction() {
    cat > debug/reproduction.sh << 'EOF'
#!/bin/bash
# Minimal reproduction script

echo "=== Bug Reproduction Steps ==="
echo ""
echo "Step 1: Setup environment"
# TODO: Add setup commands

echo "Step 2: Execute actions that trigger bug"
# TODO: Add trigger commands

echo "Step 3: Verify bug occurs"
# TODO: Add verification

echo ""
echo "Expected: [describe expected behavior]"
echo "Actual: [describe actual behavior]"
EOF

    chmod +x debug/reproduction.sh
    echo "Created reproduction script: debug/reproduction.sh"
}

create_reproduction
```

## Phase 2: Hypothesis Formation

I'll formulate testable hypotheses about the root cause:

**Hypothesis Generation Framework:**

```markdown
# Debugging Plan - [timestamp]

## Issue Description
**Summary**: [brief description]
**Severity**: Critical | High | Medium | Low
**Impact**: [affected users/systems]
**Frequency**: Always | Intermittent | Rare

## Error Details
```
[Full error message/stack trace]
```

## Environment
- **Platform**: [OS, runtime version]
- **Configuration**: [relevant settings]
- **Recent Changes**: [commits/deployments]

## Hypotheses (Prioritized)

### Hypothesis 1: [Most likely cause] - PRIORITY: HIGH
**Theory**: [explanation of suspected cause]
**Evidence**: [supporting observations]
**Test**: [how to verify/disprove]
**Expected**: [what should happen if correct]
**Result**: [ ] Pending | [ ] Confirmed | [ ] Disproved

### Hypothesis 2: [Second most likely] - PRIORITY: MEDIUM
**Theory**: [explanation]
**Evidence**: [observations]
**Test**: [verification method]
**Expected**: [expected outcome]
**Result**: [ ] Pending | [ ] Confirmed | [ ] Disproved

### Hypothesis 3: [Alternative cause] - PRIORITY: LOW
**Theory**: [explanation]
**Evidence**: [observations]
**Test**: [verification method]
**Expected**: [expected outcome]
**Result**: [ ] Pending | [ ] Confirmed | [ ] Disproved

## Investigation Log
- [timestamp]: Initial reproduction successful
- [timestamp]: Hypothesis 1 testing in progress
```

**Hypothesis Prioritization:**
1. **Recent changes** - Check git history
2. **Common patterns** - Known bug categories
3. **Environment issues** - Dependencies, config
4. **Logic errors** - Code analysis
5. **External factors** - Third-party services

## Phase 3: Systematic Testing

I'll test each hypothesis methodically:

**Testing Framework:**

```bash
#!/bin/bash
# Hypothesis Testing Script

test_hypothesis() {
    local hypothesis_num="$1"
    local test_description="$2"

    echo "=== Testing Hypothesis $hypothesis_num ==="
    echo "Test: $test_description"
    echo ""

    # Create checkpoint before testing
    git stash push -m "Debug checkpoint before hypothesis $hypothesis_num"

    # Run test
    local result="PENDING"

    # Log result
    echo "[$hypothesis_num] $test_description: $result" >> debug/test-results.log
}

# Example: Test hypothesis about missing dependency
test_dependency_hypothesis() {
    echo "Hypothesis: Missing or incompatible dependency"

    # Check dependency versions
    if [ -f "package.json" ]; then
        echo "Checking npm dependencies..."
        npm list --depth=0 2>&1 | grep -i "missing\|error" && {
            echo "❌ CONFIRMED: Missing dependencies detected"
            return 0
        }
    fi

    echo "✓ DISPROVED: All dependencies present"
    return 1
}

# Example: Test hypothesis about race condition
test_race_condition_hypothesis() {
    echo "Hypothesis: Race condition in async code"

    # Add delays to test timing sensitivity
    echo "Running test with delays..."
    # TODO: Add test with deliberate delays

    echo "Running test rapidly..."
    for i in {1..10}; do
        # TODO: Run test in tight loop
        true
    done
}

# Test each hypothesis in priority order
test_dependency_hypothesis
test_race_condition_hypothesis
```

**Binary Search Debugging:**

```bash
#!/bin/bash
# Binary search through git history to find regression

git_bisect_debug() {
    echo "=== Git Bisect Debugging ==="

    # Find last known good commit
    read -p "Enter last known good commit (or tag): " good_commit
    read -p "Enter first known bad commit (or 'HEAD'): " bad_commit

    git bisect start
    git bisect bad $bad_commit
    git bisect good $good_commit

    cat > debug/bisect-test.sh << 'EOF'
#!/bin/bash
# Automated bisect test script

# Run test
npm test || exit 1  # Exit 1 if bad, 0 if good

# Or manual verification
echo "Test the current commit and press:"
echo "  g - if this commit is good"
echo "  b - if this commit is bad"
read -n 1 response
[ "$response" = "g" ] && exit 0 || exit 1
EOF

    chmod +x debug/bisect-test.sh
    echo "Run: git bisect run ./debug/bisect-test.sh"
}
```

## Phase 4: Isolation & Simplification

I'll create minimal test cases:

**Issue Isolation:**

```bash
#!/bin/bash
# Create minimal reproducible example

create_minimal_reproduction() {
    local issue_type="$1"

    mkdir -p debug/minimal-case

    case $issue_type in
        "api")
            cat > debug/minimal-case/test.js << 'EOF'
// Minimal API test case
const fetch = require('node-fetch');

async function testIssue() {
    const response = await fetch('http://localhost:3000/api/endpoint');
    const data = await response.json();
    console.log('Response:', data);
    // Add assertion that fails
}

testIssue().catch(console.error);
EOF
            ;;

        "frontend")
            cat > debug/minimal-case/test.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Minimal Test Case</title>
</head>
<body>
    <button id="testBtn">Click to trigger issue</button>
    <div id="output"></div>

    <script>
        document.getElementById('testBtn').addEventListener('click', () => {
            // Minimal code to reproduce issue
            console.log('Testing...');
        });
    </script>
</body>
</html>
EOF
            ;;

        "database")
            cat > debug/minimal-case/test.sql << 'EOF'
-- Minimal database query to reproduce issue
BEGIN TRANSACTION;

-- Setup test data
CREATE TEMP TABLE test_data (id INT, value TEXT);
INSERT INTO test_data VALUES (1, 'test');

-- Query that demonstrates issue
SELECT * FROM test_data WHERE condition;

ROLLBACK;
EOF
            ;;
    esac

    echo "Created minimal test case in debug/minimal-case/"
}
```

## Phase 5: Solution Implementation

Once root cause is identified, I'll implement the fix:

**Fix Validation:**

```bash
#!/bin/bash
# Validate fix before committing

validate_fix() {
    echo "=== Fix Validation ==="

    # 1. Run original reproduction - should now pass
    echo "Step 1: Run original reproduction..."
    if [ -f "debug/reproduction.sh" ]; then
        ./debug/reproduction.sh && echo "✓ Original issue resolved" || {
            echo "❌ Issue still reproduces"
            return 1
        }
    fi

    # 2. Run full test suite
    echo "Step 2: Run test suite..."
    npm test 2>&1 | tee debug/post-fix-tests.log

    # 3. Check for regressions
    echo "Step 3: Check for regressions..."
    git diff HEAD -- . | grep -E "^\+" | grep -v "^+++" | head -20

    # 4. Verify no new errors
    echo "Step 4: Lint check..."
    npm run lint 2>&1 | grep -i "error" && {
        echo "⚠️  New linting errors introduced"
    } || echo "✓ No new linting errors"

    echo ""
    echo "✓ Fix validation complete"
}

validate_fix
```

**Fix Documentation:**

```markdown
## Solution

### Root Cause
[Detailed explanation of what caused the issue]

### Fix Applied
[Description of the solution]

```diff
// Before
- problematic code

// After
+ corrected code
```

### Verification
- [x] Original reproduction no longer triggers issue
- [x] All tests passing
- [x] No regressions introduced
- [x] Edge cases handled

### Prevention
[How to prevent similar issues in the future]
- Add test coverage for [scenario]
- Update validation to catch [condition]
- Add monitoring for [metric]
```

## Phase 6: Regression Prevention

I'll add safeguards to prevent recurrence:

**Test Addition:**

```bash
#!/bin/bash
# Add regression test

add_regression_test() {
    local test_framework="$1"

    case $test_framework in
        "jest")
            cat >> tests/regression.test.js << 'EOF'

describe('Regression: [Issue Description]', () => {
  test('should not reproduce issue #123', async () => {
    // Reproduce the scenario that previously failed
    const result = await functionThatHadBug();

    // Assert correct behavior
    expect(result).toBe(expectedValue);
  });
});
EOF
            ;;

        "pytest")
            cat >> tests/test_regression.py << 'EOF'

def test_issue_123_regression():
    """Regression test for [issue description]"""
    # Reproduce the scenario
    result = function_that_had_bug()

    # Assert correct behavior
    assert result == expected_value
EOF
            ;;
    esac

    echo "Added regression test to prevent future occurrence"
}
```

## Context Continuity

**Session Resume:**
When you return and run `/debug-systematic` or `/debug-systematic resume`:
- Load debugging plan and hypothesis results
- Show which hypotheses have been tested
- Continue from next untested hypothesis
- Track full debugging timeline

**Progress Example:**
```
RESUMING DEBUGGING SESSION
├── Issue: API timeout on user search
├── Hypotheses: 5 total
├── Tested: 3 (2 disproved, 1 confirmed)
├── Current: Testing database query optimization
└── Status: Root cause identified

Continuing investigation...
```

## Practical Examples

**Start Debugging:**
```
/debug-systematic "API returns 500 on POST /users"
/debug-systematic reproduce    # Create reproduction steps
/debug-systematic             # Auto-resume if session exists
```

**Hypothesis Testing:**
```
/debug-systematic test 1      # Test specific hypothesis
/debug-systematic isolate     # Create minimal reproduction
/debug-systematic bisect      # Git bisect to find regression
```

**Session Control:**
```
/debug-systematic resume      # Continue debugging
/debug-systematic status      # Show current progress
/debug-systematic solved      # Mark as solved and summarize
```

## Debugging Techniques

**Common Debugging Patterns:**

1. **Print Debugging:**
```bash
add_debug_logging() {
    echo "Adding strategic debug points..."
    # Add before suspected issue
    # Add after suspected issue
    # Compare outputs
}
```

2. **Rubber Duck Debugging:**
```markdown
## Explain to Rubber Duck
1. What the code should do: [expected behavior]
2. What the code actually does: [actual behavior]
3. Step-by-step execution: [trace through]
4. Where it diverges: [AHA moment]
```

3. **Divide and Conquer:**
```bash
# Comment out half the code
# Does issue persist?
# - Yes: Issue in remaining half
# - No: Issue in commented half
# Repeat until isolated
```

## Safety Guarantees

**Protection Measures:**
- Git checkpoints before each test
- Automated state restoration
- No destructive operations without confirmation
- Clear rollback paths

**Important:** I will NEVER:
- Modify production code without validation
- Skip hypothesis testing
- Apply fixes without verification
- Add AI attribution

## Skill Integration

When appropriate, I may suggest:
- `/test` - Run comprehensive test suite
- `/security-scan` - Check if bug is security-related
- `/commit` - Commit fix with clear message

## Advanced Debugging Tools

**Performance Profiling:**
```bash
profile_performance() {
    # Node.js profiling
    node --prof app.js
    node --prof-process isolate-*.log > profile.txt

    # Python profiling
    python -m cProfile -o profile.stats script.py
    python -m pstats profile.stats
}
```

**Memory Leak Detection:**
```bash
detect_memory_leak() {
    # Monitor memory over time
    while true; do
        ps aux | grep node | awk '{print $6}' | head -1
        sleep 5
    done | tee memory.log

    # Analyze pattern
    gnuplot << 'EOF'
set terminal png
set output 'memory-usage.png'
plot 'memory.log' with lines
EOF
}
```

**Network Debugging:**
```bash
debug_network() {
    # Capture network traffic
    tcpdump -i any -w debug/network.pcap port 3000

    # Analyze with tshark
    tshark -r debug/network.pcap -Y "http.response.code >= 400"
}
```

## What I'll Actually Do

1. **Gather information** - Comprehensive context using Grep
2. **Reproduce issue** - Create reliable reproduction
3. **Form hypotheses** - Prioritized theories about cause
4. **Test systematically** - Validate each hypothesis
5. **Isolate problem** - Minimal reproducible case
6. **Implement fix** - Targeted solution
7. **Prevent regression** - Add tests and monitoring

I'll maintain complete debugging session continuity, tracking all hypotheses and results across sessions.

**Credits:** Systematic debugging methodology based on scientific method and debugging best practices from "Debugging: The 9 Indispensable Rules" by David Agans.
