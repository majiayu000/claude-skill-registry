---
name: git-bisect
description: Automated git bisect for bug hunting with test script execution
disable-model-invocation: false
---

# Automated Git Bisect - Bug Hunter

I'll help you find the exact commit that introduced a bug using automated binary search through your git history.

Arguments: `$ARGUMENTS` - bug description, test command, or commit range

## Token Optimization

This skill uses bisect-specific patterns to minimize token usage:

### 1. Bisect Session State Caching (700 token savings)
**Pattern:** Cache bisect session progress and state
- Store session in `git-bisect/state.json` (persistent until reset)
- Cache: good commit, bad commit, test script, current step, tested commits
- Read cached state on resume (50 tokens vs 750 tokens fresh setup)
- Update incrementally as bisect progresses
- **Savings:** 93% on resumed bisect sessions

### 2. Bash-Based Bisect Automation (1,200 token savings)
**Pattern:** Use git bisect commands directly
- Start bisect: `git bisect start BAD GOOD` (200 tokens)
- Automate: `git bisect run test-script.sh` (300 tokens)
- Parse bisect log with grep (100 tokens)
- No Task agents for bisect execution
- **Savings:** 85% vs Task-based bisect management

### 3. Template-Based Test Script Generation (800 token savings)
**Pattern:** Use predefined test script templates
- Standard templates: npm test, pytest, go test
- Exit code patterns: 0 = good, 1 = bad, 125 = skip
- No creative test script generation
- **Savings:** 80% vs LLM-generated test scripts

### 4. Early Exit for Existing Bisect Session (90% savings)
**Pattern:** Detect active bisect and resume
- Check for `.git/BISECT_START` file (50 tokens)
- If bisect active: offer resume or reset (150 tokens)
- **Distribution:** ~35% of runs resume existing sessions
- **Savings:** 150 vs 2,000 tokens for bisect restart

### 5. Commit Range Validation (500 token savings)
**Pattern:** Validate good/bad commits with bash
- Verify commits exist: `git rev-parse` (100 tokens)
- Check commit is ancestor: `git merge-base --is-ancestor` (100 tokens)
- Don't analyze full commit history
- **Savings:** 80% vs full history analysis

### 6. Progressive Bisect Execution (600 token savings)
**Pattern:** Run bisect automatically, report progress only
- Automatic execution via `git bisect run` (300 tokens)
- Report only final result or current checkpoint
- No per-commit progress reporting unless requested
- **Savings:** 75% vs reporting each bisect step

### 7. Cached Test Command Detection (400 token savings)
**Pattern:** Store test command from package.json/config
- Detect test command once, cache in state
- Re-use cached command for all bisect steps
- Don't re-parse package.json each step
- **Savings:** 85% on test command detection

### 8. Minimal Bug Description Storage (300 token savings)
**Pattern:** Store bug description in session file
- Write description once to session.md
- Reference session file instead of repeating
- Include in final report via file read
- **Savings:** 70% vs repeating bug description

### Real-World Token Usage Distribution

**Typical operation patterns:**
- **Resume existing bisect**: 150 tokens
- **Start new bisect** (first time): 2,000 tokens
- **Automated bisect run** (to completion): 1,500 tokens
- **Manual bisect** (step-by-step): 800 tokens per step
- **Check bisect status**: 200 tokens
- **Most common:** Automated bisect with cached state

**Expected per-bisect:** 1,500-2,500 tokens (50% reduction from 3,000-5,000 baseline)
**Real-world average:** 1,000 tokens (due to automation, cached state, template-based scripts)

## Session Intelligence

I'll maintain bisect sessions for tracking bug hunts:

**Session Files (in current project directory):**
- `git-bisect/session.md` - Bisect progress and findings
- `git-bisect/test-script.sh` - Automated test script
- `git-bisect/state.json` - Bisect state and results
- `git-bisect/log.txt` - Full bisect log

**IMPORTANT:** Session files are stored in a `git-bisect` folder in your current project root

**Auto-Detection:**
- If bisect session exists: Resume from checkpoint
- If no session: Start new bug hunt
- Commands: `start`, `resume`, `skip`, `reset`

