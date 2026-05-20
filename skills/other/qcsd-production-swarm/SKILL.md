---
name: qcsd-production-swarm
description: "QCSD Production Telemetry phase swarm for post-release production health assessment using DORA metrics, root cause analysis, defect prediction, and cross-phase feedback loops. Consumes CI/CD outputs (RELEASE/REMEDIATE/BLOCK decisions, release readiness metrics) and produces feedback signals to Ideation and Refinement."
category: qcsd-phases
priority: critical
version: 1.0.0
tokenEstimate: 32000
# DDD Domain Mapping (from QCSD-AGENTIC-QE-MAPPING-FRAMEWORK.md)
domains:
  primary:
    - domain: learning-optimization
      agents: [qe-metrics-optimizer]
    - domain: defect-intelligence
      agents: [qe-defect-predictor, qe-root-cause-analyzer]
  conditional:
    - domain: chaos-resilience
      agents: [qe-chaos-engineer, qe-performance-tester]
    - domain: defect-intelligence
      agents: [qe-regression-analyzer, qe-pattern-learner]
    - domain: enterprise-integration
      agents: [qe-middleware-validator, qe-sap-rfc-tester, qe-sod-analyzer]
  feedback:
    - domain: learning-optimization
      agents: [qe-learning-coordinator, qe-transfer-specialist]
# Agent Inventory
agents:
  core: [qe-metrics-optimizer, qe-defect-predictor, qe-root-cause-analyzer]
  conditional: [qe-chaos-engineer, qe-performance-tester, qe-regression-analyzer, qe-pattern-learner, qe-middleware-validator, qe-sap-rfc-tester, qe-sod-analyzer]
  feedback: [qe-learning-coordinator, qe-transfer-specialist]
  total: 12
  sub_agents: 0
skills: [shift-right-testing, chaos-engineering-resilience, quality-metrics, performance-testing, holistic-testing-pact]
# Execution Models (Task Tool is PRIMARY)
execution:
  primary: task-tool
  alternatives: [mcp-tools, cli]
swarm_pattern: true
parallel_batches: 3
last_updated: 2026-02-17
enforcement_level: strict
tags: [qcsd, production, telemetry, dora, rca, defect-prediction, feedback-loop, learning, swarm, parallel, ddd]
trust_tier: 3
validation:
  schema_path: schemas/output.json
  validator_path: scripts/validate-config.json
  eval_path: evals/qcsd-production-swarm.yaml

---

# QCSD Production Swarm v1.0

Post-release production health assessment and QCSD feedback loop closure.

---

## Overview

The Production Swarm assesses release health in the live production environment using
DORA metrics, incident RCA, defect prediction, and cross-phase feedback loops. It renders
a HEALTHY / DEGRADED / CRITICAL decision and is the only QCSD phase with dual
responsibility: assessing current production health AND closing the feedback loop
back to Ideation and Refinement phases.

### QCSD Phase Positioning

| Phase | Swarm | Decision | When |
|-------|-------|----------|------|
| Ideation | qcsd-ideation-swarm | GO / CONDITIONAL / NO-GO | PI/Sprint Planning |
| Refinement | qcsd-refinement-swarm | READY / CONDITIONAL / NOT-READY | Sprint Refinement |
| Development | qcsd-development-swarm | SHIP / CONDITIONAL / HOLD | During Sprint |
| Verification | qcsd-cicd-swarm | RELEASE / REMEDIATE / BLOCK | Pre-Release / CI-CD |
| **Production** | **qcsd-production-swarm** | **HEALTHY / DEGRADED / CRITICAL** | **Post-Release** |

### Parameters

- `TELEMETRY_DATA`: Path to production telemetry, incident reports, and DORA metrics (required)
- `RELEASE_ID`: Release identifier for tracking (optional)
- `OUTPUT_FOLDER`: Where to save reports (default: `${PROJECT_ROOT}/Agentic QCSD/production/`)
- `SLA_DEFINITIONS`: Path to SLA/SLO target definitions (optional)

---

## ENFORCEMENT RULES - READ FIRST

| Rule | Enforcement |
|------|-------------|
| **E1** | You MUST spawn ALL THREE core agents in Step 2. No exceptions. |
| **E2** | You MUST put all parallel Task calls in a SINGLE message. |
| **E3** | You MUST STOP and WAIT after each batch. No proceeding early. |
| **E4** | You MUST spawn conditional agents if flags are TRUE. No skipping. |
| **E5** | You MUST apply HEALTHY/DEGRADED/CRITICAL logic exactly as specified in Step 5. |
| **E6** | You MUST generate the full report structure. No abbreviated versions. |
| **E7** | Each agent MUST read its reference files before analysis. |
| **E8** | You MUST run BOTH feedback agents in Step 8 SEQUENTIALLY. Always. Both agents. |
| **E9** | You MUST execute Step 7 learning persistence. No skipping. |

**PROHIBITED BEHAVIORS:**
- Summarizing instead of spawning agents
- Skipping agents "for brevity"
- Proceeding before background tasks complete
- Providing your own analysis instead of spawning specialists
- Omitting report sections or using placeholder text

---

## Step Execution Protocol

This skill uses a micro-file step architecture. Each step is a self-contained file
loaded one at a time to avoid "lost in the middle" context degradation.

