---
name: notebooklm-slides
description: |
  Generate pedagogically-aligned slide decks from educational content using NotebookLM.
  Use when creating chapter slide presentations with proficiency-calibrated prompts.
  NOT for static slides or non-educational presentations.
dependencies:
  - browser-use
---

# NotebookLM Slides Generation

## Quick Start

```bash
# 1. Start browser (via browser-use skill)
bash .claude/skills/browser-use/scripts/start-server.sh

# 2. Navigate to NotebookLM
# browser_navigate to notebooklm.google.com

# 3. Create notebook, upload sources, generate slides
# Use proficiency-calibrated prompts below
```

## Core Principles

1. **Proficiency-Driven**: Slides match CEFR levels (A2 beginner → C1 advanced)
2. **Framework Alignment**: Educational philosophy explicitly stated
3. **Visual Over Text**: 3-5 bullets per slide, not paragraphs
4. **Narrative Arc**: problem → transformation → opportunity → action
5. **Actionable Endings**: Concrete next steps, not "Keep learning!"

## Workflow (Per Chapter)

| Step | Action | Tool |
|------|--------|------|
| 1 | Navigate to notebooklm.google.com | browser_navigate |
| 2 | Create notebook: "Chapter X: Title" | browser_click |
| 3 | Upload ALL sources (lessons + README + quiz) | browser_click |
| 4 | Click "Slide Deck" in Studio panel | browser_click |
| 5 | Select "Presenter Slides" format | browser_click |
| 6 | Paste proficiency-calibrated prompt | browser_type |
| 7 | Click "Generate" (wait 5-30 min) | browser_click |
| 8 | Review with success criteria | Visual inspection |
| 9 | Download PDF | browser_click |
| 10 | Move to `static/slides/chapter-{NN}-slides.pdf` | Bash |

## Proficiency-Calibrated Prompts

### A2 (Beginners)

```
Create inspiring slide deck for absolute beginners (A2 proficiency).

AUDIENCE: Complete beginners with no programming experience.

FRAMEWORK TO EMPHASIZE:
• [Principle 1]: Simple, concrete explanation
• [Principle 2]: Accessible mental model
• [Principle 3]: Encouraging principle

THEMES (with specific data):
1. [Theme with concrete numbers/facts]
2. [Theme with specific example]
3. [Theme with real-world data]

TONE:
• Encouraging (not intimidating)
• Future-focused and opportunity-driven
• Simple language, no jargon
• Action-oriented

<slide_format_requirements>
Generate 12-15 slides. Each slide: 3-5 bullet points as sentences,
NOT paragraphs. Clear headings. Cover all themes.
</slide_format_requirements>

NARRATIVE: problem → transformation → opportunity → action
END WITH: Specific next steps (not "Keep learning!")
```

### B1 (Intermediate)

```
Create comprehensive slide deck for intermediate learners (B1 proficiency).

AUDIENCE: Learners with [prerequisites]. Ready for [next-level challenge].

FRAMEWORK TO EMPHASIZE:
• [Intermediate concept with practical context]
• [Problem-solving approach]
• [Real-world application pattern]

THEMES (with specific data):
1-5. [Themes with concrete examples]

TONE:
• Professional yet accessible
• Balance theory with practice
• Technical terms with context
• Critical thinking encouraged

<slide_format_requirements>
Generate 15-20 slides. Each slide: 4-6 bullet points.
Include practical examples and case studies.
</slide_format_requirements>

END WITH: Implementation strategies (step-by-step)
```

### C1 (Advanced)

```
Create detailed slide deck for advanced practitioners (C1 proficiency).

AUDIENCE: Experienced with [advanced prerequisites].

FRAMEWORK TO EMPHASIZE:
• [Theoretical frameworks and trade-offs]
• [Industry patterns and anti-patterns]
• [Critical analysis and decision-making]

THEMES: [5-7 themes with industry data]

TONE:
• Professional and rigorous
• Nuance and complexity
• Industry-standard terminology
• Analytical and evaluative

<slide_format_requirements>
Generate 20-25 slides. Each slide: 5-7 bullet points.
Include architecture diagrams, decision matrices.
</slide_format_requirements>

END WITH: Production deployment strategies
```

## Success Criteria (7 Gates)

| Gate | Check | Pass | Fail |
|------|-------|------|------|
| 1. Title | Reflects framework? | "AI Coding Revolution" | "Introduction to AI" |
| 2. Language | Matches proficiency? | A2: simple, no jargon | A2 with technical terms |
| 3. Themes | All 5-7 covered? | Each theme with data | Themes missing |
| 4. Tone | Matches spec? | Encouraging (not academic) | Wrong emotional framing |
| 5. Count | Within range? | A2: 12-15, B1: 15-20 | Outside range |
| 6. Arc | Progression clear? | problem → action | Random sequence |
| 7. Ending | Actionable? | Specific tasks | "Keep learning!" |

**Score**: 7/7 → Deploy | <7/7 → Iterate with refined prompt

## File Naming

**Format**: `chapter-{NN}-slides.pdf` (zero-padded)

```bash
# Example
mv ~/Downloads/"The-AI-Revolution.pdf" \
   "apps/learn-app/static/slides/chapter-01-slides.pdf"
```

## Integration

Add to chapter README frontmatter:

```yaml
---
title: "Chapter 1: Title"
slides:
  source: "slides/chapter-01-slides.pdf"
  title: "Chapter 1: Title"
  height: 700
---
```

Build-time plugin auto-injects PDFViewer before "What You'll Learn".

## Batch Processing

For 3+ chapters:
1. Create ALL notebooks first (before generating)
2. Upload sources for all chapters
3. Prepare all prompts in text editor
4. Generate Chapter N → prepare N+1 prompt while waiting
5. Download when ready → start next immediately

**Daily limit**: 3-5 chapters/day (NotebookLM enforced)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Generation stuck >30 min | Check browser console, verify no daily limit message |
| Text-heavy slides | Add explicit "3-5 bullets, NOT paragraphs" |
| Generic title | Include example engaging title in prompt |
| Missing themes | List all themes numbered with specific data |
| Daily limit hit | Wait 24h (midnight PT reset), notebooks persist |

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Vague audience | NotebookLM can't calibrate | "A2 beginners with no programming" |
| Skip framework | Generic output | Explicit 3-5 principles |
| Single-word tone | Ambiguous | "Encouraging (not intimidating)" |
| Leave format default | Text-heavy slides | Explicit bullet count |
| Vague endings | No student action | Specific next steps |