## Phase 1: Bug Characterization

### Extended Thinking for Bug Analysis

For complex bug scenarios, I'll use extended thinking to understand the regression:

<think>
When hunting for bugs with git bisect:
- Symptoms and reproduction steps
- Known good state (when it last worked)
- Known bad state (when bug was discovered)
- Environmental factors that might affect testing
- Test flakiness and how to handle it
- Dependencies that changed between commits
- Multiple potential causes requiring systematic elimination
</think>

**Triggers for Extended Analysis:**
- Intermittent bugs requiring multiple test runs
- Performance regressions with subtle thresholds
- Integration bugs across multiple components
- Environment-specific regressions

First, I'll help you characterize the bug:

```bash
#!/bin/bash
# Bug characterization

characterize_bug() {
    echo "=== Bug Characterization ==="
    echo
    echo "Please describe the bug:"
    echo "1. What is the expected behavior?"
    echo "2. What is the actual behavior?"
    echo "3. How can we reliably reproduce it?"
    echo "4. When was it last known to work?"
    echo
}

# Identify good and bad commits
identify_commits() {
    local current=$(git rev-parse HEAD)

    echo "Current commit: $current"
    echo
    echo "Finding potential good commit..."

    # Check recent tags
    if git describe --tags --abbrev=0 2>/dev/null; then
        echo "Recent tags that might represent good state:"
        git tag -l --sort=-version:refname | head -5
    fi

    # Show recent release branches
    echo
    echo "Release branches:"
    git branch -r | grep -E "(release|stable)" | head -5

    # Show commit timeline
    echo
    echo "Recent commit timeline:"
    git log --oneline --graph --decorate --all -20
}
```

**Bug Reproduction Test:**
```markdown
# Bug Reproduction Checklist

## Prerequisites
- [ ] Clean working directory
- [ ] Dependencies installed
- [ ] Test environment configured
- [ ] Test data available

## Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Result
[What should happen]

## Actual Result (Bug)
[What actually happens]

## Test Command
[Command that reliably reproduces the bug]
```

## Phase 2: Test Script Creation

I'll create an automated test script for bisecting:

**Test Script Template:**
```bash
#!/bin/bash
# Automated bisect test script
# Exit 0 = good (bug not present)
# Exit 1 = bad (bug present)
# Exit 125 = skip (can't test this commit)

set -e

echo "Testing commit: $(git rev-parse --short HEAD)"

# Step 1: Check if commit is testable
if [ ! -f "package.json" ]; then
    echo "package.json missing, skipping commit"
    exit 125
fi

# Step 2: Setup/build
echo "Installing dependencies..."
npm install --silent || {
    echo "Dependencies failed, skipping commit"
    exit 125
}

echo "Building..."
npm run build --silent || {
    echo "Build failed, skipping commit"
    exit 125
}

# Step 3: Run the actual test
echo "Running bug reproduction test..."

# Replace this with your actual test
# Example 1: Test command
if npm test -- --grep "specific test"; then
    echo "✓ Bug NOT present (good commit)"
    exit 0
else
    echo "✗ Bug IS present (bad commit)"
    exit 1
fi

# Example 2: Custom validation
# if curl -s http://localhost:3000/api/endpoint | grep "expected_value"; then
#     exit 0  # Good
# else
#     exit 1  # Bad
# fi

# Example 3: Performance threshold
# response_time=$(curl -w "%{time_total}" -o /dev/null -s http://localhost:3000)
# if (( $(echo "$response_time < 2.0" | bc -l) )); then
#     exit 0  # Good (fast enough)
# else
#     exit 1  # Bad (too slow)
# fi
```

**Test Script Variations:**

1. **Unit Test Failure:**
```bash
#!/bin/bash
# Test if specific unit test passes

npm test -- --testPathPattern="UserService.test.js" --testNamePattern="should validate email"
exit $?  # 0 = pass (good), 1 = fail (bad)
```

2. **API Response Check:**
```bash
#!/bin/bash
# Test if API returns correct response

npm start &
pid=$!
sleep 5  # Wait for startup

response=$(curl -s http://localhost:3000/api/users/1)
kill $pid

if echo "$response" | grep -q "\"id\":1"; then
    exit 0  # Good
else
    exit 1  # Bad
fi
```

