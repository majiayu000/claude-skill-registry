# Code Review Skill

code-review
OVERVIEW
actor: tech-lead | mandate: Verify code quality and architecture compliance | bounds: No functional changes

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to code review to keep terminology aligned.
Load the tech-lead persona brief from .spec/agents/tech-lead.agent.md for format expectations.

LIFECYCLE TRANSITION
from: BUILT ➜ to: REVIEWED
ACCEPTS_FROM: [code-implement]
tag: [code.review] (append to story ## Lifecycle Log)

WHEN TO RUN
Code implementation complete and ready for review
Quality gates required before QA handoff
Architecture compliance verification needed
Test results require validation and review

REQUIRED INPUTS
story_id
implemented_code (from code-implement)
test_results (unit and integration test results)
review_criteria (quality standards and checklists)
MCP tooling: [Read, Write, Bash]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=code_review)>>>

EXECUTION ALGORITHM
Validate prerequisites (implemented_code, test_results). If anything missing → BLOCKED format below.
Collect evidence: code repositories, test results, quality reports.
Review code for compliance with architectural patterns.
Validate test coverage and quality of automated tests.
Check adherence to coding standards and best practices.
Verify security requirements are implemented.
Document review findings and action items.
Confirm all critical quality gates are satisfied.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== Code Review Summary ===
summary:<concise summary of review findings and quality validation>
inputs:implemented_code=<ref> test_results=<ref>
evidence:quality_gates|result=<passed/failed>|ref=<path_to_review>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END Code Review Summary ===

TRANSITION LOG TEMPLATE
[TRANSITION|code.review] by tech-lead
MODE: strict|tolerant|branch
FROM_STATE: BUILT
TO_STATE: REVIEWED
WHY:
- Code implementation complete and quality validation required
- Architecture compliance verification needed before QA
OUTPUT:
=== Code Review Summary ===
summary:Validated code quality and architecture compliance with all gates passed.
inputs:implemented_code=src/modules/ test_results=tests/reports/
evidence:quality_gates|result=passed|ref=reviews/code-review-2025-10-23.md
risks:[ ]Documentation needs updates|owner=tech-lead|mitigation=add_inline_documentation
next_steps:Prepare QA handoff and test environment setup.
=== END Code Review Summary ===
FOLLOW-UP:
- Prepare QA environment - owner=qa - due=2025-10-26

BLOCKED FORMAT
BLOCKED(missing_inputs=[implemented_code, test_results], unblock_steps=[complete_implementation, run_tests])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All critical issues must be resolved before progression.
Security vulnerabilities must be addressed immediately.
Architecture compliance is mandatory for approval.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*Code Review skill for verifying code quality and architecture compliance with structured validation.*