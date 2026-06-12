---
name: distinctive-frontend-design
description: "Context-driven aesthetic exploration with anti-cliche validation."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
routing:
  triggers:
    - "frontend design"
    - "typography exploration"
    - "anti-cliche design"
    - "visual identity"
    - "design language"
  category: frontend
  pairs_with:
    - threejs-builder
    - webgl-card-effects
    - frontend-slides
---

# Distinctive Frontend Design Skill

Systematic aesthetic exploration that produces contextual, validated design specifications. Every design choice flows from project context -- purpose, audience, emotion -- not from defaults or convenience. The workflow enforces exploration before implementation: you cannot write CSS until you have a validated aesthetic direction, typography selection, color palette, animation strategy, and atmospheric background.

Optional capabilities (off unless explicitly enabled by the user): design system generation, full WCAG accessibility auditing, animation performance profiling, dark mode variant generation.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| adding motion: page load orchestration, state transitions, scroll reveals, easing | `animation-patterns.md` | Loads detailed guidance from `animation-patterns.md`. |
| applying layout rules after Phase 1 surface-type classification (app vs landing) | `app-vs-landing-rules.md` | Loads detailed guidance from `app-vs-landing-rules.md`. |
| building backgrounds: gradients, noise, geometric patterns, atmosphere | `background-techniques.md` | Loads detailed guidance from `background-techniques.md`. |
| auditing CSS for banned fonts, hardcoded colors, over-animation | `css-audit-patterns.md` | Loads detailed guidance from `css-audit-patterns.md`. |
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |
| brief-level walkthroughs: new landing page, app surface | `examples.md` | Loads detailed guidance from `examples.md`. |
| game UI, AAA game, polished game, Steam game, roguelike UI, Slay the Spire | `game-ui-polish.md` | Loads game-native polish rules that prevent website-like surfaces, excessive gradients, nested boxes, and fake-premium chrome. |
| starter code: design tokens, base styles, React/Tailwind and HTML templates | `implementation-examples.md` | Loads detailed guidance from `implementation-examples.md`. |
| performance work | `performance-budgets.md` | Loads detailed guidance from `performance-budgets.md`. |
| aesthetic direction examples and expanded phase steps | `phase-details.md` | Loads detailed guidance from `phase-details.md`. |
| picking a page structure in Phase 1 | `macrostructure-catalog.md` | Load only the single chosen `macro:*` entry by its heading anchor (e.g. `#macrostat-led`), never the whole file — one entry carries every rule the build needs. |
| before Phase 1: definitions of Hero, Full-bleed, Surface type, and other gating terms | `vocabulary.md` | Loads detailed guidance from `vocabulary.md`. |

## Instructions

### Vocabulary

See `references/vocabulary.md` for term definitions (Hero, Full-bleed, Narrative brief, Surface type, Linear-style restraint, Decorative-only motion, Brand override). Read these once before Phase 1 so the rules do not feel like jargon when they gate your work.

### Phase 1: Context Discovery

**Goal**: Understand the project deeply before making any aesthetic decisions.

**Step 1: Read and follow the repository CLAUDE.md**, then gather context by asking (adapt based on what is already known):

1. **Purpose**: What is this frontend for? (portfolio, SaaS product, creative showcase, documentation, landing page)
2. **Surface type**: Landing page or app/dashboard? Design rules diverge sharply. Landing pages lean on a full-bleed hero and narrative sequence. Apps and dashboards lean on Linear-style calm surfaces, strong typography, few colors, and dense readable information. Classify this up front because every downstream decision depends on it.
3. **Audience**: Who will use it? (developers, artists, enterprise users, general public, specific demographics)
4. **Emotion**: What should users feel? (professional, playful, sophisticated, rebellious, calm, energetic)
5. **Cultural context**: Any geographic, cultural, or thematic associations? (Japanese minimalism, industrial, retro, academic)
6. **Constraints**: Accessibility requirements, performance budgets, existing brand elements to preserve?
7. **Tech stack**: React, Vue, vanilla HTML/CSS, Next.js, framework preferences?
8. **Real content**: Gather the actual copy, real product name, real imagery, real product context. Placeholder text produces placeholder thinking. If final content is not yet available, secure at minimum the hero headline, product name, and the single promise you want the first viewport to convey.
9. **Previous projects**: Any recent frontend work? Variety across projects is mandatory, so check for choices that would overlap with recent work and avoid them.

