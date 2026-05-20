---
name: flesh-out
description: Transform raw/crude document drafts into structured content. Use when a document is a skeleton of ideas, notes, or stream-of-consciousness that needs generative expansion rather than review polish.
argument-hint: <file|folder>...
---

This skill is for **generative** work on crude/raw content at `$ARGUMENTS` - not polishing drafts.

**Stop after each stage and have changes reviewed with user.**

> **Note**: The developer's raw content captures intent. The agent expands and structures but must preserve the developer's meaning. When uncertain about intent, ask - don't assume.
>
> See `responsibilities.md` for the full agent/developer ownership matrix.


0. **Extract core ideas** (developer leads)
   - Read the raw content and identify the key concepts
   - List what the developer appears to be saying (don't fix typos yet)
   - Confirm understanding with developer before proceeding
   - Identify gaps: "You mention X but don't explain Y - should I research this?"

1. **Research and expand** (agent leads with approval)
   - Web search for external concepts if applicable
   - Find industry terminology for rough ideas
   - Identify related work the developer may want to reference
   - Propose expansions - developer approves what to include
   - **Verify every reference before presenting**: fetch URLs, confirm they resolve, confirm the source supports the claim. Do not present unverified links to the developer.

2. **Structure the content** (agent leads with approval)
   - Determine appropriate document structure (based on template if available)
   - Organize ideas into logical sections
   - Create hierarchy (headers, sub-sections)
   - Add diagrams or tables where relationships exist

3. **Polish language** (agent leads with approval)
   - Fix spelling, grammar, terminology
   - Expand acronyms on first use
   - Ensure consistent usage throughout
   - Add links to external references (verify each URL resolves before adding)

4. **Tidy up** (agent leads with approval)
   - Check with the user where to update the glossary
   - Add terms that needed clarification
   - Update references with new links

## When to Use This vs Other Skills

| Document State | Use |
|----------------|-----|
| Raw notes, bullet points, stream of consciousness | **flesh-out** |
| Typos, incomplete sentences, but has structure | **review-steps** |
| Structured but missing sections | **flesh-out** (or discuss scope first) |
| Complete draft needing polish | **review-steps** |
| Complete draft needing critical evaluation | **strong-edit** |

## Key Difference from Review

**Review** improves what exists within its structure.
**Flesh-out** creates structure from raw ideas.

Review a skeleton -> correct but incomplete document.
Flesh-out a skeleton -> complete document.
