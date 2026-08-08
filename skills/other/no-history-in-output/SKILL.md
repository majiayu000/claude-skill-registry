---
name: no-history-in-output
description: Apply whenever writing or updating a project-facing document — root CLAUDE.md, `.hedgehog/core-design.md`, specs, READMEs, or similar. Ensures the file reads as a clean, current, as-is snapshot rather than a log of edits or decisions. Applies on first generation and on every later revision, including "update," "rewrite," or "clean up" requests.
---

# No History in Output

Project-facing documents describe the current state of the thing, not the
process that produced it.

## Rules

- Never include labels like "(unchanged)", "(updated)", "(new)",
  "(revised)", or similar edit-tracking annotations in headings or body
  text.
- Never narrate the discussion that led to a decision (e.g. "we
  considered X but decided against it," "originally this was Y, now it's
  Z," "per your feedback...").
- Never include changelogs, version history, "what changed" sections, or
  meta-commentary about the conversation, unless the user explicitly
  asks for a changelog as a deliverable in its own right.
- Write every section as a plain statement of fact about the current
  design/plan/content, as if writing it fresh with full knowledge of the
  final decision — not as a diff against a prior version.
- If a section documents a resolved tradeoff or an intentional design
  choice, state the choice and its rationale plainly (e.g. "X is an
  accepted tradeoff because..."), without referencing that alternatives
  were debated or rejected earlier in conversation.
- An "update this doc" request re-derives a clean as-is document — it
  does not layer edit notes onto the previous version.

## When NOT to apply

- The user explicitly asks for a changelog, revision history, or "show
  me what changed."
- The document's entire purpose is to record a process over time — a
  friction log entry (`hedgehog friction add`), a commit message, or
  meeting notes. Those describe what happened and when on purpose.
