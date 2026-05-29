---
name: sof-party
description: Rapid cross-domain assessment using 18-series SOF Operators. Deploy 7 probes for immediate situational awareness before task force assembly.
model_tier: sonnet
parallel_hints:
  can_parallel_with: []
  must_serialize_with: []
  preferred_batch_size: 7
context_hints:
  max_file_context: 100
  compression_level: 1
  requires_git_context: true
  requires_db_context: true
escalation_triggers:
  - pattern: "mission.*impossible"
    reason: "Mission infeasibility requires strategic pivot"
  - pattern: "critical.*blocker"
    reason: "Critical blockers require immediate escalation"
---

# SOF_PARTY Skill

> **Purpose:** Rapid cross-domain assessment using 18-series Special Operations Forces operators
> **Created:** 2026-01-06
> **Trigger:** `/sof-party` command
> **Aliases:** `/sof`, `/sf`, `/18-series`

---

## When to Use

Deploy SOF_PARTY when you need rapid situational awareness across all domains:

- **After USASOC activation** - Immediate tactical assessment
- **Before task force assembly** - Determine force requirements
- **Time-critical missions** - Rapid assessment under pressure
- **Cross-domain emergencies** - When standard recon too slow
- **Unknown threat environment** - When you need all perspectives fast

**Do NOT use for:**
- Single-domain questions (use domain specialists)
- Routine reconnaissance (use /search-party)
- When you already understand the mission space

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel agents with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
7 probes × 30s each      7 probes × 30s in parallel
Total: 210s              Total: 30s (7x faster)
```

**Implication:** Always spawn all 7 operators. There is no cost savings from running fewer.

---

## The Seven Operators (18-Series)

Each operator provides a unique cross-domain lens on the mission space:

| Operator | MOS | Domain | What They Assess |
|----------|-----|--------|------------------|
| **COMMAND** | 18A | Mission Planning | Mission scope, success criteria, force requirements, timeline feasibility |
| **WEAPONS** | 18B | Offensive Capabilities | Breaking changes needed, destructive operations, rollback risk |
| **ENGINEER** | 18C | Infrastructure | System state, deployment readiness, build health, container status |
| **MEDICAL** | 18D | Compliance/Safety | ACGME impact, regulatory violations, patient safety implications |
| **COMMS** | 18E | Integration | API impacts, data flow, external dependencies, communication channels |
| **INTEL** | 18F | Threat Assessment | Unknowns, recon needs, security implications, hidden dependencies |
| **OPERATIONS** | 18Z | Execution | Timeline feasibility, resource availability, blocking dependencies |

### Operator Complementarity

**Key Insight:** These operators see the SAME mission from different perspectives. Discrepancies = high signal.

| Discrepancy Type | Signal Meaning |
|-----------------|----------------|
| COMMAND says feasible, OPERATIONS says blocked | Missing resources or unrealistic timeline |
| ENGINEER says ready, INTEL says threats detected | Infrastructure healthy but operational risk |
| MEDICAL says compliant, WEAPONS says destructive | Safety conflict with technical requirements |
| COMMS says integrated, INTEL says isolation needed | Security vs. functionality tradeoff |
| COMMAND estimates 2 days, OPERATIONS estimates 2 weeks | Scope underestimated or dependencies unclear |

---

## Invocation

### Standard Deployment (7 operators)

```
/sof-party
```

Deploys all 7 operators for comprehensive assessment.

### Mission-Specific Deployment

```
/sof-party [mission description]
```

Example:
```
/sof-party Implement auto-rollback for ACGME violations within 1 minute
```

### Targeted Assessment (subset of operators)

```
/sof-party --operators 18A,18B,18Z
```

Deploys only COMMAND, WEAPONS, OPERATIONS for quick tactical assessment.

---

## Deployment Pattern

### Via 18A_DETACHMENT_COMMANDER (CORRECT)

```python
# USASOC or ORCHESTRATOR spawns 18A_DETACHMENT_COMMANDER who manages the 7 operators
Task(
    subagent_type="general-purpose",
    description="18A_DETACHMENT_COMMANDER: SOF_PARTY Commander",
    prompt="""
## Agent: 18A_DETACHMENT_COMMANDER

You are the Detachment Commander for SOF_PARTY deployment.

## Mission
{mission_description}

## Your Task
Deploy 7 18-series operators in parallel. Each operator assesses the mission from their domain perspective.
Collect all reports and synthesize into unified OPORD-style briefing.

## Your Operators to Deploy
1. 18A-COMMAND (Mission Planning)
2. 18B-WEAPONS (Offensive Capabilities)
3. 18C-ENGINEER (Infrastructure)
4. 18D-MEDICAL (Compliance/Safety)
5. 18E-COMMS (Integration)
6. 18F-INTEL (Threat Assessment)
7. 18Z-OPERATIONS (Execution)

## Spawn each using Task tool with subagent_type="Explore"

## After all report back:
1. Cross-reference findings
2. Flag discrepancies (high-signal)
3. Assess mission feasibility
4. Recommend task force composition
5. Generate OPORD-style briefing
6. Report to USASOC or ORCHESTRATOR
"""
)
```

### Direct Deployment (Only if 18A unavailable)

```python
# Deploy all 7 operators in parallel
# WARNING: Only use if spawning from within a coordinator, NOT from ORCHESTRATOR
# Total: 7 operators, wall-clock = single operator timeout

