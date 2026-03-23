---
name: stitch-design-md
description: Analyzes a Stitch project's screens and synthesizes a natural-language DESIGN.md — visual atmosphere, color palette with hex values, typography rules, and Stitch-ready prompt snippets. Use this before stitch-loop or any multi-page build to establish design consistency.
allowed-tools:
  - "stitch*:*"
  - "Read"
  - "Write"
---

# Stitch → DESIGN.md

**Constraint:** Only use this skill when the user explicitly mentions "Stitch" or when preparing design system documentation for Stitch generation.

You are an expert **Design Systems Lead**. Your job is to analyze Stitch project assets and synthesize a **Semantic Design System** into a file named `DESIGN.md` — written in natural language, not CSS.

## When to use this vs. stitch-design-system

| Skill | What it produces | Use it for |
|-------|-----------------|-----------|
| `stitch-design-md` | Natural-language `DESIGN.md` | Feeding back into Stitch prompts; multi-page visual consistency; design docs |
| `stitch-design-system` | `design-tokens.css`, `tailwind-theme.css`, `DESIGN.md` | Code-level theming for Next.js, Svelte, React, HTML output |

Use `stitch-design-md` first if you're building more Stitch screens. Use `stitch-design-system` when you're converting to code.

## Prerequisites

- Stitch MCP Server configured
- A Stitch project with at least one designed screen

---

## Step 1: Retrieve the design

### If the user provides a Stitch URL

If the user pastes a Stitch design URL like `https://stitch.withgoogle.com/projects/3492931393329678076?node-id=375b1aadc9cb45209bee8ad4f69af450`:

1. Parse the URL:
   - `projectId` = segment after `/projects/` and before `?` (e.g. `3492931393329678076`)
   - `screenId` = query param `node-id` (e.g. `375b1aadc9cb45209bee8ad4f69af450`)
2. Call `[prefix]:get_screen` with those IDs
3. Skip ahead to Step 2

### If project/screen IDs are unknown

1. Run `list_tools` → find the Stitch MCP prefix
2. Call `[prefix]:list_projects` with `filter: "view=owned"` → select project by title → extract numeric ID
3. Call `[prefix]:list_screens` with `projects/[projectId]` → pick the representative screen
4. Call `[prefix]:get_screen` with numeric `projectId` and `screenId`
5. Call `[prefix]:get_project` with `projects/[projectId]` → get `designTheme` (font, roundness, customColor, colorMode)

### Download the assets

```bash
# Download the HTML for color and Tailwind class analysis
bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"
```

Parse the HTML for:
- Tailwind utility classes (colors, typography, spacing, shadows)
- Inline `tailwind.config` block (custom tokens)
- CSS variables

---

## Step 2: Analyze the design

Work through these layers systematically:

### 2.1 Project identity
- Project title and numeric ID (from `name` field)
- `deviceType` (MOBILE / DESKTOP / TABLET / AGNOSTIC)
- `designTheme.font`, `designTheme.roundness`, `designTheme.colorMode` from `get_project`

### 2.2 Visual atmosphere
Describe the aesthetic in 2–3 sentences. Go beyond generic adjectives — what does it feel like? What editorial or product category does it evoke?

Examples:
- "Sophisticated minimalist sanctuary — gallery-like spaciousness, photography-first, Scandinavian calm"
- "High-density productivity tool — information-first, sharp edges, focused contrast"
- "Warm artisanal brand — handcrafted feel, organic textures, generous breathing room"

### 2.3 Color palette
For each key color, write:
```
[Descriptive name] ([hex]) — [functional role]
```

Example:
```
Deep Muted Teal-Navy (#294056) — Primary actions, links, active states
Warm Barely-There Cream (#FCFAFA) — Page background
Charcoal Near-Black (#2C2C2C) — Headlines and product names
Soft Warm Gray (#6B6B6B) — Body copy and metadata
```

Aim for 4–6 colors. Include light AND dark mode backgrounds if both present.

