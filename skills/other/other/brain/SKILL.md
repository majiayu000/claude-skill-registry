---
name: loki-mode
description: Master multi-agent swarm orchestration. Spawns and coordinates specialized personas for large projects that exceed single-agent context limits. Manages 10-phase SDLC with checkpoints, memory, and human-in-the-loop gates.
triggers: [loki, swarm, orchestrate, big project, autonomous build, multi-agent, spawn, coordinate swarm]
context_cost: high
---

# Loki Mode — Master Orchestration Skill

## Goal

Coordinate a swarm of specialized agent personas through a full SDLC lifecycle, with
durable checkpoints, memory, and human approval gates — enabling large projects that
would otherwise exceed a single agent's context limits.

---

## Pre-Start Check

Before doing anything else:

```
1. Check: does agents/memory/PROJECT_STATE.md exist AND phase != S00_INITIALIZED?
   - YES → This is a RESUMED project → invoke session-resume.skill first
           Load all memory, then continue from the current phase
   - NO  → This is a NEW project → proceed with INIT below
```

---

## INIT (New Project Only)

```
1. Create directory structure if missing:
   mkdir -p agents/memory/episodic/SESSION_SNAPSHOT
   mkdir -p agents/memory/semantic
   mkdir -p agents/personas

2. Initialize memory files:
   - agents/memory/PROJECT_STATE.md    → set phase: S01, status: IN_PROGRESS
   - agents/memory/AUDIT_LOG.md        → write header + first entry: LOKI_INIT
   - agents/memory/CONTINUITY.md       → write header (empty failures list)

3. Announce to user:
   "Loki Mode initialized. Starting [PROJECT_NAME] from scratch.
    Current phase: S01_REQUIREMENTS
    All checkpoints will be saved to agents/memory/"
```

---

## Orchestration Loop — 10 SDLC Phases

### PHASE S01 — Requirements

```
Persona: prod-pm
Task:    Write PRD.md using EARS syntax
         Ask user clarifying questions (ambiguity layer)
         Fill templates/PRD_TEMPLATE.md
         Run ai-ethics-compliance.skill (Mandatory Bias Check)
         IF CRITICAL (Health/Aviation):
           - Engage prod-safety-engineer
           - Run hazard-analysis.skill (FMEA/STPA)
Output:  docs/requirements/PRD.md
         docs/requirements/EARS_REQUIREMENTS.md

Gate:    HUMAN APPROVAL REQUIRED
         Present PRD to user → wait for explicit approval
         User may request changes → loop until approved

Checkpoint: sdlc-checkpoint.skill S01
  - Write: agents/memory/episodic/SESSION_SNAPSHOT/S01_requirements.md
  - Update: agents/memory/PROJECT_STATE.md → phase: S01, status: DONE
  - Log:    agents/memory/AUDIT_LOG.md → PHASE_TRANSITION: S01 complete
```

### PHASE S02 — Architecture Design

```
Personas: prod-architect (lead), ops-security (threat review)
Tasks:    prod-architect:
            - Write PLAN.md using C4 model
            - Define Error Handling Strategy (RFC 7807) using error-handling-strategy.skill
            - Create docs/architecture/C4_ARCHITECTURE.md
            - Write ADRs for all major decisions → docs/architecture/decisions/
          ops-security:
            - Review architecture for security concerns (adversarial)
            - Run threat-model.skill on critical components
            - Write THREAT_MODEL.md → docs/security/

Output:   PLAN.md, C4_ARCHITECTURE.md, ADR-001+, THREAT_MODEL.md

Gate:     HUMAN APPROVAL REQUIRED
          Present: architecture summary + threat assessment + (Safety Case if Critical)
          Wait for approval. Loop if changes requested.

Checkpoint: sdlc-checkpoint.skill S02
```

### PHASE S03 — Technical Specification

```
Persona: prod-tech-lead (with prod-architect review)
Tasks:   - Fill templates/SPEC_TEMPLATE.md
         - Define all API contracts (OpenAPI YAML)
         - Define Event Topology (AsyncAPI) & Schemas (event-governance.skill)
         - Define database schema changes
         - Define Data Governance (Classification) & Access Control (RBAC)
         - Define RPO/RTO targets
         - Define testing strategy
Output:  SPEC.md, docs/api/openapi.yaml, docs/db/schema-changes.md

Gate:    HUMAN APPROVAL REQUIRED (lighter — may be async review)

Checkpoint: sdlc-checkpoint.skill S03
```

