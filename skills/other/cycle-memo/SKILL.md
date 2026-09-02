---
name: cycle-memo
description: 'Use after a build, QA pass, demo, user complaint, or abandoned attempt when the next pass needs lessons rather than code. Writes an evidence-backed memo and next-cycle plan so a fresh agent can preserve working assets, reject failed patterns, and test the right gates first. Not for changelog extraction; not for session handoff — use handoff.'
---

# Cycle memo

## Contract

| Field | Bound contract |
|---|---|
| Trigger | After a build, QA pass, demo, user complaint, or abandoned attempt when the useful output is what the next pass must learn rather than the code itself. |
| Authority | Reversible local writes: may write or refresh local docs under the project. No VCS, credential, published, deployed, or remote mutation. |
| Side effect | Writes or refreshes local docs for the cycle: a memo for lessons and a plan for next-cycle contracts, gates, and vocabulary. |
| Done | Every lesson traces to observed cycle evidence; every anti-pattern names a concrete failure mode and the gate that catches it; no lesson is a single reported case in disguise (each covers a class with specifics as evidence); a fresh agent can tell what to preserve, discard, and test first without reading the whole old session. |

## Inputs

Required: the original objective for the cycle and the final artifact it produced. Without both, lessons cannot be traced to evidence and the skill stops blocked.

Optional but cited when present: QA evidence, user complaints, screenshots, transcripts, diffs, and local planning notes.

## Procedure

1. Bound scope before mutation: extract lessons, not a changelog. File lists and effort summaries are not lessons. Do not defend the artifact; if it missed the product, say what missed. Done when: the scope is bounded to lesson extraction, not changelog or defense.
2. Gather cycle inputs: the original objective, the final artifact, QA evidence, user complaints, and any local planning notes. If the objective or final artifact is unavailable, stop and report blocked. Done when: the objective and final artifact are gathered, or the run stops blocked.
3. Separate working assets from misleading progress. List contracts, schemas, tests, services, vocabulary, and examples that earned reuse; set aside UI, panels, scaffolds, or abstractions that only looked productive. Preserve negative corpus: failed paths are training data, not deletions. Done when: working assets and misleading progress are separated, with failed paths preserved as negative corpus.
4. Generalize before recording. When feedback arrives as many specific complaints, cluster them upward into the shared root gap before writing anything. Record the root and its pattern family as the lesson; keep the specifics under it as evidence, not as lessons. A lesson that only fixes the reported case keeps the system human-in-the-loop: the same class returns anywhere a person did not point. Escalate every specific to the pattern that catches its whole class; the reporter's exact words are evidence, not the gate. Done when: every specific complaint is escalated to its pattern-level lesson with specifics kept as evidence.
5. Name each failure as an anti-pattern naming a concrete failure mode, not a mood. Done when: every failure is named as a concrete failure mode, not a mood.
6. Convert repeated or high-impact failures into quality gates for the next pass. Prefer hard gates over advice. Done when: repeated or high-impact failures have hard gates, not advice.
7. Convert vague user direction into architecture vocabulary a fresh agent can use. Done when: vague direction is converted to architecture vocabulary.
8. Write or refresh local docs for the cycle: a memo for lessons and a plan for next-cycle contracts, gates, and vocabulary. Cite evidence from the cycle for every lesson: objective, file facts, QA output, screenshots, transcripts, diffs, or user feedback. Keep provenance local; shipped artifacts must not describe their development history. If the next agent cannot act on a lesson, it is not a lesson yet. Done when: the memo and next-cycle plan are written with every lesson citing cycle evidence.
9. Verify a from-scratch agent could avoid the same failure from those docs alone: every lesson traces to observed cycle evidence; every anti-pattern names a concrete failure mode and the gate that catches it; no lesson is a single reported case in disguise; a fresh agent can tell what to preserve, discard, and test first without reading the whole old session. Done when: a from-scratch agent could avoid the same failure from the docs alone.

## Failure and recovery
- Missing evidence: if the objective or final artifact is unavailable, stop and report blocked. Do not fabricate lessons.
- Specific-as-lesson: if a lesson only fixes the reported case, escalate it to the pattern that catches its whole class before recording; otherwise discard it.
- Artifact defense: if a memo entry defends the artifact instead of naming what missed, discard that entry and re-extract.
- Non-actionable lesson: if the next agent cannot act on a lesson, convert it to a gate or discard it.
- Partial result: write only the lessons that pass the done predicate; leave unverified observations out of the memo.
- Rollback: all writes are local doc files. To undo, delete or revert the written docs. No VCS, credential, published, deployed, or remote mutation occurs.

## Output
A local memo of evidence-backed lessons, anti-patterns, and gates, plus a next-cycle plan of contracts, gates, and vocabulary. Together they let a fresh agent preserve working assets, discard misleading progress, and test the failure gates first without reading the whole old session.
