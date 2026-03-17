---
name: grove-ui-design
description: Create warm, nature-themed UI for Grove with glassmorphism, seasonal decorations, randomized forests, and accessible design patterns. Use when building pages, enhancing UI, or adding decorative elements.
---

# Grove UI Design Skill

## When to Activate

Activate this skill when:
- Creating or enhancing pages for Grove sites
- Adding decorative nature elements (trees, clouds, weather effects)
- Implementing glassmorphism effects for readability
- Working with the seasonal theme system
- Building navigation patterns (navbar, mobile overflow menus)
- Creating "story" pages that guide users through content
- Ensuring mobile-friendly, accessible UI
- Choosing icons or visual elements

## The Grove Aesthetic

Grove is a **place**. It's nature-themed, warm, and inviting—like a midnight tea shop with good documentation.

### Core Principles

```
Warm, introspective, queer, unapologetically building something meaningful.
Write with the warmth of a midnight tea shop and the clarity of good documentation.
```

**Every design choice should feel:**
- **Welcoming** — like entering a cozy space
- **Organic** — natural, not rigid or corporate
- **Readable** — content-first, decorations enhance, never obstruct
- **Alive** — subtle animations, seasonal changes, randomization

### Grove Mode & Terminology (GroveTerm V2)

Grove has a terminology system that automatically switches between Grove-themed terms and standard terms based on the user's **Grove Mode** setting. **Always use GroveTerm components instead of hardcoding Grove terminology in UI.**

By default, Grove Mode is OFF for new visitors. They see familiar terms: "Posts" instead of "Blooms", "Dashboard" instead of "Arbor", "Support" instead of "Porch". When users opt in via the footer toggle, they see the full nature-themed vocabulary with interactive definitions.

**The Component Suite:**

```svelte
import { GroveTerm, GroveSwap, GroveText, GroveSwapText, GroveIntro } from '@autumnsgrove/groveengine/ui';
import groveTermManifest from '$lib/data/grove-term-manifest.json';
```

| Component | Use Case | Behavior |
|-----------|----------|----------|
| `GroveTerm` | Interactive terms with popup definitions | Colored underline when ON, click for popup. Shows standard term when OFF. |
| `GroveSwap` | Silent text replacement | Reactively swaps text. No underline, no interaction. |
| `GroveText` | Parse `[[term]]` syntax in data strings | Renders `[[bloom\|posts]]` as interactive GroveTerm components. |
| `GroveSwapText` | Parse `[[term]]` syntax silently | Same parsing, silent swaps (no popups). |
| `GroveIntro` | "We call it X" page banners | Standardized intro below page titles. |

**Usage:**

```svelte
<!-- Interactive term with popup -->
<GroveTerm term="bloom" manifest={groveTermManifest} />

<!-- Custom display text -->
<GroveTerm term="wanderer" manifest={groveTermManifest}>wanderers</GroveTerm>

<!-- Silent swap (no popup, no underline) -->
<GroveSwap term="arbor" manifest={groveTermManifest} />

<!-- Parse [[term]] syntax in data strings (ideal for FAQ items, pricing, etc.) -->
<GroveText content="Your [[bloom|posts]] live in your [[garden|blog]]." manifest={groveTermManifest} />

<!-- Page intro banner: "we call it the Meadow" -->
<GroveIntro term="meadow" manifest={groveTermManifest} />
```

**Key Rules:**
- **Never hardcode Grove terms** in user-facing UI. Always use GroveTerm components.
- **Default is OFF** for new visitors. Standard, familiar terminology first.
- **URLs stay as Grove terms** (`/porch`, `/garden`) regardless of display mode.
- **Brand terms** (Grove) and **subscription tiers** (Seedling/Sapling/Oak/Evergreen) always show as-is.
- **Use `[[term]]` syntax** for data-driven content (FAQ items, pricing fineprint, feature lists).
- **Grove Mode store**: `groveModeStore` from `@autumnsgrove/groveengine/ui/stores`. Toggle lives in the footer.

See `docs/grove-user-identity.md` for the full identity language documentation and `packages/engine/src/lib/ui/components/ui/groveterm/` for component source.

---

## Glassmorphism Pattern

Glass effects create readability while revealing hints of background decoration.

### The Layering Formula

```
Background (gradients, vines, nature)
    ↓
Decorative Elements (trees, clouds, particles)
    ↓
Glass Surface (translucent + blur)
    ↓
Content (text, cards, UI)
```

### Glass Components

```svelte
import { Glass, GlassCard, GlassButton, GlassOverlay } from '@groveengine/ui/ui';

<!-- Container with glass effect -->
<Glass variant="tint" class="p-6 rounded-xl">
  <p>Readable text over busy backgrounds</p>
</Glass>

<!-- Card with glass styling -->
<GlassCard title="Settings" variant="default" hoverable>
  Content here
</GlassCard>

<!-- Glass button -->
<GlassButton variant="accent">Subscribe</GlassButton>
```

