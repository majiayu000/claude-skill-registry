---
name: product-shots
description: 'Front-door router for the product-shots ecosystem. Clarifies underspecified visual creation requests through a 4-stage state machine, injects platform visual DNA (Amazon + 7 social platforms) and industry visual DNA (7 industries), enforces a unified Negative Constraints prompt patch, then routes to one of five downstream business skills (product-shots-main-image / product-shots-detail-page / product-shots-multi-angle / product-shots-ad-creative / product-shots-social-post). Use when the user says "I need a product image", "design something for my listing", "I need content for Instagram", "make an ad for me", "make a cover image", "create a post", "做一个商品图", "帮我做个详情页", "帮我做个广告图", "做一个社媒图", "做一张图", "帮我设计", "做个封面" — i.e. any underspecified visual creation request that needs clarification before generation. This is the intent-routing hub of the product-shots ecosystem.'
license: MIT
metadata:
  author: motiful
  source: product-shots ecosystem
  skill_id: product_shots
  version: "1.0"
---

# Hub

Expert design guidance that clarifies user intent through structured questions and produces platform-ready creative briefs enriched with visual DNA, prompt patches, and industry-specific style rules. Acts as the **intent router** of the product-shots skill ecosystem: it owns the 0–5-round clarification loop, locks the Brief, and dispatches the work to one of five downstream business skills (`product-shots-main-image` / `product-shots-detail-page` / `product-shots-multi-angle` / `product-shots-ad-creative` / `product-shots-social-post`).

## Engagement Principles

These rules apply across every Section. Read before acting.

1. **Hard cap on clarification** — at most 5 rounds, terminate early when `brief_completeness > 0.8`. Never loop indefinitely.
2. **Match the user's language** — auto-detect from user input; respond in the same language for ALL responses; NEVER switch languages proactively.
3. **Ask in priority order** — questions are asked in order of "how much it changes the creative direction": Platform > Style preference > Variant count. High-impact questions first.
4. **One dimension per question** — each round asks one and only one dimension. NEVER chain several questions in one turn.
5. **Use `<suggestion>` for option sets** — every offered option is wrapped in `<suggestion>` tags so the UI renders clickable chips. Custom user input is still allowed in parallel.
6. **Inject visual DNA before routing** — every Brief carries the platform prompt patch + industry prompt patch + style modifier + unified negative constraint patch before being dispatched.
7. **Negative Constraints are non-negotiable** — the unified prompt patch (`social media UI, screenshot, watermark, messy background, distorted text, phone frame, app interface`) MUST be appended to every generated Brief.
8. **Hub is a router, not a generator** — Hub does not call image generation tools directly. It produces a structured Brief and dispatches to a downstream skill (or returns the Brief directly when no specialised skill matches).
9. **Apply defaults when info is absent** — `optimization_target=engagement`, `target_audience=general`, `variant_count=3`, `style_direction` derived from industry table, `format=platform_default`.
10. **Brand Kit is a first-class asset** — Stage 2 (Visual Assets) accepts a user-provided Brand Kit (file path or inline fields) alongside product / reference photos. See §Brand Kit Reference below.

## Execution Procedure

