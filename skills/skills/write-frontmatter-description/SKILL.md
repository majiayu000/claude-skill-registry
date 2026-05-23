---
name: write-frontmatter-description
description: "Write or rewrite frontmatter description fields for Claude Code skills and agents. Use when creating new skills/agents, description exceeds 1024 characters, description uses forbidden YAML multiline indicators (>-, |-), description contains colons that trigger quoting, description lacks trigger keywords, or when optimizing descriptions for AI tool selection. Ensures descriptions are single-line, complete, informative, front-loaded with critical information."
user-invocable: true
---

The model MUST write frontmatter descriptions following these rules.

## Formatting Rules

1. **Single-line only** - Never use YAML multiline indicators (`>-`, `|-`, `>`, `|`)
2. **No colons** - Avoid colons (`:`) as they trigger YAML quoting. Swap it for something else or rephrase.
3. **Front-load critical info** - First 1024 characters are most important
   - Claude Code may truncate to 1024 chars in some contexts
   - No hard limit, but keep key information in first 1024 chars
   - Convey purpose, triggers, and value early

A description should be a complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.

## Validation

After writing, validate with the validation script `validate_frontmatter.py`

```sh
 validate_frontmatter.py [file]
```
