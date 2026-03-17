---
name: aldea-slidedeck
description: Create Aldea-branded technical slide decks with Blueprint (Next.js 14, PDF export, dark/light themes) or Overwatch (Vite+React 19, live SPA, WebGPU shaders, Framer Motion). Supports 4 domains, 30+ components, 16 reference files, visual QA via agent-browser.
---

# Aldea Slide Deck Designer

Create professional technical slide decks with two modes:

1. **Blueprint Mode** (original) — Next.js 14, 1280x720, PDF-first, cyan blueprint grid, static slides
2. **Overwatch Mode** (new) — Vite + React 19, 1920x1080, live SPA, WebGPU shaders, Framer Motion orchestration, interactive hover states, collapsible sidebar navigation

## Mode Selection Guide

| Factor | Blueprint Mode | Overwatch Mode |
|--------|---------------|----------------|
| **Distribution** | PDF, email, print | Live URL, screen presentations |
| **Audience** | Non-technical, board, clients | Technical, investors, demos |
| **Interactivity** | Static (lightbox clicks) | Hover effects, content swaps, tooltips, shaders |
| **Dimensions** | 1280x720 | 1920x1080 |
| **Framework** | Next.js 14 | Vite + React 19 + TanStack Router |
| **Animation** | Basic motion enter/exit | Deep Framer Motion orchestration |
| **Graphics** | Static SVG, Recharts | WebGPU shaders, particle fields, network graphs |
| **Auth** | None | Optional password gate |
| **Deploy** | Static HTML + PDF | Cloudflare Workers, Vercel, Netlify |

## When to Use This Skill

- Creating new presentation decks for Aldea projects
- Building technical journey/progress presentations
- Scaffolding a Next.js slide deck with Aldea design system
- Exporting decks to PDF or static HTML for sharing
- Visualizing data, metrics, training results, or architecture

## Domains Supported

| Domain | Use Cases |
|--------|-----------|
| **Business & Finance** | KPI dashboards, revenue charts, growth trends, pricing |
| **Healthcare** | Patient metrics, clinical outcomes, treatment timelines |
| **Wellness & Coaching** | Transformation journeys, milestone celebrations, quotes |
| **AI/ML Research** | Model architecture, training metrics, STT/TTS pipelines |

---

## Design Philosophy

**Theme Selection:** Choose based on audience and distribution format.
- **Dark mode** (default): Tech/AI audiences, on-screen presentations. Deep canvas (`#0a0f1a`) with vivid cyan accents (`#00d4ff`).
- **Light mode**: PDF distribution, non-technical audiences. Off-white canvas (`#FAFBFC`) with darkened accents. See `references/design-system.md` > Light Mode.

**Blueprint Aesthetic:**
- Dual-layer grid overlay (40px coarse + 10px fine)
- Corner marks with dynamic chapter coloring via `--corner-color` CSS variable
- Clean typographic hierarchy (Major Third 1.25x ratio)

**Typography Stack:**
- Display: Playfair Display (titles, headers)
- Body: DM Sans (content, descriptions) — minimum 16px (`text-base`) for body text
- Mono: JetBrains Mono (code, labels, technical text)

**Dimensions:**
- 1280px × 720px (16:9 aspect ratio)
- Print-safe color preservation
- PDF-optimized page breaks

---

## Quick Start Workflow

### 1. Audit Reference Decks (REQUIRED)

**Before designing, audit the existing example decks for inspiration and consistency.**

```bash
# Open reference decks for audit
open ~/.claude/skills/aldea-slidedeck/assets/examples/

# Reference decks available:
# - Aldea - AI Advisor Journey - Jan 2026.pdf (dark mode, original blueprint)
# - parenting-app-user-flows-2026-01-09.pdf (dark mode, 22-slide technical)
# - subq-media-thought-leaders-2026-02.pdf (LIGHT MODE, 18-slide media deck)
```

**Audit checklist - extract from reference decks:**

