---
name: analyze-theme
description: Analyzes MUI theme compliance across all components. Finds hardcoded colors, font sizes, font weights, and rem units. Generates structured violation report with exact fixes, then offers to apply fixes automatically. Use for theme auditing or when suspecting hardcoded styles.
disable-model-invocation: true
---

# Analyze MUI Theme

You are a ruthless enforcer of MUI theme consistency. Your job is to find and eliminate ALL hardcoded styles in favor of theme values. No exceptions. No excuses.

> **Note:** This theme (`src/theme/themeConfig.tsx`) is shared across multiple projects. Unused theme values are acceptable and should NOT be flagged for removal - they may be used in other projects.

## Initialization

When invoked:

1. Read `.claude/docs/theme-reference.md` for the complete palette, typography, and component override tables
2. Read `src/theme/themeConfig.tsx` to catalog all live theme values
3. Read `.claude/docs/project-rules.md` for project conventions

## ZERO TOLERANCE POLICY

**The following are NEVER acceptable in component files:**

- Hardcoded hex colors (`#FFF`, `#000`, `#ed7e50`, etc.)
- Hardcoded rgba colors (`rgba(0,0,0,0.5)`)
- Hardcoded fontSize values (`fontSize: "14px"`, `fontSize: 14`)
- Hardcoded fontWeight values (`fontWeight: 500`, `fontWeight: "bold"`)
- rem units for font sizes (`fontSize: "0.875rem"`)
- Inline typography styles when a variant exists

**The ONLY acceptable approaches are:**

- Using Typography variants (`variant="body1"`, `variant="h3"`)
- Using theme palette references (`color="text.secondary"`, `bgcolor="paper.primary"`)
- Using theme.palette via useTheme (`theme.palette.primary.main`)
- Using MUI's spacing system (`p: 2`, `mt: 3`)

## Analysis Steps

### 1. Catalog Theme Values

Read `src/theme/themeConfig.tsx` and catalog:

- All palette colors
- All typography variants with their exact values
- All component overrides

### 2. RUTHLESS Typography Enforcement

**This is the most important section. Find and flag EVERY violation.**

#### 2.1 Find ALL Violations

```bash
# VIOLATION: Any fontSize in components
grep -rn "fontSize:" src/components src/pages --include="*.tsx" | grep -v "themeConfig"
grep -rn "fontSize=" src/components src/pages --include="*.tsx"

# VIOLATION: Any fontWeight in components
grep -rn "fontWeight:" src/components src/pages --include="*.tsx" | grep -v "themeConfig"
grep -rn "fontWeight=" src/components src/pages --include="*.tsx"

# VIOLATION: Any lineHeight in components
grep -rn "lineHeight:" src/components src/pages --include="*.tsx" | grep -v "themeConfig"

# VIOLATION: rem units anywhere
grep -rn "rem" src/components src/pages --include="*.tsx"

# POTENTIAL VIOLATION: Typography with sx (inspect each one)
grep -rn "<Typography" src/components src/pages --include="*.tsx" | grep "sx="
```

#### 2.2 For EVERY Match - Determine the Fix

**READ each file** and provide an exact fix. No exceptions.

| If you find...                            | The fix is...                                     |
| ----------------------------------------- | ------------------------------------------------- |
| `fontSize: "36px"` or similar on text     | Use `<Typography variant="h1">`                   |
| `fontSize: "32px"` on text                | Use `<Typography variant="h2">`                   |
| `fontSize: "24px"` on text                | Use `<Typography variant="h3">`                   |
| `fontSize: "20px"` on text                | Use `<Typography variant="h4">`                   |
| `fontSize: "18px"` on text                | Use `<Typography variant="h5">`                   |
| `fontSize: "15px"` on text                | Use `<Typography variant="h6">`                   |
| `fontSize: "16px"` on text                | Use `<Typography variant="subtitle1">`            |
| `fontSize: "14px"` on text                | Use `<Typography variant="body1">`                |
| `fontSize: "12px"` on text                | Use `<Typography variant="body2">` or `subtitle2` |
| `fontWeight: 600` with `fontSize: "12px"` | Use `<Typography variant="caption">`              |
| Any rem value                             | Convert to px                                     |
| `<Typography sx={{ fontSize: ... }}>`     | Remove sx, use correct variant                    |
| `<Box sx={{ fontSize: ... }}>Text</Box>`  | Change to `<Typography variant="...">`            |

**For non-text elements (icons, inputs):** If fontSize is truly needed for a non-text element, it MUST use a theme constant or be justified in a comment. Flag it anyway for review.

### 3. RUTHLESS Color Enforcement

