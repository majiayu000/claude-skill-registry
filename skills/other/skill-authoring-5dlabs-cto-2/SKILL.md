---
name: skill-authoring
description: Meta-skill for creating and improving agent skills. Use when designing new skills, refining existing skills, or understanding skill architecture patterns. Provides progressive disclosure, context efficiency principles, and skill anatomy guidelines.
---

# Skill Authoring Guide

## Core Principle: Context Window is a Public Good

The context window is shared across system prompts, conversation history, skill metadata, and user requests. Challenge each piece of information:

- "Does Claude really need this explanation?"
- "Does this paragraph justify its token cost?"

**Default assumption:** Claude is already very smart. Only add context Claude doesn't already have. Prefer concise examples over verbose explanations.

## Progressive Disclosure

Skills use three-level loading to manage context efficiently:

| Level | When Loaded | Target Size | Contains |
|-------|-------------|-------------|----------|
| **Metadata** | Always in context | ~100 words | `name` + `description` in frontmatter |
| **SKILL.md body** | When skill triggers | <5k words | Core instructions, workflow |
| **Bundled resources** | As needed by Claude | Unlimited | Scripts, references, assets |

### Implications

- **Frontmatter is critical**: The `description` field is the primary trigger mechanism
- **Body is conditional**: Only loaded after triggering - don't put "when to use" info here
- **References defer complexity**: Move detailed patterns to `references/` subdirectory

## Degrees of Freedom

Match instruction specificity to task fragility and variability:

| Freedom | When to Use | Format |
|---------|-------------|--------|
| **High** | Multiple approaches valid, context-dependent decisions | Text-based instructions |
| **Medium** | Preferred pattern exists, some variation acceptable | Pseudocode or scripts with parameters |
| **Low** | Operations fragile/error-prone, consistency critical | Specific scripts, few parameters |

Think of Claude exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

## Skill Anatomy

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name + description only)
│   └── Markdown instructions
└── Optional Resources/
    ├── references/     # Documentation loaded into context as needed
    ├── scripts/        # Executable code for deterministic operations  
    └── assets/         # Files used in output (templates, icons, fonts)
```

### Frontmatter Rules

```yaml
---
name: skill-name
description: |
  What the skill does AND when to use it.
  Include trigger keywords. Be comprehensive.
  Example: "Create MCP servers for API integrations.
  Use when building tools for external services,
  implementing Model Context Protocol servers,
  or integrating APIs into agent workflows."
---
```

- **Only `name` and `description`** - No other fields
- **Description is the trigger** - Include all "when to use" information here
- **Be specific about triggers** - List contexts, keywords, and scenarios

### SKILL.md Body Guidelines

- **Under 500 lines** - Split to references/ when approaching limit
- **No "When to Use" sections** - That info belongs in frontmatter description
- **Progressive detail** - Start with quick overview, link to references for depth
- **Imperative form** - Use "Create X" not "You should create X"

### References Directory

For skills with multiple variants, frameworks, or detailed patterns:

```
cloud-deploy/
├── SKILL.md (workflow + selection guidance)
└── references/
    ├── aws.md      # AWS-specific patterns
    ├── gcp.md      # GCP-specific patterns
    └── azure.md    # Azure-specific patterns
```

When user chooses AWS, Claude only reads `aws.md` - not all variants.

### Scripts Directory

Include executable scripts when:
- Same code is rewritten repeatedly
- Deterministic reliability is required
- Operations are complex but mechanical

```python
# scripts/validate_schema.py
# Can be executed without reading into context
# Use --help pattern for black-box usage
```

## Anti-Patterns

### ❌ Don't Create

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- User-facing documentation (skills are for agents)
- Setup/testing procedures
- Deeply nested reference structures (keep one level deep)

### ❌ Don't Include

- Information Claude already knows (common libraries, basic syntax)
- Redundant explanations (say it once, well)
- Verbose variable names in examples
- Unnecessary print statements in code examples

## Writing Guidelines

### Be Concise
```markdown
❌ "In order to accomplish this task, you will need to first..."
✅ "First, create the configuration file:"
```

### Use Tables for Structured Info
```markdown
❌ "Use X for case A. Use Y for case B. Use Z for case C."
✅ | Case | Tool |
   |------|------|
   | A    | X    |
   | B    | Y    |
   | C    | Z    |
```

### Provide Minimal Examples
```markdown
❌ A 50-line example showing every possible option
✅ A 10-line example showing the core pattern
```

## Quality Checklist

Before finalizing a skill:

- [ ] **Frontmatter description** covers all trigger scenarios
- [ ] **SKILL.md body** is under 500 lines
- [ ] **No redundancy** with Claude's base knowledge
- [ ] **Progressive disclosure** - detailed info in references/
- [ ] **Degrees of freedom** match task fragility
- [ ] **No extra files** (README, CHANGELOG, etc.)
- [ ] **Examples are minimal** but complete