| Element | What to Note |
|---------|--------------|
| **TOC Structure** | Chapter naming convention, numbering format (00, 01, 02...) |
| **Logo Placement** | Top-right Aldea logo, brightness/contrast filters |
| **Content Centering** | Horizontal centering patterns, vertical alignment |
| **Color Usage** | Accent colors per section, card border colors |
| **Typography** | Title sizes, label casing (uppercase mono for badges) |
| **Slide Chrome** | Chapter badges, slide numbers, decorative lines |
| **Image Treatment** | Opacity levels, gradient overlays, positioning |

### 2. Scaffold New Project

```bash
# Create project directory
mkdir my-slidedeck && cd my-slidedeck

# Copy scaffold files from this skill's assets
cp -r ~/.claude/skills/aldea-slidedeck/assets/scaffold/* .

# Install dependencies
npm install

# Start dev server
npm run dev  # Opens at http://localhost:3200
```

### 3. Review Iconography Options

**Before building, review available icons for your domain.**

See `references/icon-reference.md` for full library with domain-specific recommendations.

| Domain | Key Icons |
|--------|-----------|
| **AI/ML** | Brain, Cpu, Database, Layers, Network, Waveform |
| **Business** | TrendingUp, DollarSign, PieChart, Target, Users |
| **Healthcare** | Heart, Activity, Stethoscope, ShieldCheck |
| **Parenting** | Baby, Users, HandHeart, Shield, Brain, Puzzle |
| **Spirituality** | Compass, Flame, Mountain, Sunrise, Lightbulb |

**Icon libraries available:**
- **Lucide** (1,500+): `lucide-react` - General purpose, clean
- **Tabler** (5,900+): `@tabler/icons-react` - Largest collection
- **Phosphor** (7,000+): `@phosphor-icons/react` - Multiple weights (thin/bold/fill)

**Finding icons:**
- Lucide: https://lucide.dev/icons
- Tabler: https://tabler.io/icons
- Phosphor: https://phosphoricons.com

### 4. Plan Content Structure

Before building slides:
1. **Define chapters** - Group content into 4-8 logical chapters (follow `XX — CHAPTER NAME` format)
2. **Outline slides** - 3-5 slides per chapter
3. **Identify slide types** - Title, TOC, metrics, workflow, comparison, etc.
4. **Gather assets** - Screenshots, diagrams, logos, expert photos
5. **Select icons** - Map icons to chapters/concepts using icon reference

### 5. Brand Color Extraction

**Before building slides, extract and map brand colors from the client/company site.**

```bash
# Scrape the client/company site for brand identity (colors, fonts, typography)
python3 ~/.claude/skills/firecrawl/scripts/firecrawl_api.py scrape "https://client-site.com" --formats branding

# Or take a screenshot for visual reference
agent-browser open https://client-site.com
agent-browser screenshot /tmp/brand-reference.png
```

**Map extracted brand colors to chapter accents** in `slides/constants.ts`:
```tsx
// Brand alignment: [source] → [deck color]
// Example: aldea.ai primary gradient amber-to-indigo
// → Chapter accents darkened for light-mode readability
export const CH: Record<string, { color: string; icon: any; label: string }> = {
  '01': { color: '#1E3A8A', icon: Globe, label: 'Chapter One' },
  // ...
};
```

**Anti-patterns:**
- Never use bright reds (`#DC2626`, `#E11D48`) — they read as error/danger
- Never use saturated yellows (`#fbbf24`) on light backgrounds — they disappear
- Darken to amber-800/900 range (`#92400E`, `#B45309`) for readability

### 6. Research & Content Gathering

**Available research tools (separate skills/CLIs):**

| Tool | Skill/CLI | Purpose |
|------|-----------|---------|
| **Firecrawl** | `firecrawl` CLI or Firecrawl skill | Web scraping, convert URLs to markdown |
| **Exa Search** | `exa-search` skill | AI-powered neural search, code examples |
| **Reddit JSON** | Native curl (no auth) | User feedback, pain points, discussions |
| **Perplexity** | Perplexity MCP | Research synthesis, fact-checking |

**Tools for domain research:**

