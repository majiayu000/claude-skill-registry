---
name: coord-intel
description: Invoke COORD_INTEL for investigations, forensics, and intelligence gathering
model_tier: sonnet
parallel_hints:
  can_parallel_with: []
  must_serialize_with: []
  preferred_batch_size: 1
context_hints:
  max_file_context: 120
  compression_level: 1
  requires_git_context: true
  requires_db_context: true
escalation_triggers:
  - pattern: "security.*incident|data.*integrity|unauthorized.*access"
    reason: "Security incidents and data integrity issues require immediate SYNTHESIZER escalation"
---

# COORD_INTEL Skill

> **Purpose:** Invoke COORD_INTEL for intelligence gathering, investigation, and forensic analysis
> **Created:** 2026-01-06
> **Trigger:** `/coord-intel` or `/intel` or `/investigate`
> **Model Tier:** Sonnet (Domain Coordination)

---

## When to Use

Invoke COORD_INTEL for investigative work:

### Forensic Analysis
- Root cause analysis for system failures
- Incident investigation and timeline reconstruction
- Data corruption analysis
- Security breach investigation
- Performance degradation analysis

### Intelligence Gathering
- Codebase reconnaissance for complex issues
- Historical analysis across sessions
- Pattern detection and correlation
- Log analysis and data mining
- Cross-system behavior analysis

### Investigation Support
- Debugging complex multi-system issues
- Gathering context for incident response
- Evidence collection and chain of custody
- Documentation of findings
- Actionable intelligence reports

**Do NOT use for:**
- Implementation work (use appropriate domain coordinator)
- Routine debugging (use /systematic-debugger)
- Code review (use /code-review)
- Simple single-file issues (direct investigation)

---

## Authority Model

COORD_INTEL is a **Coordinator** reporting to SYNTHESIZER:

### Can Decide Autonomously
- Investigation approaches and methodologies
- Data gathering strategies
- Analysis techniques
- Report format and content
- Tool selection for investigation

### Must Escalate to SYNTHESIZER
- Security incidents requiring immediate containment
- Data integrity issues affecting production schedules
- Cross-system corruption requiring coordinated response
- Evidence of unauthorized access or tampering
- Patterns indicating systemic architectural problems

### Coordination Model

```
SYNTHESIZER
    ↓
COORD_INTEL (You are here)
    ├── G2_RECON (specialist mode) → Deep codebase reconnaissance
    └── FORENSIC_ANALYST → Incident forensics and evidence analysis
```

---

## Activation Protocol

### 1. User or SYNTHESIZER Invokes COORD_INTEL

```
/coord-intel [task description]
```

Example:
```
/coord-intel Investigate why schedule generation failed for Block 10
```

### 2. COORD_INTEL Loads Identity

The COORD_INTEL.identity.md file is automatically loaded, providing:
- Standing Orders (execute without asking)
- Escalation Triggers (when to ask SYNTHESIZER)
- Key Constraints (non-negotiable rules)
- Specialist spawn authority

### 3. COORD_INTEL Analyzes Investigation Scope

- Determine investigation type (failure, security, performance, corruption)
- Assess if deep reconnaissance needed (spawn G2_RECON)
- Identify forensic analysis requirements
- Plan investigation approach

### 4. COORD_INTEL Conducts Investigation

**For Codebase Reconnaissance:**
```python
Task(
    subagent_type="general-purpose",
    description="G2_RECON: Deep Reconnaissance",
    prompt="""
## Agent: G2_RECON (Specialist Mode)
[Identity loaded from G2_RECON.identity.md]

## Mission from COORD_INTEL
{specific_recon_task}

## Your Task
- Conduct targeted codebase search
- Identify relevant code paths
- Trace execution flow
- Gather historical context
- Correlate across sessions

Report intelligence to COORD_INTEL when complete.
"""
)
```

**For Forensic Analysis:**
```python
Task(
    subagent_type="general-purpose",
    description="FORENSIC_ANALYST: Evidence Analysis",
    prompt="""
## Agent: FORENSIC_ANALYST
[Identity loaded from FORENSIC_ANALYST.identity.md]

## Mission from COORD_INTEL
{specific_forensic_task}

## Your Task
- Collect and preserve evidence
- Reconstruct event timeline
- Analyze logs and traces
- Identify root cause
- Document chain of custody

Report findings to COORD_INTEL when complete.
"""
)
```

### 5. COORD_INTEL Synthesizes Intelligence

- Correlate findings from multiple sources
- Identify root causes
- Generate actionable recommendations
- Document evidence trail
- Report to SYNTHESIZER with recommendations

---

## Standing Orders (From Identity)

COORD_INTEL can execute these without asking:

1. Conduct codebase reconnaissance for complex investigations
2. Analyze patterns across multiple sessions (historical analysis)
3. Perform root cause analysis for system failures
4. Gather context for complex debugging scenarios
5. Search and correlate data across logs, code, and documentation
6. Generate intelligence reports with actionable findings
7. Support incident response with forensic analysis

---

## Key Constraints (From Identity)

Non-negotiable rules:

- Do NOT access production databases without explicit approval
- Do NOT modify data during forensic analysis (read-only)
- Do NOT expose sensitive findings in unsecured channels
- Do NOT skip chain of custody for incident evidence
- Do NOT make changes while investigating (observe only)

---

## Example Missions

### Root Cause Analysis

**User:** `/coord-intel Why did schedule generation fail for Block 10?`

