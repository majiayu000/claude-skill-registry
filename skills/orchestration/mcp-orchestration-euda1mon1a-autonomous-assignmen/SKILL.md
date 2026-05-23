---
name: MCP_ORCHESTRATION
description: Tool discovery, routing, chaining, error handling, and composition for the 34+ MCP scheduling tools. Use when orchestrating complex multi-tool workflows, handling MCP errors, or discovering available capabilities.
model_tier: haiku
parallel_hints:
  can_parallel_with: [code-review, test-writer, security-audit]
  must_serialize_with: [database-migration]
  preferred_batch_size: 5
---

# MCP Orchestration Skill

Expert orchestration of Model Context Protocol (MCP) tools for medical residency scheduling. Handles tool discovery, intelligent routing, error recovery, and complex multi-tool composition.

## When This Skill Activates

- Multi-step workflows requiring 2+ MCP tools
- Error recovery from failed MCP calls
- Tool capability discovery needed
- Complex scheduling operations requiring orchestration
- Debugging MCP integration issues
- Performance optimization of tool chains

## Overview

The MCP server exposes 34+ specialized tools across 6 categories:

| Category | Tools | Purpose |
|----------|-------|---------|
| **Core Scheduling** | 5 | Validation, generation, conflict detection, swaps |
| **Resilience Framework** | 13 | Utilization, contingency, defense levels, homeostasis |
| **Background Tasks** | 4 | Celery task management (start, status, cancel, list) |
| **Deployment** | 7 | Validation, security, smoke tests, rollback |
| **Empirical Testing** | 5 | Benchmarking solvers, constraints, modules |
| **Resources** | 2 | Schedule status, compliance summary |

**Total: 36 tools** available for orchestration.

## Key Orchestration Phases

### Phase 1: Discovery
1. Identify available tools matching task requirements
2. Check tool availability and health
3. Verify prerequisites (DB connection, API availability)
4. Map inputs/outputs between dependent tools

### Phase 2: Planning
1. Create execution DAG (directed acyclic graph)
2. Identify parallel vs sequential dependencies
3. Plan error handling checkpoints
4. Estimate execution time and resource usage

### Phase 3: Execution
1. Execute tools in dependency order
2. Handle transient errors with retry logic
3. Propagate results through tool chain
4. Monitor progress and resource utilization

### Phase 4: Recovery
1. Detect permanent vs transient failures
2. Execute fallback strategies
3. Rollback partial state changes if needed
4. Log errors for human escalation

## Orchestration Patterns

### Pattern 1: Sequential Chain
```
Tool A → Tool B → Tool C
```
Each tool depends on previous tool's output.

**Example:** Schedule Generation Pipeline
```
validate_deployment → generate_schedule → validate_schedule → run_smoke_tests
```

### Pattern 2: Parallel Fan-Out
```
       → Tool B
Tool A → Tool C
       → Tool D
```
Multiple tools execute concurrently on same input.

**Example:** Comprehensive Schedule Analysis
```
                → validate_schedule
schedule_status → detect_conflicts
                → check_utilization_threshold
```

### Pattern 3: Map-Reduce
```
Tool A → [Tool B, Tool B, Tool B] → Tool C
```
Parallel execution followed by aggregation.

**Example:** Multi-Person Swap Analysis
```
For each faculty:
    analyze_swap_candidates → aggregate_results → rank_by_score
```

### Pattern 4: Conditional Routing
```
Tool A → Decision → Tool B (if condition)
               → Tool C (else)
```

**Example:** Deployment Workflow
```
validate_deployment → (if valid) → promote_to_production
                   → (else)      → rollback_deployment
```

## Key Files

| File | Purpose |
|------|---------|
| `Workflows/tool-discovery.md` | MCP endpoint scanning and capability mapping |
| `Workflows/error-handling.md` | Retry logic, fallback strategies, escalation |
| `Workflows/tool-composition.md` | DAG patterns, parallel execution, result synthesis |
| `Reference/mcp-tool-index.md` | Complete tool catalog with I/O schemas |
| `Reference/tool-error-patterns.md` | Known failure modes and workarounds |
| `Reference/composition-examples.md` | Real-world multi-tool chains |

## Output

This skill produces:

