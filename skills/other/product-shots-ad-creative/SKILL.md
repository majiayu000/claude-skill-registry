---
name: product-shots-ad-creative
description: 'Designs high-performing ad creatives across Instagram, Facebook, TikTok, LinkedIn, Google (Display / Demand Gen), YouTube, Pinterest, and X/Twitter — locking platform dimensions, safe zones, text overlay policy, character limits, industry visual DNA, ad objective hierarchy, composition patterns, CTA strategy, and prompt sanitation. Use when the user says "create an ad", "design an ad creative", "make an ad", "广告创意", "帮我做个广告图", "Instagram ad", "TikTok ad", "Facebook ad", "Google Display ad", "LinkedIn ad", "YouTube ad", "Pinterest ad", "promotional image", "campaign creative", "ad banner", "投放图", or any platform-specific ad request. Routed from `product-shots` when `asset_type == "ad"` or `is_promotion == True`.'
license: MIT
metadata:
  author: motiful
  source: product-shots ecosystem
  skill_id: product_shots_ad_creative
  version: "1.0"
---

# Ad Creative Design

Designs ad creatives that are platform-native (correct dimensions, safe zones, text overlay policy, character limits), industry-precise (visual DNA per industry × ad objective), and prompt-sanitized (no platform names / UI artifacts / fake ad elements leak into the image generator). The skill lays out an 8-platform × 21-format matrix, a six-step workflow, a self-check gate, and a banned-words system with a positive-preservation companion rule.

## Engagement Principles

These rules apply across every Section. Read before acting.

1. **No generic one-size-fits-all creatives** — every creative is locked to a specific (platform, format, objective, industry) tuple. No tuple = no work.
2. **Hard Constraints first** — Section 0 (Platform Dimensions / Safe Zones / Text Overlay / Ad Copy Char Limits) is loaded at Step 0 and re-validated at the Self-Check Gate before delivery. Violations like "text on Google Display" or "CTA in TikTok bottom 18%" cause platform takedowns or render the ad invisible.
3. **Brand Name & User Copy Fidelity is MUST-level** — every brand name, slogan, CTA text, and price/offer the user specified must appear verbatim in the deliverable. Never paraphrase, translate, or substitute user-supplied copy.
4. **Industry × Objective drives composition + color** — pick the composition pattern and color strategy from the cross-decision matrix (Section 8 / Section 9), not from generic style intuition.
5. **Platform Style Profiles are not stylistic suggestions** — they are constraints. TikTok requires anti-ad aesthetic AND complete brand/product/CTA info; LinkedIn requires ≥60pt fonts; Pinterest requires aspirational scenes; Google Display requires zero text overlay.
6. **Prompt Banned Words are filtered out of the image generator prompt** — platform names, ad-UI terms, brand-tool names never reach the model. They are used internally for routing and rule selection only.
7. **Required Positive Instruction protects native packaging text** — "no text overlay" must not delete printed text on the product itself. Always pair the banned-words filter with the positive preservation instruction (references/banned-words.md §Required Positive Instruction).
8. **Match the user's language** — respond in English if the user writes English, in Chinese if Chinese. Never switch language unprompted.
9. **Use `<suggestion>` for option sets** — when proposing platform / objective / industry / asset choices, wrap them in `<suggestion>` tags. Never ask multiple questions at once.

## Execution Procedure