### Glass Variants

| Variant | Use Case | Light Mode | Dark Mode |
|---------|----------|------------|-----------|
| `surface` | Headers, navbars | 95% white | 95% slate |
| `tint` | Text over backgrounds | 60% white | 50% slate |
| `card` | Content cards | 80% white | 70% slate |
| `accent` | Callouts, highlights | 30% accent | 20% accent |
| `overlay` | Modal backdrops | 50% black | 60% black |
| `muted` | Subtle backgrounds | 40% white | 30% slate |

### CSS Utility Classes

```html
<!-- Apply directly to any element -->
<div class="glass rounded-xl p-4">Basic glass</div>
<div class="glass-tint p-6">Text container</div>
<div class="glass-accent p-4">Highlighted section</div>
<nav class="glass-surface sticky top-0">Navbar</nav>
```

### Key Pattern: Sticky Navigation

```svelte
<nav class="sticky top-[73px] z-30 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-b border-divider">
  <!-- Navigation content -->
</nav>
```

---

## Seasonal Theme System

Grove uses four seasons, each with distinct colors, weather effects, and moods.

### Season Detection

```svelte
import { season } from '$lib/stores/season';

const isSpring = $derived($season === 'spring');
const isAutumn = $derived($season === 'autumn');
const isWinter = $derived($season === 'winter');
// Summer is the default (no flag needed)
```

### Color Palette System

Import from: `@autumnsgrove/groveengine/ui/nature` or `$lib/components/nature/palette`

#### Core Palettes (Year-Round)

```typescript
import { greens, bark, earth, natural } from '@autumnsgrove/groveengine/ui/nature';

// Greens - organized dark-to-light for atmospheric depth
greens.darkForest  // #0d4a1c - Background trees
greens.deepGreen   // #166534 - Mid-distance
greens.grove       // #16a34a - Grove brand primary
greens.meadow      // #22c55e - Standard foliage
greens.spring      // #4ade80 - Bright accent
greens.mint        // #86efac - Light accent
greens.pale        // #bbf7d0 - Foreground highlights

// Bark - warm wood tones
bark.darkBark      // #3d2817 - Oak, older trees
bark.bark          // #5d4037 - Standard trunk
bark.warmBark      // #6B4423 - Pine, cedar
bark.lightBark     // #8b6914 - Young trees

// Earth - ground elements
earth.soil, earth.mud, earth.clay, earth.sand, earth.stone, earth.pebble, earth.slate

// Natural - cream and off-whites
natural.cream, natural.aspenBark, natural.bone, natural.mushroom, natural.birchWhite
```

#### Spring Palettes

```typescript
import { springFoliage, springSky, wildflowers, cherryBlossoms, cherryBlossomsPeak } from '@autumnsgrove/groveengine/ui/nature';

// Spring Foliage - yellow-green new growth
springFoliage.sprout      // #65a30d - Distant new growth
springFoliage.newLeaf     // #84cc16 - Classic spring lime
springFoliage.freshGreen  // #a3e635 - Bright foreground
springFoliage.budding     // #bef264 - Pale new leaf
springFoliage.tender      // #d9f99d - Very pale

// Spring Sky
springSky.clear    // #7dd3fc - Clear morning
springSky.soft     // #bae6fd - Pale sky

// Wildflowers - unified meadow flower colors
wildflowers.buttercup   // #facc15 - Yellow
wildflowers.daffodil    // #fde047 - Pale yellow
wildflowers.crocus      // #a78bfa - Purple crocus
wildflowers.violet      // #8b5cf6 - Wild violets
wildflowers.purple      // #a855f7 - Lupine, thistle
wildflowers.lavender    // #c4b5fd - Distant masses
wildflowers.tulipPink   // #f9a8d4 - Pink tulips
wildflowers.tulipRed    // #fb7185 - Red tulips
wildflowers.white       // #fefefe - Daisies, trillium

// Cherry Blossoms - summer standard
cherryBlossoms.deep      // #db2777 - Dense centers
cherryBlossoms.standard  // #ec4899 - Standard blossom
cherryBlossoms.light     // #f472b6 - Light petals
cherryBlossoms.pale      // #f9a8d4 - Pale blossoms
cherryBlossoms.falling   // #fbcfe8 - Falling petals

// Cherry Blossoms Peak - vibrant spring (one shade brighter!)
cherryBlossomsPeak.deep      // #ec4899
cherryBlossomsPeak.standard  // #f472b6
cherryBlossomsPeak.light     // #f9a8d4
cherryBlossomsPeak.pale      // #fbcfe8
cherryBlossomsPeak.falling   // #fce7f3
```