```bash
# Reddit JSON API (no auth required) - user feedback, pain points
curl "https://www.reddit.com/r/{SUBREDDIT}/search.json?q={QUERY}&limit=25&sort=relevance"
curl "https://www.reddit.com/r/{SUBREDDIT}/top.json?t=month&limit=50"

# Exa Search (AI-powered) - expert content, articles
exa-search "{domain} best practices" --type article

# Firecrawl - competitor decks, methodology pages
firecrawl scrape https://example.com/methodology
```

**Reddit JSON trick:** Append `.json` to any Reddit URL for structured data:
- `reddit.com/r/{sub}/top.json?t=year` - Top posts
- `reddit.com/r/{sub}/search.json?q=query` - Search results
- `reddit.com/r/{sub}/comments/POST_ID.json` - Post + comments

**Domain-specific subreddits:**

| Domain | Subreddits |
|--------|------------|
| **Parenting** | r/Parenting, r/NewParents, r/Mommit, r/Daddit, r/toddlers |
| **AI/ML** | r/MachineLearning, r/LocalLLaMA, r/artificial |
| **Healthcare** | r/medicine, r/nursing, r/healthIT |
| **Business** | r/startups, r/Entrepreneur, r/smallbusiness |

### 7. Build Slides

Each slide uses the `SlideLayout` wrapper with optional `chapterColor` and `chapterIcon` for dynamic styling:

```tsx
import { CH, TOTAL } from './constants';
import { SectionHeader, GradientCard } from './helpers';

<SlideLayout
  chapter="01 — CHAPTER NAME"
  slideNumber={3}
  totalSlides={TOTAL}
  chapterColor={CH['01'].color}
  chapterIcon={CH['01'].icon}
>
  <div className="h-full flex flex-col px-16 pt-16 pb-10">
    <SectionHeader icon={Globe} color={CH['01'].color}>
      Section Title Here
    </SectionHeader>
    <div className="grid grid-cols-3 gap-5 flex-1">
      {/* Use distinct colors per card — see Card Color Strategy */}
      <GradientCard color="#1E3A8A" icon={Globe}>...</GradientCard>
      <GradientCard color="#059669" icon={Leaf}>...</GradientCard>
      <GradientCard color="#B45309" icon={Star}>...</GradientCard>
    </div>
  </div>
</SlideLayout>
```

### 8. Design QA Checklist (REQUIRED)

**Before exporting, compare your deck against reference decks.**
See `references/visual-qa-checklist.md` for the full bug catalog and `references/2026-best-practices.md` for typography/density rules.

| Check | Requirement |
|-------|-------------|
| ✅ **TOC Slide** | Matches chapter structure, clickable cards with `scrollIntoView` navigation |
| ✅ **Logo** | Aldea logo top-right on every slide (black for light mode, white for dark) |
| ✅ **Centering** | Content horizontally centered (`items-center`, `text-center`) |
| ✅ **Chapter Badges** | Format: `XX — CHAPTER NAME`, uppercase, top-left, chapter-colored |
| ✅ **Slide Numbers** | Format: `01 / NN`, mono font, below logo |
| ✅ **Card Colors** | Distinct accent colors per card in grids of 3+ (see Card Color Strategy) |
| ✅ **Body Text** | Minimum 16px (`text-base`) — never `text-sm` for body content |
| ✅ **Content Density** | ≤ 40 words per content slide, one main idea per slide |
| ✅ **GlowBadge Size** | `size="sm"` for inline badges, `size="md"` for standalone |
| ✅ **StatsBar Position** | In-flow (`mt-auto`), never absolute positioned |
| ✅ **Color Readability** | No bright reds or saturated yellows on light backgrounds |
| ✅ **Grid Spacing** | Consistent `gap-4` or `gap-6` between elements |

#### Visual Verification with agent-browser

