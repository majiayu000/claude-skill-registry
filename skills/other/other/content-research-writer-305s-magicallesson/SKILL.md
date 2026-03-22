---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: Content Research Writer
description: "Research topics and write content like blog posts, articles, and copy"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: marketing
tags:
  - content
  - writing
  - blog
  - article
department: Marketing

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - create_docx
    - md_to_docx

# Skill Capabilities
capabilities:
  - content_creation
  - seo_writing
  - research

# Language Support
languages:
  - en
  - zh
---

# Content Research Writer

Research topics and create compelling content for blogs, articles, and marketing materials.

## Overview

This skill helps you:
- Research topics thoroughly
- Write engaging blog posts and articles
- Create SEO-optimized content
- Develop various content formats
- Maintain brand voice consistency

## How to Use

### Research Request
```
"Research [topic] for a blog post"
"What are the key points to cover about [subject]?"
"Find statistics and examples about [topic]"
```

### Writing Request
```
"Write a blog post about [topic]"
"Create a 1500-word article on [subject]"
"Draft social media posts about [topic]"
```

### With Guidelines
```
"Write about [topic] for [audience]. Tone: [professional/casual]. Include [requirements]."
```

## Content Types

### Blog Post
```markdown
# [Attention-Grabbing Title]

**Reading time**: [X] minutes
**Published**: [Date]

[Hook - opening that captures attention]

## Introduction
[Problem statement or context - why reader should care]

## [Main Section 1]
[Content with examples, data, insights]

### [Subsection if needed]
[Detailed information]

## [Main Section 2]
[Content continuing the narrative]

## [Main Section 3]
[Content building to conclusion]

## Key Takeaways
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

## Conclusion
[Summary and call to action]

---
**Related Articles**:
- [Link 1]
- [Link 2]
```

### Long-Form Article
```markdown
# [Title]: [Subtitle]

**Author**: [Name] | **Updated**: [Date] | **[X] min read**

> [Executive summary or key insight quote]

## Table of Contents
1. [Section 1]
2. [Section 2]
3. [Section 3]
...

## Introduction
[Context, importance, what reader will learn]

## [Section 1: Foundation]
[Comprehensive coverage]

### [Subsection]
[Details]

> **Expert Quote**: "[Quote]" — [Source]

## [Section 2: Deep Dive]
[Analysis, examples, case studies]

| Comparison | Option A | Option B |
|------------|----------|----------|
| [Factor 1] | [Value] | [Value] |
| [Factor 2] | [Value] | [Value] |

## [Section 3: Application]
[How-to, practical steps, implementation]

**Step 1**: [Action]
[Details]

**Step 2**: [Action]
[Details]

## Conclusion
[Summary, future implications, CTA]

## References
1. [Source 1]
2. [Source 2]
```

### How-To Guide
```markdown
# How to [Achieve Outcome]: A Step-by-Step Guide

**Difficulty**: [Beginner/Intermediate/Advanced]
**Time Required**: [Estimate]
**What You'll Need**: [Prerequisites]

## Overview
[Brief description of what reader will accomplish]

## Before You Start
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

## Step 1: [Action Verb + Task]
[Detailed instructions]

![Step 1 Screenshot/Image placeholder]

**Tip**: [Helpful tip for this step]

## Step 2: [Action Verb + Task]
[Detailed instructions]

⚠️ **Warning**: [Common mistake to avoid]

## Step 3: [Action Verb + Task]
[Detailed instructions]

## Troubleshooting
| Problem | Solution |
|---------|----------|
| [Issue 1] | [Fix] |
| [Issue 2] | [Fix] |

## Next Steps
Now that you've [accomplished X], you can:
- [Advanced topic 1]
- [Related skill 2]

## FAQ
**Q: [Common question]?**
A: [Answer]
```

### Listicle
```markdown
# [Number] [Topic] to [Benefit] in [Year]

[Brief intro explaining why this list matters]

## 1. [Item Name]
**Best for**: [Use case]

[Description - what it is and why it's included]

**Key Features**:
- [Feature 1]
- [Feature 2]

**Pros**: [Benefits]
**Cons**: [Drawbacks]

---

## 2. [Item Name]
[Same structure...]

---

## Comparison Table

| Tool | Price | Best For | Rating |
|------|-------|----------|--------|
| [1] | [Price] | [Use] | ⭐⭐⭐⭐⭐ |
| [2] | [Price] | [Use] | ⭐⭐⭐⭐ |

## Conclusion
[Summary of recommendations by use case]
```

## Research Output

### Topic Research Brief
```markdown
# Research Brief: [Topic]

## Overview
**Topic**: [Subject]
**Target Audience**: [Who]
**Content Goal**: [Inform/Persuade/Educate/Entertain]

## Key Points to Cover
1. [Main point 1]
   - Supporting info
   - Data/statistic
2. [Main point 2]
   - Supporting info
3. [Main point 3]

## Statistics & Data
| Stat | Source | Year |
|------|--------|------|
| [Statistic] | [Source] | [Year] |
| [Statistic] | [Source] | [Year] |

## Expert Quotes
> "[Quote]" — [Expert Name], [Title/Company]

## Common Questions (FAQ Potential)
1. [Question 1]?
2. [Question 2]?
3. [Question 3]?

## Competitor Content Analysis
| Article | Word Count | Strengths | Gaps |
|---------|------------|-----------|------|
| [URL 1] | [X] | [What's good] | [Missing] |

## Recommended Angle
[Unique perspective or approach to differentiate]

## Keywords
**Primary**: [main keyword]
**Secondary**: [keyword 2], [keyword 3]
**Long-tail**: [phrase 1], [phrase 2]
```

## SEO Guidelines

### Content Optimization
```markdown
## SEO Checklist

### Title
- [ ] Primary keyword included
- [ ] Under 60 characters
- [ ] Compelling and click-worthy

### Meta Description
- [ ] Primary keyword included
- [ ] 150-160 characters
- [ ] Clear value proposition

### Headers (H1, H2, H3)
- [ ] H1 matches/closely relates to title
- [ ] Keywords in H2s naturally
- [ ] Logical hierarchy

### Content
- [ ] Primary keyword in first 100 words
- [ ] Keyword density 1-2%
- [ ] Related keywords/LSI terms included
- [ ] Internal links: [X] links
- [ ] External links: [X] authoritative sources

### Media
- [ ] Images with alt text
- [ ] Compressed file sizes
- [ ] Descriptive file names

### Readability
- [ ] Short paragraphs (2-4 sentences)
- [ ] Subheadings every 300 words
- [ ] Bullet points for lists
- [ ] Reading level: [Grade X]
```

## Style Guidelines

### Tone Options
| Tone | Description | Example |
|------|-------------|---------|
| Professional | Formal, authoritative | "Research indicates that..." |
| Conversational | Friendly, relatable | "You know that feeling when..." |
| Educational | Clear, instructive | "Let's break this down..." |
| Persuasive | Compelling, action-oriented | "Imagine achieving..." |
| Playful | Fun, engaging | "Here's the plot twist..." |

### Best Practices
1. **Hook early**: First sentence should grab attention
2. **Be specific**: Data > vague claims
3. **Use examples**: Make abstract concrete
4. **Break it up**: Headers, bullets, images
5. **End strong**: Clear takeaway or CTA

## Limitations

- Cannot guarantee SEO rankings
- Statistics should be verified
- Cannot access paywalled sources
- Brand voice requires guidance
- Visual content descriptions only
