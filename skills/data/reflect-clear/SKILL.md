---
name: reflect-clear
description: Clear specific learnings from CLAUDE.md Skill Memories section. Activates for reflect clear, clear learning, remove learning, delete memory.
---

# Reflect Clear Command

**Remove specific learnings from CLAUDE.md Skill Memories section.**

## Usage

```bash
# Clear all learnings for a skill
/sw:reflect-clear --skill frontend

# Clear all learnings (with confirmation)
/sw:reflect-clear --all
```

## Arguments

| Argument | Description |
|----------|-------------|
| `--skill <name>` | Clear all learnings for skill |
| `--all` | Clear ALL learnings (requires confirmation) |

## Examples

### Clear Skill Learnings

```bash
/sw:reflect-clear --skill frontend
```

Output:
```
Clearing learnings for 'frontend' skill...

This will remove 3 learnings from CLAUDE.md:
  - "Always use Button component with variant='primary'"
  - "Use shadcn/ui for all UI components"
  - "Prefer Vercel over Cloudflare for this project"

Type 'yes' to confirm: yes

Cleared 3 learnings from frontend skill.
```

### Clear All Learnings

```bash
/sw:reflect-clear --all
```

Output:
```
Clear ALL learnings from CLAUDE.md?

This will remove 12 learnings across all skills:
  - frontend: 3
  - backend: 4
  - devops: 2
  - general: 3

Type 'yes' to confirm: yes

Cleared 12 learnings.
```

## How It Works

1. Reads CLAUDE.md to find the `## Skill Memories` section
2. Shows matching learnings for confirmation
3. On approval, removes the learnings
4. Writes updated CLAUDE.md

## Execution

When this command is invoked:

1. **Read CLAUDE.md** to find Skill Memories section
2. **Show confirmation** with what will be deleted
3. **Edit CLAUDE.md** to remove matching learnings on confirmation
