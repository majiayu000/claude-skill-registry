---
name: visual-content
description: Use when creating branded presentations or carousels. Generates museum-quality visual output from canvas philosophy, enforcing style constraints. Outputs PDF first, then converts to PPTX for editability.
version: 3.1.0
allowed-tools: Read, Write, Glob, Bash
user-invocable: false
---

# Visual Content Skill

Create gallery-quality branded presentations and carousels through artistic design philosophy.

## The Critical Understanding

Visual content creation is an act of **artistic expression**, not template filling. Every slide or card should appear as if crafted by a designer at the absolute top of their field—meticulous, intentional, worthy of display.

**What you receive**: A canvas philosophy and brand DNA—use these as foundation, not constraint.
**What you create**: Visual artifacts that are 90% design, 10% essential text.
**The standard**: Work that looks like it took countless hours, labored over with painstaking care.

---

## Part 1: Understanding Canvas Philosophy

A canvas philosophy is not a layout specification—it's an **aesthetic movement**, a manifesto for how ideas become visual form.

### How to Read a Canvas Philosophy

When you receive a `canvas-philosophy.md`, internalize its spirit:

- **The movement name** tells you the soul: "Chromatic Silence" demands restraint; "Brutalist Joy" permits boldness
- **The philosophy paragraphs** describe how ideas manifest through form, space, color, composition
- **The constraints** are sacred boundaries that define the style's character

**Read it as an artist reads a creative brief—absorb the worldview, then express it.**

### Philosophy Examples (for reference)

These illustrate the language and depth expected in a canvas philosophy:

**"Concrete Poetry"**
Communication through monumental form and bold geometry. Massive color blocks, sculptural typography (huge single words, tiny labels), Brutalist spatial divisions. Ideas expressed through visual weight and spatial tension, not explanation. Text as rare, powerful gesture—never paragraphs, only essential words integrated into visual architecture. Every element placed with the precision of a master craftsman who has labored over each decision.

**"Chromatic Language"**
Color as the primary information system. Geometric precision where color zones create meaning. Typography minimal—small sans-serif labels letting chromatic fields communicate. Information encoded spatially and chromatically. Words only anchor what color already shows. The result of painstaking chromatic calibration by someone at the top of their field.

**"Analog Meditation"**
Quiet visual contemplation through texture and breathing room. Paper grain, ink bleeds, vast negative space. Photography and illustration dominate. Typography whispered (small, restrained, serving the visual). Images breathe across pages. Text appears sparingly—short phrases, never explanatory blocks. Each composition balanced with the care of a meditation practice, meticulously crafted over countless hours.

**"Geometric Silence"**
Pure order and restraint. Grid-based precision, bold photography or stark graphics, dramatic negative space. Typography precise but minimal—small essential text, large quiet zones. Swiss formalism meets Brutalist material honesty. Structure communicates, not words. Every alignment the work of countless refinements by an expert hand.

---

## Part 2: The Subtle Reference

**CRITICAL STEP**: Before creating visuals, identify the conceptual thread from the content.

The topic becomes a **subtle, niche reference embedded within the design itself**—not literal, always sophisticated. Someone familiar with the subject should feel it intuitively, while others simply experience a masterful composition.

Think like a jazz musician quoting another song—only those who know will catch it, but everyone appreciates the music.

The canvas philosophy provides the aesthetic language. The content provides the soul—the quiet conceptual DNA woven invisibly into form, color, and composition.

---

## Part 2b: Brand Personality Loading

Before creating visuals, check `brand-philosophy.md` for `## Brand Depth` > `### Personality (Aaker Framework)`:

**If present and populated**: Read the Aaker scores and primary/secondary dimensions. Store in working context — these inform component decisions (Part 7), color intensity (Part 4), and spatial choices throughout.

**If not present**: Read voice traits from `## Verbal Identity` > `### Voice Personality`. Map to Aaker dimensions using proximity:
- precise, reliable, expert, professional → **Competence**
- warm, friendly, approachable, genuine → **Sincerity**
- bold, innovative, daring, creative → **Excitement**
- elegant, refined, luxurious, polished → **Sophistication**
- rugged, authentic, tough, adventurous → **Ruggedness**

