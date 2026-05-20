---
name: baoyu-comic
description: Knowledge comic creator supporting multiple styles (Logicomix/Ligne Claire, Ohmsha manga guide). Creates original educational comics with detailed panel layouts and sequential image generation. Use when user asks to create "知识漫画", "教育漫画", "biography comic", "tutorial comic", or "Logicomix-style comic".
---

# Knowledge Comic Creator

Create original knowledge comics with multiple visual styles.

## Usage

```bash
/baoyu-comic posts/turing-story/source.md
/baoyu-comic  # then paste content
```

## Options

| Option | Values |
|--------|--------|
| `--style` | classic (default), dramatic, warm, tech, sepia, vibrant, ohmsha, realistic, or custom description |
| `--layout` | standard (default), cinematic, dense, splash, mixed, webtoon |
| `--aspect` | 3:4 (default, portrait), 4:3 (landscape), 16:9 (widescreen) |
| `--lang` | auto (default), zh, en, ja, etc. |

Style × Layout × Aspect can be freely combined. Custom styles can be described in natural language.

**Aspect ratio is consistent across all pages in a comic.**

## Auto Selection

| Content Signals | Style | Layout |
|-----------------|-------|--------|
| Tutorial, how-to, beginner | ohmsha | webtoon |
| Computing, AI, programming | tech | dense |
| Pre-1950, classical, ancient | sepia | cinematic |
| Personal story, mentor | warm | standard |
| Conflict, breakthrough | dramatic | splash |
| Wine, food, business, lifestyle, professional | realistic | cinematic |
| Biography, balanced | classic | mixed |

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/merge-to-pdf.ts` | Merge comic pages into PDF |

## File Structure

```
[target]/
├── source.md                      # Source content (if pasted, not file)
├── analysis.md                    # Deep analysis results (YAML+MD)
├── storyboard-chronological.md    # Variant A (preserved)
├── storyboard-thematic.md         # Variant B (preserved)
├── storyboard-character.md        # Variant C (preserved)
├── characters-chronological/      # Variant A chars (preserved)
│   ├── characters.md
│   └── characters.png
├── characters-thematic/           # Variant B chars (preserved)
│   ├── characters.md
│   └── characters.png
├── characters-character/          # Variant C chars (preserved)
│   ├── characters.md
│   └── characters.png
├── storyboard.md                  # Final selected
├── characters/                    # Final selected
│   ├── characters.md
│   └── characters.png
├── prompts/
│   ├── 00-cover-[slug].md
│   └── NN-page-[slug].md
├── 00-cover-[slug].png
├── NN-page-[slug].png
└── {topic-slug}.pdf
```

**Target directory**:
- With source path: `[source-dir]/[source-name-no-ext]/comic/`
  - Example: `/posts/turing-story.md` → `/posts/turing-story/comic/`
- Without source: `./comic/[topic-slug]/`

**Directory backup**:
- If target directory exists, rename existing to `<dirname>-backup-YYYYMMDD-HHMMSS`

## Workflow

### Step 1: Analyze Content → `analysis.md`

Read source content, save it if needed, and perform deep analysis.

**Actions**:
1. **Save source content** (if not already a file):
   - If user provides a file path: use as-is
   - If user pastes content: save to `source.md` in target directory
2. Read source content
3. **Deep analysis** following `references/analysis-framework.md`:
   - Target audience identification
   - Value proposition for readers
   - Core themes and narrative potential
   - Key figures and their story arcs
4. Detect source language
5. Determine recommended page count:
   - Short story: 5-8 pages
   - Medium complexity: 9-15 pages
   - Full biography: 16-25 pages
6. Analyze content signals for style/layout recommendations
7. **Save to `analysis.md`**

**analysis.md Format**:

```yaml
---
title: "Alan Turing: Father of Computing"
topic: Biography
time_span: 1912-1954
source_language: en
user_language: zh
aspect_ratio: "3:4"
recommended_page_count: 12
---

## Target Audience

- **Primary**: Tech enthusiasts curious about computing history
- **Secondary**: Students learning about scientific breakthroughs
- **Tertiary**: General readers interested in biographical stories

## Value Proposition

