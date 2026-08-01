---
name: aerospace
description: Configure and manage AeroSpace tiling window manager for macOS. Use when
  working with window layouts, tiling configurations, workspace management, monitor
  assignments, or AeroSpace keybindings. Keywor
---

---
name: aerospace
description: Configure and manage AeroSpace tiling window manager for macOS. Use when working with window layouts, tiling configurations, workspace management, monitor assignments, or AeroSpace keybindings. Keywords: aerospace, tiling, workspaces, window manager, i3-like.
---

# AeroSpace configuration skill

## Overview

AeroSpace is an i3-like tiling window manager for macOS. It uses a tree-based tiling paradigm where windows are organized in nested containers with different layouts and orientations.

## Configuration location

- Config file: `~/.config/aerospace/aerospace.toml`
- Alternative: `~/.aerospace.toml`
- Format: TOML
- Default config: `/Applications/AeroSpace.app/Contents/Resources/default-config.toml`

## Current configuration

### Workspace organization

**Internal monitor (built-in) - workspaces 1-5:**
- Windows automatically maximize with fullscreen mode
- No gaps for maximum screen usage
- Perfect for focused single-window work

**External monitor - workspaces 6-9:**
- Three-column tiling layout
- 8px gaps between windows
- Flexible window arrangement

### Workspace assignment

```toml
[workspace-to-monitor-force-assignment]
# Internal monitor
1 = 'built-in'
2 = 'built-in'
3 = 'built-in'
4 = 'built-in'
5 = 'built-in'

# External monitor (sequence number 2)
6 = 2
7 = 2
8 = 2
9 = 2
```

### Gap configuration

```toml
[gaps]
inner.horizontal = 8
inner.vertical = 8
outer.left = 8
outer.bottom = 8
outer.top = 8
outer.right = 8
```

## Key bindings

### Window navigation
- `alt-h/j/k/l` - Focus left/down/up/right window (vim-style)

### Window movement
- `alt-shift-h/j/k/l` - Move window left/down/up/right

### Workspace switching
- `alt-1` through `alt-9` - Switch to workspace 1-9

### Move window to workspace
- `alt-shift-1` through `alt-9` - Move window to workspace and follow

### Monitor management
- `alt-,` - Focus left monitor
- `alt-.` - Focus right monitor
- `alt-shift-,` - Move workspace to left monitor
- `alt-shift-.` - Move workspace to right monitor

### Layout controls
- `alt-shift-space` - Toggle floating/tiling
- `alt-f` - Toggle fullscreen
- `alt-shift-v` - Create vertical split (for three-column layout)
- `alt-shift-o` - Toggle horizontal/vertical orientation

### Resize mode
- `alt-r` - Enter resize mode
  - `h` - Decrease width
  - `j` - Increase height
  - `k` - Decrease height
  - `l` - Increase width
  - `enter` or `esc` - Exit resize mode

### Other
- `alt-shift-r` - Reload config
- `alt-shift-q` - Close window

## Core concepts

### Tree-based tiling

Every workspace contains a tree where:
- **Containers** have a layout and orientation
- **Windows** are leaf nodes
- Containers can be nested arbitrarily

### Layout types

1. **h_tiles** - Horizontal tiles (side-by-side)
2. **v_tiles** - Vertical tiles (stacked)
3. **h_accordion** - Horizontal accordion (overlapping)
4. **v_accordion** - Vertical accordion (overlapping)

### Normalization

Two automatic normalizations keep layouts sensible:
1. Single-child containers are flattened
2. Nested containers must have opposite orientations

### Creating three-column layout

1. Open first window (takes full width)
2. Open second window (splits horizontally - two columns)
3. Focus second window and press `alt-shift-v` to create vertical split
4. Open third window (appears in the vertical split)

Result: `[Window 1] [Window 2 over Window 3]`

## CLI reference

### Overview
```bash
aerospace [-h|--help] [-v|--version] <subcommand> [<args>...]
```

### Query commands

**list-monitors** - List monitors
```bash
aerospace list-monitors
aerospace list-monitors --focused
aerospace list-monitors --format '%{monitor-id} | %{monitor-name}'
aerospace list-monitors --json
aerospace list-monitors --count
```

**list-workspaces** - List workspaces
```bash
aerospace list-workspaces --all
aerospace list-workspaces --focused
aerospace list-workspaces --monitor focused
aerospace list-workspaces --monitor all --visible --empty no
aerospace list-workspaces --format '%{workspace}' --json
```

