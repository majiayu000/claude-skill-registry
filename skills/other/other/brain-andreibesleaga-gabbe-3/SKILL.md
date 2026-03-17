---
name: neuroscience-foundations
description: Apply biological brain patterns to agent design
triggers: [neuroscience, brain, cognitive, thalamus, basal ganglia]
tags: [brain, architecture, theory]
---

# Neuroscience Foundations for Agents

## Description
This skill provides a foundational understanding of how to apply biological brain patterns to agentic software design. It covers Cortico-Thalamic loops, Basal Ganglia gating, and Neural Darwinism.

## 1. Cortico-Thalamic Loops (The Feedback/Feedforward Engine)

In the human brain, the **Thalamus** acts as a central relay station, and the **Cortex** processes information. The loop between them is essential for consciousness and attention.

### Implementation Pattern: The "Thalamic Gateway"
Instead of direct function calls between modules, route critical signals through a central "Thalamus" mediator that can:
1.  **Filter**: Only pass high-priority signals (Attention).
2.  **Breadcast**: Send important signals to multiple cortical areas (Modules) simultaneously.
3.  **Loop**: Allow the Cortex (Agent Logic) to send feedback to the Thalamus to adjust what it pays attention to next.

**Code Metaphor:**
```python
class Thalamus:
    def process_signal(self, signal):
        priority = self.calculate_salience(signal)
        if priority > THRESHOLD:
            self.broadcast_to_cortex(signal)
```

## 2. Basal Ganglia Action Selection (The Gating Mechanism)

The Basal Ganglia does not "think" of actions; it **selects** them. It inhibits all possible actions and disinhibits (releases) the most promising one based on expected reward (Dopamine).

### Implementation Pattern: The "Gited Action Selector"
Do not let your agent execute the first valid action it finds.
1.  **Generate**: The "Cortex" (LLM) generates multiple potential plans/actions.
2.  **Evaluate**: The "Basal Ganglia" (Critic/Judge) scores them based on Value (expected utility).
3.  **Select**: The mechanism releases only the highest-value action for execution.

**Key Concept:** *Go / No-Go Pathways*.
- **Direct Pathway (Go):** Facilitates the selected action.
- **Indirect Pathway (No-Go):** Suppresses competing actions.

## 3. Neural Darwinism (Selection of Somatic Groups)

Brain development and function are evolutionary processes. Groups of neurons that fuse together, wire together.

### Implementation Pattern: Evolutionary Prompts
- Maintain a "population" of system prompts or strategies.
- Track the success rate of each strategy.
- "Kill" underperforming prompts and "reproduce" (mutate) successful ones over time.

## References
- **Edelman, G. M.** (1987). *Neural Darwinism: The Theory of Neuronal Group Selection*.
- **Izhikevich, E. M.** (2007). *Dynamical Systems in Neuroscience*.
