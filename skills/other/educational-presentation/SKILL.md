---
name: educational-presentation
description: >
  Transform Claude into an expert in evidence-based educational presentation design. 
  Use when designing presentations for teaching, training, or learning contexts where 
  retention and comprehension matter. Applies Cognitive Load Theory, Mayer's 12 Principles 
  of Multimedia Learning, Gagné's 9 Events of Instruction, C.R.A.P. design principles, 
  and WCAG 2.1 AA accessibility standards. Triggers on requests to (1) create educational 
  or training presentations, (2) design slides for teaching or workshops, (3) improve 
  existing educational presentations, (4) convert content into visual presentations, 
  (5) ensure accessible and inclusive presentations, or (6) apply learning science 
  to presentation design.
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Educational Presentation Design

Transform any presentation into a cognitively-optimized learning tool based on evidence from learning science.

## Core Philosophy: Minimize Cognitive Load

**Prime Directive**: Every design decision must serve learning by:
1. Reducing extraneous load (eliminate distractions)
2. Managing intrinsic load (chunk complex content)
3. Optimizing germane load (maximize mental resources for actual learning)

**Critical Rule**: If a design element doesn't directly support learning, remove it.

---

## Essential Principles (Non-Negotiable)

### Mayer's 3 Most Critical Principles

#### 1. Coherence Principle ⭐ MOST IMPORTANT
**Rule**: Exclude all extraneous material - no decorative clipart, busy backgrounds, or irrelevant details.
**Application**: Every slide element must have a clear instructional purpose.

#### 2. Redundancy Principle ⭐ CRITICAL  
**Rule**: Do NOT put paragraphs of text on slides that will be read aloud.
**Why**: Creates "cognitive channel war" - audience can't read and listen simultaneously.
**Solution**:
- Visuals + narration = GOOD ✅
- Visuals + text wall + narration = COGNITIVE OVERLOAD ❌
- Move all paragraph text to speaker notes
- Slides should have: keywords, graphics, or charts only

#### 3. Segmenting Principle ⭐ ESSENTIAL
**Rule**: Break content into user-paced chunks using progressive disclosure or multiple slides.
**Application**: Never overwhelm with one dense slide - chunk across 3-5 slides instead.

**For all 12 Mayer principles with detailed applications**, read [`references/quick-reference.md`](references/quick-reference.md).

---

## Macro-Structure: Gagné's 9 Events Framework

Every educational presentation MUST follow this structure:

### Event 1: Gain Attention
- Thought-provoking question, surprising statistic, or compelling case study
- Stimulates curiosity and focus

### Event 2: Inform Learners of Objectives  
- "By the end of this session, you will be able to..."
- Use measurable action verbs (Analyze, Compare, Apply, Evaluate, Create)

### Event 3: Stimulate Recall of Prior Learning
- Poll question: "What do you already know about X?"
- Activates existing knowledge as foundation

### Event 4: Present the Content
- Main content slides with visuals + narration (not text walls)
- Break into digestible 3-5 minute chunks
- Apply progressive disclosure

### Event 5: Provide Learning Guidance
- Worked examples, non-examples, analogies, case studies
- Graphic organizers and mnemonics

### Event 6: Elicit Performance
- "Try this problem" or "Discuss with your neighbor"
- Interactive quiz or application exercise (non-graded)

### Event 7: Provide Feedback
- Correct answer with explanation
- Model of ideal response and common mistakes to avoid

### Event 8: Assess Performance
- Formal quiz, project prompt, or final presentation request
- Measures if objective was met

### Event 9: Enhance Retention and Transfer
- Final summary and transfer question: "How will you use this in your work?"
- Real-world problem to solve

**For detailed templates for each event**, read [`references/slide-templates.md`](references/slide-templates.md).

---

## Micro-Design: C.R.A.P. Principles

### 1. Contrast
Create visual hierarchy with strong differences:
- Large title (36-44pt) vs. smaller body (24-32pt)  
- Bright accent color on neutral background
- Bold vs. regular weight

### 2. Repetition
Reuse same fonts, colors, and layouts:
- Consistent title placement
- Same color palette on every slide
- Maximum 2 fonts for entire deck

### 3. Alignment
Nothing is placed arbitrarily:
- Use invisible grid (turn on guides)
- Left-align body text (never center paragraphs)
- Connect every element to another

