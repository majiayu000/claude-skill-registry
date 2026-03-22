---
name: qcsd-cicd-swarm
description: "QCSD Verification phase swarm for CI/CD pipeline quality gates using regression analysis, flaky test detection, quality gate enforcement, and deployment readiness assessment. Consumes Development outputs (SHIP/CONDITIONAL/HOLD decisions, quality metrics) and produces signals for Production monitoring."
category: qcsd-phases
priority: critical
version: 1.0.0
tokenEstimate: 3500
# DDD Domain Mapping (from QCSD-AGENTIC-QE-MAPPING-FRAMEWORK.md)
domains:
  primary:
    - domain: quality-assessment
      agents: [qe-quality-gate]
    - domain: test-execution
      agents: [qe-regression-analyzer]
    - domain: test-execution
      agents: [qe-flaky-hunter]
  conditional:
    - domain: security-compliance
      agents: [qe-security-scanner]
    - domain: chaos-resilience
      agents: [qe-chaos-engineer]
    - domain: coverage-analysis
      agents: [qe-coverage-specialist]
    - domain: enterprise-integration
      agents: [qe-middleware-validator, qe-soap-tester, qe-sod-analyzer]
  analysis:
    - domain: quality-assessment
      agents: [qe-deployment-advisor]
# Agent Inventory
agents:
  core: [qe-quality-gate, qe-regression-analyzer, qe-flaky-hunter]
  conditional: [qe-security-scanner, qe-chaos-engineer, qe-coverage-specialist, qe-middleware-validator, qe-soap-tester, qe-sod-analyzer]
  analysis: [qe-deployment-advisor]
  total: 10
  sub_agents: 0
skills: [shift-left-testing, shift-right-testing, regression-testing, security-testing]
# Execution Models (Task Tool is PRIMARY)
execution:
  primary: task-tool
  alternatives: [mcp-tools, cli]
swarm_pattern: true
parallel_batches: 3
last_updated: 2026-02-03
enforcement_level: strict
tags: [qcsd, verification, cicd, pipeline, quality-gate, regression, flaky, security, chaos, coverage, deployment, swarm, parallel, ddd]
trust_tier: 3
validation:
  schema_path: schemas/output.json
  validator_path: scripts/validate-config.json
  eval_path: evals/qcsd-cicd-swarm.yaml

---

# QCSD CI/CD Swarm v1.0

Shift-left quality engineering swarm for CI/CD pipeline verification and release readiness.

---

## Overview

The CI/CD Swarm takes code that passed Development quality checks and validates it is
safe to release through the CI/CD pipeline. Where the Development Swarm asks "Is the
code quality sufficient to ship?", the CI/CD Swarm asks "Is this change safe to release?"

This swarm operates at the pipeline level, analyzing test results, regression risk,
flaky test impact, security pipeline status, and infrastructure changes to render
a RELEASE / REMEDIATE / BLOCK decision.

### QCSD Phase Positioning

| Phase | Swarm | Decision | When |
|-------|-------|----------|------|
| Ideation | qcsd-ideation-swarm | GO / CONDITIONAL / NO-GO | PI/Sprint Planning |
| Refinement | qcsd-refinement-swarm | READY / CONDITIONAL / NOT-READY | Sprint Refinement |
| Development | qcsd-development-swarm | SHIP / CONDITIONAL / HOLD | During Sprint |
| **Verification** | **qcsd-cicd-swarm** | **RELEASE / REMEDIATE / BLOCK** | **Pre-Release / CI-CD** |
| Production | qcsd-production-swarm | HEALTHY / DEGRADED / CRITICAL | Post-Release |

### Parameters

- `PIPELINE_ARTIFACTS`: Path to CI/CD artifacts, test results, and build output (required, e.g., `ci/artifacts/`)
- `BASELINE_REF`: Git ref for baseline comparison (optional, default: `main`)
- `OUTPUT_FOLDER`: Where to save reports (default: `${PROJECT_ROOT}/Agentic QCSD/cicd/`)
- `DEPLOY_TARGET`: Target deployment environment (optional, e.g., `staging`, `production`)

---

## ENFORCEMENT RULES - READ FIRST

