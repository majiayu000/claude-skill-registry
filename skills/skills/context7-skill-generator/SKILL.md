---
name: context7-skill-generator
description: Automatically generates skills from Context7 MCP documentation responses
updated: 2026-01-13
---

# Context7 Skill Generator

Automatically captures Context7 MCP documentation responses and generates properly formatted skill files.

## How It Works

When Context7 MCP is invoked during a conversation, this skill:

1. **Detects Context7 usage** - Identifies when Context7 tools were called
2. **Extracts documentation** - Pulls the relevant docs from the conversation
3. **Formats as skill** - Creates proper YAML frontmatter and markdown structure
4. **Generates skill file** - Writes to the appropriate location

## Usage

### Automatic Detection

Simply invoke this skill after using Context7:

```
/skill context7-skill-generator
```

The skill will analyze the conversation for Context7 responses and prompt you for:

- **Skill name** (e.g., `latest-nextjs`, `react-compiler`)
- **Description** (brief summary of what the skill covers)
- **Plugin location** (which plugin to add the skill to)

### Manual Command

For explicit invocation with parameters:

```bash
/skill:from-context7
```

## Context7 Tool Patterns

The skill looks for these Context7 MCP tool invocations:

- `resolve-library-id` - Library resolution
- `query-docs` - Documentation queries

## Generated Skill Structure

The generated skill follows this template:

```yaml
---
name: skill-name
description: Brief description of the skill
updated: YYYY-MM-DD
source: context7
library: library-name
version: detected-version
---
```

### Sections Generated

1. **Frontmatter** - YAML metadata (name, description, updated, source, library, version)
2. **Title** - Formatted from skill name
3. **Overview** - Brief introduction
4. **Key Features** - Main functionality extracted from docs
5. **Code Examples** - Relevant examples from Context7 response
6. **API Reference** - Important API patterns
7. **Best Practices** - Usage patterns found in docs
8. **Migration Notes** - Any version-specific migration info
9. **Resources** - Links to official docs

## Output Location

Skills are generated to:

```
plugins/{plugin-name}/skills/{skill-name}/SKILL.md
```

## Example Workflow

```bash
# 1. Use Context7 to get documentation
How do I set up Next.js 16 middleware? use context7

# 2. Generate a skill from the response
/skill context7-skill-generator

# 3. Provide prompted information:
#    - Skill name: nextjs-middleware
#    - Description: Next.js 16 middleware patterns and configuration
#    - Plugin: nextjs

# 4. Skill file created at:
#    plugins/nextjs/skills/nextjs-middleware/SKILL.md
```

## Extraction Logic

### Content Identification

The skill identifies Context7 content by looking for:

- Tool results containing `resolve-library-id` or `query-docs`
- Documentation sections with code examples
- Version-specific information
- API patterns and usage examples

### Smart Formatting

- **Code blocks** - Preserved as markdown code fences
- **Headers** - Converted to proper markdown hierarchy
- **Lists** - Formatted as bulleted or numbered lists
- **Links** - Preserved as markdown links
- **Tables** - Converted to markdown tables

### Version Detection

Attempts to extract version information from:
- Explicit version mentions in docs
- Library identifiers (e.g., `/vercel/next.js`)
- Release notes or changelog entries

## Error Handling

If the skill cannot:

- **Find Context7 content**: Prompts you to paste the documentation manually
- **Determine library**: Asks for library name manually
- **Detect version**: Uses current date and notes version as "latest"

## Best Practices

1. **Review generated skills** - Always review and edit the generated skill for accuracy
2. **Add custom examples** - Supplement Context7 content with project-specific examples
3. **Keep focused** - Generate skills for specific topics, not entire libraries
4. **Update regularly** - Re-run for updated documentation as libraries evolve
5. **Index skills** - Run `update-indexes` after generating new skills

## Integration with Marketplace

This skill integrates with the IP Labs marketplace by:

- Following marketplace skill conventions (YAML frontmatter, markdown structure)
- Supporting multi-plugin skill generation
- Maintaining consistency with existing skills like `latest-nextjs` and `latest-react`

## Advanced Usage

### Batch Generation

For multiple libraries, invoke multiple times:

```bash
/skill context7-skill-generator
# (generate first skill)

/skill context7-skill-generator
# (generate second skill)
```

### Custom Sections

Add custom sections by editing the generated skill file after creation. Common additions:

- **Project-Specific Patterns** - How your team uses this library
- **Integration Examples** - Connecting with other tools in your stack
- **Troubleshooting** - Common issues and solutions
- **Performance Tips** - Optimization guidance
