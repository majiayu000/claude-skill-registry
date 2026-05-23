---
name: skill-generate
description: Create well-structured Agent Skills with proper formatting, best practices, and validation. Use when the user wants to create a new skill, needs help structuring skills, or wants to improve existing skills.
---

# Skill Generator

Generate well-structured, effective Agent Skills following Anthropic's best practices and guidelines.

## Quick Start

When asked to create a skill, I will:
1. Gather requirements and understand the skill's purpose
2. Generate proper YAML frontmatter with name and description
3. Structure instructions using progressive disclosure
4. Include relevant examples and templates
5. Validate the skill structure

## Skill Creation Process

### Step 1: Requirements Gathering

First, determine:
- **Purpose**: What specific task should this skill accomplish?
- **Triggers**: When should Claude use this skill?
- **Resources**: What files, scripts, or references are needed?
- **Complexity**: Is this a simple instruction set or does it need bundled resources?

### Step 2: Generate Structure

Create the skill following this template:

```markdown
---
name: skill-name-here  # lowercase, hyphens only, max 64 chars
description: Brief explanation of what this skill does and specific triggers for when Claude should use it. Include keywords users might mention.
---

# Skill Name

## Overview
[Brief introduction to what this skill accomplishes]

## Quick Start
[Immediate, most common use case with minimal setup]

## Core Instructions

### Primary Workflow
1. [Step-by-step instructions]
2. [Clear, actionable guidance]
3. [Expected outcomes]

### Key Principles
- [Important guidelines to follow]
- [Best practices specific to this domain]
- [Common pitfalls to avoid]

## Examples

### Example 1: [Common Use Case]
```[language]
[Concrete example code or instructions]
```

### Example 2: [Advanced Use Case]
```[language]
[More complex example]
```

## Advanced Usage
[Optional: Complex workflows, edge cases, or specialized features]

## Resources
[Optional: Reference to bundled scripts, templates, or documentation]

## Troubleshooting
[Optional: Common issues and solutions]
```

### Step 3: Apply Best Practices

#### Naming Conventions
- **Name**: Use lowercase letters, numbers, and hyphens only
- **Length**: Maximum 64 characters
- **Format**: `domain-action` or `tool-purpose` (e.g., `pdf-processing`, `api-testing`)
- **Avoid**: Reserved words like "anthropic", "claude", XML tags

#### Description Guidelines
- **Length**: Maximum 1024 characters
- **Content**: Include both WHAT the skill does and WHEN to use it
- **Keywords**: Include terms users might naturally say
- **Examples of good descriptions**:
  - "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
  - "Generate unit tests for JavaScript/TypeScript code. Use when the user asks for test creation, mentions testing, or needs test coverage improvement."

#### Progressive Disclosure Structure
- **Level 1 (Metadata)**: Keep frontmatter concise (~100 tokens)
- **Level 2 (Main Instructions)**: Core SKILL.md content (aim for under 5k tokens)
- **Level 3 (Resources)**: Additional files loaded only when needed

### Step 4: Add Supporting Resources

For complex skills, create additional resources:

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── templates/         # Reusable templates
│   └── template.md
├── scripts/           # Executable utilities
│   └── helper.py
├── examples/          # Reference implementations
│   └── example.md
└── docs/              # Additional documentation
    └── advanced.md
```

### Step 5: Validate the Skill

Run validation checks:
```python
# Use the validate_skill.py script
python scripts/validate_skill.py /path/to/skill
```

## Templates Library

### Basic Instructional Skill
For skills that provide guidance without code execution:
```bash
cat templates/basic-instruction.md
```

### Code Execution Skill
For skills that run scripts and process data:
```bash
cat templates/code-execution.md
```

### Document Processing Skill
For skills that work with files and formats:
```bash
cat templates/document-processing.md
```

### API Integration Skill
For skills that interact with external services:
```bash
cat templates/api-integration.md
```

## Common Patterns

### Pattern 1: Conditional Instructions
```markdown
## Workflow
1. Check if [condition]
   - If true: [action A]
   - If false: [action B]
2. Continue with [next step]
```

### Pattern 2: Resource References
```markdown
## Implementation
Follow the approach in [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed steps.

For configuration options, see [CONFIG.md](CONFIG.md).
```

### Pattern 3: Script Execution
```markdown
## Automated Processing
Run the processing script:
```bash
python scripts/process.py --input file.txt --output result.json
```
The script handles validation and error checking automatically.
```

## Validation Checklist

Before finalizing a skill, verify:

- [ ] YAML frontmatter is valid with required fields
- [ ] Name follows conventions (lowercase, hyphens, <64 chars)
- [ ] Description explains what AND when (<1024 chars)
- [ ] Instructions are clear and actionable
- [ ] Examples are concrete and tested
- [ ] File paths in skill use relative references
- [ ] Scripts are executable and documented
- [ ] No XML tags in name or description
- [ ] No reserved words used
- [ ] Resources are organized logically

## Output Format

When generating a skill, I will:
1. Create the complete SKILL.md file content
2. Suggest any additional resource files if needed
3. Provide installation/usage instructions
4. Validate against the checklist

## Examples of Generated Skills

### Example 1: Simple Instruction Skill
```bash
cat examples/code-review-skill.md
```

### Example 2: Complex Resource-Based Skill
```bash
cat examples/data-pipeline-skill.md
```

### Example 3: Interactive Workflow Skill
```bash
cat examples/user-interview-skill.md
```

## Best Practices Reminders

1. **Start Simple**: Begin with core functionality, add complexity later
2. **Be Specific**: Clear triggers help Claude know when to use the skill
3. **Test Thoroughly**: Validate with real use cases
4. **Document Well**: Include examples for every major feature
5. **Optimize Loading**: Keep frequently-used content in SKILL.md
6. **Security First**: Never include sensitive data or credentials
7. **Version Control**: Track changes and improvements
8. **User Feedback**: Iterate based on actual usage patterns