#### Unified Flowers Palette (NEW!)

The `flowers` namespace consolidates all flower colors into one organized structure:

```typescript
import { flowers } from '@autumnsgrove/groveengine/ui/nature';

// Meadow wildflowers (yellows, purples, pinks, whites)
flowers.wildflower.buttercup   // #facc15 - Yellow
flowers.wildflower.daffodil    // #fde047 - Pale yellow
flowers.wildflower.crocus      // #a78bfa - Purple crocus
flowers.wildflower.violet      // #8b5cf6 - Wild violets
flowers.wildflower.purple      // #a855f7 - Lupine, thistle
flowers.wildflower.lavender    // #c4b5fd - Distant masses
flowers.wildflower.tulipPink   // #f9a8d4 - Pink tulips
flowers.wildflower.tulipRed    // #fb7185 - Red tulips
flowers.wildflower.white       // #fefefe - Daisies, trillium

// Cherry blossoms - standard summer
flowers.cherry.deep      // #db2777
flowers.cherry.standard  // #ec4899
flowers.cherry.light     // #f472b6
flowers.cherry.pale      // #f9a8d4
flowers.cherry.falling   // #fbcfe8

// Cherry blossoms at peak bloom - vibrant spring
flowers.cherryPeak.deep      // #ec4899
flowers.cherryPeak.standard  // #f472b6
flowers.cherryPeak.light     // #f9a8d4
flowers.cherryPeak.pale      // #fbcfe8
flowers.cherryPeak.falling   // #fce7f3
```

**Use `flowers.wildflower` instead of `accents.flower`** — the accents version is deprecated.

#### Autumn & Winter Palettes

```typescript
import { autumn, autumnReds, winter } from '@autumnsgrove/groveengine/ui/nature';

// Autumn - warm fall foliage (dark-to-light for depth)
autumn.rust     // #9a3412 - Deep background
autumn.ember    // #c2410c - Oak-like
autumn.pumpkin  // #ea580c - Maple mid-tones
autumn.amber    // #d97706 - Classic fall
autumn.gold     // #eab308 - Aspen/birch
autumn.honey    // #facc15 - Bright foreground
autumn.straw    // #fde047 - Pale dying leaves

// Autumn Reds - cherry/maple fall foliage
autumnReds.crimson  // #be123c - Deep maple
autumnReds.scarlet  // #e11d48 - Bright cherry
autumnReds.rose     // #f43f5e - Light autumn
autumnReds.coral    // #fb7185 - Pale accent

// Winter - frost, snow, ice + frosted evergreens
winter.snow, winter.frost, winter.ice, winter.glacier
winter.frostedPine, winter.winterGreen, winter.coldSpruce
winter.winterSky, winter.twilight, winter.overcast
winter.bareBranch, winter.frostedBark, winter.coldWood
winter.hillDeep, winter.hillMid, winter.hillNear, winter.hillFront
```

#### Accent Palettes

```typescript
import { accents, wildflowers } from '@autumnsgrove/groveengine/ui/nature';

// Mushrooms - fairy tale pops of color
accents.mushroom.redCap, accents.mushroom.orangeCap, accents.mushroom.brownCap
accents.mushroom.spots, accents.mushroom.gill

// Firefly - bioluminescence
accents.firefly.glow, accents.firefly.warmGlow, accents.firefly.body

// Berry - rich saturated
accents.berry.ripe, accents.berry.elderberry, accents.berry.red

// Water - cool blue spectrum
accents.water.surface, accents.water.deep, accents.water.shallow, accents.water.lily

// Sky - time of day
accents.sky.dayLight, accents.sky.dayMid, accents.sky.sunset, accents.sky.night, accents.sky.star

// Birds - species-specific colors
accents.bird.cardinalRed, accents.bird.cardinalMask, accents.bird.cardinalBeak
accents.bird.chickadeeCap, accents.bird.chickadeeBody, accents.bird.chickadeeBelly
accents.bird.robinBody, accents.bird.robinBreast, accents.bird.robinBeak
accents.bird.bluebirdBody, accents.bird.bluebirdWing, accents.bird.bluebirdBreast

// NOTE: accents.flower is deprecated - use flowers.wildflower instead
```

#### Seasonal Helper Functions

```typescript
import { getSeasonalGreens, getCherryColors, isTreeBare, pickRandom, pickFrom } from '@autumnsgrove/groveengine/ui/nature';

// Get foliage colors mapped to season
const foliage = getSeasonalGreens(season);
// spring → springFoliage colors
// summer → greens
// autumn → autumn palette
// winter → frosted evergreen colors

// Get cherry tree colors by season
const cherryColors = getCherryColors(season);
// spring → cherryBlossomsPeak (vibrant!)
// summer → cherryBlossoms (standard)
// autumn → autumnReds
// winter → null (bare tree)

// Check if deciduous tree is bare
if (isTreeBare('cherry', 'winter')) { /* no foliage */ }

// Random color selection for natural variation
const randomGreen = pickRandom(greens);
const specificGreen = pickFrom(greens, ['grove', 'meadow']);
```

