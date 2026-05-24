---
name: zed-config
description: Configure Zed editor settings, keybindings, language servers, themes, and AI agents. Use when modifying Zed configuration, adding keybindings, setting up language servers, or configuring external agents like Claude Code. Keywords: zed, editor, settings, keybindings, keymap, LSP, language server, theme, agent, configure
allowed-tools: Read, Edit, Bash(cat:*), Bash(jq:*)
---

# Zed Editor Configuration Skill

Manages Zed editor configuration through `settings.json` and `keymap.json` files.

## Important Context

This dotfiles repository has **symlinked** the global Zed configuration:
- Configuration location: `config/zed/`
- Symlinked to: `~/.config/zed/`
- **All changes are applied globally** to the Zed installation

Configuration files:
- `config/zed/settings.json` - Main editor settings
- `config/zed/keymap.json` - Custom keybindings

## Configuration Categories

### 1. Editor Appearance & Behavior

**Theme Configuration:**
```json
{
  "theme": {
    "mode": "system",           // "system", "light", or "dark"
    "light": "One Light",
    "dark": "Zedokai"
  },
  "icon_theme": "Catppuccin Frappé"
}
```

**Font Settings:**
```json
{
  "ui_font_size": 14,
  "buffer_font_size": 14.0,
  "buffer_font_weight": 430.0
}
```

**Editor Behavior:**
```json
{
  "preferred_line_length": 120,
  "soft_wrap": "preferred_line_length",
  "autosave": {
    "after_delay": {
      "milliseconds": 200
    }
  },
  "show_completions_on_input": true
}
```

### 2. Terminal Configuration

```json
{
  "terminal": {
    "shell": {
      "program": "fish"        // Shell program (fish, zsh, bash)
    }
  }
}
```

### 3. Language Server Protocol (LSP)

**Structure:** Use nested objects (not dot-delimited strings)

**Deno:**
```json
{
  "lsp": {
    "deno": {
      "settings": {
        "deno": {
          "enable": true
        }
      }
    }
  }
}
```

**Rust Analyzer:**
```json
{
  "lsp": {
    "rust-analyzer": {
      "initialization_options": {
        "inlayHints": {
          "maxLength": null,
          "lifetimeElisionHints": {
            "enable": "skip_trivial",
            "useParameterNames": true
          }
        }
      },
      "binary": {
        "ignore_system_version": false
      },
      "enable_lsp_tasks": true
    }
  }
}
```

**Python (Ruff):**
```json
{
  "lsp": {
    "ruff": {
      "initialization_options": {
        "settings": {}
      }
    }
  }
}
```

### 4. Language-Specific Settings

Configure per-language overrides in the `languages` object:

```json
{
  "languages": {
    "Python": {
      "language_servers": ["ty", "ruff"],
      "format_on_save": "on",
      "formatter": [
        {
          "language_server": {
            "name": "ruff"
          }
        }
      ]
    },
    "TypeScript": {
      "language_servers": ["deno", "!typescript-language-server", "!vtsls", "!eslint"],
      "formatter": "language_server"
    },
    "TSX": {
      "language_servers": ["deno", "!typescript-language-server", "!vtsls", "!eslint"],
      "formatter": "language_server"
    }
  }
}
```

**Language server prioritization:**
- List servers in order of preference
- Prefix with `!` to disable (e.g., `"!typescript-language-server"`)
- Use `"..."` to expand remaining registered servers

**Available options per language:**
- `tab_size`: Indentation spaces
- `formatter`: Code formatting tool
- `format_on_save`: `"on"`, `"off"`, or `"language_server"`
- `enable_language_server`: Toggle LSP
- `hard_tabs`: Use tabs instead of spaces
- `preferred_line_length`: Max line width
- `soft_wrap`: Line wrapping behavior

### 5. AI Agent Configuration

**Agent Settings:**
```json
{
  "agent": {
    "always_allow_tool_actions": true,
    "use_modifier_to_send": true,
    "play_sound_when_agent_done": true,
    "default_profile": "write",
    "default_model": {
      "provider": "google",
      "model": "gemini-2.5-pro-exp-03-25"
    }
  }
}
```

**External Agents (Claude Code, Gemini CLI):**
```json
{
  "agent_servers": {
    "claude": {
      "env": {
        "CLAUDE_CODE_EXECUTABLE": "/path/to/custom-executable"
      }
    },
    "custom-agent": {
      "command": "node",
      "args": ["~/projects/agent/index.js", "--acp"],
      "env": {}
    }
  }
}
```

**Edit Predictions:**
```json
{
  "show_edit_predictions": false,
  "edit_predictions": {
    "mode": "eager",              // "eager" or "manual"
    "enabled_in_text_threads": false
  }
}
```

### 6. Keybindings Configuration

**File:** `config/zed/keymap.json`

**Structure:** JSON array of binding objects with optional contexts

```json
[
  {
    "context": "Editor",          // Optional: "Editor", "Terminal", "Workspace"
    "bindings": {
      "cmd-k": "assistant::InlineAssist",
      "cmd-t": "workspace::NewTerminal",
      "cmd-1": "workspace::ToggleLeftDock"
    }
  }
]
```

