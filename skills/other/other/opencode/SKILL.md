---
name: opencode
version: "1.0.0"
description: OpenCode - Open source AI coding agent for terminal, desktop, and IDE with multi-provider LLM support, custom agents, MCP integration, and granular permissions
---

# OpenCode Skill

**OpenCode** is an open source AI coding agent available as a terminal interface (TUI), desktop app, or IDE extension. It enables developers to work on code projects through conversational interactions with intelligent assistance for code explanation, implementation planning, code modification, and more.

**Key Value Proposition**: A flexible, multi-provider AI assistant with customizable agents, granular permissions, and extensive tool integrations that can be tailored for specific workflows like code review, documentation, security auditing, or development.

## When to Use This Skill

- Setting up OpenCode for a new development environment
- Creating custom agents for specialized coding workflows
- Configuring permissions for team-based development
- Building automated scripts with OpenCode CLI
- Integrating MCP servers for extended capabilities
- Troubleshooting OpenCode configuration or tool issues
- Comparing OpenCode features with other AI coding assistants

## When NOT to Use This Skill

- For Claude Code/Claude CLI specific features (different product)
- For GitHub Copilot configuration (use copilot-specific docs)
- For Cursor IDE settings (different AI editor)
- For generic LLM API usage (use provider-specific skills)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         OpenCode                                 │
│            Terminal UI / Desktop App / IDE Extension             │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│    Agents     │    │    Tools      │    │  Permissions  │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • Build       │    │ • read/write  │    │ • allow       │
│ • Plan        │    │ • edit/patch  │    │ • ask         │
│ • Custom...   │    │ • bash        │    │ • deny        │
│ • Subagents   │    │ • grep/glob   │    │ • Wildcards   │
└───────────────┘    │ • webfetch    │    └───────────────┘
                     │ • lsp         │
                     │ • MCP servers │
                     └───────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  LLM Providers │   │   Sessions    │    │   Commands    │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • OpenAI      │    │ • SQLite      │    │ • /init       │
│ • Claude      │    │ • Persistence │    │ • /undo       │
│ • Gemini      │    │ • Export/     │    │ • /share      │
│ • Groq        │    │   Import      │    │ • Custom...   │
│ • Bedrock     │    └───────────────┘    └───────────────┘
└───────────────┘
```

### Agent Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Primary Agent** | Main assistant for direct interaction | Day-to-day development |
| **Subagent** | Specialized assistant for specific tasks | Research, exploration |
| **Build** (built-in) | Full tool access for development | Writing and modifying code |
| **Plan** (built-in) | Read-only for analysis | Planning without changes |
| **General** (subagent) | Multi-step task execution | Research and investigation |
| **Explore** (subagent) | Codebase navigation | Quick file/code searching |

---

## Installation

### Quick Install (Recommended)

```bash
# Install script
curl -fsSL https://raw.githubusercontent.com/opencode-ai/opencode/refs/heads/main/install | bash

# Homebrew (macOS/Linux)
brew install opencode-ai/tap/opencode

# npm
npm install -g opencode

# Go
go install github.com/opencode-ai/opencode@latest
```

### Verify Installation

```bash
opencode --version
```

---

## Configuration

### Configuration Files

OpenCode uses `opencode.json` in your project root or global config at `~/.config/opencode/`:

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "permission": {
    "edit": "ask",
    "bash": "ask"
  },
  "agent": {
    "build": {
      "model": "claude-sonnet-4-20250514"
    },
    "plan": {
      "model": "claude-sonnet-4-20250514",
      "tools": {
        "write": false,
        "bash": false
      }
    }
  }
}
```

### Environment Variables

```bash
# API Keys (choose your provider)
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."
export GROQ_API_KEY="..."

# OpenCode Settings
export OPENCODE_CONFIG="~/.config/opencode/opencode.json"
export OPENCODE_PERMISSION="ask"  # Default permission level
export OPENCODE_AUTO_SHARE="true"  # Auto-share sessions
export OPENCODE_EXPERIMENTAL_LSP_TOOL="true"  # Enable LSP
```

---

## Tools Reference

### Built-in Tools

