---
name: new-presentation
description: Create powerful presentations using Steve Jobs's 3-Second Rule methodology. Applies the Billboard Test principles for minimal cognitive load, maximum visual impact, and elegant slide design. Use when creating product launches, pitches, explanations, or any live presentation that requires high audience retention and visual clarity. Automatically integrates with Claude's PPTX skill to generate professional PowerPoint files and always applies the Sentient Brand Guidelines skill to ensure consistent branding.
---

# Presentation Jobs - Steve Jobs Methodology

Create presentations following Steve Jobs's legendary minimalist approach, centered on the "Billboard Test" (3-Second Rule) for maximum impact and audience retention.

## When to Use This Skill

Use this skill whenever you need to create a presentation that:
- Launches a product or feature
- Pitches a business idea or proposal
- Explains complex concepts simply
- Delivers keynotes or important announcements
- Requires high audience engagement and retention

## Core Workflow

### Step 1: Understand the Request and Gather Information

Before creating the presentation, ask clarifying questions if needed:

**Essential Information:**
- **Topic/Purpose**: What is the presentation about? What's the main goal?
- **Audience**: Who will be viewing this? (executives, customers, team, investors, etc.)
- **Key Message**: What's the single most important takeaway?
- **Duration**: How long is the presentation? (helps determine slide count)
- **Content Details**: Any specific points, data, or stories to include?

**Optional Information:**
- Brand colors or visual preferences
- Existing materials to reference
- Specific examples or demos to showcase

If the user provides clear context, proceed directly to Step 2. Only ask questions when information is genuinely ambiguous or missing.

### Step 2: Read the Steve Jobs Guidelines

**MANDATORY:** Before designing any slides, read the complete Steve Jobs guidelines:
```
Read references/jobs-guidelines.md
```

This file contains the essential principles you must follow:
- The Billboard Test (3-Second Rule)
- Cognitive load minimization
- Content minimalism guidelines
- Visual design standards
- The presenter's role

### Step 2B: Apply Sentient Brand Guidelines

For every presentation, **review the Sentient Brand Guidelines skill** to apply the correct colors, typography, and logo usage:

```
Read sentient-brand-guideline/skill.md
```

Key alignment points:
- Use Sentient.io-approved logo assets and placement rules.
- Apply the official color palette (Primary Red, Beige, Green, and supporting tones) and Nunito Sans/Noto Sans typography.
- Follow the spacing, contrast, and naming conventions detailed in the guidelines.

### Step 3: Structure the Presentation

Apply the Steve Jobs 3-act storytelling structure:

**Act 1: Setup (20-30% of slides)**
- Hook the audience with a problem or opportunity
- Set context and create anticipation
- Example: "There are three products in one..."

**Act 2: Confrontation (40-50% of slides)**
- Introduce the solution/product/idea
- Demonstrate key features or concepts (one per slide)
- Use visuals and benefits, not just features
- Build emotional connection

**Act 3: Resolution (20-30% of slides)**
- Show the impact and transformation
- Call to action
- Memorable closing message

**Default Slide Count:** Target 10 slides maximum unless content complexity requires more. Quality over quantity.

### Step 4: Design Each Slide (Following the 3-Second Rule)

For EVERY slide, strictly adhere to these principles from the guidelines:

**Content Rules:**
1. **One idea per slide** - If you have multiple ideas, create multiple slides
2. **Minimal text** - Use keywords and short phrases, never paragraphs
3. **One number** - If showing data, highlight only ONE statistic prominently
4. **No bullet point overload** - Use bullets sparingly; prefer visual hierarchy

**Visual Rules:**
1. **Large, impactful visuals** - One striking image that supports the message
2. **Minimum 30-point font** - This physically prevents overcrowding
3. **Ample white space** - Negative space is powerful, not wasted
4. **High contrast** - Light on dark or dark on light for maximum legibility

**Slide Types to Use:**
- **Title slides**: Large text with minimal supporting text (e.g., "iPhone" + "Apple reinvents the phone")
- **Image slides**: Full-bleed impactful image with minimal text overlay
- **Number slides**: One big statistic with context
- **Comparison slides**: Before/after or side-by-side visuals
- **Demo slides**: Visual showing the product/concept in action

