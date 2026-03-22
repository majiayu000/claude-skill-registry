---
name: qcsd-ideation-swarm
description: "QCSD Ideation phase swarm for Quality Criteria sessions using HTSM v6.3, Risk Storming, and Testability analysis before development begins. Uses 5-tier browser cascade: Vibium -> agent-browser -> Playwright+Stealth -> WebFetch -> WebSearch-fallback."
category: qcsd-phases
priority: critical
version: 7.5.1
tokenEstimate: 3500
# DDD Domain Mapping (from QCSD-AGENTIC-QE-MAPPING-FRAMEWORK.md)
domains:
  primary:
    - domain: requirements-validation
      agents: [qe-quality-criteria-recommender, qe-requirements-validator]
    - domain: coverage-analysis
      agents: [qe-risk-assessor]
  conditional:
    - domain: security-compliance
      agents: [qe-security-auditor]
    - domain: visual-accessibility
      agents: [qe-accessibility-auditor]
    - domain: cross-domain
      agents: [qe-qx-partner]
    - domain: enterprise-integration
      agents: [qe-middleware-validator, qe-sap-rfc-tester, qe-sod-analyzer]
# Agent Inventory
agents:
  core: [qe-quality-criteria-recommender, qe-risk-assessor, qe-requirements-validator]
  conditional: [qe-accessibility-auditor, qe-security-auditor, qe-qx-partner, qe-middleware-validator, qe-sap-rfc-tester, qe-sod-analyzer]
  total: 9
  sub_agents: 0
skills: [testability-scoring, risk-based-testing, context-driven-testing, holistic-testing-pact]
# Execution Models (Task Tool is PRIMARY)
execution:
  primary: task-tool
  alternatives: [mcp-tools, cli]
swarm_pattern: true
parallel_batches: 2
last_updated: 2026-01-28
# v7.5.1 Changelog: Added prominent follow-up recommendation box at end of swarm execution (Phase URL-9)
# v7.5.0 Changelog: Added HAS_VIDEO flag detection with /a11y-ally follow-up recommendation for video caption generation
# v7.4.0 Changelog: Automated browser cascade via scripts/fetch-content.js with 30s per-tier timeouts
# v7.2.0 Changelog: Added 5-tier browser cascade (Vibium -> agent-browser -> Playwright+Stealth -> WebFetch -> WebSearch)
html_output: true
enforcement_level: strict
tags: [qcsd, ideation, htsm, quality-criteria, risk-storming, testability, swarm, parallel, ddd]
trust_tier: 3
validation:
  schema_path: schemas/output.json
  validator_path: scripts/validate-config.json
  eval_path: evals/qcsd-ideation-swarm.yaml

---

# QCSD Ideation Swarm v7.0

Shift-left quality engineering swarm for PI Planning and Sprint Planning.

---

## Overview

The Ideation Swarm assesses stories and URLs before development begins, using HTSM v6.3
quality criteria, Risk Storming, and Testability analysis. It renders a
GO / CONDITIONAL / NO-GO decision and is the first gate in the QCSD lifecycle.

### QCSD Phase Positioning

| Phase | Swarm | Decision | When |
|-------|-------|----------|------|
| **Ideation** | **qcsd-ideation-swarm** | **GO / CONDITIONAL / NO-GO** | **PI/Sprint Planning** |
| Refinement | qcsd-refinement-swarm | READY / CONDITIONAL / NOT-READY | Sprint Refinement |
| Development | qcsd-development-swarm | SHIP / CONDITIONAL / HOLD | During Sprint |
| Verification | qcsd-cicd-swarm | RELEASE / REMEDIATE / BLOCK | Pre-Release / CI-CD |
| Production | qcsd-production-swarm | HEALTHY / DEGRADED / CRITICAL | Post-Release |

### Parameters

- `URL`: Website to analyze (required for URL mode)
- `OUTPUT_FOLDER`: Where to save reports (default: `${PROJECT_ROOT}/Agentic QCSD/{domain}/`)

### Unique Features

- **URL Mode**: Automated 5-tier browser cascade for live website analysis
- **HAS_VIDEO Flag**: Detects video content and recommends `/a11y-ally` follow-up
- **HTML Output**: Generates HTML reports when `html_output: true`
- **Browser Cascade**: Vibium -> agent-browser -> Playwright+Stealth -> WebFetch -> WebSearch-fallback

---

## ENFORCEMENT RULES - READ FIRST