| Tool | Description | Permission |
|------|-------------|------------|
| `read` | Read file contents from codebase | allow |
| `write` | Create or overwrite files | edit |
| `edit` | Modify files using exact string replacements | edit |
| `patch` | Apply patch files to code | edit |
| `grep` | Search file contents using regex | allow |
| `glob` | Find files by pattern (e.g., `**/*.js`) | allow |
| `list` | List files and directories | allow |
| `bash` | Execute shell commands | ask |
| `webfetch` | Fetch and read web pages | ask |
| `lsp` | Language Server Protocol (experimental) | allow |
| `skill` | Load SKILL.md file content | allow |
| `question` | Ask user questions during execution | allow |
| `todoread/todowrite` | Task tracking during sessions | allow |

### Tool Configuration

```json
{
  "permission": {
    "*": "ask",
    "read": "allow",
    "grep": "allow",
    "glob": "allow",
    "list": "allow",
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny"
    }
  }
}
```

---

## Creating Custom Agents

### Interactive Creation

```bash
opencode agent create
```

This guides you through:
1. Selecting storage location (global or project)
2. Defining agent purpose
3. Auto-generating system prompts
4. Choosing accessible tools
5. Creating markdown configuration

### Agent Configuration (JSON)

```json
{
  "agent": {
    "reviewer": {
      "description": "Code review specialist",
      "mode": "subagent",
      "model": "claude-sonnet-4-20250514",
      "temperature": 0.3,
      "prompt": ".opencode/agent/reviewer.md",
      "tools": {
        "read": true,
        "grep": true,
        "glob": true,
        "edit": false,
        "bash": false
      },
      "permission": {
        "webfetch": "deny"
      },
      "maxSteps": 20
    }
  }
}
```

### Agent Configuration (Markdown)

Create `.opencode/agent/reviewer.md`:

```markdown
---
description: Code review specialist for quality and security
mode: subagent
model: claude-sonnet-4-20250514
temperature: 0.3
tools:
  read: true
  grep: true
  glob: true
  edit: false
  bash: false
---

You are a code review specialist focused on:

1. Code quality and best practices
2. Security vulnerabilities
3. Performance issues
4. Maintainability concerns

When reviewing code:
- Identify issues by severity (critical, major, minor)
- Provide specific line references
- Suggest concrete improvements
- Consider the project's existing patterns
```

### Agent Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `description` | string | Brief explanation (required) |
| `mode` | string | `primary`, `subagent`, or `all` |
| `model` | string | Override default model |
| `temperature` | float | Response randomness (0.0-1.0) |
| `prompt` | string | Path to system prompt file |
| `tools` | object | Enable/disable specific tools |
| `permission` | object | Override permissions |
| `maxSteps` | number | Limit iterations before text-only |

---

## Custom Commands

### Command Structure

Create `.opencode/command/review.md`:

```markdown
---
description: Review code changes
agent: reviewer
---

Review the following code changes:

$ARGUMENTS

Focus on:
1. Security vulnerabilities
2. Performance issues
3. Code style violations
4. Missing tests
```

### Using Arguments

```markdown
---
description: Create a component
---

Create a new React component named $1 in the $2 directory.

Requirements:
- TypeScript
- Styled with Tailwind
- Include tests
```

Usage: `/component Button components/ui`

### Including Shell Output

```markdown
---
description: Review recent changes
---

Review the following git diff:

`!git diff HEAD~1`

Summarize changes and identify any issues.
```

### File References

```markdown
---
description: Explain architecture
---

Based on the architecture documentation:

@ARCHITECTURE.md

Explain how the authentication system works.
```

---

## CLI Reference

### TUI Mode (Default)

```bash
# Start in current directory
opencode

# Start in specific project
opencode /path/to/project

# Continue last session
opencode --continue

# Use specific session
opencode --session <session-id>

# Override model
opencode --model claude-sonnet-4-20250514
```

### Non-Interactive Mode

```bash
# Run single prompt
opencode run "explain this codebase"

# Run with file context
opencode run --file src/main.ts "add error handling"

# Run custom command
opencode run --command review

# Output format
opencode run --format json "list all functions"
```

### Server Mode

```bash
# Start headless server
opencode serve --port 8080

# Start with web interface
opencode web --port 8080

# Connect to remote server
opencode attach http://localhost:8080
```

### Agent Management

```bash
# Create new agent
opencode agent create

# List all agents
opencode agent list
```

### MCP Integration

```bash
# Add MCP server
opencode mcp add <server-name>

# List MCP servers
opencode mcp list

# Debug MCP connection
opencode mcp debug <server-name>
```

### Session Management

```bash
# List sessions
opencode session list --max-count 10

# Export session
opencode export <session-id>

# Import session
opencode import session.json

# View usage stats
opencode stats --days 7
```

