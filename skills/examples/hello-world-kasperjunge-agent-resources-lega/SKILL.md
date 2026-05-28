---
name: hello-world
description: A simple example skill that demonstrates Claude Code skill structure
---

# Hello World Skill

This is a demonstration skill that shows how Claude Code skills work.

## When to Use

Apply this skill when the user asks you to:
- Say hello
- Demonstrate how skills work
- Greet them

## Instructions

When invoked, respond with a friendly greeting:

```
Hello, World! 👋

This response was generated using the hello-world skill.
Skills are automatically discovered and applied based on context.
```

## Key Concepts

- Skills live in `.claude/skills/<skill-name>/SKILL.md`
- They're auto-discovered based on relevance to the conversation
- Skills can include supporting files like scripts and templates
- Use skills for complex workflows that need structure

