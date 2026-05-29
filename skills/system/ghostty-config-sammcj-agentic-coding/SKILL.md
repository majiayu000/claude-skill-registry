---
name: ghostty-config
description: Guidance for editing Ghostty terminal configuration files. You must use this skill when creating or modifying Ghostty config files.
# allowed-tools: "Read,Edit,Write,Grep,Glob"
model: "inherit"
---

# Ghostty Configuration

Guidance for configuring the Ghostty terminal emulator. Ghostty uses text-based config files with sensible defaults and zero required configuration.

## Config File Locations

**XDG Path (All Platforms):**
- `$XDG_CONFIG_HOME/ghostty/config`
- Defaults to `~/.config/ghostty/config` if XDG_CONFIG_HOME undefined

**macOS Additional Path:**
- `~/Library/Application Support/com.mitchellh.ghostty/config`
- If both XDG and macOS paths exist, both are loaded with macOS path taking precedence

## Config Syntax

```
# Comments start with #
background = 282c34
foreground = ffffff
font-family = "JetBrains Mono"
keybind = ctrl+z=close_surface
font-family =                     # Empty value resets to default
```

**Rules:**
- Keys are **case-sensitive** (use lowercase)
- Whitespace around `=` is flexible
- Values can be quoted or unquoted
- Empty values reset to defaults
- Every config key works as CLI flag: `ghostty --background=282c34`

## Config Loading & Includes

Files processed sequentially - later entries override earlier ones.

```
# Include additional configs
config-file = themes/dark.conf
config-file = ?local.conf       # ? prefix = optional (no error if missing)
```

**Critical:** `config-file` directives are processed at the file's end. Keys appearing after `config-file` won't override the included file's values.

## Runtime Reloading

- **Linux:** `ctrl+shift+,`
- **macOS:** `cmd+shift+,`

Some options cannot be reloaded at runtime. Some apply only to newly created terminals.

## CLI Commands

Ghostty provides CLI actions via `ghostty +<action>`. Use `ghostty +<action> --help` for action-specific help.

### Configuration Commands

| Command                                 | Description                            |
|-----------------------------------------|----------------------------------------|
| `ghostty +show-config`                  | Show current effective configuration   |
| `ghostty +show-config --default`        | Show default configuration             |
| `ghostty +show-config --default --docs` | Show defaults with documentation       |
| `ghostty +validate-config`              | Validate configuration file for errors |
| `ghostty +edit-config`                  | Open config file in default editor     |

### Listing Commands

| Command                            | Description                           |
|------------------------------------|---------------------------------------|
| `ghostty +list-fonts`              | List available fonts (fixed-width)    |
| `ghostty +list-themes`             | List available colour themes          |
| `ghostty +list-keybinds`           | Show current keybindings              |
| `ghostty +list-keybinds --default` | Show default keybindings              |
| `ghostty +list-colors`             | List available colour names           |
| `ghostty +list-actions`            | List all available keybinding actions |

### Other Commands

| Command                 | Description                  |
|-------------------------|------------------------------|
| `ghostty +version`      | Show version information     |
| `ghostty +help`         | Show help                    |
| `ghostty +show-face`    | Show font face information   |
| `ghostty +ssh-cache`    | Manage SSH terminfo cache    |
| `ghostty +crash-report` | Generate crash report        |
| `ghostty +new-window`   | Open new window (Linux only) |
| `ghostty +boo`          | Easter egg                   |

### Launching with Options

Every config key works as a CLI flag:
```bash
ghostty --background=282c34 --font-size=14
ghostty -e top                              # Run command in terminal
```

**macOS Note:** The `ghostty` CLI is a helper tool. To launch the terminal use `open -na Ghostty.app` or `open -na Ghostty.app --args --font-size=14`.

## Keybinding Syntax

Format: `keybind = trigger=action`

### Triggers

**Modifiers:** `shift`, `ctrl`/`control`, `alt`/`opt`/`option`, `super`/`cmd`/`command`

```
keybind = ctrl+a=select_all
keybind = ctrl+shift+t=new_tab
keybind = super+backquote=toggle_quick_terminal
```

**Physical keys (W3C codes):** `KeyA`, `key_a`, `Digit1`, `BracketLeft`
- Physical keys have higher priority than unicode codepoints
- Use for non-US keyboard layouts

**Key sequences (leader keys):**
```
keybind = ctrl+a>n=new_window      # Press ctrl+a, release, press n
keybind = ctrl+a>ctrl+n=new_window # Both with ctrl
```
Sequences wait indefinitely for next key.

### Prefixes

