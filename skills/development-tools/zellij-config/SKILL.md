---
name: zellij-config
description: Configure Zellij terminal multiplexer with layouts, themes, keybindings, and behavior settings using KDL format. Use when setting up Zellij, creating layouts, customizing themes, or configuring keybinds. Keywords: zellij, terminal multiplexer, layout, theme, keybind, KDL, config, tmux alternative, terminal workspace
---

# Zellij Configuration

Configure Zellij terminal multiplexer following best practices and XDG Base Directory specification.

## Config File Locations

Zellij uses **KDL (KDL Document Language)** format and follows XDG spec:
- **Primary config**: `~/.config/zellij/config.kdl`
- **Themes**: `~/.config/zellij/themes/`
- **Layouts**: `~/.config/zellij/layouts/`

## Instructions

### 1. Identify Configuration Need

Determine what the user wants to configure:
- **Initial setup**: Create base config with sensible defaults
- **Layouts**: Pane/tab arrangements for workflows
- **Themes**: Colors and appearance customization
- **Keybindings**: Custom shortcuts and mode bindings
- **Behavior**: General settings, mouse, copy-paste

### 2. Configuration Initialization

For new setup:
```bash
# Generate default config
mkdir -p ~/.config/zellij
zellij setup --dump-config > ~/.config/zellij/config.kdl

# Check config directory location
zellij setup --check
```

### 3. Configuration Categories

#### General Settings (config.kdl)

**Basic structure:**
```kdl
// Mouse support
mouse_mode true

// Pane frames
pane_frames true

// Copy on selection
copy_on_select true

// Scrollback
scroll_buffer_size 10000

// Default shell
default_shell "fish"

// Default layout
default_layout "compact"

// Default theme
theme "catppuccin-mocha"

// UI configuration
simplified_ui false
default_mode "normal"

// Session serialization
session_serialization true

// Clipboard provider
copy_command "pbcopy"  // macOS
// copy_command "xclip -selection clipboard"  // Linux X11
// copy_command "wl-copy"  // Linux Wayland
```

**Important settings:**
- `mouse_mode`: Enable/disable mouse support
- `pane_frames`: Show borders around panes
- `copy_on_select`: Auto-copy selected text
- `scroll_buffer_size`: Lines of scrollback history
- `default_shell`: Shell to launch in new panes
- `session_serialization`: Save/restore sessions on exit
- `mirror_session`: Allow session mirroring

#### Layouts (*.kdl in layouts/)

**Basic layout structure:**
```kdl
layout {
    // Single pane
    pane

    // Vertical split with two panes
    pane split_direction="vertical" {
        pane
        pane
    }
}
```

**Common layout patterns:**

**Development layout (code + terminal):**
```kdl
layout {
    default_tab_template {
        pane size=1 borderless=true {
            plugin location="zellij:tab-bar"
        }
        children
        pane size=2 borderless=true {
            plugin location="zellij:status-bar"
        }
    }

    tab name="dev" {
        pane split_direction="vertical" {
            pane size="70%" {
                // Editor pane
            }
            pane split_direction="horizontal" {
                pane {
                    // Terminal for commands
                }
                pane {
                    // Logs or tests
                }
            }
        }
    }
}
```

**Multi-tab workspace:**
```kdl
layout {
    tab name="editor" focus=true {
        pane
    }

    tab name="servers" {
        pane split_direction="vertical" {
            pane command="npm" {
                args "run" "dev"
            }
            pane command="docker" {
                args "compose" "logs" "-f"
            }
        }
    }

    tab name="monitoring" {
        pane command="htop"
        pane command="btop"
    }
}
```

**Pane properties:**
- `split_direction`: "vertical" or "horizontal"
- `size`: Percentage ("70%") or fixed
- `command`: Executable to run
- `args`: Command arguments (space-separated strings)
- `cwd`: Working directory
- `focus`: Boolean for initial focus
- `borderless`: Hide pane borders
- `name`: Pane title

**Layout best practices:**
- Use `default_tab_template` for consistent tab structure
- Include tab-bar and status-bar plugins for UI
- Name tabs descriptively
- Set focus on primary working pane
- Use size percentages for responsive layouts

#### Themes (*.kdl in themes/)

