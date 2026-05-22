---
name: add-module
description: Create new demo or utility modules following CLY project patterns. Use when adding TUI demonstration modules to modules/demo/ or utility modules to modules/, following Bubbletea/Bubbles conventions with proper Cobra CLI integration.
---

# Add Module Skill

Automates creation of new modules in the CLY project following established patterns.

## Module Isolation Principle (CRITICAL)

**The Portability Test**: Before creating a module, ask: *"If I copy this module folder to a new repo, how hard would it be to make it work?"*

The answer should be: **trivially easy**.

### Requirements for Isolation

- **Self-contained**: All module logic lives within its directory
- **Minimal dependencies**: Only depend on stdlib, Bubbletea/Bubbles/Lipgloss, and Cobra
- **No cross-module imports**: Modules NEVER import from other modules
- **Single registration point**: Only touch parent's `cmd.go` for registration
- **Own types**: Define types locally, don't reach into other packages

### What a Module Can Import

```
✓ Standard library (fmt, strings, etc.)
✓ github.com/charmbracelet/bubbletea
✓ github.com/charmbracelet/bubbles/*
✓ github.com/charmbracelet/lipgloss
✓ github.com/spf13/cobra
✓ github.com/yurifrl/cly/pkg/*  (shared utilities - see below)
✗ github.com/yurifrl/cly/modules/*  (NEVER)
```

### Avoiding Duplication (The Balance)

Isolation doesn't mean blind copy-paste. Use `pkg/` for genuinely shared code:

| Location | Purpose | Example |
|----------|---------|---------|
| `pkg/style/` | Shared Lipgloss styles | Colors, borders, common styles |
| `pkg/keys/` | Common keybindings | Quit keys, navigation patterns |
| `pkg/tui/` | TUI utilities | Screen helpers, common components |

**Rule of Three**: Only extract to `pkg/` when 3+ modules need the same code.

**Duplication is OK when**:
- Variations exist between modules
- Extraction would create tight coupling

**Extract to pkg/ when**:
- Exact same code in 3+ places
- Code is substantial and stable
- Changes should propagate everywhere

### Module Directory = Complete Unit

```
modules/demo/spinner/
├── cmd.go        # Registration only
├── spinner.go    # All logic here
└── (optional)    # Helpers if needed, but keep in same package
```

Copy this folder → paste in new project → change import path → works.

## When to Use This Skill

- User wants to add a new demo module showcasing a Bubbletea component
- User wants to create a new utility command
- User mentions "create a module", "add a command", "new demo"

## Module Types

### Demo Modules (`modules/demo/<name>/`)
**Purpose**: Showcase Charm UI components and patterns
**Examples**: chat, spinner, table, list-simple (48 total)
**Parent**: Registered under `demo` namespace

### Utility Modules (`modules/<name>/`)
**Purpose**: Provide real functionality
**Examples**: uuid (UUID generator)
**Parent**: Registered directly under root command

## Step-by-Step Workflow

### Determine Module Type
Ask user if unclear:
- "Is this a demo (showcase component) or utility (real functionality)?"

### Find Reference (for demos)
- Check if component exists in `references/bubbletea/examples/<name>/`
- Read the reference implementation
- Note initialization code in main() function

### Create Directory Structure
```bash
# For demo:
mkdir -p modules/demo/<name>

# For utility:
mkdir -p modules/<name>
```

### Create cmd.go (Command Registration)

**Template for demos:**
```go
package <packagename>

import (
	tea "github.com/charmbracelet/bubbletea"
	"github.com/spf13/cobra"
)

func Register(parent *cobra.Command) {
	cmd := &cobra.Command{
		Use:   "<name>",
		Short: "<description>",
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

**Add tea.Program options if needed:**
- `tea.WithAltScreen()` - For fullscreen demos
- `tea.WithMouseAllMotion()` - For mouse tracking
- `tea.WithReportFocus()` - For focus/blur events

### Create Implementation File

**Extract from reference:**
- Copy type definitions (model struct, custom types)
- Copy Init(), Update(), View() methods
- Create initialModel() from main() function's initialization code
- Remove unused imports (fmt, os, log often unused after main() removal)

**Template:**
```go
package <packagename>

import (
	tea "github.com/charmbracelet/bubbletea"
	// Component imports as needed
)

