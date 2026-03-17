---
name: content_creation
description: Long-form blog posts, LinkedIn articles, and thought leadership content creation
when_to_use: When creating articles longer than 500 words, structuring thought leadership pieces, writing LinkedIn newsletter posts, or producing evergreen educational content
references:
  - references/content-structure-templates.md
  - references/thought-leadership-frameworks.md
---

# Content Creation Skill

## Overview

This skill provides structured workflows for creating high-quality long-form content: blog posts, LinkedIn articles, case studies, and thought leadership pieces that establish authority and drive engagement.

## Tools to Use

- **Perplexity**: Research facts, statistics, case studies, and expert perspectives
- **Jina**: Extract and analyze reference articles, competitor pieces
- **RAG (brand_guidelines)**: Brand voice, tone, and messaging framework
- **RAG (platform_specs)**: Platform-specific formatting requirements

## Workflow

### Step 1 — Content Brief Validation

Before writing, confirm:
- **Goal**: What should the reader do/think/feel after reading?
- **Audience**: Who is the primary reader? (role, seniority, pain points)
- **Format**: Blog post / LinkedIn article / newsletter / case study
- **Angle**: What unique perspective does this piece offer?
- **Target length**: (blog: 800–1500w, LinkedIn article: 600–1200w, thought leadership: 1000–2500w)

### Step 2 — Research Phase

1. Use Perplexity to gather supporting data:
   - "Find 3 recent statistics about [topic] from credible sources"
   - "What are expert opinions on [topic] from industry leaders?"
   - "What are the most common misconceptions about [topic]?"

2. Note sources for attribution (author, publication, year)

3. Identify 1–2 concrete examples or case studies

### Step 3 — Structure Planning (Outline)

Choose the appropriate structure:

**Problem-Solution-Impact** (best for educational content):
```
Hook: [Stat or provocative statement]
Problem: [Define the pain/challenge clearly]
Why it matters: [Stakes and consequences]
Solution: [Your approach/framework]
How-to: [3–5 actionable steps]
Real example: [Case study or anecdote]
CTA: [Next step for reader]
```

**Thought Leadership Framework** (best for LinkedIn):
```
Big claim/contrarian take
[3 supporting observations from experience]
Nuanced reality
Practical implication for reader
Personal takeaway
Soft CTA
```

**Listicle with Depth** (best for blog posts):
```
Introduction (hook + promise)
Point 1: [Header] + Explanation + Example
Point 2: [Header] + Explanation + Example
...
Conclusion: Summary + Action
```

### Step 4 — Writing Guidelines

**Voice & Tone** (load brand_voice skill for specifics):
- Active voice, concrete language
- First-person for thought leadership
- Third-person for educational/factual content
- No jargon unless audience-appropriate

**Paragraph Structure**:
- Max 3–4 sentences per paragraph
- One idea per paragraph
- Short paragraphs for online readability

**Headers**:
- H2 for main sections (every 200–300 words)
- H3 for sub-points
- Headers should be informative (not just labels)

**Opening Hook Options**:
- Surprising statistic: "73% of [audience] struggle with [problem]"
- Bold claim: "Most [X] approaches are fundamentally broken"
- Personal story: "Three years ago, I made the same mistake"
- Question: "Why does [common practice] keep failing?"

### Step 5 — Draft, Then Edit

**Drafting**:
- Write the full draft without stopping to perfect
- Use placeholders [STAT], [EXAMPLE] if data is needed later
- Fill in research from Step 2

**Editing checklist**:
- [ ] Hook in first sentence (not in second)
- [ ] Every paragraph has a clear purpose
- [ ] No passive voice unless intentional
- [ ] Transitions between sections flow naturally
- [ ] CTA is clear and single-minded
- [ ] Length matches target (no padding)

### Step 6 — SEO Pass (if applicable)

Run seo_analysis skill after draft is complete for:
- Primary keyword integration
- Metadata generation
- Header optimization

## Output Format

```markdown
## Content Draft

**Title**: [SEO-optimized title]
**Format**: [Blog / LinkedIn Article / etc.]
**Word Count**: [N words]
**Primary Keyword**: [keyword] (if SEO-focused)

---

[Full article content with headers]

---

## Content Notes
- **Sources cited**: [list]
- **CTA**: [specific CTA used]
- **Suggested publish date**: [if applicable]
- **Content gaps to fill**: [if any placeholders remain]
```

## Notes

- Always load brand_voice skill before drafting to align tone
- For Italian-language content: translate after drafting in English unless brand prefers native Italian drafting
- Thought leadership pieces should reference personal brand or company expertise specifically
- LinkedIn articles: always end with a question to drive comments
