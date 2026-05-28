---
name: resilience-dashboard
description: Generate a comprehensive resilience status report using all available MCP tools. Aggregates unified critical index, burnout Rt, early warnings, utilization, and defense levels into a single actionable dashboard.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [schedule-validator, acgme-compliance]
  must_serialize_with: [safe-schedule-generation]
  preferred_batch_size: 8
context_hints:
  max_file_context: 50
  compression_level: 1
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "RED|BLACK"
    reason: "Critical status requires immediate human attention"
  - pattern: "sacrifice.*hierarchy"
    reason: "Sacrifice hierarchy activation requires human approval"
  - keyword: ["emergency", "crisis", "N-2 failure"]
    reason: "Emergency situations require human decision-making"
---

# Resilience Dashboard

> **Purpose:** Generate a comprehensive real-time resilience status report by orchestrating multiple MCP resilience tools in parallel
> **Created:** 2025-12-28
> **Trigger:** `/resilience-dashboard` command

---

## When to Use

- Morning standup to get program health overview
- Before major scheduling decisions (block generation, swaps)
- After emergency events (absence, deployment notification)
- Weekly/monthly resilience health checks
- When program coordinator asks "How healthy is our schedule?"
- Investigating unexplained coverage gaps or faculty stress
- Post-incident retrospective analysis

---

## Required Actions

When this skill is invoked, Claude MUST:

1. **Call MCP tools in parallel** to gather resilience metrics:

   **Parallel Batch 1 - Core Metrics:**
   ```
   - get_unified_critical_index_tool(include_details=True, top_n=5)
   - calculate_burnout_rt_tool(burned_out_provider_ids=[], time_window_days=28)
   - check_utilization_threshold_tool(available_faculty, required_blocks)
   - get_defense_level_tool(coverage_rate)
   ```

   **Parallel Batch 2 - Early Warning:**
   ```
   - detect_burnout_precursors_tool (for any flagged residents)
   - run_spc_analysis_tool (if weekly hours data available)
   - calculate_fire_danger_index_tool (for high-risk residents)
   ```

   **Parallel Batch 3 - Contingency:**
   ```
   - run_contingency_analysis_resilience_tool(analyze_n1=True, analyze_n2=True)
   ```

2. **Determine overall status** using the severity hierarchy:
   - **GREEN**: All metrics healthy, no interventions needed
   - **YELLOW**: Minor concerns, monitoring recommended
   - **ORANGE**: Elevated risk, action recommended within 24 hours
   - **RED**: Critical issues, immediate intervention required
   - **BLACK**: System in crisis mode, emergency protocols active

3. **Aggregate and synthesize** the results into a unified dashboard

4. **Highlight critical issues** requiring immediate attention

5. **Provide trend analysis** if historical data is available

6. **Recommend prioritized actions** based on highest-impact interventions

---

## Output Format

Generate the dashboard in this exact markdown format:

```markdown
# Resilience Dashboard

**Generated:** [ISO timestamp]
**Period:** [date range analyzed]

## Overall Status: [GREEN/YELLOW/ORANGE/RED/BLACK]

[1-2 sentence executive summary]

---

### Critical Index: [0-100]

| Domain | Score | Status |
|--------|-------|--------|
| Contingency (N-1/N-2) | [score] | [status] |
| Epidemiology (Burnout Spread) | [score] | [status] |
| Hub Analysis (Network) | [score] | [status] |

**Top Priority Faculty:**
1. [faculty_id]: [risk pattern] - [recommended intervention]
2. ...

**Contributing Factors:**
- [factor 1]
- [factor 2]

---

### Burnout Epidemic Status

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Rt (Reproduction Number) | [value] | [spreading/controlled/declining] |
| Status | [status] | [description] |
| Intervention Level | [level] | [none/monitoring/moderate/aggressive/emergency] |

**Superspreaders Identified:** [count]
**Herd Immunity Threshold:** [%]

**Interventions:**
- [intervention 1]
- [intervention 2]

---

### Early Warning Signals

| Signal Type | Alerts | Severity |
|-------------|--------|----------|
| Seismic Precursors | [count] | [severity] |
| SPC Violations | [count] | [severity] |
| Fire Danger Index | [avg FWI] | [danger class] |

**Residents Requiring Attention:**
- [resident_id]: [signal type] - [recommended action]

---

### Capacity Status

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Utilization Rate | [%] | 80% | [status] |
| Defense Level | [level] | Prevention | [status] |
| Buffer Remaining | [%] | 20% | [status] |

**Wait Time Multiplier:** [value]x

---

### Contingency Analysis

| Analysis | Pass/Fail | Vulnerabilities |
|----------|-----------|-----------------|
| N-1 (Single Absence) | [pass/fail] | [count] critical |
| N-2 (Dual Absence) | [pass/fail] | [count] fatal pairs |

**Most Critical Faculty:** [list]

**Phase Transition Risk:** [low/medium/high/critical]

---

### Recommended Actions

**Immediate (within 24 hours):**
1. [action with specific target]
2. ...

**Short-term (within 1 week):**
1. [action with specific target]
2. ...

**Long-term (within 1 month):**
1. [action with specific target]
2. ...

---

*Dashboard generated by resilience-dashboard skill*
*Next recommended refresh: [timeframe based on status]*
```

