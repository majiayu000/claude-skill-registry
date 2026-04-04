# QA Ready Skill

qa-ready
OVERVIEW
actor: qa | mandate: Prepare test environment and fixtures | bounds: No test execution yet

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to QA preparation to keep terminology aligned.
Load the qa persona brief from .spec/agents/qa.agent.md for format expectations.

LIFECYCLE TRANSITION
from: REVIEWED ➜ to: READY
ACCEPTS_FROM: [code-review]
tag: [qa.ready] (append to story ## Lifecycle Log)

WHEN TO RUN
Code review complete and environment setup required
Test fixtures and data needed for comprehensive testing
Test environment validation required before test execution
QA resources and tools need preparation

REQUIRED INPUTS
story_id
reviewed_code (from code-review)
test_requirements (testing scope and criteria)
environment_specifications (test environment needs)
MCP tooling: [Read, Write, Bash]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=test_environment)>>>

EXECUTION ALGORITHM
Validate prerequisites (reviewed_code, test_requirements). If anything missing → BLOCKED format below.
Collect evidence: review reports, test specifications, environment requirements.
Prepare test environment with required configurations.
Create test fixtures and sample data for comprehensive testing.
Validate test tools and frameworks are properly configured.
Verify environment isolation and data consistency.
Document test environment setup and configurations.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== QA Readiness Summary ===
summary:<concise summary of test environment preparation and validation>
inputs:reviewed_code=<ref> test_requirements=<ref>
evidence:environment_validation|result=<ready/not_ready>|ref=<path_to_validation>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END QA Readiness Summary ===

TRANSITION LOG TEMPLATE
[TRANSITION|qa.ready] by qa
MODE: strict|tolerant|branch
FROM_STATE: REVIEWED
TO_STATE: READY
WHY:
- Code review complete and test environment preparation required
- Test fixtures needed for comprehensive validation
OUTPUT:
=== QA Readiness Summary ===
summary:Prepared test environment with fixtures and validated tool configurations.
inputs:reviewed_code=refs=code-review/summary.md test_requirements=docs/testing-scope.pdf
evidence:environment_validation|result=ready|ref=qa/environment-validation-2025-10-23.md
risks:[ ]Test data refresh schedule needed|owner=qa|mitigation=automated_data_refresh
next_steps:Begin contract testing and API validation.
=== END QA Readiness Summary ===
FOLLOW-UP:
- Start contract testing - owner=qa - due=2025-10-27

BLOCKED FORMAT
BLOCKED(missing_inputs=[reviewed_code, test_requirements], unblock_steps=[complete_review, define_test_scope])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
Test environment must be isolated from production systems.
All test fixtures must be version controlled and documented.
Environment validation must include security verification.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*QA Ready skill for preparing test environment and fixtures for comprehensive testing validation.*