#### Deprecated Aliases (Still Work)

```typescript
// These work but will be removed in v1.0:
import { spring, pinks, springBlossoms } from '@autumnsgrove/groveengine/ui/nature';

// spring → use springFoliage, wildflowers, springSky instead
// pinks → use cherryBlossoms instead
// springBlossoms → use cherryBlossomsPeak instead
// accents.flower → use flowers.wildflower instead
```

#### Season Mood Summary

| Season | Primary Colors | Mood |
|--------|---------------|------|
| **Spring** | `springFoliage`, `cherryBlossomsPeak`, `wildflowers` | Renewal, hope |
| **Summer** | `greens`, `cherryBlossoms` | Growth, warmth |
| **Autumn** | `autumn`, `autumnReds` | Harvest, reflection |
| **Winter** | `winter` (frost, snow, frosted pines) | Rest, stillness |

### Seasonal Weather Effects

```svelte
<!-- Winter: Snowfall -->
{#if isWinter}
  <SnowfallLayer count={40} zIndex={5} opacity={{ min: 0.4, max: 0.8 }} spawnDelay={8} />
{/if}

<!-- Spring: Cherry blossom petals -->
{#if isSpring}
  <FallingPetalsLayer count={80} zIndex={100} opacity={{ min: 0.5, max: 0.9 }} />
{/if}

<!-- Autumn: Falling leaves (tied to trees) -->
{#if isAutumn}
  <FallingLeavesLayer trees={forestTrees} season={$season} minLeavesPerTree={2} maxLeavesPerTree={4} />
{/if}
```

### Seasonal Background Gradients

```svelte
<main class="min-h-screen transition-colors duration-1000
  {isWinter ? 'bg-gradient-to-b from-slate-200 via-slate-100 to-slate-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-700' : ''}
  {isAutumn ? 'bg-gradient-to-b from-orange-100 via-amber-50 to-yellow-50 dark:from-slate-900 dark:via-amber-950 dark:to-orange-950' : ''}
  {isSpring ? 'bg-gradient-to-b from-pink-50 via-sky-50 to-lime-50 dark:from-slate-900 dark:via-pink-950 dark:to-lime-950' : ''}
  {/* Summer default */} 'bg-gradient-to-b from-sky-100 via-sky-50 to-emerald-50 dark:from-slate-900 dark:via-slate-800 dark:to-emerald-950'
">
```

### When to Use Seasons

- **Roadmap pages** — Show progress through seasonal metaphor
- **Story/about pages** — Create atmosphere and emotional connection
- **Interactive demos** — Let users toggle seasons (like /forest)
- **Help articles** — Consider seasonal decor to break up long content
- **Anywhere you want magic** — Use judgment based on page purpose

---

## Randomized Forests

The forest should feel alive and different every visit.

### Tree Generation Pattern

```typescript
interface GeneratedTree {
  id: number;
  x: number;           // percentage from left (5-93% to avoid edges)
  size: number;        // base width in pixels
  aspectRatio: number; // height = size * aspectRatio (1.0-1.5 range)
  treeType: TreeType;  // 'logo' | 'pine' | 'cherry' | 'aspen' | 'birch'
  opacity: number;     // 0.5-0.9 for depth
  zIndex: number;      // larger trees = higher z-index
}

// Aspect ratio creates natural height variation
const TREE_ASPECT_RATIO_RANGE = { min: 1.0, max: 1.5 };

function generateSectionTrees(count: number): GeneratedTree[] {
  const trees: GeneratedTree[] = [];
  const usedPositions: number[] = [];

  for (let i = 0; i < count; i++) {
    // Find non-overlapping position
    let x: number;
    let attempts = 0;
    do {
      x = 5 + Math.random() * 88;
      attempts++;
    } while (usedPositions.some(pos => Math.abs(pos - x) < 8) && attempts < 20);
    usedPositions.push(x);

    const size = 80 + Math.random() * 80;
    const aspectRatio = 1.0 + Math.random() * 0.5;
    const opacity = 0.5 + Math.random() * 0.4;
    const zIndex = size > 130 ? 3 : size > 100 ? 2 : 1;

    trees.push({ id: i, x, size, aspectRatio, treeType: pickRandom(treeTypes), opacity, zIndex });
  }

  return trees.sort((a, b) => a.x - b.x);
}
```

### Regeneration Timing

