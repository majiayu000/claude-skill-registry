---
name: "Character Aging Progression"
description: "Generate visually consistent character images across different life stages using nano-banana-pro with age-specific prompts"
applyTo: "**/*aging*,**/*age-progression*,**/*life-stage*,**/*avatar*"
triggers:
  - "age progression"
  - "aging"
  - "make me older"
  - "make me younger"
  - "age me"
  - "years old"
  - "aging trifecta"
  - "face aging"
  - "nano-banana"
  - "life stages"
  - "generate age"
  - "create age"
---

# Character Aging Progression

> Create consistent character avatars from childhood through elderhood — maintaining identity while showing natural aging.

---

## Summary

Workflow for generating age-progression image sets that maintain character identity across 13 life stages (ages 3-75). Uses nano-banana-pro with reference face image for facial consistency plus age-specific descriptors for natural aging.

**Validated**: Alex avatar set — 13 ages × successful generations

---

## Life Stage Definitions

| Age | Stage | Key Visual Markers |
|-----|-------|-------------------|
| 3   | Early Childhood | Round face, large eyes relative to face, soft features |
| 7   | Middle Childhood | More defined features, baby fat reducing |
| 13  | Early Adolescence | Face lengthening, features sharpening |
| 15  | Mid Adolescence | Adult proportions emerging, youthful skin |
| 18  | Late Adolescence | Near-adult features, fresh complexion |
| 21  | Young Adult | Adult features fully formed, peak vitality |
| 25  | Established Adult | Features settled, confident bearing |
| 30  | Adult | Subtle maturity signs, professional demeanor |
| 42  | Middle Age | Fine lines beginning, distinguished look |
| 55  | Late Middle Age | Gray appearing, crow's feet, wisdom in eyes |
| 62  | Early Senior | More pronounced lines, fuller wisdom |
| 68  | Senior | Silver/white hair dominant, deep character lines |
| 75  | Elder | Weathered dignity, life experience visible |

---

## Implementation Pattern

### Model Selection

**Recommended**: `google/nano-banana-pro` — Best face consistency with reference image

```javascript
const AGES = [3, 7, 13, 15, 18, 21, 25, 30, 42, 55, 62, 68, 75];

async function generateAgeProgression(characterConfig, referenceImage) {
  const results = [];
  
  for (const age of AGES) {
    const prompt = buildAgePrompt(characterConfig, age);
    const result = await replicate.run("google/nano-banana-pro", {
      input: {
        prompt,
        image: await toDataURI(referenceImage),
        aspect_ratio: "1:1",
        output_format: "png"
      }
    });
    results.push({ age, url: result });
  }
  
  return results;
}
```

### Age-Specific Prompt Templates

```javascript
const AGE_DESCRIPTORS = {
  3: "3-year-old toddler, round chubby cheeks, large curious eyes, soft baby features, innocent expression",
  7: "7-year-old child, youthful face beginning to mature, bright curious eyes, playful yet thoughtful",
  13: "13-year-old teenager, face lengthening into adult proportions, youthful energy, intelligent gaze",
  15: "15-year-old teen, near-adult features emerging, fresh complexion, confident yet developing",
  18: "18-year-old young adult, adult features forming, youthful skin, mature confidence emerging",
  21: "21-year-old young professional, adult features fully formed, peak vitality, sharp intelligent eyes",
  25: "25-year-old adult, established features, confident bearing, professional demeanor",
  30: "30-year-old adult, subtle signs of maturity, experienced gaze, professional polish",
  42: "42-year-old, distinguished appearance, fine lines beginning, wisdom visible in eyes",
  55: "55-year-old, gray hair appearing at temples, crow's feet, dignified bearing, deep experience",
  62: "62-year-old senior, more pronounced lines, fuller silver hair, warm wise expression",
  68: "68-year-old, silver/white hair dominant, deep character lines, experienced wise gaze",
  75: "75-year-old elder, weathered dignified face, white hair, life experience visible, gentle wisdom"
};

function buildAgePrompt(character, age) {
  const baseDesc = character.coreIdentity;  // "Alex Finch, intelligent features, analytical eyes"
  const ageDesc = AGE_DESCRIPTORS[age];
  const style = character.style || "professional portrait, soft natural lighting, clean background";
  
  return `${baseDesc}, ${ageDesc}, ${style}`;
}
```

---

## Critical Success Factors

### 1. Core Identity Markers (Constant)

Define 3-5 unchanging traits that persist across all ages:
- Eye color and shape
- Facial structure (bone structure)
- Distinctive features (e.g., dimples, nose shape)
- Expression tendencies

```javascript
const CHARACTER = {
  coreIdentity: "Alex Finch, sharp intelligent features, " +
    "distinctive analytical eyes, determined jawline, " +
    "characteristic half-smile",
  // These traits appear in EVERY age prompt
};
```

### 2. Age-Appropriate Styling

Avoid anachronisms — match style to age:
- Children: Casual, age-appropriate clothing
- Teens: Contemporary teen fashion
- Adults: Professional attire
- Seniors: Dignified, comfortable styling

### 3. Reference Image Selection

Choose a reference that shows:
- Clear facial features at neutral angle
- Good lighting without harsh shadows
- Direct or 3/4 view (not profile)
- Age 18-30 works best as reference anchor

---

## Cost Analysis

| Set Size | Model | Cost | Time |
|----------|-------|------|------|
| 13 ages | nano-banana-pro | $0.33 | ~7 min |
| 13 ages × 2 variants | nano-banana-pro | $0.65 | ~14 min |
| Full persona set (63) | nano-banana-pro | $1.58 | ~35 min |

**Best Practice**: Generate ages 21 and 42 first to validate consistency before full set.

---

## Quality Validation

### Consistency Check

Compare across ages for:
1. **Eye consistency** — Same eye color/shape throughout
2. **Feature evolution** — Natural progression, not jarring changes
3. **Identity preservation** — Recognizably same person at all ages

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Age jump too drastic | Age descriptors too different | Add intermediate transition language |
| Baby/child looks different | Reference face too adult | Use neutral young adult reference |
| Senior unrecognizable | Too much aging description | Reduce weathering descriptors |

---

## File Organization

```
characters/
  {character-name}/
    reference/
      face-reference.png
    ages/
      Alex-03.png
      Alex-07.png
      ...
      Alex-75.png
    generation-report.json
```

---

## Integration with Avatar System

Alex's avatar system uses age progression for:
1. **Birthday fallback** — Show user's age-matched Alex
2. **Persona defaults** — Age 21 is default when no persona detected
3. **Age-appropriate identity** — Users see Alex at their life stage

```typescript
// From avatarMappings.ts
export const AVAILABLE_AGES = [3, 7, 13, 15, 18, 21, 25, 30, 42, 55, 62, 68, 75];

export function findClosestAge(age: number): number {
  // Returns nearest available age from set
}
```

---

## Confidence Level

**High** — Empirically validated through:
- 13 age images generated for Alex character
- Consistent identity across full progression
- 768×768 optimized avatars deployed
- User birthday → age avatar mapping working
