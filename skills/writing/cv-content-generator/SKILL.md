---
name: cv-content-generator
description: Generate case studies, blog posts, experience updates, and variant content from the knowledge base. Use when user wants to create new CV content, write articles, or generate job-specific variants.
---

# CV Content Generator

<purpose>
Generate new content for the Universal CV portfolio by querying the knowledge base and producing structured output ready for the portfolio.
</purpose>

<when_to_activate>
Activate when the user:
- Wants to write a new case study
- Needs to create a blog post from experience
- Wants to generate a job-specific variant (redirect to `generate-variant` for full workflow)
- Needs to update experience highlights
- Asks for content based on achievements or stories

**Trigger phrases:** "create case study", "write blog post", "new content", "generate [content type]"
</when_to_activate>

<edge_cases>
| Scenario | Action |
|----------|--------|
| Full variant generation | Redirect to `generate-variant` skill for complete pipeline |
| Missing knowledge base data | Run `cv-data-ingestion` first |
| Content editing (not creation) | Use `cv-content-editor` instead |
| Writing style needed | Invoke `dmitrii-writing-style` before generating prose |
</edge_cases>

## Knowledge Base Structure

```
content/knowledge/
├── index.yaml           # Entities and relationships graph
├── achievements/        # Atomic accomplishments (STAR format)
├── stories/            # Extended narratives
├── metrics/            # Quantified results
└── raw/                # Unstructured source material
```

## Content Generation Workflow

### Step 1: Understand the Request
Determine output type:
- `case-study` → Full markdown with frontmatter for `content/case-studies/`
- `blog-post` → Markdown with frontmatter for `content/blog/`
- `variant` → YAML overrides for `content/variants/`
- `experience-update` → YAML additions for `content/experience/`

### Step 2: Query Knowledge Base

**Use deterministic scripts first** — faster and more consistent:

```bash
# Search by topic
npm run search:evidence -- --terms "revenue,growth,api"

# For variant generation with JD analysis
npm run analyze:jd -- --file source-data/jd-{company}.txt --save
npm run search:evidence -- --jd-analysis capstone/develop/jd-analysis/{slug}.yaml
```

**For deeper exploration:**
1. Read `content/knowledge/index.yaml` for entity definitions and relationships
2. Find relevant achievements in `content/knowledge/achievements/`
3. Find related stories in `content/knowledge/stories/`
4. Cross-reference themes and skills for comprehensive context

### Step 3: Generate Content

#### For Case Studies
Use this structure:
```markdown
---
id: [next number]
slug: [kebab-case-slug]
title: [Title]
company: [Company]
year: [Year]
tags: [relevant tags]
duration: [duration]
role: [role]

hook:
  headline: [3-second grab]
  impactMetric:
    value: "[X]"
    label: [metric type]
  subMetrics:
    - value: "[Y]"
      label: [secondary metric]
  thumbnail: null

cta:
  headline: [Call to action question]
  subtext: [Supporting text]
  action: calendly
  linkText: Let's talk →
---

[Opening hook - why this matters, stakes involved]

## The Challenge
[Problem statement with constraints]

## The Approach
[Hypothesis and alternatives considered table]

## Key Decision
[Critical decision point with trade-offs]

## Execution
[Phases with specific actions]

## Results
[Quantified outcomes]

## What I Learned
[Reflections - what worked, what didn't, key quote]
```

#### For Blog Posts
```markdown
---
slug: [slug]
title: [Title]
date: [YYYY-MM-DD]
tags: [tags]
excerpt: [1-2 sentence summary]
---

[Content following narrative structure from stories]
```

#### For Variants
```yaml
metadata:
  company: "[Company]"
  role: "[Role]"
  slug: "[company-role]"
  generatedAt: "[ISO timestamp]"
  jobDescription: "[JD summary]"

overrides:
  hero:
    status: "[Customized status]"
    subheadline: "[Tailored pitch]"
  about:
    tagline: "[Role-specific tagline]"
    bio: [Customized paragraphs]
    stats: [Relevant stats]

relevance:
  caseStudies:
    - slug: "[most relevant]"
      relevanceScore: 0.95
      reasoning: "[Why this matters for role]"
```

### Step 4: Validate Output
- Check all required frontmatter fields
- Ensure metrics are quantified
- Verify skills/themes match knowledge base
- Confirm narrative follows STAR format

## Examples

### Example 1: Generate Case Study
**User**: "Create a case study about the Ankr revenue growth"

**Action**:
1. Read `content/knowledge/achievements/ankr-15x-revenue.yaml`
2. Read `content/knowledge/index.yaml` for Ankr relationships
3. Generate full case study markdown
4. Output to `content/case-studies/` with proper frontmatter

### Example 2: Generate Variant
**User**: "Create a variant for a Technical PM role at Stripe"

**⚠️ For full variant workflow, use the `generate-variant` skill instead.**

Quick variant with scripts:
```bash
# 1. Analyze the JD
npm run analyze:jd -- --file source-data/jd-stripe.txt --save

# 2. Search for matching evidence
npm run search:evidence -- --jd-analysis capstone/develop/jd-analysis/stripe.yaml

# 3. Check bullet coverage
npm run check:coverage
```

**Action** (manual):
1. Query achievements with themes: `[infrastructure, revenue-growth]`
2. Find skills: `[api-design, compliance]`
3. Customize hero/about with payments/fintech angle
4. Score case studies by relevance to Stripe's domain
5. Output YAML + JSON variant files

## Output Locations

| Content Type | Output Path | Format |
|-------------|-------------|--------|
| Case Study | `content/case-studies/[##-slug].md` | Markdown |
| Blog Post | `content/blog/[date-slug].md` | Markdown |
| Variant | `content/variants/[company-role].yaml` | YAML + JSON |
| Experience | `content/experience/index.yaml` | YAML (append) |

## Quality Checklist

Before outputting content:
- [ ] All metrics are specific and quantified
- [ ] STAR format is complete (Situation, Task, Action, Result)
- [ ] Key quote/insight is memorable
- [ ] Tags align with knowledge base themes
- [ ] Frontmatter validates against schema
