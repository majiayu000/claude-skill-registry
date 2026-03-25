---
name: stitch-mcp-get-project
description: Retrieves metadata for a specific Stitch project — title, theme, create/update time. Use to inspect a project before generating new screens. Do NOT use this if you already have a screenId — use stitch-mcp-get-screen instead.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Get Project

Retrieves full metadata for a specific Stitch project. Useful for understanding an existing project's theme and screen list before generating additional screens.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

**Do NOT call this if you already have both `projectId` AND `screenId`.** In that case, call `stitch-mcp-get-screen` directly — it's more efficient.

## When to use

- User provides a Stitch project URL and you need its details
- You need to know the existing design theme before generating new consistent screens
- Verifying a project exists before proceeding

## Step 1: Parse the project ID from context

The user may provide the project reference in several formats — always extract to the `projects/ID` format:

| Input format | → Argument for `get_project` |
|---|---|
| `3780309359108792857` (numeric) | `projects/3780309359108792857` |
| `projects/3780309359108792857` | `projects/3780309359108792857` (use as-is) |
| `https://stitch.withgoogle.com/projects/3780309359108792857` | Extract ID → `projects/3780309359108792857` |

## Step 2: Call the MCP tool

```json
{
  "name": "get_project",
  "arguments": {
    "name": "projects/3780309359108792857"
  }
}
```

## Output schema

```json
{
  "name": "projects/3780309359108792857",
  "title": "Analytics Dashboard",
  "createTime": "2024-11-10T09:00:00Z",
  "updateTime": "2024-11-15T10:30:00Z",
  "deviceType": "PHONE",
  "visibility": "PRIVATE",
  "projectType": "TEXT_TO_UI",
  "origin": "STITCH",
  "metadata": {
    "isRemixed": false,
    "userRole": "OWNER"
  },
  "designTheme": {
    "colorMode": "LIGHT",
    "customColor": "#6366F1",
    "colorVariant": "TONAL_SPOT",
    "roundness": "ROUND_TWELVE",
    "spacingScale": 1,
    "headlineFont": "ROBOTO",
    "bodyFont": "ROBOTO",
    "labelFont": "ROBOTO",
    "font": "ROBOTO",
    "namedColors": {
      "primary": "#5B5FC7",
      "on_primary": "#FFFFFF",
      "primary_container": "#E1DFFF",
      "on_primary_container": "#414594",
      "secondary": "#5C5D72",
      "on_secondary": "#FFFFFF",
      "tertiary": "#785572",
      "on_tertiary": "#FFFFFF",
      "surface": "#FBF8FF",
      "on_surface": "#1B1B21",
      "surface_container": "#EFEDF5",
      "surface_container_low": "#F5F2FA",
      "surface_container_high": "#E9E7EF",
      "outline": "#777680",
      "error": "#BA1A1A",
      "on_error": "#FFFFFF"
    },
    "overridePrimaryColor": "",
    "overrideSecondaryColor": "",
    "overrideTertiaryColor": "",
    "overrideNeutralColor": "",
    "backgroundLight": "#FBF8FF",
    "backgroundDark": "#131316",
    "description": "Modern indigo-toned interface with clean surfaces",
    "designMd": "# Design System\n\n## Color Palette\n..."
  },
  "screenInstances": [
    {
      "name": "projects/3780309359108792857/screens/88805...",
      "id": "88805...",
      "sourceScreen": "screens/88805...",
      "type": "SCREEN_INSTANCE",
      "width": 412,
      "height": 892,
      "x": 0,
      "y": 0,
      "hidden": false
    },
    {
      "name": "projects/3780309359108792857/screens/99901...",
      "id": "99901...",
      "sourceScreen": "screens/99901...",
      "type": "DESIGN_SYSTEM_INSTANCE",
      "width": 412,
      "height": 892,
      "x": 500,
      "y": 0,
      "hidden": false,
      "sourceAsset": "assets/design-system-123"
    }
  ]
}
```

> `designMd` is truncated above — in practice it's a full auto-generated design system doc (often 500+ lines). `namedColors` typically contains 40+ semantic tokens; only the most common are shown here.

