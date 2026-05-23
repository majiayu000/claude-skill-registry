---
name: plan-party
description: Parallel strategy generation using G-5 Planning. Deploy 10 planning probes for multi-perspective implementation planning. Use for complex task planning after reconnaissance.
model_tier: opus
parallel_hints:
  can_parallel_with: [search-party]
  must_serialize_with: [SCHEDULING, safe-schedule-generation]
  preferred_batch_size: 10
context_hints:
  max_file_context: 100
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "production|deployment"
    reason: "Production changes require human approval"
  - pattern: "breaking.*change"
    reason: "Breaking changes need careful planning"
  - keyword: ["high-stakes", "compliance", "ACGME"]
    reason: "High-stakes changes require human oversight"
---

# PLAN_PARTY Skill

> **Purpose:** Coordinated parallel planning with 10 strategy probes
> **Created:** 2025-12-31
> **Trigger:** `/plan-party` command
> **Aliases:** `/plan`, `/strategy`, `/pp`
> **Owner:** G5_PLANNING (G-5 Staff)

---

## When to Use

Deploy PLAN_PARTY when you need multi-perspective implementation strategies:

- Complex multi-phase implementations
- High-stakes changes (production, compliance)
- Multiple valid approaches exist
- User asked for a plan before execution
- Task touches 3+ coordinator domains
- Previous similar task had issues
- After SEARCH_PARTY reconnaissance

**Do NOT use for:**
- Simple, obvious tasks (just do it)
- Emergency/time-critical (P0 - no time for planning)
- Already have a clear, validated plan
- Single-domain, single-agent work

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel planners with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
10 probes x 60s each     10 probes x 60s in parallel
Total: 600s              Total: 60s (10x faster)
```

**Implication:** Always spawn all 10 probes. There is no cost savings from running fewer.

---

## The Ten Planning Probes

| Probe | Framing | What It Produces |
|-------|---------|------------------|
| **CRITICAL_PATH** | Time-optimal | Minimum steps, dependency chain, timeline |
| **RISK_MINIMAL** | Safety-first | Conservative approach, rollback plan |
| **PARALLEL_MAX** | Concurrency | Maximum parallel streams, sync points |
| **RESOURCE_MIN** | Lean | Smallest agent count, reuse specialists |
| **QUALITY_GATE** | Test-driven | Verification at each step |
| **INCREMENTAL** | Progressive | Small PRs, feature flags |
| **DOMAIN_EXPERT** | Specialist-led | Route to coordinators |
| **PRECEDENT** | Pattern-matching | Apply proven patterns |
| **ADVERSARIAL** | Red team | Failure modes, edge cases |
| **SYNTHESIS** | Multi-objective | Pareto-optimal balance |

### Probe Details

#### CRITICAL_PATH Probe
**Focus:** What's the fastest route to completion?
- Dependency graph (DAG)
- Minimum steps to completion
- Critical path identification
- Timeline estimate, bottleneck warnings

#### RISK_MINIMAL Probe
**Focus:** How do we minimize blast radius?
- Risk matrix for each step
- Fallback and rollback procedures
- Safety gates, escalation triggers

#### PARALLEL_MAX Probe
**Focus:** Maximum concurrency extraction
- Parallelization opportunities
- Stream assignments (A, B, C...)
- Synchronization points, merge strategy

#### RESOURCE_MIN Probe
**Focus:** Lean execution, minimal overhead
- Minimum agent count
- Specialist reuse plan
- "Do it yourself" vs delegate decision

#### QUALITY_GATE Probe
**Focus:** Test-driven, verification-first
- Test strategy per step
- Acceptance criteria
- Coverage requirements, CI/CD integration

#### INCREMENTAL Probe
**Focus:** Progressive delivery, fast feedback
- Smallest viable increments
- PR strategy (many small vs few large)
- Feature flag strategy

#### DOMAIN_EXPERT Probe
**Focus:** Leverage existing coordinator expertise
- Coordinator assignment matrix
- Domain boundary respect
- Expert agent selection

#### PRECEDENT Probe
**Focus:** Apply proven patterns from history
- Similar past tasks/sessions
- Applicable patterns
- Lessons learned, anti-patterns to avoid

#### ADVERSARIAL Probe
**Focus:** Red team the plan, find weaknesses
- Failure mode analysis
- Edge case inventory
- Stress points, "What kills us?" analysis

#### SYNTHESIS Probe
**Focus:** Balance all concerns, find Pareto frontier
- Multi-objective scoring
- Trade-off analysis
- Balanced recommendation

---

## Invocation

### Full Deployment (10 probes)

```
/plan-party
```

Deploys all 10 planning probes on current intel.

### With Specific Goal

```
/plan-party "Implement batch swap support"
```

Deploys probes with explicit goal framing.

### After SEARCH_PARTY

```
# Recommended workflow
/search-party backend/app/scheduling/
# Review intel brief
/plan-party
```

---

## Decision Tree: SEARCH_PARTY vs PLAN_PARTY

| Scenario | Protocol | Example |
|----------|----------|---------|
| Need codebase intel only | SEARCH_PARTY | "What's the state of resilience?" |
| Have intel, need strategy | PLAN_PARTY | "Plan implementation for discussed issue" |
| Complex task, no context | SEARCH_PARTY then PLAN_PARTY | "Add batch swap support" |
| Simple task | Neither | "Fix typo in README" |

### Decision Rule

```python
def choose_protocol(task: Task) -> str:
    if task.complexity <= 5:
        return "DIRECT_EXECUTION"

    if not task.has_reconnaissance:
        return "SEARCH_PARTY"

    if task.complexity > 10 or task.touches_3_plus_domains:
        return "PLAN_PARTY"

    return "DIRECT_EXECUTION"
