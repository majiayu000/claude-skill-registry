---
name: charm-stack
description: Build terminal UIs with Bubbletea, Bubbles, Lipgloss, and Huh. Use when creating TUI applications, interactive forms, styled terminal output, or when user mentions Bubbletea, Bubbles, Lipgloss, Huh, Charm, or TUI development.
---

# Charm Stack TUI Development

Build beautiful, functional terminal user interfaces using the Charm stack: Bubbletea (framework), Bubbles (components), Lipgloss (styling), and Huh (forms).

## Your Role: TUI Architect

You build terminal applications using Elm Architecture patterns. You:

✅ **Implement Model-Update-View** - Core Bubbletea pattern
✅ **Compose Bubbles components** - Spinners, lists, text inputs
✅ **Style with Lipgloss** - Colors, borders, layouts
✅ **Build forms with Huh** - Interactive prompts
✅ **Handle messages properly** - KeyMsg, WindowMsg, custom messages
✅ **Follow project patterns** - Module structure from CLY

❌ **Do NOT fight the framework** - Use Elm Architecture
❌ **Do NOT skip Init** - Commands need initialization
❌ **Do NOT ignore tea.Cmd** - Critical for async operations

## Core Architecture: The Elm Architecture

### The Three Functions

Every Bubbletea program has three parts:

**Model** - Application state
```go
type model struct {
    cursor   int
    choices  []string
    selected map[int]struct{}
}
```

**Init** - Initial command
```go
func (m model) Init() tea.Cmd {
    return nil  // or return a command
}
```

**Update** - Handle messages, update state
```go
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        // Handle keyboard
    }
    return m, nil
}
```

**View** - Render UI
```go
func (m model) View() string {
    return "Hello, World!"
}
```

### Message Flow

```
User Input → Msg → Update → Model → View → Screen
    ↑                                    ↓
    └────────── tea.Cmd ─────────────────┘
```

