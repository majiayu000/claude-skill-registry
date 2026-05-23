---
name: writing-claude-skills
description: Create properly formatted Claude Code skills with YAML frontmatter, directory structure, and best practices. Use when creating new skills, converting documentation to skills, or learning how to write skills.
---

# Writing Claude Code Skills

## What is a Skill?

Skills are modular capabilities that extend Claude's functionality. They are **model-invoked** — Claude autonomously decides when to use them based on context and the skill's description.

## Directory Structure

Skills must be stored as directories containing a required `SKILL.md` file:

```
~/.claude/skills/my-skill-name/     # Personal (all projects)
.claude/skills/my-skill-name/       # Project (team-shared via git)
```

### Multi-file Structure

```
my-skill/
├── SKILL.md           # Required - main instructions
├── REFERENCE.md       # Optional - detailed reference
├── EXAMPLES.md        # Optional - usage examples
├── scripts/           # Optional - helper scripts
│   └── helper.py
└── templates/         # Optional - templates
    └── template.txt
```

## Required SKILL.md Format

```yaml
---
name: your-skill-name
description: What this skill does AND when to use it. Include trigger keywords.
---

# Skill Title

## Instructions
Step-by-step guidance for Claude.

## Examples
Concrete usage examples.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, numbers, hyphens only. Max 64 chars. Must be unique. |
| `description` | Yes | What it does AND when to use it. Max 1024 chars. Critical for discovery. |
| `allowed-tools` | No | Restricts which tools Claude can use (e.g., `Read, Grep, Glob`). |

## Writing Effective Descriptions

The description determines when Claude activates your skill.

**Good** (specific, includes triggers, keywords):
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad** (vague):
```yaml
description: Helps with documents
```

## Best Practices

1. **One skill = one capability** - Keep focused
2. **Include trigger keywords** in description
3. **Use progressive disclosure** - Main info in SKILL.md, details in supporting files
4. **Document versions** for tracking changes
5. **Use `allowed-tools`** for security-sensitive skills
6. **Test with teammates** for activation and clarity
7. **Avoid dangerous backtick patterns** - See "Dangerous Markdown Patterns" below
8. **Run verification** before committing - `./verify.sh`

## Template for New Skills

```yaml
---
name: my-new-skill
description: [Action verb] [what it does]. Use when [trigger conditions] or when the user mentions [keywords].
---

# [Skill Title]

## Overview
Brief description of capability.

## Instructions
1. First step
2. Second step
3. Third step

## Examples

### Example 1: [Use case]
[Concrete example]

## Requirements
- List any dependencies
- Required packages or tools
```

## Registering Skills in Settings

After creating a skill, configure permissions in settings.json for Claude to use it.

### Required Permissions

| Permission | Purpose |
|------------|---------|
| `Skill(name)` | Allow invoking the skill without prompts |
| `Read(~/.claude/skills/**)` | Allow reading personal skill files |

**For personal skills**, add to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Skill(your-skill-name)",
      "Read(~/.claude/skills/**)"
    ]
  }
}
```

**For project skills**, add to `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Skill(your-skill-name)",
      "Read(./.claude/skills/**)"
    ]
  }
}
```

**Notes:**
- The `Read()` permission for the skills directory only needs to be added **once** (not per-skill)
- Each new skill needs its own `Skill(name)` entry

## Validation Checklist

- [ ] SKILL.md exists in skill directory
- [ ] YAML frontmatter starts on line 1 with `---`
- [ ] `name` field: lowercase, hyphens, no spaces, max 64 chars
- [ ] `description` field: includes what AND when, max 1024 chars
- [ ] No tabs in YAML (use spaces only)
- [ ] Closing `---` before markdown content
- [ ] No dangerous backtick patterns (shell chars like `!$#` in inline code)
- [ ] `Skill(name)` added to `permissions.allow` in settings.json
- [ ] `Read(~/.claude/skills/**)` added to `permissions.allow` (once per settings file)
- [ ] `./verify.sh` passes with no errors

## Adding New Skills to This Project

Skills live in `.claude/skills/` within this repository.

### Adding Your Skill

1. Create the skill directory:
   ```bash
   mkdir -p .claude/skills/<skill-name>
   ```

2. Write your `SKILL.md` following the format in this guide

3. Update `.claude/settings.json` to add permissions:
   ```json
   "Skill(<skill-name>)"
   ```

4. Run verification:
   ```bash
   ./verify.sh --ui=false
   ```

### Checklist

Before committing:
- [ ] Skill follows naming conventions (lowercase, hyphens)
- [ ] Description is specific with trigger keywords
- [ ] No duplicate of existing skill
- [ ] `Skill(name)` added to `.claude/settings.json`
- [ ] Tested locally with `claude --debug`

## Skill Verification

Skills can break silently. Use the verification pipeline to catch issues before they cause runtime failures.

### Running Verification

```bash
./verify.sh          # Run all checks
bun run verify       # Same via npm script
```

### What Verification Checks

| Check | What It Validates |
|-------|-------------------|
| YAML frontmatter | Starts with `---`, closes properly, no tabs |
| Required fields | `name` and `description` are present |
| Name format | Lowercase, hyphens only, max 64 chars, matches directory |
| Description quality | Contains trigger keywords (warns if missing) |
| Dangerous patterns | Backtick patterns that cause bash interpretation errors |
| settings.json sync | Skills are registered, no orphan permissions |

### Dangerous Patterns to Avoid

| Pattern | Problem | Fix |
|---------|---------|-----|
| Backtick-bang-backtick followed by text and another backtick | Bash history expansion | Rephrase without backticks around the bang |
| Backtick-dollar-backtick followed by text and another backtick | Variable expansion | Use code blocks or rephrase |
| Backtick-hash-backtick followed by text and another backtick | Potential comment parsing | Use code blocks or rephrase |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not discovered | Make description specific with trigger keywords |
| Skill not auto-invoked | Add `Skill(name)` to `permissions.allow` in settings.json |
| Claude can't read skill files | Add `Read(~/.claude/skills/**)` to `permissions.allow` |
| Invalid YAML | Check: `---` on line 1, no tabs, proper indentation |
| Wrong location | Personal: `~/.claude/skills/`, Project: `.claude/skills/` |
| Scripts not running | Run: `chmod +x scripts/*.py` |
| Bash pattern error when reading skill | Check for dangerous backtick patterns (see above) |
| Skill exists but doesn't work | Run `./verify.sh` to check registration |

Debug with: `claude --debug`
