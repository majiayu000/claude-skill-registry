---
name: broll-prompting
description: Generate detailed AI image prompts for YouTube video B-roll using Imagen. Creates premium, sophisticated visuals for talking head videos targeting 30+ business owners.
---

# B-Roll Prompting for YouTube Videos

Generate comprehensive Imagen prompts for **static helper images** supporting talking head videos.

## Target Audience

**30+ year old business owners.**

This means:
- Professional, not playful
- Sophisticated, not trendy
- Clear, not clever
- Premium, not busy

---

## Visual Style: Premium Minimal

**Think:** Luxury car ad, Apple keynote, McKinsey slide.

**NOT:** Pixel art, Excalidraw sketches, blueprint grids, clip art.

### Core Elements

| Element | Treatment |
|---------|-----------|
| Background | Clean solid dark gradient, NO patterns |
| Main elements | Soft silver-white silhouettes/icons |
| Accents | Warm gold for emphasis and flow |
| Space | Generous negative space |
| Depth | Subtle shadows and glows |

### Color Palette

| Element | Hex |
|---------|-----|
| Background (top) | #1e2432 |
| Background (bottom) | #171c26 |
| Primary elements | #e8eaed |
| Secondary detail | #c5c8cc |
| Tertiary | #b8bcc2 |
| Shadows | #0d1117 at 30-40% |
| Accent (gold) | #c9a86c |
| Accent glow | #c9a86c at 8-12% |

---

## Prompt Requirements

Every prompt must be **500-1500 words** with these sections:

### 1. BACKGROUND
Exact colors, gradient direction, explicit "NO grid, NO texture, NO patterns"

### 2. COMPOSITION
Layout, spacing percentages, positioning, frame usage

### 3. EACH ELEMENT
- What it represents (be SPECIFIC - not "a car" but "BMW 650i E64 Convertible")
- Key shape characteristics that make it recognizable
- Size relative to other elements
- Color with hex code
- Shadows/glows

### 4. CONNECTING ELEMENTS
Arrow style, weight, color, position

### 5. FOCAL POINT
What draws the eye, how it's emphasized

### 6. VISUAL NARRATIVE
What story does this tell? How should the eye flow?

### 7. MOOD
What it should feel like / NOT feel like

### 8. COLOR SUMMARY
All hex codes listed

### 9. DIMENSIONS
1920x1080px

### 10. TEXT LABELS (where applicable)
Short labels identifying elements (e.g., "320i GT", "$5M", "VS", "10 Results")
- Font style, size, color, position

### 11. AVOID
Comprehensive list - be thorough

---

## Example: Car Timeline Prompt

