---
name: claude-plugins-reference-2026
description: Complete reference for Claude Code plugins system (January 2026). Use when creating plugins, understanding plugin.json schema, marketplace configuration, bundling skills/commands/agents/hooks/MCP/LSP servers, plugin caching, validation, or distribution. Covers plugin components, directory structure, installation scopes, environment variables, CLI commands, debugging, and enterprise features.
user-invocable: true
---

# Claude Code Plugins System - Complete Reference (January 2026)

Plugins extend Claude Code with skills, agents, hooks, MCP servers, and LSP servers. This reference provides complete technical specifications for creating and distributing plugins.

---

## Plugin Components Overview

Plugins can include any combination of:

- **Skills**: SKILL.md directories that Claude can invoke automatically
- **Commands**: Markdown files creating `/name` shortcuts (legacy; use skills instead)
- **Agents**: Specialized subagents for specific tasks
- **Hooks**: Event handlers responding to Claude Code events
- **MCP Servers**: Model Context Protocol servers for external tool integration
- **LSP Servers**: Language Server Protocol servers for code intelligence

---

## plugin.json Schema

The `plugin.json` file in `.claude-plugin/` defines your plugin's metadata and configuration.

### Complete Schema Example

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
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Required Fields

| Field  | Type   | Description                               | Example              |
| ------ | ------ | ----------------------------------------- | -------------------- |
| `name` | string | Unique identifier (kebab-case, no spaces) | `"deployment-tools"` |

### Metadata Fields

| Field         | Type   | Description                         | Example                                            |
| ------------- | ------ | ----------------------------------- | -------------------------------------------------- |
| `version`     | string | Semantic version                    | `"2.1.0"`                                          |
| `description` | string | Brief explanation of plugin purpose | `"Deployment automation tools"`                    |
| `author`      | object | Author information                  | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | Documentation URL                   | `"https://docs.example.com"`                       |
| `repository`  | string | Source code URL                     | `"https://github.com/user/plugin"`                 |
| `license`     | string | License identifier                  | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Discovery tags                      | `["deployment", "ci-cd"]`                          |

### Component Path Fields

| Field          | Type           | Description                                                                    | Example                                |
| -------------- | -------------- | ------------------------------------------------------------------------------ | -------------------------------------- |
| `commands`     | string\|array  | Additional command files/directories                                           | `"./custom/cmd.md"` or `["./cmd1.md"]` |
| `agents`       | array          | Agent file paths (must be array of individual files, NOT directory string)     | `["./agents/reviewer.md"]`             |
| `skills`       | string\|array  | Additional skill directories                                                   | `"./custom/skills/"`                   |
| `hooks`        | string\|object | Hook config path or inline config                                              | `"./hooks.json"`                       |
| `mcpServers`   | string\|object | MCP config path or inline config                                               | `"./mcp-config.json"`                  |
| `outputStyles` | string\|array  | Additional output style files/directories                                      | `"./styles/"`                          |
| `lspServers`   | string\|object | Language Server Protocol config for code intelligence (go to definition, etc.) | `"./.lsp.json"`                        |

**Path behavior rules:**

- Custom paths supplement default directories - they don't replace them
- If `commands/` exists, it's loaded in addition to custom command paths
- All paths must be relative to plugin root and start with `./`
- Multiple paths can be specified as arrays
- **CRITICAL**: `agents` field must ALWAYS be an array of individual file paths, never a directory string

**Common validation errors**:

```json
// CORRECT agents field
"agents": ["./agents/security-reviewer.md", "./agents/code-formatter.md"]

// INCORRECT - will fail validation
"agents": "./agents/"
"agents": "./custom/agents/"
```

---

## Plugin Directory Structure

### Standard Layout

```
enterprise-plugin/
├── .claude-plugin/           # Metadata directory
│   └── plugin.json          # Required: plugin manifest
├── commands/                 # Default command location
│   ├── status.md
│   └── logs.md
├── agents/                   # Default agent location
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook configurations
│   ├── hooks.json           # Main hook config
│   └── security-hooks.json  # Additional hooks
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # License file
└── CHANGELOG.md             # Version history
```

**Critical**: The `.claude-plugin/` directory contains ONLY the `plugin.json` file. All other directories (commands/, agents/, skills/, hooks/) must be at the plugin root, not inside `.claude-plugin/`.

### File Locations Reference