spawn_parallel([
    Task(subagent_type="Explore", description="18A-COMMAND",
         prompt=f"Assess mission planning for: {mission}\n\nProvide: scope, success criteria, force requirements, timeline."),

    Task(subagent_type="Explore", description="18B-WEAPONS",
         prompt=f"Assess offensive capabilities needed for: {mission}\n\nProvide: breaking changes, destructive ops, rollback risk."),

    Task(subagent_type="Explore", description="18C-ENGINEER",
         prompt=f"Assess infrastructure readiness for: {mission}\n\nProvide: system state, deployment readiness, build health."),

    Task(subagent_type="Explore", description="18D-MEDICAL",
         prompt=f"Assess compliance/safety for: {mission}\n\nProvide: ACGME impact, regulatory violations, patient safety."),

    Task(subagent_type="Explore", description="18E-COMMS",
         prompt=f"Assess integration requirements for: {mission}\n\nProvide: API impacts, data flow, external dependencies."),

    Task(subagent_type="Explore", description="18F-INTEL",
         prompt=f"Assess threats and unknowns for: {mission}\n\nProvide: security implications, hidden dependencies, recon needs."),

    Task(subagent_type="Explore", description="18Z-OPERATIONS",
         prompt=f"Assess execution feasibility for: {mission}\n\nProvide: timeline, resource availability, blocking dependencies."),
])
```

---

## IDE Crash Prevention (CRITICAL)

**DO NOT** have ORCHESTRATOR spawn 7 operators directly. This can cause IDE instability.

**CORRECT Pattern:**
```
ORCHESTRATOR/USASOC → spawns 1 18A_DETACHMENT_COMMANDER
                           ↓
                      18A deploys 7 operators internally
                      (manages parallelism, synthesizes results)
```

**WRONG Pattern:**
```
ORCHESTRATOR → spawns 7 operators directly → IDE CRASH RISK
```

The 18A Detachment Commander absorbs the parallelism complexity. ORCHESTRATOR only ever spawns 1 commander.

---

## Output Format

### Per-Operator Report

```markdown
## Operator: 18A-COMMAND (Mission Planning)

### Assessment Grade: [A-F]

### Mission Feasibility: [GO / NO-GO / CONDITIONAL]

### Key Findings
- [Finding 1 with severity]
- [Finding 2 with severity]

### Force Requirements
- [Required specialists/coordinators]

### Timeline Estimate
- [Estimated duration with confidence level]

### Blocking Issues
- [Critical blockers if any]

### Risk Assessment
- [Risk level: LOW / MEDIUM / HIGH / CRITICAL]
```

### OPORD-Style Briefing (Consolidated)

```markdown
## SOF_PARTY OPORD: [MISSION NAME]

### SITUATION
**Mission:** [Mission description]
**Assessment Duration:** [Time taken]
**Operators Deployed:** 7 / 7

### INTELLIGENCE (18F)
[Threat assessment, unknowns, security implications]

### MISSION FEASIBILITY: [GO / NO-GO / CONDITIONAL]

