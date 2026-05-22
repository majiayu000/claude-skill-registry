---
name: baoyu-article-illustrator
description: Smart article illustration skill. Analyzes article content and generates illustrations at positions requiring visual aids with multiple style options. Use when user asks to "add illustrations to article", "generate images for article", or "illustrate article".
---

# Smart Article Illustration Skill

Analyze article structure and content, identify positions requiring visual aids, and generate illustrations with flexible style options.

## Usage

```bash
# Auto-select style based on content
/baoyu-article-illustrator path/to/article.md

# Specify a style
/baoyu-article-illustrator path/to/article.md --style warm
/baoyu-article-illustrator path/to/article.md --style minimal
/baoyu-article-illustrator path/to/article.md --style watercolor

# Combine with other options
/baoyu-article-illustrator path/to/article.md --style playful
```

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Specify illustration style (see Style Gallery below) |

## Style Gallery

| Style | Description | Best For |
|-------|-------------|----------|
| `notion` (Default) | Minimalist hand-drawn line art, intellectual | Knowledge sharing, SaaS, productivity |
| `elegant` | Refined, sophisticated, professional | Business, thought leadership |
| `warm` | Friendly, approachable, human-centered | Personal growth, lifestyle, education |
| `minimal` | Ultra-clean, zen-like, focused | Philosophy, minimalism, core concepts |
| `playful` | Fun, creative, whimsical | Tutorials, beginner guides, fun topics |
| `nature` | Organic, calm, earthy | Sustainability, wellness, outdoor |
| `sketch` | Raw, authentic, notebook-style | Ideas, brainstorming, drafts |
| `watercolor` | Soft artistic with natural warmth | Lifestyle, travel, creative |
| `vintage` | Nostalgic aged-paper aesthetic | Historical, biography, heritage |
| `scientific` | Academic precise diagrams | Biology, chemistry, technical |
| `chalkboard` | Classroom chalk drawing style | Education, tutorials, workshops |
| `editorial` | Magazine-style infographic | Tech explainers, journalism |
| `flat` | Modern flat vector illustration | Startups, digital, contemporary |
| `retro` | 80s/90s vibrant nostalgic | Pop culture, gaming, entertainment |
| `blueprint` | Technical schematics, engineering precision | Architecture, system design |
| `vector-illustration` | Flat vector with black outlines, retro colors | Educational, creative, brand content |
| `sketch-notes` | Soft hand-drawn, warm educational feel | Knowledge sharing, tutorials |
| `pixel-art` | Retro 8-bit gaming aesthetic | Gaming, tech, developer content |
| `intuition-machine` | Technical briefing with bilingual labels | Academic, technical, bilingual |
| `fantasy-animation` | Ghibli/Disney whimsical style | Storytelling, children's, creative |

Full style specifications in `references/styles/<style>.md`

## Auto Style Selection

When no `--style` is specified, analyze content to select the best style:

| Content Signals | Selected Style |
|----------------|----------------|
| Personal story, emotion, growth, life, feeling, relationship | `warm` |
| Simple, zen, focus, essential, core, minimalist | `minimal` |
| Fun, easy, beginner, tutorial, guide, how-to, learn | `playful` |
| Nature, eco, wellness, health, organic, green, outdoor | `nature` |
| Idea, thought, concept, draft, brainstorm, sketch | `sketch` |
| Business, professional, strategy, analysis, corporate | `elegant` |
| Knowledge, concept, productivity, SaaS, notion, tool | `notion` |
| Lifestyle, travel, food, art, creative, artistic | `watercolor` |
| History, heritage, vintage, biography, classic, expedition | `vintage` |
| Biology, chemistry, medical, scientific, research, academic | `scientific` |
| Education, classroom, teaching, school, lecture, workshop | `chalkboard` |
| Explainer, journalism, magazine, in-depth, investigation | `editorial` |
| Modern, startup, app, product, digital marketing, saas | `flat` |
| 80s, 90s, retro, pop culture, music, nostalgia | `retro` |
| Architecture, system, infrastructure, engineering, technical | `blueprint` |
| Brand, explainer, children, cute, toy, geometric | `vector-illustration` |
| Notes, doodle, friendly, warm tutorial, onboarding | `sketch-notes` |
| Gaming, 8-bit, pixel, developer, retro tech | `pixel-art` |
| Bilingual, briefing, academic, research, documentation | `intuition-machine` |
| Fantasy, story, magical, Ghibli, Disney, children | `fantasy-animation` |
| Default | `notion` |

