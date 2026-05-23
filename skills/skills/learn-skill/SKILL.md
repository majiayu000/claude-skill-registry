---
name: learn_skill
description: 会話履歴や作業内容から、再利用可能なエージェントスキルを生成または追記する
---

# Meta Skill (Skill Generator)

This skill analyzes the current workflow or conversation to create reusable skills.

## Instructions

1.  **Analyze Context**:
    *   Review the recent conversation history to identify repeated tasks, complex procedures, or user preferences.
    *   Determine the inputs, steps, and desired outputs.

2.  **Draft Skill**:
    *   Choose a concise name (snake_case).
    *   Write a short description.
    *   Draft the `SKILL.md` content with YAML frontmatter and clear Markdown instructions.
    *   **Important**: The `description` in the YAML frontmatter MUST be in **Japanese**.

3.  **Save**:
    *   Create a directory `.agent/skills/<skill_name>`.
    *   Write the content to `.agent/skills/<skill_name>/SKILL.md`.

4.  **Confirm**:
    *   Notify the user that a new skill has been learned.