---

## Project Initialization

### Generate AGENTS.md

```bash
opencode
/init
```

This analyzes your project and generates `AGENTS.md` containing:
- Project structure overview
- Key patterns and conventions
- Technology stack
- Important files and directories

**Best Practice**: Commit `AGENTS.md` to version control so OpenCode understands your codebase.

---

## Permissions System

### Permission Levels

| Level | Behavior |
|-------|----------|
| `allow` | Executes without approval |
| `ask` | Prompts for user approval |
| `deny` | Blocks execution |

### Approval Responses

When prompted:
- `once` - Approve single request
- `always` - Approve matching requests for session
- `reject` - Deny the request

### Default Permissions

Most tools default to `allow`, except:
- `doom_loop` - `ask` (safety feature)
- `external_directory` - `ask` (safety feature)
- `.env*` files - `deny` (security)

### Agent-Level Overrides

Agent permissions take precedence over global:

```json
{
  "permission": {
    "bash": "ask"
  },
  "agent": {
    "build": {
      "permission": {
        "bash": "allow"
      }
    }
  }
}
```

---

## Common Use Cases

### Code Review Agent

```markdown
---
description: Systematic code review
mode: subagent
tools:
  read: true
  grep: true
  edit: false
  bash: false
---

You are a code reviewer. For each review:

1. Check for security vulnerabilities
2. Identify performance bottlenecks
3. Ensure code follows project patterns
4. Verify test coverage
5. Suggest improvements

Format findings as:
- CRITICAL: [issue]
- MAJOR: [issue]
- MINOR: [issue]
```

### Documentation Agent

```markdown
---
description: Documentation writer
mode: subagent
tools:
  read: true
  glob: true
  write: true
  bash: false
---

You write clear, comprehensive documentation.

When documenting:
1. Follow project's existing doc style
2. Include code examples
3. Document edge cases
4. Keep language accessible
```

### Security Audit Agent

```markdown
---
description: Security vulnerability scanner
mode: subagent
tools:
  read: true
  grep: true
  bash: false
  webfetch: true
---

You are a security auditor. Scan for:

1. Injection vulnerabilities (SQL, XSS, command)
2. Authentication/authorization issues
3. Sensitive data exposure
4. Insecure dependencies
5. Misconfigurations

Reference OWASP Top 10 for classification.
```

---

## Troubleshooting

### Agent Not Invoking

```
Issue: Custom agent doesn't respond to @mention
```

**Solutions:**
1. Verify agent file is in correct location (`.opencode/agent/` or `~/.config/opencode/agent/`)
2. Check `mode` is set correctly (`subagent` for @mentions)
3. Ensure YAML frontmatter is valid
4. Try `opencode agent list` to verify registration

### Permission Denied

```
Issue: Tool execution blocked unexpectedly
```

**Solutions:**
1. Check global permissions in `opencode.json`
2. Verify agent-specific overrides
3. Use `opencode run --permission allow` for testing
4. Check for conflicting wildcard patterns

### Tool Not Working

```
Issue: grep/glob returns no results
```

**Solutions:**
1. Check if files are in `.gitignore` (excluded by default)
2. Create `.ignore` file to include ignored directories
3. Verify pattern syntax is correct

### LLM Connection Issues

```
Issue: Provider not responding
```

**Solutions:**
1. Verify API key is set correctly
2. Check network connectivity
3. Run `opencode models` to list available models
4. Try `opencode models --refresh` to refresh cache

---

## Resources

### Official Documentation
- [OpenCode Docs](https://opencode.ai/docs/)
- [Agents Guide](https://opencode.ai/docs/agents/)
- [Tools Reference](https://opencode.ai/docs/tools/)
- [Permissions](https://opencode.ai/docs/permissions/)
- [CLI Reference](https://opencode.ai/docs/cli/)

### Source Code
- [GitHub Repository](https://github.com/opencode-ai/opencode)

### Related Projects
- [Charm](https://github.com/charmbracelet) - Terminal UI framework
- [MCP Protocol](https://modelcontextprotocol.io/) - Model Context Protocol

---

## Version History

- **1.0.0** (2026-01-12): Initial skill release
  - Complete OpenCode agent system documentation
  - Built-in and custom agent configuration
  - Tools reference with permission system
  - CLI commands and usage patterns
  - Custom commands and SKILL.md integration
  - MCP server integration
  - Common agent templates (review, docs, security)
  - Troubleshooting guide
