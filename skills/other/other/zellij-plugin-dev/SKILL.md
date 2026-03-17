---
name: zellij-plugin-dev
description: Develop Zellij plugins with Rust/WASM, API reference, event system, UI rendering, plugin lifecycle, and real-world examples from diverse open source plugins
---

# Zellij Plugin Development Skill

Comprehensive assistance for developing Zellij terminal multiplexer plugins using Rust and WebAssembly.

## When to Use This Skill

Trigger this skill when:

- Developing Zellij plugins in Rust/WASM
- Implementing plugin UI, rendering, or event handling
- Working with the Zellij plugin API
- Integrating external systems (Docker, Git, etc.)
- Building status bars, navigation tools, or workflow automation
- Debugging plugin issues or understanding plugin lifecycle
- Learning plugin development patterns and best practices

## Quick Reference

### Core Plugin Structure

```rust
use zellij_tile::prelude::*;

#[derive(Default)]
struct State {
    // Your plugin state
}

impl ZellijPlugin for State {
    fn load(&mut self, configuration: BTreeMap<String, String>) {
        request_permission(&[PermissionType::ReadApplicationState]);
        subscribe(&[EventType::Key, EventType::PaneUpdate]);
    }

    fn update(&mut self, event: Event) -> bool {
        // Handle events, return true to re-render
        false
    }

    fn render(&mut self, rows: usize, cols: usize) {
        // Render UI
    }
}
```

### Building

```bash
# Add WASM target
rustup target add wasm32-wasi

# Build
cargo build --release

# Location: target/wasm32-wasi/release/<PLUGIN_NAME>.wasm
```

### Loading Plugins

```bash
# Temporary load
zellij plugin -- file://<PATH_TO_FILE>

# Floating
zellij plugin --floating -- file://<PATH>

# With configuration
zellij plugin -- file://<PATH> --configuration key=value
```

## Reference Files

### Official Documentation

- **plugin-development-tutorial.md** - Complete tutorial from scaffolding to distribution
- **plugin-api-commands.md** - All 100+ plugin API commands organized by category
- **plugin-api-events.md** - Event system, subscription patterns, and event handling

### Real-World Plugin Examples

- **plugin-examples-ui-navigation.md** - Monocle (fuzzy finder) and Room (tab switcher)
- **plugin-examples-status-theming.md** - zjstatus (configurable status bar)
- **plugin-examples-external-integration.md** - zj-docker (Docker integration)

## Development Workflow

### 1. Project Setup

Use the official scaffolding tool:

```bash
zellij plugin -f -- https://github.com/zellij-org/create-rust-plugin/releases/latest/download/create-rust-plugin.wasm
```

This launches `develop-rust-plugin` for real-time iteration (Ctrl+Shift+R to rebuild).

### 2. Core Implementation

**Load Phase:**

- Request permissions
- Subscribe to events
- Initialize state

**Update Phase:**

- Handle events
- Update state
- Return true to trigger re-render

**Render Phase:**

- Draw UI based on state
- Use color indices (0-3) for theme compatibility

### 3. Testing & Distribution

**Local Testing:**

```bash
zellij plugin -- file:./target/wasm32-wasi/release/plugin.wasm
```

**Release:**

```bash
cargo build --release
# Share via awesome-zellij repository
```

## Common Patterns

### Modal UI (Floating Windows)

```kdl
bind "Ctrl t" {
    LaunchOrFocusPlugin "file:path/to/plugin.wasm" {
        floating true
    }
}
```

### Command Execution with Context

```rust
let context = BTreeMap::from([
    ("operation".to_string(), "git_status".to_string())
]);
run_command(vec!["git", "status"], context);

// Handle result
Event::RunCommandResult(exit_code, stdout, stderr, context) => {
    if context.get("operation") == Some(&"git_status".to_string()) {
        self.process_result(stdout);
    }
}
```

### Configuration-Driven Widgets

```kdl
plugin location="path/to/plugin.wasm" {
    format_left  "{widget1} {widget2}"
    format_right "{widget3}"

    widget1_param1 "value"
    widget1_param2 "value"
}
```

