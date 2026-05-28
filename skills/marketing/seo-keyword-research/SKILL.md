---
name: researching-seo-keywords
description: Expands keyword lists and analyzes search intent for content strategy. Use when the user asks about keyword research, search intent, long-tail keywords, keyword gaps, or SEO content planning.
---

# SEO Keyword Research Assistant

## When to use this skill

- User asks for keyword research
- User needs keyword variations
- User wants to analyze search intent
- User mentions finding content gaps
- User needs low-competition keywords

## Workflow

- [ ] Identify seed keywords
- [ ] Generate variations and long-tails
- [ ] Classify search intent
- [ ] Identify opportunities
- [ ] Group by topic clusters
- [ ] Prioritize for content

## Instructions

### Step 1: Gather Seed Keywords

**Required inputs:**

| Field              | Purpose                   |
| ------------------ | ------------------------- |
| Main topic/product | Core focus area           |
| Target audience    | Who you're reaching       |
| Business goal      | Traffic, leads, sales     |
| Competitors        | For gap analysis          |
| Current rankings   | What you already rank for |

**Seed keyword sources:**

| Source                | How to Use            |
| --------------------- | --------------------- |
| Product/service names | Direct terms          |
| Customer questions    | Support tickets, FAQs |
| Competitor content    | What they rank for    |
| Industry terms        | Jargon, acronyms      |
| Problem statements    | Pain points           |

### Step 2: Generate Keyword Variations

**Variation types:**

| Type       | Formula                   | Example (seed: "email marketing")     |
| ---------- | ------------------------- | ------------------------------------- |
| Long-tail  | [seed] + [modifier]       | "email marketing for small business"  |
| Question   | [question word] + [seed]  | "how to start email marketing"        |
| Comparison | [seed] vs [alternative]   | "email marketing vs social media"     |
| Best/top   | best [seed] + [qualifier] | "best email marketing software 2026"  |
| How-to     | how to [action] + [seed]  | "how to improve email marketing"      |
| Guide      | [seed] + guide/tutorial   | "email marketing guide for beginners" |
| Tool       | [seed] + tool/software    | "email marketing automation tools"    |
| Cost       | [seed] + cost/pricing     | "email marketing software pricing"    |

**Modifier categories:**

| Category | Modifiers                                         |
| -------- | ------------------------------------------------- |
| Intent   | buy, compare, review, learn, find                 |
| Time     | 2026, today, now, quick, fast                     |
| Quality  | best, top, free, cheap, premium                   |
| Audience | for beginners, for developers, for small business |
| Location | near me, in [city], [country]                     |
| Format   | template, checklist, guide, examples              |

### Step 3: Search Intent Classification

**Intent types:**

| Intent        | Signal Words                   | Content Type           | Funnel Stage           |
| ------------- | ------------------------------ | ---------------------- | ---------------------- |
| Informational | how, what, why, guide, learn   | Blog, guide, tutorial  | Top (awareness)        |
| Navigational  | [brand name], login, website   | Landing page, homepage | Middle                 |
| Commercial    | best, review, compare, vs, top | Comparison, review     | Middle (consideration) |
| Transactional | buy, price, discount, order    | Product page, pricing  | Bottom (decision)      |

**Intent identification patterns:**

```markdown
## Informational Intent

- "how to [action]"
- "what is [topic]"
- "why does [thing happen]"
- "[topic] explained"
- "[topic] tutorial"

## Commercial Investigation

- "best [product category]"
- "[product A] vs [product B]"
- "[product] review"
- "[product] alternatives"
- "top 10 [products]"

## Transactional Intent

- "buy [product]"
- "[product] price"
- "[product] discount code"
- "[product] free trial"
- "order [product] online"

## Navigational Intent

- "[brand] login"
- "[brand] website"
- "[brand] support"
```

### Step 4: Keyword Opportunity Analysis

**Opportunity scoring:**

| Factor             | Low Competition Signal                     |
| ------------------ | ------------------------------------------ |
| Search volume      | 100-1,000/month (sweet spot for new sites) |
| Keyword difficulty | Under 30 (tool-dependent)                  |
| SERP features      | Few featured snippets, no ads              |
| Top results        | Forums, outdated content, thin pages       |
| Domain authority   | Low DA sites ranking                       |

**Opportunity matrix:**

| Volume | Difficulty | Priority              |
| ------ | ---------- | --------------------- |
| High   | Low        | 🔥 Top priority       |
| Medium | Low        | ✅ Quick wins         |
| High   | Medium     | 📈 Long-term targets  |
| Low    | Low        | ⚡ Easy content       |
| High   | High       | 🎯 Authority builders |
| Low    | High       | ❌ Skip               |

### Step 5: Question-Based Keywords

**Question patterns to generate:**

| Question Word | Focus                    |
| ------------- | ------------------------ |
| How           | Process, tutorial        |
| What          | Definition, explanation  |
| Why           | Reasoning, benefits      |
| When          | Timing, triggers         |
| Where         | Location, source         |
| Which         | Comparison, selection    |
| Can/Could     | Possibility, capability  |
| Should        | Recommendation, advice   |
| Is/Are        | Verification, validation |

**Question generation template:**

```markdown
## Questions for: [Seed Keyword]

### How questions

- How to [action with keyword]?
- How does [keyword] work?
- How much does [keyword] cost?
- How long does [keyword] take?

### What questions

- What is [keyword]?
- What are the benefits of [keyword]?
- What is the best [keyword]?
- What [keyword] should I use?

### Why questions

- Why is [keyword] important?
- Why use [keyword]?
- Why does [keyword] fail?

### Comparison questions

- [Keyword A] vs [Keyword B]?
- Is [keyword] better than [alternative]?
- What's the difference between [A] and [B]?
```