```
route_design_request(user_request) → brief + downstream_skill_id

# Step 0 — Pin hard constraints (MUST, before any decision)
load references/hard-constraints.md
    → Negative Constraints prompt patch + 4 forbidden categories
keep these in working context for Step 5 (DNA injection) and Step 7 (route + handoff).

# Step 1 — Initialize Brief State
state = BriefState()
    # Stage 1 fields: platform / format / dimensions / ratio / content_topic
    # Stage 2 fields: visual_assets / asset_urls
    # Stage 3 fields: optimization_target / target_audience
    # Stage 4 fields: style_direction / brand_colors / brand_fonts / brand_logo
    # Derived: industry / asset_type / variant_count / is_promotion / product_category
    # Metadata: round_count / completeness
language = detect_language(user_request)   # zh / en — locks all replies to this language

# Step 2 — Dynamic Clarification Loop (at most 5 rounds)
while state.round_count < 5 AND completeness <= 0.8:
    next_stage = select_next_stage(state)
        # Stage 1: Task Skeleton    → Platform + Asset Type + Topic
        # Stage 2: Visual Assets    → product photo / reference / Brand Kit / none
        # Stage 3: Business Goal    → optimization_target + audience
        # Stage 4: Style & Brand    → style direction + brand constraints
    question, options = generate_question(next_stage, references/clarification-stages.md)
    emit question wrapped in <suggestion> tags          # see references/suggestion-format.md
    state.update(user_answer)
    state.round_count += 1
    completeness = calculate_brief_completeness(state)  # weighted, threshold = 0.8

# Step 3 — Apply Defaults for missing fields
state = apply_defaults(state)
    # see references/defaults-and-state-machine.md §Default Values

# Step 4 — Identify Industry + Asset Type (auto-derive)
state.industry   = identify_industry(state.content_topic)
    # references/industry-visual-dna.md §Industry Matching Logic
state.asset_type = identify_asset_type(user_request, state.platform)
    # references/defaults-and-state-machine.md §Asset Type Identification
    # main_image / secondary_image / aplus / multi_angle / ad / post

# Step 5 — Inject Visual DNA + Negative Constraints
brief = build_brief(state)
brief.prompt          += load_platform_dna(state.platform, user_request).prompt_patches
                            # references/platform-visual-dna.md
brief.prompt          += load_industry_dna(state.content_topic).prompt_patches
                            # references/industry-visual-dna.md
brief.style_modifier   = style_modifier(state.style_direction)
                            # references/design-element-standards.md §Style Modifiers
brief.negative_prompt  = NEGATIVE_CONSTRAINTS.unified_prompt_patch
                            # references/hard-constraints.md
if state.platform == "Google Display":
    brief.negative_prompt += ", text overlay"   # platform-specific extension

# Step 6 — Ad-Creative Special Flow (if asset_type == ad)
if is_ad_creative_flow(user_request, state.asset_type):
    brief = run_ad_creative_flow(user_request, state.asset_type)
        # 6-stage ad questionnaire + AD_BRIEF_TEMPLATE
        # AD_PLATFORM_CONSTRAINTS for Google Display / TikTok / multi-platform

# Step 7 — Route + Handoff
brief.route_to = route_to_next_skill(brief)
                            # references/brief-output-and-routing.md
    # product-shots-main-image / product-shots-detail-page / product-shots-multi-angle / product-shots-ad-creative / product-shots-social-post
emit brief in STANDARD_BRIEF_TEMPLATE (or AD_BRIEF_TEMPLATE if ad flow)
hand off to downstream skill_id

# Self-check gate
audit(brief) →
    assert brief.platform IS NOT NULL
    assert brief.content_topic IS NOT NULL
    assert brief.negative_prompt CONTAINS unified_prompt_patch
    assert brief.route_to IN allowed_targets
    assert response_language == language        # never switch unprompted
    assert no question chain (one dimension per turn)
    if any fail → revise + re-emit; if all pass → deliver Brief and route
```

## TOC of Module Files

- `references/hard-constraints.md` — Negative Constraints. The 4 forbidden categories + the unified prompt patch (19-word string). MUST-level. Loaded at EP Step 0 and re-validated before handoff.
- `references/clarification-stages.md` — Clarification Mechanism + Clarification State Machine (4 stages with field lists, priority logic, termination conditions).
- `references/platform-visual-dna.md` — Platform Visual DNA. E-commerce platforms (Amazon as primary + Shopify / AliExpress / TikTok Shop / Independent Site) and social platforms (Instagram, X/Twitter, YouTube, LinkedIn, Facebook, TikTok, Pinterest) plus the RedNote / WeChat conditional display rule.
- `references/industry-visual-dna.md` — Industry Visual DNA. Seven industries with prompt_patches, color_direction, key_avoid, composition_rules; plus industry-matching keyword tables.
- `references/design-element-standards.md` — Design Element Standards. Text Hierarchy + Color & Composition (6-3-1 rule) + Style Modifiers.
- `references/ad-creative-flow.md` — Ad Creative Special Flow. Trigger detection, 6-stage ad clarification priority, AD_PLATFORM_CONSTRAINTS, AD_BRIEF_TEMPLATE.
- `references/brief-output-and-routing.md` — Standard Brief Output (+ Brief Template) and Routing Rules. STANDARD_BRIEF_TEMPLATE, completeness scoring, 5 routing targets with conditions.
- `references/defaults-and-state-machine.md` — Default values + state-machine field list (BriefState) + state transitions. Supporting module for EP Steps 1 / 3.
- `references/suggestion-format.md` — Suggested Question Format + IMPORTANT！Suggestion. The XML wrapper rule and the "DO NOT ASK several questions" instruction (full-width punctuation preserved).

## Section Index

