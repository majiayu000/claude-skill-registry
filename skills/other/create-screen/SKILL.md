---
name: create-screen
description: Create a new screen component following naming conventions and architecture
category: Workflow Orchestration
---

# Skill: create-screen

## What I do

I guide creating screen components in the KaRiya TUI architecture: Bubble Tea models that render UI, handle user input, and delegate to behaviours. Screens are the view layer.

## When to use me

- Building a new UI view (list, detail, form)
- Creating a reusable screen component
- Implementing user input handling
- Adding a new screen type to an intent

## Core principles

1. **Screens render** - View() returns the string to display, nothing more
2. **Behaviours reuse** - Extract common interaction patterns into behaviours
3. **Intent owns state** - Screens receive data, don't fetch it
4. **Composition over inheritance** - Combine behaviours, don't subclass screens
5. **Naming convention** - `<entity>_<type>_screen.go`: `event_list_screen.go`

## Screen types and structure

```
SCREEN TYPES
  ListScreen    - Table/list of items (uses TableBehavior)
  DetailScreen  - Single item view
  FormScreen    - Input form (uses huh forms)
  ConfirmScreen - Yes/No confirmation

DIRECTORY
internal/cli/screens/<feature>/
    list_screen.go           # List view
    list_screen_test.go      # View + update tests
    detail_screen.go         # Detail view
    detail_screen_test.go
```

## Patterns & examples

**List screen with table behaviour:**
```go
package timeline

import (
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type ListScreen struct {
    table    *behaviors.TableBehavior
    events   []career.Event
    width    int
    height   int
}

func NewListScreen(events []career.Event) *ListScreen {
    columns := []behaviors.Column{
        {Title: "Date", Width: 12},
        {Title: "Title", Width: 30},
        {Title: "Company", Width: 20},
    }

    rows := make([]behaviors.Row, len(events))
    for i, e := range events {
        rows[i] = behaviors.Row{
            e.Date.Format("2006-01-02"),
            e.Title,
            e.Company,
        }
    }

    return &ListScreen{
        table:  behaviors.NewTable(columns, rows),
        events: events,
    }
}

func (s *ListScreen) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "enter":
            idx := s.table.SelectedIndex()
            return s, SelectEvent(s.events[idx])
        case "q":
            return s, tea.Quit
        }
    case tea.WindowSizeMsg:
        s.width = msg.Width
        s.height = msg.Height
    }
    var cmd tea.Cmd
    s.table, cmd = s.table.Update(msg)
    return s, cmd
}

func (s *ListScreen) View() string {
    return s.table.View()
}
```

**Form screen with huh:**
```go
type FormScreen struct {
    form *huh.Form
    data *FormData
}

func NewFormScreen(theme *huh.Theme) *FormScreen {
    data := &FormData{}
    form := huh.NewForm(
        huh.NewGroup(
            huh.NewInput().Title("Title").Value(&data.Title),
            huh.NewInput().Title("Company").Value(&data.Company),
        ),
    ).WithTheme(theme)

    return &FormScreen{form: form, data: data}
}
```

**Testing screens:**
```go
Describe("ListScreen", func() {
    var screen *ListScreen

    BeforeEach(func() {
        events := []career.Event{
            fixtures.NewEvent().WithTitle("Dev").Build(),
        }
        screen = NewListScreen(events)
    })

    It("renders event titles", func() {
        Expect(screen.View()).To(ContainSubstring("Dev"))
    })

    It("handles selection", func() {
        _, cmd := screen.Update(tea.KeyMsg{Type: tea.KeyEnter})
        Expect(cmd).NotTo(BeNil())
    })
})
```

## Anti-patterns to avoid

- ❌ Fetching data in the screen (screens receive data, don't query)
- ❌ Business logic in Update() (delegate to intent or service)
- ❌ Duplicating table/form logic (use behaviours)
- ❌ Hardcoded dimensions (respond to WindowSizeMsg)
- ❌ Skipping View() tests (rendering bugs are real)


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/UI-Frameworks/Create Screen.md`

## Related skills

- `create-intent` - Intents that own and display screens
- `bubble-tea-expert` - Bubble Tea framework patterns
- `huh` - Form library for input screens
- `ui-design` - Visual hierarchy and layout
- `bubble-tea-testing` - Testing TUI components
