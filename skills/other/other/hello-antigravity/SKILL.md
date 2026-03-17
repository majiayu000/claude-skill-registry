---
name: hello-antigravity
description: A simple "Hello World" skill to test your OMA installation
version: 1.0.0
author: Oh My Antigravity
---

# Hello Antigravity Skill

This is a demonstration skill for **Oh My Antigravity**. It shows the basic structure of a skill (plugin) that Antigravity can understand.

## Usage

When you need a friendly greeting or want to test if OMA is working correctly, just mention "hello antigravity" or ask me to use this skill.

## What This Skill Does

1. **Greets the user** with a warm welcome message
2. **Confirms installation** is working correctly
3. **Demonstrates skill structure** for developers creating their own plugins

## Example Output

```
🎉 Hello from Oh My Antigravity!

Your OMA installation is working perfectly.
This skill was loaded from: ~/.gemini/antigravity/skills/hello-antigravity/

Keep building amazing things!
```

## Creating Your Own Skills

To create a new skill:

1. Create a folder in `plugins/` (e.g., `plugins/my-skill/`)
2. Add a `SKILL.md` file with YAML frontmatter
3. Optionally add supporting files in `scripts/`, `examples/`, or `resources/`
4. Run `oma install my-skill`

That's it! Antigravity will now be able to use your custom skill.
