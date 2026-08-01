---
name: commands-fltman-project-scaffolder
description: Create a new Agent Skill for specialized tasks.
---

# Create a New Agent Skill

Create a new Agent Skill for specialized tasks.

## Arguments

$ARGUMENTS should contain: `<skill-name> [description]`

## What is a Skill?

A Skill is a folder containing:
- `SKILL.md` - Main instructions with YAML frontmatter
- Optional scripts and resources
- Optional reference documentation

Skills use **progressive disclosure**: only the name and description are loaded initially. The full skill content is loaded when relevant.

## Skill Creation Process

### Step 1: Gather Information

Ask the user:
1. **Skill name**: Short, descriptive (e.g., "pdf-forms", "api-testing")
2. **Purpose**: What task does this skill help with?
3. **When to use**: What triggers should activate this skill?
4. **Required tools**: Any external dependencies?

### Step 2: Create Skill Directory

```
skills/<skill-name>/
├── SKILL.md           # Main skill file
├── scripts/           # Optional helper scripts
│   └── helper.py
└── resources/         # Optional templates/examples
    └── template.md
```

### Step 3: Generate SKILL.md

Create with this structure:

```markdown
---
name: <skill-name>
description: <brief one-line description for discovery>
---

# <Skill Name>

## When to Use This Skill

<Clear description of when Claude should activate this skill>

## Prerequisites

<List any required tools, dependencies, or setup>

## Instructions

### Step 1: <First Step>
<Detailed instructions>

### Step 2: <Second Step>
<Detailed instructions>

...

## Reference Files

<Point to any additional documentation or scripts>

## Examples

### Example 1: <Common Use Case>
<Input/output examples>

## Verification

<How to verify the skill worked correctly>
```

### Step 4: Progressive Disclosure Tips

Structure the SKILL.md for progressive disclosure:
1. **Top section**: Most commonly needed info
2. **Middle sections**: Detailed procedures
3. **Bottom sections**: Edge cases and examples
4. **Separate files**: Rarely-used reference material

### Step 5: Test the Skill

1. Simulate a task that should trigger the skill
2. Verify Claude loads the skill appropriately
3. Check that instructions are clear and complete
4. Iterate based on observed behavior

## Skill Best Practices

1. **Keep it focused**: One skill = one capability
2. **Be specific**: Clear trigger conditions
3. **Include verification**: How to check success
4. **Use code wisely**: Scripts can be tools OR documentation
5. **Think from Claude's perspective**: What info does Claude need?

## Output

Create the skill directory and files, then provide:
- Summary of what was created
- How to test the skill
- Suggestions for improvement
