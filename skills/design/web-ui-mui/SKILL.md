---
name: web-ui-mui
description: Material UI component library patterns for React
---

# MUI (Material UI) Patterns

> **Quick Guide:** MUI provides pre-styled React components implementing Material Design. Use `createTheme` + `ThemeProvider` for global theming, `sx` prop for one-off styles, `styled()` for reusable styled components, and `slots`/`slotProps` for deep component customization. Prefer path imports in development for faster builds. **Current: v7.x (March 2025)** -- CSS layers support, standardized slot pattern, Grid v2 promoted, React 19 compatible. MUI X v8 for DataGrid, DatePicker, Charts.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap the app in `ThemeProvider` with a `createTheme()` instance -- never use MUI components without a theme)**

**(You MUST use path imports (`@mui/material/Button`) in development for faster startup -- barrel imports (`@mui/material`) cause 6x slower dev builds)**

**(You MUST use `slots`/`slotProps` for component inner-element customization -- `componentsProps` is deprecated in v7)**

**(You MUST use `theme.applyStyles('dark', {...})` for dark mode conditional styles -- never use `theme.palette.mode === 'dark'` which causes flickering)**

</critical_requirements>

---

**Auto-detection:** MUI, Material UI, @mui/material, @mui/system, @mui/icons-material, @mui/x-data-grid, @mui/x-date-pickers, createTheme, ThemeProvider, sx prop, styled, CssBaseline, useTheme, useMediaQuery, DataGrid, DatePicker, AppBar, Drawer, Dialog, Snackbar, TextField, Autocomplete, slotProps

**When to use:**

- Building React applications with pre-styled Material Design components
- Creating themed UIs with consistent design tokens (palette, typography, spacing)
- Implementing complex data views with DataGrid, DatePicker, or Charts (MUI X)
- Building admin dashboards, forms, and CRUD interfaces rapidly

**When NOT to use:**

- Headless/unstyled components needed (use a headless component library instead)
- Minimal bundle size is critical (MUI adds significant weight)
- Non-Material Design aesthetic required without heavy theme customization
- Server Components needed as primary rendering strategy (MUI components are client-only)

**Key patterns covered:**

- Theme setup, color schemes, and dark mode
- sx prop styling (theme-aware, responsive, callbacks)
- styled() API for reusable components
- Slots/slotProps for component customization (v7)
- Layout components (Grid, Stack, Box, Container)
- TypeScript theme augmentation

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) -- ThemeProvider, createTheme, CssBaseline, color schemes, dark mode toggle, TypeScript augmentation, Next.js integration, CSS layers
- [examples/form-inputs.md](examples/form-inputs.md) -- TextField, Select, Autocomplete, slots/slotProps customization
- [examples/layout.md](examples/layout.md) -- Grid, Stack, Box, Container, responsive card grid
- [examples/data-grid.md](examples/data-grid.md) -- @mui/x-data-grid columns, pagination, custom rendering
- [examples/feedback.md](examples/feedback.md) -- Dialog, Snackbar, Alert, Skeleton, CircularProgress
- [examples/navigation.md](examples/navigation.md) -- AppBar, Drawer, Tabs, responsive dashboard layout
- [examples/styling.md](examples/styling.md) -- styled() API, sx prop patterns, dark mode styling, custom props
- [reference.md](reference.md) -- Decision frameworks, anti-patterns, quick reference tables

---

<philosophy>

## Philosophy

MUI implements Material Design as a comprehensive React component library. It provides:

- **Design System**: Complete palette, typography, spacing, shadows, and breakpoint tokens
- **Pre-styled Components**: 50+ components with consistent visual language
- **Customization Layers**: From simple `sx` overrides to deep theme-level component restyling
- **Accessibility**: Built-in ARIA attributes, keyboard navigation, and focus management

