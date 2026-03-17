---
name: aesthetic
description: |
  Design IMPROVEMENT and iteration using Gemini API. Score designs, generate alternatives, extract design tokens.

  ALWAYS use for: "beautiful", "improve design", "better UI", "modern look", "aesthetic", "beau", "améliorer", "moderniser".
  DO NOT use for: quick bug debugging (overflow, cut-off) → use "vision-analyzer" agent instead.

  Workflow: Analyze (gemini-2.5-pro) → Generate improved (gemini-3-pro-image-preview) → Score → Iterate until ≥7/10.
---

# Aesthetic

Create aesthetically beautiful interfaces by following proven design principles and systematic workflows.

## When to Use This Skill

Use when:
- Building or designing user interfaces
- Analyzing designs from inspiration websites (Dribbble, Mobbin, Behance)
- Generating design images and evaluating aesthetic quality
- Implementing visual hierarchy, typography, color theory
- Adding micro-interactions and animations
- Creating design documentation and style guides
- Need guidance on accessibility and design systems

## Core Framework: Four-Stage Approach

### 1. BEAUTIFUL: Understanding Aesthetics
Study existing designs, identify patterns, extract principles. AI lacks aesthetic sense—standards must come from analyzing high-quality examples and aligning with market tastes.

**Reference**: [`references/design-principles.md`](references/design-principles.md) - Visual hierarchy, typography, color theory, white space principles.

### 2. RIGHT: Ensuring Functionality
Beautiful designs lacking usability are worthless. Study design systems, component architecture, accessibility requirements.

**Reference**: [`references/design-principles.md`](references/design-principles.md) - Design systems, component libraries, WCAG accessibility standards.

### 3. SATISFYING: Micro-Interactions
Incorporate subtle animations with appropriate timing (150-300ms), easing curves (ease-out for entry, ease-in for exit), sequential delays.

**Reference**: [`references/micro-interactions.md`](references/micro-interactions.md) - Duration guidelines, easing curves, performance optimization.

### 4. PEAK: Storytelling Through Design
Elevate with narrative elements—parallax effects, particle systems, thematic consistency. Use restraint: "too much of anything isn't good."

**Reference**: [`references/storytelling-design.md`](references/storytelling-design.md) - Narrative elements, scroll-based storytelling, interactive techniques.

## Workflows

### Workflow 0: Improve Existing UI (Primary Use Case)

**Purpose**: Take a screenshot of current UI and iteratively improve it using Gemini vision + generation.

**Prerequisites**:
- `GEMINI_API_KEY` configured (see `skills/ai-multimodal/SKILL.md`)
- Image path available (drag & drop or provide path)

**Steps**:

#### Step 1: Analyze Current Design

```bash
# Analyze the current UI and get a score
~/.claude/skills/ai-multimodal/scripts/run.sh gemini_batch_process.py \
  --files "/path/to/current-ui.png" \
  --task analyze \
  --prompt "Rate this UI design from 1-10 on these criteria:
    - Visual hierarchy (1-10)
    - Color harmony (1-10)
    - Typography (1-10)
    - Spacing & layout (1-10)
    - Modern feel (1-10)
    - Overall aesthetic (1-10)

    List the TOP 3 weaknesses to fix.
    List the TOP 3 strengths to preserve.
    Suggest specific improvements." \
  --model gemini-2.5-pro \
  --output /tmp/design-analysis.md
```

#### Step 2: Generate Improved Design

Based on analysis, create a design generation prompt:

```bash
~/.claude/skills/ai-multimodal/scripts/run.sh gemini_batch_process.py \
  --task generate \
  --prompt "Modern UI design for [PAGE TYPE].

PRESERVE from original:
- [Strength 1 from analysis]
- [Strength 2 from analysis]

IMPROVE:
- [Weakness 1] -> [Specific improvement]
- [Weakness 2] -> [Specific improvement]
- [Weakness 3] -> [Specific improvement]

STYLE: Clean, modern, professional
COLORS: [Extracted or improved palette]
LAYOUT: [Description based on original structure]
COMPONENTS: [Key components to include]" \
  --model gemini-3-pro-image-preview \
  --output /tmp/design-v1 \
  --aspect-ratio 16:9
```

#### Step 3: Score Generated Design

```bash
~/.claude/skills/ai-multimodal/scripts/run.sh gemini_batch_process.py \
  --files "/tmp/design-v1.png" \
  --task analyze \
  --prompt "Rate this generated UI design 1-10:
    - Does it look professional and polished?
    - Is the visual hierarchy clear?
    - Are colors harmonious?
    - Would this work as a real product?

    Overall score (1-10):
    If score < 7, list SPECIFIC fixes needed." \
  --model gemini-2.5-pro \
  --output /tmp/design-v1-score.md
```

#### Step 4: Iterate Until Score >= 7

```
LOOP:
  IF score >= 7:
    DONE - proceed to implementation
  ELSE:
    Refine prompt with specific fixes
    Regenerate design
    Re-score
    Continue until score >= 7 or max 3 iterations
```