### Step 6: Topic Cluster Organization

**Cluster structure:**

```markdown
## Topic Cluster: [Pillar Topic]

### Pillar Page (main keyword)

- Target: [High-volume keyword]
- Intent: [Informational/Commercial]
- Content: Comprehensive guide (3,000+ words)

### Cluster Content (supporting pages)

| Topic        | Keyword   | Intent   | Internal Link |
| ------------ | --------- | -------- | ------------- |
| [Subtopic 1] | [keyword] | [intent] | → Pillar      |
| [Subtopic 2] | [keyword] | [intent] | → Pillar      |
| [Subtopic 3] | [keyword] | [intent] | → Pillar      |
| [Subtopic 4] | [keyword] | [intent] | → Pillar      |
```

**Cluster example:**

```markdown
## Topic Cluster: Email Marketing

### Pillar Page

- Target: "email marketing guide"
- Intent: Informational
- Content: Ultimate Guide to Email Marketing

### Cluster Content

| Topic           | Keyword                         | Intent        |
| --------------- | ------------------------------- | ------------- |
| Getting started | "how to start email marketing"  | Informational |
| Tools           | "best email marketing software" | Commercial    |
| Templates       | "email marketing templates"     | Informational |
| Automation      | "email marketing automation"    | Commercial    |
| Metrics         | "email marketing KPIs"          | Informational |
| B2B focus       | "b2b email marketing"           | Commercial    |
| List building   | "how to build email list"       | Informational |
```

### Step 7: Competitor Gap Analysis

**Gap analysis template:**

```markdown
## Competitor Keyword Gap Analysis

### Competitors Analyzed

1. [Competitor 1 URL]
2. [Competitor 2 URL]
3. [Competitor 3 URL]

### Keywords They Rank For (You Don't)

| Keyword   | Volume | Difficulty | Competitor  | Priority   |
| --------- | ------ | ---------- | ----------- | ---------- |
| [keyword] | [vol]  | [KD]       | [who ranks] | [priority] |

### Content Gaps Identified

| Topic   | Competitor Coverage | Your Coverage | Action        |
| ------- | ------------------- | ------------- | ------------- |
| [topic] | 3 articles          | 0 articles    | Create pillar |
| [topic] | 1 article           | Outdated      | Update        |
| [topic] | None                | None          | First mover   |
```

### Step 8: Keyword Prioritization

**Prioritization framework:**

| Criteria             | Weight | Score (1-5) |
| -------------------- | ------ | ----------- |
| Search volume        | 20%    |             |
| Keyword difficulty   | 25%    |             |
| Business relevance   | 25%    |             |
| Conversion potential | 20%    |             |
| Content gap          | 10%    |             |

**Priority tiers:**

```markdown
## Keyword Priorities

### Tier 1: Immediate (This Month)

- Low difficulty + high relevance
- Quick wins for traffic
  | Keyword | Volume | KD | Intent |
  |---------|--------|----|----|

### Tier 2: Short-term (1-3 Months)

- Medium difficulty + commercial intent
- Revenue-driving content
  | Keyword | Volume | KD | Intent |
  |---------|--------|----|----|

### Tier 3: Long-term (3-6 Months)

- High difficulty + high volume
- Authority-building pillar content
  | Keyword | Volume | KD | Intent |
  |---------|--------|----|----|
```

## Output Format

```markdown
## Keyword Research: [Topic/Niche]

**Seed keywords:** [List of seeds]
**Target audience:** [Who you're reaching]
**Business goal:** [Traffic/Leads/Sales]

---

### Keyword List

| Keyword | Volume | KD  | Intent | Priority |
| ------- | ------ | --- | ------ | -------- |
|         |        |     |        |          |

### By Search Intent

**Informational:**

- [keywords]

**Commercial:**

- [keywords]

**Transactional:**

- [keywords]

---

### Topic Clusters

[Cluster organization]

---

### Question Keywords

[Question-based keywords for FAQ/content]

---

### Quick Wins (Low KD, Decent Volume)

| Keyword | Volume | KD  | Content Type |
| ------- | ------ | --- | ------------ |
|         |        |     |              |

---

### Content Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
```

## Validation

Before completing:

- [ ] Keywords classified by intent
- [ ] Volume and difficulty included
- [ ] Question keywords generated
- [ ] Topic clusters organized
- [ ] Priority tiers assigned
- [ ] Quick wins identified
- [ ] Content recommendations provided
- [ ] Competitor gaps noted

## Error Handling

- **No seed keywords**: Ask for main product/service or topic area.
- **Too broad**: Narrow with audience, location, or specific use case.
- **No volume data**: Note as "volume unknown" and prioritize by relevance.
- **All high difficulty**: Focus on long-tail variations or question keywords.
- **No competitors identified**: Search top 3 ranking for seed keywords.

## Resources

- [Ahrefs](https://ahrefs.com/) - Keyword research and competitor analysis
- [SEMrush](https://www.semrush.com/) - Keyword gap and difficulty
- [Ubersuggest](https://neilpatel.com/ubersuggest/) - Free keyword ideas
- [AnswerThePublic](https://answerthepublic.com/) - Question keywords
- [AlsoAsked](https://alsoasked.com/) - People Also Ask data
- [Google Search Console](https://search.google.com/search-console) - Current rankings
