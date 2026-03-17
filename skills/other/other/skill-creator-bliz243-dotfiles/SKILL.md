---
name: skill-creator
description: Create and manage Codex skills. Use when creating a new skill, updating an existing skill, or debugging skill activation issues. Covers skill structure, SKILL.md frontmatter, and best practices.
---

# Skill Creator

Guide for creating effective Codex skills.

## What Skills Are

Skills are modular packages that extend Codex's capabilities with specialized knowledge, workflows, and tools. They transform Codex from a general-purpose agent into a domain expert.

**Default assumption:** Codex is already smart. Only add context it doesn't have. Challenge each piece: "Does this justify its token cost?"

## Skill Structure

```
skill-name/
├── SKILL.md           # Required - main instructions
├── agents/
│   └── openai.yaml    # Optional - UI metadata and MCP dependencies
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

### agents/openai.yaml (Optional)

UI metadata for skill discovery:

```yaml
interface:
  display_name: "User-facing Name"
  short_description: "Brief description (25-64 chars)"
  default_prompt: "Use $skill-name to do X"
```

### References (Optional)

For detailed docs loaded only when needed:

```
references/
├── patterns.md      # Detailed code patterns
├── api-docs.md      # API reference
└── examples.md      # More examples
```

Keep references one level deep. For large files (>100 lines), add a table of contents.

## Skill Discovery

Codex scans these locations for skills at startup:

| Scope | Path | Use Case |
|-------|------|----------|
| Project | `.agents/skills/` | Project-specific |
| User | `~/.agents/skills/` | Personal cross-repo |
| Compat | `~/.codex/skills/` | Legacy compatibility |
| Admin | `/etc/codex/skills/` | System-wide |

Skills activate when:
- You mention a skill by name (e.g., "use brainstorming")
- The task matches a skill's `description` field
- You invoke with `$skill-name` or `/skills`

## Examples

### Simple Skill

Just create the folder with SKILL.md:

```
~/.agents/skills/code-review/
└── SKILL.md
```

### Skill with References

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
```

## Best Practices

**Do:**
- Keep SKILL.md under 500 lines
- Show concrete code examples
- Use references/ for detailed docs
- Make description specific to avoid false positives
- Test skill activation before deploying

**Don't:**
- Over-explain concepts (show patterns instead)
- Include README, CHANGELOG, or meta-docs
- Duplicate info between SKILL.md and references

## Creating a New Skill

1. Create folder: `mkdir -p ~/.agents/skills/my-skill`
2. Create SKILL.md with frontmatter and instructions
3. Optionally add agents/openai.yaml for UI metadata
4. Test with `$my-skill` or trigger keywords
5. Iterate based on real usage
