---
name: ops-party
description: Parallel operational readiness validation using G-3 OPERATIONS. Deploy 6 probes to validate workflow readiness before execution.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [roster-party, context-party]
  must_serialize_with: [SCHEDULING]
  preferred_batch_size: 6
context_hints:
  max_file_context: 50
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "blocking.*dependency"
    reason: "Critical path blocked - workflow cannot proceed"
  - pattern: "resource.*unavailable"
    reason: "Essential resources missing - escalate for provisioning"
---

# OPS_PARTY Skill

> **Purpose:** Operational readiness validation before multi-step workflow execution
> **Created:** 2026-01-06
> **Trigger:** `/ops-party` command
> **Aliases:** `/ops`, `/workflow`, `/op`

---

## When to Use

Deploy OPS_PARTY before executing complex multi-step workflows:

- Pre-flight check before schedule generation
- Validation before database migrations
- Readiness assessment before deployment
- Dependency chain verification
- Resource availability confirmation
- Critical path analysis for complex tasks

**Do NOT use for:**
- Simple single-step operations
- Already-running workflows (use for planning only)
- Post-execution validation (use QA_PARTY instead)
- Pure code exploration (use SEARCH_PARTY instead)

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel agents with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
6 probes × 30s each      6 probes × 30s in parallel
Total: 180s              Total: 30s (6x faster)
```

**Implication:** Always run all 6 probes. There is no time savings from running fewer.

**Why This Matters:** Operational validation is free when parallelized. The marginal cost of comprehensive readiness checks is zero.

---

## The Six Probes

Each probe validates a different operational dimension in parallel:

| Probe | Lens | What It Finds |
|-------|------|---------------|
| **WORKFLOW** | Step validation | Each step's preconditions, sequence correctness, logical flow |
| **RESOURCES** | Availability | Compute resources, agent availability, time budget status, capacity |
| **DEPENDENCIES** | Blocking chains | What must complete first, critical path, sequential constraints |
| **BOTTLENECKS** | Choke points | Single points of failure, resource contention, capacity limits |
| **PARALLEL** | Concurrency | What can run simultaneously, sync points, parallelization opportunities |
| **HEALTH** | System status | Stack health, container state, service availability, baseline readiness |

### Probe Details

#### WORKFLOW
- Validates logical sequence of operations
- Checks preconditions for each step
- Identifies missing prerequisites
- Verifies success criteria are measurable

#### RESOURCES
- Checks computational resources (CPU, memory, disk)
- Validates agent/worker availability
- Assesses time budget constraints
- Confirms required tools/services accessible

#### DEPENDENCIES
- Maps dependency graph
- Identifies critical path (longest sequential chain)
- Flags circular dependencies
- Validates external service dependencies

#### BOTTLENECKS
- Identifies single points of failure
- Detects resource contention (shared resources)
- Finds capacity constraints
- Highlights serialization forced by architecture

#### PARALLEL
- Identifies parallelizable operations
- Finds synchronization points
- Calculates maximum parallelism factor
- Estimates wall-clock time savings

#### HEALTH
- Checks system health (containers, services)
- Validates database connectivity
- Confirms git repository state
- Verifies baseline environment readiness

---

## Deployment Pattern

### Standard Deployment: 6 Probes in Parallel

Deploy all 6 operational probes simultaneously using G3_OPERATIONS:

```python
# G3_OPERATIONS deploys 6 probes in parallel
# Total: 6 probes, wall-clock = single probe timeout

