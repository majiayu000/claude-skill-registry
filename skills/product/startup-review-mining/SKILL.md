---
name: startup-review-mining
description: "Systematic extraction of pain points, feature gaps, switching triggers, and opportunities from review sources (B2B review sites, app stores, forums, communities, issue trackers). Includes bias hygiene, taxonomy building, and turning insights into experiments."
---

# Review Mining Skill — Quick Reference

This skill extracts recurring customer pain and constraints from reviews and testimonials, then converts them into product bets and experiments. Treat reviews as a biased sample; triangulate before betting.

**Key Distinction from `software-ux-research`**:
- `software-ux-research` = UI/UX pain points only
- `startup-review-mining` (this skill) = ALL pain dimensions (pricing, support, integration, performance, onboarding, value gaps)

**Modern Best Practices (Dec 2025)**:
- Start with source hygiene: sampling plan, platform skews, and fake-review defenses.
- Build a taxonomy (theme × segment × severity) before counting keywords.
- Convert insights into bets with explicit success metrics and decision rules.
- Handle customer/market data with purpose limitation, retention, and access controls.

---

## When to Use This Skill

Invoke when users ask for:

- Pain point extraction from reviews (any source)
- Competitive weakness analysis
- Feature gap identification
- Switching trigger analysis (why customers leave competitors)
- Market opportunity discovery through customer complaints
- Review sentiment analysis across platforms
- B2B software evaluation (G2, Capterra, TrustRadius)
- B2C app analysis (App Store, Play Store)
- Community sentiment (Reddit, HN, Twitter/X)
- Support pain patterns (forums, tickets, Stack Overflow)

---

## Quick Reference Table

| Mining Task | Source Category | Template | Output |
|-------------|-----------------|----------|--------|
| **Full Review Mining** | All sources | [review-mining-report.md](templates/review-mining-report.md) | Comprehensive pain analysis |
| **B2B Software** | G2, Capterra, TrustRadius | [b2b-review-extraction.md](templates/b2b-review-extraction.md) | Enterprise pain points |
| **B2C Apps** | App Store, Play Store | [b2c-review-extraction.md](templates/b2c-review-extraction.md) | Consumer pain points |
| **Tech Communities** | Reddit, HN, ProductHunt | [community-sentiment.md](templates/community-sentiment.md) | Technical sentiment |
| **Competitor Weakness** | Cross-platform | [competitor-weakness-matrix.md](templates/competitor-weakness-matrix.md) | Competitive gaps |
| **Switching Triggers** | All sources | [switching-trigger-analysis.md](templates/switching-trigger-analysis.md) | Why customers leave |
| **Feature Requests** | All sources | [feature-request-aggregator.md](templates/feature-request-aggregator.md) | Unmet needs |
| **Opportunity Mapping** | All sources | [opportunity-from-reviews.md](templates/opportunity-from-reviews.md) | Actionable opportunities |

---

## Review Source Hygiene (Dec 2025)

### Sampling and Bias Checklist

- Define the time window (e.g., last 6–12 months) and why.
- Sample across ratings (not only 1-star or 5-star).
- Separate segments (SMB vs enterprise; dev vs non-dev; geo; regulated vs not).
- Flag incentives and moderation (some platforms skew toward promoters).

### Fake Review and Manipulation Defenses

- Look for repeated phrasing, unnatural timing bursts, and identical complaints/praise across accounts.
- Prefer “verified” signals when available; still spot-check.
- Treat suspicious clusters as weak evidence until corroborated elsewhere.

Compliance note: if you use reviews for marketing claims or comparisons, be aware of the FTC’s consumer reviews/testimonials rule (16 CFR Part 465). Source: https://www.ftc.gov/legal-library/browse/federal-register-notices/16-cfr-part-465-trade-regulation-rule-use-consumer-reviews-testimonials-final-rule

## The 7 Pain Dimensions

Reviews reveal pain across **7 dimensions** - not just UI/UX:

