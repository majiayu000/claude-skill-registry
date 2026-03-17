---
name: {{PLUGIN_ID}}-help
description: |
  Help and documentation for {{PLUGIN_NAME}} plugin.
  Use when: user asks about available skills, commands, or how to use this plugin.
  Triggers: "help", "what can you do", "list skills", "show commands",
  "как пользоваться", "что умеешь".
---

# {{PLUGIN_NAME}} Help

Quick reference for all skills and commands in this plugin.

## Overview

{{PLUGIN_DESCRIPTION}}

## Skills

{{SKILLS_TABLE}}

## Commands

{{COMMANDS_TABLE}}

## Quick Start

### Find the right skill
```
"What skill helps with [task]?"
"List all skills for [category]"
```

### Use a skill
```
"Use the [skill-name] skill"
"Help me with [task that triggers skill]"
```

### Run a command
```
/{{PLUGIN_PREFIX}}:help          — this help
/{{PLUGIN_PREFIX}}:help:skills   — detailed skill docs
/{{PLUGIN_PREFIX}}:help:search   — find skill by task
```

## Skill Categories

{{SKILL_CATEGORIES}}

## Getting Help

- **Specific skill**: "Tell me about the [skill-name] skill"
- **Find by task**: "What skill helps with [your task]?"
- **All commands**: "/help" or ask "what commands are available?"