| Component       | Default Location             | Purpose                                    |
| --------------- | ---------------------------- | ------------------------------------------ |
| **Manifest**    | `.claude-plugin/plugin.json` | Required metadata file                     |
| **Commands**    | `commands/`                  | Skill Markdown files (legacy; use skills/) |
| **Agents**      | `agents/`                    | Subagent Markdown files                    |
| **Skills**      | `skills/`                    | Skills with `<name>/SKILL.md` structure    |
| **Hooks**       | `hooks/hooks.json`           | Hook configuration                         |
| **MCP servers** | `.mcp.json`                  | MCP server definitions                     |
| **LSP servers** | `.lsp.json`                  | Language server configurations             |

---

## Plugin Components Reference

### Skills

Plugins add skills to Claude Code, creating `/name` shortcuts that you or Claude can invoke.

**Location**: `skills/` or `commands/` directory in plugin root

**Skill structure**:

```
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

**Integration behavior:**

- Skills and commands are automatically discovered when the plugin is installed
- Claude can invoke them automatically based on task context
- Skills can include supporting files alongside SKILL.md

### Agents

Plugins can provide specialized subagents for specific tasks that Claude can invoke automatically when appropriate.

**Location**: `agents/` directory in plugin root

**File format**: Markdown files with YAML frontmatter describing agent capabilities

**Integration points:**

- Agents appear in the `/agents` interface
- Claude can invoke agents automatically based on task context
- Agents can be invoked manually by users
- Plugin agents work alongside built-in Claude agents

### Hooks

Plugins can provide event handlers that respond to Claude Code events automatically.

**Location**: `hooks/hooks.json` in plugin root, or inline in plugin.json

**Format**: JSON configuration with event matchers and actions

**Hook configuration**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Available events**:

- `PreToolUse`: Before Claude uses any tool
- `PostToolUse`: After Claude successfully uses any tool
- `PostToolUseFailure`: After Claude tool execution fails
- `PermissionRequest`: When a permission dialog is shown
- `UserPromptSubmit`: When user submits a prompt
- `Notification`: When Claude Code sends notifications
- `Stop`: When Claude attempts to stop
- `SubagentStart`: When a subagent is started
- `SubagentStop`: When a subagent attempts to stop
- `Setup`: When `--init`, `--init-only`, or `--maintenance` flags are used
- `SessionStart`: At the beginning of sessions
- `SessionEnd`: At the end of sessions
- `PreCompact`: Before conversation history is compacted

For complete hook reference and examples, see [Claude Hooks Reference](https://code.claude.com/docs/en/hooks.md)

**Hook types:**

- `command`: Execute shell commands or scripts
- `prompt`: Evaluate a prompt with an LLM (uses `$ARGUMENTS` placeholder for context)
- `agent`: Run an agentic verifier with tools for complex verification tasks

### MCP Servers

Plugins can bundle Model Context Protocol (MCP) servers to connect Claude Code with external tools and services.

**Location**: `.mcp.json` in plugin root, or inline in plugin.json

**Format**: Standard MCP server configuration

**MCP server configuration**:

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Integration behavior:**

- Plugin MCP servers start automatically when the plugin is enabled
- Servers appear as standard MCP tools in Claude's toolkit
- Server capabilities integrate seamlessly with Claude's existing tools
- Plugin servers can be configured independently of user MCP servers

### LSP Servers

Plugins can provide Language Server Protocol (LSP) servers to give Claude real-time code intelligence while working on your codebase.

LSP integration provides:

- **Instant diagnostics**: Claude sees errors and warnings immediately after each edit
- **Code navigation**: go to definition, find references, and hover information
- **Language awareness**: type information and documentation for code symbols

**Location**: `.lsp.json` in plugin root, or inline in `plugin.json`

**Format**: JSON configuration mapping language server names to their configurations

**`.lsp.json` file format**:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Inline in `plugin.json`**:

```json
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Required fields:**

| Field                 | Description                                  |
| --------------------- | -------------------------------------------- |
| `command`             | The LSP binary to execute (must be in PATH)  |
| `extensionToLanguage` | Maps file extensions to language identifiers |

**Optional fields:**

