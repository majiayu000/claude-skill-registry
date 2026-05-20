---
name: business-idea-finder
description: Find, validate, and document business ideas through problem signal mining, competitor analysis, SWOT analysis, and Business Model Canvas generation. Use when searching for business opportunities or creating complete business briefs.
category: business
license: MIT
---

# When to Use This Skill

Use this skill when you need to:

- **Find profitable business ideas** validated by real market demand
- **Identify unsolved problems** from online community discussions
- **Mine social platforms** for problem signals and opportunity patterns
- **Validate business concepts** before investing time and money
- **Discover micro-SaaS opportunities** in specific niches
- **Research B2B pain points** from technical communities
- **Find "boring" business opportunities** with high potential
- **Generate SWOT analysis** for business opportunities
- **Create Business Model Canvas** for validated ideas
- **Document complete business briefs** ready for development

# Core Concepts

## Problem Signals: The Hidden Goldmine

Most startups fail because they build something nobody wants. The solution?
**Listen first, build second.**

Every day, people publicly express frustration, wishes, and needs across social
platforms. These are **problem signals** - direct indicators of unsolved
problems worth solving.

**High-signal phrases**:

- "I wish there was..." - Unmet desire
- "Someone should build..." - Clear opportunity
- "Why doesn't anyone..." - Market gap
- "Frustrated with..." - Pain point
- "I hate..." - Emotional pain (high opportunity)
- "Does anyone know of a tool that..." - Active seeking

**The 5-Phase Discovery Process**:

1. **Niche Selection** - Choose your target market/industry
2. **Signal Mining** - Search platforms with targeted queries
3. **Problem Ranking** - Prioritize by engagement and specificity
4. **Validation** - Competitor analysis, market sizing, willingness to pay
5. **Documentation** - Capture findings for development

# Step-by-Step Idea Discovery Process

## Phase 1: Niche Selection (Day 1)

**Choose your target area**:

Narrow focus = better signals. Avoid "business ideas in general" - too broad.

**High-opportunity niches**:

- Developer tools (APIs, devops, testing, documentation)
- B2B SaaS (project management, CRM, workflow automation)
- E-commerce operations (inventory, analytics, customer service)
- Content creation (editing, publishing, analytics)
- Healthcare tech (scheduling, telehealth, compliance)
- Education (LMS, tutoring platforms, course creation)
- Real estate (property management, lead generation)

**Define your parameters**:

- Industry/vertical
- Problem type (technical, workflow, financial, operational)
- Target customer (solopreneurs, SMBs, enterprise, consumers)
- Business model preference (micro-SaaS, marketplace, API, service)

