---
name: faion-content-marketer
description: "Content marketing: strategy, copywriting, SEO, email campaigns, social media."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Content Marketer Domain Skill

Content strategy, copywriting, SEO/AEO, email marketing, social media, video/podcast production, AI-powered content creation.

## Purpose

Orchestrates content marketing: strategy development, copywriting, SEO optimization, email campaigns, social media content, video/podcast production, and AI content tools.

## Context Discovery

### Auto-Investigation

Check these project signals to understand content marketing context:

| Signal | Location | What to Look For |
|--------|----------|------------------|
| Content strategy | `.aidocs/product_docs/article-lists/` | Editorial calendar, content themes, publication schedule |
| SEO keywords | `.aidocs/product_docs/seo/` | Target keywords, search intent, content gaps |
| Existing content | `content/`, `blog/`, `docs/` | Published articles, documentation, content quality |
| Email campaigns | `templates/email/`, analytics | Email sequences, onboarding flows, newsletter |
| Social presence | Social media profiles, analytics | Platform activity, engagement, content performance |
| Video/audio | YouTube, podcast platforms | Video content, podcast episodes, production quality |
| Analytics | Google Analytics, content metrics | Top pages, traffic sources, engagement rates |

### Discovery Questions

```yaml
question: "What's your primary content goal?"
header: "Content Goal"
multiSelect: false
options:
  - label: "Build SEO traffic"
    description: "Content marketing, SEO optimization, keyword targeting"
  - label: "Grow email list"
    description: "Lead magnets, email marketing, onboarding sequences"
  - label: "Social media growth"
    description: "Platform-specific content, viral mechanics, engagement"
  - label: "Launch video/podcast"
    description: "Video strategy, podcast planning, production workflows"
```

```yaml
question: "Which content channels are priorities?"
header: "Content Channels"
multiSelect: true
options:
  - label: "Blog/SEO content"
    description: "Long-form articles, pillar pages, SEO optimization"
  - label: "Email campaigns"
    description: "Newsletters, onboarding sequences, drip campaigns"
  - label: "Social media"
    description: "Twitter, LinkedIn, Reddit, TikTok, YouTube"
  - label: "Video content"
    description: "YouTube, TikTok, short-form video"
  - label: "Podcast"
    description: "Podcast strategy, production, distribution"
```

```yaml
question: "What's your content maturity level?"
header: "Content Maturity"
multiSelect: false
options:
  - label: "Starting from scratch"
    description: "Content strategy, editorial calendar, foundational content"
  - label: "Have basic content"
    description: "Optimize existing content, expand channels, grow traffic"
  - label: "Scaling content"
    description: "AI tools, workflows, multi-channel distribution"
  - label: "Advanced optimization"
    description: "A/B testing, personalization, conversion optimization"
```

## When to Use

| Scenario | Methodologies |
|----------|---------------|
| Content strategy | growth-content-marketing → ai-content-strategy |
| SEO content | growth-content-marketing → search-everywhere-optimization |
| Copywriting | growth-copywriting-fundamentals → growth-customer-testimonials |
| Email campaigns | growth-email-marketing → growth-onboarding-emails → growth-newsletter-growth |
| Social media | Platform-specific: growth-reddit-marketing, growth-youtube-strategy, growth-tiktok-basics |
| Video content | growth-youtube-strategy + AI video tools (references/) |
| Podcast | growth-podcast-strategy + podcast production (references/) |
| Webinars | growth-webinar-planning → growth-webinar-delivery |
| AI content tools | ai-marketing-tools-stack-2026 + image/video/audio generation (references/) |

## Methodologies (16)

### Content Strategy (2)
- growth-content-marketing.md
- ai-content-strategy.md

### Copywriting (2)
- growth-copywriting-fundamentals.md
- growth-customer-testimonials.md

### Email Marketing (3)
- growth-email-marketing.md
- growth-onboarding-emails.md
- growth-newsletter-growth.md

### Social Media (5)
- growth-reddit-marketing.md
- growth-tiktok-basics.md
- growth-tiktok-strategies.md
- growth-youtube-strategy.md
- growth-podcast-strategy.md

### Webinars (2)
- growth-webinar-planning.md
- growth-webinar-delivery.md

### SEO & Modern Search (2)
- search-everywhere-optimization.md
- ai-marketing-tools-stack-2026.md

## References (30)

### Strategy (5)
- content-marketing.md
- email-marketing.md
- social-media.md
- paid-advertising.md
- execution-patterns.md

### Image Generation (10)
- image-generation.md, image-generation-comparison.md, image-generation-dalle-midjourney-flux.md
- image-generation-sd-ideogram.md, image-generation-prompting.md, image-prompt-engineering.md
- dalle-generation.md, flux-generation.md, ideogram-generation.md
- midjourney-generation.md, stable-diffusion-generation.md

### Image Workflows (3)
- image-generation-workflows.md, image-editing-workflows.md, image-production-workflows.md

### Video (4)
- ai-video-platforms.md, video-marketing.md, video-editing-basics.md, ai-video-optimization.md

### Audio (7)
- ai-tts-text-to-speech.md, ai-stt-speech-to-text.md
- audio-tts-services.md, audio-stt-services.md
- audio-editing.md, audio-voice-agents.md
- podcast-production.md

## Related Skills

- faion-marketing-manager (parent orchestrator)
- faion-gtm-strategist (GTM for content distribution)
- faion-growth-marketer (content metrics, A/B testing)
- faion-seo-manager (technical SEO)
- faion-smm-manager (social media execution)

---

*Content Marketer v1.0 | 16 Methodologies | 30 References*
