---
name: chameleon-adapt
description: Adapt UI to its environment with glassmorphism, seasonal themes, and nature components. The chameleon reads the light, blends with intention, and becomes one with the forest. Use when designing interfaces, theming pages, or making Grove feel alive.
---

# Chameleon Adapt

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

---

## Reference Routing Table

| Phase   | Reference                          | Load When                                   |
| ------- | ---------------------------------- | ------------------------------------------- |
| READ    | —                                  | No reference needed (context assessment)    |
| SKETCH  | `references/layout-patterns.md`    | When designing page structure               |
| COLOR   | `references/color-palette.md`      | When applying seasonal colors               |
| COLOR   | `references/groveterm-system.md`   | When writing user-facing text               |
| TEXTURE | `references/glass-components.md`   | When adding glassmorphism                   |
| TEXTURE | `references/nature-components.md`  | When adding nature decorations              |

---

### Phase 1: READ

_The chameleon reads the light, understanding where it lives..._

Before choosing a single color, understand the environment. Assess three things:

**What season is it?**

```svelte
import { season } from '$lib/stores/season';

const isSpring = $derived($season === 'spring');
const isAutumn = $derived($season === 'autumn');
const isWinter = $derived($season === 'winter');
// Summer is the default (no flag needed)
```

**What's the emotional tone?**

| Tone                | Season   | Mood                        |
| ------------------- | -------- | --------------------------- |
| Hope, renewal       | Spring   | Cherry blossoms, new growth |
| Growth, warmth      | Summer   | Full foliage, activity      |
| Harvest, reflection | Autumn   | Falling leaves, warm colors |
| Rest, stillness     | Winter   | Snow, frost, evergreens     |
| Dreams, far-future  | Midnight | Purple glow, fireflies      |

**Season Mood Summary:**

| Season     | Primary Colors                                       | Mood                |
| ---------- | ---------------------------------------------------- | ------------------- |
| **Spring** | `springFoliage`, `cherryBlossomsPeak`, `wildflowers` | Renewal, hope       |
| **Summer** | `greens`, `cherryBlossoms`                           | Growth, warmth      |
| **Autumn** | `autumn`, `autumnReds`                               | Harvest, reflection |
| **Winter** | `winter` (frost, snow, frosted pines)                | Rest, stillness     |

**What's the page's purpose?**

- Story/narrative pages — Full seasonal atmosphere
- Data-dense interfaces — Minimal decoration, focus on readability
- Landing/hero sections — Weather effects, randomized forests
- Forms/admin — Clean glass surfaces, no distractions

**Output:** Season selection and decoration level decision (minimal / moderate / full)

---

### Phase 2: SKETCH

_The chameleon outlines its form, creating structure..._

Build the page skeleton with glassmorphism layers. Establish the layering formula, place glass containers, and wire up the sticky navigation pattern.

Key decisions: Which glass variant fits each container? Where does content live in the z-index stack? What's the responsive breakdown?

**Reference:** Load `references/layout-patterns.md` for the layering formula, sticky nav pattern, page section templates, responsive grid patterns, spacing system, and accessibility layout rules.

**Quick glass starter:**

```svelte
import { Glass, GlassCard, GlassButton } from '@lattice/ui/ui';

<Glass variant="tint" class="p-6 rounded-xl">
  <p>Readable text over busy backgrounds</p>
</Glass>
```

**Reference:** Load `references/glass-components.md` for all glass variants, props, CSS utility classes, and composition patterns.

**Output:** Page structure with glass containers and z-index layers in place

---

### Phase 3: COLOR

_The chameleon shifts its hues, matching the forest around it..._

Apply the seasonal color palette from `@autumnsgrove/lattice/ui/nature`. Match palette choice to the emotional tone identified in READ. Use seasonal helper functions (`getSeasonalGreens`, `getCherryColors`) for consistent depth across the scene.

Also apply Grove terminology through GroveTerm components — never hardcode Grove-specific words in user-facing text.

**Reference:** Load `references/color-palette.md` for all color tokens with hex values, seasonal palettes (Spring/Summer/Autumn/Winter/Midnight), accent palettes, helper functions, and background gradient patterns.

**Reference:** Load `references/groveterm-system.md` for the GroveTerm component suite, the `[[term|standard]]` syntax, common term vocabulary, and accessibility rules.

**Output:** Color scheme applied with proper imports and seasonal variants; user-facing text uses GroveTerm components

---

### Phase 4: TEXTURE

_The chameleon adds depth—rough bark, smooth leaves, shifting light..._

Layer nature components for atmosphere. Generate the randomized forest (trees never overlap — 8% minimum gap). Add weather effects appropriate to the season. Place seasonal birds for life. Wire up Lucide icons (never emojis). Respect the responsive density table.

