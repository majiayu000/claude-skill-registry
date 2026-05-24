---
name: claude-hooks
description: Guide for creating event-driven hooks for Claude Code. Use when automating responses to tool calls, lifecycle events, or implementing custom validations.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Claude Code Hooks

Guide for creating hooks that execute shell commands or scripts in response to Claude Code events and tool calls.

## When to Use This Skill

Activate this skill when:
- Creating event-driven automations
- Implementing custom validation or formatting
- Integrating with external tools and services
- Setting up project-specific workflows
- Responding to tool execution events

## What Are Hooks?

Hooks are shell commands that execute automatically in response to specific events:

- **Tool Call Hooks**: Trigger before/after specific tool calls
- **Lifecycle Hooks**: Trigger on plugin install/uninstall
- **User Prompt Hooks**: Trigger when users submit prompts
- **Custom Events**: Application-specific trigger points

## Hook Configuration

### Location

Hooks are configured in:
- Plugin: `<plugin-root>/.claude-plugin/hooks.json`
- User-level: `.claude/hooks.json`
- Plugin manifest: Inline in `plugin.json`

### File Structure

**Standalone hooks.json:**
```json
{
  "onToolCall": {
    "Write": {
      "before": ["./hooks/format-check.sh"],
      "after": ["./hooks/lint.sh"]
    },
    "Bash": {
      "before": ["./hooks/validate-command.sh"]
    }
  },
  "onInstall": ["./hooks/setup.sh"],
  "onUninstall": ["./hooks/cleanup.sh"],
  "onUserPromptSubmit": ["./hooks/log-prompt.sh"]
}
```

**Inline in plugin.json:**
```json
{
  "hooks": {
    "onToolCall": {
      "Write": {
        "after": ["prettier --write {{file_path}}"]
      }
    }
  }
}
```

## Hook Types

### Tool Call Hooks

Execute before or after specific tool calls.

**Available Tools:**
- `Read`, `Write`, `Edit`, `MultiEdit`
- `Bash`, `BashOutput`
- `Glob`, `Grep`
- `Task`, `Skill`, `SlashCommand`
- `TodoWrite`
- `WebFetch`, `WebSearch`
- `AskUserQuestion`

**Example:**
```json
{
  "onToolCall": {
    "Write": {
      "before": [
        "echo 'Writing file: {{file_path}}'",
        "./hooks/backup.sh {{file_path}}"
      ],
      "after": [
        "prettier --write {{file_path}}",
        "git add {{file_path}}"
      ]
    },
    "Edit": {
      "after": ["eslint --fix {{file_path}}"]
    }
  }
}
```

### Lifecycle Hooks

Execute during plugin installation/uninstallation.

```json
{
  "onInstall": [
    "./hooks/setup-dependencies.sh",
    "npm install",
    "echo 'Plugin installed successfully'"
  ],
  "onUninstall": [
    "./hooks/cleanup.sh",
    "echo 'Plugin uninstalled'"
  ]
}
```

### User Prompt Submit Hook

Execute when user submits a prompt:

```json
{
  "onUserPromptSubmit": [
    "./hooks/log-interaction.sh '{{prompt}}'",
    "./hooks/check-context.sh"
  ]
}
```

## Hook Variables

Hooks have access to context-specific variables using `{{variable}}` syntax.

### Tool Call Variables

Different tools provide different variables:

**Write Tool:**
- `{{file_path}}`: Path to file being written
- `{{content}}`: Content being written (before hooks only)

**Edit Tool:**
- `{{file_path}}`: Path to file being edited
- `{{old_string}}`: String being replaced
- `{{new_string}}`: Replacement string

**Bash Tool:**
- `{{command}}`: Command being executed

**Read Tool:**
- `{{file_path}}`: Path to file being read

### Global Variables

Available in all hooks:
- `{{cwd}}`: Current working directory
- `{{timestamp}}`: Current Unix timestamp
- `{{user}}`: Current user
- `{{plugin_root}}`: Plugin installation directory

### User Prompt Variables

