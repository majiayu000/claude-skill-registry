---
name: meta-tags-optimizer
description: Creates and optimizes meta tags including title tags, meta descriptions, Open Graph tags, and Twitter cards for maximum click-through rates and social sharing engagement.
---

# Meta Tags Optimizer

This skill creates compelling, optimized meta tags that improve click-through rates from search results and enhance social media sharing. It covers title tags, meta descriptions, and social meta tags.

## When to Use This Skill

- Creating meta tags for new pages
- Optimizing existing meta tags for better CTR
- Preparing pages for social media sharing
- Fixing duplicate or missing meta tags
- A/B testing title and description variations
- Optimizing for specific SERP features
- Creating meta tags for different page types

## What This Skill Does

1. **Title Tag Creation**: Writes compelling, keyword-optimized titles
2. **Meta Description Writing**: Creates click-worthy descriptions
3. **Open Graph Optimization**: Prepares pages for social sharing
4. **Twitter Card Setup**: Optimizes Twitter-specific meta tags
5. **CTR Analysis**: Suggests improvements for better click rates
6. **Character Counting**: Ensures proper length for SERP display
7. **A/B Test Suggestions**: Provides variations for testing

## How to Use

### Create Meta Tags

```
Create meta tags for a page about [topic] targeting [keyword]
```

```
Write title and meta description for this content: [content/URL]
```

### Optimize Existing Tags

```
Improve these meta tags for better CTR: [current tags]
```

### Social Media Tags

```
Create Open Graph and Twitter card tags for [page/URL]
```

## Instructions

When a user requests meta tag optimization:

1. **Gather Page Information**

   ```markdown
   ### Page Analysis
   
   **Page URL**: [URL]
   **Page Type**: [blog/product/landing/service/homepage]
   **Primary Keyword**: [keyword]
   **Secondary Keywords**: [keywords]
   **Target Audience**: [audience]
   **Primary CTA**: [action you want users to take]
   **Unique Value Prop**: [what makes this page special]
   ```

2. **Create Optimized Title Tag**

   ```markdown
   ### Title Tag Optimization
   
   **Requirements**:
   - Length: 50-60 characters (displays fully in SERP)
   - Include primary keyword (preferably near front)
   - Make it compelling and click-worthy
   - Match search intent
   - Include brand name if appropriate
   
   **Title Tag Formula Options**:
   
   1. **Keyword | Benefit | Brand**
      "[Primary Keyword]: [Benefit] | [Brand Name]"
      
   2. **Number + Keyword + Promise**
      "[Number] [Keyword] That [Promise/Result]"
      
   3. **How-to Format**
      "How to [Keyword]: [Benefit/Result]"
      
   4. **Question Format**
      "What is [Keyword]? [Brief Answer/Hook]"
      
   5. **Year + Keyword**
      "[Keyword] in [Year]: [Hook/Update]"
   
   **Generated Title Options**:
   
   | Option | Title | Length | Power Words | Keyword Position |
   |--------|-------|--------|-------------|------------------|
   | 1 | [Title] | [X] chars | [words] | [Front/Middle] |
   | 2 | [Title] | [X] chars | [words] | [Front/Middle] |
   | 3 | [Title] | [X] chars | [words] | [Front/Middle] |
   
   **Recommended**: Option [X]
   **Reasoning**: [Why this option is best]
   
   **Title Tag Code**:
   ```html
   <title>[Selected Title]</title>
   ```
   ```

3. **Write Meta Description**

   ```markdown
   ### Meta Description Optimization
   
   **Requirements**:
   - Length: 150-160 characters (displays fully in SERP)
   - Include primary keyword naturally
   - Include clear call-to-action
   - Match page content accurately
   - Create urgency or curiosity
   - Avoid duplicate descriptions
   
   **Meta Description Formula**:
   
   [What the page offers] + [Benefit to user] + [Call-to-action]
   
   **Power Elements to Include**:
   - Numbers and statistics
   - Current year
   - Emotional triggers
   - Action verbs
   - Unique value proposition
   
   **Generated Description Options**:
   
   | Option | Description | Length | CTA | Emotional Trigger |
   |--------|-------------|--------|-----|-------------------|
   | 1 | [Description] | [X] chars | [CTA] | [Trigger] |
   | 2 | [Description] | [X] chars | [CTA] | [Trigger] |
   | 3 | [Description] | [X] chars | [CTA] | [Trigger] |
   
   **Recommended**: Option [X]
   **Reasoning**: [Why this option is best]
   
   **Meta Description Code**:
   ```html
   <meta name="description" content="[Selected Description]">
   ```
   ```