- **On mount** — Trees generate once when page loads
- **On resize (significant)** — Only if viewport bracket changes dramatically
- **Never on scroll** — Keep forest stable during reading

### Rendering Trees

```svelte
{#each forestTrees as tree (tree.id)}
  <div
    class="absolute"
    style="
      left: {tree.x}%;
      bottom: 0;
      width: {tree.size}px;
      height: {tree.size * tree.aspectRatio}px;
      opacity: {tree.opacity};
      z-index: {tree.zIndex};
      transform: translateX(-50%);
    "
  >
    {#if tree.treeType === 'logo'}
      <Logo class="w-full h-full" season={$season} animate />
    {:else if tree.treeType === 'pine'}
      <TreePine class="w-full h-full" season={$season} animate />
    {:else if tree.treeType === 'cherry'}
      <TreeCherry class="w-full h-full" season={$season} animate />
    {:else if tree.treeType === 'aspen'}
      <TreeAspen class="w-full h-full" season={$season} animate />
    {:else if tree.treeType === 'birch'}
      <TreeBirch class="w-full h-full" season={$season} animate />
    {/if}
  </div>
{/each}
```

### Responsive Density

```typescript
function calculateDensity(): number {
  const width = window.innerWidth;
  if (width < 768) return 1;        // Mobile: base count
  if (width < 1024) return 1.3;     // Tablet
  if (width < 1440) return 1.8;     // Desktop
  if (width < 2560) return 2.5;     // Large desktop
  return 3.5;                        // Ultrawide
}
```

---

## Nature Components

Grove has an extensive library of decorative components. Explore with:

```bash
# Trees
ls landing/src/lib/components/trees/
ls landing/src/lib/components/nature/trees/

# Weather (seasonal particles)
ls landing/src/lib/components/nature/weather/

# Sky (clouds, stars, moon)
ls landing/src/lib/components/nature/sky/

# Botanical (leaves, petals, vines)
ls landing/src/lib/components/nature/botanical/

# Ground (flowers, grass, mushrooms)
ls landing/src/lib/components/nature/ground/

# Structural (lattice, lanterns, paths)
ls landing/src/lib/components/nature/structural/

# Birds (cardinals, robins, bluebirds)
ls landing/src/lib/components/nature/creatures/
```

### Key Components

| Component | Use | Example Props |
|-----------|-----|---------------|
| `Logo` | Grove tree, seasonal | `season`, `animate`, `breathing` |
| `TreePine` | Evergreen, stays green in autumn | `season`, `animate` |
| `TreeCherry` | Blossoms in spring, bare in winter | `season`, `animate` |
| `TreeAspen` / `TreeBirch` | Deciduous, seasonal colors | `season`, `animate` |
| `Cloud` | Decorative sky element | `variant`, `animate`, `speed`, `direction` |
| `SnowfallLayer` | Winter particles | `count`, `opacity`, `spawnDelay` |
| `FallingPetalsLayer` | Spring cherry blossoms | `count`, `opacity`, `fallDuration` |
| `FallingLeavesLayer` | Autumn leaves (tied to trees) | `trees`, `season` |
| `Cardinal` / `Chickadee` | Winter birds | `facing` |
| `Robin` / `Bluebird` | Spring birds | `facing` |
| `Vine` | Decorative ivy/vines | varies |
| `Lantern` | Warm glow points | varies |

### Birds by Season

```svelte
<!-- Winter birds -->
{#if isWinter}
  <Cardinal facing="right" style="..." />
  <Chickadee facing="left" style="..." />
{/if}

<!-- Spring birds -->
{#if isSpring}
  <Robin facing="right" style="..." />
  <Bluebird facing="left" style="..." />
{/if}
```

---

## Midnight Bloom Palette

For **dreamy**, **far-future**, **mystical** content. The tea shop that exists at the edge of tomorrow.

```typescript
import { midnightBloom } from '$lib/components/nature/palette';

// Available colors:
midnightBloom.deepPlum   // #581c87 - Night sky depth
midnightBloom.purple     // #7c3aed - Soft purple glow
midnightBloom.violet     // #8b5cf6 - Lighter accent
midnightBloom.amber      // #f59e0b - Lantern warmth
midnightBloom.warmCream  // #fef3c7 - Tea steam, page glow
midnightBloom.softGold   // #fcd34d - Fairy lights
```

### Midnight Bloom Styling

```svelte
<section class="bg-gradient-to-b from-orange-950/50 via-purple-950 to-slate-950">
  <!-- Stars -->
  <StarCluster count={12} class="absolute top-12 left-[10%]" />

  <!-- Moon -->
  <Moon phase="waning-crescent" class="absolute top-20 right-[15%] w-16 h-16 opacity-60" />

  <!-- Fireflies -->
  <Firefly count={8} class="absolute inset-0" />

  <!-- Content with purple glass -->
  <blockquote class="bg-purple-900/30 backdrop-blur-sm border border-purple-700/30 rounded-lg p-6">
    <p class="text-purple-200 italic">Dreamy quote here...</p>
  </blockquote>
</section>
```