What readers will gain:
1. Understanding of how modern computing was born
2. Emotional connection to a brilliant but tragic figure
3. Appreciation for the human cost of innovation

## Core Themes

| Theme | Narrative Potential | Visual Opportunity |
|-------|--------------------|--------------------|
| Genius vs. Society | High conflict, dramatic arcs | Contrast scenes |
| Code-breaking | Mystery, tension | Technical diagrams as art |
| Personal tragedy | Emotional depth | Intimate, somber panels |

## Key Figures & Story Arcs

### Alan Turing (Protagonist)
- **Arc**: Misunderstood genius → War hero → Tragic end
- **Visual identity**: Disheveled academic, intense eyes
- **Key moments**: Enigma breakthrough, arrest, final days

### Christopher Morcom (Catalyst)
- **Role**: Early friend whose death shaped Turing
- **Visual identity**: Youthful, bright
- **Key moments**: School friendship, sudden death

## Content Signals

- "biography" → classic + mixed
- "computing history" → tech + dense
- "personal tragedy" → dramatic + splash

## Recommended Approaches

1. **Chronological** - follow life timeline (recommended for biography)
2. **Thematic** - organize by contributions (good for educational focus)
3. **Character-focused** - relationships drive narrative (good for emotional impact)
```

### Step 2: Generate 3 Storyboard Variants

Create three distinct variants, each combining a narrative approach with a recommended style.

| Variant | Narrative Approach | Recommended Style | Layout |
|---------|-------------------|-------------------|--------|
| A | Chronological | sepia | cinematic |
| B | Thematic | tech | dense |
| C | Character-focused | warm | standard |

**For each variant**:

1. **Generate storyboard** (`storyboard-{approach}.md`):
   - YAML front matter with narrative_approach, recommended_style, recommended_layout, aspect_ratio
   - Cover design
   - Each page: layout, panel breakdown, visual prompts
   - **Written in user's preferred language**
   - Reference: `references/storyboard-template.md`

2. **Generate matching characters** (`characters-{approach}/`):
   - `characters.md` - visual specs matching the recommended style (in user's preferred language)
   - `characters.png` - character reference sheet
   - Reference: `references/character-template.md`

**All variants are preserved after selection for reference.**

### Step 3: User Confirms All Options

**IMPORTANT**: Present ALL options in a single confirmation step using AskUserQuestion. Do NOT interrupt workflow with multiple separate confirmations.

**Determine which questions to ask**:

| Question | When to Ask |
|----------|-------------|
| Storyboard variant | Always (required) |
| Visual style | Always (required) |
| Language | Only if `source_language ≠ user_language` |
| Aspect ratio | Only if user might prefer non-default (e.g., landscape content) |

**Language handling**:
- If source language = user language: Just inform user (e.g., "Comic will be in Chinese")
- If different: Ask which language to use

**All storyboards and prompts are generated in the user's selected/preferred language.**

**Aspect ratio handling**:
- Default: 3:4 (portrait) - standard comic format
- Offer 4:3 (landscape) if content suits it (e.g., panoramic scenes, technical diagrams)
- Offer 16:9 (widescreen) for cinematic content

**AskUserQuestion format** (example with all questions):

```
Question 1 (Storyboard): Which storyboard variant?
- A: Chronological + sepia (Recommended)
- B: Thematic + tech
- C: Character-focused + warm
- Custom

Question 2 (Style): Which visual style?
- sepia (Recommended from variant)
- classic / dramatic / warm / tech / vibrant / ohmsha / realistic
- Custom description

Question 3 (Language) - only if mismatch:
- Chinese (source material language)
- English (your preference)

