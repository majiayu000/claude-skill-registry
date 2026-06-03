---
name: design-system-synthesizer
description: "Read your site's representative pages, theme files, and media library to extract a complete reusable design system — logo, colors, typography, spacing scale, component patterns. Persist it as machine data AND generate a visible style-guide page on your site that renders the tokens visually."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.1.0
  mcp-server: respira-wordpress
  category: intelligence
---

# Design System Synthesizer

**Version:** 1.1.0
**Updated:** 2026-05-24
**Freshly updated:** v1.1.0 adds Step 9 — generates a visible style-guide page inside the user's WordPress site (private draft by default, optional public publish). Renders the synthesized tokens visually: color swatches with hex codes, typography samples in actual styles, spacing scale blocks, component previews. Page is built with the active builder so it's editable in the user's normal workflow. Solves the "where do I see the design system" question — it's a page, not JSON.
**Category:** intelligence
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Read a WordPress site's representative pages, theme files, and media library to extract a complete, reusable **design system** — logo, color palette, typography, spacing scale, component patterns. Persist it to the site so every future content-creation skill references it, and every new page Claude builds matches the existing brand.

This is the foundation for on-brand AI-generated content. Without a design system, the agent guesses at colors, fonts, and spacing — and the result looks like every other AI-generated WordPress page. With a design system, the agent has explicit tokens to use, and new pages snap to the brand.

---

## What it produces

A structured `design_system` artifact stored at the site level. Schema:

```json
{
  "version": "1.0.0",
  "synthesized_at": "2026-05-24T14:30:00Z",
  "synthesized_from": ["/", "/about/", "/services/web-design/", "/blog/sample-post/", "/contact/"],
  "brand": {
    "logo_url": "https://example.com/wp-content/uploads/2025/logo.svg",
    "logo_dark_url": null,
    "favicon_url": "https://example.com/favicon.ico",
    "social_card_url": "https://example.com/wp-content/uploads/2025/og-default.jpg",
    "wordmark_text": "Acme Studio"
  },
  "colors": {
    "primary": "#2563EB",
    "secondary": "#0F172A",
    "accent": "#F59E0B",
    "neutral_900": "#0F172A",
    "neutral_700": "#334155",
    "neutral_500": "#64748B",
    "neutral_300": "#CBD5E1",
    "neutral_100": "#F1F5F9",
    "background": "#FFFFFF",
    "background_alt": "#F8FAFC",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "link": "#2563EB",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444"
  },
  "typography": {
    "heading_family": "Söhne, ui-sans-serif, system-ui, sans-serif",
    "heading_weight": 700,
    "h1_size": "3.5rem",
    "h2_size": "2.5rem",
    "h3_size": "1.875rem",
    "h4_size": "1.5rem",
    "h5_size": "1.25rem",
    "h6_size": "1rem",
    "body_family": "Söhne, ui-sans-serif, system-ui, sans-serif",
    "body_weight": 400,
    "body_size": "1rem",
    "body_line_height": 1.65,
    "mono_family": "JetBrains Mono, ui-monospace, monospace",
    "letter_spacing_heading": "-0.02em",
    "letter_spacing_body": "0"
  },
  "spacing": {
    "scale_base": 4,
    "scale_steps": [4, 8, 12, 16, 24, 32, 48, 64, 96, 128],
    "section_padding_y": "96px",
    "section_padding_x": "24px",
    "container_max_width": "1280px"
  },
  "components": {
    "button_primary": {
      "background": "primary",
      "color": "#FFFFFF",
      "padding": "12px 24px",
      "border_radius": "8px",
      "font_weight": 600
    },
    "button_secondary": { /* ... */ },
    "card": {
      "background": "background",
      "border": "1px solid neutral_300",
      "border_radius": "12px",
      "padding": "32px",
      "shadow": "0 1px 3px rgba(0,0,0,0.05)"
    },
    "hero_pattern": "centered_with_kicker_h1_subtitle_2cta",
    "section_pattern": "wide_two_column_image_left"
  },
  "voice_hints": {
    "person": "we",
    "formality": "approachable_professional",
    "sentence_length_avg_words": 14,
    "avoids": ["exclamation marks", "marketing superlatives"]
  }
}
```

The artifact is stored via `respira_update_option('respira_design_system', ...)` for v7.1. v7.2 may migrate this to a dedicated `respira_intelligence_artifacts` table if cross-site rollup is needed.

---

## When to Use

- First time setting up an AI workflow for an existing site — generate the design system so future content is on-brand
- Site rebrand — re-synthesize after the new brand lands so the AI catches the new tokens
- Before running content-creation skills (`build_page`, page generators) so the new pages match the brand
- Quarterly refresh — re-synthesize to capture brand drift

---

## Trigger Phrases

- "build a design system for my site"
- "extract my brand"
- "synthesize a design system"
- "create my design tokens"
- "what does my site look like"
- "capture my brand"
- "build my style guide"
- "extract design tokens"

