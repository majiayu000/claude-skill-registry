---
name: chameleon-adapt
description: Adapt UI to its environment with glassmorphism, seasonal themes, and nature components. The chameleon reads the light, blends with intention, and becomes one with the forest. Use when designing interfaces, theming pages, or making Grove feel alive.
---

# Chameleon Adapt 🦎

The chameleon doesn't force its environment to change. It reads the light, understanding where it lives. It sketches its form, creating structure. It shifts its hues, matching the forest around it. It adds texture—rough bark, smooth leaves, shifting light. Finally, it adapts completely, becoming one with its surroundings. The result feels organic, like it was always meant to be there.

## When to Activate

- User asks to "design this page" or "make it look Grove"
- User says "add some visual polish" or "theme this"
- User calls `/chameleon-adapt` or mentions chameleon/adapting
- Creating or enhancing pages for Grove sites
- Implementing seasonal decorations or weather effects
- Building glassmorphism containers for readability
- Adding nature components (trees, birds, particles)
- Working with the color palette system

---

## The Adaptation

```
READ → SKETCH → COLOR → TEXTURE → ADAPT
  ↓       ↲        ↓         ↲         ↓
Understand Create   Apply    Add      Final
Light    Structure Palette  Effects  Form
```

### Phase 1: READ

*The chameleon reads the light, understanding where it lives...*

Before choosing a single color, understand the environment:

**What season is it?**

```svelte
import { season } from '$lib/stores/season';

const isSpring = $derived($season === 'spring');
const isAutumn = $derived($season === 'autumn');
const isWinter = $derived($season === 'winter');
// Summer is the default (no flag needed)
```

**What's the emotional tone?**

| Tone | Season | Mood |
|------|--------|------|
| Hope, renewal | Spring | Cherry blossoms, new growth |
| Growth, warmth | Summer | Full foliage, activity |
| Harvest, reflection | Autumn | Falling leaves, warm colors |
| Rest, stillness | Winter | Snow, frost, evergreens |
| Dreams, far-future | Midnight | Purple glow, fireflies |

**What's the page's purpose?**
- Story/narrative pages → Full seasonal atmosphere
- Data-dense interfaces → Minimal decoration, focus on readability
- Landing/hero sections → Weather effects, randomized forests
- Forms/admin → Clean glass surfaces, no distractions

**Season Mood Summary:**

| Season | Primary Colors | Mood |
|--------|---------------|------|
| **Spring** | `springFoliage`, `cherryBlossomsPeak`, `wildflowers` | Renewal, hope |
| **Summer** | `greens`, `cherryBlossoms` | Growth, warmth |
| **Autumn** | `autumn`, `autumnReds` | Harvest, reflection |
| **Winter** | `winter` (frost, snow, frosted pines) | Rest, stillness |

**Output:** Season selection and decoration level decision (minimal/moderate/full)

---

### Phase 2: SKETCH

*The chameleon outlines its form, creating structure...*

Build the page skeleton with glassmorphism layers:

**The Layering Formula:**

```
Background (gradients, vines, nature)
    ↓
Decorative Elements (trees, clouds, particles)
    ↓
Glass Surface (translucent + blur)
    ↓
Content (text, cards, UI)
```

**Glass Components:**

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

**CSS Utility Classes:**

```html
<!-- Apply directly to any element -->
<div class="glass rounded-xl p-4">Basic glass</div>
<div class="glass-tint p-6">Text container</div>
<div class="glass-accent p-4">Highlighted section</div>
<nav class="glass-surface sticky top-0">Navbar</nav>
```

**Glass Variants:**

| Variant | Use Case | Light Mode | Dark Mode |
|---------|----------|------------|-----------|
| `surface` | Headers, navbars | 95% white | 95% slate |
| `tint` | Text over backgrounds | 60% white | 50% slate |
| `card` | Content cards | 80% white | 70% slate |
| `accent` | Callouts, highlights | 30% accent | 20% accent |
| `overlay` | Modal backdrops | 50% black | 60% black |
| `muted` | Subtle backgrounds | 40% white | 30% slate |

**Key Pattern: Sticky Navigation:**

```svelte
<nav class="sticky top-[73px] z-30 glass-surface border-b border-divider">
  <!-- Navigation content -->
</nav>
```