Also check for `### Spatial & Surface Profile` — if present, use its values (spacing rhythm, border radius, shadow style, layout density) to inform element placement and styling decisions.

---

## Part 3: Visual Expression

With philosophy internalized and conceptual thread identified, create the visual artifacts.

### Composition Rules Application (MANDATORY)

Before laying out ANY slide, follow this structural process:

1. **Identify slide type** — Title, Content, Image, Data/Chart, Quote, CTA, or Transition
2. **Look up focal point** — From the Composition Rules section of canvas-philosophy.md (or from `references/slide-composition-rules.md` if missing)
3. **Place focal element FIRST** — The primary visual anchor goes in position before anything else
4. **Apply style modifier** — Adjust position based on the style's layout rules (centered, asymmetric, grid, flowing)
5. **Check component frequency** — Before adding cards/icons/gradients, check if within budget across all slides
6. **Verify density** — Max 3 visual layers. No element collisions. 24px minimum spacing.

**Fallback**: If the canvas-philosophy.md does not include a Composition Rules section (legacy templates), use the defaults from `references/slide-composition-rules.md` with the style's modifiers applied.

### The Craftsmanship Standard

**CRITICAL**: To achieve human-crafted quality (not AI-generated), create work that looks like it took countless hours. Make it appear as though someone at the absolute top of their field labored over every detail with painstaking care.

Ensure the composition, spacing, color choices, typography—everything screams **expert-level craftsmanship**. This is non-negotiable.

Repeat this mantra:
- Meticulously crafted
- The product of deep expertise
- Painstaking attention to detail
- Master-level execution
- Labored over with care

### Creating Presentations (16:9)

- **Dimensions**: 1920 x 1080 pixels
- **Format**: PDF first (source of truth) → PPTX (for editability)
- **Character**: Each slide = one clear message (3-second test)
- **Text treatment**: Sparse, integrated as visual element—never paragraphs
- **Safe zones**: Nothing within 50px of edges

**The slide is a canvas, not a document.** Information lives in design choices: scale, position, color, whitespace. Words are visual accents, not content delivery.

### Creating Carousels (Mobile-First)

- **LinkedIn**: 1080 x 1350 (4:5 portrait)
- **Instagram Square**: 1080 x 1080 (1:1)
- **Instagram Portrait**: 1080 x 1350 (4:5)
- **Format**: Multi-page PDF
- **Character**: Each card = 2-second comprehension (thumb-stopping)
- **Text treatment**: Bold, scannable, commanding

**The card is a poster glimpsed while scrolling.** It must arrest attention instantly through visual impact, not dense information.

### Style Enforcement

Each piece must respect its style's **hard constraints**:

| Constraint | Purpose |
|------------|---------|
| Whitespace % | Defines the breathing room—the silence between notes |
| Word limit | Forces economy—every word must earn its place |
| Element count | Prevents visual noise—simplicity is sophistication |
| Layout rules | Establishes spatial grammar—centered, asymmetric, grid |
| Typography weight | Sets the voice—whispered, conversational, commanding |

**If content exceeds constraints, reduce. Never violate the style. The constraints ARE the style.**

---

## Part 4: Execution Principles

### Visual Hierarchy

```
1. Single focal point per slide/card—the eye knows where to land
2. Clear reading order (F-pattern or Z-pattern)—the journey is intuitive
3. Contrast guides attention—importance is visible
4. Nothing competes with the message—supporting elements support
```

### Typography as Visual Element

```
- Headlines: Bold, commanding, minimal—a single powerful statement
- Body: Avoid entirely when possible—if you must, keep it whispered
- Numbers: Large, prominent, contextualized—let data be visual
- Labels: Small, quiet, supportive—they annotate, not explain
```

**Text is always minimal and visual-first.** Let context guide whether that means whisper-quiet labels or bold typographic gestures. A pitch deck might have larger, more aggressive type than a meditation app. Regardless of approach, sophistication is non-negotiable.

