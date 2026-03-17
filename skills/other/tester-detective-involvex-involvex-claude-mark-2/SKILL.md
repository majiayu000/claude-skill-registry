---
name: tester-detective
description: "⚡ PRIMARY TOOL for: 'what's tested', 'find test coverage', 'audit test quality', 'missing tests', 'edge cases', 'test patterns'. Uses claudemem v0.3.0 AST with callers analysis for test discovery. GREP/FIND/GLOB ARE FORBIDDEN."
allowed-tools: Bash, Task, Read, AskUserQuestion
---

# ⛔⛔⛔ CRITICAL: AST STRUCTURAL ANALYSIS ONLY ⛔⛔⛔

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🧠 THIS SKILL USES claudemem v0.3.0 AST ANALYSIS EXCLUSIVELY               ║
║                                                                              ║
║   ❌ GREP IS FORBIDDEN                                                       ║
║   ❌ FIND IS FORBIDDEN                                                       ║
║   ❌ GLOB IS FORBIDDEN                                                       ║
║                                                                              ║
║   ✅ claudemem --nologo callers <name> --raw TO FIND TESTS                  ║
║   ✅ claudemem --nologo map "test spec" --raw TO MAP TEST INFRASTRUCTURE    ║
║                                                                              ║
║   ⭐ v0.3.0: callers shows which tests call each function                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

# Tester Detective Skill

**Version:** 3.3.0
**Role:** QA Engineer / Test Specialist
**Purpose:** Test coverage investigation using AST callers analysis and automated test-gaps detection

## Role Context

You are investigating this codebase as a **QA Engineer**. Your focus is on:
- **Test coverage** - What is tested vs. untested
- **Test callers** - Which tests call each function
- **Edge cases** - Boundary conditions in tests
- **Test quality** - Are tests meaningful or superficial
- **Coverage gaps** - Functions without test callers

## Why `callers` is Perfect for Test Analysis

The `callers` command shows you:
- **Test callers** = Tests appear as callers of the function
- **Coverage gaps** = No test callers = untested code
- **Test distribution** = Which tests cover which code
- **Direct relationships** = Exact test-to-code mapping

## Tester-Focused Commands (v0.3.0)

### Find Tests for a Function

```bash
# Who calls this function? (tests will appear as callers)
claudemem --nologo callers processPayment --raw

# Filter: callers from test files are your tests
# src/services/payment.test.ts:45 → This is a test!
```

### Map Test Infrastructure

```bash
# Find all test files
claudemem --nologo map "test spec describe it" --raw

# Find test utilities
claudemem --nologo map "test helper mock stub" --raw

# Find fixtures
claudemem --nologo map "fixture factory builder" --raw
```

### Test Coverage Gaps (v0.4.0+ Required)

```bash
# Find high-importance untested code automatically
claudemem --nologo test-gaps --raw

# Output:
# file: src/services/payment.ts
# line: 45-89
# name: processPayment
# pagerank: 0.034
# production_callers: 4
# test_callers: 0
# ---
# This is CRITICAL - high PageRank but no tests!
```

**Why test-gaps is better than manual analysis**:
- Automatically finds high-PageRank symbols
- Automatically counts test vs production callers
- Prioritized list of coverage gaps

**Handling Empty Results:**
```bash
GAPS=$(claudemem --nologo test-gaps --raw)
if [ -z "$GAPS" ] || echo "$GAPS" | grep -q "No test gaps"; then
  echo "Excellent test coverage! All high-importance code has tests."
  echo ""
  echo "Optional: Check lower-importance code:"
  echo "  claudemem --nologo test-gaps --min-pagerank 0.005 --raw"
else
  echo "Test Coverage Gaps Found:"
  echo "$GAPS"
fi
```

**Limitations Note:**
Test detection relies on file naming patterns:
- `*.test.ts`, `*.spec.ts`, `*_test.go`, etc.
- Integration tests in non-standard locations may not be detected
- Manual test files require naming convention updates

### Find Untested Code

**Method 1: Automated (v0.4.0+ Required - Recommended)**

```bash
# Let claudemem find all gaps automatically
GAPS=$(claudemem --nologo test-gaps --raw)

if [ -z "$GAPS" ]; then
  echo "No high-importance untested code found!"
else
  echo "$GAPS"
fi

# Focus on critical gaps only
claudemem --nologo test-gaps --min-pagerank 0.05 --raw
```

**Method 2: Manual (for specific functions, v0.3.0 compatible)**

```bash
# Get callers for a function
claudemem --nologo callers importantFunction --raw

# If NO callers from *.test.ts or *.spec.ts files:
# This function has NO tests!
```

### Test Coverage Analysis

```bash
# For each critical function, check callers
claudemem --nologo callers authenticateUser --raw
claudemem --nologo callers processPayment --raw
claudemem --nologo callers saveToDatabase --raw

# Note which have test callers and which don't
```