---

## Execution Workflow

### Step 1 — Confirm site

Call `respira_get_active_site` + `respira_get_site_context`. Note WordPress version and active theme — theme.json or customizer settings may already expose some tokens.

### Step 2 — Pick representative pages

Call `respira_list_pages`. From the list, pick 5–10 pages that should represent the brand:

- The homepage (always)
- The about page (always if present)
- One typical service or product page
- One typical blog post
- The contact page
- One landing page if any exists

If the site has fewer than 5 pages, use whatever exists. If more than 10, sample by recency and front-page-link weight.

### Step 3 — Extract logo + brand imagery

Call `respira_list_media` filtered for logo-like names (`logo`, `wordmark`, `brand`, `favicon`). Also check site identity via `respira_get_option('site_icon')` for the favicon and `respira_get_option('custom_logo')` for the custom logo URL.

### Step 4 — Read theme stylesheet for CSS variables

Call `respira_read_theme_file('style.css')` and `respira_read_theme_file('theme.json')` if FSE theme. Extract any `:root` CSS custom properties (often the cleanest source of brand tokens).

### Step 5 — Extract each picked page's builder content

For each of the 5–10 picked pages:

1. `respira_extract_builder_content(page_id)` — get the builder-native structure
2. Note colors used (background, text, buttons, links)
3. Note typography (heading sizes, families, weights)
4. Note spacing (section padding, gutters, container widths)
5. Note component patterns (hero layout, card style, navigation pattern)

### Step 6 — Synthesize

Aggregate the per-page observations into the structured `design_system` schema (see "What it produces" above). When multiple pages disagree on a value, prefer:

- The homepage's choice for hero patterns
- The most common value across all pages for body typography
- The CSS custom property value if defined (overrides per-page observation)
- The theme.json value if FSE theme (overrides CSS custom property)

For colors, identify primary / secondary / accent by frequency-of-use + role (background-of-CTA = primary; link color = link; large-text color = primary if it differs from body). Generate a neutral scale (100 → 900) by sampling backgrounds, borders, text colors.

### Step 7 — Show the synthesized system to the user

Output a human-readable summary:

```markdown
## Design system synthesized for {site_url}

**Brand**
- Logo: ![](logo_url)
- Wordmark: {wordmark_text}

**Colors**
- Primary: {primary} ▮
- Secondary: {secondary} ▮
- Accent: {accent} ▮
- Neutrals: {neutral_100} → {neutral_900} (9-step scale)

**Typography**
- Headings: {heading_family} {heading_weight}, H1 {h1_size}
- Body: {body_family} {body_weight}, {body_size}/{body_line_height}

**Spacing**
- Base: {scale_base}px, scale: {scale_steps}
- Section padding: {section_padding_y} vertical, container max {container_max_width}

**Component patterns observed**
- Hero: {hero_pattern}
- Section: {section_pattern}
- Button primary: {button_primary description}
- Card: {card description}
```

Ask the user to confirm or correct anything.

### Step 8 — Persist the data

After confirmation, call `respira_update_option('respira_design_system', <json>)`. Confirm with `respira_get_option('respira_design_system')`.

### Step 9 — Generate the visible style-guide page

The JSON in `wp_options` is the machine source of truth, but it's invisible to humans. Step 9 builds a real WordPress page on the site that **renders the synthesized tokens visually** — so the user can see their design system, send a link to teammates, and edit it like any other page.

#### Page settings

