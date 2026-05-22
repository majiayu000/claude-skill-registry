---
name: generating-blog-outlines
description: Creates structured blog post outlines based on topics and keywords. Use when the user asks about blog structure, content outlines, SEO article planning, or wants to organize ideas before writing.
---

# Blog Post Outline Generator

## When to use this skill

- User asks to outline a blog post
- User has a topic and needs structure
- User mentions SEO content planning
- User wants competitive content analysis
- User needs heading suggestions

## Workflow

- [ ] Clarify topic and target keyword
- [ ] Research search intent
- [ ] Analyze competitor structure
- [ ] Generate outline with headings
- [ ] Add keyword placement recommendations
- [ ] Suggest content angles

## Instructions

### Step 1: Gather Input

**Required information:**

| Input             | Purpose                             |
| ----------------- | ----------------------------------- |
| Primary keyword   | Main search term to target          |
| Topic/angle       | Specific focus of the article       |
| Target audience   | Who the content is for              |
| Content goal      | Inform, convert, educate, entertain |
| Word count target | Affects depth and sections          |

**Example prompt:**

```
Topic: "How to optimize images for web performance"
Keyword: "image optimization"
Audience: Frontend developers
Goal: Educational tutorial
Length: 2,000 words
```

### Step 2: Determine Search Intent

| Intent Type   | Indicators                    | Content Style              |
| ------------- | ----------------------------- | -------------------------- |
| Informational | "how to", "what is", "guide"  | Tutorial, explainer        |
| Commercial    | "best", "top", "vs", "review" | Comparison, listicle       |
| Transactional | "buy", "pricing", "download"  | Product-focused, CTA-heavy |
| Navigational  | Brand + feature               | Direct, feature-specific   |

### Step 3: Competitor Analysis

**Identify top-ranking content:**

- Check top 5 results for target keyword
- Note common headings and sections
- Identify content gaps to fill
- Assess word count and depth

**Analysis template:**

```markdown
## Competitor Analysis: [Keyword]

### Top 3 Ranking Articles

1. [Title] - [URL]
   - Word count: ~X,XXX
   - Key sections: [list]
   - Unique angle: [note]

2. [Title] - [URL]
   - Word count: ~X,XXX
   - Key sections: [list]
   - Unique angle: [note]

### Content Gaps Identified

- [ ] Missing topic: ...
- [ ] Outdated information: ...
- [ ] Better examples needed: ...
```

### Step 4: Generate Outline Structure

**Standard blog structure:**

```markdown
# [Title with Primary Keyword]

## Introduction (100-150 words)

- Hook: [attention-grabbing opener]
- Context: [why this matters now]
- Promise: [what reader will learn]
- Thesis: [main point/answer]

## [H2: First Main Section]

### [H3: Subsection if needed]

- Key point 1
- Key point 2
- Example or data point

### [H3: Another Subsection]

- Key point 1
- Supporting detail

## [H2: Second Main Section]

- Key points to cover
- Include [keyword variation] naturally

## [H2: Third Main Section]

### [H3: Practical subsection]

- Step-by-step if applicable
- Code examples if technical

## [H2: Common Mistakes / FAQ / Tips]

- Address related questions
- Add value beyond competitors

## Conclusion (100-150 words)

- Recap main points
- Actionable next step
- CTA (related content, newsletter, etc.)
```

### Step 5: Keyword Placement Strategy

| Location         | Priority | Guideline                            |
| ---------------- | -------- | ------------------------------------ |
| Title (H1)       | Required | Include primary keyword              |
| First paragraph  | Required | Within first 100 words               |
| H2 headings      | High     | 1-2 headings with keyword/variation  |
| H3 headings      | Medium   | Natural placement                    |
| Body text        | Medium   | 1-2% density, variations             |
| Meta description | Required | Include keyword near start           |
| Image alt text   | Medium   | Descriptive with keyword if relevant |
| URL slug         | Required | Short, keyword-focused               |

**Keyword variations to include:**

