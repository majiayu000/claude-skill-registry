---
name: signal-party
description: Parallel metrics collection using G-6 SIGNAL. Deploy 6 probes to gather metrics from all sources for data-driven decisions.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [search-party, ops-party]
  must_serialize_with: []
  preferred_batch_size: 6
context_hints:
  max_file_context: 50
  compression_level: 2
  requires_git_context: true
  requires_db_context: true
escalation_triggers:
  - pattern: "critical.*threshold"
    reason: "Critical threshold breaches need immediate attention"
  - pattern: "defense.*level.*(RED|BLACK)"
    reason: "Emergency defense levels require escalation"
  - keyword: ["anomaly", "violation"]
    reason: "Significant anomalies or violations require review"
---

# SIGNAL_PARTY Skill

> **Purpose:** Coordinated parallel metrics collection with 6 specialized probes
> **Created:** 2026-01-06
> **Trigger:** `/signal-party` command
> **Aliases:** `/signal`, `/metrics`, `/sp6`
> **Owner:** G6_SIGNAL (G-6 Staff)

---

## When to Use

Deploy SIGNAL_PARTY when you need comprehensive metrics intelligence:

- Performance analysis for schedules or system health
- Data-driven decision support for strategic planning
- Resilience framework health assessment
- Trend analysis and anomaly detection
- Pre-deployment validation metrics
- Evidence collection for compliance reviews
- System health monitoring and diagnostics