1. **Execution Plans**: DAG of tool dependencies with timing estimates
2. **Error Reports**: Categorized failures with recovery recommendations
3. **Performance Metrics**: Latency, throughput, resource usage
4. **Capability Maps**: Which tools can satisfy which requirements

## Error Handling Strategy

See `Workflows/error-handling.md` for complete strategy. Key principles:

1. **Retry Transient Errors**: Network timeouts, rate limits, DB locks
2. **Fail Fast on Permanent Errors**: Invalid inputs, missing resources
3. **Graceful Degradation**: Use cached data or reduced functionality
4. **Human Escalation**: Alert on unrecoverable errors

## Integration with MCP Server

The MCP server runs in Docker container `mcp-server` and exposes tools via:

- **STDIO Transport**: For Claude Desktop integration
- **HTTP Transport** (dev mode): Port 8080 for debugging

### Health Check
```bash
docker-compose logs -f mcp-server
docker-compose exec mcp-server python -c \
  "from scheduler_mcp.server import mcp; print(f'Tools: {len(mcp.tools)}')"
```

### API Connectivity Test
```bash
docker-compose exec mcp-server curl -s http://backend:8000/health
```

## Common Workflows

### 1. Schedule Safety Check
**Goal:** Comprehensive validation before deployment
```
Parallel:
  - validate_schedule(date_range)
  - detect_conflicts(date_range)
  - check_utilization_threshold()
  - run_contingency_analysis_resilience(N-1, N-2)

Aggregate results → Generate safety report
```

### 2. Emergency Coverage Response
**Goal:** Handle faculty absence with minimal disruption
```
1. run_contingency_analysis(scenario="faculty_absence", person_ids=[...])
2. For each resolution_option:
     analyze_swap_candidates(requester_id, assignment_id)
3. execute_sacrifice_hierarchy(target_level="yellow", simulate=True)
4. get_static_fallbacks() → Identify pre-computed schedules
```

### 3. Deployment Pipeline
**Goal:** Safe production deployment
```
1. validate_deployment(env="staging", git_ref="main")
2. run_security_scan(git_ref="main")
3. If all passed:
     run_smoke_tests(env="staging", suite="full")
4. If smoke tests passed:
     promote_to_production(staging_version, approval_token)
5. Monitor: get_deployment_status(deployment_id)
```

### 4. Performance Optimization
**Goal:** Identify and remove low-value code
```
Parallel:
  - benchmark_solvers(scenario_count=20)
  - benchmark_constraints(test_schedules="historical")
  - benchmark_resilience(modules=all)
  - module_usage_analysis(entry_points=["main", "api", "scheduling"])

Aggregate → Generate cut list → ablation_study(module_path)
```

---

## Concrete Implementation Examples

The workflows above are high-level. This section provides detailed, runnable code examples.

### Example 1: Parallel Safety Check with Error Handling