**Core Principle:** Theme drives everything. Define your design tokens in `createTheme()`, and all components inherit consistent styling. Override at the component level with `sx`, `styled()`, or `slots`/`slotProps`.

**MUI v7 Key Changes (March 2025):**

- CSS layers support via `enableCssLayer` (integrates with utility-first CSS frameworks)
- Standardized `slots`/`slotProps` across all components (replaces `components`/`componentsProps`)
- Grid v2 promoted to `Grid` (old Grid renamed to `GridLegacy`)
- Lab components graduated to `@mui/material` (Alert, Skeleton, Autocomplete, etc.)
- Package layout updated for ESM/CJS dual support (no deep imports beyond one level)
- React 19 full compatibility

**Pigment CSS Status:** MUI's zero-runtime CSS-in-JS engine is currently **on hold / alpha**. Production apps should continue using the default Emotion-based styling engine.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Theme Setup and Configuration

Every MUI app starts with `createTheme()` and `ThemeProvider`. The theme defines all design tokens.

```typescript
import { createTheme, ThemeProvider, CssBaseline } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    secondary: { main: "#9c27b0" },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    button: { textTransform: "none" },
  },
  shape: { borderRadius: 8 },
  spacing: 8,
});

function App({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}

export { App };
```

**Why good:** Centralized design tokens, CssBaseline normalizes cross-browser styles, all children inherit theme

For production-ready theme with color schemes, dark mode, component overrides, and TypeScript augmentation, see [examples/core.md](examples/core.md).

---

### Pattern 2: CSS Variables and Dark Mode

MUI v7 supports CSS variables natively. Use `colorSchemes` for flicker-free light/dark mode.

```typescript
const theme = createTheme({
  cssVariables: { colorSchemeSelector: "data" },
  colorSchemes: {
    light: { palette: { primary: { main: "#1976d2" } } },
    dark: { palette: { primary: { main: "#90caf9" } } },
  },
});
```

Toggle with the `useColorScheme` hook:

```typescript
import { useColorScheme } from "@mui/material/styles";
const { mode, setMode } = useColorScheme();
setMode(mode === "light" ? "dark" : "light");
```

**Why good:** CSS variables prevent flash of wrong theme on SSR, persists preference to localStorage

```typescript
// BAD: Causes SSR flicker
backgroundColor: theme.palette.mode === "dark" ? "#333" : "#fff";
// GOOD: Use applyStyles in styled()
...theme.applyStyles("dark", { backgroundColor: "#1a1a2e" });
```

For full dark mode toggle component, see [examples/core.md](examples/core.md).

---

### Pattern 3: The sx Prop

The `sx` prop is MUI's primary styling escape hatch. It accesses theme values, supports responsive breakpoints, and handles pseudo-selectors.

```typescript
<Box
  sx={{
    p: 3,                         // theme.spacing(3) = 24px
    bgcolor: "background.paper",  // theme.palette.background.paper
    borderRadius: 1,              // theme.shape.borderRadius * 1
    boxShadow: 3,                 // theme.shadows[3]
    width: { xs: "100%", md: "50%" }, // Responsive
    "&:hover": { boxShadow: 6 },
  }}
/>
```

**Why good:** Theme-aware shorthand properties, responsive without media queries

```typescript
// BAD: Inline styles bypass theme
<Box style={{ padding: 24, backgroundColor: "#1976d2" }}>
```

**Why bad:** Hardcoded values, no theme consistency, no responsive support, no dark mode awareness

For callback syntax and advanced sx patterns, see [examples/styling.md](examples/styling.md).

---

### Pattern 4: styled() API for Reusable Components

Use `styled()` when you need a reusable component with theme-aware styles. Prefer `sx` for one-off styles.

```typescript
import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";

const HOVER_ELEVATION = 8;

const StyledCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(3),
  borderRadius: theme.shape.borderRadius * 2,
  "&:hover": { boxShadow: theme.shadows[HOVER_ELEVATION] },
  ...theme.applyStyles("dark", {
    backgroundColor: theme.palette.grey[900],
  }),
}));

export { StyledCard };
```

