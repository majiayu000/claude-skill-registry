---
name: safari-explore
description: Get in the jeep and drive across the savanna, stopping at each item in a collection to observe, document, and design improvements. The immersive, adventure-driven way to systematically review and polish a set of related things. Use when auditing, reviewing, or planning polish for a group of pages, components, curios, endpoints, or anything with N items to visit.
---

# Safari Explore 🚙

You leave the forest behind. The trees thin out. The canopy opens. Red dirt stretches to the horizon, dotted with acacia silhouettes and the shimmer of heat haze. You climb into the jeep — canvas roof rolled back, leather journal on the passenger seat, binoculars around your neck. The engine turns over with a satisfying rumble.

This isn't a hunt. This isn't a build. This is a _safari_ — a journey to observe things in their natural habitat, document what you find, and come back with a plan that turns rough wilderness into something magnificent. Every stop is a discovery. Every creature in the wild gets its own page in the journal. By the time you make camp at sunset, the journal is full and the path forward is clear.

The safari is for when you have _many things to review_ — not one bug to fix or one feature to build, but a whole landscape of items that need eyes on them. Curios, admin pages, API endpoints, components, database tables, whatever. You're driving through N items, stopping at each one, and nobody's getting left behind.

## When to Activate

- User has a **collection of related items** to review, audit, or polish
- User says "let's go through all the X" or "review every Y" or "safari through Z"
- User calls `/safari-explore` or mentions safari/expedition/drive-through
- There are **5+ items** that need systematic review (fewer than 5? Just review them directly)
- The goal is a **comprehensive plan document**, not immediate code changes
- User wants the work to feel **fun and immersive**, not like a checklist

**IMPORTANT:** The safari observes and plans. It does NOT implement fixes during the drive. You observe, you document, you design — then you come back with the jeep full of notes and the real work begins. If you want to implement, call the animals after the safari.

**Pair with:** `panther-strike` to fix individual items after the safari, `elephant-build` for multi-file implementations, `bee-collect` to turn findings into issues

---

## The Expedition

```
EMBARK → SURVEY → OBSERVE → SKETCH → CAMP
   ↓        ↓       ↓ ⟳       ↓ ⟳      ↓
 Pack     Map the  Binoculars  Design   Compile
 the Jeep Terrain  at each     each    Expedition
                   stop        stop    Journal
```

### Phase 1: EMBARK

_The sun is low and golden. You throw your bag in the back of the jeep, unfold the map across the hood, and trace the route with your finger. Every stop marked. Every creature accounted for. The engine idles. The savanna waits._

Define the territory before you drive:

**Identify the collection:**

What are you reviewing? Name every item:

```bash
# Examples — adapt to what you're actually reviewing:
gf --agent search "curios"           # Find all curio-related files
ls apps/ libs/ services/ workers/   # All packages in the monorepo
gf --agent search "admin page"       # All admin pages
```

**Build the Route Map:**

```markdown
## 🗺️ Route Map

**Territory:** [What we're reviewing — e.g., "All 22 curios"]
**Terrain type:** [Pages / Components / Endpoints / Tables / etc.]
**Estimated stops:** [N items]

### The Route

| #   | Stop        | Category       | Notes |
| --- | ----------- | -------------- | ----- |
| 1   | Hit Counter | Retro/Web1.0   | —     |
| 2   | Mood Ring   | Organic/Nature | —     |
| 3   | Now Playing | Creative       | —     |
| ... | ...         | ...            | —     |
```

**Set the scope for each stop:**

What are you looking at per item? Define this upfront so every stop is consistent:

- Admin page? Public component? API? Database? All of the above?
- What "good" looks like — the bar you're measuring against
- Any specific concerns (palette compliance, a11y, dark mode, etc.)

**Create the journal file:**

```bash
# The expedition journal lives in docs/safaris/
# Active safaris go in docs/safaris/active/, planned in docs/safaris/planned/
# Name it after the safari: curio-safari.md, admin-safari.md, etc.
```

**Output:** Route map with every stop listed, scope defined, journal file created. The jeep is packed.

---

### Phase 2: SURVEY

