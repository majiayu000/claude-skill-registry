# Context Snapshot Skill

context.snapshot
OVERVIEW
actor: architect|product-ops|tech-lead|qa | mandate: Capture current status and manage log organization | bounds: No content deletion, only organization

ORIENTATION
Confirm .spec/constitution.md for current architecture and delivery guardrails.
Review .spec/glossary.md entries relevant to context management to keep terminology aligned.
Load the relevant persona brief from .spec/agents/<persona>.agent.md for format expectations.

LIFECYCLE TRANSITION
from: ANY ➜ to: SAME
ACCEPTS_FROM: []
tag: [context.snapshot] (append to story ## Lifecycle Log)

WHEN TO RUN
Handoff between personas required (snapshot operation)
Work stalling and checkpoint needed (snapshot operation)
Status checkpoint required before transition (snapshot operation)
Context preservation needed for later reference (snapshot operation)
Lifecycle Log exceeds threshold (compact operation)
Content compaction needed for usability (compact operation)
Navigation becomes difficult due to log volume (compact operation)

REQUIRED INPUTS
story_id
operation_type (snapshot/compact)
current_context (status and progress information - for snapshot)
compact_level (light/medium/aggressive - for compact)
handoff_reason (reason for snapshot - for snapshot)
MCP tooling: [Read, Write]

CONTEXT PACK
<<story.current_state>>
<<personas.active_assignments>>
<<recent_transition_log>>
<<<GLOSSARY(term=context_snapshot)>>>

EXECUTION ALGORITHM
Validate prerequisites (story_id, operation_type). If anything missing → BLOCKED format below.
Based on operation_type, execute appropriate workflow:

### SNAPSHOT OPERATION
Validate additional prerequisites (current_context, handoff_reason). If missing → BLOCKED.
Collect evidence: current state, completed work, blockers, decisions.
Document current status and progress comprehensively.
Capture unresolved questions and decision points.
Identify blockers and risks with current status.
Document handoff information and next steps.
Create clear snapshot for reference by next agent.

### COMPACT OPERATION
Validate additional prerequisites (compact_level). If missing → BLOCKED.
Analyze current Lifecycle Log size and entry patterns.
Identify key transitions and decisions to preserve.
Create archive section with detailed historical entries.
Summarize critical information in main Lifecycle Log.
Maintain audit trail with references to archived content.
Document compaction decisions and archive location.

Append the TRANSITION LOG entry to the story's ## Lifecycle Log, matching persona tone.
Update glossary/constitution if new terminology or workflows were introduced.

ARTIFACT OUTPUT
=== Context Management ===
summary:<concise summary of context management actions and outcomes>
inputs:operation_type=<type> current_context=<ref> compact_level=<ref> handoff_reason=<ref>
evidence:<operation_result>|result=<status>|ref=<path_to_artifact>
risks:[ ]<risk_description>|owner=<persona>|mitigation=<action>
next_steps:<follow-up needed or n/a>
=== END Context Management ===

TRANSITION LOG TEMPLATE

### SNAPSHOT OPERATION
[TRANSITION|context.snapshot] by <persona>
MODE: tolerant
FROM_STATE: <current_state>
TO_STATE: SAME
WHY:
- Handoff to <next_persona> requires context preservation
- Work stalling requires status checkpoint
OUTPUT:
=== Context Management ===
summary:Captured current status and context for seamless handoff continuation.
inputs:operation_type=snapshot current_context=refs=summary#current-state handoff_reason=persona_transition
evidence:status_validation|result=ready_for_handoff|ref=context/snapshot-2025-10-23.md
risks:[ ]Unresolved technical question|owner=<next_persona>|mitigation=research_needed
next_steps:Continue work with <next_persona> using captured context.
=== END Context Management ===
FOLLOW-UP:
- Resume work with <next_persona> - owner=<next_persona> - due=immediate

### COMPACT OPERATION
[TRANSITION|context.snapshot] by <persona>
MODE: tolerant
FROM_STATE: <current_state>
TO_STATE: SAME
WHY:
- Lifecycle Log exceeded threshold requiring compaction
- Task file navigation needed improvement for usability
OUTPUT:
=== Context Management ===
summary:Compacted Lifecycle Log with 25 entries archived to maintain usability.
inputs:operation_type=compact compact_level=medium current_context=refs=summary#current-state
evidence:log_size|result=25_entries_compacted|ref=archive/2025-10-23-compact.md
risks:[ ]Historical context depth reduced|owner=<persona>|mitigation=detailed_archive_indexing
next_steps:Continue with current task using streamlined log.
=== END Context Management ===
FOLLOW-UP:
- Monitor log growth - owner=<persona> - due=ongoing

BLOCKED FORMAT
BLOCKED(missing_inputs=[story_id, operation_type, <operation_specific_inputs>], unblock_steps=[identify_story, specify_operation, <operation_specific_steps>])

GUARDRAILS
Keep entries <=120 chars per line for CLI readability.
All decisions and blockers must be clearly documented.
Next steps must be specific and actionable.
Context must be sufficient for independent continuation (snapshot).
Never delete content, only reorganize and archive (compact).
Maintain complete audit trail with archive references (compact).
Preserve all decisions and transition outcomes (compact).
Update .spec/glossary.md if you introduce new terms, channels, or artifacts.

---

*Enhanced Context Snapshot skill for capturing current status and managing log organization while preserving audit trails and essential information.*