```markdown
Primary: image optimization
Variations:

- optimize images
- image compression
- web image optimization
- compress images for web
- reduce image file size
```

### Step 6: Content Angle Suggestions

**Angle frameworks:**

| Framework        | Description                  | Best For                  |
| ---------------- | ---------------------------- | ------------------------- |
| Ultimate Guide   | Comprehensive, authoritative | High-competition keywords |
| Step-by-Step     | Numbered process             | How-to queries            |
| Listicle         | Numbered tips/tools          | "Best" or "Top" queries   |
| Comparison       | X vs Y analysis              | Decision-stage content    |
| Case Study       | Real example with results    | Trust-building content    |
| Beginner's Guide | Foundational, accessible     | Awareness-stage content   |

### Outline Templates

**Tutorial/How-To:**

```markdown
# How to [Achieve Outcome]: [Benefit Statement]

## Introduction

- Problem statement
- What you'll learn

## Prerequisites / What You'll Need

## Step 1: [First Action]

## Step 2: [Second Action]

## Step 3: [Third Action]

## Troubleshooting Common Issues

## Next Steps / Advanced Tips

## Conclusion
```

**Listicle:**

```markdown
# [Number] [Adjective] [Topic] for [Outcome] in [Year]

## Introduction

- Why this list matters
- How items were selected

## 1. [Item Name]

- Key benefit
- Best for: [use case]
- Consideration: [limitation]

## 2. [Item Name]

...

## How to Choose the Right [Topic]

## Conclusion
```

**Comparison:**

```markdown
# [Option A] vs [Option B]: [Decision Framework]

## Introduction

- Why this comparison matters
- Quick verdict

## Overview Comparison Table

## [Option A] Explained

### Pros

### Cons

### Best For

## [Option B] Explained

### Pros

### Cons

### Best For

## Head-to-Head: [Criteria 1]

## Head-to-Head: [Criteria 2]

## Head-to-Head: [Criteria 3]

## Verdict: Which Should You Choose?

## Conclusion
```

### Step 7: Finalize Outline

**Checklist before delivering:**

- [ ] Title includes primary keyword
- [ ] H2s cover main topic comprehensively
- [ ] Logical flow from intro to conclusion
- [ ] Content gaps from competitors addressed
- [ ] Unique angle or value-add identified
- [ ] Word count distributed across sections
- [ ] CTA and next steps included

**Section word count distribution (2,000 words):**

```
Introduction: 150 words
Section 1: 400 words
Section 2: 400 words
Section 3: 400 words
Section 4: 350 words
Conclusion: 150 words
Buffer: 150 words
```

## Output Format

```markdown
# Blog Post Outline: [Title]

**Target Keyword:** [keyword]
**Word Count:** [target]
**Search Intent:** [type]
**Content Angle:** [framework]

---

## Outline

[Full outline with H2/H3 structure and bullet points for each section]

---

## Keyword Strategy

- Primary: [keyword]
- Variations: [list]
- Placement: [notes]

## Competitor Gaps Addressed

- [gap 1]
- [gap 2]

## Unique Value Proposition

[What makes this article stand out]
```

## Validation

Before completing:

- [ ] Primary keyword in title
- [ ] 5-8 H2 sections for comprehensive coverage
- [ ] Each section has clear purpose
- [ ] Keyword variations distributed
- [ ] Matches or exceeds competitor depth
- [ ] Includes actionable elements

## Error Handling

- **Vague topic**: Ask for specific angle or target audience.
- **No keyword provided**: Suggest keyword research or ask for target phrase.
- **Overly broad scope**: Recommend splitting into series or narrowing focus.
- **Competing with own content**: Check for cannibalization; suggest consolidation.

## Resources

- [Ahrefs Content Gap Analysis](https://ahrefs.com/content-gap)
- [Clearscope](https://www.clearscope.io/) - Content optimization
- [SurferSEO](https://surferseo.com/) - SERP analysis
- [AnswerThePublic](https://answerthepublic.com/) - Question research
