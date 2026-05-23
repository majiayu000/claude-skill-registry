---
name: skill-maker
description: |
  Create new Claude Code skills following project conventions. Use when: (1) creating
  a new skill from scratch, (2) converting learnings into reusable skills, (3) validating
  existing skills against quality standards. Provides templates, frontmatter specification,
  and quality checklist.
category: development
user-invocable: true
---

# Skill Maker

Create and validate Claude Code skills following best practices.

## Quick Start

**Create a new skill:**
1. Choose a template: `simple`, `with-references`, or `full`
2. Create directory: `skills/<skill-name>/`
3. Write SKILL.md following the template
4. Run validation: `skills validate <skill-name>`

## Templates

| Template | Structure | Use Case |
|----------|-----------|----------|
| simple | SKILL.md only | Single-file guidance, quick tips |
| with-references | + references/ | Multi-section documentation |
| full | + docs/, templates/, provenance | Comprehensive skills with examples |

See [templates/](templates/) for complete templates.

## Frontmatter Specification

Required fields:
```yaml
---
name: skill-name          # kebab-case, unique identifier
description: |            # Multi-line recommended
  What the skill does. Use when: (1) condition, (2) condition.
  Specific symptoms, error messages, or file types it handles.
---
```

Optional fields:
```yaml
category: testing|development|documentation|refactoring|security|performance
user-invocable: true      # Can be called via /skill-name
disable-model-invocation: false  # Prevent automatic loading
allowed-tools: Read,Write # Comma-separated tool names
context: fork|inline      # How skill is invoked
agent: agent-name         # Specific agent to use
```

See [references/frontmatter-spec.md](references/frontmatter-spec.md) for details.

## Description Quality

Good descriptions enable semantic matching. Include:

1. **What it does** (1 sentence)
2. **Trigger conditions** (Use when:, Helps with:)
3. **Specific context** (error messages, file types, frameworks)

### Good Example
```yaml
description: |
  Fix "ENOENT: no such file or directory" errors in npm monorepos.
  Use when: (1) npm run fails with ENOENT, (2) paths work in root
  but not packages, (3) symlinks cause resolution failures.
  Covers Lerna, Turborepo, and npm workspaces.
```

### Bad Example
```yaml
description: A skill that helps with npm problems.
```

See [references/description-guide.md](references/description-guide.md).

## Quality Checklist

Before finalizing a skill, verify:

- [ ] Name is kebab-case and descriptive
- [ ] Description > 50 characters
- [ ] Description includes trigger conditions
- [ ] Category is valid (if specified)
- [ ] Referenced files exist (references/, docs/)
- [ ] No slop patterns (placeholder content)
- [ ] Content is actionable and specific
- [ ] Tested with `skills validate`

See [references/quality-checklist.md](references/quality-checklist.md).

## Validation

Run validation on your skill:

```bash
# Validate specific skill
skills validate <skill-name>

# Validate all skills in project
skills validate

# JSON output
skills validate --json
```

Validation checks:
- Frontmatter format and required fields
- Description quality (length, trigger conditions)
- Category validity
- Slop pattern detection
- Reference file existence

## Slop Detection

The validator detects common slop patterns:

| Pattern | Example | Action |
|---------|---------|--------|
| test-skill-* | `test-skill-1234567890` | Delete |
| Placeholder content | "NEW content with improvements!" | Rewrite |
| Generic names | "# Test Skill" | Rename |
| Lorem ipsum | Any placeholder text | Remove |

## Skill Chaining

This skill works with:

- **claudeception**: Extract learnings → create skill with skill-maker
- **tdd**: Write tests first when adding CLI validation features
- **dogfood-skills**: Use `skills validate` after creating skills

## Creating Your First Skill

1. **Identify the knowledge**: What non-obvious solution did you discover?
2. **Check existing skills**: Is there already a skill for this?
3. **Choose template**: Start with `simple` unless you need references
4. **Write SKILL.md**: Follow frontmatter spec and description guidelines
5. **Validate**: Run `skills validate <name>`
6. **Test**: Use the skill in a real scenario

## Directory Structure

**All skills live in the root `skills/` directory** (canonical location):

```
skills/<skill-name>/
├── SKILL.md              # Required: Main skill file
├── references/           # Optional: Supporting documentation
│   ├── guide.md
│   └── examples.md
├── templates/            # Optional: Code/config templates
├── scripts/              # Optional: Helper scripts
└── .provenance.json      # Optional: Source tracking
```

The `.claude/skills/` symlink makes skills available to Claude Code. Never create skills directly in `packages/skills/skills/` (generated at build time).

## Tips

- Start simple, add complexity only when needed
- Keep SKILL.md focused on actionable guidance
- Use references/ for detailed documentation
- Include concrete examples, not just theory
- Update skills when you learn more
