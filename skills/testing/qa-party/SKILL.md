---
name: qa-party
description: Parallel validation deployment. Spawn 8+ QA agents to run tests, builds, lints, and health checks simultaneously. Zero marginal wall-clock cost.
model_tier: sonnet
parallel_hints:
  can_parallel_with: []
  must_serialize_with: [plan-party]
  preferred_batch_size: 12
context_hints:
  max_file_context: 50
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "critical.*fail"
    reason: "Critical test failures need investigation"
  - pattern: "docker.*down"
    reason: "Infrastructure issues need human intervention"
  - keyword: ["security", "blocking"]
    reason: "Security or blocking issues require escalation"
---

# QA_PARTY Skill

> **Purpose:** Coordinated parallel validation with 8+ QA agents
> **Created:** 2025-12-31
> **Trigger:** `/qa-party` command
> **Aliases:** `/validate`, `/qa`, `/qp`

---

## When to Use

Deploy QA_PARTY when you need comprehensive validation:

- After CCW completes a workstream
- Before creating a PR
- After merging changes
- Regression testing after major refactors
- CI/CD equivalent for local validation

**Do NOT use for:**
- Single test file execution
- Quick lint check
- When you know exactly what failed

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel agents with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
8 checks × 60s each      8 checks × 60s in parallel
Total: 480s              Total: 60s (8x faster)
```

**Implication:** Always spawn all QA agents. There is no cost savings from running fewer.

---

## Deployment Pattern

### Standard Deployment: 8 QA Agents

Deploy 8 QA agents in parallel, each running a specific validation domain:

| QA Agent | Target | Commands |
|----------|--------|----------|
| QA-FRONTEND-BUILD | Next.js build | `npm run build` |
| QA-FRONTEND-LINT | ESLint + TypeScript | `npm run lint && npm run type-check` |
| QA-FRONTEND-TESTS | Jest tests | `npm test` |
| QA-BACKEND-LINT | Ruff check + format | `ruff check . && ruff format --check .` |
| QA-BACKEND-TESTS | pytest suite | `pytest tests/ -v --tb=short` |
| QA-DOCKER-HEALTH | Container status | `docker compose ps && docker compose logs --tail=50` |
| QA-API-SMOKE | Endpoint health | `curl http://localhost:8000/health` |
| QA-MCP-TOOLS | MCP server validation | `docker compose exec mcp-server python -c "..."` |

### Extended Deployment: 12 QA Agents

For comprehensive validation, add domain-specific test splits:

| QA Agent | Target | Commands |
|----------|--------|----------|
| QA-BACKEND-ACGME | ACGME compliance tests | `pytest tests/ -m acgme -v` |
| QA-BACKEND-RESILIENCE | Resilience tests | `pytest tests/resilience/ -v` |
| QA-BACKEND-SCHEDULING | Scheduling tests | `pytest tests/scheduling/ -v` |
| QA-SECURITY-AUDIT | Security patterns | `ruff check . --select S` |

---

## Invocation

### Full Deployment (8 agents)

```
/qa-party
```

Deploys all 8 QA agents in parallel.

### Quick Deployment (4 agents)

```
/qa-party --quick
```

Deploys 4 critical agents (BUILD, LINT-BACKEND, LINT-FRONTEND, DOCKER).

### Extended Deployment (12 agents)

```
/qa-party --full
```

Deploys all 12 agents including domain-specific test splits.

### Single Domain

```
/qa-party frontend
/qa-party backend
/qa-party docker
```

Deploys agents for specific domain only.

---

## Spawn Pattern