### 4. Proximity
Group related items close together:
- Place labels directly next to graphics
- Use whitespace to separate unrelated groups

**For detailed C.R.A.P. applications**, read [`references/quick-reference.md`](references/quick-reference.md).

---

## Typography & Color Essentials

### Typography Rules
- **Font Choice**: Sans-serif only (Arial, Calibri, Verdana, Helvetica)
- **Size**: Main Title 36-44pt, Body Text 24-32pt minimum
- **Alignment**: Left-align all body text, never center
- **Emphasis**: Use bold, never underline or ALL CAPS

### Color Strategy
**60-30-10 Rule**:
- 60% Primary (neutral background: white, off-white, dark gray)
- 30% Secondary (structural elements: title bars, sidebars)  
- 10% Accent (key words, buttons, arrows - bright, contrasting)

**Accessibility (WCAG 2.1 AA)**:
- 4.5:1 contrast ratio for normal text
- 3:1 contrast ratio for large text (18pt+)
- Never use red/green or blue/yellow combinations

**Tools**: WebAIM Contrast Checker, Adobe Color, Coolors

---

## Visual Elements & Multimedia

### Images & Icons
- ✅ High-quality, relevant photographs
- ✅ Professional icons (Noun Project, Flaticon, Iconoir)  
- ✅ Icons can replace bullet points
- ❌ No decorative clipart or "seductive details"

### Charts & Diagrams
- Simplify to one clear message per chart
- Use progressive disclosure for complex diagrams
- Label directly on elements (not separate legend)

**Free Legal Resources**:
- Images: Unsplash, Wikimedia Commons
- Icons: Noun Project, Flaticon, Iconoir

---

## Progressive Disclosure & Animations

### When to Use
- 3+ bullet points or list items
- Complex diagrams or processes
- Step-by-step explanations

### How to Implement
**PowerPoint**: Animations > Add Animation > Appear > Effect Options: On Click
**Google Slides**: Insert > Animation > Appear/Fade In > On Click

**Critical Rules**:
- Use "Appear" or "Fade" only (no distracting effects)
- Set to "On Click" not "After Previous"
- Build diagrams piece-by-piece

---

## Accessibility (WCAG 2.1 AA)

