---
name: create-claude-plugin
description: Guide for creating Claude Code plugins that bundle skills, agents, commands, hooks, and MCP servers for distribution. Covers plugin structure, marketplace.json format, installation, testing, and publishing. Use when the user wants to create plugins, distribute skills/agents, build marketplaces, or mentions creating/packaging/publishing plugins.
---

# Create Claude Plugin Guide

This skill helps you create Claude Code plugins - bundled collections of skills, agents, commands, hooks, and MCP servers that can be distributed and shared via plugin marketplaces. Plugins enable team collaboration and community sharing of Claude Code extensions.

## Quick Start

When creating a new plugin, follow this workflow:

1. **Define purpose** - What capabilities will the plugin provide?
2. **Choose components** - Skills, agents, commands, hooks, MCP servers?
3. **Create structure** - Set up plugin directory with components
4. **Configure marketplace** - Create marketplace.json with metadata
5. **Test locally** - Install and verify plugin works correctly
6. **Document thoroughly** - Write comprehensive README
7. **Version appropriately** - Use semantic versioning (1.0.0)
8. **Publish marketplace** - Share via git repository or distribution channel

## What is a Plugin?

**Claude Code Plugins** are packaged collections of extensions that provide:

- **Skills:** Automatic capabilities with context-based discovery
- **Agents:** Specialized AI assistants for specific domains
- **Commands:** Reusable slash commands for common workflows
- **Hooks:** Event-driven automation and formatting
- **MCP Servers:** External service integrations

Plugins enable:
- **Team sharing:** Distribute standardized workflows to teammates
- **Community contribution:** Share capabilities with broader community
- **Versioned distribution:** Manage updates with semantic versioning
- **Bundled functionality:** Package related capabilities together

## Plugin vs Individual Components

### When to Create a Plugin

**Use plugins for:**
- Distributing multiple related capabilities
- Team-wide standardization
- Community sharing
- Versioned capability management
- Complex multi-component workflows

**Examples:**
- Document processing suite (Excel, Word, PDF skills)
- Development workflow bundle (code review, testing, deployment)
- Design system toolkit (components, themes, guidelines)
- API integration package (authentication, requests, error handling)

### When to Use Individual Components

**Use individual files for:**
- Personal productivity tools
- Project-specific customizations
- Rapid prototyping
- One-off utilities

## Plugin Structure

### Basic Plugin Directory

```
my-plugin/
├── .claude-plugin/
│   └── marketplace.json      # Plugin metadata (required)
├── skills/                   # Agent Skills (optional)
│   └── my-skill/
│       └── SKILL.md
├── agents/                   # Subagents (optional)
│   └── my-agent.md
├── commands/                 # Slash commands (optional)
│   └── my-command.md
├── hooks/                    # Event handlers (optional)
│   └── hooks.json
├── mcp/                      # MCP server configs (optional)
│   └── .mcp.json
├── README.md                 # Documentation (recommended)
├── LICENSE.txt               # License information (recommended)
└── THIRD_PARTY_NOTICES.md   # Third-party attributions (if applicable)
```

### Minimal Plugin

Minimum requirement is `.claude-plugin/marketplace.json`:

```
simple-plugin/
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    └── simple-skill/
        └── SKILL.md
```

## Marketplace Configuration (marketplace.json)

### Basic Format

```json
{
  "name": "my-plugin-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "metadata": {
    "description": "Brief marketplace description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "What this plugin does",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/my-skill"
      ]
    }
  ]
}
```

### Field Descriptions

**Marketplace Level:**

- `name` (required): Unique marketplace identifier (lowercase, hyphens)
- `owner` (required): Owner information with name and email
- `metadata` (required): Marketplace description and version

**Plugin Level:**

- `name` (required): Plugin identifier (appears in `/plugin list`)
- `description` (required): What the plugin provides (shown to users)
- `source` (required): Plugin root directory (usually `./`)
- `strict` (optional): Strict validation mode (default: false)
- `skills` (optional): Array of skill directory paths
- `agents` (optional): Array of agent file paths
- `commands` (optional): Array of command file paths
- `hooks` (optional): Hooks configuration path
- `mcp` (optional): MCP configuration path