---

## Icons: Lucide Only

**NEVER** use emojis. **ALWAYS** use Lucide icons.

```svelte
import { MapPin, Check, Leaf, Trees, Mail } from 'lucide-svelte';

<!-- Good -->
<MapPin class="w-4 h-4" />
<Check class="w-5 h-5 text-green-500" />

<!-- Bad - NEVER do this -->
<!-- ❌ 🌱 📧 ✅ -->
```

### Standardized Icon Mapping

Use these icons consistently across the project:

| Concept | Icon | Notes |
|---------|------|-------|
| **Navigation** | | |
| Home | `Home` | |
| About | `Info` | |
| Vision | `Telescope` | Looking forward |
| Roadmap | `Map` | Journey/direction |
| Pricing | `HandCoins` | Money/currency |
| Knowledge | `BookOpen` | Learning/docs |
| Forest | `Trees` | Community blogs |
| Blog | `PenLine` | Writing |
| **Features** | | |
| Email | `Mail` | |
| Storage | `HardDrive` | |
| Theming | `Palette` | Customization |
| Authentication | `ShieldCheck` | Security |
| Cloud | `Cloud` | Remote/serverless |
| Search | `SearchCode` | Code/advanced search |
| Archives | `Archive` | Backups |
| Upload | `Upload` | |
| Video | `Video` | |
| Comments | `MessagesSquare` | User discussions |
| GitHub | `Github` | External links to GitHub |
| **States** | | |
| Success | `Check` | Completed/valid |
| Error | `X` | Failed/close |
| Loading | `Loader2` | With animate-spin |
| **Content** | | |
| Posts | `FileText` | Blog posts |
| Tags | `Tag` | Categorization |
| Growth | `Sprout` | Grove brand, new beginnings |
| Heart | `Heart` | Love, care |
| External | `ExternalLink` | Opens new tab |
| Location | `MapPin` | Current position |
| **Phases** | | |
| Coming Soon | `Seedling` | Something growing |
| Refinement | `Gem` | Polish, quality |
| The Dream | `Sparkles` | Mystical (use sparingly!) |
| Night | `Star` | Midnight themes |
| **Actions** | | |
| Getting Started | `Compass` | Guidance |
| What's New | `Megaphone` | Announcements |
| Next Steps | `Lightbulb` | Ideas |

### Icon Mapping Tables in Files

Create a consistent icon map at the top of each component/page that uses icons:

```typescript
// landing/src/lib/utils/icons.ts - Centralized icon registry
import {
  Mail, HardDrive, Palette, ShieldCheck, Cloud, SearchCode,
  Archive, Upload, MessagesSquare, Github, Check, X, Loader2,
  FileText, Tag, Sprout, Heart, ExternalLink, MapPin, // ... etc
} from 'lucide-svelte';

export const featureIcons = {
  mail: Mail,
  harddrive: HardDrive,
  palette: Palette,
  shieldcheck: ShieldCheck,
  cloud: Cloud,
  searchcode: SearchCode,
  // ... all mapped icons
} as const;

export const stateIcons = {
  success: Check,
  error: X,
  loading: Loader2,
} as const;
```

Then use in components:

```svelte
<script lang="ts">
  import { featureIcons } from '$lib/utils/icons';
</script>

{#each features as feature}
  <svelte:component this={featureIcons[feature.icon]} class="w-5 h-5" />
{/each}
```

**Benefits:**
- Single source of truth for all icons
- Prevents undefined icon errors
- Easy to maintain and extend
- Reusable across entire project

### Icon Usage Guidelines

1. **Always use icon maps** - Never hardcode icon imports in every component
2. **Avoid overusing Sparkles** - Reserve for truly mystical/magical contexts
3. **Be consistent** - Use the same icon for the same concept everywhere
4. **Semantic meaning** - Choose icons that convey meaning, not just decoration
5. **Export from central utility** - Use `landing/src/lib/utils/icons.ts` for all icon sets

### Icon Sizing

```svelte
<!-- Inline with text -->
<span class="inline-flex items-center gap-1.5">
  <Leaf class="w-4 h-4" /> Feature name
</span>

<!-- Button icon -->
<button class="p-2">
  <Menu class="w-5 h-5" />
</button>

<!-- Large decorative -->
<Gem class="w-8 h-8 text-amber-400" />
```

---

## Icon Composition (Building Block Pattern)

**Philosophy:** "The grove doesn't need to be drawn. It just needs to be arranged."