```

---

## IDE Crash Prevention (CRITICAL)

**DO NOT** have ORCHESTRATOR spawn 10 planning probes directly. This causes IDE seizure and crashes.

**CORRECT Pattern:**
```
ORCHESTRATOR -> spawns 1 G5_PLANNING (G-5 Commander)
                    |
              G5_PLANNING deploys 10 probes internally
              (manages parallelism, synthesizes results)
```

**WRONG Pattern:**
```
ORCHESTRATOR -> spawns 10 planners directly -> IDE CRASH
```

The G-5 Commander (G5_PLANNING) absorbs the parallelism complexity. ORCHESTRATOR only ever spawns 1 coordinator.

---

## Spawn Pattern via G5_PLANNING Commander

### Via G5_PLANNING Commander (CORRECT)

```python
# ORCHESTRATOR spawns G5_PLANNING who manages the 10 planning probes
Task(
    subagent_type="general-purpose",
    description="G5_PLANNING: PLAN_PARTY Commander",
    prompt="""
## Agent: G5_PLANNING (G-5 Commander)

You are the G-5 Plans Commander for PLAN_PARTY deployment.

## Mission
Deploy 10 planning probes in parallel. Each probe applies a different strategic framing.
Collect all plans and synthesize into unified execution plan.

## Intel Brief
[Insert G2_RECON intel brief here]

## Your Planning Probes to Deploy
1. CRITICAL_PATH - Time-optimal planning
2. RISK_MINIMAL - Safety-first approach
3. PARALLEL_MAX - Maximum concurrency
4. RESOURCE_MIN - Lean execution
5. QUALITY_GATE - Test-driven approach
6. INCREMENTAL - Progressive delivery
7. DOMAIN_EXPERT - Specialist-led routing
8. PRECEDENT - Pattern matching
9. ADVERSARIAL - Red team analysis
10. SYNTHESIS - Multi-objective balance

## Spawn each using Task tool with subagent_type="Explore"

## After all report back:
1. Cross-reference plans
2. Calculate convergence score
3. Identify trade-offs
4. Generate execution plan
5. Report to ORCHESTRATOR
"""
)
```

### Direct Deployment (Only if G5_PLANNING unavailable)

```python
# Deploy all 10 probes in parallel
# WARNING: Only use if spawning from within a coordinator, NOT from ORCHESTRATOR
# Total: 10 probes, wall-clock = single probe timeout

spawn_parallel([
    Task(subagent_type="Explore", description="CRITICAL_PATH",
         prompt="Plan with time-optimal framing: minimum steps, dependencies"),
    Task(subagent_type="Explore", description="RISK_MINIMAL",
         prompt="Plan with safety-first framing: rollback at every step"),
    Task(subagent_type="Explore", description="PARALLEL_MAX",
         prompt="Plan with concurrency framing: maximum parallel streams"),
    Task(subagent_type="Explore", description="RESOURCE_MIN",
         prompt="Plan with lean framing: minimal agents, reuse specialists"),
    Task(subagent_type="Explore", description="QUALITY_GATE",
         prompt="Plan with test-driven framing: verification at each step"),
    Task(subagent_type="Explore", description="INCREMENTAL",
         prompt="Plan with progressive framing: small PRs, feature flags"),
    Task(subagent_type="Explore", description="DOMAIN_EXPERT",
         prompt="Plan with specialist framing: route to domain coordinators"),
    Task(subagent_type="Explore", description="PRECEDENT",
         prompt="Plan with pattern framing: apply proven approaches"),
    Task(subagent_type="Explore", description="ADVERSARIAL",
         prompt="Plan with red team framing: failure modes, edge cases"),
    Task(subagent_type="Explore", description="SYNTHESIS",
         prompt="Plan with balanced framing: Pareto-optimal trade-offs"),
])
```

---

## Plan Synthesis

After all 10 probes report back:

1. **Cross-reference plans** across framings
2. **Calculate convergence score** (N/10 probes agree)
3. **Identify trade-offs** (speed vs safety, parallel vs lean)
4. **Generate execution plan**

### Convergence Analysis

**Key Insight:** Same goal, different strategies. Convergence reveals high-confidence decisions:

| Convergence Type | Signal Meaning |
|-----------------|----------------|
| 10/10 agree on step | High-confidence critical step |
| CRITICAL_PATH vs RISK_MINIMAL disagree | Speed/safety trade-off to surface |
| PARALLEL_MAX and DOMAIN_EXPERT align | Coordinator assignment validated |
| ADVERSARIAL flags unique concern | Hidden risk discovered |
| PRECEDENT matches approach | Pattern is proven |

### Strategy Selection Matrix

| Scenario | User Risk Tolerance | Selection |
|----------|-------------------|-----------|
| High convergence (8+/10) | Any | Execute consensus plan |
| Speed vs Safety split | LOW | RISK_MINIMAL approach |
| Speed vs Safety split | HIGH | CRITICAL_PATH approach |
| Parallelism debate | Time-critical | PARALLEL_MAX approach |
| Parallelism debate | Resource-limited | RESOURCE_MIN approach |

---

## Output Format

### Execution Plan

```markdown
## PLAN_PARTY Execution Plan

