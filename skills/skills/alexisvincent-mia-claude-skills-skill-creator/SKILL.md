---
name: skill-creator
description: Creates and improves Claude Code skills using best practices. Use when user wants to build, modify, or enhance a skill. Guides through skill architecture, progressive disclosure, workflow design, and testing patterns.
---

# Skill Creator

Create high-quality skills that extend Claude's capabilities using best practices for conciseness, progressive disclosure, and testability.

## When to Use This Skill

Invoke this skill when:
- Creating a new skill from scratch
- Improving an existing skill's structure or content
- Reviewing a skill for best practices compliance
- Troubleshooting skill performance issues
- Planning skill architecture before implementation

## Quick Start Workflow

Follow this checklist for creating a new skill:

### 1. Understand the Need
- [ ] Document 2-3 concrete usage examples of the skill in action
- [ ] Identify what Claude needs to know vs. what can be external references
- [ ] Determine if scripts, templates, or other assets are needed
- [ ] Assess task fragility (high freedom vs. low freedom needed)

### 2. Plan the Structure
- [ ] Choose skill name (gerund form: `doing-something`, max 64 chars, lowercase/hyphens)
- [ ] Write description (what it does + when to use, max 1024 chars)
- [ ] List required reference files for detailed content
- [ ] Identify reusable assets (templates, boilerplate, etc.)
- [ ] Plan any utility scripts for deterministic operations

### 3. Initialize Skill Structure

Use the init_skill.py script to scaffold your new skill:

```bash
cd .claude/skills/skill-creator/scripts
./init_skill.py your-skill-name --path /path/to/skills
```

This creates:
```
your-skill-name/
├── SKILL.md              # Template with TODOs and structural guidance
├── references/           # Example reference documentation
│   └── api_reference.md
├── assets/              # Example asset placeholder
│   └── example_asset.txt
└── scripts/             # Example script
    └── example.py
```

The script provides a comprehensive template with:
- Structural pattern guidance (workflow-based, task-based, reference-based, capabilities-based)
- Example files showing best practices
- TODOs marking sections to customize
- Resource organization examples

### 4. Customize SKILL.md

The generated SKILL.md includes inline guidance:

- [ ] Complete the description in YAML frontmatter (what + when to use)
- [ ] Choose appropriate structural pattern for your skill (delete guidance section when done)
- [ ] Replace placeholder sections with actual content
- [ ] Add workflows, examples, and references as needed
- [ ] Delete example files in scripts/, references/, and assets/ if not needed

### 5. Apply Best Practices
- [ ] Keep SKILL.md under 500 lines (move details to references)
- [ ] Use imperative language ("Do this" not "You should do")
- [ ] Include validation steps before making changes
- [ ] Provide both flexible guidance and strict templates where appropriate
- [ ] Add clear success criteria for each workflow step

### 6. Validate and Test

Run the validation script to check your skill structure:

```bash
cd .claude/skills/skill-creator/scripts
./quick_validate.py /path/to/your-skill-name
```

The validator checks:
- SKILL.md exists and has valid YAML frontmatter
- Required fields (name, description) are present
- Name follows hyphen-case convention (lowercase, hyphens, digits only)
- Description doesn't contain invalid characters

Then test with real usage:
- [ ] Create test scenarios before extensive documentation
- [ ] Test with different model sizes if relevant (Opus vs. Haiku)
- [ ] Verify progressive disclosure works (references load only when needed)
- [ ] Gather real-world usage feedback

### 7. Package for Distribution (Optional)

To create a distributable zip file:

```bash
cd .claude/skills/skill-creator/scripts
./package_skill.py /path/to/your-skill-name [output-directory]
```

This will:
- Validate the skill structure
- Create a compressed zip file
- Include all skill files (SKILL.md, references, assets, scripts)

The packaged skill can be shared with others or backed up.

## Best Practices Quick Reference

Key principles: **conciseness**, **progressive disclosure**, and **matching specificity to task fragility**.

For comprehensive guidance, see [[references/best-practices.md]].

## Common Patterns

### Plan-Validate-Execute Pattern
```markdown
1. Analyze requirements and create a plan
2. Show plan to user for validation
3. Execute after approval
4. Verify results and report completion
```

### Progressive Reference Loading
```markdown
## Overview
Brief summary here.

## Detailed Guide
For full implementation details, see [[references/implementation.md]].

## Examples
Review [[references/examples.md]] for common patterns.
```

### Script Integration
```markdown
## Running Analysis
Execute the analysis script:
```bash
./scripts/analyze.sh input.txt
```
Review output, then proceed with recommended changes.
```

## Reference Files

Load these on-demand for detailed guidance:

- [[references/best-practices.md]] - Comprehensive best practices guide
- [[references/structure-guide.md]] - Detailed structure and architecture patterns
- [[references/examples.md]] - Real-world skill examples and templates

## Anti-Patterns to Avoid

❌ **Don't**: Include extensive documentation in SKILL.md
✅ **Do**: Move details to reference files

❌ **Don't**: Use passive voice or vague language
✅ **Do**: Use imperative, actionable instructions

❌ **Don't**: Create deeply nested file references
✅ **Do**: Keep all references one level deep from SKILL.md

❌ **Don't**: Generate code for deterministic operations
✅ **Do**: Provide pre-made scripts for consistency

❌ **Don't**: Build skills for anticipated problems
✅ **Do**: Create test scenarios first, solve real problems

## Skill Quality Checklist

Before finalizing a skill, verify:

- [ ] Name follows gerund form and naming conventions
- [ ] Description explains both what and when (<1024 chars)
- [ ] SKILL.md is under 500 lines
- [ ] Detailed content moved to reference files
- [ ] Workflows include validation steps
- [ ] Clear success criteria provided
- [ ] Templates provided for format-critical outputs
- [ ] Scripts used for deterministic operations
- [ ] Tested with concrete examples
- [ ] Progressive disclosure working correctly

## Getting Help

For questions about skill architecture or best practices:
1. Use `./scripts/init_skill.py` to scaffold a new skill with templates
2. Review [[references/best-practices.md]] for comprehensive guidance
3. Check [[references/examples.md]] for real-world patterns
4. Run `./scripts/quick_validate.py` to validate your skill structure

---

*This skill helps you create skills that are concise, actionable, and optimized for Claude's context window through progressive disclosure.*
