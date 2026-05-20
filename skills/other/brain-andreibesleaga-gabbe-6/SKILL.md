---
name: self-improvement
description: Evolutionary mechanisms for the agent to rewrite its own prompts (Neuroplasticity).
context_cost: very_high
tools: [replace_file_content, task_boundary]
---

# Self-Improvement Skill

> "The software that writes itself."

## 1. Evolutionary Prompts (The Genome)
Treat the `system_prompt` and `skill.md` files as **DNA**.
- **Genes:** Individual instructions (e.g., "Always use TDD").
- **Phenotype:** The agent's actual behavior in a session.
- **Fitness Function:** Did the user accept the code? Did the tests pass?

## 2. The Mutation Cycle
When the agent encounters a novel failure or success:
1.  **Selection:** Identify the "Gene" (Prompt Instruction) responsible.
2.  **Mutation:** Rewrite the instruction.
    - *Example:* Change "Write clean code" -> "Write clean code adhering to AIRBNB style guiding."
3.  **Crossover:** Combine two successful skills into a new hybrid skill.

## 3. Recursive Self-Editing
The agent has permission to edit its own skill files.

**Protocol:**
1.  **Trigger:** "I keep failing to import this library correctly."
2.  **Analysis:** "My knowledge base is outdated."
3.  **Action:** calling `replace_file_content` on `my-language.skill.md`.
4.  **Commit:** "Updated skill memory with correct import syntax."

## 4. Safety Guardrails (Homeostasis)
To prevent "Cancer" (Runaway bad mutations):
- **Version Control:** All skill edits must be git-committed.
- **Revert:** If `success_rate` drops after a mutation, auto-revert.
- **Core Immutable:** The "Prime Directives" (Safety, Obedience) cannot be mutated.

## 5. Implementation

```python
def optimize_prompt(task_history):
    # 1. Analyze Failure
    failure_pattern = find_pattern(task_history, status="failed")
    
    # 2. Propose Mutation
    new_instruction = llm.generate_fix(failure_pattern)
    
    # 3. Simulate (Mental Sandbox)
    predicted_success = llm.simulate(new_instruction)
    
    # 4. Integrate
    if predicted_success > threshold:
        update_skill_file(new_instruction)
```
