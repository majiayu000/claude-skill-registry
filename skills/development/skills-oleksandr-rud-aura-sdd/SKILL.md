---
name: skills-oleksandr-rud-aura-sdd
description: 'actor: product-ops | mandate: Capture requirements and acceptance criteria
  | bounds: No technical implementation details'
---

# Product PRD Skill

product-prd
OVERVIEW
actor: product-ops | mandate: Capture requirements and acceptance criteria | bounds: No technical implementation details

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to PRD development to keep terminology aligned.
Load the product-ops persona brief from .spec/agents/product-ops.agent.md for format expectations.

LIFECYCLE TRANSITION
from: PRD_READY ➜ to: PRD_READY
ACCEPTS_FROM: [product-discovery]
tag: [product.prd] (append to story ## Lifecycle Log)

WHEN TO RUN
Requirements need detailed specification after discovery
Acceptance criteria must be defined with measurable outcomes
Success metrics require clarification and quantification
Stakeholder requirements need formal documentation

REQUIRED INPUTS
story_id
validated_problem (from product-discovery)
stakeholder_requirements (detailed stakeholder inputs)
acceptance_criteria (measurable success criteria)
MCP tooling: [Read, Write]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=acceptance_criteria)>>>

EXECUTION ALGORITHM
Validate prerequisites (validated_problem, stakeholder_requirements). If anything missing → BLOCKED format below.
Collect evidence: stakeholder inputs, requirement specifications, success criteria.
Define measurable acceptance criteria with clear pass/fail conditions.
Document user stories with specific, testable outcomes.
Validate success metrics are SMART (Specific, Measurable, Achievable, Relevant, Time-bound).
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== PRD Requirements ===
summary:<concise summary of requirements captured>
inputs:validated_problem=<ref> stakeholder_requirements=<ref> acceptance_criteria=<ref>
evidence:stakeholder_review|result=<approved/pending>|ref=<path_to_review>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END PRD Requirements ===

TRANSITION LOG TEMPLATE
[TRANSITION|product.prd] by product-ops
MODE: strict|tolerant|branch
FROM_STATE: PRD_READY
TO_STATE: PRD_READY
WHY:
- Requirements need detailed specification with measurable outcomes
- Acceptance criteria must be defined for implementation success
OUTPUT:
=== PRD Requirements ===
summary:Captured detailed requirements with measurable acceptance criteria and success metrics.
inputs:validated_problem=refs=discovery/summary.md stakeholder_requirements=docs/stakeholder-inputs.pdf
evidence:stakeholder_review|result=approved|ref=reviews/prd-approval-2025-10-23.md
risks:[ ]Requirements scope may exceed timeline|owner=product-ops|mitigation=prioritize_mvp_features
next_steps:Proceed with agile planning and resource allocation.
=== END PRD Requirements ===
FOLLOW-UP:
- Schedule implementation planning - owner=product-ops - due=2025-10-26

BLOCKED FORMAT
BLOCKED(missing_inputs=[validated_problem, stakeholder_requirements], unblock_steps=[complete_discovery, gather_requirements])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All acceptance criteria must be measurable and testable.
Success metrics must include specific targets and measurement methods.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*Product PRD skill for capturing detailed requirements and acceptance criteria with measurable success metrics.*