**Key Syntax:**
- **Modifiers:** `cmd-`, `ctrl-`, `alt-`, `shift-`, `fn-`
- **Sequences:** Space-separated (e.g., `"cmd-k cmd-s"`)
- **Platform-agnostic:** Use `secondary-` to adapt to platform

**Common Actions:**
- `workspace::ToggleBottomDock` - Toggle bottom panel
- `workspace::NewTerminal` - Open new terminal
- `workspace::ToggleLeftDock` - Toggle file explorer
- `workspace::ToggleRightDock` - Toggle right panel
- `assistant::InlineAssist` - Inline AI assist
- `file_finder::Toggle` - Open file finder
- `task::Spawn` - Run task
- `pane::ActivatePreviousItem` / `pane::ActivateNextItem` - Navigate tabs
- `["agent::NewExternalAgentThread", { "agent": "claude_code" }]` - Open agent with args

**Context Options:**
- `"Editor"` - Any editor pane
- `"Editor && mode == full"` - Main code editors only
- `"Terminal"` - Terminal panes
- `"!Editor && !Terminal"` - Everywhere except editors/terminals

**Disable Binding:**
```json
{
  "context": "Workspace",
  "bindings": {
    "cmd-r": null              // Disables cmd-r
  }
}
```

### 7. SSH Connections

Configure remote development environments:

```json
{
  "ssh_connections": [
    {
      "host": "betty",
      "projects": [
        {
          "paths": ["/home/user/Development/project"]
        }
      ]
    }
  ]
}
```

### 8. Tabs Configuration

```json
{
  "tabs": {
    "git_status": true,         // Show git status colors
    "file_icons": true          // Show file type icons
  }
}
```

## Workflow Instructions

### Reading Current Configuration

**Always start by reading the current config:**
```
Read config/zed/settings.json
Read config/zed/keymap.json
```

### Modifying Settings

**Use Edit tool for precise changes:**
1. Read the current configuration
2. Identify the exact JSON to modify
3. Use Edit to replace the specific section
4. Preserve formatting and comments

**Example - Add new language server:**
```json
// Before:
{
  "lsp": {
    "deno": { ... }
  }
}

// After:
{
  "lsp": {
    "deno": { ... },
    "gopls": {
      "initialization_options": {
        "usePlaceholders": true
      }
    }
  }
}
```

### Adding Keybindings

**Append to the bindings object:**
```json
// Existing:
{
  "bindings": {
    "cmd-t": "workspace::NewTerminal"
  }
}

// Add new binding:
{
  "bindings": {
    "cmd-t": "workspace::NewTerminal",
    "cmd-r": "editor::Rename"
  }
}
```

### Validating Configuration

After modifications:
1. Check JSON syntax is valid (preserve trailing commas in objects/arrays)
2. Ensure comments use `//` format
3. Verify nested structure (especially for `lsp` and `languages`)

## Common Configuration Tasks

### Add New Language Server

1. Read current `lsp` section
2. Add server configuration under `lsp` key
3. Optionally add language-specific settings under `languages`

### Change Theme

```json
{
  "theme": {
    "mode": "dark",
    "dark": "Tokyo Night"
  }
}
```

### Configure Formatter

```json
{
  "languages": {
    "JavaScript": {
      "formatter": {
        "external": {
          "command": "prettier",
          "arguments": ["--stdin-filepath", "{buffer_path}"]
        }
      },
      "format_on_save": "on"
    }
  }
}
```

### Add Custom Keybinding for External Agent

```json
{
  "bindings": {
    "cmd-3": ["agent::NewExternalAgentThread", { "agent": "claude_code" }]
  }
}
```

## Best Practices

1. **Read before editing** - Always read current config to understand structure
2. **Preserve comments** - Keep existing `//` comments intact
3. **Use nested objects** - For LSP, use `{ "lsp": { "server": { "settings": {} } } }`
4. **Test incrementally** - Make one change at a time
5. **Check Zed docs** - Reference official docs for available options
6. **Language-specific overrides** - Use `languages` object to override global settings
7. **Context-aware keybindings** - Use `context` to scope shortcuts appropriately

## Troubleshooting

**Invalid JSON:** Zed supports extended JSON with `//` comments but requires valid structure

**LSP not working:**
- Check `enable_language_server` setting
- Verify `initialization_options` structure
- Ensure language server binary is installed

**Keybinding conflicts:**
- Check base keymap setting (`"base_keymap": "JetBrains"`)
- Use `null` to disable conflicting default bindings
- Test in relevant context (Editor vs Terminal vs Workspace)

**Changes not applying:**
- Configuration is symlinked from `config/zed/` to `~/.config/zed/`
- Changes take effect immediately in Zed (no restart needed for most settings)
- Some LSP changes require server restart

## Quick Reference

**Current Configuration Files:**
- Settings: `config/zed/settings.json`
- Keybindings: `config/zed/keymap.json`
- Conversations: `config/zed/conversations/`
- Custom Prompts: `config/zed/prompts/`
- Themes: `config/zed/themes/`

**Current Base Keymap:** JetBrains

**Current Languages Configured:**
- Python (ty, ruff LSP, format on save)
- TypeScript (Deno LSP, disable default TS servers)
- TSX (Deno LSP, disable default TS servers)

**Current LSP Servers:**
- Deno (enabled)
- Rust Analyzer (inlay hints, analyzer target dir)
- Ruff (Python)
