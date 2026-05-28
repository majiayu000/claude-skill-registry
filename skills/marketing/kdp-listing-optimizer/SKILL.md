---
name: kdp-listing-optimizer
description: Optimize Amazon KDP book listings for maximum conversion and discoverability. Use when creating or improving book titles, subtitles, descriptions, backend keywords, A+ content, author bios, or any Amazon product listing element. Triggers on requests to write book descriptions, optimize Amazon listings, improve book metadata, or enhance KDP product pages.
---

# KDP Listing Optimizer

Create high-converting Amazon book listings using proven copywriting frameworks.

## Listing Anatomy & Character Limits

| Element | Limit | Impact |
|---------|-------|--------|
| Title | 200 chars | SEO + Click-through |
| Subtitle | 200 chars | Keywords + Clarity |
| Description | 4,000 chars | Conversion |
| Backend Keywords | 7 × 50 chars | Discoverability |
| Author Bio | 2,000 chars | Trust |
| Editorial Reviews | 1,200 chars each | Social Proof |

## Title Optimization Formula

**Structure:** `[Primary Keyword]: [Promise/Benefit] - [Differentiator]`

**Examples:**
```
❌ Weak: "My Book About Marketing"
✅ Strong: "Digital Marketing Mastery: The Step-by-Step System to Generate Leads and Sales Online - Even If You're Starting From Zero"
```

**Title Checklist:**
- [ ] Primary keyword in first 5 words
- [ ] Clear benefit or outcome
- [ ] Specific (numbers, timeframes, audiences)
- [ ] Under 80 characters for mobile display

## Description Framework: PASTOR

Write descriptions using the PASTOR formula:

### P - Problem
```
Open with the reader's pain point. Use "you" language.

Example:
"You've tried every diet, read every book, and still can't lose those last 20 pounds. The frustration of watching the scale refuse to budge—despite doing everything 'right'—is exhausting."
```

### A - Amplify
```
Make the problem feel urgent. What happens if unsolved?

Example:
"Every year that passes makes it harder. Your metabolism slows. Your energy drops. And that dream of feeling confident in your own skin fades further away."
```

### S - Story/Solution
```
Introduce yourself and your solution.

Example:
"After 15 years as a registered dietitian and helping 10,000+ clients, I discovered something surprising: the problem isn't willpower—it's your approach."
```

### T - Transformation
```
Paint the picture of success. What will life look like?

Example:
"Imagine waking up energized. Fitting into clothes you haven't worn in years. Having people ask what your secret is."
```

### O - Offer
```
Explain what's in the book. Use bullet points.

Example:
"Inside this book, you'll discover:
• The 3 metabolism myths keeping you stuck (and what to do instead)
• My proven 4-week reset protocol used by 10,000+ clients
• 50+ recipes that taste amazing AND burn fat
• The exact meal timing strategy that maximizes results"
```

### R - Response
```
Clear call-to-action.

Example:
"Scroll up and click 'Buy Now' to start your transformation today. Your future self will thank you."
```

## HTML Formatting for Descriptions

Amazon allows limited HTML in descriptions:

```html
<h2>Section Header</h2>
<p>Paragraph text goes here.</p>
<b>Bold text</b>
<i>Italic text</i>
<br> Line break
<ul><li>Bullet point</li></ul>
```

**Optimal Description Structure:**
```html
<h2>Are You Tired of [PROBLEM]?</h2>
<p>[Problem paragraph - 2-3 sentences]</p>

<h2>What If There Was a Better Way?</h2>
<p>[Solution intro - 2-3 sentences]</p>

<h2>Inside This Book, You'll Discover:</h2>
<ul>
<li><b>[Benefit 1]</b> - [Brief explanation]</li>
<li><b>[Benefit 2]</b> - [Brief explanation]</li>
<li><b>[Benefit 3]</b> - [Brief explanation]</li>
<li><b>[Benefit 4]</b> - [Brief explanation]</li>
<li><b>[Benefit 5]</b> - [Brief explanation]</li>
</ul>

<h2>Who Is This Book For?</h2>
<p>[Target audience description]</p>

<h2>About the Author</h2>
<p>[Brief credibility statement]</p>

<p><b>Ready to [TRANSFORMATION]?</b></p>
<p>Scroll up and click "Buy Now" to get started today!</p>
```

## Backend Keyword Strategy

### The 7-Keyword Framework

Amazon allows 7 keyword phrases (50 chars each). Optimize each slot:

| Slot | Strategy | Example |
|------|----------|---------|
| 1 | Main topic + audience | marketing book entrepreneurs |
| 2 | Problem keywords | lead generation struggling |
| 3 | Solution keywords | sales funnel automation |
| 4 | Comparison keywords | alternative to expert secrets |
| 5 | Format keywords | guide workbook exercises |
| 6 | Audience demographics | small business owner startup |
| 7 | Related topics | social media facebook ads |

### Keyword Rules

✅ **DO:**
- Use all 350 characters (7 × 50)
- Separate phrases with spaces
- Include misspellings people search
- Use singular and plural forms

❌ **DON'T:**
- Repeat title/subtitle words
- Use competitor brand names
- Include "book," "kindle," "ebook"
- Use quotation marks or punctuation

## A+ Content Modules

If Brand Registered, create A+ Content with 5-7 modules:

### Recommended Module Order

1. **Hero Banner** - Book cover + tagline
2. **About the Author** - Photo + credibility
3. **What You'll Learn** - 3-5 key takeaways
4. **Book Preview** - Table of contents or chapter preview
5. **Testimonials** - 2-3 reader quotes
6. **Comparison Chart** - Your book vs. alternatives
7. **CTA Banner** - Final push to purchase

### A+ Content Specs

| Module Type | Image Size | Text Limit |
|-------------|------------|------------|
| Standard Image | 970 × 600 px | None |
| Header | 970 × 300 px | None |
| Comparison Chart | 150 × 150 px icons | 250 chars/cell |
| Standard Text | N/A | 6,000 chars |

## Conversion Rate Optimization

### Above-the-Fold Checklist

First 300 characters of description = highest impact

- [ ] Hook in first sentence
- [ ] Specific number or stat
- [ ] Clear target audience
- [ ] Immediate benefit promise

### Social Proof Elements

| Element | Where | Impact |
|---------|-------|--------|
| Review quotes | Editorial Reviews | High |
| Credentials | Author Bio | High |
| Numbers served | Description | Medium |
| Awards/features | Editorial Reviews | Medium |

## Quick Reference: High-Converting Listing

```markdown
TITLE (80 chars ideal):
[Keyword]: [Specific Promise] for [Audience]

SUBTITLE (80 chars ideal):
The [Framework/System] to [Outcome] in [Timeframe]

DESCRIPTION (2,500-3,500 chars optimal):
├── Hook (problem) - 150 chars
├── Amplify pain - 200 chars
├── Solution intro - 200 chars
├── "What you'll learn" bullets - 800 chars
├── Target audience - 200 chars
├── Author credibility - 200 chars
└── CTA - 100 chars

KEYWORDS (7 × 50 chars):
Slot 1: [topic] [audience] [format]
Slot 2: [problem] [pain point]
Slot 3: [solution] [outcome]
Slot 4: [comparison] [alternative]
Slot 5: [format] [style] [approach]
Slot 6: [demographic] [role]
Slot 7: [related] [adjacent topics]
```

## Scripts

- **Keyword analyzer**: See `scripts/keyword_analyzer.py`
- **Description validator**: See `scripts/description_validator.py`