**Output:** Page structure with glass containers in place

---

### Phase 3: COLOR

*The chameleon shifts its hues, matching the forest around it...*

Apply the seasonal color palette:

**Import from:** `@autumnsgrove/groveengine/ui/nature`

**Core Palettes (Year-Round):**

```typescript
import { greens, bark, earth, natural } from '@autumnsgrove/groveengine/ui/nature';

// Greens - organized dark-to-light for depth
greens.darkForest   // #0d4a1c - Background trees
greens.deepGreen    // #166534 - Mid-distance
greens.grove        // #16a34a - Grove brand primary
greens.meadow       // #22c55e - Standard foliage
greens.spring       // #4ade80 - Bright accent
greens.mint         // #86efac - Light accent
greens.pale         // #bbf7d0 - Foreground highlights

// Bark - warm wood tones
bark.darkBark       // #3d2817 - Oak, older trees
bark.bark           // #5d4037 - Standard trunk
bark.warmBark       // #6B4423 - Pine, cedar
bark.lightBark      // #8b6914 - Young trees

// Earth - ground elements
earth.soil, earth.mud, earth.clay, earth.sand, earth.stone, earth.pebble, earth.slate

// Natural - cream and off-whites
natural.cream, natural.aspenBark, natural.bone, natural.mushroom, natural.birchWhite
```

**Spring Palette:**

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

**Unified Flowers Palette:**

```typescript
import { flowers } from '@autumnsgrove/groveengine/ui/nature';

// Use flowers.wildflower instead of accents.flower (deprecated)
flowers.wildflower.buttercup   // #facc15 - Yellow
flowers.wildflower.crocus      // #a78bfa - Purple crocus
flowers.wildflower.tulipPink   // #f9a8d4 - Pink tulips

// Cherry blossoms
flowers.cherry.deep      // #db2777
flowers.cherry.standard  // #ec4899
flowers.cherry.light     // #f472b6

// Cherry blossoms at peak bloom
flowers.cherryPeak.deep      // #ec4899
flowers.cherryPeak.standard  // #f472b6
```

**Autumn Palette:**

```typescript
import { autumn, autumnReds } from '@autumnsgrove/groveengine/ui/nature';

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
```

**Winter Palette:**

```typescript
import { winter } from '@autumnsgrove/groveengine/ui/nature';

// Winter - frost, snow, ice + frosted evergreens
winter.snow, winter.frost, winter.ice, winter.glacier
winter.frostedPine, winter.winterGreen, winter.coldSpruce
winter.winterSky, winter.twilight, winter.overcast
winter.bareBranch, winter.frostedBark, winter.coldWood
winter.hillDeep, winter.hillMid, winter.hillNear, winter.hillFront
```

**Midnight Bloom Palette:**

For **dreamy**, **far-future**, **mystical** content:

```typescript
import { midnightBloom } from '$lib/components/nature/palette';

midnightBloom.deepPlum   // #581c87 - Night sky depth
midnightBloom.purple     // #7c3aed - Soft purple glow
midnightBloom.violet     // #8b5cf6 - Lighter accent
midnightBloom.amber      // #f59e0b - Lantern warmth
midnightBloom.warmCream  // #fef3c7 - Tea steam, page glow
midnightBloom.softGold   // #fcd34d - Fairy lights
```

**Seasonal Helper Functions:**

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

**Accent Palettes:**

```typescript
import { accents } from '@autumnsgrove/groveengine/ui/nature';

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
```

**Output:** Color scheme applied with proper imports and seasonal variants

---

### Phase 4: TEXTURE

*The chameleon adds depth—rough bark, smooth leaves, shifting light...*

Layer nature components for atmosphere:

**Randomized Forests:**

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