| Field                   | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `args`                  | Command-line arguments for the LSP server                 |
| `transport`             | Communication transport: `stdio` (default) or `socket`    |
| `env`                   | Environment variables to set when starting the server     |
| `initializationOptions` | Options passed to the server during initialization        |
| `settings`              | Settings passed via `workspace/didChangeConfiguration`    |
| `workspaceFolder`       | Workspace folder path for the server                      |
| `startupTimeout`        | Max time to wait for server startup (milliseconds)        |
| `shutdownTimeout`       | Max time to wait for graceful shutdown (milliseconds)     |
| `restartOnCrash`        | Whether to automatically restart the server if it crashes |
| `maxRestarts`           | Maximum number of restart attempts before giving up       |

**Important**: You must install the language server binary separately. LSP plugins configure how Claude Code connects to a language server, but they don't include the server itself.

**Available LSP plugins:**

| Plugin           | Language server            | Install command                                                                            |
| ---------------- | -------------------------- | ------------------------------------------------------------------------------------------ |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` or `npm install -g pyright`                                          |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                     |
| `rust-lsp`       | rust-analyzer              | [See rust-analyzer installation](https://rust-analyzer.github.io/manual.html#installation) |

---

## Plugin Caching and File Resolution

For security and verification purposes, Claude Code copies plugins to a cache directory rather than using them in-place. Understanding this behavior is important when developing plugins that reference external files.

### How Plugin Caching Works

When you install a plugin, Claude Code copies the plugin files to a cache directory:

- **For marketplace plugins with relative paths**: The path specified in the `source` field is copied recursively. For example, if your marketplace entry specifies `"source": "./plugins/my-plugin"`, the entire `./plugins` directory is copied.
- **For plugins with `.claude-plugin/plugin.json`**: The implicit root directory (the directory containing `.claude-plugin/plugin.json`) is copied recursively.

### Path Traversal Limitations

Plugins cannot reference files outside their copied directory structure. Paths that traverse outside the plugin root (such as `../shared-utils`) will not work after installation because those external files are not copied to the cache.

### Working with External Dependencies

If your plugin needs to access files outside its directory, you have two options:

**Option 1: Use symlinks**

Create symbolic links to external files within your plugin directory. Symlinks are honored during the copy process:

```bash
# Inside your plugin directory
ln -s /path/to/shared-utils ./shared-utils
```

The symlinked content will be copied into the plugin cache.

**Option 2: Restructure your marketplace**

Set the plugin path to a parent directory that contains all required files, then provide the rest of the plugin manifest directly in the marketplace entry:

```json
{
  "name": "my-plugin",
  "source": "./",
  "description": "Plugin that needs root-level access",
  "commands": ["./plugins/my-plugin/commands/"],
  "agents": ["./plugins/my-plugin/agents/"],
  "strict": false
}
```

This approach copies the entire marketplace root, giving your plugin access to sibling directories.

**Note**: Symlinks that point to locations outside the plugin's logical root are followed during copying. This provides flexibility while maintaining the security benefits of the caching system.

---

## Plugin Installation Scopes

When you install a plugin, you choose a **scope** that determines where the plugin is available and who else can use it:

| Scope     | Settings file                 | Use case                                                 |
| --------- | ----------------------------- | -------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`     | Personal plugins available across all projects (default) |
| `project` | `.claude/settings.json`       | Team plugins shared via version control                  |
| `local`   | `.claude/settings.local.json` | Project-specific plugins, gitignored                     |
| `managed` | `managed-settings.json`       | Managed plugins (read-only, update only)                 |

---

## Environment Variables

**`${CLAUDE_PLUGIN_ROOT}`**: Contains the absolute path to your plugin directory. Use this in hooks, MCP servers, and scripts to ensure correct paths regardless of installation location.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

**`${CLAUDE_PROJECT_DIR}`**: Project root directory (where Claude Code was started).

---

## Plugin Marketplaces

### Marketplace Schema

Create `.claude-plugin/marketplace.json` in your repository root:

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

### Required Marketplace Fields

| Field     | Type   | Description                         | Example        |
| --------- | ------ | ----------------------------------- | -------------- |
| `name`    | string | Marketplace identifier (kebab-case) | `"acme-tools"` |
| `owner`   | object | Marketplace maintainer information  |                |
| `plugins` | array  | List of available plugins           |                |

**Reserved names**: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `life-sciences` are reserved for official Anthropic use.

### Plugin Sources

#### Relative paths

For plugins in the same repository:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