## DesignTheme field reference

| Field | Type | Values / Notes |
|-------|------|----------------|
| `colorMode` | enum | `LIGHT`, `DARK` |
| `customColor` | string | Hex seed color (e.g. `#6366F1`). This is the color seed — NOT called `primaryColor` |
| `colorVariant` | enum | `MONOCHROME`, `NEUTRAL`, `TONAL_SPOT`, `VIBRANT`, `EXPRESSIVE`, `FIDELITY`, `CONTENT`, `RAINBOW`, `FRUIT_SALAD` |
| `roundness` | enum | `ROUND_FOUR`, `ROUND_EIGHT`, `ROUND_TWELVE`, `ROUND_FULL` |
| `spacingScale` | number | `0`–`3` (density multiplier) |
| `headlineFont` | enum | 28-font set: `ROBOTO`, `OPEN_SANS`, `LATO`, `MONTSERRAT`, `POPPINS`, `INTER`, `PLAYFAIR_DISPLAY`, `MERRIWEATHER`, `RALEWAY`, `NUNITO`, `SOURCE_SANS_3`, `OSWALD`, `QUICKSAND`, `CABIN`, `BARLOW`, `WORK_SANS`, `DM_SANS`, `SPACE_GROTESK`, `SORA`, `OUTFIT`, `PLUS_JAKARTA_SANS`, `MANROPE`, `ALBERT_SANS`, `FIGTREE`, `GEIST`, `ONEST`, `INSTRUMENT_SANS`, `GENERAL_SANS` |
| `bodyFont` | enum | Same 28-font set |
| `labelFont` | enum | Same 28-font set |
| `font` | enum | **Deprecated** — legacy single-font field, same enum |
| `namedColors` | object | 40+ semantic color tokens (`primary`, `on_primary`, `surface`, `surface_container`, `outline`, `error`, etc.) |
| `overridePrimaryColor` | string | Hex override, empty string if unused |
| `overrideSecondaryColor` | string | Hex override, empty string if unused |
| `overrideTertiaryColor` | string | Hex override, empty string if unused |
| `overrideNeutralColor` | string | Hex override, empty string if unused |
| `backgroundLight` | string | Hex background for light mode |
| `backgroundDark` | string | Hex background for dark mode |
| `description` | string | Brief aesthetic description of the theme |
| `designMd` | string | Auto-generated design system markdown — the full token spec. Can be very long |

## Project-level fields

| Field | Type | Values / Notes |
|-------|------|----------------|
| `deviceType` | string | `PHONE`, `TABLET`, `DESKTOP`, etc. |
| `visibility` | enum | `PRIVATE`, `PUBLIC` |
| `projectType` | enum | `TEXT_TO_UI`, `PROJECT_DESIGN`, etc. |
| `origin` | enum | `STITCH`, `IMPORTED_FROM_GALILEO` |
| `metadata.isRemixed` | boolean | Whether this project was remixed from another |
| `metadata.userRole` | string | `OWNER`, `VIEWER`, etc. |

## ScreenInstance fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Numeric screen ID |
| `sourceScreen` | string | Path reference to the source screen |
| `type` | enum | `SCREEN_INSTANCE`, `DESIGN_SYSTEM_INSTANCE`, `GROUP_INSTANCE` |
| `width` / `height` | number | Pixel dimensions |
| `x` / `y` | number | Canvas position |
| `hidden` | boolean | Whether hidden in the project |
| `sourceAsset` | string | Present on `DESIGN_SYSTEM_INSTANCE` types — references the design system asset |

## Using the theme data

Use `designMd` and `namedColors` when generating new screens — they contain the authoritative design system for this project. Pass `namedColors` to `stitch-design-system` for instant token extraction.

## After getting the project

- Note the `designTheme` — use it to keep new screens visually consistent
- Note the `screenInstances` list — extract screenId values if you need to inspect specific screens
- Use `stitch-mcp-list-screens` for a richer view of the screen list including thumbnails