```bash
# Start dev server
npm run dev &

# Screenshot each slide for visual inspection
agent-browser open http://localhost:3200
agent-browser screenshot /tmp/slide-01.png  # Title
agent-browser scroll down 720
agent-browser screenshot /tmp/slide-02.png  # TOC
# ... repeat for each slide

# Read each screenshot and check for:
# - Text overlapping other elements
# - Colors unreadable against background
# - Cards/bars extending beyond parent containers
# - GlowBadge text disproportionate to surrounding text
# - StatsBar colors matching corresponding GradientCards
```

### 9. Export & Share

```bash
# Build static HTML (shareable folder)
npm run export
# Output: out/

# Generate PDF (requires dev server running)
npm run dev &
npm run pdf
# Output: output/[name]-YYYY-MM-DD.pdf

# Verify page count matches slide count
mdls -name kMDItemNumberOfPages output/*.pdf

# Zip for distribution
zip -rq deck.zip out/
```

---

## Component Library

### Core Components

| Component | Purpose |
|-----------|---------|
| `SlideLayout` | Universal wrapper with branding, grid, chrome. Props: `chapterColor`, `chapterIcon` |
| `SectionHeader` | Centered icon + gradient lines + heading. Props: `icon`, `color`, `children` |
| `GradientCard` | Rounded card with gradient bg + left accent bar. Props: `color`, `icon?`, `children` |
| `StatsBar` | In-flow stats footer (NOT absolute). Props: `stats: { value, label, color }[]` |
| `GlowBadge` | Inline metric callout with glow shadow. Props: `color`, `children`, `size: 'sm'\|'md'` |
| `MetricCard` | Numbered key points with descriptions |
| `FlowDiagram` | Sequential workflow visualization |
| `ComparisonTable` | Feature comparison matrices |
| `CodeBlock` | Syntax-highlighted code snippets |
| `ImageLightbox` | Zoomable image with modal overlay |
| `ImageGallery` | Grid of lightbox-enabled images |

### Chart Components (Recharts)

| Component | Purpose |
|-----------|---------|
| `ChartCard` | Wrapper with blueprint styling |
| `MetricsChart` | Line/area charts for time series |
| `ComparisonChart` | Bar charts for comparisons |
| `RadarChart` | Multi-dimensional analysis |

### Animation Components (Motion)

| Component | Purpose |
|-----------|---------|
| `AnimatedSlide` | Entrance animations (fade, slideUp, scale, blur) |
| `AnimatedList` | Staggered list item reveals |
| `AnimatedNumber` | Counter animation for metrics |

### Diagram Components

| Component | Purpose |
|-----------|---------|
| `ArchitectureDiagram` | Node-based system diagrams (React Flow) |
| `MermaidDiagram` | Markdown-based flowcharts (Mermaid) |

### ML Visualization Components

| Component | Purpose |
|-----------|---------|
| `AttentionHeatmap` | Transformer attention weight visualization |
| `AudioWaveform` | STT/TTS audio signal display |
| `TrainingMetrics` | Loss/accuracy training curves |

---

## Slide Type Templates

| Type | Use Case | Key Elements |
|------|----------|--------------|
| **Title** | Opening slide | Large logo, title, subtitle, decorative lines |
| **TOC** | Chapter overview | Expandable cards, color-coded chapters, icons |
| **Metrics Grid** | KPIs, evaluation criteria | 3-column MetricCard grid |
| **Workflow** | Process flows | FlowDiagram + info boxes |
| **Technical** | Architecture, code | CodeBlock + description sidebar |
| **Comparison** | Feature matrices | ComparisonTable or side-by-side columns |
| **Image** | Screenshots, diagrams | Full-width image with lightbox |
| **Timeline** | Chronological events | Horizontal timeline with markers |
| **Chart** | Data visualization | MetricsChart/ComparisonChart in ChartCard |
| **Architecture** | System diagrams | ArchitectureDiagram with custom nodes |
| **Training** | ML results | TrainingMetrics with loss/accuracy curves |

See `references/slide-templates.md` for detailed templates.

---

## Icon Libraries

Included icon packs:

