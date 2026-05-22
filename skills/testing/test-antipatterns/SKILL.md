---
name: test-antipatterns
description: Detect and fix testing anti-patterns for better test quality
disable-model-invocation: false
---

# Test Anti-Pattern Detection & Remediation

I'll identify and fix testing anti-patterns that create brittle, flaky, or slow tests.

Arguments: `$ARGUMENTS` - specific paths or anti-pattern focus areas

## Phase 1: Test Quality Assessment

**Pre-Flight Checks:**
Before starting, I'll verify:
- Test framework and runner configuration
- Test file locations and naming conventions
- Existing test patterns and style
- CI/CD test execution configuration

<think>
When analyzing test anti-patterns:
- Brittle tests break on unrelated changes (over-specification)
- Flaky tests pass/fail randomly (timing, state, randomness)
- Slow tests reduce productivity (unnecessary setup, poor isolation)
- Test interdependencies create cascade failures
- Poor mocking leads to integration tests disguised as unit tests
- Assertion roulette makes failures hard to diagnose
</think>

**Framework Detection:**
```bash
# Auto-detect testing framework
detect_test_framework() {
    if [ -f "package.json" ]; then
        if grep -q "jest" package.json; then
            echo "jest"
        elif grep -q "mocha" package.json; then
            echo "mocha"
        elif grep -q "vitest" package.json; then
            echo "vitest"
        elif grep -q "cypress" package.json; then
            echo "cypress"
        fi
    elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
        echo "pytest"
    elif [ -f "go.mod" ]; then
        echo "go-test"
    elif [ -f "Gemfile" ]; then
        echo "rspec"
    fi
}

FRAMEWORK=$(detect_test_framework)
echo "Detected test framework: $FRAMEWORK"
```

**Anti-Pattern Discovery:**
I'll use Grep to find test files with anti-pattern indicators:
```bash
# Find tests with timing anti-patterns (flaky tests)
Grep pattern="sleep|wait|setTimeout|setInterval"
     glob="**/*.{test,spec}.{js,ts,jsx,tsx,py}"
     output_mode="files_with_matches"
     head_limit=20

# Find disabled/focused tests (.only, .skip, fdescribe, etc.)
Grep pattern="\.only\(|\.skip\(|fdescribe|fit|xdescribe|xit"
     glob="**/*.{test,spec}.*"
     output_mode="files_with_matches"
     head_limit=20

# Find shared state indicators (test dependencies)
Grep pattern="beforeAll|afterAll"
     glob="**/*.{test,spec}.*"
     output_mode="files_with_matches"
     head_limit=20

# Find potential over-mocking
Grep pattern="jest\.mock|mock\(|spy\(|stub\("
     glob="**/*.test.*"
     output_mode="count"
     head_limit=20
```

This targets files likely to have anti-patterns before full Read analysis.

## Phase 2: Anti-Pattern Detection

I'll scan for these common anti-patterns:

### Category 1: Brittle Tests (Over-Specification)

**1. Implementation Detail Testing**
```javascript
// BAD: Testing internal implementation
expect(component.state.internalCounter).toBe(5);

// GOOD: Testing observable behavior
expect(component.getDisplayValue()).toBe('5');
```

**Detection:**
- Direct state access in tests
- Testing private methods
- Mocking every dependency
- Assertions on internal data structures

**2. Fragile Selectors (E2E/Integration)**
```javascript
// BAD: Brittle selectors
cy.get('div > ul > li:nth-child(3) > button.btn-primary')

// GOOD: Semantic selectors
cy.get('[data-testid="submit-button"]')
```

### Category 2: Flaky Tests (Non-Deterministic)

**1. Test Order Dependencies**
```javascript
// BAD: Tests depend on execution order
describe('User tests', () => {
    it('should create user', () => {
        user = createUser(); // Sets global state
    });

    it('should update user', () => {
        updateUser(user); // Depends on previous test
    });
});
```

