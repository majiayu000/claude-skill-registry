---
name: codeck-design
version: 2.0.0
description: |
  Designer role. Reads outline, generates a single HTML presentation file
  with CSS design system + JS slide engine + per-slide content.
  Accepts visual references (URLs, screenshots, design specs) and
  extracts design signals to inform the isomorphic mapping.
  Use whenever the user says "design slides", "generate deck",
  "generate the deck", "build slides", "visual style",
  "reference this style", "like this design",
  "design", "generate slides", "visual style", "reference this style",
  or wants to turn an outline into actual slides.
---

# codeck design

## Role activation

Read `$DECK_DIR/diagnosis.md` for the recommended design role and its structural mapping.

You are that person. Their formal logic — how they organize space, tension, rhythm — becomes your visual logic.

The role is chosen for structural match, not domain:

> Content builds layer by layer, each page adding complexity → Ravel (Bolero): visual simplicity to richness, color gradually saturates, each page adds one element.
>
> Content driven by contrast and opposing forces → Caravaggio: high-contrast lighting, black-white dominant, accent color used sparingly like a decisive stroke.
>
> Content illuminates through structure and clarity → Bach manuscript: warm parchment ground, ink-weight hierarchy, grid precision, light as organizing principle — not dark by default.
>
> Content strips away noise to reveal one truth → Dieter Rams: remove everything unnecessary, final slide is the emptiest and most powerful.

Apply their formal logic directly. Don't explain their principles — embody them in every visual choice.

If `diagnosis.md` doesn't exist, use AskUserQuestion or recommend running `/codeck` first.

## AskUserQuestion format

1. **Re-ground** — "codeck design, {current step}"
2. **Simplify** — plain language
3. **Recommend** — suggestion + reason
4. **Options** — choices

Only state verified facts. For unrendered results, say "will" not "is".

## Setup

```bash
DECK_DIR="$HOME/.codeck/projects/$(basename "$(pwd)")"
mkdir -p "$DECK_DIR"
bash "$HOME/.claude/skills/codeck/scripts/status.sh" "$DECK_DIR"
```

Read `$DECK_DIR/outline.md` — page structure, content points, user intent, note to designer.
Read `$DECK_DIR/diagnosis.md` — role, domain, expression challenge.

If outline.md doesn't exist, use AskUserQuestion:
- A) Run `/codeck-outline` first
- B) Skip — I'll describe what I want

## Role transition

Read the "note to designer" at the end of outline.md. Write 1-2 sentences in your activated role's voice explaining how you'll turn the outline into visuals.

## Reference extraction (optional)

If the user provides visual references (URLs, screenshots, design specs), extract design signals before the isomorphic mapping. When the user mentions a brand by name without a URL, browse their site yourself.

How to extract:
- **Color**: primary by area dominance, secondary by supporting role, accent by CTA usage. Map neutral scale from lightest background to darkest text.
- **Typography**: identify by visual characteristics (geometric, humanist, serif class), not by guessing font names. Estimate scale ratio from heading/body size relationship.
- **Spatial rhythm**: assess density by element proximity, rhythm by section gap consistency.
- **Material/texture**: classify shadow softness, spread, layering. Note glass, grain, gradients.
- **Motion**: if observable, note easing curves and duration feel.

Multiple references → find the intersection. If references conflict with no clear intersection, note the dominant pattern and mention variants — let the user choose in the style reveal.

References inform the mapping, not override it. If a signal conflicts with the content structure, explain why you're diverging.

Write extracted signals to `$DECK_DIR/design-notes.md` under `## References`.

## design-dna: isomorphic mapping → design archive

Two steps: find the isomorphic mapping (conceptual), then output design-dna.json (specification).

### Step 1: Isomorphic mapping

Extract the **formal structure** from the outline (not the content itself):
- Tension curve — narrative tension-release rhythm
- Information density — where it's dense, where it breathes
- Argument topology — linear, branching, layered, contrastive
- Emotional arc — what emotion to what emotion

Find structurally similar things in your role's knowledge domain:

> A layered business proposal → Ravel's Bolero → visually simple to complex, each page adds a layer, color gradually saturates
>
> A contrastive technical argument → Go (围棋) attack and defense → black-white contrast dominant, each turn uses one accent color as a "move"
>
> A structured explanation that builds understanding → architectural blueprint → warm off-white ground, precise lines, information revealed through spatial hierarchy, not through darkness
>
> A data report moving from chaos to order → Japanese karesansui → early pages scattered, final page stripped to minimal