```
Elegant minimal timeline illustration showing a three-stage car ownership journey, presented as a sophisticated horizontal progression from left to right against a clean dark background. The sequence shows: BMW 320i Gran Turismo → BMW 650i E64 Convertible → BMW Z4 Roadster → ? (unknown next car).

BACKGROUND:
Solid deep navy-charcoal gradient (#1e2432 at top transitioning subtly to #171c26 at bottom). NO grid lines, NO texture, NO patterns. The background should be completely clean and uncluttered, allowing the car silhouettes to be the sole focus. This solid dark backdrop creates a premium, automotive showroom feeling.

COMPOSITION:
Horizontal layout occupying the middle horizontal band of the frame. Three car silhouettes arranged left to right with generous, equal spacing - approximately 20-25% of frame width between each. All cars sit on the same invisible baseline, roughly centered vertically (around 45% from top). The arrangement should feel balanced and breathable.

SIZE PROGRESSION:
- Car 1 (320i GT): Medium-large, elevated stance
- Car 2 (650i): Largest - long and wide grand tourer
- Car 3 (Z4): Noticeably SMALLER and LOWER - compact sports car

CAR 1 - BMW 320i Gran Turismo:
Side profile facing right. NOT a standard sedan - the GT has a distinctive fastback/liftback profile.

Key characteristics:
- Extended wheelbase
- Raised rear roofline flowing into fastback tail
- Continuous slope to lifted tailgate (not sedan trunk drop-off)
- Four doors with Hofmeister kink at C-pillar
- Higher ride height than standard sedan

Soft silver-white (#e8eaed) solid fill. Subtle window tint (#c5c8cc). Wheels in #b8bcc2. Soft ground shadow (#0d1117 at 30-40%).

CAR 2 - BMW 650i E64 Convertible:
Side profile facing right, soft top DOWN. 2004-2010 6 Series grand touring convertible.

Key characteristics:
- Long, sweeping hood (front-engine V8 GT)
- Large two-door body - significantly larger than a compact roadster
- Open-top profile showing low windshield rake and folded soft top
- Short rear deck with upward kick
- Wider, more muscular stance

LARGEST silhouette of the three. Same color treatments.

CAR 3 - BMW Z4 Roadster:
Side profile facing right, top DOWN. Compact two-seat sports car.

Key characteristics:
- Dramatically long hood relative to tiny cabin
- Very short rear overhang
- Cabin positioned far back toward rear axle
- Low, aggressive stance - LOWER than both previous cars
- "Shark nose" front profile
- Pronounced rear haunches

Visibly MORE COMPACT than 650i. Same color treatments.

CONNECTING ARROWS:
Between each car: thin horizontal line (~2px) with subtle chevron arrowhead.
- Color: Warm gold (#c9a86c)
- Length: ~60-80px
- Vertically aligned with car centers

QUESTION MARK:
After final arrow.
- Size: 80-100px tall
- Color: Warm gold (#c9a86c)
- Style: Clean sans-serif
- Subtle glow: #c9a86c at 8-12% opacity

VISUAL NARRATIVE:
Progression tells story: practical GT → luxury convertible → pure sports car → ???
Size differences and body evolution readable without labels.

MOOD:
Premium, sophisticated, minimal, intriguing. Luxury automotive brand feel.
NOT: Car dealership flyer, blueprint, clip art, children's illustration.

COLOR SUMMARY:
- Background: #1e2432 to #171c26
- Cars: #e8eaed
- Windows: #c5c8cc
- Wheels: #b8bcc2
- Shadows: #0d1117 at 30-40%
- Gold accents: #c9a86c

DIMENSIONS: 1920x1080px

AVOID:
- Grid lines, blueprint elements
- Brand logos or badges
- Excessive detail (door handles, mirrors)
- Same size for all cars
- Pure white (#ffffff)
- Text or labels
- Gradients on car bodies
- 3D perspective
- Photorealistic rendering
- Cartoon/sketch styles
- Busy backgrounds
- Heavy arrows
- Closed roofs on convertibles
```

---

## Visual Categories

| Type | Description |
|------|-------------|
| **Timeline** | Progression left to right with arrows |
| **Comparison** | Split composition showing A vs B |
| **Data** | Charts, growth indicators (minimal, no labels) |
| **Concept** | Abstract ideas as visual metaphors |
| **Process** | Sequential steps, numbered/connected |
| **UI Mockup** | Simplified interfaces (not screenshots) |

---

## Key Rules

1. **Be extremely specific** - "BMW 650i E64" not "a car"
2. **500-1500 words per prompt** - if shorter, not detailed enough
3. **No pixel art, Excalidraw, or blueprints** - wrong for 30+ business owners
4. **Clean dark background + gold accents** - signature style
5. **Premium automotive/editorial aesthetic** - luxury brand feel
6. **Include AVOID section** - prevent unwanted elements
7. **Text IS allowed** - Imagen 3 handles text well. Use short labels (car names, numbers, "VS") not sentences

---

## Output Format

```markdown
# B-Roll Prompts: [Video Title]

**Target Audience:** 30+ business owners
**Visual Style:** Premium minimal
**Dimensions:** All 1920x1080px

---

## Summary

| # | Visual | Type | Timestamp |
|---|--------|------|-----------|
| 01 | [Name] | [Type] | 0:30 |

---

## BROLL-01: [Name]

**Timestamp:** 0:30
**Supports:** "[Script quote]"
**Purpose:** [What this accomplishes]

### Prompt:

[Full 500-1500 word prompt]

---
```