```python
# Deploy all 8 QA agents in parallel
# Wall-clock = slowest agent timeout

spawn_parallel([
    Task(subagent_type="general-purpose", description="QA-FRONTEND-BUILD",
         prompt="""
Run frontend build validation:
```bash
cd /Users/aaronmontgomery/Autonomous-Assignment-Program-Manager/frontend
npm run build 2>&1
```
Report: PASS/FAIL with error count and key errors if any.
"""),

    Task(subagent_type="general-purpose", description="QA-FRONTEND-LINT",
         prompt="""
Run frontend lint validation:
```bash
cd /Users/aaronmontgomery/Autonomous-Assignment-Program-Manager/frontend
npm run lint 2>&1
npm run type-check 2>&1
```
Report: PASS/FAIL with error count and categories.
"""),

    Task(subagent_type="general-purpose", description="QA-FRONTEND-TESTS",
         prompt="""
Run frontend test suite:
```bash
cd /Users/aaronmontgomery/Autonomous-Assignment-Program-Manager/frontend
npm test -- --passWithNoTests 2>&1
```
Report: PASS/FAIL with test counts (passed/failed/skipped).
"""),

    Task(subagent_type="general-purpose", description="QA-BACKEND-LINT",
         prompt="""
Run backend lint validation:
```bash
cd /Users/aaronmontgomery/Autonomous-Assignment-Program-Manager/backend
./venv/bin/ruff check . 2>&1
./venv/bin/ruff format --check . 2>&1
```
Report: PASS/FAIL with error count and categories.
"""),

    Task(subagent_type="general-purpose", description="QA-BACKEND-TESTS",
         prompt="""
Run backend test suite:
```bash
cd /Users/aaronmontgomery/Autonomous-Assignment-Program-Manager/backend
./venv/bin/python -m pytest tests/ -v --tb=short 2>&1 | head -100
```
Report: PASS/FAIL with test counts (passed/failed/errors).
"""),

    Task(subagent_type="general-purpose", description="QA-DOCKER-HEALTH",
         prompt="""
Check Docker container health:
```bash
docker compose ps 2>&1
docker compose logs --tail=20 backend 2>&1
docker compose logs --tail=20 mcp-server 2>&1
```
Report: Container status (running/stopped) and any error logs.
"""),

    Task(subagent_type="general-purpose", description="QA-API-SMOKE",
         prompt="""
Run API smoke tests:
```bash
curl -s http://localhost:8000/health 2>&1
curl -s http://localhost:8000/api/v1/docs 2>&1 | head -20
```
Report: PASS/FAIL with response status and any errors.
"""),

    Task(subagent_type="general-purpose", description="QA-MCP-TOOLS",
         prompt="""
Validate MCP server tools:
```bash
docker compose exec mcp-server python -c "from scheduler_mcp.server import mcp; print(f'Tools loaded: {len(mcp.tools)}')" 2>&1
```
Report: PASS/FAIL with tool count.
"""),
])
```

---

## Output Format

### Per-Agent Report

Each QA agent reports:

```markdown
## QA Agent: [NAME]

**Status:** PASS / FAIL / PARTIAL
**Duration:** Xs

### Results
- [Metric 1]: [value]
- [Metric 2]: [value]

### Errors (if any)
```
[error output]
```

### Recommended Fix
[If FAIL, suggest fix]
```

### Consolidated Dashboard

```markdown
## QA_PARTY Validation Dashboard

| Agent | Status | Duration | Key Metric |
|-------|--------|----------|------------|
| QA-FRONTEND-BUILD | PASS | 45s | 0 errors |
| QA-FRONTEND-LINT | FAIL | 12s | 6 errors |
| QA-FRONTEND-TESTS | FAIL | 8s | 164 failing |
| QA-BACKEND-LINT | PASS | 5s | 0 errors |
| QA-BACKEND-TESTS | PASS | 120s | 312/312 passed |
| QA-DOCKER-HEALTH | PASS | 3s | 7/7 running |
| QA-API-SMOKE | PASS | 1s | 200 OK |
| QA-MCP-TOOLS | PASS | 2s | 70 tools |

### Overall: 6/8 PASS (75%)

### Blocking Issues
1. Frontend lint: 6 errors (`no-this-alias` × 5, `no-assign-module-variable` × 1)
2. Frontend tests: 164 failing (Jest transform broken)

### Non-Blocking Issues
[None]

### Recommended CCW Tasks
1. Fix `no-this-alias` violations in `src/lib/validation/error-messages.ts`
2. Fix Jest transform configuration
```

---

## Failure Recovery

### Minimum Viable QA

Validation can proceed with degraded confidence if:
- QA-BACKEND-LINT passes ✓
- QA-BACKEND-TESTS passes ✓
- QA-DOCKER-HEALTH passes ✓

### Circuit Breaker

If Docker is down: Skip QA-API-SMOKE, QA-MCP-TOOLS, QA-BACKEND-TESTS (containerized).