| Dimension | What to Look For | Example Signals |
|-----------|------------------|-----------------|
| **1. UI/UX Pain** | Usability, navigation, design | "confusing interface", "hard to find", "ugly design" |
| **2. Pricing Pain** | Cost, billing, contracts | "too expensive", "hidden fees", "locked in contract" |
| **3. Support Pain** | Response time, resolution quality | "slow support", "unhelpful", "no documentation" |
| **4. Integration Pain** | API complexity, data migration | "can't connect to X", "migration nightmare", "no API" |
| **5. Performance Pain** | Speed, reliability, uptime | "slow", "crashes", "downtime", "buggy" |
| **6. Onboarding Pain** | Setup complexity, time-to-value | "took weeks to set up", "steep learning curve" |
| **7. Value Pain** | Feature gaps, unmet jobs | "missing X feature", "can't do Y", "not what I needed" |

---

## Decision Tree: Choosing Mining Approach

```text
Review Mining Need: [What do you want to learn?]
    |
    +-- Finding pain points in a market?
    |   +-- B2B software? → G2 + Capterra + TrustRadius (resources/source-by-source-extraction.md#b2b)
    |   +-- Consumer app? → App Store + Play Store (resources/source-by-source-extraction.md#b2c)
    |   +-- Developer tool? → GitHub Issues + Stack Overflow + HN (resources/source-by-source-extraction.md#tech)
    |
    +-- Analyzing specific competitors?
    |   +-- Direct comparison? → Competitor Weakness Matrix (templates/competitor-weakness-matrix.md)
    |   +-- Why customers switch? → Switching Trigger Analysis (templates/switching-trigger-analysis.md)
    |   +-- Feature gaps? → Feature Request Aggregator (templates/feature-request-aggregator.md)
    |
    +-- Finding opportunities?
    |   +-- Quick wins (<2 weeks)? → Opportunity Template (templates/opportunity-from-reviews.md#quick-wins)
    |   +-- Medium bets (2-8 weeks)? → Opportunity Template (templates/opportunity-from-reviews.md#medium)
    |   +-- Big differentiation? → Opportunity Template (templates/opportunity-from-reviews.md#big-bets)
    |
    +-- Understanding sentiment?
    |   +-- Real-time complaints? → Twitter/X monitoring (resources/source-by-source-extraction.md#social)
    |   +-- Community opinion? → Reddit + HN (resources/source-by-source-extraction.md#community)
    |   +-- Launch feedback? → ProductHunt (resources/source-by-source-extraction.md#producthunt)
    |
    +-- Comprehensive analysis?
        +-- Full market research? → Review Mining Report (templates/review-mining-report.md)
```

---

## Review Sources (Complete Guide)

### Tier 1: Very High Signal (Start Here)

| Source | Type | Best For | How to Access |
|--------|------|----------|---------------|
| **G2** | B2B Reviews | Enterprise software pain | g2.com/products/[name]/reviews |
| **TrustRadius** | B2B Reviews | In-depth technical reviews | trustradius.com/products/[name]/reviews |
| **App Store** | B2C Reviews | iOS app pain | apps.apple.com + AppFollow/Appbot |
| **Play Store** | B2C Reviews | Android app pain | play.google.com + AppFollow/Appbot |
| **GitHub Issues** | Developer | Bug patterns, feature requests | github.com/[org]/[repo]/issues |
| **Hacker News** | Tech Community | Technical critiques, scalability | news.ycombinator.com + Algolia search |
| **Reddit** | Community | Raw unfiltered opinions | reddit.com/r/[subreddit] |

### Tier 2: High Signal

| Source | Type | Best For | How to Access |
|--------|------|----------|---------------|
| **Capterra** | B2B Reviews | SMB software comparisons | capterra.com/p/[id]/[name]/reviews |
| **ProductHunt** | Launch Feedback | First impressions, early adopters | producthunt.com/products/[name] |
| **Stack Overflow** | Developer | Integration difficulties | stackoverflow.com/questions/tagged/[tag] |
| **Gartner Peer Insights** | Enterprise | Enterprise pain, vendor comparisons | gartner.com/reviews/market/[market] |
| **Twitter/X** | Social | Real-time complaints | twitter.com/search?q=[product] |