**Key concepts:**
- Messages are immutable events
- Update returns new model (don't mutate)
- Commands run async, generate more messages
- View is pure function of model state

## Bubbletea Patterns

### Basic Program

```go
package main

import (
    "fmt"
    "os"

    tea "github.com/charmbracelet/bubbletea"
)

type model struct {
    choices  []string
    cursor   int
    selected map[int]struct{}
}

func initialModel() model {
    return model{
        choices:  []string{"Buy carrots", "Buy celery", "Buy kohlrabi"},
        selected: make(map[int]struct{}),
    }
}

func (m model) Init() tea.Cmd {
    return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "up", "k":
            if m.cursor > 0 {
                m.cursor--
            }

        case "down", "j":
            if m.cursor < len(m.choices)-1 {
                m.cursor++
            }

        case "enter", " ":
            _, ok := m.selected[m.cursor]
            if ok {
                delete(m.selected, m.cursor)
            } else {
                m.selected[m.cursor] = struct{}{}
            }
        }
    }
    return m, nil
}

func (m model) View() string {
    s := "What should we buy?\n\n"

    for i, choice := range m.choices {
        cursor := " "
        if m.cursor == i {
            cursor = ">"
        }

        checked := " "
        if _, ok := m.selected[i]; ok {
            checked = "x"
        }

        s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
    }

    s += "\nPress q to quit.\n"
    return s
}

func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
        os.Exit(1)
    }
}
```

### Commands (tea.Cmd)

Commands enable async operations. They return messages.

**Simple command:**
```go
func checkServer() tea.Msg {
    // Do work
    return statusMsg{online: true}
}

// In Update:
case tea.KeyMsg:
    if msg.String() == "c" {
        return m, checkServer  // Execute command
    }
```

**Command that runs async:**
```go
func fetchData() tea.Cmd {
    return func() tea.Msg {
        resp, err := http.Get("https://api.example.com/data")
        if err != nil {
            return errMsg{err}
        }
        return dataMsg{resp}
    }
}
```

**Batch commands:**
```go
return m, tea.Batch(
    cmd1,
    cmd2,
    cmd3,
)
```

**Tick command (for animations):**
```go
type tickMsg time.Time

func tick() tea.Cmd {
    return tea.Tick(time.Second, func(t time.Time) tea.Msg {
        return tickMsg(t)
    })
}

// In Init:
func (m model) Init() tea.Cmd {
    return tick()
}

// In Update:
case tickMsg:
    m.lastTick = time.Time(msg)
    return m, tick()  // Keep ticking
```

### Window Size Handling

```go
type model struct {
    width  int
    height int
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.width = msg.Width
        m.height = msg.Height
        return m, nil
    }
    return m, nil
}

func (m model) View() string {
    return lipgloss.Place(
        m.width,
        m.height,
        lipgloss.Center,
        lipgloss.Center,
        "Centered text",
    )
}
```

### Program Options

```go
p := tea.NewProgram(
    initialModel(),
    tea.WithAltScreen(),       // Use alternate screen buffer
    tea.WithMouseCellMotion(), // Enable mouse
)
```

## Bubbles Components

Bubbles provides ready-made components. Each is a tea.Model.

### Spinner

```go
import "github.com/charmbracelet/bubbles/spinner"

type model struct {
    spinner spinner.Model
}

func initialModel() model {
    s := spinner.New()
    s.Spinner = spinner.Dot
    s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
    return model{spinner: s}
}

func (m model) Init() tea.Cmd {
    return m.spinner.Tick
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    m.spinner, cmd = m.spinner.Update(msg)
    return m, cmd
}

func (m model) View() string {
    return m.spinner.View() + " Loading..."
}
```

**Spinner types:**
- `spinner.Line`
- `spinner.Dot`
- `spinner.MiniDot`
- `spinner.Jump`
- `spinner.Pulse`
- `spinner.Points`
- `spinner.Globe`
- `spinner.Moon`

### Text Input

```go
import "github.com/charmbracelet/bubbles/textinput"

type model struct {
    textInput textinput.Model
}

func initialModel() model {
    ti := textinput.New()
    ti.Placeholder = "Enter your name"
    ti.Focus()
    ti.CharLimit = 156
    ti.Width = 20

    return model{textInput: ti}
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "enter":
            name := m.textInput.Value()
            // Use the name
            return m, tea.Quit
        }
    }

    m.textInput, cmd = m.textInput.Update(msg)
    return m, cmd
}

func (m model) View() string {
    return fmt.Sprintf(
        "What's your name?\n\n%s\n\n%s",
        m.textInput.View(),
        "(esc to quit)",
    )
}
```

### List

```go
import "github.com/charmbracelet/bubbles/list"

type item struct {
    title, desc string
}

func (i item) Title() string       { return i.title }
func (i item) Description() string { return i.desc }
func (i item) FilterValue() string { return i.title }

type model struct {
    list list.Model
}

func initialModel() model {
    items := []list.Item{
        item{title: "Raspberry Pi", desc: "A small computer"},
        item{title: "Arduino", desc: "Microcontroller"},
        item{title: "ESP32", desc: "WiFi & Bluetooth"},
    }

    l := list.New(items, list.NewDefaultDelegate(), 0, 0)
    l.Title = "Hardware"

    return model{list: l}
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.list.SetSize(msg.Width, msg.Height)

    case tea.KeyMsg:
        if msg.String() == "enter" {
            selected := m.list.SelectedItem().(item)
            // Use selected
        }
    }

    var cmd tea.Cmd
    m.list, cmd = m.list.Update(msg)
    return m, cmd
}
```

### Table

```go
import "github.com/charmbracelet/bubbles/table"

func initialModel() model {
    columns := []table.Column{
        {Title: "ID", Width: 4},
        {Title: "Name", Width: 10},
        {Title: "Status", Width: 10},
    }

    rows := []table.Row{
        {"1", "Alice", "Active"},
        {"2", "Bob", "Inactive"},
    }

    t := table.New(
        table.WithColumns(columns),
        table.WithRows(rows),
        table.WithFocused(true),
        table.WithHeight(7),
    )

    s := table.DefaultStyles()
    s.Header = s.Header.
        BorderStyle(lipgloss.NormalBorder()).
        BorderForeground(lipgloss.Color("240"))
    t.SetStyles(s)

    return model{table: t}
}
```

### Viewport (Scrolling)

```go
import "github.com/charmbracelet/bubbles/viewport"

type model struct {
    viewport viewport.Model
    content  string
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.viewport = viewport.New(msg.Width, msg.Height)
        m.viewport.SetContent(m.content)
    }

    var cmd tea.Cmd
    m.viewport, cmd = m.viewport.Update(msg)
    return m, cmd
}

func (m model) View() string {
    return m.viewport.View()
}
```

### Progress

```go
import "github.com/charmbracelet/bubbles/progress"

type model struct {
    progress progress.Model
    percent  float64
}

func initialModel() model {
    return model{
        progress: progress.New(progress.WithDefaultGradient()),
        percent:  0.0,
    }
}

func (m model) View() string {
    return "\n" + m.progress.ViewAs(m.percent) + "\n\n"
}
```

## Lipgloss Styling

### Basic Styles

```go
import "github.com/charmbracelet/lipgloss"

var (
    // Define styles
    titleStyle = lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("170")).
        Background(lipgloss.Color("235")).
        Padding(0, 1)

    errorStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true)

    successStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("42"))
)

// Use styles
title := titleStyle.Render("Hello")
err := errorStyle.Render("Error!")
```

### Colors

```go
// ANSI 16 colors
lipgloss.Color("5")      // magenta

// ANSI 256 colors
lipgloss.Color("86")     // aqua
lipgloss.Color("201")    // hot pink

// True color (hex)
lipgloss.Color("#0000FF") // blue
lipgloss.Color("#FF6B6B") // red

// Adaptive (light/dark)
lipgloss.AdaptiveColor{
    Light: "236",
    Dark:  "248",
}
```

### Layout & Spacing

```go
style := lipgloss.NewStyle().
    Width(50).
    Height(10).
    Padding(1, 2).       // top/bottom, left/right
    Margin(1, 2, 3, 4).  // top, right, bottom, left
    Align(lipgloss.Center)
```

### Borders

```go
style := lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(lipgloss.Color("63")).
    Padding(1, 2)

// Border types
lipgloss.NormalBorder()
lipgloss.RoundedBorder()
lipgloss.ThickBorder()
lipgloss.DoubleBorder()
lipgloss.HiddenBorder()

// Selective borders
style.BorderTop(true).
    BorderLeft(true)
```

### Joining Layouts

```go
// Horizontal
row := lipgloss.JoinHorizontal(
    lipgloss.Top,     // Alignment
    box1, box2, box3,
)

// Vertical
col := lipgloss.JoinVertical(
    lipgloss.Left,
    box1, box2, box3,
)

// Positions: Top, Center, Bottom, Left, Right
```

### Positioning

```go
// Place in whitespace
centered := lipgloss.Place(
    width, height,
    lipgloss.Center,    // horizontal
    lipgloss.Center,    // vertical
    content,
)
```

### Advanced Styling

```go
style := lipgloss.NewStyle().
    Bold(true).
    Italic(true).
    Underline(true).
    Strikethrough(true).
    Blink(true).
    Faint(true).
    Reverse(true)
```

## Huh Forms

Build interactive forms and prompts.

### Basic Form

```go
import "github.com/charmbracelet/huh"

var (
    burger   string
    toppings []string
    name     string
)

func runForm() error {
    form := huh.NewForm(
        huh.NewGroup(
            huh.NewSelect[string]().
                Title("Choose your burger").
                Options(
                    huh.NewOption("Classic", "classic"),
                    huh.NewOption("Chicken", "chicken"),
                    huh.NewOption("Veggie", "veggie"),
                ).
                Value(&burger),

            huh.NewMultiSelect[string]().
                Title("Toppings").
                Options(
                    huh.NewOption("Lettuce", "lettuce"),
                    huh.NewOption("Tomato", "tomato"),
                    huh.NewOption("Cheese", "cheese"),
                ).
                Limit(3).
                Value(&toppings),
        ),

        huh.NewGroup(
            huh.NewInput().
                Title("What's your name?").
                Value(&name).
                Validate(func(s string) error {
                    if s == "" {
                        return fmt.Errorf("name required")
                    }
                    return nil
                }),
        ),
    )

    return form.Run()
}
```

### Field Types

**Input** - Single line text:
```go
huh.NewInput().
    Title("Username").
    Placeholder("Enter username").
    Value(&username)
```

**Text** - Multi-line text:
```go
huh.NewText().
    Title("Description").
    CharLimit(400).
    Value(&description)
```

**Select** - Choose one:
```go
huh.NewSelect[string]().
    Title("Pick one").
    Options(
        huh.NewOption("Option 1", "opt1"),
        huh.NewOption("Option 2", "opt2"),
    ).
    Value(&choice)
```

**MultiSelect** - Choose multiple:
```go
huh.NewMultiSelect[string]().
    Title("Pick several").
    Options(...).
    Limit(3).
    Value(&choices)
```

**Confirm** - Yes/No:
```go
huh.NewConfirm().
    Title("Are you sure?").
    Affirmative("Yes").
    Negative("No").
    Value(&confirmed)
```

### Accessible Mode

```go
form := huh.NewForm(...)
form.WithAccessible(true)  // Screen reader friendly
```

### In Bubble Tea

```go
type model struct {
    form *huh.Form
}

func (m model) Init() tea.Cmd {
    return m.form.Init()
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    form, cmd := m.form.Update(msg)
    if f, ok := form.(*huh.Form); ok {
        m.form = f
    }

    if m.form.State == huh.StateCompleted {
        // Form done, get values
        return m, tea.Quit
    }

    return m, cmd
}

func (m model) View() string {
    if m.form.State == huh.StateCompleted {
        return "Done!\n"
    }
    return m.form.View()
}
```

## CLY Project Patterns

### Module Structure

```
modules/demo/spinner/
├── cmd.go        # Register() and run()
└── spinner.go    # Bubbletea model
```

**cmd.go:**
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

**spinner.go:**
```go
package spinner

import (
    "github.com/charmbracelet/bubbles/spinner"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type model struct {
    spinner spinner.Model
}

func initialModel() model {
    s := spinner.New()
    s.Spinner = spinner.Dot
    s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
    return model{spinner: s}
}

func (m model) Init() tea.Cmd {
    return m.spinner.Tick
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "q" {
            return m, tea.Quit
        }
    }

    var cmd tea.Cmd
    m.spinner, cmd = m.spinner.Update(msg)
    return m, cmd
}

func (m model) View() string {
    return m.spinner.View() + " Loading...\n"
}
```

## Common Patterns

### Loading State

```go
type model struct {
    loading bool
    spinner spinner.Model
    data    []string
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "r" {
            m.loading = true
            return m, fetchData
        }

    case dataMsg:
        m.loading = false
        m.data = msg.data
        return m, nil
    }

    if m.loading {
        var cmd tea.Cmd
        m.spinner, cmd = m.spinner.Update(msg)
        return m, cmd
    }

    return m, nil
}

func (m model) View() string {
    if m.loading {
        return m.spinner.View() + " Loading data..."
    }
    return renderData(m.data)
}
```

### Error Handling

```go
type model struct {
    err error
}

type errMsg struct{ err error }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case errMsg:
        m.err = msg.err
        return m, nil
    }
    return m, nil
}

func (m model) View() string {
    if m.err != nil {
        return errorStyle.Render("Error: " + m.err.Error())
    }
    return normalView()
}
```

### Multi-View Navigation

```go
type view int

const (
    viewMenu view = iota
    viewList
    viewDetail
)

type model struct {
    currentView view
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "1":
            m.currentView = viewMenu
        case "2":
            m.currentView = viewList
        case "3":
            m.currentView = viewDetail
        }
    }
    return m, nil
}

func (m model) View() string {
    switch m.currentView {
    case viewMenu:
        return renderMenu()
    case viewList:
        return renderList()
    case viewDetail:
        return renderDetail()
    }
    return ""
}
```

## Best Practices

### Model Immutability

**✅ GOOD - Return new state:**
```go
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    m.counter++  // Modify copy
    return m, nil
}
```

**❌ BAD - Mutate pointer:**
```go
func (m *model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    m.counter++  // Mutates original
    return m, nil
}
```

### Quit Handling

Always handle quit signals:
```go
case tea.KeyMsg:
    switch msg.String() {
    case "ctrl+c", "q", "esc":
        return m, tea.Quit
    }
```

### Alt Screen

Use alt screen for full-screen apps:
```go
p := tea.NewProgram(
    initialModel(),
    tea.WithAltScreen(),
)
```

### Component Composition

Embed Bubbles components:
```go
type model struct {
    spinner   spinner.Model
    textInput textinput.Model
    list      list.Model
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmds []tea.Cmd
    var cmd tea.Cmd

    m.spinner, cmd = m.spinner.Update(msg)
    cmds = append(cmds, cmd)

    m.textInput, cmd = m.textInput.Update(msg)
    cmds = append(cmds, cmd)

    return m, tea.Batch(cmds...)
}
```

## Checklist

- [ ] Model contains all state
- [ ] Init returns initial command
- [ ] Update handles all message types
- [ ] Update returns new model (immutable)
- [ ] View is pure function
- [ ] Quit handling present
- [ ] Window resize handled
- [ ] Commands for async ops
- [ ] Bubbles components updated
- [ ] Lipgloss for all styling
- [ ] Follows CLY module structure

## Resources

- [Bubbletea Tutorial](https://github.com/charmbracelet/bubbletea/tree/main/tutorials)
- [Bubbletea Examples](https://github.com/charmbracelet/bubbletea/tree/main/examples)
- [Bubbles Components](https://github.com/charmbracelet/bubbles)
- [Lipgloss Docs](https://github.com/charmbracelet/lipgloss)
- [Huh Forms](https://github.com/charmbracelet/huh)
- CLY examples: `modules/demo/*/`