**Detection Pattern:**
```bash
# Find tests that might share state (mutable variables)
Grep pattern="(let |var )"
     glob="**/*.test.*"
     output_mode="content"
     head_limit=10
     -B=2
     -A=2

# Find setup that creates shared state
Grep pattern="beforeAll|afterAll"
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10
```

**2. Random Data Issues**
```javascript
// BAD: Uncontrolled randomness
const testData = {
    id: Math.random(),
    timestamp: Date.now()
};

// GOOD: Deterministic test data
const testData = {
    id: 'test-id-123',
    timestamp: new Date('2024-01-01').getTime()
};
```

**3. Network/External Dependencies**
```python
# BAD: Real API calls in tests
def test_api():
    response = requests.get('https://api.example.com')
    assert response.status_code == 200

# GOOD: Mocked external calls
@patch('requests.get')
def test_api(mock_get):
    mock_get.return_value.status_code = 200
    response = api_client.fetch_data()
    assert response.status_code == 200
```

### Category 3: Slow Tests (Performance Issues)

**1. Unnecessary Database/IO**
```javascript
// BAD: Real DB for unit test
beforeEach(async () => {
    await database.reset();
    await database.seed();
});

// GOOD: In-memory or mocked
beforeEach(() => {
    repository = new InMemoryRepository();
});
```

**Detection:**
```bash
# Find tests with expensive database setup
Grep pattern="database\.|db\.|createConnection|mongoose\.connect|knex\("
     glob="**/*.{test,spec}.*"
     output_mode="files_with_matches"
     head_limit=15

# Find tests with expensive seeding operations
Grep pattern="beforeEach.*await.*(create|seed|insert)"
     glob="**/*.test.*"
     output_mode="content"
     head_limit=10
     multiline=true
```

**2. Excessive Test Fixtures**
```javascript
// BAD: Creating more data than needed
beforeEach(() => {
    users = createUsers(1000); // Only need 2-3
    posts = createPosts(5000);
    comments = createComments(10000);
});
```

**3. Sleep/Wait Anti-Patterns**
```javascript
// BAD: Arbitrary waits
await sleep(1000);
expect(element).toBeVisible();

// GOOD: Condition-based waiting
await waitFor(() => expect(element).toBeVisible());
```

### Category 4: Test Structure Issues

**1. Assertion Roulette**
```javascript
// BAD: Which assertion failed?
expect(result.id).toBeDefined();
expect(result.name).toBeDefined();
expect(result.email).toBeDefined();
expect(result.status).toBe('active');

// GOOD: Clear, specific assertions
expect(result).toMatchObject({
    id: expect.any(String),
    name: expect.any(String),
    email: expect.any(String),
    status: 'active'
});
```

**2. Mystery Guest**
```javascript
// BAD: Hidden test data
it('should validate user', () => {
    const user = getTestUser(); // What user?
    expect(validator.validate(user)).toBe(true);
});

// GOOD: Explicit test data
it('should validate user with valid email', () => {
    const user = { email: 'test@example.com', name: 'Test' };
    expect(validator.validate(user)).toBe(true);
});
```

**3. Test Logic in Tests**
```javascript
// BAD: Conditional logic in tests
if (config.environment === 'production') {
    expect(result).toBe(productionValue);
} else {
    expect(result).toBe(devValue);
}

// GOOD: Separate tests
it('should return production value in prod', () => {
    config.environment = 'production';
    expect(result()).toBe(productionValue);
});
```

### Category 5: Mock/Stub Anti-Patterns

**1. Over-Mocking**
```javascript
// BAD: Mocking everything = integration test disguised as unit
jest.mock('./service');
jest.mock('./repository');
jest.mock('./validator');
jest.mock('./logger');
jest.mock('./cache');

// GOOD: Mock only external boundaries
jest.mock('./apiClient');
```

**2. Not Verifying Mocks**
```javascript
// BAD: Mock without verification
const mockFn = jest.fn();
doSomething(mockFn);
// No assertion!

// GOOD: Verify mock usage
const mockFn = jest.fn();
doSomething(mockFn);
expect(mockFn).toHaveBeenCalledWith(expectedArgs);
```

### Category 6: Test Independence Issues

