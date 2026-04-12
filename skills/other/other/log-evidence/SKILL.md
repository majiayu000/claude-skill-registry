---
name: log-evidence
description: "Record findings from completed offline human tasks (interviews, observations, outreach) back into the canvas. The re-entry point after /handoff."
---

# Log Evidence Skill

The re-entry point after offline human work. Takes raw conversation notes, observations, or survey results and integrates them into the canvas with proper provenance.

## When to Use

- After completing a human task from `canvas/human-tasks.yml`
- When the user returns from an offline conversation and has findings to record
- When SessionStart reminds about pending human tasks and the user has completed them
- When the user pastes conversation notes or interview summaries

## Workflow

1. **Check pending tasks**:
   - Read `canvas/human-tasks.yml` for `pending_tasks`
   - List them: "You have [N] pending human task(s): [objective summaries]"
   - Ask: "Which task did you complete? Or paste your notes and I'll match them."

2. **Guided evidence capture** (if user doesn't have a filled template):
   - Who did you talk to? (role and context, not name -- privacy)
   - What did you learn? (open-ended first, let them tell the story)
   - Any direct quotes worth capturing?
   - Anything surprising or contradicting our current assumptions?
   - JTBD signals: functional job, emotional job, social job?
   - Any follow-up conversations needed?

3. **Classify the evidence** on Gilad's ladder:
   - Single conversation -> `anecdotal` (0.3)
   - 2 conversations with consistent signals -> `anecdotal` (0.3), note convergence
   - 3+ triangulated conversations -> `data-supported` (0.5-0.6)
   - Explain the classification: "One conversation is anecdotal evidence. We'd need 2-3 more to call it data-supported."

4. **Update canvas provenance**:
   - Identify the relevant canvas file and section (from the task's `canvas_refs`)
   - If the canvas entry has NO provenance object yet (early project), create one:
     ```yaml
     provenance:
       evidence_type: anecdotal  # single conversation
       evidence_sources:
         - "interview-YYYY-MM-DD-[role-descriptor]"
       source_classes:
         - external_human
       captured_at: "YYYY-MM-DDTHH:MM:SSZ"
       confidence: 0.3
     ```
   - If provenance already exists: add to `evidence_sources` and `source_classes` arrays
   - Update `evidence_type` if the new evidence strengthens it
   - Update `confidence` score with explicit reasoning
   - Update `captured_at` timestamp

5. **Update `canvas/human-tasks.yml`**:
   - Move task from `pending_tasks` to `completed_tasks`
   - Record: `completed_at`, `evidence_logged_to`, `key_findings`, `source_class: external_human`

### Task Cancellation

If the user reports a task couldn't be completed (contact unavailable, timing didn't work, etc.):
1. Ask: "Should we cancel this task or reschedule it?"
2. If cancel: move to `completed_tasks` with `source_class: cancelled` and a note explaining why
3. If reschedule: update the task's `objective` or `target_persona` if needed, keep in `pending_tasks`
4. Either way: "The evidence gap still exists. Consider `/handoff` to plan an alternative approach."

6. **Check for contradictions**:
   - Compare findings against existing canvas data
   - If findings contradict assumptions: flag clearly
     - "This contradicts [canvas section / assumption]. The user said [X] but we assumed [Y]."
     - Suggest: "Consider running `/devils-advocate` to stress-test this assumption, or update the canvas with `/canvas-update`."
   - If findings support assumptions: note the confirmation
     - "This supports [canvas section]. Confidence for [item] can increase."

7. **Recalculate confidence**:
   - Show before/after: "Diamond confidence: 0.45 -> 0.52 (added 1 external_human source)"
   - If this was the first external evidence: "First external human voice recorded. Evidence ratio improved from 0% to [X]%."

8. **Suggest next steps**:
   - If more conversations needed: "One conversation is a start. Consider `/handoff` for 1-2 more to reach triangulation."
   - If enough evidence: "Evidence looks solid for `/diamond-progress` to attempt the next transition."
   - If contradictions found: "Before progressing, resolve the contradiction. Run `/devils-advocate` or revisit the canvas."

## Canvas Output

- Updates: relevant canvas file provenance (evidence_sources, source_classes, evidence_type, confidence)
- Updates: `canvas/human-tasks.yml` (moves task to completed)
- May update: `canvas/opportunities.yml`, `canvas/user-needs.yml`, `canvas/jobs-to-be-done.yml` depending on findings

## Theory Citations

- Torres (CDH): Triangulation requirement (3+ sources for data-supported)
- Gilad (Evidence-Guided): Confidence ladder classification
- Christensen (JTBD): Functional/emotional/social capture structure
- Argyris (Double-Loop): Contradiction detection triggers assumption questioning
