---
name: bubble-tea-expert
description: Expert in Charm's Bubble Tea TUI framework and implementation patterns
category: UI Frameworks
---

# Skill: bubble-tea-expert

## What I do

I provide Bubble Tea TUI expertise: the Elm Architecture (Model-View-Update), tea.Cmd/tea.Msg patterns, component composition, key handling, and Lip Gloss styling for terminal interfaces in Go.

## When to use me

- Building terminal user interfaces with Bubble Tea
- Implementing the Model-View-Update pattern in Go
- Composing multiple components (screens, forms, lists)
- Handling keyboard input and custom messages
- Styling TUI output with Lip Gloss

## Core principles

1. **Model-View-Update** - All state in Model, all changes via Update, all rendering in View
2. **Messages drive state** - Never mutate state directly; return new model + commands
3. **Commands for side effects** - Network, file I/O, timers go through `tea.Cmd`
4. **Compose components** - Each component has its own Model/Update/View; parent orchestrates
5. **Lip Gloss for styling** - Separate style from structure; define styles as constants

## Patterns & examples

**Basic Model-View-Update:**
```go
type model struct {
  cursor  int
  choices []string
  selected map[int]struct{}
}

func (m model) Init() tea.Cmd {
  return nil // no initial command
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
  switch msg := msg.(type) {
  case tea.KeyMsg:
    switch msg.String() {
    case "q", "ctrl+c":
      return m, tea.Quit
    case "up", "k":
      if m.cursor > 0 { m.cursor-- }
    case "down", "j":
      if m.cursor < len(m.choices)-1 { m.cursor++ }
    case "enter", " ":
      if _, ok := m.selected[m.cursor]; ok {
        delete(m.selected, m.cursor)
      } else {
        m.selected[m.cursor] = struct{}{}
      }
    }
  }
  return m, nil
}

func (m model) View() string {
  s := "Pick items:\n\n"
  for i, choice := range m.choices {
    cursor := " "
    if m.cursor == i { cursor = ">" }
    checked := " "
    if _, ok := m.selected[i]; ok { checked = "x" }
    s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
  }
  return s + "\nq to quit\n"
}
```

**Custom messages and commands:**
```go
// ✅ Correct: define domain messages
type statusMsg string
type errMsg struct{ err error }

func fetchStatus() tea.Msg {
  resp, err := http.Get("https://api.example.com/status")
  if err != nil { return errMsg{err} }
  defer resp.Body.Close()
  body, _ := io.ReadAll(resp.Body)
  return statusMsg(body)
}

// In Update:
case tea.KeyMsg:
  if msg.String() == "r" {
    return m, fetchStatus  // fire command
  }
case statusMsg:
  m.status = string(msg)
case errMsg:
  m.err = msg.err
```

**Component composition:**
```go
// ✅ Correct: parent delegates to child components
type parentModel struct {
  activeTab int
  tabs      []string
  list      listModel
  detail    detailModel
}

func (m parentModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
  switch m.activeTab {
  case 0:
    newList, cmd := m.list.Update(msg)
    m.list = newList.(listModel)
    return m, cmd
  case 1:
    newDetail, cmd := m.detail.Update(msg)
    m.detail = newDetail.(detailModel)
    return m, cmd
  }
  return m, nil
}

// ❌ Wrong: one giant Update with all logic mixed
```

**Lip Gloss styling:**
```go
var (
  titleStyle = lipgloss.NewStyle().
    Bold(true).
    Foreground(lipgloss.Color("205")).
    MarginBottom(1)

  selectedStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("170")).
    Bold(true)
)

func (m model) View() string {
  title := titleStyle.Render("My App")
  item := selectedStyle.Render(m.choices[m.cursor])
  return lipgloss.JoinVertical(lipgloss.Left, title, item)
}
```

## Anti-patterns to avoid

- ❌ Mutating model outside Update (breaks Elm Architecture)
- ❌ Side effects in View (View is pure rendering only)
- ❌ Blocking operations in Update (use `tea.Cmd` for async work)
- ❌ Monolithic Update function (decompose into component Updates)
- ❌ Hardcoded ANSI codes (use Lip Gloss styles instead)


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/UI-Frameworks/Bubble Tea Expert.md`

## Related skills

- `bubble-tea-testing` - Testing Bubble Tea applications
- `huh` - Interactive forms built on Bubble Tea
- `ui-design` - Visual hierarchy and layout principles
- `golang` - Core Go idioms used in Bubble Tea
- `vhs` - Terminal recording for TUI demos and documentation