```python
"""Complete safety check implementation with error handling."""
import asyncio
from typing import Dict, List, Any
from datetime import date, datetime

async def comprehensive_safety_check(
    start_date: date,
    end_date: date,
    timeout_seconds: int = 60
) -> Dict[str, Any]:
    """
    Orchestrate parallel safety checks with robust error handling.

    Args:
        start_date: Schedule validation start date
        end_date: Schedule validation end date
        timeout_seconds: Maximum time to wait for all checks

    Returns:
        Safety report with pass/fail status and recommendations
    """
    # Phase 1: Define all checks with timeout wrapper
    async def safe_call(coro, check_name: str):
        """Wrapper that handles timeouts and exceptions."""
        try:
            result = await asyncio.wait_for(coro, timeout=30)
            return {"success": True, "data": result, "check": check_name}
        except asyncio.TimeoutError:
            return {"success": False, "error": "Timeout after 30s", "check": check_name}
        except Exception as e:
            return {"success": False, "error": str(e), "check": check_name}

    # Phase 2: Execute checks in parallel
    checks = [
        safe_call(validate_schedule_mcp(start_date, end_date), "validation"),
        safe_call(detect_conflicts_mcp(start_date, end_date), "conflicts"),
        safe_call(check_utilization_threshold_mcp(), "utilization"),
        safe_call(run_contingency_analysis_mcp(["N-1", "N-2"]), "contingency")
    ]

    results = await asyncio.gather(*checks)

    # Phase 3: Aggregate and analyze results
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "date_range": f"{start_date} to {end_date}",
        "checks_run": len(results),
        "checks_passed": sum(1 for r in results if r["success"]),
        "details": {},
        "blocking_issues": [],
        "warnings": [],
        "status": "PASS"
    }

    for result in results:
        check_name = result["check"]
        if result["success"]:
            report["details"][check_name] = result["data"]

            # Check-specific logic
            if check_name == "validation" and not result["data"].get("is_valid"):
                report["blocking_issues"].append("ACGME validation failed")
                report["status"] = "FAIL"

            if check_name == "conflicts" and result["data"].get("conflict_count", 0) > 0:
                report["blocking_issues"].append(
                    f"{result['data']['conflict_count']} conflicts detected"
                )
                report["status"] = "FAIL"

            if check_name == "utilization" and result["data"].get("exceeds_threshold"):
                report["warnings"].append("Utilization exceeds 80% threshold")

        else:
            # Check failed - add to warnings (non-blocking)
            report["warnings"].append(f"{check_name} check failed: {result['error']}")
            report["details"][check_name] = {"error": result["error"]}

    # Phase 4: Generate recommendations
    if report["status"] == "FAIL":
        report["recommendation"] = "DO NOT DEPLOY"
        report["next_steps"] = ["Fix blocking issues", "Re-run safety check"]
    elif report["warnings"]:
        report["recommendation"] = "DEPLOY WITH CAUTION"
        report["next_steps"] = ["Review warnings", "Monitor after deployment"]
    else:
        report["recommendation"] = "SAFE TO DEPLOY"
        report["next_steps"] = ["Proceed with deployment"]

    return report
```

### Example 2: Emergency Coverage with Tiered Strategies

```python
"""Multi-tier emergency coverage orchestration."""

async def handle_emergency_absence(
    absent_faculty_id: str,
    absence_start: date,
    absence_end: date
) -> Dict[str, Any]:
    """
    Handle faculty absence using tiered fallback strategies.

    Strategy Tiers (in order):
    1. Swap-based coverage (least disruptive)
    2. Sacrifice hierarchy (controlled degradation)
    3. Static fallback schedule (pre-approved backup)
    4. Manual escalation (all automation failed)

    Returns:
        Resolution plan with selected strategy
    """
    response = {
        "absent_faculty_id": absent_faculty_id,
        "strategies_attempted": [],
        "selected_strategy": None,
        "execution_steps": []
    }

    # TIER 1: Try swap-based coverage
    print("Tier 1: Attempting swap matching...")
    try:
        # Get affected assignments
        contingency = await run_contingency_analysis_mcp(
            scenario="faculty_absence",
            person_ids=[absent_faculty_id],
            start_date=absence_start,
            end_date=absence_end
        )

        affected = contingency.get("affected_assignments", [])
        swap_success_count = 0

        # Try to find swaps for each affected assignment
        for assignment_id in affected[:10]:  # Limit to first 10
            try:
                candidates = await analyze_swap_candidates_mcp(
                    requester_id=absent_faculty_id,
                    assignment_id=assignment_id
                )

                if candidates.get("candidates"):
                    swap_success_count += 1

            except Exception as e:
                print(f"  Swap analysis failed for {assignment_id}: {e}")

        # If we can cover >= 80% via swaps, use this strategy
        coverage_ratio = swap_success_count / len(affected) if affected else 0
        response["strategies_attempted"].append({
            "tier": 1,
            "strategy": "swap_based",
            "coverage": f"{coverage_ratio:.0%}",
            "viable": coverage_ratio >= 0.8
        })

        if coverage_ratio >= 0.8:
            response["selected_strategy"] = "swap_based_coverage"
            response["execution_steps"] = [
                f"Notify {swap_success_count} potential swap partners",
                "Execute approved swaps",
                "Monitor remaining gaps"
            ]
            return response

    except Exception as e:
        response["strategies_attempted"].append({
            "tier": 1,
            "strategy": "swap_based",
            "error": str(e)
        })

    # TIER 2: Try sacrifice hierarchy
    print("Tier 2: Evaluating sacrifice hierarchy...")
    try:
        sacrifice = await execute_sacrifice_hierarchy_mcp(
            target_level="yellow",
            simulate=True
        )

        has_violations = bool(sacrifice.get("acgme_violations"))
        response["strategies_attempted"].append({
            "tier": 2,
            "strategy": "sacrifice_hierarchy",
            "acgme_compliant": not has_violations,
            "viable": not has_violations
        })

        if not has_violations:
            response["selected_strategy"] = "controlled_degradation"
            response["execution_steps"] = [
                "Activate YELLOW defense level",
                f"Suspend {len(sacrifice.get('suspended_services', []))} services",
                "Notify personnel",
                "Monitor compliance"
            ]
            return response

    except Exception as e:
        response["strategies_attempted"].append({
            "tier": 2,
            "strategy": "sacrifice_hierarchy",
            "error": str(e)
        })

    # TIER 3: Try static fallback
    print("Tier 3: Checking static fallbacks...")
    try:
        fallbacks = await get_static_fallbacks_mcp()

        for fallback in fallbacks.get("fallback_schedules", []):
            if (fallback["start_date"] <= absence_start.isoformat() and
                fallback["end_date"] >= absence_end.isoformat()):

                response["strategies_attempted"].append({
                    "tier": 3,
                    "strategy": "static_fallback",
                    "fallback_name": fallback["name"],
                    "viable": True
                })

                response["selected_strategy"] = "static_fallback"
                response["execution_steps"] = [
                    f"Activate fallback: {fallback['name']}",
                    "Notify all personnel",
                    "Update assignments",
                    "Monitor for 24h"
                ]
                return response

        response["strategies_attempted"].append({
            "tier": 3,
            "strategy": "static_fallback",
            "viable": False,
            "reason": "No suitable fallback found"
        })

    except Exception as e:
        response["strategies_attempted"].append({
            "tier": 3,
            "strategy": "static_fallback",
            "error": str(e)
        })

    # TIER 4: Manual escalation
    print("Tier 4: All automation failed - escalating")
    response["selected_strategy"] = "manual_escalation"
    response["execution_steps"] = [
        "Escalate to Program Director",
        "Provide impact analysis",
        "Request manual coverage assignment"
    ]

    return response
```

