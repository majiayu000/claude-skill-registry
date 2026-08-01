---
name: skills-oleksandr-rud-aura-sdd
description: 'actor: qa | mandate: Verify end-to-end user journeys | bounds: No performance
  optimization'
---

# QA E2E Testing Skill

qa-e2e
OVERVIEW
actor: qa | mandate: Verify end-to-end user journeys | bounds: No performance optimization

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to E2E testing to keep terminology aligned.
Load the qa persona brief from .spec/agents/qa.agent.md for format expectations.

LIFECYCLE TRANSITION
from: CONTRACT_VALIDATED ➜ to: E2E_COMPLETE
ACCEPTS_FROM: [qa-contract]
tag: [qa.e2e] (append to story ## Lifecycle Log)

WHEN TO RUN
Contract validation complete and user journeys require testing
Critical workflows need end-to-end validation
Release readiness needs comprehensive testing
User experience verification required

REQUIRED INPUTS
story_id
test_scenarios (user journey and workflow definitions)
performance_baselines (SLA and performance requirements)
contract_validation (from qa-contract)
MCP tooling: [Read, Write, Bash]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=e2e_testing)>>>

EXECUTION ALGORITHM
Validate prerequisites (test_scenarios, contract_validation). If anything missing → BLOCKED format below.
Collect evidence: test scenarios, performance requirements, validation results.
Execute end-to-end tests for all critical user journeys.
Validate workflows across multiple systems and interfaces.
Test error handling and recovery scenarios.
Verify user experience and accessibility compliance.
Compare results against performance baselines and SLAs.
Document test failures and required fixes.
Generate Go/No-Go recommendation with evidence.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== E2E Validation Summary ===
summary:<concise summary of E2E testing results and Go/No-Go recommendation>
inputs:test_scenarios=<ref> performance_baselines=<ref>
evidence:e2e_tests|result=<pass_rate>|ref=<path_to_test_results>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END E2E Validation Summary ===

TRANSITION LOG TEMPLATE
[TRANSITION|qa.e2e] by qa
MODE: strict|tolerant|branch
FROM_STATE: CONTRACT_VALIDATED
TO_STATE: E2E_COMPLETE
WHY:
- Contract validation completed and user journeys require testing
- Release readiness needs comprehensive validation
OUTPUT:
=== E2E Validation Summary ===
summary:Validated all critical user journeys with performance within SLA requirements.
inputs:test_scenarios=docs/e2e/scenarios.md performance_baselines=docs/performance/sla.yaml
evidence:e2e_tests|result=95%_pass|ref=qa/e2e/test-results-2025-10-23.out performance|result=within_sla|ref=qa/performance/load-test.csv
risks:[ ]Mobile responsiveness not fully tested|owner=qa|mitigation=mobile_regression_testing
next_steps:Prepare Go/No-Go recommendation for stakeholder review.
=== END E2E Validation Summary ===
FOLLOW-UP:
- Generate stakeholder report - owner=product-ops - due=2025-10-29

BLOCKED FORMAT
BLOCKED(missing_inputs=[test_scenarios, performance_baselines], unblock_steps=[define_scenarios, establish_baselines])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All critical user journeys must be validated.
Performance must meet defined SLA requirements.
Security testing must be integrated in E2E scenarios.
Go/No-Go decisions must be evidence-based.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*QA E2E Testing skill for verifying end-to-end user journeys with comprehensive validation and Go/No-Go decisions.*