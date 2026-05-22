---
name: Blog Writing
description: Create SEO-optimized blog posts that engage readers and rank in search results
version: 1.0.0
triggers:
  - "blog post"
  - "write blog"
  - "create article"
  - "blog article"
  - "skill:blog-writing"
---

# Blog Writing

## Purpose

This skill transforms topics into polished, SEO-optimized blog posts that:
- Engage readers from headline to CTA
- Rank in search engine results
- Establish thought leadership
- Drive organic traffic and conversions

## When to Use This Skill

- Creating educational how-to guides
- Writing thought leadership pieces
- Producing listicles and comparison posts
- Writing case studies and success stories
- Creating evergreen content for SEO
- Publishing news commentary and analysis

## Core Concepts

### SEO-First Structure

```typescript
interface BlogPost {
  title: string;           // Keyword-rich, 50-60 chars
  metaDescription: string; // 150-160 chars, includes CTA
  headings: H2[];          // 3-7 H2s for readability
  paragraphs: Paragraph[]; // 2-4 sentences each
  keywords: string[];      // Primary + 3-5 secondary
  links: ExternalLink[];   // 2-4 authoritative sources
}
```

### The Skyscraper Technique

1. Find top-ranking content for target keyword
2. Identify gaps and improvement opportunities
3. Create comprehensive content (2x better)
4. Reach out for backlinks

### Content Pillar Strategy

```markdown
Pillar Page (10,000+ words)
├── Topic Cluster Content 1 (1,500 words)
├── Topic Cluster Content 2 (1,500 words)
├── Topic Cluster Content 3 (1,500 words)
└── Topic Cluster Content 4 (1,500 words)
```

## Patterns

### Pattern 1: How-To Guide Structure

```markdown
# How to [Achieve Desired Outcome]: [Timeframe or Method]

## What You'll Learn
- Learning outcome 1
- Learning outcome 2
- Learning outcome 3

## Step 1: [First Major Step]
### What You're Doing
[Clear explanation in 2-3 sentences]

### Why It Matters
[Brief rationale]

### How to Do It
1. [Sub-step with detail]
2. [Sub-step with detail]
3. [Sub-step with detail]

### Pro Tips
- Insider technique
- Common mistake to avoid

## Step 2: [Second Major Step]
[Same structure]

## Common Challenges
| Challenge | Solution |
|-----------|----------|
| [Challenge 1] | [Solution 1] |
| [Challenge 2] | [Solution 2] |

## FAQ
**Q: [Common question]**
A: [Direct answer]

## Your Turn
[Actionable CTA with next step]
```

### Pattern 2: Listicle Structure

```markdown
# [Number] [Powerful Adjective] Ways to [Desired Outcome]

## Why [Desired Outcome] Matters
[Compelling hook, 2-3 paragraphs]

## The Methods
1. **[Method 1]**
   - Description with context
   - When to use this approach
   - Example implementation

2. **[Method 2]**
   - [Same structure]

3. **[Method 3]**
   - [Same structure]

[...continue through all methods]

## My Top Pick
[Reasoning for best method with evidence]

## Quick Implementation Checklist
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3
```

## Step-by-Step Process

1. **Keyword Research**
   - Use Ahrefs/Semrush for volume and difficulty
   - Find long-tail variations
   - Analyze search intent (informational, navigational, transactional)

2. **Content Brief Creation**
   - Define primary keyword
   - Identify 3-5 secondary keywords
   - Outline H2 structure
   - Specify word count target (1,500-3,000 words)

3. **Drafting**
   - Write H2s first as outline
   - Expand each section with 2-4 paragraphs
   - Include examples, statistics, expert quotes

4. **SEO Optimization**
   - Place primary keyword in title, H1, first paragraph, conclusion
   - Add secondary keywords in H2s and naturally throughout
   - Include 2-4 external links to authoritative sources
   - Add internal links to related content

5. **Review and Refine**
   - Check readability (aim for Grade 6-8)
   - Verify all claims have citations
   - Test mobile formatting
   - Run through SEO checklist

## FrankX Application

```markdown
# How to Create Transformative Content That Changes Minds

**[FrankX Brand Voice: Provocative, visionary]**

The content landscape has shifted. Yesterday's SEO tricks won't work tomorrow.

Here's how to create content that doesn't just rank—it transforms.

## Why Traditional Content Fails

Most content gets ignored because it:

- States the obvious
- Lacks distinct perspective
- Fails to challenge assumptions

## The FrankX Approach

[Your brand-specific framework with consciousness/transformation themes]

## Quick Implementation
1. Lead with a provocative premise
2. Back it with evidence
3. Connect to transformation
4. End with actionable framework
```

## Anti-Patterns

| Bad Practice | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| Keyword stuffing | Hurts readability, penalized by Google | Natural keyword integration |
| Generic introductions | Fails to hook readers | Start with hook, story, or question |
| Thin content (<1,000 words) | Doesn't satisfy search intent | Comprehensive 1,500+ words |
| No clear CTA | Misses conversion opportunity | Specific, actionable next step |
| Ignoring featured snippets | Loses valuable SERP real estate | Answer question in 50 words |

## Quick Commands

```bash
# Create blog post from topic
skill:blog-writing, create a how-to guide about [TOPIC]

# Write thought leadership piece
skill:blog-writing, write an opinion piece on [TREND]

# Generate listicle
skill:blog-writing, create a listicle about [CATEGORY]

# SEO audit existing content
skill:seo-optimization, audit my blog post at [URL]
```

## Related Skills

- `seo-optimization` - Optimize content for search engines
- `content-strategy` - Plan content calendar and topics
- `social-media` - Promote blog posts across platforms
- `newsletter` - Distribute via email

## Resources

- `resources/templates.md` - Blog post templates for different types
- `resources/seo-checklist.md` - Pre-publication SEO verification
- `resources/examples.md` - High-performing blog post examples
