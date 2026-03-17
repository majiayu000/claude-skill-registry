---
name: performance-correlation
description: |
  Correlate content attributes with performance metrics across GA4, GSC, and SE Ranking.
  Identify what drives performance and build optimization hypotheses.
---

# Performance Correlation

## When to Use

- Connecting content changes to metric changes
- Identifying what drives performance
- Building optimization hypotheses
- A/B test analysis
- Content audit findings

## Cross-Source Correlation Patterns

### Pattern Library

#### Pattern 1: High Impressions + Low CTR + Good Position

```
GSC: Impressions ↑ | CTR ↓ | Position 3-7
GA4: N/A (users don't click)
```

**Diagnosis**: Title/meta description not compelling enough

**Evidence Needed**:
- Compare your snippet to competitors in positions 1-2
- Check for SERP features stealing attention
- Analyze query intent match

**Recommended Actions**:
1. Rewrite title with power words, numbers, or year
2. Add compelling meta description with clear benefit
3. Target featured snippet if applicable

**Expected Impact**: +50-100% CTR improvement possible

---

#### Pattern 2: High CTR + Low Engagement

```
GSC: CTR ↑ | Position stable
GA4: Bounce ↑ | Time on Page ↓ | Scroll Depth ↓
```

**Diagnosis**: Content doesn't match search intent or promise

**Evidence Needed**:
- Compare content to search query expectations
- Check if title oversells/misleads
- Analyze competing content that ranks

**Recommended Actions**:
1. Align content opening with search intent
2. Deliver promised value in first 100 words
3. Add table of contents for scanners

**Expected Impact**: -20-30% bounce rate, +50% time on page

---

#### Pattern 3: High Engagement + Low Rankings

```
GA4: Time on Page ↑ | Bounce ↓ | Scroll Depth ↑
GSC: Position ↓ | Impressions ↓
SE Ranking: Visibility ↓
```

**Diagnosis**: Good content but weak SEO signals

**Evidence Needed**:
- Check backlink profile vs competitors
- Analyze internal linking to this page
- Review technical SEO factors

**Recommended Actions**:
1. Build quality backlinks to page
2. Add internal links from high-authority pages
3. Improve on-page SEO (keyword density, headers)

**Expected Impact**: +5-15 position improvement over 2-3 months

---

#### Pattern 4: Declining Rankings + Stable Traffic

```
SE Ranking: Position ↓ | Visibility ↓
GSC: Impressions → | Clicks → (or slight ↓)
GA4: Traffic → (from brand/direct)
```

**Diagnosis**: Competitors advancing, brand queries protecting you

**Evidence Needed**:
- Competitor content comparison
- Content freshness analysis
- Backlink velocity comparison

**Recommended Actions**:
1. Content refresh with updated data/examples
2. Add new sections competitors have
3. Accelerate link building

**Expected Impact**: Prevent further decline, regain positions

---

#### Pattern 5: Good Rankings + Low Impressions

```
SE Ranking: Position 1-5
GSC: Impressions ↓ | CTR normal
GA4: Traffic ↓
```

**Diagnosis**: Keyword losing search volume

**Evidence Needed**:
- Google Trends for keyword
- Seasonal patterns analysis
- Industry shifts

**Recommended Actions**:
1. Target related growing keywords
2. Expand content for related queries
3. Consider pivoting topic angle

**Expected Impact**: Capture adjacent search demand

---

#### Pattern 6: Position Volatility

```
GSC: Position fluctuates ±10 daily
SE Ranking: Inconsistent ranking reports
```

**Diagnosis**: Google testing your content, or thin content threshold

**Evidence Needed**:
- Content depth vs competitors
- E-E-A-T signals present
- Page experience metrics

**Recommended Actions**:
1. Strengthen E-E-A-T signals
2. Add depth and originality
3. Improve page experience

**Expected Impact**: Position stabilization within 2-4 weeks

## Correlation Matrix Template

### Content Changes Timeline

Track all modifications to correlate with metrics:

```markdown
## Content Change Log: {URL}

| Date | Change Type | Description | Scope |
|------|-------------|-------------|-------|
| 2025-12-01 | Content | Added 500 words on AI SEO | Major |
| 2025-12-10 | Meta | Updated title tag | Minor |
| 2025-12-15 | Links | Added 3 internal links | Minor |
| 2025-12-20 | Technical | Improved page speed | Technical |
```

