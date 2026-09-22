---
name: product-shots-multi-angle
description: 'Generates 9 consistent multi-angle fashion-editorial portraits from a single reference image, with locked identity (face/skin/eyes), preserved hairstyle structure, faithful outfit/accessories, and a unified photography style across all frames. Use when the user says "multi-angle", "multi-angle shots", "九连拍", "多角度九连拍", "9-angle portraits", "fashion lookbook", "model consistency series", "consistent portraits from one photo", "generate 9 angles of this model", or "e-commerce model multi-angle pack". Part of the product-shots ecosystem for cross-border e-commerce apparel and accessory listings.'
license: MIT
metadata:
  author: motiful
  source: product-shots ecosystem
  skill_id: product_shots_multi_angle
  version: "1.0"
persona: fashion editorial director specializing in multi-image model campaigns
---

# Multi-Angle

> **Persona** — *You are a fashion editorial director specializing in multi-image model campaigns.*

Produces a 9-image fashion-editorial series (the "Model Consistency Series") from a single user-uploaded reference photo. The skill extracts 14 controllable variables from the reference, presents 3 photography-style presets (Retro Analog Flash / Soft Muted Film / Hard Flash Editorial), then renders 9 task-prompt templates (one per image) with strict crop, pose, hairstyle, and style continuity rules so all 9 frames read as a single shoot.

This skill is part of the **product-shots** ecosystem — designed for cross-border e-commerce apparel, footwear, and accessory listings that need a coherent multi-angle lookbook from a single reference shot.

## Engagement Principles

These rules apply across every Section. Read before acting.

1. **Reference image is mandatory** — every image-generation call MUST pass `REFERENCE_IMAGE` as image input. Pure text descriptions are not allowed; identity consistency cannot be guaranteed without it.
2. **Analyse before generate** — extract all 14 variables from the reference image before filling any prompt. Never guess defaults, never skip extraction.
3. **Hairstyle structure is non-negotiable** — every prompt MUST include `{HAIRSTYLE} intact`, `NO loose hair`, `NO reinterpretation`. A tied / pinned / braided hairstyle in the reference must remain so across all 9 angles.
4. **Crop boundaries are hard constraints** — "framed to mid-thigh" means knees/lower legs/feet are forbidden in frame; "framed to chest" forbids the abdomen; "framed to hip line" forbids thighs. Treat each frame's crop as a verifiable rule, not a hint.
5. **Style is global** — the same `{PHOTOGRAPHY_STYLE}` block is repeated verbatim in every one of the 9 prompts. No image may look cleaner / more digital / higher-contrast than the others.
6. **Accessories follow the reference** — if the reference has accessories AND the crop reveals them → keep them; if the reference has none → never add them; if the crop excludes them → annotate with `where possible` or `No accessories — frame doesn't reach them`.
7. **Pause for style selection** — if the user has not specified a style and has not uploaded a style reference image, present the 3 presets via `<suggestion>` chips (do not auto-pick a default).
8. **Batch generate by default** — produce all 9 images in a single batch unless the user explicitly asks for stepwise review (avoids inter-call model drift).
9. **Match the user's language** — respond in the language the user writes in. Never switch unprompted.

## Execution Procedure