**list-windows** - List windows
```bash
aerospace list-windows --all
aerospace list-windows --focused
aerospace list-windows --workspace focused
aerospace list-windows --workspace 1
aerospace list-windows --monitor focused
aerospace list-windows --pid <pid>
aerospace list-windows --app-bundle-id <bundle-id>
aerospace list-windows --format '%{window-id} | %{app-name} | %{window-title}'
aerospace list-windows --json
```

**list-apps** - List running applications
```bash
aerospace list-apps
```

**list-modes** - List binding modes
```bash
aerospace list-modes
```

**list-exec-env-vars** - List environment variables for exec commands
```bash
aerospace list-exec-env-vars
```

**config** - Query config options
```bash
aerospace config <key>
```

### Window management

**focus** - Focus window
```bash
aerospace focus left|down|up|right
aerospace focus dfs-next|dfs-prev
aerospace focus --window-id <id>
aerospace focus --dfs-index <index>
aerospace focus left --ignore-floating
aerospace focus right --boundaries workspace --boundaries-action wrap-around-the-workspace
```

**move** - Move window
```bash
aerospace move left|down|up|right
aerospace move --window-id <id> left
aerospace move right --boundaries workspace --boundaries-action stop
```

**swap** - Swap windows
```bash
aerospace swap left|down|up|right
```

**resize** - Resize window
```bash
aerospace resize smart +50           # Smart resize (larger)
aerospace resize smart -50           # Smart resize (smaller)
aerospace resize width +100          # Increase width by 100px
aerospace resize height -50          # Decrease height by 50px
aerospace resize --window-id <id> smart +50
```

**close** - Close window
```bash
aerospace close
aerospace close --window-id <id>
```

**close-all-windows-but-current** - Close all windows except current
```bash
aerospace close-all-windows-but-current
```

### Layout commands

**layout** - Change layout
```bash
# Specific layouts
aerospace layout h_tiles             # Horizontal tiles
aerospace layout v_tiles             # Vertical tiles
aerospace layout h_accordion         # Horizontal accordion
aerospace layout v_accordion         # Vertical accordion

# Orientations
aerospace layout horizontal          # Change to horizontal
aerospace layout vertical            # Change to vertical

# Toggle commands (cycles through options)
aerospace layout tiles accordion              # Toggle tile vs accordion
aerospace layout horizontal vertical          # Toggle orientation
aerospace layout floating tiling              # Toggle float vs tiling

# Window-specific
aerospace layout --window-id <id> floating
```

**join-with** - Join windows under common parent
```bash
aerospace join-with left|down|up|right
aerospace join-with right            # Create nested vertical split
aerospace join-with down             # Create nested horizontal split
aerospace join-with --window-id <id> right
```

**split** - Split focused window
```bash
aerospace split horizontal|vertical
```

**flatten-workspace-tree** - Flatten workspace tree
```bash
aerospace flatten-workspace-tree
```

**balance-sizes** - Balance window sizes
```bash
aerospace balance-sizes
```

### Fullscreen commands

**fullscreen** - Toggle AeroSpace fullscreen
```bash
aerospace fullscreen
aerospace fullscreen on
aerospace fullscreen off
aerospace fullscreen on --no-outer-gaps
aerospace fullscreen --window-id <id>
```

**macos-native-fullscreen** - Toggle macOS fullscreen
```bash
aerospace macos-native-fullscreen
```

**macos-native-minimize** - Minimize window
```bash
aerospace macos-native-minimize
```

### Workspace commands

**workspace** - Focus workspace
```bash
aerospace workspace 1                # Switch to workspace 1
aerospace workspace next             # Next workspace
aerospace workspace prev             # Previous workspace
aerospace workspace next --wrap-around
aerospace workspace 5 --auto-back-and-forth
aerospace workspace 3 --fail-if-noop
```

**workspace-back-and-forth** - Toggle between workspaces
```bash
aerospace workspace-back-and-forth
```

**move-node-to-workspace** - Move window to workspace
```bash
aerospace move-node-to-workspace 1
aerospace move-node-to-workspace next
aerospace move-node-to-workspace prev --wrap-around
aerospace move-node-to-workspace 5 --focus-follows-window
aerospace move-node-to-workspace --window-id <id> 3
```

**move-workspace-to-monitor** - Move workspace to monitor
```bash
aerospace move-workspace-to-monitor left|down|up|right
aerospace move-workspace-to-monitor next|prev
aerospace move-workspace-to-monitor <monitor-pattern>
```

**summon-workspace** - Move workspace to focused monitor
```bash
aerospace summon-workspace 1
```

### Monitor commands

**focus-monitor** - Focus monitor
```bash
aerospace focus-monitor left|down|up|right
aerospace focus-monitor next|prev
aerospace focus-monitor <monitor-pattern>
aerospace focus-monitor next --wrap-around
```

