---
name: seoengine
description: "Keyword research, competitive analysis, and full blog post generation. Takes your topic, finds the keywords, analyzes competitors, and writes SEO-optimized content. Use when: creating content for organic search, building topical authority, or optimizing existing content. NOT for: black-hat SEO, keyword stuffing, or link schemes."
homepage: https://pawhub.ai/seoengine
metadata:
  {
    "openpaw":
      {
        "emoji": "💡",
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/seoengine",
              "bins": ["seoengine"],
              "label": "Install SEOEngine (npm)",
            },
          ],
      },
  }
---

# SEOEngine 💡

Topic in, SEO-optimized content out. Keyword research, competitor analysis, outline generation, and full blog posts. All the SEO work, none of the tedium.

## When to Use

✅ **USE this skill when:**

- Creating blog content for organic search
- Building topical authority in your niche
- Optimizing existing content
- Researching keyword opportunities
- Analyzing competitor content strategies
- Planning content calendars
- Improving page rankings
- Finding content gaps

## When NOT to Use

❌ **DON'T use this skill when:**

- Black-hat SEO techniques → against Google TOS
- Keyword stuffing → harms rankings
- Link schemes or manipulation → risky
- Duplicate/spun content → penalized
- Thin content generation → low quality
- Misleading meta descriptions → bad UX

## Example Interactions

**You:** Research keywords for "AI agents for business"

**Paw:** *analyzing search landscape*

**Primary keyword:** "AI agents for business"
- Search volume: 2,900/month
- Difficulty: Medium (45/100)
- CPC: $8.20

**Related keywords (high opportunity):**
1. "ai automation for small business" — 1,600/mo, Low difficulty (28)
2. "business process automation ai" — 1,200/mo, Low (32)
3. "ai agents use cases" — 890/mo, Medium (42)
4. "how to implement ai in business" — 720/mo, Low (29)

**Long-tail opportunities:**
- "best ai agents for customer service" (320/mo, very low difficulty)
- "ai workflow automation tools" (290/mo, very low)
- "ai agent platforms comparison" (210/mo, very low)

**Competitor analysis:** Top 10 pages are mostly:
- Generic listicles (surface-level)
- Vendor landing pages (sales-heavy)
- **Gap:** No deep how-to guides or case studies

**Recommendation:** Write "How to Implement AI Agents in Your Business (2026 Guide)" targeting primary + 3-4 related keywords. Include case studies. 🎯

Want me to create the outline?

---

**You:** Yes

**Paw:** **Outline:** "How to Implement AI Agents in Your Business (2026 Guide)"

**Meta Description (155 chars):**
"Step-by-step guide to implementing AI agents in your business. Real use cases, tools comparison, and ROI analysis. Updated 2026."

**H1:** How to Implement AI Agents in Your Business (2026 Guide)

**Intro (150-200 words)**
- Hook: AI agents aren't just hype anymore
- Target keywords: "AI agents for business," "business process automation AI"
- Promise: by end of guide, you'll know exactly how to start

**H2: What Are AI Agents? (And Why Businesses Are Using Them)**
- Define AI agents clearly
- Differentiate from chatbots
- Why 2026 is the tipping point
- Keywords: "ai automation for small business"

**H2: Top Use Cases for AI Agents in Business**
- Customer service automation
- Sales/lead qualification
- Data entry and processing
- Meeting scheduling and coordination
- Content creation support
- **Include:** "ai agents use cases" keyword

**H2: How to Choose the Right AI Agent Platform**
- Comparison table (5-7 platforms)
- Criteria: pricing, integrations, ease of use
- Keywords: "ai agent platforms comparison"

**H2: Step-by-Step Implementation Guide**
1. Identify highest-impact workflows
2. Pilot with small use case
3. Measure results
4. Scale what works
- Keywords: "how to implement ai in business"

**H2: Real Case Studies**
- 3 businesses, different sizes
- Before/after metrics
- Lessons learned

**H2: Common Pitfalls (And How to Avoid Them)**
- Over-automation too fast
- Choosing wrong use case
- Ignoring change management

**H2: ROI Calculator**
- Simple framework
- Time saved × hourly rate
- Example calculation

**Conclusion**
- Recap
- CTA: Try these platforms (affiliate links)
- Keywords: "best ai agents for customer service"

**Word count target:** 2,500-3,000 words
**Internal links:** 3-5 to other posts
**External links:** Authority sources (MIT Tech Review, HBR, etc.)
**Images:** 5-7 (comparison table, flowchart, screenshots)

Ready to write the full post? (yes/edit outline)

---

**You:** Write it

**Paw:** *starts writing*

**Generating post...**
⏳ Researching sources
⏳ Analyzing top-ranking content
⏳ Writing with SEO optimization
⏳ Adding semantic keywords
⏳ Optimizing readability

*3 minutes later...*

✅ **Blog post complete** (2,847 words)

**SEO Score:** 89/100 (excellent)

**Optimizations applied:**
- ✅ Primary keyword in H1, first 100 words, and conclusion
- ✅ Related keywords naturally distributed
- ✅ Readability: Flesch score 68 (good for general audience)
- ✅ Internal linking opportunities marked
- ✅ Meta description optimized
- ✅ Image alt text suggestions included
- ✅ Schema markup recommendations

**Preview (first 200 words):**

---

# How to Implement AI Agents in Your Business (2026 Guide)

AI agents aren't just hype anymore. They're handling customer service for Fortune 500 companies, qualifying leads for SMBs, and automating workflows that used to require entire teams.

But here's the thing: most businesses still don't know where to start.

If you've been wondering how to implement AI agents in your business without burning budget on failed experiments, you're in the right place. This guide covers everything from choosing the right use cases to measuring ROI—with real examples from businesses that actually did it.

By the end, you'll have a clear roadmap for bringing AI automation into your operations. No fluff, no vendor pitches. Just what works.

## What Are AI Agents? (And Why Businesses Are Using Them)

Let's start with the basics.

An AI agent is software that can execute tasks autonomously on your behalf. Unlike chatbots (which just respond to questions), agents take action...

[continues...]

---

**Next steps:**
- Review/edit? (`seoengine edit post-123`)
- Publish to CMS? (WordPress, Webflow, etc.)
- Check plagiarism? (runs Copyscape check)
- Export? (Markdown, HTML, Google Docs)

What do you want to do? 📝

## Commands

```bash
# Keyword research
seoengine research "topic"

# Competitor analysis
seoengine analyze "keyword"

# Generate outline
seoengine outline "topic" --keywords "kw1,kw2"

# Write full post
seoengine write "topic" --length 2500

# Optimize existing content
seoengine optimize existing-post.md

# Content gap analysis
seoengine gaps --competitor "competitor.com"

# Publish to WordPress
seoengine publish post-123 --platform wordpress
```

## Pricing

- **Free tier:** 3 posts/month, basic SEO
- **Pro:** $29/month — unlimited posts, advanced SEO, publishing integrations

Install: [pawhub.ai/seoengine](https://pawhub.ai/seoengine)

---

Built for content marketers who hate SEO busywork. 💡🐾
