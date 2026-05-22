---
name: baoyu-slide-deck
description: Generate professional slide deck images from content. Creates comprehensive outlines with style instructions, then generates individual slide images. Use when user asks to "create slides", "make a presentation", "generate deck", or "slide deck".
---

# Slide Deck Generator

Transform content into professional slide deck images with flexible style options.

## Usage

```bash
/baoyu-slide-deck path/to/content.md
/baoyu-slide-deck path/to/content.md --style sketch-notes
/baoyu-slide-deck path/to/content.md --audience executives
/baoyu-slide-deck path/to/content.md --lang zh
/baoyu-slide-deck path/to/content.md --slides 10
/baoyu-slide-deck path/to/content.md --outline-only
/baoyu-slide-deck  # Then paste content
```

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/merge-to-pptx.ts` | Merge slides into PowerPoint |
| `scripts/merge-to-pdf.ts` | Merge slides into PDF |

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style (see Style Gallery) |
| `--audience <type>` | Target audience: beginners, intermediate, experts, executives, general |
| `--lang <code>` | Output language (en, zh, ja, etc.) |
| `--slides <number>` | Target slide count |
| `--outline-only` | Generate outline only, skip image generation |

## Style Gallery

| Style | Description | Best For |
|-------|-------------|----------|
| `blueprint` (Default) | Technical schematics, grid texture | Architecture, system design |
| `chalkboard` | Black chalkboard, colorful chalk | Education, tutorials, classroom |
| `notion` | SaaS dashboard, card-based layouts | Product demos, SaaS, B2B |
| `bold-editorial` | Magazine cover, bold typography, dark | Product launches, keynotes |
| `corporate` | Navy/gold, structured layouts | Investor decks, proposals |
| `dark-atmospheric` | Cinematic dark mode, glowing accents | Entertainment, gaming |
| `editorial-infographic` | Magazine explainers, flat illustrations | Tech explainers, research |
| `fantasy-animation` | Ghibli/Disney style, hand-drawn | Educational, storytelling |
| `intuition-machine` | Technical briefing, bilingual labels | Technical docs, academic |
| `minimal` | Ultra-clean, maximum whitespace | Executive briefings, premium |
| `pixel-art` | Retro 8-bit, chunky pixels | Gaming, developer talks |
| `scientific` | Academic diagrams, precise labeling | Biology, chemistry, medical |
| `sketch-notes` | Hand-drawn, warm & friendly | Educational, tutorials |
| `vector-illustration` | Flat vector, retro & cute | Creative, children's content |
| `vintage` | Aged-paper, historical styling | Historical, heritage, biography |
| `watercolor` | Hand-painted textures, natural warmth | Lifestyle, wellness, travel |

## Auto Style Selection

| Content Signals | Selected Style |
|-----------------|----------------|
| tutorial, learn, education, guide, intro, beginner | `sketch-notes` |
| classroom, teaching, school, chalkboard, blackboard | `chalkboard` |
| architecture, system, data, analysis, technical | `blueprint` |
| creative, children, kids, cute, illustration | `vector-illustration` |
| briefing, academic, research, bilingual, infographic, concept | `intuition-machine` |
| executive, minimal, clean, simple, elegant | `minimal` |
| saas, product, dashboard, metrics, productivity | `notion` |
| investor, quarterly, business, corporate, proposal | `corporate` |
| launch, marketing, keynote, bold, impact, magazine | `bold-editorial` |
| entertainment, music, gaming, creative, atmospheric | `dark-atmospheric` |
| explainer, journalism, science communication | `editorial-infographic` |
| story, fantasy, animation, magical, whimsical | `fantasy-animation` |
| gaming, retro, pixel, developer, nostalgia | `pixel-art` |
| biology, chemistry, medical, pathway, scientific | `scientific` |
| history, heritage, vintage, expedition, historical | `vintage` |
| lifestyle, wellness, travel, artistic, natural | `watercolor` |
| Default | `blueprint` |

## Design Philosophy

This deck is designed for **reading and sharing**, not live presentation:
- Each slide must be **self-explanatory** without verbal commentary
- Structure content for **logical flow** when scrolling
- Include **all necessary context** within each slide
- Optimize for **social media sharing** and offline reading

## File Management

### Output Directory

Each session creates an independent directory named by content slug:

```
slide-deck/{topic-slug}/
├── source-{slug}.{ext}    # Source files (text, images, etc.)
├── outline.md
├── outline-{style}.md     # Style variant outlines
├── prompts/
│   └── 01-slide-cover.md, 02-slide-{slug}.md, ...
├── 01-slide-cover.png, 02-slide-{slug}.png, ...
├── {topic-slug}.pptx
└── {topic-slug}.pdf
```

**Slug Generation**:
1. Extract main topic from content (2-4 words, kebab-case)
2. Example: "Introduction to Machine Learning" → `intro-machine-learning`

### Conflict Resolution

If `slide-deck/{topic-slug}/` already exists:
- Append timestamp: `{topic-slug}-YYYYMMDD-HHMMSS`
- Example: `intro-ml` exists → `intro-ml-20260118-143052`

### Source Files

Copy all sources with naming `source-{slug}.{ext}`:
- `source-article.md` (main text content)
- `source-diagram.png` (image from conversation)
- `source-data.xlsx` (additional file)

Multiple sources supported: text, images, files from conversation.

## Workflow

### Step 1: Analyze Content

1. Save source content (if pasted, save as `source.md`)
2. Follow `references/analysis-framework.md` for deep content analysis
3. Determine style (use `--style` or auto-select from signals)
4. Detect languages (source vs. user preference)
5. Plan slide count (`--slides` or dynamic)

### Step 2: Generate Outline Variants

1. Generate 3 style variant outlines based on content analysis
2. Follow `references/outline-template.md` for structure
3. Save as `outline-{style}.md` for each variant

### Step 3: User Confirmation

**Single AskUserQuestion with all applicable options:**

| Question | When to Ask |
|----------|-------------|
| Style variant | Always (3 options + custom) |
| Language | Only if source ≠ user language |

After selection:
- Copy selected `outline-{style}.md` to `outline.md`
- Regenerate in different language if requested
- User may edit `outline.md` for fine-tuning

If `--outline-only`, stop here.

### Step 4: Generate Prompts

1. Read `references/base-prompt.md`
2. Combine with style instructions from outline
3. Add slide-specific content
4. Save to `prompts/` directory

### Step 5: Generate Images

1. Select available image generation skill
2. Generate session ID: `slides-{topic-slug}-{timestamp}`
3. Generate each slide with same session ID
4. Report progress: "Generated X/N"

### Step 6: Merge to PPTX and PDF

```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pptx.ts <slide-deck-dir>
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <slide-deck-dir>
```

### Step 7: Output Summary

```
Slide Deck Complete!

