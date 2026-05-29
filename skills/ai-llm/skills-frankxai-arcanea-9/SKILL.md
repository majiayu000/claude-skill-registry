
---
name: starlight-core
description: Enhance Claude with Deep Thinking (First Principles, Systems Thinking)
---

# Starlight Core (The Pre-Frontal Cortex)

Use this skill when the user asks "/think" or when you face a complex architectural challenge.

## 1. The Reasoning Engine
You MUST pause and construct a markdown response based on the active Strategy.

**Active Strategy:** `02_PROTOCOL/STRATEGIES/FIRST_PRINCIPLES.md` (Default)
**Active Strategy:** `02_PROTOCOL/STRATEGIES/SYSTEMS_THINKING.md` (Use for Architecture)

## 2. Thinking Steps (Chain of Thought)
1.  **Read:** Load the content of the relevant Strategy File.
2.  **Analyze:** Apply the strategy's mental model to the User's problem.
    *   *First Principles:* Deconstruct to base truths. Rebuild.
    *   *Systems Thinking:* Map components, feedback loops, and emergent properties.
3.  **Synthesize:** Generate a **"Strategic Insight"** block.
4.  **Advise:** Provide a recommended course of action for the "Hands" (Coding Skills).

## 3. The Output Format
> **Thinking Process:**
> *   **Principle:** (e.g., Separation of Concerns)
> *   **Application:** (e.g., Divide the Monolith into Micro-Services)
> *   **Verdict:** Proceed with Refactor.

## 4. Benevolence Check
Before finalizing, ask: "Does this solution serve the User's long-term vision?"
