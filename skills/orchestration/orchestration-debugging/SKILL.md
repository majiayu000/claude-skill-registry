---
name: ORCHESTRATION_DEBUGGING
description: Troubleshoot agent & tool failures in scheduling orchestration. Use when MCP tools fail, agent communication breaks, constraint engines error, or database operations timeout. Provides systematic incident response and root cause analysis.
---

# ORCHESTRATION_DEBUGGING

A comprehensive debugging skill for diagnosing and resolving failures in the AI-orchestrated scheduling system, including MCP tool integration, agent workflows, constraint engine, and database operations.

## When This Skill Activates

- **MCP Tool Failures**: Timeout, connection errors, or incorrect responses
- **Agent Communication Issues**: Multi-agent workflows failing to coordinate
- **Constraint Engine Errors**: OR-Tools solver failures, constraint conflicts
- **Database Operation Failures**: Deadlocks, connection pool exhaustion, slow queries
- **Schedule Generation Failures**: Validation errors, compliance violations, infeasible schedules
- **Background Task Issues**: Celery worker crashes, task timeouts, queue backlogs
- **API Integration Failures**: Backend API errors, authentication issues, rate limiting

## Overview

This skill provides structured workflows for:

1. **Incident Review**: Post-mortem analysis with root cause identification
2. **Log Analysis**: Systematic log parsing across services (backend, MCP, Celery, database)
3. **Root Cause Analysis**: 5-whys investigation methodology
4. **Common Failure Patterns**: Catalog of known issues with solutions
5. **Debugging Checklist**: Step-by-step troubleshooting for each component

## Architecture Context

### System Components

```
Claude Agent
    ↓ (MCP Protocol)
MCP Server (29+ tools)
    ↓ (HTTP API)
FastAPI Backend
    ↓ (SQLAlchemy)
PostgreSQL Database
    ↓ (Async Tasks)
Celery + Redis
```

### Common Failure Points

| Layer | Component | Failure Mode |
|-------|-----------|--------------|
| **Agent** | Claude Code | Token limits, context overflow, skill conflicts |
| **MCP** | Tool invocation | Timeout, serialization errors, auth failures |
| **API** | FastAPI routes | Validation errors, database session issues |
| **Service** | Business logic | Constraint violations, ACGME compliance failures |
| **Solver** | OR-Tools engine | Infeasible constraints, timeout, memory exhaustion |
| **Database** | PostgreSQL | Deadlocks, connection pool exhaustion, slow queries |
| **Tasks** | Celery workers | Task timeout, serialization errors, queue backlog |

## Core Debugging Phases

### Phase 1: DETECTION
**Goal:** Identify what failed and where

```
1. Check error visibility
   - User-facing error message
   - API response logs
   - Backend service logs
   - Database query logs
   - MCP server logs

2. Establish failure scope
   - Single request or systemic?
   - Reproducible or intermittent?
   - User-specific or system-wide?
```

### Phase 2: DIAGNOSIS
**Goal:** Understand why it failed

```
1. Trace request path
   - Agent → MCP → API → Service → Database
   - Identify where the chain breaks

2. Collect evidence
   - Error stack traces
   - Recent code changes (git log)
   - Database state (queries, locks)
   - System resources (CPU, memory, connections)
```

### Phase 3: RESOLUTION
**Goal:** Fix the issue

```
1. Implement fix
   - Code changes
   - Configuration updates
   - Database repairs

2. Verify fix
   - Reproduce original failure
   - Confirm fix resolves it
   - Check for regressions
```

### Phase 4: PREVENTION
**Goal:** Prevent recurrence

```
1. Document incident
   - Root cause
   - Fix applied
   - Lessons learned

2. Implement safeguards
   - Add tests
   - Add monitoring
   - Update documentation
```

## Workflow Files

### Workflows/incident-review.md
Post-mortem template for systematic incident analysis:
- Timeline reconstruction
- Impact assessment
- Root cause identification (5-whys)
- Remediation actions
- Prevention measures

**Use when:** After resolving a major incident or when debugging a complex failure

### Workflows/log-analysis.md
Log parsing and correlation across services:
- Log location discovery
- Error pattern extraction
- Cross-service correlation
- Timeline reconstruction
- Anomaly detection

**Use when:** Error is unclear or spans multiple services

### Workflows/root-cause-analysis.md
5-whys investigation methodology:
- Problem statement definition
- Iterative questioning
- Evidence gathering
- Root cause identification

**Use when:** Surface-level fix is clear but underlying cause is not

## Reference Files

### Reference/common-failure-patterns.md
Catalog of known issues with symptoms and fixes:
- Database connection failures
- MCP tool timeouts
- Constraint engine errors
- Agent communication failures
- Each with: Symptoms → Diagnosis → Fix

**Use when:** Encountering a familiar-looking error

### Reference/debugging-checklist.md
Step-by-step troubleshooting guide:
- Service health checks
- Log verification
- Database inspection
- MCP tool status
- Agent state verification

