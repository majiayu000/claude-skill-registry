---
name: ai-native-product-refounding
description: A framework for transitioning from incremental SaaS development to an AI-native product strategy. Use this skill when you need to "refound" an existing product for the AI era, accelerate shipping velocity for AI features, or upskill a product team to be more hands-on with LLM primitives.
---

# AI-Native Product Refounding

In the AI era, product market fit must be constantly "refounded." This framework moves teams away from "blunt instruments" (long roadmaps, rigid PRDs) toward a high-velocity, hands-on approach where the product is shaped by the unique capabilities of evolving models.

## Core Principles

- **Vibes before Evals**: During the divergent "discovery" phase of an AI feature, prioritize "vibe-checking" (open-ended testing) over rigid evaluation benchmarks. Converge on formal evals only once the core "Aha!" moment is found.
- **The Hybrid Prototyper**: PMs, Engineers, and Designers must collapse silos. A PM must be "technical enough to be dangerous" and a designer must understand LLM tool-calling limits to build realistic UX.
- **Greedy Inference**: Be "intentionally wasteful" with compute for strategic insights. Spend hundreds of dollars on LLM calls to analyze sales transcripts or user data if it yields one "astute" product insight.

## The Refounding Workflow

### 1. Conduct the "Clean Slate" Audit
Before adding AI to an existing feature, ask: "If I were founding this company/feature from scratch today with current AI capabilities, what would the native experience be?"
- Identify if your current product is a "Lego kit" (useful primitives) or "Legacy weight."
- Determine if the AI should be an assistant (sidebar) or the primary agent (the default interface).

### 2. Bifurcate into Fast and Slow Thinking
Restructure the team into two distinct modes to prevent infrastructure from slowing down innovation:
- **Fast Thinking (The AI Platform Group):** Focus on near-weekly shipping. Their goal is "jaw-dropping" value and rapid experimentation.
- **Slow Thinking (The Durable Group):** Focus on infrastructure, data complexity, and scalability (e.g., high-scale data stores) that cannot be "hacked" together in a week.

### 3. Implement the "Play" Mandate
To understand what models can actually do, the team must use them "hourly."
- **Cancel Meetings:** Give the team a full day or week to do nothing but play with new AI products (e.g., Cursor, Runway, NotebookLM).
- **Project-Based Learning:** Force every PM to build a "weekend project" using AI (e.g., a personalized CRM or an automated researcher) to learn the constraints of code-gen and prompting.

### 4. Move from PRDs to Interactive Prototypes
AI behavior is non-deterministic; you cannot "word-smith" your way to a great experience in a document.
- **Show, Don't Tell:** Share Replit links or interactive prototypes instead of slide decks.
- **Inspect the "Chain of Thought":** When reviewing an AI feature, don't just look at the output. Test "unrealistic" prompts to see where the logic breaks.

## Examples

**Example 1: Refounding a Search Feature**
- **Context:** An enterprise app has a traditional keyword search.
- **Old Approach:** Create a roadmap to add semantic search and filters over three months.
- **AI-Native Refounding:** Create a "Fast Thinking" pod to build a natural language agent that crawls the web and internal data simultaneously. Use "vibe-coding" to test if the agent can answer "Which of my podcast guests have never been asked about their failures?" and iterate daily based on results.

**Example 2: Strategic Greedy Inference**
- **Context:** A PM is trying to identify why a certain segment is churning.
- **Input:** 500 sales call transcripts.
- **Application:** Use an "LLM Map-Reduce" approach. Break the transcripts into chunks, run LLM calls on each to extract "Product Gaps," then run an aggregation LLM call to synthesize the top 3 strategic shifts.
- **Output:** A high-fidelity report that would have taken a consultant weeks to produce, delivered in 30 minutes for $150 in API costs.

## Common Pitfalls

- **The "Check-the-Box" AI Feature:** Adding a basic chat sidebar that doesn't utilize the product's unique data. If the AI doesn't manipulate the core primitives of your app, it’s just a wrapper.
- **Premature Evals:** Setting up complex evaluation pipelines before you've found a "magical" user experience. This constrains creativity and slows down the "Fast Thinking" group.
- **Role Silos:** Waiting for a designer to finish a Figma file before an engineer tries the prompt. PMs should use tools like v0 or Lovable to build the "vibe" of the UI themselves first.
- **Polishing the "Golden Path":** Only testing prompts that you know work. You must try to "stump" the AI during development to find the necessary guardrails.