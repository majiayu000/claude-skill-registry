---
name: production-incident-responder
description: Crisis response skill for production system failures. Integrates with MCP resilience tools to detect, diagnose, and respond to critical system failures. Use when production system shows signs of failure or during emergency situations.
model_tier: opus
parallel_hints:
  can_parallel_with: []
  must_serialize_with: [safe-schedule-generation, SCHEDULING]
  preferred_batch_size: 1
context_hints:
  max_file_context: 100
  compression_level: 0
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "RED|BLACK"
    reason: "Critical/catastrophic defense levels require immediate human intervention"
  - pattern: "circuit.*breaker|trip"
    reason: "Circuit breaker events require human review"
  - pattern: "N-2|multiple.*absence"
    reason: "Multiple simultaneous failures need human decision-making"
  - keyword: ["ACGME violation", "regulatory", "external staffing"]
    reason: "Compliance and staffing changes require human approval"
---

# Production Incident Responder

A crisis response skill that leverages MCP (Model Context Protocol) tools to act on the deployed/working program during critical failures.

## When This Skill Activates

- Production system health check fails
- ACGME compliance violations detected
- Utilization exceeds 80% threshold
- Coverage gaps identified
- Circuit breaker trips
- Defense level escalates to ORANGE or higher

## MCP Integration

This skill connects to the MCP server which provides real-time access to:

### Tier 1: Critical Resilience Tools
| MCP Tool | Purpose | Trigger |
|----------|---------|---------|
| `check_utilization_threshold_tool` | Monitor 80% queuing theory limit | Utilization > 75% |
| `get_defense_level_tool` | Nuclear safety graduated response | Any escalation |
| `run_contingency_analysis_resilience_tool` | N-1/N-2 vulnerability analysis | Faculty absence |
| `get_static_fallbacks_tool` | Pre-computed backup schedules | Critical failure |
| `execute_sacrifice_hierarchy_tool` | Triage-based load shedding | RED/BLACK level |

### Tier 2: Strategic Tools
| MCP Tool | Purpose | Trigger |
|----------|---------|---------|
| `analyze_homeostasis_tool` | Feedback loop health | Sustained stress |
| `calculate_blast_radius_tool` | Failure containment | Zone health warning |
| `analyze_le_chatelier_tool` | Equilibrium shift analysis | Resource strain |

### Tier 3: Advanced Analytics
| MCP Tool | Purpose | Trigger |
|----------|---------|---------|
| `analyze_hub_centrality_tool` | Single point of failure ID | Vulnerability scan |
| `assess_cognitive_load_tool` | Coordinator burnout risk | Decision queue > 7 |
| `check_mtf_compliance_tool` | Military compliance/DRRS | Readiness check |

## Incident Response Protocol

### Level 1: DETECTION (Automated)

```
System Health Check
├── Check utilization via MCP: check_utilization_threshold_tool
├── Get defense level: get_defense_level_tool
├── Run compliance check: check_mtf_compliance_tool
└── Assess cognitive load: assess_cognitive_load_tool

If any metric is YELLOW or worse → Escalate to Level 2
```

### Level 2: DIAGNOSIS (Automated + Human Review)

```
Root Cause Analysis
├── Run contingency analysis: run_contingency_analysis_resilience_tool
│   ├── N-1 analysis (single failure resilience)
│   ├── N-2 analysis (dual failure resilience)
│   └── Cascade simulation
├── Analyze hub centrality: analyze_hub_centrality_tool
│   └── Identify critical personnel
├── Check blast radius: calculate_blast_radius_tool
│   └── Identify affected zones
└── Analyze equilibrium: analyze_le_chatelier_tool
    └── Predict sustainability

Output: Incident Report with Recommendations
```

### Level 3: RESPONSE (Human Approval Required)

```
Response Actions (by severity)

GREEN → No action needed, continue monitoring
YELLOW → Warning: Review recommendations
ORANGE → Critical: Implement mitigations
  ├── Get static fallbacks: get_static_fallbacks_tool
  └── Prepare sacrifice hierarchy (simulate only)
RED → Emergency: Activate crisis protocols
  ├── Execute sacrifice hierarchy: execute_sacrifice_hierarchy_tool
  ├── Activate fallback schedules
  └── Generate SITREP: check_mtf_compliance_tool
BLACK → Catastrophic: Emergency services only
  ├── Execute maximum load shedding
  └── Generate MFR/RFF documentation
```

### Level 4: RECOVERY (Post-Incident)

```
Recovery Actions
├── Monitor homeostasis: analyze_homeostasis_tool
├── Track allostatic load
├── Verify equilibrium restoration
└── Document lessons learned
```

## MCP Server Connection

### Prerequisites

```bash
# Start MCP server
cd mcp-server
pip install -e .
python -m scheduler_mcp.server

# Ensure backend is running
cd backend
uvicorn app.main:app --reload

# Start Celery for async operations
./scripts/start-celery.sh both
```

### MCP Configuration

Add to Claude Desktop or IDE MCP config:

```json
{
  "mcpServers": {
    "residency-scheduler": {
      "command": "python",
      "args": ["-m", "scheduler_mcp.server"],
      "cwd": "/path/to/mcp-server"
    }
  }
}
```

## Crisis Response Workflows

### Workflow 1: Faculty Absence Emergency

