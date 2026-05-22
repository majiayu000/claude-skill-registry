---
name: codegeass-testing
description: Comprehensive pre-merge testing for CodeGeass. Tests PR changes FIRST, then runs regression tests on all CLI commands and Dashboard API endpoints.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# CodeGeass Pre-Merge Testing

**CRITICAL**: This skill tests PR changes FIRST, then runs regression tests to ensure nothing is broken.

## Dynamic Context (injected before execution)

### PR/Branch Context
!`git branch --show-current 2>&1`
!`git log --oneline -5 2>&1`

### Files Changed in This PR
!`git diff --name-only HEAD~5 2>&1 | head -30`
!`git diff --stat HEAD~5 2>&1 | tail -20`

### Modified Backend Files (routers/services)
!`git diff --name-only HEAD~5 -- "*.py" 2>&1 | grep -E "(routers|services|cli)" | head -20`

### Diff of Modified Router Files
!`git diff HEAD~5 -- "**/routers/*.py" 2>&1 | head -100`

### Diff of Modified Service Files
!`git diff HEAD~5 -- "**/services/*.py" 2>&1 | head -100`

### CLI Overview
!`codegeass --help 2>&1`

### Current Tasks (for testing filters)
!`codegeass task list 2>&1 | head -30`
!`codegeass task tag list 2>&1`

### Dashboard Health
!`curl -s http://localhost:8001/health 2>&1 || echo "Dashboard not running"`

---

## Test Execution Instructions

**Order matters**: Test PR changes FIRST, then run regression tests.

---

## Phase 0: Prerequisites

1. **Verify codegeass installation**:
   ```bash
   which codegeass && codegeass --version
   ```

2. **Start Dashboard if not running**:
   ```bash
   curl -s http://localhost:8001/health || {
     nohup codegeass dashboard > /tmp/dashboard.log 2>&1 &
     sleep 3
   }
   ```

3. **Create test task with tags** (for filter testing):
   ```bash
   codegeass task create \
     --name "cg-test-task" \
     --schedule "0 0 * * *" \
     --prompt "Test task for pre-merge testing" \
     --working-dir "$(pwd)" \
     --model haiku \
     --tag test --tag automation
   ```

---

## Phase 1: PR Feature Testing (PRIORITY)

**CRITICAL**: Analyze the git diff and test ALL new/modified functionality FIRST.

### 1.1 Identify What Changed

Look at the dynamic context above to identify:
- Which routers were modified (e.g., `routers/tasks.py`)
- Which services were modified (e.g., `services/task_service.py`)
- Which CLI commands were modified
- What new parameters/endpoints were added

### 1.2 Test New API Parameters

If `routers/tasks.py` was modified, check for new query parameters and test each one:

```bash
# Example: If search/filter was added to GET /api/tasks
# Test search parameter
curl -s "http://localhost:8001/api/tasks?search=test" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'search=test: {len(d)} results')
for t in d[:3]: print(f'  - {t[\"name\"]}')"

# Test tags filter
curl -s "http://localhost:8001/api/tasks?tags=test" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'tags=test: {len(d)} results')
for t in d[:3]: print(f'  - {t[\"name\"]}')"

# Test status filter
curl -s "http://localhost:8001/api/tasks?status=success" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'status=success: {len(d)} results')"

# Test model filter
curl -s "http://localhost:8001/api/tasks?model=opus" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'model=opus: {len(d)} results')"

# Test enabled filter
curl -s "http://localhost:8001/api/tasks?enabled=true" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'enabled=true: {len(d)} results')"

# Test combined filters
curl -s "http://localhost:8001/api/tasks?search=test&enabled=true" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'search+enabled: {len(d)} results')"
```

### 1.3 Test New CLI Options

If CLI commands were modified, test any new options:

```bash
# Example: If --search or --filter was added to task list
codegeass task list --help  # Check for new options
```

### 1.4 Test Edge Cases for New Features

```bash
# Empty search
curl -s "http://localhost:8001/api/tasks?search=" | python3 -c "
import sys,json; d=json.load(sys.stdin); print(f'Empty search: {len(d)} results (should return all)')"

# Non-existent tag
curl -s "http://localhost:8001/api/tasks?tags=nonexistent" | python3 -c "
import sys,json; d=json.load(sys.stdin); print(f'Non-existent tag: {len(d)} results (should be 0)')"

# Invalid status
curl -s "http://localhost:8001/api/tasks?status=invalid"
# Should return 422 validation error

# Multiple tags
curl -s "http://localhost:8001/api/tasks?tags=test&tags=deploy" | python3 -c "
import sys,json; d=json.load(sys.stdin); print(f'Multiple tags: {len(d)} results')"
```

### 1.5 Verify Frontend Integration (if applicable)

If frontend files were modified:
```bash
# Check if frontend build works
cd dashboard/frontend && npm run build 2>&1 | tail -10

# Or just verify the static files were updated
ls -la src/codegeass/dashboard/static/assets/*.js | head -5
```

---

## Phase 2: Regression Testing (CLI Commands)

Test all CLI commands to ensure PR didn't break anything.

