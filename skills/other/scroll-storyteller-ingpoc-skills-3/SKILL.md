---
name: scroll-storyteller
description: Use when creating interactive scroll-based storytelling experiences with mouse-following spotlight effects, animated SVG art, and the Anthropic design language. Load for explainer pages, product showcases, visual narratives, or any content needing immersive scroll storytelling with organic shapes and smooth animations. Supports GSAP-powered or lightweight CSS-only animations.
keywords: scroll, storytelling, interactive, svg, animation, spotlight, hero section, explainer, showcase, gsap, scrolltrigger
license: MIT
---

# Scroll Storyteller

Create immersive, interactive storytelling experiences using Anthropic's authentic design language: strict duotone palette, organic Bézier SVG paths, custom cursors, and chapter-based narratives.

## Workflow

Use `AskUserQuestion` to gather preferences, then generate:

| Step | Question | Options |
|------|----------|---------|
| 1 | Animation? | GSAP (rich) vs CSS-only (lightweight) |
| 2 | Mood? | Warm vs Cool vs Creative |
| 3 | Palette? | (show 3-4 based on mood) |
| 4 | Topic? | Biblical/Tech/Business/Personal/Custom |
| 5 | Chapters? | 3, 4, or 5 |
| 6 | Content per chapter | Title, description, keywords |

**Generate:**
```bash
bash ~/.claude/skills/scroll-storyteller/scripts/generate.sh my-story <palette> [--gsap] [--chapters N]
```

**Post-generation:** Customize content, create SVGs (see `references/structure-templates.md`)

## SVG Illustration Workflow

Each chapter needs a topic-relevant SVG that matches the narrative position:

| Position | Purpose | Composition | Example |
|----------|---------|-------------|---------|
| **Hero** | Set scene, show contrast | Wide (1000x1000), 2 silhouettes | David vs Goliath distant |
| **Chapter 1** | Introduce protagonist | Centered figure + context | Shepherd with sheep |
| **Chapter 2** | Show conflict/obstacle | Imposing, fills frame | Giant warrior |
| **Chapter 3** | Resolution/triumph | Dynamic, radiating | Victor + fallen + rays |
| **Chapter 4** | Deepening conflict (optional) | Crowded, escalating | Army masses, threats multiply |
| **Chapter 5** | Final climax (optional) | Action, decisive | Stone flying, impact moment |
| **Finale** | Symbolic summary | Centered symbol | Crown + light |

**Light/Dark Pattern by Chapter Count:**
- **3 chapters:** Ch1=Light → Ch2=Dark → Ch3=Light
- **4 chapters:** Ch1=Light → Ch2=Dark → Ch3=Light → Ch4=Dark
- **5 chapters:** Ch1=Light → Ch2=Dark → Ch3=Light → Ch4=Dark → Ch5=Light

**Process:**
1. Load `references/svg-illustration-guide.md` for theme → element mapping
2. Identify chapter position (hero/ch1/ch2/ch3/ch4/ch5/finale)
3. Extract topic keywords from chapter content
4. Select SVG elements from element library:
   - Characters: figure-small, figure-large, figure-triumphant, figure-action
   - Nature: hills, sun, tree, path, clouds, lightning, wind
   - Objects: staff, crown, shield, weapon, stone, obstacle
   - Abstract: radiate, rings, trajectory, converge, impact
5. Compose using position template
6. Apply palette mood style (see `references/design-harmony.md` → Palette Mood → SVG Style)
7. Add animation classes: `organic-path`, `fade-path`, `scale-path`

**SVG Checklist:**
- [ ] Uses only `var(--deep)` and `var(--foam)` colors
- [ ] All paths are organic Bézier curves (Q/C commands)
- [ ] No geometric primitives (circle, rect, ellipse)
- [ ] Opacity range matches palette mood
- [ ] Composition matches chapter position
- [ ] Symbolically represents chapter content

## Animation Styles

