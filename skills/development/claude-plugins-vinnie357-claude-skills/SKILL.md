---
name: claude-plugins
description: Guide for creating and validating Claude Code plugin.json files. Use when creating plugins, validating plugin schemas, or troubleshooting plugin configuration.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Claude Code Plugin

Guide for creating, validating, and managing plugin.json files for Claude Code plugins. Includes schema validation, best practices, and automated tools.

## When to Use This Skill

Activate this skill when:
- Creating or editing `.claude-plugin/plugin.json` files
- Validating plugin.json schema compliance
- Setting up new plugin directories
- Troubleshooting plugin configuration issues
- Understanding plugin manifest structure

## Plugin Manifest Schema

### File Location

All plugin manifests must be located at `.claude-plugin/plugin.json` within the plugin directory.

### Complete Schema

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "skills": ["./skills/skill-one", "./skills/skill-two"]
}
```

### Required Fields

- `name`: Plugin identifier (kebab-case, lowercase alphanumeric and hyphens only)

### Optional Fields

**Metadata:**
- `version`: Semantic version number (recommended)
- `description`: Brief explanation of plugin functionality
- `license`: SPDX license identifier (e.g., MIT, Apache-2.0)
- `keywords`: Array of searchability and categorization tags
- `homepage`: Documentation or project URL
- `repository`: Source control URL

**Author Information:**
- `author.name`: Creator name
- `author.email`: Contact email
- `author.url`: Personal or organization website

**Component Paths:**
- `skills`: Array of skill directory paths (relative to plugin root)
- `commands`: String path or array of command file/directory paths
- `agents`: String path or array of agent file paths
- `hooks`: String path to hooks.json or hooks configuration object
- `mcpServers`: String path to MCP config or configuration object

## Field Validation Rules

### name
- **Format**: kebab-case (lowercase alphanumeric and hyphens only)
- **Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*$`
- **Examples**:
  - Valid: `my-plugin`, `core-skills`, `elixir-tools`
  - Invalid: `myPlugin`, `my_plugin`, `My-Plugin`, `plugin-`

### version
- **Format**: Semantic versioning
- **Pattern**: `^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$`
- **Examples**:
  - Valid: `1.0.0`, `2.1.3`, `1.0.0-beta.1`, `1.0.0+build.123`
  - Invalid: `1.0`, `v1.0.0`, `1.0.0.0`

### license
- **Format**: SPDX license identifier
- **Common values**: `MIT`, `Apache-2.0`, `GPL-3.0`, `BSD-3-Clause`, `ISC`
- **Reference**: https://spdx.org/licenses/

### keywords
- **Format**: Array of strings
- **Purpose**: Discoverability, searchability, categorization
- **Recommendations**: Use lowercase, be specific, include domain terms

### Paths (skills, commands, agents, hooks, mcpServers)
- **Format**: Relative paths from plugin root
- **Recommendations**: Use `./` prefix for clarity
- **Skills**: Array of directory paths containing SKILL.md files
- **Commands**: Can be string (single path) or array of paths
- **Agents**: Can be string (directory) or array of file paths

## Invalid Fields in plugin.json

The following fields are **only valid in marketplace.json** entries and must NOT appear in plugin.json:

- `dependencies`: Dependencies belong in marketplace entries, not plugin manifests
- `category`: Categorization is marketplace-level metadata
- `strict`: Controls marketplace behavior, not plugin definition
- `source`: Plugin location is defined in marketplace, not in plugin itself
- `tags`: Use `keywords` instead

## Validation Workflow

### 1. Schema Validation

Use the provided Nushell script to validate plugin.json:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin.nu .claude-plugin/plugin.json
```

This validates:
- JSON syntax
- Required field presence (name)
- Kebab-case naming
- Field type correctness
- Path accessibility (for relative paths)
- Invalid field detection

### 2. Path Validation

Validate that referenced paths exist:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin-paths.nu .claude-plugin/plugin.json
```

Checks:
- Skills directories exist and contain SKILL.md
- Command files/directories exist
- Agent files/directories exist
- Hooks configuration exists
- MCP server configuration exists

### 3. Initialization Helper