## PHASE 0: MANDATORY SETUP

### Step 1: Verify claudemem v0.3.0

```bash
which claudemem && claudemem --version
# Must be 0.3.0+
```

### Step 2: If Not Installed → STOP

Use AskUserQuestion (see ultrathink-detective for template)

### Step 3: Check Index Status

```bash
# Check claudemem installation and index
claudemem --version && ls -la .claudemem/index.db 2>/dev/null
```

### Step 3.5: Check Index Freshness

Before proceeding with investigation, verify the index is current:

```bash
# First check if index exists
if [ ! -d ".claudemem" ] || [ ! -f ".claudemem/index.db" ]; then
  # Use AskUserQuestion to prompt for index creation
  # Options: [1] Create index now (Recommended), [2] Cancel investigation
  exit 1
fi

# Count files modified since last index
STALE_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) \
  -newer .claudemem/index.db 2>/dev/null | grep -v "node_modules" | grep -v ".git" | grep -v "dist" | grep -v "build" | wc -l)
STALE_COUNT=$((STALE_COUNT + 0))  # Normalize to integer

if [ "$STALE_COUNT" -gt 0 ]; then
  # Get index time with explicit platform detection
  if [[ "$OSTYPE" == "darwin"* ]]; then
    INDEX_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" .claudemem/index.db 2>/dev/null)
  else
    INDEX_TIME=$(stat -c "%y" .claudemem/index.db 2>/dev/null | cut -d'.' -f1)
  fi
  INDEX_TIME=${INDEX_TIME:-"unknown time"}

  # Get sample of stale files
  STALE_SAMPLE=$(find . -type f \( -name "*.ts" -o -name "*.tsx" \) \
    -newer .claudemem/index.db 2>/dev/null | grep -v "node_modules" | grep -v ".git" | head -5)

  # Use AskUserQuestion (see template in ultrathink-detective)
fi
```

### Step 4: Index if Needed

```bash
claudemem index
```

---

## Workflow: Test Coverage Analysis (v0.3.0)

### Phase 0: Automated Gap Detection (v0.4.0+ Required)

```bash
# Run test-gaps FIRST - it does the work for you
GAPS=$(claudemem --nologo test-gaps --raw)

if [ -z "$GAPS" ]; then
  echo "No gaps found at default threshold"
  echo "Optionally check with lower threshold:"
  claudemem --nologo test-gaps --min-pagerank 0.005 --raw
else
  # This gives you a prioritized list of:
  # - High-PageRank symbols
  # - With 0 test callers
  # - Sorted by importance
  echo "$GAPS"
fi
```

### Phase 1: Map Test Infrastructure

```bash
# Find test configuration
claudemem --nologo map "jest vitest mocha config" --raw

# Find test utilities and mocks
claudemem --nologo map "mock stub spy helper" --raw
```

### Phase 2: Identify Critical Functions

```bash
# Map the feature area
claudemem --nologo map "payment processing" --raw

# High-PageRank functions are most critical to test
```

### Phase 3: Check Test Coverage via Callers

```bash
# For each critical function, check callers
claudemem --nologo callers PaymentService --raw

# Look for callers from test files:
# src/services/payment.test.ts:23 ← TEST CALLER
# src/controllers/checkout.ts:45 ← NOT A TEST
```

### Phase 4: Find Coverage Gaps

```bash
# Functions with NO test callers = untested
# Make a list of untested critical functions
```

### Phase 5: Analyze Test Quality

```bash
# For functions with test callers, read the tests
# Check: Are they testing edge cases? Error paths?
```

## Output Format: Test Coverage Report

### 1. Test Infrastructure Summary

```
┌─────────────────────────────────────────────────────────┐
│                   TEST INFRASTRUCTURE                    │
├─────────────────────────────────────────────────────────┤
│  Framework: Vitest 2.x                                  │
│  Test Files: 156 files (*.spec.ts, *.test.ts)          │
│  Test Utils: src/__tests__/utils/                       │
│  Search Method: claudemem v0.3.0 (callers analysis)    │
└─────────────────────────────────────────────────────────┘
```

### 2. Coverage by Function (via callers)

```
| Function            | Test Callers | Coverage |
|---------------------|--------------|----------|
| authenticateUser    | 5 tests      | ✅ Good   |
| processPayment      | 3 tests      | ✅ Good   |
| calculateDiscount   | 0 tests      | ❌ None   |
| sendEmail           | 1 test       | ⚠️ Low    |
| updateUserProfile   | 0 tests      | ❌ None   |
```

### 3. Untested Critical Functions

```
🔴 HIGH PRIORITY - No Test Callers:
   └── calculateDiscount (PageRank: 0.034)
       └── callers show: 4 production callers, 0 test callers
   └── updateUserProfile (PageRank: 0.028)
       └── callers show: 3 production callers, 0 test callers

⚠️ MEDIUM PRIORITY - Few Test Callers:
   └── sendEmail (PageRank: 0.021)
       └── callers show: 1 test, no edge case tests
```

