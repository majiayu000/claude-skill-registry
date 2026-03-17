# Claude Code Skill Conventions

Claude Code-specific features for skills. This supplements the generic skill conventions in SKILL.md.

## @ File References

The `@` symbol in SKILL.md (and CLAUDE.md) files includes another file's content into the AI's context. This is the primary mechanism for composing instructions from multiple files.

```markdown
---
name: MySkill
description: Does something useful...
---

@conventions.md
@tools-reference.md

# MySkill
...
```

Both referenced files get expanded inline before the AI sees the skill. Resolution is always relative to the SKILL.md file's directory.

### Resolution Rules

| SKILL.md location | `@companion.md` resolves to |
|--------------------|-----------------------------|
| `skills/MySkill/SKILL.md` | `skills/MySkill/companion.md` |
| `~/.claude/skills/MySkill/SKILL.md` | `~/.claude/skills/MySkill/companion.md` |

### Directory References

`@src/components/` shows the file listing of that directory -- useful for giving the AI a structural overview without reading every file.

### When to Use @ References

- **Any content the skill needs** -- conventions, reference tables, shared config, tool catalogs
- **Content shared across multiple skills** in the same module
- **Provider-specific content** that only applies to Claude Code
- **Large reference material** that would bloat the main SKILL.md

Keep inline when the section is short (<20 lines) and tightly coupled to the skill body.

## CLAUDE.md @ References

CLAUDE.md files (global or project-level) use the same `@` mechanism:

| Level | File | Applies to |
|-------|------|-----------|
| Global | `~/.claude/CLAUDE.md` | Every project, every session |
| Project | `<project>/CLAUDE.md` | All sessions in this project |
| Project-local | `<project>/.claude/CLAUDE.md` | All sessions (gitignored) |

### When to Extract from CLAUDE.md

Extract a section into a separate `@`-referenced file when:
- **It's domain-specific** -- tool catalogs, API references, module docs
- **It's reusable across projects** -- coding conventions, commit rules
- **It exceeds ~50 lines** -- large blocks dilute surrounding instructions
- **It changes independently** -- tool docs update on different cadence than project rules

### Naming Conventions

| Pattern | Use for |
|---------|---------|
| `RTK.md`, `TOOLS.md` | Uppercase -- tool/system references |
| `conventions.md` | Lowercase -- style and practice docs |
| `<module>.md` | Module-specific reference |

## Skill Discovery

Claude Code discovers skills through `plugin.json`:

```json
{
    "skills": ["./skills"]
}
```

Every directory listed is scanned for `*/SKILL.md` files. Skills in later directories override earlier ones of the same name (last wins).

## Skill Load Hooks

Skills can execute shell commands on load using `!` backtick lines at the end of SKILL.md:

```markdown
!`some-command arg1 arg2`
```

These run when the skill is invoked. Use for loading additional context, checking prerequisites, or initializing state.
