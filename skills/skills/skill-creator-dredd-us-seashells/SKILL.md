---
name: skill-creator
description: Meta-skill to generate new Claude Agent Skills from natural-language descriptions. Use when creating skills, building custom workflows, generating new capabilities, or extending Claude's functionality. Outputs complete SKILL.md files with proper frontmatter (name, description, optional allowed-tools) and clear instructions. Handles multi-file skills with progressive disclosure patterns. Triggers on requests to "create skill", "build skill", "generate skill", or "new capability".
---

# Skill Creator Meta-Skill

## Purpose

Generate new Claude Agent Skills from natural-language descriptions following the official Claude Agent Skills specification. This skill ensures all generated skills are compliant with the official spec, use proper frontmatter, and follow best practices.

## When to Use

Use this skill when you need to:
- Create new skills for specific domains or workflows
- Expand your skill toolkit with custom patterns
- Bootstrap specialized capabilities
- Build team-specific or project-specific skills
- Convert existing patterns into reusable skills

## Official Skill Format

All generated skills MUST follow this structure:

### File Structure
```
.claude/skills/my-skill/
├── SKILL.md (required, uppercase)
├── examples/ (optional)
│   └── usage.md
├── templates/ (optional)
│   └── template.yaml
└── scripts/ (optional)
    └── helper.py
```

### SKILL.md Frontmatter Format

The frontmatter is YAML between `---` markers at the top of SKILL.md:

```yaml
---
name: skill-name-lowercase-hyphenated
description: Comprehensive description of what the skill does, when to use it, and trigger keywords users would mention. Include specific use cases and context. Max 1024 characters.
allowed-tools: Read, Grep, Glob  # Optional: restrict tool usage
---
```

**Required fields:**
- `name`: Lowercase with hyphens (e.g., `api-integrator`, `plan-execute`)
- `description`: Comprehensive 200-1024 character description

**Optional fields:**
- `allowed-tools`: Comma-separated list of allowed tools (e.g., `Read, Grep, Glob, Write`)

