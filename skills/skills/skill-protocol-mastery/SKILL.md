---
name: skill-protocol-mastery
description: This skill should be used when the user asks to "create a skill", "write a SKILL.md", "validate skill structure", "improve skill description", "understand skill protocol", "design skill architecture", or needs guidance on progressive disclosure, trigger phrases, writing style, or skill validation for Claude Code.
version: 1.0.0
---

# Skill Protocol Mastery

This skill provides comprehensive guidance for creating, validating, and optimizing Agent Skills for Claude Code, based on the official Anthropic protocol specification and best practices.

## Core Concepts

### What Skills Are

Skills are modular packages that extend Claude's capabilities through:
- Specialized workflows for specific domains
- Tool integrations for file formats or APIs
- Domain expertise with company-specific knowledge
- Bundled resources (scripts, references, assets)

### Progressive Disclosure Architecture

Skills use a three-level loading system:

| Level | Content | When Loaded | Size Limit |
|-------|---------|-------------|------------|
| 1 | Metadata (name + description) | Always | ~100 words |
| 2 | SKILL.md body | When triggered | 1,500-2,000 words |
| 3 | Bundled resources | As needed | Unlimited* |

*Scripts execute without loading into context.

## Skill Structure

### Required Files

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable utilities
    ├── references/   - Detailed documentation
    ├── examples/     - Working code samples
    └── assets/       - Templates, images, fonts
```

### YAML Frontmatter Requirements

**Validation Rules:**
- `name`: 1-64 characters, pattern `^[a-z0-9-]+$`, no reserved words
- `description`: 1-1024 characters, third-person, specific triggers

**Template:**
```yaml
---
name: skill-identifier
description: This skill should be used when the user asks to "trigger phrase 1", "trigger phrase 2", "trigger phrase 3". Provides [capability description].
version: 1.0.0
---
```

## Writing Style Requirements

### Imperative/Infinitive Form (Required)

Write verb-first instructions, not second person:

✅ **Correct:**
```markdown
To create a hook, define the event type.
Configure the MCP server with authentication.
Validate settings before use.
```

❌ **Incorrect (second person - avoid):**
```
[Second person] create a hook by defining the event type.
[Second person] configure the MCP server.
[Second person] validate settings before use.
```

### Third-Person Descriptions (Required)

✅ **Correct:**
```yaml
description: This skill should be used when the user asks to "create X"...
```

❌ **Incorrect:**
```yaml
description: Use this skill when you want to create X...
```

## Description Quality Patterns

### Strong Trigger Phrases

Include exact phrases users would say:

```yaml
# Good - specific triggers
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", or mentions hook events (PreToolUse, PostToolUse, Stop).

# Bad - vague
description: Provides guidance for working with hooks.
```

### Description Components

1. **Third-person opener**: "This skill should be used when..."
2. **Specific triggers**: "create X", "configure Y", "validate Z"
3. **Context keywords**: File types, domain terms, action verbs
4. **Capability summary**: What the skill provides

## Content Organization

### What Goes in SKILL.md

Include (always loaded when triggered):
- Core concepts and overview
- Essential procedures and workflows
- Quick reference tables
- Pointers to references/examples/scripts
- Most common use cases

**Keep under 2,000 words, maximum 3,000 words**

### What Goes in references/

Move to references (loaded as needed):
- Detailed patterns and advanced techniques
- Comprehensive API documentation
- Migration guides and edge cases
- Extensive examples and walkthroughs

**Each file can be 2,000-5,000+ words**

### What Goes in scripts/

Utility scripts for:
- Validation tools
- Testing helpers
- Parsing utilities
- Automation scripts

**Must be executable and documented**

## Skill Creation Workflow

### Step 1: Understand Use Cases

Gather concrete examples of skill usage:
- "What would a user say to trigger this skill?"
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"

### Step 2: Plan Resources

Analyze examples to identify:
- Scripts for repetitive code
- References for detailed documentation
- Assets for templates and output files
- Examples for working demonstrations

### Step 3: Create Structure

```bash
mkdir -p skills/skill-name/{references,examples,scripts}
touch skills/skill-name/SKILL.md
```

### Step 4: Write SKILL.md

1. Create frontmatter with third-person description and triggers
2. Write lean body (1,500-2,000 words) in imperative form
3. Reference all supporting files clearly

### Step 5: Validate

Run validation checklist (see `references/validation-checklist.md`)

### Step 6: Iterate

Test with real usage, improve based on observations.

## Quick Reference Templates

### Minimal Skill

```
skill-name/
└── SKILL.md
```

### Standard Skill (Recommended)

```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.sh
```

### Complete Skill

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.sh
│   └── example2.json
└── scripts/
    └── validate.sh
```

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Weak triggers | Skill doesn't load | Add specific phrases users say |
| Second person | Inconsistent style | Use imperative form |
| Too much in SKILL.md | Context bloat | Move to references/ |
| Missing references | Claude can't find details | Add resource pointers |
| Vague description | Poor discovery | Include concrete scenarios |

## Best Practices Summary

✅ **DO:**
- Use third-person in description
- Include specific trigger phrases
- Keep SKILL.md lean (1,500-2,000 words)
- Use progressive disclosure
- Write in imperative form
- Reference supporting files
- Provide working examples

❌ **DON'T:**
- Use second person anywhere
- Have vague trigger conditions
- Put everything in SKILL.md
- Leave resources unreferenced
- Skip validation

## Additional Resources

### Reference Files

For detailed guidance, consult:
- **`references/protocol-specification.md`** - Complete protocol spec
- **`references/validation-checklist.md`** - Full validation checklist
- **`references/json-schemas.md`** - Schema documentation

### Example Files

Working examples in `examples/`:
- **`examples/minimal-skill/`** - Simple skill template
- **`examples/standard-skill/`** - Recommended structure
- **`examples/complete-skill/`** - Full-featured skill

### Utility Scripts

Validation tools in `scripts/`:
- **`scripts/validate-skill.py`** - Validate skill structure
- **`scripts/check-frontmatter.sh`** - Check YAML frontmatter

### JSON Schemas

Validation schemas in `assets/`:
- **`assets/skill-schema.json`** - Complete skill schema
- **`assets/skill-frontmatter-schema.json`** - Frontmatter schema