```
generate_multi_angle_series(user_request) → 9_images

# Step 0 — Pin hard constraints (MUST, before any decision)
load references/hard-constraints.md
    → Reference Image / Analyse-Before-Generate / Hairstyle Intact /
      Accessory Fidelity / Crop Boundaries / Style Unity / Override / Batch
keep these in working context for Steps 1-4 — violations break identity / hairstyle /
crop integrity which the validation views (Image 4 back, Image 8 side) cannot recover.

# Step 1 — Reference image gate + constraint pre-check
if user did NOT upload REFERENCE_IMAGE:
    abort with: "This skill requires a reference image to guarantee identity consistency.
                 Please upload a photo and retry."
    # NEVER fall back to text-only description.
# Pre-check RULE_001 + RULE_002 setup before extraction proceeds (extracted_vars
# + prompts + outputs are empty at this stage — call gates the workflow entry).
enforce_constraints(extracted_vars={}, prompts=[], outputs=[])
    → see references/hard-constraints.md §Execution Procedure (RULE_001 reference-image
      presence; later re-invoked at Step 5 with full payload).

# Step 2 — Extract 14 variables from reference (Vision pass)
extracted_vars = extract_variables(reference_image=REFERENCE_IMAGE)
    → see references/variables-and-workflow.md §Variable Extraction Specifications
    REQUIRED   = REFERENCE_IMAGE, HAIR_COLOR, HAIRSTYLE, SKIN_TONE, EYE_COLOR,
                 FACE_SHAPE, OUTFIT, BACKGROUND_COLOR, PHOTOGRAPHY_STYLE, ASPECT_RATIO
    OPTIONAL   = HAIR_ACCESSORIES, BAG, JEWELRY, OTHER_ACCESSORIES (default "none")
    if any required field cannot be extracted with confidence → ask the user to clarify
    (do NOT silently default).

# Step 3 — Photography style selection
# Inference sources (per variables-and-workflow.md §Style detection):
#   has_explicit_style_specification(user_request) → True if user_request
#     contains any keyword in STYLE_KEYWORDS_LIST (e.g., "retro", "flash",
#     "muted", "editorial", "soft", "analog")
#   has_style_reference_image(context) → True if context.attached_images
#     contains an image flagged role="style_reference" by the caller
selected_style = select_or_emit_presets(reference_image=REFERENCE_IMAGE,
                                        has_style_kw=has_explicit_style_specification(user_request))
    → see references/photography-style-presets.md §Execution Procedure
    # Returns chosen_style block verbatim OR pauses (emits 3 preset images +
    # 5 <suggestion> chips) and waits for user click. Never auto-picks a default.

# Step 4 — Fill 9 task-prompt templates (single batch)
image_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9]
prompts = fill_task_prompts(extracted_vars=extracted_vars,
                            selected_style=selected_style,
                            image_ids=image_ids)
    → see references/task-prompts.md §Execution Procedure
      + references/task-prompts-6-9.md (images 6-9)
    # Each prompt repeats the full {PHOTOGRAPHY_STYLE} block verbatim.
    # Each prompt re-asserts {HAIRSTYLE} intact + NO loose hair where applicable.

images = Skill("product-shots-image-gen",
               f"batch_generate: {len(prompts)} prompts | "
               f"reference_image={REFERENCE_IMAGE} | "
               f"model=gemini-3-pro-image-preview")
# Do NOT substitute with direct API call. product-shots-image-gen owns
# API-key resolution + reference-image preprocessing.
assert images.delivered and len(images) == 9

# Step 5 — Self-check gate (re-validate against hard-constraints)
enforce_constraints(extracted_vars=extracted_vars, prompts=prompts, outputs=images)
    → see references/hard-constraints.md §Execution Procedure (full 8-rule sweep)
critical checks (subset of RULE_003 / RULE_005 / RULE_006):
    - Image 4 (back view) — hairstyle structure visible from behind, no loose hair
    - Image 8 (side profile) — hairstyle structure visible from side, no loose hair
    - Image 5 (extreme close-up) — only eyes/nose/lips visible, no forehead/chin/shoulders
    - All 9 — same {PHOTOGRAPHY_STYLE} signature (lighting / shadow direction / grain)
if any check fails → regenerate the affected image(s)

# Step 6 — User overrides (re-render selectively)
on user override of any extracted variable:
    extracted_vars = apply_user_overrides(extracted_vars, user_overrides)
        → see references/variables-and-workflow.md §Variable Override Logic
        # Internally calls mark_affected_images_for_regeneration(variable_key):
        HAIRSTYLE / HAIR_COLOR / HAIR_ACCESSORIES → re-render images 1-9
        OUTFIT                                     → re-render 1, 2, 3, 4, 6, 7, 8, 9 (skip 5)
        BAG / JEWELRY                              → re-render 1, 2, 3, 6, 9 (in-frame ones)
        PHOTOGRAPHY_STYLE                          → re-render images 1-9
```

## TOC of Module Files