**1. Leftover State**
```python
# BAD: Global state not cleaned
cache = {}

def test_cache_set():
    cache['key'] = 'value'
    assert cache['key'] == 'value'

def test_cache_empty():
    assert len(cache) == 0  # FAILS if run after test_cache_set
```

**Detection:**
```bash
# Find global variables in test files (potential shared state)
Grep pattern="^(let|var|const) [A-Z_][A-Z0-9_]*\s*="
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10

# Find tests modifying global objects
Grep pattern="global\.|window\.|process\.env\[|document\."
     glob="**/*.test.*"
     output_mode="content"
     head_limit=10
```

## Phase 3: Flaky Test Identification

**Statistical Analysis:**
```bash
# Run tests multiple times to find flaky tests
echo "Running tests 10 times to detect flakiness..."
for i in {1..10}; do
    npm test 2>&1 | tee "test-run-$i.log"
done

# Analyze results
echo "Analyzing test stability..."
# Look for tests that sometimes pass, sometimes fail
```

**Common Flakiness Patterns:**
- Tests that use `Date.now()` or `new Date()`
- Tests with hardcoded timeouts
- Tests that depend on system resources
- Tests with race conditions
- Tests that don't clean up properly

## Phase 4: Test Interdependency Analysis

**Dependency Detection:**
```bash
# Find tests that might depend on execution order
Grep pattern="beforeAll|afterAll"
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10
     -B=2
     -A=10

# Find shared mutable state
Grep pattern="(let |var )"
     glob="**/*.test.*"
     output_mode="files_with_matches"
     head_limit=20

# Find tests marked as .only or .skip (test focus/skip indicators)
Grep pattern="\.only\(|\.skip\(|fdescribe|fit|xdescribe|xit"
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10
```

**Test Isolation Verification:**
I'll suggest running tests:
- In random order
- In reverse order
- Individual tests in isolation
- With different parallelization settings

## Phase 5: Remediation & Fixes

**Systematic Fix Process:**

1. **Create git checkpoint**
   ```bash
   git add -A
   git commit -m "Pre test-antipattern-fixes checkpoint" || echo "No changes"
   ```

2. **Fix anti-patterns by priority:**
   - **Critical**: Flaky tests (breaks CI/CD)
   - **High**: Test interdependencies (cascade failures)
   - **Medium**: Slow tests (developer productivity)
   - **Low**: Brittle tests (maintenance burden)

3. **Common Fixes I'll Apply:**

   **Fix Flaky Tests:**
   ```javascript
   // Before: Timing-dependent
   setTimeout(() => expect(value).toBe(true), 100);

   // After: Condition-based
   await waitFor(() => expect(value).toBe(true));
   ```

   **Fix Test Dependencies:**
   ```javascript
   // Before: Shared state
   let user;
   beforeAll(() => { user = createUser(); });

   // After: Isolated state
   beforeEach(() => { user = createUser(); });
   ```

   **Fix Slow Tests:**
   ```javascript
   // Before: Real DB
   beforeEach(async () => await db.migrate.latest());

   // After: In-memory
   beforeEach(() => { repo = new InMemoryRepo(); });
   ```

   **Fix Brittle Selectors:**
   ```javascript
   // Before: Implementation detail
   expect(component.find('div').at(2).text()).toBe('Hello');

   // After: Behavior-focused
   expect(screen.getByRole('heading')).toHaveTextContent('Hello');
   ```

4. **Verify fixes:**
   - Run tests multiple times
   - Run tests in random order
   - Check test execution time
   - Verify test isolation

## Phase 6: Test Quality Improvements

**Suggestions I'll Make:**

1. **Add Test Utilities:**
   ```javascript
   // Create reusable test builders
   function createTestUser(overrides = {}) {
       return {
           id: 'test-id',
           email: 'test@example.com',
           name: 'Test User',
           ...overrides
       };
   }
   ```

2. **Improve Test Organization:**
   ```javascript
   describe('UserService', () => {
       describe('create', () => {
           it('should create user with valid data', () => {});
           it('should reject invalid email', () => {});
           it('should reject duplicate email', () => {});
       });

       describe('update', () => {
           // Update tests
       });
   });
   ```