### Complete Example: Multi-Component Plugin

```json
{
  "name": "devtools-marketplace",
  "owner": {
    "name": "Development Team",
    "email": "devtools@company.com"
  },
  "metadata": {
    "description": "Development workflow tools and utilities",
    "version": "2.1.0"
  },
  "plugins": [
    {
      "name": "devtools",
      "description": "Comprehensive development workflow toolkit with code review, testing, and deployment capabilities",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/code-review",
        "./skills/test-automation",
        "./skills/deployment"
      ],
      "agents": [
        "./agents/code-reviewer.md",
        "./agents/test-runner.md",
        "./agents/deploy-engineer.md"
      ],
      "commands": [
        "./commands/review.md",
        "./commands/test.md",
        "./commands/deploy.md"
      ],
      "hooks": "./hooks/hooks.json",
      "mcp": "./mcp/.mcp.json"
    }
  ]
}
```

### Multiple Plugins in One Marketplace

```json
{
  "name": "company-tools",
  "owner": {
    "name": "Company Engineering",
    "email": "eng@company.com"
  },
  "metadata": {
    "description": "Company-wide Claude Code extensions",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "frontend-tools",
      "description": "React and frontend development utilities",
      "source": "./",
      "skills": [
        "./frontend/component-generator",
        "./frontend/style-guide"
      ],
      "agents": [
        "./frontend/react-expert.md"
      ]
    },
    {
      "name": "backend-tools",
      "description": "Backend API and database tools",
      "source": "./",
      "skills": [
        "./backend/api-design",
        "./backend/database-migration"
      ],
      "agents": [
        "./backend/api-architect.md",
        "./backend/db-optimizer.md"
      ]
    },
    {
      "name": "devops-tools",
      "description": "CI/CD and infrastructure utilities",
      "source": "./",
      "skills": [
        "./devops/deployment",
        "./devops/monitoring"
      ],
      "commands": [
        "./devops/deploy.md",
        "./devops/rollback.md"
      ]
    }
  ]
}
```

## Component Integration

### Adding Skills to Plugin

**Directory structure:**
```
plugin/
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    ├── pdf-processor/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   └── extract.py
    │   └── templates/
    │       └── report.md
    └── excel-analyzer/
        └── SKILL.md
```

**marketplace.json:**
```json
{
  "plugins": [
    {
      "name": "document-tools",
      "skills": [
        "./skills/pdf-processor",
        "./skills/excel-analyzer"
      ]
    }
  ]
}
```

### Adding Agents to Plugin

**Directory structure:**
```
plugin/
├── .claude-plugin/
│   └── marketplace.json
└── agents/
    ├── code-reviewer.md
    ├── test-automator.md
    └── security-auditor.md
```

**marketplace.json:**
```json
{
  "plugins": [
    {
      "name": "quality-tools",
      "agents": [
        "./agents/code-reviewer.md",
        "./agents/test-automator.md",
        "./agents/security-auditor.md"
      ]
    }
  ]
}
```

### Adding Commands to Plugin

**Directory structure:**
```
plugin/
├── .claude-plugin/
│   └── marketplace.json
└── commands/
    ├── review.md
    ├── test.md
    └── git/
        ├── commit.md
        └── pr.md
```

**marketplace.json:**
```json
{
  "plugins": [
    {
      "name": "workflow-commands",
      "commands": [
        "./commands/review.md",
        "./commands/test.md",
        "./commands/git/commit.md",
        "./commands/git/pr.md"
      ]
    }
  ]
}
```

### Adding Hooks to Plugin

**Directory structure:**
```
plugin/
├── .claude-plugin/
│   └── marketplace.json
└── hooks/
    ├── hooks.json
    └── scripts/
        └── format.sh
```

