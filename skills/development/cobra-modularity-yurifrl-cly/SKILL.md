---
name: cobra-modularity
description: Build modular CLI applications with Cobra framework. Use when structuring CLI commands, implementing modular command architecture, handling flags and arguments, or when user mentions Cobra, CLI modularity, command registration, or spf13/cobra.
---

# Cobra Modular CLI Architecture

Build scalable, maintainable CLI applications using Cobra with modular command registration patterns.

## Your Role: CLI Architect

You help structure CLI applications with clean, modular architecture. You:

✅ **Design modular command structure** - Self-contained command modules
✅ **Implement Register pattern** - Commands register themselves
✅ **Handle flags properly** - Persistent vs local, parsing, validation
✅ **Structure subcommands** - Nested command hierarchies
✅ **Apply Cobra idioms** - RunE for errors, PreRun hooks, etc.
✅ **Follow project patterns** - Use existing module conventions

❌ **Do NOT centralize commands** - Keep modules self-contained
❌ **Do NOT modify root unnecessarily** - Add via registration only
❌ **Do NOT ignore errors** - Use RunE, not Run

## Core Principles

### 1. Modular Command Registration

Commands live in their own packages and register with parent commands.

**✅ GOOD - Self-registering module:**
```go
// modules/demo/cmd.go
package demo

import "github.com/spf13/cobra"

func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "demo",
        Short: "Demo commands",
    }
    parent.AddCommand(cmd)

    // Register subcommands
    spinner.Register(cmd)
    list.Register(cmd)
}
```

**❌ BAD - Centralized registration:**
```go
// cmd/root.go - DON'T do this
func init() {
    RootCmd.AddCommand(demoCmd)
    RootCmd.AddCommand(listCmd)
    RootCmd.AddCommand(spinnerCmd)
    // Root knows too much
}
```

### 2. Command Structure Pattern

**Standard module layout:**
```
modules/demo/
├── cmd.go              # Register function
├── spinner/
│   ├── cmd.go         # spinner.Register()
│   └── spinner.go     # Implementation
└── list/
    ├── cmd.go         # list.Register()
    └── list.go        # Implementation
```

**Benefits:**
- Module is self-contained
- Easy to add/remove commands
- No changes to root when adding modules
- Testable in isolation

### 3. Error Handling

**Use RunE (not Run):**

**✅ GOOD:**
```go
cmd := &cobra.Command{
    Use:   "fetch",
    Short: "Fetch data",
    RunE:  run,  // Returns error
}

func run(cmd *cobra.Command, args []string) error {
    if err := doWork(); err != nil {
        return fmt.Errorf("fetch failed: %w", err)
    }
    return nil
}
```

**❌ BAD:**
```go
cmd := &cobra.Command{
    Run: func(cmd *cobra.Command, args []string) {
        doWork()  // Error ignored
    },
}
```

## Cobra Command Structure

### Basic Command

```go
package mycommand

import (
    "github.com/spf13/cobra"
)

func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "mycommand",
        Short: "Short description",
        Long:  `Long description with examples`,
        RunE:  run,
    }
    parent.AddCommand(cmd)
}

func run(cmd *cobra.Command, args []string) error {
    // Implementation
    return nil
}
```

### With Flags

**Local flags (command-specific):**
```go
var (
    flagName   string
    flagCount  int
    flagVerbose bool
)

func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "process",
        Short: "Process data",
        RunE:  run,
    }

    // String flag with shorthand
    cmd.Flags().StringVarP(&flagName, "name", "n", "", "Name (required)")
    cmd.MarkFlagRequired("name")

    // Int flag
    cmd.Flags().IntVarP(&flagCount, "count", "c", 10, "Count")

    // Bool flag
    cmd.Flags().BoolVarP(&flagVerbose, "verbose", "v", false, "Verbose output")

    parent.AddCommand(cmd)
}

func run(cmd *cobra.Command, args []string) error {
    // Use flagName, flagCount, flagVerbose
    return nil
}
```

**Persistent flags (inherited by subcommands):**
```go
func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "server",
        Short: "Server commands",
    }

    // Available to all subcommands
    cmd.PersistentFlags().StringP("config", "c", "", "Config file")

    parent.AddCommand(cmd)

    // Register subcommands
    start.Register(cmd)  // Can access --config
    stop.Register(cmd)   // Can access --config
}
```

### With Arguments

**Exact args:**
```go
cmd := &cobra.Command{
    Use:   "delete <id>",
    Short: "Delete item by ID",
    Args:  cobra.ExactArgs(1),  // Requires exactly 1 arg
    RunE:  run,
}

func run(cmd *cobra.Command, args []string) error {
    id := args[0]
    return deleteItem(id)
}
```

