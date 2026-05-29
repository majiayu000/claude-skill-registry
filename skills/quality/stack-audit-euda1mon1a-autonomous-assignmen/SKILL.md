---
name: stack-audit
description: Comprehensive stack health audit for codebase and infrastructure. Runs 10 health checks covering frontend, backend, migrations, Docker, API integrity, and backup status. Use routinely to prevent "time loops" from accumulated issues.
model_tier: haiku
parallel_hints:
  can_parallel_with: [qa-party, lint-monorepo]
  must_serialize_with: []
  preferred_batch_size: 1
context_hints:
  max_file_context: 10
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "status.*RED"
    reason: "Critical health issues detected"
  - pattern: "Sacred Backups.*FAIL"
    reason: "Missing backups before database changes"
---

# Stack Health Audit

Comprehensive codebase and infrastructure health monitoring to prevent accumulated issues from causing development "time loops".

## When to Use This Skill

- **Routinely:** At session start and before major changes
- **Before commits:** Quick validation before committing
- **After deployments:** Verify stack health post-deploy
- **Debugging:** When something feels off but you can't pinpoint it
- **CI/CD integration:** As part of automated health checks

## How to Run

### Quick Mode (Skip Build)
```bash
python3 scripts/ops/stack_audit.py --quick
```

### Full Audit
```bash
python3 scripts/ops/stack_audit.py
```

### JSON Output (for parsing)
```bash
python3 scripts/ops/stack_audit.py --json
```

### Dry Run (no report file)
```bash
python3 scripts/ops/stack_audit.py --no-report
```

## 10 Health Checks

| Check | What It Validates |
|-------|-------------------|
| **Frontend Type Check** | TypeScript strict mode errors |
| **Frontend Lint** | ESLint warnings and errors |
| **Frontend Build** | Next.js build success (skipped in --quick) |
| **Backend Lint (Ruff)** | Python linting |
| **Backend Type Check (mypy)** | Python type checking |
| **Migration State** | Alembic migration consistency |
| **Alembic Head Sync** | DB is at latest migration head |
| **Docker Containers** | Container health status |
| **API Health** | Endpoint availability, CORS, pagination, schema |
| **Sacred Backups** | Backup existence and freshness |

## Status Levels

| Status | Meaning | Exit Code |
|--------|---------|-----------|
| **GREEN** | All checks pass | 0 |
| **YELLOW** | Warnings only | 1 |
| **RED** | Errors detected | 2 |

## Report Location

Reports are written to:
```
.claude/dontreadme/stack-health/YYYY-MM-DD_HHMMSS.md
```

Trend analysis compares current run to previous runs for pattern detection.

## Integration with Celery

The audit runs automatically via Celery every 4 hours:
```python
# backend/app/tasks/stack_health_tasks.py
@celery.task(name="stack.health_check")
def stack_health_check():
    """Run comprehensive stack health audit."""
```

## Antigravity Recommendations

The following checks were added based on antigravity session recommendations:

1. **API Pagination** - Verify APIs handle limit/offset correctly
2. **Schema Validation** - Check activity_type enum values match expected
3. **Alembic Head Sync** - Ensure DB migrations are current
4. **Block Dates API** - Verify blocks endpoint returns valid data
5. **CORS Headers** - Check CORS configuration
6. **Sacred Backups** - Verify backups exist before major changes

## Example Output

```
Running stack health audit...
  [1/10] Frontend type-check...
  [2/10] Frontend lint...
  [3/10] Frontend build...
  [4/10] Backend lint (Ruff)...
  [5/10] Backend type-check (mypy)...
  [6/10] Migration state...
  [7/10] Alembic head sync...
  [8/10] Docker containers...
  [9/10] API health & data integrity...
  [10/10] Sacred backups...

======================================================================
Stack Health: GREEN
======================================================================
  Frontend Type Check: PASS (0 issues)
  Frontend Lint: PASS (0 issues)
  ...
```

## When Issues Are Found

### RED Status Actions

1. Review the generated report in `.claude/dontreadme/stack-health/`
2. Address blocking issues first (FAIL status)
3. Re-run after fixes to confirm resolution
4. Check trend analysis for recurring patterns

### Common Fixes

| Issue | Fix |
|-------|-----|
| Frontend Type Errors | `npm run type-check` then fix errors |
| Alembic Out of Sync | `alembic upgrade head` |
| Missing Backups | `./scripts/backup_db.sh` before schema changes |
| Docker Unhealthy | `docker-compose restart <service>` |
| API Errors | Check backend logs: `docker-compose logs -f backend` |

## Related Skills

- `/lint-monorepo` - Focus on linting only
- `/qa-party` - Comprehensive QA validation
- `/deployment-validator` - Pre-deploy validation
- `/systematic-debugger` - When issues need investigation

---
*Script location: `scripts/ops/stack_audit.py`*
*Celery task: `backend/app/tasks/stack_health_tasks.py`*
