---
name: wezterm-dev
description: This skill should be used when the user asks to "configure WezTerm", "wezterm config", "customize terminal", "set up wezterm", "wezterm lua", or mentions general WezTerm configuration questions. For specific topics, focused skills may be more appropriate.
version: 0.7.11
---

# WezTerm Development

Configure and customize WezTerm terminal emulator with Lua, focusing on Claude Code workflows.

## First Action: Check Reference Cache

Before proceeding, check if the cache needs refreshing:

1. Read `${CLAUDE_PLUGIN_ROOT}/.cache/learnings.md` (if it exists)
2. Check the `last_refresh` date in the YAML frontmatter
3. If missing or stale, refresh using the terminal-cache skill pattern
4. Preserve any existing Learnings section when refreshing

## Before Starting: Backup Configuration

## Configuration File Location

`/.config/wezterm/wezterm.lua` (Windows: `C:\Users\<username>\.wezterm.lua`)

## Base Configuration

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- Font and appearance
config.font = wezterm.font('FiraCode Nerd Font')
config.font_size = 10
config.color_scheme = 'Catppuccin Mocha'

-- Window settings
config.initial_cols = 120
config.initial_rows = 28
config.window_padding = { left = 4, right = 4, top = 4, bottom = 4 }

return config
```

## Focused Skills

For specific configuration topics, use these focused skills:

| Topic | Skill | Trigger Phrases |
|-------|-------|-----------------|
| Keybindings | `/wezterm-dev:wezterm-keybindings` | "leader key", "tmux-style", "pane splitting" |
| Visual Customization | `/wezterm-dev:wezterm-visual` | "opacity", "blur", "cursor", "colors", "theme" |
| Tab Bar | `/wezterm-dev:wezterm-tabs` | "tab bar", "nerd font icons", "process icons" |
| Agent Deck | `/wezterm-dev:wezterm-agent-deck` | "agent deck", "claude monitoring", "agent status" |

## Troubleshooting

For debugging issues, the wezterm-troubleshoot agent can autonomously diagnose and fix common problems.

## Testing and Debugging

1. **Reload config**: `Cmd+Shift+,`
2. **Debug log**: `wezterm.log_info('message')` - view in debug overlay (`Ctrl+Shift+L`)
3. **Test icons**: Create test script with Nerd Font characters

## Reference Files

- **`references/tab-formatting.md`** - Complete tab title implementation
- **`references/status-bar.md`** - Right status bar with git branch
- **`references/nerd-font-icons.md`** - Comprehensive icon reference
- **`references/agent-deck.md`** - Agent Deck configuration details
- **`references/cache-management.md`** - Cache system documentation

## Example Files

- **`examples/wezterm-complete.lua`** - Full working configuration

## Resources

- Official docs: https://wezfurlong.org/wezterm/config/
- GitHub: https://github.com/wez/wezterm
- Nerd Fonts: https://www.nerdfonts.com/
