---
name: wait-what
description: 'Use when the user says "wait, what", "the explanation is unclear", "say that again", or asks to restate the last response in plain language. Not for tasks that require source or remote-system changes.'
---

# Wait, what

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User says "wait, what", "I don't follow", "say that again", "the explanation is unclear", or "restate in plain language". |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Restates the same claim without softening; nothing touches disk. |
| Done | The claim is re-pitched with the missing frame supplied, in plain English and the project''s ubiquitous language. |

## Inputs

The trigger identifies which explanation failed. Read `CONTEXT.md` if it exists; no external file is required when it is absent. Read the per-context `CONTEXT.md` beside the relevant source when the project keeps a `CONTEXT-MAP.md`. If no `CONTEXT.md` or `CONTEXT-MAP.md` exists, use the names already in the code.

## Entry phrasings

One skill, three entry phrasings, one mechanism: re-pitch the same claim with the missing frame supplied in plain language:

- "wait, what" or "say that again": the explanation did not land. Re-pitch the same claim, preserving its substance and conclusions, and lead with the context the explanation assumed.
- "the explanation is unclear" or "context was omitted": the prior explanation skipped background, definitions, assumptions, causal links, or prerequisite steps. Re-pitch from scratch in plain language, embedding the missing context at the point where the original jumped ahead.
- "restate in plain language" or "bro": restate the last response concisely without jargon. Preserve the original meaning and add no new claims, opinions, or information beyond the source response.

All three produce one plain-language re-pitch in chat. None touches disk.

## Procedure

1. Identify the explanation that did not land: the last assistant message immediately before the trigger. Done when: the failed explanation is identified.
2. Restate the same claim, preserving its substance and conclusions. Do not soften, hedge, or replace it with an easier version. Done when: the claim is restated with substance and conclusions intact.
3. Re-pitch it: lead with the context the explanation assumed (one or two sentences on where the conversation is and what the message was answering: the gap is a missing frame, not a missing word); write in ISO 24495-1 English (short sentences, active voice, direct address, common words replacing jargon); use the project''s ubiquitous language. Done when: the claim is re-pitched with the missing frame supplied in plain English and ubiquitous language.

## Failure and recovery
- Non-converged: the user signals they do not understand after one re-pitch. Stop. Do not elaborate, restate a third time, or widen scope. The user is the authority on whether the explanation landed. Report `non-converged`.
- No prior explanation or response: if no prior assistant message exists to re-pitch or restate, stop and report that there is nothing to restate. Do not invent a prior explanation.
- Ambiguous confusion signal: if the user's indication is unclear about which part was hard to follow, ask which part of the prior explanation was unclear before re-pitching.
- Scope creep: if the re-pitch would require teaching an entire prerequisite topic, state the prerequisite boundary and offer to cover it separately. Do not widen into a tutorial.
- Clean re-pitch: keep the re-pitch free of caveats, meta-commentary, or references to the original explanation's failure.

## Output
A single re-pitched message in the conversation, in plain English with the missing context supplied.