type model struct {
	// State fields
}

func initialModel() model {
	// Initialization from reference's main()
	return model{}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			return m, tea.Quit
		}
	}
	return m, nil
}

func (m model) View() string {
	return "Your UI\n"
}
```

### Register Module

**For demos** - Edit `modules/demo/cmd.go`:
```go
import (
	yourmodule "github.com/yurifrl/cly/modules/demo/your-module"
)

func init() {
	// ... existing registrations
	yourmodule.Register(DemoCmd)
}
```

**For utilities** - Edit `cmd/root.go`:
```go
import (
	"github.com/yurifrl/cly/modules/yourutil"
)

func init() {
	// ... existing registrations
	yourutil.Register(RootCmd)
}
```

### Validation Checklist

- [ ] Compiles: `go build`
- [ ] Shows in help: `go run main.go --help` or `go run main.go demo --help`
- [ ] Runs: `go run main.go <command>` (or `go run main.go demo <name>`)
- [ ] Quits cleanly with 'q' or Ctrl+C
- [ ] No unused imports

## Common Patterns

### Package Naming
- Directory with hyphens: `list-simple/`
- Package name with underscores: `package list_simple`
- Import alias: `listsimple "github.com/yurifrl/cly/modules/demo/list-simple"`

### Extracting initialModel()

**In reference main():**
```go
func main() {
	s := spinner.New()
	s.Spinner = spinner.Dot
	m := model{spinner: s}
	tea.NewProgram(m).Run()
}
```

**Extract to:**
```go
func initialModel() model {
	s := spinner.New()
	s.Spinner = spinner.Dot
	return model{spinner: s}
}
```

### Helper Functions
If reference has helpers (like getPackages(), filter(), etc.), copy them to the implementation file.

## Examples to Reference

**Simple**: `modules/demo/spinner/` - Basic component
**Complex**: `modules/demo/list-fancy/` - Multiple files (delegate.go, randomitems.go)
**Utility**: `modules/uuid/` - Real functionality with list UI
**Advanced**: `modules/demo/chat/` - Multiple components (textarea + viewport)

## Quick Reference Commands

```bash
# Test compilation
go build

# View help
go run main.go --help
go run main.go demo --help

# Run demo
go run main.go demo <name>

# Run utility
go run main.go <name>

# Clean dependencies
go mod tidy
```

## Best Practices

**Start from reference** - All 48 Bubbletea examples available in references/
**Copy existing module** - Fastest way to get structure right
**Test incrementally** - Build and run after each file
**Clean imports early** - Remove fmt/os/log before testing
**Follow naming** - Hyphens in names, underscores in packages

## Troubleshooting

### Build Errors
- **"undefined: initialModel"** → Function not created or private (make sure it's `initialModel`, not `InitialModel`)
- **"unused import"** → Remove it from imports
- **"package name mismatch"** → Check hyphens vs underscores

### Runtime Errors
- **"could not open TTY"** → Normal in non-interactive shells, try in terminal
- **Component not responding** → Check Update() delegates to component's Update()
- **Can't quit** → Verify KeyMsg handling for "q" and "ctrl+c"

---

# Module Template

**Use this template to add new commands quickly.**

---

## Module Categories

### Demo Modules (UI Component Showcases)
**Location**: `modules/demo/<name>/`
**Purpose**: Demonstrate Charm components and patterns
**Examples**: `chat`, `spinner`, `table`, `list-simple`

**When to use**: Showcasing UI components, TUI patterns, Bubbletea features

### Utility Modules (Real Functionality)
**Location**: `modules/<name>/`
**Purpose**: Provide actual utility commands
**Examples**: `uuid` (UUID generator)

**When to use**: Commands users will actually use for work

---

## Quick Steps

### For Demo Modules
- Find reference: `references/bubbletea/examples/<component>/`
- Copy pattern: `cp -r modules/demo/spinner modules/demo/<newname>`
- Adapt implementation from reference
- Register in `modules/demo/cmd.go` init()
- Test

### For Utility Modules
- Copy pattern: `cp -r modules/uuid modules/<newname>`
- Implement functionality
- Register in `cmd/root.go` init()
- Test

---

## Demo Module Template

### File: `modules/demo/<name>/cmd.go`

```go
package <packagename>  // Use underscores for hyphens: list_simple for list-simple

