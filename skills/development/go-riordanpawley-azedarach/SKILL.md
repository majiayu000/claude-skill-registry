---
name: go-riordanpawley-azedarach
description: 'Purpose: Idiomatic Bubbletea patterns learned from Glow, Soft Serve,
  and community best practices'
---

# Bubbletea Patterns Skill

**Version:** 1.0
**Purpose:** Idiomatic Bubbletea patterns learned from Glow, Soft Serve, and community best practices

## Overview

Bubbletea implements the Elm Architecture:
- **Model** - Application state
- **Update** - State transitions (messages → new model, commands)
- **View** - Rendering model to terminal

**Key:** The program sends messages (tea.Msg), Update handles them, returns (newModel, optionalCmd)

## Model Architecture

### Nested Models Pattern

For non-trivial apps, use nested models with a top-level router:

```go
type Model struct {
    // Shared state accessible to all sub-models
    common *CommonModel

    // Sub-models (each implements tea.Model)
    board    *board.Model
    detail   *detail.Model
    settings *settings.Model
    overlays  *overlay.Stack

    // Current state for routing
    state State
}

type CommonModel struct {
    config  *config.Config
    width   int
    height  int
    styles  *styles.Styles
    program *tea.Program // For sending messages from goroutines
}
```

**Key insight from Glow**: Share common state via pointer to avoid duplication across sub-models.

### Init: Batch Sub-Model Initialization

```go
func (m Model) Init() tea.Cmd {
    return tea.Batch(
        m.board.Init(),
        m.detail.Init(),
        m.settings.Init(),
        loadInitialData,  // Your custom init command
    )
}
```

### Update: Message Routing Pattern

**Pass ALL messages to relevant sub-models**, not just "active" one:

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmds []tea.Cmd

    // Global handlers first (window size, quit, etc.)
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.common.width = msg.Width
        m.common.height = msg.Height
        // Propagate to all sub-models
        m.board.SetSize(msg.Width, msg.Height)
        m.detail.SetSize(msg.Width, msg.Height)
        return m, nil

    case tea.KeyMsg:
        // Handle quit regardless of state
        if msg.String() == "ctrl+c" {
            return m, tea.Quit
        }
    }

    // Route to active overlay first (if any)
    if m.overlays.Current() != nil {
        overlay, cmd := m.overlays.Current().Update(msg)
        m.overlays.SetCurrent(overlay)
        if cmd != nil {
            cmds = append(cmds, cmd)
        }
        // Overlays may consume the message
        if m.overlays.Current() != nil {
            return m, tea.Batch(cmds...)
        }
    }

    // Route to current view
    switch m.state {
    case StateBoard:
        newBoard, cmd := m.board.Update(msg)
        m.board = newBoard.(*board.Model)
        cmds = append(cmds, cmd)
    case StateDetail:
        newDetail, cmd := m.detail.Update(msg)
        m.detail = newDetail.(*detail.Model)
        cmds = append(cmds, cmd)
    }

    return m, tea.Batch(cmds...)
}
```

## Commands

### tea.Cmd Types

```go
// Command returning a message
func fetchTasks() tea.Cmd {
    return func() tea.Msg {
        return TasksLoadedMsg{tasks: getTasks()}
    }
}

// Command with timeout
func fetchWithTimeout() tea.Cmd {
    return tea.Tick(time.Second, func(t time.Time) tea.Msg {
        return TimeoutMsg{}
    })
}

// Command from goroutine
func asyncWork() tea.Cmd {
    ch := make(chan tea.Msg)
    go func() {
        defer close(ch)
        ch <- WorkDoneMsg{result: doWork()}
    }()
    return func() tea.Msg {
        return <-ch
    }
}

// Batch commands
func (m Model) Init() tea.Cmd {
    return tea.Batch(
        m.board.Init(),
        m.detail.Init(),
        tea.Tick(time.Second, tickerTick),  // Periodic
    )
}
```

### Sending Messages from Goroutines

```go
// In goroutine, send via program
func (s *Service) pollState(program *tea.Program) {
    for {
        time.Sleep(500 * time.Millisecond)
        state := s.checkState()
        program.Send(StateChangedMsg{state: state})
    }
}

// In model Update, handle the message
case StateChangedMsg msg:
    // Handle state change
```

## View Pattern

### Delegated Views

```go
func (m Model) View() string {
    switch m.state {
    case StateBoard:
        return m.board.View()
    case StateDetail:
        return m.detail.View()
    case StateSettings:
        return m.settings.View()
    default:
        return ""
    }
}
```

### Styled Views (Lip Gloss)

```go
var (
    // Define styles once (avoid reallocation in View())
    baseStyle   = lipgloss.NewStyle()
    titleStyle  = baseStyle.Bold(true).Foreground(lipgloss.Color("205"))
    activeStyle = baseStyle.Background(lipgloss.Color("240"))
)

func (m Model) View() string {
    return lipgloss.NewStyle().
        Width(m.common.width).
        Height(m.common.height).
        Render(
            lipgloss.Place(
                m.common.width, m.common.height,
                lipgloss.Center, lipgloss.Center,
                m.content.View(),
            ),
        )
}
```

### Border Styles

```go
var (
    boxStyle = lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("63")).
        Padding(1, 2)
)

func (m Model) View() string {
    return boxStyle.Render(m.content)
}
```

## State Management

### Simple State Enum

```go
type State int

const (
    StateBoard State = iota
    StateDetail
    StateSettings
)
```

### State with Data

```go
type State struct {
    view ViewType
    selectedItem int
    isLoading   bool
}
```

## Message Types

### Custom Messages

```go
// Define custom message types (avoid collisions)
type TaskSelectedMsg struct {
    id string
}

