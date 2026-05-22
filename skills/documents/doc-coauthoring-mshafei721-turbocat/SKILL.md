---
name: doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
---

# Doc Co-Authoring Workflow

This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a substantial writing task

## Three Stages

### Stage 1: Context Gathering

**Goal:** Close the gap between what the user knows and what Claude knows.

**Initial Questions:**
1. What type of document is this?
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context?

Encourage the user to dump all context they have: background, discussions, why alternatives aren't being used, organizational context, timeline, technical dependencies.

### Stage 2: Refinement & Structure

**Goal:** Build the document section by section through brainstorming, curation, and iterative refinement.

For each section:
1. Ask clarifying questions about what to include
2. Brainstorm 5-20 options
3. User indicates what to keep/remove/combine
4. Draft the section
5. Refine through surgical edits

Start with whichever section has the most unknowns.

### Stage 3: Reader Testing

**Goal:** Test the document with a fresh perspective to catch blind spots.

1. Predict reader questions
2. Test with a sub-agent (no context bleed)
3. Run additional checks for ambiguity, false assumptions, contradictions
4. Fix any gaps identified

## Tips for Effective Guidance

- Be direct and procedural
- Always give user agency to adjust the process
- Don't let context gaps accumulate
- Quality over speed
