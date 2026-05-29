---
name: plugin-marketplace
description: Guide for creating and managing Claude Code plugin marketplaces. Use when setting up a marketplace, validating marketplace.json, or distributing plugins.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Claude Code Plugin Marketplace

Guide for creating, validating, and managing plugin marketplaces for Claude Code. Includes schema validation, best practices, and automated tools.

## When to Use This Skill

Activate this skill when:
- Creating or editing `.claude-plugin/marketplace.json` files
- Validating marketplace schema compliance
- Setting up plugin repositories with marketplaces
- Troubleshooting marketplace configuration issues
- Converting plugin structures to marketplace format
- Creating plugin entries with advanced features

## Marketplace Schema Overview

### Required Structure

All marketplaces must be located at `.claude-plugin/marketplace.json` in the repository root.

**Required Fields:**
- `name`: Marketplace identifier (kebab-case, lowercase alphanumeric and hyphens only)
- `owner`: Object with maintainer details (`name` required, `email` optional)
- `plugins`: Array of plugin definitions (can be empty)

**Optional Metadata:**
- `metadata.description`: Summary of marketplace purpose
- `metadata.version`: Marketplace version tracking (semantic versioning recommended)
- `metadata.pluginRoot`: Base directory for relative plugin source paths

### Plugin Entry Schema

**IMPORTANT: Schema Relationship**

Plugin entries use the plugin manifest schema with all fields made optional, plus marketplace-specific fields (`source`, `strict`, `category`, `tags`). This means any field valid in a plugin.json file can also be used in a marketplace entry.

- When `strict: false`, the marketplace entry serves as the complete plugin manifest if no plugin.json exists
- When `strict: true` (default), marketplace fields supplement the plugin's own manifest file

Each plugin entry in the `plugins` array requires:

**Mandatory:**
- `name`: Plugin identifier (kebab-case)
- `source`: Location specification (string path or object)

**Standard Metadata:**
- `description`: Brief explanation of plugin functionality
- `version`: Semantic version number
- `author`: Creator information (object with `name`, optional `email`)
- `homepage`: Documentation or project URL
- `repository`: Source control URL
- `license`: SPDX license identifier (e.g., MIT, Apache-2.0)
- `keywords`: Array of discovery and categorization tags
- `category`: Organizational grouping
- `tags`: Additional searchability terms

**Component Configuration:**
- `commands`: Custom paths to command files or directories
- `agents`: Custom paths to agent files
- `hooks`: Custom hooks configuration or path to hooks file
- `mcpServers`: MCP server configurations or path to MCP config
- `skills`: Array of skill directory paths

**Strict Mode Control:**
- `strict`: Boolean (default: `true`)
  - `true`: Plugin must include plugin.json; marketplace fields supplement it
  - `false`: Marketplace entry serves as complete manifest (no plugin.json needed)

**Dependencies:**
- `dependencies`: Array of plugin names this plugin depends on (format: `"namespace:plugin-name"`)

## Plugin Source Formats

### Relative Path
```json
"source": "./plugins/my-plugin"
```

### Relative Path with pluginRoot
```json
// In marketplace metadata
"metadata": {
  "pluginRoot": "./plugins"
}

// In plugin entry
"source": "my-plugin"  // Resolves to ./plugins/my-plugin
```

### GitHub Repository
```json
"source": {
  "source": "github",
  "repo": "owner/plugin-repo",
  "path": "optional/subdirectory",
  "branch": "main"
}
```

### Git URL
```json
"source": {
  "source": "url",
  "url": "https://gitlab.com/team/plugin.git",
  "branch": "main"
}
```

## Environment Variables

Use `${CLAUDE_PLUGIN_ROOT}` in paths to reference the plugin's installation directory:

```json
{
  "skills": [
    "${CLAUDE_PLUGIN_ROOT}/skills/my-skill"
  ],
  "commands": [
    "${CLAUDE_PLUGIN_ROOT}/commands"
  ]
}
```

This ensures paths work correctly regardless of installation location.

## Advanced Plugin Entry Features

### Inline Plugin Definitions

Use `strict: false` to define complete plugin manifests inline without requiring plugin.json:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "strict": false,
  "description": "Complete plugin definition inline",
  "version": "1.0.0",
  "author": {
    "name": "Developer Name"
  },
  "skills": [
    "${CLAUDE_PLUGIN_ROOT}/skills/skill-one",
    "${CLAUDE_PLUGIN_ROOT}/skills/skill-two"
  ]
}
```

### Component Path Override

Customize component locations:

```json
{
  "name": "custom-paths",
  "source": "./plugins/custom",
  "strict": false,
  "commands": ["${CLAUDE_PLUGIN_ROOT}/custom-commands"],
  "agents": ["${CLAUDE_PLUGIN_ROOT}/custom-agents"],
  "hooks": {
    "onInstall": "${CLAUDE_PLUGIN_ROOT}/hooks/install.sh"
  },
  "mcpServers": "${CLAUDE_PLUGIN_ROOT}/mcp-config.json"
}
```

### Metadata Supplementation

With `strict: true`, marketplace entries can add metadata not in plugin.json:

```json
{
  "name": "existing-plugin",
  "source": "./plugins/existing",
  "strict": true,
  "category": "development",
  "keywords": ["added", "from", "marketplace"],
  "homepage": "https://docs.example.com"
}
```

## Validation Workflow

### 1. Schema Validation

Use the provided Nushell script to validate marketplace.json:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-marketplace.nu .claude-plugin/marketplace.json
```

