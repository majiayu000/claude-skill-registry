---
name: janitor-check
description: "Check skills for errors and missing info"
metadata:
  version: 1.0.0
---

# Skill Check

Check all skills against best practices and quality standards.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/lint.sh
```

## Rules Checked

### Critical
- Broken symlinks
- Missing SKILL.md file
- Missing frontmatter delimiters (`---`)

### Warning
- Missing or empty `name` field
- Missing or empty `description` field
- Description too short (< 30 chars) or too long (> 200 chars)
- Description doesn't explain trigger conditions (missing "when"/"use when")
- Folder name doesn't match `name` field
- Missing `version` field

### Info
- No body content after frontmatter
- No Gotchas section
- Large files (>500 lines) without progressive disclosure

## Best Practices Reference

### Description Quality
- 50-200 characters
- Must explain WHEN to trigger, not just WHAT it does
- Include trigger keywords the user might say
- Format: "Use when [condition]. Also use when [user says X, Y, Z]."

### Frontmatter
- `name` - required, matches folder name
- `description` - required, model-facing trigger description
- `version` - recommended

## Related Skills

- For auto-fixing issues found: `/janitor-fix`
- For duplicate detection: `/janitor-duplicates`
- For full health report: `/janitor-report`