**Range of args:**
```go
Args: cobra.RangeArgs(1, 3),  // 1 to 3 args
Args: cobra.MinimumNArgs(1),  // At least 1 arg
Args: cobra.MaximumNArgs(2),  // At most 2 args
```

**Custom validation:**
```go
Args: func(cmd *cobra.Command, args []string) error {
    if len(args) != 1 {
        return fmt.Errorf("requires exactly one arg")
    }
    if !isValidID(args[0]) {
        return fmt.Errorf("invalid ID: %s", args[0])
    }
    return nil
},
```

## Module Patterns

### Demo Module Pattern (CLY)

**Parent command** - `modules/demo/cmd.go`:
```go
package demo

import (
    "github.com/spf13/cobra"
    spinner "github.com/yurifrl/cly/modules/demo/spinner"
)

var DemoCmd = &cobra.Command{
    Use:   "demo",
    Short: "Demo TUI components",
}

func Register(parent *cobra.Command) {
    parent.AddCommand(DemoCmd)
}

func init() {
    // Register all demo subcommands
    spinner.Register(DemoCmd)
    // ... more demos
}
```

**Subcommand** - `modules/demo/spinner/cmd.go`:
```go
package spinner

import (
    tea "github.com/charmbracelet/bubbletea"
    "github.com/spf13/cobra"
)

func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "spinner",
        Short: "Spinner demo",
        RunE:  run,
    }
    parent.AddCommand(cmd)
}

func run(cmd *cobra.Command, args []string) error {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        return err
    }
    return nil
}
```

### Utility Module Pattern (CLY)

**Standalone command** - `modules/uuid/cmd.go`:
```go
package uuid

import (
    tea "github.com/charmbracelet/bubbletea"
    "github.com/spf13/cobra"
)

func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "uuid",
        Short: "Generate UUIDs",
        Long:  "Interactive UUID generator with history",
        RunE:  run,
    }
    parent.AddCommand(cmd)
}

func run(cmd *cobra.Command, args []string) error {
    p := tea.NewProgram(initialModel())
    _, err := p.Run()
    return err
}
```

**Registered in root** - `cmd/root.go`:
```go
import (
    "github.com/yurifrl/cly/modules/uuid"
    "github.com/yurifrl/cly/modules/demo"
)

func init() {
    uuid.Register(RootCmd)
    demo.Register(RootCmd)
}
```

## Advanced Patterns

### PreRun Hooks

**Validate before run:**
```go
cmd := &cobra.Command{
    Use:  "deploy",
    PreRunE: func(cmd *cobra.Command, args []string) error {
        // Validation
        if !fileExists(configFile) {
            return fmt.Errorf("config not found: %s", configFile)
        }
        return nil
    },
    RunE: run,
}
```

**Setup before run:**
```go
PreRunE: func(cmd *cobra.Command, args []string) error {
    // Setup database connection
    db, err = connectDB()
    return err
},
```

### PostRun Hooks

**Cleanup after run:**
```go
PostRun: func(cmd *cobra.Command, args []string) {
    // Cleanup
    db.Close()
    tempFile.Remove()
},
```

### Persistent PreRun (Inherited)

```go
cmd := &cobra.Command{
    Use: "api",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        // Runs before ALL subcommands
        return loadConfig()
    },
}
```

### Flag Dependencies

**Require flag if another present:**
```go
cmd.Flags().String("format", "", "Output format")
cmd.Flags().String("output", "", "Output file")

cmd.MarkFlagsRequiredTogether("format", "output")
```

**Mutually exclusive flags:**
```go
cmd.Flags().Bool("json", false, "JSON output")
cmd.Flags().Bool("yaml", false, "YAML output")

cmd.MarkFlagsMutuallyExclusive("json", "yaml")
```

### Subcommand Groups

```go
parent := &cobra.Command{
    Use:   "api",
    Short: "API commands",
}

// Group 1
parent.AddGroup(&cobra.Group{
    ID:    "server",
    Title: "Server Commands:",
})

cmd1 := &cobra.Command{
    Use:     "start",
    GroupID: "server",
}

cmd2 := &cobra.Command{
    Use:     "stop",
    GroupID: "server",
}

parent.AddCommand(cmd1, cmd2)
```

## Configuration Integration

### With Viper

```go
import (
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var cfgFile string

func Register(parent *cobra.Command) {
    cmd := &cobra.Command{
        Use:   "server",
        Short: "Run server",
        PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
            return initConfig()
        },
        RunE: run,
    }

    cmd.PersistentFlags().StringVar(&cfgFile, "config", "", "Config file")

    // Bind flag to viper
    viper.BindPFlag("config", cmd.PersistentFlags().Lookup("config"))

    parent.AddCommand(cmd)
}

func initConfig() error {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        viper.SetConfigName("config")
        viper.SetConfigType("yaml")
        viper.AddConfigPath(".")
        viper.AddConfigPath("$HOME/.myapp")
    }

    viper.AutomaticEnv()
    return viper.ReadInConfig()
}

func run(cmd *cobra.Command, args []string) error {
    port := viper.GetInt("server.port")
    // Use config
    return nil
}
```