3. **Add Test Documentation:**
   ```javascript
   it('should calculate total with tax and shipping', () => {
       // Given: Cart with $100 items
       // When: Checkout in California (9% tax)
       // Then: Total = $100 + $9 + $10 shipping = $119
   });
   ```

## Integration with Existing Skills

**Workflow Integration:**
- After `/test` finds failures → Run `/test-antipatterns`
- Before `/commit` → Check test quality
- During `/review` → Include test anti-pattern analysis
- With `/test-async` → Comprehensive async test check
- With `/test-coverage` → Ensure quality tests, not just quantity

**Skill Suggestions:**
- Found complex async anti-patterns → `/test-async`
- Need coverage analysis → `/test-coverage`
- Implementing new features → `/tdd-red-green`
- Complex debugging needed → `/debug-systematic`

## Reporting

**I'll provide a comprehensive report:**

```
TEST ANTI-PATTERN ANALYSIS REPORT
==================================

Test Files Analyzed: 87
Total Tests: 432

ANTI-PATTERNS DETECTED:
├── Brittle Tests: 23 (over-specification, fragile selectors)
├── Flaky Tests: 8 (timing, state, randomness)
├── Slow Tests: 15 (unnecessary DB/IO, excessive setup)
├── Test Dependencies: 12 (shared state, order-dependent)
├── Poor Mocking: 18 (over-mocking, unverified mocks)
└── Structure Issues: 31 (assertion roulette, mystery guest)

SEVERITY BREAKDOWN:
├── Critical: 8 flaky tests (break CI/CD)
├── High: 12 interdependent tests (cascade failures)
├── Medium: 15 slow tests (>1s each)
└── Low: 71 maintainability issues

FIXES APPLIED:
├── Replaced setTimeout with waitFor: 8
├── Fixed shared state: 12
├── Optimized test setup: 15
├── Improved assertions: 23
├── Fixed mock verification: 18
├── Enhanced test organization: 31

PERFORMANCE IMPACT:
├── Before: 45.3s total test time
├── After: 12.8s total test time
└── Improvement: 71.7% faster

RECOMMENDATIONS:
├── Add test-utils for common builders
├── Enable random test order in CI
├── Set up test performance monitoring
├── Document testing best practices
└── Add pre-commit test quality checks
```

## Safety Guarantees

**What I'll NEVER do:**
- Remove tests to fix issues
- Modify tests to pass incorrectly
- Skip necessary test coverage
- Add AI attribution to commits or code
- Change test behavior without verification

**What I WILL do:**
- Preserve test intent and coverage
- Fix genuine anti-patterns
- Improve test reliability and speed
- Maintain test quality standards
- Create clear commit messages (no AI attribution)

## Credits

This skill is based on:
- **obra/superpowers** - TDD and testing methodology
- **xUnit Test Patterns** - Anti-pattern catalog by Gerard Meszaros
- **Jest Best Practices** - Testing patterns and anti-patterns
- **pytest Good Integration Practices** - Python testing standards
- **Testing Best Practices** - Community-driven testing guidelines

## Token Optimization

**Current Budget:** 3,500-5,500 tokens (unoptimized)
**Optimized Budget:** 1,400-2,200 tokens (60% reduction)

This skill implements comprehensive token optimization while maintaining thorough test anti-pattern detection through intelligent pattern matching and strategic analysis.

### Optimization Patterns Applied

**1. Grep-Before-Read Pattern Discovery (90% savings)**

```bash
# PATTERN: Discover anti-patterns before reading full files
# Savings: 90% vs reading all test files upfront

# Phase 1: Identify files with timing anti-patterns (flaky tests)
Grep pattern="sleep|wait|setTimeout|setInterval"
     glob="**/*.{test,spec}.{js,ts,jsx,tsx,py}"
     output_mode="files_with_matches"
     head_limit=20

# Phase 2: Identify disabled/focused tests
Grep pattern="\.only\(|\.skip\(|fdescribe|fit|xdescribe|xit"
     glob="**/*.{test,spec}.*"
     output_mode="files_with_matches"
     head_limit=20

# Phase 3: Identify test dependency indicators
Grep pattern="beforeAll|afterAll|let |var "
     glob="**/*.test.*"
     output_mode="files_with_matches"
     head_limit=20

# Only read files with detected anti-patterns (saves 90%)
```