**Step 1b: Pick one macrostructure** before any aesthetic direction. Choose a single `macro:*` page-structure id from `references/macrostructure-catalog.md` based on the purpose and content from Step 1 (e.g. `macro:stat-led`, `macro:long-document`, `macro:split-hero`). Load only the one entry you pick, addressed by its heading anchor — not the whole catalog. Structure chosen before color and type keeps every page from collapsing into the same hero-then-cards template. Record the chosen id; it becomes the `macrostructure` field in the spec output and feeds the variety check in Phase 6.

**Step 2: Define 3-5 distinct aesthetic directions** using `references/color-inspirations.json` and `references/font-catalog.json` as starting points. Providing multiple directions prevents anchoring on a first instinct, which is the primary source of generic "AI slop" output. See `references/phase-details.md` for example directions (Neo-Brutalist Technical, Warm Artisan, Midnight Synthwave, Botanical Minimal, Arctic Technical).

**Step 3: Output** `aesthetic_direction.json` with chosen direction(s) and contextual justification. Every direction must link back to project purpose, audience, and emotion -- context-driven justification is what separates distinctive design from arbitrary choices. See `references/implementation-examples.md` for template.

**Step 4: Write the narrative brief**. Before any code or visual exploration, commit three sentences to the page: visual thesis, content plan, interaction thesis. See `references/phase-details.md` for the full definition with examples.

**Gate**: A single `macro:*` macrostructure id is chosen and recorded. Aesthetic direction is defined with contextual justification linking project purpose, audience, and emotion to the chosen direction. Narrative brief from Step 4 is written with visual thesis, content plan, and interaction thesis. Proceed only after all three gate items pass.

**Skip-if-answered**: If the user's original request already provides the surface type, the product name, and a clear promise for the hero, treat those answers as already gathered. Ask only for missing context. The context-gathering questions exist to close gaps, not to gate every request on ceremony.

### Phase 2: Typography Selection

**Goal**: Select distinctive, contextual font pairings that define the design's personality.

**Step 1: Load** `references/font-catalog.json`. All fonts in the catalog are pre-approved. Use alternatives to the following overused fonts, which are overused to the point of invisibility and signal generic output: Inter, Roboto, Arial, Helvetica, system fonts (e.g., `-apple-system, BlinkMacSystemFont, 'Segoe UI'`), Space Grotesk. Keep them out of selections and fallback stacks.

**Step 2: Select font pairing** following the selection process and criteria in `references/phase-details.md` (5-step process, two-typefaces-maximum rule, brand-first rule).

**Step 3: Validate** font selection against the banned list. See `references/phase-details.md` for the validation block and manual verification steps.

**Step 4: Document** typography specification with font families, weights, usage roles, and rationale for each selection. Be specific -- include exact font names and weights, not vague descriptions. See `references/implementation-examples.md` for template.

**Gate**: Font validation passes with no banned fonts, no recent reuse, and a confirmed aesthetic match. Proceed only after the gate passes.

### Phase 3: Color Palette

**Goal**: Create a contextual palette with clear dominance hierarchy, not a random collection of colors.

**Step 1: Research** cultural/contextual inspiration using `references/color-inspirations.json`. See `references/phase-details.md` for the full list of inspiration source categories. Select an inspiration source that resonates with the project context from Phase 1. The palette must trace back to that context -- convenience or personal preference is not a valid reason for a color choice.

**Step 2: Build palette** with strict dominance structure:
- **Dominant** (60-70%): Base background and major surfaces -- this sets the mood
- **Secondary** (20-30%): Supporting elements, containers, navigation -- provides structure
- **Accent** (5-10%): High-impact moments, CTAs, highlights -- demands attention sparingly
- **Functional**: Success, warning, error, info states -- consistent across all designs

Colors distributed evenly without a clear dominant create visual chaos. The 60/30/10 ratio is non-negotiable because without it, no coherent aesthetic emerges.

**One accent color, not two.** The accent slot is for a single hue. If a second accent seems necessary, it is almost always either (a) a functional color (error/success/warning/info, which belongs in the Functional group), or (b) a weight variation of the dominant or secondary. Two competing accents dilute the hierarchy and signal a page that does not know what it wants the user to look at.

**Step 3: Check the palette against the cliche list** in `references/preferred-patterns.json`. See `references/phase-details.md` for the explicit reference set (purple-on-white, generic blue, etc.).

**Step 4: Validate** palette against cliche detection. See `references/phase-details.md` for the validation block and manual verification steps.

**Gate**: Palette passes cliche detection and demonstrates a clear 60/30/10 dominance ratio. Proceed only after the gate passes.

### Phase 4: Animation Strategy

**Goal**: Design choreography for high-impact moments only. Restraint is a feature -- animating everything dilutes impact and signals lack of intentionality.