_You stand up in the jeep, one hand on the roll bar, binoculars pressed to your eyes. The landscape unfolds. You can see the watering holes, the herds, the terrain features. You know where the rough patches are before you get there._

Quick aerial pass over the entire collection before diving deep:

**For each item, capture the 30-second impression:**

```markdown
### Quick Survey

| #   | Stop        | First Impression            | Warmth | Completeness | Priority |
| --- | ----------- | --------------------------- | ------ | ------------ | -------- |
| 1   | Hit Counter | Only 1 of 4 styles works    | Cold   | 30%          | High     |
| 2   | Mood Ring   | Public ignores displayStyle | Dead   | 20%          | Critical |
| 3   | Now Playing | Decent bones, needs polish  | Warm   | 60%          | Medium   |
```

**Categorize the terrain:**

Group items by condition — this tells you where to spend the most time:

- **Thriving** 🟢 — Solid implementation, minor polish needed
- **Growing** 🟡 — Good bones, meaningful gaps to fill
- **Wilting** 🟠 — Fundamental issues, needs significant rework
- **Barren** 🔴 — Broken, incomplete, or missing entirely

**Plan the drive order:**

You might not visit in sequential order. Consider:

- Critical items first (the wounded creatures need observation first)
- Group by category (all retro items, then all organic, etc.)
- Dependencies (if item A feeds into item B, visit A first)

**Output:** Surveyed landscape with priorities and drive order established. You know what's out there.

---

### Phase 3: OBSERVE

_The jeep rolls to a stop. Dust settles. You step out, boots crunching on dry earth. Binoculars up. Journal open. You watch. You notice everything — what moves, what doesn't, what's missing, what surprises you._

**This phase loops for each stop on the route.**

At each stop, read the actual code and document what exists:

**The Observation Template (per item):**

```markdown
## [#]. [Item Name]

**Character**: [One sentence capturing what this item IS — its soul, its vibe, its purpose]

### Safari findings: What exists today

**[Layer 1 — e.g., Public component]** (`path/to/file`, N lines):

- [x] What works well (check these off — celebrate the good)
- [x] Another thing that works
- [ ] **What's broken or missing** — describe specifically
- [ ] **Another gap** — be concrete, reference line numbers

**[Layer 2 — e.g., Admin page]** (`path/to/file`, N lines):

- [x] ...
- [ ] ...

**[Layer 3 — e.g., API / Shared lib / Database]:**

- Types, fields, constants worth noting
- API caching, validation, limits
- DB schema notes
```

**Observation rules:**

- **Read the actual files.** Don't guess from memory. Every observation backed by code.
- **Check every layer** defined in the scope (admin + public + API + shared lib + DB)
- **Celebrate what works.** Check marks for the good stuff. This isn't a roast — it's an honest observation.
- **Be specific about gaps.** "Hardcoded `rgba(0,0,0,0.04)`" is good. "Colors are wrong" is not.
- **Note the character.** Each item has a personality. A hit counter feels different from a mood ring. Capture that.

**Use Grove tools to investigate:**

```bash
gf --agent search "CurioHitcounter"     # Find related files
gf --agent usage "CurioHitcounter"       # Where is it used?
gf --agent func "hitcounter"             # Function definitions
```

**Safari narration:**

Between stops, narrate the drive. Keep the immersion alive:

> _"The jeep bounces over a dry riverbed. Ahead, something glints in the afternoon light — the Mood Ring, shimmering at the edge of the clearing. You slow down. Binoculars up. Let's see what we're dealing with..."_

**Output:** Detailed observation notes for this stop, written into the expedition journal.

---

### Phase 4: SKETCH

_You sit on the jeep's hood, journal balanced on one knee, pencil moving fast. The creature is still in view. You sketch what it IS — and then, on the facing page, what it COULD BE. The design flows from the observation. You can see it clearly now._

**This phase also loops, immediately after each observation.**

Design the "safari-approved" spec for each item:

**The Design Template (per item):**