---

## Common Failure Modes and Solutions

Real-world orchestration failures and how to handle them.

### Failure Mode 1: MCP Server Unresponsive

**Symptoms:**
- All MCP tool calls timeout
- Connection refused errors
- No response from health check

**Detection:**
```python
async def check_mcp_health() -> bool:
    """Verify MCP server is responsive."""
    try:
        # Simple health check with short timeout
        result = await asyncio.wait_for(
            schedule_status_mcp(),
            timeout=5
        )
        return True
    except asyncio.TimeoutError:
        print("ERROR: MCP server not responding")
        return False
    except Exception as e:
        print(f"ERROR: MCP health check failed: {e}")
        return False
```

**Recovery Steps:**
```bash
# 1. Check container status
docker-compose ps mcp-server

# 2. Check logs for errors
docker-compose logs --tail=50 mcp-server

# 3. Restart container if needed
docker-compose restart mcp-server

# 4. Verify backend connectivity from MCP
docker-compose exec mcp-server curl http://backend:8000/health
```

**Prevention:**
- Implement health checks before orchestration
- Use circuit breaker pattern for repeated failures
- Set reasonable timeouts (30s default, not 5min)

### Failure Mode 2: Partial Results from Parallel Fan-Out

**Symptoms:**
- Some tools succeed, others fail
- Incomplete data for aggregation
- Missing expected fields in results

**Example Scenario:**
```python
# 3 out of 4 checks succeeded - what do we do?
results = await asyncio.gather(*checks, return_exceptions=True)
# [
#   {"data": {...}},           # Success
#   TimeoutError(),             # Failed
#   {"data": {...}},           # Success
#   ConnectionError()           # Failed
# ]
```

