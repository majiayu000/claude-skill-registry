---
name: brand-kit-playground
description: >
  Generate an interactive HTML brand playground that shows your brand rendered
  live — palette, typography, logo, voice — with a social card and OG image
  preview that updates as you tweak tokens. Opens in browser. The visual
  approval step for the /cmo flow: /visual-style writes the brand, this skill
  shows it. Use when the user says "show me my brand", "brand playground",
  "preview my brand", "what does our brand look like", "visual preview",
  "brand kit", "see my colors", "how does my brand look", or after /visual-style
  completes and the user needs to approve the visual identity before moving to
  content generation. Also use when someone says "I want to see it" during any
  brand-building conversation.
reads:
  - brand/creative-kit.md
  - brand/voice-profile.md
  - brand/positioning.md
  - brand/audience.md
writes:
  - brand/creative-kit.md
  - brand/assets.md
depends-on:
  - visual-style
triggers:
  - brand playground
  - show me my brand
  - preview my brand
  - what does our brand look like
  - visual preview
  - brand kit
  - see my colors
  - how does my brand look
  - brand kit playground
  - render my brand
allowed-tools:
  - Bash(open *)
---

# /brand-kit-playground — Visual Brand Workbench

Your brand lives in markdown files. This skill renders it as a living, interactive HTML page the user opens in their browser — palette swatches, type specimens, logo lockups, and a real social card preview that updates as they tweak tokens. When they're happy, they copy the structured JSON and you write it back to `brand/creative-kit.md`.

This is the visual approval step in the /cmo flow. `/visual-style` writes the brand identity. This skill shows it.

---

## On Activation

1. Read `brand/creative-kit.md` — extract the Colors, Typography, and Visual Brand Style sections.
   - If the file is template/empty: **warn** the user. "Your creative kit is empty — the playground will use placeholder values. Run `/visual-style` first for a real preview, or continue and I'll use defaults you can tweak."
   - If it has real content: proceed. Parse colors (hex values), fonts (family names), border radius, shadows, gradients.
2. Read `brand/voice-profile.md` — extract tone adjectives, vocabulary preferences, headline style.
3. Read `brand/positioning.md` — extract the primary positioning angle for the social card headline.
4. Read `brand/audience.md` if it exists — extract audience description for the voice snapshot panel.
5. If no brand files exist at all: proceed with sensible defaults. The playground works at L0. Show placeholder brand with a note: "These are defaults. Fill in your brand files and re-run for a real preview."

---

## What You Build

A **single self-contained HTML file** with inline CSS and JS. Zero external dependencies except Google Fonts (loaded via `<link>`). No framework. No build step. No server.

The file is written to the project root as `brand-playground.html` and opened in the user's default browser via `open brand-playground.html`.

### Layout

```
+-- BRAND BAR ------------------------------------------------+
|  [Logo] Project Name Brand Playground    [Light/Dark toggle] |
+--------------------------------------------------------------+
|                    |                                          |
|  CONTROLS          |  TAB: [Brand System] [Social Card] [OG] |
|  --------          |  ----------------------------------------|
|                    |                                          |
|  > Colors          |  (Brand System tab)                     |
|    Primary [pick]  |  COLOR PALETTE                          |
|    Secondary       |  ## ## ## ## ## (live swatches)          |
|    Accent          |                                         |
|                    |  TYPOGRAPHY                             |
|  > Typography      |  Display: Aa Space Grotesk              |
|    Display font    |  Body: Aa Inter Regular                 |
|    Body font       |  Mono: Aa JetBrains Mono               |
|    Scale ratio     |                                         |
|                    |  VOICE SNAPSHOT                         |
|  > Visual Style    |  Tone: confident, warm, technical       |
|    Border radius   |  Audience: indie developers             |
|    Shadow depth    |  Style: short-punchy headlines          |
|    Texture         |                                         |
|                    |  (Social Card tab)                      |
|  > Social Card     |  +---------------------------+          |
|    Headline        |  |                           |          |
|    Subhead         |  |  We just shipped          |          |
|    Badge text      |  |  dark mode                |          |
|    Layout [v]      |  |                           |          |
|    Background [v]  |  |  [logo]          [NEW]    |          |
|                    |  |                           |          |
|  > Presets         |  +---------------------------+          |
|    Launch          |  1200x675 - Twitter/X                   |
|    Blog Post       |                                         |
|    Feature         |  MULTI-PREVIEW:                         |
|                    |  [Tw] [Li] [IG] [St]                    |
+--------------------+-----------------------------------------+
|  TOKEN OUTPUT (structured JSON)              [Copy Tokens]   |
+--------------------------------------------------------------+
```

### Three Tabs

**Tab 1: Brand System** — The identity overview. Color palette rendered as large swatches with hex values and contrast ratios. Typography specimens at the brand's modular scale. Logo lockups (primary, mark, on-dark) if logo paths exist in creative-kit.md. Voice snapshot showing tone, vocabulary, headline style from voice-profile.md.

