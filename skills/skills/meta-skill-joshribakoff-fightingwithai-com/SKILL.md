## Skills vs Commands

- **Commands**: You type `/command` to trigger
- **Skills**: Claude auto-discovers and invokes when relevant

## Structure

Skills are **folders** with a `SKILL.md` file, plus optional scripts, unit tests, or tools:
```
.claude/skills/magic-links/
├── SKILL.md
├── scripts/
├── tests/
└── tools/
```

## Project Convention

Each skill gets a matching command so humans can trigger it manually:
```
.claude/commands/magic-links.md  →  "Invoke the magic-links skill"
.claude/skills/magic-links/SKILL.md
```

The command file just references the skill (more portable than symlinks, works everywhere).