function generateSectionTrees(count: number): GeneratedTree[] {
  const trees: GeneratedTree[] = [];
  const usedPositions: number[] = [];

  for (let i = 0; i < count; i++) {
    // Find non-overlapping position (8% minimum gap)
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

**Rendering Trees:**

```svelte
{#each forestTrees as tree (tree.id)}
  <div
    class="absolute"
    style="left: {tree.x}%; bottom: 0; width: {tree.size}px; 
           height: {tree.size * tree.aspectRatio}px; 
           opacity: {tree.opacity}; z-index: {tree.zIndex};
           transform: translateX(-50%);"
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

**Regeneration Timing:**

- **On mount** — Trees generate once when page loads
- **On resize (significant)** — Only if viewport bracket changes dramatically
- **Never on scroll** — Keep forest stable during reading

**Responsive Density:**

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

**Weather Effects:**

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

**Seasonal Background Gradients:**

```svelte
<main class="min-h-screen transition-colors duration-1000
  {isWinter ? 'bg-gradient-to-b from-slate-200 via-slate-100 to-slate-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-700' : ''}
  {isAutumn ? 'bg-gradient-to-b from-orange-100 via-amber-50 to-yellow-50 dark:from-slate-900 dark:via-amber-950 dark:to-orange-950' : ''}
  {isSpring ? 'bg-gradient-to-b from-pink-50 via-sky-50 to-lime-50 dark:from-slate-900 dark:via-pink-950 dark:to-lime-950' : ''}
  {/* Summer default */} 'bg-gradient-to-b from-sky-100 via-sky-50 to-emerald-50 dark:from-slate-900 dark:via-slate-800 dark:to-emerald-950'
">
```

**Seasonal Birds:**

```svelte
<!-- Winter birds -->
{#if isWinter}
  <Cardinal facing="right" class="absolute top-20 left-[15%]" />
  <Chickadee facing="left" class="absolute top-32 right-[20%]" />
{/if}

<!-- Spring birds -->
{#if isSpring}
  <Robin facing="right" class="absolute top-24 left-[10%]" />
  <Bluebird facing="left" class="absolute top-28 right-[15%]" />
{/if}
```

**Key Nature Components:**

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

**Icons: Lucide Only:**

**NEVER** use emojis. **ALWAYS** use Lucide icons.

```svelte
import { MapPin, Check, Leaf, Trees, Mail } from 'lucide-svelte';

<!-- Good -->
<MapPin class="w-4 h-4" />
<Check class="w-5 h-5 text-green-500" />

<!-- Bad - NEVER do this -->
<!-- ❌ 🌱 📧 ✅ -->
```

**Standardized Icon Mapping:**

Create a consistent icon map at the top of each component/page:

```typescript
// landing/src/lib/utils/icons.ts - Centralized icon registry
import {
  Mail, HardDrive, Palette, ShieldCheck, Cloud, SearchCode,
  Archive, Upload, MessagesSquare, Github, Check, X, Loader2,
  FileText, Tag, Sprout, Heart, ExternalLink, MapPin,
} from 'lucide-svelte';

export const featureIcons = {
  mail: Mail,
  harddrive: HardDrive,
  palette: Palette,
  shieldcheck: ShieldCheck,
  cloud: Cloud,
  searchcode: SearchCode,
} as const;
```

**Icon Usage Guidelines:**

1. **Always use icon maps** - Never hardcode icon imports in every component
2. **Avoid overusing Sparkles** - Reserve for truly mystical/magical contexts
3. **Be consistent** - Use the same icon for the same concept everywhere
4. **Semantic meaning** - Choose icons that convey meaning, not just decoration
5. **Export from central utility** - Use `landing/src/lib/utils/icons.ts`

**Icon Sizing:**

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

**Output:** Nature components layered with proper z-index and responsive density

---

### Phase 5: ADAPT

*The chameleon becomes one with its surroundings—complete adaptation...*

Final polish and accessibility:

**Mobile Responsiveness:**

```svelte
<!-- Reduce particle counts on mobile -->
<SnowfallLayer count={isLargeScreen ? 100 : 40} ... />

<!-- Responsive forest density -->
function calculateDensity(): number {
  const width = window.innerWidth;
  if (width < 768) return 1;        // Mobile
  if (width < 1024) return 1.3;     // Tablet
  if (width < 1440) return 1.8;     // Desktop
  return 2.5;                        // Large screens
}
```

**Mobile Overflow Menu:**

Desktop navigation items that don't fit should go to a mobile sheet menu:

```svelte
<!-- Mobile menu button (visible md:hidden) -->
<button onclick={() => mobileMenuOpen = true} class="md:hidden p-2">
  <Menu class="w-5 h-5" />
</button>

<!-- Sheet menu -->
<MobileMenu bind:open={mobileMenuOpen} onClose={() => mobileMenuOpen = false} />
```

**Decorative Elements on Mobile:**

| Element | Mobile Treatment |
|---------|-----------------|
| Trees | Reduce count, simplify (density multiplier = 1) |
| Particles | Reduce count (40→20 snowflakes) |
| Clouds | Hide some, keep 2-3 |
| Complex animations | Reduce or disable |
| Touch targets | Minimum 44x44px |

**Accessibility:**

```svelte
<!-- Respect reduced motion -->
{#if !prefersReducedMotion}
  <FallingLeavesLayer ... />
{/if}

<!-- Touch targets minimum 44x44px -->
<button class="p-3 min-w-[44px] min-h-[44px]">
  <Menu class="w-5 h-5" />
</button>
```

**Performance Guidelines:**

```svelte
<!-- Reduce particle counts on mobile -->
<SnowfallLayer count={isLargeScreen ? 100 : 40} ... />

<!-- Skip complex effects for reduced-motion -->
{#if !prefersReducedMotion}
  <FallingLeavesLayer ... />
{/if}
```

**User Identity Language:**

| Term | Who | Use For |
|------|-----|---------|
| **Wanderer** | Everyone | Greetings, welcome messages, all users |
| **Rooted** | Subscribers | Subscription confirmations, thank-yous |
| **Pathfinder** | Trusted guides | Community leaders (appointed) |
| **Wayfinder** | Autumn | The grove keeper (singular) |

**In UI text:**
- "Welcome, Wanderer." (not "Welcome, user")
- "Welcome back, Wanderer." (dashboard greeting)
- "You've taken root." (subscription confirmation)
- "Thanks for staying rooted." (payment received)

**Final Checklist:**

- [ ] Glass effects used for text readability over busy backgrounds?
- [ ] Lucide icons, no emojis?
- [ ] Mobile overflow menu for navigation items?
- [ ] Decorative elements respect `prefers-reduced-motion`?
- [ ] Touch targets at least 44x44px?
- [ ] Seasonal colors match the page's emotional tone?
- [ ] Trees randomized with proper spacing (8% minimum gap)?
- [ ] Dark mode supported with appropriate glass variants?
- [ ] User-facing text follows Grove voice?

**Output:** Fully adapted, accessible, responsive UI ready for production

---

## Chameleon Rules

### Intention
Every color choice serves the content. Decoration enhances readability—it never obstructs it.

### Restraint
Not every page needs a forest. Data-dense interfaces deserve clean glass surfaces without distraction.

### Authenticity
Use the seasonal system as intended. Spring isn't just "light colors"—it's renewal and hope.

### Communication
Use adaptation metaphors:
- "Reading the light..." (understanding context)
- "Sketching the form..." (building structure)
- "Shifting hues..." (applying colors)
- "Adding texture..." (layering components)
- "Full adaptation..." (final polish)

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

## Example Adaptation

**User:** "Make this about page feel like Grove"

**Chameleon flow:**

1. 🦎 **READ** — "Page is about the team's journey. Emotional tone: reflection. Season: Autumn (harvest)."

2. 🦎 **SKETCH** — "Create glass card containers, sticky nav with glass-surface, layering formula in place."

3. 🦎 **COLOR** — "Import autumn palette (rust, ember, amber, gold), warm gradients, autumnReds for accent."

4. 🦎 **TEXTURE** — "Add randomized aspen/birch trees, FallingLeavesLayer, autumn birds (cardinals), Lucide icons for UI elements."

5. 🦎 **ADAPT** — "Responsive density, reduced-motion support, 'Welcome, Wanderer' greeting, 44px touch targets, dark mode."

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| Story/narrative page | Full seasonal atmosphere, weather effects |
| Data-dense interface | Minimal decoration, focus on glass readability |
| Landing/hero section | Randomized forest, particles, seasonal birds |
| Form/admin interface | Clean glass surfaces, no nature distractions |
| Mobile-first page | Reduce tree count, simpler effects |
| Accessibility concern | Respect prefers-reduced-motion, keep glass for readability |

---

*The forest welcomes those who adapt with intention.* 🦎