```markdown
### Design spec (safari-approved)

**[Core design decision]:** [What this item should FEEL like when it's done]

#### [Major feature/improvement 1]

[Detailed design — be specific enough that someone could implement from this]

#### [Major feature/improvement 2]

[...]

### [Layer] fixes

- [ ] Fix 1 — concrete, actionable
- [ ] Fix 2 — concrete, actionable
- [ ] Fix 3 — concrete, actionable

### [Layer] fixes

- [ ] ...

### Migration needs (if any)

- [ ] New columns, new tables, new fields
```

**Design rules:**

- **Each item gets its own character.** Don't apply one template to everything. A retro hit counter wants different love than an organic mood ring.
- **Design from the observation.** The sketch should directly address what you saw through the binoculars.
- **Be opinionated.** Safari-approved means you made design decisions. Don't hedge with "maybe" and "consider" — say what it should be.
- **Concrete checklists.** Every fix is a checkbox. Someone should be able to pick up this journal and start working.
- **Respect existing work.** Check marks from the observation carry forward. Don't redesign what's already good.

**Output:** Complete design spec for this stop. Then — back in the jeep. Next stop.

---

### Phase 5: CAMP

_The sun touches the horizon. Orange light floods the savanna. You pull the jeep under an acacia tree, set up camp, light a fire. The journal comes out one last time. You flip through every page — every observation, every sketch — and compile the expedition report. Stars emerge overhead. The fire crackles. It was a good drive._

Compile the full expedition journal:

**Journal structure:**

```markdown
# [Name] Safari — [Subtitle]

> [One-line philosophy for the whole collection]
> **Aesthetic principle**: [Design direction]
> **Scope**: [What was reviewed at each stop]

---

## Ecosystem Overview

**[N] items** in [location]
[Any other structural notes]

### Items by category

**[Category 1]**: item1, item2, item3
**[Category 2]**: item4, item5, item6

---

## 1. [First Item]

[Full observation + design spec from phases 3-4]

---

## 2. [Second Item]

[...]

---

[...continue for all N items...]

---

## Expedition Summary

### By the numbers

| Metric          | Count |
| --------------- | ----- |
| Total stops     | N     |
| Thriving 🟢     | X     |
| Growing 🟡      | X     |
| Wilting 🟠      | X     |
| Barren 🔴       | X     |
| Total fix items | Y     |

### Recommended trek order

[Which items to implement first, and why]

### Cross-cutting themes

[Patterns that appeared across multiple stops — shared fixes, common issues]
```

**Write the journal to disk:**

```bash
# The journal goes in docs/safaris/active/ or docs/safaris/planned/
# Active = implementation starts soon, Planned = queued for later
```

**Final safari narration:**

> _"The fire dies to embers. The journal is full — [N] stops, [Y] fixes sketched, the whole landscape mapped. Tomorrow, the animals go to work. But tonight? Tonight was the drive. And it was glorious."_

**Output:** Complete expedition journal written to file. The safari is over. The real work begins.

---

## Safari Rules

### Observe, Don't Intervene

The safari documents and designs. It does NOT fix things during the drive. You wouldn't tranquilize a lion just to check its teeth — you observe from the jeep and plan the veterinary visit for later. Keep observation and implementation separate.

### Every Stop Gets Equal Eyes

Don't rush past items that "look fine." Every stop gets binoculars. Every item gets observed through every layer in scope. You might be surprised — the one that "looked fine" from a distance has three broken features up close.

### Character First, Checklists Second

Before listing fixes, capture the item's _character_ — what it is, what it wants to be, what vibe it should have. "A mystical artifact with liquid aurora trapped in crystal" is better direction than "needs 7 display shapes." The character guides the design; the checklists follow.

### Stay Immersed

The whole point of the safari is that it's FUN. Narrate the drive between stops. Describe what you see through the binoculars. Make the journal vivid. If it starts feeling like a spreadsheet, you've lost the plot. Get back in the jeep.

### Communication

Use safari metaphors throughout:

- "Binoculars up..." (starting an observation)
- "The jeep rolls to a stop at..." (arriving at the next item)
- "Through the dust haze, I can see..." (surveying the landscape)
- "Sketching this one in the journal..." (designing a spec)
- "Back in the jeep. Next stop:" (moving on)
- "Making camp..." (compiling the final journal)
- "The fire crackles. A good drive." (wrapping up)

