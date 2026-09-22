---
name: product-shots-social-post
description: 'Designs social-platform-native visuals (Feed, Story, Reel, Carousel formats) for Instagram, TikTok, Facebook, Pinterest, RedNote, LinkedIn, X/Twitter and other social platforms — with platform-correct dimensions, safe zones, industry visual DNA, engagement hooks, and cross-slide consistency. Use when the user says "social post", "Instagram post", "IG post", "TikTok post", "Facebook post", "Pinterest pin", "social carousel", "feed post", "story post", "make a post", "design a social visual", "社媒帖", "做一个社媒图", or any underspecified social-media visual request. Routed from `product-shots` for the organic-social branch (non-ad).'
license: MIT
metadata:
  author: motiful
  source: product-shots ecosystem
  skill_id: product_shots_social_post
  version: "1.0"
---

# Social Post

Designs social-platform-native visuals (Feed, Story, Reel, Carousel) across Instagram, TikTok, Facebook, Pinterest, RedNote, LinkedIn, X/Twitter and other social platforms by combining nine canonical formats, seven industry visual-DNA presets, a seven-step workflow, a carousel framework with cross-slide consistency anchoring, and a self-audit gate. The skill produces a design description, optional caption, and self-check score per output.

The format taxonomy (Feed Square 1:1 / Feed Portrait 4:5 / Story 9:16 / Reel Cover 9:16 / Carousel 4:5 / etc.) maps directly across Instagram, TikTok, Facebook, RedNote, and Pinterest — the same aspect ratios are platform-native on all of them. Platform-specific safe-zone tuning lives in `references/hard-constraints.md`.

## Engagement Principles

These rules apply across every Section. Read before acting.

1. **Lock dimensions first** — every request resolves to one of nine formats with explicit width × height and aspect ratio. No format = no work.
2. **Industry DNA before composition** — match the user's industry to one of the seven presets; load its prompt patch + composition + color + lighting + common errors as a single bundle.
3. **Layered constraint priority** — Hard Constraints (Section 0) > Industry Rules (Section 1) > User Preferences > Model defaults. When user color overrides, industry default yields.
4. **Carousel consistency is per-slide repetition** — the consistency anchor is repeated verbatim at the start of every slide's prompt, not declared once.
5. **Mandatory self-audit before delivery** — every output passes the 14-item check (Section 4) and emits the seven-line Self-Check score.
6. **Banned words are filtered out of generator prompts** — platform names / UI terms / screenshot terms / brand-tool names never reach the image model. They are used only for internal format selection and industry matching.
7. **Match the user's language** — respond in English if user writes English, in Chinese if user writes Chinese. Never switch language unprompted.
8. **Use `<suggestion>` for option sets** — when proposing platform / format / industry choices, wrap them in `<suggestion>` tags. Never ask multiple questions at once.

## Execution Procedure

```
generate_social_visual(user_request) → design_description + caption + self_check + image

# Step 0 — Pin hard constraints (MUST, before any decision)
load references/hard-constraints.md
    → Dimensions table / Safe Zones / Text Overlay Rules / Design Quality Baseline / Banned Words
keep these in working context for Steps 1, 5, 6 — violation produces fake UI artifacts,
watermarks, occluded CTAs, or platform-policy breaks.
preflight = enforce_constraints(format=null, output_text=null, prompt_text=user_request)
                                              # references/hard-constraints.md
                                              # pre-flight banned-word scan on the user request
assert preflight.pass

# Step 1 — Confirm Format and Scenario (lock dimensions first)
format = resolve_format(user_request)         # references/hard-constraints.md §Default Format Selection
    if user specified format → use it
    else apply default scenario logic:
        single image content       → Feed Portrait 4:5
        multi-page knowledge       → Carousel 4:5
        short-lived / ad           → Story 9:16
        short-video cover          → Reel Cover 9:16
dimensions, ratio, safe_zone = lookup(format) # references/hard-constraints.md

# Step 2 — Identify Industry (auto-load Visual DNA)
industry_bundle = load_industry_dna(user_request)
                                              # references/industry-dna.md
                                              # returns {prompt_patch, composition, color,
                                              # lighting, common_errors, ig_references}
                                              # on no_match → closest industry as base + adjust

# Step 3 — Define Engagement Goal
goal = SHARE | SAVE | COMMENT
    if user specified → use it
    else infer from content type:
        education / how-to     → SAVE
        lifestyle / humor      → SHARE
        opinion / debate       → COMMENT

# Step 4 — Define the Hook (3-Second Rule)
hook_type = Bold Claim | Curiosity Gap | Visual Shock
    drives Slide-1 design (Carousel) or headline strategy (single image)

# Step 5 — Composition + Color (Industry × Format cross-decision)
composition = industry_bundle.composition + safe_zone constraints
color       = brand_color (if exists, overrides) or industry_bundle.color
lighting    = industry_bundle.lighting
text        = format.text_overlay_rule (references/hard-constraints.md §Text Overlay)
if format == Carousel:
    slides = build_carousel(content, hook_type, industry_bundle, brand_color, goal)
                                                                              # references/carousel-framework.md

# Step 6 — Self-Check Gate (mandatory)
audited_output = run_workflow(user_request)
                                              # references/workflow-and-self-check.md
                                              # runs Section 2 steps + Section 4 14-item audit
findings = enforce_constraints(format, audited_output.output_text, audited_output.prompt_text)
                                              # references/hard-constraints.md
                                              # re-validates sizing, safe zone, overlay, quality, banned words
assert findings.pass
    if any item fails → revise prompt, regenerate
    if all pass       → emit self_check score block

# Step 7 — Iterative Refinement
on user satisfied → offer style variants / cross-platform adaptation / Carousel expansion / caption (if absent)
on user request   → adjust color / composition / style / format / hook (supports local edit, no full regen)

# Output assembly + dispatch image generation
grid_strategy, caption = finalize_grid_and_caption(format, user_caption, brand_account_context)
                                              # references/grid-and-caption.md
emit design_description (6 items per references/workflow-and-self-check.md §Section 6)
emit caption — separate text block, never rendered into image
emit self_check_score (7-line block)

image = Skill("product-shots-image-gen",
              f"generate: {rendered_prompt} | format={format} | aspect={ratio}")
# Do NOT substitute with direct API call.
assert image.delivered
```

