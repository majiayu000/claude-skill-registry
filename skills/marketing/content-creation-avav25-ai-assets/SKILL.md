---
name: content-creation
description: Content creation tools, AI content generators, image generation workflows, copywriting patterns, page content optimization, blog authoring patterns, content research workflows, and SEO content sync procedures. Use when creating page content, blog posts, generating visuals with AI tools, writing conversion copy, optimizing landing pages, integrating external content services, or synchronizing content across metadata and structured data. Provides tool guides, prompt templates, content brief templates, and quality checklists.
user-invocable: true
---

# Content Creation

Systematic content creation skill with AI tool integration guides, copywriting templates, visual content workflows, and quality gates. Produces high-converting, brand-consistent page content using modern tools and services.

## When to Use

- Creating page content (headlines, body copy, CTAs, feature descriptions)
- Writing blog posts (research, content brief, authoring, cross-linking)
- Generating visual content with AI tools (Midjourney, DALL-E, Stable Diffusion)
- Writing landing page copy optimized for conversion
- Integrating external content generation services
- Optimizing existing page content for engagement and conversion
- Synchronizing content changes across visible text, SEO metadata, and JSON-LD structured data
- Creating content briefs for designers and copywriters

## When NOT to Use

- Designing UI components or layouts (use `ui-ux-design` skill)
- Writing technical documentation (use `Agent(content-writer)` role)
- Conducting SEO audits (use `/seo-review` workflow)
- Implementing frontend code (use `Agent(frontend-engineer)` role)

## AI Content Generation Tools

### Text Generation

| Tool | Best For | Integration |
|---|---|---|
| **ChatGPT (GPT-4o)** | Long-form copy, creative writing, brainstorming | API or web UI |
| **Claude** | Nuanced writing, analysis, brand voice adherence | API or web UI |
| **Gemini** | Multimodal content (text + image analysis) | API or web UI |
| **Jasper** | Marketing copy, ad copy, email sequences | SaaS platform |
| **Copy.ai** | Short-form copy, social media, product descriptions | SaaS platform |

### Image Generation

| Tool | Best For | Output Quality |
|---|---|---|
| **Midjourney** | Photorealistic images, artistic illustrations, brand visuals | Highest quality, best aesthetics |
| **DALL-E 3** | Quick concept images, illustrations, diagrams | Good quality, natural language prompts |
| **Stable Diffusion** | Custom fine-tuned models, batch generation, full control | Varies, highest flexibility |
| **Flux** | Fast generation, good quality, open source | High quality, fast |
| **Ideogram** | Text in images, logos, typography-heavy visuals | Best for text rendering |
| **Leonardo.ai** | Game assets, consistent characters, style transfer | Good for series/consistency |

### Stock and Asset Services

| Service | Content Type | License |
|---|---|---|
| **Unsplash** | Photography | Free commercial use |
| **Pexels** | Photography + Video | Free commercial use |
| **Undraw** | SVG illustrations | Free, customizable colors |
| **Storyset** | Animated illustrations | Free with attribution |
| **Lottie / LottieFiles** | Micro-animations | Free + premium |
| **Noun Project** | Icons | CC or paid license |
| **Envato Elements** | All creative assets | Subscription license |

### Video and Animation

| Tool | Best For |
|---|---|
| **Loom** | Quick product demos, walkthroughs |
| **Synthesia** | AI avatar videos, explainers |
| **Runway** | AI video generation, editing |
| **Rive** | Interactive animations for web |
| **Spline** | 3D web experiences |

## Content Quality Gates

Every piece of content must pass these gates before publication:

### Gate 1: Accuracy
- [ ] All product claims are verifiable
- [ ] Statistics cite sources
- [ ] Screenshots match current product version
- [ ] Pricing information is current
- [ ] Legal claims reviewed (guarantees, SLA, compliance)

### Gate 2: Brand Alignment
- [ ] Voice matches brand guidelines
- [ ] Tone appropriate for context and audience
- [ ] Terminology consistent with existing content
- [ ] Visual style matches brand identity
- [ ] No off-brand humor, slang, or references

### Gate 3: Conversion Optimization
- [ ] Clear value proposition above the fold
- [ ] Single primary CTA per section
- [ ] Benefits-focused (not feature-focused)
- [ ] Social proof near decision points
- [ ] Friction minimized (short forms, clear next steps)

### Gate 4: Accessibility
- [ ] All images have descriptive alt text
- [ ] Video has captions
- [ ] Text meets contrast requirements (4.5:1)
- [ ] Content readable at 200% zoom
- [ ] No information conveyed by color alone

### Gate 5: SEO and Content Sync
- [ ] Unique title tag with primary keyword
- [ ] Unique meta description
- [ ] Heading hierarchy (H1→H2→H3)
- [ ] Internal links with descriptive anchors
- [ ] Structured data where applicable
- [ ] All content surfaces in sync (see `seo-content-sync-checklist.md`)

### Gate 6: Legal and Ethics
- [ ] No fabricated testimonials or reviews
- [ ] No misleading before/after claims
- [ ] AI-generated images reviewed for artifacts and bias
- [ ] Proper attribution for third-party content
- [ ] License compliance for stock assets
- [ ] No dark patterns in copy

### Gate 7: Humanization (mandatory)
- [ ] Text scanned for AI writing patterns using `@humanizer` skill
- [ ] No AI vocabulary words (delve, foster, landscape, tapestry, underscore, vibrant, pivotal)
- [ ] No promotional inflation (nestled, groundbreaking, stunning, renowned)
- [ ] No chatbot artifacts or sycophantic tone
- [ ] No em dash overuse, emoji decoration, or bold-header lists
- [ ] No filler phrases, excessive hedging, or generic positive conclusions
- [ ] Anti-AI audit performed for text longer than 2 paragraphs
- [ ] Text sounds natural when read aloud

See `content-tools-guide.md` for detailed AI prompting workflows and `page-content-patterns.md` for proven page structure templates.

## Integration

- **Follows rules**: `Agent(content-designer)` (content strategy, conversion copy), `Agent(ui-ux-designer)` (visual direction), `humanize-content` rule (enforces AI pattern removal)
- **Used by workflows**: `/blog-post` (blog authoring), `/ui-ux-design` (content phase), `/docs` (public-facing content)
- **Skills**: `@humanizer` (Gate 7 — AI writing pattern removal)
- **Companion resources**: `content-tools-guide.md`, `page-content-patterns.md`, `seo-content-sync-checklist.md`