**Do NOT use for:**
- Simple single-metric queries (use direct MCP tool calls)
- When only one lens is needed
- Interpreting data (SIGNAL collects, doesn't recommend)

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel agents with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
6 probes × 60s each      6 probes × 60s in parallel
Total: 360s              Total: 60s (6x faster)
```

**Implication:** Always spawn all probes. There is no cost savings from running fewer.

---

## The Six Probes

Deploy 6 SIGNAL probes in parallel, each gathering metrics from a different domain:

| Probe | Lens | What It Finds |
|-------|------|---------------|
| **SCHEDULING** | Solver metrics | Generation time, constraint violations, coverage gaps, fairness scores |
| **RESILIENCE** | Health scores | Utilization thresholds, N-1/N-2 status, defense levels, circuit breaker state |
| **COMPLIANCE** | ACGME status | 80-hour violations, 1-in-7 violations, near-misses, compliance trends |
| **PERFORMANCE** | System health | API response times, error rates, resource usage, throughput metrics |
| **AGENTS** | Execution metrics | Success rates, latencies, spawn counts, token usage, timeout incidents |
| **TRENDS** | Time series | Week-over-week changes, anomalies, patterns, seasonal variations |

### Probe Details

#### SCHEDULING Probe
**Focus:** Scheduling engine performance and quality
- Solver execution time (median, p95, p99)
- Constraint violation counts by type
- Coverage gaps and unassigned shifts
- Schedule fairness scores (variance, equity)
- Swap success/failure rates
- Recent schedule generation attempts

#### RESILIENCE Probe
**Focus:** Resilience framework health indicators
- Current defense level (GREEN/YELLOW/ORANGE/RED/BLACK)
- Utilization percentage vs. 80% threshold
- N-1 contingency status (can lose 1 resident?)
- N-2 contingency status (can lose 2 residents?)
- Circuit breaker states (CLOSED/OPEN/HALF_OPEN)
- Unified Critical Index score
- Recovery distance metrics

#### COMPLIANCE Probe
**Focus:** ACGME compliance monitoring
- 80-hour rule violations (current, trend)
- 1-in-7 day off violations
- Supervision ratio violations
- Compliance percentage by rule type
- Near-miss events (within 5% of limit)
- Compliance trend (improving/stable/degrading)

#### PERFORMANCE Probe
**Focus:** System performance and resource usage
- API endpoint response times (p50, p95, p99)
- Error rate percentage by endpoint
- Database query performance
- Cache hit rates
- Memory and CPU utilization
- Request throughput (req/sec)

#### AGENTS Probe
**Focus:** Agent execution performance
- Agent success rate by archetype
- Average execution time by agent type
- Token usage per agent (min/avg/max)
- Timeout incident count
- Spawn latency metrics
- Agent health status

#### TRENDS Probe
**Focus:** Temporal patterns and anomalies
- Week-over-week metric changes
- Month-over-month comparisons
- Identified anomalies (>3σ from baseline)
- Seasonal patterns detected
- Emerging trends (improving/degrading)
- Correlation analysis across metrics

---

## Deployment Pattern

### Standard Deployment: 6 SIGNAL Probes

Deploy 6 SIGNAL probes in parallel:

| SIGNAL Probe | Target Domain | MCP Tools Used |
|-------------|---------------|----------------|
| SIGNAL-SCHEDULING | Scheduling performance | `generate_schedule`, `validate_schedule`, `detect_conflicts` |
| SIGNAL-RESILIENCE | Resilience health | `check_utilization_threshold`, `analyze_n1_contingency`, `get_defense_level` |
| SIGNAL-COMPLIANCE | ACGME compliance | `validate_schedule` (ACGME rules), compliance audit tools |
| SIGNAL-PERFORMANCE | System metrics | API health checks, database performance queries |
| SIGNAL-AGENTS | Agent performance | Agent execution logs, session metrics |
| SIGNAL-TRENDS | Time series | Historical data analysis, baseline comparisons |

---

## Invocation

### Full Deployment (6 probes)

```
/signal-party
```

Deploys all 6 SIGNAL probes in parallel.

### Targeted Deployment (specific domain)

```
/signal-party resilience
/signal-party scheduling
/signal-party compliance
```

Deploys single probe for specific domain.

### Quick Metrics (3 critical probes)

```
/signal-party --quick
```

Deploys 3 critical probes (SCHEDULING, RESILIENCE, COMPLIANCE).

---

## IDE Crash Prevention (CRITICAL)

**DO NOT** have ORCHESTRATOR spawn 6 SIGNAL probes directly. This causes IDE seizure and crashes.

**CORRECT Pattern:**
```
ORCHESTRATOR → spawns 1 G6_SIGNAL (G-6 Commander)
                    ↓
              G6_SIGNAL deploys 6 probes internally
              (manages parallelism, synthesizes results)
```

**WRONG Pattern:**
```
ORCHESTRATOR → spawns 6 SIGNAL probes directly → IDE CRASH
```

The G-6 Commander (G6_SIGNAL) absorbs the parallelism complexity. ORCHESTRATOR only ever spawns 1 coordinator.

---

## Spawn Pattern

### Via G6_SIGNAL Commander (CORRECT)

```python
# ORCHESTRATOR spawns G6_SIGNAL who manages the 6 SIGNAL probes
Task(
    subagent_type="general-purpose",
    description="G6_SIGNAL: SIGNAL_PARTY Commander",
    prompt="""
## Agent: G6_SIGNAL (G-6 Commander)

You are the G-6 Signal Commander for SIGNAL_PARTY deployment.

## Mission
Deploy 6 SIGNAL probes in parallel. Each probe collects metrics from a different domain.
Collect all reports and synthesize into unified metrics dashboard.

## Your SIGNAL Probes to Deploy
1. SIGNAL-SCHEDULING
2. SIGNAL-RESILIENCE
3. SIGNAL-COMPLIANCE
4. SIGNAL-PERFORMANCE
5. SIGNAL-AGENTS
6. SIGNAL-TRENDS

## Spawn each using Task tool with subagent_type="Explore"

## After all report back:
1. Cross-reference metrics
2. Flag anomalies and trends
3. Generate consolidated dashboard
4. Report to ORCHESTRATOR
"""
)
```

### Direct Deployment (Only if G6_SIGNAL unavailable)

```python
# Deploy all 6 SIGNAL probes in parallel
# WARNING: Only use if spawning from within a coordinator, NOT from ORCHESTRATOR
# Total: 6 probes, wall-clock = single probe timeout

spawn_parallel([
    Task(subagent_type="Explore", description="SIGNAL-SCHEDULING",
         prompt="Collect scheduling metrics: solver time, violations, coverage, fairness"),
    Task(subagent_type="Explore", description="SIGNAL-RESILIENCE",
         prompt="Collect resilience metrics: defense level, utilization, N-1/N-2, circuit breakers"),
    Task(subagent_type="Explore", description="SIGNAL-COMPLIANCE",
         prompt="Collect ACGME compliance metrics: 80-hour violations, 1-in-7 status, trends"),
    Task(subagent_type="Explore", description="SIGNAL-PERFORMANCE",
         prompt="Collect system performance: response times, error rates, resource usage"),
    Task(subagent_type="Explore", description="SIGNAL-AGENTS",
         prompt="Collect agent metrics: success rates, execution time, token usage"),
    Task(subagent_type="Explore", description="SIGNAL-TRENDS",
         prompt="Analyze trends: week-over-week, anomalies, patterns, correlations"),
])
```

---

## Metrics Synthesis

After all 6 SIGNAL probes report back:

1. **Cross-reference metrics** across domains
2. **Flag anomalies** (metrics >3σ from baseline)
3. **Identify trends** (improving/stable/degrading)
4. **Detect correlations** (e.g., utilization → defense level)
5. **Generate consolidated dashboard**

### Cross-Domain Analysis

**Key Insight:** Same timeframe, different lenses. Correlations between domains are high-signal:

| Correlation Type | Signal Meaning |
|-----------------|----------------|
| SCHEDULING slow, RESILIENCE degrading | Solver struggling with tight constraints |
| COMPLIANCE violations up, UTILIZATION high | Approaching 80% threshold causing violations |
| PERFORMANCE slow, AGENTS timing out | System resource contention affecting agents |
| TRENDS anomaly, RESILIENCE defense level change | System responded to emerging pattern |
| SCHEDULING violations, COMPLIANCE clean | Validation gap or recent fix deployed |

---

## Output Format

### Per-Probe Report

```markdown
## SIGNAL Probe: [DOMAIN]

### Status: [GREEN/YELLOW/RED]

### Key Metrics
- [Metric 1]: [value] [trend arrow]
- [Metric 2]: [value] [vs. baseline]

### Anomalies Detected
- [Metric] at [value] (expected [baseline range])

### Trend Analysis
- [Metric] [improving/degrading] at [rate]

### Data Quality
- Sources: [list]
- Confidence: [%]
```

### Consolidated Dashboard

```markdown
## SIGNAL_PARTY Metrics Dashboard (6 Probes Deployed)

| Domain | Status | Key Metric | Trend | Priority Findings |
|--------|--------|------------|-------|-------------------|
| Scheduling | GREEN | Solver: 2.3s avg | Stable | 3 coverage gaps |
| Resilience | YELLOW | Utilization: 76% | Up 4% | Approaching threshold |
| Compliance | GREEN | 100% compliant | Stable | 0 violations |
| Performance | GREEN | API: 120ms p95 | Down 10% | Improved cache hit |
| Agents | GREEN | 96% success | Stable | 2 timeout incidents |
| Trends | YELLOW | Utilization rising | Linear | Projected breach in 2 weeks |

### Cross-Domain Correlations
[High-signal findings where metrics across domains correlate]

### Anomalies Flagged
[Metrics >3σ from baseline with context]

### Trending Issues
[What's improving or degrading with projections]

### Recommended Actions
1. [Highest priority based on data]
2. [Next priority]

### Data Quality
- Time range: [range]
- Sources: [N sources queried]
- Confidence: [%]
```

---

## MCP Tool Integration

SIGNAL_PARTY uses MCP tools for data collection:

### Scheduling Metrics
- `generate_schedule` - Trigger test generation for timing
- `validate_schedule` - Check constraint violations
- `detect_conflicts` - Identify coverage gaps
- `analyze_swap_candidates` - Swap feasibility metrics

### Resilience Metrics
- `check_utilization_threshold_tool` - Utilization percentage
- `analyze_n1_contingency_tool` - N-1 coverage status
- `analyze_n2_contingency_tool` - N-2 coverage status
- `get_unified_critical_index_tool` - Overall risk score
- `check_defense_level_tool` - Current defense level
- `get_circuit_breaker_state_tool` - Circuit breaker status
- `calculate_burnout_rt_tool` - Burnout reproduction rate

### Compliance Metrics
- `validate_schedule` (ACGME mode) - Rule violations
- Audit trail queries - Historical compliance

### Performance Metrics
- System logs - API response times, error rates
- Database queries - Query performance, connection pool
- Resource monitoring - CPU, memory, disk usage

### Agent Metrics
- Session files - Agent execution records
- Execution traces - Success/failure, timing, tokens

### Trend Analysis
- Historical data - Baseline comparisons
- Statistical analysis - Anomaly detection, correlation

---

## Timeout Profiles

| Profile | Duration | Best For |
|---------|----------|----------|
| **DASH** | 45s | Quick triage, status check |
| **STANDARD** | 90s | Normal metrics collection (default) |
| **DEEP** | 180s | Comprehensive analysis, trend correlation |

---

## Failure Recovery

### Minimum Viable Metrics

Mission can proceed if:
- SCHEDULING (baseline performance) ✓
- RESILIENCE (system health) ✓
- COMPLIANCE (regulatory status) ✓
- At least 1 of remaining 3 probes

### Circuit Breaker

If > 2 consecutive probe failures: Trip to OPEN state, fall back to direct MCP tool calls.

---

## Integration with Other Protocols

### With SEARCH_PARTY (G-2 Recon)

```
SEARCH_PARTY discovers code/architecture
    ↓
SIGNAL_PARTY collects performance data
    ↓
Combined intel informs decisions
```

### With PLAN_PARTY (G-5 Planning)

```
SIGNAL_PARTY provides baseline metrics
    ↓
PLAN_PARTY uses data for strategy
    ↓
Post-execution: SIGNAL_PARTY validates results
```

### With QA_PARTY (IG Validation)

```
QA_PARTY runs tests
    ↓
SIGNAL_PARTY collects test metrics
    ↓
AGENTS probe tracks test performance
```

---

## Command Structure

### Oversight Hierarchy

Metrics collection falls under **G-6 SIGNAL** function:

```
ORCHESTRATOR (you)
    └── G6_SIGNAL (G-6 Commander - Signal/Data Processing)
            ├── SIGNAL-SCHEDULING (6 metrics collectors)
            ├── SIGNAL-RESILIENCE (6 metrics collectors)
            ├── SIGNAL-COMPLIANCE (6 metrics collectors)
            ├── SIGNAL-PERFORMANCE (6 metrics collectors)
            ├── SIGNAL-AGENTS (6 metrics collectors)
            └── SIGNAL-TRENDS (6 metrics collectors)
                    = 36 parallel metrics collectors
```

**Staff Distinction:**
- **G-2 (SEARCH_PARTY)**: Intelligence/Reconnaissance - explores code and architecture
- **G-6 (SIGNAL_PARTY)**: Signal Corps - collects metrics and performance data
- **G-5 (PLAN_PARTY)**: Plans - uses intel and metrics for strategy

---

## Escalation Rules

| Situation | Escalate To | Reason |
|-----------|-------------|--------|
| Critical threshold breach | ORCHESTRATOR | Immediate action required |
| Defense level RED or BLACK | ORCHESTRATOR + COORD_RESILIENCE | Emergency response |
| Compliance violations | SYNTHESIZER + COMPLIANCE_AUDITOR | Regulatory implications |
| Anomaly pattern detected | SYNTHESIZER | Interpretation needed |
| Data interpretation needed | Domain expert | G-6 collects, doesn't interpret |
| Trend requires investigation | DEVCOM_RESEARCH | Advanced analysis |

---

## Success Criteria

**Successful Metrics Collection:**
- Data accuracy: >95% validation pass rate
- Completeness: >90% of expected sources covered
- Timeliness: Dashboard generated within timeout
- Clarity: Metrics presented with context and trends
- Provenance: All data sources documented

**Successful Pattern Detection:**
- Sensitivity: Identifies anomalies at >2σ level
- Specificity: False positive rate <5%
- Actionability: Flagged issues include context
- Cross-domain: Correlations identified

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `search-party` | Code/architecture reconnaissance (G-2 function) |
| `plan-party` | Strategic planning using metrics (G-5 function) |
| `qa-party` | Validation and testing (IG function) |
| `resilience-dashboard` | Interactive resilience-specific dashboard |
| `schedule-validator` | Deep schedule validation |
| `systematic-debugger` | When metrics reveal issues to debug |

---

## Protocol Reference

Full protocol documentation: `.claude/Agents/G6_SIGNAL.md`

Related documentation:
- `.claude/dontreadme/reconnaissance/OVERNIGHT_BURN/SESSION_8_MCP/mcp-tools-resilience.md`
- `.claude/dontreadme/reconnaissance/OVERNIGHT_BURN/SESSION_8_MCP/mcp-tools-analytics.md`
- `docs/architecture/cross-disciplinary-resilience.md`

---

*SIGNAL_PARTY: Six lenses, one timeframe, data-driven decisions. The correlations are the signal.*
