---
name: continuous-improvement
description: Capture learnings after tasks. Triggers on task completion, repeated mistakes, retrospective requests, or "what did I learn".
---

# Continuous Improvement

After completing a task, briefly reflect and capture learnings.

## When to Activate

- Task just completed
- Same mistake made twice
- User asks "what did I learn" or "retrospective"
- Complex process was difficult or slow

## Reflect (30 seconds)

Ask yourself:
- What worked well?
- What was difficult or slow?
- What's missing (automation, docs, tools)?

## Capture

| Learning Type | Action |
|---------------|--------|
| Pattern/gotcha | Store in Memory MCP |
| Missing automation | Create issue/TODO |
| Repeated mistake | Update `.claude/rules/` |
| Complex process | Create `.claude/skills/` |

## Memory Pattern

When storing a learning in Memory MCP:

```javascript
mcp__memory__create_entities({
  entities: [{
    name: "Learning_TOPIC",
    entityType: "development_learning",
    observations: [
      "Context: What was happening",
      "Learning: What was learned",
      "Application: How to apply it"
    ]
  }]
})
```

## Improvement Actions

| Issue | Solution |
|-------|----------|
| Same mistake twice | Add rule to `.claude/rules/` |
| Manual process > 5 min | Create skill or hook |
| New tool/pattern | Store in Memory MCP |
| Missing documentation | Update docs |

## Rule Addition Example

When you make the same mistake twice:

1. Identify the pattern
2. Create or update a rule file:

```markdown
# .claude/rules/my-rules.md
---
paths: relevant/path/**
description: Rules for this area
---

## Critical Rules

| Rule | Why |
|------|-----|
| Don't do X | Because Y happens |
```

## Skill Addition Example

When a process is complex and repeated:

1. Create skill directory: `.claude/skills/my-skill/`
2. Create SKILL.md:

```markdown
# .claude/skills/my-skill/SKILL.md
---
name: my-skill
description: When this skill should activate
---

# My Skill

## When to Activate
[Trigger conditions]

## Process
[Steps to follow]
```

## Run `/improve-claude-config` for major configuration updates.