4. **Create Open Graph Tags**

   ```markdown
   ### Open Graph Tags (Facebook, LinkedIn, etc.)
   
   **Required OG Tags**:
   
   ```html
   <!-- Primary Open Graph Tags -->
   <meta property="og:type" content="[article/website/product]">
   <meta property="og:url" content="[Full canonical URL]">
   <meta property="og:title" content="[OG-optimized title - up to 60 chars]">
   <meta property="og:description" content="[OG description - up to 200 chars]">
   <meta property="og:image" content="[Image URL - 1200x630px recommended]">
   
   <!-- Optional but Recommended -->
   <meta property="og:site_name" content="[Website Name]">
   <meta property="og:locale" content="en_US">
   ```
   
   **OG Type Selection Guide**:
   
   | Page Type | og:type |
   |-----------|---------|
   | Blog post | article |
   | Homepage | website |
   | Product | product |
   | Video | video.other |
   | Profile | profile |
   
   **OG Title Considerations**:
   - Can be different from title tag
   - Optimize for social sharing context
   - More conversational tone acceptable
   - Up to 60 characters ideal
   
   **OG Description Considerations**:
   - Can be longer than meta description (up to 200 chars)
   - Focus on shareability
   - What would make someone click when shared?
   
   **OG Image Requirements**:
   - Recommended size: 1200x630 pixels
   - Minimum size: 600x315 pixels
   - Format: JPG or PNG
   - Keep text to less than 20% of image
   - Include branding subtly
   ```

5. **Create Twitter Card Tags**

   ```markdown
   ### Twitter Card Tags
   
   **Card Type Selection**:
   
   | Card Type | Best For | Image Size |
   |-----------|----------|------------|
   | summary | Articles, blogs | 144x144 min |
   | summary_large_image | Visual content | 300x157 min |
   | player | Video/audio | 640x360 min |
   | app | Mobile apps | 800x418 |
   
   **Twitter Card Code**:
   
   ```html
   <!-- Twitter Card Tags -->
   <meta name="twitter:card" content="[summary_large_image/summary]">
   <meta name="twitter:site" content="@[YourTwitterHandle]">
   <meta name="twitter:creator" content="@[AuthorTwitterHandle]">
   <meta name="twitter:title" content="[Title - 70 chars max]">
   <meta name="twitter:description" content="[Description - 200 chars max]">
   <meta name="twitter:image" content="[Image URL]">
   <meta name="twitter:image:alt" content="[Image description for accessibility]">
   ```
   
   **Twitter-Specific Considerations**:
   - Shorter titles work better (under 70 chars)
   - Include @mentions if relevant
   - Hashtag-relevant terms can help discovery
   - Test with Twitter Card Validator
   ```

6. **Additional Meta Tags**

   ```markdown
   ### Additional Recommended Meta Tags
   
   **Canonical URL** (Prevent duplicates):
   ```html
   <link rel="canonical" href="[Preferred URL]">
   ```
   
   **Robots Tag** (Indexing control):
   ```html
   <meta name="robots" content="index, follow">
   ```
   
   **Viewport** (Mobile optimization):
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```
   
   **Author** (For articles):
   ```html
   <meta name="author" content="[Author Name]">
   ```
   
   **Language**:
   ```html
   <html lang="en">
   ```
   
   **Article-Specific** (For blog posts):
   ```html
   <meta property="article:published_time" content="[ISO 8601 date]">
   <meta property="article:modified_time" content="[ISO 8601 date]">
   <meta property="article:author" content="[Author URL]">
   <meta property="article:section" content="[Category]">
   <meta property="article:tag" content="[Tag 1]">
   ```
   ```

7. **Generate Complete Meta Tag Block**

   ```markdown
   ## Complete Meta Tags
   
   Copy and paste this complete meta tag block:
   
   ```html
   <!-- Primary Meta Tags -->
   <title>[Optimized Title]</title>
   <meta name="title" content="[Optimized Title]">
   <meta name="description" content="[Optimized Description]">
   <link rel="canonical" href="[Canonical URL]">
   
   <!-- Open Graph / Facebook -->
   <meta property="og:type" content="[type]">
   <meta property="og:url" content="[URL]">
   <meta property="og:title" content="[OG Title]">
   <meta property="og:description" content="[OG Description]">
   <meta property="og:image" content="[Image URL]">
   <meta property="og:site_name" content="[Site Name]">
   
   <!-- Twitter -->
   <meta name="twitter:card" content="summary_large_image">
   <meta name="twitter:url" content="[URL]">
   <meta name="twitter:title" content="[Twitter Title]">
   <meta name="twitter:description" content="[Twitter Description]">
   <meta name="twitter:image" content="[Image URL]">
   
   <!-- Additional -->
   <meta name="robots" content="index, follow">
   <meta name="author" content="[Author]">
   ```
   ```

8. **Provide CTR Optimization Tips**

   ```markdown
   ## CTR Optimization Analysis
   
   ### Power Words Used
   - [Word 1] - Creates [emotion/action]
   - [Word 2] - Creates [emotion/action]
   
   ### CTR Boosting Elements
   
   | Element | Present | Impact |
   |---------|---------|--------|
   | Numbers | Yes/No | +20-30% CTR |
   | Current Year | Yes/No | +15-20% CTR |
   | Power Words | Yes/No | +10-15% CTR |
   | Question | Yes/No | +10-15% CTR |
   | Brackets | Yes/No | +10% CTR |
   
   ### A/B Test Suggestions
   
   Test these variations:
   
   **Version A** (Current):
   - Title: [Title]
   - Description: [Description]
   
   **Version B** (Test):
   - Title: [Alternative title]
   - Description: [Alternative description]
   - Hypothesis: [Why this might perform better]
   ```

## Example

**User**: "Create meta tags for a blog post about 'how to start a podcast in 2024'"

**Output**:

```markdown
## Meta Tags: How to Start a Podcast (2024)