spawn_parallel([
    Task(subagent_type="Analyze", description="OPS-WORKFLOW",
         prompt="Validate workflow step sequence and preconditions"),
    Task(subagent_type="Analyze", description="OPS-RESOURCES",
         prompt="Check resource availability and capacity"),
    Task(subagent_type="Analyze", description="OPS-DEPENDENCIES",
         prompt="Map dependency chains and critical path"),
    Task(subagent_type="Analyze", description="OPS-BOTTLENECKS",
         prompt="Identify bottlenecks and single points of failure"),
    Task(subagent_type="Analyze", description="OPS-PARALLEL",
         prompt="Identify parallelization opportunities and sync points"),
    Task(subagent_type="Analyze", description="OPS-HEALTH",
         prompt="Validate system health and baseline readiness"),
])
```

---

## Invocation

### Full Deployment (6 probes)

```
/ops-party
```

Deploys all 6 operational validation probes.

### Targeted Workflow

```
/ops-party generate_schedule_block_10
```

Validates readiness for specific workflow.

### Quick Check (critical only)

```
/ops-party --quick
```

Deploys 3 critical probes (WORKFLOW, DEPENDENCIES, HEALTH).

---

## Spawn Pattern

### Via G3_OPERATIONS (RECOMMENDED)

```python
# ORCHESTRATOR spawns G3_OPERATIONS who manages the 6 probes
Task(
    subagent_type="general-purpose",
    description="G3_OPERATIONS: OPS_PARTY Commander",
    prompt="""
## Agent: G3_OPERATIONS (G-3 Operations Commander)

You are the G-3 Operations Officer validating workflow readiness.

## Mission
Deploy 6 operational validation probes in parallel.
Collect all reports and synthesize into GO/NO-GO recommendation.

## Your 6 Probes to Deploy
1. OPS-WORKFLOW (sequence validation)
2. OPS-RESOURCES (availability check)
3. OPS-DEPENDENCIES (critical path analysis)
4. OPS-BOTTLENECKS (failure point detection)
5. OPS-PARALLEL (concurrency analysis)
6. OPS-HEALTH (system status)

## Spawn each using Task tool with subagent_type="Analyze"

## After all report back:
1. Cross-reference findings
2. Identify blocking issues (NO-GO conditions)
3. Calculate estimated execution time
4. Generate GO/NO-GO recommendation with rationale
5. Report to ORCHESTRATOR

## GO Criteria (all must pass):
- WORKFLOW: All steps have satisfied preconditions
- RESOURCES: Sufficient capacity available
- DEPENDENCIES: No circular deps, critical path identified
- BOTTLENECKS: No single points of failure OR mitigation in place
- PARALLEL: Parallelization plan exists (if applicable)
- HEALTH: All required services operational

## NO-GO Conditions (any fails mission):
- Missing critical dependencies
- Insufficient resources
- Circular dependency detected
- Critical service down
- Workflow preconditions not met
"""
)
```

### Direct Deployment (fallback)

```python
# Only use if G3_OPERATIONS unavailable
# Deploy all 6 probes in parallel from coordinator
spawn_parallel([
    Task(subagent_type="Analyze", description="OPS-WORKFLOW",
         prompt="""Validate workflow steps for: [WORKFLOW_NAME]

         Check:
         1. Each step has clear preconditions
         2. Sequence is logical (outputs feed inputs)
         3. Success criteria are measurable
         4. Rollback plan exists for failures

         Report: READY/BLOCKED with specific issues"""),

    Task(subagent_type="Analyze", description="OPS-RESOURCES",
         prompt="""Check resource availability for: [WORKFLOW_NAME]

         Check:
         1. Compute: CPU/memory/disk availability
         2. Agents: Worker capacity, queue depth
         3. Time: Budget vs estimated duration
         4. Services: Required tools/APIs accessible

         Report: SUFFICIENT/INSUFFICIENT with gaps"""),

    Task(subagent_type="Analyze", description="OPS-DEPENDENCIES",
         prompt="""Map dependencies for: [WORKFLOW_NAME]

         Check:
         1. Build dependency graph
         2. Identify critical path (longest chain)
         3. Detect circular dependencies
         4. Validate external service dependencies

         Report: CLEAR/BLOCKED with critical path"""),

    Task(subagent_type="Analyze", description="OPS-BOTTLENECKS",
         prompt="""Identify bottlenecks in: [WORKFLOW_NAME]

         Check:
         1. Single points of failure
         2. Resource contention (shared resources)
         3. Capacity constraints
         4. Forced serialization

         Report: RESILIENT/FRAGILE with mitigations"""),

    Task(subagent_type="Analyze", description="OPS-PARALLEL",
         prompt="""Analyze parallelization for: [WORKFLOW_NAME]

         Check:
         1. Identify parallelizable steps
         2. Find synchronization points
         3. Calculate max parallelism factor
         4. Estimate wall-clock vs total time

         Report: Parallel plan with time savings"""),

    Task(subagent_type="Analyze", description="OPS-HEALTH",
         prompt="""Validate system health for: [WORKFLOW_NAME]

         Check:
         1. Container status (docker ps)
         2. Database connectivity
         3. Git repository state (uncommitted changes?)
         4. Service availability (API endpoints)

         Report: HEALTHY/DEGRADED with issues"""),
])
```

---

## Operational Synthesis

After all 6 probes report back, G3_OPERATIONS synthesizes findings:

### GO/NO-GO Decision Matrix

| Condition | Impact | GO/NO-GO |
|-----------|--------|----------|
| All probes GREEN | Proceed | **GO** |
| WORKFLOW/DEPENDENCIES RED | Cannot execute | **NO-GO** |
| RESOURCES/HEALTH YELLOW | Degraded performance | **GO** (with warnings) |
| BOTTLENECKS RED + no mitigation | High failure risk | **NO-GO** |
| PARALLEL optimization available | Faster execution | **GO** (with plan) |

### Critical Path Analysis

```
Example Output:
Critical Path: 8 steps, 240s estimated
  Step 1: Validate input (30s) → ready
  Step 2: Load data (60s) → blocked (DB connection YELLOW)
  Step 3: Process (90s) → ready
  Step 4: Validate output (30s) → ready
  Step 5: Commit (30s) → ready