**Solution Pattern:**
```python
async def robust_parallel_execution(
    tools: List[tuple[str, Callable]],
    min_success_ratio: float = 0.75
) -> Dict[str, Any]:
    """
    Execute tools in parallel with partial failure tolerance.

    Args:
        tools: List of (name, async_callable) tuples
        min_success_ratio: Minimum fraction that must succeed

    Returns:
        Aggregated results with success indicators

    Raises:
        OrchestraionError: If too many tools fail
    """
    tasks = [tool[1]() for tool in tools]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = []
    failures = []

    for (name, _), result in zip(tools, results):
        if isinstance(result, Exception):
            failures.append({"tool": name, "error": str(result)})
        else:
            successes.append({"tool": name, "data": result})

    success_ratio = len(successes) / len(tools)

    report = {
        "total": len(tools),
        "succeeded": len(successes),
        "failed": len(failures),
        "success_ratio": success_ratio,
        "successes": successes,
        "failures": failures
    }

    if success_ratio < min_success_ratio:
        raise OrchestrationError(
            f"Only {success_ratio:.0%} of tools succeeded "
            f"(minimum: {min_success_ratio:.0%})"
        )

    return report
```

### Failure Mode 3: Tool Output Schema Mismatch

**Symptoms:**
- KeyError when accessing expected fields
- Type errors when processing results
- Unexpected None values

**Example:**
```python
# Expected schema
expected = {"is_valid": bool, "violations": list}

# Actual response (missing field)
actual = {"is_valid": True}  # Where's violations?

# Code crashes
violations = result["violations"]  # KeyError!
```

**Solution Pattern:**
```python
from typing import Optional
from pydantic import BaseModel, Field

class ValidationResult(BaseModel):
    """Expected schema for validation tool."""
    is_valid: bool
    violations: list = Field(default_factory=list)
    timestamp: Optional[str] = None

def safe_extract(raw_result: Dict[str, Any]) -> ValidationResult:
    """
    Safely parse tool output with schema validation.

    Raises:
        ValidationError: If required fields missing or wrong type
    """
    try:
        return ValidationResult(**raw_result)
    except ValidationError as e:
        print(f"WARNING: Tool output schema mismatch: {e}")
        # Return safe default
        return ValidationResult(is_valid=False, violations=["Schema parse error"])
```

### Failure Mode 4: Dependency Chain Breaks Mid-Execution

**Symptoms:**
- Tool B needs output from Tool A, but Tool A failed
- Cascading failures down the dependency chain
- Incomplete state changes

**Example:**
```python
# Sequential dependency: A → B → C
result_a = await tool_a()  # Succeeds
result_b = await tool_b(result_a["value"])  # FAILS - what about C?
result_c = await tool_c(result_b["value"])  # Can't run - result_b doesn't exist
```

**Solution Pattern:**
```python
async def execute_dependency_chain(
    tools: List[tuple[str, Callable]],
    rollback_on_failure: bool = True
) -> Dict[str, Any]:
    """
    Execute tools with dependencies, rolling back on failure.

    Args:
        tools: List of (name, tool_func) in dependency order
        rollback_on_failure: Whether to undo previous steps on failure

    Returns:
        Chain execution report
    """
    results = {}
    executed_tools = []

    for tool_name, tool_func in tools:
        try:
            # Execute with previous results as context
            result = await tool_func(results)
            results[tool_name] = result
            executed_tools.append(tool_name)

        except Exception as e:
            # Chain broken - decide rollback
            report = {
                "status": "FAILED",
                "failed_at": tool_name,
                "completed": executed_tools,
                "error": str(e)
            }

            if rollback_on_failure:
                print(f"Rolling back {len(executed_tools)} completed steps...")
                for completed_tool in reversed(executed_tools):
                    try:
                        # Call rollback if available
                        rollback_func = getattr(
                            tool_func,
                            "rollback",
                            None
                        )
                        if rollback_func:
                            await rollback_func(results[completed_tool])
                    except Exception as rollback_error:
                        print(f"Rollback failed for {completed_tool}: {rollback_error}")

                report["rollback"] = "ATTEMPTED"

            return report

    return {
        "status": "COMPLETED",
        "completed": executed_tools,
        "results": results
    }
```

---

## Integration Examples

How to call MCP tools from different contexts.

### From FastAPI Endpoint

```python
"""MCP orchestration from API route."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import date

router = APIRouter()

@router.post("/schedule/safety-check")
async def api_safety_check(
    start_date: date,
    end_date: date,
    background_tasks: BackgroundTasks
):
    """
    Trigger safety check via API.

    For long-running checks, use background task.
    """
    try:
        # Quick check - run synchronously
        if (end_date - start_date).days <= 7:
            report = await comprehensive_safety_check(start_date, end_date)
            return report

        # Long check - run in background
        else:
            task_id = str(uuid.uuid4())
            background_tasks.add_task(
                run_safety_check_background,
                task_id,
                start_date,
                end_date
            )
            return {
                "task_id": task_id,
                "status": "RUNNING",
                "message": "Check started in background"
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Safety check failed: {str(e)}"
        )
```