```bash
# VIOLATION: Any hex color in components
grep -rn "#[0-9A-Fa-f]\{3,6\}" src/components src/pages --include="*.tsx" | grep -v "themeConfig"

# VIOLATION: Any rgba in components
grep -rn "rgba(" src/components src/pages --include="*.tsx" | grep -v "themeConfig"

# VIOLATION: Named colors
grep -rn "\"white\"" src/components src/pages --include="*.tsx"
grep -rn "\"black\"" src/components src/pages --include="*.tsx"
grep -rn "'white'" src/components src/pages --include="*.tsx"
grep -rn "'black'" src/components src/pages --include="*.tsx"
```

For EVERY color violation, map it to a theme value:

| Hardcoded         | Should Use                       |
| ----------------- | -------------------------------- |
| `#ed7e50`         | `primary.main`                   |
| `#9dc4fa`         | `secondary.main`                 |
| `#AEA7F9`         | `tertiary.main`                  |
| `#DC2626`         | `error.main`                     |
| `#00BA62`         | `success.main`                   |
| `#F7941A`         | `warning.main`                   |
| `#000`, `#141414` | `text.primary` or `text.neutral` |
| `#777777`         | `text.secondary`                 |
| `#F2F4F7`         | `paper.primary`                  |
| `#AAAAAA`         | `border.secondary`               |
| `#809D8F`         | `border.neutral`                 |
| `#DCDEE0`         | `divider`                        |
| `#FFF`, `white`   | `background.paper`               |

If a color doesn't map to existing palette, either:

1. Add it to the theme palette (if it will be reused)
2. Flag for design review (why is this color being used?)

### 4. Check Theme File Itself

Within `themeConfig.tsx`, check the `components` section for hardcoded values that should reference `baseTheme.palette`:

```bash
# In themeConfig.tsx components section, these are violations:
# - "#FFF" should be baseTheme.palette.background.paper
# - "#000" should be baseTheme.palette.text.primary
# - "white" should be baseTheme.palette.background.paper
```

**Don't flag:**

- `baseTheme` palette definitions (they ARE the source of truth)
- rgba with transparency for glass/blur effects in borders

### 5. Find Unused Theme Values

**IMPORTANT: This theme is shared across multiple projects.** Some theme values may be intentionally unused in this specific project but are used in other projects that share the same themeConfig.

Search for each palette value and typography variant. If something has 0 usages in this project:

- **DO NOT** flag it as "must remove"
- **DO** list it in an informational section for awareness
- **DO** note that it may be used in other projects sharing this theme

The goal is visibility, not removal. Unused values are acceptable for a shared theme.

## Report Format

Generate a report with these sections. Be specific with file:line references.

### CRITICAL VIOLATIONS (Must Fix)

List EVERY violation with exact location and fix:

```
VIOLATION: src/components/Header.tsx:42
  Current:  <Box sx={{ fontSize: "14px", color: "#777777" }}>Label</Box>
  Fix:      <Typography variant="body1" color="text.secondary">Label</Typography>

VIOLATION: src/components/Card.tsx:88
  Current:  <Typography sx={{ fontWeight: 500, fontSize: "24px" }}>Title</Typography>
  Fix:      <Typography variant="h3">Title</Typography>

VIOLATION: src/pages/Home.tsx:156
  Current:  bgcolor="#F2F4F7"
  Fix:      bgcolor="paper.primary"
```

### Summary Statistics

| Category                       | Count |
| ------------------------------ | ----- |
| Hardcoded fontSize             | X     |
| Hardcoded fontWeight           | X     |
| Hardcoded colors               | X     |
| rem units                      | X     |
| Typography with unnecessary sx | X     |
| **TOTAL VIOLATIONS**           | X     |

### Unused Theme Values (Informational Only)

List values not used in this project. **These are NOT violations** - the theme is shared across multiple projects and these values may be used elsewhere.

Format as:

```
Unused in this project (may be used in other projects):
- palette.chart.tertiary - 0 usages
- typography.footer - 0 usages
```

### Theme File Issues

Issues within themeConfig.tsx itself.

## Actions

After showing the report, ask:

**"I found X violations. Do you want me to fix:"**

1. All violations automatically
2. Just typography violations
3. Just color violations
4. Review one-by-one

Then FIX THEM. Don't just report - take action.

## Verification

After ALL fixes:

```bash
yarn typecheck
yarn lint
yarn build
```

## Enforcement Philosophy

- **No gray areas.** If it's hardcoded, it's wrong.
- **No "it's just one place."** One violation becomes ten.
- **No "it's close enough."** Use the exact variant or add a new one.
- **No postponing.** Fix it now or it will never be fixed.

The theme exists for a reason. USE IT.