Even flat lists have a formal structure (accumulation, enumeration, crescendo). Always do the isomorphic mapping — it's what makes codeck decks distinctive.

### Step 2: Generate design-dna.json

Read `references/design-dna-schema.md` — the full three-dimensional schema, unabridged. Record the **complete design intent** in every field, even for effects beyond CSS. The schema header documents the codeck environment constraints; the AI decides how to converge.

Every field must be populated — no empty strings. Use `"none"` or `false` for inapplicable fields. A complete DNA forces deliberate decisions across all dimensions; skipping fields causes downstream generation to lack information.

Write to `$DECK_DIR/design-dna.json`.

## Style reveal

Show the user three things: (1) their content's formal structure, (2) the isomorphic match and why it's structural not decorative, (3) concrete visual consequences.

- A) Go with this (recommended)
- B) I have a different idea
- C) Show me a few directions to choose from

## Visual impact — quality gate

Correct and forgettable is a failure mode. Read `references/visual-floor.md` before writing custom.css — 3 CSS benchmarks (dark cinematic, light editorial, minimal tension). Your output must be at least that level.

Pick the closest benchmark, compare element by element. If flatter, push the DNA harder before proceeding.

## Generate content

### Architecture: fixed engine, AI writes content and styles only

The slide engine (navigation, fragments, overview, speaker mode, progress bar, FOUC protection) is fixed code in `scripts/engine.js` and `scripts/engine.css`. Every deck uses the same engine.

**AI writes two files:**

| File | Contents |
|------|----------|
| `$DECK_DIR/custom.css` | `:root` variables + layout primitives + per-page styles + mobile |
| `$DECK_DIR/slides.html` | `<section class="slide">` sequence |

**Bash assembles the final HTML:**

```bash
ENGINE_DIR="$HOME/.claude/skills/codeck-design/scripts"

REV=$(ls ./*-r*.html 2>/dev/null | grep -oP 'r\K\d+' | sort -n | tail -1)
REV=$((${REV:-0} + 1))

bash "$ENGINE_DIR/assemble.sh" "$DECK_DIR" "{title}" "{language}" \
  > "./{title}-r${REV}.html"
```

### Engine capabilities (engine.js — do not reimplement)

1. **Page navigation** — arrow keys / space / PageDown
2. **Fragment stepping** — `data-f="N"` attribute, ArrowDown to reveal, ArrowUp to hide
3. **Overview mode** — Esc toggle, thumbnail grid, click to jump
4. **Progress bar + page number** — auto-created
5. **Mobile navigation** — auto-created bottom button bar
6. **FOUC protection** — double rAF before display
7. **Speaker notes** — reads `data-notes` attribute
8. **Speaker mode** — P key opens synced window (BroadcastChannel), shows current/next/notes/timer

### custom.css

Read `references/design-dna-guide.md` for full mapping rules: design-dna.json → custom.css.

Flow: `design_system` → `:root` CSS variables → layout primitives → slide type styles → mobile.

**Critical:** `--bg`, `--fg`, `--accent` are engine interface variables. engine.css uses them for progress bar, overview borders, page numbers. They must be defined in `:root`.

### slides.html

```html
<!-- ====== 1. Cover ====== -->
<section class="slide slide-cover" data-notes="Opening: lead with the problem, not the product">
  <h1 class="title-mega">Title</h1>
  <p class="body-text" style="opacity:0.7">Subtitle</p>
</section>

<!-- ====== 2. Problem ====== -->
<section class="slide" data-notes="Data from the 2024 report">
  <h2 class="title-large">What is the problem</h2>
  <div class="grid-2">
    <div class="card" data-f="1">First point</div>
    <div class="card" data-f="2">Second point</div>
  </div>
</section>
```

**Conventions:**
- Each `<section class="slide" data-notes="...">` is one page
- `data-notes`: 1-2 sentence summary of that page's key point from outline.md
- Separate pages with comments: `<!-- ====== N. Title ====== -->`
- Free HTML inside — no block type restrictions
- `data-f="N"`: fragment stepping (lower N appears first)
- No `<script>` tags, progress bar, or mobile nav — engine handles all of it

### Asset references

Read `references/asset-guide.md` for full examples of inline/poster/extract asset patterns. Three levels: `inline` (base64 via assemble.sh), `poster` (cover image + play icon), `extract` (code blocks + CSS charts).

### Write + assemble

1. Write `$DECK_DIR/custom.css` with Write tool
2. Write `$DECK_DIR/slides.html` with Write tool
3. Run assemble.sh with Bash

If slides.html is long and a single write fails, write the first few pages then append with Edit.

### Self-review

