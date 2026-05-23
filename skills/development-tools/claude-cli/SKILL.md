---
name: claude-cli
description: Use claude CLI for interactive AI sessions, scripting with print mode, MCP server management, and plugin configuration. Master session management, tool control, and automation workflows.
---

# Claude CLI - Command Line Interface

You are a specialist in using the `claude` CLI (Claude Code). This skill provides comprehensive workflows, best practices, and common patterns for interactive sessions, scripting, MCP management, and automation.

## What is Claude CLI?

The `claude` CLI is the command-line interface for Claude Code that provides:
- **Interactive sessions** - Default conversational mode for coding and problem-solving
- **Print mode** - Non-interactive output for pipes, scripts, and automation
- **Session management** - Continue, resume, and fork conversations
- **MCP integration** - Configure and manage Model Context Protocol servers
- **Plugin system** - Extend functionality with marketplace plugins
- **Tool control** - Fine-grained control over available tools
- **Flexible output** - Text, JSON, or streaming formats

## Core Modes

### Interactive Mode (Default)

```bash
# Start interactive session
claude

# Start with a prompt
claude "explain this codebase"

# Continue last conversation
claude --continue
claude -c

# Resume specific session
claude --resume
claude -r SESSION_ID

# Fork a session (new ID, same history)
claude --resume SESSION_ID --fork-session
```

### Print Mode (Non-Interactive)

```bash
# Single response, then exit
claude --print "what is rust?"
claude -p "explain async/await"

# Pipe input
echo "explain this code" | claude -p

# Pipe output
claude -p "list all rust files" | grep "src/"

# JSON output for parsing
claude -p --output-format json "summarize this"

# Streaming JSON (realtime)
claude -p --output-format stream-json "analyze logs"
```

## Session Management

### Continue Last Conversation

```bash
# Continue most recent session
claude --continue
claude -c

# Continue and fork (new session ID)
claude -c --fork-session
```

### Resume Specific Session

```bash
# Interactive selection
claude --resume
claude -r

# Specific session ID
claude -r abc123-def456-789

# Resume and fork
claude -r abc123 --fork-session
```

### Custom Session ID

```bash
# Use specific UUID
claude --session-id 12345678-1234-1234-1234-123456789abc
```

## Model Selection

### Model Aliases

```bash
# Use Sonnet (default)
claude --model sonnet

# Use Opus
claude --model opus

# Use Haiku
claude --model haiku
```

### Full Model Names

```bash
# Specific version
claude --model claude-sonnet-4-5-20250929
claude --model claude-opus-4-20250514
claude --model claude-haiku-4-20250430
```

### Fallback Model (Print Mode Only)

```bash
# Fallback to Haiku if Sonnet overloaded
claude -p --fallback-model haiku "analyze this"
```

## Tool Control

### Specify Available Tools

```bash
# Only specific tools
claude -p --tools "Bash,Read,Edit" "refactor code"

# Default tools
claude -p --tools default "write function"

# No tools (chat only)
claude -p --tools "" "explain concept"
```

### Allow/Disallow Tools

```bash
# Allow specific tool patterns
claude --allowed-tools "Bash(git:*)" "commit changes"
claude --allowed-tools "Bash(npm:*),Read,Edit" "update package"

# Disallow tools
claude --disallowed-tools "Bash(rm:*)" "clean directory"
claude --disallowed-tools "Write" "analyze code"

# Multiple patterns
claude --allowed-tools "Bash(git:*)" "Bash(cargo:*)" "rust workflow"
```

## System Prompts

### Set System Prompt

```bash
# Replace default system prompt
claude --system-prompt "You are a Rust expert. Focus on idiomatic code."

# Append to default
claude --append-system-prompt "Always explain your reasoning."
```

## Permission Modes

