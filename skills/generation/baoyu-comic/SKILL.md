---
name: baoyu-comic
description: Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and sequential image generation. Use when user asks to create "知识漫画", "教育漫画", "biography comic", "tutorial comic", or "Logicomix-style comic".
---

# Knowledge Comic Creator

Create original knowledge comics with flexible art style × tone combinations.

## Usage

```bash
/baoyu-comic posts/turing-story/source.md
/baoyu-comic article.md --art manga --tone warm
/baoyu-comic  # then paste content
```

## Options

### Visual Dimensions

| Option | Values | Description |
|--------|--------|-------------|
| `--art` | ligne-claire (default), manga, realistic, ink-brush, chalk | Art style / rendering technique |
| `--tone` | neutral (default), warm, dramatic, romantic, energetic, vintage, action | Mood / atmosphere |
| `--layout` | standard (default), cinematic, dense, splash, mixed, webtoon | Panel arrangement |
| `--aspect` | 3:4 (default, portrait), 4:3 (landscape), 16:9 (widescreen) | Page aspect ratio |
| `--lang` | auto (default), zh, en, ja, etc. | Output language |

### Art Styles (画风)

| Style | 中文 | Description |
|-------|------|-------------|
| `ligne-claire` | 清线 | Uniform lines, flat colors, European comic tradition (Tintin, Logicomix) |
| `manga` | 日漫 | Large eyes, manga conventions, expressive emotions |
| `realistic` | 写实 | Digital painting, realistic proportions, sophisticated |
| `ink-brush` | 水墨 | Chinese brush strokes, ink wash effects |
| `chalk` | 粉笔 | Chalkboard aesthetic, hand-drawn warmth |

### Tones (基调)

| Tone | 中文 | Description |
|------|------|-------------|
| `neutral` | 中性 | Balanced, rational, educational |
| `warm` | 温馨 | Nostalgic, personal, comforting |
| `dramatic` | 戏剧 | High contrast, intense, powerful |
| `romantic` | 浪漫 | Soft, beautiful, decorative elements |
| `energetic` | 活力 | Bright, dynamic, exciting |
| `vintage` | 复古 | Historical, aged, period authenticity |
| `action` | 动作 | Speed lines, impact effects, combat |

### Preset Shortcuts

Presets with special rules beyond art+tone:

| Preset | Equivalent | Special Rules |
|--------|-----------|---------------|
| `--style ohmsha` | `--art manga --tone neutral` | Visual metaphors, NO talking heads, gadget reveals |
| `--style wuxia` | `--art ink-brush --tone action` | Qi effects, combat visuals, atmospheric elements |
| `--style shoujo` | `--art manga --tone romantic` | Decorative elements, eye details, romantic beats |

### Compatibility Matrix

| Art Style | ✓✓ Best | ✓ Works | ✗ Avoid |
|-----------|---------|---------|---------|
| ligne-claire | neutral, warm | dramatic, vintage, energetic | romantic, action |
| manga | neutral, romantic, energetic, action | warm, dramatic | vintage |
| realistic | neutral, warm, dramatic, vintage | action | romantic, energetic |
| ink-brush | neutral, dramatic, action, vintage | warm | romantic, energetic |
| chalk | neutral, warm, energetic | vintage | dramatic, action, romantic |

Art Style × Tone × Layout can be freely combined. Incompatible combinations work but may produce unexpected results.

## Auto Selection

Content signals determine default art + tone + layout (or preset):

| Content Signals | Art Style | Tone | Layout | Preset |
|-----------------|-----------|------|--------|--------|
| Tutorial, how-to, beginner | manga | neutral | webtoon | **ohmsha** |
| Computing, AI, programming | manga | neutral | dense | **ohmsha** |
| Technical explanation, educational | manga | neutral | webtoon | **ohmsha** |
| Pre-1950, classical, ancient | realistic | vintage | cinematic | - |
| Personal story, mentor | ligne-claire | warm | standard | - |
| Conflict, breakthrough | (inherit) | dramatic | splash | - |
| Wine, food, business, lifestyle | realistic | neutral | cinematic | - |
| Martial arts, wuxia, xianxia | ink-brush | action | splash | **wuxia** |
| Romance, love, school life | manga | romantic | standard | **shoujo** |
| Biography, balanced | ligne-claire | neutral | mixed | - |

**When preset is recommended**: Load `references/presets/{preset}.md` and apply all special rules.

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