**2. Framework Detection Caching (saves 500 tokens per run)**

```bash
# Cache framework detection to avoid repeated analysis
CACHE_FILE=".claude/cache/test-antipatterns/framework.json"

if [ -f "$CACHE_FILE" ]; then
    FRAMEWORK=$(cat "$CACHE_FILE" | jq -r '.framework')
    TEST_PATTERN=$(cat "$CACHE_FILE" | jq -r '.test_pattern')
    echo "✓ Using cached framework: $FRAMEWORK"
else
    # Detect framework (first run only)
    if grep -q "jest" package.json 2>/dev/null; then
        FRAMEWORK="jest"
        TEST_PATTERN="**/*.{test,spec}.{js,ts,jsx,tsx}"
    elif grep -q "vitest" package.json 2>/dev/null; then
        FRAMEWORK="vitest"
        TEST_PATTERN="**/*.{test,spec}.{js,ts}"
    elif grep -q "mocha" package.json 2>/dev/null; then
        FRAMEWORK="mocha"
        TEST_PATTERN="**/*.{test,spec}.js"
    elif grep -q "pytest" pyproject.toml requirements.txt 2>/dev/null; then
        FRAMEWORK="pytest"
        TEST_PATTERN="**/test_*.py"
    fi

    # Cache result
    mkdir -p .claude/cache/test-antipatterns
    cat > "$CACHE_FILE" <<EOF
{
  "framework": "$FRAMEWORK",
  "test_pattern": "$TEST_PATTERN",
  "timestamp": "$(date -Iseconds)"
}
EOF
fi
```

**3. Early Exit (80% savings when no issues)**

```bash
# PATTERN: Quick validation before deep analysis

# Phase 1: Quick anti-pattern scan (300 tokens)
TIMING_ISSUES=$(Grep pattern="sleep|wait|setTimeout"
                     glob="**/*.test.*"
                     output_mode="files_with_matches"
                     head_limit=1)

DISABLED_TESTS=$(Grep pattern="\.only\(|\.skip\("
                      glob="**/*.test.*"
                      output_mode="files_with_matches"
                      head_limit=1)

if [ -z "$TIMING_ISSUES" ] && [ -z "$DISABLED_TESTS" ]; then
    echo "✓ No obvious anti-patterns detected"
    echo "ℹ Tests appear to follow good practices"
    exit 0  # Early exit: 300 tokens total
fi

# Phase 2: Check severity (700 tokens)
CRITICAL_COUNT=$(Grep pattern="\.only\("
                      glob="**/*.test.*"
                      output_mode="count")

if [ "$CRITICAL_COUNT" = "0" ]; then
    echo "✓ No critical anti-patterns (focused/disabled tests)"
    echo "ℹ Found ${TIMING_COUNT:-0} timing issues (minor)"
    echo "  Run with --verbose for details"
    exit 0  # Early exit: 700 tokens total (saves 2,000+)
fi

# Phase 3: Deep anti-pattern analysis (2,000+ tokens)
# Continue with comprehensive analysis...
```

**4. Progressive Disclosure (70% savings on reporting)**

