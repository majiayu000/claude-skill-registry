---
name: qcsd-development-swarm
description: "QCSD Development phase swarm for in-sprint code quality assurance using TDD adherence, code complexity analysis, coverage gap detection, and defect prediction. Consumes Refinement outputs (BDD scenarios, SFDIPOT priorities) and produces signals for Verification."
category: qcsd-phases
priority: critical
version: 1.0.0
tokenEstimate: 3400
# DDD Domain Mapping (from QCSD-AGENTIC-QE-MAPPING-FRAMEWORK.md)
domains:
  primary:
    - domain: test-generation
      agents: [qe-tdd-specialist]
    - domain: coverage-analysis
      agents: [qe-coverage-specialist]
    - domain: code-intelligence
      agents: [qe-code-complexity]
  conditional:
    - domain: security-compliance
      agents: [qe-security-scanner]
    - domain: chaos-resilience
      agents: [qe-performance-tester]
    - domain: test-generation
      agents: [qe-mutation-tester]
    - domain: enterprise-integration
      agents: [qe-message-broker-tester, qe-sap-idoc-tester, qe-sod-analyzer]
  analysis:
    - domain: defect-intelligence
      agents: [qe-defect-predictor]
# Agent Inventory
agents:
  core: [qe-tdd-specialist, qe-code-complexity, qe-coverage-specialist]
  conditional: [qe-security-scanner, qe-performance-tester, qe-mutation-tester, qe-message-broker-tester, qe-sap-idoc-tester, qe-sod-analyzer]
  analysis: [qe-defect-predictor]
  total: 10
  sub_agents: 0
skills: [tdd-london-chicago, mutation-testing, performance-testing, security-testing]
# Execution Models (Task Tool is PRIMARY)
execution:
  primary: task-tool
  alternatives: [mcp-tools, cli]
swarm_pattern: true
parallel_batches: 3
last_updated: 2026-02-03
enforcement_level: strict
tags: [qcsd, development, tdd, complexity, coverage, security, performance, mutation, defect-prediction, swarm, parallel, ddd]
trust_tier: 3
validation:
  schema_path: schemas/output.json
  validator_path: scripts/validate-config.json
  eval_path: evals/qcsd-development-swarm.yaml

---

# QCSD Development Swarm v1.0

Shift-left quality engineering swarm for in-sprint code quality assurance.

---

## Overview

The Development Swarm takes refined stories (that passed Refinement) and validates
code quality during sprint execution. Where the Ideation Swarm asks "Should we
build this?" and the Refinement Swarm asks "How should we test this?", the
Development Swarm asks "Is the code quality sufficient to ship?"

### QCSD Phase Positioning

| Phase | Swarm | Decision | When |
|-------|-------|----------|------|
| Ideation | qcsd-ideation-swarm | GO / CONDITIONAL / NO-GO | PI/Sprint Planning |
| Refinement | qcsd-refinement-swarm | READY / CONDITIONAL / NOT-READY | Sprint Refinement |
| **Development** | **qcsd-development-swarm** | **SHIP / CONDITIONAL / HOLD** | **During Sprint** |
| Verification | qcsd-cicd-swarm | RELEASE / REMEDIATE / BLOCK | Pre-Release / CI-CD |
| Production | qcsd-production-swarm | HEALTHY / DEGRADED / CRITICAL | Post-Release |

### Parameters

- `SOURCE_PATH`: Source code directory to analyze (required, e.g., `src/auth/`)
- `TEST_PATH`: Test directory for coverage analysis (optional, e.g., `tests/auth/`)
- `OUTPUT_FOLDER`: Where to save reports (default: `${PROJECT_ROOT}/Agentic QCSD/development/`)

---

## ENFORCEMENT RULES - READ FIRST

| Rule | Enforcement |
|------|-------------|
| **E1** | You MUST spawn ALL THREE core agents (qe-tdd-specialist, qe-code-complexity, qe-coverage-specialist) in Step 2. No exceptions. |
| **E2** | You MUST put all parallel Task calls in a SINGLE message. |
| **E3** | You MUST STOP and WAIT after each batch. No proceeding early. |
| **E4** | You MUST spawn conditional agents if flags are TRUE. No skipping. |
| **E5** | You MUST apply SHIP/CONDITIONAL/HOLD logic exactly as specified in Step 5. |
| **E6** | You MUST generate the full report structure. No abbreviated versions. |
| **E7** | Each agent MUST read its reference files before analysis. |
| **E8** | You MUST apply qe-defect-predictor analysis on ALL code changes in Step 8. Always. |
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