**Why good:** Reusable, theme-aware, dark mode handled with `applyStyles`

For styled with custom props (`shouldForwardProp`), gradient buttons, and more, see [examples/styling.md](examples/styling.md).

---

### Pattern 5: Slots and SlotProps (v7 Standard)

In MUI v7, `slots` and `slotProps` are the standardized API for customizing component inner elements. The older `components`/`componentsProps` API is deprecated.

```typescript
<Autocomplete
  slots={{ paper: Paper }}
  slotProps={{
    paper: { elevation: 8, sx: { borderRadius: 2 } },
    listbox: { sx: { maxHeight: 300 } },
  }}
  renderInput={(params) => <TextField {...params} label="Framework" />}
/>
```

**Why good:** Standardized API across all MUI components, replaces deprecated patterns

```typescript
// BAD: Deprecated in v7
<Autocomplete componentsProps={{ paper: { elevation: 8 } }} />
```

For callback slotProps and advanced customization, see [examples/form-inputs.md](examples/form-inputs.md).

---

### Pattern 6: Layout Components

MUI provides `Box`, `Stack`, `Grid`, and `Container` for layout. In v7, `Grid` is the former Grid2.

```typescript
// Grid: 12-column responsive layout (v7 uses size prop)
const SIDEBAR_COLUMNS = 4;
const MAIN_COLUMNS = 8;

<Grid container spacing={3}>
  <Grid size={{ xs: 12, md: SIDEBAR_COLUMNS }}><Sidebar /></Grid>
  <Grid size={{ xs: 12, md: MAIN_COLUMNS }}><MainContent /></Grid>
</Grid>

// Stack: single-axis layout with consistent spacing
<Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
  <Button variant="contained">Save</Button>
  <Button variant="outlined">Cancel</Button>
</Stack>

// Container: centered content with maxWidth
<Container maxWidth="lg" sx={{ py: 4 }}>{children}</Container>
```

**When to use each:** Box (flex/sx wrapper), Stack (single axis), Grid (12-column), Container (page centering)

For product card grids, dashboard layouts, and more, see [examples/layout.md](examples/layout.md).

---

### Pattern 7: TypeScript Theme Augmentation

Extend MUI's theme type system when adding custom palette colors or typography variants.

```typescript
// theme-augmentation.d.ts
declare module "@mui/material/styles" {
  interface Palette {
    neutral: Palette["primary"];
  }
  interface PaletteOptions {
    neutral?: PaletteOptions["primary"];
  }
}
declare module "@mui/material/Button" {
  interface ButtonPropsColorOverrides {
    neutral: true;
  }
}
```

Then use in theme and components:

```typescript
const theme = createTheme({
  palette: { neutral: { main: "#64748b", contrastText: "#fff" } },
});
<Button color="neutral" variant="contained">Neutral</Button>
```

**Why good:** Full type safety, IDE autocomplete for custom colors/variants

For complete augmentation with typography variants, see [examples/core.md](examples/core.md).

---

### Pattern 8: Next.js App Router Integration

MUI requires `AppRouterCacheProvider` from `@mui/material-nextjs` for proper SSR style injection.

```typescript
// app/layout.tsx
import { AppRouterCacheProvider } from "@mui/material-nextjs/v15-appRouter";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppRouterCacheProvider>
          <ThemeProvider theme={theme}>
            <CssBaseline />
            {children}
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}

export default RootLayout; // Next.js requires default export for layouts
```

**Why good:** Prevents style hydration mismatches, CSS layers enable predictable specificity with utility-first CSS

For CSS layers integration and Vite setup, see [examples/core.md](examples/core.md).

</patterns>

---

<performance>

## Performance Optimization

### Import Optimization