```
generate_ad_creative(user_request) → variant[] + self_check
# This EP IS the inlined procedural backbone. Each Step calls the EP entry point
# of its corresponding reference module — bindings below are bidirectional (every
# call has a matching `def` in references/*.md).

# Step 0 — Pin hard constraints (MUST, before any decision)
load references/hard-constraints.md
    → Platform Dimensions / Safe Zones / Text Overlay Rules / Ad Copy Char Limits
load references/banned-words.md
    → Prompt Banned Words + Required Positive Instruction (Preserve Native Packaging Text)
keep these in working context for every step.
defer enforcement to Step 6 — `enforce_constraints(format, output_text, prompt_text, user_copy)`
will be called there with the four params built up over Steps 1–5.

# Step 1 — Platform + Objective (Quick Start: 7 required fields)
brief_state = preflight(user_request)  # references/quick-start-and-fidelity.md
collect 7_required_fields:
    platform, format, ad_objective, industry,
    visual_assets, brand_kit, copy (brand_name / slogan / cta / price)
missing = [f for f in 7_required_fields if not provided(f)]
if missing:
    filled = Skill("product-shots", f"fill missing fields: {missing}")
    # `Skill("product-shots", "fill missing fields: <list>")` — the hub/router skill owns Quick Start clarification.
    # ad-creative owns the post-fill workflow. Do not substitute with manual clarification questions.
    assert filled.delivered          # Step 2 requires the filled brief
    brief = filled.brief
else:
    brief = brief_state.ready_brief
for phrase in [brief.copy.brand_name, brief.copy.slogan, brief.copy.cta, brief.copy.price]:
    if phrase: register_protected_phrase(phrase)   # references/banned-words.md

# run_workflow(brief) is the canonical procedural backbone. Steps 2–6 below
# unfold it inline so the EP stays readable; each named call matches a `def`
# entry in the corresponding reference module.
result = run_workflow(brief)   # references/workflow-and-self-check.md

# Step 2 — Industry + Brand
industry = match_industry(user_request)
bundle   = load_industry_bundle(industry)   # references/industry-style-rules.md
                                            # (color palette / composition / typography / CTA tone / forbidden)
if brief.brand_kit:
    kit = parse_brand_kit(brief.brand_kit)    # references/industry-style-rules.md
    apply_brand_kit_overrides(bundle, kit):
        • brand colors  → primary palette  (overrides industry defaults)
        • brand fonts   → headlines
        • brand logo    → composed per platform safe-zone rules

# Step 3 — Visual Asset Audit
"Available assets determine the creative ceiling."
classified_assets = classify(brief.visual_assets)   # references/composition-patterns.md
    # ∈ {has_product_photo, has_model_photo, has_logo_only, has_none, ...}
    # drives composition pattern selection in Step 4

# Step 4 — Composition + Color (Industry × Objective cross-decision)
composition    = select_composition_pattern(industry, ad_objective, classified_assets)
    # references/composition-patterns.md (12 patterns)
color_strategy = pick_color_strategy(industry, brief.brand_kit)
    # references/color-and-cta-strategy.md §Color Strategy
cta_strategy   = pick_cta_strategy(ad_objective, platform)
    # references/color-and-cta-strategy.md §CTA Strategy
apply_objective_rules(creative, ad_objective)
    # references/ad-objective-rules.md — info hierarchy / cta_intensity / text_density
validate_color_scheme(color_strategy.primary, industry)
    # references/color-and-cta-strategy.md / industry-style-rules.md

# Step 5 — Platform Adaptation Layer (inject platform-specific differences)
for each target_platform in brief.platforms:
    apply_platform_profile(prompt, target_platform)
        # references/platform-style-profiles.md (tone / production / text style / cadence)
    prompt = sanitize_prompt(prompt, protected_phrases)
        # references/banned-words.md — filter banned words, restore user copy,
        # inject Required Positive Instruction (Preserve Native Packaging Text)
multi_platform_fanout(brief, brief.platforms)
    # references/multi-platform-output.md (per-platform output + cross-format consistency)
# Section 16 — fill any deferred field with DEFAULTS
for field in required_fields:
    if not provided(field) and user_deferred(field):
        use DEFAULTS[field]   # references/failures-defaults-output.md §Defaults

# Step 6 — Self-Check Gate (mandatory) — Quality Check Before Delivery
for each variant:
    findings = enforce_constraints(format, output_text, prompt_text, user_copy)
        # references/hard-constraints.md — re-validates dimensions / safe zones /
        # text overlay / char limits / banned words / Required Positive Instruction /
        # Brand Name & User Copy Fidelity (user_copy preserved verbatim)
    if findings:
        revise prompt and regenerate
        continue
    apply_objective_rules(variant, ad_objective)         # Check 10 promotion validation
    validate_tiktok_native_aesthetic(variant)            # Check 7 platform_tone (when platform == tiktok)
    validate_color_scheme(dominant_colors, industry)     # Check 6 industry forbidden colors
    if all pass → emit variant

# Output assembly — variant[] + self_check_score block per
# references/failures-defaults-output.md §Section 17 VARIANT_OUTPUT_SCHEMA.
emit variant[] + self_check_score
on user request → iterate
on user satisfied:
    Run: `Skill("product-shots-image-gen", f"render variants: {variant[].prompt} use_case=text-overlay")`
    Do not substitute with manual image-generation prompts or direct model calls.
    Record output — final delivery to the user requires the rendered images.
    use_case=text-overlay is REQUIRED for ad-creative — ad copy (headlines,
    CTAs, price chips) MUST render legibly; this routes to gpt-image-2.
    See product-shots-image-gen/references/model-selection.md.
```

