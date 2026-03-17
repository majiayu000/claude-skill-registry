# PRD Audit Skill (Agent-Based)

## Metadata
- skill_name: prd-audit
- activation_code: PRD_AUDIT_V1
- version: 2.0.0
- category: validation
- phase: 4

## Description

Agent-based PRD audit orchestrator. Spawns specialized audit agents to evaluate PRD quality across 90 dimensions using LLM reasoning. Each agent applies expert judgment to its audit category, returning structured findings.

## Activation Criteria

- Triggered after Phase 3 PRD Validation completes
- When user says "audit PRD", "run audit", "quality gate", or "phase 4"
- When `PHASE3_COMPLETE` signal is detected
- Before Phase 5 Task Decomposition

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRD AUDIT ORCHESTRATOR                       │
│                      (This Skill)                               │
├─────────────────────────────────────────────────────────────────┤
│  1. Profile Selection (negotiate with user)                     │
│  2. Spawn Audit Agents (parallel where possible)                │
│  3. Collect Findings                                            │
│  4. Apply Gate Logic                                            │
│  5. Emit Phase Signal                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Audit Agent 1 │   │ Audit Agent 2 │   │ Audit Agent N │
│ (Category I)  │   │ (Category II) │   │ (Category XX) │
│               │   │               │   │               │
│ Reads PRD     │   │ Reads PRD     │   │ Reads PRD     │
│ Applies       │   │ Applies       │   │ Applies       │
│ Checklist     │   │ Checklist     │   │ Checklist     │
│ Returns JSON  │   │ Returns JSON  │   │ Returns JSON  │
└───────────────┘   └───────────────┘   └───────────────┘
```

## Audit Profiles

| Profile | Categories | Audits | Use Case |
|---------|------------|--------|----------|
| `quick` | I, II (partial) | ~10 | Fast iteration, PR reviews |
| `security` | V (all) | 7 | Security-focused gate |
| `production` | II, V, VII, VIII | ~25 | Pre-deployment readiness |
| `full` | All 20 | 90 | Comprehensive release gate |
| `custom` | User-selected | Varies | Targeted review |

## Workflow

### Step 1: Profile Selection

Present options to user:

```
Phase 2: PRD Audit

Select audit profile:
  1. Quick (~10 audits) - Structure and core requirements
  2. Security (7 audits) - Authentication, authorization, data protection
  3. Production (~25 audits) - Deployment readiness
  4. Full (90 audits) - Comprehensive quality gate
  5. Custom - Select specific categories

Or specify categories: "audit categories II, V, VII"
```

### Step 2: Spawn Audit Agents

For each selected category, spawn an audit agent using the Task tool:

```markdown
**Agent Task: Category II - Requirements Quality Audit**

You are a requirements quality auditor. Analyze the PRD for requirements quality issues.

**PRD to audit:** [Read the PRD file]

**Reference:** Consult .claude/docs/PRD-AUDIT-FRAMEWORK.md for Category II audits (4-10)

**Your task:**
1. Read the entire PRD carefully
2. For each audit in Category II (audits 4-10), evaluate the PRD against the checklist
3. Use your judgment - these are not simple pattern matches
4. Return findings in the specified JSON format

**Audits to perform:**
- Audit 4: EARS Syntax Compliance - Are requirements properly structured?
- Audit 5: RFC 2119 Keywords - Are SHALL/SHOULD/MAY used correctly?
- Audit 6: Testability - Can each requirement be objectively verified?
- Audit 7: Ambiguity Detection - Are there vague terms that need clarification?
- Audit 8: Completeness - Are there gaps in coverage?
- Audit 9: Atomicity - Are requirements single-purpose?
- Audit 10: Traceability - Do IDs link properly?