Generate a template plugin.json:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/init-plugin.nu
```

Creates `.claude-plugin/plugin.json` with proper structure.

## Best Practices

### Naming Conventions

- **Plugin name**: Use descriptive kebab-case (e.g., `elixir-phoenix`, `rust-tools`, `core-skills`)
- **Avoid generic names**: Be specific about the plugin's purpose
- **Match directory name**: Plugin name should match its directory name

### Versioning Strategy

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Increment MAJOR for breaking changes
- Increment MINOR for new features (backward compatible)
- Increment PATCH for bug fixes
- Use pre-release tags for beta versions (`1.0.0-beta.1`)

### Path Organization

**Recommended structure:**
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── skill-one/
│   └── skill-two/
├── commands/
└── agents/
```

**In plugin.json:**
```json
{
  "skills": [
    "./skills/skill-one",
    "./skills/skill-two"
  ],
  "commands": ["./commands"],
  "agents": ["./agents"]
}
```

### Metadata Completeness

Always include:
- `version`: Track plugin evolution
- `description`: Help users understand purpose
- `license`: Clarify usage terms
- `keywords`: Improve discoverability
- `repository`: Enable contributions

### Author Information

Include contact information for:
- Bug reports
- Feature requests
- Contributions
- Questions

## Common Validation Errors

### Error: Invalid kebab-case name

```json
// ❌ Invalid
"name": "myPlugin"
"name": "my_plugin"
"name": "My-Plugin"

// ✅ Valid
"name": "my-plugin"
"name": "core-skills"
```

### Error: Invalid field for plugin.json

```json
// ❌ Invalid (dependencies only in marketplace.json)
{
  "name": "my-plugin",
  "dependencies": ["other-plugin"]
}

// ✅ Valid
{
  "name": "my-plugin",
  "keywords": ["tool", "utility"]
}
```

### Error: Skill path doesn't exist

```json
// ❌ Invalid (path not found)
"skills": ["./skills/nonexistent"]

// ✅ Valid (path exists with SKILL.md)
"skills": ["./skills/my-skill"]
```

### Error: Invalid version format

```json
// ❌ Invalid
"version": "1.0"
"version": "v1.0.0"

// ✅ Valid
"version": "1.0.0"
"version": "2.1.3-beta.1"
```

## Creating a New Plugin

### Step 1: Initialize Directory Structure

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/skills
```

### Step 2: Create plugin.json

Use the initialization script:

```bash
cd my-plugin
nu ${CLAUDE_PLUGIN_ROOT}/scripts/init-plugin.nu
```

Or create manually:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "My plugin description",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": []
}
```

### Step 3: Add Skills

1. Create skill directory: `mkdir -p skills/my-skill`
2. Create SKILL.md in skill directory
3. Add to plugin.json:

```json
{
  "skills": ["./skills/my-skill"]
}
```

### Step 4: Validate

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin.nu .claude-plugin/plugin.json
```

### Step 5: Test

Install locally to test:

```bash
claude-code install ./
```

## Hooks Configuration

Hooks can be inline or referenced:

**Inline:**
```json
{
  "hooks": {
    "onInstall": "./scripts/install.sh",
    "onUninstall": "./scripts/uninstall.sh"
  }
}
```

**Referenced:**
```json
{
  "hooks": "./config/hooks.json"
}
```

## MCP Servers Configuration

MCP servers can be inline or referenced:

**Inline:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["./workspace"]
    }
  }
}
```

**Referenced:**
```json
{
  "mcpServers": "./mcp-config.json"
}
```

## Troubleshooting

### Plugin Not Loading

- Verify plugin.json exists at `.claude-plugin/plugin.json`
- Check JSON syntax is valid
- Ensure name field is present and kebab-case
- Validate all path references exist

### Skills Not Found

- Check skill paths in plugin.json match actual directories
- Ensure each skill directory contains SKILL.md file
- Verify paths use relative format (`./skills/name`)

### Commands Not Appearing

- Verify command paths exist
- Check commands are .md files or directories containing .md files
- Ensure paths are relative to plugin root

### Validation Fails

Run validation with verbose output:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin.nu .claude-plugin/plugin.json --verbose
```

## References

For detailed schema specifications and examples, see:
- `references/plugin-schema.md`: Complete JSON schema specification
- `references/plugin-examples.md`: Real-world plugin.json examples

## Script Usage

All validation and utility scripts are located in `scripts/`:
- `validate-plugin.nu`: Complete plugin.json validation
- `validate-plugin-paths.nu`: Verify all referenced paths exist
- `init-plugin.nu`: Generate plugin.json template
- `format-plugin.nu`: Format and sort plugin.json

Execute scripts with:
```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/[script-name].nu [args]
```
