---
name: strong-edit
description: Critical editorial analysis of articles. Examines structure, argument strength, relevance, and readability. Use for substantive editing - challenging what's said and how, not just polish.
argument-hint: <file|folder>...
---

This skill is for **critical evaluation** of `$ARGUMENTS` - not polish (review-steps) or generation (flesh-out).

**Stop after each stage and have changes reviewed with user.**

> **Note**: Strong editing challenges the content itself. The agent identifies weaknesses; the developer decides what to change. Stages 0-4 are **critique only** — no edits are made to the document. Edits happen in Stage 5 after the critique is complete.
>
> See `responsibilities.md` for the full agent/developer ownership matrix.


0. **Read and identify the core argument** (developer confirms)
   - What is this article trying to say?
   - Who is the intended audience?
   - What action or understanding should readers have afterward?
   - Confirm understanding before proceeding — critique requires understanding intent

1. **Evaluate structure** (agent critiques, developer discusses)
   - Does the opening hook the reader and state the thesis?
   - Does each section serve the argument?
   - Is the logical flow sound? (premise -> evidence -> conclusion)
   - Are there structural gaps or non-sequiturs?
   - Is the conclusion earned by what precedes it?
   - Present findings and ask the developer which structural issues matter most before moving on

2. **Assess relevance and focus** (agent critiques, developer discusses)
   - Does every paragraph serve the core argument?
   - Identify tangents, digressions, or scope creep
   - Flag content that weakens the piece by diluting focus
   - Identify missing content that would strengthen the argument
   - Recommend cuts (be specific — quote what should go)
   - Ask: which of these cuts does the developer agree with? Is anything flagged actually intentional?

3. **Challenge the argument** (agent critiques, developer discusses)
   - Are claims supported by evidence?
   - Are there logical fallacies or unsupported leaps?
   - What would a skeptical reader question?
   - Are counterarguments acknowledged where needed?
   - Is the argument differentiated from obvious alternatives?
   - Ask: does the developer have evidence or context that addresses these challenges?

4. **Evaluate readability** (agent critiques, developer discusses)
   - Is the complexity appropriate for the audience?
   - Are sentences and paragraphs appropriately sized?
   - Is jargon explained or should it be avoided?
   - Does the piece maintain momentum or does it drag?
   - Are transitions clear?
   - Ask: are there readability choices that are deliberate (e.g. technical jargon for an expert audience)?

5. **Strengthen weak sections** (agent proposes edits, developer approves)
   - Based on the agreed critique from stages 1-4, now edit the document
   - Rewrite sections that aren't working
   - Tighten verbose passages
   - Sharpen vague statements into concrete claims
   - Replace weak examples with stronger ones
   - If edits introduce or modify external references, verify each URL resolves and supports the claim before presenting

6. **Final assessment** (agent leads)
   - Does the piece achieve its stated purpose?
   - What's the single biggest remaining weakness?
   - Recommendation: publish / revise further / rethink approach


## When to Use This vs Other Skills

| Document State | Use |
|----------------|-----|
| Raw notes, bullets, stream of consciousness | **flesh-out** |
| Draft with typos, incomplete sentences | **review-steps** |
| Complete draft needing critical evaluation | **strong-edit** |
| Polished draft, final check | **review-steps** |
| Finalized document needs agent-friendly restructuring | **agent-optimize** |

## Key Differences

| Aspect | review-steps | flesh-out | strong-edit |
|--------|--------------|-----------|-------------|
| Focus | Polish | Generate | Critique |
| Input | Draft with structure | Raw notes | Complete draft |
| Question | "Is this correct?" | "What should this say?" | "Does this work?" |
| Risk | Missing substance | Meaning distortion | Over-editing |
| Output | Cleaner version | Structured document | Critical assessment + revisions |

## Strong Edit Philosophy

Good editing is subtractive. The best edits often involve removing what doesn't serve the piece rather than adding more. Every word should earn its place.

Challenge the author's assumptions. If something seems unclear, it may be unclear - or wrong. Don't fix; question.

Respect the author's voice. Strong editing improves the piece; it doesn't rewrite it into a different piece. Propose changes in the author's style, not generic "good writing."