## TOC of Module Files

- `references/hard-constraints.md` — Section 5 (Hard Constraints, 4 sub: Platform Dimensions / Safe Zones / Text Overlay Rules / Ad Copy Character Limits). MUST-level. Loaded at EP Step 0 and re-validated at Step 6.
- `references/banned-words.md` — Section 20 (Prompt Banned Words, 3 sub: Exception / Banned Words List / Required Positive Instruction). MUST-level. Loaded at EP Step 0 alongside hard-constraints.md and re-validated at Step 6. Split from hard-constraints.md to keep both files under the 300-line cap.
- `references/quick-start-and-fidelity.md` — Section 3 (Target Users), Section 4 (Quick Start — 7 Required Fields), Section 5 (Brand Name & User Copy Fidelity Rule).
- `references/workflow-and-self-check.md` — Section 6 (Core Workflow Six-Step Process), the procedural backbone with the Self-Check Gate.
- `references/industry-style-rules.md` — Section 7 (Industry Style Rules), industry × visual parameters (color, composition, typography, CTA tone, forbidden, market share).
- `references/ad-objective-rules.md` — Section 8 (Ad Objective Rules — Objective Determines Information Hierarchy).
- `references/platform-style-profiles.md` — Section 9 (Platform Style Profiles — Quick Reference, per-platform tone / production / text style / refresh cadence / what works / avoid).
- `references/composition-patterns.md` — Section 10 (Composition Patterns — Shared Pattern Library, 12 patterns).
- `references/color-and-cta-strategy.md` — Section 11 (Color Strategy: Industry × Color Matrix + Color Rules) + Section 12 (CTA Strategy).
- `references/multi-platform-output.md` — Section 13 (Multi-Platform Output Rules) + Section 14 (Creative Fatigue & Refresh Cadence).
- `references/failures-defaults-output.md` — Section 15 (Common Failure Modes) + Section 16 (Defaults — Fallback Values When User Doesn't Specify) + Section 17 (Output Format) + Section 18 (Performance Benchmarks).

## Section Index

```
Goal — No Generic One-Size-Fits-All Creatives        → SKILL.md §Goal
Language Rule                                        → SKILL.md §Language Rule
Target Users — Small Business Owners and Marketers   → references/quick-start-and-fidelity.md §Target Users
Quick Start — 7 Required Fields Before Generating    → references/quick-start-and-fidelity.md §Quick Start
Brand Name & User Copy Fidelity Rule                 → references/quick-start-and-fidelity.md §Fidelity Rule
Hard Constraints — Must Not Be Violated              → references/hard-constraints.md
  Platform Dimensions — Quick Reference
  Safe Zones — Each Platform's UI Overlays Differ Completely
  Text Overlay Rules — Text Policies Vary Drastically Across Platforms
  Ad Copy Character Limits
Core Workflow — Six-Step Process                     → references/workflow-and-self-check.md
  Step 1: Platform + Objective
  Step 2: Industry + Brand
  Step 3: Visual Asset Audit — Available Assets Determine the Creative Ceiling
  Step 4: Composition + Color — Determined by Industry × Objective
  Step 5: Platform Adaptation Layer — Inject Platform-Specific Differences
  Step 6: Self-Check Gate — Quality Check Before Delivery
Industry Style Rules                                 → references/industry-style-rules.md
Ad Objective Rules — Objective Determines Info Hierarchy → references/ad-objective-rules.md
Platform Style Profiles — Quick Reference            → references/platform-style-profiles.md
Composition Patterns — Shared Pattern Library        → references/composition-patterns.md
Color Strategy — Industry-Based Color Guide          → references/color-and-cta-strategy.md §Color Strategy
  Industry × Color Matrix
  Color Rules
CTA Strategy — Call-to-Action Design Rules           → references/color-and-cta-strategy.md §CTA Strategy
Multi-Platform Output Rules                          → references/multi-platform-output.md §Multi-Platform Output
Creative Fatigue & Refresh Cadence                   → references/multi-platform-output.md §Refresh Cadence
Common Failure Modes                                 → references/failures-defaults-output.md §Common Failure Modes
Defaults — Fallback Values When User Doesn't Specify → references/failures-defaults-output.md §Defaults
Output Format — Standard Output per Variant          → references/failures-defaults-output.md §Output Format
Performance Benchmarks — Key Data Reference          → references/failures-defaults-output.md §Performance Benchmarks
Prompt Banned Words — Avoid Watermarks, UI Artifacts, and Fake Ad Elements
                                                     → references/banned-words.md
  Exception: User-Specified Content Passthrough
  Banned Words List
  Required Positive Instruction — Preserve Native Packaging Text
IMPORTANT！Suggestion                                → SKILL.md §IMPORTANT — Suggestion Format
```

## Goal

Design ad creatives that are platform-native (precise dimensions, safe zones, text overlay policy, character limits), industry-precise (visual DNA matched to industry × ad objective), and prompt-clean (no fake UI / watermarks / platform names leak into the image generator). Refuse to produce a generic "one-size-fits-all" image. Every variant passes a self-check gate before delivery.

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
Instagram (Feed / Story / Reel / Carousel) / Facebook / TikTok / LinkedIn /
Google Display / Google Demand Gen / YouTube / Pinterest / X (Twitter) / Other platform.
```

This is the front-end rendering instruction — option sets are wrapped in `<suggestion>` tags so the UI renders them as clickable chips.

## Cross-Skill Notes

- **Upstream router**: `product-shots` routes here when `asset_type == "ad"` or `is_promotion == True`. The conditional pre-fill for Quick Start fields happens inside `product-shots`'s clarification state machine; the actual six-step workflow runs **inside this skill** (Section 6).
- **Quick Start dependency**: when any of the 7 required fields is missing, this skill defers to `product-shots` for clarification (`"If any of these are missing, use hub first."`). This is **conditional pre-fill**, not a hand-off — once fields are filled, control returns here.
- **Brand Kit**: when the user provides a Brand Kit (file path or inline colors / fonts / logo), Step 2 integrates it as hard constraints. Brand Kit overrides industry-default colors and is a cross-skill consistency anchor shared with all peer product-shots skills.
- **Industry Visual DNA** is shared with `product-shots-social-post` and `product-shots` (cross-skill consistency).
- **Image generation backend**: rendered prompts are dispatched to `product-shots-image-gen` (the product-shots image-gen engine) which abstracts the underlying API (OmniMaaS / OpenAI / Gemini).
- **Adjacent boundary skills** (peers, not invoked from inside `product-shots-ad-creative`): `product-shots-social-post` (organic social content, no ad-objective layer), `product-shots-main-image` (Amazon-compliant product main image), `product-shots-detail-page` (Amazon A+ Content), `product-shots-multi-angle` (model-consistency portrait series).

## Tooling

- `product-shots` — invoked when any of the 7 required fields is missing (Quick Start gate).
- `product-shots-image-gen` — invoked at output assembly to actually generate images from the composed prompts.
- Brand Kit input (Step 2) — parsed directly from a user-provided file path or inline fields. No external tool call required.