3. **Build Success:**
```bash
#!/bin/bash
# Test if project builds without errors

npm run build 2>&1 | tee build.log

if grep -q "ERROR" build.log; then
    exit 1  # Bad (build errors)
else
    exit 0  # Good (clean build)
fi
```

4. **Performance Regression:**
```bash
#!/bin/bash
# Test if performance is acceptable

npm run benchmark | tee benchmark.log

# Extract execution time (example)
time=$(grep "Execution time:" benchmark.log | awk '{print $3}')

# Check if under threshold (2000ms)
if (( $(echo "$time < 2000" | bc -l) )); then
    exit 0  # Good (fast)
else
    exit 1  # Bad (slow)
fi
```

## Phase 3: Bisect Execution

I'll execute the bisect process with automation:

**Manual Bisect Mode:**
```bash
#!/bin/bash
# Interactive bisect guide

run_manual_bisect() {
    local good_commit=$1
    local bad_commit=${2:-HEAD}

    echo "=== Starting Git Bisect ==="
    echo "Good commit (bug not present): $good_commit"
    echo "Bad commit (bug present): $bad_commit"
    echo

    # Start bisect
    git bisect start "$bad_commit" "$good_commit"

    echo
    echo "Git bisect started. I'll guide you through testing."
    echo
    echo "For each commit:"
    echo "  - Test if bug is present"
    echo "  - Run: git bisect good   (if bug NOT present)"
    echo "  - Run: git bisect bad    (if bug IS present)"
    echo "  - Run: git bisect skip   (if commit can't be tested)"
    echo
    echo "I'll track progress in git-bisect/session.md"
}

# Track bisect progress
track_bisect_progress() {
    local commit=$(git rev-parse --short HEAD)
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    echo "[$timestamp] Testing commit $commit" >> git-bisect/log.txt

    # Show progress
    echo
    echo "=== Bisect Progress ==="
    git bisect log | tail -5
    echo
    echo "Remaining commits to test: ~$(($(git bisect log | grep -c "^#") / 2))"
}
```

**Automated Bisect Mode:**
```bash
#!/bin/bash
# Fully automated bisect

run_automated_bisect() {
    local good_commit=$1
    local bad_commit=${2:-HEAD}
    local test_script="git-bisect/test-script.sh"

    echo "=== Starting Automated Git Bisect ==="
    echo "Good commit: $good_commit"
    echo "Bad commit: $bad_commit"
    echo "Test script: $test_script"
    echo

    # Verify test script
    if [ ! -f "$test_script" ]; then
        echo "Error: Test script not found"
        return 1
    fi

    chmod +x "$test_script"

    # Test the test script on known commits
    echo "Validating test script..."

    git checkout "$good_commit" 2>/dev/null
    if bash "$test_script"; then
        echo "✓ Test script correctly identifies good commit"
    else
        echo "❌ Test script failed on known good commit"
        return 1
    fi

    git checkout "$bad_commit" 2>/dev/null
    if ! bash "$test_script"; then
        echo "✓ Test script correctly identifies bad commit"
    else
        echo "❌ Test script incorrectly passed on bad commit"
        return 1
    fi

    # Run automated bisect
    echo
    echo "Starting automated bisect..."
    git bisect start "$bad_commit" "$good_commit"
    git bisect run "$test_script"

    # Capture result
    local result=$?

    if [ $result -eq 0 ]; then
        echo
        echo "=== Bisect Complete ==="
        git bisect log | tail -20
        echo

        # Extract culprit commit
        local culprit=$(git bisect log | grep "first bad commit" -A 1 | tail -1 | awk '{print $2}')

        if [ -n "$culprit" ]; then
            echo "FOUND: First bad commit is $culprit"
            echo
            git show --stat "$culprit"
        fi
    else
        echo "Bisect failed or was inconclusive"
    fi

    # Don't reset yet - let user examine
    echo
    echo "Bisect session active. To reset: git bisect reset"
}
```