| Prefix         | Effect                                                                                |
|----------------|---------------------------------------------------------------------------------------|
| `global:`      | System-wide (macOS: needs Accessibility permissions; Linux: needs XDG Desktop Portal) |
| `all:`         | Apply to all terminal surfaces                                                        |
| `unconsumed:`  | Don't consume input (passes through)                                                  |
| `performable:` | Only consume if action succeeds                                                       |

Combine prefixes: `global:unconsumed:ctrl+a=reload_config`

**Note:** Sequences cannot be used with `global:` or `all:` prefixes.

### Special Values

- `keybind = clear` - Remove ALL keybindings
- `keybind = ctrl+a=unbind` - Remove specific binding
- `keybind = ctrl+a=ignore` - Prevent processing by Ghostty and terminal

## Shell Integration

Auto-injection for: **bash**, **zsh**, **fish**, **elvish**

```
shell-integration = detect    # Default - auto-detect shell
shell-integration = none      # Disable auto-injection
shell-integration = fish      # Force specific shell
```

### Shell Integration Features

```
shell-integration-features = cursor,sudo,title
shell-integration-features = no-cursor    # Disable specific feature
```

| Feature        | Description                   |
|----------------|-------------------------------|
| `cursor`       | Blinking bar at prompt        |
| `sudo`         | Preserve terminfo with sudo   |
| `title`        | Set window title from shell   |
| `ssh-env`      | SSH environment compatibility |
| `ssh-terminfo` | Auto terminfo on remote hosts |

### What Shell Integration Enables

1. Smart close (no confirm when at prompt)
2. New terminals start in previous terminal's directory
3. Prompt resizing via redraw
4. Ctrl/Cmd+triple-click selects command output
5. `jump_to_prompt` keybinding works
6. Alt/Option+click repositions cursor at prompt

### Manual Setup (if auto-injection fails)

**Bash** (add to `~/.bashrc` at top):
```bash
if [ -n "${GHOSTTY_RESOURCES_DIR}" ]; then
    builtin source "${GHOSTTY_RESOURCES_DIR}/shell-integration/bash/ghostty.bash"
fi
```

**Zsh:**
```zsh
source ${GHOSTTY_RESOURCES_DIR}/shell-integration/zsh/ghostty-integration
```

**Fish:**
```fish
source "$GHOSTTY_RESOURCES_DIR"/shell-integration/fish/vendor_conf.d/ghostty-shell-integration.fish
```

**macOS Note:** `/bin/bash` does NOT support automatic shell integration. Install Bash via Homebrew or manually source the script.

## Common Configuration Patterns

### Theme with Light/Dark Mode

```
theme = light:catppuccin-latte,dark:catppuccin-mocha
```

### Quick Terminal (Drop-down)

```
quick-terminal-position = top
quick-terminal-size = 50%
quick-terminal-autohide = true
keybind = global:super+backquote=toggle_quick_terminal
```

### Custom Colour Palette

```
palette = 0=#1d2021
palette = 1=#cc241d
# ... (0-255 supported)
```

### Font Configuration

```
font-family = "JetBrains Mono"
font-family-bold = "JetBrains Mono Bold"
font-size = 14
font-feature = -calt        # Disable ligatures
font-feature = -liga
```

### Background Transparency

```
background-opacity = 0.9
background-blur = true      # macOS, KDE Plasma only
```

## Platform-Specific Notes

**macOS Only:**
- `window-position-x/y`, `window-save-state`, `window-step-resize`
- `window-vsync`, `window-colorspace`
- `macos-titlebar-style`, `toggle_window_float_on_top`
- `font-thicken`, `font-thicken-strength`
- `toggle_visibility`, `undo`, `redo`, `check_for_updates`
- Global keybindings require Accessibility permissions

**Linux/GTK Only:**
- `window-title-font-family`, `window-subtitle`
- `window-titlebar-background/foreground` (requires `window-theme = ghostty`)
- `window-show-tab-bar`, `gtk-single-instance`
- `toggle_maximize`, `toggle_window_decorations`
- `toggle_tab_overview`, `toggle_command_palette`
- `prompt_surface_title`

**Linux Wayland Only:**
- `quick-terminal-keyboard-interactivity`
- `gtk-quick-terminal-layer`, `gtk-quick-terminal-namespace`

**FreeType (Linux) Only:**
- `freetype-load-flags`

## Reference Files

For complete option and keybinding references, load:

- **`references/options.md`** - All config options by category (font, colour, window, etc.)
- **`references/keybindings.md`** - All keybinding actions with parameters

Load these when you need specific option details, valid values, or keybinding action syntax.