**Deliverable**: Clear niche statement (e.g., "Project management tools for
marketing agencies")

## Phase 2: Signal Mining (Days 2-3)

**Search each platform with problem-signal queries**.

Use the query patterns in
[references/platform-strategies.md](references/platform-strategies.md) and
[references/problem-signals.md](references/problem-signals.md).

**Platform prioritization**:

1. **Reddit** (highest signal density)
   - r/SaaS, r/startups, r/SomebodyMakeThis, r/Entrepreneur
   - Query: `site:reddit.com "I wish there was" project management tools`

2. **HackerNews** (technical/B2B focus)
   - "Ask HN" posts with technical problems
   - Query:
     `site:news.ycombinator.com "Ask HN" looking for project management tool`

3. **IndieHackers** (revenue validation data)
   - Unsolved problems discussions
   - Query: `site:indiehackers.com "would pay for" project management`

4. **Twitter/X** (real-time frustration)
   - Tool complaints and workflow pain
   - Query: `"I hate" project management software`,
     `"why is it so hard to" project tracking`

5. **Product Hunt** (gap analysis)
   - Browse launches for missing features
   - Query: Check low-engagement launches in your niche

6. **Threads** (casual needs)
   - Informal requests and complaints
   - Query: `"someone should build" project management`,
     `"I need" better tracking tool`

**Deliverable**: 30-50 raw problem signals with source links

## Phase 3: Problem Ranking (Day 4)

**Score each problem signal**:

| Criteria                  | Weight | Scoring                                        |
| ------------------------- | ------ | ---------------------------------------------- |
| **Engagement**            | 3x     | Upvotes, comments, shares                      |
| **Recency**               | 2x     | Last 7 days (10), 30 days (7), 90+ days (3)    |
| **Specificity**           | 2x     | Detailed problem (10), vague (3)               |
| **Frequency**             | 2x     | Repeated across platforms (10), one-off (3)    |
| **Willingness to Pay**    | 3x     | "Would pay for" mentioned (10), no mention (3) |
| **Technical Feasibility** | 1x     | Solo-buildable (10), requires team (3)         |

**Calculate score**: Sum weighted values. Prioritize scores 60+.

**Red flags** (skip these):

- ❌ Solved by existing tools (unless differentiation is clear)
- ❌ Too small market (<1,000 potential customers)
- ❌ High regulatory hurdles (healthcare data, fintech compliance)
- ❌ Requires network effects to work (marketplaces, social platforms)

**Deliverable**: Ranked list of top 10-15 validated problems with scores

## Phase 4: Validation (Days 5-7)

**For each top problem, conduct deep validation**:

### Competitor Analysis

Search: `[problem description] tool`, `[niche] software`, `[task] app`

**Assess**:

- Number of competitors (0-2 = green field, 3-5 = competitive, 10+ = saturated)
- Differentiation opportunities (UX, price, features, integration)
- Competitor weaknesses (complaints, missing features, poor reviews)

### Market Sizing

**Indicators**:

- Google Trends: Search volume trends for related terms
- Subreddit/community size (e.g., r/SaaS has 200K+ members)
- Search volume: Use tools like Ahrefs/SEMrush (or estimate via Google Ads
  planner)
- "Would pay for" mentions: Pricing discussions reveal budget

### Willingness to Pay Signals

Look for:

- "How much would you pay for X?"
- "I'd pay $X/month for..."
- "Currently paying for [tool] but hate it"
- "Any tool that does [X], budget is $Y"

**Validation checklist**:

- [ ] 50+ people expressed this problem (across platforms)
- [ ] Mentioned in last 30 days (recency)
- [ ] Clear willingness to pay (or B2B budget implied)
- [ ] Technically feasible for solo developer
- [ ] Market size >1,000 potential customers
- [ ] Clear differentiation from existing solutions

**Deliverable**: 3-5 validated business opportunities with full analysis

## Phases 5-7: Analysis and Documentation

For SWOT analysis templates, Business Model Canvas framework, and final
documentation checklist, see
[references/analysis-templates.md](references/analysis-templates.md).

# Common Mistakes

**Mistake 1: Starting Without a Niche**

- **Problem**: "Find me any business idea" returns generic, low-opportunity
  results
- **Solution**: Start with specific industry, customer type, problem domain

**Mistake 2: Ignoring Engagement Signals**

- **Problem**: Treating all complaints equally (some are just venting)
- **Solution**: Prioritize high-upvote, recent, detailed posts with active
  discussion

**Mistake 3: Skipping Competitor Research**

- **Problem**: "No one has built this!" (usually means it's a bad idea or
  already exists)
- **Solution**: Thorough competitor search before falling in love with an idea

**Mistake 4: Overlooking "Boring" Opportunities**

- **Problem**: Only chasing sexy ideas (AI, crypto, social networks)
- **Solution**: B2B tools, workflow automation, "boring" SaaS have higher
  success rates

**Mistake 5: Building for Consumers First**

- **Problem**: Consumer apps need massive distribution, low willingness to pay
- **Solution**: Start with B2B - higher willingness to pay, clearer ROI

**Mistake 6: Ignoring Technical Feasibility**

- **Problem**: Finding great problems that require 10-person team to solve
- **Solution**: Filter for solo-founder feasibility (MVP in 1-3 months)

# Success Metrics

**Idea Quality Indicators**:

| Metric                 | Weak Signal     | Strong Signal        | Excellent Signal     |
| ---------------------- | --------------- | -------------------- | -------------------- |
| **Engagement**         | <10 upvotes     | 10-50 upvotes        | 50+ upvotes          |
| **Recency**            | 90+ days old    | 30-90 days           | <7 days              |
| **Specificity**        | Vague complaint | Clear problem stated | Detailed use case    |
| **Frequency**          | One-off mention | Few times per month  | Multiple platforms   |
| **Willingness to Pay** | Not mentioned   | Implied B2B budget   | Explicit "would pay" |
| **Competitor Density** | 10+ competitors | 3-5 competitors      | 0-2 competitors      |
| **Market Size**        | <1K customers   | 1K-10K customers     | 10K+ customers       |

**Validation checklist**:

- ✅ Found 50+ problem signals across platforms
- ✅ At least 3 signals with 50+ engagement
- ✅ Clear willingness to pay expressed
- ✅ Technically feasible for solo founder
- ✅ Differentiation from existing solutions clear
- ✅ Market size sufficient (>1K potential customers)

# Deep Dives

For comprehensive search strategies, validation frameworks, and opportunity
patterns, see the references:

**[references/problem-signals.md](references/problem-signals.md)**

- Complete list of high-signal phrases ("I wish", "why doesn't", "frustrated
  with")
- Platform-specific query patterns
- How to distinguish venting from genuine opportunity
- Engagement signal analysis

**[references/platform-strategies.md](references/platform-strategies.md)**

- Reddit: Subreddits, advanced search operators, engagement filters
- HackerNews: "Ask HN" analysis, technical pain points
- Twitter/X: Complaint mining, tool frustration searches
- Threads: Informal need detection
- Product Hunt: Gap analysis in launches
- IndieHackers: Unsolved problems and revenue validation

**[references/validation-framework.md](references/validation-framework.md)**

- Competitor analysis methodology
- Market sizing approaches (free and paid tools)
- Willingness-to-pay signal detection
- Technical feasibility assessment
- Differentiation strategy framework

**[references/opportunity-patterns.md](references/opportunity-patterns.md)**

- High-potential business patterns (API products, micro-SaaS, developer tools)
- "Boring" business opportunities with high success rates
- B2B vs B2C trade-offs
- Workflow automation sweet spots
- Integration and data migration opportunities

---

## Next Steps

After finding and validating business ideas:

1. **Use `indie-saas-validation-master` skill** - Pre-launch planning, MVP
   scoping, customer development interviews
2. **Use `pricing-strategy-designer` skill** - Monetization model design,
   pricing tier structure
3. **Use `technical-automation-architect` skill** - Define pragmatic MVP
   architecture, build-vs-buy boundaries, and delivery approach
4. **Use `customer-retention-optimizer` skill** - Plan retention strategies
   before launch

---

## Sources

- [Indie Hackers - Unsolved Problems Discussions](https://www.indiehackers.com/)
- [Reddit r/SomebodyMakeThis](https://www.reddit.com/r/somebodymakethis/)
- [Hacker News "Ask HN" Posts](https://news.ycombinator.com/)
- [Product Hunt - Browse Launches](https://www.producthunt.com/)