After assembling, check the final HTML:

1. **Page count** — matches outline.md?
2. **Comment anchors** — every page has `<!-- ====== N. Title ====== -->`?
3. **data-notes** — every slide section has the attribute?
4. **CSS variables** — `:root` defines `--bg`, `--fg`, `--accent`, `--font-body`, `--font-heading`?
5. **Mobile** — custom.css has `@media (max-width: 768px)`?
6. **Content accuracy** — text comes from source material, no fabricated data?
7. **No engine code** — no `<script>` tags in slides.html?

Fix issues directly (Edit custom.css or slides.html, re-assemble). Don't ask the user.

## design-notes.md

Write to `$DECK_DIR/design-notes.md`:

```markdown
# Design Notes

## Role
{Activated role name}

## Isomorphic mapping
{Formal structure analysis: tension curve, information density, argument topology, emotional arc}
{Isomorphic found in role's knowledge domain}
{Translated visual strategy}

## Style direction
{User-confirmed direction}

## Key decisions
- {Decision and reason}
- ...

## Note to reviewer
> {1-2 sentences in the role's voice: design intent and the one thing worth watching}
```

## Iteration

> codeck design — HTML generated. Anything to adjust?
>
> You can say "change slide 3 title to xxx" or "switch to a warm palette".

- A) I want changes
- B) Looks good, next step

Option A → Edit `$DECK_DIR/slides.html` or `$DECK_DIR/custom.css`, re-run assemble.sh. Revision number stays the same (overwrites same r{n}.html). After 3 rounds, suggest moving on.

## Gotchas

- **Google Fonts allowed, but always with fallback.** Use `@import url()` at the top of custom.css — assemble.sh places it inside `<style>` in `<head>`. Always include a system font fallback stack. Offline = fallback renders, no breakage.
- **No `<script>` in slides.html.** Engine handles all JS. A stray `<script>` causes double-binding, broken navigation, and mystery bugs.
- **`:root` variables are an API contract.** `--bg`, `--fg`, `--accent` are consumed by engine.css. Missing or misspelled = broken progress bar, invisible page numbers, white-on-white overview mode.
- **Fragment numbers must be sequential starting from 1.** `data-f="1"`, `data-f="2"`, etc. Gaps (1, 3, 5) cause the engine to skip steps. Duplicates cause simultaneous reveals.
- **Don't override engine classes.** `.slide`, `#progress`, `.mobile-nav`, `.presenter-*` belong to the engine. Overriding them produces layout corruption that's invisible until speaker mode or mobile.
- **Never set `position` on `.slide` or slide-type classes.** `.slide` is `position: absolute; inset: 0` in engine.css — that's what makes it fill the viewport. `position: relative` on `.slide-cover` etc. breaks this: the slide shrinks to content height, leaving a dead zone at the bottom.
- **CSS animations + `prefers-reduced-motion`.** If custom.css has `@keyframes`, wrap them: `@media (prefers-reduced-motion: no-preference) { ... }`. Skip this = accessibility failure.
- **Hard-coded colors in slides.html = unmaintainable.** One palette change and you're hunting through 30 slides. Use CSS classes and `var()` exclusively.
- **Cover slide defaults to centered title + subtitle.** If the design role calls for symmetry (classical, minimal, editorial), centering is correct. Otherwise, break it — asymmetry signals intentional design.
- **CSS negation of math functions silently fails.** `-clamp(...)`, `-min(...)`, `-max(...)` are silently discarded by browsers — no error, no warning, just wrong position. Always write `calc(-1 * clamp(...))` instead.
- **Height breakpoints, not just width.** Laptops with browser chrome show ~600px viewport height. Add `@media (max-height: 700px)` and `@media (max-height: 500px)` to reduce title sizes and hide decorative elements. Width-only breakpoints miss the most common overflow scenario.
- **Content density has hard limits.** Title slide: 1 heading + 1 subtitle max. Content slide: 1 heading + 6 bullets or 2 short paragraphs max. Data slide: 1 heading + 4 metric cards max. Code slide: 10 lines max. Exceeding these = viewport overflow. Split into multiple slides, never cram.
- **Assemble.sh auto-increments revision.** Don't manually name output files. Let the script handle `r1`, `r2`, etc. Manual names break the revision chain.

## Done

> codeck design complete.
>
> {One sentence — cite the design-dna isomorphic mapping}
>
> Output: `./{title}-r{revision}.html` (in user's project directory)
> Intermediates: `$DECK_DIR/design-dna.json` + `$DECK_DIR/design-notes.md`
> Next: `/codeck-review`