For creating custom logos, illustrations, or decorative elements, compose existing Lucide icons rather than drawing custom SVG from scratch. This ensures visual consistency with the icon system.

### Why This Pattern?

- **Consistency** — Icons match the Lucide aesthetic (24x24 grid, 2px strokes, round caps)
- **Minimal custom code** — Let Lucide do the heavy lifting
- **Maintainable** — Updating Lucide updates your compositions
- **MIT licensed** — All paths come from open-source icons

### How to Extract Lucide Paths

Lucide icons use a 24×24 viewBox with 2px strokes. Extract paths directly from source:

```bash
# Find icon paths in Lucide source
curl -s https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/tree-pine.svg
# Look for the <path d="..." /> elements
```

**Key Lucide icon paths for Grove compositions:**

```typescript
// TreePine - conifer silhouette
const treePine = {
  canopy: 'm17 14 3 3.3a1 1 0 0 1-.7 1.7H4.7a1 1 0 0 1-.7-1.7L7 14h-.3a1 1 0 0 1-.7-1.7L9 9h-.2A1 1 0 0 1 8 7.3L12 3l4 4.3a1 1 0 0 1-.8 1.7H15l3 3.3a1 1 0 0 1-.7 1.7H17Z',
  trunk: 'M12 22v-3'
};

// TreeDeciduous - deciduous/round tree
const treeDeciduous = {
  canopy: 'M8 19a4 4 0 0 1-2.24-7.32A3.5 3.5 0 0 1 9 6.03V6a3 3 0 1 1 6 0v.04a3.5 3.5 0 0 1 3.24 5.65A4 4 0 0 1 16 19Z',
  trunk: 'M12 19v3'
};

// Moon - crescent moon
const moon = 'M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401';

// Flame - campfire/hearth
const flame = 'M12 3q1 4 4 6.5t3 5.5a1 1 0 0 1-14 0 5 5 0 0 1 1-3 1 1 0 0 0 5 0c0-2-1.5-3-1.5-5q0-2 2.5-4';
```

### Composing with SVG Transforms

Use `<g transform="...">` to position, scale, and rotate icons:

```svelte
<svg viewBox="0 0 48 32" fill="none">
  <!-- Left tree (larger, foreground) -->
  <g transform="translate(2, 4) scale(0.85)"
     stroke={color} stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d={treePine.canopy} />
    <path d={treePine.trunk} />
  </g>

  <!-- Right tree (smaller, background, tilted) -->
  <g transform="translate(20, 8) scale(0.65) rotate(-5, 12, 12)"
     stroke={color} stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
     opacity="0.7">
    <path d={treePine.canopy} />
    <path d={treePine.trunk} />
  </g>

  <!-- Add simple custom elements sparingly -->
  <circle cx="30" cy="10" r="1.5" fill={glowColor} opacity="0.8" /> <!-- firefly -->
  <path d="M2 28h44" stroke={color} stroke-width="1.5" opacity="0.3" /> <!-- ground -->
</svg>
```

### Transform Cheatsheet

| Transform | Effect | Example |
|-----------|--------|---------|
| `translate(x, y)` | Move origin | `translate(20, 8)` moves icon right 20, down 8 |
| `scale(s)` | Uniform size | `scale(0.65)` makes icon 65% size |
| `rotate(deg, cx, cy)` | Rotation around point | `rotate(-5, 12, 12)` tilts 5° around center |
| Combined | Chain transforms | `translate(20, 8) scale(0.65) rotate(-5, 12, 12)` |

### Example: Grove Logo Compositions

See `/landing/src/lib/components/logo-concepts/` for real implementations:

| Logo | Composition |
|------|-------------|
| `LogoFireflyForest` | TreePine + TreeDeciduous + glowing circles |
| `LogoGatheringHearth` | Two trees angled toward center Flame |
| `LogoStarlightPines` | Two TreePines + Moon + star circles |
| `LogoShelter` | Two TreePines forming archway + Moon |
| `LogoWinterGrove` | TreePines + snow line accents |

### Guidelines

1. **Use Lucide paths as primary structure** — Trees, moon, flame, etc.
2. **Custom SVG only for simple primitives** — circles (fireflies), lines (ground, snow)
3. **Maintain Lucide styling** — 2px strokes, round caps/joins, consistent opacity
4. **Create depth with opacity/scale** — Larger = foreground (opacity 0.9), smaller = background (0.5-0.7)
5. **Keep viewBox aspect ratios reasonable** — 40×32 or 48×32 for horizontal compositions

### When to Use

- **Logos & branding** — Compose icons into unique marks
- **Illustrations** — Scene building (forest, sky, etc.)
- **Custom icons** — When Lucide doesn't have exactly what you need
- **Seasonal variations** — Same composition, different elements (snow, blossoms)

---

## Mobile Considerations

