---
name: baoyu-slide-deck
description: Generate professional slide deck images from content. Creates comprehensive outlines with style instructions, then generates individual slide images. Use when user asks to "create slides", "make a presentation", "generate deck", or "slide deck".
---

# Slide Deck Generator

Transform content into professional slide deck with comprehensive outlines and generated slide images.

## Usage

```bash
# From markdown file
/baoyu-slide-deck path/to/article.md

# With style preference
/baoyu-slide-deck path/to/article.md --style corporate
/baoyu-slide-deck path/to/article.md --style playful
/baoyu-slide-deck path/to/article.md --style technical

# With audience specification
/baoyu-slide-deck path/to/article.md --audience beginners
/baoyu-slide-deck path/to/article.md --audience executives

# With language
/baoyu-slide-deck path/to/article.md --lang zh
/baoyu-slide-deck path/to/article.md --lang en

# Outline only (no image generation)
/baoyu-slide-deck path/to/article.md --outline-only

# Direct content input
/baoyu-slide-deck
[paste content]
```

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style preset (see Style Gallery) |
| `--audience <type>` | Target audience level |
| `--lang <code>` | Output language (en, zh, etc.) |
| `--slides <number>` | Target slide count (max 20) |
| `--outline-only` | Generate outline only, skip image generation |

## Style Gallery

| Style | Description |
|-------|-------------|
| `editorial` (Default) | Clean, sophisticated, minimalist |
| `corporate` | Professional, trustworthy, polished |
| `technical` | Precise, data-driven, analytical |
| `playful` | Bold, energetic, engaging |
| `minimal` | Ultra-clean, zen-like, focused |
| `storytelling` | Narrative-driven, cinematic, immersive |
| `warm` | Cozy, healing, hand-drawn illustration style |
| `retro-flat` | Flat vector illustration with retro palette |
| `notion` | Minimalist hand-drawn line art, intellectual |

Detailed style definitions: `references/styles/<style>.md`

## Auto Style Selection

When no `--style` is specified, analyze content for style signals:

| Content Signals | Selected Style |
|----------------|----------------|
| AI, coding, tech, digital, algorithm, data | `technical` |
| Business, strategy, investment, corporate | `corporate` |
| Personal story, journey, narrative, emotion | `storytelling` |
| Simple, zen, focus, essential, one idea | `minimal` |
| Fun, creative, workshop, educational | `playful` |
| Research, analysis, thought leadership | `editorial` |
| Wellness, healing, cozy, self-care, lifestyle, comfort | `warm` |
| Tutorial, explainer, how-to, beginner, product, guide | `retro-flat` |
| Knowledge, concept, productivity, SaaS, notion, intellectual | `notion` |

## Audience Presets

| Audience | Approach |
|----------|----------|
| `beginners` | Step-by-step, more context, simpler visuals |
| `intermediate` | Balanced detail, some assumed knowledge |
| `experts` | Dense information, technical depth, less hand-holding |
| `executives` | High-level insights, key metrics, strategic focus |
| `general` | Accessible language, broad appeal, clear takeaways |

## File Management

### With Article Path

```
path/to/
├── article.md
└── slide-deck/
    ├── outline.md
    ├── prompts/
    │   ├── 01-cover.md
    │   ├── 02-content-1.md
    │   └── ...
    ├── 01-cover.png
    ├── 02-content-1.png
    └── ...
```

### Without Article Path

```
./baoyu-slide-deck-outputs/YYYY-MM-DD/[topic-slug]/
├── outline.md
├── prompts/
│   ├── 01-cover.md
│   └── ...
├── 01-cover.png
└── ...
```

## Workflow

### Step 1: Analyze Content & Select Style

1. Read source content
2. If `--style` specified, use that style
3. Otherwise, analyze content for style signals
4. Extract key information:
   - Core narrative and key messages
   - Important data points and statistics
   - Logical flow and structure
   - Target audience signals

### Step 2: Generate Outline

Create outline with `STYLE_INSTRUCTIONS` block and slide specifications.

**Outline Format**:

