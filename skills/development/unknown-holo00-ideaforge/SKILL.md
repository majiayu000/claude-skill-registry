---
name: skill-creator
description: Guide for creating effective skills. Use this skill when you want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

Guide for creating effective skills that extend Claude's capabilities.

## About Skills

Skills are modular, self-contained packages that provide:
1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

## Core Principles

### Concise is Key

The context window is a public good. Only add context Claude doesn't already have.

- Challenge each piece of information: "Does Claude really need this?"
- Prefer concise examples over verbose explanations
- Default assumption: Claude is already very smart

### Set Appropriate Degrees of Freedom

| Freedom Level | When to Use | Format |
|---------------|-------------|--------|
| **High** | Multiple approaches valid, context-dependent | Text instructions |
| **Medium** | Preferred pattern exists, some variation OK | Pseudocode/scripts with params |
| **Low** | Fragile operations, consistency critical | Specific scripts, few params |

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation loaded as needed
    └── assets/       - Files used in output (templates, etc.)
```

### SKILL.md (Required)

**Frontmatter (YAML)**:
- `name`: Skill identifier (lowercase, hyphenated)
- `description`: What it does AND when to trigger it

**Body (Markdown)**:
- Instructions and guidance
- Only loaded AFTER the skill triggers

### Bundled Resources (Optional)

**scripts/** - Executable code for deterministic tasks
- When: Same code rewritten repeatedly, or reliability needed
- Benefits: Token efficient, deterministic

**references/** - Documentation loaded as needed
- When: Detailed info Claude should reference while working
- Best practice: Keep SKILL.md lean, load refs only when needed

**assets/** - Files used in output
- When: Templates, images, boilerplate needed in final output
- Examples: logo.png, template.docx, starter code

## What NOT to Include

- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- User-facing documentation
- Setup/testing procedures

## Skill Creation Process

### 1. Understand with Concrete Examples
- What functionality should the skill support?
- What would users say to trigger it?
- Get example use cases

### 2. Plan Reusable Contents
For each example:
1. Consider how to execute from scratch
2. Identify helpful scripts, references, assets

### 3. Create the Skill Structure
```bash
mkdir skill-name
touch skill-name/SKILL.md
```

### 4. Write SKILL.md

**Frontmatter example**:
```yaml
---
name: my-skill
description: Does X when Y. Triggers include A, B, C.
---
```

**Body**: Include only essential procedural instructions.

### 5. Add Resources (if needed)
- Create scripts/, references/, assets/ as needed
- Test scripts to ensure they work
- Delete any unused example files

### 6. Iterate
- Use the skill on real tasks
- Notice struggles or inefficiencies
- Update SKILL.md or resources
- Test again

## Progressive Disclosure Patterns

### Pattern 1: High-level guide with references
```markdown
# PDF Processing

## Quick start
[Basic example]

## Advanced features
- **Form filling**: See [FORMS.md](references/FORMS.md)
- **API reference**: See [REFERENCE.md](references/REFERENCE.md)
```

### Pattern 2: Domain-specific organization
```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 3: Framework variants
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

## Best Practices

1. Keep SKILL.md under 500 lines
2. Split content into reference files when approaching limit
3. Keep references one level deep from SKILL.md
4. Include table of contents for files >100 lines
5. Use imperative/infinitive form in writing