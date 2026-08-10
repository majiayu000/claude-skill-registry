---
name: content-strategy
description: Develop and execute a content strategy that maps content to audience needs, funnel stages, and business goals through editorial planning and performance analysis. Use when the user requests content strategy or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Content Strategy

This skill enables an AI agent to build a comprehensive content strategy from the ground up or audit and improve an existing one. The agent defines content pillars aligned to business objectives, maps content types to funnel stages (TOFU/MOFU/BOFU), creates editorial calendars, and establishes a measurement framework. The output is a repeatable system for producing, distributing, and optimizing content that drives traffic, engagement, and conversions.

## Workflow

1. **Audit existing content and define goals.** Inventory all current content assets — blog posts, landing pages, case studies, videos, whitepapers — with their publication dates, traffic, and conversion metrics. Identify top performers, underperformers, and content gaps. Align the strategy to 2–3 measurable goals such as "increase organic traffic 40% in 6 months" or "generate 200 MQLs per month from content."

2. **Research the target audience and build personas.** Define 2–4 buyer personas with demographics, job roles, pain points, content consumption habits, and preferred channels. Map each persona to their buyer journey stages: awareness (problem recognition), consideration (evaluating solutions), and decision (selecting a vendor). This determines what content types each persona needs at each stage.

3. **Establish content pillars and topic clusters.** Define 3–5 content pillars — broad themes that align with the product's value proposition and audience needs. Under each pillar, plan a cluster of 8–15 supporting pieces that link back to a comprehensive pillar page. This structure builds topical authority for SEO and creates a logical content architecture.

4. **Build the editorial calendar.** Plan content production on a rolling 3-month horizon. For each piece, specify the topic, target keyword, content format (blog, video, infographic, podcast), funnel stage, assigned persona, distribution channels, author, and publish date. Balance content across pillars and funnel stages — roughly 60% TOFU, 30% MOFU, and 10% BOFU.

5. **Define distribution and repurposing workflows.** For each content piece, plan the distribution path: organic social posts, email newsletter inclusion, syndication partners, and paid promotion budget. Design repurposing chains — for example, a long-form blog post becomes a LinkedIn carousel, a Twitter/X thread, an email snippet, and a short video. This multiplies reach without multiplying production effort.

6. **Set up measurement and iteration cadence.** Define KPIs for each funnel stage: TOFU (traffic, impressions, social shares), MOFU (email signups, content downloads, time on page), BOFU (demo requests, free trial starts, SQLs). Review content performance biweekly, retire or update underperforming content quarterly, and refresh the editorial calendar monthly.

## Usage

Provide the agent with your business type, target audience, existing content (if any), and goals. The agent will return a complete content strategy with pillars, editorial calendar, and distribution plan.

**Prompt:** `Create a content strategy for a B2B cybersecurity startup targeting IT directors at mid-market companies. Goal: generate 150 leads/month from content within 6 months.`

## Examples

### Example 1: Three-Month Editorial Calendar

**Request:** Create a Q2 content calendar for a SaaS HR platform targeting startup founders.

| Week | Topic | Format | Funnel | Pillar | Channel | Keyword |
|------|-------|--------|--------|--------|---------|---------|
| W1 Apr | How to Write Your First Employee Handbook | Blog (2,000 words) | TOFU | HR Compliance | Organic + LinkedIn | employee handbook template |
| W2 Apr | Employee Handbook Checklist (PDF) | Downloadable guide | MOFU | HR Compliance | Email + Gated landing page | — |
| W3 Apr | 5 Onboarding Mistakes That Increase Turnover | Blog (1,500 words) | TOFU | Employee Onboarding | Organic + Twitter/X | onboarding mistakes |
| W4 Apr | Video: Setting Up PTO Policies in HRBot | Tutorial video (8 min) | BOFU | Product Demos | YouTube + Email | — |
| W1 May | Remote Hiring: Compliance in 5 States | Blog (2,500 words) | TOFU | Remote Work | Organic + LinkedIn | remote hiring compliance |
| W2 May | Startup Compensation Benchmarks 2025 | Data report + infographic | MOFU | Compensation | Gated + Social | startup salary benchmarks |
| W3 May | How We Helped Acme Scale from 10 to 100 Employees | Case study | BOFU | Product Demos | Email + Sales enablement | — |
| W4 May | Ask an HR Expert: Live Q&A Webinar | Webinar | MOFU | HR Compliance | Email + LinkedIn Events | — |
| W1 Jun | Performance Review Templates That Actually Work | Blog + templates | TOFU | Performance Mgmt | Organic + Pinterest | performance review template |
| W2 Jun | MOFU Email Nurture Sequence (5-part) | Email series | MOFU | Cross-pillar | Email automation | — |
| W3 Jun | Comparison: HRBot vs BambooHR vs Gusto | Comparison page | BOFU | Product Demos | Organic + Paid search | hrbot vs bamboohr |
| W4 Jun | Q2 Content Performance Review | Internal report | — | — | Internal | — |

