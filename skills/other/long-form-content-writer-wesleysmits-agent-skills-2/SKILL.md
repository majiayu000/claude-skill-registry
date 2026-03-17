---
name: writing-long-form-content
description: Generates comprehensive blog post drafts with proper structure. Use when the user asks to write a full article, create blog content, draft long-form posts, or needs complete written content with SEO optimization.
---

# Long-Form Content Writer

## When to use this skill

- User asks to write a blog post or article
- User has an outline and needs full content
- User wants 1,500+ word articles
- User mentions content drafting or copywriting
- User needs SEO-optimized written content

## Workflow

- [ ] Gather topic, keyword, and requirements
- [ ] Confirm or create outline
- [ ] Write introduction with hook
- [ ] Draft body sections
- [ ] Write conclusion with CTA
- [ ] Apply formatting and polish

## Instructions

### Step 1: Gather Requirements

**Required inputs:**

| Input          | Purpose                                 |
| -------------- | --------------------------------------- |
| Topic/title    | What the article covers                 |
| Target keyword | SEO focus term                          |
| Word count     | Length target (1,500-5,000)             |
| Tone           | Professional, conversational, technical |
| Audience       | Who is reading this                     |
| Outline        | Structure (or create one)               |

**Optional inputs:**

- Brand voice guidelines
- Competitor articles to differentiate from
- Specific points to include
- CTAs or products to mention
- Internal links to include

### Step 2: Introduction Framework

**Hook types (choose one):**

| Hook Type      | Example                                 |
| -------------- | --------------------------------------- |
| Statistic      | "73% of developers struggle with..."    |
| Question       | "Have you ever wondered why..."         |
| Bold statement | "Everything you know about X is wrong." |
| Story          | "Last week, a client asked me..."       |
| Pain point     | "If you're tired of dealing with..."    |

**Introduction structure (100-150 words):**

```markdown
[Hook - 1-2 sentences that grab attention]

[Context - Why this matters now, the problem or opportunity]

[Credibility - Brief qualifier: experience, research, results]

[Promise - What the reader will learn or achieve]

[Thesis - Main point or answer preview]
```

**Example introduction:**

```markdown
Every second your images take to load, you lose 7% of potential conversions.
For e-commerce sites, that translates to thousands in lost revenue monthly.

Image optimization isn't just about smaller files—it's about delivering
the right format, size, and quality for every device and connection speed.

After optimizing images for over 200 client sites, I've identified the
techniques that consistently cut load times by 60% or more.

In this guide, you'll learn the exact process to audit, optimize, and
automate image delivery—whether you're using Next.js, WordPress, or
vanilla HTML.

The key insight: modern image optimization is about smart automation,
not manual compression.
```

### Step 3: Body Section Writing

**Section structure:**

```markdown
## [H2: Section Title with Keyword Variation]

[Opening sentence - transition from previous section or introduce topic]

[Core explanation - 2-3 paragraphs covering the main point]

[Example, data, or evidence - concrete illustration]

[Practical application - how reader uses this]

[Transition - lead into next section]
```

**Writing techniques:**

| Technique              | Application                                  |
| ---------------------- | -------------------------------------------- |
| Short paragraphs       | 2-4 sentences max for web reading            |
| Varied sentence length | Mix short punchy with longer explanatory     |
| Active voice           | "Use this tool" not "This tool can be used"  |
| Second person          | "You" focused, reader-centric                |
| Specific over vague    | "37% increase" not "significant improvement" |
| Show don't tell        | Examples over assertions                     |

**Transition phrases:**

- "Building on this..."
- "Now that you understand X, let's explore..."
- "This leads to an important question..."
- "Here's where it gets interesting..."
- "But there's a catch..."
- "Let's put this into practice..."

### Step 4: Content Formatting

**Use formatting for scannability:**

```markdown
## Use H2 for Main Sections

### Use H3 for Subsections

**Bold key terms** and important takeaways.

_Italics for emphasis_ or introducing new terms.

> Blockquotes for expert quotes or callouts

- Bullet points for lists of 3+ items
- Keep bullets parallel in structure
- Start with action verbs when possible

1. Numbered lists for sequential steps
2. Or ranked items
3. Keep to 5-7 items max

| Tables   | For Comparisons |
| -------- | --------------- |
| Option A | Best for X      |
| Option B | Best for Y      |

`Inline code` for technical terms, commands, or file names.
```

### Step 5: Keyword Integration

**Natural keyword placement:**

```markdown
Primary keyword: "image optimization"

✅ Natural: "Image optimization reduces page load times significantly."
❌ Forced: "For image optimization, image optimization techniques help."

✅ Variation: "Optimizing images for the web requires..."
✅ LSI term: "Compressing photos without quality loss..."
✅ Long-tail: "How to optimize images for mobile devices..."
```

**Keyword density guide:**

- Primary keyword: 0.5-1.5% (5-15 times per 1,000 words)
- Variations: 3-5 per 1,000 words
- Use naturally; never force

### Step 6: Conclusion Framework