**Note**: Relative paths only work when users add your marketplace via Git (GitHub, GitLab, or git URL). If users add your marketplace via a direct URL to the `marketplace.json` file, relative paths will not resolve correctly.

#### GitHub repositories

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

You can pin to a specific branch, tag, or commit:

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Field  | Type   | Description                                                           |
| ------ | ------ | --------------------------------------------------------------------- |
| `repo` | string | Required. GitHub repository in `owner/repo` format                    |
| `ref`  | string | Optional. Git branch or tag (defaults to repository default branch)   |
| `sha`  | string | Optional. Full 40-character git commit SHA to pin to an exact version |

#### Git repositories

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

You can pin to a specific branch, tag, or commit:

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Field | Type   | Description                                                           |
| ----- | ------ | --------------------------------------------------------------------- |
| `url` | string | Required. Full git repository URL (must end with `.git`)              |
| `ref` | string | Optional. Git branch or tag (defaults to repository default branch)   |
| `sha` | string | Optional. Full 40-character git commit SHA to pin to an exact version |

---

## CLI Commands Reference

Claude Code provides CLI commands for non-interactive plugin management, useful for scripting and automation.

### plugin install

Install a plugin from available marketplaces.

```bash
claude plugin install <plugin> [options]
```

**Arguments:**

- `<plugin>`: Plugin name or `plugin-name@marketplace-name` for a specific marketplace

**Options:**

| Option                | Description                                       | Default |
| --------------------- | ------------------------------------------------- | ------- |
| `-s, --scope <scope>` | Installation scope: `user`, `project`, or `local` | `user`  |
| `-h, --help`          | Display help for command                          |         |

**Examples:**

```bash
# Install to user scope (default)
claude plugin install formatter@my-marketplace

# Install to project scope (shared with team)
claude plugin install formatter@my-marketplace --scope project

# Install to local scope (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Remove an installed plugin.

```bash
claude plugin uninstall <plugin> [options]
```

**Arguments:**

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option                | Description                                         | Default |
| --------------------- | --------------------------------------------------- | ------- |
| `-s, --scope <scope>` | Uninstall from scope: `user`, `project`, or `local` | `user`  |
| `-h, --help`          | Display help for command                            |         |

**Aliases:** `remove`, `rm`

### plugin enable

Enable a disabled plugin.

```bash
claude plugin enable <plugin> [options]
```

**Arguments:**

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option                | Description                                    | Default |
| --------------------- | ---------------------------------------------- | ------- |
| `-s, --scope <scope>` | Scope to enable: `user`, `project`, or `local` | `user`  |
| `-h, --help`          | Display help for command                       |         |

### plugin disable

Disable a plugin without uninstalling it.

```bash
claude plugin disable <plugin> [options]
```

**Arguments:**

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option                | Description                                     | Default |
| --------------------- | ----------------------------------------------- | ------- |
| `-s, --scope <scope>` | Scope to disable: `user`, `project`, or `local` | `user`  |
| `-h, --help`          | Display help for command                        |         |

### plugin update

Update a plugin to the latest version.

```bash
claude plugin update <plugin> [options]
```

**Arguments:**

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option                | Description                                               | Default |
| --------------------- | --------------------------------------------------------- | ------- |
| `-s, --scope <scope>` | Scope to update: `user`, `project`, `local`, or `managed` | `user`  |
| `-h, --help`          | Display help for command                                  |         |

---

## Debugging and Development Tools

### Debugging Commands

Use `claude --debug` to see plugin loading details:

```bash
claude --debug
```

This shows:

- Which plugins are being loaded
- Any errors in plugin manifests
- Command, agent, and hook registration
- MCP server initialization

### Common Issues

| Issue                               | Cause                                  | Solution                                                                 |
| ----------------------------------- | -------------------------------------- | ------------------------------------------------------------------------ |
| Plugin not loading                  | Invalid `plugin.json`                  | Validate JSON syntax with `claude plugin validate` or `/plugin validate` |
| `agents: Invalid input`             | Used directory string instead of array | Change `"agents": "./agents/"` to `"agents": ["./agents/file.md"]`       |
| Commands not appearing              | Wrong directory structure              | Ensure `commands/` at root, not in `.claude-plugin/`                     |
| Hooks not firing                    | Script not executable                  | Run `chmod +x script.sh`                                                 |
| MCP server fails                    | Missing `${CLAUDE_PLUGIN_ROOT}`        | Use variable for all plugin paths                                        |
| Path errors                         | Absolute paths used                    | All paths must be relative and start with `./`                           |
| LSP `Executable not found in $PATH` | Language server not installed          | Install the binary (e.g., `npm install -g typescript-language-server`)   |

### Validation Commands

```bash
# CLI (from terminal)
claude plugin validate .
claude plugin validate ./path/to/plugin

