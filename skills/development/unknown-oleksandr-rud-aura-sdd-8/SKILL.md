# Code Implementation Skill

code-implement
OVERVIEW
actor: tech-lead | mandate: Build feature with automated tests | bounds: No architecture changes

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to code implementation to keep terminology aligned.
Load the tech-lead persona brief from .spec/agents/tech-lead.agent.md for format expectations.

LIFECYCLE TRANSITION
from: PLANNED ➜ to: BUILT
ACCEPTS_FROM: [agile-planning, architect-plan]
tag: [code.implement] (append to story ## Lifecycle Log)

WHEN TO RUN
Implementation plan approved with architecture guidance
Development resources allocated and ready for execution
Backlog items sequenced and prioritized
Technical requirements clearly defined

REQUIRED INPUTS
story_id
architecture_plan (from architect-plan)
implementation_requirements (from agile-planning)
development_resources (team allocation)
MCP tooling: [Read, Write, Edit, Bash]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=implementation)>>>

EXECUTION ALGORITHM
Validate prerequisites (architecture_plan, implementation_requirements). If anything missing → BLOCKED format below.
Collect evidence: architecture specifications, implementation guides, resource assignments.
Implement core functionality following architectural patterns.
Create and execute automated tests for critical paths.
Validate code compliance with quality standards.
Document implementation decisions and trade-offs.
Verify test coverage meets defined thresholds.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== Implementation Summary ===
summary:<concise summary of implementation completion and test results>
inputs:architecture_plan=<ref> implementation_requirements=<ref>
evidence:unit_tests|result=<passing_percentage>|ref=<path_to_results>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END Implementation Summary ===

TRANSITION LOG TEMPLATE
[TRANSITION|code.implement] by tech-lead
MODE: strict|tolerant|branch
FROM_STATE: PLANNED
TO_STATE: BUILT
WHY:
- Implementation planning complete with architecture guidance
- Development resources allocated and ready for execution
OUTPUT:
=== Implementation Summary ===
summary:Implemented core functionality with automated tests and architecture compliance.
inputs:architecture_plan=refs=arch/plan.md implementation_requirements=docs/backlog.md
evidence:unit_tests|result=95%_passing|ref=tests/unit/results.out code_coverage|result=87%|ref=coverage/report.html
risks:[ ]Performance under load not yet validated|owner=qa|mitigation=load_testing_before_release
next_steps:Request code review and prepare QA handoff.
=== END Implementation Summary ===
FOLLOW-UP:
- Schedule code review - owner=architect - due=2025-10-25

BLOCKED FORMAT
BLOCKED(missing_inputs=[architecture_plan, implementation_requirements], unblock_steps=[complete_architecture, finalize_planning])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All code must follow established architectural patterns.
Automated tests required for all critical paths.
Test coverage must meet or exceed defined thresholds.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*Code Implementation skill for building features with automated tests and architecture compliance.*