---
name: cli
description: CLI command structure, Cobra patterns, execution flow, hidden internal commands
disable-model-invocation: false
---

# CLI Architecture Skill

This skill covers the CLI implementation in Invowk, including Cobra command structure, dynamic command registration, TUI component wrappers, and the execution flow.

Use this skill when working on:
- `cmd/invowk/` - CLI commands and structure
- Adding new CLI commands or subcommands
- Modifying command output format
- TUI component integration
- Error handling and exit codes

---

## Command Hierarchy Structure

The CLI is organized under `root.go` with these main command groups:

| Command | Description |
|---------|-------------|
| `invowk cmd` | Dynamic command execution (discovered from invkfiles/modules) |
| `invowk module` | Module management (validate, create, alias, deps) |
| `invowk config` | Configuration management |
| `invowk init` | Initialize new invkfiles |
| `invowk tui` | Interactive terminal UI components (gum-like) |
| `invowk internal` | **Hidden** internal commands |
| `invowk completion` | Shell completion |

---

## Hidden Internal Commands Policy

**CRITICAL: All `invowk internal *` commands MUST remain hidden.**

```go
&cobra.Command{
    Use:    "internal",
    Hidden: true,  // ALWAYS true for internal commands
}
```

**Rules:**
- Internal commands are for inter-process communication and subprocess execution
- Do NOT document in website docs
- Only mention in `.claude/` and `README.md`
- Used by container runtime, SSH server, TUI server internals

---

## Dynamic Command Registration

The discovery → registration flow (`cmd_discovery.go`):

```
Discovery → Validation → Command Registration
                ↓
        DiscoveredCommandSet
         ├── Commands: all discovered
         ├── AmbiguousNames: conflicts
         └── SourceOrder: sorted sources
```

### Transparent Namespace

Unambiguous commands are registered under their `SimpleName`:

```bash
# Only one source defines "build" → user can run directly
invowk cmd build

# Multiple sources define "deploy" → requires disambiguation
invowk cmd @foo deploy      # Using @source prefix
invowk cmd --from foo deploy  # Using --from flag
```

### Hierarchical Tree Building

Multi-word commands (e.g., "deploy staging") are built into a command tree with automatically created parent commands.

---

## TUI Component Wrapper Pattern

All TUI components follow a **dual-layer delegation pattern** (`tui_*.go`):

```go
func runTuiInput(cmd *cobra.Command, args []string) error {
    // Layer 1: Check if running under parent TUI server
    if client := tuiserver.NewClientFromEnv(); client != nil {
        // Delegate to parent TUI server via HTTP/IPC
        result, err := client.Input(tuiserver.InputRequest{...})
        return handleResult(result)
    }

    // Layer 2: Direct TUI rendering
    result, err := tui.Input(tui.InputOptions{...})
    return handleResult(result)
}
```

### Available TUI Commands

| Command | Purpose |
|---------|---------|
| `tui input` | Single-line text input |
| `tui choose` | Single/multi-select from list |
| `tui confirm` | Yes/no confirmation |
| `tui spin` | Spinner with command execution |
| `tui filter` | Fuzzy filter |
| `tui file` | File picker |
| `tui table` | Display/select from table |
| `tui pager` | Scrollable content viewer |
| `tui format` | Markdown/code/emoji formatting |
| `tui write` | Multi-line text editor |

**Benefits:**
- Commands work both standalone and nested in TUI server
- Output to stdout for piping/variable assignment
- Consistent behavior across execution contexts

---

## Discovery → Runtime → Execution Flow

The complete execution path (`cmd_execute.go`):

```
runCommandWithFlags()
    │
    ├── discovery.GetCommand(cmdName)
    │
    ├── Validate runtime selection
    │   └── Check allowed runtimes for platform
    │
    ├── Validate dependencies
    │   ├── Tools (runtime-aware)
    │   ├── Filepaths (runtime-aware)
    │   ├── Capabilities (host-only)
    │   ├── CustomChecks (runtime-aware)
    │   ├── EnvVars (host-only)
    │   └── Commands (existence check)
    │
    ├── Create ExecutionContext
    │   ├── Selected runtime
    │   ├── Implementation script
    │   ├── Positional arguments
    │   ├── Environment config
    │   ├── Working directory
    │   └── Force rebuild flag
    │
    ├── Create runtime.Registry
    │
    └── Execute via selected runtime
```

---

## Disambiguation Pattern

Two methods for specifying command source:

### @source Prefix (First Argument)

```bash
invowk cmd @foo deploy      # Run deploy from foo.invkmod
invowk cmd @invkfile build  # Run build from invkfile.cue
```

### --from Flag

```bash
invowk cmd --from foo deploy
```

### Source Name Normalization