Parallel Opportunities:
  Steps 3.1, 3.2, 3.3 can run in parallel (90s → 30s, save 60s)

Recommendation: NO-GO (resolve DB connection issue first)
```

---

## Output Format

### Per-Probe Report

```markdown
## Probe: [PROBE_NAME]

### Status: [GREEN/YELLOW/RED]

### Findings
- [Finding 1 with severity]
- [Finding 2 with severity]

### Blocking Issues
- [Any NO-GO conditions]

### Recommendations
- [Specific actions to resolve issues]
```

### Operational Readiness Report

```markdown
## OPS_PARTY Operational Readiness Report

**Workflow:** [WORKFLOW_NAME]
**Assessment Time:** [TIMESTAMP]
**Decision:** [GO / NO-GO / GO WITH WARNINGS]

### Summary

| Probe | Status | Issues | Blocking |
|-------|--------|--------|----------|
| WORKFLOW | GREEN | 0 | No |
| RESOURCES | YELLOW | 2 | No |
| DEPENDENCIES | GREEN | 0 | No |
| BOTTLENECKS | YELLOW | 1 | No |
| PARALLEL | GREEN | 0 | No |
| HEALTH | GREEN | 0 | No |

### Critical Path
- **Total Steps:** 8
- **Estimated Duration:** 240s (sequential) / 120s (optimized)
- **Longest Chain:** Step 1 → 2 → 3 → 4 (210s)

### Blocking Issues
None

### Warnings
- RESOURCES: High memory usage (78%) - may impact performance
- BOTTLENECKS: Database connection is single point of failure

### Parallelization Plan
- Steps 3.1, 3.2, 3.3 can run in parallel (save 60s)
- Steps 5 and 6 are independent (save 30s)
- Total optimization: 240s → 120s (50% reduction)

### GO/NO-GO Recommendation

**Decision: GO WITH WARNINGS**

**Rationale:**
- All critical preconditions satisfied
- No blocking dependencies
- Sufficient resources (with monitoring)
- Parallelization plan reduces execution time 50%

**Conditions:**
1. Monitor memory usage during execution
2. Implement DB connection retry logic
3. Execute parallel steps per plan

**Estimated Execution Time:** 120s (with parallelization)

