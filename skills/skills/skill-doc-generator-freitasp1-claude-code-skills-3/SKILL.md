---
name: skill-doc-generator
description: Auto-generates standardized README documentation from SKILL.md files, validates consistency (frontmatter, descriptions, terminology), and creates usage examples. Use when documenting individual skills, generating docs for multiple skills in a directory, or validating skill quality standards.
---

# Skill Documentation Generator

Auto-generate high-quality README documentation for skills with built-in consistency validation and example generation.

## Overview

This skill automates the creation of standardized README files for skills by analyzing SKILL.md files, extracting structure and examples, validating quality standards, and generating comprehensive documentation. It ensures consistency across skill documentation while providing actionable validation feedback.

## Workflow

### Single Skill Documentation

Generate documentation for one skill:

1. **Analyze the skill**:
   ```bash
   python scripts/analyze_skill.py <skill_directory>
   ```
   Extracts metadata, sections, code blocks, and resources.

2. **Validate consistency**:
   ```bash
   python scripts/validate_consistency.py <skill_directory> --verbose
   ```
   Checks frontmatter, description quality, and terminology.

3. **Generate README**:
   ```bash
   python scripts/generate_readme.py <skill_directory> [output_path]
   ```
   Creates README.md with validation results.

### Batch Documentation

Document multiple skills at once:

```bash
python scripts/document_directory.py <directory> [options]
```

**Options:**
- `--output <dir>`: Specify output directory
- `--no-recursive`: Don't search subdirectories
- `--no-index`: Skip index file generation
- `--no-validate`: Skip validation checks

**Example:**
```bash
# Document all user skills with validation
python scripts/document_directory.py /mnt/skills/user --output ./docs

# Quick pass without validation
python scripts/document_directory.py ./my-skills --no-validate
```

## Script Reference

### analyze_skill.py
Parses SKILL.md and extracts structured information.

**Usage**: `python scripts/analyze_skill.py <skill_directory>`

**Returns**:
- Metadata (name, description)
- Sections and structure
- Code blocks with language tags
- Referenced resources (scripts, references, assets)
- Statistics (line count, section count)

### validate_consistency.py
Validates skill quality against standards defined in references/consistency-rules.md.

**Usage**: `python scripts/validate_consistency.py <skill_directory> [--verbose]`

**Checks**:
- Frontmatter completeness and format
- Description quality (length, clarity, triggers)
- Structure appropriateness
- Terminology consistency
- Resource references
- Code example quality

**Severity Levels**:
- **ERROR**: Breaks functionality (missing required fields)
- **WARNING**: Quality issues (naming, unreferenced resources)
- **INFO**: Suggestions (style, optional improvements)

### generate_readme.py
Creates README.md from skill analysis.

**Usage**: `python scripts/generate_readme.py <skill_directory> [output_path]`

**Generates**:
- Title and description
- Overview from SKILL.md
- Trigger scenarios
- Structure statistics
- Bundled resource lists with links
- Key sections overview
- Usage examples (up to 3)
- Validation results (optional)

**Template**: See references/readme-template.md for structure.

### document_directory.py
Batch processes multiple skills in a directory.

**Usage**: `python scripts/document_directory.py <directory> [options]`

**Features**:
- Recursive skill discovery
- Parallel validation and documentation
- Index generation with categorization
- Summary statistics
- Error handling per skill

## Quality Standards

Validation enforces these standards:

### Frontmatter
- **name**: Lowercase with hyphens (e.g., `skill-name`)
- **description**: 50-500 chars, clear triggers
- Must start with capital letter
- Include "when" or "use" phrases

### Structure
- Body: 100+ chars minimum, <500 lines recommended
- Sections: Overview/workflow recommended
- Resources: All files referenced in SKILL.md

### Terminology
- Use imperative form: "Use" not "You should use"
- Capitalize "Claude" consistently
- Avoid vague terms: "various", "multiple"
- Active voice preferred

See references/consistency-rules.md and references/terminology-standards.md for complete standards.

## Reference Files

### readme-template.md
Standard README structure and best practices. Defines:
- Required sections
- Optional sections
- Formatting guidelines
- Link conventions

### consistency-rules.md
Detailed validation criteria. Covers:
- Frontmatter requirements
- Description quality metrics
- Structure guidelines
- Resource validation
- Error severity definitions

### terminology-standards.md
Standard vocabulary and style guide. Includes:
- Writing style (imperative form)
- Common terms and their usage
- Phrases to avoid
- Formatting conventions
- Consistency checklist

## Examples

### Example 1: Document a Single Skill
```bash
# Analyze
python scripts/analyze_skill.py ./my-skill

# Validate
python scripts/validate_consistency.py ./my-skill --verbose

# Generate README
python scripts/generate_readme.py ./my-skill
```

### Example 2: Batch Process with Index
```bash
# Document all skills in a directory
python scripts/document_directory.py /mnt/skills/user \
  --output ./documentation \
  --recursive
```

### Example 3: Quick Validation Pass
```bash
# Just validate without generating docs
python scripts/validate_consistency.py ./my-skill
```

## Common Use Cases

**New skill creation**: Generate documentation as part of skill development
**Quality audits**: Validate existing skills against standards
**Documentation updates**: Regenerate READMEs after SKILL.md changes
**Batch operations**: Document entire skill libraries
**CI/CD integration**: Automated validation in deployment pipelines

## Tips

- Run validation before generating documentation to catch issues early
- Use `--verbose` flag to see INFO-level suggestions
- Reference files provide the "why" behind validation rules
- Generated READMEs include validation results for transparency
- Index files help navigate large skill collections