**The 2-to-3 rule**. Ship two or three intentional motions per page, not ten. Motion creates presence and hierarchy. Too much motion creates noise. The interaction thesis from Phase 1 should already name the three slots; this phase choreographs them in detail.

**Step 1: Fill the three motion slots** (entrance, scroll, interaction). See `references/phase-details.md` for slot definitions, the moments NOT worth animating, the decorative-only litmus, and recommended stack.

**Step 2: Design choreography** for each identified moment. Reference `references/animation-patterns.md` for battle-tested patterns and `references/phase-details.md` for the choreography catalog summary.

**Step 3: Define easing curves and timing** for the design. See `references/phase-details.md` for the easing-by-purpose table and duration-by-scope table.

**Gate**: At least one high-impact moment has a fully defined choreography including element order, easing curves, and timing values. Proceed only after this is defined.

### Phase 5: Hero Composition, Background & Atmosphere

**Goal**: Construct the first viewport as a single composition, then add depth and mood through layered effects. Flat solid-color backgrounds fail this phase because they produce no atmospheric depth -- every surface needs at least two layers.

**Step 0: Hero composition rules** (landing pages). The first viewport must read as one composition, not a grid of parts. See `references/phase-details.md` for the hard rules (one composition, no cards in hero, full-bleed by default, brand-first, one job per section, hero image litmus). Apps and dashboards follow different rules; see `references/app-vs-landing-rules.md`.

**Step 1: Choose technique** from `references/background-techniques.md` based on aesthetic direction. See `references/phase-details.md` for the technique-by-aesthetic mapping.

**Step 2: Implement** background CSS that matches the aesthetic direction. See `references/phase-details.md` for the minimum-layers requirement (base surface color, gradient layer, pattern/texture layer).

**Step 3: Verify** background does not compromise text readability. Check contrast ratios against WCAG AA minimums.

**Gate**: Background uses at least 2 layers creating visual depth and atmospheric mood. Solid single-color backgrounds fail this gate.

### App vs Landing Page Rules

See `references/app-vs-landing-rules.md` for the full rule sets, app litmus test, and landing litmus test. The surface type classified in Phase 1 determines which rule set governs layout. Mixing the two rule sets is the fastest way to produce a page that feels generic in one direction and cluttered in the other.

### Phase 6: Validation & Scoring

**Goal**: Objective quality assessment before any finalization. Validation must run before delivering specifications -- skipping it means flaws compound through every downstream implementation decision.

**Step 1: Run comprehensive validation**

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_design.py \
  --fonts "Display,Body" --palette palette.json --project NAME \
  --macrostructure macro:CHOSEN-ID --animation --background \
  --emitted-css generated.html
