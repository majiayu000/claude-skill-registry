---
name: vibe
description: >
  Generate and deploy production-grade websites from a natural language description.
  Use when asked to "vibe a site", "vibe code this", "build me a website and publish it",
  "create a landing page and deploy it", "make a portfolio site and put it online",
  "generate a site and ship it", or any request combining website creation with deployment.
  Produces a live URL via here.now.
---

# vibe

Generate a complete, production-quality website from a description and deploy it live in seconds.

**Requires the here-now skill.** If `~/.agents/skills/here-now/scripts/publish.sh` does not exist, tell the user:
`npx skills add heredotnow/skill --skill here-now -g`

## Workflow

### Phase 0: Design Decision (BEFORE any code)

Read `references/DESIGN_SYSTEM.md` before generating anything.

Determine from the user's request:

1. **Site type** — Read `references/SITE_TYPES.md` and match the closest archetype.
2. **Aesthetic direction** — Pick ONE bold direction (do not default to "modern and clean"):
   - Brutally minimal | Luxury/refined | Editorial/magazine | Brutalist/raw
   - Art deco/geometric | Retro-futuristic | Organic/natural | Industrial/utilitarian
   - Soft/pastel | Dark cinematic | Warm earthy | Monochrome high-contrast
3. **Font pairing** — Select from `references/DESIGN_SYSTEM.md` font pairings. NEVER use Inter, Roboto, Arial, or system-ui as the primary font.
4. **Color palette** — Choose a dominant color with one sharp accent. NEVER default to purple/indigo gradients.
5. **Layout strategy** — Break from the default hero > 3-column features > testimonials > CTA. Use asymmetry, overlap, grid-breaking elements, or unconventional section flow.

Present the design plan to the user in 2-3 sentences. Wait for approval before generating code.

### Phase 1: Generate

Create a self-contained static site in a working directory (default: `./vibe-output/`).

**File structure:**
```
vibe-output/
  index.html
  styles.css        (if CSS exceeds 50 lines)
  app.js            (only if interactive behavior needed)
```

For simple sites, a single `index.html` with embedded `<style>` and `<script>` is preferred.

**Generation rules:**
- Follow every rule in `references/DESIGN_SYSTEM.md` — no exceptions
- Use Google Fonts via `<link>` for distinctive typography
- Use CSS custom properties for all colors and spacing
- All images: use `https://images.unsplash.com/photo-{id}?w={w}&h={h}&fit=crop` with real Unsplash photo IDs or inline SVG illustrations
- Mobile-first responsive design with breakpoints at 768px and 1024px
- Include `<meta name="viewport">`, `<meta charset="UTF-8">`, proper `<title>`
- Semantic HTML: `<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`, `<button>`, `<a>`
- Real content — never lorem ipsum. Generate realistic text appropriate to the site type
- Dark mode: include `color-scheme: dark light` and respect `prefers-color-scheme`

### Phase 2: Review

Before deploying, verify against this checklist:
- [ ] No purple/indigo gradients as default palette
- [ ] No Inter, Roboto, Arial, or system-ui as primary font
- [ ] CSS custom properties defined for colors and spacing
- [ ] All interactive elements have focus-visible states
- [ ] Touch targets are at least 44x44px
- [ ] `prefers-reduced-motion` is respected
- [ ] No `transition: all` — list specific properties
- [ ] No `<div onClick>` — use `<button>` or `<a>`
- [ ] All images have explicit `width` and `height`
- [ ] Responsive at 375px, 768px, and 1024px widths

Fix any failures before proceeding.

### Phase 3: Deploy

```bash
cd ./vibe-output && ~/.agents/skills/here-now/scripts/publish.sh .
```

Read `stderr` for `publish_result.*` fields. Example output:

```
publish_result.site_url=https://your-slug.here.now/
publish_result.auth_mode=anonymous
publish_result.expires_at=2026-02-27T00:00:00.000Z
publish_result.claim_url=https://here.now/claim?slug=your-slug&token=abc123
```

Report to the user:

- The live URL (always)
- "Expires in 24 hours" (only if `publish_result.auth_mode=anonymous`)
- The claim URL (only if `publish_result.claim_url` is non-empty and starts with `https://`)
- Warn: "Save the claim URL — it cannot be recovered"

### Phase 4: Iterate

If the user requests changes:
1. Edit the files in `./vibe-output/`
2. Read `.herenow/state.json` to find the existing slug
3. Republish with `--slug` flag to update in place:
```bash
cd ./vibe-output && ~/.agents/skills/here-now/scripts/publish.sh . --slug {slug}
```

## What to Tell the User

- Always share the live URL prominently
- Describe the design choices made (font, palette, layout) in 1-2 sentences
- If anonymous: mention 24h expiry and the claim URL
- Never expose `.herenow/state.json` paths or internal API details
- If the user wants permanent hosting: guide them through here.now API key setup (see here-now skill docs)

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Generate code before deciding on aesthetics | Complete Phase 0 design decision first |
| Default to purple/indigo | Pick a bold, context-appropriate palette |
| Use Inter/Roboto/Arial/system-ui | Pick a distinctive Google Font pairing |
| Use `hero > 3-col features > testimonials > CTA` | Design an unconventional layout for the context |
| Add bounce/spring to every element | One orchestrated page-load animation |
| Write placeholder/lorem text | Generate realistic content for the site type |
| Use `<div onClick>` | Use `<button>` for actions, `<a>` for navigation |
| Skip mobile testing | Design mobile-first, verify at 375px |
