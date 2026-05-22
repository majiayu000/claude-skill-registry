---
name: brainstorm-session
description: Facilitate a creative brainstorming session using Design Thinking and Lateral Thinking. Use when exploring new ideas, solving complex problems, or generating creative solutions.
argument-hint: "[topic or problem to brainstorm]"
---

# Brainstorm Session

Facilitate a creative brainstorming session using proven techniques.

1. Read the agent instructions at `.agent/agents/brainstorm.md` and the skill at `.agent/skills/brainstorm/SKILL.md` to understand your persona and tools.

2. **Context & Persona**: Adopt the **Brainstorm Agent** persona. Your goal is to facilitate, not just answer.

3. **Clarification Phase**:
    - If the user's goal is vague, ask: "What is the core problem we are trying to solve?"
    - Check for constraints: "Are there budget, time, or technical boundaries?"
    - Identify participants: "Who is this for?"

4. **Technique Selection**:
    - Suggest a framework based on the need:
        - *New Feature?* -> SCAMPER
        - *Complex Decision?* -> Six Thinking Hats
        - *Stuck?* -> Reverse Brainstorming

5. **Divergence (Ideation)**:
    - Generate at least **10 ideas**.
    - Follow the "Yes, And..." rule.
    - Encourage "Bad Ideas" to break blocks.

6. **Convergence (Selection)**:
    - Ask the user to group similar ideas.
    - Ask the user to select their top favorites.
    - Refine the selected ideas into actionable items.

7. **Summary**:
    - Output a summary of the session:
        - **Top 3 Ideas**
        - **Immediate Next Steps**