Output directory: `comic/{topic-slug}/`
- Slug: 2-4 words kebab-case from topic (e.g., `alan-turing-bio`)
- Conflict: append timestamp (e.g., `turing-story-20260118-143052`)

**Contents**:
- `source-{slug}.{ext}` - Source files
- `analysis.md` - Content analysis
- `storyboard.md` - Storyboard with panel breakdown
- `characters/characters.md` - Character definitions
- `characters/characters.png` - Character reference sheet
- `prompts/NN-{cover|page}-[slug].md` - Generation prompts
- `NN-{cover|page}-[slug].png` - Generated images
- `{topic-slug}.pdf` - Final merged PDF

## Workflow

### Progress Checklist

Copy and track progress:

```
Comic Progress:
- [ ] Step 1: Load preferences + Analyze content
- [ ] Step 2: Confirmation 1 - Style & options ⚠️ REQUIRED
- [ ] Step 3: Generate storyboard + characters
- [ ] Step 4: Confirmation 2 - Review outline (if requested)
- [ ] Step 5: Generate images (sequential)
- [ ] Step 6: Merge to PDF
- [ ] Step 7: Completion report
```

### Flow

```
Input → Preferences → Analyze → [Confirm 1: Style + Skip?] → Storyboard → [Confirm 2: if needed] → Generate → PDF → Complete
```

### Step 1: Setup & Analyze

**1.1 Load Preferences (EXTEND.md)**

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-comic/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-comic/EXTEND.md" && echo "user"
```

┌──────────────────────────────────────────────┬───────────────────┐
│                     Path                     │     Location      │
├──────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-comic/EXTEND.md          │ Project directory │
├──────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-comic/EXTEND.md    │ User home         │
└──────────────────────────────────────────────┴───────────────────┘

**When EXTEND.md Found** → Read, parse, **output summary to user**:

```
📋 Loaded preferences from [full path]
├─ Watermark: [enabled/disabled] [content if enabled]
├─ Art Style: [style name or "auto-select"]
├─ Tone: [tone name or "auto-select"]
├─ Layout: [layout or "auto-select"]
├─ Language: [language or "auto-detect"]
└─ Character presets: [count] defined
```

**MUST output this summary** so user knows their current configuration. Do not skip or silently load.

**When EXTEND.md Not Found** → First-time setup:

1. Inform user: "No preferences found. Let's set up your defaults."
2. Use AskUserQuestion to collect preferences (see `references/config/first-time-setup.md`)
3. Create EXTEND.md at user-chosen location
4. Confirm: "✓ Preferences saved to [path]"

**EXTEND.md Supports**: Watermark | Preferred art/tone/layout | Custom style definitions | Character presets | Language preference

Schema: `references/config/preferences-schema.md`

**Important**: Once EXTEND.md exists, watermark, language, and style defaults are NOT asked again in Confirmation 1 or 2. These are session-persistent settings.

**1.2 Analyze Content → `analysis.md`**

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
5. **Determine language**:
   - If EXTEND.md has `language` → use it
   - Else if `--lang` option provided → use it
   - Else → use detected source language
6. Determine recommended page count:
   - Short story: 5-8 pages
   - Medium complexity: 9-15 pages
   - Full biography: 16-25 pages
7. Analyze content signals for art/tone/layout recommendations
8. **Save to `analysis.md`**

**analysis.md Format**: YAML front matter (title, topic, time_span, source_language, user_language, aspect_ratio, recommended_page_count, recommended_art, recommended_tone) + sections for Target Audience, Value Proposition, Core Themes, Key Figures & Story Arcs, Content Signals, Recommended Approaches. See `references/analysis-framework.md` for full template.

### Step 2: Confirmation 1 - Style & Options ⚠️

**Purpose**: Select visual style + decide whether to review outline before generation. **Do NOT skip.**

**Note**: Watermark and language already configured in EXTEND.md (Step 1).

**Display summary**:
- Content type + topic identified
- Key figures extracted
- Time span detected
- Recommended page count
- Language: [from EXTEND.md or detected]
- **Recommended style**: [art] + [tone] (based on content signals)

**Use AskUserQuestion** for:

**Question 1: Visual Style**

If a preset is recommended (see Auto Selection), show it first:

```
header: "Style"
question: "Which visual style for this comic?"
options:
  - label: "[preset name] preset (Recommended)"       # If preset recommended
    description: "[preset description] - includes special rules"
  - label: "[recommended art] + [recommended tone] (Recommended)"  # If no preset
    description: "Best match for your content based on analysis"
  - label: "ligne-claire + neutral"
    description: "Classic educational, Logicomix style"
  - label: "ohmsha preset"
    description: "Educational manga with visual metaphors, gadgets, NO talking heads"
  - label: "Custom"
    description: "Specify your own art + tone or preset"