# In Claude Code session
/plugin validate .
/plugin validate ./path/to/plugin
```

### Testing Without Installation

```bash
# Load plugin for current session only
claude --plugin-dir ./my-plugin

# Load multiple plugins
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

---

## Enterprise Features

### Required Marketplaces for Teams

Configure your repository so team members are automatically prompted to install your marketplace when they trust the project folder. Add your marketplace to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

You can also specify which plugins should be enabled by default:

```json
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

### Managed Marketplace Restrictions

For organizations requiring strict control over plugin sources, administrators can restrict which plugin marketplaces users are allowed to add using the `strictKnownMarketplaces` setting in managed settings.

When `strictKnownMarketplaces` is configured in managed settings, the restriction behavior depends on the value:

| Value               | Behavior                                                         |
| ------------------- | ---------------------------------------------------------------- |
| Undefined (default) | No restrictions. Users can add any marketplace                   |
| Empty array `[]`    | Complete lockdown. Users cannot add any new marketplaces         |
| List of sources     | Users can only add marketplaces that match the allowlist exactly |

**Common configurations:**

Disable all marketplace additions:

```json
{
  "strictKnownMarketplaces": []
}
```

Allow specific marketplaces only:

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

Allow all marketplaces from an internal git server using regex pattern matching:

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**How restrictions work:**

Restrictions are validated early in the plugin installation process, before any network requests or filesystem operations occur. This prevents unauthorized marketplace access attempts.

The allowlist uses exact matching for most source types. For a marketplace to be allowed, all specified fields must match exactly:

- For GitHub sources: `repo` is required, and `ref` or `path` must also match if specified in the allowlist
- For URL sources: the full URL must match exactly
- For `hostPattern` sources: the marketplace host is matched against the regex pattern

Because `strictKnownMarketplaces` is set in managed settings, individual users and project configurations cannot override these restrictions.

---

## Private Repository Authentication

| Provider  | Environment variables        | Notes                                     |
| --------- | ---------------------------- | ----------------------------------------- |
| GitHub    | `GITHUB_TOKEN` or `GH_TOKEN` | Personal access token or GitHub App token |
| GitLab    | `GITLAB_TOKEN` or `GL_TOKEN` | Personal access token or project token    |
| Bitbucket | `BITBUCKET_TOKEN`            | App password or repository access token   |

Set the token in your shell configuration (e.g., `.bashrc`, `.zshrc`) or pass it when running Claude Code:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**For manual installation and updates:** Claude Code uses your existing git credential helpers. If `git clone` works for a private repository in your terminal, it works in Claude Code too.

**For background auto-updates:** Set the appropriate authentication token in your environment. GitHub Actions automatically provides `GITHUB_TOKEN` for repositories in the same organization.

---

## Distribution and Versioning

### Version Management

Follow semantic versioning for plugin releases:

```json
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**Version format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backward-compatible additions)
- **PATCH**: Bug fixes (backward-compatible fixes)

**Best practices:**

- Start at `1.0.0` for your first stable release
- Update the version in `plugin.json` before distributing changes
- Document changes in a `CHANGELOG.md` file
- Use pre-release versions like `2.0.0-beta.1` for testing

---

## Constraints and Limitations

- Plugins copied to cache, not used in-place
- Cannot reference files outside plugin directory (`../` fails)
- LSP servers require separate binary installation
- All paths must be relative, start with `./`
- Path traversal (`..`) not allowed
- Scripts must be executable (`chmod +x`)
- Reserved marketplace names: `claude-code-marketplace`, `anthropic-plugins`, `agent-skills`

---

## Sources

- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md) (accessed 2026-01-28)
- [Create Plugins](https://code.claude.com/docs/en/plugins.md) (accessed 2026-01-28)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md) (accessed 2026-01-28)
- [Skills Reference](https://code.claude.com/docs/en/skills.md)
- [Hooks Reference](https://code.claude.com/docs/en/hooks.md)
- [MCP Reference](https://code.claude.com/docs/en/mcp.md)