```typescript
// GOOD: Path imports -- fast in development
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";

// BAD: Barrel imports -- 6x slower dev startup
import { Button } from "@mui/material";
import { Delete } from "@mui/icons-material";
```

Path imports skip barrel file parsing. `@mui/icons-material` has 2000+ modules -- barrel imports force parsing all of them.

**Exception:** Next.js 13.5+ auto-optimizes via `optimizePackageImports`.

### Memoize Expensive Props

```typescript
// GOOD: Columns outside component (stable reference)
const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 90 },
];
function Table({ rows }: { rows: User[] }) {
  return <DataGrid rows={rows} columns={columns} />;
}

// BAD: Inline columns cause re-render every parent render
```

### Stable Slot References

```typescript
// GOOD: Defined outside render
const CustomPaper = (props: PaperProps) => <Paper {...props} elevation={8} />;
<Autocomplete slots={{ paper: CustomPaper }} />

// BAD: Inline function causes remount every render
<Autocomplete slots={{ paper: (props) => <Paper {...props} /> }} />
```

### ESLint Rule for Import Enforcement

```json
{
  "rules": {
    "no-restricted-imports": [
      "error",
      {
        "patterns": [
          {
            "regex": "^@mui/[^/]+$",
            "message": "Use path imports: import Button from '@mui/material/Button'"
          }
        ]
      }
    ]
  }
}
```

</performance>

---

<decision_framework>

## Decision Framework

### Styling Approach

```
How many places will this style be used?
+-- One place --> sx prop (inline, theme-aware)
+-- Multiple places (same type) --> styled() (reusable, typed)
+-- All instances of a component --> theme.components (global override)
+-- Customize inner elements --> slots/slotProps
```

### Layout Component Selection

```
What kind of layout?
+-- Single axis (row or column) --> Stack
+-- 12-column grid --> Grid
+-- Centered page content --> Container
+-- Flexible box with sx --> Box
+-- Both axes + complex --> Grid (nested)
```

### Component vs Custom Build

```
Does MUI have this component?
+-- YES --> Use it
|   +-- Minor style changes --> sx prop
|   +-- Structural changes --> slots/slotProps
|   +-- Completely different behavior --> Build custom
+-- NO --> Build custom
    +-- Simple interaction --> Base HTML + sx
    +-- Complex interaction --> Consider a headless component library
```

### Color Scheme Strategy

```
Do you need dark mode?
+-- YES --> Use colorSchemes in createTheme
|   +-- System preference only --> cssVariables: true
|   +-- Manual toggle --> useColorScheme hook
|   +-- Both --> colorSchemeSelector: "data" + useColorScheme
+-- NO --> Single palette in createTheme
```

### MUI X Component Selection

```
What data display do you need?
+-- Tabular data
|   +-- Simple (< 100 rows, no editing) --> Table component
|   +-- Complex (sorting, filtering, pagination) --> DataGrid
|   +-- Large dataset (100K+ rows) --> DataGridPro (virtualized)
+-- Date/time input --> DatePicker / DateTimePicker
+-- Charts --> MUI X Charts
+-- Tree structure --> TreeView
```

</decision_framework>

---

<integration>

## Integration Notes

**React 19:** Full compatibility in MUI v7.

**SSR Frameworks:** Use `@mui/material-nextjs` with `AppRouterCacheProvider` for Next.js App Router. See [examples/core.md](examples/core.md) for setup.

**CSS Layers:** Enable with `enableCssLayer` to integrate with utility-first CSS frameworks. Allows predictable specificity ordering.

**Form Libraries:** MUI `TextField` works with any form library via `inputRef` for registration or controlled `value`/`onChange` props. Map validation errors to `helperText` and `error` props.

**Styling Engine:** Emotion is the default and only production-ready engine. `@emotion/react` and `@emotion/styled` are required peer dependencies.

**Package Ecosystem:**

