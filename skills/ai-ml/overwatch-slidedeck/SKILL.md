---
name: overwatch-slidedeck
description: "Build interactive live slide decks with Vite + React 19, TanStack Router, WebGPU shaders, Framer Motion orchestration, 1920x1080, access-gated SPA. 39 components (layout, interaction, graphics, chrome, navigation), direction-aware slide transitions, presenter mode with speaker notes and BroadcastChannel sync, Playwright PNG/PDF export, YAML-driven authoring, Cloudflare/Vercel/Netlify deploy. Triggers on: slide deck, presentation, pitch deck, investor deck, product demo, conference talk, live slides, WebGPU slides, interactive presentation, presenter mode, speaker notes, overwatch deck."
argument-hint: [deck-name or spec.yaml path]
disable-model-invocation: true
---

# Overwatch Slide Deck Designer

Build interactive, presentation-grade slide decks as live SPAs—not static PDFs. Vite + React 19 + TanStack Router, 1920x1080 native resolution, WebGPU shader backgrounds, Framer Motion orchestration, collapsible sidebar navigation, keyboard controls, an optional access gate, and deploy to Cloudflare Workers / Vercel / Netlify.

## When to Use This Skill

- Live presentations (investor pitches, product demos, conference talks)
- Interaction-rich decks with hover states, content swaps, tooltips
- WebGPU shader backgrounds for dramatic cover slides
- Decks that need an access gate (client-side; see Access Gate section for its limits)
- Keyboard-navigated presentations with sidebar navigation

## Domains Supported

| Domain | Use Cases |
|--------|-----------|
| **Business & Finance** | KPI dashboards, revenue charts, growth trends, pricing |
| **Healthcare** | Patient metrics, clinical outcomes, treatment timelines |
| **Wellness & Coaching** | Transformation journeys, milestone celebrations, quotes |
| **AI/ML Research** | Model architecture, training metrics, STT/TTS pipelines |

---

## Quick Start Workflow

### 1. Audit Reference Screenshots

Review existing example screenshots for aesthetic consistency before designing.

```bash
open ~/.claude/skills/overwatch-slidedeck/assets/examples/
```