**Return JSON:**
{
  "category": "II",
  "category_name": "Requirements Quality",
  "audits_performed": [4, 5, 6, 7, 8, 9, 10],
  "findings": [
    {
      "audit_id": 4,
      "audit_name": "EARS Syntax Compliance",
      "status": "failed|passed|partial",
      "severity": "critical|high|medium|low",
      "issues": [
        {
          "location": "Section 4.2, FR-003",
          "problem": "Requirement uses passive voice hiding responsibility",
          "current": "Data will be validated",
          "suggested": "WHEN data is submitted, the system SHALL validate against schema X"
        }
      ],
      "passed_items": ["All FRs have unique IDs", "Trigger conditions are specific"],
      "recommendations": ["Rewrite 3 requirements using EARS event-driven pattern"]
    }
  ],
  "summary": {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 1
  }
}
```

### Step 3: Parallel Execution Strategy

Launch agents in parallel where they don't have dependencies:

**Parallel Group 1 (Single-PRD audits):**
- Category I: Document Structure (audits 1-3)
- Category II: Requirements Quality (audits 4-10)
- Category IX: Test Coverage (audits 47-54)
- Category X: Documentation Quality (audits 55-59)

**Parallel Group 2 (Technical audits):**
- Category V: Security (audits 23-29)
- Category VI: Performance/Scalability (audits 30-35)
- Category VII: Reliability/Resilience (audits 36-40)
- Category VIII: Operational Readiness (audits 41-46)

**Sequential (Cross-PRD audits - need other PRDs):**
- Category III: Technical Architecture (audits 11-16)
- Category IV: Cross-PRD Consistency (audits 17-22)
- Category XI: Gap Analysis (audits 60-63)
- Category XVII: Interoperability (audits 81-83)

### Step 4: Collect and Aggregate Findings

After all agents complete, aggregate findings:

```json
{
  "audit_report": {
    "prd_file": "docs/PRD.md",
    "profile": "production",
    "timestamp": "2025-12-11T12:00:00Z",
    "categories_audited": ["I", "II", "V", "VII", "VIII"],
    "summary": {
      "total_audits": 25,
      "passed": 18,
      "failed": 7,
      "critical": 2,
      "high": 3,
      "medium": 2,
      "low": 0
    },
    "findings_by_severity": {
      "critical": [
        {"audit": 23, "issue": "No authentication mechanism specified"},
        {"audit": 36, "issue": "No availability SLA defined"}
      ],
      "high": [
        {"audit": 4, "issue": "3 requirements missing EARS syntax"},
        {"audit": 25, "issue": "Encryption at rest not specified for PII"},
        {"audit": 47, "issue": "No acceptance criteria for 5 requirements"}
      ],
      "medium": [...]
    },
    "gate_status": "BLOCKED"
  }
}
```

### Step 5: Gate Decision

Apply gate logic:

```
CRITICAL findings: MUST be resolved before proceeding
HIGH findings: SHOULD be resolved, or user must acknowledge
MEDIUM findings: MAY be deferred with justification
LOW findings: Tracked for future improvement

Gate Logic:
  IF critical > 0:
    STATUS = BLOCKED
    MESSAGE = "Resolve {n} critical findings to proceed"
  ELSE IF high > 0:
    STATUS = REQUIRES_ACKNOWLEDGMENT
    MESSAGE = "Acknowledge {n} high findings to proceed"
  ELSE:
    STATUS = PASSED
    MESSAGE = "Audit passed. Proceeding to Phase 3."
```

### Step 6: User Interaction

Present findings and await decision:

```
╔══════════════════════════════════════════════════════════════╗
║                    PHASE 4: PRD AUDIT COMPLETE               ║
╠══════════════════════════════════════════════════════════════╣
║  Profile: production (25 audits)                             ║
║  Passed: 18 | Failed: 7                                      ║
╠══════════════════════════════════════════════════════════════╣
║  CRITICAL (2) - Must resolve:                                ║
║    • [Audit 23] No authentication mechanism specified        ║
║    • [Audit 36] No availability SLA defined                  ║
║                                                              ║
║  HIGH (3) - Acknowledge to proceed:                          ║
║    • [Audit 4] 3 requirements missing EARS syntax            ║
║    • [Audit 25] Encryption at rest not specified for PII     ║
║    • [Audit 47] No acceptance criteria for 5 requirements    ║
╠══════════════════════════════════════════════════════════════╣
║  STATUS: BLOCKED                                             ║
║                                                              ║
║  Options:                                                    ║
║    • Fix critical issues and re-run: "re-audit"              ║
║    • View full report: "show audit report"                   ║
║    • View specific finding: "show audit 23"                  ║
╚══════════════════════════════════════════════════════════════╝
```

## Agent Prompts by Category

### Category I: Document Structure Agent

```
You are auditing PRD document structure. Evaluate:

Audit 1 - Template Compliance:
- Are all required sections present?
- Is metadata complete (version, date, author)?
- Are headers properly nested?

Audit 2 - Cross-Reference Integrity:
- Do internal references (Section X, Figure Y) exist?
- Do PRD references (PRD-XXX) point to real documents?
- Are requirement IDs (FR-XXX) consistent?

Audit 3 - Version Control:
- Is there a change history?
- Does versioning follow semver?
- Are changes meaningfully described?