## File Management

### Output Directory

Each session creates an independent directory named by content slug:

```
illustrations/{topic-slug}/
├── source-{slug}.{ext}    # Source files (text, images, etc.)
├── outline.md
├── outline-{style}.md     # Style variant outlines
├── prompts/
│   ├── illustration-concept-a.md
│   ├── illustration-concept-b.md
│   └── ...
├── illustration-concept-a.png
├── illustration-concept-b.png
└── ...
```

**Slug Generation**:
1. Extract main topic from content (2-4 words, kebab-case)
2. Example: "The Future of AI" → `future-of-ai`

### Conflict Resolution

If `illustrations/{topic-slug}/` already exists:
- Append timestamp: `{topic-slug}-YYYYMMDD-HHMMSS`
- Example: `ai-future` exists → `ai-future-20260118-143052`

### Source Files

Copy all sources with naming `source-{slug}.{ext}`:
- `source-article.md` (main text content)
- `source-photo.jpg` (image from conversation)
- `source-reference.pdf` (additional file)

Multiple sources supported: text, images, files from conversation.

## Workflow

### Step 1: Analyze Content & Select Style

1. Read article content
2. If `--style` specified, use that style
3. Otherwise, scan for style signals and auto-select
4. **Language detection**:
   - Detect **source language** from article content
   - Detect **user language** from conversation context
   - Note if source_language ≠ user_language (will ask in Step 4)
5. Extract key information:
   - Main topic and themes
   - Core messages per section
   - Abstract concepts needing visualization

### Step 2: Identify Illustration Positions

**Three Purposes of Illustrations**:
1. **Information Supplement**: Help understand abstract concepts
2. **Concept Visualization**: Transform abstract ideas into concrete visuals
3. **Imagination Guidance**: Create atmosphere, enhance reading experience

**Content Suitable for Illustrations**:
- Abstract concepts needing visualization
- Processes/steps needing diagrams
- Comparisons needing visual representation
- Core arguments needing reinforcement
- Scenarios needing imagination guidance

**Illustration Count**:
- Consider at least 1 image per major section
- Prioritize core arguments and abstract concepts
- **Principle: More is better than fewer**

### Step 3: Generate Illustration Plan

```markdown
# Illustration Plan

**Article**: [article path]
**Style**: [selected style]
**Illustration Count**: N images

---

## Illustration 1

**Insert Position**: [section name] / [paragraph description]
**Purpose**: [why illustration needed here]
**Visual Content**: [what the image should show]
**Filename**: illustration-[slug].png

---

## Illustration 2
...
```

### Step 4: Review & Confirm

**Purpose**: Let user confirm all options in a single step before image generation.

**IMPORTANT**: Present ALL options in a single confirmation step using AskUserQuestion. Do NOT interrupt workflow with multiple separate confirmations.

1. **Generate 3 style variants**:
   - Analyze content to select 3 most suitable styles
   - Generate complete illustration plan for each style variant
   - Save as `outline-{style}.md` (e.g., `outline-notion.md`, `outline-tech.md`, `outline-warm.md`)

2. **Determine which questions to ask**:

   | Question | When to Ask |
   |----------|-------------|
   | Style variant | Always (required) |
   | Language | Only if `source_language ≠ user_language` |

3. **Present options** (use AskUserQuestion with all applicable questions):

   **Question 1 (Style)** - always:
   - Style A (recommended): [style name] - [brief description]
   - Style B: [style name] - [brief description]
   - Style C: [style name] - [brief description]
   - Custom: Provide custom style reference

   **Question 2 (Language)** - only if source ≠ user language:
   - [Source language] (matches article language)
   - [User language] (your preference)

   **Language handling**:
   - If source language = user language: Just inform user (e.g., "Prompts will be in Chinese")
   - If different: Ask which language to use for prompts