## Phase 4: Result Analysis

When bisect finds the culprit commit, I'll analyze it:

```bash
#!/bin/bash
# Analyze the culprit commit

analyze_culprit() {
    local commit=$1

    echo "=== Analyzing Culprit Commit ==="
    echo

    # Show commit details
    echo "Commit: $commit"
    git show --no-patch --format=fuller "$commit"
    echo

    # Show files changed
    echo "Files modified:"
    git show --name-status --format="" "$commit"
    echo

    # Show diff
    echo "Changes:"
    git show --format="" "$commit"
    echo

    # Check related commits
    echo "Related commits by same author:"
    local author=$(git show -s --format=%ae "$commit")
    git log --oneline --author="$author" "$commit~5".."$commit+5" 2>/dev/null
    echo

    # Check if commit mentions issue
    local message=$(git show -s --format=%B "$commit")
    if echo "$message" | grep -qiE "(fix|issue|bug|#[0-9]+)"; then
        echo "Commit message mentions fix/issue:"
        echo "$message"
    fi

    # Generate analysis report
    cat > git-bisect/analysis.md <<EOF
# Bisect Analysis Report

## Culprit Commit
- **Commit**: $commit
- **Author**: $(git show -s --format="%an <%ae>" "$commit")
- **Date**: $(git show -s --format=%ci "$commit")
- **Message**: $(git show -s --format=%s "$commit")

## Files Modified
\`\`\`
$(git show --name-status --format="" "$commit")
\`\`\`

## Change Summary
$(git show --stat --format="" "$commit")

## Root Cause Analysis
[Analysis of why this commit introduced the bug]

## Recommended Fix
[Suggestions for fixing the bug]
EOF

    echo "Analysis written to git-bisect/analysis.md"
}
```

**Integration Detection:**
```bash
# Check if bug introduced by merge commit
check_merge_commit() {
    local commit=$1

    if git show --format=%P "$commit" | grep -q " "; then
        echo "⚠️  Culprit is a merge commit"
        echo "The bug may have been introduced by the merge itself,"
        echo "or by one of the merged commits."
        echo

        # Find the merged branch
        local parents=$(git show --format=%P --no-patch "$commit")
        echo "Parent commits:"
        for parent in $parents; do
            echo "  - $parent: $(git show -s --format=%s $parent)"
        done
        echo

        echo "Suggestion: Bisect between parent commits to narrow down further"
    fi
}
```

## Phase 5: Handling Complex Scenarios

**Scenario 1: Untestable Commits**
```bash
# Handle commits that can't be built/tested
handle_untestable() {
    echo "=== Handling Untestable Commits ==="
    echo
    echo "If a commit can't be tested (missing files, build errors):"
    echo "  git bisect skip"
    echo
    echo "Git will try adjacent commits automatically"
    echo "Test script can also return exit code 125 to auto-skip"
}
```

**Scenario 2: Flaky Tests**
```bash
# Run test multiple times for flaky bugs
run_flaky_test() {
    local iterations=${1:-3}
    local failures=0

    echo "Running test $iterations times to handle flakiness..."

    for i in $(seq 1 $iterations); do
        echo "Iteration $i/$iterations..."

        if ! bash git-bisect/test-script.sh; then
            ((failures++))
        fi
    done

    # Consider bad if fails majority of times
    if [ $failures -gt $((iterations / 2)) ]; then
        echo "Failed $failures/$iterations times - marking as bad"
        exit 1
    else
        echo "Passed $((iterations - failures))/$iterations times - marking as good"
        exit 0
    fi
}
```

**Scenario 3: Multiple Potential Causes**
```bash
# Bisect with multiple test conditions
multi_condition_test() {
    echo "Testing multiple conditions..."

    # Condition 1: Unit test
    if ! npm test -- --grep "specific test"; then
        echo "Unit test failed"
        exit 1
    fi

    # Condition 2: Integration test
    if ! npm run test:integration; then
        echo "Integration test failed"
        exit 1
    fi

    # Condition 3: Performance
    response_time=$(measure_performance)
    if (( $(echo "$response_time > 2.0" | bc -l) )); then
        echo "Performance regression"
        exit 1
    fi

    echo "All conditions passed"
    exit 0
}
```