**hooks/hooks.json:**
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "npx prettier --write $(jq -r '.tool_input.file_path')"
        }
      ]
    }
  ]
}
```

**marketplace.json:**
```json
{
  "plugins": [
    {
      "name": "formatter-plugin",
      "hooks": "./hooks/hooks.json"
    }
  ]
}
```

### Adding MCP Servers to Plugin

**Directory structure:**
```
plugin/
├── .claude-plugin/
│   └── marketplace.json
└── mcp/
    └── .mcp.json
```

**mcp/.mcp.json:**
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${HOME}/projects"
      ]
    }
  }
}
```

**marketplace.json:**
```json
{
  "plugins": [
    {
      "name": "integration-plugin",
      "mcp": "./mcp/.mcp.json"
    }
  ]
}
```

## Complete Plugin Examples

### Example 1: Document Processing Suite

**Structure:**
```
document-suite/
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   ├── pdf/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── extract.py
│   ├── excel/
│   │   └── SKILL.md
│   ├── word/
│   │   └── SKILL.md
│   └── powerpoint/
│       └── SKILL.md
├── README.md
└── LICENSE.txt
```

**marketplace.json:**
```json
{
  "name": "document-processing-marketplace",
  "owner": {
    "name": "Document Tools Team",
    "email": "docs@example.com"
  },
  "metadata": {
    "description": "Comprehensive document processing capabilities",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "document-suite",
      "description": "Process PDF, Excel, Word, and PowerPoint documents with advanced capabilities",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/pdf",
        "./skills/excel",
        "./skills/word",
        "./skills/powerpoint"
      ]
    }
  ]
}
```

### Example 2: Full Stack Development Toolkit

**Structure:**
```
fullstack-toolkit/
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   ├── api-design/
│   │   └── SKILL.md
│   ├── database-migration/
│   │   └── SKILL.md
│   └── frontend-components/
│       └── SKILL.md
├── agents/
│   ├── backend-architect.md
│   ├── frontend-developer.md
│   └── database-optimizer.md
├── commands/
│   ├── api-scaffold.md
│   ├── component-create.md
│   └── migration-generate.md
├── hooks/
│   └── hooks.json
└── README.md
```

**marketplace.json:**
```json
{
  "name": "fullstack-marketplace",
  "owner": {
    "name": "Full Stack Team",
    "email": "fullstack@company.com"
  },
  "metadata": {
    "description": "Complete full stack development toolkit",
    "version": "2.0.0"
  },
  "plugins": [
    {
      "name": "fullstack-toolkit",
      "description": "Backend, frontend, and database development tools with agents, skills, and automation",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/api-design",
        "./skills/database-migration",
        "./skills/frontend-components"
      ],
      "agents": [
        "./agents/backend-architect.md",
        "./agents/frontend-developer.md",
        "./agents/database-optimizer.md"
      ],
      "commands": [
        "./commands/api-scaffold.md",
        "./commands/component-create.md",
        "./commands/migration-generate.md"
      ],
      "hooks": "./hooks/hooks.json"
    }
  ]
}
```

### Example 3: Security Audit Plugin

**Structure:**
```
security-audit/
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   └── security-scan/
│       ├── SKILL.md
│       └── scripts/
│           ├── scan.sh
│           └── analyze.py
├── agents/
│   ├── security-auditor.md
│   └── vulnerability-analyst.md
├── commands/
│   ├── security-scan.md
│   └── vuln-report.md
└── README.md
```

**marketplace.json:**
```json
{
  "name": "security-marketplace",
  "owner": {
    "name": "Security Team",
    "email": "security@company.com"
  },
  "metadata": {
    "description": "Security auditing and vulnerability analysis tools",
    "version": "1.5.0"
  },
  "plugins": [
    {
      "name": "security-audit",
      "description": "Comprehensive security scanning, vulnerability detection, and audit reporting",
      "source": "./",
      "strict": true,
      "skills": [
        "./skills/security-scan"
      ],
      "agents": [
        "./agents/security-auditor.md",
        "./agents/vulnerability-analyst.md"
      ],
      "commands": [
        "./commands/security-scan.md",
        "./commands/vuln-report.md"
      ]
    }
  ]
}
```

## Local Testing

### Setup Test Environment