```bash
# Auto-accept edits (no confirmation)
claude --permission-mode acceptEdits

# Bypass all permissions
claude --permission-mode bypassPermissions

# Plan mode (planning workflow)
claude --permission-mode plan

# Default (normal confirmations)
claude --permission-mode default
```

### Dangerous Permissions

```bash
# Skip ALL permission checks (use in sandboxes only)
claude --dangerously-skip-permissions

# Allow skipping as an option (not default)
claude --allow-dangerously-skip-permissions
```

## MCP Server Management

### List MCP Servers

```bash
# List configured servers
claude mcp list
```

### Add MCP Server

```bash
# Add HTTP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Add SSE server
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Add stdio server
claude mcp add --transport stdio myserver npx -y my-mcp-server

# Add with environment variables
claude mcp add --transport stdio airtable \
  --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

### Add from JSON

```bash
# Add stdio server from JSON
claude mcp add-json myserver '{"command":"node","args":["server.js"]}'

# Add SSE server from JSON
claude mcp add-json sse-server '{"url":"https://example.com/sse"}'
```

### Import from Claude Desktop

```bash
# Import all MCP servers from Claude Desktop
claude mcp add-from-claude-desktop

# Import specific server
claude mcp add-from-claude-desktop --name myserver
```

### Remove MCP Server

```bash
# Remove server
claude mcp remove myserver
```

### Get MCP Server Details

```bash
# Show configuration
claude mcp get myserver
```

### Reset Project MCP Choices

```bash
# Reset approved/rejected project-scoped servers
claude mcp reset-project-choices
```

### MCP Configuration

```bash
# Load MCP from config file
claude --mcp-config config.json

# Load from JSON string
claude --mcp-config '{"myserver":{"command":"node","args":["server.js"]}}'

# Multiple configs
claude --mcp-config config1.json config2.json