```

Pass `--macrostructure` so the variety check penalizes a structure matching the last two projects (mirrors the font/palette step-down). Pass `--emitted-css` once generated output exists (Phase 7) to scan the rendered CSS for slop. The slop scan reports warnings and does not fail the build yet; promote a rule to error in `css_slop_rules.py` to make it blocking.

**Step 2: Review** validation report and the rendered-CSS slop scan. See `references/phase-details.md` for the full list of report checks (banned fonts, cliche colors, dominance ratio, motion count, hero composition, macrostructure variety, rendered-CSS slop rules, etc.).

**Step 3: Address issues** -- if overall score < 80:
1. Review each failed check in the report
2. Iterate on the specific problematic area (return to that phase)
3. Re-run validation after each fix
4. Keep iterating until the score is at least 80 before moving to specification output

**Gate**: Validation score is at least 80 (Grade B or higher). Deliver specification output only after the gate passes.

### Phase 7: Design Specification Output

**Goal**: Deliver a complete, implementable design specification. Only implement what was directly requested -- focus on distinctive aesthetics, not unnecessary abstractions or design system scaffolding unless the user explicitly asked for it.

**Step 0: Emit the design stamp** as the first line of the generated CSS. The stamp is a one-line comment recording the build's structural and quality results so a later run can re-audit statelessly and the variety check can recover the macro id from output:

```
/* vexjoy-design: macro=<id> theme=<name> contrast=<pass|fail> nav=<id> footer=<id> mobile=<pass|fail> */
```

Fill each field from this build's decisions: `macro` is the Phase 1 id, `theme` the palette name, `contrast`/`mobile` the WCAG and responsive results, `nav`/`footer` the chosen patterns. The stamp is a claim, not proof — the Phase 6 slop scan (`css_slop_rules.py`) verifies the rendered CSS independently rather than trusting the stamp. See `references/phase-details.md` for the field reference.

**Step 1: Generate CSS custom properties** (design tokens) covering typography, colors, spacing, shadows, and animation values. Reference `references/implementation-examples.md` for comprehensive token template.

**Step 2: Create base styles** that apply tokens to:
- Typography hierarchy (display, heading, body, mono)
- Atmospheric background (layered gradients/patterns)
- Layout reset and defaults

**Step 3: Document design specification** as a structured document covering:
- Aesthetic direction and inspiration
- Typography system with font families, weights, and usage roles
- Color palette with dominance structure and hex values
- Animation strategy with timing specifications
- Background technique and implementation
- Validation score and grade

**Step 4: If implementation is requested**, provide framework-specific starter code. Reference `references/implementation-examples.md` for React+Tailwind config, HTML+CSS templates, and design system templates.

**Step 5: Clean up** temporary exploration artifacts (intermediate JSON files, draft palettes). Keep only the final specification and validation report.

**Gate**: Design specification document delivered with all sections complete and validation score included.

### Examples

See `references/examples.md` for two worked examples (new landing page, design audit) showing the phase sequence end-to-end.

## Reference Material

### Design Catalogs

These reference files contain the curated domain knowledge that drives design decisions:

- `${CLAUDE_SKILL_DIR}/references/font-catalog.json`: Curated fonts by aesthetic category (banned fonts excluded)
- `${CLAUDE_SKILL_DIR}/references/color-inspirations.json`: Cultural/contextual color palette sources
- `${CLAUDE_SKILL_DIR}/references/animation-patterns.md`: High-impact animation choreography patterns with CSS and React examples
- `${CLAUDE_SKILL_DIR}/references/background-techniques.md`: Atmospheric background creation methods with code snippets
- `${CLAUDE_SKILL_DIR}/references/preferred-patterns.json`: Banned fonts, cliche colors, layout and component cliches
- `${CLAUDE_SKILL_DIR}/references/implementation-examples.md`: CSS tokens, base styles, framework templates, specification document templates
- `${CLAUDE_SKILL_DIR}/references/project-history.json`: Aesthetic choices across projects (auto-generated by validation)
- `${CLAUDE_SKILL_DIR}/references/vocabulary.md`: Term definitions used as hard rules across phases
- `${CLAUDE_SKILL_DIR}/references/macrostructure-catalog.md`: Named `macro:*` page structures (skeleton + anti-cliche note per entry); pick one in Phase 1, load only the chosen entry by heading anchor
- `${CLAUDE_SKILL_DIR}/references/phase-details.md`: Detailed selection processes, validation blocks, easing/timing tables, hero composition rules, validation checks
- `${CLAUDE_SKILL_DIR}/references/app-vs-landing-rules.md`: Full rule sets for landing vs app surface types
- `${CLAUDE_SKILL_DIR}/references/examples.md`: Worked examples for new landing page and design audit
- `${CLAUDE_SKILL_DIR}/references/error-handling.md`: Recovery for banned fonts, cliche palettes, low distinctiveness scores
- `${CLAUDE_SKILL_DIR}/references/game-ui-polish.md`: Game-native UI polish rules for AAA/Steam/roguelike surfaces, including failure modes learned from Road to AEW
- `${CLAUDE_SKILL_DIR}/references/css-audit-patterns.md`: grep/rg detection commands for banned fonts, hardcoded colors, over-animation, and flat backgrounds in implementation code — load when auditing CSS/SCSS/TSX files or verifying a generated spec was implemented correctly
- `${CLAUDE_SKILL_DIR}/references/performance-budgets.md`: CSS property render costs, compositor-thread promotion rules, layout thrashing detection commands, frame budget reference — load when animation performance is in scope or "animation performance profiling" optional capability is enabled

## Error Handling

See `references/error-handling.md` for recovery procedures covering banned fonts, cliche color schemes, and low distinctiveness scores.

## References

- `${CLAUDE_SKILL_DIR}/references/font-catalog.json`
- `${CLAUDE_SKILL_DIR}/references/color-inspirations.json`
- `${CLAUDE_SKILL_DIR}/references/animation-patterns.md`
- `${CLAUDE_SKILL_DIR}/references/background-techniques.md`
- `${CLAUDE_SKILL_DIR}/references/preferred-patterns.json`
- `${CLAUDE_SKILL_DIR}/references/implementation-examples.md`
- `${CLAUDE_SKILL_DIR}/references/project-history.json`
- `${CLAUDE_SKILL_DIR}/references/game-ui-polish.md`
- `${CLAUDE_SKILL_DIR}/references/css-audit-patterns.md`
- `${CLAUDE_SKILL_DIR}/references/performance-budgets.md`
- `${CLAUDE_SKILL_DIR}/references/macrostructure-catalog.md`