---

## Integration with CCW

### Pre-CCW Validation
```
/qa-party --quick
```
Establish baseline before CCW burns tasks.

### Post-CCW Validation
```
/qa-party --full
```
Comprehensive validation after CCW completes.

### Report to CCW
After running `/qa-party`, generate CCW directive:

```markdown
## CCW Task from QA_PARTY

QA-FRONTEND-LINT failed with 6 errors:

Files to fix:
- `frontend/src/lib/validation/error-messages.ts` (lines 18, 40, 68, 97, 315)
- `frontend/src/utils/debounce.ts` (no-this-alias)
- `frontend/src/utils/lazy-loader.ts` (no-assign-module-variable)

Pattern to apply:
```typescript
// Before (triggers no-this-alias)
const self = this;
callback.apply(self, args);

// After
callback.apply(this, args);
// OR use arrow function
```

Acceptance: `npm run lint` exits 0.
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `search-party` | Reconnaissance before QA (G-2 function) |
| `code-review` | IG teams invoke for code quality checks |
| `systematic-debugger` | When QA fails, debug root cause |
| `test-writer` | When QA reveals missing coverage |
| `lint-monorepo` | Unified linting for Python/TypeScript |
| `security-audit` | Security-focused code audit |

### Skill vs Subagent Types

**Important distinction:**

| Type | Mechanism | Examples |
|------|-----------|----------|
| **Skills** | Invoke via Skill tool | `/code-review`, `/test-writer`, `/lint-monorepo` |
| **Subagents** | Spawn via Task tool | `Explore`, `Plan`, `general-purpose` |

IG teams use `subagent_type="general-purpose"` with Task tool, but they CAN invoke skills like `/code-review` within their execution.

---

## Command Structure

### Oversight Hierarchy

QA/Testing falls under **IG (Inspector General)** function, not G-2 (Intel):

```
ORCHESTRATOR (you)
    └── COORD_QUALITY (IG Commander - Inspections & Quality)
            ├── QA-IG-BACKEND-ROUTES (10 test agents)
            ├── QA-IG-BACKEND-SERVICES (10 test agents)
            ├── QA-IG-BACKEND-MODELS (10 test agents)
            ├── QA-IG-BACKEND-SCHEDULING (10 test agents)
            ├── QA-IG-BACKEND-RESILIENCE (10 test agents)
            ├── QA-IG-BACKEND-ACGME (10 test agents)
            ├── QA-IG-FRONTEND-COMPONENTS (10 test agents)
            ├── QA-IG-FRONTEND-HOOKS (10 test agents)
            ├── QA-IG-FRONTEND-PAGES (10 test agents)
            ├── QA-IG-LINT-BACKEND (10 lint agents)
            ├── QA-IG-LINT-FRONTEND (10 lint agents)
            └── QA-IG-SECURITY (10 audit agents)
                    = 120 QA agents
