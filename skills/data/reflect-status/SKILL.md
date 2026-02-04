---
name: reflect-status
description: Show reflection configuration and learning statistics. Activates for reflect status, reflection status, memory status, learnings status.
---

# Reflect Status Command

**Show reflection configuration and learning statistics.**

## Usage

```bash
/sw:reflect-status
```

## Output Example

```
REFLECT: Status Dashboard

CONFIGURATION

  Reflection:      Enabled
  Model:           haiku
  Max/session:     3

SKILL MEMORIES (CLAUDE.md)

  Skill           Learnings
  ─────────────────────────
  devops          1
  frontend        2
  backend         3
  general         2
  ─────────────────────────
  Total:          8

RECENT LEARNINGS

  - [devops] LSP requires ENABLE_LSP_TOOL=1 env var
  - [frontend] Use shadcn/ui Button component
  - [backend] Return 404 for missing resources

COMMANDS

  /sw:reflect          Manual reflection now
  /sw:reflect-on       Enable auto-reflect
  /sw:reflect-off      Disable auto-reflect
  /sw:reflect-clear    Clear specific learnings
```

## Information Displayed

| Section | Contents |
|---------|----------|
| **Configuration** | Enable status, model, max learnings per session |
| **Skill Memories** | Count of learnings per skill from CLAUDE.md |
| **Recent Learnings** | Latest learnings with skill category |
| **Commands** | Quick reference for reflect commands |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/sw:reflect` | Manual reflection |
| `/sw:reflect-on` | Enable auto-reflect |
| `/sw:reflect-off` | Disable auto-reflect |

## Execution

When this command is invoked:

1. **Read config** from `.specweave/config.json` for reflect settings
2. **Read CLAUDE.md** to find Skill Memories section
3. **Parse learnings** by skill category
4. **Display dashboard** with all sections