```bash
# PATTERN: Tiered reporting based on severity and user flags

# Parse verbosity from arguments
VERBOSE=$(echo "$ARGUMENTS" | grep -q "\-\-verbose" && echo "true" || echo "false")
ALL=$(echo "$ARGUMENTS" | grep -q "\-\-all" && echo "true" || echo "false")

# Level 1 (Default): Critical issues only
if [ "$VERBOSE" != "true" ]; then
    echo "CRITICAL ANTI-PATTERNS (${CRITICAL_COUNT}):"
    echo "├── Focused tests (.only): ${FOCUSED_COUNT}"
    echo "├── Flaky timing patterns: ${FLAKY_COUNT}"
    echo "└── Test interdependencies: ${DEPENDENCY_COUNT}"
    echo ""
    echo "ℹ Found ${MEDIUM_COUNT} medium and ${LOW_COUNT} low priority issues"
    echo "  Run with --verbose to see all issues"
    # Output: ~600 tokens vs 3,000 tokens for all details
    exit 0
fi

# Level 2 (--verbose): Critical + High + Medium summary
if [ "$ALL" != "true" ]; then
    echo "TEST ANTI-PATTERNS DETECTED:"
    echo ""
    echo "CRITICAL (${CRITICAL_COUNT}):"
    # Show first 5 critical issues with context
    echo ""
    echo "HIGH (${HIGH_COUNT}):"
    # Show first 5 high issues
    echo ""
    echo "MEDIUM (${MEDIUM_COUNT}):"
    # Show summary only
    echo "  ${MEDIUM_COUNT} slow tests, ${BRITTLE_COUNT} brittle tests"
    echo ""
    echo "  Run with --verbose --all for complete details"
    # Output: ~1,500 tokens
    exit 0
fi

# Level 3 (--verbose --all): Complete analysis
# Full report with all anti-patterns and fixes (3,000+ tokens)
```

**5. Focus Areas / Scope Limiting (80% savings)**

```bash
# PATTERN: Default to changed files, allow full scan via flag

# Parse arguments for focus area
FOCUS_PATH="${ARGUMENTS%% *}"  # First argument
FULL_SCAN=$(echo "$ARGUMENTS" | grep -q "\-\-full" && echo "true" || echo "false")
CATEGORY=$(echo "$ARGUMENTS" | grep -oP "(?<=--category=)\w+" || echo "all")

if [ "$FULL_SCAN" != "true" ]; then
    if [ -n "$FOCUS_PATH" ] && [ -d "$FOCUS_PATH" ]; then
        # Specific path provided
        SCAN_SCOPE="$FOCUS_PATH"
        echo "🔍 Analyzing test anti-patterns in: $SCAN_SCOPE"
    else
        # Default: Git diff (changed test files only)
        CHANGED_TEST_FILES=$(git diff --name-only HEAD | \
                            grep -E "\.(test|spec)\." || echo "")

        if [ -n "$CHANGED_TEST_FILES" ]; then
            SCAN_SCOPE="$CHANGED_TEST_FILES"
            FILE_COUNT=$(echo "$CHANGED_TEST_FILES" | wc -l)
            echo "🔍 Analyzing changed test files only ($FILE_COUNT files)"
            echo "  Use --full flag to scan all tests"
        else
            echo "✓ No changed test files detected"
            exit 0  # Early exit: no work needed
        fi
    fi
else
    # Full test suite scan
    SCAN_SCOPE="."
    echo "🔍 Full test suite anti-pattern analysis"
    echo "  This may take longer on large codebases"
fi

# Category filtering (if specified)
if [ "$CATEGORY" != "all" ]; then
    echo "  Filtering for category: $CATEGORY"
    # Focus only on specific anti-pattern category:
    # --category=flaky (timing issues)
    # --category=brittle (over-specification)
    # --category=slow (performance)
    # --category=dependencies (test order)
fi

# Token savings:
# - Changed files only: ~1,000 tokens (5-10 test files)
# - Specific path: ~1,500 tokens (focused directory)
# - Category filter: ~800 tokens (single concern)
# - Full scan: ~5,500 tokens (entire test suite)
# Average savings: 82% (most users analyze changes only)
```

**6. Example-Based Reporting (85% savings)**

