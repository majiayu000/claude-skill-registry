---
name: paper-comic
description: |
  Generate educational comics from academic papers, using visual storytelling to explain core ideas and innovations.
  Supports 4 art styles: classic (clean lines), tech (futuristic), warm (friendly), chalk (blackboard).
  Uses genimg-gemini-web to generate images.
---

# Paper Comic - Academic Paper to Comic Generator

Transform academic papers into coherent educational comics, making complex concepts easier to understand through visual storytelling.

## Usage

```bash
/paper-comic /path/to/paper.pdf
/paper-comic /path/to/paper.pdf --style tech
/paper-comic  # Then paste the paper content
```

## Art Style Options

| Style | Features | Suitable Papers |
|-------|-----------|-----------------|
| **classic** | Clean-line style, simple and professional, easy to read | General purpose, most papers (default) |
| **tech** | Futuristic look, circuit and neon elements | AI/Computer/Engineering papers |
| **warm** | Gentle tone, nostalgic feeling, approachable | Psychology/Cognitive Science/Education |
| **chalk** | Blackboard effect, academic atmosphere | Math/Physics/Theoretical papers |

## Output Structure

```
[output-dir]/
├── outline.md           # Storyboard and scene outline
├── characters/
│   ├── characters.md    # Character definitions
│   └── characters.png   # Character reference image
├── prompts/
│   ├── 00-cover.md      # Cover prompt
│   └── XX-page.md       # Page prompts
├── 00-cover.png         # Cover page
└── XX-page.png          # Comic pages
```

**Output Directory**:
- If source files exist: `[source-dir]/comic/`
- If no source files: `comic-outputs/YYYY-MM-DD/[topic-slug]/`

## Workflow

### Step 1: Analyze the Paper

1. Read paper content (PDF or Markdown)
2. Extract key information:
   - Paper title and authors
   - Research background and motivation
   - Core innovations (1–3)
   - Key methods/algorithms
   - Main experimental results
3. Automatically recommend an art style based on the paper field (or use user-specified style)

### Step 2: Design Narrative Structure

**Four-part structure** (suitable for 8–12 pages of comic):

| Stage | Pages | Content |
|--------|--------|---------|
| **Introduction** | 1–2 pages | Problem background — why the research is needed |
| **Exploration** | 2–3 pages | Limitations of existing methods, leading to innovation |
| **Core** | 3–5 pages | Explain the innovation in detail, visualized with metaphors |
| **Summary** | 1–2 pages | Experimental results, significance, and future outlook |

### Step 3: Define Characters

Create `characters/characters.md`:

**Required characters**:
- **Mentor**: The explainer, wise and approachable
- **Student**: Represents the reader, asks questions and learns
- **Concept embodiment** (optional): A personified version of an abstract concept

**Character consistency rules**:
- Mentor and student must appear in ≥60% of pages
- Each page should clearly list appearing characters
- Character design must remain consistent throughout all pages

### Step 4: Create Storyboard

Create `outline.md`, containing:
- Metadata (title, art style, page count)
- Cover design
- Panel layout and content of each page

**Storyboard rules**:
- Each page has 3–5 panels
- Note which characters, scenes, and dialogue appear in each panel
- All dialogue must be written in Chinese
- Formulas should be represented visually, not as text formulas

### Step 5: Generate Images

Use genimg-gemini-web to generate images (requires Google account authentication):

```bash
# Get skill installation path (assuming installed via npx skills add)
SKILL_DIR="$HOME/.claude/skills/genimg-gemini-web"
# Or if located elsewhere:
# SKILL_DIR="$HOME/.codex/skills/genimg-gemini-web"

# Generate character reference image
npx -y bun "$SKILL_DIR/scripts/main.ts" \
  --promptfiles references/base-prompt.md characters/characters.md \
  --image characters/characters.png \
  --sessionId comic-[topic]-[timestamp]

# Generate pages (use the same sessionId for consistency)
npx -y bun "$SKILL_DIR/scripts/main.ts" \
  --promptfiles references/base-prompt.md prompts/XX-page.md \
  --image XX-page.png \
  --sessionId comic-[topic]-[timestamp]
```

**Important**: Use the same `--sessionId` across all runs to ensure consistent character appearance.

**First run**: Chrome will open for Google account authentication; cookies will then be cached.

### Step 6: Generate Final Document

Generate `[topic]-paper-comic.md`:

```markdown
# [Paper Title] - Comic Interpretation

## Overview
- **Paper**: [Title]
- **Art Style**: [Selected Style]
- **Pages**: [N]
- **Generated on**: [YYYY-MM-DD]

## Comic Pages

### Cover


### Page 1

**Content**: [Brief summary of this page’s content]

...

## Core Knowledge Points
1. [Concept 1]
2. [Concept 2]
3. [Concept 3]
```

## Key Principles

### Text Requirements
- **All dialogue and narration must be in Chinese**
- Professional terms: Chinese + English, e.g., “梯度下降 (Gradient Descent)”
- Text must be clear and readable

### Formula Handling
- **Do not write formulas as text**
- Use visual or metaphorical representations instead
- Example: Gradient descent → draw a small ball rolling down a hill

### Visual Consistency
- Characters’ appearance must remain consistent
- Scene style should be uniform
- Narrative logic should flow clearly and progressively

## Reference Files

- `references/base-prompt.md` - Base prompt template
- `references/styles/classic.md` - Clean-line style
- `references/styles/tech.md` - Tech style
- `references/styles/warm.md` - Warm style
- `references/styles/chalk.md` - Chalkboard style