### State Synchronization

```rust
fn load(&mut self, _config: BTreeMap<String, String>) {
    subscribe(&[EventType::PaneUpdate]);
}

fn update(&mut self, event: Event) -> bool {
    match event {
        Event::PaneUpdate(panes) => {
            self.sync_pane_state(panes);
            true
        }
        _ => false
    }
}
```

## Permission Categories

**Read-Only:**

- `ReadApplicationState` - Access mode, tabs, panes, sessions

**Write Operations:**

- `ChangeApplicationState` - Modify panes, tabs, navigation
- `OpenFiles` - Open files in $EDITOR
- `OpenTerminalsOrPlugins` - Create terminal/plugin panes
- `WriteToStdin` - Write to pane stdin

**Advanced:**

- `RunCommands` - Execute background commands
- `Reconfigure` - Modify configuration
- `WebAccess` - HTTP requests
- `FullHdAccess` - Host filesystem access

## Plugin Categories & Examples

### UI & Navigation

- **monocle** - Fuzzy file finder with gitignore support
- **room** - Tab search and switcher
- **harpoon** - Quick pane navigation

### Status & Display

- **zjstatus** - Configurable status bar with theming
- **zellij-datetime** - Date/time display
- **zjframes** - Pane frame management

### Development Tools

- **multitask** - Mini-CI system
- **grab** - Rust code fuzzy finder
- **zellij-bookmarks** - Command bookmarks

### External Integration

- **zj-docker** - Docker container management
- **zj-git-branch** - Git branch operations

### Session Management

- **zellij-sessionizer** - Folder-based sessions
- **zsm** - Session switcher with zoxide

## Resources

### Documentation

- **Official Docs:** https://zellij.dev/documentation/plugins
- **Rust API:** https://docs.rs/zellij-tile/latest/zellij_tile/
- **Tutorial:** https://zellij.dev/tutorials/developing-a-rust-plugin/

### Community

- **awesome-zellij:** https://github.com/zellij-org/awesome-zellij
- **Discord:** Zellij community for developer support
- **GitHub Topic:** https://github.com/topics/zellij-plugin

### Tools

- **create-rust-plugin:** Scaffolding tool (plugin)
- **develop-rust-plugin:** Live development helper (plugin)
- **rust-plugin-example:** Official example repository

## Working with This Skill

### For Beginners

Start with `plugin-development-tutorial.md` for foundational concepts and step-by-step guidance.

### For Specific Features

- UI/Navigation: See `plugin-examples-ui-navigation.md`
- Status Bars/Theming: See `plugin-examples-status-theming.md`
- External Integration: See `plugin-examples-external-integration.md`
- API Commands: See `plugin-api-commands.md`
- Events: See `plugin-api-events.md`

### For Code Examples

Each example file contains real-world patterns extracted from production plugins.

## Advanced Topics

### Widget Systems

Build configurable, composable UI components (see zjstatus example).

### External Process Management

Spawn and manage long-running processes (see zj-docker example).

### Multi-Agent Patterns

Coordinate multiple plugins via message passing.

### Performance Optimization

- Static vs dynamic rendering modes
- Efficient state updates
- Resource-conscious command execution

## Notes

- Plugins compile to WASM (wasm32-wasi target)
- Use color indices (0-3) instead of hex for theme compatibility
- Always check exit codes for command execution
- Leverage Zellij's pane system for long-running processes
- Use context maps to route command results
- Request permissions during `load()` phase

## File Organization

```
references/
  ├── plugin-development-tutorial.md      # Complete tutorial
  ├── plugin-api-commands.md              # API reference
  ├── plugin-api-events.md                # Event system
  ├── plugin-examples-ui-navigation.md    # UI patterns
  ├── plugin-examples-status-theming.md   # Configuration & theming
  └── plugin-examples-external-integration.md  # External systems

scripts/
  # Helper scripts for development automation

assets/
  # Templates, boilerplate, example projects
```

## Updating

To refresh this skill with updated documentation:

1. Re-run the scraper with the same configuration
2. Add new plugin examples as they emerge
3. Update patterns based on community best practices