### Mission: [What was asked]

### Selected Strategy: [PROBE_NAME] with modifications from [OTHER_PROBES]

### Convergence Score: [N/10 probes agreed on core approach]

### Execution Plan

#### Phase 1: [Name] (Parallel)
| Stream | Owner | Task | Depends On |
|--------|-------|------|------------|
| A | COORD_ENGINE | [task] | - |
| B | COORD_PLATFORM | [task] | - |

#### Phase 2: [Name] (Sequential)
| Step | Owner | Task | Gate |
|------|-------|------|------|
| 1 | [agent] | [task] | [test/review] |
| 2 | [agent] | [task] | [test/review] |

### Risk Mitigations (from ADVERSARIAL)
- [Risk 1]: [Mitigation baked into plan]

### Quality Gates (from QUALITY_GATE)
- [ ] Gate 1: [criteria]

### Rollback Plan (from RISK_MINIMAL)
- Checkpoint 1: [what to save]
- Rollback procedure: [how to undo]

### Trade-offs Accepted
- Chose [X] over [Y] because [rationale]

### Estimated Timeline
- Phase 1: [time]
- Phase 2: [time]
- Total: [time]

### Confidence: [HIGH/MEDIUM/LOW]
```

---

## Integration with SEARCH_PARTY

### Full Intelligence-to-Execution Pipeline

```
User Request
    |
ORCHESTRATOR receives task
    |
G2_RECON deploys SEARCH_PARTY (10 recon probes)
    |--- PERCEPTION, INVESTIGATION, ARCANA
    |--- HISTORY, INSIGHT, RELIGION
    |--- NATURE, MEDICINE, SURVIVAL, STEALTH
    |
G2_RECON synthesizes Intel Brief
    |
G5_PLANNING deploys PLAN_PARTY (10 planning probes)
    |--- CRITICAL_PATH, RISK_MINIMAL, PARALLEL_MAX
    |--- RESOURCE_MIN, QUALITY_GATE, INCREMENTAL
    |--- DOMAIN_EXPERT, PRECEDENT, ADVERSARIAL, SYNTHESIS
    |
G5_PLANNING synthesizes Execution Plan
    |
ORCHESTRATOR reviews, approves, or escalates to user
    |
Parallel Execution
    |
Result Synthesis
    |
User Delivery
```

### Signal Propagation

```
SEARCH_PARTY -> Intel Brief -> PLAN_PARTY -> Execution Plan -> ORCHESTRATOR
     |                            |                              |
(10 recon signals)          (10 plan signals)          (execution signals)
     |                            |                              |
Synthesis                    Synthesis                      Synthesis
(G2_RECON)                 (G5_PLANNING)                  (COORD_AAR)
```

---

## Timeout Profiles

| Profile | Duration | Best For |
|---------|----------|----------|
| **DASH** | 60s | Quick planning, simple tasks |
| **STANDARD** | 90s | Normal planning (default) |
| **DEEP** | 180s | Complex multi-domain planning |

---

## Failure Recovery

### Minimum Viable Plan

Mission can proceed if:
- CRITICAL_PATH (baseline plan) present
- RISK_MINIMAL (safety) present
- ADVERSARIAL (red team) present
- At least 4 of remaining 7 probes

### Circuit Breaker

If > 3 consecutive probe failures: Trip to OPEN state, fall back to single-planner mode.

---

## Protocol Reference

Full protocol documentation: `.claude/protocols/PLAN_PARTY.md`

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `search-party` | Upstream reconnaissance before planning |
| `qa-party` | Downstream validation after execution |
| `startup` | Session initialization |
| `startupO` | ORCHESTRATOR mode initialization |
| `systematic-debugger` | Post-execution debugging if issues |

---

*PLAN_PARTY: Ten strategies, one goal, signal-amplified planning. Convergence is confidence.*