### From Celery Task

```python
"""MCP orchestration from Celery background task."""
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def celery_emergency_coverage(
    self,
    absent_faculty_id: str,
    absence_start: str,
    absence_end: str
):
    """
    Handle emergency coverage in background.

    Retries up to 3 times on transient failures.
    """
    try:
        # Celery tasks aren't async - use asyncio.run
        result = asyncio.run(
            handle_emergency_absence(
                absent_faculty_id,
                date.fromisoformat(absence_start),
                date.fromisoformat(absence_end)
            )
        )

        return {
            "status": "COMPLETED",
            "strategy": result["selected_strategy"],
            "execution_plan": result["execution_steps"]
        }

    except Exception as e:
        # Retry on transient errors
        if "timeout" in str(e).lower() or "connection" in str(e).lower():
            self.retry(exc=e, countdown=30)  # Retry after 30s
        else:
            # Permanent error - don't retry
            return {
                "status": "FAILED",
                "error": str(e)
            }
```

### From CLI Script

```python
"""MCP orchestration from command-line script."""
import asyncio
import sys
from datetime import date

async def main():
    """CLI entrypoint for safety check."""
    if len(sys.argv) != 3:
        print("Usage: safety_check.py START_DATE END_DATE")
        print("Example: safety_check.py 2025-01-15 2025-02-14")
        sys.exit(1)

    start = date.fromisoformat(sys.argv[1])
    end = date.fromisoformat(sys.argv[2])

    print(f"Running safety check: {start} to {end}")
    print("-" * 60)

    report = await comprehensive_safety_check(start, end)

    print(f"\nStatus: {report['status']}")
    print(f"Recommendation: {report['recommendation']}")

    if report['blocking_issues']:
        print("\nBlocking Issues:")
        for issue in report['blocking_issues']:
            print(f"  ❌ {issue}")

    if report['warnings']:
        print("\nWarnings:")
        for warning in report['warnings']:
            print(f"  ⚠️  {warning}")

    print("\nNext Steps:")
    for step in report['next_steps']:
        print(f"  • {step}")

    # Exit code based on status
    sys.exit(0 if report['status'] == "PASS" else 1)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Best Practices

1. **Always check tool prerequisites** before execution
2. **Use background tasks** for long-running operations (>30s)
3. **Poll task status** instead of blocking on Celery tasks
4. **Implement timeouts** for all MCP calls (default: 30s)
5. **Log all tool inputs/outputs** for debugging
6. **Cache tool results** when appropriate (compliance summary, static fallbacks)
7. **Parallelize independent tools** to reduce latency
8. **Handle partial failures gracefully** in fan-out patterns

## Troubleshooting

### MCP Server Not Responding
```bash
# Check container status
docker-compose ps mcp-server

# View logs
docker-compose logs -f mcp-server

# Restart server
docker-compose restart mcp-server
```

### Backend API Unreachable from MCP
```bash
# Test connectivity from MCP container
docker-compose exec mcp-server curl -s http://backend:8000/health

# Check network
docker network inspect autonomous-assignment-program-manager_default
```

### Tool Returns Unexpected Result
1. Check tool signature in `Reference/mcp-tool-index.md`
2. Verify input schema matches expected format
3. Check backend API logs: `docker-compose logs backend`
4. Review error patterns in `Reference/tool-error-patterns.md`

## Real-World Scenario: Multi-Skill Integration

Complete end-to-end example showing MCP orchestration integrated with other skills.

### Scenario: Pre-Deployment Safety Validation

**User Request:** "Validate Block 10 schedule before deploying to production"

**Orchestration Flow:**

```
MCP_ORCHESTRATION (this skill)
    ↓
    Invokes: comprehensive_safety_check() using MCP tools
    ↓
    ├─→ constraint-preflight (verify all constraints registered)
    ├─→ schedule-validator (ACGME compliance verification)
    └─→ safe-schedule-generation (ensure backup exists)
    ↓
    If PASS: production-incident-responder (deployment monitoring)
    If FAIL: systematic-debugger (investigate failures)
