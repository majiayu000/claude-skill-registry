---
name: bubbletea-code-review
description: Reviews BubbleTea TUI code for proper Elm architecture, model/update/view patterns, and Lipgloss styling. Use when reviewing terminal UI code using charmbracelet/bubbletea.
---

# BubbleTea Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Elm architecture, tea.Cmd as data | [references/elm-architecture.md](references/elm-architecture.md) |
| Model state, message handling | [references/model-update.md](references/model-update.md) |
| View rendering, Lipgloss styling | [references/view-styling.md](references/view-styling.md) |
| Component composition, Huh forms | [references/composition.md](references/composition.md) |
| Bubbles components (list, table, etc.) | [references/bubbles-components.md](references/bubbles-components.md) |

## CRITICAL: Avoid False Positives

**Read [elm-architecture.md](references/elm-architecture.md) first!** The most common review mistake is flagging correct patterns as bugs.

### NOT Issues (Do NOT Flag These)

| Pattern | Why It's Correct |
|---------|------------------|
| `return m, m.loadData()` | `tea.Cmd` is returned immediately; runtime executes async |
| Value receiver on `Update()` | Standard BubbleTea pattern; model returned by value |
| Nested `m.child, cmd = m.child.Update(msg)` | Normal component composition |
| Helper functions returning `tea.Cmd` | Creates command descriptor, no I/O in Update |
| `tea.Batch(cmd1, cmd2)` | Commands execute concurrently by runtime |

### ACTUAL Issues (DO Flag These)

| Pattern | Why It's Wrong |
|---------|----------------|
| `os.ReadFile()` in Update | Blocks UI thread |
| `http.Get()` in Update | Network I/O blocks |
| `time.Sleep()` in Update | Freezes UI |
| `<-channel` in Update (blocking) | May block indefinitely |
| `huh.Form.Run()` in Update | Blocking call |

## Review Checklist

### Architecture
- [ ] **No blocking I/O in Update()** (file, network, sleep)
- [ ] Helper functions returning `tea.Cmd` are NOT flagged as blocking
- [ ] Commands used for all async operations

### Model & Update
- [ ] Model is immutable (Update returns new model, not mutates)
- [ ] Init returns proper initial command (or nil)
- [ ] Update handles all expected message types
- [ ] WindowSizeMsg handled for responsive layout
- [ ] tea.Batch used for multiple commands
- [ ] tea.Quit used correctly for exit

### View & Styling
- [ ] View is a pure function (no side effects)
- [ ] Lipgloss styles defined once, not in View
- [ ] Key bindings use key.Matches with help.KeyMap

### Components
- [ ] Sub-component updates propagated correctly
- [ ] Bubbles components initialized with dimensions
- [ ] Huh forms embedded via Update loop (not Run())

## Critical Patterns

### Model Must Be Immutable

```go
// BAD - mutates model
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    m.items = append(m.items, newItem)  // mutation!
    return m, nil
}

// GOOD - returns new model
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    newItems := make([]Item, len(m.items)+1)
    copy(newItems, m.items)
    newItems[len(m.items)] = newItem
    m.items = newItems
    return m, nil
}
```

### Commands for Async/IO

```go
// BAD - blocking in Update
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    data, _ := os.ReadFile("config.json")  // blocks UI!
    m.config = parse(data)
    return m, nil
}

// GOOD - use commands
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    return m, loadConfigCmd()
}

func loadConfigCmd() tea.Cmd {
    return func() tea.Msg {
        data, err := os.ReadFile("config.json")
        if err != nil {
            return errMsg{err}
        }
        return configLoadedMsg{parse(data)}
    }
}
```

### Styles Defined Once

```go
// BAD - creates new style each render
func (m Model) View() string {
    style := lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("205"))
    return style.Render("Hello")
}

// GOOD - define styles at package level or in model
var titleStyle = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("205"))

func (m Model) View() string {
    return titleStyle.Render("Hello")
}
```

## When to Load References

- **First time reviewing BubbleTea** → [elm-architecture.md](references/elm-architecture.md) (prevents false positives)
- Reviewing Update function logic → [model-update.md](references/model-update.md)
- Reviewing View function, styling → [view-styling.md](references/view-styling.md)
- Reviewing component hierarchy → [composition.md](references/composition.md)
- Using Bubbles components → [bubbles-components.md](references/bubbles-components.md)

## Review Questions

1. Is Update() free of blocking I/O? (NOT: "is the cmd helper blocking?")
2. Is the model immutable in Update?
3. Are Lipgloss styles defined once, not in View?
4. Is WindowSizeMsg handled for resizing?
5. Are key bindings documented with help.KeyMap?
6. Are Bubbles components sized correctly?