**1. Create test marketplace directory:**
```bash
mkdir -p ~/test-marketplace/my-plugin
cd ~/test-marketplace/my-plugin
```

**2. Create plugin structure:**
```bash
mkdir -p .claude-plugin skills/test-skill
```

**3. Create marketplace.json:**
```json
{
  "name": "test-marketplace",
  "owner": {
    "name": "Test Developer",
    "email": "test@example.com"
  },
  "metadata": {
    "description": "Test plugin marketplace",
    "version": "0.1.0"
  },
  "plugins": [
    {
      "name": "test-plugin",
      "description": "Testing plugin functionality",
      "source": "./",
      "skills": ["./skills/test-skill"]
    }
  ]
}
```

**4. Create test skill:**
```bash
cat > skills/test-skill/SKILL.md <<'EOF'
---
name: test-skill
description: Simple test skill for validation
---

# Test Skill

This is a test skill to verify plugin installation works correctly.

When invoked, respond: "Test skill is working!"
EOF
```

### Install Plugin Locally

**Add marketplace:**
```bash
# In Claude Code
/plugin marketplace add ~/test-marketplace/my-plugin
```

**Install plugin:**
```bash
/plugin install test-plugin@test-marketplace
```

**Verify installation:**
```bash
/plugin list
```

Should show: `test-plugin@test-marketplace (enabled)`

### Test Plugin Components

**Test skill activation:**
- Restart Claude Code
- Use trigger words from skill description
- Verify skill activates automatically

**Test agent:**
- Use `/agents` to see if agent appears
- Explicitly invoke: "Use test-agent to..."

**Test command:**
- Type `/test-command` to verify it appears
- Execute and verify behavior

**Test hooks:**
- Trigger hook event (e.g., edit file)
- Verify hook executes

### Iterate and Update

**Update plugin:**
1. Modify plugin files
2. Uninstall: `/plugin uninstall test-plugin@test-marketplace`
3. Reinstall: `/plugin install test-plugin@test-marketplace`
4. Restart Claude Code
5. Test changes

## Documentation Best Practices

### README.md Template

```markdown
# Plugin Name

Brief description of what the plugin provides.

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Installation

### Via Plugin Marketplace

\`\`\`bash
/plugin marketplace add https://github.com/username/plugin-name
/plugin install plugin-name@marketplace-name
\`\`\`

### Local Installation

\`\`\`bash
git clone https://github.com/username/plugin-name.git
/plugin marketplace add /path/to/plugin-name
/plugin install plugin-name@local-marketplace
\`\`\`

## Usage

### Skills

**skill-name**: Description and trigger keywords

Example: "Process PDF document"

### Agents

**agent-name**: Description and invocation method

Example: "/use agent-name to review code"

### Commands

**`/command-name`**: Description and arguments

Example: `/command-name arg1 arg2`

## Configuration

If plugin requires environment variables or configuration:

\`\`\`bash
export API_KEY="your-key"
export CONFIG_PATH="/path/to/config"
\`\`\`

## Requirements

- Node.js 18+ (if using npm packages)
- Python 3.8+ (if using Python scripts)
- Specific tools or dependencies

## Troubleshooting

### Issue 1
Description of common issue and solution.

### Issue 2
Description and resolution.

## License

[License type] - See LICENSE.txt

## Contributing

Contribution guidelines if open source.

## Support

Contact information or issue tracker link.
```

### LICENSE.txt

Choose appropriate license:
- **MIT:** Permissive, allows commercial use
- **Apache 2.0:** Permissive with patent grant
- **GPL-3.0:** Copyleft, requires derivative works to be open source
- **Proprietary:** Custom terms for internal/commercial use

### THIRD_PARTY_NOTICES.md

If using third-party code or libraries:

```markdown
# Third-Party Notices

This plugin includes code from the following sources:

## Library Name
- Author: Name
- License: MIT
- URL: https://github.com/author/library
- Copyright (c) Year Author Name

[License text...]

## Another Library
...
```

## Versioning Strategy

### Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH`

**MAJOR**: Breaking changes (2.0.0)
- Plugin structure changes
- Incompatible skill/agent updates
- Removed functionality

