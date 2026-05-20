---
name: meta-prompting
description: Agents optimizing prompts for other agents (Chain of Thought, Tree of Thoughts).
role: orch-planner
triggers:
  - optimize prompt
  - better prompt
  - chain of thought
  - system prompt
  - prompt engineering
---

# meta-prompting Skill

This skill enables "Meta-Cognition": thinking about how to think.

## 1. Optimization Strategies
- **CoT (Chain of Thought)**: "Let's think step by step." (Force reasoning before answer).
- **ToT (Tree of Thoughts)**: "Generate 3 possible solutions. Evaluate each. Pick the best."
- **Few-Shot**: Provide 3 examples of "Input -> Output" to guide the model.

## 2. Dynamic Prompt Construction
Instead of static prompts, build them based on context:
1.  **Role**: "You are a world-class [Role]."
2.  **Context**: "We are building [Project]. The tech stack is [Stack]."
3.  **Constraint**: "Do not use [Forbidden Lib]. Answer in [Format]."

## 3. Self-Correction Prompts
- "Review your previous answer. Did you meet all requirements? If not, rewrite it."
- "Are there any security vulnerabilities in the code you just wrote?"

## 4. Tool Use Prompts
- "You have access to `grep`. Use it to find the definition of `User` class before guessing."