- **Title:** "Design System" (overridable)
- **Slug:** `/design-system/` (overridable; check via `respira_list_pages` and append `-2` if conflict)
- **Status:** `private` by default (visible only to logged-in editors). Ask the user: *"Publish as private (admin-only preview) or public?"* — default to private.
- **Excluded from sitemap, robots noindex** by default (so even if accidentally published, it doesn't pollute search).
- **Builder:** the active builder (Bricks / Elementor / Divi / Gutenberg / Oxygen / Breakdance / etc.) — never raw HTML. Use `respira_get_builder_inline_schemas` to confirm available modules before building.

#### Page structure (the section spine)

Build the page with `respira_build_page` using this section spine, mapping each section to the active builder's native modules:

1. **Hero**
   - Eyebrow: "Design System · synthesized {synthesized_at} from {n} pages"
   - H1: "{brand.wordmark_text} Design System" (or "Design System" if no wordmark)
   - Subtitle: "The visual foundation every page generated on this site references."
   - Logo image (from `brand.logo_url`) prominently displayed

2. **Brand identity**
   - Logo card with full logo, dimensions, file type
   - Favicon swatch
   - Social card preview if `brand.social_card_url`
   - Wordmark in heading typography if `brand.wordmark_text`

3. **Color palette**
   - 4 primary swatches (primary / secondary / accent / background) — each a large color block with hex code, role name, and "use for" guidance
   - 9-step neutral scale — horizontal strip from neutral_100 → neutral_900 with hex codes
   - Semantic colors row (link / success / warning / error) — smaller swatches

4. **Typography**
   - **Heading sample:** all six heading levels (H1 → H6) rendered in actual `heading_family` + `heading_weight` + their specified sizes, each labeled with the size value
   - **Body sample:** a real paragraph in `body_family` + `body_weight` + `body_size` + `body_line_height` so the user can SEE the body reading experience
   - **Mono sample:** a code block in `mono_family`
   - Side panel listing the font stacks verbatim (with fallbacks) and font-loading note (Google Fonts / Adobe Fonts / self-hosted)

5. **Spacing scale**
   - Visual blocks for each step in `scale_steps` — a colored rectangle whose height matches the step value, labeled with the pixel value
   - "Section padding" block showing actual section padding visually
   - "Container max-width" line showing the max-width as a horizontal ruler

6. **Components**
   - Button primary + button secondary rendered in actual styles (background, color, padding, border-radius)
   - Card example with real content ("Card title", short body, button)
   - Hero pattern description with a wireframe sketch
   - Section pattern description with a wireframe sketch

7. **Voice hints** (if synthesized)
   - Person used
   - Formality descriptor
   - Avoided words (the strongest signal)
   - Cross-link to the Brand Voice Synthesizer skill — *"For the full brand voice including signature phrases, signature openers, and a real paragraph example, run the [Brand Voice Synthesizer](/skills/brand-voice-synthesizer)."*

8. **Footer**
   - Synthesis metadata: source pages list, synthesized timestamp, version
   - "Edit this page" link to the builder edit URL
   - "Re-synthesize" instructions: *"Run the Design System Synthesizer skill again any time to refresh. The artifact will be diffed before overwriting."*

#### Builder mapping

`respira_build_page` accepts a section spine and renders it as native builder modules. For each section above, the page builder picks the closest module:

| Section | Bricks | Elementor | Divi 5 | Gutenberg |
|---|---|---|---|---|
| Color swatches | div block grid + heading + text | Inner Section + Heading + Text widgets | Row + Column + Code module | core/columns + core/group blocks |
| Heading samples | heading element ×6 | Heading widget ×6 | Text module ×6 | core/heading blocks ×6 |
| Button samples | button element | Button widget | Button module | core/buttons block |
| Spacing blocks | div block with explicit height | Inner Section with margin | Code module with custom CSS | core/spacer blocks |

Do NOT render with raw HTML even when the builder doesn't have a perfect 1:1 mapping. If a section can't be cleanly built (e.g. the spacing-scale visualization requires inline styles the builder doesn't expose), fall back to a labeled bullet list — never a `<div>` blob.

#### Output

After page creation, output:

```markdown
## ✓ Design system saved + style-guide page created

**Machine source of truth:** `wp_options.respira_design_system` (queryable via `respira_get_option`)

**Human view:** {page_url} · status: private (editors only)

**Open it now:** [{page_title} in the editor]({builder_edit_url})

**Promote to public:** call `respira_update_page(id={page_id}, status='publish')` if you want this visible on your site as a /design-system/ landing.

**Re-sync any time:** run this skill again. Existing data is diffed and the page is regenerated (with the option to keep customizations).
```

---

## How other skills use the design system

Once persisted, future skills (Page Template Library, Brand Voice Synthesizer, future content-generation skills) should call `respira_get_option('respira_design_system')` at the top of their workflow. They use the tokens to:

- Pick colors when generating new sections (use primary, secondary, accent — never invented hex values)
- Match typography when generating headings (heading_family, heading_weight, sizes)
- Match spacing when laying out sections (use the spacing scale, not arbitrary pixel values)
- Match component patterns when generating heros, cards, buttons (reference button_primary etc.)

This is the foundation. Every other content skill stands on it.

---

## Hard rules

- Never invent design tokens. Every color, font, size, and pattern in the artifact must trace to an observation in the source pages, theme files, or media. If a token can't be inferred, leave it null — don't guess.
- Never overwrite an existing design system silently. If `respira_get_option('respira_design_system')` returns existing data, show the user the diff before overwriting.
- The logo URL must be an absolute URL. Use `wp_get_attachment_url()` semantics, not a relative path.
- Color values must be hex (`#RRGGBB`). Convert `rgb()`, `rgba()`, named colors to hex.
- Font families preserve the full font-stack as written in CSS (with fallbacks), not just the primary family name.

---

## Telemetry

Records: site URL hash, number of pages sampled, builder active, theme name, colors detected count, typography sources used (theme.json / CSS variables / per-page observation), success/failure, total duration. No actual color values, font names, or logo URLs are sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`

---

## Future (v7.2)

Storage will migrate from `wp_options` to a dedicated `respira_intelligence_artifacts` table for cross-site rollups and Studio-tier multi-site dashboards. The schema above is stable — the storage layer change is transparent to consuming skills.