type TasksLoadedMsg struct {
    tasks []Task
}

type StateChangedMsg struct {
    state SessionState
}
```

### Built-in Messages

| Message | Description |
|----------|-------------|
| `tea.InitMsg` | Program started (return initial cmd) |
| `tea.QuitMsg` | Request program exit |
| `tea.WindowSizeMsg` | Terminal size changed |
| `tea.KeyMsg` | Key press event |
| `tea.MouseMsg` | Mouse event (enable with tea.WithMouseCellMotion()) |
| `tea.TickMsg` | Timer event (from tea.Tick) |

## Keyboard Patterns

### Key Matching

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit
        case "up", "k":
            m.cursor--
        case "down", "j":
            m.cursor++
        case "enter":
            return m, m.selectCurrent()
        }
    }
    return m, nil
}
```

### Key Types

```go
case tea.KeyMsg:
    switch msg.Type {
    case tea.KeyRunes:
        // Any character key (letters, numbers, etc.)
    case tea.KeyEnter, tea.KeySpace:
        // Enter or Space
    case tea.KeyUp, tea.KeyDown, tea.KeyLeft, tea.KeyRight:
        // Arrow keys
    case tea.KeyCtrlC, tea.KeyCtrlD:
        // Ctrl combinations
    }
```

### Alt/Modifer Keys

```go
case tea.KeyMsg:
    if msg.Alt {
        // Alt+key
    }
```

## Component Patterns

### Using Bubbles

```go
import (
    "github.com/charmbracelet/bubbles/list"
    "github.com/charmbracelet/bubbles/textinput"
    "github.com/charmbracelet/bubbles/viewport"
)

type Model struct {
    list    list.Model
    input   textinput.Model
    content viewport.Model
}

func (m Model) Init() tea.Cmd {
    m.list = list.New(..., list.NewDefaultDelegate())
    m.input = textinput.New()
    m.content = viewport.New(0, 0)
    return nil
}
```

### Focus Management

```go
type Model struct {
    focused focusedComponent
}

type focusedComponent int

const (
    focusList focusedComponent = iota
    focusInput
)

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "tab" {
            // Cycle focus
            m.focused = (m.focused + 1) % 2
        }
    }

    // Update based on focus
    switch m.focused {
    case focusList:
        var cmd tea.Cmd
        m.list, cmd = m.list.Update(msg)
        return m, cmd
    case focusInput:
        var cmd tea.Cmd
        m.input, cmd = m.input.Update(msg)
        return m, cmd
    }
}
```

## Performance Patterns

### View Memoization

```go
// ❌ BAD: Reallocates styles every render
func (m Model) View() string {
    return lipgloss.NewStyle().
        Bold(true).
        Render("Title")
}

// ✅ GOOD: Styles defined once
var titleStyle = lipgloss.NewStyle().Bold(true)

func (m Model) View() string {
    return titleStyle.Render("Title")
}
```

### View Optimization

```go
// ❌ BAD: Renders entire content every frame
func (m Model) View() string {
    return m.content
}

// ✅ GOOD: Only render what changed
func (m Model) View() string {
    if m.needsRender {
        m.needsRender = false
        return m.content
    }
    return ""  // Skip rendering
}
```

## Common Patterns

### Confirmation Dialog

```go
type ConfirmModel struct {
    question string
    confirmed bool
}

func (m ConfirmModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "y" {
            m.confirmed = true
            return m, tea.Quit
        }
        if msg.String() == "n" || msg.String() == "esc" {
            return m, tea.Quit
        }
    }
    return m, nil
}

func (m ConfirmModel) View() string {
    return fmt.Sprintf("%s [y/n]", m.question)
}
```

### Loading State

```go
type Model struct {
    loading bool
    content string
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case LoadStartMsg:
        m.loading = true
    case LoadDoneMsg:
        m.loading = false
        m.content = msg.data
    }
    return m, nil
}

func (m Model) View() string {
    if m.loading {
        return "Loading..."
    }
    return m.content
}
```

### Error Handling

```go
type Model struct {
    err error
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case errMsg:
        m.err = msg.err
    }
    return m, nil
}

func (m Model) View() string {
    if m.err != nil {
        return lipgloss.NewStyle().
            Foreground(lipgloss.Color("196")).
            Render(fmt.Sprintf("Error: %v", m.err))
    }
    return m.content
}
```

## Best Practices

1. **Define styles once** as package-level variables (avoid View() reallocation)
2. **Pass context** to goroutines and check for cancellation
3. **Use tea.Batch** to combine multiple commands
4. **Handle tea.WindowSizeMsg** to respond to terminal resizes
5. **Type switch on messages** (not fmt.Sprintf, slower)
6. **Keep View() pure** - no side effects, just render state
7. **Use bubbles components** for lists, inputs, viewports
8. **Close channels** from sender side only
9. **Use tea.Quit** to exit gracefully
10. **Test with different terminal sizes** for responsive layouts

## References

- [Bubbletea Tutorial](https://github.com/charmbracelet/bubbletea/tree/master/tutorials)
- [Bubbletea Examples](https://github.com/charmbracelet/bubbletea/tree/master/examples)
- [Lip Gloss Documentation](https://github.com/charmbracelet/lipgloss)
- [Bubbles Components](https://github.com/charmbracelet/bubbles)
- [Glow Source](https://github.com/charmbracelet/glow) - Production patterns
- [Soft Serve Source](https://github.com/charmbracelet/soft-serve) - Production patterns