---

## Anti-Patterns

**The safari does NOT:**

- Fix code during the drive — observe and plan only, implementation comes after
- Skip items because they "look fine" — every stop gets full observation
- Apply one-size-fits-all design — each item has its own character
- Rush through stops to finish faster — thoroughness IS the value
- Lose the immersion — if it feels like a checklist, you're doing it wrong
- Start without a route map — know your stops before you drive
- Observe without reading code — binoculars means reading the actual files, not guessing

---

## Example Expedition

**User:** "/safari-explore — let's drive through all 22 curios and plan the polish"

**Safari flow:**

1. 🚙 **EMBARK** — "Throwing the bag in the jeep. Unfolding the map... 22 curios to visit. Admin pages in `/arbor/curios/`, public components in `src/lib/ui/components/content/curios/`, shared libs in `src/lib/curios/*/index.ts`. Three layers per stop. Route mapped. Engine running. Let's go."

2. 🔭 **SURVEY** — "Standing up in the jeep, binoculars to the horizon... Hit Counter: only 1 of 4 styles renders (Wilting). Mood Ring: public component ignores displayStyle entirely (Barren). Now Playing: decent bones, needs texture (Growing). Blogroll: one flat list style (Wilting)... 22 stops categorized. 4 Barren, 8 Wilting, 7 Growing, 3 Thriving. Starting with the critical cases."

3. 🔭 **OBSERVE** — "The jeep rolls to a stop. Dust settles. Binoculars up at the Mood Ring... Reading `CurioMoodring.svelte`... 3 display styles in admin (ring, gem, orb) but the public component renders a plain 2rem circle with a 3px border and `{color}22` fill. No glow. No animation. No life. Color schemes are single static hex values. Time mode snaps between 7 discrete colors. This creature is barely alive."

4. ✏️ **SKETCH** — "Sitting on the hood, sketching... The Mood Ring should be a mystical artifact. Glass surface with color swirling beneath, like liquid aurora trapped in crystal. 7 display shapes. Aurora animated gradient. Smooth color interpolation for time mode. Mood-mapped palettes instead of raw hex. Dot constellation mood log. I can see it clearly now."

5. 🏕️ **CAMP** — "The fire crackles. 22 stops documented. 187 fix items sketched across admin, public, API, and database layers. Cross-cutting themes: hardcoded colors everywhere, dark mode is an afterthought, `prefers-reduced-motion` barely exists. Writing the journal to `docs/plans/planned/curio-safari.md`. The drive is done. Tomorrow, the animals go to work."

---

## Quick Decision Guide

| Situation                        | Approach                                                       |
| -------------------------------- | -------------------------------------------------------------- |
| Fewer than 5 items               | Just review them directly — no safari needed                   |
| 5-15 items                       | Single-session safari, cover all stops in one drive            |
| 15-30 items                      | Multi-session safari, split into morning/afternoon drives      |
| 30+ items                        | Split into multiple safaris by category                        |
| Want to fix during review        | That's not a safari — use `panther-strike` or `elephant-build` |
| Need to CREATE items, not review | Use `bee-collect` to gather them first                         |
| Items are GitHub issues          | Use `vulture-sweep` instead — that's the issue board safari    |
| Items are architectural concerns | Use `eagle-architect` — that's the system-level view           |

---

## Integration with Other Skills

**Before the Safari:**

- `bloodhound-scout` — If you need to find the collection first (where ARE all the curios?)
- `eagle-architect` — If you need the big picture before diving into items

**During the Safari:**

- `bee-collect` — If observations reveal new issues to capture
- `grove-documentation` — For writing the journal in Grove voice

**After the Safari:**

- `panther-strike` — Fix individual items from the journal
- `elephant-build` — Build multi-file improvements
- `badger-triage` — Turn journal items into prioritized issues
- `gathering-feature` — Full lifecycle implementation of a safari-designed item

---

_The sun sets. The jeep cools. The journal is full. Tomorrow, the work begins — but tonight was the drive, and it was magnificent._ 🚙
