---
name: astro-blog-structure
description: Phase 2 - Content Structure planning for blog articles
---

# Astro Blog - Phase 2: Structure

**Priority Legend:**
- ⭐ **ALWAYS** - Every article, non-negotiable
- 🎯 **HIGH-VALUE** - Competitive keywords, commercial/pillar content

**⚠️ CRITICAL:** Read `astro-blog/references/human-voice.md` NOW before planning structure to avoid AI-like patterns

---

## Content Structure Planning

### ⭐ Core Structure (Every Article)
- [ ] **H2 section density** - 3-4 sections (standard 1000-1500w) OR 5-8 sections (pillar 3000-5000w)
- [ ] **H2s are questions** - Prefer specific questions users actually ask. Example: "How much does solar panel installation cost in the UK?" NOT "Pricing Overview"
- [ ] **H3 subheadings** - Use only for H2 sections >400 words. Max 3-4 H3s per H2. Keeps content scannable
- [ ] **TOC required** - If article >800 words, add table of contents after intro
- [ ] **Component density limits** - Max 5-7 components (standard) or 8-12 (pillar). Components = QueryAnswer, TL;DR, ExpertInsight, EngagementHook, etc.
- [ ] **Visual breaks** - No more than 3 paragraphs (150-300 words) without image/list/table/component

### ⭐ Above-the-Fold Optimization (Every Article)
Must appear without scrolling:
- [ ] **Desktop layout (1920x1080)** - H1 (80-120px) + Hero image (400-500px) + QueryAnswer (150-200px) = ~850px total
- [ ] **Mobile layout (375x667)** - H1 (100-140px) + Hero 4:3 ratio (280-300px) + QueryAnswer first sentence (120-160px) = ~600px total
- [ ] **Hero image optimization** - Eager loading (`loading="eager"`), <100KB filesize, descriptive filename (solar-panels-uk-2026.webp)
- [ ] **QueryAnswer placement** - Immediately after hero image, contains direct answer in first 40-60 words

### ⭐ Required Components
- [ ] **QueryAnswer** - Direct answer <120 words with specific numbers. Example: "Solar panels cost £5,000-£8,000 in the UK (2026). A typical 4kW system saves £600/year..."
- [ ] **TL;DR** - If >1000 words, exactly 3 key takeaways in bullet list
- [ ] **ExpertInsight** - 1-2 (standard) or 2-3 (pillar). Practical insider tips, NOT generic advice
- [ ] **Author Bio** - 50-80 words at end. Format: [Experience] + [Credentials] + [Social proof] + [Location/specialization] + LinkedIn link

### ⭐ Internal Linking (Every Article)
- [ ] **Minimum links** - 2-4 (standard) or 8-12 (pillar) contextual internal links
- [ ] **First link placement** - Within first 100 words to related article
- [ ] **Descriptive anchors** - "solar panel installation costs" NOT "click here" or "this article"

### 🎯 Pillar-Cluster Linking (Pillar/Cluster Articles Only)
- [ ] **Bidirectional links** - Pillar links to ALL clusters (woven into sections). Each cluster links back to pillar (intro or conclusion). Related clusters link to each other
- [ ] **Contextual integration** - Links woven into prose with context. NOT listed at end. Example: "Understanding solar panel installation costs helps budget for the broader solar investment strategy."
- [ ] **Publication order** - Publish pillar first (establishes authority), then add 1-2 cluster articles per month

### ⭐ External Links (Every Article)
Minimum 4 external links:
- [ ] **1 citation link** - Academic/research supporting a claim (journal, .ac.uk, official study)
- [ ] **1 authority link** - Industry authority site (trade body, gov.uk, certification body)
- [ ] **1 reputation link** - High-authority mention (Which?, BBC, Guardian, LinkedIn profile)
- [ ] **1 contextual link** - Related resource that adds value for reader
- [ ] **Authority sites** - Prefer: gov.uk, .ac.uk, Which?, trade bodies, professional LinkedIn profiles
- [ ] **Context sentences** - Every link needs explanatory sentence. NO "source" or "here" as anchor text
- [ ] **Rel attributes** - All external links: `rel="noopener noreferrer"`. Affiliate links add: `rel="nofollow sponsored"`

### ⭐ Images & Video (Every Article)
- [ ] **Image count** - 3-5 images (standard) or 6-10 images (pillar). Roughly every 250-350 words
- [ ] **Descriptive filenames** - solar-panel-installation-uk-2026.webp NOT IMG_1234.jpg or image-1.webp
- [ ] **Image captions** - REQUIRED for: screenshots, before/after comparisons, case studies, charts/graphs
- [ ] **Video** - 0-1 video (standard) or 1-2 videos (pillar). Use facade loading (thumbnail + play button, loads on click). Include min 3 chapter timestamps

### 🎯 Conversion Elements (Commercial/Transactional)
- [ ] **Content upgrade** - REQUIRED for commercial/transactional. Offer gated PDF checklist, template, or detailed guide related to article topic
- [ ] **Interactive tool** - REQUIRED for transactional, strongly recommended for commercial. Calculator generates 22% of leads
- [ ] **Social proof** - 2-3 elements: Volume metrics ("500+ installations"), trust seals (MCS, Which?, certifications), testimonials with names
- [ ] **Review integration** - Display review snippets near QueryAnswer AND before primary CTA. Increases traffic 100%+

---

## Output Required

Provide full article outline with:
1. **H2 sections** (3-4 standard, 5-8 pillar) - all as questions
2. **Component placement** - Where each component appears
3. **Internal link targets** - 2-4 links (standard), 8-12 (pillar)
4. **Image descriptions** - What images needed and where
5. **CTA placement** - Where CTAs appear in flow

---

## Next Step

After completing structure, use **astro-blog-write** skill for Phase 3.