**Execute steps sequentially by reading each step file with the Read tool.**

### Steps

1. **Flag Detection** -- `steps/01-flag-detection.md` -- Retrieve CI/CD signals, detect telemetry source, evaluate all 7 flags
2. **Core Agents** -- `steps/02-core-agents.md` -- Spawn qe-metrics-optimizer, qe-defect-predictor, qe-root-cause-analyzer in parallel
3. **Batch 1 Results** -- `steps/03-batch1-results.md` -- Wait for core agents, extract all metrics
4. **Conditional Agents** -- `steps/04-conditional-agents.md` -- Spawn flagged conditional agents in parallel
5. **Decision Synthesis** -- `steps/05-decision-synthesis.md` -- Apply HEALTHY/DEGRADED/CRITICAL logic
6. **Report Generation** -- `steps/06-report-generation.md` -- Generate executive summary and full report
7. **Learning Persistence** -- `steps/07-learning-persistence.md` -- Store findings to memory, save persistence record
8. **Feedback Loop** -- `steps/08-feedback-loop.md` -- Run learning coordinator then transfer specialist (sequential)
9. **Final Output** -- `steps/09-final-output.md` -- Display completion summary with all scores

### Execution Instructions

1. Use the Read tool to load the current step file (e.g., `Read({ file_path: ".claude/skills/qcsd-production-swarm/steps/01-flag-detection.md" })`)
2. Execute the step's instructions completely
3. Verify all success criteria are met before proceeding
4. Pass the step's output as context to the next step
5. If a step fails, halt and report the failure point -- do not skip ahead

### Resume Support

To resume from a specific step: specify `--from-step N` and the orchestrator will
skip to step N. Ensure you have the required prerequisite data from prior steps.

---

## Agent Inventory

| Agent | Type | Domain | Batch |
|-------|------|--------|-------|
| qe-metrics-optimizer | Core (always) | learning-optimization | 1 |
| qe-defect-predictor | Core (always) | defect-intelligence | 1 |
| qe-root-cause-analyzer | Core (always) | defect-intelligence | 1 |
| qe-chaos-engineer | Conditional (HAS_INFRASTRUCTURE_CHANGE) | chaos-resilience | 2 |
| qe-performance-tester | Conditional (HAS_PERFORMANCE_SLA) | chaos-resilience | 2 |
| qe-regression-analyzer | Conditional (HAS_REGRESSION_RISK) | defect-intelligence | 2 |
| qe-pattern-learner | Conditional (HAS_RECURRING_INCIDENTS) | defect-intelligence | 2 |
| qe-middleware-validator | Conditional (HAS_MIDDLEWARE) | enterprise-integration | 2 |
| qe-sap-rfc-tester | Conditional (HAS_SAP_INTEGRATION) | enterprise-integration | 2 |
| qe-sod-analyzer | Conditional (HAS_AUTHORIZATION) | enterprise-integration | 2 |
| qe-learning-coordinator | Feedback (always, sequential) | learning-optimization | 3 |
| qe-transfer-specialist | Feedback (always, sequential) | learning-optimization | 3 |

**Total: 12 agents (3 core + 7 conditional + 2 feedback)**

---

## Quality Gate Thresholds

| Metric | HEALTHY | DEGRADED | CRITICAL |
|--------|---------|----------|----------|
| DORA Score | >= 0.7 | 0.4 - 0.69 | < 0.4 |
| SLA Compliance | >= 99% | 95 - 98.9% | < 95% |
| Incident Severity | P3/P4/NONE | P2 | P0/P1 |
| Defect Trend | declining/stable | stable (density > 2) | increasing + density > 5 |
| RCA Completeness | >= 80% | 50 - 79% | < 50% |

---

## Report Filename Mapping

| Agent | Report Filename | Step |
|-------|----------------|------|
| qe-metrics-optimizer | `02-dora-metrics.md` | 2 |
| qe-defect-predictor | `03-defect-prediction.md` | 2 |
| qe-root-cause-analyzer | `04-root-cause-analysis.md` | 2 |
| qe-chaos-engineer | `05-chaos-resilience.md` | 4 |
| qe-performance-tester | `06-performance-sla.md` | 4 |
| qe-regression-analyzer | `07-regression-analysis.md` | 4 |
| qe-pattern-learner | `08-pattern-analysis.md` | 4 |
| Learning Persistence | `09-learning-persistence.json` | 7 |
| qe-middleware-validator | `10-middleware-health.md` | 4 |
| qe-sap-rfc-tester | `11-sap-health.md` | 4 |
| qe-sod-analyzer | `12-sod-compliance.md` | 4 |
| Feedback agents | `13-feedback-loops.md` | 8 |
| Synthesis | `01-executive-summary.md` | 6 |

---

## Execution Model Options

| Model | When to Use | Agent Spawn |
|-------|-------------|-------------|
| **Task Tool** (PRIMARY) | Claude Code sessions | `Task({ subagent_type, run_in_background: true })` |
| **MCP Tools** | MCP server available | `fleet_init({})` / `task_submit({})` |
| **CLI** | Terminal/scripts | `swarm init` / `agent spawn` |

---

## Key Principle

**Production health is measured by outcomes, not intentions. This swarm provides
evidence-based production assessment and closes the QCSD feedback loop.**