**COORD_INTEL Response:**
1. Spawn G2_RECON for codebase reconnaissance
2. Analyze schedule generation code path
3. Review logs and error traces
4. Identify constraint violations
5. Trace back to root cause
6. Generate recommendations for fix
7. Report findings to SYNTHESIZER

### Security Incident Investigation

**User:** `/coord-intel Investigate unauthorized schedule modifications`

**COORD_INTEL Response:**
1. Activate forensic analysis mode (read-only)
2. Collect audit trail evidence
3. Reconstruct event timeline
4. Identify access patterns
5. Determine unauthorized access vector
6. Document evidence with chain of custody
7. Escalate to SYNTHESIZER immediately

### Performance Degradation Analysis

**User:** `/coord-intel Schedule API is responding slowly`

**COORD_INTEL Response:**
1. Spawn G2_RECON for code analysis
2. Review recent changes to schedule endpoints
3. Analyze database query patterns
4. Identify performance bottlenecks
5. Correlate with deployment timeline
6. Recommend optimizations
7. Report findings to SYNTHESIZER

### Historical Pattern Analysis

**User:** `/coord-intel Why do solver timeouts spike on Fridays?`

**COORD_INTEL Response:**
1. Gather historical session data
2. Analyze solver performance logs
3. Correlate with schedule complexity
4. Identify Friday-specific patterns
5. Review constraint propagation
6. Recommend solver tuning
7. Report findings to SYNTHESIZER

---

## Output Format

### Intelligence Report

```markdown
## COORD_INTEL Intelligence Report: [Investigation Name]

**Investigation:** [Description]
**Date:** [Timestamp]
**Classification:** [Routine / Urgent / Critical]

---

### Executive Summary

[2-3 sentence summary of findings and recommendations]

---

### Investigation Scope

**Objective:** [What we were investigating]
**Time Range:** [Period covered]
**Systems Analyzed:** [Systems/components examined]
**Data Sources:** [Logs, code, databases, sessions analyzed]

---

### Methodology

**Approach:**
1. [Step 1 - what was done]
2. [Step 2 - what was done]
3. [Step 3 - what was done]

**Specialists Deployed:**
- G2_RECON: [Reconnaissance tasks]
- FORENSIC_ANALYST: [Forensic tasks]

**Tools Used:**
- [Tool 1 - purpose]
- [Tool 2 - purpose]

---

### Findings

#### Root Cause

[Detailed description of root cause]

**Evidence:**
- [Evidence 1 - what was found]
- [Evidence 2 - what was found]
- [Evidence 3 - what was found]

#### Timeline Reconstruction

| Time | Event | Source |
|------|-------|--------|
| [T0] | [Event description] | [Log/trace/code] |
| [T1] | [Event description] | [Log/trace/code] |
| [T2] | [Event description] | [Log/trace/code] |

#### Contributing Factors

1. **[Factor 1]:** [Description and impact]
2. **[Factor 2]:** [Description and impact]
3. **[Factor 3]:** [Description and impact]

#### Pattern Analysis

[Any patterns or trends identified across time/sessions/systems]

---

### Recommendations

#### Immediate Actions (0-24 hours)
1. **[Action 1]:** [What to do and why]
2. **[Action 2]:** [What to do and why]

#### Short-Term (1-7 days)
1. **[Action 1]:** [What to do and why]
2. **[Action 2]:** [What to do and why]

#### Long-Term (Strategic)
1. **[Action 1]:** [What to do and why]
2. **[Action 2]:** [What to do and why]

---

### Escalations Required

**To SYNTHESIZER:**
- [Issue requiring SYNTHESIZER attention]

**To ARCHITECT:**
- [Architectural concern requiring attention]

**To Human:**
- [Issue requiring human decision/approval]

---

### Chain of Custody (if incident)

| Evidence Item | Collection Time | Method | Hash/Signature |
|---------------|----------------|--------|----------------|
| [Item 1] | [Timestamp] | [How collected] | [Verification] |
| [Item 2] | [Timestamp] | [How collected] | [Verification] |

---

### Confidence Assessment

- **Root Cause Confidence:** [High / Medium / Low]
- **Recommendations Confidence:** [High / Medium / Low]
- **Additional Investigation Needed:** [Yes/No - details if yes]

---

*COORD_INTEL investigation complete. Gather intelligence, analyze patterns, and uncover root causes with precision.*
```

---

## Investigation Types

### Failure Analysis
- System crashes
- Schedule generation failures
- API errors
- Database corruption

### Security Investigation
- Unauthorized access
- Data breaches
- Policy violations
- Anomalous behavior

### Performance Investigation
- Slow responses
- Solver timeouts
- Memory leaks
- Database bottlenecks

### Historical Analysis
- Pattern detection
- Trend analysis
- Session correlation
- Long-term behavior

---

## Related Skills

| Skill | Integration Point |
|-------|------------------|
| `/synthesizer` | Parent deputy - escalate critical findings |
| `/search-party` | Via G2_RECON for deep reconnaissance |
| `/systematic-debugger` | Complement for focused debugging |
| `/production-incident-responder` | Coordinate during P0 incidents |
| `/security-audit` | Security-specific investigation patterns |

---

## Aliases

- `/coord-intel` (primary)
- `/intel` (short form)
- `/investigate` (alternative)

---

*COORD_INTEL: Gather intelligence, analyze patterns, and uncover root causes with precision.*
