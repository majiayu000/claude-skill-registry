---
name: create-plugin
description: Create a new Claude Code plugin with proper directory structure and manifest. Use when the user wants to create a new plugin from scratch. Sets up plugin.json, directory structure, and optional components.
---

# Create Plugin Skill

Create new Claude Code plugins with proper structure and configuration.

## Plugin Directory Structure

```
plugin-name/
├── .claude-plugin/           # Required: Metadata directory
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Optional: Command definitions
│   ├── command1.md
│   └── command2.md
├── agents/                   # Optional: Agent definitions
│   ├── agent1.md
│   └── agent2.md
├── skills/                   # Optional: Agent Skills
│   ├── skill-name/
│   │   └── SKILL.md
│   └── another-skill/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Optional: Hook configurations
│   ├── hooks.json           # Main hook config
│   └── additional-hooks.json
├── .mcp.json                # Optional: MCP server definitions
├── scripts/                 # Optional: Hook and utility scripts
│   ├── script1.sh
│   └── script2.py
├── LICENSE                  # Optional: License file
├── CHANGELOG.md             # Optional: Version history
└── README.md                # Optional: Documentation
```

## Plugin Manifest (plugin.json)

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case recommended) |
| `version` | string | Semantic version (e.g., "1.2.0") |
| `description` | string | Brief description of the plugin |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `author` | object | Author information |
| `author.name` | string | Author's name (required if author present) |
| `author.email` | string | Author's email |
| `author.url` | string | Author's website or GitHub profile |
| `homepage` | string | Plugin documentation URL |
| `repository` | string | Git repository URL |
| `license` | string | License identifier (e.g., "MIT", "Apache-2.0") |
| `keywords` | array | Searchable keywords |
| `commands` | string or array | Custom command locations (directory or file paths) |
| `agents` | array | Array of agent file paths (must end with .md) |
| `hooks` | string | Custom hook configuration file location |
| `mcpServers` | string | Custom MCP server configuration file location |

## CRITICAL: Manifest Format

### Commands Configuration

Commands MUST be a **string** (directory path) or **array of strings** (file paths):

**CORRECT - Directory path:**
```json
{
  "commands": "./commands/"
}
```

**CORRECT - Array of file paths:**
```json
{
  "commands": ["./commands/lint.md", "./commands/format.md"]
}
```

**CORRECT - Single custom path:**
```json
{
  "commands": "./custom/commands/special.md"
}
```

**WRONG - Object format (INVALID):**
```json
{
  "commands": {
    "my-command": {
      "description": "...",
      "source": "..."
    }
  }
}
```

### Agents Configuration

Agents MUST be an **array of file paths** ending with `.md`:

**CORRECT:**
```json
{
  "agents": [
    "./agents/my-agent.md",
    "./agents/another-agent.md"
  ]
}
```

**CORRECT - Single agent:**
```json
{
  "agents": ["./agents/expert.md"]
}
```

**WRONG - Directory path (INVALID):**
```json
{
  "agents": "./agents/"
}
```

**WRONG - Object format (INVALID):**
```json
{
  "agents": {
    "agent-name": {
      "description": "...",
      "file": "..."
    }
  }
}
```

### Skills Auto-Discovery

Skills are automatically discovered from the `skills/` directory. No manifest entry needed.

Each skill must be in its own folder with a `SKILL.md` file:
```
skills/
├── skill-name/
│   └── SKILL.md
└── another-skill/
    └── SKILL.md
```

## Example Manifests

### Minimal
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A simple plugin for Claude Code"
}
```

### With Commands and Agents
```json
{
  "name": "code-quality",
  "version": "1.0.0",
  "description": "Code quality tools including linting and review",
  "author": {
    "name": "Developer",
    "email": "dev@example.com"
  },
  "commands": "./commands/",
  "agents": [
    "./agents/code-reviewer.md"
  ]
}
```

### Complete
```json
{
  "name": "enterprise-plugin",
  "version": "1.2.0",
  "description": "Enterprise-grade development plugin",
  "author": {
    "name": "Jane Developer",
    "email": "jane@example.com",
    "url": "https://github.com/janedev"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/janedev/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "security", "compliance"],
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/security-expert.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json"
}
```

## Creation Process

1. **Plan the plugin**
   - Define the plugin's purpose
   - List components needed (commands, agents, skills)
   - Choose a descriptive name (kebab-case)

2. **Create directory structure**
   ```bash
   mkdir -p plugin-name/.claude-plugin
   mkdir -p plugin-name/agents
   mkdir -p plugin-name/commands
   mkdir -p plugin-name/skills
   ```

3. **Create plugin.json**
   ```json
   {
     "name": "plugin-name",
     "version": "1.0.0",
     "description": "Plugin description",
     "author": {
       "name": "Author Name"
     },
     "commands": "./commands/",
     "agents": ["./agents/my-agent.md"]
   }
   ```

4. **Add components**
   - Add agents to `agents/` with proper frontmatter
   - Add commands to `commands/` with proper frontmatter
   - Add skills to `skills/skill-name/SKILL.md`

5. **IMPORTANT: Register in marketplace.json**
   Every new plugin MUST be added to `.claude-plugin/marketplace.json`

6. **Validate the plugin**
   ```bash
   ./scripts/validate-all-plugins.sh plugin-name
   ```

7. **Commit the changes**
   Include both the plugin directory AND marketplace.json

## Adding to Marketplace (REQUIRED)

**Every new plugin must be registered in `.claude-plugin/marketplace.json`.**

Add a new entry to the `plugins` array:

```json
{
  "plugins": [
    // ... existing plugins ...
    {
      "name": "plugin-name",
      "description": "Brief plugin description",
      "source": "./plugins/plugin-name",
      "category": "development"
    }
  ]
}
```

### Marketplace Entry Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Must match plugin.json name |
| `description` | Yes | Brief description for marketplace listing |
| `source` | Yes | Relative path to plugin directory |
| `category` | Yes | One of: `productivity`, `development`, `security` |

### Categories

- `productivity` - Workflow, project management, documentation tools
- `development` - Code quality, testing, language-specific tools
- `security` - Security, compliance, privacy tools

## Testing Your Plugin

1. Add marketplace: `/plugin marketplace add ./path-to-marketplace`
2. Install plugin: `/plugin install plugin-name@marketplace-name`
3. Verify with `/help` to see commands
4. Test components individually

## Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing required file: .claude-plugin/plugin.json` | No manifest | Create `.claude-plugin/plugin.json` |
| `plugin.json missing required fields` | Missing name, version, or description | Add all required fields |
| `'author' must be an object` | Author is a string | Use object format with `name` field |
| `Invalid JSON syntax` | Trailing commas, missing quotes | Fix JSON syntax |
| `agents: Invalid input: must end with ".md"` | Using directory path for agents | Use array of file paths: `["./agents/name.md"]` |

## Best Practices

1. **Use semantic versioning** for the `version` field
2. **Include descriptive keywords** for better discoverability
3. **Provide author information** for attribution and support
4. **Link to repository** for open-source contributions
5. **Document your plugin** with a README.md
6. **Track changes** with CHANGELOG.md
7. **Use clear names** that describe the plugin's purpose
8. **Keep descriptions concise** but informative

## Migration Guide

If you have an existing plugin without `plugin.json`:

```bash
cd plugins/your-plugin
mkdir -p .claude-plugin
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Your plugin description",
  "author": {
    "name": "Your Name"
  }
}
EOF
```