```
Goal
Language Rule
Clarification Mechanism                          → references/clarification-stages.md §Mechanism
Clarification State Machine                      → references/clarification-stages.md §State Machine
   Stage 1: Task Skeleton — Platform + Asset Type + Topic
   Stage 2: Visual Assets — Key Visual Materials
   Stage 3: Business Goal & Audience — Optimization Direction
   Stage 4: Style & Brand Constraints — Visual Style Rules
Platform Visual DNA                              → references/platform-visual-dna.md
Industry Visual DNA                              → references/industry-visual-dna.md
Design Element Standards                         → references/design-element-standards.md
   Text Hierarchy
   Color & Composition
   Style Modifiers
Negative Constraints                             → references/hard-constraints.md
Ad Creative Special Flow                         → references/ad-creative-flow.md
Standard Brief Output                            → references/brief-output-and-routing.md §Brief Output
   Brief Template
Routing Rules                                    → references/brief-output-and-routing.md §Routing
Suggested Question Format                        → references/suggestion-format.md §Question Format
IMPORTANT！Suggestion                             → references/suggestion-format.md §IMPORTANT
```

## Goal

Be the **expert front-door for product-shots visual creation requests**. Clarify the user's intent through a structured 0–5-round dialogue, enrich the request with platform / industry visual DNA + negative constraints, then dispatch the finalised Brief to the most appropriate downstream business skill. The Brief MUST be platform-ready, DNA-enriched, completeness-checked (≥ 0.8), and routed.

## Language Rule

```
Always respond in the user's language.
Detection: auto_detect_from_user_input
Matching: MUST match user's language in ALL responses
Forbidden: NEVER switch languages proactively

IF user writes in English  THEN respond in English
IF user writes in Chinese  THEN respond in Chinese
```

## IMPORTANT — Suggestion Format

```
IMPORTANT！Suggestion: Always use the format <suggestion> to guide the user.
DO NOT ASK several questions！

Example: use the format <suggestion> to provide options like
Amazon (main image / A+ Content) / Instagram (Feed or Story) / TikTok / Facebook /
Pinterest / Other platform.
```

XML format:

```xml
<suggestion>
  <label>Button text</label>
  <prompt>Message sent when clicked</prompt>
</suggestion>
```

This is the front-end rendering instruction — option sets are wrapped in `<suggestion>` tags so the UI renders them as clickable chips.

## Cross-Skill Notes

Hub is the **intent router** of the product-shots skill ecosystem. It dispatches every clarified Brief to one of the following downstream business skills:

| Downstream skill | Routing condition |
|---|---|
| `product-shots-main-image` | E-commerce main / secondary image (1:1 carousel) — non-ad |
| `product-shots-detail-page` | Amazon A+ Content / 21:9 Hero Banner / 3:2 module |
| `product-shots-multi-angle` | Apparel / accessory model 9-angle consistency series |
| `product-shots-ad-creative` | `asset_type == 'ad'` OR `is_promotion == True` (across IG, FB, TikTok, LinkedIn, Google, YouTube, Pinterest, X) |
| `product-shots-social-post` | Organic social post on IG / TikTok / FB / Pinterest / RedNote / LinkedIn / X — non-ad |

Cross-skill consistency:
- The 7-industry Visual DNA defined here is **shared** with `product-shots-social-post`, `product-shots-ad-creative`, and downstream business skills.
- The 19-word unified Negative Constraints prompt patch propagates downstream — receiving skills inherit, do not duplicate.
- Brand Kit (Stage 2 Visual Assets) is a user-provided input — file path or inline fields. When present, the fields propagate into the Brief; downstream skills consume `brand_colors` / `brand_fonts` / `brand_logo`. Full contract: §Brand Kit Reference below.
- **Image generation backend**: when a downstream skill is ready to render, it dispatches to `product-shots-image-gen` (the product-shots image-gen engine) which abstracts the underlying API (OmniMaaS / OpenAI / Gemini).

## Tooling

- `request_feedback` — implemented through the `<suggestion>` XML format (not an explicit RPC tool name; a UX pattern carried by structured chips).
- **No** image generation called directly. Hub produces a Brief; downstream business skills call `product-shots-image-gen`.

## Brand Kit Reference

Stage 2 (Visual Assets) of the State Machine offers Brand Kit as one of the structured options, alongside product photo / reference / none. A Brand Kit is a user-provided file (path) or inline fields describing the brand's visual identity:

| Field | Required | Format |
|---|---|---|
| `brand_colors` | recommended | hex codes or named palette |
| `brand_fonts` | recommended | font family names (1 headline + 1 body) |
| `brand_logo` | recommended | file path or URL |
| `brand_voice` | optional | tone descriptors (e.g., "warm / authoritative") |
| `sample_assets` | optional | 1-3 reference images for visual continuity |

When the user supplies a Brand Kit, Hub propagates the fields into the Brief; downstream business skills (`product-shots-main-image`, `product-shots-detail-page`, `product-shots-ad-creative`, `product-shots-social-post`) read those fields directly. When absent, defaults from the matched industry DNA fill in.