| Library | Import | Icons |
|---------|--------|-------|
| **Lucide** | `lucide-react` | 1,500+ |
| **Tabler** | `@tabler/icons-react` | 5,900+ |
| **Phosphor** | `@phosphor-icons/react` | 7,000+ |

See `references/icon-reference.md` for domain-specific recommendations.

---

## Domain Templates

Pre-built templates for common use cases:

```
domain-templates/
├── business/      # KPI dashboards, revenue charts, pricing
├── healthcare/    # Patient metrics, clinical outcomes
├── wellness/      # Transformation journeys, quotes
└── ml-research/   # Model architecture, training, STT/TTS
```

Import and customize:

```tsx
// Example: ML training slide
import { TrainingProgressSlide } from '../domain-templates/ml-research/templates';

<TrainingProgressSlide slideNumber={15} />
```

---

## Color Palette

### Dark Mode
```css
--canvas-900: #0a0f1a;  --canvas-800: #0f1729;  --canvas-700: #141e35;
--text-primary: #e2e8f0; --text-secondary: #94a3b8; --text-muted: #64748b;
--blueprint-cyan: #00d4ff; --blueprint-grid: rgba(30,58,95,0.25);
```

### Light Mode (recommended for PDF)
```css
--canvas-900: #FAFBFC;  --canvas-800: #F1F3F5;  --canvas-700: #E8ECF0;
--text-primary: #1A1D23; --text-secondary: #4A5568; --text-muted: #8896A6;
--blueprint-cyan: #0891B2; --blueprint-grid: rgba(100,130,170,0.08);
```

### Chart Colors (both themes)
```css
#00d4ff / #0891B2  /* Cyan - primary data */
#60a5fa            /* Blue - secondary */
#a78bfa            /* Purple - tertiary */
#34d399 / #059669  /* Green - positive */
#f97316 / #B45309  /* Orange - warning */
```

See `references/design-system.md` for full token tables and card color strategy.

---

## Reference Documentation

| File | Purpose |
|------|---------|
| `references/design-system.md` | Colors (dark + light), typography, spacing, grid, card color strategy |
| `references/component-patterns.md` | Component props, examples, TOC navigation pattern |
| `references/visual-qa-checklist.md` | Agent-browser screenshot workflow, 10 common visual bugs + fixes |
| `references/2026-best-practices.md` | Typography scale, content density, color rules, structural patterns |
| `references/slide-templates.md` | 8+ slide type templates |
| `references/export-workflow.md` | PDF and static export guide |
| `references/data-visualization.md` | Chart components and best practices |
| `references/icon-reference.md` | Icon libraries by domain |
| `references/animation-patterns.md` | Motion components and timing |
| `references/ml-visualization.md` | ML-specific components |
| `references/custom-asset-generation.md` | Custom icon/graphic generation pipeline |

---

## Custom Asset Generation

Generate custom icons and graphics matching the blueprint aesthetic:

**Pipeline:** Nano Banana Pro → ImageMagick → Potrace → SVG Cleanup

```bash
# Generate blueprint-styled icon
nano-banana-pro "Minimalist neural network icon, flat design,
  3 solid colors, cyan #00d4ff on dark #0a0f1a, geometric"

# Vectorize
magick output.png -posterize 4 -colors 4 processed.png
potrace processed.pbm -s -o icon.svg

# Optimize
svgo icon.svg -o icon-optimized.svg
```

**Alternative:** Use SVGMaker MCP for direct text-to-SVG generation.

**Required Tools:**
- `nano-banana-pro` skill (Gemini 3 Pro image generation)
- ImageMagick (`brew install imagemagick`)
- Potrace (`brew install potrace`)
- SVGO (`npm install -g svgo`)

See `references/custom-asset-generation.md` for full workflow and domain-specific prompts

---

## Overwatch Mode

### When to Use Overwatch Mode

- Live presentations (investor pitches, product demos, conference talks)
- Interaction-rich decks with hover states, content swaps, tooltips
- WebGPU shader backgrounds for dramatic cover slides
- Decks that need password protection
- Keyboard-navigated presentations with sidebar navigation

### Quick Start (Overwatch Mode)