This validates:
- JSON syntax
- Required fields presence
- Kebab-case naming
- Field type correctness
- Source path accessibility (for relative paths)

### 2. Plugin Entry Validation

Validate individual plugin entries:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin-entry.nu .claude-plugin/marketplace.json "plugin-name"
```

Checks:
- Required fields (name, source)
- Strict mode consistency
- Dependency references
- Path validity
- Component configuration

### 3. Dependency Graph Validation

Check for circular dependencies and missing dependencies:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-dependencies.nu .claude-plugin/marketplace.json
```

## Best Practices

### Naming Conventions

- **Marketplace name**: Use your GitHub username or organization (e.g., `vinnie357`)
- **Plugin names**: Use descriptive kebab-case (e.g., `elixir-phoenix`, `rust-tools`, `core-skills`)
- **Categories**: Standardize on common categories: `development`, `language`, `tools`, `frontend`, `backend`, `meta`

### Versioning Strategy

- Use semantic versioning for both marketplace and plugins
- Bump marketplace version when adding/removing plugins
- Bump plugin versions when updating skills or configuration
- Document breaking changes in plugin descriptions

### Dependency Management

- Always declare `dependencies` for plugins that require other plugins
- Keep dependency chains shallow (avoid deep nesting)
- Consider creating a meta-plugin (like `all-skills`) that bundles related plugins
- Use namespace prefixes for dependencies (e.g., `all-skills:core`)

### Strict Mode Decision

**Use `strict: false` when:**
- Creating simple, self-contained plugins
- All configuration is in marketplace.json
- You want centralized management
- Plugin is unlikely to be distributed independently

**Use `strict: true` when:**
- Plugin has complex configuration
- Plugin may be distributed separately
- Plugin has its own versioning lifecycle
- You want to supplement existing plugin.json with marketplace metadata

### Source Path Organization

```json
{
  "metadata": {
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "core",
      "source": "core"  // Resolves to ./plugins/core
    },
    {
      "name": "external",
      "source": {
        "source": "github",
        "repo": "org/repo"
      }
    }
  ]
}
```

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

### Error: Missing required owner field

```json
// ❌ Invalid
{
  "name": "marketplace"
}

// ✅ Valid
{
  "name": "marketplace",
  "owner": {
    "name": "Developer Name"
  }
}
```

### Error: Invalid source path

```json
// ❌ Invalid (path doesn't exist)
"source": "./plugins/nonexistent"

// ✅ Valid (path exists)
"source": "./plugins/core"
```

### Error: Circular dependencies

```json
// ❌ Invalid
{
  "plugins": [
    {
      "name": "plugin-a",
      "dependencies": ["namespace:plugin-b"]
    },
    {
      "name": "plugin-b",
      "dependencies": ["namespace:plugin-a"]
    }
  ]
}
```

## Creating a New Marketplace

### Step 1: Initialize Structure

```bash
mkdir -p .claude-plugin
```

### Step 2: Create Marketplace File

Use the validation script to generate a template:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/init-marketplace.nu
```

This creates `.claude-plugin/marketplace.json` with required fields.

### Step 3: Add Plugin Entries

For each plugin, decide on strict mode and add entry:

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "metadata": {
    "description": "Your marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "plugin-name",
      "strict": false,
      "description": "Plugin description",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      },
      "license": "MIT",
      "category": "development",
      "skills": [
        "${CLAUDE_PLUGIN_ROOT}/skills/skill-one"
      ]
    }
  ]
}
```

### Step 4: Validate

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-marketplace.nu .claude-plugin/marketplace.json
```

### Step 5: Test Installation

```bash
claude-code install ./
```

## Migrating Existing Plugins

### From Individual Plugins to Marketplace

1. **Identify plugins**: List all plugin.json files
2. **Decide on strict mode**: Choose per plugin based on complexity
3. **Create marketplace.json**: Add all plugins with appropriate configuration
4. **Test each plugin**: Verify installation works correctly
5. **Document dependencies**: Add dependency arrays where needed

### Migration Script

Use the provided script to analyze existing structure:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/analyze-plugins.nu .
```

This scans for plugin.json files and suggests marketplace.json structure.

## Troubleshooting

### Plugin Not Found After Installation

- Verify `source` path is correct
- Check `pluginRoot` in metadata if using relative paths
- Ensure plugin directory exists at specified location

### Skills Not Loading

- Verify skill paths use `${CLAUDE_PLUGIN_ROOT}` if needed
- Check that skill directories contain SKILL.md files
- Validate skill paths in plugin entry or plugin.json

### Dependency Resolution Fails

- Ensure dependency names match exactly (including namespace)
- Check that all dependencies are listed in marketplace
- Verify no circular dependencies exist

### Validation Errors

Run validation script with verbose mode:

```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/validate-marketplace.nu .claude-plugin/marketplace.json --verbose
```

## References

For detailed schema specifications and examples, see:
- `references/schema-specification.md`: Complete JSON schema
- `references/examples.md`: Real-world marketplace examples
- `references/migration-guide.md`: Step-by-step migration instructions

## Script Usage

All validation and utility scripts are located in `scripts/`:
- `validate-marketplace.nu`: Full marketplace validation
- `validate-plugin-entry.nu`: Individual plugin entry validation
- `validate-dependencies.nu`: Dependency graph validation
- `init-marketplace.nu`: Generate marketplace template
- `analyze-plugins.nu`: Analyze existing plugin structure
- `format-marketplace.nu`: Format and sort marketplace.json

Execute scripts with:
```bash
nu ${CLAUDE_PLUGIN_ROOT}/scripts/[script-name].nu [args]
```