### Must-Have Requirements
1. **Alt text** on all images and charts
2. **Contrast** meets 4.5:1 ratio (verify with tools)
3. **Built-in layouts** (don't use text boxes floating arbitrarily)
4. **Reading order** checked and corrected
5. **Color independence** (don't rely on color alone for meaning)

### Tools
**PowerPoint**: File > Info > Check for Issues > Check Accessibility
**Google Slides**: Grackle Slides add-on

**For complete accessibility checklist**, read [`references/validation.md`](references/validation.md).

---

## Common Mistakes to Avoid

### ❌ The Bullet Point Slide of Death
**Problem**: 8+ bullet points with full sentences, presented all at once
**Fix**: Chunk across 3-4 slides, one clear message per slide, use progressive disclosure

### ❌ The Text Wall
**Problem**: Paragraphs of text on slide while presenter reads aloud
**Fix**: Move ALL paragraph text to speaker notes, leave only keywords/graphics

### ❌ The Clipart Catastrophe  
**Problem**: Generic clipart that doesn't illustrate the concept
**Fix**: Use high-quality, relevant photographs or professional icons

### ❌ The Overwhelming Diagram
**Problem**: Complex flowchart revealed all at once
**Fix**: Build piece-by-piece using progressive disclosure

### ❌ The Centered Everything
**Problem**: All text centered on slide
**Fix**: Left-align all body text, use invisible grid

**For detailed before/after transformations**, read [`references/before-after.md`](references/before-after.md).

---

## Workflow: Creating a Presentation

### Step 1: Plan the Structure (5-10 minutes)
1. Define learning objectives (measurable action verbs)
2. Outline using Gagné's 9 Events framework
3. Identify key concepts that need pre-training
4. Plan practice opportunities and feedback

### Step 2: Create Content Slides (30-60 minutes)
1. Start with slide titles (one clear idea per slide)
2. Add relevant visuals first (not as decoration)
3. Add minimal text (keywords only, not sentences)
4. Write detailed speaker notes (what you'll say)
5. Apply C.R.A.P. principles consistently

### Step 3: Implement Progressive Disclosure (10-20 minutes)
1. Identify slides with 3+ items
2. Add "Appear" animations set to "On Click"
3. Test flow and timing

### Step 4: Validate Before Delivery (10-15 minutes)
1. Run accessibility checker
2. Verify contrast ratios
3. Check reading order
4. Confirm all images have alt text
5. Test on actual presentation screen

**For comprehensive validation checklist (174 points)**, read [`references/validation.md`](references/validation.md).

---

## Decision Trees

### "Should I put this text on the slide?"

```
Will I read this text aloud?
├─ YES → Move to speaker notes ✅
│      (Use visual + keyword only on slide)
└─ NO → Consider keeping on slide
       ├─ Is it a keyword/label? → Keep ✅
       ├─ Is it a technical term that must be referenced? → Keep ✅  
       └─ Is it a full sentence/paragraph? → Move to notes ✅
```

### "Which chart should I use?"

```
What's your data story?
├─ Comparing categories → Bar/Column chart
├─ Showing trend over time → Line graph
├─ Part-to-whole relationship → Pie/Donut (max 5 slices)
└─ Correlation between variables → Scatter plot
```

---

## Quick Validation Checklist

Before delivering, verify:

### Structure ✓
- [ ] Follows Gagné's 9 Events framework
- [ ] Clear learning objectives stated
- [ ] Includes practice opportunity and feedback

### Cognitive Load ✓  
- [ ] No slide has more than one main idea
- [ ] Complex content is chunked appropriately
- [ ] All decorative elements removed (Coherence)
- [ ] No text walls + narration (Redundancy)

### Design ✓
- [ ] Strong contrast creates clear hierarchy
- [ ] Consistent repetition throughout
- [ ] All elements aligned on grid
- [ ] Generous whitespace on every slide

### Typography ✓
- [ ] Sans-serif fonts used
- [ ] Maximum 2 fonts
- [ ] All text minimum 24pt
- [ ] Body text left-aligned

### Color ✓
- [ ] 60-30-10 rule applied
- [ ] All text meets 4.5:1 contrast ratio
- [ ] No red/green or blue/yellow combinations

### Multimedia ✓
- [ ] Every slide has words AND pictures
- [ ] High-quality, relevant images only
- [ ] Labels placed next to graphics

### Interaction ✓
- [ ] Progressive disclosure applied where appropriate
- [ ] Animations set to "On Click"
- [ ] "Appear" or "Fade" only

### Accessibility ✓
- [ ] Alt text on all images/charts
- [ ] Built-in layouts used
- [ ] Contrast ratios verified

---

## Key Mantras

1. **"If it doesn't support learning, delete it."** (Coherence Principle)
2. **"Visual + narration, not visual + text + narration."** (Redundancy Principle)
3. **"One slide, one idea."** (Segmenting Principle)
4. **"Clean isn't empty; clean is focused."** (Whitespace)
5. **"Beautiful is efficient."** (Cognitive Load Theory)
6. **"Design for everyone or design for no one."** (Accessibility)

---

## Reference Files Guide

This skill includes detailed reference files for specific needs:

### [`references/quick-reference.md`](references/quick-reference.md)
**Use when**: You need rapid decisions during creation or want a scannable checklist
**Contains**: 
- 30-second checklist
- Mayer's 12 in 12 seconds
- Gagné's 9 in 9 slides
- C.R.A.P. in 4 questions
- Typography rules express
- Color 60-30-10 rule
- Progressive disclosure guide
- Accessibility 5 must-haves
- Top 5 errors to avoid
- Chart selection guide

### [`references/slide-templates.md`](references/slide-templates.md)  
**Use when**: You want ready-to-use templates for specific slide types
**Contains**:
- 20+ templates organized by Gagné's 9 Events
- Opening slides (3 templates)
- Objectives, Recall, Content, Guidance templates
- Practice, Feedback, Assessment templates
- Transfer/Application templates
- Special slides (Section Divider, Summary, Q&A, Thank You, References)
- Selection guide for each template

### [`references/before-after.md`](references/before-after.md)
**Use when**: You want to see concrete transformations or understand common mistakes
**Contains**:
- 6 major transformation examples
- Cognitive analysis of problems
- Step-by-step solutions applied
- C.R.A.P.-Mayer scoring for validation
- Visual comparisons showing improvements

### [`references/validation.md`](references/validation.md)
**Use when**: You need comprehensive pre-delivery validation
**Contains**:
- 174-point complete validation checklist
- 13 evaluation sections with scoring
- Pedagogical Structure (20 pts)
- Mayer Principles (24 pts)
- C.R.A.P. Design (16 pts)
- Typography, Colors, Visuals (40 pts)
- Animations, Whitespace, Accessibility (36 pts)
- Content, Duration, Storytelling, Consistency (38 pts)
- Scoring system: 95-100% = Excellence, 85-94% = Very Good, 70-84% = Acceptable, <70% = Rework needed

---

## Implementation with Technical Tools

### PowerPoint/Google Slides
When creating presentations in PowerPoint or Google Slides:
1. Apply these principles manually
2. Use built-in accessibility checkers
3. Verify contrast with WebAIM or Coolors
4. Test progressive disclosure animations

### Creating with Claude (pptx skill)
When Claude needs to create actual .pptx files:
1. This skill provides the **pedagogical design** and **content structure**
2. The `pptx` skill provides the **technical implementation** (html2pptx, python-pptx)
3. Use this skill first to design, then pptx skill to build

**Workflow**:
1. Use educational-presentation skill to plan structure and content
2. Create detailed slide outlines with speaker notes
3. Use pptx skill to implement the technical file creation
4. Return to this skill for final validation

---

## Core Theories & Further Reading

**Foundational Theories**:
- Cognitive Load Theory (Sweller)
- Mayer's Cognitive Theory of Multimedia Learning
- Gagné's Nine Events of Instruction
- Bloom's Taxonomy

**Design Principles**:
- Robin Williams' C.R.A.P. Principles
- WCAG 2.1 Accessibility Guidelines

**Recommended Books**:
- "Presentation Zen" by Garr Reynolds
- "Slide:ology" by Nancy Duarte  
- "Multimedia Learning" by Richard E. Mayer

---

## Summary: Start Here

**New to educational presentations?** Follow this path:
1. Read this SKILL.md file completely (15 minutes)
2. Review [`references/quick-reference.md`](references/quick-reference.md) (10 minutes)
3. Start creating with [`references/slide-templates.md`](references/slide-templates.md) (5 minutes per template)
4. Validate with checklist above before delivery

**Improving existing presentations?** Follow this path:
1. Read [`references/before-after.md`](references/before-after.md) to identify common mistakes (30 minutes)
2. Apply transformations to your slides
3. Validate with [`references/validation.md`](references/validation.md) (15-30 minutes)

**Quick reference during creation?** Keep [`references/quick-reference.md`](references/quick-reference.md) open

---

**Remember**: Beautiful presentations are cognitively efficient presentations. Every design choice should serve learning, not just aesthetics.

---

## What Claude Does vs What You Decide

| Claude handles | You provide |
|---------------|-------------|
| Applying Gagné's 9 Events structure | Learning objectives and content |
| Enforcing Mayer's 12 Principles | Domain expertise and examples |
| Checking accessibility (WCAG 2.1 AA) | Visual design preferences |
| Suggesting progressive disclosure | Pacing and delivery style |
| Running validation checklist | Final approval and refinement |

---

## Skill Boundaries

### This skill excels for:
- Training and educational presentations
- Workshop and course materials
- Learning-focused content where retention matters
- Accessible presentation design

### This skill is NOT ideal for:
- Sales pitch decks → Different structure needed
- Entertainment presentations → Engagement over retention
- Infographics → Static design, not progressive

---

## Iteration Guide

| Pass | Focus | Action |
|------|-------|--------|
| **1st** | Structure | Apply Gagné's 9 Events framework |
| **2nd** | Cognitive Load | Check Coherence, Redundancy, Segmenting |
| **3rd** | Design | Apply C.R.A.P. principles |
| **4th** | Accessibility | Run WCAG checklist |

---

## Skill Metadata

```yaml
name: educational-presentation
category: content
subcategory: presentations
version: 2.0
author: GUIA
source_expert: Richard Mayer, Robert Gagné, Robin Williams
source_work: Multimedia Learning, Conditions of Learning, The Non-Designer's Design Book
difficulty: intermediate
mode: cyborg
tags: [presentation, education, training, cognitive-load, mayer, gagne, accessibility]
created: 2026-02-03
updated: 2026-02-03
```