### Risk Mitigation
- Database SPOF: Implement connection pooling + retry logic
- Memory pressure: Monitor and throttle if exceeds 85%
```

---

## Timeout Profiles

| Profile | Duration | Best For |
|---------|----------|----------|
| **QUICK** | 30s | Fast sanity check, 3 critical probes |
| **STANDARD** | 60s | Normal operational validation (default) |
| **THOROUGH** | 120s | Complex workflows, high-risk operations |

---

## Integration with Workflow Execution

### Pre-Execution Pattern

```
1. User requests workflow execution
2. ORCHESTRATOR spawns G3_OPERATIONS
3. G3_OPERATIONS deploys OPS_PARTY (6 probes)
4. Probes report back (parallel, 60s total)
5. G3_OPERATIONS synthesizes GO/NO-GO
6. If GO: Proceed with workflow
7. If NO-GO: Report blockers to user
8. If GO WITH WARNINGS: Proceed with monitoring
```

### Workflow Optimization

OPS_PARTY not only validates readiness but also optimizes execution:

- **PARALLEL probe** identifies parallelization opportunities
- **BOTTLENECKS probe** suggests mitigations
- **DEPENDENCIES probe** provides critical path for sequencing

**Result:** Faster, safer workflow execution with clear time estimates.

---

## Failure Recovery

### Minimum Viable Validation

Mission can proceed with reduced validation if:
- WORKFLOW (sequence validation) ✓
- DEPENDENCIES (critical path) ✓
- HEALTH (system status) ✓

### Circuit Breaker

If > 2 consecutive probe failures: Trip to OPEN state, abort validation.

**Fallback:** Manual validation required before proceeding.

---

## Example Use Cases

### Schedule Generation

```
/ops-party generate_block_10_schedule

Output:
- WORKFLOW: 12 steps validated, preconditions met
- RESOURCES: Solver capacity OK, 8 cores available
- DEPENDENCIES: ACGME rules loaded, resident data ready
- BOTTLENECKS: Database is SPOF (mitigation: connection pool)
- PARALLEL: Steps 4-7 can parallelize (save 120s)
- HEALTH: All services GREEN

Decision: GO
Estimated Time: 180s (down from 300s with parallelization)
```

### Database Migration

```
/ops-party alembic_upgrade_head

Output:
- WORKFLOW: Migration path validated (3 pending migrations)
- RESOURCES: Database backup complete, disk space OK
- DEPENDENCIES: No blocking schema locks detected
- BOTTLENECKS: Migration #2 will lock table (60s downtime)
- PARALLEL: Migrations must run sequentially
- HEALTH: Database GREEN, backup verified

Decision: GO WITH WARNINGS
Downtime Window: 60s during migration #2
```

### Deployment

```
/ops-party deploy_to_production

Output:
- WORKFLOW: Build → Test → Deploy sequence validated
- RESOURCES: CI/CD queue empty, runner available
- DEPENDENCIES: All external services reachable
- BOTTLENECKS: Blue/green deployment mitigates downtime
- PARALLEL: Tests can run in parallel (save 5min)
- HEALTH: All containers GREEN, no active incidents

Decision: GO
Estimated Time: 8min (down from 13min)
```

---

## Protocol Reference

Full protocol documentation: `.claude/protocols/OPS_PARTY.md`

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `search-party` | Codebase reconnaissance before planning |
| `qa-party` | Post-execution validation and testing |
| `plan-party` | Strategy generation after validation |
| `systematic-debugger` | When NO-GO issues need debugging |

---

## Integration with G-3 OPERATIONS

OPS_PARTY is the primary tool of G3_OPERATIONS (Operations Officer).

**G-3 Responsibilities:**
- Operational planning
- Resource allocation
- Workflow optimization
- Risk assessment
- Execution readiness

**OPS_PARTY provides:**
- Systematic readiness validation
- Quantified risk assessment
- Time-optimized execution plans
- GO/NO-GO recommendations with rationale

**Chain of Command:**
```
ORCHESTRATOR
    ↓
G3_OPERATIONS (Operations Officer)
    ↓
OPS_PARTY (6 parallel probes)
```

---

*OPS_PARTY: Six lenses, one mission, zero marginal cost. Readiness is not optional.*