## TOC of Module Files

- `references/hard-constraints.md` — Section 0 (Dimensions / Safe Zones / Text Overlay / Quality Baseline) + Section 9 (Prompt Banned Words). MUST-level. Loaded at EP Step 0.
- `references/industry-dna.md` — Section 1: seven industries × six dimensions (Prompt Patch, composition, color, lighting, common errors, social references).
- `references/carousel-framework.md` — Section 3: 7-Slide Framework + Swipe Psychology + Visual Consistency and Typography (cross-slide anchor template).
- `references/workflow-and-self-check.md` — Section 2 (Core Workflow seven steps) + Section 4 (Common Mistakes self-audit, 14 items) + Section 6 (Output Format).
- `references/grid-and-caption.md` — Section 5 (Feed Grid Aesthetics, five strategies) + Section 7 (Caption & Copywriting incl. Social Caption Persona).

## Section Index

```
Goal
Language Rule
0. Hard Constraints                            → references/hard-constraints.md
  Dimensions / Safe Zones / Text Overlay / Quality Baseline
1. Industry Visual DNA                          → references/industry-dna.md
  1.1 Beauty / 1.2 Fashion / 1.3 Tech / 1.4 Lifestyle
  1.5 Travel / 1.6 Food / 1.7 Fitness
2. Core Workflow                                → references/workflow-and-self-check.md §Workflow
  Step 1: Confirm Format and Scenario — Lock Dimensions First
  Step 2: Identify Industry — Auto-Load Visual DNA
  Step 3: Define Engagement Goal
  Step 4: Define the Hook — 3-Second Rule
  Step 5: Composition and Color — Industry × Format Cross-Decision
  Step 6: Self-Check Gate
  Step 7: Iterative Refinement
3. Carousel Standards (Applies when format = Carousel) → references/carousel-framework.md
  A. The 7-Slide Framework
  B. Swipe Psychology
  C. Visual Consistency and Typography
4. Common Mistakes and Self-Audit (Mandatory Gate)    → references/workflow-and-self-check.md §Self-Audit
5. Feed Grid Aesthetics                               → references/grid-and-caption.md §Grid
  Common Grid Strategies / Grid Rules
6. Output Format                                       → references/workflow-and-self-check.md §Output Format
  Design Description (6 Items) / Caption / Self-Check Score
7. Caption & Copywriting                               → references/grid-and-caption.md §Caption
  In-Image Text vs. Caption / Caption Logic / Social Caption Persona
8. Prompt Banned Words — Prevent Artifacts / Watermarks / Screenshot Look
                                                       → references/hard-constraints.md §Section 9
IMPORTANT！Suggestion
```

## Goal

Design social-platform-native visuals (Feed, Story, Reel, Carousel) across Instagram, TikTok, Facebook, Pinterest, RedNote, LinkedIn, and X/Twitter — platform-correct (dimensions / safe zones), industry-appropriate (seven Visual DNA presets), engagement-tuned (SHARE / SAVE / COMMENT), and grid-coherent (Feed harmony). Every output passes a 14-item self-audit and emits a seven-line self-check score.

## Language Rule

```
Always respond in the user's language.
IF user writes in English THEN respond in English
IF user writes in Chinese THEN respond in Chinese
NEVER switch language unprompted.
```

## IMPORTANT — Suggestion Format

```
IMPORTANT！Suggestion:
Always use <suggestion> format to guide the user.
Do not ask several questions at once.

Example: use <suggestion> format to provide options like
Instagram / TikTok / Facebook / Pinterest / RedNote / LinkedIn / X (Twitter) / Other platform.
```

This is the front-end rendering instruction — option sets are wrapped in `<suggestion>` tags so the UI renders them as clickable chips.

## Cross-Skill Notes

- **Upstream router**: `product-shots` routes here for the organic-social branch when `asset_type ∈ {post, carousel, feed, story, reel}` AND `is_promotion != True`. Promotional / ad creative requests route to `product-shots-ad-creative` instead.
- **Industry Visual DNA presets** (seven industries) are shared with `product-shots` and `product-shots-ad-creative` (cross-skill consistency).
- **Sibling skills**: `product-shots-main-image` / `product-shots-detail-page` (Amazon product/detail page imagery) — can produce source assets that get repurposed for social posts; `product-shots-multi-angle` (model 9-angle series) — produces fashion lookbook content that can be reframed for social Carousel. `product-shots-ad-creative` handles paid promotion / ad-objective creative with platform takedown-risk rules.
- **Image generation backend**: rendered prompts are dispatched to `product-shots-image-gen` (the product-shots image-gen engine) which abstracts the underlying API (OmniMaaS / OpenAI / Gemini).

## Tooling

The skill emits design prompts and self-check output. Image generation is invoked through `product-shots-image-gen` (the product-shots image-gen engine) using the prompts produced here.