---

## Tool Orchestration Details

### MCP Tools Called

| Tool | Purpose | Required Inputs | Criticality |
|------|---------|-----------------|-------------|
| `get_unified_critical_index_tool` | Multi-factor risk aggregation | None (auto-fetches) | HIGH |
| `calculate_burnout_rt_tool` | Burnout epidemic modeling | `burned_out_provider_ids` | HIGH |
| `detect_burnout_precursors_tool` | Seismic STA/LTA detection | `resident_id`, `signal_type`, `time_series` | MEDIUM |
| `run_spc_analysis_tool` | Western Electric rules | `resident_id`, `weekly_hours` | MEDIUM |
| `calculate_fire_danger_index_tool` | CFFDRS burnout prediction | `resident_id`, metrics | MEDIUM |
| `check_utilization_threshold_tool` | 80% queuing threshold | `available_faculty`, `required_blocks` | HIGH |
| `get_defense_level_tool` | Defense-in-depth status | `coverage_rate` | HIGH |
| `run_contingency_analysis_resilience_tool` | N-1/N-2 vulnerability | Analysis flags | HIGH |

### Parallel Execution Strategy

```
Time ─────────────────────────────────────────────────────►

Phase 1 (Core):
├── get_unified_critical_index_tool ─────────┐
├── calculate_burnout_rt_tool ───────────────┤
├── check_utilization_threshold_tool ────────┤  All parallel
└── get_defense_level_tool ──────────────────┘

Phase 2 (Early Warning) - after Phase 1 if flagged residents:
├── detect_burnout_precursors_tool ──────────┐
├── run_spc_analysis_tool ───────────────────┤  Parallel
└── calculate_fire_danger_index_tool ────────┘

Phase 3 (Contingency) - runs in parallel with Phase 2:
└── run_contingency_analysis_resilience_tool ─┘

Phase 4: Aggregate ──► Format ──► Output
```

### Status Determination Logic

```python
def determine_overall_status(results):
    """
    Determine overall status from aggregated tool results.

    Severity precedence: BLACK > RED > ORANGE > YELLOW > GREEN
    """
    # Any emergency-level result = BLACK
    if any(r.severity == "emergency" for r in results):
        return "BLACK"

    # Any critical-level result = RED
    if any(r.severity == "critical" for r in results):
        return "RED"

    # Any elevated/warning with high impact = ORANGE
    if (results.unified_index.overall_index >= 60 or
        results.burnout_rt.rt >= 1.5 or
        results.utilization.utilization_rate >= 0.85):
        return "ORANGE"

    # Any warning-level result = YELLOW
    if any(r.severity in ["warning", "elevated"] for r in results):
        return "YELLOW"

    return "GREEN"
```

---

## Examples

### Example 1: Healthy Program

**User:** `/resilience-dashboard`

**Output:**
```markdown
# Resilience Dashboard

**Generated:** 2025-12-28T10:30:00Z
**Period:** 2025-12-01 to 2025-12-28

## Overall Status: GREEN

All resilience metrics are within healthy thresholds. No immediate interventions required.

### Critical Index: 28

| Domain | Score | Status |
|--------|-------|--------|
| Contingency (N-1/N-2) | 0.25 | Healthy |
| Epidemiology (Burnout Spread) | 0.20 | Healthy |
| Hub Analysis (Network) | 0.30 | Healthy |

... [rest of dashboard with green metrics]

### Recommended Actions

**Immediate (within 24 hours):**
1. None required

**Short-term (within 1 week):**
1. Continue routine monitoring

*Next recommended refresh: 7 days*
```

### Example 2: Elevated Risk

**User:** `/resilience-dashboard`

**Output:**
```markdown
# Resilience Dashboard

**Generated:** 2025-12-28T10:30:00Z
**Period:** 2025-12-01 to 2025-12-28

## Overall Status: ORANGE

Elevated risk detected in contingency analysis. Two faculty members identified as single points of failure. Recommend cross-training within 24 hours.

### Critical Index: 58

| Domain | Score | Status |
|--------|-------|--------|
| Contingency (N-1/N-2) | 0.72 | CRITICAL |
| Epidemiology (Burnout Spread) | 0.35 | Warning |
| Hub Analysis (Network) | 0.55 | Elevated |

**Top Priority Faculty:**
1. FAC-007: STRUCTURAL_BURNOUT - Immediate workload reduction
2. FAC-012: INFLUENTIAL_HUB - Cross-training priority

... [rest of dashboard]

### Recommended Actions

**Immediate (within 24 hours):**
1. Begin cross-training for FAC-007 backup coverage
2. Review FAC-012 schedule for workload distribution

*Next recommended refresh: 24 hours*
```

