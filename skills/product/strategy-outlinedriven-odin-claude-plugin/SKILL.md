---
name: strategy
description: 'Use when defining product strategy, starting or redirecting a product, or repairing stale STRATEGY.md. Interviews the user with reject-by-default pushback against a drafted strategy document, then writes accepted updates back. Not for project plans, roadmaps, scheduling, or work needing no interview.'
disable-model-invocation: true
---

# Strategy: interview-driven product anchor

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants product strategy, is starting or redirecting a product, or an existing STRATEGY.md has gone stale. |
| Authority | Read-only on the repository aside from the target strategy document. Write accepted updates back to that document only. No other file is touched. |
| Side effect | Writes updates to one strategy document at the operating repository root. |
| Done | Required sections cleared the reject-by-default gate; accepted updates written back to the document and read back to confirm. |

## Inputs

Required: a drafted strategy document staged for review. If no strategy document exists, the user must draft one first or ask the skill to interview toward a first draft.

Optional: a named section argument on invocation (e.g. `/strategy approach`) targets a specific section for update.

On-demand reads (loaded at the step that needs them):

- `references/interview.md`: question bank, pushback rules, anti-pattern examples, and per-section quality bar. Read before any interview turn.
- `assets/strategy-template.md`: locked section skeleton and post-write checklist. Read when assembling or repairing the draft.

## Refusal

- Required section fails the reject-by-default gate: write nothing, say so in one line. Exit.
- No human available to interview: exit. Fabrication is worse than no strategy.
- File write or read-back mismatch: report the mismatch. Do not claim done.
- Intent cannot be pinned: announce the ambiguity. Ask the user to state intent explicitly before proceeding.

## Procedure

1. Confirm the document is staged. Resolve the operating repo root with `git rev-parse --show-toplevel`; the anchor is `$root/STRATEGY.md`. Read the document. If it does not exist, tell the user to draft one or ask for a first-draft interview. If a section argument was supplied, note which section to focus on. Done when: the document is read and the review scope is confirmed.

2. Interview the user to clarify intent and constraints based on document content. Load `references/interview.md` for the question bank, pushback rules, and per-section quality bar. For each section in the document (target problem, approach, persona, metrics, tracks, then optional milestones, non-goals, marketing): ask the opening question, apply the reject-by-default gate, push back at most twice on a weak answer, then capture the answer in the user's own words. When a section argument was supplied, re-interview only that section and preserve every untouched section. Done when: all sections in scope are re-interviewed and the gate verdict is recorded for each.

The reject-by-default gate runs in order: (1) Specific, not vague: names a concrete situation or choice, and is falsifiable. (2) Connected: approach answers the target problem; tracks serve the approach; metrics could plausibly regress. (3) The user's strategy, not the agent's: captured in the user's own language after pushback, not auto-completed.

3. Propose specific updates reflecting the interview outcome. For each section that failed the gate or changed during the interview, draft the updated text in the user's language. Present the proposed updates in chat and offer one edit round. Done when: the proposed updates are presented and the edit round is completed.

4. Write accepted updates back to the document. Read `assets/strategy-template.md` for the section skeleton and post-write checklist when assembling the final text. Set `last_updated` to today's ISO date. Write the document, then read it back to confirm it landed as intended. Done when: the file is written and the read-back matches.

## Failure modes

- Partial result: if a targeted section cannot clear the gate after two rounds of pushback, the untouched sections remain intact. No clobber.
- Non-mutation: only the target strategy document is written. The working tree is otherwise untouched.

## Output

One strategy document written to the operating repository root, read back to confirm. A clean "not enough to anchor yet" is a valid terminal output when required sections cannot clear the gate.