### PHASE S04 — Task Decomposition

```
Persona: prod-tech-lead (with orch-planner)
Tasks:   - Read SPEC.md + PLAN.md
         - Decompose into atomic tasks (15-minute rule enforced)
         - Fill templates/TASKS_TEMPLATE.md
         - Assign each task to the appropriate eng-* persona
         - Identify dependencies (DAG) AND Independent tasks
         - **Parallelism**: Mark independent tasks with `[PARALLEL]` tag
         
         - **Adaptive Check**:
           - *If Plan Complexity > High*: Inject `S02_DEEP_RESEARCH` (Consult KIs / Web)
           - *If Security Critical*: Inject `safety-scan` pre-check

Output:  project/tasks.md with T-NNN IDs, status: TODO, tags: [PARALLEL] if applicable

Gate:    orch-judge reviews task decomposition:
         - Are all tasks < 15 minutes?
         - Does task coverage match SPEC acceptance criteria?
         - Are parallel groups correctly identified?

Checkpoint: sdlc-checkpoint.skill S04
```

### PHASE S05 — Implementation

```
Persona: orch-planner (coordinator), eng-* (executors)

Implementation Loop (repeats until all tasks DONE):
  1. orch-planner analyzes `project/tasks.md`:
     - Identifies next batch of independent TODO tasks (Parallel Group)
     - Or next sequential task if dependencies exist

  2. **Context Retrieval (RAG)**:
     - Invoke `knowledge-connect.skill` query: "How to implement [task keywords]?"
     - Retrieve top 3 relevant snippets from `VECTOR_DB_CONFIG` source
     - **On Failure**: Log warning "RAG Unavailable", attempt fallback to `filesystem` search, or proceed with available context only.
     - Inject into task context

  3. **Delegation (A2A Check)**:
     - Is this task for an external agent? (e.g., "Ask Security Swarm")
     - YES -> Invoke `agent-interop.skill` -> Delegate -> Wait -> generic result
     - NO  -> Assign to internal `eng-*` persona

  4. **Execution (Parallel/Batch)**:
     - For each task in current batch (concurrently if model supports):
       
       assigned eng-* persona executes RARV Cycle:
       REASON:  Load task context + AGENTS.md + CONTINUITY.md + RAG Context
                Write mini-plan before touching files

       ACT:     Write failing test (TDD Red — MANDATORY)
                Verify test fails before implementing
                Run `safety-scan.skill` (Guardrail)
                Implement minimal code (Apply secure-coding.skill triggers)
                Update project/tasks.md: status → IN_PROGRESS

       REFLECT: Library-First? Layer boundaries? Security inputs? PII in logs?

       VERIFY:  Run: [test command]      → must be GREEN
                Run: [typecheck]         → zero errors
                Run: [lint]              → zero errors
                Run: agentic-linter      → no violations

  5. **Batch Result Processing**:
     - If VERIFY passes:
       - Update project/tasks.md: status → DONE
       - Write audit-trail.skill entry: TASK_DONE
     
     - If VERIFY fails:
       - **Quick Check**: Invoke `ci-autofix` (Autonomous Remediation)
         - If FIXED -> Proceed to DONE logic
       - **Dynamic Optimization**: Invoke `self-heal.skill` (max 5 attempts)
         - *Input*: Error log + Task Context + RAG Context
         - *Output*: Fix applied OR Escalation
       - **Meta-Optimization**: If `self-heal` FAILS repeatedly (>3x):
         - Invoke `meta-optimize.skill` (Rewrite the failing skill/prompt)
         - Log: "Self-Evolution Triggered for [Skill Name]"
       - If escalated:
         - orch-coordinator logs HUMAN_ESCALATION
         - task status → BLOCKED

  6. Repeat until all tasks DONE

Checkpoint: sdlc-checkpoint.skill S05
  (Save after every batch to prevent state loss)
```

### PHASE S06 — Testing & Quality

