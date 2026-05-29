---
name: astro-blog-validate
description: Phase 5 - Validation checks before publishing
---

# Astro Blog - Phase 5: Validation

**Priority Legend:**
- ⭐ **ALWAYS** - Every article, non-negotiable
- 🎯 **HIGH-VALUE** - Competitive keywords, commercial/pillar content

---

## Validation Checklist

### ⭐ Critical Checks (Must Pass - Every Article)
- [ ] **Human voice test** - Read first 3 paragraphs aloud. Would someone guess AI wrote this? If yes, rewrite with more variety and imperfection
- [ ] **Component density** - Count all components (QueryAnswer, TL;DR, ExpertInsight, EngagementHook, etc). Max 5-7 (standard), 8-12 (pillar)
- [ ] **Intentional typos** - Count typing errors. Need 2-4 per article (thier, recieve, definately). NOT grammar errors
- [ ] **AI pattern detection** - Check for: All answer-first paragraphs? Transition words (Moreover, Furthermore)? Meta-commentary (It's important to note)? If yes, fix

### ⭐ Readability Scores (Every Article)
Use hemingwayapp.com or readabilityformulas.com:
- [ ] **Hemingway Grade: 6-8** (max 10 acceptable)
- [ ] **Flesch Reading Ease: 60-70** (Plain English)
- [ ] **Flesch-Kincaid Grade: 8-10** (max 12 for technical)
- [ ] **Sentence length: <20%** of sentences exceed 25 words
- [ ] **Passive voice: <10%** of sentences

### ⭐ Content Quality (Every Article)
- [ ] **Intent declared** - Frontmatter has `intent` field
- [ ] **CTA matches intent** - Check mapping table (informational→Newsletter, commercial→Quote, etc)
- [ ] **Answer in first 120 words** - QueryAnswer contains specific, direct answer with numbers
- [ ] **TL;DR present** - If >1000 words, TL;DR with exactly 3 bullet points
- [ ] **TOC present** - If >800 words, table of contents after intro
- [ ] **H2 density** - 3-4 H2 sections (standard) or 5-8 H2 sections (pillar)
- [ ] **ExpertInsight count** - 1-2 (standard) or 2-3 (pillar). NOT one per H2 (too formulaic)

### ⭐ Structure (Every Article)
- [ ] **Internal links: 2-4** (standard) or 8-12 (pillar)
- [ ] **First link position** - Within first 100 words
- [ ] **Anchor text quality** - Descriptive phrases, no "click here" or "this article"
- [ ] **Images: 3-5** (standard) or 6-10 (pillar)
- [ ] **Image filenames** - Descriptive with keywords (solar-panels-uk-2026.webp)
- [ ] **Image captions** - Present on screenshots, case studies, charts
- [ ] **Visual spacing** - No text blocks >350 words without image/list/table
- [ ] **Paragraph length** - Max 100 words, prefer 50-80 words

### ⭐ External Links (Every Article)
- [ ] **Minimum 4 links** - 1 citation + 1 authority + 1 reputation + 1 contextual
- [ ] **Authority quality** - At least 2 links to: gov.uk, .ac.uk, Which?, trade bodies, or professional LinkedIn profiles
- [ ] **Context sentences** - Every external link has explanatory sentence (no "source" or "here" anchors)
- [ ] **Rel attributes** - All external links have `rel="noopener noreferrer"`. Affiliate links add `rel="nofollow sponsored"`

### ⭐ Technical Validation (Every Article)
- [ ] **Required frontmatter** - All fields present: title, description, pubDate, intent, topic, primaryCTA, category, author, entities
- [ ] **Meta description: 150-160 chars** - Use formula: [Answer] + [Benefit] + [Proof] + [CTA]
- [ ] **FAQ schema** - Required for commercial/comparison intent. 3-5 questions (standard), 5-8 (pillar)
- [ ] **HowTo schema** - Required for process/guide articles. 3-10 steps
- [ ] **TypeScript strict** - No `any` types in components
- [ ] **NO `client:load`** - All interactive components use `client:visible` or `client:idle`

### ⭐ Performance (Every Article)
Run Lighthouse audit:
- [ ] **PageSpeed Mobile ≥90**
- [ ] **PageSpeed Desktop ≥95**
- [ ] **Bundle sizes** - <100KB JavaScript, <50KB CSS
- [ ] **Hero image** - `loading="eager"` + `fetchpriority="high"`
- [ ] **Other images** - `loading="lazy"`

### ⭐ E-E-A-T (Every Article)
- [ ] **ExperienceBlock data** - Real case studies OR marked as placeholder. NO fabricated data
- [ ] **Author credentials** - Verifiable via LinkedIn profile link
- [ ] **All statistics sourced** - No "Studies show..." without citation and link

### 🎯 Information Gain (High-Value Articles)
- [ ] **At least ONE of:** (1) Original data/survey, (2) Unique case study, (3) Contrarian insight backed by evidence, (4) New framework/methodology, (5) Expert quote from interview

---

## Output Required

Confirm:
1. **All ⭐ checks passed** - List any failures that need fixing
2. **Readability scores** - Hemingway, Flesch scores meet targets
3. **Performance scores** - Lighthouse mobile ≥90, desktop ≥95
4. **Article ready to publish** - Yes/No

---

## Final Step

Article complete and validated. Ready to publish!