**Theme structure:**
```kdl
themes {
    custom_theme {
        fg "#cdd6f4"
        bg "#1e1e2e"
        black "#45475a"
        red "#f38ba8"
        green "#a6e3a1"
        yellow "#f9e2af"
        blue "#89b4fa"
        magenta "#f5c2e7"
        cyan "#94e2d5"
        white "#bac2de"
        orange "#fab387"
    }
}
```

**Color properties (all RGB or hex):**
- `fg`: Foreground text
- `bg`: Background
- `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`: ANSI colors
- `orange`: Additional accent color

**UI component theming:**
```kdl
themes {
    detailed_theme {
        // Base colors
        fg "#cdd6f4"
        bg "#1e1e2e"

        // ANSI colors
        black "#45475a"
        red "#f38ba8"
        green "#a6e3a1"
        yellow "#f9e2af"
        blue "#89b4fa"
        magenta "#f5c2e7"
        cyan "#94e2d5"
        white "#bac2de"
        orange "#fab387"

        // Frame colors
        text_unselected {
            base 255 255 255
            background 30 30 46
        }

        text_selected {
            base 49 50 68
            background 205 214 244
        }

        ribbon_unselected {
            base 255 255 255
            background 88 91 112
        }

        ribbon_selected {
            base 49 50 68
            background 137 180 250
        }

        frame_unselected {
            base 88 91 112
            background 30 30 46
        }

        frame_selected {
            base 137 180 250
            background 30 30 46
        }
    }
}
```

**Built-in themes to reference:**
- `catppuccin-mocha`, `catppuccin-latte`
- `dracula`
- `gruvbox-dark`, `gruvbox-light`
- `nord`
- `tokyo-night`, `tokyo-night-storm`

**Apply theme:**
```kdl
// In config.kdl
theme "custom_theme"
```

Or via command line:
```bash
zellij options --theme custom_theme
```

#### Keybindings (in config.kdl)

**Keybinding structure:**
```kdl
keybinds {
    normal {
        bind "Ctrl g" { SwitchToMode "locked"; }
        bind "Ctrl p" { SwitchToMode "pane"; }
        bind "Ctrl t" { SwitchToMode "tab"; }
        bind "Ctrl n" { SwitchToMode "resize"; }
        bind "Ctrl h" { MoveFocus "Left"; }
        bind "Ctrl l" { MoveFocus "Right"; }
        bind "Ctrl j" { MoveFocus "Down"; }
        bind "Ctrl k" { MoveFocus "Up"; }
    }

    pane {
        bind "Ctrl p" { SwitchToMode "normal"; }
        bind "h" { MoveFocus "Left"; }
        bind "l" { MoveFocus "Right"; }
        bind "j" { MoveFocus "Down"; }
        bind "k" { MoveFocus "Up"; }
        bind "n" { NewPane; SwitchToMode "normal"; }
        bind "d" { NewPane "Down"; SwitchToMode "normal"; }
        bind "r" { NewPane "Right"; SwitchToMode "normal"; }
        bind "x" { CloseFocus; SwitchToMode "normal"; }
        bind "f" { ToggleFocusFullscreen; SwitchToMode "normal"; }
    }

    tab {
        bind "Ctrl t" { SwitchToMode "normal"; }
        bind "n" { NewTab; SwitchToMode "normal"; }
        bind "x" { CloseTab; SwitchToMode "normal"; }
        bind "r" { SwitchToMode "renametab"; }
        bind "h" { GoToPreviousTab; }
        bind "l" { GoToNextTab; }
        bind "1" { GoToTab 1; SwitchToMode "normal"; }
        bind "2" { GoToTab 2; SwitchToMode "normal"; }
        bind "3" { GoToTab 3; SwitchToMode "normal"; }
    }

    resize {
        bind "Ctrl n" { SwitchToMode "normal"; }
        bind "h" { Resize "Left"; }
        bind "j" { Resize "Down"; }
        bind "k" { Resize "Up"; }
        bind "l" { Resize "Right"; }
        bind "=" { Resize "Increase"; }
        bind "-" { Resize "Decrease"; }
    }

    locked {
        bind "Ctrl g" { SwitchToMode "normal"; }
    }
}
```

**Available modes:**
- `normal`: Default mode
- `pane`: Pane management
- `tab`: Tab management
- `resize`: Pane resizing
- `move`: Moving panes
- `scroll`: Scrollback navigation
- `locked`: Input pass-through (all keys go to terminal)
- `renametab`, `renamepane`: Renaming modes
- `session`: Session management

