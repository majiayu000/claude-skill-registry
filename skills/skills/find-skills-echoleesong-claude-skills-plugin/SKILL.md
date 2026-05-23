---
name: find-skills
description: Helps users discover and install capabilities from the open agent skills ecosystem. Use when users ask "how do I do X" for specialized tasks, request "find a skill for X", want to extend agent capabilities, or need help with specific domains (testing, design, deployment, etc.).
---

# Find Skills

This skill helps users discover and install capabilities from the open agent skills ecosystem.

## When to Use

Trigger this when users:
- Ask "how do I do X" or "can you do X" for specialized tasks
- Request "find a skill for X"
- Want to extend agent capabilities
- Need help with specific domains (testing, design, deployment, etc.)

## Skills CLI Basics

The Skills CLI (`npx skills`) is a package manager for agent skills:

**Key commands:**
- `npx skills find [query]` - Search for skills
- `npx skills add <package>` - Install a skill
- `npx skills check` - Check for updates
- `npx skills update` - Update all skills

Browse at: https://skills.sh/

## Workflow

1. **Understand the need** - Identify domain and specific task
2. **Search** - Run `npx skills find [query]` with relevant keywords
3. **Present options** - Show skill name, purpose, install command, and skills.sh link
4. **Install if desired** - Use `npx skills add <owner/repo@skill> -g -y`

## Common Categories

Web Development, Testing, DevOps, Documentation, Code Quality, Design, Productivity

## Search Tips

- Use specific keywords ("react testing" vs "testing")
- Try alternative terms
- Check popular sources like `vercel-labs/agent-skills`

## If Nothing Found

Acknowledge the gap, offer direct help, and suggest creating a custom skill with `npx skills init`.
