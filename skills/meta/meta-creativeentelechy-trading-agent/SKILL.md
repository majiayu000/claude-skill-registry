# skills/meta/swarm-optimization-skill.md
---
name: "Swarm Architecture & Prompt Engineering"
description: "Principles for rewriting Agent Personas and Skill files to improve coordination and logic."
---

## Core Philosophy: "Code is Cheap, Context is King"
To fix a behavioral bug, you rarely need to change the Python code first. You usually need to change the **Agent's Instructions**.

## Debugging Agent Failure Modes
1.  **Hallucination**: The agent tries to use a tool it doesn't have.
    * *Fix*: Edit the `tools` list in `rules/X.md` OR restrict the instruction to available tools.
2.  **Looping/Indecision**: The agent keeps asking for clarification.
    * *Fix*: Add a "Default Action" protocol. (e.g., "If unsure, Default to Safe Mode").
3.  **Lazy Execution**: The agent gives a summary instead of the code.
    * *Fix*: Add a "Constraint": "You must output the full file content. No placeholders."

## Role Optimization Strategies
* **The "Separation of Concerns" Patch**:
    * If an agent is overwhelmed, split their duties.
    * *Example*: If `@Quant` is failing to log trades because it's too busy calculating signals, move the Logging duty to `@MLEng`.
* **The "Explicit Handoff" Patch**:
    * If agents are ignoring each other, hardcode the communication.
    * *Example*: Update `@Frontend`: "You strictly listen to `ws://localhost:8000`. You do not calculate your own indicators."

## Prompt Refinement Patterns
When rewriting `System Instructions` in agent files:
* **Use Negatives Constraints**: "Do NOT use `time.sleep()`."
* **Use Chain-of-Thought Triggers**: "Before answering, list 3 potential risks."
* **Use Artifact Mandates**: "Your output must always be a JSON block."