```bash
# Create project from Overwatch scaffold
cp -r ~/.claude/skills/aldea-slidedeck/assets/scaffold-overwatch/ ./my-deck
cd my-deck

# Install dependencies
npm install

# Start dev server
npm run dev  # Opens at http://localhost:5173
# Navigate to /deck/1
```

### Adding Slides

1. Create a new file in `src/slides/` (e.g., `02-problem.tsx`):
```tsx
import { SlideWrapper } from "../components/layout/SlideWrapper";
import { SplitLayout } from "../components/layout/SplitLayout";
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

2. Register in `src/config.ts`:
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

### Component Library (Overwatch)

#### Layout Components
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

#### Interaction Components
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

#### Graphics Components
| Component | Import | Purpose |
|-----------|--------|---------|
| `WebGPUCanvas` | `graphics/WebGPUCanvas` | WebGPU shader host + CSS gradient fallback |
| `ParticleField` | `graphics/ParticleField` | Floating particle animation |
| `NetworkGraph` | `graphics/NetworkGraph` | Pulsing node-ring visualization |
| `SVGRadarChart` | `graphics/SVGRadarChart` | Zero-dependency SVG radar chart with pathLength animation |

#### Utility Hooks
| Hook | Import | Purpose |
|------|--------|---------|
| `useAutoCycle` | `hooks/useAutoCycle` | Generic auto-advancing timer: `[currentItem, index, setIndex]` |
| `useTypewriter` | `hooks/useTypewriter` | Character-by-character text reveal: `{ displayText, isComplete }` |

### Navigation

- **Sidebar:** Auto-collapses after 3s, hover to expand, spring-animated
- **Keyboard:** ArrowRight/Space (next), ArrowLeft (prev), Home/End
- **URL-based:** `/deck/1`, `/deck/2`, etc. via TanStack Router
- **Preloading:** Adjacent slides are preloaded for instant navigation

### Password Protection

Set `config.auth.password` in `src/config.ts`:
```typescript
auth: { password: "your-password" }  // Empty string = no auth
```

Supports `?pw=your-password` URL param for direct access.

### Data-Driven Authoring

For faster deck creation, provide a YAML spec file that describes each slide's type, content, and mode. The spec serves as Claude's brief—not template codegen.

```bash
# Initialize a new deck from a YAML spec
node ~/.claude/skills/aldea-slidedeck/scripts/init-deck-from-spec.mjs deck-spec.yaml ./my-deck
```

The script copies the scaffold, generates `config.ts`, and creates empty slide files. Claude then fills in each slide using the spec + `references/overwatch-slide-templates.md`.

See `references/overwatch-deck-schema.md` for the full YAML schema covering all 14 slide types.

### Deployment

```bash
# Build static SPA
npm run build
# Output: dist/

# Deploy to Cloudflare Workers
npx wrangler deploy

# Deploy to Vercel
npx vercel

