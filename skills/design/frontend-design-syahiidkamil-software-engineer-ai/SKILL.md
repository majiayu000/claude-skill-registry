---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
original_source: Modified from anthropics/claude-code-skills, licensed under Apache 2.0
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Step 1: Context-Driven Design Reasoning

Before any aesthetic choices, use deductive reasoning to derive the right design from the context:

- **Domain**: What is this? (enterprise SaaS, creative portfolio, fintech, healthcare, e-commerce, etc.)
- **Audience**: Who uses this? A CFO expects different visual language than a teenager. A developer tool looks different from a wedding planner.
- **Tone**: Professional? Playful? Trustworthy? Edgy? The context dictates this — don't pick a tone arbitrarily.
- **Visual Appropriateness**: Does a gradient help or hurt? A law firm landing page with neon gradients destroys trust. A music app without color energy feels dead. Every visual choice must survive the question: "Does this serve the context?"

Derive the design from the problem, don't impose a style onto it.

## Step 2: Break the Probability Bias

LLMs are next-token predictors optimized via backpropagation. This creates a natural bias toward the most statistically probable (generic) output. To counter this:

1. **Generate 5 design directions** ranging from highest probability (most generic/expected) to lowest probability (most unexpected/distinctive)
2. **Scrutinize the top 1-2** — these are the AI slop zone. Don't default to them, but individual elements may still work if they genuinely serve the context
3. **Cherry-pick across all 5** — select elements that are distinctive yet contextually appropriate, regardless of which tier they came from
4. **Combine deliberately** — merge the best unconventional choices into one cohesive direction

Present the chosen direction to the user briefly before implementing. This ensures every design is intentionally de-biased.

## Step 3: Think in Pure HTML/CSS/JS First

LLMs have deepest mastery over raw web fundamentals. Use this to your advantage:

- **Design in HTML/CSS/JS mentally first** — even if the target is React/Vue/Svelte. The browser is the ground truth.
- **Prototype the visual in vanilla form** — CSS is where the design lives. Get the aesthetics right at this layer.
- **Then translate** to the target framework/component structure. The conversion is mechanical; the design thinking is not.

This prevents framework abstractions from flattening creative choices.

## Step 4: Curate and Verify

Adopt the mindset of a senior UI/UX Designer — someone who both solves usability problems and crafts visually beautiful, creative interfaces. Evaluate the output through that expert lens:

- **UX Review**: Does the layout guide the user's eye correctly? Is the information hierarchy clear? Are interactive elements discoverable and intuitive? Would a real designer approve the flow?
- **Visual Design Review**: Step back and judge the aesthetics as a designer would. Does the composition feel balanced and intentional? Do colors, typography, and spacing work together harmoniously? Is there a clear visual identity?
- **Ask the user to verify**: Request the user to paste a screenshot of the rendered result, or if browser tools (Playwright) are available, use them to view the output directly.
- **Iterate like a designer**: Refine based on what's actually rendered, not what the code theoretically produces. Adjust spacing by pixels, tweak color values, fine-tune font weights — the details are the design.

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.