```

**Staff Distinction:**
- **G-2 (SEARCH_PARTY)**: Intelligence/Reconnaissance - explores and gathers information
- **IG (QA_PARTY)**: Inspector General - tests, validates, and ensures quality

### Coordinator Responsibilities

| Role | Agent | Responsibility |
|------|-------|----------------|
| **IG Commander** | COORD_QUALITY | Deploys 12 IG teams, synthesizes results, assigns follow-up |
| **IG Teams** | QA-IG-* (12) | Each manages 10 test workers, reports to COORD_QUALITY |
| **Workers** | QA agents (120) | Execute single test file/slice, report PASS/FAIL |
| **Auditor** | DELEGATION_AUDITOR | Post-run metrics (agent efficiency, failure patterns) |
| **AAR** | COORD_AAR | After Action Review (what went well, what didn't) |

### Coordinator Spawn Pattern

```python
# ORCHESTRATOR spawns COORD_QUALITY who spawns 12 G-2s
Task(
    subagent_type="general-purpose",
    description="COORD_QUALITY: QA_PARTY Commander",
    prompt="""
## Agent: COORD_QUALITY
You are the Quality Coordinator commanding QA_PARTY deployment.

## Mission
Deploy 12 IG QA teams in parallel. Each team runs 10 test workers.
Collect all reports and synthesize into unified dashboard.

## Your IG Teams to Deploy
1. QA-IG-BACKEND-ROUTES
2. QA-IG-BACKEND-SERVICES
3. QA-IG-BACKEND-MODELS
4. QA-IG-BACKEND-SCHEDULING
5. QA-IG-BACKEND-RESILIENCE
6. QA-IG-BACKEND-ACGME
7. QA-IG-FRONTEND-COMPONENTS
8. QA-IG-FRONTEND-HOOKS
9. QA-IG-FRONTEND-PAGES
10. QA-IG-LINT-BACKEND
11. QA-IG-LINT-FRONTEND
12. QA-IG-SECURITY

## Spawn all 12 in parallel using Task tool with subagent_type="general-purpose"

## After all report back:
1. Aggregate results into dashboard
2. Identify blocking issues
3. Generate CCW task list for failures
4. Report to ORCHESTRATOR
"""
)
```

### IG Team Spawn Pattern (Each Team Deploys 10 Workers)

```python
# Example: QA-IG-BACKEND-ROUTES spawning 10 workers
Task(
    subagent_type="general-purpose",
    description="QA-IG-BACKEND-ROUTES",
    prompt="""
## Agent: QA-IG-BACKEND-ROUTES
You are an IG QA team commanding 10 test workers for backend routes.

## Mission
Run pytest on route test files. Distribute across 10 parallel workers.

## Your Test Slice
```bash
cd /Users/aaronmontgomery/Autonomous-Assignment-Program-Manager/backend
find tests -name "test_*routes*.py" -o -name "test_*api*.py"
```

## Spawn 10 workers (or use pytest-xdist)
Option A: Task tool with 10 parallel agents
Option B: pytest -n 10 --dist loadfile tests/routes/

## Report Format
| Worker | Test File | Status | Passed | Failed | Errors |
|--------|-----------|--------|--------|--------|--------|
| 01 | test_auth_routes.py | PASS | 12 | 0 | 0 |
| 02 | test_schedule_routes.py | FAIL | 8 | 2 | 0 |
...

Report to COORD_QUALITY with this table.
"""
)
```

---

## Scaled Deployment: 120 QA Agents

### How to Get 120 QA Testers Going

The key is **test file distribution**. Instead of running one agent per validation type, we split the work:

| Validation Type | Approximate Files | Agents |
|-----------------|-------------------|--------|
| Backend test files | ~60 files | 60 agents |
| Frontend test files | ~50 files | 50 agents |
| Frontend components (untested) | ~254 | 10 agents (batch) |
| **Total** | | **120 agents** |

### Invocation

```
/qa-party --scale 120
```

### Discovery Phase (Run First)

Before spawning 120 agents, discover test targets:

```bash
# Backend: Find all test files
find backend/tests -name "test_*.py" -type f | wc -l  # ~60 files

# Frontend: Find all test files
find frontend/__tests__ -name "*.test.ts" -o -name "*.test.tsx" | wc -l  # ~50 files

# Frontend: Find untested components
find frontend/src/components -name "*.tsx" | wc -l  # ~254 components
```

### Scaled Spawn Pattern

```python
# Phase 1: Discover test files
import subprocess

# Backend tests
backend_tests = subprocess.run(
    ["find", "backend/tests", "-name", "test_*.py", "-type", "f"],
    capture_output=True, text=True
).stdout.strip().split("\n")

# Frontend tests
frontend_tests = subprocess.run(
    ["find", "frontend/__tests__", "-name", "*.test.ts*"],
    capture_output=True, text=True
).stdout.strip().split("\n")

# Phase 2: Generate 120 parallel tasks
tasks = []

# 60 backend test agents (one per file)
for i, test_file in enumerate(backend_tests[:60]):
    tasks.append(
        Task(
            subagent_type="general-purpose",
            description=f"QA-BACKEND-{i:02d}",
            prompt=f"""
Run single backend test file:
```bash
cd /Users/.../backend
./venv/bin/python -m pytest {test_file} -v --tb=short 2>&1
```
Report: PASS/FAIL with test count.
"""
        )
    )

