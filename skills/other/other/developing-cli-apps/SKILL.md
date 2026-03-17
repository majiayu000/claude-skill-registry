---
name: developing-cli-apps
description: Develop CLI applications in Go. Use when creating or modifying CLI commands, adding flags or arguments, implementing command workflows, building interactive prompts, handling signals and exit codes, or working with stdin/stdout/stderr. Currently uses Cobra for command structure and Huh for interactive UI.
---

# CLI Application Development

Standards for building CLI applications in Go. Currently uses [Cobra](https://github.com/spf13/cobra) for command structure and [Huh](https://github.com/charmbracelet/huh) for interactive UI.

**Interactive UI patterns:** See [Interactive UI Reference](references/interactive-ui.md)

## Command Organization

- One file per command in `cmd/`, file name matches command name (camelCase)
- All commands registered in their own `init()` function via `rootCmd.AddCommand()`
- See `cmd/root.go` for the root command structure and initialization chain
- See any existing command file (e.g., `cmd/version.go`) for a minimal example

## Adding a New Command

1. Create a new file in `cmd/` (camelCase name matching the command)
2. Define a `cobra.Command` variable with `Use` and `Short` fields
3. In `init()`: register with `rootCmd.AddCommand()`, define flags, bind to Viper
4. Suppress the init lint: `//nolint:gochecknoinits // Cobra requires an init function to set up the command structure.`

## Flag Conventions

| Scope | Method |
|-------|--------|
| Global (all commands) | `rootCmd.PersistentFlags()` |
| Local (one command) | `cmd.Flags()` |

- Use `StringVar`/`BoolVar`/`CountVarP` (pointer-binding) for all flags
- Bind every flag to Viper: `viper.BindPFlag("name", cmd.Flags().Lookup("name"))`
- Use kebab-case for flag names: `--git-clone-protocol`, not `--gitCloneProtocol`
- Provide meaningful defaults and descriptions

## Initialization Chain

Global dependencies are initialized via `cobra.OnInitialize()` in `root.go`. Each initializer sets a package-level global. Order matters — later initializers may depend on earlier ones. Read `root.go` for the current chain.

## Error Handling in Commands

- Use `Run` (not `RunE`) — errors are handled inline with `logger.Error()` + `os.Exit(1)`
- Use `logger.Success()` for positive completion messages
- Keep `Run` functions thin — delegate to business logic in `lib/`

## Signal Handling and Cleanup

- Signal handlers are registered in `setupCleanup()` in `root.go`
- `PersistentPostRun` on root command handles successful completion cleanup
- Separate `cleanupAndExit()` function for error/signal paths
- Always clean up resources (loggers, temp files) on all exit paths

## Non-Interactive Mode

The `--non-interactive` flag:
- Disables all interactive prompts (Huh forms)
- Disables progress indicators
- Uses automatic defaults or explicit flag values instead
- Enables CI/CD and scripted usage

## Output Modes

| Flags | Mode | Behavior |
|-------|------|----------|
| (none) | Progress | Hierarchical spinners, hide command output |
| `--plain` | Plain | Simple log messages, hide command output |
| `-v` / `-vv` | Passthrough | Show all command output |
| `--non-interactive` | Passthrough | Show all command output |

See `GetDisplayMode()` in `root.go` for the resolution logic.

## Key Rules

- Commands should not import each other; share state via package-level variables in `cmd/`
- Use `fmt.Fprint(os.Stderr, ...)` for error output, logger for structured messages
- Always respect `--non-interactive` in any new interactive functionality