**move-node-to-monitor** - Move window to monitor
```bash
aerospace move-node-to-monitor left|down|up|right
aerospace move-node-to-monitor next|prev
aerospace move-node-to-monitor <monitor-pattern>
```

**move-mouse** - Move mouse cursor
```bash
aerospace move-mouse monitor-lazy-center
aerospace move-mouse monitor-force-center
aerospace move-mouse window-lazy-center
aerospace move-mouse window-force-center
```

### Mode commands

**mode** - Activate binding mode
```bash
aerospace mode service
aerospace mode resize
aerospace mode main
```

**trigger-binding** - Trigger binding manually
```bash
aerospace trigger-binding --mode main --key alt-1
```

### System commands

**reload-config** - Reload configuration
```bash
aerospace reload-config
```

**enable** - Enable/disable window management
```bash
aerospace enable on|off|toggle
```

**volume** - Manipulate volume
```bash
aerospace volume <args>
```

**debug-windows** - Debug Accessibility API
```bash
aerospace debug-windows
```

### Focus back-and-forth

**focus-back-and-forth** - Toggle focus
```bash
aerospace focus-back-and-forth
```

## Common operations

### Quick status checks
```bash
# Current workspace
aerospace list-workspaces --focused

# All windows on current workspace
aerospace list-windows --workspace focused

# All monitors
aerospace list-monitors

# Current window tree
aerospace list-windows --workspace focused --format '%{window-id} | %{app-name}'
```

### Reload config
```bash
aerospace reload-config
# or use keybinding: alt-shift-r
```

## Monitor patterns

Workspace assignment supports:
- `main` - Primary monitor
- `secondary` - Non-main monitor (2-monitor setups only)
- `<number>` - Monitor sequence (1-based, left to right)
- `<regex>` - Case-insensitive substring match
- `'^pattern$'` - Full regex match

Example:
```toml
[workspace-to-monitor-force-assignment]
1 = 'main'
2 = 'secondary'
3 = 1                    # First monitor (leftmost)
4 = 2                    # Second monitor
5 = 'built-in'           # Substring match
6 = '^dell.*'            # Regex match
7 = ['secondary', 'dell'] # Multiple patterns (fallback)
```

## Configuration examples

### Per-monitor gaps
```toml
[gaps]
# Different gaps per monitor
inner.horizontal = [{ monitor.main = 0 }, { monitor.secondary = 8 }, 5]
outer.left = [{ monitor.'built-in' = 0 }, 10]
```

### Window callbacks
```toml
# Auto-tile all new windows
[[on-window-detected]]
if.during-aerospace-startup = false
run = 'layout tiling'

# Specific workspace behavior
[[on-window-detected]]
if.workspace = [1, 2, 3]
run = 'fullscreen on --no-outer-gaps'

# App-specific layout
[[on-window-detected]]
if.app-name-regex-substring = 'Terminal'
run = 'move-node-to-workspace 1'
```

### Custom modes
```toml
[mode.service.binding]
esc = 'mode main'
r = ['flatten-workspace-tree', 'mode main']
f = ['layout floating tiling', 'mode main']
h = ['layout horizontal vertical', 'mode main']

[mode.main.binding]
alt-shift-semicolon = 'mode service'
```

## Troubleshooting

### Check if AeroSpace is running
```bash
ps aux | rg -i aerospace
```

### View current workspace
```bash
aerospace list-workspaces --monitor focused --empty no
```

### View window tree
```bash
aerospace list-windows --workspace focused --format '%{window-id} | %{app-name} | %{window-title}'
```

### Config not loading
- Check config file location: `~/.config/aerospace/aerospace.toml`
- Validate TOML syntax
- Reload config: `aerospace reload-config` or `alt-shift-r`
- Check AeroSpace logs in Console.app

### Keybindings not working
- Check for conflicts with other apps (Hammerspoon, Karabiner, etc.)
- Verify modifier keys are correct
- Test with: `aerospace list-workspaces --monitor focused`

### Windows not tiling
- Check if window is floating: `aerospace list-windows --workspace focused`
- Toggle tiling: `alt-shift-space`
- Some apps force floating mode

## Resources

- Repository: https://github.com/nikitabobko/AeroSpace
- Documentation: https://github.com/nikitabobko/AeroSpace/blob/main/docs/guide.adoc
- Default config: https://github.com/nikitabobko/AeroSpace/blob/main/docs/config-examples/default-config.toml
- i3-like config example: https://github.com/nikitabobko/AeroSpace/blob/main/docs/config-examples/i3-like-config-example.toml