## Best Practices

### 1. Keep Commands Focused

**One responsibility per command:**
```go
// ✅ GOOD
cly uuid              # Generate UUIDs
cly demo spinner      # Show spinner demo

// ❌ BAD
cly utils  # Does everything
```

### 2. Use Meaningful Names

```go
// ✅ GOOD
Use: "generate",
Use: "list-users",
Use: "deploy-app",

// ❌ BAD
Use: "do",
Use: "run",
Use: "execute",
```

### 3. Provide Good Help

```go
cmd := &cobra.Command{
    Use:   "deploy <environment>",
    Short: "Deploy application",
    Long: `Deploy the application to specified environment.

Environments: dev, staging, prod

Examples:
  cly deploy dev
  cly deploy prod --version v1.2.3`,
    Example: `  cly deploy dev
  cly deploy prod --version v1.2.3`,
}
```

### 4. Validate Early

```go
PreRunE: func(cmd *cobra.Command, args []string) error {
    // Validate flags
    if port < 1 || port > 65535 {
        return fmt.Errorf("invalid port: %d", port)
    }

    // Check prerequisites
    if !commandExists("docker") {
        return fmt.Errorf("docker not found")
    }

    return nil
},
```

### 5. Handle Interrupts

```go
import (
    "context"
    "os/signal"
    "syscall"
)

func run(cmd *cobra.Command, args []string) error {
    ctx, stop := signal.NotifyContext(
        context.Background(),
        os.Interrupt,
        syscall.SIGTERM,
    )
    defer stop()

    return runWithContext(ctx)
}
```

## Testing Commands

### Test Registration

```go
func TestRegister(t *testing.T) {
    parent := &cobra.Command{Use: "root"}
    Register(parent)

    require.Len(t, parent.Commands(), 1)
    require.Equal(t, "mycommand", parent.Commands()[0].Use)
}
```

### Test Command Execution

```go
func TestRun(t *testing.T) {
    cmd := &cobra.Command{
        Use:  "test",
        RunE: run,
    }

    cmd.SetArgs([]string{"arg1", "arg2"})

    err := cmd.Execute()
    require.NoError(t, err)
}
```

### Test with Flags

```go
func TestRunWithFlags(t *testing.T) {
    cmd := &cobra.Command{
        Use:  "test",
        RunE: run,
    }

    var flagValue string
    cmd.Flags().StringVar(&flagValue, "flag", "", "test flag")

    cmd.SetArgs([]string{"--flag", "value"})

    err := cmd.Execute()
    require.NoError(t, err)
    require.Equal(t, "value", flagValue)
}
```

## Common Pitfalls

**❌ Using Run instead of RunE:**
```go
Run: func(cmd *cobra.Command, args []string) {
    // Can't return errors!
    doWork()
}
```

**✅ Use RunE:**
```go
RunE: func(cmd *cobra.Command, args []string) error {
    return doWork()
}
```

**❌ Not validating args:**
```go
RunE: func(cmd *cobra.Command, args []string) error {
    id := args[0]  // Panic if no args!
    return nil
}
```

**✅ Validate with Args:**
```go
cmd := &cobra.Command{
    Args: cobra.ExactArgs(1),
    RunE: run,
}
```

**❌ Centralizing all commands:**
```go
// root.go
RootCmd.AddCommand(cmd1)
RootCmd.AddCommand(cmd2)
RootCmd.AddCommand(cmd3)
// Tight coupling
```

**✅ Module registration:**
```go
// Each module registers itself
module1.Register(RootCmd)
module2.Register(RootCmd)
```

## Checklist

- [ ] Command uses RunE (not Run)
- [ ] Register() function for modularity
- [ ] Args validated with Args field
- [ ] Flags bound to variables
- [ ] Required flags marked
- [ ] Good Short description
- [ ] Detailed Long description
- [ ] Examples provided
- [ ] Errors wrapped with context
- [ ] Tests for command execution

## Reference

**CLY Project Structure:**
```
cmd/
└── root.go              # Root command, imports modules

modules/
├── demo/
│   ├── cmd.go          # demo.Register()
│   └── spinner/
│       └── cmd.go      # spinner.Register()
└── uuid/
    └── cmd.go          # uuid.Register()
```

**Pattern:** Each module registers itself, no central registration.

## Resources

- [Cobra Docs](https://cobra.dev/)
- [Cobra User Guide](https://github.com/spf13/cobra/blob/main/user_guide.md)
- [Viper Config](https://github.com/spf13/viper)
- CLY examples: `modules/demo/`, `modules/uuid/`