**Tab 2: Social Card** — A live social card preview rendered with the brand tokens. The user types a headline, picks a layout variant (centered, split, overlay, minimal), chooses a background style (gradient, solid, dark, light). The card re-renders instantly. Below: a multi-preview strip showing the same card at Twitter (1200x675), LinkedIn (1200x627), Instagram (1080x1080), and Story (1080x1920) aspect ratios.

**Tab 3: OG Image** — Same pattern as social card but for OG images. Inputs: title, description, author, category tag. Layouts: editorial, minimal, bold. Target: 1200x630.

### Controls Panel (Left Side)

Controls are grouped by concern. Each group is collapsible. Controls update the preview instantly — no "Apply" button.

| Token | Control | Range |
|-------|---------|-------|
| Colors (primary, secondary, accent, background, foreground) | Color picker (native `<input type="color">`) | Any hex |
| Display font | Dropdown | 10 curated options + current brand font |
| Body font | Dropdown | 10 curated options + current brand font |
| Scale ratio | Slider | 1.125 (Major Second) to 1.5 (Perfect Fifth) |
| Border radius | Slider | 0px to 24px |
| Shadow depth | Slider | none / sm / md / lg / xl |
| Social card headline | Text input | Max 60 chars |
| Social card layout | Segmented buttons | Centered / Split / Overlay / Minimal |
| Social card background | Dropdown | Gradient / Solid / Dark / Light |

### Token Output (Bottom)

A `<pre>` block showing the current token state as structured JSON:

```json
{
  "colors": {
    "primary": "#6366F1",
    "primaryForeground": "#FFFFFF",
    "secondary": "#7C3AED",
    "accent": "#F59E0B",
    "background": "#FFFFFF",
    "foreground": "#0F172A"
  },
  "typography": {
    "display": { "family": "Space Grotesk", "weights": [700, 800] },
    "body": { "family": "Inter", "weights": [400, 500, 600] },
    "scale": { "base": 16, "ratio": 1.25 }
  },
  "visual": {
    "borderRadius": "8px",
    "shadowDepth": "md",
    "texture": "none"
  }
}
```

A "Copy Tokens" button copies this JSON to the clipboard. The user pastes it back into the conversation. The agent reads the JSON and updates `brand/creative-kit.md` accordingly.

### Presets

Include 3-5 presets that snap all controls to a cohesive combination:

| Preset | Vibe | Colors | Type | Visual |
|--------|------|--------|------|--------|
| **Tech Startup** | Clean, modern, confident | Indigo + violet + amber | Space Grotesk + Inter | 8px radius, md shadow |
| **Indie Maker** | Warm, approachable, fun | Coral + teal + gold | Instrument Serif + DM Sans | 12px radius, lg shadow |
| **Enterprise** | Precise, authoritative, refined | Navy + slate + emerald | General Sans + IBM Plex | 4px radius, sm shadow |
| **Creative Studio** | Bold, expressive, artistic | Hot pink + lime + black | Space Grotesk + Syne | 0px radius, none shadow |
| **From Brand** | Current creative-kit.md values | (extracted) | (extracted) | (extracted) |

The "From Brand" preset is always first and always selected on load. It represents the current brand state. Other presets are for exploration.

---

## How You Generate It

### Step 1: Extract Tokens

Parse `brand/creative-kit.md` into structured data. Look for:

- **Colors section**: hex values for primary, secondary, accent. If not found, derive from the first hex codes mentioned anywhere in the file.
- **Typography section**: font family names, weights. If Google Fonts, construct the `<link>` URL.
- **Visual Brand Style section**: aesthetic direction, lighting, composition notes. Use these to inform the playground's own aesthetic (dark mode vs light, gradient direction, texture).
- **Logo paths**: if mentioned, include as `<img>` tags in the brand system tab.

If parsing is ambiguous, use reasonable defaults and note what you assumed.

### Step 2: Write the HTML

Use the template structure from [references/html-architecture.md](references/html-architecture.md). The file should be 800-1500 lines depending on brand complexity. Key implementation details:

- All CSS as `<style>` in `<head>`. Brand tokens as CSS custom properties on `:root`.
- All JS as `<script>` before `</body>`. Single `state` object, single `updateAll()` function.
- Google Fonts loaded via `<link rel="stylesheet">` — this is the ONE external dependency.
- Dark/light toggle switches `:root` variables. Both themes use the brand palette.
- Social card renderer uses absolute positioning within a fixed-aspect-ratio container.
- Multi-preview strip uses CSS `transform: scale()` to show all sizes simultaneously.
- Color pickers use native `<input type="color">` — no library needed.
- Token output updates on every state change via `JSON.stringify(state.tokens, null, 2)`.
- Copy button uses `navigator.clipboard.writeText()`.

### Step 3: Open It

```bash
open brand-playground.html
```

Tell the user: "Your brand playground is open in the browser. Play with the controls — every change updates the preview instantly. When you're happy with how it looks, click 'Copy Tokens' and paste the JSON here. I'll update your brand files."

### Step 4: Process Feedback

When the user pastes the token JSON back:

1. Parse it.
2. Diff against current `brand/creative-kit.md` values.
3. Show the diff: "You changed primary from #6366F1 to #4F46E5 and increased border radius to 12px. Want me to update creative-kit.md?"
4. On confirmation, write the changes to the appropriate sections of `creative-kit.md`.
5. Log the update to `brand/assets.md`: "Brand playground session — updated colors and visual style."

---

## Integration with /cmo Flow

This skill slots into the /cmo foundation-building workflow:

```
/cmo activation
  -> mktg init (if needed)
  -> 3 research agents in parallel (brand, audience, competitors)
  -> /visual-style (writes creative-kit.md)
  -> /brand-kit-playground (renders creative-kit.md as interactive HTML)
     -> User tweaks in browser
     -> User copies tokens
     -> Agent updates creative-kit.md
  -> Continue to /image-gen, /creative, etc.
```

The playground is the **approval gate** between brand definition and brand execution. Before this skill existed, the user approved their visual identity by reading markdown. Now they see it rendered.

---

## Progressive Enhancement Levels

| Level | Context | Behavior |
|-------|---------|----------|
| **L0** | No brand files | Placeholder brand with defaults. Full functionality. Note: "These are defaults." |
| **L1** | creative-kit.md only | Tokens extracted. No voice or positioning in the snapshot panels. |
| **L2** | creative-kit + voice | Tokens + voice snapshot. Social card headlines informed by voice style. |
| **L3** | creative-kit + voice + positioning | Full context. Social card headline defaults to positioning angle. |
| **L4** | All 4 files | Complete playground with audience info in voice panel. Best experience. |

---

## Anti-Patterns

| Anti-pattern | Instead | Why |
|-------------|---------|-----|
| Generating a Next.js app with npm install | Single HTML file, zero dependencies | The playground must be instant. `npm install` is a 30-second wall that kills the flow. `/app-store-screenshots` scaffolds Next.js because it needs html-to-image for PNG export. This skill only needs browser rendering. |
| Using a framework (React, Vue, etc.) | Vanilla JS with a state object | Frameworks add bundle size, build complexity, and failure modes. The /playground plugin proves vanilla JS works for interactive previews. |
| Making the HTML generic/template-looking | The playground LOOKS like the brand | If the brand is dark and moody, the playground chrome should be dark. If the brand is warm and organic, the playground should feel warm. The playground's own aesthetic is derived from the brand tokens — it's not neutral gray chrome. |
| Hardcoding Google Fonts URLs | Construct URLs from the font names in creative-kit.md | The user's brand may use any font. Read the font name, build the URL. If the font isn't on Google Fonts, fall back to the closest system font. |
| Skipping the multi-preview strip | Always show at least 3 aspect ratios | The whole point of the social card tab is to see how the brand renders at real platform dimensions. One size isn't enough — the user needs to see Twitter vs Instagram vs Story to catch layout problems. |
| Outputting raw CSS instead of JSON tokens | Structured JSON with semantic names | The agent needs to parse the output and write it to creative-kit.md. CSS variables are for the browser. JSON tokens are for the agent loop. |
| Asking the user to manually edit creative-kit.md after the playground | Read the pasted JSON and write the changes yourself | The playground exists to make brand editing visual. Making the user edit markdown afterward defeats the purpose. |

---

## Governance Checks (Built Into the HTML)

The playground includes a governance strip below the preview:

```
[checkmark] Contrast: AA   [checkmark] Heading readable   [warning] Accent on bg: 2.8:1 (needs 3:1)
```

Implementation: after each state change, run WCAG contrast ratio checks on all text-background combinations. Use the relative luminance formula inline — no library needed. Flag failures as warnings with the specific ratio.

---

## Font Curation

For the font dropdowns, offer these curated options plus whatever the brand currently uses:

**Display fonts:** Space Grotesk, General Sans, Instrument Serif, Syne, Clash Display, Satoshi, Plus Jakarta Sans, Outfit, Bricolage Grotesque, Manrope

**Body fonts:** Inter, DM Sans, IBM Plex Sans, Source Sans 3, Nunito Sans, Geist, Work Sans, Rubik, Lato, Open Sans

These are all on Google Fonts. The dropdown should show the font name rendered in that font (via per-option `font-family`).

---

## File Output

| File | Path | Description |
|------|------|-------------|
| Playground HTML | `brand-playground.html` (project root) | The interactive playground |
| Asset log entry | `brand/assets.md` | "Brand playground generated — [date]" |

The HTML file is gitignored by convention (it's a generated artifact). The user can regenerate it anytime by re-running the skill.

---

## Error Recovery

| Problem | Fix |
|---------|-----|
| creative-kit.md has no parseable colors | Use defaults. Note which values were assumed in the token output. |
| Font not found on Google Fonts | Use the closest system font. Show a warning: "Couldn't load [font]. Using [fallback]." |
| User doesn't paste tokens back | That's fine. The playground served its purpose as a visual check. No brand files need updating. |
| Logo path in creative-kit.md doesn't resolve | Skip logo rendering. Show placeholder text: "[Logo]". |
| User wants to re-run after brand changes | Just re-run the skill. It reads current brand files and generates a fresh HTML. |