Topic: [topic]
Style: [style name]
Location: [directory path]
Slides: N total

- 01-slide-cover.png ✓ Cover
- 02-slide-intro.png ✓ Content
- ...
- {NN}-slide-back-cover.png ✓ Back Cover

Outline: outline.md
PPTX: {topic-slug}.pptx
PDF: {topic-slug}.pdf
```

## Slide Modification

See `references/modification-guide.md` for:
- Edit single slide workflow
- Add new slide (with renumbering)
- Delete slide (with renumbering)
- File naming conventions

## References

| File | Content |
|------|---------|
| `references/analysis-framework.md` | Deep content analysis for presentations |
| `references/outline-template.md` | Outline structure and STYLE_INSTRUCTIONS format |
| `references/modification-guide.md` | Edit, add, delete slide workflows |
| `references/content-rules.md` | Content and style guidelines |
| `references/base-prompt.md` | Base prompt for image generation |
| `references/styles/<style>.md` | Full style specifications |

## Notes

- Image generation: 10-30 seconds per slide
- Auto-retry once on generation failure
- Use stylized alternatives for sensitive public figures
- Maintain style consistency via session ID

## Extension Support

Custom styles and configurations via EXTEND.md.

**Check paths** (priority order):
1. `.baoyu-skills/baoyu-slide-deck/EXTEND.md` (project)
2. `~/.baoyu-skills/baoyu-slide-deck/EXTEND.md` (user)

If found, load before Step 1. Extension content overrides defaults.
