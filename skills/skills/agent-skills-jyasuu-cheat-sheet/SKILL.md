---
name: agent-skills
description: Create, use, and manage Agent Skills for Claude. Use when working with Skills, creating custom capabilities, or understanding how Skills extend Claude's functionality. Covers Skill architecture, file structure, and best practices.
---

# Agent Skills

Agent Skills are modular capabilities that extend Claude's functionality. Each Skill packages instructions, metadata, and optional resources that Claude uses automatically when relevant.

## Quick Start

```yaml
# A basic skill structure
---
name: my-skill
description: Brief description of what this Skill does
---

# My Skill

## Instructions
Clear, step-by-step guidance for Claude to follow

## Examples
Concrete examples of using this Skill
```

## Why use Skills

Skills provide domain-specific expertise that transforms general-purpose agents into specialists. Unlike prompts, Skills load on-demand and eliminate repetitive guidance.

**Key benefits**:
- **Specialize Claude**: Tailor capabilities for specific domains
- **Reduce repetition**: Create once, use automatically
- **Compose capabilities**: Combine Skills to build complex workflows

## How Skills Work

Skills leverage Claude's VM environment with filesystem access. They exist as directories containing instructions, executable code, and reference materials.

### Three Levels of Loading

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **Level 1: Metadata** | Always (startup) | ~100 tokens | `name` and `description` from YAML frontmatter |
| **Level 2: Instructions** | When triggered | Under 5k tokens | SKILL.md body with guidance |
| **Level 3+: Resources** | As needed | Unlimited | Bundled files executed via bash |

Progressive disclosure ensures only relevant content occupies the context window.

### Skill Directory Structure

```
my-skill/
├── SKILL.md              # Main instructions
├── GUIDE.md              # Additional guidance
├── REFERENCE.md          # API reference
└── scripts/
    └── helper.py         # Utility scripts
```

**Instructions**: Additional markdown files with specialized guidance
**Code**: Executable scripts that Claude runs via bash
**Resources**: Reference materials like schemas, templates, examples

## Skill Structure

Every Skill requires a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance]

## Examples
[Concrete examples]
```

### Field Requirements

**name**:
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- Cannot contain XML tags
- Cannot use reserved words: "anthropic", "claude"

**description**:
- Must be non-empty
- Maximum 1024 characters
- Cannot contain XML tags
- Should explain what the Skill does AND when to use it

## Creating Custom Skills

### For Claude Code

1. Create a directory in `.claude/skills/`
2. Add a `SKILL.md` file with YAML frontmatter
3. Optionally add supporting files (guides, scripts, resources)
4. Claude discovers and uses them automatically

```bash
.claude/skills/
├── my-skill/
│   ├── SKILL.md
│   └── scripts/
│       └── helper.sh
└── another-skill/
    └── SKILL.md
```

### For Claude API

1. Create Skill as a directory with `SKILL.md`
2. Upload via Skills API (`/v1/skills` endpoints)
3. Reference `skill_id` in the `container` parameter
4. Requires beta headers:
   - `code-execution-2025-08-25`
   - `skills-2025-10-02`
   - `files-api-2025-04-14`

### For Claude.ai

1. Create Skill as a directory with `SKILL.md`
2. Zip the skill directory
3. Upload through Settings > Features
4. Available on Pro, Max, Team, Enterprise plans

## Best Practices

### Writing Effective Skills

**Be specific about when to use**:
```yaml
description: Extract text from PDF files using pdfplumber. Use when user mentions PDFs, text extraction, or document processing.
```

**Include concrete examples**:
```markdown
## Examples

To extract text from a PDF:
```python
import pdfplumber
with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Organize progressively**:
- Quick start first
- Common workflows
- Advanced scenarios
- Reference materials

### Bundling Resources

**Use scripts for reliability**:
```bash
# Scripts execute without loading code into context
$ bash validate.sh
Validation passed
```

**Include reference materials**:
- API documentation
- Database schemas
- Code examples
- Templates

## Security Considerations

**Use Skills from trusted sources only**:

- **Audit thoroughly**: Review all files bundled in the Skill
- **External sources are risky**: Skills fetching external content pose risks
- **Tool misuse**: Malicious Skills can invoke tools in harmful ways
- **Data exposure**: Skills with sensitive data access could leak information
- **Treat like installing software**: Only use Skills from trusted sources

## Cross-Surface Availability

| Surface | Custom Skills | Pre-built Skills |
|---------|---------------|------------------|
| Claude API | Yes | Yes (pptx, xlsx, docx, pdf) |
| Claude Code | Yes (filesystem-based) | No |
| Claude.ai | Yes (uploaded) | Yes (pptx, xlsx, docx, pdf) |

**Custom Skills do not sync across surfaces** - manage separately for each.

### Runtime Environment

**Claude API**:
- No network access
- No runtime package installation
- Pre-configured dependencies only

**Claude Code**:
- Full network access
- Local package installation only

**Claude.ai**:
- Varying network access (depends on settings)

## Pre-built Agent Skills

Available immediately:

- **PowerPoint (pptx)**: Create presentations, edit slides, analyze content
- **Excel (xlsx)**: Create spreadsheets, analyze data, generate charts
- **Word (docx)**: Create documents, edit content, format text
- **PDF (pdf)**: Generate formatted PDF documents and reports

## Sharing Models

| Surface | Scope |
|---------|-------|
| Claude.ai | Individual user only |
| Claude API | Workspace-wide |
| Claude Code | Personal (`~/.claude/skills/`) or project-based (`.claude/skills/`) |

## Advanced Patterns

### Chaining Skills

Combine Skills to build complex workflows:
1. Skill A processes input
2. Skill B transforms output
3. Skill C validates results

### Environment-Aware Skills

Design Skills to adapt to runtime:
```markdown
## Runtime Notes

- Claude API: Use pre-installed packages only
- Claude Code: Can install packages locally
- Adjust behavior based on available tools
```

### Progressive Disclosure

Structure Skills so Claude loads only what's needed:
```markdown
# Main Skill

## Quick Start
Essential information for common tasks

## Advanced Usage
Detailed guidance when needed

See [REFERENCE.md](REFERENCE.md) for complete API documentation.
```

## Troubleshooting

### Skill Not Loading

1. Verify `SKILL.md` exists in skill directory
2. Check YAML frontmatter is valid
3. Ensure `name` uses only lowercase letters, numbers, hyphens
4. Confirm `description` is non-empty

### Permission Issues

- Claude Code: Check `.claude/skills/` directory permissions
- Claude API: Verify beta headers are set correctly
- Claude.ai: Confirm plan includes code execution

### Context Overflow

- Move detailed reference to separate files
- Use scripts for complex operations
- Structure with progressive disclosure

## File Reference

- [Authoring Best Practices](/docs/en/agents-and-tools/agent-skills/best-practices)
- [Use Skills with Claude API](/docs/en/build-with-claude/skills-guide)
- [Use Skills in Claude Code](https://code.claude.com/docs/en/skills)
- [Agent Skills SDK](/docs/en/agent-sdk/skills)