# 50 frontend test agents (one per file)
for i, test_file in enumerate(frontend_tests[:50]):
    tasks.append(
        Task(
            subagent_type="general-purpose",
            description=f"QA-FRONTEND-{i:02d}",
            prompt=f"""
Run single frontend test file:
```bash
cd /Users/.../frontend
npm test -- {test_file} --passWithNoTests 2>&1
```
Report: PASS/FAIL with test count.
"""
        )
    )

# 10 component batch agents (25 components each)
components = [...254 component files...]
batch_size = 25
for i in range(10):
    batch = components[i*batch_size:(i+1)*batch_size]
    tasks.append(
        Task(
            subagent_type="general-purpose",
            description=f"QA-COMPONENT-BATCH-{i:02d}",
            prompt=f"""
Check component testability for batch:
{chr(10).join(batch)}

For each component, report:
- Has test file: Y/N
- Export issues: Y/N
- Dependencies missing: Y/N
"""
        )
    )

# Spawn all 120 in parallel
spawn_parallel(tasks)
```

### Alternative: Pytest-xdist Native Parallelism

If you want pytest's native parallelism instead of Task tool parallelism:

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 120 parallel workers
cd backend
pytest tests/ -n 120 --dist loadfile
```

This uses pytest's built-in parallelism, which:
- Handles test isolation automatically
- Distributes by file (--dist loadfile) or by test (--dist load)
- Aggregates results natively

### Hybrid Approach: 12 IG Teams × 10 Test Slices

Model after SEARCH_PARTY structure (using IG instead of G-2):

| IG QA Team | Domain | 10 Test Slices |
|------------|--------|----------------|
| QA-IG-BACKEND-ROUTES | `tests/routes/` | 10 route test files |
| QA-IG-BACKEND-SERVICES | `tests/services/` | 10 service test files |
| QA-IG-BACKEND-MODELS | `tests/models/` | 10 model test files |
| QA-IG-BACKEND-SCHEDULING | `tests/scheduling/` | 10 scheduling tests |
| QA-IG-BACKEND-RESILIENCE | `tests/resilience/` | 10 resilience tests |
| QA-IG-BACKEND-ACGME | `tests/ -m acgme` | 10 ACGME test files |
| QA-IG-FRONTEND-COMPONENTS | `__tests__/components/` | 10 component tests |
| QA-IG-FRONTEND-HOOKS | `__tests__/hooks/` | 10 hook tests |
| QA-IG-FRONTEND-PAGES | `__tests__/pages/` | 10 page tests |
| QA-IG-LINT-BACKEND | `ruff` by module | 10 module batches |
| QA-IG-LINT-FRONTEND | `eslint` by dir | 10 directory batches |
| QA-IG-SECURITY | Security checks | 10 audit patterns |

Each IG team spawns 10 workers = 120 parallel QA agents.

### Practical Limits

| Constraint | Limit | Mitigation |
|------------|-------|------------|
| **IDE stability** | **1-2 direct spawns** | **ORCHESTRATOR spawns COORD_QUALITY only** |
| Task tool concurrency | ~10-20 parallel | Batch into IG teams |
| pytest-xdist workers | ~CPU cores × 2 | Use `-n auto` |
| Jest workers | ~CPU cores | Use `--maxWorkers` |
| Memory per agent | ~100MB | Monitor with `docker stats` |

### CRITICAL: IDE Crash Prevention

**DO NOT** have ORCHESTRATOR spawn 8+ agents directly. This causes IDE seizure and crashes.

**CORRECT Pattern:**
```
ORCHESTRATOR → spawns 1 COORD_QUALITY (IG Commander)
                    ↓
              COORD_QUALITY manages 12 IG teams internally
              (uses pytest-xdist, jest parallel, or sequential Task spawns)
```

**WRONG Pattern:**
```
ORCHESTRATOR → spawns 8+ QA agents directly → IDE CRASH
```

The coordinator absorbs the parallelism complexity. ORCHESTRATOR only ever spawns 1-2 coordinators at a time.

### Recommendation

For this codebase:

```
/qa-party --scale 120
```

Deploys:
- 12 G-2 QA agents (like SEARCH_PARTY)
- Each G-2 runs 10 test slices via pytest-xdist or jest parallel
- Total: 120 parallel test executions
- Wall-clock: ~60-120 seconds (limited by slowest test suite)

---

*QA_PARTY: Eight agents, one validation, zero marginal cost. The failures are the signal.*
