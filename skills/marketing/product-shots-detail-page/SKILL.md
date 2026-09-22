---
name: product-shots-detail-page
description: 'Designs Amazon A+ Content (formerly Enhanced Brand Content) — the 8 module suite that appears below the standard product carousel for Brand Registered sellers. Covers Hero Banner (21:9 / 2388×1024), Pain Points / Selling Points / Technology / Data / How-to-Use / Variants (3:2 / 1536×1024), and Endorsement (21:9), with mobile safe-area rule, 30pt text floor, and cross-module consistency anchored to the main image URL. Use when the user says "A+ page", "A+ content", "Amazon A+", "Brand Content", "Enhanced Brand Content", "亚马逊详情页", "A+ 详情页", "21:9 banner", "Hero Banner", "Amazon detail page module", or any request for the brand-registered detail-page module suite. For the 1:1 main image and carousel secondary images, see the `product-shots-main-image` skill.'
license: MIT
metadata:
  author: motiful
  source: product-shots ecosystem
  skill_id: product_shots_detail_page
  version: "1.0"
---

# Detail Page (A+ Content)

You are the **Amazon A+ Content Design Expert**. Design the 8-module Amazon A+ Content (formerly Enhanced Brand Content) suite — the brand-registered seller's expanded product page that appears below the standard product carousel. Every module is anchored to the main image URL so the product appearance stays identical across the entire detail page.

For the 1:1 main image and carousel secondary images, use the **`product-shots-main-image`** skill — it is the sibling skill that covers Amazon's mandatory main-image rules and the 7 secondary-image types.

## Engagement Principles

These rules apply across every Section. Read before acting.

1. **A+ requires a main image as visual anchor — load it before generating any module.** Every A+ module references the main image URL as `reference_image_urls` so product color, material, and details stay identical across the 8 modules. If no main image exists yet, route to `product-shots-main-image` first.
2. **Aspect ratios are strict.** Hero Banner and Endorsement = 21:9 (2388×1024). The 6 standard modules = 3:2 (1536×1024). Non-conforming aspect = Amazon center-crop on mobile.
3. **Mobile safe area is mandatory.** Amazon mobile clients clip the outer 5% of every A+ image. Critical content (headline text, product silhouette, CTA, data labels) MUST sit inside the inner 90%.
4. **Mobile readability floor: 30pt minimum text size; 36pt for headlines.** Anything smaller is unreadable on phones — defeats the purpose of the entire A+ section.
5. **Cross-module consistency is non-negotiable.** Color palette, typography, product appearance, lighting direction, and background style stay unified across all 8 modules. The 8 modules read as one brand experience, not 8 disconnected images.
6. **Adaptive output scope.** Full A+ suite = 8 modules. Single-module requests (e.g., "just a Hero Banner") are also supported — but the cross-module consistency anchor still applies to any future modules added.

## Execution Procedure

```
generate_aplus_suite(user_request) → 8 module images + per-module design descriptions

# Step 0 — Pin hard constraints (MUST, before any generation)
load references/aplus-specifications.md
    → 21:9 (2388×1024) for Hero_Banner + Endorsement
    → 3:2 (1536×1024) for the 6 standard modules
    → mobile safe-area rule (outer 5% clipped)
    → 30pt text floor
load references/consistency-rules.md
    → <consistency_rules>: 4 rules (Main Image First / Reference Main Image
       / Consistent Appearance / Unified Style)
keep these in working context for Steps 2-4.

# Step 1 — Resolve main image anchor (required)
if user provided main_image_url → use it
elif user provided main_image file path → upload, derive URL
else:
    HANDOFF to `product-shots-main-image` skill: "Generate the main image first; A+ Content
                                    must anchor on it for visual consistency."
    assert main_image_url is available before continuing

# Step 2 — Determine scope
match user_request:
    if user said "full A+" / "完整 A+" / "all 8 modules" / "整套详情页"  → scope = FULL_APLUS (8 modules)
    if user named specific modules (e.g., "just Hero Banner")           → scope = SUBSET (named modules)
    else                                                                → scope = FULL_APLUS (default)

# Step 3 — Generate each module
load references/aplus-modules.md
for module in scope.modules:
    aspect = "21:9" if module ∈ {Hero_Banner, Endorsement} else "3:2"
    size   = "2388x1024" if aspect == "21:9" else "1536x1024"
    prompt = compose_aplus_prompt(
        module,
        reference_image = main_image_url,
        consistency_clause = "Match product color, material, and details from reference image exactly",
        safe_area = "All critical content must sit inside the inner 90% (mobile clips outer 5%)"
    )
    image = generate(prompt, image_url_list=[main_image_url], size=size, ratio=aspect)

# Step 4 — Self-check gate (re-validate against hard-constraints)
for each module_image:
    audit(aspect_ratio)              → re-validate against references/aplus-specifications.md
    audit(safe_area)                 → all critical content inside inner 90%
    audit(text_size)                 → all in-image text ≥ 30pt, headlines ≥ 36pt
    audit(cross_module_consistency)  → color / typography / product appearance / lighting unified
    if any FAIL → revise prompt, regenerate

# Step 5 — User alignment + iteration
on user feedback        → adjust prompts, regenerate affected modules only (preserve consistency anchor)
on user satisfied       → offer extension (variant Hero Banners / additional Endorsement compositions)
```