```

**Implementation:**

```python
async def validate_block_10_deployment():
    """
    Complete pre-deployment validation orchestration.

    Integrates multiple skills and MCP tools.
    """
    print("Step 1: MCP_ORCHESTRATION - Running comprehensive safety check...")

    # Use MCP tools for parallel checks
    safety_report = await comprehensive_safety_check(
        start_date=date(2025, 2, 3),
        end_date=date(2025, 3, 2)
    )

    if safety_report["status"] == "FAIL":
        print("\n❌ Safety check FAILED")
        print("Step 2: Invoking systematic-debugger skill...")

        # Systematic debugging of failures
        for issue in safety_report["blocking_issues"]:
            print(f"  Investigating: {issue}")
            # Debugger skill would explore root causes

        return {
            "deployment_approved": False,
            "reason": "Safety check failed",
            "next_action": "Fix issues identified by systematic-debugger"
        }

    # Additional validation via other skills
    print("\n✓ MCP safety checks passed")
    print("Step 2: Running constraint-preflight...")

    # Ensure all constraints are properly registered
    preflight_ok = await run_constraint_preflight()

    if not preflight_ok:
        return {
            "deployment_approved": False,
            "reason": "Constraint preflight failed",
            "next_action": "Review constraint registration"
        }

    print("Step 3: Running schedule-validator...")

    # Detailed ACGME compliance check
    validation_result = await run_schedule_validator(
        start_date=date(2025, 2, 3),
        end_date=date(2025, 3, 2)
    )

    if not validation_result["acgme_compliant"]:
        return {
            "deployment_approved": False,
            "reason": "ACGME violations detected",
            "violations": validation_result["violations"],
            "next_action": "Fix compliance violations"
        }

    print("Step 4: Ensuring database backup exists...")

    # Safe schedule generation - verify backup
    backup_status = await check_schedule_backup()

    if not backup_status["backup_exists"]:
        print("  Creating backup before deployment...")
        await create_schedule_backup()

    # All checks passed - approve deployment
    print("\n✅ All validation passed - DEPLOYMENT APPROVED")

    return {
        "deployment_approved": True,
        "safety_report": safety_report,
        "acgme_compliant": True,
        "backup_id": backup_status.get("backup_id"),
        "next_action": "Proceed to production deployment"
    }
```

**Output Example:**

```
Step 1: MCP_ORCHESTRATION - Running comprehensive safety check...
  ✓ Schedule validation: PASS
  ✓ Conflict detection: PASS (0 conflicts)
  ✓ Utilization check: PASS (78.3% < 80%)
  ⚠ Contingency analysis: 1 N-1 failure detected

✓ MCP safety checks passed
Step 2: Running constraint-preflight...
  ✓ All 47 constraints registered
  ✓ No orphaned constraints detected

Step 3: Running schedule-validator...
  ✓ 80-hour rule: PASS (all weeks compliant)
  ✓ 1-in-7 rule: PASS (all residents have 1 day off per week)
  ✓ Supervision ratios: PASS

Step 4: Ensuring database backup exists...
  Backup exists: backup_20250202_143022

✅ All validation passed - DEPLOYMENT APPROVED

Next Action: Proceed to production deployment
```

---

## Related Skills

- **constraint-preflight**: Verify constraints before schedule generation (integrates with validation workflow)
- **safe-schedule-generation**: Database backup before write operations (ensures rollback capability)
- **production-incident-responder**: Crisis response using MCP tools (handles deployment failures)
- **systematic-debugger**: Root cause analysis of tool failures (investigates orchestration errors)
- **schedule-validator**: ACGME compliance verification (complements MCP validation tools)
- **acgme-compliance**: Regulatory expertise (validates MCP tool compliance checks)

## Version

- **Created:** 2025-12-26
- **MCP Server Version:** 0.1.0
- **Total Tools:** 36
- **Backend API:** FastAPI 0.109.0

---

*For detailed tool signatures and schemas, see `Reference/mcp-tool-index.md`*
*For error handling procedures, see `Workflows/error-handling.md`*
*For composition patterns, see `Reference/composition-examples.md`*
