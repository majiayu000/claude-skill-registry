---
name: bubble-tea-testing
description: Testing Bubble Tea TUI applications
category: Testing BDD
---

# Skill: bubble-tea-testing

## What I do

I provide Bubble Tea testing expertise: testing Update logic, verifying View output, testing commands, component integration, and using teatest for program-level testing.

## When to use me

- Unit testing Bubble Tea model Update logic
- Verifying View output contains expected content
- Testing tea.Cmd return values and side effects
- Integration testing composed components
- Using teatest for full program simulation

## Core principles

1. **Test Update directly** - Feed messages, assert on returned model
2. **View is pure** - Test View output as string matching
3. **Commands are testable** - Test message types returned by commands
4. **Isolate components** - Test components independently before composition
5. **Golden files** - Use teatest golden files for visual regression

## Patterns & examples

**Testing Update logic:**
```go
func TestModelUpdate(t *testing.T) {
  g := gomega.NewWithT(t)
  m := initialModel()

  // Simulate pressing "down" key
  updated, cmd := m.Update(tea.KeyMsg{Type: tea.KeyDown})
  result := updated.(model)

  g.Expect(result.cursor).To(gomega.Equal(1))
  g.Expect(cmd).To(gomega.BeNil())
}

func TestQuitOnCtrlC(t *testing.T) {
  g := gomega.NewWithT(t)
  m := initialModel()

  _, cmd := m.Update(tea.KeyMsg{Type: tea.KeyCtrlC})

  // tea.Quit returns a special quit message
  g.Expect(cmd).NotTo(gomega.BeNil())
}
```

**Testing View output:**
```go
func TestViewShowsCursor(t *testing.T) {
  g := gomega.NewWithT(t)
  m := model{
    cursor:  1,
    choices: []string{"Alpha", "Beta", "Gamma"},
    selected: map[int]struct{}{},
  }

  view := m.View()

  g.Expect(view).To(gomega.ContainSubstring("> Beta"))
  g.Expect(view).NotTo(gomega.ContainSubstring("> Alpha"))
}

func TestViewShowsSelectedItems(t *testing.T) {
  g := gomega.NewWithT(t)
  m := model{
    cursor:  0,
    choices: []string{"Alpha", "Beta"},
    selected: map[int]struct{}{0: {}},
  }

  view := m.View()

  g.Expect(view).To(gomega.ContainSubstring("[x] Alpha"))
  g.Expect(view).To(gomega.ContainSubstring("[ ] Beta"))
}
```

**Testing with teatest (program-level):**
```go
func TestFullProgram(t *testing.T) {
  m := initialModel()
  tm := teatest.NewModel(t, m, teatest.WithInitialTermSize(80, 24))

  // Send key sequence
  tm.Send(tea.KeyMsg{Type: tea.KeyDown})
  tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
  tm.Send(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("q")})

  // Wait for program to finish
  tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second))

  // Assert final output
  out := tm.FinalOutput(t)
  if !strings.Contains(string(out), "[x]") {
    t.Error("expected selected item in output")
  }
}
```

**Testing commands that return messages:**
```go
func TestFetchStatusCommand(t *testing.T) {
  g := gomega.NewWithT(t)
  m := initialModel()

  // Trigger the command
  _, cmd := m.Update(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("r")})
  g.Expect(cmd).NotTo(gomega.BeNil())

  // Execute the command and check the message type
  msg := cmd()
  _, isStatus := msg.(statusMsg)
  _, isErr := msg.(errMsg)
  g.Expect(isStatus || isErr).To(gomega.BeTrue())
}
```

## Absolute Rules (Bubble Tea Testing Contract)

MUST NOT:
- Call `Program.Run()` in tests — creates blocking event loop
- Call `SubmitHuhForm()` in tests — deadlocks waiting for TUI interaction
- Block waiting for TUI interaction in any form
- Put business logic inside `Update()` methods

MUST DO:
- Extract business logic into pure functions (no Bubble Tea dependencies)
- Test pure functions directly, not through the event loop
- Call `Update()` manually with tea.KeyMsg for UI behavior tests
- Keep Update() as thin adapter: route messages → call domain logic → transition state

**Required Architecture**:
- Pure Domain Layer: business logic, validation, rules — no Bubble Tea imports, deterministic, called directly from Godog steps
- TUI Layer: rendering adapter only — ExtractInput() extracts data, Update() routes messages, View() displays results

**Enforcement Rule** (4-step process for writing tests):
1. Identify business logic
2. Extract it into a pure function
3. Test the pure function with unit tests
4. Do NOT test the runtime event loop

## Anti-patterns to avoid

- ❌ Testing via terminal output only (test Update logic directly)
- ❌ Skipping View tests (rendering bugs are common)
- ❌ Testing Lip Gloss styling (test content, not colours)
- ❌ Large integration tests without unit coverage
- ❌ Ignoring command return values

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Bubble Tea Testing.md`

## Related skills

- `bubble-tea-expert` - Bubble Tea framework patterns being tested
- `ginkgo-gomega` - BDD framework for structuring Bubble Tea tests
- `gomock` - Mocking dependencies in Bubble Tea components
- `golang` - Core Go testing idioms