| Package                | Purpose                                   | Version |
| ---------------------- | ----------------------------------------- | ------- |
| `@mui/material`        | Core components (Button, TextField, etc.) | v7.x    |
| `@mui/system`          | sx prop, styled(), ThemeProvider          | v7.x    |
| `@mui/icons-material`  | 2000+ Material Design icons               | v7.x    |
| `@mui/x-data-grid`     | DataGrid (free tier)                      | v8.x    |
| `@mui/x-data-grid-pro` | DataGrid Pro (sorting, filtering, etc.)   | v8.x    |
| `@mui/x-date-pickers`  | DatePicker, TimePicker                    | v8.x    |
| `@mui/x-charts`        | Bar, Line, Pie, Scatter charts            | v8.x    |
| `@mui/x-tree-view`     | TreeView component                        | v8.x    |
| `@mui/material-nextjs` | Next.js SSR integration                   | v7.x    |
| `@emotion/react`       | Required peer dependency                  | v11.x   |
| `@emotion/styled`      | Required peer dependency                  | v11.x   |

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `theme.palette.mode === 'dark'` for conditional styles (causes SSR flicker -- use `theme.applyStyles('dark', {...})`)
- Missing `ThemeProvider` wrapper (components render with MUI defaults instead of your design tokens)
- Using barrel imports from `@mui/material` or `@mui/icons-material` (6x slower dev builds)
- Inline object/function definitions in `slots` prop (causes component remount every render)

**Medium Priority Issues:**

- Using deprecated `components`/`componentsProps` instead of `slots`/`slotProps` (removed in future versions)
- Using `GridLegacy` instead of the new `Grid` component with `size` prop
- Hardcoding colors/spacing instead of using theme tokens (`#1976d2` vs `primary.main`)
- Using `style` prop instead of `sx` (bypasses theme, no responsive support)
- Deep importing beyond one level: `@mui/material/styles/createTheme` (broken in v7 ESM)

**Common Mistakes:**

- Forgetting `CssBaseline` (inconsistent cross-browser baseline styles)
- Not memoizing DataGrid `columns` array (causes unnecessary re-renders)
- Using `@mui/lab` for graduated components (Alert, Skeleton, etc. are now in `@mui/material`)
- Missing TypeScript augmentation for custom palette colors (no autocomplete, type errors at usage)
- Setting `zIndex` manually on MUI components (conflicts with MUI's z-index scale)

**Gotchas & Edge Cases:**

- MUI components are **client-only** -- they require `'use client'` in Next.js App Router pages, not just layout
- `sx` prop arrays merge styles left-to-right; later items override earlier ones (useful for conditional styles)
- `spacing` theme value is a **multiplier**, not pixels: `spacing(2)` = `2 * 8px` = `16px` by default
- `Grid` `size` prop in v7 replaces `xs`/`sm`/`md`/`lg`/`xl` individual props from Grid2
- `TextField` is a composed component (Input + InputLabel + FormHelperText) -- use `slotProps.input` to target the actual input element
- `Dialog` `TransitionProps` must not remount the Transition component -- keep it stable between renders
- `useMediaQuery` returns `false` during SSR -- design for mobile-first and handle the hydration mismatch
- `createTheme` is not tree-shakeable -- a large theme config doesn't increase bundle, but unused components still need tree shaking via path imports

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap the app in `ThemeProvider` with a `createTheme()` instance -- never use MUI components without a theme)**

**(You MUST use path imports (`@mui/material/Button`) in development for faster startup -- barrel imports (`@mui/material`) cause 6x slower dev builds)**

**(You MUST use `slots`/`slotProps` for component inner-element customization -- `componentsProps` is deprecated in v7)**

**(You MUST use `theme.applyStyles('dark', {...})` for dark mode conditional styles -- never use `theme.palette.mode === 'dark'` which causes flickering)**

**Failure to follow these rules will cause SSR flickering, degraded dev performance, and deprecated API usage.**

</critical_reminders>