4. **Apply selection**:
   - Copy selected `outline-{style}.md` to `outline.md`
   - If custom style provided, generate new plan with that style
   - If different language selected, regenerate outline in that language
   - User may edit `outline.md` directly for fine-tuning
   - If modified, reload plan before proceeding

5. **Proceed only after explicit user confirmation**

### Step 5: Create Prompt Files

Save prompts to `prompts/` directory with style-specific details.

**All prompts are written in the user's confirmed language preference.**

**Prompt Format**:

```markdown
Illustration theme: [concept in 2-3 words]
Style: [style name]

Visual composition:
- Main visual: [description matching style]
- Layout: [element positioning]
- Decorative elements: [style-appropriate decorations]

Color scheme:
- Primary: [style primary color]
- Background: [style background color]
- Accent: [style accent color]

Text content (if any):
- [Any labels or captions in content language]

Style notes: [specific style characteristics]
```

### Step 6: Generate Images

**Image Generation Skill Selection**:
1. Check available image generation skills
2. If multiple skills available, ask user to choose

**Generation Flow**:
1. Call selected image generation skill with prompt file and output path
2. Generate images sequentially
3. After each image, output progress: "Generated X/N"
4. On failure, auto-retry once
5. If retry fails, log reason, continue to next

### Step 7: Update Article

Insert generated images at corresponding positions:

```markdown
![illustration description]([article-name]/illustrations/illustration-[slug].png)
```

**Insertion Rules**:
- Insert image after corresponding paragraph
- Leave one blank line before and after image
- Alt text uses concise description in article's language

### Step 8: Output Summary

```
Article Illustration Complete!

Article: [article path]
Style: [style name]
Generated: X/N images successful

Illustration Positions:
- illustration-xxx.png → After section "Section Name"
- illustration-yyy.png → After section "Another Section"
...

[If any failures]
Failed:
- illustration-zzz.png: [failure reason]
```

## Illustration Modification

Support for modifying individual illustrations after initial generation.

### Edit Single Illustration

Regenerate a specific illustration with modified prompt:

1. Identify illustration to edit (e.g., `illustration-concept-overview.png`)
2. Update prompt in `prompts/illustration-concept-overview.md` if needed
3. If content changes significantly, update slug in filename
4. Regenerate image
5. Update article if image reference changed

### Add New Illustration

Add a new illustration to the article:

1. Identify insertion position in article
2. Create new prompt with appropriate slug (e.g., `illustration-new-concept.md`)
3. Generate new illustration image
4. Update `outline.md` with new illustration entry
5. Insert image reference in article at the specified position

### Delete Illustration

Remove an illustration from the article:

1. Identify illustration to delete (e.g., `illustration-concept-overview.png`)
2. Remove image file and prompt file
3. Remove image reference from article
4. Update `outline.md` to remove illustration entry

### File Naming Convention

Files use meaningful slugs for better readability:
```
illustration-[slug].png
illustration-[slug].md (in prompts/)
```

Examples:
- `illustration-concept-overview.png`
- `illustration-workflow-diagram.png`
- `illustration-key-benefits.png`

**Slug rules**:
- Derived from illustration purpose/content (kebab-case)
- Must be unique within the article
- When content changes significantly, update slug accordingly

## References

| File | Content |
|------|---------|
| `references/styles/<style>.md` | Full style specifications with colors, elements, rules |

## Notes

- Illustrations serve the content: supplement information, visualize concepts
- Maintain selected style consistency across all illustrations in one article
- Image generation typically takes 10-30 seconds per image
- Sensitive figures should use cartoon alternatives
- Prompts written in user's confirmed language preference
- Illustration text (labels, captions) should match article language

## Extension Support

Custom styles and configurations via EXTEND.md.

**Check paths** (priority order):
1. `.baoyu-skills/baoyu-article-illustrator/EXTEND.md` (project)
2. `~/.baoyu-skills/baoyu-article-illustrator/EXTEND.md` (user)

If found, load before Step 1. Extension content overrides defaults.
