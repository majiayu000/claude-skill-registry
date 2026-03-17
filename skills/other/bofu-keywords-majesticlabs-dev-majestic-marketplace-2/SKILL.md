---
name: bofu-keywords
description: Find bottom-of-funnel keywords with high purchase intent for any product. Uses Perplexity for real-time search data.
triggers:
  - bofu keywords
  - bottom of funnel keywords
  - high intent keywords
  - buyer keywords
  - conversion keywords
allowed-tools: Read, Write, Edit, Grep, Glob, mcp__perplexity-ask__perplexity_ask
---

# Bottom-of-Funnel Keyword Finder

Find high-intent keywords that indicate someone is ready to buy, sign up, or convert.

## What Are BOFU Keywords?

Bottom-of-funnel keywords signal purchase intent:
- **Transactional**: "buy", "pricing", "discount", "coupon"
- **Comparative**: "vs", "alternative to", "compared to"
- **Evaluative**: "review", "pros and cons", "is it worth it"
- **Solution-specific**: "best [category] for [use case]"

## Required Input

Ask the user for:
1. **Product/Service name**
2. **Product category** (e.g., "project management software", "email marketing tool")
3. **Known competitors** (optional but helpful)
4. **Target use cases** (what problems does it solve?)

## Research Process

### Step 1: Generate Keyword Patterns

Apply these BOFU patterns to the product:

**Transactional Intent:**
- `[product] pricing`
- `[product] plans`
- `[product] free trial`
- `[product] discount`
- `[product] coupon code`
- `buy [product]`
- `[product] subscription`

**Comparative Intent:**
- `[product] vs [competitor]`
- `[product] alternative`
- `[product] competitors`
- `best [category] tools`
- `[product] compared to [competitor]`
- `switch from [competitor] to [product]`

**Evaluative Intent:**
- `[product] review`
- `[product] reviews [year]`
- `is [product] worth it`
- `[product] pros and cons`
- `[product] honest review`
- `[product] for [use case]`

**Problem-Solution Intent:**
- `best [category] for [use case]`
- `[category] for small business`
- `[category] for startups`
- `[category] for enterprise`
- `how to [solve problem] with [product]`

### Step 2: Use Perplexity for Validation

Use Perplexity MCP to research:
1. Which competitors are commonly compared
2. What questions people ask before buying
3. Common objections and concerns
4. Popular use cases and niches

Example Perplexity query:
```
What are the most common questions people ask before buying [product category] software? What comparisons do they search for?
```

### Step 3: Categorize by Intent Level

| Intent Level | Keyword Type | Example | Priority |
|--------------|--------------|---------|----------|
| **Highest** | Pricing/Buy | "[product] pricing" | P1 |
| **High** | Comparison | "[product] vs [competitor]" | P1 |
| **High** | Reviews | "[product] review 2025" | P1 |
| **Medium** | Alternatives | "best [category] tools" | P2 |
| **Medium** | Use-case | "[category] for [niche]" | P2 |

## Output Format

```markdown
## BOFU Keywords for [Product]

### Highest Intent (Ready to Buy)
| Keyword | Search Intent | Content Type |
|---------|---------------|--------------|
| [product] pricing | Transactional | Pricing page |
| [product] free trial | Transactional | Trial signup |
| [product] discount | Transactional | Promo page |

### High Intent (Comparing Options)
| Keyword | Search Intent | Content Type |
|---------|---------------|--------------|
| [product] vs [competitor] | Comparative | Comparison page |
| [product] alternative | Comparative | Comparison page |
| [product] review | Evaluative | Review/landing page |

### Medium Intent (Evaluating Category)
| Keyword | Search Intent | Content Type |
|---------|---------------|--------------|
| best [category] for [use case] | Solution | Listicle/guide |
| [category] comparison | Comparative | Comparison guide |

### Keyword Clusters for Content Strategy

**Cluster 1: Pricing & Plans**
- [keyword list]
- Recommended content: Transparent pricing page with FAQ

**Cluster 2: Competitor Comparisons**
- [keyword list]
- Recommended content: Individual vs pages for each competitor

**Cluster 3: Reviews & Social Proof**
- [keyword list]
- Recommended content: Customer stories, case studies

### Quick Wins
Keywords with high intent but likely low competition:
1. [keyword] - [reason it's a quick win]
2. [keyword] - [reason]
3. [keyword] - [reason]

### Content Recommendations
For each cluster, suggest specific pages to create.
```

## What This Skill Does NOT Do

- Provide search volume data (use Ahrefs/SEMrush for that)
- Guarantee rankings
- Replace keyword research tools
- Do competitor keyword gap analysis

## When to Use This vs. Other Skills

| Use `bofu-keywords` when... | Use other skills when... |
|-----------------------------|--------------------------|
| Need conversion-focused keywords | Need top-of-funnel content ideas |
| Planning landing pages | Planning blog strategy |
| Building comparison pages | Building educational content |
| Optimizing for signups | Building brand awareness |
