# PM Sync Skill

pm-sync
OVERVIEW
actor: product-ops | mandate: Update stakeholders and close story | bounds: No technical changes, communication only

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to stakeholder communication to keep terminology aligned.
Load the product-ops persona brief from .spec/agents/product-ops.agent.md for format expectations.

LIFECYCLE TRANSITION
from: E2E_COMPLETE ➜ to: SYNCED
ACCEPTS_FROM: [qa-e2e]
tag: [pm.sync] (append to story ## Lifecycle Log)

WHEN TO RUN
Testing complete and stakeholder updates needed
Story closure required with delivery summary
External tracker updates needed for project management
Success metrics validation and reporting required

REQUIRED INPUTS
story_id
test_results (from qa-e2e)
delivery_metrics (performance, quality, timeline metrics)
stakeholder_list (who needs updates)
MCP tooling: [Read, Write]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=stakeholder)>>>

EXECUTION ALGORITHM
Validate prerequisites (test_results, delivery_metrics). If anything missing → BLOCKED format below.
Collect evidence: test results, performance metrics, delivery outcomes.
Validate all success metrics have been achieved or exceeded.
Prepare stakeholder communication with delivery summary.
Document final outcomes and lessons learned.
Update external project management systems if required.
Draft gate artifact using the structure in ARTIFACT OUTPUT.
Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== Stakeholder Update ===
summary:<concise summary of delivery completion and stakeholder communication>
inputs:test_results=<ref> delivery_metrics=<ref> stakeholder_list=<ref>
evidence:kpi_validation|result=<met/exceeded>|ref=<path_to_metrics>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END Stakeholder Update ===

TRANSITION LOG TEMPLATE
[TRANSITION|pm.sync] by product-ops
MODE: strict|tolerant|branch
FROM_STATE: E2E_COMPLETE
TO_STATE: SYNCED
WHY:
- Testing complete and stakeholder communication required
- Story closure needed with delivery summary and outcomes
OUTPUT:
=== Stakeholder Update ===
summary:Completed stakeholder communication and story closure with successful delivery.
inputs:test_results=refs=qa/e2e/results.md delivery_metrics=docs/performance-summary.pdf
evidence:kpi_validation|result=met|ref=metrics/final-kpi-validation.csv
risks:[ ]Post-launch monitoring required|owner=product-ops|mitigation=setup_alerts
next_steps:Archive story and begin post-launch monitoring.
=== END Stakeholder Update ===
FOLLOW-UP:
- Archive project artifacts - owner=product-ops - due=2025-10-28

BLOCKED FORMAT
BLOCKED(missing_inputs=[test_results, delivery_metrics], unblock_steps=[complete_testing, gather_metrics])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All success metrics must be validated before stakeholder communication.
Stakeholder updates must include both achievements and lessons learned.
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*PM Sync skill for stakeholder communication and story closure with delivery validation and outcomes reporting.*