---
name: qcsd-refinement-swarm
description: "QCSD Refinement phase swarm for Sprint Refinement sessions using SFDIPOT product factors, BDD scenario generation, and requirements validation."
category: qcsd-phases
priority: critical
version: 1.0.0
tokenEstimate: 3200
# DDD Domain Mapping (from QCSD-AGENTIC-QE-MAPPING-FRAMEWORK.md)
domains:
  primary:
    - domain: requirements-validation
      agents: [qe-product-factors-assessor, qe-bdd-generator, qe-requirements-validator]
  conditional:
    - domain: contract-testing
      agents: [qe-contract-validator]
    - domain: code-intelligence
      agents: [qe-impact-analyzer, qe-dependency-mapper]
    - domain: enterprise-integration
      agents: [qe-middleware-validator, qe-odata-contract-tester, qe-sod-analyzer]
  transformation:
    - domain: test-generation
      agents: [qe-test-idea-rewriter]
# Agent Inventory
agents:
  core: [qe-product-factors-assessor, qe-bdd-generator, qe-requirements-validator]
  conditional: [qe-contract-validator, qe-impact-analyzer, qe-dependency-mapper, qe-middleware-validator, qe-odata-contract-tester, qe-sod-analyzer]
  transformation: [qe-test-idea-rewriter]
  total: 10
  sub_agents: 0
skills: [context-driven-testing, testability-scoring, risk-based-testing]
# Execution Models (Task Tool is PRIMARY)
execution:
  primary: task-tool
  alternatives: [mcp-tools, cli]
swarm_pattern: true
parallel_batches: 3
last_updated: 2026-02-02
enforcement_level: strict
tags: [qcsd, refinement, sfdipot, bdd, gherkin, requirements, swarm, parallel, ddd]
trust_tier: 3
validation:
  schema_path: schemas/output.json
  validator_path: scripts/validate-config.json
  eval_path: evals/qcsd-refinement-swarm.yaml

---

# QCSD Refinement Swarm v1.0

Shift-left quality engineering swarm for Sprint Refinement sessions.

---

## Overview

The Refinement Swarm takes user stories that passed Ideation and prepares them
for Sprint commitment using SFDIPOT product factors, BDD scenarios, and INVEST validation.
It renders a READY / CONDITIONAL / NOT-READY decision.

### QCSD Phase Positioning

| Phase | Swarm | Decision | When |
|-------|-------|----------|------|
| Ideation | qcsd-ideation-swarm | GO / CONDITIONAL / NO-GO | PI/Sprint Planning |
| **Refinement** | **qcsd-refinement-swarm** | **READY / CONDITIONAL / NOT-READY** | **Sprint Refinement** |
| Development | qcsd-development-swarm | SHIP / CONDITIONAL / HOLD | During Sprint |
| Verification | qcsd-cicd-swarm | RELEASE / REMEDIATE / BLOCK | Pre-Release / CI-CD |
| Production | qcsd-production-swarm | HEALTHY / DEGRADED / CRITICAL | Post-Release |

### Parameters

- `STORY_CONTENT`: User story with acceptance criteria (required)
- `OUTPUT_FOLDER`: Where to save reports (default: `${PROJECT_ROOT}/Agentic QCSD/refinement/`)

---

## ENFORCEMENT RULES - READ FIRST

| Rule | Enforcement |
|------|-------------|
| **E1** | MUST spawn ALL THREE core agents in Step 2. |
| **E2** | MUST put all parallel Task calls in a SINGLE message. |
| **E3** | MUST STOP and WAIT after each batch. |
| **E4** | MUST spawn conditional agents if flags are TRUE. |
| **E5** | MUST apply READY/CONDITIONAL/NOT-READY logic exactly. |
| **E6** | MUST generate the full report structure. |
| **E7** | Each agent MUST read its reference files before analysis. |
| **E8** | MUST apply qe-test-idea-rewriter transformation in Step 8. |
| **E9** | MUST execute Step 7 learning persistence. |

---

## Step Execution Protocol

Execute steps sequentially by reading each step file with the Read tool.

### Steps

1. **Flag Detection** -- `steps/01-flag-detection.md` -- Analyze story content, evaluate all 7 flags
2. **Core Agents** -- `steps/02-core-agents.md` -- Spawn qe-product-factors-assessor, qe-bdd-generator, qe-requirements-validator
3. **Batch 1 Results** -- `steps/03-batch1-results.md` -- Wait and extract metrics
4. **Conditional Agents** -- `steps/04-conditional-agents.md` -- Spawn flagged agents
5. **Decision Synthesis** -- `steps/05-decision-synthesis.md` -- Apply READY/CONDITIONAL/NOT-READY logic
6. **Report Generation** -- `steps/06-report-generation.md` -- Generate refinement report
7. **Learning Persistence** -- `steps/07-learning-persistence.md` -- Store findings to memory
8. **Transformation** -- `steps/08-transformation.md` -- Run test idea rewriter on all test ideas
9. **Final Output** -- `steps/09-final-output.md` -- Display completion summary

### Execution Instructions

1. Use the Read tool to load the current step file
2. Execute the step's instructions completely
3. Verify all success criteria are met
4. Pass output as context to next step
5. If a step fails, halt and report

### Resume Support

To resume from a specific step: specify `--from-step N`.

---

## Agent Inventory

| Agent | Type | Domain | Batch |
|-------|------|--------|-------|
| qe-product-factors-assessor | Core | requirements-validation | 1 |
| qe-bdd-generator | Core | requirements-validation | 1 |
| qe-requirements-validator | Core | requirements-validation | 1 |
| qe-contract-validator | Conditional (HAS_API) | contract-testing | 2 |
| qe-impact-analyzer | Conditional (HAS_REFACTORING) | code-intelligence | 2 |
| qe-dependency-mapper | Conditional (HAS_DEPENDENCIES) | code-intelligence | 2 |
| qe-middleware-validator | Conditional (HAS_MIDDLEWARE) | enterprise-integration | 2 |
| qe-odata-contract-tester | Conditional (HAS_SAP_INTEGRATION) | enterprise-integration | 2 |
| qe-sod-analyzer | Conditional (HAS_AUTHORIZATION) | enterprise-integration | 2 |
| qe-test-idea-rewriter | Transformation (always) | test-generation | 3 |

**Total: 10 agents (3 core + 6 conditional + 1 transformation)**

---

## Key Principle

**Refinement quality determines sprint success. This swarm ensures stories are
testable, complete, and ready for development commitment.**
