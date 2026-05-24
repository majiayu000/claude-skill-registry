---
name: ghostty-config
description: Configure and optimize Ghostty terminal with themes, fonts, keybindings, and performance settings. Use when setting up Ghostty, creating terminal configs, customizing keybinds, or troubleshooting terminal behavior. Keywords: ghostty, terminal, config, keybind, theme, font, terminal config, ghostty.conf
---

# Ghostty Terminal Configuration

Configure Ghostty terminal emulator following best practices and XDG Base Directory specification.

## Config File Location

Ghostty follows XDG spec:
- **Primary**: `~/.config/ghostty/config`
- **Theme files**: `~/.config/ghostty/themes/`

## Instructions

### 1. Identify Configuration Need

Determine what the user wants to configure:
- **Initial setup**: Create base config with sensible defaults
- **Theming**: Colors, fonts, appearance
- **Keybindings**: Custom shortcuts and actions
- **Performance**: GPU, scrollback, shell integration
- **Behavior**: Window management, tabs, quick terminal

### 2. Configuration Categories

#### Font Configuration

```ini
# Font family with fallbacks
font-family = "JetBrains Mono"
font-size = 13

# Font variants
font-family-bold = "JetBrains Mono"
font-family-italic = "JetBrains Mono"

# OpenType features (disable ligatures example)
font-feature = -calt

# Variable font axes (optional)
# font-variation = wght=450
```

**Guidelines:**
- Use monospace fonts with good Unicode coverage
- Size 12-14 for optimal readability
- Consider ligature preferences (coding vs terminal work)
- Test font rendering before committing

#### Theme & Appearance

```ini
# Use built-in theme
theme = "catppuccin-mocha"

# Or custom colors
background = #1e1e2e
foreground = #cdd6f4
cursor-color = #f5e0dc

# Transparency and effects
background-opacity = 0.95
background-blur-radius = 20  # macOS/KDE only

# Window styling
window-padding-x = 4
window-padding-y = 4
window-decoration = true
```

**Best practices:**
- Start with built-in themes: `catppuccin-*`, `solarized-*`, `gruvbox-*`
- Keep opacity ≥ 0.85 for readability
- Use background blur for aesthetics without sacrificing legibility
- Match padding to your workflow (minimal vs spacious)

#### Keybinding Patterns

**Syntax:** `keybind = trigger=action`

**Common patterns:**

```ini
# Navigation
keybind = ctrl+shift+h=goto_split:left
keybind = ctrl+shift+j=goto_split:bottom
keybind = ctrl+shift+k=goto_split:top
keybind = ctrl+shift+l=goto_split:right

# Splits
keybind = ctrl+shift+enter=new_split:right
keybind = ctrl+shift+\=new_split:down

# Tabs
keybind = super+t=new_tab
keybind = super+w=close_surface
keybind = super+1=goto_tab:1
keybind = super+2=goto_tab:2

# Copy/Paste
keybind = super+c=copy_to_clipboard
keybind = super+v=paste_from_clipboard

# Font sizing
keybind = super+plus=increase_font_size:1
keybind = super+minus=decrease_font_size:1
keybind = super+0=reset_font_size

# Quick terminal (dropdown)
keybind = global:super+grave=toggle_quick_terminal

# Unbind unwanted defaults
keybind = ctrl+shift+n=unbind
```

**Advanced keybind features:**

```ini
# Global keybinds (system-wide, macOS only)
keybind = global:super+shift+t=new_window

# Multi-key sequences
keybind = ctrl+a>c=new_window

# Prefixes
keybind = all:ctrl+shift+r=reload_config
keybind = unconsumed:ctrl+space=text:\x00
keybind = performable:super+c=copy_to_clipboard
```

**Modifier aliases:**
- `ctrl` = `control`
- `alt` = `opt` = `option`
- `super` = `cmd` = `command`

**Key types:**
- Unicode codepoints: `ö`, `é`, `⌘`
- Physical keys (W3C codes): `KeyA`, `Digit1`
- Function keys: `F1`, `F12`
- Special: `escape`, `enter`, `tab`, `backspace`

#### Shell Integration

```ini
# Auto-detect shell features
shell-integration = detect
shell-integration-features = cursor,sudo,title

# Custom shell
command = /usr/bin/fish

# Environment variables
env = EDITOR=nvim
env = TERM=xterm-256color
```

#### Performance & Behavior

```ini
# Scrollback
scrollback-limit = 10000

# Mouse
mouse-scroll-multiplier = 3
copy-on-select = clipboard

# Window state
window-save-state = default
window-inherit-working-directory = true

# Tab behavior
window-new-tab-position = current
```

### 3. Configuration Workflow

1. **Read existing config** (if present):
   ```bash
   Read ~/.config/ghostty/config
   ```

2. **Determine changes needed** based on user request

3. **Apply changes** using Edit or Write:
   - Use Edit for incremental changes to existing config
   - Use Write for new configs or major rewrites

4. **Validate syntax**:
   - Check modifier spelling (ctrl, shift, alt, super)
   - Verify action names (use official docs reference)
   - Ensure proper INI formatting

5. **Test recommendations**:
   - "Changes apply to new terminals/windows only"
   - Suggest restarting Ghostty or opening new window
   - For global keybinds, mention accessibility permissions (macOS)

### 4. Common Configuration Tasks

#### Complete Initial Setup

Create minimal but functional config:
```ini
# Font
font-family = "JetBrains Mono"
font-size = 13

# Theme
theme = "catppuccin-mocha"
background-opacity = 0.95

# Shell
shell-integration = detect
command = /usr/bin/fish

# Behavior
copy-on-select = clipboard
window-inherit-working-directory = true
```

#### Add Vim-style Navigation

```ini
keybind = ctrl+h=goto_split:left
keybind = ctrl+j=goto_split:bottom
keybind = ctrl+k=goto_split:top
keybind = ctrl+l=goto_split:right
```

#### Theme Switching

```ini
# Built-in themes
theme = catppuccin-mocha  # dark
theme = catppuccin-latte  # light

# Custom theme file
theme = /Users/user/.config/ghostty/themes/custom.conf
```

#### Quick Terminal Setup

```ini
# Dropdown terminal
keybind = global:super+grave=toggle_quick_terminal
quick-terminal-position = top
quick-terminal-screen = main
quick-terminal-animation-duration = 0.2
```

### 5. Reference Documentation

For comprehensive options, reference:
- Main config: https://ghostty.org/docs/config/reference
- Keybindings: https://ghostty.org/docs/config/keybind

List all available actions and defaults:
```bash
ghostty +list-keybinds --default
```

### 6. Integration with Dotfiles

Since this is a dotfiles repo following XDG spec:

1. **Store config**: `config/ghostty/config`
2. **Symlink to XDG location**:
   ```bash
   ln -sf ~/Development/dotfiles/config/ghostty ~/.config/ghostty
   ```
3. **Update link-config.sh** to include Ghostty
4. **Add to README** in tools section

## Output Format

When configuring Ghostty:

1. **Show changes clearly** using code blocks
2. **Explain rationale** for non-obvious settings
3. **Provide test commands** when relevant
4. **Note runtime behavior**: "Restart Ghostty or open new window to see changes"
5. **Include file paths** using `file:line` format for navigation

## Project Context

This dotfiles repo:
- Uses Nix for package management (`flake.nix`)
- Symlinks configs from `config/**` to `~/.config/`
- Follows XDG Base Directory spec
- Uses Fish shell by default
- Prioritizes reproducibility and cross-platform support
