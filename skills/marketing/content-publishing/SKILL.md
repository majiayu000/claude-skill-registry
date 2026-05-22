---
name: Content Publishing
slug: content-publishing
description: Automated content publishing pipeline for ID8Labs. Generates essays in Eddie's voice, publishes to id8labs.app, and distributes to social media (X, LinkedIn).
category: marketing
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "release"
  - "announce"
  - "publish"
  - "essay"
  - "research article"
  - "content pipeline"
  - "write release"
  - "post to X"
  - "post to LinkedIn"
tags:
  - content
  - publishing
  - social-media
  - essays
  - marketing
  - automation
  - voice
  - distribution
---

# Content Publishing Pipeline Skill

Automated content publishing pipeline for ID8Labs that integrates with Pipeline Stage 10.5 (ANNOUNCE). This skill generates essays in Eddie's authentic voice, publishes them to id8labs.app, and distributes derived social content to X/Twitter and LinkedIn.

From product releases to research articles, this skill orchestrates the complete journey from idea to multi-channel distribution while maintaining consistent voice and messaging.

## Core Workflows

### Workflow 1: Full Release Announcement Pipeline
**Purpose:** End-to-end release announcement from essay to social distribution

**Command:** `/announce-release`

**Steps:**
1. Generate release essay in Eddie's voice
2. Create MDX file with frontmatter
3. Commit to id8labs-hub repository
4. Wait for Vercel deployment
5. Generate social media slices
6. Post to X/Twitter
7. Post to LinkedIn
8. Update pipeline status

**Pipeline Flow:**
```
[Release Trigger]
       |
[/write-release or /write-research]
   Apply Eddie's voice profile
       |
[/publish-essay]
   Create MDX in id8labs-hub/core/content/essays/
   Git commit -> Vercel auto-deploy
       |
[/post-tweet]
   Generate X thread from essay
   Post to @id8labs
       |
[/post-linkedin]
   Adapt essay for LinkedIn
   Post to Eddie's profile
```

### Workflow 2: Generate Release Essay
**Purpose:** Write compelling release announcement in Eddie's voice

**Command:** `/write-release`

**Eddie's Voice Profile:**

**Core Moves:**
- Open unexpected (visceral, confessional)
- Hardship as credentials
- Pattern recognition (micro -> macro)
- Movement from I to We
- Direct loving close

**Signature Phrases:**
- "I'll be honest..."
- "Here's the thing about..."
- "I don't know about you but..."
- "(Loud ape sounds)"

**Tone Calibration:**
- Vulnerable but not weak
- Intense but not aggressive
- Raw but intentional

**Structure Pattern:**
1. Visceral opening - Sound, confession, or unexpected entry
2. Personal context - Where you've been, what shaped you
3. Observation/Pattern - What you're seeing that others miss
4. Universal connection - How your story is everyone's story
5. Call to collective action - The invitation to join
6. Warm direct close - Love, gratitude, solidarity

### Workflow 3: Generate Research Article
**Purpose:** Write thought leadership content around product themes

**Command:** `/write-research`

**Steps:**
1. Define research topic
2. Gather sources and data
3. Apply Eddie's voice
4. Structure as thought piece
5. Include practical insights

### Workflow 4: Publish Essay to Website
**Purpose:** Commit essay as MDX file to id8labs-hub repository

**Command:** `/publish-essay`

**MDX Frontmatter Template:**
```yaml
---
title: "Essay Title"
slug: "essay-slug"
date: "2025-01-06"
category: "release"
excerpt: "Brief excerpt for previews"
author:
  name: "Eddie Belaval"
  avatar: "/images/eddie-avatar.jpg"
tags: ["tag1", "tag2"]
---
```

**Steps:**
1. Format essay as MDX
2. Generate slug and metadata
3. Commit to GitHub
4. Trigger Vercel deployment
5. Verify live URL

### Workflow 5: Social Media Distribution
**Purpose:** Generate and post platform-specific content

**Commands:** `/post-tweet`, `/post-linkedin`

**Twitter/X Strategy:**
- Under 280 characters for single tweet
- 5-tweet thread for complex topics
- Hook with main insight
- End with link to full essay

**LinkedIn Strategy:**
- Professional but authentic
- Include personal reflection
- 3-5 paragraphs
- Use line breaks for readability
- End with discussion question

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/announce-release` | Full pipeline: essay -> website -> X -> LinkedIn |
| `/write-release` | Generate release essay in Eddie's voice |
| `/write-research` | Generate research article in Eddie's voice |
| `/publish-essay` | Create MDX file, commit, and deploy to website |
| `/post-linkedin` | Post to LinkedIn via Playwright |
| `/post-tweet` | Post to X/Twitter via Playwright |

## Content Categories

| Category | When to Use |
|----------|-------------|
| `release` | Major product releases, new features |
| `research` | Insights discovered while building |
| `essay` | Long-form personal/technical writing |

## Website Integration

Essays are published to `id8labs.app/essays/{slug}`:
- MDX files go to: `/id8labs-hub/core/content/essays/`
- Frontmatter: title, subtitle, date, author, category, tags
- Vercel auto-deploys on git push to main

## Usage Examples

**Announce a release:**
```
/announce-release v1.2.0 "New dashboard with real-time metrics"
```

**Write a research article:**
```
/write-research "The 70% problem in AI tooling"
```

**Publish an essay manually:**
```
/publish-essay "My Essay Title" --content "<mdx content>"
```

## Best Practices

- **Voice Consistency:** Always apply Eddie's voice profile for authenticity
- **Platform Optimization:** Tailor content length and format for each platform
- **Timing:** Post during peak engagement hours (9-11am EST)
- **Thread Strategy:** Use threads for complex topics on X
- **Engagement:** Respond to comments within 24 hours
- **Cross-linking:** Link social posts to full essays
- **Analytics:** Track engagement metrics post-publication
- **Scheduling:** Plan content calendar in advance
- **A/B Testing:** Test different hooks and CTAs
- **Repurposing:** Turn essays into multiple social posts over time

## Output Locations

| Content Type | Location |
|--------------|----------|
| Essays | `https://id8labs.app/essays/{slug}` |
| X/Twitter | `https://x.com/id8labs/status/{id}` |
| LinkedIn | `https://linkedin.com/posts/{id}` |
| MDX Files | `id8labs-hub/core/content/essays/` |

## Requirements

- Git access to id8labs-hub repo
- Comet browser with debugging for social posting
- Logged into X as @id8labs
- Logged into LinkedIn as Eddie Belaval

## Pipeline Integration

This skill integrates with ID8Pipeline Stage 10.5:

```
Stage 10: Ship
    |
Stage 10.5: Announce <- Content Publishing Skill
    |
    |-- Generate essay
    |-- Publish to website
    |-- Post to X
    |-- Post to LinkedIn
    |
Stage 11: Listen & Iterate
```

Skip Stage 10.5 only for internal/minor releases that don't warrant public announcement.

## Error Handling

- **Generation Failures:** Retry with refined prompts
- **GitHub Conflicts:** Pull latest before commit
- **Deployment Timeouts:** Check Vercel dashboard manually
- **Social API Limits:** Space posts 1 hour apart
- **Platform Outages:** Queue content for later posting

## When to Use This Skill

Invoke this skill when:
- Announcing product releases
- Publishing thought leadership content
- Distributing content to social media
- Writing in Eddie's voice
- Managing the content pipeline
- Creating research articles
- Coordinating multi-channel publishing
