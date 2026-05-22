---
name: ln-503-manual-tester
description: Performs manual testing of Story AC via executable bash scripts saved to tests/manual/. Creates reusable test suites per Story. Worker only.
---

# Manual Tester

Manually verifies Story AC on running code and reports structured results for the quality gate.

## Purpose & Scope
- Create executable test scripts in `tests/manual/` folder of target project.
- Run AC-driven checks via bash/curl (API) or puppeteer (UI).
- Save scripts permanently for regression testing (not temp files).
- Document results in Linear with pass/fail per AC and script path.
- No status changes or task creation.

## Workflow

### Phase 1: Setup tests/manual structure
1) **Read `docs/project/runbook.md`** — get Docker commands, API base URL, test prerequisites, environment setup
2) Check if `tests/manual/` folder exists in project root
3) If missing, create structure:
   - `tests/manual/config.sh` — shared configuration (BASE_URL, helpers, colors)
   - `tests/manual/README.md` — folder documentation (see README.md template below)
   - `tests/manual/test-all.sh` — master script to run all test suites (see test-all.sh template below)
4) If exists, read existing `config.sh` to reuse settings (BASE_URL, tokens)

### Phase 2: Create Story test script
1) Fetch Story, parse AC into Given/When/Then list (3-5 expected)
2) Detect API vs UI (API → curl, UI → puppeteer)
3) Generate test script: `tests/manual/{NN}-{story-slug}/test-{story-slug}.sh`
   - Header: Story ID, AC list, prerequisites
   - Test function per AC + edge/error cases
   - Summary output (PASSED/FAILED/TOTAL)
4) Make script executable (`chmod +x`)

### Phase 2.5: Update Documentation
1) Update `tests/manual/README.md`:
   - Add new test to "Available Test Suites" table
   - Include Story ID, AC covered, run command
2) Update `tests/manual/test-all.sh`:
   - Add call to new script in SUITES array
   - Maintain execution order (00-setup first, then numbered suites)

### Phase 3: Execute and report
1) Rebuild Docker containers (no cache), ensure healthy
2) Run generated script, capture output
3) Parse results (pass/fail counts)
4) Post Linear comment with:
   - AC matrix (pass/fail per AC)
   - Script path: `tests/manual/{NN}-{story-slug}/test-{story-slug}.sh`
   - Rerun command: `cd tests/manual && ./{NN}-{story-slug}/test-{story-slug}.sh`

## Critical Rules
- Scripts saved to project `tests/manual/`, NOT temp files.
- Rebuild Docker before testing; fail if rebuild/run unhealthy.
- Keep language of Story (EN/RU) in script comments and Linear comment.
- No fixes or status changes; only evidence and verdict.
- Script must be idempotent (can rerun anytime).

## Definition of Done
- `tests/manual/` structure exists (config.sh, README.md, test-all.sh created if missing).
- Test script created at `tests/manual/{NN}-{story-slug}/test-{story-slug}.sh`.
- Script is executable and idempotent.
- **README.md updated** with new test suite in "Available Test Suites" table.
- **test-all.sh updated** with call to new script in SUITES array.
- App rebuilt and running; tests executed.
- Verdict and Linear comment posted with script path and rerun command.

## Script Templates

### README.md (created once per project)

```markdown
# Manual Testing Scripts

> **SCOPE:** Bash scripts for manual API testing. Complements automated tests with CLI-based workflows.

## Quick Start

```bash
cd tests/manual
./00-setup/create-account.sh  # (if auth required)
./test-all.sh                 # Run ALL test suites
```

## Prerequisites

- Docker containers running (`docker compose ps`)
- jq installed (`apt-get install jq` or `brew install jq`)

## Folder Structure

```
tests/manual/
├── config.sh          # Shared configuration (BASE_URL, helpers, colors)
├── README.md          # This file
├── test-all.sh        # Run all test suites
├── 00-setup/          # Account & token setup (if auth required)
│   ├── create-account.sh
│   └── get-token.sh
└── {NN}-{topic}/      # Test suites by Story
    └── test-{slug}.sh