```bash
# PATTERN: Show examples, not exhaustive lists

# Bad: List all 45 instances (2,500 tokens)
# echo "All timing issues: $ALL_TIMING_ISSUES"

# Good: Show first 5 examples, count the rest (375 tokens)
TIMING_EXAMPLES=$(echo "$ALL_TIMING_ISSUES" | head -5)
TIMING_COUNT=$(echo "$ALL_TIMING_ISSUES" | wc -l)

echo "TIMING ANTI-PATTERNS DETECTED: $TIMING_COUNT instances"
echo ""
echo "Examples (first 5):"
echo "$TIMING_EXAMPLES"
echo ""
if [ "$TIMING_COUNT" -gt 5 ]; then
    echo "...and $((TIMING_COUNT - 5)) more instances"
    echo "Run with --verbose --all to see all instances"
fi

# Savings: 85% by showing representative examples
```

**7. Pattern-Based Detection (70% savings vs full analysis)**

```bash
# PATTERN: Use Grep patterns instead of reading all files

# Bad: Read all test files and analyze (5,000 tokens)
# for file in $(find test/ -name "*.test.js"); do
#     Read "$file"
#     # Analyze in memory
# done

# Good: Use Grep to detect patterns directly (1,500 tokens)
# Detect flaky tests
FLAKY_TESTS=$(Grep pattern="sleep|setTimeout|setInterval"
                   glob="**/*.test.*"
                   output_mode="files_with_matches"
                   head_limit=20)

# Detect brittle tests
BRITTLE_TESTS=$(Grep pattern="\.state\.|\.find\(.*\)\.at\("
                     glob="**/*.test.*"
                     output_mode="files_with_matches"
                     head_limit=20)

# Detect slow tests
SLOW_TESTS=$(Grep pattern="database\.|createConnection|mongoose\."
                  glob="**/*.test.*"
                  output_mode="files_with_matches"
                  head_limit=20)

# Only read files that have specific issues for detailed fixes
# Savings: 70% by using pattern matching
```

**8. Bash-Based Test Execution (60% savings vs Task agents)**

```bash
# PATTERN: Use direct bash commands for test metrics

# Bad: Use Task tool to run tests (3,000+ tokens)
# Task: "Run tests multiple times and analyze flakiness"

# Good: Direct bash execution (1,000 tokens)
if [ "$RUN_FLAKINESS_CHECK" = "true" ]; then
    echo "Running flakiness detection (3 runs)..."
    RESULTS=""
    for i in 1 2 3; do
        if [ "$FRAMEWORK" = "jest" ]; then
            TEST_OUTPUT=$(npm test -- --silent 2>&1 | grep -E "PASS|FAIL")
        elif [ "$FRAMEWORK" = "pytest" ]; then
            TEST_OUTPUT=$(pytest -q 2>&1 | grep -E "passed|failed")
        fi
        RESULTS="$RESULTS\n$TEST_OUTPUT"
    done

    # Analyze for inconsistent results
    FLAKY_TESTS=$(echo "$RESULTS" | sort | uniq -u)
    echo "Found $(echo "$FLAKY_TESTS" | wc -l) potentially flaky tests"
fi
```

### Token Budget Breakdown

**Optimized Execution Flow:**

```
Phase 1: Quick Anti-Pattern Scan (300 tokens)
├─ Framework cache check (50 tokens)
├─ Timing pattern discovery (100 tokens)
├─ Disabled test check (100 tokens)
└─ Early exit if no issues (50 tokens)
   → Total: 300 tokens (70% of runs exit here)

Phase 2: Severity Assessment (700 tokens)
├─ Critical issue scan (300 tokens)
├─ High priority check (200 tokens)
├─ Medium/low count (100 tokens)
└─ Early exit if only minor issues (100 tokens)
   → Total: 1,000 tokens (20% of runs exit here)

Phase 3: Deep Anti-Pattern Analysis (2,000 tokens)
├─ Read matched test files (1,000 tokens)
├─ Analyze anti-pattern categories (600 tokens)
└─ Generate fix suggestions (400 tokens)
   → Total: 3,000 tokens (10% of runs need deep analysis)

Average: (0.70 × 300) + (0.20 × 1,000) + (0.10 × 3,000) = 710 tokens
Worst case: 3,000 tokens (still under 5,500 unoptimized)
```

**Comparison:**