### Title Tag
```html
<title>How to Start a Podcast in 2024: Complete Beginner's Guide</title>
```
**Length**: 54 characters ✅
**Keyword**: "how to start a podcast" at front ✅
**Power Words**: "Complete", "Beginner's" ✅

### Meta Description
```html
<meta name="description" content="Learn how to start a podcast in 2024 with our step-by-step guide. Covers equipment, hosting, recording, and launching your first episode. Start podcasting today!">
```
**Length**: 158 characters ✅
**Keyword**: Included naturally ✅
**CTA**: "Start podcasting today!" ✅

### Complete Meta Tag Block

```html
<!-- Primary Meta Tags -->
<title>How to Start a Podcast in 2024: Complete Beginner's Guide</title>
<meta name="description" content="Learn how to start a podcast in 2024 with our step-by-step guide. Covers equipment, hosting, recording, and launching your first episode. Start podcasting today!">
<link rel="canonical" href="https://yoursite.com/how-to-start-a-podcast/">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://yoursite.com/how-to-start-a-podcast/">
<meta property="og:title" content="How to Start a Podcast in 2024 (Complete Guide)">
<meta property="og:description" content="Everything you need to launch your podcast: equipment recommendations, hosting platforms, recording tips, and step-by-step launch checklist. No experience required.">
<meta property="og:image" content="https://yoursite.com/images/podcast-guide-2024.jpg">
<meta property="og:site_name" content="Your Site Name">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="How to Start a Podcast in 2024 🎙️">
<meta name="twitter:description" content="Complete beginner's guide to launching your podcast. Equipment, hosting, recording, and more.">
<meta name="twitter:image" content="https://yoursite.com/images/podcast-guide-2024.jpg">
<meta name="twitter:site" content="@YourHandle">

<!-- Article Tags -->
<meta property="article:published_time" content="2024-01-15T08:00:00+00:00">
<meta property="article:author" content="https://yoursite.com/author/name">
<meta property="article:section" content="Podcasting">
<meta property="article:tag" content="podcasting">
<meta property="article:tag" content="content creation">
```

### A/B Test Variations

**Title Variation B**:
"Start a Podcast in 2024: Step-by-Step Guide (+ Free Checklist)"

**Title Variation C**:
"How to Start a Podcast: 2024 Guide [Equipment + Software + Tips]"

**Description Variation B**:
"Want to start a podcast in 2024? This guide covers everything: equipment ($100 budget option), best hosting platforms, recording tips, and how to get your first 1,000 listeners."
```

## Page-Type Templates

### Homepage

```html
<title>[Brand Name] - [Primary Value Proposition]</title>
<meta name="description" content="[Brand] helps [audience] [achieve goal]. [Key feature/benefit]. [CTA]">
```

### Product Page

```html
<title>[Product Name] - [Key Benefit] | [Brand]</title>
<meta name="description" content="[Product] [key features]. [Price/offer if applicable]. [Social proof]. [CTA]">
```

### Blog Post

```html
<title>[How to/What is/Number] [Keyword] [Benefit/Year]</title>
<meta name="description" content="[What they'll learn]. [Key points covered]. [CTA]">
```

### Service Page

```html
<title>[Service] in [Location] - [Brand] | [Differentiator]</title>
<meta name="description" content="[Service description]. [Experience/credentials]. [Key benefit]. [CTA]">
```

## Tips for Success

1. **Front-load keywords** - Put important terms at the beginning
2. **Match intent** - Description should preview what page delivers
3. **Be specific** - Vague descriptions get ignored
4. **Test variations** - Small changes can significantly impact CTR
5. **Update regularly** - Add current year, refresh messaging
6. **Check competitors** - See what's working in your SERP

## Related Skills

- [seo-content-writer](../seo-content-writer/) - Create content for meta tags
- [schema-markup-generator](../schema-markup-generator/) - Add structured data
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) - Audit all meta tags
- [serp-analysis](../../research/serp-analysis/) - Analyze competitor meta tags

