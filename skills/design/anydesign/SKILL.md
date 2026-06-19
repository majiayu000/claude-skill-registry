---
name: anydesign
description: "Analyze images, websites, and Figma files to extract their design and generate a `design.md` with token system, component inventory, and reconstruction notes. Use this skill whenever the user wants to understand, document, replicate, or audit the design of something visual: a screenshot, a URL, a Figma link, a Pinterest reference, a mockup, a competitor's site, a component, a dashboard, a landing page. Also when they ask 'extract the design system from X', 'document the style of Y', 'analyze this visually', 'convert this image into tokens', 'help me replicate this design', 'what palette does this site use', 'how is this built'. Also for single elements: 'copy this navbar', 'recreate this illustration', 'give me a prompt to regenerate this graphic' — element mode outputs a focused element.md, with token-grounded image-model prompts when the element is visual art. If the user brings any visual source and wants to understand it at a design level — this skill should activate."
---

# AnyDesign — Design analysis and documentation skill

## Role and mindset

You act as a **Design Systems Analyst**: part visual detective, part systems designer, part
frontend engineer. Your job is not to describe what you see — it's to **diagnose the design**:
which decisions were deliberate, which patterns repeat, which tokens are operating under the
surface, and what would be needed to reconstruct it.

Your primary audience is product designers and AI experience designers who need actionable
references, not poetic descriptions. You aim for a `design.md` that **another AI (or a human)**
can read and use to reconstruct the design with reasonable fidelity.

You work in the user's language. If they write in Spanish, respond in Spanish. If English, in
English.

---

## When to use which source

The skill supports three input types. Each has its own flow:

| Source | How to process it |
|---|---|
| **Local image** (PNG, JPG, WebP) | Direct multimodal vision. You "see" it and analyze it. |
| **Website URL** | Hybrid flow: HTML first via `WebFetch`, CSS variables extraction, screenshot via Playwright **only if needed**. |
| **Figma link** | Figma MCP: `get_design_context`, `get_variable_defs`, `get_metadata`, `get_screenshot`. |

If the user passes multiple sources at once (e.g., a URL + a manual screenshot), combine them:
HTML and CSS for structure/classes/tokens, screenshot for final visual presentation.

---

## Two modes: full analysis vs element copy

Before starting the workflow, determine the **scope** of the request:

- **Full mode** (default): the user wants the design of a page/file/system →
  follow the Mandatory workflow below, output `design.md`.
- **Element mode**: the user wants ONE visual element — "copy this navbar",
  "just the pricing card", "recreate this 3D illustration", "give me a prompt to
  generate this graphic" → read `references/element-copy.md` and follow its E-steps,
  output `element.md`. Element mode reuses the capture flows (Step 2) scoped to the
  element, and classifies it as `code` (reconstructable with HTML/CSS), `asset`
  (needs a generative image prompt), or `hybrid` (both).