- `{{prompt}}`: User's submitted prompt text

## Hook Examples

### Auto-Format on Write

```json
{
  "onToolCall": {
    "Write": {
      "after": [
        "prettier --write {{file_path}}",
        "eslint --fix {{file_path}}"
      ]
    }
  }
}
```

### Pre-Commit Validation

```json
{
  "onToolCall": {
    "Bash": {
      "before": ["./hooks/validate-git-command.sh '{{command}}'"]
    }
  }
}
```

**validate-git-command.sh:**
```bash
#!/bin/bash

COMMAND="$1"

# Block force push to main/master
if [[ "$COMMAND" =~ "git push --force" ]] && [[ "$COMMAND" =~ "main|master" ]]; then
  echo "ERROR: Force push to main/master is not allowed"
  exit 1
fi

exit 0
```

### Automatic Backups

```json
{
  "onToolCall": {
    "Write": {
      "before": ["cp {{file_path}} {{file_path}}.backup"]
    },
    "Edit": {
      "before": ["cp {{file_path}} {{file_path}}.backup"]
    }
  }
}
```

### Logging and Analytics

```json
{
  "onToolCall": {
    "Write": {
      "after": ["./hooks/log-file-change.sh {{file_path}}"]
    }
  },
  "onUserPromptSubmit": ["./hooks/log-prompt.sh '{{prompt}}'"]
}
```

**log-file-change.sh:**
```bash
#!/bin/bash

FILE="$1"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "$TIMESTAMP - Modified: $FILE" >> .claude/file-changes.log
```

### Integration with External Tools

```json
{
  "onToolCall": {
    "Write": {
      "after": [
        "notify-send 'File Updated' 'Modified {{file_path}}'",
        "curl -X POST https://api.example.com/notify -d 'file={{file_path}}'"
      ]
    }
  }
}
```

## Hook Execution

### Execution Order

Multiple hooks execute in array order:

```json
{
  "onToolCall": {
    "Write": {
      "after": [
        "echo 'Step 1'",  // Runs first
        "echo 'Step 2'",  // Runs second
        "echo 'Step 3'"   // Runs third
      ]
    }
  }
}
```

### Exit Codes

**Before Hooks:**
- Exit code `0`: Continue with tool execution
- Exit code non-zero: **Block tool execution**, show error to user

**After Hooks:**
- Exit codes are logged but don't affect tool execution
- Tool has already completed

### Error Handling

```bash
#!/bin/bash

# Before hook - blocks tool on error
if [[ ! -f "$1" ]]; then
  echo "ERROR: File does not exist"
  exit 1  # Blocks tool execution
fi

# Validation passed
exit 0
```

## Best Practices

### Keep Hooks Fast

Hooks block execution - keep them lightweight:

```json
{
  "onToolCall": {
    "Write": {
      // ✅ Fast linter
      "after": ["eslint --fix {{file_path}}"]

      // ❌ Slow test suite
      // "after": ["npm test"]
    }
  }
}
```

### Use Absolute Paths

Reference scripts with paths relative to plugin:

```json
{
  "onInstall": ["${CLAUDE_PLUGIN_ROOT}/hooks/setup.sh"]
}
```

### Validate Input

Always validate hook variables:

```bash
#!/bin/bash

FILE="$1"

if [[ -z "$FILE" ]]; then
  echo "ERROR: No file path provided"
  exit 1
fi

if [[ ! -f "$FILE" ]]; then
  echo "ERROR: File does not exist: $FILE"
  exit 1
fi
```

### Provide Clear Feedback

```bash
#!/bin/bash

echo "Running pre-commit checks..."

if ! npm run lint; then
  echo "❌ Linting failed. Please fix errors before committing."
  exit 1
fi

echo "✅ All checks passed"
exit 0
```

### Handle Edge Cases

```bash
#!/bin/bash

# Handle files with spaces in names
FILE="$1"

# Validate file type
if [[ ! "$FILE" =~ \.(js|ts|jsx|tsx)$ ]]; then
  # Skip non-JavaScript files silently
  exit 0
fi

# Run formatter
prettier --write "$FILE"
```