### 2.4 Typography
- Font family name (from `designTheme.font` or Tailwind class)
- Weight scale (what's used for display, section headers, body, labels)
- Any notable letter-spacing, line-height, or size conventions

### 2.5 Shape and geometry
Translate Tailwind classes to descriptive language:
- `rounded-full` → "Pill-shaped"
- `rounded-lg` (12px) → "Gently rounded corners"
- `rounded-md` (8px) → "Subtly rounded corners"
- `rounded-none` → "Sharp, squared-off edges"

### 2.6 Depth and elevation
Describe shadow presence and style:
- `shadow-none` → "Flat, no shadow"
- `shadow-sm` → "Whisper-soft diffused shadow"
- `shadow-lg` → "Prominent floating elevation"

### 2.7 Layout principles
- Max content width, grid columns, breakpoint behavior
- Base spacing unit (4px / 8px system)
- Section margins and padding patterns
- Touch target sizes (if mobile)

---

## Step 3: Write DESIGN.md

Use this exact structure:

```markdown
# Design System: [Project Title]
**Project ID:** [numeric ID]
**Device:** [MOBILE / DESKTOP / TABLET / AGNOSTIC]

## 1. Visual Theme & Atmosphere
[2–3 sentences describing the overall aesthetic and mood]

## 2. Color Palette & Roles
- **[Descriptive Name]** ([#hex]) — [Functional role]
- **[Descriptive Name]** ([#hex]) — [Functional role]
[...4–6 colors total]

## 3. Typography Rules
**Primary Font:** [Name] — [One-line character description]

- **Display (H1):** [weight], [size range]
- **Section (H2):** [weight], [size range]
- **Body:** [weight], line-height [value], [size]
- **Labels/Captions:** [weight], [size]

## 4. Component Stylings
- **Buttons:** [shape (Xpx radius)], [color], [padding]; hover [behavior]
- **Cards/Containers:** [roundness (Xpx)], [background], [shadow]; hover [behavior]
- **Inputs/Forms:** [border style], [background], [roundness], [focus behavior]

## 5. Layout Principles
- Max content width: [value]; [grid description]; [column behavior at breakpoints]
- Base spacing unit: [4px/8px]; section margins [range]; touch targets [size]

## 6. Design System Notes for Stitch Generation
[This section is copy-paste ready for new Stitch prompts]

When creating new screens:
- **Atmosphere:** "[Quote the atmosphere description from Section 1]"
- **Colors:** Always use descriptive name + hex (e.g. "[Name] ([#hex])")
- **Shape:** "[Describe buttons and cards using the language from Section 4]"
- **Spacing:** "[Describe the whitespace/density philosophy]"
- **Font:** [Font name] — [one-line descriptor]
```

---

## Step 4: Integration

Tell the user what to do with it:

```
## DESIGN.md created

Saved to: ./DESIGN.md

**How to use it:**

1. **More Stitch screens:** Copy Section 6 into the DESIGN SYSTEM block of your next Stitch prompt.
   This keeps every new screen visually consistent with your existing design.

2. **Multi-page build with stitch-loop:** Include Section 6 in every `next-prompt.md` baton file.

3. **Code conversion:** Hand off to `stitch-design-system` when you're ready to generate
   `design-tokens.css` and `tailwind-theme.css` for your framework.
```

---

## Best practices

- **Descriptive over technical:** "Ocean-deep Cerulean (#0077B6)" not just "blue"
- **Functional roles matter:** Don't just name the color — say what it does
- **Section 6 is the payoff:** This is the copy-paste block that makes every future screen consistent
- **Be precise:** Exact hex codes always. Vague approximations ("kind of warm beige") are useless

## Common pitfalls

- Leaving `rounded-xl` in the doc instead of translating to "generously rounded corners (12px)"
- Listing colors without functional roles
- Skipping the font weight scale (just saying "Manrope" doesn't tell you when to use 400 vs 600)
- Writing Section 6 without the actual hex codes — useless for Stitch

---

## References

- `examples/usage.md` — Worked examples
- `examples/DESIGN.md` — Complete sample output for a furniture e-commerce site
- `docs/color-prompt-guide.md` — 8 ready-to-use color palettes for inspiration
- `scripts/fetch-stitch.sh` — Reliable HTML downloader for GCS URLs
