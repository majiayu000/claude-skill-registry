---
name: sequential-thinking
description: Break down complex problems into a step-by-step chain of thought for better reasoning
triggers: [think, reason, complex, plan, analyze, sequential]
tags: [brain, core, reasoning]
---

# Sequential Thinking Skill

## Goal
Solve complex problems by breaking them down into small, logical steps. This prevents "jumping to conclusions" and reduces hallucination.

## Steps

1. **Decompose**
   - Break the user's request into atomic components.
   - List what you know, what you assume, and what you need to find out.

2. **Plan**
   - Outline a linear sequence of steps to solve the problem.
   - Example: Research -> Hypothesis -> Limit Test -> Implement -> Verify.

3. **Execute Step-by-Step**
   - Validating each step before moving to the next.
   - If a step fails or reveals new info, update the Plan.

4. **Review & Sythesize**
   - Review your chain of reasoning. Does the conclusion logically follow?
   - Formulate the final answer based on the verified steps.

## Constraints
- Do NOT output the final answer until the thinking process is complete.
- Be explicit about uncertainty ("I am 80% confident that...").
- Use `<thinking>` blocks if supported by the interface, otherwise clear headers.