**Reference:** Load `references/nature-components.md` for the full component catalog, randomized forest generation algorithm, weather effect snippets, seasonal bird placement, icon registry pattern, and mobile particle count adjustments.

**Output:** Nature components layered with proper z-index and responsive density

---

### Phase 5: ADAPT

_The chameleon becomes one with its surroundings—complete adaptation..._

Final polish and accessibility. Reduce particle counts for mobile. Add the mobile overflow sheet menu for navigation. Verify `prefers-reduced-motion` wraps all particle layers. Confirm all touch targets are 44x44px minimum. Check dark mode glass variants. Run CI.

**Verification (mandatory):**

```bash
pnpm install
gw ci --affected --fail-fast --diagnose
```

If CI fails: read diagnostics, fix, re-run. The chameleon does not leave broken code behind its color shift.

**Final Checklist (after CI passes):**

- [ ] CI: `gw ci --affected` passes clean
- [ ] Glass effects used for text readability over busy backgrounds?
- [ ] Lucide icons, no emojis?
- [ ] Mobile overflow menu for navigation items?
- [ ] Decorative elements respect `prefers-reduced-motion`?
- [ ] Touch targets at least 44x44px?
- [ ] Seasonal colors match the page's emotional tone?
- [ ] Trees randomized with proper spacing (8% minimum gap)?
- [ ] Dark mode supported with appropriate glass variants?
- [ ] User-facing text follows Grove voice?
- [ ] Grove terminology uses GroveTerm components (not hardcoded)?
- [ ] `[[term]]` syntax used in data-driven content strings?

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

| Pattern                | Good For                                          |
| ---------------------- | ------------------------------------------------- |
| **Glassmorphism**      | Text over backgrounds, navbars, cards, modals     |
| **Randomized forests** | Story pages, about pages, visual sections         |
| **Seasonal themes**    | Roadmaps, timelines, emotional storytelling       |
| **Midnight Bloom**     | Future features, dreams, mystical content         |
| **Weather particles**  | Hero sections, transitions between seasons        |
| **Birds**              | Adding life to forest scenes, seasonal indicators |

## When NOT to Use

| Pattern                   | Avoid When                                         |
| ------------------------- | -------------------------------------------------- |
| **Heavy decoration**      | Data-dense pages, admin interfaces, forms          |
| **Particle effects**      | Performance-critical pages, accessibility concerns |
| **Seasonal colors**       | Brand-critical contexts needing consistent colors  |
| **Multiple glass layers** | Can cause blur performance issues                  |
| **Randomization**         | Content that needs to match between sessions       |
| **Complex forests**       | Mobile-first pages, simple informational content   |

---

## Example Adaptation

**User:** "Make this about page feel like Grove"

**Chameleon flow:**

1. **READ** — "Page is about the team's journey. Emotional tone: reflection. Season: Autumn (harvest). Decoration level: full."

2. **SKETCH** — "Load `references/layout-patterns.md`. Create glass card containers, sticky nav with `glass-surface`, layering formula in place."

3. **COLOR** — "Load `references/color-palette.md`. Import autumn palette (rust, ember, amber, gold), warm gradients, `autumnReds` for accent. Load `references/groveterm-system.md` for user-facing text."

4. **TEXTURE** — "Load `references/nature-components.md` and `references/glass-components.md`. Add randomized aspen/birch trees, `FallingLeavesLayer`, autumn birds (cardinals), Lucide icons."

5. **ADAPT** — "Responsive density, reduced-motion support, `GroveTerm` for 'Welcome, Wanderer' greeting, 44px touch targets, dark mode verified. Run `gw ci --affected`."

---

## Quick Decision Guide

| Situation             | Action                                                     |
| --------------------- | ---------------------------------------------------------- |
| Story/narrative page  | Full seasonal atmosphere, weather effects                  |
| Data-dense interface  | Minimal decoration, focus on glass readability             |
| Landing/hero section  | Randomized forest, particles, seasonal birds               |
| Form/admin interface  | Clean glass surfaces, no nature distractions               |
| Mobile-first page     | Reduce tree count, simpler effects                         |
| Accessibility concern | Respect prefers-reduced-motion, keep glass for readability |

---

## Integration with Other Skills

- **`/gathering-ui`** — Pairs chameleon with deer-sense for accessible UI in one pass
- **`/deer-sense`** — Accessibility audit after adaptation
- **`/grove-ui-design`** — Broader UI design patterns and component selection
- **`/beaver-build`** — Write tests covering interactive UI after adaptation

---

_The forest welcomes those who adapt with intention._