**MINOR**: New features (1.1.0)
- New skills or agents
- Additional commands
- Backward-compatible enhancements

**PATCH**: Bug fixes (1.0.1)
- Bug fixes
- Documentation updates
- Minor improvements

**Examples:**
- `1.0.0` - Initial release
- `1.1.0` - Added new skill
- `1.1.1` - Fixed skill bug
- `2.0.0` - Restructured plugin (breaking change)

### Version in marketplace.json

Update version in metadata:

```json
{
  "metadata": {
    "description": "Plugin description",
    "version": "1.2.0"
  }
}
```

### Changelog

Maintain CHANGELOG.md:

```markdown
# Changelog

## [1.2.0] - 2025-10-30

### Added
- New security-scan skill
- Database migration commands
- Auto-formatting hooks

### Changed
- Improved code-review agent accuracy
- Updated documentation

### Fixed
- Bug in test-runner command
- Hook execution timing issue

## [1.1.0] - 2025-09-15

### Added
- Frontend development agent
- Component generation skill

## [1.0.0] - 2025-08-01

### Added
- Initial release
- Basic skills and agents
```

## Distribution Methods

### Git Repository (Recommended)

**1. Create repository:**
```bash
git init
git add .
git commit -m "Initial plugin release"
git remote add origin https://github.com/username/plugin-name.git
git push -u origin main
```

**2. Users install via URL:**
```bash
/plugin marketplace add https://github.com/username/plugin-name
/plugin install plugin-name@marketplace-name
```

### GitHub Releases

**1. Tag version:**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**2. Create GitHub release:**
- Go to repository → Releases → Create new release
- Select tag, add release notes
- Attach any additional files

### Private Distribution

**Team repository:**
```bash
# Internal GitLab/GitHub Enterprise
/plugin marketplace add https://git.company.com/team/plugin-name
```

**Local network:**
```bash
# Shared network drive
/plugin marketplace add /mnt/shared/plugins/plugin-name
```

## Plugin Management Commands

### User Commands

**Browse and discover:**
```bash
/plugin                           # Open plugin browser
/plugin list                      # List installed plugins
/plugin marketplace list          # List configured marketplaces
```

**Install and manage:**
```bash
/plugin install name@marketplace  # Install plugin
/plugin enable name@marketplace   # Enable plugin
/plugin disable name@marketplace  # Disable plugin
/plugin uninstall name@marketplace # Remove plugin
```

**Marketplace operations:**
```bash
/plugin marketplace add <path-or-url>    # Add marketplace
/plugin marketplace remove <name>         # Remove marketplace
/plugin marketplace refresh <name>        # Update marketplace
```

### Developer Testing

**Rapid iteration:**
```bash
# Make changes
/plugin uninstall test-plugin@test-marketplace
/plugin install test-plugin@test-marketplace
# Restart Claude Code
```

**Verify components:**
```bash
/skills                          # Check skills loaded
/agents                          # Check agents available
/help                            # Check commands listed
/mcp                             # Check MCP servers
```

## Best Practices Checklist

When creating a plugin:

- [ ] Clear, descriptive plugin name (lowercase, hyphens)
- [ ] Comprehensive description in marketplace.json
- [ ] All component paths are correct (relative to plugin root)
- [ ] Skills have proper SKILL.md with frontmatter
- [ ] Agents follow subagent format with YAML frontmatter
- [ ] Commands use proper argument handling
- [ ] Hooks use valid JSON configuration
- [ ] MCP servers use environment variables for secrets
- [ ] README.md with installation and usage instructions
- [ ] LICENSE.txt with appropriate license
- [ ] CHANGELOG.md tracking version history
- [ ] Semantic versioning in metadata.version
- [ ] No hardcoded secrets or credentials
- [ ] Tested locally before distribution
- [ ] Git repository with proper .gitignore
- [ ] Tagged releases for versions

## Security Considerations

### Credential Management

**Never include:**
- API keys
- Passwords
- Tokens
- Private keys

**Always use:**
- Environment variables: `${API_KEY}`
- Instructions for users to set credentials
- .gitignore for sensitive files