- `references/hard-constraints.md` — The 8 Rules (RULE_001-008) covering reference image, analysis-first, hairstyle intact, accessory fidelity, crop boundaries, style unity, override handling, batch generation. Loaded at EP Step 0, re-validated at EP Step 5.
- `references/variables-and-workflow.md` — Section 1 (14 input variables + extraction specs for HAIRSTYLE / OUTFIT / SKIN_TONE) + Section 3 (Workflow) + variable-override re-render logic.
- `references/photography-style-presets.md` — Section 2: the 3 presets (Retro Analog Flash / Soft Muted Film / Hard Flash Editorial) with verbatim lighting / shadow / film / colour / material specs, plus the style-selection output format (3 preset images + 5 `<suggestion>` chips).
- `references/task-prompts.md` — Section 4.1-4.5: Image 1 Three-Quarter Fashion Portrait through Image 5 Extreme Facial Close-Up. Each prompt template uses `{VARIABLE}` placeholders.
- `references/task-prompts-6-9.md` — Section 4.6-4.9: Image 6 Over-Right-Shoulder Glance through Image 9 Opposing Torso Twist. Split from `task-prompts.md` to keep both files under the 300-line cap.

## Section Index

```
1. Variables                                            → references/variables-and-workflow.md §Variables
   14 variables: REFERENCE_IMAGE, HAIR_COLOR, HAIRSTYLE, HAIR_ACCESSORIES,
   SKIN_TONE, EYE_COLOR, FACE_SHAPE, OUTFIT, BAG, JEWELRY, OTHER_ACCESSORIES,
   BACKGROUND_COLOR, PHOTOGRAPHY_STYLE, ASPECT_RATIO
2. Photography Style Presets                            → references/photography-style-presets.md
   2.1 Preset A — Retro Analog Flash
   2.2 Preset B — Soft Muted Film
   2.3 Preset C — Hard Flash Editorial
3. Workflow                                             → references/variables-and-workflow.md §Workflow
4. Task Prompts                                         → references/task-prompts.md (images 1-5)
                                                         + references/task-prompts-6-9.md (images 6-9)
   4.1 Image 1 — Three-Quarter Fashion Portrait              → task-prompts.md
   4.2 Image 2 — High-Angle Bird's-Eye View                  → task-prompts.md
   4.3 Image 3 — Over-the-Shoulder Close-Up                  → task-prompts.md
   4.4 Image 4 — Back View with Hairstyle Visible            → task-prompts.md
   4.5 Image 5 — Extreme Facial Close-Up                     → task-prompts.md
   4.6 Image 6 — Over-Right-Shoulder Glance                  → task-prompts-6-9.md
   4.7 Image 7 — Low-Angle Upward Gaze, Contrapposto         → task-prompts-6-9.md
   4.8 Image 8 — Side Profile, Chest Crop                    → task-prompts-6-9.md
   4.9 Image 9 — Medium Portrait, Opposing Torso Twist       → task-prompts-6-9.md
5. Rules                                                → references/hard-constraints.md
   8 rules: Identity / Workflow / Hair / Accessories / Crop / Style / Override / Batch
```

## Cross-Skill Notes

- This skill is invoked **only when the user explicitly requests multi-angle / 9-angle / model-consistency portraits**, typically for apparel, footwear, or accessory listings. Routed from `product-shots` when `asset_type ∈ {multi-angle, lookbook, model-series}`.
- `REFERENCE_IMAGE`-anchored identity locking is a pattern shared conceptually with `product-shots-main-image` and `product-shots-detail-page` (which anchor on the main product image instead of a model reference), but the three skills do not call each other.
- Photography-style preset images (3 hard-coded CDN URLs) are owned by this skill.
- Image generation is delegated to `product-shots-image-gen` (the product-shots image-gen engine) — this skill produces prompts and `reference_image` inputs; `product-shots-image-gen` calls the actual API.

## Tooling

The skill emits prompts + reference image binding. Actual image generation is invoked through `product-shots-image-gen` (the product-shots image-gen engine), or by any image-to-image–capable tool the host platform exposes. Vision-based variable extraction (Step 2) is invoked by the parent agent (Planner) using the rules and prompt templates produced here. The 9-image batch is rendered by passing `REFERENCE_IMAGE` as the reference input to the image-generation model and the filled task templates as text prompts.
