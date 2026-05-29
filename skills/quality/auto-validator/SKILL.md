---
name: auto-validator
description: Programmatic asset compliance validation using vision analysis and Northcote scorecard. Eliminates manual validation loops—upload image, receive scored JSON with correction prompts in 30 seconds.
---

# Auto-Validator Skill

## Purpose

Automates Northcote Curio asset validation. Upload generated image → receive compliance JSON with scores, violations, and auto-generated correction prompt. Replaces 10-minute conversational validation with 30-second programmatic assessment.

## Trigger Conditions

Use when:
- Gemini/DALL-E generates asset attempt
- Need compliance score (0-100 across 6 dimensions)
- Require iteration decision (≥90 package | <90 regenerate)
- Want correction prompt for next attempt

## Validation Scorecard

**Dimension 1: Geographic Authenticity (0-20)**
- All specimens Australian endemic
- Test: "Did organism challenge European taxonomy?"
- Violations: Non-Australian fauna, generic specimens

**Dimension 2: Translucency Physics (0-20)**
- Light transmission (not glow) visible
- Internal structures shown through material
- Percentage compliance: 60-80% molt, 40-60% membrane, 20-40% leaves

**Dimension 3: Scale Hierarchy (0-20)**
- PRIMARY 1.5-2× SECONDARY
- SECONDARY 2-3× TERTIARY
- Clear focal points established

**Dimension 4: Density Zones (0-20)**
- Upper-left ≤20% coverage, 200×200px empty
- Lower-right ≤30% coverage, 150×150px empty
- Central 60-80% Wunderkammer density

**Dimension 5: Background Color (0-10)**
- Target: #1A1714 ±5% tolerance
- No sepia/brown drift
- Theatrical void maintained

**Dimension 6: Typography (0-10)**
- Serif font (Crimson Text style)
- Cream #F5F0E8 at 85% opacity
- 5-6 labels maximum
- Format: "Fig. X. Scientific name (Common)"

## Workflow

**Input:** Image file path or upload
**Process:**
1. Extract hex colors (sample 50 points)
2. Identify specimens (Vision API recognition)
3. Measure density zones (pixel coverage analysis)
4. Detect translucency (luminance gradient detection)
5. Count/validate typography (OCR)
6. Score each dimension
7. Generate violation list
8. Build correction prompt

**Output:** JSON structure

```json
{
  "asset_id": "ASSET-3",
  "overall_score": 87,
  "decision": "REGENERATE | PACKAGE",
  "dimensions": {
    "geographic_authenticity": {"score": 18, "violations": []},
    "translucency_physics": {"score": 14, "violations": ["Spider molt opaque"]},
    "scale_hierarchy": {"score": 19, "violations": []},
    "density_zones": {"score": 16, "violations": ["Upper-left 25%"]},
    "background_color": {"score": 9, "violations": []},
    "typography": {"score": 8, "violations": ["7 labels (max 6)"]}
  },
  "correction_prompt": "CRITICAL FIXES:\n- Spider molt: Add '60-80% light-transmissive amber chitin'\n- Upper-left: Specify '200×200px COMPLETELY EMPTY'\n- Reduce annotations to 5 labels",
  "iteration_priority": "high"
}
```

## Integration Points

**With Flash-Sidekick:**
- Call `analyze_code_quality` on generated prompt → identify vague language
- Call `web_research_synthesis` for specimen geographic validation

**With Gemini:**
- Auto-validator output → correction_prompt → paste directly into next generation

**With Claude Desktop:**
- Decision gate: score ≥90 triggers Asset-Packager skill
- Score <90 triggers Prompt-Composer with corrections

## Usage Example

```python
# Pseudo-workflow
result = auto_validator.validate(
    image_path="/downloads/asset-3-attempt-2.png",
    asset_id="ASSET-3",
    target_score=90
)

if result['decision'] == 'PACKAGE':
    asset_packager.run(result)
else:
    corrected_prompt = prompt_composer.apply_corrections(
        base_prompt=original_prompt,
        corrections=result['correction_prompt']
    )
    # Send to Gemini for regeneration
```

## Efficiency Gain

**Before:** 10-15 min manual validation per attempt
**After:** 30 sec programmatic validation
**Savings:** 20× faster validation, 95% time reduction
**Scale Impact:** 10 assets × 2-3 attempts = 3-5 hours saved

## Implementation Notes

- Vision API for specimen identification + color extraction
- Pixel density analysis for zone coverage
- Luminance gradient detection for translucency validation
- OCR for typography verification
- Deterministic scoring (not subjective)

---

*Replaces conversational validation with programmatic compliance measurement. Critical path acceleration for high-volume asset generation.*