**Common actions:**
- `SwitchToMode "mode"`: Change mode
- `MoveFocus "direction"`: Focus navigation (Left/Right/Up/Down)
- `NewPane`, `NewPane "direction"`: Create pane
- `CloseFocus`: Close focused pane
- `NewTab`, `CloseTab`: Tab management
- `GoToTab N`: Jump to tab number
- `GoToPreviousTab`, `GoToNextTab`: Tab navigation
- `Resize "direction"`: Resize panes
- `ToggleFocusFullscreen`: Maximize/restore pane
- `TogglePaneFrames`: Show/hide borders
- `Quit`: Exit Zellij

**Key syntax:**
- `"Ctrl x"`: Control + key
- `"Alt x"`: Alt + key
- `"Ctrl Alt x"`: Multiple modifiers
- `"F1"` through `"F12"`: Function keys
- `"Space"`, `"Enter"`, `"Tab"`, `"Esc"`: Special keys
- Multiple bindings: `bind "x" "X" { Action; }`

### 4. Configuration Workflow

1. **Read existing config** (if present):
   ```bash
   Read ~/.config/zellij/config.kdl
   ```

2. **For new configs**, generate base:
   ```bash
   zellij setup --dump-config > ~/.config/zellij/config.kdl
   ```

3. **Apply changes** using Edit or Write:
   - Use Edit for incremental changes
   - Use Write for new files (layouts, themes)

4. **Validate KDL syntax**:
   - Proper nesting with braces `{}`
   - Quoted strings for keys and values
   - No trailing commas
   - Comments use `//`

5. **Test changes**:
   - Most config changes apply to new panes/tabs/sessions
   - Config file is live-reloaded
   - Use `zellij setup --check` to verify paths

### 5. Common Configuration Tasks

#### Complete Initial Setup

```kdl
// Mouse and UI
mouse_mode true
pane_frames true
simplified_ui false

// Behavior
copy_on_select true
scroll_buffer_size 10000
session_serialization true

// Shell and theme
default_shell "fish"
theme "catppuccin-mocha"

// Clipboard (macOS)
copy_command "pbcopy"
```

#### Vim-Style Keybindings

```kdl
keybinds {
    normal {
        bind "Ctrl h" { MoveFocus "Left"; }
        bind "Ctrl j" { MoveFocus "Down"; }
        bind "Ctrl k" { MoveFocus "Up"; }
        bind "Ctrl l" { MoveFocus "Right"; }

        bind "Ctrl n" { NewPane; }
        bind "Ctrl x" { CloseFocus; }
    }
}
```

#### Custom Development Layout

```kdl
layout {
    tab name="dev" {
        pane split_direction="vertical" {
            pane size="60%"
            pane split_direction="horizontal" {
                pane command="npm" {
                    args "run" "dev"
                }
                pane
            }
        }
    }
}
```

### 6. Integration with Dotfiles

Since this is a dotfiles repo following XDG spec:

1. **Store configs**: `config/zellij/config.kdl`
2. **Store layouts**: `config/zellij/layouts/*.kdl`
3. **Store themes**: `config/zellij/themes/*.kdl`
4. **Symlink to XDG location**:
   ```bash
   ln -sf ~/Development/dotfiles/config/zellij ~/.config/zellij
   ```
5. **Update link-config.sh** to include Zellij
6. **Add to flake.nix** package list
7. **Add to README** in tools section

## Output Format

When configuring Zellij:

1. **Show changes clearly** using KDL code blocks
2. **Explain structure** for complex layouts/themes
3. **Provide test commands** when relevant
4. **Note live reload**: "Config changes apply automatically"
5. **Include file paths** using `file:line` format

## Project Context

This dotfiles repo:
- Uses Nix for package management (`flake.nix`)
- Symlinks configs from `config/**` to `~/.config/`
- Follows XDG Base Directory spec
- Uses Fish shell by default
- Prioritizes reproducibility and cross-platform support

## Reference Documentation

For comprehensive options, reference:
- Configuration: https://zellij.dev/documentation/configuration.html
- Keybindings: https://zellij.dev/documentation/keybindings.html
- Themes: https://zellij.dev/documentation/themes.html
- Layouts: https://zellij.dev/documentation/layouts.html

Useful commands:
```bash
# Check config paths
zellij setup --check

# Generate default config
zellij setup --dump-config

# List available actions
zellij action --help
```
