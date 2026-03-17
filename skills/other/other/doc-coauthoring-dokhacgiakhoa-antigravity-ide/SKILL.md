---
version: 4.1.0-fractal
name: doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
---

# Doc Co-Authoring Workflow

This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a substantial writing task

**Initial offer:**
Offer the user a structured workflow for co-authoring the document. Explain the three stages:

1. **Context Gathering**: User provides all relevant context while Claude asks clarifying questions
2. **Refinement & Structure**: Iteratively build each section through brainstorming and editing
3. **Reader Testing**: Test the doc with a fresh Claude (no context) to catch blind spots before others read it

Explain that this approach helps ensure the doc works well when others read it (including when they paste it into Claude). Ask if they want to try this workflow or prefer to work freeform.

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Stage 1: Context Gathering

**Goal:** Close the gap between what the user knows and what Claude knows, enabling smart guidance later.

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Initial Questions](./sub-skills/initial-questions.md)
### 2. [Info Dumping](./sub-skills/info-dumping.md)
### 3. [Step 1: Clarifying Questions](./sub-skills/step-1-clarifying-questions.md)
### 4. [Step 2: Brainstorming](./sub-skills/step-2-brainstorming.md)
### 5. [Step 3: Curation](./sub-skills/step-3-curation.md)
### 6. [Step 4: Gap Check](./sub-skills/step-4-gap-check.md)
### 7. [Step 5: Drafting](./sub-skills/step-5-drafting.md)
### 8. [Step 6: Iterative Refinement](./sub-skills/step-6-iterative-refinement.md)
### 9. [Quality Checking](./sub-skills/quality-checking.md)
### 10. [Near Completion](./sub-skills/near-completion.md)
### 11. [Testing Approach](./sub-skills/testing-approach.md)
### 12. [Step 1: Predict Reader Questions](./sub-skills/step-1-predict-reader-questions.md)
### 13. [Step 2: Test with Sub-Agent](./sub-skills/step-2-test-with-sub-agent.md)
### 14. [Step 3: Run Additional Checks](./sub-skills/step-3-run-additional-checks.md)
### 15. [Step 4: Report and Fix](./sub-skills/step-4-report-and-fix.md)
### 16. [Step 1: Predict Reader Questions](./sub-skills/step-1-predict-reader-questions.md)
### 17. [Step 2: Setup Testing](./sub-skills/step-2-setup-testing.md)
### 18. [Step 3: Additional Checks](./sub-skills/step-3-additional-checks.md)
### 19. [Step 4: Iterate Based on Results](./sub-skills/step-4-iterate-based-on-results.md)
### 20. [Exit Condition (Both Approaches)](./sub-skills/exit-condition-both-approaches.md)