| Style | Library | Size | Best For |
|-------|---------|------|----------|
| **GSAP** | GSAP 3.x + ScrollTrigger | ~45KB | Rich interactions, SVG draw, orbits, timelines |
| **CSS-only** | None (IntersectionObserver) | 0KB | Lightweight, fast load, simple reveals |

### GSAP Features
- SVG path draw animations (strokeDasharray)
- Continuous orbit/rotation effects
- Scroll-linked timeline control
- Parallax with scrub
- Staggered animations with precise timing

### CSS-only Features
- IntersectionObserver reveals
- CSS transitions with delays
- Transform-based animations
- No external dependencies
- Smaller bundle size

## Duotone Palettes

| # | Theme | Light | Dark | Mood |
|---|-------|-------|------|------|
| 1 | **Anthropic** | `#FAF9F5` cream | `#141413` charcoal | Warm |
| 2 | **Midnight** | `#E8F4F8` ice | `#0D1B2A` navy | Cool |
| 3 | **Sepia** | `#F5F0E6` parchment | `#2C1810` espresso | Warm |
| 4 | **Forest** | `#F0F4F0` mist | `#1A2E1A` evergreen | Creative |
| 5 | **Dusk** | `#F4F0F8` lavender | `#1E1A2E` violet | Creative |
| 6 | **Ember** | `#FFF5F0` blush | `#2A1A14` ember | Warm |
| 7 | **Steel** | `#F0F2F5` silver | `#1A1C20` graphite | Cool |
| 8 | **Ocean** | `#F0F8F8` foam | `#0A1A1A` deep | Cool |

**Mood → Palette mapping:**
- **Warm**: 1 (Anthropic), 3 (Sepia), 6 (Ember)
- **Cool**: 2 (Midnight), 7 (Steel), 8 (Ocean)
- **Creative**: 4 (Forest), 5 (Dusk)

## Design Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| **Authentic** (default) | Strict duotone, organic paths | Editorial, brand storytelling |
| **Expressive** | Multi-color accents allowed | Product showcases, demos |

## Core Features

| Feature | Description |
|---------|-------------|
| **Custom Cursor** | Dual-layer cursor with smooth easing, mix-blend-mode |
| **Hero Section** | **GSAP**: Flowing organic lines (1000x1000 background). **CSS-only**: Desk lamp with animated light cone reveal |
| **Spotlight Layer** | Radial gradient follows cursor on dark sections |
| **Staggered Reveals** | Title words animate in sequence on load |
| **Chapter Structure** | Alternating light/dark sections with transitions |
| **Organic SVGs** | Hand-drawn Bézier paths, fill-only (no strokes) |
| **Parallax** | Subtle depth movement on scroll |

## Anthropic Design Language

### Strict Duotone Palette

| Element | Hex | CSS Variable |
|---------|-----|--------------|
| Cream (light) | `#FAF9F5` | `--cream` |
| Charcoal (dark) | `#141413` | `--charcoal` |

**Rule:** No other colors. All illustrations use exactly these two.

### Typography

| Role | Font | Fallback |
|------|------|----------|
| Display/Headings | Instrument Serif | Georgia, serif |
| Body/UI | Inter | -apple-system, sans-serif |

**Characteristics:**
- Large, editorial headings (clamp 3rem - 7rem)
- Light weight (300-400)
- Negative letter-spacing on display (-0.02em)
- Generous line-height (1.5-1.8)

### SVG Design Rules

| Rule | Description |
|------|-------------|
| **Fills only** | Never use strokes for main shapes |
| **Organic paths** | Complex Bézier curves, hand-drawn feel |
| **viewBox** | Always 1000x1000 or 500x500 (square) |
| **2-4 paths** | Keep compositions simple |
| **Layered** | Light shapes behind, dark in front |

**Anti-patterns:**
```
❌ <circle>, <rect>, <ellipse> (geometric)
❌ stroke="..." on main elements
❌ Multiple colors
✅ <path d="M... Q... C..."> with organic curves
```

### Topic-Driven SVG Generation

The `svg-generator.sh` helper automatically selects appropriate SVG templates based on chapter content:

| Keywords | Template | Best For |
|----------|----------|----------|
| identity, profile, self, unique | **Fingerprint + Verification** | Personal identity concepts |
| network, connect, distributed, system | **Central Hub + Network** | System architecture concepts |
| protect, secure, vault, lock | **Protected Vault + Links** | Security concepts |
| growth, learn, knowledge, tree | **Knowledge Tree** | Learning/growth concepts |
| enforce, filter, gate, barrier | **Gateway Arches** | Enforcement/validation |
| trust, hand, collaboration | **Hand Holding + Connection** | Partnership concepts |
| unify, finale, complete | **Concentric Symbol** | Conclusion/unity |

**Usage:**
```bash
# Source the generator in your script
source scripts/svg-generator.sh

# Generate SVG for a chapter (position: hero/ch1/ch2/ch3/ch4/ch5/finale)
generate_svg_for_chapter \
  "ch1" \
  "Digital Identity" \
  "Your unique identity on the blockchain" \
  "var(--foam)" \
  "var(--deep)" \
  "fade-path"
```

**Positions:** `hero` | `ch1` | `ch2` | `ch3` | `ch4` | `ch5` | `finale`

## Animation Patterns

For detailed GSAP and CSS animation patterns, see [`references/animation-patterns.md`](./references/animation-patterns.md)

**Animation Classes:**
| Class | Description | Usage |
|-------|-------------|-------|
| `organic-path` | Base class for all SVG paths | Always applied |
| `fade-path` | Fade in animation | Default for most paths |
| `scale-path` | Scale up animation | Combined with fade-path |
| `draw-path` | Stroke draw animation (GSAP only) | For line/path drawing effects |

## Narrative Structure

For narrative structure and HTML templates, see [`references/structure-templates.md`](./references/structure-templates.md)

## Resources

| File | Purpose | Load When |
|------|---------|-----------|
| `scripts/generate.sh` | Creates HTML (CSS-only or GSAP with --gsap) | Starting new project |
| `scripts/svg-generator.sh` | Topic-driven SVG generation helper | Creating custom illustrations |
| `references/animation-patterns.md` | **GSAP + CSS animation patterns** | **Implementing animations** |
| `references/structure-templates.md` | **Narrative structure + HTML templates** | **Building sections** |
| `references/svg-illustration-guide.md` | **Theme → SVG element mapping, templates** | **Creating topic-relevant illustrations** |
| `references/example-david-goliath.md` | **Complete worked example with all 5 SVGs** | **Learning SVG composition patterns** |
| `references/anthropic-design.md` | Full design system reference | Deep customization |
| `references/gsap-patterns.md` | GSAP + ScrollTrigger recipes | Using GSAP animation style |
| `references/css-only-patterns.md` | IntersectionObserver recipes | Using CSS-only animation style |
| `references/design-harmony.md` | Visual cohesion + palette-mood SVG styling | Ensuring consistent design quality |

### Example Files

| File | Animation | Description |
|------|-----------|-------------|
| `agent-harness-gsap.html` | GSAP | Full experience with orbit SVGs, draw animations, parallax |
| `agent-harness-anthropic.html` | CSS-only | Lightweight with IntersectionObserver reveals |

## Usage Workflow

1. **Choose Animation Style**: GSAP (rich) or CSS-only (lightweight)
2. **Choose Palette**: Select mood → pick specific palette
3. **Select Chapter Count**: Choose 3, 4, or 5 chapters
4. **Plan Narrative**: Hero + selected chapters + finale
5. **Generate**: `bash scripts/generate.sh project-name <palette> [--gsap]`
6. **Customize Content**: Replace placeholder text
7. **Add Illustrations**: Use organic path templates from assets/
8. **Test**: Verify animations, cursor, scroll behavior
9. **Ship**: Single self-contained HTML file

## Accessibility

- `prefers-reduced-motion` support (disables animations)
- Touch device detection (hides custom cursor)
- Semantic HTML structure
- High contrast duotone

## Token Efficiency

- Scripts execute without loading context (0 tokens)
- SVG templates are copy-paste patterns
- Single HTML output, no build step
- CSS custom properties for easy theming
