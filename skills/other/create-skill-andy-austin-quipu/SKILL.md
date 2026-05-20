---
name: create-skill
description: Guide for creating well-structured Claude Code skills with proper YAML frontmatter, focused descriptions, and supporting files. Use when the user wants to create a new skill, build a custom skill, extend Claude's capabilities, or mentions creating/designing/building skills.
---

# Create Skill Guide

This skill helps you create new Claude Code skills following official best practices and standards.

## Quick Start

When creating a new skill, follow this workflow:

1. **Understand the requirement** - Ask clarifying questions about the skill's purpose
2. **Choose location** - Determine if this is personal (~/.claude/skills/) or project (.claude/skills/)
3. **Create directory structure** - Set up skill directory with SKILL.md and supporting files
4. **Write SKILL.md** - Follow the format below
5. **Test activation** - Verify the skill activates with appropriate user prompts

## SKILL.md Format

Every skill requires a SKILL.md file with this structure:

```markdown
---
name: skill-name-here
description: Brief description of what this skill does and when to use it (include trigger terms)
---

# Skill Title

Main skill instructions go here in Markdown format.
```

### Frontmatter Requirements

**Required fields:**
- `name`: Lowercase letters, numbers, hyphens only (max 64 characters)
- `description`: What the skill does AND when to use it (max 1024 characters)

**Optional fields:**
- `allowed-tools`: Comma-separated list to restrict tool access (e.g., "Read, Grep, Glob")

### Description Best Practices

Write descriptions that help Claude discover when to activate the skill:

**GOOD - Specific with trigger terms:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**BAD - Too vague:**
```yaml
description: Helps with documents
```

**Key principles:**
- Include both WHAT the skill does and WHEN to use it
- Mention specific file types, workflows, or keywords users might say
- Add trigger terms that distinguish this skill from similar ones
- Be specific enough for Claude to autonomously decide to use it

## Directory Structure Examples

### Simple Skill (Instructions Only)
```
skill-name/
└── SKILL.md
```

### Complex Skill (With Supporting Files)
```
skill-name/
├── SKILL.md
├── reference.md          # Additional documentation
├── examples.md          # Usage examples
├── scripts/
│   ├── helper.py
│   └── utilities.sh
└── templates/
    ├── template.txt
    └── sample.json
```

## Referencing Supporting Files

Use relative paths within SKILL.md:

```markdown
For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt
```

Use this template: [template.txt](templates/template.txt)
```

Claude loads supporting files progressively as needed to manage context efficiently.

## Tool Restrictions

Restrict which tools Claude can use when the skill is active:

```yaml
---
name: read-only-analyzer
description: Analyze code without making changes
allowed-tools: Read, Grep, Glob, Bash
---
```

This is useful for:
- Security-sensitive workflows (read-only access)
- Limited-scope skills (prevent unintended modifications)
- Ensuring permission-free execution

## Skill Locations

**Personal skills** (`~/.claude/skills/`):
- Available across all projects
- Private to your machine
- Not version controlled

**Project skills** (`.claude/skills/`):
- Shared with team via git
- Project-specific capabilities
- Automatically available when teammates pull changes

**Plugin skills**:
- Bundled with installed plugins
- Recommended for distribution

## Creation Checklist

When creating a new skill, ensure:

- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] Name uses only lowercase, numbers, and hyphens
- [ ] Description includes BOTH what it does AND when to use it
- [ ] Description mentions specific trigger terms/keywords
- [ ] Description is under 1024 characters
- [ ] Supporting files use Unix-style paths (forward slashes)
- [ ] Instructions are clear and actionable
- [ ] Tool restrictions are appropriate (if specified)
- [ ] Directory is in correct location (personal vs project)

## Testing Your Skill

After creating a skill:

1. **Restart Claude Code** - Changes require restart to take effect
2. **Test activation** - Use trigger terms from description to verify Claude activates it
3. **Check debug mode** - Run `claude --debug` to see loading errors
4. **Verify instructions** - Ensure the skill produces expected results

## Common Issues

**Skill not activating:**
- Description too vague - add specific trigger terms
- Wrong file location - verify path matches ~/.claude/skills/ or .claude/skills/
- Invalid YAML - check frontmatter syntax (opening/closing ---, proper indentation)

**Supporting files not found:**
- Use Unix-style paths (forward slashes)
- Verify relative paths are correct from SKILL.md location
- Check file permissions

**Tool access denied:**
- Review `allowed-tools` restrictions
- Consider if restrictions are too limiting
- Remove field entirely to allow all tools

## Version History Template

Include in your SKILL.md for tracking changes:

```markdown
## Version History

### v1.0.0 (2025-10-30)
- Initial release
- Core functionality for X, Y, Z

### v1.1.0 (2025-11-15)
- Added support for feature A
- Fixed bug in B
- Updated documentation
```

## Sharing Skills

**Best practice**: Distribute via plugins for team access

**Project sharing**:
1. Create skill in `.claude/skills/skill-name/`
2. Commit to git
3. Team members automatically get access on pull

## Key Principles

1. **One skill, one purpose** - Keep skills focused on specific capabilities
2. **Descriptive names** - Use clear, searchable names
3. **Trigger-rich descriptions** - Include keywords users would naturally say
4. **Progressive disclosure** - Use supporting files for complex details
5. **Unix conventions** - Always use forward slashes in paths
6. **Test thoroughly** - Verify activation with real user prompts

## Example: Creating a PDF Processing Skill

```yaml
---
name: pdf-processor
description: Extract text and tables from PDF files, fill forms, merge PDFs, and convert to other formats. Use when working with PDF files or when user mentions PDFs, form filling, document extraction, or PDF conversion.
allowed-tools: Read, Write, Bash, Grep
---

# PDF Processor

This skill handles PDF file operations using various tools.

## Capabilities

- Extract text from PDFs
- Parse tables and structured data
- Fill PDF forms programmatically
- Merge multiple PDFs
- Convert PDFs to text/images

## Usage

When the user asks to work with PDF files, I will:

1. Check if required tools are installed (pdftotext, pdftk, etc.)
2. Perform the requested operation
3. Verify output and report results

## Examples

See [examples.md](examples.md) for detailed usage scenarios.

## Requirements

Requires installation of PDF utilities. See [reference.md](reference.md) for setup instructions.
```

## Workflow Summary

When a user asks you to create a skill:

1. **Clarify requirements** - What should the skill do? When should it activate?
2. **Choose location** - Personal or project skill?
3. **Design structure** - Simple (SKILL.md only) or complex (with supporting files)?
4. **Write frontmatter** - Name and description with trigger terms
5. **Write instructions** - Clear, actionable Markdown content
6. **Add supporting files** - If needed (templates, scripts, docs)
7. **Set tool restrictions** - If appropriate for security/scope
8. **Create the files** - Write all content to correct location
9. **Provide testing guidance** - How to verify it works

Remember: Skills are model-invoked. Claude autonomously decides when to use them based on the description, so make descriptions specific and keyword-rich.
