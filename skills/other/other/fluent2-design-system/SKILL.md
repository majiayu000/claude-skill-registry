---
name: fluent2-design-system
description: >
  Build interfaces using Microsoft's Fluent 2 design system via @fluentui/react-components (v9).
  Use when the user requests UI built with Fluent UI, Fluent 2, Microsoft design language,
  Teams-style UI, or Office-style interfaces. Covers: React component usage, theming with
  FluentProvider, styling with makeStyles/tokens/Griffel, design token application, layout
  patterns, typography, color system, accessibility, dark/light/high-contrast themes, and
  custom branding. Also triggers for: "make it look like Teams/Outlook/Office", "use Fluent",
  "Microsoft design system", "@fluentui", or any request to build UI that follows Microsoft's
  design language. Do NOT use for Fluent UI v8 (@fluentui/react) unless migrating to v9.
---

# Fluent 2 Design System

Build production-grade interfaces using Microsoft's Fluent 2 design system with `@fluentui/react-components` (v9).

## Quick Start

Every Fluent 2 React app requires a `FluentProvider` wrapping the component tree with a theme:

```jsx
import {
  FluentProvider,
  webLightTheme,
  webDarkTheme,
  Button,
  tokens,
  makeStyles,
  mergeClasses,
} from "@fluentui/react-components";

export default function App() {
  return (
    <FluentProvider theme={webLightTheme}>
      <Button appearance="primary">Hello Fluent 2</Button>
    </FluentProvider>
  );
}
```

Install: `npm install @fluentui/react-components`

## Core Architecture

### Theming

- **Built-in themes**: `webLightTheme`, `webDarkTheme`, `teamsLightTheme`, `teamsDarkTheme`, `teamsHighContrastTheme`
- **Custom branding**: Use `createLightTheme(brandRamp)` / `createDarkTheme(brandRamp)` with a `BrandVariants` object (keys `10`–`160`)
- **Nesting**: `FluentProvider` can nest for sub-trees with different themes
- Theme values are emitted as CSS custom properties on the provider element

### Styling with Griffel

Use `makeStyles` (from `@fluentui/react-components`) — never inline styles or external CSS for token-aware styling.

```jsx
const useStyles = makeStyles({
  root: {
    backgroundColor: tokens.colorNeutralBackground1,
    color: tokens.colorNeutralForeground1,
    display: "flex",
    gap: tokens.spacingHorizontalM,
    padding: tokens.spacingVerticalM,
  },
  active: {
    backgroundColor: tokens.colorBrandBackground,
    color: tokens.colorNeutralForegroundOnBrand,
  },
});

function MyComponent({ isActive }) {
  const styles = useStyles();
  return (
    <div className={mergeClasses(styles.root, isActive && styles.active)}>
      Content
    </div>
  );
}
```

**Critical rules**:
- Define `makeStyles` outside components (module scope)
- Use `mergeClasses()` to compose classes — never concatenate strings
- Use `tokens.*` for all colors, spacing, typography, radii, shadows — never hardcode hex/px values
- CSS shorthands (`border`, `borderRadius`, `padding`, etc.) are **not supported** — use `shorthands.*` helper or longhand properties
- Pseudo-selectors use nested objects: `":hover": { color: tokens.colorBrandForeground1 }`
- Media queries use nested objects: `"@media (min-width: 768px)": { flexDirection: "row" }`

### Component Model

All v9 components follow a consistent pattern:
- **Slots**: Named sub-parts (e.g., `root`, `icon`, `content`) that accept props or JSX
- **Appearance variants**: `"primary"`, `"secondary"`, `"subtle"`, `"transparent"`, `"outline"`
- **Size variants**: `"small"`, `"medium"`, `"large"`
- **Shape variants**: `"rounded"`, `"circular"`, `"square"`

Override component styles via `className` with `makeStyles`/`mergeClasses`.

## Design Tokens

Tokens are the bridge between design intent and code. Always use `tokens.*` — never raw values.

**For complete token reference tables (color, typography, spacing, elevation, stroke, corner radius), see** `references/tokens.md`.

### Token Categories at a Glance

| Category | Prefix | Example |
|---|---|---|
| Neutral colors | `colorNeutral*` | `tokens.colorNeutralBackground1` |
| Brand colors | `colorBrand*` | `tokens.colorBrandBackground` |
| Status colors | `colorPalette{Color}*` | `tokens.colorPaletteRedForeground1` |
| Typography | `fontFamily*`, `fontSize*`, `fontWeight*`, `lineHeight*` | `tokens.fontSizeBase300` |
| Spacing | `spacingHorizontal*`, `spacingVertical*` | `tokens.spacingHorizontalM` |
| Border radius | `borderRadius*` | `tokens.borderRadiusMedium` |
| Stroke width | `strokeWidth*` | `tokens.strokeWidthThin` |
| Shadow | `shadow*` | `tokens.shadow4` |
| Duration | `duration*` | `tokens.durationNormal` |
| Easing | `curve*` | `tokens.curveEasyEase` |

### Two-Layer Token System

1. **Global tokens** — context-agnostic raw values (e.g., `colorBlue60`, `fontSize300`)
2. **Alias tokens** — semantic meaning applied to globals (e.g., `colorBrandBackground` → blue, `colorNeutralForeground1` → dark gray)

In code, consume alias tokens via the `tokens` object.

## Layout

