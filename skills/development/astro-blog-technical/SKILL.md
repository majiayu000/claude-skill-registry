---
name: astro-blog-technical
description: Phase 4 - Technical implementation (frontmatter, schema, performance)
---

# Astro Blog - Phase 4: Technical

**Priority Legend:**
- ⭐ **ALWAYS** - Every article, non-negotiable
- 💡 **OPTIONAL** - Enhancement when relevant

---

## Technical Implementation

### ⭐ Frontmatter (Every Article)
```yaml
---
title: "Solar Panel Cost UK 2026: Complete Guide"  # 50-60 chars
description: "Solar panels cost £5,000-£8,000 in the UK. Compare prices, savings, and grants for 2026. Get accurate quotes in 60 seconds."  # 150-160 chars
pubDate: 2026-01-15
intent: commercial  # informational | commercial | comparison | transactional
topic: solar-panels  # For pillar-cluster linking
primaryCTA: quote-calculator  # GTM tracking
category: solar-energy
author: team  # Use named author for YMYL content
entities: [solar panels, installation cost, energy savings, government grants, ROI, inverter, monocrystalline, payback period]  # 5-10 items
pillar: false  # true = 2500+ words + 8-12 internal links
experienceVerified: false  # true ONLY after human verifies ExperienceBlock data
---
```

**Meta description formula:** [Answer] + [Benefit] + [Proof] + [CTA]
Example: "Solar panels cost £5,000-£8,000 in the UK (2026). Save £600/year on energy bills. Compare quotes from MCS-certified installers. Get accurate pricing in 60 seconds."

### ⭐ Structured Data (@graph Schema)
Required schema markup for every article:

**Article schema (always required):**
```json
{
  "@type": "Article",
  "headline": "Solar Panel Cost UK 2026: Complete Guide",
  "description": "...",
  "datePublished": "2026-01-15",
  "dateModified": "2026-01-15",
  "author": { "@type": "Person", "name": "...", "sameAs": "https://linkedin.com/in/..." }
}
```

**FAQ schema (REQUIRED for commercial/comparison):**
- [ ] 3-5 questions (standard) or 5-8 questions (pillar)
- [ ] Use actual PAA questions from Google
- [ ] Each answer 40-60 words

**HowTo schema (REQUIRED for process/guide articles):**
- [ ] 3-10 steps
- [ ] Each step has name + text
- [ ] Include time estimates if applicable

**Author Person schema:**
```json
{
  "@type": "Person",
  "name": "John Smith",
  "jobTitle": "Solar Energy Consultant",
  "sameAs": "https://linkedin.com/in/johnsmith",
  "image": "/authors/john-smith.jpg"
}
```

**VideoObject schema (if video present):**
- [ ] Include chapter timestamps (min 3)
- [ ] Format: "0:00 Introduction, 2:15 Cost Breakdown, 5:40 Savings Calculator"

### ⭐ Technical Quality (Every Article)
- [ ] **TypeScript strict** - No `any` types, explicit return types on functions
- [ ] **Component hydration** - NEVER use `client:load`. ONLY `client:visible` (on scroll) or `client:idle` (after page interactive)
- [ ] **Performance budgets** - <100KB JavaScript, <50KB CSS, ≥90 mobile Lighthouse score, ≥95 desktop Lighthouse score
- [ ] **Image optimization** - Hero: `loading="eager"` + `fetchpriority="high"`. All others: `loading="lazy"`. Descriptive alt text on ALL images
- [ ] **ARIA labels** - Complex components (calculators, tabs, accordions) need `role` and `aria-label` attributes

### ⭐ E-E-A-T Signals (Every Article)
- [ ] **Author credentials** - Verifiable via LinkedIn + industry profile. For YMYL (health, finance), use named expert author
- [ ] **Experience content** - ExperienceBlock data must be real (verified case studies) OR marked as placeholder. NO fabricated data
- [ ] **Trust badges** - Display certifications, Which? Trusted Trader, trade body memberships near bio and CTAs

### 💡 llms.txt Update (Optional)
Add entry to `/public/llms.txt`:
```
# Solar Panel Cost UK 2026
Solar panels cost £5,000-£8,000 in the UK (2026). 4kW system saves £600/year. Compare monocrystalline vs polycrystalline. Government grants available.
> /blog/solar-panel-cost-uk-2026
```
Keep under 100 tokens per entry.

---

## Output Required

Provide:
1. **Complete frontmatter** - All required fields filled
2. **Schema markup** - Article + FAQ/HowTo + Author + Video (if applicable)
3. **Performance optimization** - Proper hydration, image loading, ARIA labels

---

## Next Step

After completing technical setup, use **astro-blog-validate** skill for Phase 5.