### Color Application

```
- Use brand palette or selected alternative palette exclusively
- Primary: 60% of color usage—the dominant voice
- Secondary: 30% of color usage—the supporting harmony
- Accent: 10% for emphasis only—the punctuation
- Never introduce off-brand colors—consistency builds trust
```

**Personality-informed intensity** (from Part 2b):
- **Excitement** → Push toward vibrant saturation, bolder color blocks, higher contrast accents
- **Sophistication** → Pull toward muted/desaturated application, restrained accent use
- **Sincerity** → Favor warm, accessible mid-saturation tones
- **Competence** → Clean, systematic color application with clear hierarchy
- **Ruggedness** → Deep earthy values, textured color application

### Spatial Communication

```
- Whitespace is not empty—it's active, meaningful silence
- Placement carries meaning—center = importance, edges = supporting
- Proportion creates rhythm—vary scale intentionally
- Margins are sacred—nothing touches edges, nothing overlaps
```

---

## Part 5: Anti-Patterns (Death to These)

- **Bullet point lists**: The death of visual communication
- **Wall of text**: Violates the 3-second rule, breaks the visual contract
- **Clip art or stock clichés**: Instant amateur signal
- **Competing focal points**: Confusion disguised as richness
- **Decoration without purpose**: If it doesn't serve the message, delete it
- **Violating whitespace minimums**: Cramped = desperate
- **Exceeding word limits**: Discipline defines mastery
- **Generic template feel**: The opposite of everything we're doing

---

## Part 6: The Final Polish

**IMPORTANT**: Before declaring done, assume the user already said: "It isn't perfect enough. It must be pristine, a masterpiece of craftsmanship, as if it were about to be displayed in a museum."

**CRITICAL**: To refine the work, avoid adding more elements. Instead, refine what exists and make it extremely crisp. Rather than adding a new graphic or changing a font, ask: **"How can I make what's already here more of a piece of art?"**

Take a second pass:
- Check every alignment
- Verify every spacing decision
- Confirm nothing overlaps
- Ensure breathing room between all elements
- Polish until it gleams

---

## Part 6b: Accessibility & Safety (MANDATORY)

**These checks are NON-NEGOTIABLE before any output is finalized.**

### Contrast Validation (WCAG AA)

| Requirement | Value |
|-------------|-------|
| Minimum contrast ratio | **4.5:1** for all text |
| Large text (24px+) | 3:1 acceptable |
| Standard | WCAG 2.1 AA |

**Before rendering ANY text:**
1. Calculate contrast ratio between text color and background
2. If ratio < 4.5:1, auto-fix with safe alternative (white on dark, near-black on light)
3. Log warning if auto-fix was needed

See `references/technical-implementation.md` → "Accessibility & Safety Checks" for `validate_contrast()` code.

### No Overlap Rule (ABSOLUTE)

**Text elements MUST NEVER overlap.** This includes:
- Text on text
- Text on logos
- Text on icons
- Text bleeding into margins

**Before placing ANY element:**
1. Calculate bounding box (position + dimensions)
2. Check against all existing elements for collision
3. Check against safe zone margins
4. If collision detected → STOP and adjust position or reduce content

### Safe Zone Enforcement

| Format | Margin | Safe Area |
|--------|--------|-----------|
| Presentation (1920×1080) | 50px | 1820×980 usable |
| Carousel (1080×1350) | 54px (5%) | 972×1242 usable |

**Nothing may cross these boundaries:**
- No text
- No logos (except intentional bleed designs)
- No icons
- No cards

### Gradient Text Safety

When text appears on gradients:
- Test contrast at **BOTH ends** of the gradient
- Minimum 4.5:1 at the **lowest contrast point**
- If fail: add semi-transparent backing behind text OR use text shadow

### Pre-Render Checklist (EVERY slide/card)

```
□ All text passes 4.5:1 contrast check
□ No elements overlap
□ All elements within safe zone
□ Word count within style limit
□ Element count within style limit
□ Gradient text readable at both ends (if applicable)
```

**If ANY check fails, DO NOT render. Fix the issue first.**