```markdown
# Slide Deck Outline: [Topic]

**Source**: [source file or "Direct input"]
**Style**: [selected style]
**Audience**: [target audience]
**Language**: [output language]
**Slide Count**: N slides
**Generated**: YYYY-MM-DD HH:mm

---

<STYLE_INSTRUCTIONS>
Design Aesthetic: [Overall style description]
Background Color: [Description and Hex Code]
Primary Font: [Font name for Headlines]
Secondary Font: [Font name for Body copy]
Color Palette:
  Primary Text Color: [Hex Code]
  Primary Accent Color: [Hex Code]
Visual Elements: [Lines, shapes, imagery style, etc.]
</STYLE_INSTRUCTIONS>

---

## Slide 1: [Descriptive Title]

**Position**: Cover
**Filename**: 01-cover.png

// NARRATIVE GOAL
[Storytelling purpose within the overall arc]

// KEY CONTENT
Headline: [Main message - narrative, not "Title: Subtitle" format]
Sub-headline: [Supporting context]
Body:
- [Key point 1 with specific data from source]
- [Key point 2 with specific data from source]

// VISUAL
[Detailed description of imagery, charts, graphics, or abstract visuals]

// LAYOUT
[Composition, hierarchy, spatial arrangement, focus points]

---

## Slide 2: [First Content]
...

## Slide N: [Back Cover]
...
```

**Required Slide Structure**:
1. **Slide 1**: Cover Slide (poster-style, heroic typography)
2. **Slides 2-N-1**: Content slides (consistent internal style)
3. **Slide N**: Back Cover (closing statement, not "Thank You")

### Step 3: Save Outline

Save outline as `outline.md` in target directory.

If `--outline-only` flag is set, stop here.

### Step 4: Create Prompt Files

For each slide, create a style-specific prompt file.

**Prompt Format**:

```markdown
Slide theme: [slide title]
Style: [style name]
Position: [cover/content/back-cover]

Visual composition:
- Main visual: [style-appropriate description from VISUAL section]
- Layout: [from LAYOUT section]
- Decorative elements: [style-specific decorations]

Color scheme:
- Background: [style background color]
- Primary text: [style text color]
- Accent: [style accent color]

Text content:
- Headline: [headline text]
- Sub-headline: [sub-headline if any]
- Body points: [bullet points if any]

Style notes: [specific style characteristics to emphasize]
```

### Step 5: Generate Images

For each slide, generate using:

```bash
/baoyu-gemini-web --promptfiles [SKILL_ROOT]/skills/baoyu-slide-deck/prompts/system.md [TARGET_DIR]/prompts/01-cover.md --image [TARGET_DIR]/01-cover.png
```

Generation flow:
1. Generate images sequentially
2. After each image, output progress: "Generated X/N"
3. On failure, auto-retry once
4. If retry fails, log reason, continue to next

### Step 6: Completion Report

```
Slide Deck Generated!

Topic: [topic]
Style: [style name]
Audience: [audience]
Location: [directory path]
Slides: N total

- 01-cover.png ✓ Cover
- 02-content-1.png ✓ Content
- 03-content-2.png ✓ Content
- ...
- 0N-back-cover.png ✓ Back Cover

Outline: outline.md

[If any failures]
Failed:
- 0X-slide-name.png: [failure reason]
```

## Notes

### Design Philosophy
- Deck is designed for **reading and sharing**, not live presentation
- Structure should be self-explanatory without a presenter
- Include enough context for visuals to be understood standalone
- Err on the side of audience having **more expertise** than expected

### Content Rules
- Maximum 20 slides per deck
- Every data point must trace to source material
- All details in prompts - image generator has no access to source

### Style Rules
- Avoid AI-generated clichés ("It wasn't just X, it was Y")
- Use narrative headlines, not "Title: Subtitle" format
- Cover and Back Cover should be visually distinct (poster-style)
- Back Cover should be meaningful closure, not "Thank You" or "Questions?"

### Prohibited
- Never include photorealistic images of prominent individuals
- Never include placeholder slides for author name, date, etc.

### Image Generation
- Image generation typically takes 10-30 seconds per slide
- Auto-retry once on generation failure
- Use cartoon alternatives for sensitive public figures
- Output language matches content language
- Maintain style consistency across all slides
