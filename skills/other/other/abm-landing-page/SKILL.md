---
name: abm-landing-page
description: Create personalized ABM (Account-Based Marketing) landing pages for specific prospects. Takes a LinkedIn URL, analyzes their background, and creates a targeted landing page that feels authentic (not AI-generated). Trigger words: "create landing page", "personalized page", "abm", "prospect page", "target page for"
allowed-tools: Bash, Read, Write, Edit, WebFetch, WebSearch, Task
---

# ABM Landing Page Skill

Create highly personalized landing pages for specific prospects that maximize conversion while avoiding AI detection patterns.

## Workflow

### Step 1: Profile Analysis

Given a LinkedIn URL, extract:

1. **Current role & company** - What do they do day-to-day?
2. **Past experience** - What tools/platforms have they used?
3. **Pain points** - Based on job descriptions, what problems do they face?
4. **Industry jargon** - What specific terms would they use?
5. **Certifications** - What credentials do they have?

Use the LinkedIn profile to understand their world deeply.

### Step 2: Create Segment-Based URL

**NEVER use the person's name in the URL.** Create a segment that looks like a category page:

| Bad | Good |
|-----|------|
| `/for/jon` | `/for/uipath-certified` |
| `/for/sarah-smith` | `/for/rpa-consultants` |
| `/for/john-doe` | `/for/enterprise-it-leaders` |

The URL should look like it's targeting a role/segment, not an individual.

### Step 3: Content Guidelines

#### DO:
- Use industry-specific jargon only insiders would know
- Reference specific tools/products they've used (e.g., `idx_aaname`, `DU model`, `Orchestrator`)
- Write conversational, slightly imperfect copy
- Vary sentence length and structure
- Include specific scenarios ("Saturday 2am. The upgrade failed.")
- Use casual language ("Classic.", "Ship it and hope.")

#### DON'T:
- Use emojis or icon grids
- Use buzzwords like "10x", "revolutionary", "transform", "self-healing"
- Use repetitive sentence structures
- Use overly polished, perfect prose
- Use generic marketing speak
- Mention the person's name anywhere on the page

### Step 4: Page Structure

```
app/for/[segment-name]/
  page.tsx       # Server component with metadata + JSON-LD schema
  client.tsx     # Client component with UI
```

#### page.tsx Template (with SEO/AEO optimizations)

```tsx
import { Metadata } from "next";
import SegmentPageClient from "./client";

export const metadata: Metadata = {
  title: "For [Segment] | Mediar",
  description: "[Short, casual description of the pain point]",
  robots: "noindex, nofollow", // Private page - don't index
};

// JSON-LD Schema for AI/search crawlers
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Article",
  headline: "[Page headline]",
  description: "[Description]",
  datePublished: "2026-01-20",
  dateModified: "2026-01-20",
  author: { "@type": "Organization", name: "Mediar", url: "https://mediar.ai" },
  publisher: { "@type": "Organization", name: "Mediar", url: "https://mediar.ai" },
  mainEntity: {
    "@type": "FAQPage",
    mainEntity: [
      // Add FAQ items based on their pain points
      {
        "@type": "Question",
        name: "[Question they'd ask]",
        acceptedAnswer: { "@type": "Answer", text: "[Direct answer]" },
      },
    ],
  },
};

export default function SegmentPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <SegmentPageClient />
    </>
  );
}
```

#### client.tsx Structure

Use semantic HTML for AI crawlers:

```tsx
<article>
  <header>  {/* Hero section */}
    <h1>...</h1>
    <p>Updated <time dateTime="2026-01-20">January 2026</time></p>
  </header>

  <section>  {/* TL;DR */}
    <h2>TL;DR</h2>
    <ul>...</ul>
  </section>

  <section>  {/* Pain points */}
    <h2>...</h2>
  </section>

  <section>  {/* Comparison - use <table> not divs */}
    <h2>...</h2>
    <table>...</table>
  </section>

  <section>  {/* Social proof */}
    <h2>...</h2>
  </section>

  <section>  {/* Demo/Video */}
    <h2>...</h2>
  </section>

  <section>  {/* CTA */}
    <h2>...</h2>
  </section>
</article>
```