### Step 5: Create the Presentation Using PPTX Skill

**MANDATORY:** Always read the PPTX skill before generating presentations:
```
Read /mnt/skills/public/pptx/SKILL.md
```

Then create the presentation following both the PPTX skill's technical requirements AND the Steve Jobs design principles.

**Key Integration Points:**
- Use the PPTX skill's methods for creating slides
- Apply Jobs principles to ALL content and layout decisions
- Ensure visual hierarchy through font sizes (30pt minimum)
- Leverage white space in slide layouts
- Use high-contrast color schemes
- Keep text minimal on every slide

### Step 6: Present the Deliverable

After creating the presentation:

1. **Provide the PPTX file** with a clear download link
2. **Summarize the structure** - Brief overview of the slide flow
3. **Highlight the key message** - Remind the user of the core takeaway
4. **Presenter notes** - Offer brief guidance on delivery:
   - The slides support YOU, not replace you
   - Practice until you can speak naturally without reading
   - Let the visuals amplify your spoken message
   - Embrace pauses and white space in delivery

## Quality Checklist

Before finalizing, verify each slide passes these tests:

**The 3-Second Test:**
- [ ] Can the main point be grasped in 3-5 seconds?
- [ ] Is there only ONE core idea per slide?
- [ ] Would this work as a highway billboard?

**Design Standards:**
- [ ] Font size minimum 30 points?
- [ ] Ample white space around elements?
- [ ] High contrast for legibility?
- [ ] Large, impactful visual (not decorative clipart)?

**Content Standards:**
- [ ] Minimal text (keywords, not sentences)?
- [ ] Only one statistic if showing data?
- [ ] Bullets used sparingly or not at all?
- [ ] Presenter as storyteller, not reading slides?

## Important Reminders

**What This Skill Is:**
- A methodology for creating minimalist, high-impact presentations
- Based on proven cognitive science principles
- Designed for live delivery with a presenter

**What This Skill Is Not:**
- Not for creating document-style slide decks meant to be read independently
- Not for comprehensive reports (recommend separate documents for those)
- Not for slides that replace the presenter

**Hybrid Strategy:**
If the user needs both a live presentation AND detailed documentation, recommend creating:
1. A minimalist presentation (using this skill) for live delivery
2. A separate detailed document (using docx skill) for pre-reads or leave-behinds

## Examples of Jobs-Style Slides

**Product Launch:**
- Slide 1: "iPhone" (large text, black background)
- Slide 2: "Apple reinvents the phone" (single line, image of iPhone)
- Slide 3: Three icons showing iPod + Phone + Internet
- Slide 4: "All in one device" with product image

**Concept Explanation:**
- Slide 1: Problem statement (one sentence + evocative image)
- Slide 2: "The Solution" (just those two words, large)
- Slide 3: Key benefit #1 (visual + 3-5 words)
- Slide 4: Key benefit #2 (visual + 3-5 words)
- Slide 5: "Imagine..." (showing the transformation)

**Business Pitch:**
- Slide 1: Hook - "What if..." (provocative question)
- Slide 2: Market opportunity (ONE big number)
- Slide 3: The problem (powerful image)
- Slide 4: Our solution (visual demo)
- Slide 5: Why now (timing/traction in visual form)

## Best Practices

1. **Start with the message, not the slides** - Know your core story first
2. **Embrace simplicity** - Every element must earn its place
3. **Test the 3-second rule** - If you can't get it in 3 seconds, simplify
4. **Use visuals emotionally** - Images should evoke feeling, not just illustrate
5. **Practice extensively** - Minimalist slides require confident delivery
6. **Remember: YOU are the presentation** - Slides are your supporting cast

## Common Mistakes to Avoid

❌ Putting full sentences on slides
❌ Using bullet points as a crutch
❌ Multiple ideas competing on one slide
❌ Small font sizes (<30pt)
❌ Cluttered layouts with no white space
❌ Decorative images that don't support the message
❌ Reading the slides verbatim
❌ Treating slides like documents

## References

- `references/jobs-guidelines.md` - Complete Steve Jobs 3-Second Rule guidelines (READ THIS FIRST)