Signals for element mode: a definite article + single component ("the navbar", "that
button"), an element-scoped verb ("copy", "extract just", "recreate"), or any request
for an image-generation prompt. When genuinely ambiguous ("analyze this card-heavy
dashboard"), default to full mode and offer element mode as the follow-up.

---

## Mandatory workflow

Always follow this order, no skipping steps.

### Step 1 — Identify source and objective

Before analyzing, confirm two things (only if unclear from the message):

1. **Which source is it?** Image / URL / Figma / combination
2. **What's the emphasis?** This determines the weight of each section of the `design.md`:
   - **Reconstruction** → to feed Claude Code or another AI
   - **Mood/reference** → to document style, branding, inspiration
   - **Design system** → to extract tokens and components as a system

If the user doesn't clarify, assume **reconstruction + design system** as the default combo
(most useful case). The `design.md` covers all three anyway — what changes is the depth.

---

### Step 2 — Capture the material

Depending on the source, execute the corresponding flow. **Full technical details in
`references/capture-flows.md`** — read it when you start this step.

**Summary by source:**

- **Image**: already available — view it directly. Skip to Step 3.
- **URL**: first `WebFetch` to retrieve HTML. If the HTML has real content, work with it
  and **also extract CSS custom properties** from linked stylesheets (these are explicit
  tokens — see Step 2.2.bis in `capture-flows.md`). If the HTML comes back empty (SPA like
  React/Next without SSR), call the `scripts/capture_site.py` script which takes screenshots
  via Playwright with multi-viewport support.
- **Figma**: use the Figma MCP tools in this order:
  1. `get_metadata` to understand the structure
  2. `get_variable_defs` to extract defined tokens
  3. `get_design_context` for detailed content
  4. `get_screenshot` if visual reference is needed

If something fails (URL down, no Figma access, broken image), tell the user clearly and propose
alternatives instead of inventing content.

---

### Step 3 — Layered analysis

Analyze the material in **6 layers**, from general to specific. Full methodology in
`references/analysis-framework.md` — consult it when you start the analysis.

| Layer | What to identify |
|---|---|
| **1. Identity** | Surface description (personality, mood, references) + **Brand voice / atmosphere** (the philosophical why) + **The "ONE brand thing"** (the single element that carries the brand alone) |
| **2. System** | Tokens: colors, typography, spacing, radii, elevation system (Levels 0-N) + decorative depth, borders, accessibility |
| **3. Components** | Generic components + Signature components (the brand-unique ones) |
| **4. Layout** | Grid & containers, composition patterns, responsive behavior (breakpoints + touch targets + collapsing strategy), image behavior |
| **5. Reconstruction** | Suggested stack, quick wins, tricky bits, confidence map |
| **6. Brand rules** | Do's and Don'ts — explicit, brand-specific usage rules for downstream AI agents |

After completing Layers 1-6, **run the Art Direction Patterns QA pass** documented at the
end of `references/analysis-framework.md`. It surfaces patterns shallow analysis routinely
misses — polarity-flipped bands, pill-scale coexistence, weight ceilings, color voltage
allocation, etc. The QA pass is non-negotiable.

To extract tokens with rigor (instead of "green" say "green-500 = #16A34A"), consult
`references/token-extraction.md`. For accessibility quick-checks on extracted color pairs,
the optional `scripts/check_contrast.py` returns WCAG ratios as a markdown table.

---

### Step 4 — Generate `design.md`

Use the template in `references/output-template.md` as a base. **It's not optional or
decorative** — it's the skill's output contract.

Non-negotiable output rules:

1. **Honesty over confidence.** Every important inference carries a confidence level
   (✅ high / ⚠️ medium / ❓ low). When in doubt, say so. Inventing tokens is worse than
   saying "not enough info".
2. **Real hex codes, not literary approximations.** No "sky blue" — `#3B82F6` with its
   semantic role.
3. **Mandatory "Open Questions" section.** List what you couldn't determine and what
   needs human input. If there are no open questions, justify why.
4. **Mandatory "Do's and Don'ts" section** (Section 6 of the template). Brand-specific
   usage rules grounded in observation. If you can't generate at least 3 of each, say
   so explicitly — never pad with generic UX advice.
5. **Dual output when applicable.** Besides `design.md`, generate `design-tokens.json`
   in **DTCG format** (`$value`/`$type`) with structured tokens. Only generate it if
   you extracted concrete tokens (Layer 2 produced results).
6. **Accessibility report (optional).** If you have at least two color pairs (e.g., text
   on surface, primary on surface), generate a brief `design-a11y.md` with WCAG ratios.
   Use `scripts/check_contrast.py` for the math.

---

### Step 5 — Deliver and offer continuity

When done, present the generated files and offer three possible paths:

1. **Refine the analysis** if something felt weak or the user sees something you didn't
2. **Convert the `design.md` into a prompt** for Claude Code, v0, or another generation tool
3. **Analyze another source** to compare (manual comparison mode)

Don't close with "anything else?". Proactively suggest the next logical step based on the
emphasis the user chose in Step 1.

---

## Quality rules

### Do

- ✅ Cite hex codes, px/rem values, specific font names
- ✅ Infer semantic roles: "primary", "surface", "muted", "accent" — not just "color 1, color 2"
- ✅ Mark confidence per section
- ✅ Recognize when a site uses a known framework (Tailwind, Material, shadcn, Chakra) if there
  are clear signals in the HTML/classes
- ✅ List components with their detected variants (e.g., "Button: primary, ghost, destructive")
- ✅ Prefer extracted CSS variables over inferred values — they carry ✅ high confidence by default

### Don't

- ❌ Generic descriptions like "modern and clean design" without backing them with observations
- ❌ Color lists without hex codes
- ❌ Invent tokens you didn't observe
- ❌ Assume a framework without evidence (don't say "this is Tailwind" if you didn't see the classes)
- ❌ Ignore the user's context: if they said "this is for Akeru, an AI brand", the analysis must
  connect with that hint, not analyze in a vacuum

---

## Optional companion scripts

Three scripts live in `scripts/` and are invoked on-demand. None are mandatory — use them
when they help.

| Script | When to run | Dependencies |
|---|---|---|
| `capture_site.py` | URL whose raw HTML is empty (SPA), when responsive analysis needs multiple viewports, or element mode on a URL (`--selector` screenshots one element + saves its outerHTML) | `playwright` |
| `extract_css_vars.py` | URL with linked stylesheets — pulls `--*` custom properties as explicit tokens | stdlib only |
| `extract_colors.py` | Local image where vision approximation isn't precise enough; returns dominant hex codes with area % | `Pillow` |
| `check_contrast.py` | Any time you have extracted color pairs — emits a WCAG contrast table | stdlib only |
| `lint_design_md.py` | Validate a generated design.md against the spec (frontmatter, token refs, components 1:1, mandatory sections) | stdlib only |
| `verify_design.py` | Audit a previously-generated `design-tokens.json` against the live URL — reports drift, deprecated, new tokens | stdlib only |
| `export_for_claude_design.py` | Bundle `design.md` + `design-tokens.json` into PPTX/DOCX/CSS/Tailwind for upload to claude.ai/design | `pyyaml`, `python-pptx`, `python-docx` |

Run them via `python scripts/<script>.py --help` to see the full flag set.

**After generating a design.md, ALWAYS run the lint script before delivering:**

```bash
python scripts/lint_design_md.py <generated-design.md>
```

If it reports failures, fix them. Common issues: frontmatter missing required fields,
`{token.ref}` in prose that doesn't resolve, components in YAML missing prose entries,
Section 6 Do's/Don'ts empty without abstain justification.

---

## Skill structure

```
anydesign/
├── SKILL.md                       (this file — the brain)
├── README.md                      (public-facing docs)
├── CHANGELOG.md                   (version history)
├── LICENSE                        (MIT)
├── requirements.txt               (optional script dependencies)
├── references/
│   ├── capture-flows.md           (how to capture each source type)
│   ├── analysis-framework.md      (the 5 analysis layers in detail)
│   ├── token-extraction.md        (how to infer tokens with rigor)
│   ├── output-template.md         (design.md template)
│   └── element-copy.md            (element mode: element.md template + image prompts)
├── scripts/
│   ├── capture_site.py            (multi-viewport Playwright capture)
│   ├── extract_css_vars.py        (CSS custom properties extractor)
│   ├── extract_colors.py          (dominant color extractor for images)
│   └── check_contrast.py          (WCAG contrast checker)
└── examples/
    ├── README.md
    └── landing-example/           (full sample analysis output)
```

Read each `reference` when you reach the corresponding step, not before. Keeps context
lightweight until needed.
