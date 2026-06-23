---
name: rootnode-session-handoff
description: >-
  Produces structured XML session continuation documents for multi-session
  workflows. Captures all active work streams, decisions with rationale,
  uploaded file content, conversation knowledge, artifacts, and open items
  into an ingestion-optimized handoff file. Generates closeout checklist
  covering Memory updates, build_context.md assessment, propagation items,
  and file delivery. Use when approaching context limits, wrapping up a
  session, or managing complex work across multiple conversations. Trigger
  on: "create a handoff," "session closeout," "wrap up this session,"
  "prepare for handoff," "continue next session," "save our progress," "we're
  running out of context," "context is getting long," "let's pick this up
  next time." Do NOT use for Memory optimization, context budget analysis,
  project audits, or simple conversation summaries with no continuation
  intent (for related work, use rootnode-memory-optimization or
  rootnode-context-budget if available).
license: Apache-2.0
metadata:
  author: rootnode
  version: "1.0"
  original-source: "Seed-project methodology synthesis"
---

# Session Handoff

> **Calibration:** Tier 1, Opus-primary. See repository README for model compatibility.

Produce structured session continuation documents when multi-session workflows need a clean breakpoint. The handoff file is an XML document optimized for Claude ingestion at the start of the next conversation. It captures everything the next session needs to resume work immediately — active tracks, decisions, ingested content, artifacts, and open items.

## Important

**The handoff document replaces the conversation, not supplements it.** The next session's Claude has no access to this conversation. Everything that matters must be in the handoff document or in a persistent store (Memory, knowledge files, delivered files). If it only exists in conversation, it goes in the document at full fidelity.

**Decisions without rationale are the #1 continuity failure.** A decision captured as "decided to use approach X" forces the next session to either blindly follow it or re-derive the reasoning. Always capture the why alongside the what.

**Each handoff is a clean snapshot, not an accumulating log.** When continuing from a prior handoff, the new document replaces the old one. Unresolved items carry forward explicitly. The document never grows by appending.

**XML format is non-negotiable.** The handoff document is always XML. The structural parsing reliability outweighs any readability tradeoff. Users review the XML directly before uploading; pretty-printing is acceptable but the structure must remain valid.

---

## Pipeline

### Stage 1 — Inventory

Catalog everything from the current session. Work through each category:

**Objectives.** What the session set out to accomplish. Pull from opening messages, any prior handoff document, or stated goals. If continuing from a prior handoff, reference it.

**Activity tracks.** Every concurrent work stream — active, deferred, or carried from a prior handoff. For each track: starting state, what was accomplished, current state, next steps. See references/handoff-template.md for the per-track XML structure.

**Decisions.** Every substantive decision with rationale and implications. This is the highest-value content.

**Uploaded content.** Files uploaded or loaded during the session. Capture the working understanding — relevant facts, constraints, data extracted — not raw content. Flag whether the next session needs the original re-uploaded.

**Conversation knowledge.** Information from discussion that didn't come from files. Verbal context, discovered constraints, clarifications that shaped the work. This is the most at-risk content — it exists nowhere else.

**Artifacts.** Files created, updated, or delivered. Track filenames (with `{code}_` prefix), locations, and content summaries.

**Open items.** Unresolved questions, deferred items, blockers, follow-ups.

### Stage 2 — Assess

Apply the persistence test to each inventoried item: **if the next session's Claude wouldn't have it without this document, it goes in at full fidelity. Everything else gets a reference pointer.**

Check these persistence layers:
- **Memory edits from this session** → reference, don't duplicate
- **Project knowledge files** → reference by name, don't reproduce content
- **Delivered files** → reference path and `{code}_` filename, capture only the summary
- **build_context.md** → if updated this session, note it reflects current state; if not yet updated, flag needed updates in the closeout
- **Conversation-only content** → full fidelity in the handoff

### Stage 3 — Structure

Organize the inventory into the XML handoff format. Read references/handoff-template.md for the complete schema. Apply ingestion optimization:

1. **Density over prose.** Every sentence carries information. No transitional phrases, no narrative connectors.
2. **Specific over summary.** "4-stage pipeline: Inventory → Assess → Structure → Produce" beats "decided on the pipeline." The next session needs specifics.
3. **State over history.** Where things stand, not how they got there. Exception: rejected alternatives that prevent the next session from re-proposing them.
4. **Consistent structure.** Same XML schema every time. Predictable structure enables reliable parsing.
5. **Self-contained on conversation knowledge.** Conversation-only content at full fidelity. Persistent-store content as reference pointers.
6. **Re-upload flags.** Every ingested file gets an explicit true/false.

### Stage 4 — Produce

Output the handoff document as a downloadable XML file. Then produce the closeout checklist in conversation. Read references/closeout-checklist.md for the full template and Memory update patterns.

**File naming:** `{prefix}_session_handoff_{YYYY-MM-DD}.xml` (e.g., `support_session_handoff_2026-04-13.xml`). Multiple same-day handoffs append `_a`, `_b`.

---

## Proactive vs. Requested Handoff

**Requested** (user says "wrap up," "create a handoff," etc.): Full pipeline at full depth. Complete all in-flight deliverables that can be finished quickly first. Thoroughness is the priority.

**Proactive** (context pressure at ~70%): Urgency-aware pipeline. Same stages, adjusted execution:

- Inventory prioritizes in-flight work over completed work
- Before producing, assess whether near-complete items (estimated under 10% of remaining budget) should be finished first
- Document leads with active track state and next steps; completed-work sections are compressed
- Note estimated remaining context in the header

---

## Conventions and Patterns

