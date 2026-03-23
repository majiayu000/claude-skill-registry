---
name: stitch-mcp-create-design-system
description: Creates a reusable Stitch Design System from theme tokens — colors, fonts, roundness, saturation. Can be applied to future screens for visual consistency.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Create Design System

Creates a new Stitch Design System — a reusable theme configuration that can be applied to any screen. This bridges the gap between local CSS token extraction (via `stitch-design-system`) and Stitch-native design tokens that persist across generations.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

## When to use

- After extracting CSS tokens via `stitch-design-system` and wanting to persist them in Stitch
- User wants consistent theming across multiple screens or projects
- The orchestrator's Step 7 offers to create a Stitch Design System from extracted tokens
- User explicitly asks to create a design system in Stitch

## Call the MCP tool

```json
{
  "name": "create_design_system",
  "arguments": {
    "designSystem": {
      "displayName": "SaaS Dashboard Theme",
      "theme": {
        "colorMode": "LIGHT",
        "font": "DM_SANS",
        "roundness": "ROUND_EIGHT",
        "saturation": 3,
        "customColor": "#6366F1",
        "backgroundLight": "#FFFFFF",
        "backgroundDark": "#18181B",
        "description": "Professional SaaS aesthetic — clean, indigo accent, airy spacing"
      },
      "designTokens": "--color-primary: #6366F1;\n--color-bg: #FFFFFF;\n--font-family: 'DM Sans';",
      "styleGuidelines": "Use indigo for interactive elements. Gray-50 backgrounds for cards. 8px border radius."
    },
    "projectId": "3780309359108792857"
  }
}
```

## Parameter reference

### `designSystem` — required object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `displayName` | string | Yes | Human-readable name for the design system |
| `theme` | DesignTheme | Yes | Visual configuration — see below |
| `designTokens` | string | No | CSS custom properties or token definitions |
| `styleGuidelines` | string | No | Natural-language design rules |

### `theme` (DesignTheme) — the visual configuration

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `colorMode` | enum | `LIGHT`, `DARK` | Base appearance mode |
| `font` | enum | See font list below | Primary typeface |
| `roundness` | enum | `ROUND_FOUR`, `ROUND_EIGHT`, `ROUND_TWELVE`, `ROUND_FULL` | Border radius scale |
| `saturation` | int | 1–4 | Color vibrancy (1 = muted, 4 = vivid) |
| `customColor` | string | Hex color | Primary brand color |
| `backgroundLight` | string | Hex color | Light mode background |
| `backgroundDark` | string | Hex color | Dark mode background |
| `preset` | string | — | Optional preset theme name |
| `description` | string | — | Brief aesthetic description |

### Available fonts (28 options)

**Sans-serif:** `INTER`, `DM_SANS`, `GEIST`, `SORA`, `MANROPE`, `RUBIK`, `MONTSERRAT`, `WORK_SANS`, `SPACE_GROTESK`, `PLUS_JAKARTA_SANS`, `PUBLIC_SANS`, `SOURCE_SANS_THREE`, `NUNITO_SANS`, `ARIMO`, `HANKEN_GROTESK`, `IBM_PLEX_SANS`, `SPLINE_SANS`, `LEXEND`, `EPILOGUE`, `BE_VIETNAM_PRO`, `METROPOLIS`

**Serif:** `NOTO_SERIF`, `NEWSREADER`, `DOMINE`, `LIBRE_CASLON_TEXT`, `EB_GARAMOND`, `LITERATA`, `SOURCE_SERIF_FOUR`

### `projectId` — optional, numeric only

```
✅ "3780309359108792857"
❌ "projects/3780309359108792857"
```

If provided, associates the design system with a specific project. If omitted, creates a global design system.

## Mapping CSS tokens to DesignTheme

When creating from extracted `design-tokens.css`:

| CSS Variable | → DesignTheme field |
|---|---|
| `--color-primary` | `customColor` |
| `--color-bg` or `--bg-light` | `backgroundLight` |
| `--bg-dark` | `backgroundDark` |
| `--font-family` | `font` (map to closest enum value) |
| `--radius` or `--border-radius` | `roundness` (4px→FOUR, 8px→EIGHT, 12px→TWELVE, 16px+→FULL) |

## Output

Returns an Asset object with a `name` field — **store this** for future `update_design_system` and `apply_design_system` calls:

```json
{
  "name": "assets/ds_abc123",
  "displayName": "SaaS Dashboard Theme",
  "designSystem": { ... }
}
```

## After creating

- Store the `name` value (e.g., `assets/ds_abc123`) — you'll need it for apply/update
- Offer: "Apply this design system to existing screens?" → `stitch-mcp-apply-design-system`
- The orchestrator stores this for automatic application in Step 5b