| Rule | Enforcement |
|------|-------------|
| **E1** | You MUST spawn ALL THREE core agents (qe-quality-criteria-recommender, qe-risk-assessor, qe-requirements-validator) in Step 2. No exceptions. |
| **E2** | You MUST put all parallel Task calls in a SINGLE message. |
| **E3** | You MUST STOP and WAIT after each batch. No proceeding early. |
| **E4** | You MUST spawn conditional agents if flags are TRUE. No skipping. |
| **E5** | You MUST apply GO/CONDITIONAL/NO-GO logic exactly as specified in Step 5. |
| **E6** | You MUST generate the full report structure. No abbreviated versions. |
| **E7** | Each agent MUST read its reference files before analysis. |
| **E8** | You MUST execute Step 7 learning persistence. No skipping. |

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

1. **Flag Detection** -- `steps/01-flag-detection.md` -- Fetch URL content (browser cascade), detect all 7 flags (HAS_UI, HAS_SECURITY, HAS_UX, HAS_VIDEO, HAS_MIDDLEWARE, HAS_SAP_INTEGRATION, HAS_AUTHORIZATION)
2. **Core Agents** -- `steps/02-core-agents.md` -- Spawn qe-quality-criteria-recommender, qe-risk-assessor, qe-requirements-validator in parallel
3. **Batch 1 Results** -- `steps/03-batch1-results.md` -- Wait for core agents, extract all metrics
4. **Conditional Agents** -- `steps/04-conditional-agents.md` -- Spawn flagged conditional agents in parallel
5. **Decision Synthesis** -- `steps/05-decision-synthesis.md` -- Apply GO/CONDITIONAL/NO-GO logic
6. **Report Generation** -- `steps/06-report-generation.md` -- Generate executive summary and full report
7. **Learning Persistence** -- `steps/07-learning-persistence.md` -- Store findings to memory, save persistence record, include video follow-up recommendation
8. **Final Output** -- `steps/08-final-output.md` -- Display completion summary with all scores and follow-up recommendations

### Execution Instructions

1. Use the Read tool to load the current step file (e.g., `Read({ file_path: ".claude/skills/qcsd-ideation-swarm/steps/01-flag-detection.md" })`)
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
| qe-quality-criteria-recommender | Core (always) | requirements-validation | 1 |
| qe-risk-assessor | Core (always) | coverage-analysis | 1 |
| qe-requirements-validator | Core (always) | requirements-validation | 1 |
| qe-accessibility-auditor | Conditional (HAS_UI) | visual-accessibility | 2 |
| qe-security-auditor | Conditional (HAS_SECURITY) | security-compliance | 2 |
| qe-qx-partner | Conditional (HAS_UX) | cross-domain | 2 |
| qe-middleware-validator | Conditional (HAS_MIDDLEWARE) | enterprise-integration | 2 |
| qe-sap-rfc-tester | Conditional (HAS_SAP_INTEGRATION) | enterprise-integration | 2 |
| qe-sod-analyzer | Conditional (HAS_AUTHORIZATION) | enterprise-integration | 2 |

**Total: 9 agents (3 core + 6 conditional)**

**Note**: The Ideation swarm has 8 steps (not 9) because it has no separate final
analysis agent step. The HAS_VIDEO flag triggers a follow-up recommendation for
`/a11y-ally` but does not spawn an additional agent.

---

## Quality Gate Thresholds

| Metric | GO | CONDITIONAL | NO-GO |
|--------|-----|-------------|-------|
| Testability Score | >= 70% | 40 - 69% | < 40% |
| Risk Score | LOW/MEDIUM | HIGH (mitigatable) | CRITICAL |
| Requirements Completeness | >= 80% | 50 - 79% | < 50% |
| Quality Criteria Coverage | >= 7/10 categories | 4-6/10 categories | < 4/10 categories |

---

## Report Filename Mapping

| Agent | Report Filename | Step |
|-------|----------------|------|
| qe-quality-criteria-recommender | `02-quality-criteria.md` | 2 |
| qe-risk-assessor | `03-risk-assessment.md` | 2 |
| qe-requirements-validator | `04-requirements-validation.md` | 2 |
| qe-accessibility-auditor | `05-accessibility-audit.md` | 4 |
| qe-security-auditor | `06-security-audit.md` | 4 |
| qe-qx-partner | `07-ux-assessment.md` | 4 |
| qe-middleware-validator | `08-middleware-assessment.md` | 4 |
| qe-sap-rfc-tester | `09-sap-assessment.md` | 4 |
| qe-sod-analyzer | `10-sod-compliance.md` | 4 |
| Learning Persistence | `11-learning-persistence.json` | 7 |
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

**Quality is built in from the start, not tested in at the end. This swarm ensures
stories are viable, testable, and risk-assessed before any code is written.**