Apply judgment. A missing optional section is low severity.
A broken reference to a critical dependency is high severity.
```

### Category II: Requirements Quality Agent

```
You are a requirements engineer auditing requirement quality. Evaluate:

Audit 4 - EARS Syntax: Do requirements follow WHEN/WHILE/WHERE patterns?
Audit 5 - RFC 2119: Are SHALL/SHOULD/MAY used correctly and consistently?
Audit 6 - Testability: Can each requirement be objectively verified?
Audit 7 - Ambiguity: Are there vague terms (fast, secure, user-friendly)?
Audit 8 - Completeness: Are there obvious gaps in functionality?
Audit 9 - Atomicity: Are requirements single-purpose or compound?
Audit 10 - Traceability: Do IDs exist and link properly?

Be thorough but fair. Flag real issues, not style preferences.
A requirement like "the system shall be secure" is CRITICAL - it's untestable.
A minor formatting inconsistency is LOW.
```

### Category V: Security Agent

```
You are a security architect auditing security requirements. Evaluate:

Audit 23 - Authentication: Is authn specified? What methods? MFA?
Audit 24 - Authorization: Is authz specified? RBAC? Least privilege?
Audit 25 - Data Protection: Encryption at rest? In transit? Key management?
Audit 26 - Input Validation: SQL injection? XSS? Command injection?
Audit 27 - Logging/Monitoring: Security events logged? Tamper-proof?
Audit 28 - Secrets Management: How are credentials stored? Rotated?
Audit 29 - Supply Chain: Dependencies vetted? SBOM? Vulnerability scanning?

Missing authentication for a user-facing system is CRITICAL.
Missing MFA for an internal tool might be MEDIUM.
Use your security expertise to calibrate severity.
```

### Category VII: Reliability Agent

```
You are an SRE auditing reliability requirements. Evaluate:

Audit 36 - Fault Tolerance: How does the system handle failures?
Audit 37 - FMEA: Are failure modes identified with mitigations?
Audit 38 - Recovery: RTO/RPO defined? Backup strategy?
Audit 39 - Graceful Degradation: What happens under partial failure?
Audit 40 - Chaos Engineering: Is resilience testing planned?

A production system with no availability target is CRITICAL.
Missing chaos testing for an internal tool is LOW.
```

## Cross-PRD Audits

For cross-PRD audits (Categories III, IV, XI, XVII), the agent needs access to related PRDs:

```
You are auditing cross-PRD consistency. You have access to:
- Primary PRD: docs/PRD-025.md (the one being audited)
- Related PRDs: docs/PRD-001.md, docs/PRD-005.md, docs/PRD-020.md

Audit 11 - Interface Contracts:
- Do IMPORTS in PRD-025 have matching EXPORTS in other PRDs?
- Are interface names and types consistent?

Audit 17-22 - Naming Consistency:
- Are similar concepts named the same way across PRDs?
- Are there conflicting definitions?
```

## Output Files

After audit completion:

1. **Audit Report**: `.claude/audit-report.json` - Full findings
2. **Signal File**: `.claude/.signals/audit-complete.json` or `audit-blocked.json`
3. **Workflow State**: Update `.claude/.workflow-state.json` with Phase 2 status

## Phase Transition

```
IF gate_status == "PASSED":
    WRITE ".claude/.signals/phase4-complete.json"
    UPDATE workflow_state.phase4.status = "complete"
    EMIT "Phase 4 complete. Proceeding to Phase 5: Task Decomposition."

ELSE IF gate_status == "REQUIRES_ACKNOWLEDGMENT":
    PROMPT user for acknowledgment
    IF acknowledged:
        WRITE ".claude/.signals/phase4-complete.json" with acknowledged_items
        PROCEED to Phase 5

ELSE:  # BLOCKED
    WRITE ".claude/.signals/phase4-blocked.json"
    UPDATE workflow_state.phase4.status = "blocked"
    PROMPT user to fix critical issues
```

## Resumability

If audit is interrupted, state is saved:

```json
{
  "audit_state": {
    "profile": "full",
    "started": "2025-12-11T12:00:00Z",
    "completed_categories": ["I", "II"],
    "in_progress_categories": ["V"],
    "pending_categories": ["VII", "VIII", "IX"],
    "findings_so_far": [...]
  }
}
```

Resume with: "resume audit" or "continue phase 4"

## Integration with Audit Framework

The full audit framework is available at:
- `.claude/docs/PRD-AUDIT-FRAMEWORK.md` (90 audits, 20 categories)

Agents should reference this document for detailed checklists.
