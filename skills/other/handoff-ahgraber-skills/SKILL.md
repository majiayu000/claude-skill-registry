---
name: handoff
description: "Use when ongoing work must continue in a new conversation, session, or agent with no shared history. Triggers: 'handoff', 'prepare context for next chat', 'summarize for a new session', 'continue this in another conversation'. Not for same-chat status updates or repository documentation."
---

# Handoff

Produce a transfer-ready handoff for in-progress work.

## Critical Constraints

- Assume the recipient can only see the handoff output and nothing else.
- Output one fully filled handoff payload in chat.
- Do not create a handoff file unless explicitly requested.
- Do not rely on references like "above" or "earlier in this thread".
- If information is missing, write `Unknown` and specify what is needed.

## When to Use

- Handing off work to a new conversation or agent.
- Resetting context while preserving execution continuity.
- Transferring partially complete implementation/debugging work.
- Capturing next actions before ending a session.

## When Not to Use

- Simple same-thread progress updates.
- Creating long-lived project documentation.
- Retrospectives not intended for immediate continuation.

## Workflow

1. Extract the objective, success criteria, and current status from available context.
2. Collect concrete evidence: files touched, commands run, validation status, blockers, and risks.
3. Capture decisions with rationale so the recipient understands intent and tradeoffs.
4. Fill every section of `assets/handoff-template.md`.
5. Ensure next steps are ordered and step 1 is immediately executable.
6. Return the completed template in chat for copy/paste.

## Output Rules

- Match the template section headings exactly.
- Keep statements specific and verifiable; avoid vague summaries.
- Include validation details (passed, failed, or not run).
- Include blockers with owner/dependency and concrete impact.

## Quality Checklist

- The goal and definition of done are explicit.
- Done vs. pending work is unambiguous.
- Blockers include dependency/owner and impact.
- Validation status includes what passed, failed, or was skipped.
- The first next step can be executed immediately.
- The recipient can proceed without asking for missing context.

## References

- `assets/handoff-template.md` - canonical output format.
