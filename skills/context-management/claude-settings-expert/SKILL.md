---
name: claude-settings-expert
description: Expert on Claude Code settings.json configuration, permissions, sandbox, environment variables, and settings hierarchy. Triggers when user mentions settings.json, permissions, allow rules, deny rules, sandbox, hooks configuration, or settings precedence.
allowed-tools: Read, Write, Edit, Grep, Glob
model: sonnet
---

# Claude Code Settings Expert

## Purpose

Provide expert guidance on configuring Claude Code through settings.json, including permissions, hooks, sandbox configuration, environment variables, and settings hierarchy. Auto-invokes when users need help with settings.

## When to Use

Auto-invoke when users mention:
- **Settings files** - "settings.json", "configure", "configuration"
- **Permissions** - "allow", "deny", "ask", "permissions", "permission rules"
- **Hooks** - "hooks configuration", "PreToolUse hooks", "PostToolUse hooks"
- **Sandbox** - "sandbox settings", "sandboxing", "filesystem isolation"
- **Environment** - "environment variables", "env", "$CLAUDE_PROJECT_DIR"
- **Hierarchy** - "settings precedence", "user settings", "project settings"

## Knowledge Base

- Official docs: `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_settings.md`
- IAM docs: Look for IAM/permissions documentation
- Hooks docs: `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_hooks.md`

## Settings File Locations

### Hierarchy (highest to lowest precedence)

1. **Enterprise managed policies**
   - macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
   - Linux/WSL: `/etc/claude-code/managed-settings.json`
   - Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`
   - Cannot be overridden by users

2. **Command line arguments**
   - Temporary overrides for specific session
   - Example: `claude --dangerously-skip-permissions`

3. **Local project settings**
   - `.claude/settings.local.json`
   - Personal project settings (not committed)
   - Git-ignored automatically

4. **Shared project settings**
   - `.claude/settings.json`
   - Team-shared settings in source control
   - Committed to repository

5. **User settings**
   - `~/.claude/settings.json`
   - Personal global settings
   - Apply to all projects

### When to Use Each

**User settings** (`~/.claude/settings.json`):
- Personal preferences across all projects
- Personal API keys
- Personal slash commands
- Personal output style

**Project settings** (`.claude/settings.json`):
- Team permissions
- Project-specific hooks
- Required plugins/marketplaces
- Team workflow configuration

**Local project** (`.claude/settings.local.json`):
- Personal project overrides
- Experimental settings
- Local-only preferences
- Not shared with team

## Process

### 1. Identify Need

Ask clarifying questions:

```
What would you like to configure?

1. **Permissions** - Allow/deny specific tools or commands
2. **Hooks** - Automate tool execution workflows
3. **Sandbox** - Enable filesystem/network isolation
4. **Environment** - Set environment variables
5. **Plugins** - Configure plugins and marketplaces
6. **Model** - Override default model
7. **Other** - Company announcements, cleanup, etc.
```

### 2. Determine Scope

Ask about scope:

```
Where should this configuration apply?