- **Grid**: Use CSS Grid/Flexbox — Fluent 2 v9 has no `Stack` component
- **Spacing scale**: 4px base unit. Values: `XXS`(2), `XS`(4), `S`(8), `M`(12), `L`(16), `XL`(20), `XXL`(24), `XXXL`(32)
- **Column grid**: 12-column framework recommended for web; use CSS grid
- **Alignment**: Use `tokens.spacingHorizontal*` and `tokens.spacingVertical*` for consistent spacing

## Typography

- **Primary typeface**: Segoe UI (web), Segoe UI Variable (Windows), SF Pro (macOS/iOS), Roboto (Android)
- **Font stack**: `tokens.fontFamilyBase` = Segoe UI → system fallbacks → sans-serif
- **Monospace**: `tokens.fontFamilyMonospace`
- **Text presets**: Use `<Text>` component with preset variants — `Caption1`, `Body1`, `Body1Strong`, `Subtitle1`, `Subtitle2`, `Title1`, `Title2`, `Title3`, `LargeTitle`, `Display`
- **Alignment**: Left-align for LTR; Fluent handles RTL automatically via Griffel

## Color System

Three palettes:
1. **Neutral** — blacks, whites, grays for surfaces, text, layout
2. **Brand** — accent colors reinforcing identity (default Microsoft brand = blue)
3. **Shared/Status** — cross-product colors: red (danger), green (success), yellow (warning), blue (informational)

**Interaction states**: rest → hover (darker) → pressed (darkest). Focus adds a thicker stroke, not a color change.

## Accessibility

- All components include ARIA roles, keyboard navigation (via Tabster), and focus management
- High contrast: use `teamsHighContrastTheme` or handle `@media (forced-colors: active)` with system colors (`ButtonText`, `Highlight`, etc.)
- Focus indicators are visible by default — never remove them
- Ensure WCAG contrast via semantic token pairing (e.g., `colorNeutralForeground1` on `colorNeutralBackground1`)

## Component Inventory

**For the full categorized component list with usage notes, see** `references/components.md`.

### Most-Used Components

**Actions**: Button, CompoundButton, SplitButton, ToggleButton, MenuButton, Link
**Inputs**: Input, Textarea, Select, Combobox, Dropdown, Checkbox, RadioGroup, Switch, Slider, SpinButton, DatePicker, TimePicker
**Layout**: Card, Divider, Drawer, Dialog, Popover, Tooltip
**Data Display**: Table, DataGrid, Tree, Accordion, Badge, Avatar, AvatarGroup, Tag, Persona
**Navigation**: TabList, Breadcrumb, Nav (preview)
**Feedback**: Toast, MessageBar, ProgressBar, Spinner, Skeleton
**Surfaces**: Menu, Toolbar, Overflow

## Common Patterns

### App Shell Layout

```jsx
const useStyles = makeStyles({
  app: {
    backgroundColor: tokens.colorNeutralBackground1,
    display: "grid",
    gridTemplateColumns: "1fr",
    gridTemplateRows: "auto 1fr auto",
    height: "100vh",
    width: "100%",
  },
  header: {
    borderBottom: `${tokens.strokeWidthThin} solid ${tokens.colorNeutralStroke1}`,
    paddingTop: tokens.spacingVerticalS,
    paddingBottom: tokens.spacingVerticalS,
    paddingLeft: tokens.spacingHorizontalM,
    paddingRight: tokens.spacingHorizontalM,
  },
  content: {
    display: "grid",
    gridTemplateColumns: "280px 1fr",
    overflow: "hidden",
  },
  nav: {
    borderRight: `${tokens.strokeWidthThin} solid ${tokens.colorNeutralStroke1}`,
    overflowY: "auto",
  },
  main: {
    overflowY: "auto",
    paddingLeft: tokens.spacingHorizontalL,
    paddingRight: tokens.spacingHorizontalL,
    paddingTop: tokens.spacingVerticalL,
    paddingBottom: tokens.spacingVerticalL,
  },
});
```

### Custom Brand Theme

```jsx
import { createLightTheme, createDarkTheme } from "@fluentui/react-components";

const myBrand = {
  10: "#020305", 20: "#111723", 30: "#16263D",
  40: "#193253", 50: "#1B3F6A", 60: "#1B4C82",
  70: "#18599B", 80: "#1267B4", 90: "#3174C2",
  100: "#4F82C8", 110: "#6790CF", 120: "#7F9ED5",
  130: "#96ADDC", 140: "#ADBCE3", 150: "#C4CBE9",
  160: "#DBDBF0",
};

const lightTheme = createLightTheme(myBrand);
const darkTheme = createDarkTheme(myBrand);
```

### Dark Mode Toggle

```jsx
function App() {
  const [isDark, setIsDark] = useState(false);
  return (
    <FluentProvider theme={isDark ? webDarkTheme : webLightTheme}>
      <Switch
        label="Dark mode"
        checked={isDark}
        onChange={(_, data) => setIsDark(data.checked)}
      />
    </FluentProvider>
  );
}
```

## Anti-Patterns

- ❌ Hardcoded colors (`color: "#333"`) — use `tokens.colorNeutralForeground1`
- ❌ CSS shorthand properties in `makeStyles` (`border: "1px solid red"`) — use longhand or `shorthands.*`
- ❌ String concatenation of classNames — use `mergeClasses()`
- ❌ Inline `style` props for token-based values — use `makeStyles` with `tokens`
- ❌ Importing from `@fluentui/react` (v8) in v9 projects — use `@fluentui/react-components`
- ❌ Using v8 `Stack` — use CSS Grid or Flexbox
- ❌ Overriding CSS custom properties from the color system directly in CSS — the adaptive color system is JS-driven
- ❌ Removing focus indicators — accessibility requirement
