# QA Contract Testing Skill

qa-contract
OVERVIEW
actor: qa | mandate: Validate API/event contracts | bounds: No performance testing

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to contract testing to keep terminology aligned.
Load the qa persona brief from .spec/agents/qa.agent.md for format expectations.

LIFECYCLE TRANSITION
from: READY ➜ to: CONTRACT_VALIDATED
ACCEPTS_FROM: [qa-ready]
tag: [qa.contract] (append to story ## Lifecycle Log)

WHEN TO RUN
Test environment ready and contract validation required
API contracts need compatibility and compliance verification
Event schemas require testing and validation
Integration compatibility must be confirmed

REQUIRED INPUTS
story_id
api_contracts (API specifications and schemas)
integration_specs (integration requirements and expectations)
test_environment (validated from qa-ready)
MCP tooling: [Read, Write, Bash]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=contract_testing)>>>

EXECUTION ALGORITHM
Validate prerequisites (api_contracts, test_environment). If anything missing → BLOCKED format below.
Collect evidence: API specifications, integration requirements, environment details.
Execute contract tests for all API endpoints and interfaces.
Validate request/response schemas against specifications.
Test error handling and edge case scenarios.
Verify event schemas and message formats.
Document contract violations and compatibility issues.
Validate all contracts meet compliance requirements.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== Contract Validation Summary ===
summary:<concise summary of contract testing results and compliance>
inputs:api_contracts=<ref> integration_specs=<ref>
evidence:contract_tests|result=<passed/failed>|ref=<path_to_test_results>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END Contract Validation Summary ===

TRANSITION LOG TEMPLATE
[TRANSITION|qa.contract] by qa
MODE: strict|tolerant|branch
FROM_STATE: READY
TO_STATE: CONTRACT_VALIDATED
WHY:
- Test environment ready and API contracts require validation
- Integration compatibility must be confirmed before E2E testing
OUTPUT:
=== Contract Validation Summary ===
summary:Validated all API contracts and integration points with full compliance.
inputs:api_contracts=docs/api/specs.yaml integration_specs=docs/integration/requirements.md
evidence:contract_tests|result=100%_pass|ref=qa/contract-test-results-2025-10-23.csv
risks:[ ]Rate limiting not yet tested|owner=qa|mitigation=add_load_testing
next_steps:Proceed with end-to-end user journey validation.
=== END Contract Validation Summary ===
FOLLOW-UP:
- Schedule E2E testing - owner=qa - due=2025-10-28

BLOCKED FORMAT
BLOCKED(missing_inputs=[api_contracts, test_environment], unblock_steps=[finalize_contracts, complete_environment_setup])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All contract violations must be resolved before progression.
Security testing must be included in contract validation.
Backward compatibility must be verified and documented.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*QA Contract Testing skill for validating API/event contracts for compatibility and compliance.*