### Tier 3: Medium Signal

| Source | Type | Best For | How to Access |
|--------|------|----------|---------------|
| **Software Advice** | B2B | SMB-focused reviews | softwareadvice.com/[category] |
| **LinkedIn** | Professional | B2B complaints, professional sentiment | linkedin.com/feed |
| **Quora** | Q&A | Questions = unmet needs | quora.com/topic/[topic] |
| **YouTube Comments** | Tutorial | Confusion points, documentation gaps | youtube.com/watch?v=[id] |
| **Public Support Forums** | Support | Recurring issues, workarounds | [product].community.com |

---

## Navigation: Resources

### Extraction Methodology
- [resources/source-by-source-extraction.md](resources/source-by-source-extraction.md) - Platform-specific extraction guides for each source with search queries, filters, and export methods

### Analysis Frameworks
- [resources/pain-categorization-framework.md](resources/pain-categorization-framework.md) - 7-dimension pain taxonomy with severity scoring and prioritization
- [resources/sentiment-analysis-patterns.md](resources/sentiment-analysis-patterns.md) - Identifying pain vs praise, detecting intensity, and spotting trends

### Competitive Intelligence
- [resources/competitor-review-comparison.md](resources/competitor-review-comparison.md) - Cross-competitor analysis methodology with switching trigger identification

### Opportunity Mapping
- [resources/review-to-opportunity-mapping.md](resources/review-to-opportunity-mapping.md) - Converting pain points to actionable product opportunities with ROI estimation

### External References
- [data/sources.json](data/sources.json) - Review platform URLs, API endpoints, and tool recommendations

---

## Navigation: Templates

### Full Reports
- [templates/review-mining-report.md](templates/review-mining-report.md) - Comprehensive mining report with all dimensions

### Source-Specific Extraction
- [templates/b2b-review-extraction.md](templates/b2b-review-extraction.md) - B2B software review extraction (G2, Capterra, TrustRadius)
- [templates/b2c-review-extraction.md](templates/b2c-review-extraction.md) - Consumer app review extraction (App Store, Play Store)
- [templates/community-sentiment.md](templates/community-sentiment.md) - Community sentiment analysis (Reddit, HN, ProductHunt)

### Competitive Analysis
- [templates/competitor-weakness-matrix.md](templates/competitor-weakness-matrix.md) - Cross-competitor weakness comparison
- [templates/switching-trigger-analysis.md](templates/switching-trigger-analysis.md) - Why customers leave competitors
- [templates/feature-request-aggregator.md](templates/feature-request-aggregator.md) - Unmet needs collection

### Pain Analysis
- [templates/pain-point-extraction-worksheet.md](templates/pain-point-extraction-worksheet.md) - Structured worksheet for 7-dimension pain extraction

### Opportunity Output
- [templates/opportunity-from-reviews.md](templates/opportunity-from-reviews.md) - Pain → Opportunity conversion

---

## Related Skills

- [../software-ux-research/SKILL.md](../software-ux-research/SKILL.md) - **UI/UX Sibling**: UI/UX-specific research (this skill goes broader)
- [../startup-idea-validation/SKILL.md](../startup-idea-validation/SKILL.md) - **Consumer**: Uses review mining data for validation scoring
- [../startup-trend-prediction/SKILL.md](../startup-trend-prediction/SKILL.md) - **Parallel**: Combines with trend data for timing
- [../router-startup/SKILL.md](../router-startup/SKILL.md) - **Orchestrator**: Routes to this skill for pain discovery
- [../product-management/SKILL.md](../product-management/SKILL.md) - **Consumer**: Uses pain points for discovery and roadmapping

---

## Operational Workflow

### Standard Mining Flow