import (
	tea "github.com/charmbracelet/bubbletea"
	"github.com/spf13/cobra"
)

func Register(parent *cobra.Command) {
	cmd := &cobra.Command{
		Use:   "<name>",
		Short: "<short description>",
		Long:  "<detailed description>",
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

### File: `modules/demo/<name>/<name>.go`

```go
package <packagename>

import (
	tea "github.com/charmbracelet/bubbletea"
	// Add component imports as needed:
	// "github.com/charmbracelet/bubbles/spinner"
	// "github.com/charmbracelet/bubbles/list"
	// "github.com/charmbracelet/bubbles/table"
	// "github.com/charmbracelet/lipgloss"
)

type model struct {
	// Component state
	quitting bool
	err      error
}

func initialModel() model {
	// Initialize your model here
	// Extract this from reference example's main() function
	return model{}
}

func (m model) Init() tea.Cmd {
	return nil
	// Or return component's Init: spinner.Tick, textarea.Blink, etc.
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			m.quitting = true
			return m, tea.Quit
		}
	}

	return m, nil
}

func (m model) View() string {
	if m.quitting {
		return "Goodbye!\n"
	}

	return "Your UI here\nPress q to quit\n"
}
```

---

## Registration Patterns

### Demo Module Registration

**File**: `modules/demo/cmd.go`

```go
import (
	// ...
	yourmodule "github.com/yurifrl/cly/modules/demo/your-module"
)

func init() {
	// ...
	yourmodule.Register(DemoCmd)
}
```

### Utility Module Registration

**File**: `cmd/root.go`

```go
import (
	// ...
	"github.com/yurifrl/cly/modules/yourutil"
)

func init() {
	uuid.Register(RootCmd)
	demo.Register(RootCmd)
	yourutil.Register(RootCmd)  // Add here
}
```

---

## Bubbletea Program Options

Some demos require special options when creating the tea.Program:

### AltScreen (Fullscreen Mode)
```go
func run(cmd *cobra.Command, args []string) error {
	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	_, err := p.Run()
	return err
}
```
**Use when**: Demo should use alternate screen buffer (fullscreen, eyes, cellbuffer)
**Examples**: `modules/demo/fullscreen/`, `modules/demo/eyes/`

### Mouse Support
```go
p := tea.NewProgram(initialModel(), tea.WithMouseAllMotion())
```
**Use when**: Demo needs mouse tracking
**Example**: `modules/demo/mouse/`

### Focus Reporting
```go
p := tea.NewProgram(initialModel(), tea.WithReportFocus())
```
**Use when**: Demo needs to know when terminal gains/loses focus
**Example**: `modules/demo/focus-blur/`

### Input Filtering
```go
p := tea.NewProgram(initialModel(), tea.WithFilter(filterFunc))
```
**Use when**: Need to intercept/modify messages before Update()
**Example**: `modules/demo/prevent-quit/`

---

## Reference Examples (48 Available)

All 48 Bubbletea examples are in `references/bubbletea/examples/` and `modules/demo/`:

### Core Components
| Demo | Shows | Reference |
|------|-------|-----------|
| `spinner` | Animated loading | `references/bubbletea/examples/spinner` |
| `list-simple` | Selection lists | `references/bubbletea/examples/list-simple` |
| `table` | Data tables | `references/bubbletea/examples/table` |
| `textinput` | Single-line input | `references/bubbletea/examples/textinput` |
| `textarea` | Multi-line input | `references/bubbletea/examples/textarea` |
| `progress-static` | Progress bars | `references/bubbletea/examples/progress-static` |

### Advanced
| Demo | Shows | Reference |
|------|-------|-----------|
| `chat` | Textarea + Viewport | `references/bubbletea/examples/chat` |
| `file-picker` | File selection | `references/bubbletea/examples/file-picker` |
| `credit-card-form` | Complex forms | `references/bubbletea/examples/credit-card-form` |
| `split-editors` | Multiple panes | `references/bubbletea/examples/split-editors` |

**All 48 examples** are available - explore `modules/demo/` for implementations.

---

## Adapting Reference Examples

### Step-by-Step Process

**Find reference**: `references/bubbletea/examples/<component>/main.go`
**Read main() function**: This has initialization code
**Extract to initialModel()**: Move setup from main() to initialModel()
**Copy Model implementation**: Copy type definitions, Init(), Update(), View()
**Clean imports**: Remove `fmt`, `os`, `log` if unused
**Create cmd.go**: Use template above with Register() function

### Example: Adapting Spinner

**Reference**: `references/bubbletea/examples/spinner/main.go`

**Extract this from main()**:
```go
s := spinner.New()
s.Spinner = spinner.Dot
s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
return model{spinner: s}
```

**Becomes initialModel()**:
```go
func initialModel() model {
	s := spinner.New()
	s.Spinner = spinner.Dot
	s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
	return model{spinner: s}
}
```

---

## Naming Conventions

### Command Names
- **Lowercase** only
- **Hyphens** for multi-word: `list-simple`, `credit-card-form`, `altscreen-toggle`

### Package Names
- **Lowercase**, **no hyphens**
- Use underscores: `list_simple`, `credit_card_form`, `altscreen_toggle`
- Go converts hyphens automatically during import

### File Names
- `cmd.go` - Always this name (command registration)
- `<name>.go` - Main implementation (e.g., `spinner.go`, `list-simple.go`)
- Additional files: `delegate.go`, `helpers.go`, `types.go` (if needed)

---

## Checklist

### Before Implementation
- [ ] Decided: demo or utility module?
- [ ] Found reference example (if demo)
- [ ] Command name chosen (lowercase, hyphens if multi-word)

### During Implementation
- [ ] Created directory in correct location
- [ ] Created cmd.go with Register() function
- [ ] Created implementation file with initialModel()
- [ ] Package name matches conventions
- [ ] Imports are clean (no unused)

### After Implementation
- [ ] Registered in parent cmd.go init()
- [ ] Import added to parent cmd.go
- [ ] Compiles: `go build`
- [ ] Appears in help: `go run main.go --help` or `go run main.go demo --help`
- [ ] Runs: `go run main.go <command>`
- [ ] Quits cleanly with 'q' or Ctrl+C

---

## Tips

**Start with existing demos** - 48 working examples to learn from
**Copy working code** - Don't reinvent, adapt from references
**Test frequently** - Build and run after each change
**Keep it simple** - Single file until complexity demands splitting
**Use shared styles** - Import `pkg/style` for consistent theming
**Follow the pattern** - Look at 3-4 similar modules before starting

---

## Troubleshooting

### "undefined: initialModel"
- Make sure initialModel() function exists in implementation file
- Check it's exported (lowercase 'i' makes it package-private)

### "package name mismatch"
- Directory name with hyphens → package name with underscores
- Example: `list-simple/` → `package list_simple`

### "unused import"
- Remove `fmt`, `os`, `log` if not actually used
- Check your View() and Update() functions
- Common after removing main() function

### "command not showing in help"
- Verify Register() called in parent's init()
- Check import path is correct
- Run `go mod tidy`

---

## Advanced Patterns

### Multiple Files (Complex Modules)
```
modules/demo/list-fancy/
├── cmd.go           # Command registration
├── list-fancy.go    # Model and main logic
├── delegate.go      # Custom item delegate
└── randomitems.go   # Helper functions
```

### With Flags
```go
var demoType string

func Register(parent *cobra.Command) {
	cmd := &cobra.Command{
		Use:   "demo",
		Short: "Demo with flag",
		RunE:  run,
	}

	cmd.Flags().StringVarP(&demoType, "type", "t", "default", "Demo type")
	parent.AddCommand(cmd)
}

func run(cmd *cobra.Command, args []string) error {
	// Use demoType variable in initialModel()
	p := tea.NewProgram(initialModel(demoType))
	_, err := p.Run()
	return err
}
```

### With Required Args
```go
func Register(parent *cobra.Command) {
	cmd := &cobra.Command{
		Use:   "download <url>",
		Short: "Download with progress",
		Args:  cobra.ExactArgs(1),  // Require 1 argument
		RunE:  run,
	}
	parent.AddCommand(cmd)
}

func run(cmd *cobra.Command, args []string) error {
	url := args[0]
	p := tea.NewProgram(initialModel(url))
	_, err := p.Run()
	return err
}
```