---

## Part 7: Visual Components (Optional)

Some styles support visual components that enhance the design. **Components are opt-in** (user enables during template creation) **but should be used intelligently** based on content—not on every slide just because they're enabled.

### Component Decision Gates (MANDATORY)

Before using ANY visual component on a slide, pass through these gates IN ORDER:

**Gate 1: Style Permission**
Does the selected style allow this component? (Check style-constraints.md or enforcement block)
- If NO → skip component entirely
- If YES → proceed to Gate 2

**Gate 2: Content + Personality Justification**
Does the slide's content warrant this component? Also consider the brand's primary Aaker dimension (from Part 2b):
- **Cards**: Does the slide have 2+ related points that benefit from grouping? If single message → no cards. *Personality modifier: Excitement brands → lower threshold (use cards more freely for visual energy); Sophistication brands → higher threshold (use cards sparingly, prefer negative space).*
- **Icons**: Is there a clear, unforced visual metaphor? If you have to think about it → no icon. *Personality modifier: Sincerity/Excitement brands → icons add warmth/energy; Sophistication brands → icons risk feeling casual, prefer typographic emphasis.*
- **Gradients**: Is this a hook, transition, or CTA slide? If content slide → no gradient. *Personality modifier: Excitement brands → gradients add dynamism; Competence brands → solid colors communicate precision.*
- If NO justification → skip component
- If YES → proceed to Gate 3

**Gate 3: Frequency Budget**
Is this component within its presentation-wide budget?
- Cards: used on ≤60% of slides so far?
- Icons: used on ≤50% of slides so far?
- Gradients: used on ≤3 slides total?
- If OVER budget → skip component, use alternative treatment
- If WITHIN budget → proceed to Gate 4

**Gate 4: Density Check**
Will adding this component exceed 3 visual layers on this slide?
- Background + content + this component = 3 layers max
- Cards + gradient on same slide = usually too dense (exception: Pitch-Velocity, Memphis)
- If TOO dense → skip component
- If OK → use component

**When a component fails a gate**, use these alternatives:
- Instead of a card → bold text with accent underline or increased font size
- Instead of an icon → typographic emphasis, a number, or additional whitespace
- Instead of a gradient → solid brand-tinted background color

### Component Availability by Style

Before using components, verify the style supports them (see `style-constraints.md`):

| Component | Supported Styles | Not Allowed |
|-----------|-----------------|-------------|
| **Cards** | Dramatic, Organic, Hygge, Lagom, Swiss, Memphis, Feng Shui, Iki, Tech-Modern, Data-Forward, Corporate-Confident, Pitch-Velocity, Narrative-Clean (subtle) | Ma, Yeo-baek |
| **Icons** | Dramatic, Organic, Hygge, Lagom, Swiss, Memphis, Feng Shui, Iki, Tech-Modern, Pitch-Velocity, Data-Forward (trend only) | Minimal, Wabi-Sabi, Shibui, Ma, Yeo-baek, Corporate-Confident, Narrative-Clean |
| **Gradients** | Dramatic, Organic, Hygge, Memphis, Feng Shui, Pitch-Velocity, Tech-Modern (subtle only) | Minimal, Swiss, Ma, Yeo-baek, Lagom, Data-Forward, Corporate-Confident, Narrative-Clean |

### Using Cards

Draw rounded containers for content grouping. See `references/technical-implementation.md` for:
- `draw_content_card()` - Basic rounded container
- `draw_icon_card()` - Square card with centered icon
- `draw_feature_card()` - Card with icon, title, description

### Using Icons

Lucide icons available via the icon helper. The plugin sets `BRAND_CONTENT_DESIGN_DIR` via SessionStart hook.

```python
import os
import sys
from pathlib import Path

# Plugin sets BRAND_CONTENT_DESIGN_DIR automatically
plugin_dir = os.environ.get('BRAND_CONTENT_DESIGN_DIR')
if plugin_dir:
    sys.path.insert(0, str(Path(plugin_dir) / "scripts"))

from icons import get_icon_png, search_icons, ICON_CATEGORIES

icon_path = get_icon_png('lightbulb', color='#3B82F6', size=48)
canvas.drawImage(icon_path, x, y, width=48, height=48, mask='auto')
```