# Deploy to Netlify
npx netlify deploy --prod
```

**No PDF export** — Overwatch Mode is for live presentations. For static output, use agent-browser screenshots.

### Overwatch Reference Documentation

| File | Purpose |
|------|---------|
| `references/overwatch-design-system.md` | Color tokens, typography, dimensions, slide modes |
| `references/overwatch-interactions.md` | Animation patterns, timing, 19 interaction components + hooks |
| `references/overwatch-shaders.md` | WebGPU setup, WGSL syntax, custom shaders, fallback |
| `references/overwatch-slide-templates.md` | 14 slide type templates with component composition |
| `references/overwatch-advanced-patterns.md` | Reference-only patterns: waterfall, carousel, strikethrough, dual-layer shader |
| `references/overwatch-deck-schema.md` | YAML schema for data-driven deck authoring |

---

## Blueprint Mode (Original)

The sections below document the original Blueprint Mode.

## Scaffold Assets

- `assets/scaffold/` - Blueprint Mode starter template
  - package.json with all dependencies
  - Component library (20+ components): SlideLayout, SectionHeader, GradientCard, StatsBar, GlowBadge, MetricCard, FlowDiagram, etc.
  - CSS design tokens (globals.css) with both dark and light mode themes
  - Export script (export-pdf.js)
  - `slides/` - Modular file structure template
  - `public/images/aldea-logo.png` — White logo (dark mode)
  - `public/images/aldea-logo-black.png` — Black logo (light mode)

- `assets/scaffold-overwatch/` - Overwatch Mode starter template
  - Vite + React 19 + TanStack Router + Framer Motion + Tailwind 4
  - 10 layout components: SlideWrapper, Headline, SubHeadline, Eyebrow, BodyText, MonoLabel, Divider, SplitLayout, CenterLayout, GridLayout
  - 12 interaction components: AnimatedItem, StaggeredAnimation, HoverLift, GlowBorder, ExpandableCard, Accordion, TabGroup, QuoteRotator, RevealCaption, Tooltip, PulseIndicator, Skeleton
  - 3 graphics components: WebGPUCanvas (with CSS gradient fallback), ParticleField, NetworkGraph
  - 1 WGSL shader: lava-nebula.wgsl (raymarching nebula effect)
  - Chrome: DeckShell, PasswordGate, MobileBlock, SlideCounter
  - Navigation: Sidebar (collapsible), SlideScaler (ResizeObserver), KeyboardNav (arrow/space/home/end)
  - Example cover slide with shader background
  - CSS design tokens with 3 slide modes (dark/white/orange)

- `assets/examples/` - **Reference decks for audit workflow**
  - `Aldea - AI Advisor Journey - Jan 2026.pdf` - Dark mode, original blueprint aesthetic
  - `parenting-app-user-flows-2026-01-09.pdf` - Dark mode, 22-slide technical deck
  - `subq-media-thought-leaders-2026-02.pdf` - **LIGHT MODE**, 18-slide media deck — brand-aligned colors, distinct card colors, GradientCard/GlowBadge components
  - `static-export/` - HTML export example with all assets

---

## Dependencies

```json
{
  "recharts": "^2.12.0",
  "lucide-react": "^0.468.0",
  "@tabler/icons-react": "^3.24.0",
  "@phosphor-icons/react": "^2.1.0",
  "motion": "^11.15.0",
  "@xyflow/react": "^12.3.0",
  "mermaid": "^11.4.0"
}
```

---

## Example Usage

```bash
# User request:
"Create a slide deck for the parenting app user flows"

# Workflow (follows 9-step process):
1. AUDIT: Open assets/examples/, review existing decks for TOC, logos, centering
2. SCAFFOLD: Copy assets/scaffold/* to new project, npm install, npm run dev
3. ICONS: Review references/icon-reference.md, select Parenting domain icons
4. PLAN: Define chapters (00-Pre-Session, 01-First Launch, etc.), outline slides
5. BRAND: Extract brand colors with Firecrawl, map to chapter accents in constants.ts
6. RESEARCH: Use Reddit JSON API for user pain points, Exa for expert content
7. BUILD: Create slides with SlideLayout + chapterColor/chapterIcon, use distinct card colors
8. QA: Visual verification with agent-browser screenshots, check against 2026-best-practices.md
9. EXPORT: npm run pdf, verify page count with mdls
```

## Tips

- **Keep slides focused** - One main idea per slide, ≤ 40 words per content slide
- **Use consistent spacing** - px-16 horizontal, pt-16/pb-10 vertical
- **Leverage new components** - SectionHeader for headings, GradientCard for content, StatsBar for metrics
- **Distinct card colors** - Never use the same accent for all cards in a grid of 3+
- **Body text minimum 16px** - Use `text-base`, never `text-sm` for body content
- **GlowBadge sizing** - `size="sm"` for inline, `size="md"` for standalone
- **StatsBar in-flow** - Always `mt-auto`, never absolute positioned
- **Visual verify** - Screenshot every slide with agent-browser before export
- **Test exports early** - PDF rendering may differ from browser
- **Update slide count** - TOTAL in constants.ts, SlideLayout shows "/ N"
