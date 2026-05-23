---
name: skill-anatomy
description: Comprehensive guide for understanding and fixing skill structure issues. Use this skill when skills aren't loading, when creating new skills, when organizing skills for open-source vs personal use, or when troubleshooting Claude Code skill discovery. Covers flat hierarchy requirement, SKILL.md structure, bundled resources, gitignore patterns, and the personal- prefix convention.
---

# Skill Anatomy & Troubleshooting

## Quick Reference

### Skill Not Loading?

1. **Check hierarchy** - Skills must be directly under `.claude/skills/` (flat structure)
2. **Check SKILL.md** - Must have valid YAML frontmatter with `name` and `description`
3. **Restart Claude Code** - Skills are loaded at startup

### Create a New Skill

```bash
mkdir .claude/skills/my-skill
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Clear description of what the skill does AND when to use it.
---

# My Skill

Your instructions here.
EOF
```

## Flat Hierarchy Requirement

**Critical**: Claude Code only discovers skills in a **flat hierarchy**.

```
✅ CORRECT - Skills discovered:
.claude/skills/
├── skill-a/SKILL.md
├── skill-b/SKILL.md
└── skill-c/SKILL.md

❌ WRONG - Skills NOT discovered:
.claude/skills/
├── core/
│   └── skill-a/SKILL.md    # NOT discovered
├── examples/
│   └── skill-b/SKILL.md    # NOT discovered
└── local/
    └── skill-c/SKILL.md    # NOT discovered
```

Each skill must be a direct child of `.claude/skills/`.

## SKILL.md Structure

### Required: YAML Frontmatter

```yaml
---
name: skill-name
description: What the skill does AND when to use it. Include trigger phrases.
---
```

- `name`: Unique identifier (must match folder name by convention)
- `description`: **Primary trigger mechanism** - Claude uses this to decide when to invoke the skill

### Description Best Practices

Include both what the skill does AND specific triggers:

```yaml
# ✅ Good - Clear triggers
description: Query WhatsApp messages from the database. Use when asked to "search messages", "find conversations", "message history", or any WhatsApp data retrieval.

# ❌ Bad - No triggers
description: Handles WhatsApp message queries.
```

### Markdown Body

Instructions and guidance for using the skill. Keep under 500 lines - use references for detailed content.

## Bundled Resources

### Optional Directories

```
skill-name/
├── SKILL.md           # Required
├── scripts/           # Optional: executable code
├── references/        # Optional: documentation loaded on-demand
└── assets/            # Optional: files for output (templates)
```

### scripts/

Executable code (Python/Bash) for deterministic tasks:

- Executed WITHOUT loading into context window
- Must be referenced from SKILL.md
- Test scripts before committing

### references/

Documentation loaded as-needed into context:

- NOT loaded until Claude determines it's needed
- Must be referenced from SKILL.md with clear guidance on when to use
- Keep files under 10k words; include grep patterns for larger files

### assets/

Files used in output (not loaded into context):

- Templates, images, fonts, boilerplate code
- Copied or modified as part of skill output

### What NOT to Include

- README.md, CHANGELOG.md, INSTALLATION.md
- LICENSE files
- Test files
- Documentation about the skill creation process

## Personal Skills Convention

Personal skills contain organization-specific content (IPs, credentials, project IDs) and should not be in open-source repos.

### Naming Convention

```
personal-<skill-name>
```

Examples:

- `personal-production-debugging` - Contains server IPs, SSH credentials
- `personal-jira-project-management` - Contains JIRA Cloud IDs, project keys
- `personal-whatsapp-messages` - Contains phone numbers, group IDs

### Gitignore Pattern

Add to `.gitignore`:

```gitignore
# Personal skills (prefixed with personal-)
.claude/skills/personal-*/
```

### Creating a Personal Skill

```bash
mkdir .claude/skills/personal-my-org-skill
# Add SKILL.md with name: personal-my-org-skill
# Automatically gitignored
```

## Troubleshooting

### Skills not showing in Claude Code

1. **Verify flat structure**:

   ```bash
   ls .claude/skills/*/SKILL.md
   ```

   Each skill should be listed directly, not nested.

2. **Check SKILL.md syntax**:

   ```bash
   head -5 .claude/skills/my-skill/SKILL.md
   ```

   Must start with `---`, have `name:` and `description:`, end with `---`.

3. **Restart Claude Code** - Skills are loaded at startup.

### Skill triggers but content is wrong

- Check `name:` in frontmatter matches folder name
- Ensure `description:` includes the trigger phrases being used

### Personal skills appearing in git

- Verify `.gitignore` has `.claude/skills/personal-*/`
- Check skill folder name starts with `personal-`
- Run `git check-ignore -v .claude/skills/personal-<name>/`

### Reference files not loading

- Ensure reference is mentioned in SKILL.md with clear guidance
- Check file path is correct (relative to skill folder)
- Reference files load on-demand, not automatically

## Migration Checklist

When restructuring skills from nested to flat:

1. Move all skill folders directly under `.claude/skills/`
2. Update `name:` in each SKILL.md to match new folder name
3. Rename personal skills with `personal-` prefix
4. Update `.gitignore` for personal skill pattern
5. Update documentation references to old paths
6. Restart Claude Code to pick up changes