# Strict mode (only use specified config)
claude --strict-mcp-config --mcp-config config.json
```

### Project-Level MCP Configuration (.mcp.json)

**IMPORTANT**: Project-specific MCP servers belong in a `.mcp.json` file at the project root.

#### .mcp.json File Structure

Create `.mcp.json` in your project root with this structure:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

#### Common Patterns

**Node.js MCP server:**
```json
{
  "mcpServers": {
    "myserver": {
      "command": "node",
      "args": ["./dist/index.js"],
      "env": {
        "API_KEY": ""
      }
    }
  }
}
```

**Python/uvx MCP server:**
```json
{
  "mcpServers": {
    "knowledge_base": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type",
        "persistent",
        "--data-dir",
        "/path/to/data"
      ],
      "env": {
        "ANONYMIZED_TELEMETRY": "false"
      }
    }
  }
}
```

**Language server integration:**
```json
{
  "mcpServers": {
    "gopls": {
      "command": "/path/to/mcp-language-server",
      "args": ["--workspace", ".", "--lsp", "gopls", "--", "-mode=stdio"],
      "transport": "stdio"
    }
  }
}
```

**Docker/Podman container:**
```json
{
  "mcpServers": {
    "github": {
      "command": "podman",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

**Multiple servers in one project:**
```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "gdrive": {
      "command": "gdrive",
      "args": ["mcp", "stdio"]
    }
  }
}
```

#### Usage

When Claude CLI runs in a project directory:

```bash
# Automatically detects and loads .mcp.json
claude

# View which servers are loaded
claude mcp list

# Reset project server approvals
claude mcp reset-project-choices
```

**Key Points:**
- Place `.mcp.json` at project root
- Claude prompts to approve/reject project servers on first use
- Use for project-specific tools (language servers, project APIs, local databases)
- Separate from global user MCP configuration
- Safe to commit to version control (but NEVER commit secrets in `env`)

#### .gitignore Pattern for Secrets

If your `.mcp.json` contains secrets, create a template:

```bash
# .mcp.json.example (commit this)
{
  "mcpServers": {
    "myserver": {
      "command": "node",
      "args": ["./dist/index.js"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}

# .gitignore
.mcp.json
```

Then developers copy `.mcp.json.example` to `.mcp.json` and add their credentials.

## Plugin Management

### List Available Plugins

```bash
# Browse marketplace
claude plugin marketplace
```

### Install Plugin

```bash
# Install from default marketplace
claude plugin install my-plugin

# Install from specific marketplace
claude plugin install my-plugin@my-marketplace
```

### Uninstall Plugin

```bash
claude plugin uninstall my-plugin
claude plugin remove my-plugin
```

### Enable/Disable Plugin

```bash
# Disable plugin
claude plugin disable my-plugin

# Enable plugin
claude plugin enable my-plugin
```

### Validate Plugin

```bash
# Validate plugin manifest
claude plugin validate /path/to/plugin/
```

### Load Plugin Directory

```bash
# Load plugins from custom directory
claude --plugin-dir /path/to/plugins/

# Multiple directories
claude --plugin-dir dir1/ dir2/
```

## Settings and Configuration

### Settings File

```bash
# Load from file
claude --settings /path/to/settings.json

# Load from JSON string
claude --settings '{"verbose":true,"model":"opus"}'
```

### Setting Sources

```bash
# Only user settings
claude --setting-sources user

# User and project settings
claude --setting-sources user,project

# All sources (user, project, local)
claude --setting-sources user,project,local
```

### Additional Directories

```bash
# Allow access to extra directories
claude --add-dir /path/to/data/

# Multiple directories
claude --add-dir /data/ /cache/ /logs/
```

## Output Formats (Print Mode)

### Text Output (Default)

```bash
# Plain text response
claude -p "summarize file.txt"
```

### JSON Output

```bash
# Single JSON result
claude -p --output-format json "analyze code"

# Parse with jq
claude -p --output-format json "list issues" | jq '.response'
```

### Streaming JSON

```bash
# Real-time streaming
claude -p --output-format stream-json "long analysis"

# Include partial messages
claude -p --output-format stream-json --include-partial-messages "task"
```

### Input Formats

```bash
# Text input (default)
echo "prompt" | claude -p

# Streaming JSON input
cat input.jsonl | claude -p --input-format stream-json

# Replay user messages (for acknowledgment)
cat input.jsonl | claude -p \
  --input-format stream-json \
  --output-format stream-json \
  --replay-user-messages
```

## Debug and Verbose Modes

### Debug Mode

```bash
# Enable all debug output
claude --debug

# Filter debug categories
claude --debug "api,hooks"

# Exclude categories
claude --debug "!statsig,!file"

# Debug with print mode
claude -p --debug "test prompt"
```

### Verbose Mode

```bash
# Override verbose setting
claude --verbose
```

## IDE Integration

```bash
# Auto-connect to IDE on startup
claude --ide
```

## Maintenance Commands

### Check Health

```bash
# Run doctor to check auto-updater
claude doctor
```

### Update

```bash
# Check for updates and install
claude update
```

### Install Specific Version

```bash
# Install stable version
claude install stable

# Install latest version
claude install latest

# Install specific version
claude install 1.2.3
```

### Setup Authentication

```bash
# Setup long-lived auth token
claude setup-token
```

### Migrate Installer

```bash
# Migrate from global npm to local install
claude migrate-installer
```

## Common Workflows

### Workflow 1: Quick Analysis (Print Mode)

```bash
# Analyze file and exit
claude -p "summarize errors in app.log"

# Pipe to other tools
claude -p "extract function names from code.rs" | sort | uniq
```

### Workflow 2: Scripted Automation

```bash
# JSON output for parsing
result=$(claude -p --output-format json "count TODO comments")
count=$(echo "$result" | jq -r '.response')
echo "Found $count TODOs"
```

### Workflow 3: Restricted Tool Access

```bash
# Only allow git operations
claude --allowed-tools "Bash(git:*)" -p "show recent commits"

# Disallow destructive operations
claude --disallowed-tools "Bash(rm:*)" "Bash(mv:*)" "clean project"
```

### Workflow 4: Custom System Prompt

```bash
# Specialized code reviewer
claude --system-prompt "You are a security-focused code reviewer. \
  Look for vulnerabilities, SQL injection, XSS, and auth issues." \
  "review authentication.py"
```

### Workflow 5: Session Forking

```bash
# Resume session and fork for experimentation
claude -r abc123 --fork-session

# Try different approach without affecting original
claude -c --fork-session
```

### Workflow 6: MCP Server Setup

```bash
# Add custom MCP server
claude mcp add --transport stdio mytools npx -y my-tools-server

# Test in session
claude "use mytools to analyze data"

# Remove if not needed
claude mcp remove mytools
```

### Workflow 7: Project-Level MCP Configuration

```bash
# Create .mcp.json in project root
cat > .mcp.json <<'EOF'
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
EOF

# Start claude - automatically detects .mcp.json
claude

# Approve project servers when prompted
# Servers are now available for this project only

# Reset approvals if needed
claude mcp reset-project-choices
```

### Workflow 8: Plugin Workflow

```bash
# Install plugin
claude plugin install code-analyzer

# Use in session
claude "analyze code quality with code-analyzer"

# Disable temporarily
claude plugin disable code-analyzer
```

### Workflow 9: Batch Processing with Stream JSON

```bash
# Process multiple prompts
cat prompts.jsonl | claude -p \
  --input-format stream-json \
  --output-format stream-json > results.jsonl
```

### Workflow 10: Model Fallback for Reliability

```bash
# Try Sonnet, fall back to Haiku if overloaded
claude -p --model sonnet --fallback-model haiku "analyze data"
```

### Workflow 11: Sandboxed Execution

```bash
# Safe sandbox with no permissions needed
claude -p --dangerously-skip-permissions --tools "Read" "analyze code"
```

## Best Practices

### 1. Use Print Mode for Scripting

```bash
# Good - print mode for automation
claude -p "count errors" | wc -l

# Avoid - interactive for scripts
claude "count errors"  # Waits for user input
```

### 2. Specify Tools for Security

```bash
# Restrict tools in production scripts
claude -p --tools "Read,Grep" "find pattern"

# Disallow dangerous operations
claude --disallowed-tools "Bash(rm:*)" "cleanup task"
```

### 3. Use JSON for Parsing

```bash
# Easy to parse
claude -p --output-format json "analyze" | jq '.response'

# Harder to parse
claude -p "analyze"  # Mixed output
```

### 4. Fork Sessions for Experimentation

```bash
# Keep original session intact
claude -r session-id --fork-session

# Experiment without fear
```

### 5. Use Fallback Models for Reliability

```bash
# Production scripts should handle overload
claude -p --fallback-model haiku "critical task"
```

### 6. Debug with Filtering

```bash
# See relevant debug info only
claude --debug "api,mcp" "test mcp server"

# Exclude noisy categories
claude --debug "!statsig,!analytics" "run workflow"
```

### 7. Organize MCP Servers

```bash
# List before adding
claude mcp list

# Use clear names
claude mcp add --transport stdio db-tools npx -y db-mcp-server

# Remove unused servers
claude mcp remove old-server
```

### 8. Use System Prompts for Consistency

```bash
# Create specialized assistants
claude --append-system-prompt "Always explain your reasoning step by step."
```

## Quick Reference

```bash
# Interactive mode
claude                                  # Start session
claude -c                               # Continue last session
claude -r                               # Resume session (interactive)
claude -r SESSION_ID                    # Resume specific session

# Print mode
claude -p "prompt"                      # Single response
claude -p --output-format json "prompt" # JSON output
claude -p --tools "Bash,Read" "prompt"  # Specific tools

# Model selection
claude --model opus                     # Use Opus
claude --fallback-model haiku           # Fallback model

# Tool control
claude --allowed-tools "Bash(git:*)"    # Allow only git
claude --disallowed-tools "Bash(rm:*)"  # Disallow rm

# MCP management
claude mcp list                         # List servers
claude mcp add --transport stdio name cmd # Add server
claude mcp remove name                  # Remove server

# Plugin management
claude plugin install name              # Install plugin
claude plugin uninstall name            # Uninstall plugin
claude plugin enable name               # Enable plugin
claude plugin disable name              # Disable plugin

# System prompts
claude --system-prompt "prompt"         # Set system prompt
claude --append-system-prompt "text"    # Append to system

# Debug
claude --debug                          # Enable debug
claude --debug "category,!exclude"      # Filter debug

# Maintenance
claude doctor                           # Check health
claude update                           # Update CLI
claude setup-token                      # Setup auth token
```

## Common Patterns

### Pattern 1: Safe Code Analysis

```bash
claude -p --tools "Read,Grep" "analyze security vulnerabilities in src/"
```

### Pattern 2: Automated Git Workflow

```bash
claude -p --allowed-tools "Bash(git:*)" "review and summarize recent commits"
```

### Pattern 3: JSON Parsing Pipeline

```bash
claude -p --output-format json "list all functions" | \
  jq -r '.response' | \
  grep "pub fn"
```

### Pattern 4: Streaming Analysis

```bash
cat large_log.txt | \
  claude -p --output-format stream-json "find error patterns" | \
  jq -r 'select(.type == "response") | .content'
```

### Pattern 5: Multi-Model Fallback

```bash
claude -p --model sonnet --fallback-model haiku "time-sensitive analysis"
```

## Tips and Tricks

1. **Session Management**: Use `--fork-session` to experiment without affecting original conversation
2. **Tool Safety**: Always use `--allowed-tools` or `--disallowed-tools` for untrusted prompts
3. **Automation**: Prefer `--output-format json` for reliable parsing in scripts
4. **Performance**: Use `--fallback-model haiku` for faster responses when quality isn't critical
5. **Debugging**: Use `--debug "!noisy,!category"` to exclude verbose logs
6. **MCP Servers**: Test new servers with `claude --strict-mcp-config` to isolate issues
7. **Plugins**: Disable unused plugins to reduce startup time
8. **Print Mode**: Always use `-p` in scripts to avoid interactive prompts

## Integration Examples

### With Git

```bash
# Review changes before commit
claude -p --allowed-tools "Bash(git:*),Read" "review staged changes and suggest commit message"
```

### With CI/CD

```bash
# Automated code review
claude -p --tools "Read,Grep" --output-format json "analyze code quality" > report.json
```

### With Logs

```bash
# Real-time log analysis
tail -f app.log | claude -p --output-format stream-json "detect anomalies"
```

### With Makefiles/Justfiles

```just
# Analyze code quality
analyze:
    claude -p --tools "Read,Grep" "run code quality analysis"

# Generate documentation
docs:
    claude -p --output-format json "generate API docs from code" | jq -r '.response' > API.md
```

## Summary

**Primary use cases:**
- Interactive coding sessions (default mode)
- Scripted automation (print mode)
- MCP server integration (global and project-level)
- Plugin management
- Tool-controlled execution

**Key advantages:**
- Flexible output formats (text, JSON, streaming)
- Fine-grained tool control
- Session persistence and forking
- MCP protocol support (use `.mcp.json` for project-specific servers)
- Extensible plugin system

**Most common commands:**
- `claude` - Start interactive session
- `claude -p "prompt"` - Print mode for scripting
- `claude -c` - Continue last conversation
- `claude mcp list` - Manage MCP servers
- `claude --allowed-tools "pattern" "prompt"` - Restrict tool access

**Project-level MCP:**
- Create `.mcp.json` in project root for project-specific MCP servers
- Automatically loaded when Claude runs in that directory
- Separate from global user configuration