```

**Preset vs Art+Tone**: Presets include special rules beyond art+tone. `ohmsha` = manga + neutral + visual metaphor rules + character roles + NO talking heads. Plain `manga + neutral` does NOT include these rules.

**Question 2: Narrative Focus** (multiSelect: true)
```
header: "Focus"
question: "What should the comic emphasize? (Select all that apply)"
options:
  - label: "Biography/life story"
    description: "Follow a person's journey through key life events"
  - label: "Concept explanation"
    description: "Break down complex ideas visually"
  - label: "Historical event"
    description: "Dramatize important historical moments"
  - label: "Tutorial/how-to"
    description: "Step-by-step educational guide"
```

**Question 3: Target Audience**
```
header: "Audience"
question: "Who is the primary reader?"
options:
  - label: "General readers"
    description: "Broad appeal, accessible content"
  - label: "Students/learners"
    description: "Educational focus, clear explanations"
  - label: "Industry professionals"
    description: "Technical depth, domain knowledge"
  - label: "Children/young readers"
    description: "Simplified language, engaging visuals"
```

**Question 4: Outline Review**
```
header: "Review"
question: "Do you want to review the outline before image generation?"
options:
  - label: "Yes, let me review (Recommended)"
    description: "Review storyboard and characters before generating images"
  - label: "No, generate directly"
    description: "Skip outline review, start generating immediately"
```

**After response**:
1. Update `analysis.md` with user preferences
2. **Store `skip_outline_review`** flag based on Question 4 response
3. → Step 3

### Step 3: Generate Storyboard + Characters

Create storyboard and character definitions using the confirmed style from Step 2.

**Loading Style References**:
- Art style: `references/art-styles/{art}.md`
- Tone: `references/tones/{tone}.md`
- If preset (ohmsha/wuxia/shoujo): also load `references/presets/{preset}.md`

**Generate**:

1. **Storyboard** (`storyboard.md`):
   - YAML front matter with art_style, tone, layout, aspect_ratio
   - Cover design
   - Each page: layout, panel breakdown, visual prompts
   - **Written in user's preferred language** (from Step 1)
   - Reference: `references/storyboard-template.md`
   - **If using preset**: Load and apply preset rules from `references/presets/`

2. **Character definitions** (`characters/characters.md`):
   - Visual specs matching the art style (in user's preferred language)
   - Include Reference Sheet Prompt for later image generation
   - Reference: `references/character-template.md`

**After generation**:
- If `skip_outline_review` is true → Skip Step 4, go directly to Step 5
- If `skip_outline_review` is false → Continue to Step 4

### Step 4: Confirmation 2 - Review Outline (Conditional)

**Skip this step** if user selected "No, generate directly" in Step 2.

**Purpose**: User reviews and confirms storyboard + characters before generation.

**Display**:
- Page count and structure
- Art style + Tone combination
- Page-by-page summary (Cover → P1 → P2...)
- Character list with brief descriptions

**Use AskUserQuestion**:

```
header: "Confirm"
question: "Ready to generate images with this outline?"
options:
  - label: "Yes, proceed (Recommended)"
    description: "Generate character sheet and comic pages"
  - label: "Edit storyboard first"
    description: "I'll modify storyboard.md before continuing"
  - label: "Edit characters first"
    description: "I'll modify characters/characters.md before continuing"
  - label: "Edit both"
    description: "I'll modify both files before continuing"
