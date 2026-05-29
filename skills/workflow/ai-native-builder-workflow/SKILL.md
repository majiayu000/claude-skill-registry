---
name: ai-native-builder-workflow
description: A complete end-to-end framework for non-technical product managers to build and ship software using AI coding agents. Use this when starting a side project, building a prototype, or automating internal tools without an engineering team.
---

This workflow enables non-technical individuals to build production-ready applications by orchestrating AI models as a technical co-founder, developer, and QA lead.

## Core Principles

- **The CTO Persona**: Treat the AI as a Technical Owner. Instruct it to challenge your ideas, avoid "people-pleasing" (sycophancy), and own the technical architecture while you own the problem and user experience.
- **Exposure Therapy**: Gradually move from simple chat interfaces (ChatGPT/Claude Projects) to dedicated builders (Bolt/Lovable) to pro-level IDEs (Cursor/Claude Code).
- **Planning over Vibe-ing**: Never let the AI start coding until a markdown plan is finalized. Eager coding leads to architectural debt and complex bugs.

## The /Command Workflow

Implement these custom prompts as reusable `/commands` within your AI coding environment (Cursor, Claude Code, or IDE system prompts).

### 1. Capture: `/create-issue`
**Purpose**: Quickly capture bugs or features without breaking development flow.
- **Instruction**: Tell the AI to stop what it's doing and summarize the thought into a specific format.
- **Format**: TLDR, Current State, Expected Outcome, and Priority.
- **Integration**: Use MCP (Model Context Protocol) to automatically create a ticket in Linear or GitHub.

### 2. Deep Dive: `/exploration-phase`
**Purpose**: Force the AI to understand the technical implications before writing code.
- **Process**: Provide the issue ID as context.
- **Requirement**: The AI must analyze the codebase and ask 5-10 clarifying questions regarding data models, UX, edge cases, and architectural impact.
- **Goal**: Identify "Key Areas" of the code that will be affected.

### 3. Strategy: `/create-plan`
**Purpose**: Generate a source-of-truth roadmap for the build.
- **Structure**: Create a `plan.md` file including:
  - **TLDR**: High-level goal.
  - **Critical Decisions**: Tech stack choices or logic changes.
  - **Task Checklist**: Step-by-step implementation guide with status checkboxes (`[ ]`).
- **Review**: Manually approve this plan before moving to execution.

### 4. Execute: `/execute`
**Purpose**: Move the plan into code.
- **Process**: Feed the `plan.md` to the coding agent (e.g., Cursor Composer or Claude Code).
- **Control**: Execute one task at a time to ensure the UI and logic remain stable.

### 5. Multi-Model QA: `/peer-review`
**Purpose**: Catch errors that a single model might miss by creating "model friction."
- **Technique**: Have different LLMs review the same code.
- **Workflow**:
  1. Run `/review` with Claude to find its own mistakes.
  2. Copy the code into a different model (e.g., GPT-4o or Gemini 1.5 Pro).
  3. Use the `/peer-review` prompt: *"You are the dev lead. Other team leads found these issues [paste issues]. Either fix them or explain why they are not real issues based on our specific context."*
- **The "Fight"**: Allow the models to argue technical points until a consensus is reached.

### 6. Continuous Learning: `/learning-opportunity`
**Purpose**: Build your technical intuition while building.
- **Prompt**: *"I am a technical PM in the making. Explain this specific technical decision or error using the 80/20 rule. Focus on architecture and mental models, not just syntax."*

## Maintaining the "Harness"

To keep the AI effective as the project grows, you must maintain its documentation.

- **`/update-docs`**: After every major feature, have the AI update the project’s documentation (e.g., `architecture.md`, `api-routes.md`) so the next agent session has full context.
- **Post-Mortems**: When the AI makes a mistake, ask: *"What in your system prompt or current documentation caused this error?"* Update the system prompt to prevent that specific category of error from recurring.

## Examples

**Example 1: Feature Ideation**
- **Context**: You want to add a drag-and-drop "fill-in-the-blank" quiz type to a learning app.
- **Input**: `/create-issue I want a drag and drop quiz type. 30% of tests should have this. 6 potential answers, 2 blanks.`
- **Application**: AI creates a Linear ticket. You then run `/exploration-phase` where the AI asks how the state should be handled if a user drags the same answer to two different spots.
- **Output**: A comprehensive technical plan that accounts for drag-and-drop library dependencies before any code is written.

**Example 2: Bug Resolution**
- **Context**: The app crashes only on mobile Safari.
- **Input**: Run the code through GPT-4o for a second opinion.
- **Application**: GPT identifies a CSS incompatibility. Use `/peer-review` to feed that feedback back to Claude.
- **Output**: Claude acknowledges the oversight and provides a cross-browser compatible fix.

## Common Pitfalls

- **The Sycophancy Trap**: The AI will often agree with your bad ideas just to be helpful. Explicitly prompt it to be a "Cantankerous CTO" who protects the codebase.
- **The "Slop" Accumulation**: Letting the AI generate thousands of lines without review. Use a "deslop" mindset: ask the AI to refactor for conciseness and remove redundant comments or unused imports after a feature is done.
- **Skipping the /review**: Assuming the code works because it "looks" right. Always run the code locally and trigger a `/review` from a competing model.