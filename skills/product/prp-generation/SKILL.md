---
name: prp-generation
description: Generate a Product Requirements Prompt (PRP) from a feature description. Use when starting work on a new feature.
---

# PRP Generation

Generate a Product Requirements Prompt (PRP) in Markdown format.

## When to Use This Skill

Use this skill when:
- Starting work on a new feature
- Converting a feature idea into a detailed specification
- Creating documentation suitable for a junior developer to implement

## Initial Response Rule

**When this skill is invoked, ALWAYS start by asking the user to
describe their feature. DO NOT jump to clarifying questions until
they have provided an initial description.**

## Process

**CRITICAL: Follow this process EXACTLY in sequence. DO NOT SKIP AHEAD!**

### Step 1: Wait for Initial Feature Description

- **STOP AND WAIT** for the user to describe the feature
- The user MUST provide at least a brief description FIRST
- DO NOT ask any questions until the user has provided this initial description
- Simply acknowledge and ask: "What feature would you like to create a PRP for?"

### Step 2: Ask Clarifying Questions

**ONLY AFTER** the user provides their feature description:

- Ask 3-5 FOCUSED clarifying questions based on what's unclear
- DO NOT ask all possible questions - only what's needed
- Provide options in letter/number lists for easy selection
- Goal: understand the "what" and "why", not the "how"

**Example questions:**

- **Problem/Goal**: "What problem does this feature solve for the user?"
- **Target User**: "Who is the primary user of this feature?"
- **Core Functionality**: "Can you describe the key actions a user should be able to perform?"
- **Acceptance Criteria**: "How will you know when this feature is successfully implemented?"
- **Scope/Boundaries**: "Are there specific things this feature should NOT do?"
- **Edge Cases**: "Are there potential edge cases or error conditions to consider?"

### Step 3: Generate PRP

Based on the initial description AND the user's answers to clarifying questions,
generate a PRP using the structure below. Ensure it's suitable for a junior
developer to understand.

### Step 4: Save PRP

Save the generated document as `.ai/[feature-name]/prp.md`
Confirm with the user that the PRP has been saved

## PRP Structure

The generated PRP should include:

1. **Introduction/Overview**: Briefly describe the feature and the problem it solves
2. **Goals**: List the specific, measurable objectives
3. **User Stories**: Detail user narratives describing feature usage and benefits
4. **Functional Requirements**: Specific functionalities the feature must have (numbered)
5. **Non-Goals (Out of Scope)**: What this feature will NOT include
6. **Design Considerations** (Optional): UI/UX requirements, mockups, component styles
7. **Technical Considerations** (Optional): Constraints, dependencies, integration points
8. **Success Metrics**: How success will be measured
9. **Open Questions**: Remaining questions needing clarification

## Target Audience

Assume the primary reader is a **junior developer**. Therefore:
- Requirements should be explicit and unambiguous
- Avoid jargon where possible
- Provide enough detail for understanding purpose and core logic

## Output Format

- **Format**: Markdown (`.md`)
- **Location**: `.ai/[feature-name]/prp.md`
- **Line width**: Wrap at 78 columns

## Final Instructions

1. Do NOT start implementing the PRP
2. Make sure to ask the user clarifying questions
3. Take the user's answers and improve the PRP
