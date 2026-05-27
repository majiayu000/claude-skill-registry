---
name: astro-blog-write
description: Phase 3 - Writing blog content with human voice and SEO optimization
---

# Astro Blog - Phase 3: Writing

**Priority Legend:**
- ⭐ **ALWAYS** - Every article, non-negotiable
- 🎯 **HIGH-VALUE** - Competitive keywords, commercial/pillar content

**⚠️ CRITICAL:** Read `astro-blog/references/human-voice.md` BEFORE writing to avoid AI patterns.

---

## Writing Guidelines

### ⭐ Human Voice (CRITICAL - Every Article)
- [ ] **Paragraph variety** - Mix 3 styles: (1) Answer-first for key points, (2) Narrative for stories/examples, (3) Build-up for engagement. NOT all answer-first (=robotic)
- [ ] **Component density check** - Article should feel natural, NOT template-like. If reader can "see the formula", you've overused components
- [ ] **Intentional imperfection** - 2-4 typing errors per article: thier, recieve, definately, enviroment, seperate, occured. NOT grammar errors (no "They was")

**Common AI patterns to AVOID:**
- Starting every paragraph with answer/conclusion
- Transition phrases: "Moreover," "Furthermore," "Additionally," "In conclusion,"
- Meta-commentary: "It's important to note," "It's worth mentioning," "Let's explore,"
- Overuse of "comprehensive," "robust," "delve into," "landscape," "realm"

### ⭐ Readability Standards (Every Article)
- [ ] **Paragraph length** - Max 100 words, prefer 50-80 words (2-3 sentences). Mobile-friendly
- [ ] **Sentence variety** - Mix lengths: Short (5-10 words), Medium (15-20 words), Long (25-30 words). Avoid monotony
- [ ] **Readability targets** - Hemingway Grade 6-8 (max 10), Flesch Reading Ease 60-70, <20% sentences >25 words, <10% passive voice
- [ ] **Technical definitions** - First mention of technical term: **bold** + 15-25 word definition. Example: "**Photovoltaic cells** convert sunlight directly into electricity using semiconductor materials."
- [ ] **List preference** - 3+ related items = use list format (NOT prose). Scannability + LLM extraction

### ⭐ Featured Snippet Optimization (Every Article)

**Paragraph snippets (40-60 words):**
Place immediately after relevant H2. Format:
```
## How much do solar panels cost in the UK?

Solar panels cost £5,000-£8,000 for a typical UK home in 2026. This includes panels, inverter, and installation. A 4kW system (standard 3-bed house) costs £6,500 on average and saves £600/year on electricity bills.
```
Character count: 280-320 chars. Structure: Answer → Evidence → Context

**List snippets:**
- [ ] **5-8 items** - Google truncates at 8
- [ ] **Parallel structure** - Each item starts same way (verb, noun, "How to")
- [ ] **Bolded labels** - **Item name:** Description (10-15 words)

Example:
```
## What are the types of solar panels?

1. **Monocrystalline panels:** Highest efficiency (18-22%), best for limited roof space, premium price
2. **Polycrystalline panels:** Mid-range efficiency (15-17%), good value, blue appearance
3. **Thin-film panels:** Flexible, lowest efficiency (10-12%), cheapest option
```

**Table snippets:**
- [ ] **3-4 columns max** - Mobile rendering limit
- [ ] **5-7 rows max** - Snippet height limit
- [ ] **Specific data** - NO "varies", "depends", "contact for quote". Use exact numbers or ranges
- [ ] **Bold final row** - For "Best for" or "Our recommendation"

### ⭐ Citations & Entity (Every Article)
- [ ] **All statistics sourced** - Every number/stat has citation. Format: "Solar panels save £600/year on average (Energy Saving Trust, 2026)." Link "Energy Saving Trust" to source
- [ ] **Entity salience** - Main entity (service/product) prominent in: First 100 words, first sentence after each H2, meta description
- [ ] **Semantic keywords** - Use related terms naturally. Example: Solar panels article uses: photovoltaic, PV system, inverter, installation, renewable energy. NO keyword stuffing

### 🎯 Engagement (High-Value Articles)
- [ ] **Bucket brigades** - 2-4 (standard) or 5-8 (pillar). Curiosity transitions that hold attention. Examples: "Here's the thing:", "But wait—there's more:", "The bottom line?", "Want to know the secret?"
- [ ] **EngagementHooks** - 0-2 (standard) or 2-4 (pillar) MAX. Use sparingly. These are formatted callout boxes with surprising stats or contrarian statements

---

## Output Required

Provide:
1. **Full article draft** following structure from Phase 2
2. **Human voice** with paragraph variety and intentional imperfections
3. **Proper citations** for all statistics
4. **Featured snippet optimization** for key H2s

---

## Next Step

After completing writing, use **astro-blog-technical** skill for Phase 4.
