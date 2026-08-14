---
name: hedgehog-adopt-elicit
description: Use when `hedgehog-adopt` is about to add an intent for a large or under-specified unit of change on an already-adopted repo — "add billing," "support multi-tenancy," anything whose scope isn't already obvious from how the user asked for it. Runs a short, targeted clarifying pass (a handful of questions, not a shelf) and returns goal/outcome text ready for `hedgehog intent add`. Invoked by `hedgehog-adopt`'s "Adding the first (or next) change-work" step; don't run standalone, and don't run for a clear, bounded request — that goes straight to `hedgehog intent add` without this skill.
---

# Hedgehog Adopt Elicit

A short clarifying pass for one oversized or ambiguous change request on
an adopted repo, run in the same conversation already talking to the
user — never as a detached subagent, since the answers are the point of
asking. This is not `hedgehog-planning-intake`'s BMAD shelf run small:
that shelf elicits product drivers (persistence, deployment target,
integration surface) for a project that doesn't exist yet. Here the
project already exists; what's missing is only the shape of *this one
change*.

## When this runs

`hedgehog-adopt` calls this skill for one request at a time, right before
it would otherwise call `hedgehog intent add` directly. A request needs
this pass when its scope isn't already clear from how it was asked —
"add billing," "support multi-tenancy," anything where a reasonable
`--goal`/`--outcome` pair isn't obvious without more information. A
request that's already bounded ("fix the auth timeout bug", "add a rate
limit to the signup endpoint") skips this skill entirely.

## Ask, then fold the answers in

Ask a small number of targeted questions — usually three or four, never
a fixed script:

- What's actually in scope for this change, in the user's own terms.
- What's explicitly out of scope, if anything is likely to be assumed in
  by mistake.
- Any constraint the user already knows and hasn't said yet (a
  compliance requirement, an existing table or endpoint this has to work
  with, a deadline that affects how big a first cut should be).

Stop once the answers are enough to write a `--goal` and `--outcome` a
stranger could build from without guessing — don't keep probing past
that point, and don't ask about anything `hedgehog-adopt`'s own read of
the repo (commands, seams, shape) already answered.

Write the answers straight into the intent's `--goal`/`--outcome` text
when `hedgehog-adopt` calls `hedgehog intent add`. Nothing here gets
archived, written to disk, or locked — no file, no `.hedgehog/BMAD/`-style
record. If the request turns out too large for one intent, say so and
propose splitting it into more than one `hedgehog intent add` call,
each sized the way every other adopted-repo intent is: a unit of change,
not a domain module.

## Constraints

- Never elicit product-level drivers already settled by the repo's
  existence — stack, persistence, deployment target. Those are
  `hedgehog-planning-intake`'s questions for a project being built, not
  this skill's for a change to one that exists.
- Never write a file. This skill's only output is text that becomes part
  of an intent's `--goal`/`--outcome`.
- Never run for a request that's already bounded. Asking questions a
  clear request already answered is friction, not diligence.