```

**After response**:
1. If user wants to edit → Wait for user to finish editing, then ask again
2. If user confirms → Continue to Step 5

### Step 5: Generate Images

With confirmed storyboard + art style + tone + aspect ratio:

**Style Reference Loading**:
- Read `references/art-styles/{art}.md` for rendering guidelines
- Read `references/tones/{tone}.md` for mood/color adjustments
- If preset: Read `references/presets/{preset}.md` for special rules

**5.1 Generate Character Reference Sheet** (first):
1. Use Reference Sheet Prompt from `characters/characters.md`
2. Generate → `characters/characters.png`
3. This ensures visual consistency for all subsequent pages

**5.2 Generate Comic Pages**:

**For each page (cover + pages)**:
1. Save prompt to `prompts/NN-{cover|page}-[slug].md` (in user's preferred language)
2. Generate image using confirmed art style and tone guidelines
3. Report progress after each generation

**Watermark Application** (if enabled in preferences):
Add to each image generation prompt:
```
Include a subtle watermark "[content]" positioned at [position]
with approximately [opacity*100]% visibility. The watermark should
be legible but not distracting from the comic panels and storytelling.
Ensure watermark does not overlap speech bubbles or key action.
```
Reference: `references/config/watermark-guide.md`

**Image Generation Skill Selection**:
- Check available image generation skills
- If multiple skills available, ask user preference

**Character Reference Handling** (IMPORTANT for visual consistency):

1. Read the selected image generation skill's SKILL.md
2. Check if it supports reference image input (look for parameters like `--ref`, `--reference`, `--image-ref`, etc.)

| Skill Support | Action |
|---------------|--------|
| **Supports reference image** | Pass `characters/characters.png` using the skill's reference parameter |
| **Does NOT support reference image** | Prepend `characters/characters.md` content to each page prompt |

Always verify the exact parameter name from the skill's documentation before calling.

**Session Management**:
If image generation skill supports `--sessionId`:
1. Generate unique session ID: `comic-{topic-slug}-{timestamp}`
2. Use same session ID for all pages
3. Ensures visual consistency across generated images

### Step 6: Merge to PDF

After all images generated:

```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <comic-dir>
```

Creates `{topic-slug}.pdf` with all pages as full-page images.

### Step 7: Completion Report

```
Comic Complete!
Title: [title] | Art: [art] | Tone: [tone] | Pages: [count] | Aspect: [ratio] | Language: [lang]
Watermark: [enabled/disabled]
Location: [path]
✓ analysis.md
✓ characters.png
✓ 00-cover-[slug].png ... NN-page-[slug].png
✓ {topic-slug}.pdf
```

## Page Modification

| Action | Steps |
|--------|-------|
| **Edit** | Update prompt → Regenerate image → Regenerate PDF |
| **Add** | Create prompt at position → Generate image → Renumber subsequent (NN+1) → Update storyboard → Regenerate PDF |
| **Delete** | Remove files → Renumber subsequent (NN-1) → Update storyboard → Regenerate PDF |

**File naming**: `NN-{cover|page}-[slug].png` (e.g., `03-page-enigma-machine.png`)
- Slugs: kebab-case, unique, derived from content
- Renumbering: Update NN prefix only, slugs unchanged

## Preset: Ohmsha

Default: Use Doraemon characters (大雄=learner, 哆啦A梦=mentor, 胖虎=challenge, 静香=support). Custom characters via `--characters "Student:小明,Mentor:教授"` or character presets in EXTEND.md.

Requirements: Visual metaphors, NO talking heads, narrative page titles.

See `references/presets/ohmsha.md` and `references/ohmsha-guide.md` for details.

## References

Detailed templates and guidelines in `references/` directory:

**Core Templates**:
- `analysis-framework.md` - Deep content analysis for comic adaptation
- `character-template.md` - Character definition format and examples
- `storyboard-template.md` - Storyboard structure and panel breakdown
- `ohmsha-guide.md` - Ohmsha manga style specifics

**Style Definitions** (new 3-dimension system):
- `art-styles/` - Art style definitions (ligne-claire, manga, realistic, ink-brush, chalk)
- `tones/` - Tone definitions (neutral, warm, dramatic, romantic, energetic, vintage, action)
- `presets/` - Preset shortcuts with special rules (ohmsha, wuxia, shoujo)
- `layouts/` - Layout definitions (standard, cinematic, dense, splash, mixed, webtoon)

**Config**:
- `config/preferences-schema.md` - EXTEND.md schema
- `config/first-time-setup.md` - First-time setup flow
- `config/watermark-guide.md` - Watermark configuration

## Notes

- Auto-retry once on failure | Cartoon alternatives for sensitive figures
- Use confirmed language preference | Maintain style consistency
- **Step 2 confirmation required** - do not skip (style selection + outline review option)
- **Step 4 conditional** - only if user requested outline review in Step 2
- Watermark/language configured once in EXTEND.md, not asked in confirmations

## Extension Support

Custom configurations via EXTEND.md. See **Step 1.1** for paths and supported options.
