---
name: building-glamorous-tuis
description: >-
  Build beautiful terminal UIs with Charmbracelet. For SHELL/BASH scripts: use
  Gum (prompts, spinners, selection), VHS (recording), Mods (AI), Freeze
  (screenshots), Glow (markdown). For GO applications: use Bubble Tea
  (framework), Bubbles (components), Lip Gloss (styling), Huh (forms), Glamour
  (markdown), Harmonica (animation). For INFRASTRUCTURE: Wish (SSH apps), Soft
  Serve (Git), teatest (testing). Trigger on: shell scripts needing UI, Go CLI
  tools, terminal dashboards, SSH applications, or "make this CLI prettier."
---

# Building Glamorous TUIs with Charmbracelet

## Quick Router

**What are you building?**

| Context | Solution | Reference |
|---------|----------|-----------|
| **Shell/Bash script** | Gum, VHS, Mods, Freeze | [→ Shell Scripts](#for-shell-scripts) |
| **Go CLI/TUI** | Bubble Tea + Lip Gloss | [→ Go TUI](#for-go-applications) |
| **SSH-accessible app** | Wish + Bubble Tea | [→ Infrastructure](#for-infrastructure) |
| **Recording demos** | VHS | [→ Shell Scripts](#vhs-quick-start) |
| **Testing TUIs** | teatest | [→ Infrastructure](#for-infrastructure) |

---

## For Shell Scripts

**No Go required.** Gum gives you all the UI primitives.

```bash
brew install gum
```

### Essential Gum Commands

```bash
# Input
NAME=$(gum input --placeholder "Your name")

# Selection (single)
COLOR=$(gum choose "red" "green" "blue")

# Selection (multi)
ITEMS=$(gum choose --no-limit "a" "b" "c")

# Fuzzy filter (from stdin)
BRANCH=$(git branch | gum filter)

# Confirmation
gum confirm "Continue?" && echo "yes"

# Spinner
gum spin --title "Working..." -- long-command

# Styled output
gum style --border rounded --padding "1 2" "Hello"

# File picker
FILE=$(gum file .)
```

### Quick Recipe: Git Commit

```bash
TYPE=$(gum choose "feat" "fix" "docs" "refactor")
MSG=$(gum input --placeholder "commit message")
gum confirm "Commit?" && git commit -m "$TYPE: $MSG"
```

### VHS Quick Start

Record terminal → GIF:

```bash
brew install vhs

cat > demo.tape << 'EOF'
Output demo.gif
Set Theme "Catppuccin Mocha"
Type "echo hello"
Enter
Sleep 1s
EOF

vhs demo.tape
```

### Other Shell Tools

| Tool | Install | One-liner |
|------|---------|-----------|
| **Mods** | `brew install mods` | `git diff \| mods "review this"` |
| **Glow** | `brew install glow` | `glow README.md` |
| **Freeze** | `brew install freeze` | `freeze code.go -o screenshot.png` |

**[Full Shell Reference →](references/shell-scripts.md)**

---

## For Go Applications

### Instant Start

```bash
go get github.com/charmbracelet/bubbletea \
       github.com/charmbracelet/lipgloss
```

### Minimal TUI (Copy & Run)

```go
package main

import (
    "fmt"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

var highlight = lipgloss.NewStyle().Foreground(lipgloss.Color("212")).Bold(true)

type model struct {
    items  []string
    cursor int
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        case "up", "k":
            if m.cursor > 0 { m.cursor-- }
        case "down", "j":
            if m.cursor < len(m.items)-1 { m.cursor++ }
        case "enter":
            fmt.Printf("Selected: %s\n", m.items[m.cursor])
            return m, tea.Quit
        }
    }
    return m, nil
}

func (m model) View() string {
    s := ""
    for i, item := range m.items {
        if i == m.cursor {
            s += highlight.Render("▸ "+item) + "\n"
        } else {
            s += "  " + item + "\n"
        }
    }
    return s + "\n(↑/↓ move, enter select, q quit)"
}

func main() {
    m := model{items: []string{"Option A", "Option B", "Option C"}}
    tea.NewProgram(m).Run()
}
```

### Library Cheat Sheet

| Need | Library | Example |
|------|---------|---------|
| TUI framework | `bubbletea` | `tea.NewProgram(model).Run()` |
| Components | `bubbles` | `list.New()`, `textinput.New()` |
| Styling | `lipgloss` | `style.Foreground(lipgloss.Color("212"))` |
| Forms (simple) | `huh` | `huh.NewInput().Title("Name").Run()` |
| Markdown | `glamour` | `glamour.Render(md, "dark")` |
| Animation | `harmonica` | `harmonica.NewSpring()` |

### Quick Patterns

**Styled Output (no TUI):**
```go
style := lipgloss.NewStyle().Foreground(lipgloss.Color("205")).Bold(true)
fmt.Println(style.Render("Hello!"))
```

**Simple Form (no TUI):**
```go
var name string
huh.NewInput().Title("Your name?").Value(&name).Run()
```

**Confirmation:**
```go
var ok bool
huh.NewConfirm().Title("Delete?").Value(&ok).Run()
```

**[Full Go TUI Reference →](references/go-tui.md)**
**[Component API →](references/component-catalog.md)**
**[Advanced Patterns →](references/advanced-patterns.md)**

---

## For Infrastructure

### Wish: SSH Apps

Serve TUI over SSH:

```go
s, _ := wish.NewServer(
    wish.WithAddress(":2222"),
    wish.WithHostKeyPath(".ssh/key"),
    wish.WithMiddleware(
        bubbletea.Middleware(handler),
        logging.Middleware(),
    ),
)
s.ListenAndServe()
```

Connect: `ssh localhost -p 2222`

### Other Infrastructure

| Tool | Purpose | Install |
|------|---------|---------|
| **Soft Serve** | Self-hosted Git | `brew install soft-serve` |
| **Pop** | Send email | `brew install pop` |
| **Skate** | Key-value store | `brew install skate` |
| **Melt** | SSH key backup | `brew install melt` |
| **Wishlist** | SSH gateway | `go install github.com/charmbracelet/wishlist` |

### Testing TUIs

```go
tm := teatest.NewTestModel(t, model)
tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
tm.Type("hello")
teatest.WaitFor(t, tm, func(b []byte) bool {
    return strings.Contains(string(b), "expected")
})
```

**[Full Infrastructure Reference →](references/infrastructure.md)**

---

## Decision Guide

```
Is it a shell script?
├─ Yes → Use Gum
│        Need recording? → VHS
│        Need AI? → Mods
│
└─ No (Go application)
   │
   ├─ Just need styled output?
   │  └─ Lip Gloss only (no Bubble Tea)
   │
   ├─ Need simple prompts/forms?
   │  └─ Huh standalone
   │
   ├─ Need full interactive TUI?
   │  └─ Bubble Tea + Bubbles + Lip Gloss
   │
   └─ Need SSH access?
      └─ Wish + Bubble Tea
```

---

## When NOT to Use Charm

- **Output is piped:** `mytool | grep` → plain text
- **CI/CD:** No terminal → use flags/env vars
- **One simple prompt:** Maybe `fmt.Scanf` is fine

**Escape hatch:**
```go
if !term.IsTerminal(os.Stdin.Fd()) || os.Getenv("NO_TUI") != "" {
    runPlainMode()
    return
}
```

---

## All References

| Reference | Contents |
|-----------|----------|
| [Shell Scripts](references/shell-scripts.md) | Gum, VHS, Mods, Freeze, Glow - complete |
| [Go TUI](references/go-tui.md) | Bubble Tea patterns, debugging, anti-patterns |
| [Infrastructure](references/infrastructure.md) | Wish, Soft Serve, teatest, x/term |
| [Component Catalog](references/component-catalog.md) | All Bubbles components API |
| [Advanced Patterns](references/advanced-patterns.md) | Theming, layouts, production architecture |
