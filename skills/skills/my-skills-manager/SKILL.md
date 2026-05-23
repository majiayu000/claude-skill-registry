---
name: my-skills-manager
description: Manages personal skills by adding new skills to the my-skills directory or updating existing skills based on user context. Use when user requests to add skills to "マイスキル" (my skills) or update existing personal skills.
---

# My Skills Manager

## Functionality

### Adding Skills
When user says "マイスキルに追加" (add to my skills):
1. Create a new directory with an appropriate name in the same directory
2. Create a SKILL.md file following the Agent Skills specification

### Updating Skills
When user says "マイスキルを更新" (update my skills):
1. Analyze context to identify which skill needs updating
2. If the target skill is unclear, present options 1, 2, 3 to the user
3. Wait for user selection before proceeding with the update

## Implementation Notes
- Always follow the Agent Skills specification format with proper frontmatter
- Use English for skill content body
- Include required frontmatter fields: name, description
- Consider optional fields like metadata, compatibility when relevant
- Keep skill descriptions clear and actionable for AI agents