These are recommended patterns for production use of the Skill. They are not platform requirements — adopt them where they fit your workflow, override where they do not.

**File naming:** Use a project-specific prefix to keep handoffs identifiable across projects (e.g., `support_session_handoff_2026-04-13.xml`, `analytics_session_handoff_2026-04-13.xml`). Project-prefixed names route correctly when handoffs are stored in cross-project file systems.

**Institutional memory file:** If your project maintains a `build_context.md` or equivalent file that tracks phases, decisions, and project evolution, the closeout should always assess whether that file needs updating and specify what. Projects without an institutional memory file skip this item.

**Propagation tracking:** If the session changed system-wide facts (file counts, behavioral configurations, architectural state), the closeout should flag propagation items so downstream references stay in sync with reality. Where a propagation checklist exists in your project documentation, follow it.

**Phase-gated work:** When projects use numbered build phases, the handoff captures current phase, phase objectives, and within-phase progress. Cross-phase sessions document both phases.

**Cross-project handoffs:** Design specs or artifacts intended for another project are flagged with the target project name in the artifacts section and as explicit open items.

**Sequential methodology:** Actions in the continuation plan are sequenced, not a parallel backlog. The starter prompt identifies the single first action. Adjust to parallel sequencing if your workflow favors it.

**Terse starter prompts:** Match the user's communication style for starter prompts. Reference the handoff file, state what to resume, done. Avoid re-establishing context the handoff document already covers.

**Complete file outputs:** Always output the full XML document. Never diffs or partial content.

**Cloud storage as canonical:** When files are stored in cloud storage (Google Drive, Dropbox, OneDrive, S3, etc.) outside the conversation, reference paths/URIs in artifact tracking rather than reproducing content. Note the delivery output path explicitly so the next session can locate files.

---

## Examples

### Example 1: Single-Track Session, Clean Break

**Input:** User has been designing a Skill spec for 2 hours. "Let's wrap this up for next time."

**Actions:**
1. Inventory: one track (Skill design), decisions on pipeline stages and XML format, no uploaded files, several conversation knowledge items about design rationale.
2. Assess: design spec file delivered to outputs (reference it). Decisions and conversation knowledge are conversation-only — full fidelity.
3. Structure: one activity track at IN_PROGRESS, 3 decisions, no ingested content, 1 artifact, 2 open items.
4. Produce: XML file + closeout checklist.

**Result:** `{prefix}_session_handoff_2026-04-13.xml` with focused single-track continuation plan. Starter prompt: "Uploading handoff from yesterday's design session. Resume with [specific next step]."

### Example 2: Multi-Track with Cross-Project Handoff

**Input:** Three tracks — design spec (complete), institutional memory file update (in progress), strategic positioning decision that needs to flow to a separate project in the portfolio. "Create a handoff."

**Actions:**
1. Inventory: three tracks with mixed status. Cross-project artifact identified.
2. Assess: completed design spec file delivered (reference). Institutional memory file changes are conversation-only (full fidelity). Strategic decision needs cross-project flag.
3. Structure: Track 1 COMPLETE, Track 2 IN_PROGRESS, Track 3 DEFERRED. Artifacts section flags design spec as "cross-project → target project." Open items include strategic decision propagation to the receiving project.
4. Produce: XML file. Closeout notes Memory updates and propagation items.

**Result:** Multi-track handoff with cross-project items explicitly flagged. Continuation plan sequences institutional memory file update first, then strategic decision propagation.

### Example 3: Proactive Trigger

**Input:** Context pressure alert at ~70%. Two tracks — one at ~80% done, one at ~30%.

**Actions:**
1. Assess remaining budget. The ~80% track needs approximately 5% of remaining budget to complete — recommend finishing it.
2. Complete the near-done track. Then run full pipeline for the handoff.
3. Urgency-aware document: completed track compressed, 30%-done track at full detail.

**Result:** One fewer open item in the handoff. Starter prompt focuses on the ~30% track.

---

## When to Use This Skill

Use when:
- Approaching context window limits and need to continue in a new session
- Wrapping up a session with intent to continue the work
- Managing complex multi-track work across conversation boundaries
- Context pressure detected at ~70% and in-flight work cannot complete in remaining budget

Do NOT use when:
- Optimizing Memory layer content (use rootnode-memory-optimization if available)
- Analyzing context budget health (use rootnode-context-budget if available)
- Auditing project structure (use rootnode-project-audit if available)
- Summarizing a conversation with no continuation intent
- The session's work is fully complete with no pending items

---

## Troubleshooting

**Next session doesn't pick up where we left off:** The starter prompt is too vague or too short. It must reference the handoff file by name, state the first action, and orient Claude to the project. Check that conversation-only knowledge was captured at full fidelity, not summarized.

**Decisions get re-litigated in the next session:** Rationale is missing or too thin. Each decision needs not just the choice but the reasoning and implications. If the next session proposes an alternative that was already rejected, the handoff should have captured that rejection.

**Uploaded file content lost between sessions:** Re-upload flag was set to false when it should have been true, or the key content summary was too thin. The summary should capture every fact, constraint, or data point that influenced the session's work — not just a description of the file.

**Handoff document is too long for the next session's context:** Too much completed-work detail. Compress completed tracks to essentials (what was done, final state). The next session needs current state and next steps, not a history of completed work.

**Open items fall through the cracks:** Check that `items_carried_forward` in the continuation plan includes unresolved items from any prior handoff. Each handoff must account for the full chain, not just the current session.

**Cross-project items don't get actioned:** They need to appear in both the artifacts section (with target project flagged) and the open items section (with specific action needed). A cross-project item only in artifacts is easy to miss.
