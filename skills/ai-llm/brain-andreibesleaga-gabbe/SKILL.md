---
name: learning-adaptation
description: Mechanisms for In-Context Reinforcement Learning, Meta-Learning, and Neuroplasticity.
context_cost: high
tools: [replace_file_content, write_to_file]
---

# Learning & Adaptation Skill

> "Neurons that fire together, wire together." (Hebbian Learning)

## 1. Synaptic Plasticity (Rewiring)
This skill allows the system to "rewire" itself based on experience.
- **Potentiation (Strengthening):** If a prompt/tool works well, save it to a "Best Practices" bank.
- **Depression (Weakening):** If a tool fails often, add a warning or deprecate it.

## 2. Meta-Learning (Learning to Learn)
The agent should not just learn *information*; it should learn *strategies*.

### Strategy Reflection Loop
After a task is complete, perform a "Post-Mortem":
1.  **Observation:** "I hallucinated a library name."
2.  **Hypothesis:** "I didn't check the docs first."
3.  **New Rule:** ("ALWAYS check docs for library imports.")
4.  **Storage:** Save to `system_rules.md`.

## 3. Reinforcement Learning (RL) Integration
- **Actor:** The Agent performing the task.
- **Critic:** A separate module (or human) that scores the outcome (Reward).
- **Policy Update:** Update the **Few-Shot Context**.
    - *Old:* Zero-shot prompt.
    - *New:* Prompt + 3 Successful Examples from `learning-adaptation` bank.

## 4. Episodic Consolidation (Dreaming)
Biological brains consolidate short-term memories into long-term structures during sleep.

### Implementation: The "Nightly Build"
1.  **Compress:** Run a summarization job on the day's logs.
2.  **Extract:** Extract key facts and successful code patterns.
3.  **Consolidate:** Update the Knowledge Graph and clear the raw logs.

## References
- **Sutton, R. S., & Barto, A. G.** (2018). *Reinforcement Learning: An Introduction*.
- **Hebb, D. O.** (1949). *The Organization of Behavior*.