1. **Flag Detection** -- `steps/01-flag-detection.md` -- Scan source code and tests, detect all 6 flags
2. **Core Agents** -- `steps/02-core-agents.md` -- Spawn qe-tdd-specialist, qe-code-complexity, qe-coverage-specialist in parallel
3. **Batch 1 Results** -- `steps/03-batch1-results.md` -- Wait for core agents, extract all metrics
4. **Conditional Agents** -- `steps/04-conditional-agents.md` -- Spawn flagged conditional agents in parallel
5. **Decision Synthesis** -- `steps/05-decision-synthesis.md` -- Apply SHIP/CONDITIONAL/HOLD logic
6. **Report Generation** -- `steps/06-report-generation.md` -- Generate executive summary and full report
7. **Learning Persistence** -- `steps/07-learning-persistence.md` -- Store findings to memory, save persistence record
8. **Defect Predictor** -- `steps/08-defect-predictor.md` -- Run qe-defect-predictor analysis on all code changes
9. **Final Output** -- `steps/09-final-output.md` -- Display completion summary with all scores

### Execution Instructions

1. Use the Read tool to load the current step file (e.g., `Read({ file_path: ".claude/skills/qcsd-development-swarm/steps/01-flag-detection.md" })`)
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
| qe-tdd-specialist | Core (always) | test-generation | 1 |
| qe-code-complexity | Core (always) | code-intelligence | 1 |
| qe-coverage-specialist | Core (always) | coverage-analysis | 1 |
| qe-security-scanner | Conditional (HAS_SECURITY_CODE) | security-compliance | 2 |
| qe-performance-tester | Conditional (HAS_PERFORMANCE_CODE) | chaos-resilience | 2 |
| qe-mutation-tester | Conditional (HAS_CRITICAL_CODE) | test-generation | 2 |
| qe-message-broker-tester | Conditional (HAS_MIDDLEWARE) | enterprise-integration | 2 |
| qe-sap-idoc-tester | Conditional (HAS_SAP_INTEGRATION) | enterprise-integration | 2 |
| qe-sod-analyzer | Conditional (HAS_AUTHORIZATION) | enterprise-integration | 2 |
| qe-defect-predictor | Analysis (always) | defect-intelligence | 3 |

**Total: 10 agents (3 core + 6 conditional + 1 analysis)**

---

## Quality Gate Thresholds

| Metric | SHIP | CONDITIONAL | HOLD |
|--------|------|-------------|------|
| TDD Adherence | >= 80% | 60 - 79% | < 60% |
| Code Complexity | Avg <= 10 | Avg 11-15 | Avg > 15 |
| Test Coverage | >= 80% | 60 - 79% | < 60% |
| Mutation Score | >= 70% | 50 - 69% | < 50% |
| Security Issues | No HIGH/CRITICAL | MEDIUM only | HIGH/CRITICAL found |

---

## Report Filename Mapping

| Agent | Report Filename | Step |
|-------|----------------|------|
| qe-tdd-specialist | `02-tdd-analysis.md` | 2 |
| qe-code-complexity | `03-complexity-analysis.md` | 2 |
| qe-coverage-specialist | `04-coverage-analysis.md` | 2 |
| qe-security-scanner | `05-security-scan.md` | 4 |
| qe-performance-tester | `06-performance-analysis.md` | 4 |
| qe-mutation-tester | `07-mutation-testing.md` | 4 |
| qe-message-broker-tester | `08-middleware-health.md` | 4 |
| qe-sap-idoc-tester | `09-sap-integration.md` | 4 |
| qe-sod-analyzer | `10-sod-compliance.md` | 4 |
| Learning Persistence | `11-learning-persistence.json` | 7 |
| qe-defect-predictor | `12-defect-prediction.md` | 8 |
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

**Code quality is measured by evidence, not intentions. This swarm provides
in-sprint quality assessment to ensure code meets engineering standards before
entering the CI/CD pipeline.**