| Rule | Enforcement |
|------|-------------|
| **E1** | You MUST spawn ALL THREE core agents (qe-quality-gate, qe-regression-analyzer, qe-flaky-hunter) in Step 2. No exceptions. |
| **E2** | You MUST put all parallel Task calls in a SINGLE message. |
| **E3** | You MUST STOP and WAIT after each batch. No proceeding early. |
| **E4** | You MUST spawn conditional agents if flags are TRUE. No skipping. |
| **E5** | You MUST apply RELEASE/REMEDIATE/BLOCK logic exactly as specified in Step 5. |
| **E6** | You MUST generate the full report structure. No abbreviated versions. |
| **E7** | Each agent MUST read its reference files before analysis. |
| **E8** | You MUST apply qe-deployment-advisor analysis on ALL pipeline data in Step 8. Always. |
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

1. **Flag Detection** -- `steps/01-flag-detection.md` -- Scan pipeline artifacts, detect all 6 flags
2. **Core Agents** -- `steps/02-core-agents.md` -- Spawn qe-quality-gate, qe-regression-analyzer, qe-flaky-hunter in parallel
3. **Batch 1 Results** -- `steps/03-batch1-results.md` -- Wait for core agents, extract all metrics
4. **Conditional Agents** -- `steps/04-conditional-agents.md` -- Spawn flagged conditional agents in parallel
5. **Decision Synthesis** -- `steps/05-decision-synthesis.md` -- Apply RELEASE/REMEDIATE/BLOCK logic
6. **Report Generation** -- `steps/06-report-generation.md` -- Generate executive summary and full report
7. **Learning Persistence** -- `steps/07-learning-persistence.md` -- Store findings to memory, save persistence record
8. **Deployment Advisor** -- `steps/08-deployment-advisor.md` -- Run qe-deployment-advisor analysis on all pipeline data
9. **Final Output** -- `steps/09-final-output.md` -- Display completion summary with all scores

### Execution Instructions

1. Use the Read tool to load the current step file (e.g., `Read({ file_path: ".claude/skills/qcsd-cicd-swarm/steps/01-flag-detection.md" })`)
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
| qe-quality-gate | Core (always) | quality-assessment | 1 |
| qe-regression-analyzer | Core (always) | test-execution | 1 |
| qe-flaky-hunter | Core (always) | test-execution | 1 |
| qe-security-scanner | Conditional (HAS_SECURITY_PIPELINE) | security-compliance | 2 |
| qe-chaos-engineer | Conditional (HAS_INFRA_CHANGE) | chaos-resilience | 2 |
| qe-coverage-specialist | Conditional (HAS_PERFORMANCE_PIPELINE) | coverage-analysis | 2 |
| qe-middleware-validator | Conditional (HAS_MIDDLEWARE) | enterprise-integration | 2 |
| qe-soap-tester | Conditional (HAS_SAP_INTEGRATION) | enterprise-integration | 2 |
| qe-sod-analyzer | Conditional (HAS_AUTHORIZATION) | enterprise-integration | 2 |
| qe-deployment-advisor | Analysis (always) | quality-assessment | 3 |

**Total: 10 agents (3 core + 6 conditional + 1 analysis)**

---

## Quality Gate Thresholds

| Metric | RELEASE | REMEDIATE | BLOCK |
|--------|---------|-----------|-------|
| Test Pass Rate | >= 99% | 95 - 98.9% | < 95% |
| Regression Count | 0 | 1-3 (P2/P3) | Any P0/P1 |
| Flaky Test Rate | < 2% | 2 - 5% | > 5% |
| Quality Gate | ALL PASS | WARN gates only | ANY FAIL gate |
| Security Scan | No HIGH/CRITICAL | MEDIUM only | HIGH/CRITICAL found |
| Coverage Delta | >= 0% | -1% to -5% | < -5% |

---

## Report Filename Mapping

| Agent | Report Filename | Step |
|-------|----------------|------|
| qe-quality-gate | `02-quality-gates.md` | 2 |
| qe-regression-analyzer | `03-regression-analysis.md` | 2 |
| qe-flaky-hunter | `04-flaky-test-analysis.md` | 2 |
| qe-security-scanner | `05-security-scan.md` | 4 |
| qe-chaos-engineer | `06-chaos-resilience.md` | 4 |
| qe-coverage-specialist | `07-coverage-analysis.md` | 4 |
| qe-middleware-validator | `08-middleware-health.md` | 4 |
| qe-soap-tester | `09-soap-contracts.md` | 4 |
| qe-sod-analyzer | `10-sod-compliance.md` | 4 |
| Learning Persistence | `11-learning-persistence.json` | 7 |
| qe-deployment-advisor | `12-deployment-advisory.md` | 8 |
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

**Release safety is verified by evidence, not assumptions. This swarm provides
pipeline-level quality assessment to ensure every release meets quality gates.**
