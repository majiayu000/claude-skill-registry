---
name: huh
description: Interactive form library (Go) and patterns
category: UI Frameworks
---

# Skill: huh

## What I do

I provide huh form library expertise: building interactive terminal forms with field types (Input, Text, Select, MultiSelect, Confirm), groups, validation, theming, and accessible form patterns in Go.

## When to use me

- Building interactive terminal forms for user input
- Choosing the right field type for each input
- Adding validation to form fields
- Grouping fields into multi-step forms
- Theming forms to match application style

## Core principles

1. **Declarative form building** - Define fields and groups, huh handles navigation
2. **Validation at field level** - Validate each field independently with closures
3. **Groups for flow** - Group related fields; each group is one "page"
4. **Accessible by default** - huh handles focus, keyboard nav, screen readers
5. **Built on Bubble Tea** - Forms are Bubble Tea models; compose with other components

## Patterns & examples

**Basic form with validation:**
```go
var name string
var email string

form := huh.NewForm(
  huh.NewGroup(
    huh.NewInput().
      Title("Name").
      Value(&name).
      Validate(func(s string) error {
        if len(s) < 2 {
          return fmt.Errorf("name must be at least 2 characters")
        }
        return nil
      }),
    huh.NewInput().
      Title("Email").
      Value(&email).
      Validate(func(s string) error {
        if !strings.Contains(s, "@") {
          return fmt.Errorf("invalid email address")
        }
        return nil
      }),
  ),
)

err := form.Run()
if err != nil { log.Fatal(err) }
fmt.Printf("Hello, %s (%s)\n", name, email)
```

**Select and MultiSelect:**
```go
var role string
var permissions []string

form := huh.NewForm(
  huh.NewGroup(
    huh.NewSelect[string]().
      Title("Role").
      Options(
        huh.NewOption("Administrator", "admin"),
        huh.NewOption("Editor", "editor"),
        huh.NewOption("Viewer", "viewer"),
      ).
      Value(&role),

    huh.NewMultiSelect[string]().
      Title("Permissions").
      Options(
        huh.NewOption("Read", "read"),
        huh.NewOption("Write", "write"),
        huh.NewOption("Delete", "delete"),
      ).
      Value(&permissions),
  ),
)
```

**Multi-step form with groups:**
```go
// ✅ Correct: each group is a step/page
form := huh.NewForm(
  // Step 1: Personal info
  huh.NewGroup(
    huh.NewInput().Title("First Name").Value(&firstName),
    huh.NewInput().Title("Last Name").Value(&lastName),
  ).Title("Personal Information"),

  // Step 2: Preferences
  huh.NewGroup(
    huh.NewSelect[string]().Title("Theme").
      Options(huh.NewOption("Dark", "dark"), huh.NewOption("Light", "light")).
      Value(&theme),
    huh.NewConfirm().Title("Enable notifications?").Value(&notify),
  ).Title("Preferences"),
)

// ❌ Wrong: all fields in one giant group (overwhelming)
```

**Confirm with description:**
```go
var proceed bool

huh.NewConfirm().
  Title("Deploy to production?").
  Description("This will affect 1,234 users").
  Affirmative("Yes, deploy").
  Negative("Cancel").
  Value(&proceed)
```

**Custom theme:**
```go
theme := huh.ThemeCharm()  // or ThemeDracula(), ThemeCatppuccin()
form := huh.NewForm(groups...).WithTheme(theme)
```

## Anti-patterns to avoid

- ❌ All fields in one group (break into logical steps for complex forms)
- ❌ Validation only after submit (validate per-field for immediate feedback)
- ❌ Ignoring `Run()` error (user may cancel with Ctrl+C)
- ❌ Complex logic in validators (keep validators simple; pre-process data)
- ❌ Hardcoded styles (use themes for consistent appearance)


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/UI-Frameworks/Huh.md`

## Related skills

- `huh-testing` - Testing huh form components
- `bubble-tea-expert` - Bubble Tea framework that huh builds on
- `ux-design` - User experience principles for form design
- `golang` - Core Go patterns used with huh