### Example 2: Content Audit with Recommendations

**Request:** Audit the existing blog for `startuphub.io` (42 posts published over 18 months).

**Audit Findings:**

| Category | Count | Avg Monthly Traffic | Action |
|----------|-------|-------------------|--------|
| High performers (>1,000 visits/mo) | 6 | 2,400 | Update with fresh data, add CTAs, interlink with MOFU content |
| Moderate performers (200–1,000 visits/mo) | 14 | 480 | Optimize titles/meta descriptions, add internal links, refresh examples |
| Low performers (<200 visits/mo) | 18 | 65 | Consolidate 8 thin posts into 4 comprehensive guides; redirect old URLs |
| Outdated content (>12 months, no updates) | 12 | 110 | Update statistics and screenshots, re-publish with current date |
| No-traffic content (<10 visits/mo) | 4 | 6 | Evaluate for removal or complete rewrite; 301 redirect to related content |

**Top Recommendations:**
1. **Consolidate thin content.** Merge the 8 low-traffic posts on overlapping topics into 4 pillar-style guides. This reduces index bloat and concentrates link equity.
2. **Add MOFU conversion paths.** Only 3 of 42 posts include a content upgrade or lead magnet CTA. Add relevant downloadable assets to the top 20 posts.
3. **Fix internal linking.** 15 posts have zero internal links. Create a hub-and-spoke linking structure around the 3 strongest content pillars.
4. **Establish a refresh cadence.** Commit to updating 4 posts per month with current year data, new screenshots, and expanded sections.

## Best Practices

- **Balance content across funnel stages.** A common mistake is publishing only TOFU blog posts. Without MOFU comparison guides and BOFU case studies, traffic does not convert. Target a 60/30/10 split.
- **Repurpose every long-form piece into at least 3 derivative formats.** A single blog post can become a LinkedIn carousel, a Twitter/X thread, an email newsletter section, and a short-form video. This triples distribution without tripling production cost.
- **Set a sustainable publishing cadence.** Two high-quality posts per week consistently outperforms five mediocre posts per week. Quality signals (time on page, backlinks, shares) compound over time.
- **Tie every content piece to a measurable outcome.** Each piece should have a primary CTA: subscribe, download, book a demo, start a free trial. Content without a next step is a dead end.
- **Use content briefs for every piece.** A brief should include the target keyword, search intent, competitor URLs to beat, outline with H2/H3 headings, target word count, and internal links to include. Briefs improve consistency and reduce revision cycles.
- **Document your strategy in a living playbook.** Include brand voice guidelines, persona definitions, pillar topics, and distribution checklists. This enables new team members to execute without losing quality.

## Edge Cases

- **Brand-new sites with no existing content.** Skip the audit phase and prioritize creating 3 pillar pages and 10–15 supporting posts before diversifying into other formats. Focus on low-difficulty keywords to build initial domain authority.
- **Highly regulated industries (finance, healthcare).** All content requires compliance review before publication. Build a 2-week legal review buffer into the editorial calendar and maintain an approval workflow.
- **Seasonal businesses.** Plan content production 8–12 weeks ahead of peak season. Publish evergreen foundational content year-round and layer seasonal pieces on top during peak windows.
- **Limited budget or solo creator.** Reduce to 2 content pillars and 1 post per week. Focus on SEO-driven evergreen content that compounds over time rather than social-first content that decays quickly.
- **Pivoting product or audience.** When the product repositions, audit existing content for alignment with the new positioning. Archive or redirect misaligned content rather than deleting it, to preserve any existing backlinks and authority.
