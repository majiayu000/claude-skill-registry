---
name: skill-cookiecutterproject-slug
description: '{{cookiecutter.project_description}}'
---

---
name: skill-{{cookiecutter.project_slug}}
description: {{cookiecutter.project_description}}
---

<!--
⚠️ AGENT INSTRUCTIONS: This is a skeleton SKILL.md template
When details about this CLI tool become clearer, update this file with:

1. **When to use section**: Add 3-5 specific use cases (bullet points)
2. **Purpose section**: Expand the tool's purpose and capabilities
3. **When to Use This Skill**: Add specific scenarios and anti-patterns
4. **Installation**: Keep the standard installation instructions
5. **Quick Start**: Add 2-3 practical quick start examples
6. **Core Commands**: Add detailed documentation for each CLI command in collapsible sections
7. **Advanced Features**: Document advanced features like verbosity, shell completion, pipelines
8. **Troubleshooting**: Add common issues and solutions
9. **Best Practices**: Add 3-5 best practices for using the tool
10. **Resources**: Update with actual GitHub URL and documentation links

CRITICAL REQUIREMENTS:
- Keep description in frontmatter ≤ 50 characters (hard limit)
- Use progressive disclosure with <details> tags
- Include comprehensive examples in each section
- Provide troubleshooting guidance
- Keep always-visible content minimal (overview only)
- Put detailed info in expandable sections
- Use emojis for section summaries (📖 Core, ⚙️ Advanced, 🔧 Troubleshooting)
-->

# When to use
<!-- TODO: Add specific use cases when CLI functionality is known -->
- When you need to use {{cookiecutter.project_slug}} CLI tool
- When you need comprehensive guidance on CLI commands
- When you need examples and troubleshooting

# {{cookiecutter.project_name}} Skill

## Purpose

<!-- TODO: Expand with specific tool capabilities -->
This skill provides access to the `{{cookiecutter.project_slug}}` CLI tool. {{cookiecutter.project_description}}.

## When to Use This Skill

**Use this skill when:**
<!-- TODO: Add specific scenarios, e.g., -->
- You need to understand how to use {{cookiecutter.project_slug}}
- You need comprehensive examples and patterns
- You need troubleshooting guidance

**Do NOT use this skill for:**
<!-- TODO: Add anti-patterns, e.g., -->
- Tasks unrelated to {{cookiecutter.project_slug}}
- Quick syntax lookups (use slash commands instead)

## CLI Tool: {{cookiecutter.project_slug}}

<!-- TODO: Add tool overview -->
The `{{cookiecutter.project_slug}}` is a command-line interface tool that {{cookiecutter.project_description}}.

### Installation

```bash
# Clone and install
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}.git
cd {{cookiecutter.project_slug}}
uv tool install .
```

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Start

<!-- TODO: Add 2-3 practical quick start examples when commands are known -->
```bash
# Example 1: Basic usage
{{cookiecutter.project_slug}} --help

# Example 2: Show version
{{cookiecutter.project_slug}} --version
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

<!-- TODO: Add detailed command documentation for each CLI command -->
<!-- Template for each command:

### command-name - Brief Description

Detailed explanation of what this command does.

**Usage:**
```bash
{{cookiecutter.project_slug}} command-name ARGUMENT [OPTIONS]
```

**Arguments:**
- `ARGUMENT`: Description of argument
- `--option VALUE` / `-o VALUE`: Description of option
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Example 1: Basic usage
{{cookiecutter.project_slug}} command-name "example"

# Example 2: With options
{{cookiecutter.project_slug}} command-name "example" --option value

# Example 3: Pipeline usage
{{cookiecutter.project_slug}} command-name "example" --json | jq '.'
```

**Output:**
Description of what this command returns.

---

Repeat for each command...
-->

### help - Show Help Information

Display help information for CLI commands.

**Usage:**
```bash
{{cookiecutter.project_slug}} --help
{{cookiecutter.project_slug}} COMMAND --help
```

**Examples:**
```bash
# General help
{{cookiecutter.project_slug}} --help

# Command help
{{cookiecutter.project_slug}} command --help

# Version info
{{cookiecutter.project_slug}} --version
```

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

<!-- TODO: Add advanced features documentation -->

### Multi-Level Verbosity Logging

Control logging detail with progressive verbosity levels. All logs output to stderr.

**Logging Levels:**

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Examples:**
```bash
# INFO level - see operations
{{cookiecutter.project_slug}} command -v

# DEBUG level - see detailed info
{{cookiecutter.project_slug}} command -vv

# TRACE level - see all internals
{{cookiecutter.project_slug}} command -vvv
```

---

### Shell Completion

Native shell completion for bash, zsh, and fish.

**Installation:**
```bash
# Bash (add to ~/.bashrc)
eval "$({{cookiecutter.project_slug}} completion bash)"

# Zsh (add to ~/.zshrc)
eval "$({{cookiecutter.project_slug}} completion zsh)"

# Fish (save to completions)
{{cookiecutter.project_slug}} completion fish > ~/.config/fish/completions/{{cookiecutter.project_slug}}.fish
```

---

### Pipeline Composition

<!-- TODO: Add pipeline examples when commands support --json and --stdin -->
Compose commands with Unix pipes for powerful workflows.

**Examples:**
```bash
# Example pipeline workflows will be added when CLI commands are implemented
{{cookiecutter.project_slug}} command --json | jq '.'
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Command not found**
```bash
# Verify installation
{{cookiecutter.project_slug}} --version

# Reinstall if needed
cd {{cookiecutter.project_slug}}
uv tool install . --reinstall
```

<!-- TODO: Add command-specific troubleshooting when functionality is known -->

**Issue: General errors**
- Try with verbose flag: `-vv` to see detailed error information
- Check that all prerequisites are installed
- Ensure you're using Python 3.14+

### Getting Help

```bash
# Show help
{{cookiecutter.project_slug}} --help

# Command-specific help
{{cookiecutter.project_slug}} COMMAND --help
```

</details>

## Exit Codes

- `0`: Success
- `1`: Client error (invalid arguments, validation failed)
- `2`: Server error (API error, network issue)
- `3`: Network error (connection failed, timeout)

## Output Formats

<!-- TODO: Update with actual output formats when commands are implemented -->

**Default Output:**
- Human-readable formatted output
- Varies by command

**JSON Output (`--json` flag):**
- Machine-readable structured data
- Perfect for pipelines and processing
- Available on commands that support structured output

## Best Practices

<!-- TODO: Add command-specific best practices -->
1. **Use verbosity progressively**: Start with `-v`, increase to `-vv`/`-vvv` only if needed
2. **Check help first**: Use `--help` to understand command options
3. **Leverage shell completion**: Install completion for better CLI experience

## Resources

- **GitHub**: https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}
- **Python Package Index**: https://pypi.org/project/{{cookiecutter.project_slug}}/
- **Documentation**: <!-- TODO: Add documentation URL if available -->
