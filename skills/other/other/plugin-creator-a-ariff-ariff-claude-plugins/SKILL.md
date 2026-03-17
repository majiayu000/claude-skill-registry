---
name: plugin-creator
description: >-
  Use this skill when asked to "create a plugin", "build a new plugin",
  "make a Claude Code plugin", "scaffold plugin", "plugin structure",
  "add commands/agents/skills/hooks to plugin", or when helping with plugin development.
---

# Plugin Creator Skill

This skill provides comprehensive guidance for creating Claude Code plugins with proper structure, following official patterns from the Anthropic claude-code repository.

## Plugin Directory Structure

A complete Claude Code plugin follows this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin metadata manifest
├── agents/                  # Optional: Agent definitions (.md files)
│   └── agent-name.md
├── skills/                  # Optional: Skill directories
│   └── skill-name/
│       └── SKILL.md
├── commands/                # Optional: Slash commands (.md files)
│   └── command-name.md
├── hooks/                   # Optional: Event handlers
│   └── hooks.json           # Hook configuration
└── README.md                # Plugin documentation
```

## Plugin Manifest (plugin.json)

Required fields:
- `name`: Plugin identifier (kebab-case, 3-50 chars)

Optional fields:
- `version`: Semantic version (X.Y.Z)
- `description`: Brief description
- `author`: Object with `name` and optional `email`
- `mcpServers`: MCP server configurations

Example:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": {
    "name": "Your Name",
    "email": "email@example.com"
  }
}
```

## Creating Agents

Agent files go in `agents/` directory with `.md` extension.

Agent frontmatter fields:
- `name`: Agent identifier (required)
- `description`: Triggering conditions with `<example>` blocks
- `model`: `inherit` (default), `sonnet`, `opus`, or `haiku`
- `color`: `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`
- `tools`: Array of allowed tools (optional, all tools if omitted)

Agent template:
```markdown
---
name: my-agent
description: >-
  Use this agent when the user asks to "do something", "perform action",
  or mentions specific keywords.

  <example>
  Context: User wants to perform specific task
  user: "Please do the thing"
  assistant: "I'll use the my-agent agent to help with this."
  <commentary>
  User explicitly requested the functionality this agent provides.
  </commentary>
  </example>
model: inherit
color: green
tools: ["Read", "Write", "Bash"]
---

You are an expert [role] specializing in [domain].

**Core Responsibilities:**
1. First responsibility
2. Second responsibility
3. Third responsibility

**Process:**
1. Analyze the request
2. Plan the approach
3. Execute the solution
4. Verify the results

**Quality Standards:**
- Standard one
- Standard two

**Output Format:**
Describe expected output format here.
```

## Creating Skills

Skills go in `skills/` directory, each in its own subdirectory with a `SKILL.md` file.

Skill frontmatter:
- `name`: Skill identifier (required)
- `description`: When to trigger (with strong trigger phrases)

Skill template:
```markdown
---
name: my-skill
description: >-
  Use this skill when asked to "specific action", "related task",
  "keyword phrase", or when dealing with [domain].
---

# Skill Name

Brief description of what this skill provides.

## When to Use

- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## Core Concepts

Explain the main concepts and techniques.

## Best Practices

1. Practice one
2. Practice two
3. Practice three

## Examples

### Example 1: Basic Usage
```code
example code here
```

### Example 2: Advanced Usage
```code
more complex example
```
```

## Creating Commands

Commands go in `commands/` directory with `.md` extension.

Command frontmatter:
- `description`: What the command does (shown in `/` menu)
- `argument-hint`: Placeholder text for arguments (optional)
- `allowed-tools`: Array of tools command can use (optional)

Command template:
```markdown
---
description: Brief description of what command does
argument-hint: <optional argument>
allowed-tools: ["Read", "Write", "Bash"]
---

Instructions for Claude when this command is invoked.

You should:
1. Step one
2. Step two
3. Step three
```

## Creating Hooks

Hooks go in `hooks/hooks.json` and execute on specific events.

Hook events:
- `PreToolUse`: Before tool execution (validate/block)
- `PostToolUse`: After tool execution (audit/react)
- `Stop`: When Claude stops (force continue)
- `SubagentStop`: When subagent stops
- `SessionStart`: When session begins (load context)
- `SessionEnd`: When session ends (cleanup)
- `UserPromptSubmit`: When user submits prompt
- `PreCompact`: Before context compaction
- `Notification`: On notifications

hooks.json template:
```json
{
  "description": "Plugin hooks description",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-write.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

Hook types:
- `command`: Execute bash script
- `prompt`: LLM-based evaluation (for Stop, SubagentStop)

Important: Use `${CLAUDE_PLUGIN_ROOT}` for portable paths within plugin.

## Hook Scripts

Create executable scripts in `scripts/` directory:

```bash
#!/usr/bin/env bash
# scripts/validate-write.sh

# Read JSON input from stdin
INPUT=$(cat)

# Extract fields
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Validation logic
if [[ "$FILE_PATH" == *.env* ]]; then
  echo "Cannot write to .env files" >&2
  exit 2  # Exit 2 = block with message to Claude
fi

exit 0  # Exit 0 = allow
```

Exit codes:
- `0`: Success, allow action
- `2`: Block action, stderr shown to Claude
- Other: Non-blocking error, stderr shown to user

## Plugin Creation Workflow

1. **Plan** - Determine needed components (agents, skills, commands, hooks)
2. **Create structure** - Set up directories and plugin.json
3. **Implement components** - Create each component file
4. **Add hooks** - If automation needed
5. **Document** - Write README.md
6. **Test** - Use `claude --plugin-dir /path/to/plugin`
7. **Validate** - Check structure matches specification

## Quick Start Commands

Create minimal plugin:
```bash
mkdir -p my-plugin/.claude-plugin
echo '{"name":"my-plugin","version":"1.0.0"}' > my-plugin/.claude-plugin/plugin.json
```

Add an agent:
```bash
mkdir -p my-plugin/agents
# Create agents/my-agent.md with frontmatter
```

Add a skill:
```bash
mkdir -p my-plugin/skills/my-skill
# Create skills/my-skill/SKILL.md
```

Add hooks:
```bash
mkdir -p my-plugin/hooks my-plugin/scripts
# Create hooks/hooks.json and scripts/*.sh
```

## References

- Official plugins: https://github.com/anthropics/claude-code/tree/main/plugins
- Plugin documentation: https://code.claude.com/docs/en/plugins
- Hooks reference: https://code.claude.com/docs/en/hooks