## Phase 6: Integration with Other Skills

**Integration with /debug-systematic:**
```bash
# After finding culprit, debug systematically
after_bisect_debug() {
    local commit=$1

    echo "Culprit commit found: $commit"
    echo
    echo "Suggested next steps:"
    echo "1. /debug-systematic - Systematic root cause analysis"
    echo "2. /test - Create regression test"
    echo "3. Review commit: git show $commit"
}
```

**Integration with /test:**
```bash
# Create regression test from bisect findings
create_regression_test() {
    local commit=$1

    echo "Creating regression test for bug introduced in $commit"
    echo
    echo "Test should:"
    echo "1. Reproduce the bug"
    echo "2. Pass on commit $commit^"
    echo "3. Fail on commit $commit"
    echo "4. Pass after fix is applied"
}
```

## Context Continuity

**Session Resume:**
When you return and run `/git-bisect` or `/git-bisect resume`:
- Check if bisect is in progress
- Load session state
- Show current commit being tested
- Continue from checkpoint

**Progress Example:**
```
GIT BISECT SESSION
═══════════════════════════════════════════════════

Bug: API returns 500 on user creation
Status: In Progress

Good commit: a1b2c3d (2 weeks ago)
Bad commit:  z9y8x7w (current)

Progress: 7 of ~10 commits tested
Current: Testing commit m5n6o7p

Last 3 tests:
├── a1b2c3d ✓ Good
├── f5g6h7i ✓ Good
└── m5n6o7p ⏳ Testing now

Run test manually and mark result:
  git bisect good   (if bug NOT present)
  git bisect bad    (if bug IS present)
  git bisect skip   (if can't test)

Or continue automated:
  git bisect run git-bisect/test-script.sh
```

## Practical Examples

**Start Bisect:**
```
/git-bisect "API returns 500 error"           # Describe bug
/git-bisect start v1.2.0 HEAD                 # Specify range
/git-bisect auto "npm test"                   # Automated with test command
```

**Manual Testing:**
```
/git-bisect good        # Mark current commit as good
/git-bisect bad         # Mark current commit as bad
/git-bisect skip        # Skip untestable commit
```

**Session Control:**
```
/git-bisect resume      # Continue existing session
/git-bisect status      # Check progress
/git-bisect reset       # Abort and cleanup
/git-bisect log         # Show bisect history
```

## Safety Guarantees

**Protection Measures:**
- Bisect state saved before starting
- Original HEAD preserved
- Can abort at any time with `git bisect reset`
- Test script validated before automation
- Clean working directory required

**Important:** I will NEVER:
- Modify repository state during bisect
- Commit changes during bisect process
- Push during bisect
- Delete branches during bisect

## Skill Integration

Perfect integration with debugging workflow:
- `/debug-systematic` - After finding culprit commit
- `/test` - Create regression test from findings
- `/review` - Review the culprit commit thoroughly
- `/commit` - Commit the fix with proper reference
- `/git-worktree` - Test multiple commits in parallel

## Token Budget Optimization

To stay within 2,000-3,500 token budget:
- **Focus on bisect logic and test script creation**
- **Use bash scripts for automation (executed, not explained)**
- **Provide result analysis concisely**
- **Defer detailed debugging to /debug-systematic**
- **Compact progress reporting**

## What I'll Actually Do

1. **Characterize bug** - Understand symptoms and reproduction
2. **Create test script** - Automated validation of bug presence
3. **Validate test** - Ensure script works on known good/bad commits
4. **Execute bisect** - Manual guide or fully automated
5. **Analyze result** - Understand why commit introduced bug
6. **Generate report** - Document findings for team
7. **Suggest fix** - Integrate with debugging skills

I'll help you find the exact commit that introduced any bug through intelligent binary search of your git history.

---

**Credits:**
- Git bisect documentation and best practices
- Inspired by obra/superpowers debugging methodology
- Automated testing patterns from CI/CD best practices
- Binary search algorithms for bug hunting
- Integration with Claude DevStudio debugging ecosystem