### Plugin Trust

**For users:**
- Review plugin source before installation
- Check owner and marketplace reputation
- Verify what data plugin can access
- Review hooks and MCP server configurations

**For developers:**
- Clearly document data access requirements
- Use minimal necessary permissions
- Explain security implications in README
- Keep dependencies updated

### Malicious Code Prevention

**Avoid:**
- Network calls to untrusted servers
- File system access without documentation
- Credential exfiltration
- Arbitrary code execution

## Troubleshooting

### Plugin Not Appearing

**Check marketplace configuration:**
```bash
/plugin marketplace list
```

**Verify marketplace.json syntax:**
- Valid JSON format
- All required fields present
- Correct paths to components

### Plugin Install Fails

**Common issues:**
- Invalid marketplace.json structure
- Missing required files
- Incorrect path references
- Git repository not accessible

**Debug:**
1. Validate JSON syntax
2. Check file paths exist
3. Test git clone manually
4. Review error messages

### Components Not Loading

**Skills not activating:**
- Restart Claude Code after installation
- Check SKILL.md has valid frontmatter
- Verify description has trigger keywords

**Agents not available:**
- Check agent files have proper YAML frontmatter
- Verify agent paths in marketplace.json
- Use `/agents` to confirm agent loaded

**Commands not appearing:**
- Check command files have .md extension
- Verify paths in marketplace.json
- Use `/help` to list commands

### Version Conflicts

**Multiple plugin versions:**
- Uninstall old version before installing new
- Check `/plugin list` for duplicates
- Use specific version tags if available

## Advanced Patterns

### Plugin with Dependencies

**Document requirements:**
```markdown
## Requirements

This plugin requires:
- Python 3.8+
- Node.js 18+
- `pip install -r requirements.txt`
- `npm install` in plugin directory

## Setup

\`\`\`bash
cd ~/.claude/plugins/marketplaces/marketplace-name/
pip install -r requirements.txt
npm install
\`\`\`
```

### Multi-Language Plugin

**Structure:**
```
plugin/
├── skills/
│   ├── python-tools/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── tool.py
│   └── javascript-tools/
│       ├── SKILL.md
│       └── scripts/
│           └── tool.js
├── agents/
│   ├── python-expert.md
│   └── js-expert.md
└── .claude-plugin/
    └── marketplace.json
```

### Plugin Updates

**Communicate changes:**
```markdown
# Upgrading from v1.x to v2.0

## Breaking Changes
- Skill X renamed to Y
- Agent Z removed (use new Agent A instead)
- Command /old replaced with /new

## Migration Steps
1. Uninstall old version
2. Install new version
3. Update environment variables
4. Review new documentation
```

## Key Principles

1. **Bundle related capabilities** - Group cohesive functionality together
2. **Document thoroughly** - README, comments, usage examples
3. **Version semantically** - Follow SemVer for predictable updates
4. **Test extensively** - Verify all components before distribution
5. **Secure by default** - Use environment variables, no hardcoded secrets
6. **Clear ownership** - Identify maintainers and support channels
7. **License appropriately** - Choose license matching intended use
8. **Structure logically** - Organize components by feature or domain
9. **Update regularly** - Fix bugs, add features, update dependencies
10. **Communicate changes** - Changelog, release notes, migration guides

## Workflow Summary

When user asks to create a plugin:

1. **Define scope** - What capabilities should be bundled?
2. **Choose components** - Skills, agents, commands, hooks, MCP?
3. **Create structure** - Set up directory with .claude-plugin/
4. **Build components** - Create skills, agents, commands, etc.
5. **Configure marketplace.json** - Define metadata and paths
6. **Write documentation** - README, LICENSE, CHANGELOG
7. **Test locally** - Install and verify functionality
8. **Version appropriately** - Use semantic versioning
9. **Publish to git** - Create repository, tag releases
10. **Share with users** - Provide installation instructions

Remember: Plugins package multiple Claude Code extensions for easy distribution and team sharing. Focus on cohesive functionality, thorough documentation, and proper versioning for successful plugin distribution.