`normalizeSourceName()` handles various formats:
- `"foo"` → `"foo"`
- `"foo.invkmod"` → `"foo"`
- `"invkfile"` → `"invkfile"`
- `"invkfile.cue"` → `"invkfile"`

---

## Error Handling & Exit Codes

### ExitError Type

```go
type ExitError struct {
    Code int
    Err  error
}
```

**Pattern:**
- Command `RunE` returns `ExitError` for non-zero exit codes
- Root `Execute()` catches `ExitError` and calls `os.Exit(exitErr.Code)`
- Prevents cascading error messages while maintaining proper exit codes

### Styled Error Rendering

`cmd_render.go` provides styled error messages for:
- Argument validation failures
- Dependency errors
- Runtime mismatches
- Ambiguous commands
- Host platform compatibility issues

---

## Styling System

Unified color palette (`styles.go`):

| Color | Hex | Use |
|-------|-----|-----|
| ColorPrimary | `#7C3AED` | Titles (purple) |
| ColorMuted | `#6B7280` | Subtitles (gray) |
| ColorSuccess | `#10B981` | Success (green) |
| ColorError | `#EF4444` | Errors (red) |
| ColorWarning | `#F59E0B` | Warnings (amber) |
| ColorHighlight | `#3B82F6` | Commands/links (blue) |
| ColorVerbose | `#9CA3AF` | Verbose output (light gray) |

**Reusable Styles:**
- `TitleStyle`, `SubtitleStyle`, `SuccessStyle`, `ErrorStyle`
- `WarningStyle`, `CmdStyle`, `VerboseStyle`

---

## Global Flags

### Root Command (Persistent)

```go
--verbose, -v     // Enable verbose output
--config          // Custom config file path
--interactive, -i // Run in alternate screen buffer
```

### Cmd Command

```go
--runtime, -r     // Override runtime (must be allowed)
--from            // Specify source for disambiguation
--force-rebuild   // Force container image rebuild
```

---

## Configuration Loading

Flow from `root.go`:

```go
Execute()
    ↓
cobra.OnInitialize(initRootConfig)
    ├── Apply --config flag override
    ├── Load config via config.Load()
    ├── Surface errors as warnings (non-fatal)
    ├── Apply verbose/interactive from config if not set via flags
    └── Store in GetVerbose(), GetInteractive() accessors
```

**Priority:** CLI flags > config file > defaults

---

## Module Commands

Module management (`module.go`):

| Command | Purpose |
|---------|---------|
| `module validate` | Validate module structure & dependencies |
| `module create` | Create new module |
| `module list` | List discovered modules |
| `module archive` | Package module as archive |
| `module import` | Import external module |
| `module alias` | Create module aliases |

### Dependency Management

```bash
module add <module>     # Add dependency
module remove <module>  # Remove dependency
module sync             # Sync dependencies
module update           # Update dependencies
module deps             # Inspect dependency tree
```

---

## Discovery Integration Points

```go
disc := discovery.New(cfg)

// Discover and validate all commands (with ambiguity detection)
commandSet, err := disc.DiscoverAndValidateCommandSet()

// Get specific command info (for execution)
cmdInfo, err := disc.GetCommand(cmdName)

// List all discovered commands (for completion)
commands, err := disc.DiscoverCommands()

// List all discovered files (for module operations)
files, err := disc.DiscoverAll()
```

---

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| Transparent namespace | Users don't specify source for unambiguous commands |
| Explicit disambiguation | Require @source or --from for ambiguous commands |
| Platform-aware execution | Different runtimes, validation per platform |
| Dual-layer TUI | Support standalone and server-delegated rendering |
| Styled consistency | Unified color palette across all output |
| Hidden internals | Internal commands not documented to users |
| Configuration priority | CLI flags > config file > defaults |

---

## File Organization

| File | Purpose |
|------|---------|
| `root.go` | Root command, global flags, config loading |
| `cmd.go` | `invowk cmd` parent, disambiguation |
| `cmd_discovery.go` | Dynamic command registration |
| `cmd_execute.go` | Command execution, validation |
| `cmd_render.go` | Styled error rendering |
| `module.go` | Module commands |
| `tui_*.go` | TUI component wrappers |
| `styles.go` | Unified styling system |
| `internal_*.go` | Hidden internal commands |

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Forgetting `Hidden: true` on internal cmd | Users see internal commands | Add `Hidden: true` to command |
| Hardcoded exit in RunE | Error message not shown | Return `ExitError` instead |
| Missing TUI server check | TUI components fail in nested context | Use dual-layer pattern |
| Not using styled output | Inconsistent CLI appearance | Use styles from `styles.go` |
| Wrong flag priority | Config overrides CLI flag | Check precedence logic |