### Example 3: Crisis Mode

**User:** `/resilience-dashboard` (during deployment event)

**Output:**
```markdown
# Resilience Dashboard

**Generated:** 2025-12-28T10:30:00Z
**Period:** 2025-12-01 to 2025-12-28

## Overall Status: RED

CRITICAL: Multiple faculty absences due to deployment have triggered N-2 failure state.
Defense level escalated to CONTAINMENT. Sacrifice hierarchy activation recommended.

### Critical Index: 82

... [dashboard with critical metrics]

### Recommended Actions

**Immediate (within 24 hours):**
1. ESCALATE: Request human approval for sacrifice hierarchy activation
2. Activate static fallback schedule "deployment"
3. Contact backup pool for emergency coverage
4. Generate SITREP for program director

*Next recommended refresh: 4 hours*
```

---

## Escalation Rules

**Escalate to human when:**

1. Overall status is RED or BLACK
2. N-2 analysis shows fatal faculty pairs
3. Burnout Rt >= 2.0 (rapid spread)
4. Defense level reaches CONTAINMENT or EMERGENCY
5. Sacrifice hierarchy execution is recommended
6. Multiple universal-critical faculty identified
7. Utilization exceeds 90%

**Can handle automatically:**

1. GREEN/YELLOW status reporting
2. Data aggregation and formatting
3. Trend analysis from historical data
4. Routine monitoring recommendations
5. Identification of at-risk individuals
6. Prioritization of action items

---

## Error Handling

If MCP tools fail, the dashboard should:

1. **Report partial results** with clear indication of missing data
2. **Note which tools failed** and potential impact
3. **Provide fallback recommendations** based on available data
4. **Suggest retry** if transient failures suspected

Example partial output:
```markdown
## Overall Status: YELLOW (Partial Data)

**Warning:** Some metrics unavailable due to tool failures:
- get_unified_critical_index_tool: Timeout (retrying...)
- calculate_burnout_rt_tool: Success
- check_utilization_threshold_tool: Success

Dashboard reflects available data only. Full refresh recommended.
```

---

## Integration with Other Skills

| Related Skill | Integration Point |
|--------------|-------------------|
| `production-incident-responder` | Escalate when status is RED/BLACK |
| `RESILIENCE_SCORING` | Deep-dive into specific metrics |
| `MCP_ORCHESTRATION` | Tool failure recovery |
| `safe-schedule-generation` | Trigger backup before risky operations |
| `acgme-compliance` | Cross-reference compliance violations |

---

## Configuration

Default parameters (can be overridden via args):

```yaml
unified_critical_index:
  include_details: true
  top_n: 5

burnout_rt:
  time_window_days: 28

contingency_analysis:
  analyze_n1: true
  analyze_n2: true
  include_cascade_simulation: false
  critical_faculty_only: true

refresh_intervals:
  green: "7 days"
  yellow: "3 days"
  orange: "24 hours"
  red: "4 hours"
  black: "1 hour"
```

---

## Validation Checklist

Before completing resilience dashboard generation, verify:

- [ ] **All Core Tools Responded:** Unified critical index, burnout Rt, utilization, and defense level all returned data
- [ ] **Status Determination:** Overall status (GREEN/YELLOW/ORANGE/RED/BLACK) accurately reflects worst metric severity
- [ ] **Top Priority Faculty Identified:** Critical index includes top N faculty with specific risk patterns
- [ ] **Actionable Recommendations:** Immediate/short-term/long-term actions are specific (not generic)
- [ ] **Escalation Rules Applied:** RED/BLACK status triggers appropriate human escalation warnings
- [ ] **Partial Failure Handling:** If MCP tools failed, dashboard clearly indicates missing data and limitations
- [ ] **Trend Context Included:** If historical data available, trends are shown (improving/worsening)
- [ ] **Next Refresh Interval:** Recommended refresh time matches status severity (GREEN=7d, RED=4h)
- [ ] **Quality Gate:** Dashboard provides enough context for a program coordinator to make decisions

## Version

- **Created:** 2025-12-28
- **MCP Tools Required:** 8 resilience tools
- **Estimated Execution Time:** 5-15 seconds (parallel execution)

---

*This skill provides a single-pane-of-glass view into program resilience, enabling proactive intervention before issues become crises.*
