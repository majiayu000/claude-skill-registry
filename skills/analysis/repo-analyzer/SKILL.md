---
name: repo-analyzer
description: Code repository analysis and technical documentation generation skill
author: Claude Code Skills Factory
version: 1.0.0
tags:
  - code-analysis
  - documentation
  - repository
  - technical-writing
  - architecture
---

# Repo Analyzer Skill

A comprehensive code repository analysis and technical documentation generation skill that scans repositories and generates detailed summary reports.

## Purpose

This skill analyzes code repositories to generate comprehensive technical documentation including:
- Repository overview and purpose
- Directory structure and responsibilities
- Technology stack and dependencies
- Core modules and business domains
- Key execution workflows
- Architecture design and extension patterns
- Onboarding guidance
- Risk analysis and technical debt

## When to Use This Skill

Use this skill when you need to:
- Understand a new codebase quickly
- Generate technical documentation for a repository
- Analyze repository architecture and dependencies
- Create onboarding guides for new developers
- Assess technical debt and maintenance risks

## How It Works

The skill performs an 8-step analysis:

1. **Repository Global Scan** - Scans directory structure, identifies languages, counts files
2. **Project Positioning** - Infers project purpose from README, directory names, dependencies
3. **Directory Structure Mapping** - Analyzes key directory responsibilities and relationships
4. **Tech Stack Analysis** - Parses dependency files, analyzes technology choices
5. **Core Module Abstraction** - Identifies core modules and business boundaries
6. **Execution Flow Analysis** - Traces program startup and typical execution paths
7. **Onboarding Path Generation** - Creates safe modification points and reading order
8. **Risk Assessment** - Identifies potential maintenance risks and technical debt

## Usage

### Basic Usage

```bash
python repo_analyzer.py /path/to/repository
```

### With Output File

```bash
python repo_analyzer.py /path/to/repository --output report.md
```

### With Custom Depth

```bash
python repo_analyzer.py /path/to/repository --depth 3
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `repository_path` | Path to the repository to analyze | Required |
| `--output` | Output file path for the report | `repo_analysis_report.md` |
| `--depth` | Directory scanning depth | `2` |
| `--include-risks` | Include risk assessment section | `true` |
| `--verbose` | Enable verbose logging | `false` |

## Output Format

The skill generates a comprehensive Markdown report with the following sections:

1. **Repository Overview** - Project type, purpose, scale, complexity
2. **Project Structure** - Core directory responsibilities and relationships
3. **Technology Stack** - Core frameworks, infrastructure, middleware
4. **Core Modules & Business Domains** - Key business modules and collaboration patterns
5. **Key Execution Workflows** - Program startup and typical request paths
6. **Architecture Design** - Architectural style, design patterns, extension paths
7. **Quick Start Guide** - Recommended reading order, safe modification points
8. **Risk Points & Considerations** - Potential maintenance risks and pitfalls

## Installation

### Project-Level Installation

```bash
# Copy skill to project .claude directory
cp -r generated-skills/repo-analyzer .claude/skills/
```

### User-Level Installation

```bash
# Copy skill to user .claude directory
cp -r generated-skills/repo-analyzer ~/.claude/skills/
```

## Files

- `repo_analyzer.py` - Main analysis script
- `requirements.txt` - Python dependencies
- `SKILL.md` - This documentation file
- `examples/` - Example analysis reports

## Dependencies

- Python 3.8+
- `pyyaml` - For parsing YAML configuration files
- `toml` - For parsing TOML configuration files
- `chardet` - For file encoding detection

## Examples

### Analyze Current Repository

```bash
python repo_analyzer.py .
```

### Generate Report for Specific Path

```bash
python repo_analyzer.py /projects/my-app --output my_analysis.md
```

### Analyze with Custom Settings

```bash
python repo_analyzer.py /path/to/repo --depth 3 --include-risks false --verbose true
```

## Limitations

- Analysis is based on static code structure, not runtime behavior
- Business logic inference is limited to code organization patterns
- Dependency analysis requires standard package manager files
- Complex monorepos may require deeper scanning depth

## Best Practices

1. **Start with default settings** - Use depth=2 for most repositories
2. **Review inferred information** - Always validate inferred project purposes
3. **Customize for complex repos** - Increase depth for deeply nested structures
4. **Combine with manual review** - Use the report as a starting point for deeper analysis

## Troubleshooting

### Common Issues

1. **Permission errors** - Ensure read access to the repository directory
2. **Encoding issues** - The skill uses chardet to detect file encodings
3. **Missing dependencies** - Install required packages from requirements.txt
4. **Large repositories** - May take longer to process; consider increasing timeout

### Debug Mode

Enable verbose logging for detailed processing information:

```bash
python repo_analyzer.py /path/to/repo --verbose true
```

## Related Skills

- `code-reviewer` - For detailed code quality analysis
- `architecture-validator` - For architectural pattern validation
- `dependency-auditor` - For security vulnerability scanning

## Contributing

To contribute to this skill:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This skill is released under the MIT License.

## Changelog

### v1.0.0
- Initial release with 8-step analysis framework
- Support for multiple dependency file formats
- Markdown report generation
- Configurable scanning depth

---

**Note**: This skill generates documentation based on code structure analysis. Always validate the generated insights with domain experts and actual code behavior.