### 4. Test Quality Notes

```
📝 OBSERVATIONS:

1. calculateDiscount has 4 production callers but 0 test callers
   → Critical business logic untested!

2. sendEmail has 1 test caller
   → Only happy path tested, no error scenarios

3. authenticateUser has 5 test callers
   → Good coverage including edge cases
```

## Scenarios

### Scenario: "What's tested?"

```bash
# Step 1: Map the feature
claudemem --nologo map "payment" --raw

# Step 2: For each function, check callers
claudemem --nologo callers processPayment --raw
claudemem --nologo callers validateCard --raw
claudemem --nologo callers chargeCustomer --raw

# Step 3: Count test callers vs production callers
```

### Scenario: Finding Coverage Gaps

```bash
# Step 1: Find high-PageRank (important) functions
claudemem --nologo map --raw

# Step 2: Check callers for each
claudemem --nologo callers importantFunc1 --raw
claudemem --nologo callers importantFunc2 --raw

# Step 3: Functions with 0 test callers = gap
```

### Scenario: Test Quality Audit

```bash
# Step 1: Find test callers
claudemem --nologo callers targetFunction --raw

# Step 2: Read each test file at the caller line
# Step 3: Check: Does test cover edge cases? Errors?
```

## Result Validation Pattern

After EVERY claudemem command, validate results:

### Callers Validation for Tests

When checking test coverage:

```bash
CALLERS=$(claudemem --nologo callers processPayment --raw)
EXIT_CODE=$?

# Check for command failure
if [ "$EXIT_CODE" -ne 0 ]; then
  DIAGNOSIS=$(claudemem status 2>&1)
  # Use AskUserQuestion for recovery
fi

# Validate we got callers, not an error
if echo "$CALLERS" | grep -qi "error\|failed"; then
  # Actual error, not 0 callers
  # Use AskUserQuestion
fi

# Count test vs production callers
TEST_CALLERS=$(echo "$CALLERS" | grep -E "\.test\.|\.spec\.|_test\." | wc -l)
PROD_CALLERS=$(echo "$CALLERS" | grep -v -E "\.test\.|\.spec\.|_test\." | wc -l)

# Report coverage ratio
if [ "$TEST_CALLERS" -eq 0 ]; then
  echo "WARNING: No test coverage found for this function"
fi
```

### Empty Results Validation

```bash
RESULTS=$(claudemem --nologo map "test spec describe" --raw)

if [ -z "$RESULTS" ]; then
  echo "WARNING: No test infrastructure found"
  # May indicate:
  # 1. Tests in non-standard locations
  # 2. Index doesn't include test files
  # 3. Wrong query terms
  # Use AskUserQuestion
fi
```

---

## FALLBACK PROTOCOL

**CRITICAL: Never use grep/find/Glob without explicit user approval.**

If claudemem fails or returns irrelevant results:

1. **STOP** - Do not silently switch tools
2. **DIAGNOSE** - Run `claudemem status`
3. **REPORT** - Tell user what happened
4. **ASK** - Use AskUserQuestion for next steps

```typescript
// Fallback options (in order of preference)
AskUserQuestion({
  questions: [{
    question: "claudemem test coverage analysis failed or found no tests. How should I proceed?",
    header: "Test Coverage Issue",
    multiSelect: false,
    options: [
      { label: "Reindex codebase", description: "Run claudemem index (~1-2 min)" },
      { label: "Try different query", description: "Search for different test patterns" },
      { label: "Use grep (not recommended)", description: "Traditional search - loses caller analysis" },
      { label: "Cancel", description: "Stop investigation" }
    ]
  }]
})
```

**See ultrathink-detective skill for complete Fallback Protocol documentation.**

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| `grep "test"` | No caller relationships | `claudemem --nologo callers func --raw` |
| Assume tests exist | Miss coverage gaps | Verify with callers analysis |
| Count test files | Doesn't show what's tested | Check callers per function |
| Skip PageRank | Miss critical gaps | Focus on high-PageRank untested |

## Testing Tips

1. **Use callers to find tests** - Tests appear as callers of functions
2. **No test callers = no tests** - Coverage gap identified
3. **High PageRank + no tests = critical gap** - Prioritize these
4. **Read test callers** - Verify quality, not just existence
5. **Check edge cases** - Are error paths tested?

## Notes

- **`callers` reveals test coverage** - Tests are just callers from test files
- **High-PageRank untested = critical gap** - Most impactful coverage issues
- **Production callers vs test callers** - Ratio shows coverage health
- Filter callers by file path (*.test.ts, *.spec.ts) to find tests
- Works best with TypeScript, Go, Python, Rust codebases

---

**Maintained by:** MadAppGang
**Plugin:** code-analysis v2.7.0
**Last Updated:** December 2025 (v3.3.0 - Cross-platform compatibility, inline templates, improved validation)