15 reference screenshots demonstrate the canonical aesthetic: dark backgrounds, orange accent (#ff6e41), Playfair Display headings, interactive hover states, WebGPU shader covers.

### 2. Scaffold New Project

```bash
cp -r ~/.claude/skills/overwatch-slidedeck/assets/scaffold/ ./my-deck
cd my-deck
npm install
npm run dev  # Opens at http://localhost:5173
# Navigate to /deck/1
```

### 3. Review Iconography Options

| Domain | Key Icons |
|--------|-----------|
| **AI/ML** | Brain, Cpu, Database, Layers, Network, Waveform |
| **Business** | TrendingUp, DollarSign, PieChart, Target, Users |
| **Healthcare** | Heart, Activity, Stethoscope, ShieldCheck |
| **Parenting** | Baby, Users, HandHeart, Shield, Brain, Puzzle |
| **Spirituality** | Compass, Flame, Mountain, Sunrise, Lightbulb |

**Icon libraries (not included in scaffold—install as needed):**
- **Lucide** (1,500+): `lucide-react` — https://lucide.dev/icons
- **Tabler** (5,900+): `@tabler/icons-react` — https://tabler.io/icons
- **Phosphor** (7,000+): `@phosphor-icons/react` — https://phosphoricons.com

### 4. Plan Content Structure

1. **Define sections** — Group content into 4-8 logical sections
2. **Outline slides** — 3-5 slides per section
3. **Identify slide types** — Cover, social proof, split text, feature grid, timeline, quote, CLI demo, etc. (14 types available—see `references/slide-templates.md`)
4. **Gather assets** — Screenshots, diagrams, logos, expert photos
5. **Select icons** — Map icons to sections/concepts

**What separates a hand-crafted deck from AI slop.** VCs and executives now read dozens of generated decks a week and can spot them instantly — same stock layouts, same buzzword density, same fabricated polish. The failure modes to design against:

- **No unsourced numbers.** "47% growth" with no traceable source is the signature tell of a generated deck. Every statistic on a slide comes from the research phase (step 6) with a source the presenter can name. If the number can't be sourced, cut the slide, not the sourcing.
- **Headlines carry the insight.** Title the data slide "Churn dropped 31% after the onboarding fix," never "Churn Data." A slide whose headline could sit on any company's deck says nothing.
- **Specificity over vocabulary.** "Reviews 1,324 documents in 40 seconds" beats "leverages cutting-edge AI to transform document workflows." When a sentence would survive on a competitor's deck unchanged, rewrite it.
- **One motion grammar per deck.** Pick one entrance vocabulary (which AnimatedItem variants, one duration scale, one easing) and hold it across every slide — motion consistency is what makes 20 slides read as one designed object rather than a template assembly.
- **Decks travel without the presenter.** Boards forward slides; executives read them on phones at night. Every slide must be self-explanatory — hover-revealed content needs its key point visible before the hover.

### 5. Brand Color Extraction

Extract and map brand colors from the client/company site before building slides.

```bash
# Scrape the client/company site for brand identity
python3 ~/.claude/skills/firecrawl/scripts/firecrawl_api.py scrape "https://client-site.com" --formats branding

# Or take a screenshot for visual reference
agent-browser open https://client-site.com
agent-browser screenshot /tmp/brand-reference.png
```

Override the primary accent in `src/styles/globals.css`:
```css
:root {
  --color-orange: #your-brand-color;
  --color-orange-muted: #your-darker-variant;
}
```

**Anti-patterns:**
- Never use bright reds (`#DC2626`, `#E11D48`)—they read as error/danger
- Never use saturated yellows (`#fbbf24`) on light backgrounds—they disappear
- Darken to amber-800/900 range (`#92400E`, `#B45309`) for readability

### 6. Research & Content Gathering

**Available research tools (separate skills/CLIs):**

| Tool | Skill/CLI | Purpose |
|------|-----------|---------|
| **Firecrawl** | `firecrawl` CLI or Firecrawl skill | Web scraping, convert URLs to markdown |
| **Exa Search** | `exa-search` skill | AI-powered neural search, code examples |
| **Reddit JSON** | Native curl (no auth) | User feedback, pain points, discussions |

```bash
# Reddit JSON API (no auth required)
curl "https://www.reddit.com/r/{SUBREDDIT}/search.json?q={QUERY}&limit=25&sort=relevance"

# Exa Search (AI-powered)
exa-search "{domain} best practices" --type article

# Firecrawl - competitor decks, methodology pages
firecrawl scrape https://example.com/methodology
```

### 7. Build Slides

Each slide lives in `src/slides/` and uses the `SlideWrapper`:

```tsx
import { SlideWrapper } from "../components/layout/SlideWrapper";
import { Headline } from "../components/layout/Headline";
import { BodyText } from "../components/layout/BodyText";

export default function ProblemSlide() {
  return (
    <SlideWrapper mode="dark">
      <Headline>The Problem</Headline>
      <BodyText className="mt-8">Your content here</BodyText>
    </SlideWrapper>
  );
}
```

Register each slide in `src/config.ts`:
```typescript
export const slides: SlideEntry[] = [
  { id: "cover", fileKey: "01-cover", title: "Cover", shortTitle: "Cover" },
  { id: "problem", fileKey: "02-problem", title: "The Problem", shortTitle: "Problem" },
];

const slideModules = {
  "01-cover": () => import("./slides/01-cover"),
  "02-problem": () => import("./slides/02-problem"),
};
```

**Slide modes:** `dark` (deep charcoal, default), `white` (off-white, text-heavy analytical), `orange` (accent background, emphasis/quotes). Most slides use dark; white for analytical content; orange sparingly.

**Slide transitions:** the shell animates between slides via AnimatePresence, direction-aware (forward enters from the right, backward from the left). Deck-level default in `config.transition` (`none | fade | slide | scale`, default `fade`) with `config.transitionDuration` in ms; per-slide overrides via the same fields on a `SlideEntry`. One transition type per deck is the rule — per-slide overrides exist for section dividers and the closing slide, not variety. `prefers-reduced-motion` and `?static=1` both force `none`.

**Speaker notes:** `notes?: string` on any `SlideEntry` (or `notes:` in the YAML spec). Notes render only in presenter mode — the audience window never shows them.

### 8. Design QA Checklist

Before deploying, verify with agent-browser screenshots at `http://localhost:5173`:

| Check | Requirement |
|-------|-------------|
| ✅ **Slide modes** | SlideWrapper `mode` matches content type (dark/white/orange) |
| ✅ **Sidebar** | Auto-collapses after 3s, hover expands, nav indicator tracks |
| ✅ **Shader fallback** | WebGPU cover degrades to animated CSS gradient |
| ✅ **Keyboard nav** | ArrowRight/Space (next), ArrowLeft (prev), Home/End |
| ✅ **Access gate** | If configured, blocks without correct password |
| ✅ **Typography** | Playfair Display for headlines, Inter for body, IBM Plex Mono for labels |
| ✅ **Hover states** | HoverLift, GlowBorder, ExpandableCard respond correctly |
| ✅ **Animations** | StaggeredAnimation entrance on each slide, no layout thrash |
| ✅ **Mobile block** | Shows "Desktop Required" below 375px viewport |
| ✅ **Slide counter** | Bottom-right counter shows correct `01/NN` |
| ✅ **Transitions** | Forward/backward navigation animates in opposite directions; one grammar deck-wide |
| ✅ **Reduced motion** | With `prefers-reduced-motion`, transitions and auto-cycling stop, content renders final-state |
| ✅ **Presenter sync** | `/presenter/1` shows notes + next slide; navigation syncs both windows |
| ✅ **Deep links** | Invalid `/deck/N` clamps to a valid slide; deployed deep links don't 404 |

```bash
# Visual verification workflow — slides change by URL, not scroll
npm run dev &
agent-browser open http://localhost:5173/deck/1
agent-browser screenshot /tmp/slide-01.png
agent-browser open http://localhost:5173/deck/2
agent-browser screenshot /tmp/slide-02.png
```

### 9. Present

Open `/presenter/1` in a second window (or second screen) alongside the audience deck:

- Current slide, next-slide preview, speaker notes, elapsed timer, slide counter
- Keyboard navigation works in either window; a `BroadcastChannel('overwatch-deck')` keeps both in sync — navigate in the presenter, the audience follows, and vice versa
- Same-origin windows only (two tabs/windows of the same deployment); for remote presenting, share the audience window over the call and drive from the presenter

### 10. Export (PNG / PDF)

The deck stays live-first; export is derived output for board packets and email:

```bash
cd ~/.claude/skills/overwatch-slidedeck/scripts && npm install  # once: playwright, pdf-lib, yaml
npm run dev &  # deck must be serving
node ~/.claude/skills/overwatch-slidedeck/scripts/export-deck.mjs --url http://localhost:5173 --out ./export --pdf
```

Each slide renders at 1920x1080 with `?static=1` and reduced-motion emulation so entrances land in their final state — no mid-animation frames. `--pdf` merges the PNGs into `deck.pdf`. Shader covers export as their current frame; expect the live deck to look better than its export, by design.

### 11. Deploy

```bash
# Build static SPA
npm run build
# Output: dist/

# Deploy to Cloudflare Workers (wrangler.jsonc included in scaffold)
npx wrangler deploy

# Deploy to Vercel (vercel.json included)
npx vercel

# Deploy to Netlify (public/_redirects included)
npx netlify deploy --prod
```

SPA rewrites for all three hosts ship in the scaffold, so `/deck/7` opened directly on a deployed URL resolves instead of 404ing.

---

## Component Library

### Layout Components (10)

| Component | Import | Purpose |
|-----------|--------|---------|
| `SlideWrapper` | `layout/SlideWrapper` | Full-slide container with `mode` prop (dark/white/orange) |
| `Headline` | `layout/Headline` | 140px display title |
| `SubHeadline` | `layout/SubHeadline` | 72px secondary title |
| `Eyebrow` | `layout/Eyebrow` | Small caps category label |
| `BodyText` | `layout/BodyText` | Body copy (sm/md/lg) |
| `MonoLabel` | `layout/MonoLabel` | Monospace label (sm/md/lg) |
| `Divider` | `layout/Divider` | Configurable hr (thin/medium/thick) |
| `SplitLayout` | `layout/SplitLayout` | Two-column with ratio (1:1, 2:1, 1:2, 3:2, 2:3) |
| `CenterLayout` | `layout/CenterLayout` | Centered flex container |
| `GridLayout` | `layout/GridLayout` | 2/3/4 column grid |

### Interaction Components (18)

| Component | Import | Purpose |
|-----------|--------|---------|
| `AnimatedItem` | `interactions/AnimatedItem` | Entrance variants: fade/slideUp/slideLeft/scale |
| `StaggeredAnimation` | `interactions/StaggeredAnimation` | Parent container with stagger timing |
| `HoverLift` | `interactions/HoverLift` | Hover elevation (sm/md/lg) |
| `GlowBorder` | `interactions/GlowBorder` | Mouse-tracking gradient border |
| `ExpandableCard` | `interactions/ExpandableCard` | Click-to-expand with layout animation |
| `Accordion` | `interactions/Accordion` | Collapsible sections |
| `TabGroup` | `interactions/TabGroup` | Tabbed content panels |
| `QuoteRotator` | `interactions/QuoteRotator` | Auto-cycling quotes with dot indicators |
| `ContentRotator` | `interactions/ContentRotator` | Auto-cycling arbitrary ReactNode children with dots |
| `SocialProofCard` | `interactions/SocialProofCard` | Platform-styled testimonial (twitter/linkedin/testimonial) |
| `TerminalTyper` | `interactions/TerminalTyper` | Typewriter CLI demo with macOS terminal chrome |
| `TimelineConnector` | `interactions/TimelineConnector` | Horizontal roadmap with animated SVG connectors |
| `InfiniteScrollTicker` | `interactions/InfiniteScrollTicker` | Vertical marquee with gradient masks |
| `ProgressBar` | `interactions/ProgressBar` | Animated horizontal fill bar with label |
| `RevealCaption` | `interactions/RevealCaption` | Hover caption overlay |
| `Tooltip` | `interactions/Tooltip` | Position-aware tooltip |
| `PulseIndicator` | `interactions/PulseIndicator` | Pulsing dot + expanding ring |
| `Skeleton` | `interactions/Skeleton` | Loading placeholder |

### Graphics Components (4)

| Component | Import | Purpose |
|-----------|--------|---------|
| `WebGPUCanvas` | `graphics/WebGPUCanvas` | WebGPU shader host + CSS gradient fallback |
| `ParticleField` | `graphics/ParticleField` | Floating particle animation |
| `NetworkGraph` | `graphics/NetworkGraph` | Pulsing node-ring visualization |
| `SVGRadarChart` | `graphics/SVGRadarChart` | Zero-dependency SVG radar chart with pathLength animation |

### Utility Hooks (3)

| Hook | Import | Purpose |
|------|--------|---------|
| `useAutoCycle` | `hooks/useAutoCycle` | Generic auto-advancing timer: `[currentItem, index, setIndex]`. Pauses while the tab is hidden; no-ops under reduced motion |
| `useTypewriter` | `hooks/useTypewriter` | Character-by-character text reveal: `{ displayText, isComplete }`. Pauses while hidden; renders full text under reduced motion |
| `useReducedMotion` | `hooks/useReducedMotion` | Live `prefers-reduced-motion` subscription — every animated component reads it |

Every auto-cycling and entrance component honors `prefers-reduced-motion` (final state, no cycling) and interactive components (TabGroup, Accordion, Tooltip) carry ARIA roles and keyboard navigation. Global keyboard shortcuts ignore keypresses on interactive targets.

---

## Navigation

- **Sidebar:** Auto-collapses after 3s, hover to expand, spring-animated (`stiffness: 400, damping: 30`)
- **Keyboard:** ArrowRight/Space (next), ArrowLeft (prev), Home/End
- **URL-based:** `/deck/1`, `/deck/2`, etc. via TanStack Router
- **Preloading:** Adjacent slides (n-1, n+1, n+2) are preloaded for instant navigation

---

## Access Gate

Set `config.auth.password` in `src/config.ts`:
```typescript
auth: { password: "your-password" }  // Empty string = no gate
```

Supports `?pw=your-password` URL param for direct access. State persists via sessionStorage.

This is an access gate, not security: it's client-side, so the password and all slide content ship in the JavaScript bundle to anyone who requests the URL. It keeps casual link-forwards from opening the deck — the right tool for "don't let this circulate ahead of the meeting." For a deck that genuinely cannot leak (unannounced financials, M&A), put real authorization in front of the assets — Cloudflare Access or Vercel deployment protection — and keep the gate for UX.

---

## Data-Driven Authoring

For faster deck creation, provide a YAML spec file describing each slide's type, content, and mode:

```bash
node ~/.claude/skills/overwatch-slidedeck/scripts/init-deck-from-spec.mjs deck-spec.yaml ./my-deck
```

The script copies the scaffold, generates `config.ts`, and creates empty slide files. Fill in each slide using the spec + `references/slide-templates.md`.

See `references/deck-schema.md` for the full YAML schema covering all 14 slide types.

---

## Custom Asset Generation

Generate custom icons and graphics matching the Overwatch aesthetic:

**Pipeline:** Nano Banana Pro → ImageMagick → Potrace → SVG Cleanup

```bash
# Generate an icon matching the dark/orange aesthetic
nano-banana-pro "Minimalist neural network icon, flat design,
  3 solid colors, orange #ff6e41 on dark #0c0c0e, geometric"

# Vectorize
magick output.png -posterize 4 -colors 4 processed.png
potrace processed.pbm -s -o icon.svg

# Optimize
svgo icon.svg -o icon-optimized.svg
```

**Required tools:**
- `nano-banana-pro` skill (Gemini 3 Pro image generation)
- ImageMagick (`brew install imagemagick`)
- Potrace (`brew install potrace`)
- SVGO (`npm install -g svgo`)

---

## Reference Documentation

| File | Purpose |
|------|---------|
| `references/design-system.md` | Color tokens, typography, dimensions, 3 slide modes |
| `references/interactions.md` | Animation patterns, timing, 18 interaction components + the useAutoCycle/useTypewriter hooks |
| `references/shaders.md` | WebGPU setup, WGSL syntax, custom shaders, fallback |
| `references/slide-templates.md` | 14 slide type templates with component composition |
| `references/advanced-patterns.md` | 6 domain-specific patterns (waterfall, carousel, strikethrough, dual-layer shader) |
| `references/deck-schema.md` | YAML schema for data-driven deck authoring |

---

## Tips

- **One idea per slide** — keep content density low; Overwatch decks are visual, not textual
- **Slide modes matter** — dark for most content, white for analytical/text-heavy, orange for emphasis moments
- **Import from `"motion/react"`** — not `"framer-motion"` (the package is `motion` v12+)
- **Shader fallback** — always test with WebGPU disabled; the CSS gradient fallback must look intentional
- **Test keyboard nav** — ArrowRight/Space/ArrowLeft/Home/End should work on every slide
- **Preload wisely** — the scaffold preloads n-1, n+1, n+2; adjust in `routes/deck.$slide.tsx` if needed
- **Deploy early** — test on Cloudflare/Vercel before the presentation; local dev can mask font loading issues

## Related Skills

- **aldea-slidedeck** — static single-file HTML decks (Blueprint Mode). If the deck ships as a file rather than a URL, use aldea.
- **conductor-motion** — self-contained behavioral animation demos (typewriter, progress, streaming text). Borrow its timing constants for in-slide motion; don't rebuild its patterns as React components.
- **component-gallery** — pattern research for slide content (real product UI, tool-call displays, dashboards). Query it before inventing an interface mock.
- **minoan-frontend-design** — creative direction and typography once the deck structure is set.
