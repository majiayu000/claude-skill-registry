---
name: skill-creator
description: Create and manage Claude Code skills. Use when creating a new skill, updating an existing skill, or debugging skill activation issues. Covers skill structure, skill-rules.json configuration, trigger patterns, and best practices.
---

# Skill Creator

Guide for creating effective Claude Code skills.

## What Skills Are

Skills are modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a domain expert.

**Default assumption:** Claude is already smart. Only add context Claude doesn't have. Challenge each piece: "Does this justify its token cost?"

## Skill Structure

```
skill-name/
├── SKILL.md           # Required - main instructions
├── references/        # Optional - detailed docs loaded on-demand
├── scripts/           # Optional - executable code
└── assets/            # Optional - templates, images, files for output
```

### SKILL.md (Required)

```markdown
---
name: my-skill
description: What it does AND when to use it. Include trigger keywords.
---

# My Skill

## Quick Start
[Essential workflow - what to do first]

## Patterns
[Show correct patterns with code examples]

## Anti-Patterns
[Show what to avoid with code examples]

## Reference
- See [detailed-ref.md](references/detailed-ref.md) for more
```

**Key rules:**
- Keep under 500 lines (use references/ for details)
- Description is the trigger - include all "when to use" info there
- Show examples over explanations
- Imperative form: "Use X" not "You should use X"

### References (Optional)

For detailed docs loaded only when needed:

```
references/
├── patterns.md      # Detailed code patterns
├── api-docs.md      # API reference
└── examples.md      # More examples
```

Keep references one level deep. For large files (>100 lines), add a table of contents.

## Skill Rules Configuration

Add to `~/.claude/config/skill-rules.json` to control when skills activate:

```json
{
  "skills": [
    {
      "name": "my-skill",
      "type": "suggest",
      "triggers": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?component"],
      "description": "Shown when skill is suggested"
    }
  ]
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill name (matches folder name) |
| `type` | Yes | `suggest` (advisory) or `block` (required) |
| `triggers` | No | Keywords that activate skill (case-insensitive) |
| `intentPatterns` | No | Regex patterns for implicit intent |
| `description` | No | Message shown when suggested |

### Trigger Types

**Keywords** - exact substring match (case-insensitive):
```json
"triggers": ["aggregate", "repository", "svelte"]
```
- "create **aggregate**" ✅
- "Create Aggregate" ✅ (case-insensitive)
- "aggregation" ✅ (substring)

**Intent Patterns** - regex for action + domain:
```json
"intentPatterns": [
  "(create|add|implement).*?(service|component)",
  "(pause|cancel|resume).*?subscription"
]
```

Tips:
- Use non-greedy: `.*?` not `.*`
- Common verbs: create, add, implement, modify, fix, build
- Test at regex101.com

## Examples

### Simple Skill (No Rules)

Just create the folder with SKILL.md:

```
~/.claude/skills/code-review/
└── SKILL.md
```

Invoke with `/code-review` or skill triggers from description.

### Skill with Auto-Suggestion

```json
{
  "skills": [
    {
      "name": "frontend-design",
      "type": "suggest",
      "triggers": ["ui", "component", "styling", "css", "tailwind"],
      "intentPatterns": ["(build|create|design).*?(page|component|ui)"],
      "description": "Use frontend-design for distinctive UI"
    }
  ]
}
```

### Domain-Specific Skill

```
ddd-patterns/
├── SKILL.md              # Core workflow
└── references/
    ├── aggregates.md     # Aggregate patterns
    ├── repositories.md   # Repository patterns
    └── services.md       # Service patterns
```

SKILL.md references these only when relevant:
```markdown
## Aggregates
See [references/aggregates.md](references/aggregates.md) for patterns.

## Repositories
See [references/repositories.md](references/repositories.md) for patterns.
```

## Best Practices

**Do:**
- Keep SKILL.md under 500 lines
- Show concrete code examples
- Use references/ for detailed docs
- Make triggers specific to avoid false positives
- Test trigger patterns before deploying

**Don't:**
- Over-explain concepts (show patterns instead)
- Use broad keywords ("system", "work", "file")
- Include README, CHANGELOG, or meta-docs
- Duplicate info between SKILL.md and references

## Debugging

### Skill Not Triggering

1. Check skill folder exists in `~/.claude/skills/`
2. Verify SKILL.md has valid frontmatter (name + description)
3. Check skill-rules.json is valid JSON: `jq . ~/.claude/config/skill-rules.json`
4. Test keywords are in your prompt (case-insensitive substring)
5. Test intent patterns at regex101.com

### Creating a New Skill

1. Create folder: `mkdir ~/.claude/skills/my-skill`
2. Create SKILL.md with frontmatter and instructions
3. Optionally add to skill-rules.json for auto-suggestion
4. Test with `/my-skill` or trigger keywords
5. Iterate based on real usage
