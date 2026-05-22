---
name: mui
description: "Material UI component library best practices for React applications. Component patterns, theming, styling with sx prop, custom components. Trigger: When using Material-UI components, implementing MUI theming, or creating custom MUI-based components."
skills:
  - conventions
  - a11y
  - react
  - typescript
  - humanizer
dependencies:
  "@mui/material": ">=5.0.0 <6.0.0"
  react: ">=17.0.0 <19.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# MUI (Material UI) Skill

## Overview

Best practices for using Material UI components in React applications with proper theming, customization, and accessibility.

## Objective

Enable developers to build consistent, accessible UIs using MUI components with proper theme configuration and customization patterns.

---

## Extended Mandatory Read Protocol

This skill uses the **Extended Mandatory Read Protocol** for complex MUI patterns (40+ patterns total).

### Reading Strategy

1. **ALWAYS read**: This main SKILL.md (covers 80% of common MUI cases)
2. **Read references/ when**:
   - Decision Tree indicates "**MUST read** {reference}"
   - Quick Reference Table marks it "Required Reading: ✅"
   - Critical Pattern says "**[CRITICAL] See** {reference} for..."
   - Working with advanced MUI features (DataGrid, complex forms, theming)

### When to Read References

| Situation                             | Read SKILL.md | Read references/ | Which References                    |
| ------------------------------------- | ------------- | ---------------- | ----------------------------------- |
| Basic MUI components (Button, Box)    | ✅ Yes        | ❌ No            | SKILL.md covers all needed patterns |
| Component library patterns            | ✅ Yes        | ✅ Yes           | components.md (required)            |
| Theme customization / dark mode       | ✅ Yes        | ✅ Yes           | theming.md (required)               |
| Advanced styling (sx, styled API)     | ✅ Yes        | ✅ Yes           | customization.md (required)         |
| Tables, DataGrid, Lists               | ✅ Yes        | ✅ Yes           | data-display.md (required)          |
| Form validation, Select, Autocomplete | ✅ Yes        | ✅ Yes           | forms.md (required)                 |
| Multiple advanced features            | ✅ Yes        | ✅ Yes           | All relevant references             |

### Available References

All reference files located in `skills/mui/references/`:

- **README.md**: Overview of all MUI references and navigation guide
- **components.md**: Button, TextField, Typography, layouts, navigation (required for component patterns)
- **theming.md**: createTheme, palette, dark mode, component overrides (required for theme customization)
- **customization.md**: sx prop, styled API, custom variants, performance (required for advanced styling)
- **data-display.md**: Table, DataGrid, List, Card patterns (required for data display)
- **forms.md**: TextField validation, Select, Autocomplete, Formik integration (required for forms)

### Conditional Language

- **"MUST read"** → **Obligatory** - Read immediately before proceeding
- **"CHECK"** or "Consider" → **Suggested** - Read if you need deeper understanding
- **"OPTIONAL"** → **Ignorable** - Read only for learning or edge cases

### Example: Theme Customization Task

```
1. User: "Set up dark mode with custom palette"
2. Read: skills/mui/SKILL.md (this file)
3. Check Decision Tree: "Dark mode? → MUST read theming.md"
4. Read: skills/mui/references/theming.md (REQUIRED)
5. Execute: Implement dark mode with createTheme and ThemeProvider
```

---

## When to Use

Use this skill when:

- Building UI with Material-UI components
- Implementing MUI theming and design system
- Customizing MUI components with sx prop or styled API
- Creating consistent spacing, typography, and color systems
- Integrating MUI with React applications

Don't use this skill for:

- Tailwind CSS styling (use tailwindcss skill)
- Plain CSS/HTML (use css/html skills)
- Custom component libraries (use react skill)

---

## Critical Patterns

### ✅ REQUIRED: Use ThemeProvider

```typescript
// ✅ CORRECT: Wrap app with ThemeProvider
import { ThemeProvider, createTheme } from '@mui/material';

const theme = createTheme({ /* config */ });

<ThemeProvider theme={theme}>
  <App />
</ThemeProvider>

// ❌ WRONG: Using MUI without theme (inconsistent styling)
<App /> // No ThemeProvider
```

### ✅ REQUIRED: Use sx Prop for One-Off Styles

```typescript
// ✅ CORRECT: sx prop with theme values
<Box sx={{ p: 2, bgcolor: 'primary.main' }}>

// ❌ WRONG: Inline styles (loses theme consistency)
<Box style={{ padding: '16px', backgroundColor: '#1976d2' }}>
```

### ✅ REQUIRED: Use MUI Components Over Custom HTML

```typescript
// ✅ CORRECT: MUI components with built-in accessibility
<Button variant="contained" onClick={handleClick}>Submit</Button>

// ❌ WRONG: Custom HTML without accessibility
<div className="button" onClick={handleClick}>Submit</div>
```

---

## Conventions

Refer to conventions for:

- Code organization

Refer to a11y for:

- Keyboard navigation
- ARIA attributes

Refer to react for:

- Component patterns
- Hooks usage

### MUI Specific

- Use MUI components over custom HTML when available
- Implement theme provider for consistent styling
- Use sx prop for one-off styling
- Leverage styled API for reusable styled components
- Follow MUI's accessibility guidelines

---

## Decision Tree

**One-off styling?** → Use `sx` prop with theme values: `sx={{ p: 2, bgcolor: 'primary.main' }}`.

**Reusable styled component?** → Use `styled()` API to create custom components. **[CRITICAL] See** `references/customization.md` for styled API patterns.

**Global theme change?** → Configure in `createTheme()`, apply via `ThemeProvider`. **[CRITICAL] See** `references/theming.md` for theme setup.

**Need custom variant?** → Extend theme with component variants in theme configuration. **[CRITICAL] See** `references/customization.md` for variant patterns.

**Responsive styling?** → Use theme breakpoints: `sx={{ p: { xs: 1, md: 2 } }}` or `theme.breakpoints.up('md')`.

**Dark mode?** → Create separate light/dark themes, toggle via ThemeProvider. **[CRITICAL] See** `references/theming.md` for dark mode implementation.

**Custom component?** → Extend MUI component with styled API or composition pattern. **[CRITICAL] See** `references/components.md` for component patterns.

**Building forms?** → Use TextField, Select, Autocomplete with validation. **[CRITICAL] See** `references/forms.md` for form patterns.

**Displaying tables/lists?** → Use Table, DataGrid, List components. **[CRITICAL] See** `references/data-display.md` for data display patterns.

---

## Example

```typescript
import { Button, Box, ThemeProvider, createTheme } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

<ThemeProvider theme={theme}>
  <Box sx={{ p: 2 }}>
    <Button variant="contained" color="primary">
      Click Me
    </Button>
  </Box>
</ThemeProvider>
```

---

## Edge Cases

**Theme nesting:** Nested ThemeProviders merge themes. Use this for component-specific overrides.

**SSR styling:** Use `@mui/material/styles` ServerStyleSheets for server-side rendering to prevent FOUC.

**Custom breakpoints:** Define in theme: `createTheme({ breakpoints: { values: { mobile: 0, tablet: 640, desktop: 1024 } } })`.

**sx prop performance:** For frequently re-rendered components, use `styled()` instead of sx to avoid inline style recalculation.

**Icon size inconsistency:** Use `fontSize` prop: `<Icon fontSize="small" />` for consistent sizing.

---

## References

- https://mui.com/material-ui/getting-started/
- https://mui.com/material-ui/customization/theming/