### Overflow Menu Pattern

Desktop navigation items that don't fit should go to a mobile sheet menu:

```svelte
<!-- Mobile menu button (visible md:hidden) -->
<button onclick={() => mobileMenuOpen = true} class="md:hidden p-2">
  <Menu class="w-5 h-5" />
</button>

<!-- Sheet menu -->
<MobileMenu bind:open={mobileMenuOpen} onClose={() => mobileMenuOpen = false} />
```

### Decorative Elements on Mobile

| Element | Mobile Treatment |
|---------|-----------------|
| Trees | Reduce count, simplify (density multiplier = 1) |
| Particles | Reduce count (40→20 snowflakes) |
| Clouds | Hide some, keep 2-3 |
| Complex animations | Reduce or disable |
| Touch targets | Minimum 44x44px |

### Performance Guidelines

```svelte
<!-- Reduce particle counts on mobile -->
<SnowfallLayer count={isLargeScreen ? 100 : 40} ... />

<!-- Skip complex effects for reduced-motion -->
{#if !prefersReducedMotion}
  <FallingLeavesLayer ... />
{/if}
```

---

## When to Use

| Pattern | Good For |
|---------|----------|
| **Glassmorphism** | Text over backgrounds, navbars, cards, modals |
| **Randomized forests** | Story pages, about pages, visual sections |
| **Seasonal themes** | Roadmaps, timelines, emotional storytelling |
| **Midnight Bloom** | Future features, dreams, mystical content |
| **Weather particles** | Hero sections, transitions between seasons |
| **Birds** | Adding life to forest scenes, seasonal indicators |

## When NOT to Use

| Pattern | Avoid When |
|---------|------------|
| **Heavy decoration** | Data-dense pages, admin interfaces, forms |
| **Particle effects** | Performance-critical pages, accessibility concerns |
| **Seasonal colors** | Brand-critical contexts needing consistent colors |
| **Multiple glass layers** | Can cause blur performance issues |
| **Randomization** | Content that needs to match between sessions |
| **Complex forests** | Mobile-first pages, simple informational content |

---

## Reference Pages

Study these for implementation patterns:

- **`/forest`** — Full randomized forest with all seasons
- **`/roadmap`** — Seasonal sections, progressive decoration, midnight bloom
- **`/vision`** — Narrative page with glass callouts

---

## OG Images (Social Previews)

Grove uses dynamic OG images for social media previews (Discord, Twitter, iMessage, etc.).

### Architecture

OG images are generated by a separate Cloudflare Worker at `og.grove.place` due to WASM bundling limitations with SvelteKit + Cloudflare Pages.

```
grove.place/api/og?title=X
       ↓ 302 redirect
og.grove.place/?title=X
       ↓ workers-og
PNG image (1200×630)
```

### API

```
GET https://og.grove.place/?title=X&subtitle=Y&accent=HEX
```

| Param | Default | Description |
|-------|---------|-------------|
| `title` | "Grove" | Main title (max 100 chars) |
| `subtitle` | "A place to Be." | Subtitle (max 200 chars) |
| `accent` | "16a34a" | Hex color without # (forest green) |

### Adding OG to New Pages

Use the SEO component which handles OG meta tags:

```svelte
<script>
  import SEO from '$lib/components/SEO.svelte';
</script>

<SEO
  title="Page Title"
  description="Page description for search engines"
  ogImage="/api/og?title=Page%20Title&subtitle=Custom%20subtitle"
/>
```

### Files

- `packages/og-worker/` — Standalone Worker (uses `workers-og`)
- `landing/src/routes/api/og/+server.ts` — Proxy to og.grove.place
- `landing/src/lib/components/SEO.svelte` — Meta tag management

---

## Integration with Other Skills

When writing text for Grove UI (tooltips, buttons, onboarding, error messages), invoke the **grove-documentation** skill first. The voice should match the visuals.

**Typical flow:**
1. Design the UI component/page
2. Activate `grove-documentation` for any user-facing text
3. Write content following Grove voice principles
4. Return to visual implementation

---

## Quick Checklist

Before shipping a Grove page:

- [ ] Glass effects used for text readability over busy backgrounds?
- [ ] Lucide icons, no emojis?
- [ ] Mobile overflow menu for navigation items?
- [ ] Decorative elements respect `prefers-reduced-motion`?
- [ ] Touch targets at least 44x44px?
- [ ] Seasonal colors match the page's emotional tone?
- [ ] Trees randomized with proper spacing (8% minimum gap)?
- [ ] Dark mode supported with appropriate glass variants?
- [ ] User-facing text follows Grove voice (see `grove-documentation`)?
- [ ] Grove terminology uses GroveTerm components (not hardcoded)?
- [ ] Data-driven content uses `[[term]]` syntax with GroveText?