**Use when:** Starting investigation with no clear direction

## Key Files to Inspect

### Backend Logs
```bash
# Application logs
docker-compose logs backend --tail=200 --follow

# Uvicorn access logs
docker-compose logs backend | grep "POST\|GET\|PUT\|DELETE"

# Error-specific logs
docker-compose logs backend 2>&1 | grep -i "error\|exception\|failed"
```

### MCP Server Logs
```bash
# MCP server output
docker-compose logs mcp-server --tail=100 --follow

# Tool invocation logs
docker-compose logs mcp-server | grep "tool_call\|error"

# API connectivity
docker-compose exec mcp-server curl -s http://backend:8000/health
```

### Database Logs
```bash
# Connect to database
docker-compose exec db psql -U scheduler -d residency_scheduler

# Check active queries
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

# Check locks
SELECT * FROM pg_locks WHERE NOT granted;
```

### Celery Logs
```bash
# Worker logs
docker-compose logs celery-worker --tail=100 --follow

# Beat scheduler logs
docker-compose logs celery-beat --tail=50 --follow

# Check queue status
docker-compose exec redis redis-cli LLEN celery
```

## Output Format

### Quick Status Check
```
SYSTEM HEALTH: [GREEN|YELLOW|ORANGE|RED]

Backend API: ✓ Responding (200ms avg)
MCP Server: ✓ Connected (29 tools available)
Database: ✓ 8/20 connections used
Celery: ✗ 3 failed tasks in queue
Redis: ✓ Connected

ISSUES DETECTED:
1. Celery worker timeout on schedule generation task
2. 2 database deadlocks in last hour

RECOMMENDED ACTION: Review celery worker logs and database lock contention
```

### Full Incident Report
```markdown
## INCIDENT REPORT: [Title]

**Date**: 2025-12-26 14:32 UTC
**Severity**: [LOW|MEDIUM|HIGH|CRITICAL]
**Status**: [INVESTIGATING|RESOLVED|MONITORING]
**Reporter**: [Agent/User/Automated]

### Summary
One-sentence description of what failed

### Timeline
- 14:30 - First error detected
- 14:31 - Service degraded
- 14:35 - Fix implemented
- 14:40 - Service restored

### Impact
- Users affected: [number or "all"]
- Data integrity: [preserved/compromised]
- ACGME compliance: [maintained/violated]
- Downtime: [duration]

### Root Cause
Detailed explanation using 5-whys methodology

### Resolution
What was done to fix the issue

### Prevention
How to prevent this in the future

### Action Items
- [ ] Add monitoring for [metric]
- [ ] Create test case for [scenario]
- [ ] Update documentation for [component]
```

## Error Handling Best Practices

### 1. Preserve Context
```python
# Bad - loses context
try:
    result = await some_operation()
except Exception:
    raise HTTPException(status_code=500, detail="Operation failed")

# Good - preserves stack trace
try:
    result = await some_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise HTTPException(
        status_code=500,
        detail="Operation failed - check logs for details"
    )
```

### 2. Log Diagnostic Information
```python
logger.info(f"Starting operation with params: {params}")
logger.debug(f"Intermediate state: {state}")
logger.error(f"Operation failed at step {step}", exc_info=True)
```

### 3. Add Request IDs
```python
# For tracing requests across services
request_id = str(uuid.uuid4())
logger.info(f"[{request_id}] Processing schedule generation")
```

## Integration with Other Skills

### With systematic-debugger
For code-level debugging:
1. ORCHESTRATION_DEBUGGING identifies which component failed
2. systematic-debugger investigates the code

### With production-incident-responder
For production emergencies:
1. production-incident-responder handles immediate crisis
2. ORCHESTRATION_DEBUGGING performs post-mortem

### With automated-code-fixer
For automated fixes:
1. ORCHESTRATION_DEBUGGING identifies root cause
2. automated-code-fixer applies tested solution

## Escalation Criteria

**ALWAYS escalate to human when:**
1. Data corruption detected
2. Security vulnerability discovered
3. ACGME compliance violated
4. Multi-hour outage
5. Root cause unclear after investigation
6. Fix requires database migration or schema change

**Can handle automatically:**
1. Configuration issues
2. Known failure patterns with documented fixes
3. Resource exhaustion (restart services)
4. Transient network errors
5. Log analysis and report generation

## Monitoring Recommendations

After resolving incidents, add monitoring for:
- Error rate by endpoint
- Request latency (p50, p95, p99)
- Database connection pool usage
- Celery queue depth
- MCP tool success rate
- Schedule generation success rate

## References

- `/docs/development/DEBUGGING_WORKFLOW.md` - Overall debugging methodology
- `/docs/development/CI_CD_TROUBLESHOOTING.md` - CI/CD specific patterns
- `/mcp-server/RESILIENCE_MCP_INTEGRATION.md` - MCP tool documentation
- `/backend/app/core/logging.py` - Logging configuration
- `Workflows/` - Detailed workflow templates
- `Reference/` - Common patterns and checklists