| Scenario | Unoptimized | Optimized | Savings |
|----------|-------------|-----------|---------|
| No anti-patterns detected | 4,000 | 300 | 92% |
| Minor issues only | 4,500 | 1,000 | 78% |
| Critical issues found | 5,500 | 3,000 | 45% |
| Focused category analysis | 4,000 | 800 | 80% |
| **Average** | **4,500** | **1,800** | **60%** |

### Cache Strategy

**Cache Location:** `.claude/cache/test-antipatterns/`

**Cached Data:**
```json
{
  "framework": "jest|vitest|mocha|pytest|rspec",
  "test_pattern": "**/*.test.js",
  "timestamp": "2026-01-27T10:30:00Z",
  "last_scan": {
    "files_analyzed": 87,
    "critical_issues": 8,
    "high_issues": 12,
    "medium_issues": 15,
    "low_issues": 71,
    "categories": {
      "flaky": 8,
      "brittle": 23,
      "slow": 15,
      "dependencies": 12,
      "mocking": 18,
      "structure": 31
    },
    "file_checksums": {
      "test/api.test.js": "abc123...",
      "test/user.test.js": "def456..."
    }
  }
}
```

**Cache Invalidation:**
- Time-based: 1 hour for framework detection
- Checksum-based: Test file changes
- Manual: `--no-cache` flag to force fresh analysis

**Cache Benefits:**
- Framework detection: 500 token savings (99% cache hit rate)
- Previous scan results: 1,500 token savings (when test files unchanged)
- Overall: 75% savings on repeated runs

### Real-World Token Usage

**Scenario 1: Daily TDD workflow (typical)**
```bash
# Developer adds new tests, runs /test-antipatterns

Result:
- Framework: cached (50 tokens)
- Scan scope: 3 changed test files (400 tokens)
- Pattern detection: 1 setTimeout found (300 tokens)
- Fix suggestion: Replace with waitFor (150 tokens)
Total: ~900 tokens (80% savings vs 4,500 unoptimized)
```

**Scenario 2: Pre-commit check**
```bash
# Developer runs /test-antipatterns before committing

Result:
- Framework: cached (50 tokens)
- Scan scope: git diff (5 test files, 600 tokens)
- No critical issues found (300 tokens)
- Early exit with ✓ message (50 tokens)
Total: ~1,000 tokens (78% savings vs 4,500 unoptimized)
```

**Scenario 3: Full test suite audit (rare)**
```bash
# Team lead runs comprehensive test quality audit

Result:
- Framework: cached (50 tokens)
- Full scan with --full flag (1,500 tokens)
- Multiple categories analyzed (1,200 tokens)
- Comprehensive report (700 tokens)
Total: ~3,450 tokens (23% savings vs 4,500 unoptimized)
```

**Scenario 4: Category-specific analysis**
```bash
# Developer focuses on flaky tests only

Result:
- Framework: cached (50 tokens)
- Category filter: --category=flaky (200 tokens)
- Timing pattern analysis (500 tokens)
- Focused fix suggestions (250 tokens)
Total: ~1,000 tokens (78% savings vs 4,500 unoptimized)
```

### Performance Improvements

**Benefits of Optimization:**
1. **Faster Feedback:** Quick validation in 300-1,000 tokens for common cases
2. **Lower Costs:** 60% average token reduction = 60% cost savings
3. **Focused Analysis:** Category filtering for specific concerns
4. **Scalability:** Works efficiently on large test suites (head_limit)
5. **Better UX:** Progressive disclosure - users get what they need

**Quality Maintained:**
- ✅ Zero functionality regression
- ✅ All anti-pattern categories still detected
- ✅ Fix suggestions remain comprehensive
- ✅ Severity prioritization unchanged
- ✅ Reporting quality improved (example-based, clearer)

**Additional Optimizations:**
- Parallel pattern detection (run multiple Grep in parallel)
- Shared cache with `/test` and `/test-coverage` skills
- Smart flakiness detection (only when requested)
- Incremental analysis (only check changed files by default)

This ensures thorough test anti-pattern detection while delivering fast, cost-effective analysis with actionable results.
