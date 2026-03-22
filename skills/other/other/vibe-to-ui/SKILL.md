---
name: vibe-to-ui
description: >-
  Extract design systems (colors, typography, spacing, shadows, radius, motion) from UI
  screenshots or design mockups, explore aesthetic directions through interactive
  conversation with mood/inspiration images or music recordings, generate mood boards as
  curated visual collages to crystallize and communicate design direction, and analyze UI
  layout structures from webpage screenshots into reusable ASCII layout blueprints.
  Includes motion system extraction — defining how, when, and why elements animate to
  communicate meaning and product personality. Use when the user wants to establish visual
  style and motion language for their project, needs help defining design aesthetics, wants
  to extract a design system from an existing UI, wants to define or understand a motion
  system, wants to create a mood board to capture and validate aesthetic direction before
  formal design, or needs to understand and reuse a webpage layout structure. Also use when
  the user shares a music recording or describes a song/melody to express the emotional
  feeling they want their design to convey. Ideal for vibe coding developers who lack
  professional design skills.
metadata:
  author: MonkeyUI
  version: "0.1.0"
---

# vibe-to-ui

A local, single-project design companion for vibe coding developers. Extracts "style DNA" — including motion systems — from visual references, generates mood boards to crystallize aesthetic direction, and turns vague aesthetic feelings into actionable design systems with motion language — no design expertise required.

