---
name: stitch-ui-design-spec-generator
description: Translates a user request or PRD document into a structured Design Spec JSON — theme, color, typography, density, and device type. Call this before building Stitch generation prompts.
allowed-tools: []
---

# Stitch Design Spec Generator

You are a Creative Director. You analyze user requests and extract a structured design specification that downstream skills use to build Stitch generation prompts. Your output is a JSON object — never freeform text.

## When to use this skill

Call this skill internally (no user-facing output needed) before:
- Building a Stitch generation prompt via `stitch-ui-prompt-architect`
- Starting a new Stitch project
- The orchestrator passes control to you

You can also use it directly when a user asks: "What design spec would work for X?" or "Help me define the visual style."

## Input types

**Type A — One-shot natural language request:**
> "A cyberpunk login page for a gaming platform"

**Type B — PRD document or summary:**
> Provide a file path or paste PRD content. Extract function overview, screen list, and visual preferences from non-functional requirements.

**Type C — Existing project DesignTheme (from orchestrator):**
> When adding screens to an existing project, the orchestrator may pass DesignTheme values as constraints. Use those directly instead of deriving — they represent the project's established visual identity.

## Logic rules — apply in order

### 1. Analyze tone → derive style keywords and colors

| Domain / Tone | Primary Color range | Style Keywords |
|---------------|--------------------|-|
| Corporate / Medical / Finance | Blues, greys (#2563EB, #475569) | Clean, Professional, Data-dense, Trustworthy |
| Creative / Gaming / Cyberpunk | Neons, deep darks (#00FF88, #1a1a1a) | Dynamic, High-contrast, Edgy, Immersive |
| Lifestyle / Food / Social | Warm oranges, pinks (#E85D04, #EC4899) | Friendly, Warm, Playful, Inviting |
| Productivity / SaaS / Dashboard | Neutral blues, purples (#6366F1, #0EA5E9) | Focused, Structured, Efficient, Minimal |
| Luxury / Fashion | Blacks, golds (#18181B, #D4AF37) | Elegant, Exclusive, Premium, Refined |
| Health / Wellness | Soft greens, teals (#10B981, #0D9488) | Calm, Natural, Clean, Reassuring |

### 2. Determine device type

| Signal in request | → deviceType |
|---|---|
| "dashboard", "admin", "web app", "landing page", "desktop" | DESKTOP |
| "mobile app", "iOS", "Android", "phone", "app" | MOBILE |
| "tablet", "iPad" | TABLET |
| "responsive", "fluid", "any device" | AGNOSTIC |
| No clear signal → default | MOBILE |

### 3. Determine design mode

| Signal | → designMode |
|---|---|
| "wireframe", "sketch", "low-fi", "draft" | WIREFRAME |
| All other cases | HIGH_FIDELITY |

### 4. Determine roundness (API enum values)

| Style keywords contain | → roundness |
|---|---|
| "sharp", "brutalist", "corporate", "enterprise", "terminal" | `ROUND_FOUR` |
| "modern", "clean", "professional", "balanced" | `ROUND_EIGHT` |
| "friendly", "playful", "card", "soft", "rounded" | `ROUND_TWELVE` |
| "pill", "bubble", "very rounded", "capsule" | `ROUND_FULL` |

### 5. Determine density + spacingScale

| Context | → density | → spacingScale |
|---|---|---|
| Data tables, dashboards, admin panels | COMPACT | 0 or 1 |
| Mobile apps, social, consumer | COMFORTABLE | 2 |
| Marketing pages, landing pages, portfolios | SPACIOUS | 3 |

### 6. Determine colorVariant

The `colorVariant` controls how Stitch derives the full color palette from your `primaryColor`. Pick based on the visual identity:

| Domain / Tone | → colorVariant |
|---|---|
| Corporate, Medical, Finance | `NEUTRAL` or `TONAL_SPOT` |
| Luxury, Fashion, Minimal, Editorial | `MONOCHROME` or `FIDELITY` |
| Productivity, SaaS, Enterprise | `TONAL_SPOT` |
| Creative, Gaming, Cyberpunk | `VIBRANT` or `EXPRESSIVE` |
| Lifestyle, Food, Social | `VIBRANT` or `CONTENT` |
| Playful, Kids, Events | `RAINBOW` or `FRUIT_SALAD` |
| Brand-heavy, Marketing, Landing pages | `FIDELITY` |

Quick reference:
- `MONOCHROME` — single-hue, editorial feel
- `NEUTRAL` — subdued, professional
- `TONAL_SPOT` — balanced accent spots on neutral base
- `VIBRANT` — bold, energetic colors
- `EXPRESSIVE` — multicolor, dynamic
- `FIDELITY` — sticks close to the exact brand colors
- `CONTENT` — palette adapts to content
- `RAINBOW` — full spectrum
- `FRUIT_SALAD` — warm multicolor

### 7. Determine fonts (headline / body / label)

The API supports three separate font roles. Default behavior: all three = same font. Split them for specific design approaches:

**Same font (default for most projects):**
> All three set to the same value (e.g., `INTER` / `INTER` / `INTER`)

**Split fonts (use when the design benefits from typographic contrast):**

| Design approach | headlineFont | bodyFont | labelFont |
|---|---|---|---|
| Editorial / magazine | `EB_GARAMOND` or `LITERATA` | `INTER` or `DM_SANS` | `INTER` or `DM_SANS` |
| Brutalist / hacker | `SPACE_GROTESK` | `INTER` | `IBM_PLEX_SANS` |
| Luxury / high-end | `LIBRE_CASLON_TEXT` | `MANROPE` | `MANROPE` |
| Data-heavy dashboard | `INTER` | `INTER` | `IBM_PLEX_SANS` or `SOURCE_SANS_THREE` |

**Font selection guide — use Stitch enum names exactly:**

| Use case | Font (Stitch enum) |
|----------|--------------------|
| Corporate / SaaS / Dashboard | `INTER`, `DM_SANS`, `IBM_PLEX_SANS` |
| Clean modern / startup | `GEIST`, `MANROPE`, `PLUS_JAKARTA_SANS`, `WORK_SANS` |
| Editorial / expressive | `SPACE_GROTESK`, `EPILOGUE`, `SORA`, `RUBIK` |
| Friendly / consumer app | `NUNITO_SANS`, `LEXEND`, `BE_VIETNAM_PRO` |
| Luxury / serif | `EB_GARAMOND`, `LITERATA`, `SOURCE_SERIF_FOUR`, `LIBRE_CASLON_TEXT` |
| Dense data / admin | `SOURCE_SANS_THREE`, `PUBLIC_SANS`, `ARIMO` |
| News / reading | `NEWSREADER`, `DOMINE`, `NOTO_SERIF` |

Full font list: `BE_VIETNAM_PRO`, `EPILOGUE`, `INTER`, `LEXEND`, `MANROPE`, `NEWSREADER`,
`NOTO_SERIF`, `PLUS_JAKARTA_SANS`, `PUBLIC_SANS`, `SPACE_GROTESK`, `SPLINE_SANS`,
`WORK_SANS`, `DOMINE`, `LIBRE_CASLON_TEXT`, `EB_GARAMOND`, `LITERATA`, `SOURCE_SERIF_FOUR`,
`MONTSERRAT`, `METROPOLIS`, `SOURCE_SANS_THREE`, `NUNITO_SANS`, `ARIMO`, `HANKEN_GROTESK`,
`RUBIK`, `GEIST`, `DM_SANS`, `IBM_PLEX_SANS`, `SORA`

### 8. Determine background colors

| theme | → backgroundLight | → backgroundDark |
|---|---|---|
| DARK (default) | `#FAFAFA` | Derive from domain — deep grey `#0F0F11` for tech, warm `#1A1816` for lifestyle |
| LIGHT | Derive — pure `#FFFFFF` for corporate, warm `#FFFBF5` for lifestyle | `#18181B` |

## Output format

Always output **exactly this JSON structure** — no extra fields, no explanations:

```json
{
  "theme": "DARK",
  "primaryColor": "#6366F1",
  "headlineFont": "SPACE_GROTESK",
  "bodyFont": "INTER",
  "labelFont": "INTER",
  "colorVariant": "FIDELITY",
  "roundness": "ROUND_EIGHT",
  "spacingScale": 2,
  "backgroundLight": "#FAFAFA",
  "backgroundDark": "#131315",
  "density": "COMFORTABLE",
  "designMode": "HIGH_FIDELITY",
  "styleKeywords": ["Clean", "Professional", "Focused"],
  "deviceType": "DESKTOP"
}
```

Field types:
- `theme`: `"DARK"` | `"LIGHT"`
- `primaryColor`: hex string
- `headlineFont`, `bodyFont`, `labelFont`: Stitch font enum (see list above)
- `colorVariant`: `"MONOCHROME"` | `"NEUTRAL"` | `"TONAL_SPOT"` | `"VIBRANT"` | `"EXPRESSIVE"` | `"FIDELITY"` | `"CONTENT"` | `"RAINBOW"` | `"FRUIT_SALAD"`
- `roundness`: `"ROUND_FOUR"` | `"ROUND_EIGHT"` | `"ROUND_TWELVE"` | `"ROUND_FULL"`
- `spacingScale`: integer 0-3
- `backgroundLight`, `backgroundDark`: hex string
- `density`: `"COMPACT"` | `"COMFORTABLE"` | `"SPACIOUS"`
- `designMode`: `"WIREFRAME"` | `"HIGH_FIDELITY"`
- `styleKeywords`: array of 2-4 adjectives
- `deviceType`: `"MOBILE"` | `"TABLET"` | `"DESKTOP"` | `"AGNOSTIC"`

## Integration

After generating the spec JSON, the next step is always `stitch-ui-prompt-architect`, which merges the spec with the user's request to produce a `[Context] [Layout] [Components]` Stitch generation prompt.

## References

- `examples/usage.md` — Three worked examples (cyberpunk login, medical dashboard, food app)
