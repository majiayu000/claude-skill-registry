---
name: skill-bootstrap
description: Bootstrap new skills quickly from natural language descriptions. Use when you need to create a new skill fast, generate utility capabilities, or scaffold documentation. For critical discipline-enforcing skills, follow up with skill-hardening. Triggers on "create skill", "bootstrap skill", "new skill", "generate skill".
---

# Skill Bootstrap

## Purpose

Generate new skills rapidly from natural language descriptions. This skill prioritizes speed and compliance with the official Claude Agent Skills specification over bulletproofing.

**For critical discipline-enforcing skills, use skill-hardening after bootstrapping.**

## When to Use

- Creating utility skills quickly
- Bootstrapping API wrappers or reference guides
- Generating skill scaffolding from descriptions
- Rapid prototyping of new capabilities
- Team-specific or project-specific tools

**When NOT to use:**
- Discipline-enforcing skills (use skill-hardening instead)
- Complex pattern skills requiring rigorous testing
- Skills that agents must follow under pressure

## Quick Start

```markdown
User: "Create a skill for validating JSON schemas"

You: [Use this skill to generate SKILL.md]
```

## Official Skill Format

### File Structure
```
.claude/skills/my-skill/
├── SKILL.md              # Required, uppercase
├── examples/             # Optional
│   └── usage.md
├── templates/            # Optional
│   └── template.yaml
└── scripts/              # Optional
    └── helper.py
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name-lowercase-hyphenated
description: What the skill does, when to use it, trigger keywords. Max 1024 characters.
allowed-tools: Read, Grep, Glob  # Optional: restrict tool usage
---
```

**Required fields:**
- `name`: Lowercase with hyphens
- `description`: 200-1024 characters, include what/when/triggers

**Optional fields:**
- `allowed-tools`: Comma-separated tool restrictions

**Do NOT include:**
- `version`, `category`, `activation_criteria`, `triggers` (as array)

### Description Best Practices

**Critical:** The description determines when Claude activates the skill.

**Good description:**
```yaml
description: Validate JSON documents against JSON Schema specifications. Use when working with JSON validation, API request/response validation, or data integrity checks. Supports draft-07, draft-2019-09 schemas. Triggers on "JSON schema", "validate JSON", "schema validation".
```

**Bad description:**
```yaml
description: Helps with Excel files  # Too vague
```

## Bootstrap Process

### Step 1: Parse Request
Extract:
- **Name**: lowercase-hyphenated
- **Purpose**: core functionality
- **Triggers**: keywords and use cases
- **Scope**: included/excluded

### Step 2: Generate SKILL.md

Structure:
```markdown
---
name: extracted-name
description: [Comprehensive description]
---

# Skill Name

## Purpose
Brief explanation

## When to Use
- Use case 1
- Use case 2

## Core Instructions
Step-by-step guidance

### Patterns and Examples
Code examples

## Dependencies (Optional)
Required tools/libraries

## Version
v1.0.0
```

### Step 3: Evaluate Supporting Files

Create only if they add significant value:
- `examples/` → for detailed usage patterns
- `templates/` → for reusable structures
- `scripts/` → for helper utilities

Use progressive disclosure:
```markdown
For examples, see [examples/usage.md](examples/usage.md)
```

### Step 4: Validate

Check:
- ✓ SKILL.md exists (uppercase)
- ✓ Frontmatter has `name` and `description`
- ✓ Description is 200-1024 characters
- ✓ No invalid frontmatter fields
- ✓ Supporting files referenced correctly

## Tool Restrictions (allowed-tools)

Use when you want to restrict Claude's tools:

```yaml
---
name: safe-file-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

**When to use:**
- Read-only skills
- Safety-critical workflows
- Limited-scope operations

## After Bootstrapping

### For Utility Skills
Deploy and use. Monitor for issues.

### For Discipline-Enforcing Skills
**Required:** Use skill-hardening to bulletproof the skill with TDD.

```markdown
⚠️ This skill enforces discipline. Run skill-hardening to test it:
- Create pressure scenarios
- Verify agents comply under stress
- Close loopholes
```

## Example: Simple Skill

**Request:** "Create a skill for validating JSON schemas"

**Generated SKILL.md:**
```markdown
---
name: json-schema-validator
description: Validate JSON documents against JSON Schema specifications. Use when working with JSON validation, API request/response validation, configuration file validation, or data integrity checks. Supports draft-07, draft-2019-09, and draft-2020-12 schemas. Triggers on "JSON schema", "validate JSON", "schema validation", "JSON structure check".
---

# JSON Schema Validator

## Purpose
Validate JSON documents against JSON Schema specifications.

## When to Use
- Validating API payloads
- Checking configuration files
- Data integrity verification

## Core Instructions

1. **Identify Schema**: Locate the JSON Schema
2. **Load JSON**: Read the document to validate
3. **Validate**: Compare against schema rules
4. **Report**: List validation errors with paths

### Basic Validation Pattern

```python
import jsonschema
import json

def validate_json(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, "Valid"
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)
```

## Dependencies
- Python 3.7+
- jsonschema library

## Version
v1.0.0
```

## Example: Multi-File Skill

**Request:** "Create a skill for API testing with examples"

**Generated structure:**
```
.claude/skills/api-testing/
├── SKILL.md
├── examples/
│   └── rest-api-example.md
└── templates/
    └── test-template.yaml
```

## Best Practices

### Keep It Minimal
- Don't create files just because you can
- Each supporting file should add value
- Examples should teach, not overwhelm

### Description Writing
- Start with action verbs: "Analyze", "Generate", "Transform"
- Include specific file types: ".xlsx", ".json", ".py"
- List concrete use cases
- End with explicit triggers

### Progressive Disclosure
Supporting files load on-demand. Reference them:
```markdown
See [examples/usage.md](examples/usage.md) for detailed examples.
```

## Integration with Other Skills

| Next Step | When | Skill |
|-----------|------|-------|
| Test & bulletproof | Discipline-enforcing skills | skill-hardening |
| Extract from session | After using skill in real work | skill-extract-pattern |
| Evolve with metrics | Based on usage feedback | skill-evolve |

## Version

v1.0.0 (2025-01-28) - Bootstrap-focused refactor of skill-creator