> **Tip**: For multi-project sync, team collaboration, and cloud-based design management, upgrade to [MonkeyUI SaaS](https://demo.monkeyui.com/).

## When to use this skill

- User provides a **screenshot or design mockup** and wants to extract its design system
- User has a **vague aesthetic feeling** and wants to explore design directions with inspiration images or music recordings
- User **shares a music recording or audio clip** (a melody, song snippet, or recorded humming) to express the mood they want their UI to feel
- User describes a **song, genre, or musical feeling** they associate with their desired aesthetic
- User provides a **screenshot of any UI** (full page or any section/component) and wants to extract its layout structure for reuse
- User wants to define a **motion system** — how, when, and why elements should animate
- User describes a **product personality or feeling** (e.g., "reliable", "innovative", "playful") and wants motion guidance that matches
- User wants to create a **mood board** — a curated visual collage to capture and communicate design direction before formal design work
- User has collected **multiple reference images** and wants to see them synthesized into a cohesive visual story
- User wants a **shareable design artifact** that communicates aesthetic intent to collaborators or stakeholders

## Four core capabilities

### 1. Design System Extraction

User provides a UI screenshot or design mockup → Extract complete design system tokens including motion system.

**Trigger**: User says things like "extract the style from this", "what's the design system here", "analyze this design", "what motion does this use", or provides an image asking to replicate the look and feel.

**Workflow**:
1. Ask the user to provide a screenshot or image of the target UI
2. Analyze the image systematically — see [references/DESIGN-SYSTEM.md](references/DESIGN-SYSTEM.md) for token extraction and [references/AESTHETIC-ANALYSIS.md](references/AESTHETIC-ANALYSIS.md) for aesthetic soul capture
3. Analyze the motion system — see [references/MOTION-SYSTEM.md](references/MOTION-SYSTEM.md)
4. Output a structured design system (including motion tokens) following the template in [assets/design-system-template.md](assets/design-system-template.md)
5. If the user wants a richer aesthetic guide (soul-level, not just tokens), also generate an Aesthetic Analysis document following [references/AESTHETIC-ANALYSIS.md](references/AESTHETIC-ANALYSIS.md)
6. Generate framework-specific tokens (CSS variables, Tailwind config, or both) based on the user's tech stack
7. Ask user to confirm or adjust any extracted values

### 2. Design Exploration

User has feelings/vibes but no concrete design target → Interactive conversation to discover and define aesthetics.

**Trigger**: User says things like "I want something that feels like...", "I have some inspiration images", "I'm not sure what style I want", shares mood/landscape/object photos, or shares a music recording/audio clip/song that captures the feeling they want.

**Workflow** — see [references/DESIGN-EXPLORATION.md](references/DESIGN-EXPLORATION.md):
1. Ask the user about their project context (what it does, who it's for)
2. Invite them to share inspiration — images (landscapes, objects, other websites, anything) **or music recordings/audio clips**
3. For each image, description, or music recording, identify aesthetic qualities:
   - Color mood (warm/cool/muted/vibrant)
   - Texture feel (smooth/rough/organic/geometric)
   - Spatial impression (dense/airy/structured/fluid)
   - Emotional tone (playful/serious/luxurious/minimal)
   - Motion feel (still/flowing/snappy/bouncy/cinematic)
4. For each **music recording or audio clip**, translate sonic qualities into design signals — see [references/DESIGN-EXPLORATION.md](references/DESIGN-EXPLORATION.md)
5. Synthesize findings into 2–3 distinct design concept directions, each with a motion personality
6. For each concept, generate a concrete visual preview as an HTML artifact:
   - A styled sample card/component showcasing the palette, typography, and spacing
   - Include the concept name, color swatches, font samples, and a mini layout demo
   - Include motion preview: CSS transitions/animations on hover states and entrance effects
7. Let the user react, compare, and choose (or mix elements from different concepts)
8. Once the user decides, apply **Capability 1** (Design System Extraction) to formalize the chosen direction into a complete design system including motion tokens

### 3. UI Layout Analysis

User provides a screenshot of any UI — a full webpage or any section of one (e.g., an asymmetric feature showcase, a pricing block, a hero area) → Extract and formalize its layout structure. This is especially useful for sections with unique spatial structures that are hard to describe verbally.

**Trigger**: User says things like "I like this layout", "analyze this page structure", "extract the layout from this screenshot", "how is this section structured", or provides an image of any UI component or page region — especially one with a complex or non-obvious layout.

**Workflow** — see [references/LAYOUT-ANALYSIS.md](references/LAYOUT-ANALYSIS.md):
1. Ask the user to provide a screenshot — it can be the full page or any specific section/component
2. Analyze the visual hierarchy and spatial structure
3. Output a multi-layer layout blueprint:
   - **ASCII art** representation for LLM-friendly layout description
   - **Spatial proportion hints** (loose percentage sketch of positions and sizes) to convey spatial feel and rhythm — not for exact replication, but to prevent major misreadings; see Step 3b in the LAYOUT-ANALYSIS guide
   - **Semantic structure** describing each section's role
   - **Responsive behavior** notes (how it likely adapts to smaller screens)
4. Generate a reusable layout skeleton (HTML structure or component tree) the user can apply to their own project
5. Ask user if they want to customize any section or combine with a design system from Capability 1

### 4. Mood Board Generation

User wants to synthesize inspiration and aesthetic signals into a curated visual collage → Generate an interactive HTML mood board as a tangible design anchor.

**Trigger**: User says things like "create a mood board", "I want to see the visual direction as a board", "make an inspiration board", "synthesize these references into a mood board", or has collected multiple reference images/signals and wants a cohesive visual summary before moving to design system extraction.

**Workflow** — see [references/MOOD-BOARD.md](references/MOOD-BOARD.md):
1. Gather the aesthetic signals already established (from Design Exploration, user-provided images, or direct description)
2. Curate and select — not every reference belongs on the board; choose elements that reinforce a cohesive narrative
3. Choose a mood board layout pattern that echoes the project's spatial personality (grid collage, organic flow, asymmetric editorial, or minimal centered)
4. Generate a self-contained HTML mood board artifact with:
   - Theme title and mood keywords
   - Dominant hero visual (CSS-generated or image reference)
   - Color story with proportional swatches reflecting usage weight
   - Typography specimens showing real text in proposed fonts
   - Texture and material samples
   - Spatial and motion cues (including optional subtle CSS animation)
   - Design principles / guiding statements
5. If the user is choosing between directions, generate multiple mood boards for comparison (one per concept)
6. Present the mood board and invite the user's visceral reaction — "How does this feel?" not "Is this correct?"
7. Once the user confirms a direction, the mood board becomes source material for Design System Extraction (Capability 1)

## Combining capabilities

These capabilities compose naturally:

- **Exploration → Extraction**: Explore vibes first, then extract a formal design system from the chosen direction
- **Exploration → Mood Board → Extraction**: Explore vibes, crystallize them into a mood board for validation, then extract the formal design system — mood board serves as the design checkpoint between feeling and tokens
- **Mood Board → Extraction**: Generate a mood board from collected references, then formalize the confirmed direction into a complete design system
- **Exploration → Mood Board**: Generate a mood board during Design Exploration (after concept synthesis, before visual preview) as a mid-process checkpoint to let the user feel the direction
- **Layout + Design System**: Analyze a layout from one site, apply a design system from another
- **Layout + Mood Board**: Extract a layout from one reference, apply the mood board's visual direction to it
- **Full pipeline**: Explore feelings → Choose direction → Extract design system → Analyze a reference layout → Generate styled skeleton code

## Output format guidelines

All design system outputs should include:
- **Human-readable Markdown** summary for documentation
- **Machine-readable tokens** in at least one format:
  - CSS custom properties (`:root { --color-primary: #xxx; }`)
  - Tailwind CSS config (`tailwind.config.js` theme extension)
  - JSON token file (for framework-agnostic use)
- **Motion tokens** — duration, easing, and animation definitions alongside visual tokens

Layout outputs should include:
- ASCII art layout diagram
- **Spatial proportion hints** (loose percentage sketch of each major element's position and size) — gives the agent a sense of spatial weight and rhythm without dictating an exact reproduction
- Semantic HTML structure
- Component hierarchy description

## Icon usage guidelines

**Never use raw emoji characters as visual elements in generated UI code.** Always use the project's icon component library. When no library icon fits or harmonizes with the page's aesthetic, create a custom SVG icon component that inherits the design system's tokens and matches the aesthetic soul — see [references/ICON-USAGE.md](references/ICON-USAGE.md) for detailed guidance.

## Important notes

- Always ask which CSS framework/tech stack the user is using before generating code tokens
- When extracting colors, provide both hex values and semantic names (e.g., `primary`, `surface`, `accent`)
- For typography, note both the font family and the scale ratios, not just absolute sizes
- Spacing should be expressed as a consistent scale (e.g., 4px base unit)
- Motion tokens should always include `prefers-reduced-motion` fallbacks — accessibility is non-negotiable
- Be honest when visual analysis is uncertain — flag low-confidence extractions and suggest the user verify