Question 4 (Aspect) - only if relevant:
- 3:4 Portrait (Recommended)
- 4:3 Landscape
- 16:9 Widescreen
```

**After confirmation**:
1. Copy selected storyboard → `storyboard.md`
2. Copy selected characters → `characters/`
3. Update YAML front matter with confirmed style, language, aspect_ratio
4. If style differs from variant's recommended: regenerate `characters/characters.png`
5. User may edit files directly for fine-tuning

### Step 4: Generate Images

With confirmed storyboard + style + aspect ratio:

**For each page (cover + pages)**:
1. Save prompt to `prompts/NN-{cover|page}-[slug].md` (in user's preferred language)
2. Generate image using confirmed style and aspect ratio
3. Report progress after each generation

**Image Generation Skill Selection**:
- Check available image generation skills
- If multiple skills available, ask user preference

**Character Reference Handling**:
- If skill supports reference image: pass `characters/characters.png`
- If skill does NOT support reference image: include `characters/characters.md` content in prompt

**Session Management**:
If image generation skill supports `--sessionId`:
1. Generate unique session ID: `comic-{topic-slug}-{timestamp}`
2. Use same session ID for all pages
3. Ensures visual consistency across generated images

### Step 5: Merge to PDF

After all images generated:

```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <comic-dir>
```

Creates `{topic-slug}.pdf` with all pages as full-page images.

### Step 6: Completion Report

```
Comic Complete!
Title: [title] | Style: [style] | Pages: [count] | Aspect: [ratio] | Language: [lang]
Location: [path]
✓ analysis.md
✓ characters.png
✓ 00-cover-[slug].png ... NN-page-[slug].png
✓ {topic-slug}.pdf
```

## Page Modification

Support for modifying individual pages after initial generation.

### Edit Single Page

Regenerate a specific page with modified prompt:

1. Identify page to edit (e.g., `03-page-enigma-machine.png`)
2. Update prompt in `prompts/03-page-enigma-machine.md` if needed
3. If content changes significantly, update slug in filename
4. Regenerate image using same session ID and aspect ratio
5. Regenerate PDF

### Add New Page

Insert a new page at specified position:

1. Specify insertion position (e.g., after page 3)
2. Create new prompt with appropriate slug (e.g., `04-page-bletchley-park.md`)
3. Generate new page image (same aspect ratio)
4. **Renumber files**: All subsequent pages increment NN by 1
   - `04-page-tragedy.png` → `05-page-tragedy.png`
   - Slugs remain unchanged
5. Update `storyboard.md` with new page entry
6. Regenerate PDF

### Delete Page

Remove a page and renumber:

1. Identify page to delete (e.g., `03-page-enigma-machine.png`)
2. Remove image file and prompt file
3. **Renumber files**: All subsequent pages decrement NN by 1
   - `04-page-tragedy.png` → `03-page-tragedy.png`
   - Slugs remain unchanged
4. Update `storyboard.md` to remove page entry
5. Regenerate PDF

### File Naming Convention

Files use meaningful slugs for better readability:
```
NN-cover-[slug].png / NN-page-[slug].png
NN-cover-[slug].md / NN-page-[slug].md (in prompts/)
```

Examples:
- `00-cover-turing-story.png`
- `01-page-early-life.png`
- `02-page-cambridge-years.png`
- `03-page-enigma-machine.png`

**Slug rules**:
- Derived from page title/content (kebab-case)
- Must be unique within the comic
- When page content changes significantly, update slug accordingly

**Renumbering**:
- After add/delete, update NN prefix for affected pages
- Slug remains unchanged unless content changes
- Maintain sequential numbering with no gaps

## Style-Specific Guidelines

### Ohmsha Style (`--style ohmsha`)

Additional requirements for educational manga:
- **Default: Use Doraemon characters directly** - No need to create new characters
  - 大雄 (Nobita): Student role, curious learner
  - 哆啦A梦 (Doraemon): Mentor role, explains concepts with gadgets
  - 胖虎 (Gian): Antagonist/challenge role, represents obstacles or misconceptions
  - 静香 (Shizuka): Supporting role, asks clarifying questions
- Custom characters only if explicitly requested: `--characters "Student:小明,Mentor:教授"`
- Must use visual metaphors (gadgets, action scenes) - NO talking heads
- Page titles: narrative style, not "Page X: Topic"

**Reference**: `references/ohmsha-guide.md` for detailed guidelines.

## References

Detailed templates and guidelines in `references/` directory:
- `analysis-framework.md` - Deep content analysis for comic adaptation
- `character-template.md` - Character definition format and examples
- `storyboard-template.md` - Storyboard structure and panel breakdown
- `ohmsha-guide.md` - Ohmsha manga style specifics
- `styles/` - Detailed style definitions
- `layouts/` - Detailed layout definitions
