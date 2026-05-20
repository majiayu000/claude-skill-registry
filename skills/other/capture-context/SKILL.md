---
name: capture-context
description: "Scan the current session and write a self-contained Session Context section into the plan file, preserving accumulated knowledge before context clearing. Use when the user asks to \"capture context\", \"save context to plan\", \"add context to plan\", \"preserve context\", \"save what we know to the plan\", or before approving a plan and clearing context."
---

# Capture Context

Make the plan file self-contained so implementation can proceed after clearing context.

## Step 1: Locate the Plan File

Find the active plan file path from the plan mode system prompt. Read the file to determine whether it already has content.

If no plan file exists, create one at the path specified by plan mode.

## Step 2: Scan the Conversation

Extract information across these categories. Skip any category where nothing relevant was discussed.

1. **Work State** — Commits made, branches created, PRs opened. Current branch and its relationship to the base branch. Build and test status. What is implemented vs. what remains.
2. **Codebase Findings** — Files explored and their relevance. Reference implementations discovered (exact file paths and line ranges). Patterns and utilities identified for reuse. Architecture or module boundaries understood.
3. **Decisions and Rationale** — Approaches chosen and why. Alternatives considered and why they were rejected. Constraints that shaped the design. User preferences expressed during discussion.
4. **Requirements Refinement** — How the original request evolved through discussion. Scope narrowed or expanded. Acceptance criteria clarified. Dependencies identified.
5. **Open Questions** — Unresolved items that need attention during implementation. Assumptions made that should be verified. Risks or unknowns flagged.

If the scan yields nothing substantial, tell the user and stop.

## Step 3: Write the Session Context Section

Write a `## Session Context` section in the plan file.

**Placement:**

- If the plan already has content, insert as the first section before implementation details
- If the plan already has a `## Session Context` section, merge new information into it. Prefer newer information when it conflicts with earlier content. Deduplicate and preserve the category structure.
- If the plan is empty, write it as the first section

**Writing guidelines:**

- Use concrete details: file paths, commit hashes, branch names, line numbers
- Keep each item to 1-3 lines. This is a reference document, not a narrative.
- Preserve reasoning: "chose X because Y" is more valuable than just "chose X"
- Include code snippets only when essential for understanding (key signatures, critical types)
- When an earlier approach was abandoned, capture only the final state. Mention the abandoned approach only if its rationale matters for implementation.

## Step 4: Verify Completeness

Re-scan the conversation with these checks:

1. **Resumability** — Could someone reading only this plan start implementing without the original conversation?
2. **Decision coverage** — Does every non-obvious choice in the implementation plan have its rationale captured?
3. **No orphaned references** — Is every file, branch, or PR mentioned in implementation steps grounded in Session Context?

Update the section if gaps are found.

## Step 5: Present Summary

Tell the user what was captured: a brief count of items per category and any notable gaps.

## Rules

- Capture knowledge, not logistics. "We debugged for 20 minutes" is irrelevant; the resulting finding is relevant.
- Omit context any developer would already know or that the implementation steps make obvious.
- Do not duplicate information already present in other plan sections.
- Do not capture secrets, credentials, or environment-specific details.