#### Step 5: Extract Implementation Specs

```bash
~/.claude/skills/ai-multimodal/scripts/run.sh gemini_batch_process.py \
  --files "/tmp/design-final.png" \
  --task extract \
  --prompt "Extract implementation specs from this design:

1. COLOR PALETTE (hex codes):
   - Primary:
   - Secondary:
   - Background:
   - Text:
   - Accent:

2. TYPOGRAPHY:
   - Headings: font, size, weight
   - Body: font, size, weight
   - Labels: font, size, weight

3. SPACING SYSTEM:
   - Base unit (px):
   - Common paddings:
   - Common margins:

4. COMPONENTS TO CREATE:
   - [Component name]: [Brief description]

5. TAILWIND CLASSES SUGGESTIONS:
   - [Component]: [Suggested classes]

Return as JSON." \
  --model gemini-2.5-pro \
  --format json \
  --output /tmp/design-specs.json
```

#### Step 6: Implement

Use the extracted specs to modify code:
- Update Tailwind config with colors
- Create/modify components
- Apply typography and spacing

**Quick Command** (all-in-one):
```bash
# Store in a shell function for quick access
design-improve() {
  local img="$1"
  local output="${2:-/tmp/design-improved}"

  echo "1. Analyzing current design..."
  ~/.claude/skills/ai-multimodal/scripts/run.sh gemini_batch_process.py \
    --files "$img" --task analyze \
    --prompt "Rate 1-10, list top 3 weaknesses and improvements" \
    --model gemini-2.5-pro --output "${output}-analysis.md"

  echo "Analysis saved to ${output}-analysis.md"
  echo "2. Review analysis, then run design generation with refined prompt"
}
```

---

### Workflow 1: Capture & Analyze Inspiration

**Purpose**: Extract design guidelines from inspiration websites.

**Steps**:
1. Browse inspiration sites (Dribbble, Mobbin, Behance, Awwwards)
2. Use **chrome-devtools** skill to capture full-screen screenshots (not full page)
3. Use **ai-multimodal** skill to analyze screenshots and extract:
   - Design style (Minimalism, Glassmorphism, Neo-brutalism, etc.)
   - Layout structure & grid systems
   - Typography system & hierarchy
     **IMPORTANT:** Try to predict the font name (Google Fonts) and font size in the given screenshot, don't just use Inter or Poppins.
   - Color palette with hex codes
   - Visual hierarchy techniques
   - Component patterns & styling
   - Micro-interactions
   - Accessibility considerations
   - Overall aesthetic quality rating (1-10)
4. Document findings in project design guidelines using templates

### Workflow 2: Generate & Iterate Design Images

**Purpose**: Create aesthetically pleasing design images through iteration.

**Steps**:
1. Define design prompt with: style, colors, typography, audience, animation specs
2. Use **ai-multimodal** skill to generate design images with Gemini API
3. Use **ai-multimodal** skill to analyze output images and evaluate aesthetic quality
4. If score < 7/10 or fails professional standards:
   - Identify specific weaknesses (color, typography, layout, spacing, hierarchy)
   - Refine prompt with improvements
   - Regenerate with **ai-multimodal** or use **media-processing** skill to modify outputs (resize, crop, filters, composition)
5. Repeat until aesthetic standards met (score ≥ 7/10)
6. Document final design decisions using templates

## Design Documentation

### Create Design Guidelines
Use [`assets/design-guideline-template.md`](assets/design-guideline-template.md) to document:
- Color patterns & psychology
- Typography system & hierarchy
- Layout principles & spacing
- Component styling standards
- Accessibility considerations
- Design highlights & rationale

Save in project `./docs/design-guideline.md`.

### Create Design Story
Use [`assets/design-story-template.md`](assets/design-story-template.md) to document:
- Narrative elements & themes
- Emotional journey
- User journey & peak moments
- Design decision rationale

Save in project `./docs/design-story.md`.

## Resources & Integration

### Related Skills
- **ai-multimodal**: Analyze documents, screenshots & videos, generate design images, edit generated images, evaluate aesthetic quality using Gemini API
- **chrome-devtools**: Capture full-screen screenshots from inspiration websites, navigate between pages, interact with elements, read console logs & network requests
- **media-processing**: Refine generated images (FFmpeg for video, ImageMagick for images)
- **ui-styling**: Implement designs with shadcn/ui components + Tailwind CSS utility-first styling
- **web-frameworks**: Build with Next.js (App Router, Server Components, SSR/SSG)

### Reference Documentation
**References**: [`references/design-resources.md`](references/design-resources.md) - Inspiration platforms, design systems, AI tools, MCP integrations, development strategies.

## Key Principles

1. Aesthetic standards come from humans, not AI—study quality examples
2. Iterate based on analysis—never settle for first output
3. Balance beauty with functionality and accessibility
4. Document decisions for consistency across development
5. Use progressive disclosure in design—reveal complexity gradually
6. Always evaluate aesthetic quality objectively (score ≥ 7/10)