See `references/technical-implementation.md` for full icon usage patterns.

### Using Gradients

Background transitions for depth:
```python
# See references/technical-implementation.md for draw_gradient_background
```

### Slide-Type Quick Reference

| Slide Type | Cards | Icons | Gradient |
|------------|:-----:|:-----:|:--------:|
| Hook/Opening | ✗ | ✗ | ✓ |
| Features/Steps | ✓ | ✓ | ✗ |
| Data/Stats | ◐ | ✗ | ✗ |
| Quote | ◐ | ✗ | ✗ |
| CTA/Closing | ✗ | ✗ | ✓ |

**Legend:** ✓ = Use | ◐ = If content warrants | ✗ = Avoid

**Remember**: Visual components must serve the message. When in doubt, use fewer.

---

## Part 8: Technical Implementation

For PDF generation code patterns, see `references/technical-implementation.md`:
- Asset preparation (SVG→PNG conversion, font loading)
- reportlab patterns for presentations (1920x1080) and carousels (1080x1350)
- Color parsing from brand-philosophy.md
- Positioning patterns: Centered (Ma/Minimal), Asymmetric (Dramatic/Iki), Grid (Swiss)
- **Visual components: Cards, gradients, icons**

### Quick Reference

| Task | Action |
|------|--------|
| Logo format | **PNG or JPG only** - SVG not supported by reportlab |
| SVG logo | Convert to PNG with cairosvg (`/brand-extract` does this automatically) |
| Custom fonts | Load from `{PROJECT_PATH}/assets/fonts/` |
| Presentations | 1920x1080, 50px safe zones |
| Carousels | 1080x1350 (LinkedIn), 5% margins |
| Colors | Parse from brand-philosophy.md color table |

### Output Process

1. **Generate PDF** (source of truth) - Use `pdf` skill with reportlab
2. **Convert to PPTX** (presentations only) - Use `pptx` skill for editability

---

## Part 9: Workflow Integration

This skill is called by:
- `/template-presentation` - Generate sample.pdf + sample.pptx
- `/template-carousel` - Generate sample.pdf
- `/presentation` - Generate final presentation
- `/presentation-quick` - Generate final presentation (fast path)
- `/carousel` - Generate final carousel
- `/carousel-quick` - Generate final carousel (fast path)

## Part 10: Input Requirements

When invoking this skill, provide:

1. **Canvas philosophy content** (from template's canvas-philosophy.md)
2. **Style enforcement block** (from style-constraints.md)
3. **Content outline** (slide/card content to render)
4. **Brand philosophy** (colors, fonts, logo from brand-philosophy.md)
5. **Output format** (presentation or carousel)
6. **Dimensions** (based on content type)
7. **Visual components config** (optional - from canvas-philosophy.md Visual Components section)

### No-Brand Safeguard

If `brand-philosophy.md` is not found OR contains no `## Color Palette` section:
- **STOP generation** — inform user: "No brand colors found. Run `/brand-extract` first to analyze your brand."
- If user insists on proceeding: use deliberately bland neutrals (#1a1a1a, #666, #f5f5f5, system fonts)
- Never fall back to any recognizable brand colors

### Pre-Output Brand Bias Check

Before finalizing any presentation or carousel:
```
□ All colors derived from brand-philosophy.md color table
□ All fonts loaded from project assets/fonts/ or brand-philosophy.md
□ Colors traced to brand-philosophy.md (not copied from reference docs or runtime fallbacks)
□ No generic font defaults (unless brand actually uses them)
□ Text colors WCAG-validated against actual background
```

---

## Part 11: The Ultimate Test

Before finalizing, ask:

> Would this work hang in a design museum?
> Would a creative director approve this for a premium client?
> Does every pixel serve the message?
> Does it look like someone labored over it with painstaking care?

If yes to all four, the work is ready.

If no to any, return to Part 6 and polish until it gleams.