**IMPORTANT - Do NOT include these fields (they're not in the official spec):**
- ❌ `activation_criteria`
- ❌ `token_estimate`
- ❌ `version`
- ❌ `category`
- ❌ `triggers` (as array)
- ❌ `confidence`
- ❌ `token_budget`

### Description Best Practices

The description is THE MOST CRITICAL field. It determines when Claude activates the skill.

**Include these elements:**
1. **WHAT**: What the skill does
2. **WHEN**: When to use it
3. **TRIGGERS**: Keywords users would mention
4. **CONTEXT**: Specific use cases or scenarios

**Good description example:**
```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts, and extract data from .xlsx files. Use when working with Excel files, spreadsheets, data analysis, tabular data, or financial reports. Handles formulas, multi-sheet workbooks, and data validation. Triggers on "Excel", "spreadsheet", ".xlsx", "pivot table", "chart".
```

**Bad description example (too vague):**
```yaml
description: Helps with Excel files
```

### SKILL.md Body Structure

After the frontmatter, include these sections:

```markdown
# Skill Name

## Purpose
Brief explanation of what this skill accomplishes.

## When to Use
Specific scenarios where this skill should be activated:
- Use case 1
- Use case 2
- Use case 3

## Core Instructions
Detailed step-by-step instructions for Claude to follow:

1. **Step 1**: What to do
2. **Step 2**: How to do it
3. **Step 3**: Validation or output

### Patterns and Examples
Code examples or patterns to follow.

## Progressive Disclosure (Optional)
If you have supporting files, reference them:

For more examples, see [examples/usage.md](examples/usage.md).

For templates, see [templates/template.yaml](templates/template.yaml).

Run helper scripts:
```bash
python scripts/helper.py
```

Claude loads these files only when the link is followed or script is referenced.

## Dependencies (Optional)
List any required tools, libraries, or environment:
- Python 3.8+
- Required packages: requests, pydantic
- Optional: jq for JSON processing

## Best Practices (Optional)
- Best practice 1
- Best practice 2

## Version
v1.0.0 (2025-10-23)
```

## Tool Restrictions (allowed-tools)

Use `allowed-tools` when you want to restrict which tools Claude can use when this skill is active:

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use for read-only analysis, code review, or when you need to examine files without modification.
allowed-tools: Read, Grep, Glob
---
```

When this skill activates, Claude can ONLY use Read, Grep, and Glob - no Write, Delete, or other tools.

**When to use tool restrictions:**
- Read-only skills (analysis, review)
- Safety-critical workflows
- Limited-scope operations
- Testing or dry-run scenarios

**Available tool names:**
Read, Write, Grep, Glob, Delete, and other standard tools (check Claude Code documentation for full list)

## Multi-File Skills with Progressive Disclosure

Supporting files are loaded on-demand to save tokens:

### Create Supporting Files

**examples/usage.md** - Usage examples:
```markdown
# Usage Examples

## Example 1: Basic Usage
[Detailed example]

## Example 2: Advanced Usage
[Complex example with edge cases]
```

**templates/template.yaml** - Reusable templates:
```yaml
# Template for common pattern
task:
  name: "template-name"
  steps:
    - action: "do something"
```

**scripts/helper.py** - Helper scripts:
```python
#!/usr/bin/env python3
"""
Helper script for skill operations
"""

def process_data(input_file):
    # Implementation
    pass
```

### Reference from SKILL.md

```markdown
## Examples

See [examples/usage.md](examples/usage.md) for detailed examples.

## Templates

Use the template in [templates/template.yaml](templates/template.yaml).

## Helper Scripts

Run the helper script:
```bash
python scripts/helper.py input.txt
```
```

Claude loads these files only when needed, keeping initial token usage low.

## Skill Generation Process

When generating a new skill:

### Step 1: Parse User Description
Extract:
- **Name**: Convert to lowercase-hyphenated format
- **Purpose**: Core functionality
- **Triggers**: Keywords and use cases
- **Scope**: What's included/excluded

### Step 2: Write Description
Create comprehensive 200-1024 character description including:
- What the skill does
- When to use it
- Trigger keywords
- Specific contexts/scenarios

### Step 3: Structure SKILL.md
```markdown
---
name: extracted-name
description: [Comprehensive description from Step 2]
---

[Rest of skill body]
```

### Step 4: Add Core Instructions
Write clear, actionable instructions:
- Step-by-step processes
- Decision trees for complex logic
- Examples showing expected patterns
- Error handling guidance

### Step 5: Evaluate Supporting Files
Ask yourself:
- Do examples help? → Create examples/
- Are templates needed? → Create templates/
- Do scripts add value? → Create scripts/
- Keep it minimal - don't over-engineer

### Step 6: Reference Supporting Files
Use progressive disclosure:
```markdown
For advanced usage, see [examples/advanced.md](examples/advanced.md).
```

### Step 7: Validate
Check:
- ✓ SKILL.md (uppercase) exists
- ✓ Frontmatter has `name` and `description`
- ✓ Description is 200-1024 chars
- ✓ No invalid frontmatter fields
- ✓ Instructions are clear and actionable
- ✓ Supporting files are referenced correctly

## Generation Examples

### Example 1: Simple Skill (No Supporting Files)

**User request:** "Create a skill for validating JSON schemas"

**Generated SKILL.md:**
```markdown
---
name: json-schema-validator
description: Validate JSON documents against JSON Schema specifications. Use when working with JSON validation, API request/response validation, configuration file validation, or data integrity checks. Supports draft-07, draft-2019-09, and draft-2020-12 schemas. Triggers on "JSON schema", "validate JSON", "schema validation", "JSON structure check".
---

# JSON Schema Validator

## Purpose
Validate JSON documents against JSON Schema specifications to ensure data integrity and structure compliance.

## When to Use
- Validating API request/response payloads
- Checking configuration files
- Data integrity verification
- Schema compliance testing

## Core Instructions

1. **Identify Schema**: Locate or receive the JSON Schema specification
2. **Load JSON**: Read the JSON document to validate
3. **Validate**: Compare JSON against schema rules
4. **Report**: List all validation errors with paths and messages

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

### Example 2: Multi-File Skill

**User request:** "Create a skill for API testing with examples and templates"

**Generated structure:**
```
.claude/skills/api-testing/
├── SKILL.md
├── examples/
│   └── rest-api-example.md
└── templates/
    └── test-template.yaml
```

**SKILL.md:**
```markdown
---
name: api-testing
description: Test REST and GraphQL APIs with automated request generation, response validation, and performance measurement. Use when testing APIs, validating endpoints, checking response schemas, or measuring API performance. Supports authentication (Bearer, Basic, OAuth), rate limiting, and retry logic. Triggers on "API test", "test endpoint", "API validation", "REST test", "GraphQL query".
allowed-tools: Read, Write, Grep
---

# API Testing Skill

## Purpose
Comprehensive API testing with request generation, validation, and performance metrics.

## When to Use
- Testing REST or GraphQL endpoints
- Validating API responses
- Performance benchmarking
- Integration testing
- CI/CD pipeline testing

## Core Instructions

[... detailed instructions ...]

## Examples

See [examples/rest-api-example.md](examples/rest-api-example.md) for complete examples.

## Templates

Use [templates/test-template.yaml](templates/test-template.yaml) as a starting point.

## Version
v1.0.0
```

**examples/rest-api-example.md:**
```markdown
# REST API Testing Examples

## Example 1: GET Request with Auth
[Detailed example]

## Example 2: POST with Validation
[Detailed example]
```

**templates/test-template.yaml:**
```yaml
api_test:
  endpoint: "https://api.example.com/resource"
  method: "GET"
  auth:
    type: "Bearer"
    token: "${API_TOKEN}"
  expect:
    status: 200
    schema: "response-schema.json"
```

## Meta-Loop Protection

If asked to create a skill-creator skill:
```
"This is the skill-creator skill. It already exists. Did you mean to:
1. Update this skill?
2. Create a different meta-skill?
3. Extend this skill with new capabilities?"
```

## Best Practices

### For Simple Skills
- Single SKILL.md file
- Clear, concise instructions
- 1-3 code examples
- No supporting files unless truly valuable

### For Complex Skills
- SKILL.md with core instructions
- examples/ for detailed usage patterns
- templates/ for reusable structures
- scripts/ ONLY if demonstrating non-obvious patterns

### Description Writing
- Start with action verbs: "Analyze", "Generate", "Transform"
- Include specific file types: ".xlsx", ".json", ".py"
- List concrete use cases
- Add domain terms: "API", "database", "spreadsheet"
- End with explicit triggers: "Use when [scenario]"

### Keep It Minimal
- Don't create files just because you can
- Each supporting file should add significant value
- Scripts should show patterns, not be production tools
- Examples should teach, not overwhelm

## Testing Generated Skills

After generating a skill:

1. **Syntax check**: Validate YAML frontmatter
2. **Description check**: 200-1024 characters
3. **Activation test**: Create prompt with triggers
4. **Instruction test**: Follow the instructions manually
5. **Supporting files**: Verify all references work

## Version

v1.0.0 (2025-10-23) - Official Claude Agent Skills Specification