```text
1. SCOPE (Define Target)
   +-- Which product/market to analyze?
   +-- Which competitors to include?
   +-- Time range (last 6-12 months recommended)

2. EXTRACT (Gather Data)
   +-- B2B: G2 → Capterra → TrustRadius
   +-- B2C: App Store → Play Store
   +-- Tech: GitHub → HN → Stack Overflow
   +-- Social: Twitter/X → Reddit → LinkedIn

3. CATEGORIZE (7 Dimensions)
   +-- UI/UX Pain
   +-- Pricing Pain
   +-- Support Pain
   +-- Integration Pain
   +-- Performance Pain
   +-- Onboarding Pain
   +-- Value Pain

4. SCORE (Prioritize)
   +-- Frequency (how often mentioned)
   +-- Severity (how painful)
   +-- Addressability (can we solve it?)

5. MAP (Convert to Opportunities)
   +-- Quick Wins (<2 weeks)
   +-- Medium Bets (2-8 weeks)
   +-- Big Differentiation (8+ weeks)

6. OUTPUT (Deliverable)
   +-- Review Mining Report
   +-- Competitor Weakness Matrix
   +-- Opportunity Backlog
```

### Integration with Validation Pipeline

```text
USER ASKS                              SKILL FLOW
──────────────────────────────────────────────────────────────
"Find opportunities in X market"  → startup-review-mining → Pain Report
                                         ↓
"What's trending?"               → startup-trend-prediction → Timing Analysis
                                         ↓
"Should we build this?"          → startup-idea-validation → GO/NO-GO Score
                                         ↓
"What skills do we need?"        → router-startup → Implementation Path
```

---

## Turning Insights Into Bets

- Convert pains → opportunities using [templates/opportunity-from-reviews.md](templates/opportunity-from-reviews.md).
- Turn opportunities into decisions using:
  - [../product-management/templates/strategy/opportunity-assessment.md](../product-management/templates/strategy/opportunity-assessment.md)
  - [../startup-idea-validation/templates/validation-experiment-planner.md](../startup-idea-validation/templates/validation-experiment-planner.md)

## Do / Avoid (Dec 2025)

### Do

- Keep an audit trail (source links, sampling notes, timestamps).
- Score insights by frequency × severity × segment importance × addressability.
- Triangulate top insights via interviews, support tickets, or usage data.

### Avoid

- Keyword counting without context or segmentation.
- Treating sentiment as demand without willingness-to-pay signals.
- Copying competitor feature requests without understanding the underlying job.

## What Good Looks Like

- Coverage: a defined time window and segment tags (plan documented, not ad-hoc scraping).
- Taxonomy: 10–30 themes with frequency + severity, each backed by verbatim quotes and links.
- Quality: spot-check a sample of clustered/summarized outputs and log corrections.
- Actionability: top themes become hypotheses with experiments and decision thresholds.
- Compliance: respect platform terms and detect suspicious/fake-review patterns (audit trail preserved).

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Summarization and clustering: require spot-checks and preserve source links.
- Automated extraction: log prompts/settings and keep reproducibility notes.

---

## Usage Notes

**For Claude**: When user asks to "find pain points" or "analyze reviews":
1. Ask which market/product/competitors to analyze
2. Use source-by-source-extraction.md for platform-specific queries
3. Categorize findings into 7 pain dimensions
4. Score by frequency × severity × addressability
5. Output using review-mining-report.md template

**For Claude**: When user asks to "find opportunities":
1. First extract pain points (above workflow)
2. Use review-to-opportunity-mapping.md to convert
3. Categorize into Quick Wins / Medium Bets / Big Differentiation
4. Feed to startup-idea-validation for scoring

**Output Formats**:
- Pain points: 7-dimension matrix with severity scores
- Competitor analysis: Weakness comparison with quote evidence
- Opportunities: Prioritized backlog with effort/impact estimates
- Switching triggers: Why customers leave (ranked by frequency)

**Key Principle**: Reviews are the voice of the customer. Mine them systematically.
