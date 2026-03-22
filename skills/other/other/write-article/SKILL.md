---
name: write-article
description: "Write the full blog article using research notes, article outline, and generated diagrams. Follows the exact pedagogical style of the DeepSeek chapters. Use when research, plan, and figures are all ready."
allowed-tools: Read, Grep, Glob
---

# Article Writing Skill

## Input
$ARGUMENTS = topic name

## Prerequisites Check
Before writing, verify these files exist:
- research/<topic-slug>.md (research notes)
- plan/<topic-slug>_outline.md (article outline)
- figures/output/*.png (generated diagrams)

If any are missing, stop and tell the user what is needed.

## Writing Process

### Step 1: Load All Context
Read the research notes and article outline thoroughly.
List all available diagrams in figures/output/.
Match each planned diagram to its generated .png file.

**IMPORTANT: Visually open and look at EVERY diagram in figures/output/
before writing.** You need to see what the diagrams actually show so you
can describe them accurately in the article text. Do NOT write blind
descriptions of images you have not seen. If a diagram does not match
what you expected from the outline, note it and adjust your writing
to match what the diagram actually shows.

If any planned diagram is missing from figures/output/, do NOT reference
it in the article. Instead, leave a placeholder comment:
`<!-- MISSING DIAGRAM: fig_xxx.png - needs generation -->`
so the user knows which diagrams still need to be created.

### Step 2: Write the Article
Follow the outline section by section. For each section, apply
these rules from CLAUDE.md:

**Opening Section:**
```markdown
# <Article Title>

**This article covers:**
- Bullet point 1
- Bullet point 2
- Bullet point 3

<Bridge paragraph connecting to prerequisites>

<Reference to roadmap figure>

![Figure X.1 <Caption>](figures/output/fig_roadmap.png)

As shown in figure X.1, our roadmap highlights...
```

**Every Subsequent Section:**
```markdown
## <Section Title>

<Opening paragraph: 2-3 sentences establishing context>

<Introduce figure BEFORE showing it:>
"Let's examine the complete workflow, as illustrated in figure X.Y."

![Figure X.Y <Caption>](figures/output/fig_xxx.png)

<Explain figure AFTER showing it:>
"As shown in figure X.Y, the process begins with..."

<Detailed explanation with bullet points:>
- **Component Name**: Explanation of what it does...
- **Next Component**: Explanation...

<Transition to next subsection>
```

### Step 3: Apply the Writing Style Rules

MANDATORY style rules (from CLAUDE.md):

1. **NO em dashes.** Use commas, semicolons, or separate sentences.
   WRONG: "The model — which uses attention — processes tokens"
   RIGHT: "The model, which uses attention, processes tokens"

2. **"We" perspective** throughout.
   "Let's trace the journey..."
   "We have successfully built..."
   "Now that we understand..."

3. **Short paragraphs** of 2 to 4 sentences maximum.

4. **Bold lead-in** on bullet points:
   - **Input Matrix**: Shape (4, 8), four tokens...
   - **Expert 1 Importance**: 0.9 + 0.5 = 1.4

5. **Concrete running example** traced through every step.
   Use the example defined in the plan (e.g., 4 tokens, shape (4, 8)).
   Show exact numbers, shapes, and values at every transformation.

6. **Figure references** use this exact pattern:
   Before: "as illustrated in figure X.Y" or "shown in figure X.Y"
   After: "As shown in figure X.Y, ..." or "As illustrated in figure X.Y, ..."

7. **Enthusiasm for clever ideas:**
   "This is the magic of..."
   "This is a profound change."
   "The answer lies in a beautiful trick."

8. **Transition sentences** between sections:
   "Now that we have X, it's time to open the black box."
   "We have successfully built X. But this raises a new question..."
   "Having explored the theory, let's put our knowledge to the test."

9. **Callout boxes** for key definitions (1-2 per article):
   > **What is a Hidden State?** A hidden state is another name for...

10. **Summary section** with substantial bullet points (2-3 sentences each).

### Step 4: Self-Review Checklist
After completing the draft, verify:
- [ ] Every section has at least one figure
- [ ] All figures are referenced BEFORE and AFTER showing them
- [ ] All figure .png files exist in figures/output/ (visually confirmed)
- [ ] Figure descriptions in the text match what the images ACTUALLY show
- [ ] No references to missing or broken images
- [ ] No em dashes anywhere in the text
- [ ] Running example is consistent throughout
- [ ] Matrix shapes are shown at every transformation
- [ ] Bold lead-ins on all bullet points
- [ ] Short paragraphs (max 4 sentences)
- [ ] "We" perspective used consistently
- [ ] Transitions between all sections
- [ ] Opening has "This article covers" bullets
- [ ] Closing has substantial summary bullets
- [ ] Total figure count is 25 to 35
- [ ] Any missing diagrams have <!-- MISSING DIAGRAM --> placeholders

### Step 5: Save the Draft
Save to: drafts/<topic-slug>.md

## Output
Report to the user:
- Article title
- Word count
- Figure count
- Show the first 3 paragraphs as preview
- List any issues found in self-review