```
1. DETECT
   - Receive absence notification
   - Run: check_utilization_threshold_tool

2. DIAGNOSE
   - Run: run_contingency_analysis_resilience_tool(scenario="faculty_absence")
   - Check N-1 resilience: Can we survive this absence?
   - Identify coverage gaps

3. RESPOND (based on impact)
   LOW IMPACT:
   - Use swap marketplace for coverage
   - No escalation needed

   MEDIUM IMPACT:
   - Activate backup pool
   - Run: get_static_fallbacks_tool(scenario="single_absence")
   - Implement fallback schedule

   HIGH IMPACT:
   - Escalate defense level
   - Run: execute_sacrifice_hierarchy_tool(target_level="yellow", simulate_only=true)
   - Review load shedding options
   - REQUIRE HUMAN APPROVAL before execution

4. RECOVER
   - Monitor homeostasis post-incident
   - Verify coverage restored
```

### Workflow 2: Mass Casualty / Deployment Event

```
1. DETECT
   - Multiple absences reported (e.g., military deployment)
   - Run: check_utilization_threshold_tool
   - Expected: ORANGE or RED level

2. DIAGNOSE
   - Run: run_contingency_analysis_resilience_tool(analyze_n1=true, analyze_n2=true)
   - Run: analyze_hub_centrality_tool
   - Identify fatal faculty combinations
   - Calculate cascade risk

3. RESPOND
   - Run: get_static_fallbacks_tool(scenario="deployment")
   - Run: execute_sacrifice_hierarchy_tool(target_level="orange", simulate_only=true)
   - Present options to coordinator:
     a) Implement partial load shedding
     b) Request external locum coverage
     c) Activate cross-training coverage
   - REQUIRE HUMAN APPROVAL

4. COMPLIANCE
   - Run: check_mtf_compliance_tool(generate_sitrep=true)
   - Generate DRRS readiness report
   - Document MFR if circuit breaker trips

5. RECOVER
   - Monitor Le Chatelier equilibrium
   - Track days until exhaustion
   - Plan for resource restoration
```

### Workflow 3: ACGME Compliance Violation

```
1. DETECT
   - Compliance check fails (80-hour, 1-in-7, supervision)
   - Run: validate_schedule via MCP

2. DIAGNOSE
   - Identify specific violations
   - Check affected residents/faculty
   - Calculate severity

3. RESPOND
   SINGLE VIOLATION:
   - Use conflict auto-resolution
   - Run: detect_conflicts(include_auto_resolution=true)
   - Apply suggested fix

   MULTIPLE VIOLATIONS:
   - Run: run_contingency_analysis_resilience_tool
   - May need schedule regeneration
   - ESCALATE to human

4. DOCUMENT
   - Log compliance event
   - Generate audit trail
```

## Escalation Rules

### ALWAYS Escalate to Human When:

1. Defense level reaches RED or BLACK
2. Circuit breaker trips
3. Multiple simultaneous absences (N-2+)
4. ACGME violation cannot be auto-resolved
5. Sacrifice hierarchy execution required (not just simulation)
6. External staffing needed
7. Regulatory documentation required

### Can Handle Automatically:

1. GREEN/YELLOW level monitoring
2. Single swap facilitation
3. Backup pool assignment (if available)
4. Simulation mode analysis
5. Report generation
6. Compliance checking

## Response Time Expectations

| Severity | Detection | Analysis | Response |
|----------|-----------|----------|----------|
| GREEN | Continuous | N/A | N/A |
| YELLOW | < 5 min | < 10 min | < 1 hour |
| ORANGE | < 1 min | < 5 min | < 30 min |
| RED | Immediate | < 2 min | < 15 min |
| BLACK | Immediate | < 1 min | Immediate |

## Integration with Other Skills

### With automated-code-fixer
If crisis response reveals code issues:
1. Document the issue
2. Escalate to automated-code-fixer skill
3. Apply fix through quality gates
4. Re-run health check

### With code-quality-monitor
Post-incident:
1. Run full quality check
2. Ensure no degradation from crisis response
3. Document any technical debt incurred

## Reporting Format

### Quick Status (for monitoring)
```
PRODUCTION STATUS: YELLOW

Utilization: 78% (threshold: 80%)
Defense Level: 2 - CONTROL
Coverage: 94%
Pending Decisions: 5
Active Alerts: 2

Next Action: Monitor, no immediate action required
```

### Incident Report (for escalation)
```markdown
## INCIDENT REPORT

**Severity**: ORANGE
**Time Detected**: 2025-12-20 14:32 UTC
**Status**: ACTIVE - AWAITING HUMAN APPROVAL

### Summary
Two faculty members reported simultaneous absence due to medical emergency.

### Impact Assessment
- Utilization: 85% (above threshold)
- Coverage Gaps: 8 blocks over next 7 days
- ACGME Risk: Supervision ratio violation in 3 blocks
- Cascade Risk: MEDIUM

### MCP Analysis Results
- N-1 Resilience: FAILED
- N-2 Resilience: N/A (already at N-2)
- Hub Centrality: Dr. Smith identified as critical (betweenness: 0.42)

### Recommended Actions
1. Activate static fallback schedule "dual_absence"
2. Request backup pool coverage for PM blocks
3. Consider sacrifice hierarchy level YELLOW (suspend optional education)

### Required Approvals
- [ ] Coordinator approval for fallback activation
- [ ] Medical director review of supervision plan

### Generated Documentation
- SITREP attached
- MFR template prepared (pending circuit breaker status)
```

## References

- `/mcp-server/RESILIENCE_MCP_INTEGRATION.md` - Full MCP resilience integration
- `/mcp-server/src/scheduler_mcp/resilience_integration.py` - Tool implementations
- `/backend/app/resilience/` - Backend resilience framework
- `/docs/architecture/resilience-framework.md` - Architecture overview
