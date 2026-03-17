---
name: skill-first
description: Check for relevant skills before starting any task. Triggers on task start, new requests, beginning work, or implementation.
---

# Skill-First Discipline

Before responding to ANY user request, check if a matching skill exists.

## Checklist

1. **Scan available skills** - Review the Skill tool's available skills listing
2. **Match request to skill** - Does any skill cover this task type?
3. **Load if matched** - Use `Skill` tool to load it
4. **Announce usage** - Tell the user: "I'm using [skill-name] to [action]"
5. **Follow exactly** - Execute the skill's guidance without deviation

## Rationalizations to Reject

If you catch yourself considering these, stop and check for skills:

- "This is simple, I don't need a skill"
- "I'll just do this quickly"
- "The skill is overkill"
- "I already know how to do this"

These are failure modes. If a skill exists for your task, use it.

## Discovering Available Skills

The Skill tool shows all installed skills in its "Available Skills" section. Skills are organized by source:

- **majestic-engineer**: Code search, TDD, diagrams, CI, git worktrees
- **majestic-rails**: Ruby/Rails coding, RSpec, Minitest, gem building
- **majestic-tools**: Brainstorming, skill creation, skill-first
- **majestic-marketing**: Copy editing

To list skills programmatically:
```bash
find ~/.claude -path "*/skills/*/SKILL.md" 2>/dev/null | xargs -I{} grep "^name:" {}
```

## When to Skip

Skip only when:
- Answering factual questions (no task involved)
- Simple clarifications
- User explicitly declines skill usage

For everything else, skill-first is mandatory.
