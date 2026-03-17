---
name: review-steps
description: Structured review for polishing documents. Fixes language, improves clarity, checks structural consistency, and compares against best practice. Use when a draft has structure but needs a thorough review pass.
argument-hint: <file|folder>...
---

This skill is for **polishing** existing documents at `$ARGUMENTS` — not generating structure (flesh-out) or critiquing substance (strong-edit).

**Stop after each stage and have changes reviewed with user.**

> **Feedback loop**: When the user gives feedback on a stage, **revise that stage's output** by synthesizing the feedback with your review findings. Don't just acknowledge the feedback or apply it verbatim — incorporate it into the review work you've already done and present updated suggestions. Only move to the next stage when the user approves.

> **Note**: Review improves what exists within its structure. The agent handles mechanical checks and research; the developer holds final authority on judgment calls. When a suggestion changes meaning, ask — don't assume.
>
> See `responsibilities.md` for the full agent/developer ownership matrix.

0. **Read and understand the document** (developer confirms)
   - Read the target document and identify its current state
   - What is the document about and who is the intended audience?
   - Is this a draft that needs polish, or does it need more fundamental work (flesh-out or strong-edit instead)?
   - Confirm understanding before proceeding

1. **Review for language and consistency** (agent leads, developer approves)
   - Are there spelling, grammar, or punctuation errors?
   - Is terminology used consistently throughout?
   - Are there inconsistent patterns (e.g. mixing "e.g." and "for example")?
   - Fix issues and present changes for approval

2. **Review for conceptual clarity** (agent leads, developer approves)
   - Are there incomplete sentences or unclear phrasing?
   - Are acronyms expanded on first use?
   - Are there concepts that need further explanation for the target audience?
   - Are there terms that should be added to a glossary?
   - Ask: are any deliberately terse sections intentional (e.g. notes-to-self, placeholders)?

3. **Review vs relevant structure** (agent leads, developer approves)
   - Do other documents in the same folder or project follow a defined structure?
   - Does this document conform to that structure, or deviate for good reason?
   - Are there missing sections that the structure expects?
   - Ask: are structural deviations intentional?

4. **Review vs industry best practice** (agent assists, developer leads)
   - Web search for relevant frameworks and approaches in this domain
   - How does this document compare against industry patterns?
   - Are there gaps, missing considerations, or areas for improvement?
   - Identify unique differentiators worth preserving
   - Present findings as discussion points — the developer judges relevance and fit

5. **Tidy up** (agent leads, developer approves)
   - Add markup links for 3rd party tools and concepts referenced in the text
   - Check with the user where to update the glossary
   - Add terms that needed clarification

6. **Verify links and claims** (agent leads, developer approves)
   - Extract every URL in the document (inline links, reference links, raw URLs)
   - Fetch each URL and confirm it resolves (200, not 404/domain-not-found)
   - For each agent-sourced reference (added in Stages 4 or 5), verify the linked page supports the claim made in the document
   - Flag any URL that fails or any claim that doesn't match its source
   - Present a verification table: URL | status | source (human/agent) | notes
   - Developer decides what to fix, replace, or remove

> **Why this stage exists**: Agent-sourced references can be fabricated. A hallucinated URL with a plausible domain name will survive every other stage because reviewers (human and agent) evaluate structure, argument, and voice, not link targets. Verification must be an explicit step, not assumed.

## Pipeline Position

This skill sits in the middle of the composition pipeline: **flesh-out** -> **review-steps** -> **strong-edit** -> **agent-optimize**. Use it after a document has structure, before it needs critical evaluation.

## When to Use This vs Other Skills

| Document State | Use |
|----------------|-----|
| Raw notes, bullets, stream of consciousness | **flesh-out** |
| Draft with structure, needs polish | **review-steps** |
| Complete draft needing critical evaluation | **strong-edit** |
| Finalized document needs agent-friendly restructuring | **agent-optimize** |