### OPERATOR ASSESSMENTS

| Operator | MOS | Feasibility | Key Finding | Risk |
|----------|-----|-------------|-------------|------|
| COMMAND | 18A | GO | 3-day mission, requires 4 specialists | LOW |
| WEAPONS | 18B | CONDITIONAL | Breaking changes to swap engine | MEDIUM |
| ENGINEER | 18C | GO | Infrastructure ready, tests passing | LOW |
| MEDICAL | 18D | GO | No ACGME violations expected | LOW |
| COMMS | 18E | GO | 2 API endpoints affected | LOW |
| INTEL | 18F | CONDITIONAL | Unknown dependency on Redis | MEDIUM |
| OPERATIONS | 18Z | NO-GO | Missing required MCP tools | HIGH |

### CROSS-OPERATOR DISCREPANCIES
[High-signal findings where operators disagreed]

Example:
- **COMMAND vs OPERATIONS**: COMMAND estimates 3 days, OPERATIONS flags 2-week dependency on MCP tool development
- **ENGINEER vs INTEL**: ENGINEER reports infrastructure ready, INTEL identifies Redis version mismatch risk

### RECOMMENDED TASK FORCE COMPOSITION

Based on assessments, recommend deploying:

**Deputy:** [ARCHITECT / SYNTHESIZER / both]

**Coordinators Needed:**
- [COORD_1]: [Why needed]
- [COORD_2]: [Why needed]

**Specialists Required:**
- [SPECIALIST_1]: [Task]
- [SPECIALIST_2]: [Task]

**Estimated Force Size:** [N] agents
**Estimated Duration:** [Timeline]

### BLOCKING ISSUES (IF ANY)

**Critical Blockers:**
1. [Issue 1]
2. [Issue 2]

**Resolution Required Before Mission Start**

### COMMANDER'S RECOMMENDATION

[GO / NO-GO / CONDITIONAL GO]

**Reasoning:** [Why this recommendation]

**Conditional Requirements (if applicable):**
1. [Condition 1]
2. [Condition 2]
```

---

## Mission Flow Integration

### Typical SOF_PARTY Workflow

```
User requests complex mission
    ↓
User invokes /usasoc
    ↓
USASOC activates 18A_DETACHMENT_COMMANDER
    ↓
/sof-party runs (7 operators assess in parallel)
    ↓
OPORD briefing generated
    ↓
USASOC assembles task force based on OPORD
    ↓
Mission executes
```

### Decision Point

After SOF_PARTY assessment:

| Feasibility | Action |
|------------|--------|
| **GO** | Assemble task force, execute immediately |
| **CONDITIONAL GO** | Resolve conditions first, then execute |
| **NO-GO** | Escalate to ORCHESTRATOR for strategic pivot |

---

## Timeout Profiles

| Profile | Duration | Best For |
|---------|----------|----------|
| **RAPID** | 30s | Emergency assessment, P0 incidents |
| **STANDARD** | 60s | Normal SOF assessment (default) |
| **THOROUGH** | 120s | Complex missions with many unknowns |

---

## Failure Recovery

### Minimum Viable Assessment

Mission can proceed if:
- 18A-COMMAND (mission planning) ✓
- 18Z-OPERATIONS (execution feasibility) ✓
- At least 3 of remaining 5 operators

### Circuit Breaker

If > 2 consecutive operator failures: Trip to OPEN state, report to USASOC/ORCHESTRATOR.

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `/usasoc` | Activate before /sof-party for time-critical missions |
| `/search-party` | Deeper reconnaissance after SOF assessment |
| `/qa-party` | Validation after task force execution |
| `/plan-party` | Strategic planning after SOF assessment |
| `systematic-debugger` | When SOF identifies specific issues to debug |

---

## Authority Model

SOF_PARTY operates under **USASOC authority** when activated via /usasoc:
- Can draw specialists from any domain
- Wide lateral authority to investigate
- Reports directly to USASOC or ORCHESTRATOR
- Bypasses normal hierarchy for time-critical assessment

Under normal operations (not USASOC):
- Reports to ORCHESTRATOR
- Follows standard chain of command
- Advisory role only

---

*SOF_PARTY: Seven perspectives, one mission, zero marginal cost. The discrepancies are the signal.*