```
Persona: eng-qa (lead), orch-judge (validator)

eng-qa Tasks:
  - Run full test suite → verify all green
  - Check coverage ≥ 96% per module
  - Run integration test suite
  - Identify any missing test scenarios from EARS acceptance criteria
  - Fill any gaps via tdd-cycle.skill

orch-judge Tasks:
  - 7-Gate Quality Check:
    Gate 1: Lint/Syntax  → ESLint/PHP-CS-Fixer → zero errors
    Gate 2: Type Safety  → tsc/PHPStan         → zero errors
    Gate 3: Coverage     → Vitest/Pest          → ≥ 96%
    Gate 4: Integration  → Docker Compose       → all green
    Gate 5: Security     → dependency-security.skill → no critical vulnerabilities
    Gate 6: Complexity   → Cyclomatic < 10 for all functions
    Gate 7: Architecture → architecture-governance.skill → no layer violations (Fitness Functions)
    Gate 8: E2E          → e2e-test-suite (Playwright/Cypress) → all critical flows PASS
    Gate 9: EARS         → All acceptance criteria have passing tests

  If any gate fails: assign remediation task to eng-* persona → loop

Gate:    All 9 gates PASS

Checkpoint: sdlc-checkpoint.skill S06
```

### PHASE S07 — Security Review

```
Personas: ops-security (adversarial), eng-qa (verification)

ops-security Tasks:
  - security-audit.skill → OWASP Top 10 full scan
  - threat-model.skill → verify mitigations implemented
  - privacy-audit.skill → PII scan (if applicable)
  - ai-safety-guardrails.skill → Verify protection against prompt injection
  - compliance-review.skill → if regulated (SOC2/PCI/HIPAA)
  - Fill: templates/SECURITY_CHECKLIST.md
  - Document all findings in: docs/security/SECURITY_REVIEW.md

Acceptance:
  - SECURITY_CHECKLIST.md: all items ✓
  - No HIGH severity open findings
  - All MEDIUM findings have documented mitigations or accepted risks

Gate:    SECURITY_CHECKLIST passed + no critical CVEs

Checkpoint: sdlc-checkpoint.skill S07
```

### PHASE S08 — Human Review

```
Personas: prod-tech-lead (review prep), orch-judge (EARS compliance)

Prep:
  - prod-tech-lead generates review summary:
    - What was built (linked to SPEC acceptance criteria)
    - All ADRs made during implementation
    - All security findings and resolutions
    - Test coverage report
    - Any known limitations or deferred tech debt
  - orch-judge: final EARS compliance check
    - All requirements addressed? (DONE)
    - Any "Nice to Have" deferred with documented reason?

  - **Double Verification Protocol**:
    1. orch-judge verifies logic & specs (Automated)
    2. prod-tech-lead verifies code quality & patterns (Human-Proxy)
    3. prod-ethicist verifies final safety check (Safety)

Gate:    DOUBLE VERIFICATION + HUMAN APPROVAL REQUIRED
         This is a mandatory stop — no autonomous continuation.
         Human may request changes → loop back to S05 for specific tasks.

Checkpoint: sdlc-checkpoint.skill S08
```

### PHASE S09 — Staging Deployment

```
Persona: ops-devops (lead), eng-qa (smoke tests)

ops-devops Tasks:
  - deployment.skill → staging environment
  - Verify CI/CD pipeline passes
  - Run smoke tests against staging

eng-qa Tasks:
  - Verify critical user flows work in staging
  - Verify Restore from Backup (backup-recovery.skill) — Mandatory
  - Verify DLQ Consumption & Replay (queue-management.skill)
  - Check monitoring/alerting is configured
  - Run performance-audit.skill against staging

Gate:    All smoke tests GREEN + monitoring verified
         (If Critical: Failover Test PASS via reliability-engineering.skill)

Checkpoint: sdlc-checkpoint.skill S09
```

### PHASE S10 — Production Deployment