### 2.1 Task Commands
```bash
codegeass task list
codegeass task show cg-test-task
codegeass task stats cg-test-task
codegeass task enable cg-test-task
codegeass task disable cg-test-task
codegeass task update cg-test-task --timeout 120
codegeass task tag list
codegeass task tag show test
```

### 2.2 Skill Commands
```bash
codegeass skill list
codegeass skill show release
codegeass skill validate release
codegeass skill render release "1.0.0"
codegeass skill reload
```

### 2.3 Scheduler Commands
```bash
codegeass scheduler status
codegeass scheduler upcoming
codegeass scheduler due
codegeass scheduler show-cron
codegeass scheduler test-cron
```

### 2.4 Other Command Groups
```bash
codegeass logs list --limit 5
codegeass logs stats
codegeass notification list
codegeass notification providers
codegeass approval list
codegeass approval stats
codegeass cron validate "0 * * * *"
codegeass cron describe "0 9 * * 1-5"
codegeass data stats
codegeass data location
codegeass provider list
codegeass provider check
codegeass execution list
codegeass project list
codegeass project platforms
```

---

## Phase 3: Regression Testing (API Endpoints)

### 3.1 Core Endpoints
```bash
curl -s http://localhost:8001/health
curl -s http://localhost:8001/api/tasks
curl -s http://localhost:8001/api/skills
curl -s http://localhost:8001/api/scheduler/status
curl -s http://localhost:8001/api/logs?limit=5
curl -s http://localhost:8001/api/notifications/channels
curl -s http://localhost:8001/api/approvals
curl -s http://localhost:8001/api/executions
curl -s http://localhost:8001/api/projects
curl -s http://localhost:8001/api/providers
```

### 3.2 CRUD Operations
```bash
# Create task via API
curl -s -X POST http://localhost:8001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"name": "cg-api-test", "schedule": "0 0 * * *", "prompt": "API test", "working_dir": "'"$(pwd)"'"}'

# Verify in CLI
codegeass task show cg-api-test

# Delete via API
TASK_ID=$(codegeass task show cg-api-test 2>&1 | grep "^│ ID:" | awk '{print $3}')
curl -s -X DELETE http://localhost:8001/api/tasks/$TASK_ID
```

---

## Phase 4: Integration Testing

### 4.1 CLI-to-API Consistency
```bash
# Create via CLI
codegeass task create --name "cg-integration" --schedule "0 0 * * *" --prompt "test"
# Verify in API
TASK_ID=$(codegeass task show cg-integration 2>&1 | grep "^│ ID:" | awk '{print $3}')
curl -s http://localhost:8001/api/tasks/$TASK_ID | grep -q "cg-integration" && echo "PASS"
# Cleanup
codegeass task delete cg-integration --yes
```

### 4.2 Architecture Check
```bash
# Verify Dashboard uses CLI library
grep -c "from codegeass\." src/codegeass/dashboard/services/*.py
grep -c "from codegeass\." src/codegeass/dashboard/routers/*.py
```

---

## Phase 5: Cleanup

```bash
codegeass task delete cg-test-task --yes 2>/dev/null || true
```

---

## Phase 6: Generate Report

Create JSON report at `data/test-reports/pre-merge-<timestamp>.json`:

```json
{
  "timestamp": "<ISO>",
  "branch": "<branch>",
  "commit": "<hash>",
  "pr_changes": {
    "files_modified": ["<list>"],
    "new_features_tested": ["<list>"],
    "all_passed": true|false
  },
  "summary": {
    "total_tests": <n>,
    "passed": <n>,
    "failed": <n>,
    "success_rate": "<pct>"
  },
  "pr_tests": {
    "total": <n>,
    "passed": <n>,
    "failed": <n>,
    "results": [...]
  },
  "regression_tests": {
    "cli": {"passed": <n>, "failed": <n>},
    "api": {"passed": <n>, "failed": <n>}
  },
  "failures": []
}
```

---

## Quick Reference: Common PR Test Patterns

### If `routers/tasks.py` modified:
```bash
# Test all query params
curl -s "http://localhost:8001/api/tasks?search=X"
curl -s "http://localhost:8001/api/tasks?tags=X"
curl -s "http://localhost:8001/api/tasks?status=X"
curl -s "http://localhost:8001/api/tasks?model=X"
curl -s "http://localhost:8001/api/tasks?enabled=X"
curl -s "http://localhost:8001/api/tasks?summary_only=true"
```

### If `routers/skills.py` modified:
```bash
curl -s http://localhost:8001/api/skills
curl -s http://localhost:8001/api/skills/{name}
curl -s "http://localhost:8001/api/skills/{name}/preview?arguments=X"
```

### If `services/task_service.py` modified:
```bash
# Test filtering logic
curl -s "http://localhost:8001/api/tasks?search=security"
curl -s "http://localhost:8001/api/tasks?tags=deploy&enabled=true"
```

### If CLI commands modified:
```bash
codegeass <command> --help  # Check new options
codegeass <command> <new-option>  # Test it
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Dashboard not running | `codegeass dashboard &` |
| 422 Validation Error | Check query param format |
| Empty results | Verify test data exists |
| Import errors | `pip install -e .` |