## Security Considerations

### Validate Commands

Before hooks can block dangerous operations:

```json
{
  "onToolCall": {
    "Bash": {
      "before": ["./hooks/validate-command.sh '{{command}}'"]
    }
  }
}
```

**validate-command.sh:**
```bash
#!/bin/bash

COMMAND="$1"

# Block dangerous patterns
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "dd if="
  "mkfs"
  "> /dev/sda"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if [[ "$COMMAND" =~ $pattern ]]; then
    echo "ERROR: Dangerous command blocked: $pattern"
    exit 1
  fi
done

exit 0
```

### Limit Hook Scope

Only hook necessary tools:

```json
{
  // ✅ Specific tools only
  "onToolCall": {
    "Write": { "after": ["./format.sh {{file_path}}"] }
  }

  // ❌ Don't hook everything unnecessarily
}
```

### Sanitize Variables

```bash
#!/bin/bash

# Sanitize file path
FILE=$(realpath "$1")

# Ensure file is within project
if [[ ! "$FILE" =~ ^$(pwd) ]]; then
  echo "ERROR: File outside project directory"
  exit 1
fi
```

## Debugging Hooks

### Enable Verbose Output

```json
{
  "onToolCall": {
    "Write": {
      "before": ["set -x; ./hooks/debug.sh {{file_path}}; set +x"]
    }
  }
}
```

### Log Hook Execution

```bash
#!/bin/bash

LOG_FILE=".claude/hooks.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "$TIMESTAMP - Hook: $0, Args: $@" >> "$LOG_FILE"

# Rest of hook logic...
```

### Test Hooks Manually

```bash
# Test hook with sample data
./hooks/format.sh "src/main.js"

# Check exit code
echo $?
```

## Common Hook Patterns

### Auto-Format Pipeline

```json
{
  "onToolCall": {
    "Write": {
      "after": [
        "prettier --write {{file_path}}",
        "eslint --fix {{file_path}}"
      ]
    },
    "Edit": {
      "after": [
        "prettier --write {{file_path}}",
        "eslint --fix {{file_path}}"
      ]
    }
  }
}
```

### Test on Write

```json
{
  "onToolCall": {
    "Write": {
      "after": ["./hooks/run-relevant-tests.sh {{file_path}}"]
    }
  }
}
```

### Git Integration

```json
{
  "onToolCall": {
    "Write": {
      "after": ["git add {{file_path}}"]
    },
    "Edit": {
      "after": ["git add {{file_path}}"]
    }
  }
}
```

## Troubleshooting

### Hook Not Executing

- Check hook file has execute permissions: `chmod +x hooks/script.sh`
- Verify path is correct relative to plugin root
- Check JSON syntax in hooks.json
- Look for errors in Claude Code logs

### Hook Blocking Tool

- Check exit code of before hooks
- Add debug logging
- Test hook script manually
- Verify validation logic

### Variables Not Substituting

- Check variable name spelling: `{{file_path}}` not `{{filepath}}`
- Verify variable is available for that tool
- Quote variables in bash: `"{{file_path}}"`

## Templates

Reference templates for common hook configurations:

```
claude-hooks/
└── templates/
    ├── plugin-hook.md    # Plugin hook configuration example
    └── skill-hook.md     # Skill/subagent frontmatter hooks example
```

### Plugin Hook Template

Example configuration for defining hooks in a plugin's `hooks/hooks.json`:
- PostToolUse hook with `Write|Edit` matcher
- Uses `${CLAUDE_PLUGIN_ROOT}` for script references
- Includes timeout configuration

### Skill Hook Template

Example frontmatter for embedding hooks directly in skills:
- Supported events: PreToolUse, PostToolUse, Stop
- Hooks scoped to component lifecycle
- Runs only when skill/subagent is active

## References

For more information:
- Claude Code Hooks Documentation: https://code.claude.com/docs/en/hooks
- Plugin Configuration: https://code.claude.com/docs/en/plugins#hooks