```
Persona: ops-devops (lead), ops-sre (reliability check)

Pre-deployment:
  - ops-sre: verify rollback plan is documented
  - ops-sre: verify monitoring/alerting will cover new features
  - ops-sre: confirm SLO thresholds are set

Deployment:
  - deployment.skill → production
  - Feature flags (if applicable): enable for canary %
  - Monitor for 15 minutes after deployment

Post-deployment:
  - ops-monitor: verify dashboards show normal metrics
  - Write deployment record to AUDIT_LOG.md

Gate:    Production healthy for 15+ minutes

Checkpoint: sdlc-checkpoint.skill S10
  - THIS IS THE FINAL CHECKPOINT
  - Update PROJECT_STATE.md: phase: COMPLETE
  - Write completion summary to AUDIT_LOG.md
  - Archive SESSION_SNAPSHOT: S10_production.md
```

---

## Interruption Handling

At any point during S05 (implementation), save state:

```
On graceful exit:
  1. Complete current task if < 50% remaining work
  2. sdlc-checkpoint.skill → save mid-phase snapshot
  3. Update PROJECT_STATE.md with exact position
  4. Log: AUDIT_LOG.md → SESSION_END

On unexpected interruption (context limit, crash):
  - Next session: session-resume.skill will detect incomplete tasks
  - Any BLOCKED task will appear in resume report
  - Resume from last DONE task
```

---

## Human-in-the-Loop Protocol

Loki Mode requires human approval at these gates:
- **S01**: Requirements approval (PRD.md)
- **S02**: Architecture approval (PLAN.md + threat model)
- **S08**: Final code review before deployment

Loki Mode escalates to human when:
- Self-heal loop exhausted (5 attempts, still failing)
- Architecture change needed (beyond original PLAN.md)
- Security finding with HIGH severity requiring policy decision
- Conflicting requirements found in PRD/SPEC
- CONSTITUTION.md amendment needed
- Any BLOCKED task after 24 hours

Human responses must be recorded in AUDIT_LOG.md before proceeding.

---

## Memory Management

Throughout the project:

```
After each task DONE:
  → audit-trail.skill: log TASK_DONE

After each self-heal resolution:
  → If root cause was non-obvious:
    Write to agents/memory/CONTINUITY.md:
    "Past failure: [what failed]. Root cause: [why]. Resolution: [what worked]."

After each research finding (from orch-researcher):
  → Write to agents/memory/semantic/PROJECT_KNOWLEDGE_TEMPLATE.md

After each SDLC phase:
  → sdlc-checkpoint.skill: write SESSION_SNAPSHOT
  → Update agents/memory/PROJECT_STATE.md
```

---

## Failure Escalation Protocol

```
Task fails:
  → self-heal.skill (attempts 1-4)
  → self-heal attempt 5 fails
  → orch-coordinator creates escalation:

Escalation report contains:
  1. Task ID and description
  2. Acceptance criteria that failed
  3. 5 attempts with: approach tried, error encountered, why it failed
  4. Research findings (from orch-researcher)
  5. Two recommended options for human decision
  6. Estimated impact of deferral

After escalation:
  → project/tasks.md: task status → BLOCKED
  → AUDIT_LOG.md: HUMAN_ESCALATION entry
  → ALL autonomous work on this task stops
  → Project continues on unblocked tasks (if DAG allows)
  → Human responds → orch-coordinator applies decision → retry
```

---

## Output Format

At start of each phase:
```
[LOKI] Phase S0X — [PHASE NAME]
Persona(s): [list]
Goal: [one sentence]
Expected outputs: [list]
```

At end of each phase:
```
[LOKI] Checkpoint S0X — SAVED
Gate status: [PASS/PENDING HUMAN APPROVAL/BLOCKED]
Next: [next phase or waiting for human]
```

At interruption:
```
[LOKI] State saved to: agents/memory/episodic/SESSION_SNAPSHOT/
Resume with: "continue loki project" or "session-resume"
Current position: Phase S0X, Task T-NNN
```

---

## Constraints

- Never skip a required HUMAN APPROVAL gate
- Never advance a task to DONE without passing VERIFY phase
- Never modify AUDIT_LOG.md existing entries (append only)
- Never start S05 without S01-S04 checkpoints saved
- Never deploy to production without S07 security review
- Self-heal loop hard limit: 5 attempts per task
- Tasks must remain atomic: if scope grows, decompose further
- orch-judge has veto power over any phase completion
