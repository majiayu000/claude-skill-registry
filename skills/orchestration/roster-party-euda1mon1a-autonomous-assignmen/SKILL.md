---
name: roster-party
description: Parallel team composition analysis using G-1 PERSONNEL. Deploy 6 probes for comprehensive roster assessment before complex task assembly.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [search-party, plan-party]
  must_serialize_with: []
  preferred_batch_size: 6
context_hints:
  max_file_context: 50
  compression_level: 2
  requires_git_context: false
  requires_db_context: false
---

# ROSTER_PARTY Skill

> **Purpose:** Coordinated parallel team composition analysis with 6 specialized probes
> **Created:** 2026-01-06
> **Trigger:** `/roster-party` command
> **Aliases:** `/roster`, `/team`, `/rp`
> **Owner:** G1_PERSONNEL (G-1 Staff)

---

## When to Use

Deploy ROSTER_PARTY when you need comprehensive agent roster intelligence:

- Before complex multi-agent task assembly
- Team composition decisions for large initiatives
- Agent capability assessment for new feature areas
- Post-feature retrospective (which agents worked well together?)
- Identifying specialist gaps before major work
- Pre-planning for search-party or plan-party deployment
- When FORCE_MANAGER needs data-driven team recommendations

**Do NOT use for:**
- Simple single-agent tasks
- When you already know which specialist to use
- Emergency tasks (no time for analysis)
- Routine work with established patterns

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel probes with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
6 probes × 30s each      6 probes × 30s in parallel
Total: 180s              Total: 30s (6x faster)
```

**Implication:** Always spawn all 6 probes. There is no cost savings from running fewer.

---

## The Six Probes

| Probe | Lens | What It Finds |
|-------|------|---------------|
| **CAPABILITY** | Agent inventory | Full roster by domain, what each agent can do |
| **COVERAGE** | Gap analysis | Missing specialists, uncovered domains |
| **UTILIZATION** | Usage patterns | Hot agents (overused), cold agents (underused) |
| **READINESS** | Availability | Agents blocked, in-flight, or ready |
| **SYNERGY** | Team fit | Complementary pairs, conflict risks |
| **PRECEDENT** | Historical | What team compositions worked before |

### Probe Details

#### CAPABILITY Probe
**Focus:** What agents exist and what can they do?
- Read all `.claude/Agents/*.md` specifications
- Build roster matrix: Agent -> Archetype -> Capabilities -> Model Tier
- Domain mapping: Which agents cover which domains?
- Authority levels: Who can decide vs. who must escalate?

#### COVERAGE Probe
**Focus:** Where are the capability gaps?
- Map required domains to agent coverage
- Identify uncovered domains (no agent exists)
- Flag single-agent domains (bus factor = 1 risk)
- Recommend new agent archetypes for gaps

#### UTILIZATION Probe
**Focus:** Which agents are over/under-utilized?
- Parse delegation metrics from recent sessions
- Calculate usage frequency per agent
- Hot agent detection (>80% session appearance → possible gap)
- Cold agent detection (<10% appearance → stale or unnecessary?)

#### READINESS Probe
**Focus:** Which agents are available right now?
- Check agent status (Active/Draft/Deprecated)
- Identify blocked agents (missing dependencies, broken specs)
- Flag agents with recent failures or corrections needed
- Availability matrix for immediate deployment

#### SYNERGY Probe
**Focus:** Which agents work well together?
- Analyze successful multi-agent sessions (from history)
- Identify complementary pairs (e.g., ARCHITECT + IMPLEMENTATION_SPECIALIST)
- Flag known conflict patterns (competing authorities, overlapping domains)
- Team chemistry recommendations

#### PRECEDENT Probe
**Focus:** What team compositions have worked before?
- Search session logs for similar tasks
- Extract successful team compositions
- Identify patterns: "For feature X, use agents A, B, C"
- Anti-patterns: "Don't pair X with Y"

---

## Invocation

### Full Deployment (6 probes)

```
/roster-party
```

Deploys all 6 roster analysis probes.

### Targeted Deployment

```
/roster-party --domain scheduling
```

Focuses probes on specific domain.

### Quick Assessment

```
/roster-party --quick
```

Deploys 3 critical probes (CAPABILITY, COVERAGE, READINESS).

---

## IDE Crash Prevention (CRITICAL)

**DO NOT** have ORCHESTRATOR spawn 6 probes directly. This causes IDE seizure and crashes.

**CORRECT Pattern:**
```
ORCHESTRATOR → spawns 1 G1_PERSONNEL (G-1 Commander)
                    ↓
              G1_PERSONNEL deploys 6 probes internally
              (manages parallelism, synthesizes results)
```

**WRONG Pattern:**
```
ORCHESTRATOR → spawns 6 probes directly → IDE CRASH
```

The G-1 Commander (G1_PERSONNEL) absorbs the parallelism complexity. ORCHESTRATOR only ever spawns 1 coordinator.

---

## Spawn Pattern

### Via G1_PERSONNEL Commander (CORRECT)

```python
# ORCHESTRATOR spawns G1_PERSONNEL who manages the 6 probes
Task(
    subagent_type="general-purpose",
    description="G1_PERSONNEL: ROSTER_PARTY Commander",
    prompt="""
## Agent: G1_PERSONNEL (G-1 Commander)

You are the G1_PERSONNEL agent responsible for ROSTER_PARTY deployment.

## Mission
Deploy 6 roster analysis probes in parallel. Each probe analyzes the agent roster from a different lens.
Collect all reports and synthesize into unified team recommendation.

## Your Probes to Deploy
1. CAPABILITY - Agent inventory and capability mapping
2. COVERAGE - Gap analysis for domain coverage
3. UTILIZATION - Usage patterns and hot/cold agent detection
4. READINESS - Availability and status checks
5. SYNERGY - Team chemistry and complementary pairs
6. PRECEDENT - Historical team composition patterns

## Context to Provide Each Probe
- Agent specs location: /absolute/path/to/.claude/Agents/
- Delegation metrics: /absolute/path/to/.claude/Scratchpad/DELEGATION_METRICS.md
- Session logs: /absolute/path/to/.claude/dontreadme/sessions/ (for PRECEDENT)

## Spawn each using Task tool with subagent_type="Explore"

## After all report back:
1. Cross-reference findings
2. Build team recommendation matrix
3. Flag readiness blockers
4. Generate roster brief with team composition options
5. Report to ORCHESTRATOR
"""
)
```

### Direct Deployment (Only if G1_PERSONNEL unavailable)

```python
# Deploy all 6 probes in parallel
# WARNING: Only use if spawning from within a coordinator, NOT from ORCHESTRATOR
# Total: 6 probes, wall-clock = single probe timeout

spawn_parallel([
    Task(subagent_type="Explore", description="CAPABILITY",
         prompt="Build agent roster matrix: read all .claude/Agents/*.md and map capabilities"),
    Task(subagent_type="Explore", description="COVERAGE",
         prompt="Gap analysis: identify uncovered domains and single-agent risks"),
    Task(subagent_type="Explore", description="UTILIZATION",
         prompt="Usage patterns: parse delegation metrics for hot/cold agents"),
    Task(subagent_type="Explore", description="READINESS",
         prompt="Availability check: agent status, blockers, recent failures"),
    Task(subagent_type="Explore", description="SYNERGY",
         prompt="Team chemistry: analyze successful multi-agent sessions"),
    Task(subagent_type="Explore", description="PRECEDENT",
         prompt="Historical patterns: what team compositions worked for similar tasks"),
])
```

---

## Roster Synthesis

After all 6 probes report back:

1. **Cross-reference findings** across lenses
2. **Build team recommendation matrix**
3. **Flag readiness blockers**
4. **Generate roster brief with options**

### Convergence Analysis

**Key Insight:** Same roster, different lenses. Discrepancies between probes are high-signal:

| Discrepancy Type | Signal Meaning |
|-----------------|----------------|
| CAPABILITY says exists, READINESS says blocked | Agent exists but not deployable |
| COVERAGE flags gap, UTILIZATION shows hot agent | Existing agent overloaded, need specialization |
| SYNERGY recommends pair, PRECEDENT shows conflict | Team worked once but had issues |
| UTILIZATION shows cold agent, COVERAGE shows gap | Agent exists but isn't being used correctly |
| PRECEDENT shows success, READINESS shows unavailable | Need to unblock or find substitute |

---

## Output Format

### Per-Probe Report

```markdown
## ROSTER_PARTY Probe: [PROBE_NAME]

### Key Findings
- [Finding 1 with severity]
- [Finding 2 with severity]

### Agent Highlights
- **[AGENT_NAME]**: [Capability/Status/Pattern]

### Gaps/Blockers Identified
- [What's missing or blocked]

### Recommendations
1. [Immediate action]
2. [Next priority]
```

### Consolidated Team Brief

```markdown
## ROSTER_PARTY Team Brief (6 Probes Deployed)

### Task Context
[What task are we assembling a team for?]

### Roster Overview
| Agent | Domain | Archetype | Status | Utilization | Ready? |
|-------|--------|-----------|--------|-------------|--------|
| ARCHITECT | Design | Critic | Active | High | ✓ |
| QA_TESTER | Quality | Validator | Active | Medium | ✓ |
| IMPLEMENTATION_SPECIALIST | Execution | Generator | Active | Low | ✗ (blocked) |
| ...   | ...    | ...       | ...    | ...         | ...    |

### Team Composition Options

#### Option A: Speed-Optimal (CRITICAL_PATH focus)
| Role | Agent | Why |
|------|-------|-----|
| Lead | [AGENT] | [Justification] |
| Specialist | [AGENT] | [Justification] |

**Pros:** [Advantages]
**Cons:** [Risks]
**Confidence:** HIGH/MEDIUM/LOW

#### Option B: Safety-First (RISK_MINIMAL focus)
| Role | Agent | Why |
|------|-------|-----|
| Lead | [AGENT] | [Justification] |
| Validator | [AGENT] | [Justification] |

**Pros:** [Advantages]
**Cons:** [Risks]
**Confidence:** HIGH/MEDIUM/LOW

#### Option C: Precedent-Based (Historical success)
| Role | Agent | Why |
|------|-------|-----|
| Lead | [AGENT] | Used in [SESSION_XX] successfully |
| Support | [AGENT] | Paired well in past |

**Pros:** Proven pattern
**Cons:** [Any known issues]
**Confidence:** HIGH/MEDIUM/LOW

### Capability Gaps Identified
1. **[GAP]** - [Severity: P1/P2/P3]
   - Impact: [How this affects team assembly]
   - Workaround: [Temporary solution if available]
   - Long-term: [Recommend new agent or capability expansion]

### Readiness Blockers
- **[AGENT]**: [Blocker description and resolution needed]

### Synergy Notes
- **Complementary Pairs:** [AGENT_A + AGENT_B work well together]
- **Avoid Pairing:** [AGENT_X + AGENT_Y have authority conflicts]

### Recommended Team
[Based on all probe data, which option do you recommend?]

**Justification:** [Why this team balances speed, safety, capability, and synergy]

### Confidence Score: [X/6 probes converged]
```

---

## Integration with FORCE_MANAGER

ROSTER_PARTY provides data-driven inputs to FORCE_MANAGER for team assembly decisions.

### Workflow Integration

```
User Request: Complex Task
    |
ORCHESTRATOR recognizes multi-agent need
    |
G1_PERSONNEL deploys ROSTER_PARTY (6 probes)
    |--- CAPABILITY, COVERAGE, UTILIZATION
    |--- READINESS, SYNERGY, PRECEDENT
    |
G1_PERSONNEL synthesizes Team Brief
    |
FORCE_MANAGER reviews options
    |
FORCE_MANAGER selects team composition
    |
ORCHESTRATOR spawns selected agents
    |
Parallel Execution
```

### Signal Flow

```
ROSTER_PARTY → Team Brief → FORCE_MANAGER → Team Selection → ORCHESTRATOR
     |                          |                              |
(6 roster signals)      (composition decision)        (agent spawning)
     |                          |                              |
Synthesis                 Strategic selection           Execution
(G1_PERSONNEL)            (FORCE_MANAGER)             (Coordinators)
```

---

## Decision Tree: When to Use ROSTER_PARTY

| Scenario | Protocol | Example |
|----------|----------|---------|
| Know which agents needed | Skip ROSTER_PARTY | "Use ARCHITECT to review design" |
| Multi-agent, unclear composition | ROSTER_PARTY | "Major refactor across 3 domains" |
| After SEARCH_PARTY, before PLAN_PARTY | ROSTER_PARTY | "Recon done, now who plans?" |
| Gap suspected | ROSTER_PARTY (COVERAGE focus) | "Do we have a frontend specialist?" |
| Team didn't work well last time | ROSTER_PARTY (SYNERGY focus) | "Find better agent pairing" |

### Decision Rule

```python
def choose_roster_party(task: Task) -> bool:
    if task.requires_agents <= 1:
        return False  # Single agent, no team needed

    if task.team_composition_known:
        return False  # Already know the team

    if task.complexity > 15 or task.crosses_3_plus_domains:
        return True  # Complex multi-domain work

    if last_similar_task_had_team_issues:
        return True  # Learn from past composition failures

    return False  # Default: skip if team is obvious
```

---

## Timeout Profiles

| Profile | Duration | Best For |
|---------|----------|----------|
| **QUICK** | 30s | Availability check, simple tasks |
| **STANDARD** | 60s | Normal roster analysis (default) |
| **DEEP** | 120s | Comprehensive gap analysis, precedent search |

---

## Failure Recovery

### Minimum Viable Team Brief

Mission can proceed if:
- CAPABILITY (roster inventory) ✓
- READINESS (who's available) ✓
- At least 2 of remaining 4 probes

### Circuit Breaker

If > 2 consecutive probe failures: Trip to OPEN state, fall back to FORCE_MANAGER manual selection.

---

## Common Patterns

### Pattern 1: Pre-Feature Team Assembly

```
Task: "Implement batch swap feature"

ROSTER_PARTY deployment:
1. CAPABILITY: Need SCHEDULER, IMPLEMENTATION_SPECIALIST, QA_TESTER
2. COVERAGE: Scheduler domain well-covered, batch ops might be gap
3. UTILIZATION: SCHEDULER is hot agent (appears 85% of sessions)
4. READINESS: All 3 agents active and available
5. SYNERGY: SCHEDULER + IMPLEMENTATION_SPECIALIST paired successfully in Session 42
6. PRECEDENT: Similar feature (bulk assign) used same team

Recommendation: SCHEDULER (lead), IMPLEMENTATION_SPECIALIST (execution), QA_TESTER (validation)
Confidence: 6/6 probes converged
```

### Pattern 2: Gap Discovery

```
Task: "Add real-time collaboration feature"

ROSTER_PARTY deployment:
1. CAPABILITY: No WebSocket specialist found
2. COVERAGE: **GAP IDENTIFIED** - Real-time domain uncovered
3. UTILIZATION: N/A (no agent to measure)
4. READINESS: N/A (no agent exists)
5. SYNERGY: Would need to pair with FRONTEND_ENGINEER
6. PRECEDENT: No similar features implemented

Recommendation: Escalate to TOOLSMITH to create REALTIME_SPECIALIST agent
Workaround: FRONTEND_ENGINEER + BACKEND_SPECIALIST can attempt, but high risk
Confidence: 5/6 probes converged on gap
```

### Pattern 3: Overloaded Agent Intervention

```
Task: "Scheduling engine optimization"

ROSTER_PARTY deployment:
1. CAPABILITY: SCHEDULER handles all scheduling concerns
2. COVERAGE: Single agent covers entire scheduling domain (bus factor = 1)
3. UTILIZATION: **HOT AGENT** SCHEDULER appears in 92% of sessions
4. READINESS: SCHEDULER available but showing signs of scope creep
5. SYNERGY: SCHEDULER increasingly paired with OPTIMIZATION_SPECIALIST
6. PRECEDENT: Last 3 optimization tasks used SCHEDULER + OPTIMIZATION_SPECIALIST

Recommendation: Consider splitting SCHEDULER responsibilities
- Create CONSTRAINT_SPECIALIST for constraint logic
- Keep SCHEDULER focused on core engine
- OPTIMIZATION_SPECIALIST for performance tuning
Confidence: 6/6 probes converged on overload pattern
```

---

## Protocol Reference

Full protocol documentation: `.claude/protocols/ROSTER_PARTY.md` (to be created)

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `search-party` | Codebase reconnaissance (can run in parallel with roster-party) |
| `plan-party` | Strategy generation (run after roster-party for team-aware planning) |
| `startup` | Session initialization |
| `startupO` | ORCHESTRATOR mode initialization |
| `hierarchy` | View full agent command structure |

---

## Integration with Search-Party and Plan-Party

### Full Mission Workflow

```
Complex Multi-Domain Task
    |
ORCHESTRATOR spawns (in parallel):
    |--- G2_RECON (SEARCH_PARTY) → Intel Brief
    |--- G1_PERSONNEL (ROSTER_PARTY) → Team Brief
    |
ORCHESTRATOR waits for both
    |
ORCHESTRATOR spawns G5_PLANNING (PLAN_PARTY)
    |-- Context: Intel Brief + Team Brief
    |-- Output: Execution Plan with agent assignments
    |
FORCE_MANAGER reviews plan + team
    |
Team spawned and execution begins
```

**Key Insight:** SEARCH_PARTY and ROSTER_PARTY can run in parallel (independent), then both feed into PLAN_PARTY (sequential dependency).

---

*ROSTER_PARTY: Six lenses on the roster, zero marginal cost. Know your troops before the battle.*