### Metric Response Timeline

Map metric changes to content changes:

```markdown
## Metric Response Analysis

| Date | Metric | Before | After | Change | Likely Cause |
|------|--------|--------|-------|--------|--------------|
| Dec 5 | Position | 8.2 | 6.1 | +2.1 | Content expansion |
| Dec 12 | CTR | 2.1% | 3.8% | +1.7pp | Title update |
| Dec 18 | Time on Page | 2:10 | 3:45 | +1:35 | Content depth |
| Dec 22 | LCP | 2.8s | 1.9s | -0.9s | Speed optimization |
```

### Correlation Confidence

Rate confidence in cause-effect relationships:

```markdown
## Correlation Confidence Assessment

| Change | Metric Impact | Confidence | Reasoning |
|--------|---------------|------------|-----------|
| +500 words | Position +2.1 | HIGH | Timing matches, logical connection |
| Title update | CTR +1.7pp | HIGH | Direct relationship, immediate effect |
| Internal links | ? | LOW | Too recent, effect delayed |
| Speed fix | Bounce -5% | MEDIUM | Timing matches, indirect relationship |
```

## Multi-Source Correlation

### Unified Performance View

```markdown
## Cross-Platform Correlation: {URL}

### Traffic & Visibility
| Source | Metric | Value | Trend | Correlation |
|--------|--------|-------|-------|-------------|
| GSC | Impressions | 15,200 | ↑ +12% | Search visibility growing |
| GSC | Clicks | 428 | ↑ +8% | Traffic following visibility |
| GA4 | Sessions | 512 | ↑ +10% | Confirms GSC data |
| SE Ranking | Visibility | 42 | ↑ +5 | Ranking improvements |

### Engagement Quality
| Source | Metric | Value | Trend | Correlation |
|--------|--------|-------|-------|-------------|
| GSC | CTR | 2.8% | → stable | Snippet unchanged |
| GA4 | Bounce Rate | 38% | ↓ -4% | Content improvements working |
| GA4 | Avg Time | 3:42 | ↑ +0:45 | Users more engaged |
| GA4 | Scroll Depth | 72% | ↑ +8% | Content structure improved |

### Ranking Performance
| Source | Keyword | Position | Change | Opportunity |
|--------|---------|----------|--------|-------------|
| SE Ranking | seo guide | 4 | +2 | Target position 1-3 |
| SE Ranking | seo best practices | 7 | +1 | Content gap vs leader |
| GSC | seo tips 2025 | 12 | -3 | Needs freshness update |
```

## Hypothesis Building

### Template

```markdown
## Optimization Hypothesis

**Observation**: {what the data shows}

**Hypothesis**: {proposed cause-effect relationship}

**Test Plan**:
1. {specific change to make}
2. {metrics to monitor}
3. {timeframe for evaluation}

**Success Criteria**:
- Primary: {main metric target}
- Secondary: {supporting metric targets}

**Risk Assessment**:
- Probability of success: {HIGH|MEDIUM|LOW}
- Potential downside: {risk description}
- Mitigation: {how to minimize risk}
```

### Example Hypothesis

```markdown
## Optimization Hypothesis: CTR Improvement

**Observation**: Page ranks #4 for "seo guide 2025" with 15K monthly
impressions but only 2.8% CTR (below 5% benchmark).

**Hypothesis**: Updating title to include "Complete" and current year
will increase CTR by appealing to users seeking comprehensive, fresh content.

**Test Plan**:
1. Change title from "SEO Guide: Tips for Success" to
   "Complete SEO Guide 2025: 15 Proven Strategies"
2. Monitor: CTR, impressions, position, clicks
3. Evaluate after 2 weeks of data

**Success Criteria**:
- Primary: CTR increases from 2.8% to >4%
- Secondary: Clicks increase by >30%
- Position maintains or improves

**Risk Assessment**:
- Probability of success: HIGH (title changes typically show results)
- Potential downside: Slight position fluctuation during testing
- Mitigation: Don't change other page elements simultaneously
```
