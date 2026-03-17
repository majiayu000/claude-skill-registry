---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

Interactive guide for creating high-quality Claude skills.

## When to Use This Skill

Use this skill when:
- User wants to create a new Claude skill
- User wants to update or improve an existing skill  
- User needs guidance on skill structure and best practices
- User wants to extend Claude's capabilities for specific workflows

## Skill Structure

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/ - Executable code (Python/Bash/etc.)
    ├── references/ - Documentation loaded into context as needed
    └── assets/ - Files used in output (templates, icons, fonts, etc.)
```

## Required Components

###  Frontmatter (YAML)

```yaml
---
name: my-skill-name
description: A clear, comprehensive description of what this skill does and when to use it
---
```

**Critical**: The `description` field is how Claude determines when to use the skill. Be specific and comprehensive about:
- What the skill does
- When it should be used
- What types of queries trigger it
- What output it produces

### Body (Markdown)

The markdown content contains:
- **Instructions**: Step-by-step guidance for using the skill
- **Examples**: Concrete usage examples
- **Guidelines**: Best practices and rules
- **Workflows**: Detailed procedures

## Optional Bundled Resources

### 1. scripts/

**When to include**: When the skill needs executable code

**Examples**:
- `scripts/analyzer.py` - Python data analysis script
- `scripts/formatter.sh` - Bash formatting utility
- `scripts/validator.js` - JavaScript validation tool

**Rules**:
- Must be tested before inclusion
- Should be well-documented
- Include error handling

### 2. references/

**When to include**: When the skill needs detailed reference material that shouldn't bloat SKILL.md

**Examples**:
- `references/schema.md` - Database schema documentation
- `references/api-spec.md` - API endpoint reference
- `references/examples.md` - Extended examples

**Rules**:
- Move detailed info here, keep SKILL.md lean
- Avoid duplication between SKILL.md and references/
- Use for schemas, specs, detailed examples

### 3. assets/

**When to include**: When the skill needs files used in output

**Examples**:
- `assets/logo.png` - Brand assets
- `assets/template.pptx` - PowerPoint templates
- `assets/boilerplate/` - HTML/React starter code
- `assets/fonts/` - Custom typography

**Rules**:
- Only for files used in final output
- Not for documentation (use references/ instead)
- Templates, images, icons, boilerplate code

## Creation Workflow

### Step 1: Analyze the Use Case

Ask clarifying questions:
1. What specific task will this skill handle?
2. What are 3-5 concrete examples of user queries?
3. What makes this task repetitive or specialized?
4. What context or knowledge is required?
5. Are there existing tools/APIs to integrate?

### Step 2: Identify Reusable Resources

For each concrete example, identify:
- Scripts that would be helpful
- Reference documentation needed
- Assets/templates to include

### Step 3: Create the Structure

1. Start with SKILL.md frontmatter
2. Write clear, comprehensive description
3. Add instruction sections
4. Create scripts/ if needed
5. Add references/ for detailed docs
6. Include assets/ for templates

### Step 4: Test the Skill

1. Test all scripts to ensure they work
2. Verify references are complete
3. Check assets are properly formatted
4. Validate SKILL.md instructions are clear

## Best Practices

### Description Writing

✅ **Good description**:
"Analyzes Brevard County foreclosure auctions using 12-stage pipeline. Searches AcclaimWeb for liens, calculates max bid using ARV formula, generates BID/REVIEW/SKIP recommendations. Use when analyzing foreclosure properties, calculating max bids, or generating auction reports."

❌ **Bad description**:
"Helps with foreclosure analysis"

### Instruction Writing

- Be specific and actionable
- Include concrete examples
- Define workflows step-by-step
- Explain when to use vs not use
- Provide success criteria

### Resource Organization

- Keep SKILL.md focused on procedures
- Move detailed docs to references/
- Test all scripts before inclusion
- Organize assets logically

## Common Skill Patterns

### 1. Domain Expert Skill
Focus: Specialized knowledge in a field
Resources: references/ with domain docs, examples
Example: foreclosure-analysis, medical-coding

### 2. Workflow Automation Skill
Focus: Repeatable multi-step processes
Resources: scripts/ for automation, templates in assets/
Example: git-workflow, deployment-checklist

### 3. Integration Skill
Focus: Using external APIs/tools
Resources: references/ with API docs, scripts/ for API calls
Example: stripe-integration, supabase-setup

### 4. Template/Boilerplate Skill
Focus: Starting points for projects
Resources: assets/ with templates, references/ with docs
Example: react-boilerplate, brand-guidelines

## Examples

See the following skills as references:
- **frontend-design**: Creative workflow with aesthetic guidelines
- **mcp-builder**: Technical integration with detailed specs
- **docx**: Complex file manipulation with scripts
- **brand-guidelines**: Assets and references combination