**Section Order:**
1. **Header/Hero** - One punchy question about their main pain point + visible date
2. **TL;DR** - 3-4 bullet key takeaways (AI loves this)
3. **Pain Points** - 4-6 specific scenarios they'd recognize (no icons)
4. **Comparison** - Their current tool vs Mediar (use `<table>`, not divs)
5. **Social Proof** - Testimonials from similar roles
6. **Demo/Video** - Concrete example relevant to their work
7. **CTA** - Simple, low-commitment ask

### Step 5: PostHog Tracking

Track page views and CTA clicks with segment identifiers (not personal info):

```tsx
useEffect(() => {
  if (posthog) {
    posthog.capture("segment_page_viewed", {
      page: "/for/[segment]",
      segment: "[segment_identifier]",
    });
  }
}, [posthog]);
```

---

## Anti-AI Detection Checklist

Before shipping, verify:

- [ ] URL uses segment name, not person's name
- [ ] No person's name appears anywhere on page
- [ ] No emoji icons in content
- [ ] No generic buzzwords (10x, revolutionary, transform, unlock, empower)
- [ ] Sentence lengths vary significantly
- [ ] Some sentences are short. Really short.
- [ ] Industry jargon is specific and accurate
- [ ] Copy has personality quirks (em-dashes, fragments, casual asides)
- [ ] Transitions aren't too smooth/perfect
- [ ] Specific scenarios beat generic benefits

---

## Example Pain Points by Role

### UiPath Developer
- Selector maintenance (`aaname`, `idx`, anchor elements)
- Exception handling (try-catch everything)
- Document Understanding training
- Orchestrator updates/maintenance windows
- Version compatibility issues
- Teaching junior devs best practices

### Power Automate User
- Desktop flow reliability
- Connection refresh issues
- Premium connector costs
- Flow run history limits
- Debugging cloud flows

### IT Manager (RPA)
- Bot licensing costs ($420/bot/month)
- Infrastructure overhead
- Scaling attended vs unattended
- Security/compliance concerns
- Measuring ROI

### Finance/Ops (End User)
- Manual data entry between systems
- Copy-paste errors
- Month-end close delays
- Report generation time
- Audit trail requirements

---

## Copy Style Guide

### Headers
- Questions work well: "What if selectors just worked?"
- Casual statements: "The stuff that eats your week"
- Direct: "Same task, different approach"

### Descriptions
Write like you're talking to a colleague:

**Too polished (AI-sounding):**
> "Our advanced AI-powered automation platform revolutionizes enterprise workflow management through intelligent self-healing capabilities."

**Better (human):**
> "You know the drill. Chrome updates, your idx_aaname breaks. Someone touches the DOM, your anchor element vanishes. We got tired of it too."

### CTAs
Keep them casual:
- "Book 15 min" (not "Schedule Your Personalized Demo Today")
- "Or check the code" (not "Explore Our Open Source Repository")
- "See how we handle it" (not "Discover How Our Platform Transforms Your Workflows")

---

## File Locations

- Landing pages: `app/for/[segment]/`
- Shared components: Use existing components from `components/`
- Lead capture: Use `LeadCaptureModal` from `components/landing/lead-capture-modal`

---

## Quick Start

When user provides a LinkedIn URL:

1. Visit the profile and extract role, experience, skills
2. Identify their likely pain points based on tools they've used
3. Create segment name from their role (e.g., "uipath-certified", "rpa-consultants")
4. Generate `page.tsx` and `client.tsx` in `app/for/[segment]/`
5. Run dev server and preview in browser
6. Iterate based on feedback

---

---

## SEO & AI Search Optimization (AEO)

AI systems (ChatGPT, Perplexity, Claude, Google AI Overviews) now extract and cite content. Traditional SEO focused on ranking in Google's 10 blue links. Now you're also optimizing for:

- AI Overviews (Google's AI-generated summaries)
- ChatGPT/Bing Chat responses
- Perplexity, Claude, Gemini and other AI assistants
- Traditional search (still matters, but shrinking share of clicks)

### Key Concepts

#### 1. Answer Engine Optimization (AEO)

AI systems extract and synthesize answers. Your content needs to be:
- **Directly answerable** - Clear, concise statements that AI can quote
- **Well-structured** - Headers, lists, tables that parse cleanly
- **Authoritative** - Cited sources, credentials, E-E-A-T signals

#### 2. What AI Models Prioritize

- **Recency** - Fresh, updated content (datestamps matter)
- **Specificity** - Detailed, niche expertise over generic coverage
- **Consensus** - Information that aligns with authoritative sources
- **Structure** - Schema markup, FAQs, clear hierarchies

#### 3. Citation Optimization

When AI cites sources, it favors:
- Original research/data
- First-hand expertise
- Unique perspectives not found elsewhere
- Well-organized reference content

### Tactical Changes

#### Content Format

**OLD:** 2000-word SEO articles padded with fluff
**NEW:** Dense, skimmable, fact-rich content with clear takeaways

#### Structure That Works

- Lead with the answer (inverted pyramid)
- Use descriptive H2/H3s that could be standalone queries
- Include "What is X" and "How to Y" sections
- Add FAQ schema for common questions
- Tables for comparisons (AI loves structured data)

#### Technical Must-Haves

- **Schema markup** - FAQ, HowTo, Article, Organization
- **Fast load times** - AI crawlers have timeouts
- **Clean HTML** - Semantic markup over div soup
- **Indexable content** - No JS-only rendering for critical content

### What's Declining vs Rising

**Declining:**
- Keyword stuffing (AI understands semantics)
- Thin affiliate content (AI prefers primary sources)
- Link farms/PBNs (less weight in AI training data curation)
- Click-bait titles (AI evaluates content quality, not CTR)

**Rising:**
- Topical authority - Deep coverage of your niche
- Brand mentions - Even without links, mentioned brands get cited
- Community presence - Reddit, forums, discussions influence AI
- Multi-format content - Video transcripts, podcasts feed AI training

### Quick Wins

1. Add FAQ sections with natural questions
2. Update publish dates and content regularly
3. Create comparison tables for your category
4. Write definitive "What is X" explainers
5. Get mentioned in Reddit/forum discussions
6. Claim and optimize your knowledge panel
7. Use structured data aggressively

### Key HTML Tags Reference

| Tag/Attribute | Purpose |
|--------------|---------|
| `<article>` | Semantic content wrapper |
| `<time datetime="">` | Machine-readable dates |
| `<h1>` - `<h3>` | Clear hierarchy (one H1) |
| `<ul>`, `<ol>` | Lists AI can parse |
| `<table>` | Comparisons, data |
| `itemscope/itemprop` | Inline microdata |
| `application/ld+json` | Structured data blocks |

### Minimum Viable Implementation

Every ABM landing page MUST have:

1. One JSON-LD block per page (Article or FAQPage)
2. Semantic HTML (`<article>`, `<section>`, `<header>`, `<time>`)
3. Clear H1 → H2 → H3 hierarchy
4. Visible "Updated: [date]" near title
5. TL;DR or Key Takeaways at top

### FAQ Schema Template

Add questions based on their pain points:

```json
{
  "@type": "Question",
  "name": "How does Mediar handle selector maintenance?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "Mediar uses AI to locate UI elements by their visual appearance and context, not brittle selectors. When Chrome updates or the DOM changes, the AI adapts automatically."
  }
}
```

### Schema Types by Page

| Page Type | Recommended Schema |
|-----------|-------------------|
| ABM Landing Page | Article + FAQPage |
| Compare pages | ComparisonTable or ItemList |
| Case studies | Article with author, datePublished |
| How-to content | HowTo schema |
| Solutions pages | Article or Service schema |

---

## Resources

- Anti-AI detection research: https://octet.design/journal/how-to-detect-ai-content/
- SEO/AEO guide: `C:\Users\User\SEO & AI Search Optimization Cras.txt`
- Existing landing pages to reference: `app/compare/` directory
- Lead capture component: `components/landing/lead-capture-modal.tsx`
- PostHog setup: See `posthog` skill