- **User-level** (`~/.claude/settings.json`) - All your projects
- **Project-level** (`.claude/settings.json`) - This project, shared with team
- **Local** (`.claude/settings.local.json`) - This project, just you
```

### 3. Build Configuration

Based on needs, construct the appropriate JSON:

## Permission Configuration

### Structure

```json
{
  "permissions": {
    "allow": ["permission-rule"],
    "ask": ["permission-rule"],
    "deny": ["permission-rule"],
    "additionalDirectories": ["../path"],
    "defaultMode": "default" | "plan" | "acceptEdits" | "bypassPermissions",
    "disableBypassPermissionsMode": "disable"
  }
}
```

### Permission Rules

**Tool-specific:**
```json
{
  "permissions": {
    "allow": [
      "Read(~/.zshrc)",
      "Bash(git diff:*)",
      "Bash(npm run lint:*)",
      "Bash(npm run test:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Bash(curl:*)",
      "WebFetch",
      "WebSearch"
    ]
  }
}
```

**Bash permissions:**
- Use prefix matching (not regex)
- `Bash(git:*)` - All git commands
- `Bash(git diff:*)` - Only git diff commands
- Can be bypassed (not for security, use sandbox for that)

**Read/Write permissions:**
- `Read(./secrets/**)` - Recursive pattern
- `Read(./.env)` - Specific file
- `Write(./dist/**)` - Allow writes to dist

**Permission modes:**
- `default` - Ask for permission
- `plan` - Plan mode (no execution without approval)
- `acceptEdits` - Auto-approve edits only
- `bypassPermissions` - Approve all (dangerous)

### Example: Secure Development

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(npm run lint:*)",
      "Bash(npm run test:*)",
      "Read(~/.gitconfig)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(rm -rf:*)",
      "WebFetch",
      "WebSearch"
    ],
    "defaultMode": "default"
  }
}
```

## Hooks Configuration

### Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command" | "prompt",
            "command": "bash command",
            "prompt": "LLM prompt with $ARGUMENTS",
            "timeout": 60
          }
        ]
      }
    ]
  },
  "disableAllHooks": false
}
```

### Example: Auto-Format and Validate

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/add-context.sh"
          }
        ]
      }
    ]
  }
}
```

## Sandbox Configuration

### Structure

```json
{
  "sandbox": {
    "enabled": true | false,
    "autoAllowBashIfSandboxed": true | false,
    "excludedCommands": ["git", "docker"],
    "allowUnsandboxedCommands": true | false,
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowLocalBinding": true | false,
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    },
    "enableWeakerNestedSandbox": false
  }
}
```

### Example: Strict Sandbox

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "allowUnsandboxedCommands": false,
    "network": {
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  },
  "permissions": {
    "deny": [
      "Read(.envrc)",
      "Read(~/.aws/**)",
      "Read(./secrets/**)"
    ]
  }
}
```

**Notes:**
- Filesystem access via Read/Write/Edit deny rules
- Network access via WebFetch allow/deny rules
- macOS/Linux only (not Windows)

## Environment Variables

### Structure

```json
{
  "env": {
    "KEY": "value",
    "NODE_ENV": "production",
    "API_URL": "https://api.example.com"
  }
}
```

### Common Variables

```json
{
  "env": {
    "ANTHROPIC_MODEL": "claude-sonnet-4-5-20250929",
    "DISABLE_TELEMETRY": "1",
    "DISABLE_AUTOUPDATER": "1",
    "DISABLE_PROMPT_CACHING": "0",
    "MAX_THINKING_TOKENS": "10000",
    "BASH_DEFAULT_TIMEOUT_MS": "120000"
  }
}
```

## Plugin Configuration

### Structure

```json
{
  "enabledPlugins": {
    "plugin-name@marketplace-name": true | false
  },
  "extraKnownMarketplaces": {
    "marketplace-name": {
      "source": {
        "source": "github" | "git" | "directory",
        "repo": "org/repo",
        "url": "https://git.example.com/repo.git",
        "path": "/local/path"
      }
    }
  }
}
```

### Example: Team Plugins

```json
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment@company-tools": true,
    "security-scanner@company-tools": false
  },
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  }
}
```

## Other Settings

### Model Override

```json
{
  "model": "claude-sonnet-4-5-20250929"
}
```

### Cleanup Period

```json
{
  "cleanupPeriodDays": 20
}
```

### Company Announcements

```json
{
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs"
  ]
}
```

### Force Login Method

```json
{
  "forceLoginMethod": "console",
  "forceLoginOrgUUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

### API Key Helper

```json
{
  "apiKeyHelper": "/bin/generate_temp_api_key.sh"
}
```

### Disable Co-Authored-By

```json
{
  "includeCoAuthoredBy": false
}
```

### Status Line

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

### Output Style

```json
{
  "outputStyle": "Explanatory"
}
```

## Complete Example: Enterprise Project

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(docker ps:*)",
      "Bash(kubectl get:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/production.json)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(git push:*)",
      "WebFetch",
      "WebSearch"
    ],
    "ask": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Write(./src/**)"
    ],
    "defaultMode": "default",
    "disableBypassPermissionsMode": "disable"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/lint-and-format.sh",
            "timeout": 60
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker", "kubectl"],
    "network": {
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  },
  "env": {
    "NODE_ENV": "development",
    "DISABLE_TELEMETRY": "1"
  },
  "enabledPlugins": {
    "security-scanner@company-tools": true,
    "code-quality@company-tools": true
  },
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  },
  "companyAnnouncements": [
    "Welcome to Company Dev! See docs.company.com for coding standards",
    "Reminder: All PRs require security scan approval"
  ],
  "model": "claude-sonnet-4-5-20250929",
  "cleanupPeriodDays": 20,
  "includeCoAuthoredBy": true
}
```

## Validation

### Check JSON Syntax

```bash
# Validate JSON
cat .claude/settings.json | jq .

# Pretty-print
cat .claude/settings.json | jq . > temp.json && mv temp.json .claude/settings.json
```

### Test Configuration

```bash
# Start Claude Code with debug
claude --debug

# Check settings loaded
# Look for: "Loading settings from..."
```

### Verify Permissions

```bash
# Run /permissions in Claude Code
/permissions

# Check what's allowed/denied
```

## Troubleshooting

### Settings Not Applied

**Check:**
1. JSON syntax is valid (`jq` validation)
2. File location is correct
3. Restart Claude Code after changes
4. Check precedence (higher-level settings override)

### Permission Rules Not Working

**Check:**
1. Rule syntax: `Tool(pattern)`
2. Case-sensitive tool names
3. Bash uses prefix matching (not regex)
4. Precedence: deny > ask > allow

### Hooks Not Running

**Check:**
1. `disableAllHooks` is not `true`
2. Hook configuration is valid
3. Script has execute permissions
4. Restart Claude Code
5. Use `/hooks` to verify loaded

### Sandbox Issues

**Check:**
1. macOS/Linux only (not Windows)
2. Docker/Podman installed
3. Permissions for Docker socket
4. Check `excludedCommands` for needed tools

## Best Practices

### DO:
✅ Use project settings for team configuration
✅ Use local settings for personal overrides
✅ Validate JSON syntax before committing
✅ Document why rules exist (comments via tools)
✅ Test settings before sharing with team
✅ Use specific permission rules
✅ Set appropriate timeouts for hooks
✅ Use `$CLAUDE_PROJECT_DIR` in hooks

### DON'T:
❌ Commit sensitive data to project settings
❌ Use `bypassPermissions` mode in shared config
❌ Make permission rules too broad
❌ Forget to restart after changes
❌ Use hardcoded paths in hooks
❌ Disable all hooks globally without reason
❌ Override enterprise managed settings (you can't)

## Sensitive Files

### Exclude from Claude Code

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./.envrc)",
      "Read(./secrets/**)",
      "Read(./.aws/**)",
      "Read(./config/credentials.json)",
      "Read(./config/production.json)",
      "Read(./.ssh/**)",
      "Read(./build/**)",
      "Read(./dist/**)",
      "Read(./node_modules/**)"
    ]
  }
}
```

## Settings Merging

Settings from different levels are merged:

**Example:**

User settings:
```json
{
  "permissions": {
    "allow": ["Read(~/.gitconfig)"]
  }
}
```

Project settings:
```json
{
  "permissions": {
    "deny": ["Read(./.env)"]
  }
}
```

**Merged result:**
```json
{
  "permissions": {
    "allow": ["Read(~/.gitconfig)"],
    "deny": ["Read(./.env)"]
  }
}
```

Arrays are concatenated, objects are merged.

## Interactive Configuration

Offer to create/update settings:

```
I can help you configure this. Would you like me to:

1. Create a new settings.json file
2. Update existing settings.json
3. Show you what to add manually

Where should I make these changes?
- User settings (~/.claude/settings.json)
- Project settings (.claude/settings.json)
- Local settings (.claude/settings.local.json)
```

## Resources

- **Official Settings Docs:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_settings.md`
- **Hooks Reference:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_hooks.md`
- **Sandbox Guide:** Look for sandboxing documentation
- **IAM Guide:** Look for permissions documentation