**Conclusion structure (100-150 words):**

```markdown
[Recap - Summarize 2-3 main takeaways]

[Reinforcement - Why this matters/benefits]

[Action step - One specific thing to do next]

[CTA - Related resource, newsletter, service, or next article]

[Closing thought - Memorable final line]
```

**Example conclusion:**

```markdown
Image optimization isn't a one-time task—it's a system. By implementing
modern formats (WebP, AVIF), responsive sizing, and lazy loading, you'll
see immediate improvements in Core Web Vitals and user experience.

The sites that rank highest and convert best treat performance as a
feature, not an afterthought.

**Your next step:** Audit your top 5 landing pages with Lighthouse and
identify your largest image offenders. Start there.

Want the complete checklist? Download our [Image Optimization Audit
Template] and systematically improve every page.

Fast sites win. Make yours one of them.
```

### Step 7: Quality Checklist

**Before delivering, verify:**

| Check                            | Status |
| -------------------------------- | ------ |
| Word count meets target          | [ ]    |
| Keyword in title, intro, 1-2 H2s | [ ]    |
| Each section has clear purpose   | [ ]    |
| Examples/data support claims     | [ ]    |
| Paragraphs 2-4 sentences         | [ ]    |
| Formatting aids scanning         | [ ]    |
| Transitions between sections     | [ ]    |
| Conclusion has CTA               | [ ]    |
| No fluff or filler content       | [ ]    |
| Reads naturally aloud            | [ ]    |

### Content Templates

**Tutorial article:**

```markdown
# How to [Achieve Outcome]: A Step-by-Step Guide

## Introduction

[Hook + promise]

## What is [Topic] and Why Does It Matter?

[Foundation and context]

## What You'll Need Before Starting

[Prerequisites, tools, knowledge]

## Step 1: [First Action]

[Detailed instructions with examples]

## Step 2: [Second Action]

[Detailed instructions with examples]

## Step 3: [Third Action]

[Detailed instructions with examples]

## Common Mistakes to Avoid

[Pitfalls and how to prevent them]

## Troubleshooting

[FAQ or common issues]

## Next Steps

[Advanced techniques or related topics]

## Conclusion

[Recap + CTA]
```

**Listicle article:**

```markdown
# [Number] [Adjective] Ways to [Achieve Outcome]

## Introduction

[Why this list, how items were selected]

## 1. [Method/Tool/Tip Name]

[2-3 paragraphs: what, why, how]

## 2. [Method/Tool/Tip Name]

[2-3 paragraphs: what, why, how]

...continue for each item...

## How to Choose the Right Approach

[Decision framework]

## Conclusion

[Summary of best options + CTA]
```

**Comparison article:**

```markdown
# [Option A] vs [Option B]: Which is Right for You?

## Introduction

[Why compare, quick verdict teaser]

## Quick Comparison Table

[Side-by-side key differences]

## What is [Option A]?

[Overview, history, use case]

## What is [Option B]?

[Overview, history, use case]

## [Comparison Criterion 1]: [Winner]

[Analysis with evidence]

## [Comparison Criterion 2]: [Winner]

[Analysis with evidence]

## [Comparison Criterion 3]: [Winner]

[Analysis with evidence]

## Pricing Comparison

[If applicable]

## The Verdict

[Clear recommendation with nuance]

## Conclusion

[Summary + CTA]
```

## Word Count Guidelines

| Article Type        | Target      | Sections |
| ------------------- | ----------- | -------- |
| Quick guide         | 1,500       | 4-5 H2s  |
| Standard post       | 2,000-2,500 | 5-7 H2s  |
| Comprehensive guide | 3,000-4,000 | 7-10 H2s |
| Ultimate guide      | 5,000+      | 10+ H2s  |

**Section distribution (2,500 words):**

- Introduction: 150 words
- Section 1: 350 words
- Section 2: 400 words
- Section 3: 400 words
- Section 4: 400 words
- Section 5: 350 words
- FAQ/Bonus: 300 words
- Conclusion: 150 words

## Validation

Before completing:

- [ ] Word count within 10% of target
- [ ] All outline points covered
- [ ] Keyword integrated naturally
- [ ] Every claim has support
- [ ] Formatting consistent
- [ ] Introduction hooks reader
- [ ] Conclusion drives action
- [ ] No grammatical errors

## Error Handling

- **Outline too vague**: Ask for specific sections or create detailed outline first.
- **Word count too short**: Add examples, data, case studies, or expand "how to" sections.
- **Keyword stuffing**: Reduce density; use variations and synonyms.
- **Lacks depth**: Add expert quotes, statistics, or real-world examples.
- **Off-topic drift**: Refer back to outline; cut tangential content.

## Resources

- [Hemingway Editor](https://hemingwayapp.com/) - Readability check
- [Grammarly](https://www.grammarly.com/) - Grammar and tone
- [CoSchedule Headline Analyzer](https://coschedule.com/headline-analyzer)
- [Clearscope](https://www.clearscope.io/) - Content optimization