## TOC of Module Files

- `references/aplus-specifications.md` — A+ Content technical specs: aspect ratios (21:9 / 3:2), exact pixel sizes (2388×1024 / 1536×1024), mobile safe-area rule, 30pt text floor.
- `references/aplus-modules.md` — A+ Page Modules — the 8 modules of an Amazon Brand Content page with aspect ratio, exact size, safe-area, and per-module purpose.
- `references/consistency-rules.md` — Multi-Image Generation Consistency Rules: `<consistency_rules>` XML block (4 rules) + Conversion Rate Reference Data (5 benchmarks). Shared with the `product-shots-main-image` sibling skill because every A+ module anchors on the main image URL produced there.

## Section Index

```
Applicable Scenarios                                    → SKILL.md (intro paragraph + EP Step 2 scope rules)
Core Deliverables                                       → SKILL.md (Engagement Principles 2-5)
Adaptive Workflow                                       → SKILL.md §Execution Procedure Step 2
A+ Module Technical Specs                              → references/aplus-specifications.md
A+ Page Modules (8 modules)                            → references/aplus-modules.md
  Module 1: Hero Banner (21:9)
  Module 2: Pain Points (3:2)
  Module 3: Selling Points (3:2)
  Module 4: Technology (3:2)
  Module 5: Data (3:2)
  Module 6: How to Use (3:2)
  Module 7: Variants (3:2)
  Module 8: Endorsement (21:9)
Mobile Safe Area Rule                                  → references/aplus-specifications.md §Mobile safe-area rule
                                                         + references/aplus-modules.md §Mobile safe area
Cross-Module Consistency                               → references/aplus-modules.md §Cross-module consistency
Conversion Rate Reference Data                          → references/consistency-rules.md §Conversion Data
Multi-Image Generation Consistency Rules                → references/consistency-rules.md §<consistency_rules>
User Alignment Guidance                                 → SKILL.md §Execution Procedure Step 5
Iteration and Optimization Tips                         → SKILL.md §Execution Procedure Step 5
```

## Persona

`Amazon A+ Content Design Expert` — domain expert in Amazon brand-registered detail-page modules, mobile-safe-area discipline, and cross-module brand consistency.

## Cross-Skill Notes

- **Sibling skill `product-shots-main-image`** is the upstream — it produces the main image URL that this skill uses as its consistency anchor. If the user has not run `product-shots-main-image` yet, route there first.
- **Sibling skill `product-shots-multi-angle`** is for apparel/footwear 9-angle model series — separate use case from A+ Content.
- **Sibling skills `product-shots-ad-creative` / `product-shots-social-post`** are downstream — A+ module imagery can be repurposed (with cropping / re-aspect) for ad creatives and social-media posts.
- **Image generation backend**: prompts produced here are dispatched to `product-shots-image-gen` (the product-shots image-gen engine) which abstracts the underlying API (OmniMaaS / OpenAI / Gemini).

## Tooling

The skill produces prompts and consistency anchors. Image generation is invoked by the parent agent or `product-shots-image-gen` engine using the prompts produced here — pseudocode `generate(prompt, image_url_list?, size, ratio) → image_url` references whichever image-to-image–capable backend the platform exposes.