```

## Available Test Suites

<!-- Add new test suites here when creating new tests -->

| Suite | Story | AC Covered | Run Command |
|-------|-------|------------|-------------|
| — | — | — | — |

## Adding New Tests

1. Create script in `{NN}-{topic}/test-{slug}.sh`
2. **Update this README** (Available Test Suites table)
3. **Update `test-all.sh`** (add to SUITES array)
```

### test-all.sh (created once per project)

```bash
#!/bin/bash
# =============================================================================
# Run all manual test suites
# =============================================================================
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

echo "=========================================="
echo "Running ALL Manual Test Suites"
echo "=========================================="

check_jq
check_api

# Setup (if exists)
[ -f "$SCRIPT_DIR/00-setup/create-account.sh" ] && "$SCRIPT_DIR/00-setup/create-account.sh"
[ -f "$SCRIPT_DIR/00-setup/get-token.sh" ] && "$SCRIPT_DIR/00-setup/get-token.sh"

# Test suites (add new suites here)
SUITES=(
    # "01-auth/test-auth-flow.sh"
    # "02-translation/test-translation.sh"
)

PASSED=0; FAILED=0
for suite in "${SUITES[@]}"; do
    echo ""
    echo "=========================================="
    echo "Running: $suite"
    echo "=========================================="
    if "$SCRIPT_DIR/$suite"; then
        ((++PASSED))
        print_status "PASS" "$suite"
    else
        ((++FAILED))
        print_status "FAIL" "$suite"
    fi
done

echo ""
echo "=========================================="
echo "TOTAL: $PASSED suites passed, $FAILED failed"
echo "=========================================="
[ $FAILED -eq 0 ] && exit 0 || exit 1
```

### config.sh (created once per project)

```bash
#!/bin/bash
# Shared configuration for manual testing scripts
export BASE_URL="${BASE_URL:-http://localhost:8080}"
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export NC='\033[0m'

print_status() {
    local status=$1; local message=$2
    case $status in
        "PASS") echo -e "${GREEN}[PASS]${NC} $message" ;;
        "FAIL") echo -e "${RED}[FAIL]${NC} $message" ;;
        "WARN") echo -e "${YELLOW}[WARN]${NC} $message" ;;
        "INFO") echo -e "[INFO] $message" ;;
    esac
}

check_jq() {
    command -v jq &> /dev/null || { echo "Error: jq required"; exit 1; }
}

check_api() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health" 2>/dev/null)
    if [ "$response" != "200" ]; then
        echo "Error: API not reachable at $BASE_URL"
        exit 1
    fi
    print_status "INFO" "API reachable at $BASE_URL"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export SCRIPT_DIR
```

### Test script structure (per Story)

```bash
#!/bin/bash
# =============================================================================
# {STORY-ID}: {Story Title}
# =============================================================================
# AC tested: AC1, AC2, AC3...
# Prerequisites: Docker running, jq installed
# Usage: ./test-{story-slug}.sh
# =============================================================================

set -e
THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$THIS_DIR/../config.sh"

check_jq
check_api

PASSED=0; FAILED=0; TOTAL=0

run_test() {
    local name=$1; local func=$2
    ((++TOTAL))
    echo ""
    echo "TEST $TOTAL: $name"
    if $func; then
        ((++PASSED))
        print_status "PASS" "$name"
    else
        ((++FAILED))
        print_status "FAIL" "$name"
    fi
}

# AC1: Given/When/Then
test_ac1() {
    # curl commands here
    return 0
}

run_test "AC1: Description" test_ac1

# Summary
echo ""
echo "=========================================="
echo "SUMMARY: $PASSED/$TOTAL passed, $FAILED failed"
echo "=========================================="
[ $FAILED -eq 0 ] && exit 0 || exit 1
```

## Reference Files
- Script format reference: prompsit-api `tests/manual/` (production example)
- AC format: `shared/templates/test_task_template.md` (or local `docs/templates/` in target project)
- Risk-based context: `ln-510-test-planner/references/risk_based_testing_guide.md`

---
**Version:** 3.1.0 (Added mandatory runbook.md reading for Docker/API setup)
**Last Updated:** 2026-01-09
