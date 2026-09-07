---
name: grasp
description: Build a walkthrough the user works through until they can pass a quiz on it. Use when the user needs to understand something deeply and be quizzed on it.
---

Read around the thing before reading it. Write with the clarity and flow of Martin Kleppmann: smooth transitions, callouts at key concepts and edge cases. One idea per section; cut what no quiz question needs, the skippable layer excepted. Where nothing in the thing or its history says why, write that the reason is not recorded. Never guess one.

Four sections, in this order.

**Background** — what the reader must already hold: deep context marked skippable, then the slice the thing touches. For a change, the world as it was before it. How the job queue works at all is the skippable layer; the retry branch this change edits is the slice.

**Intuition** — the goal and the core idea before the thing itself. Toy data — three rows and one duplicate, not the production table — and a few drawn diagrams, never ASCII, reused through the walkthrough.

**Walkthrough** — the thing itself, literate: prose that carries its key passages, in conceptual order, never source order. The write that sets the flag, then the read that trusts it, then the test that pins the order, whatever the files sort to; the claim, then the evidence, then the exception, whatever a paper's sections do.

**Quiz** — multiple choice on the substance, as many questions as it carries. Real understanding, no gotchas: "what happens to a retry that arrives during shutdown" asks it; "which file changed" does not. Every option carries feedback on why it is right or wrong, hidden until the reader commits; a miss names the section to re-read, never a score, streak, or grade.

Default medium: one page outside the repo, `YYYY-MM-DD-<slug>.html`, one long scroll with the quiz live, opened for them (`open <path>`). Invite the reader to pass before acting on it. Passing is theirs to report, not yours to claim.

The reader lacks how it behaves, not what it is → use **toy** skill. The reader is an audience → use **land** skill. One view or one plain line would make the point → not grasp; say so and stop.
