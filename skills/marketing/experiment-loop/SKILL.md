---
name: experiment-loop
description: Weekly experiment tracking loop for MD Home Care. Scans content changes, measures traffic impact via PostHog and GSC, and makes keep/iterate/revert decisions with lag-adjusted attribution.
---

# Experiment Loop for MD Home Care

Tracks content changes, measures their impact on traffic and rankings, and decides whether to keep, iterate, or revert. Runs weekly.

## CRITICAL: Lag Times for YMYL Content

YMYL content (aged care, disability services) has longer lag times than SaaS content. Do not evaluate changes too early.

| Change Type | SEO Lag | AEO Lag | Evaluation Window |
|-------------|---------|---------|-------------------|
| Service page optimization | 10-21 days | 3-7 days | 3 weeks minimum |
| Location page creation | 14-21 days | 7-14 days | 3 weeks minimum |
| Blog post publishing | 7-14 days | 3-7 days | 2 weeks minimum |
| Provider comparison addition | 7-14 days | 3-7 days | 2 weeks minimum |
| Trust signal enhancement | 10-21 days | 7-14 days | 3 weeks minimum |
| FAQ addition | 7-14 days | 3-7 days | 2 weeks minimum |

---

## Step 1: Weekly Git Scan

Identify all content changes from the past week:

```bash
cd ~/Projects/mdhomecarebuild

# All content changes in last 7 days
git log --since="7 days ago" --name-only --pretty=format:"%h %s" -- "src/content/**/*.md" "src/content/**/*.mdx"

# Summarize by type
git log --since="7 days ago" --name-only --pretty=format:"" -- "src/content/blog/*.md" | sort -u | head -20
git log --since="7 days ago" --name-only --pretty=format:"" -- "src/content/services/*.md" | sort -u | head -20
git log --since="7 days ago" --name-only --pretty=format:"" -- "src/content/providers/*.md" | sort -u | head -20
```

Categorize each change:

- **New page:** Completely new content file
- **Major edit:** Structural changes (new sections, comparison tables, rewritten H1/H2)
- **Minor edit:** Small fixes (typos, link updates, frontmatter changes)

---

## Step 2: Baseline Measurement

For each changed page, capture the pre-change baseline. If baseline was not captured before the change, use the previous period as proxy.

### GSC Baseline

```bash
cd ~/Projects/mdhomecarebuild

# For each changed page, get keyword data
python3 src/scripts/advanced_gsc_analyzer.py --page "/services/[slug]"
python3 src/scripts/advanced_gsc_analyzer.py --page "/blog/[slug]"
```

Record:
- Top 10 keywords by clicks
- Average position for primary keyword
- Total impressions and clicks (last 7 days)

### PostHog Baseline

```bash
# Page traffic
python3 src/scripts/posthog_analytics.py --page "/services/[slug]" --days 7

# AI referral traffic
python3 src/scripts/posthog_analytics.py --ai-referrals --days 7
```

Record:
- Total pageviews (last 7 days)
- AI referral visits to that page
- Traffic sources breakdown

---

## Step 3: Post-Change Measurement

After the evaluation window has passed (see lag times table), measure again.

```bash
# GSC: same page analysis
python3 src/scripts/advanced_gsc_analyzer.py --page "/services/[slug]"

# PostHog: same page traffic
python3 src/scripts/posthog_analytics.py --page "/services/[slug]" --days 7
python3 src/scripts/posthog_analytics.py --ai-referrals --days 7
```

---

## Step 4: Attribution and Decision

### Compare Metrics

For each experiment, calculate:

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Organic clicks (7d) | X | Y | +/- % |
| Impressions (7d) | X | Y | +/- % |
| Avg position (primary KW) | X | Y | +/- positions |
| AI referral visits (7d) | X | Y | +/- % |
| Total pageviews (7d) | X | Y | +/- % |

### Decision Framework

**KEEP** if:
- Organic clicks increased >10%
- OR average position improved by 2+ positions
- OR AI referral visits increased >20%
- OR impressions increased >15% (leading indicator)
- AND no negative impact on other pages (cannibalization check)

**ITERATE** if:
- Mixed signals (some metrics up, some flat)
- OR small positive movement (<10% clicks) that suggests potential
- OR evaluation window has not fully elapsed
- Action: Make targeted refinements and re-evaluate after another cycle

**REVERT** if:
- Organic clicks decreased >15%
- AND average position dropped by 3+ positions
- AND no compensating AI referral increase
- Action: Restore previous version via git, document what went wrong

**WAIT** if:
- Change is too recent (within lag window)
- Action: Re-evaluate next week

---

## Step 5: Log to Playbook

Record every experiment result in PLAYBOOK.md:

```markdown
## [Date] - [Experiment Name]

**Category:** [Service page optimization / Location page / Blog post / Comparison / Trust signal / FAQ]
**Page:** [URL path]
**Change:** [Brief description of what was changed]
**Hypothesis:** [What we expected to happen]

**Baseline (pre-change):**
- Organic clicks (7d): X
- Avg position (primary KW): X
- AI referrals (7d): X

**Result (post-change, measured [date]):**
- Organic clicks (7d): Y (+/- %)
- Avg position (primary KW): Y (+/- positions)
- AI referrals (7d): Y (+/- %)

**Decision:** KEEP / ITERATE / REVERT / WAIT
**Lesson:** [What we learned]
```

---

## Experiment Categories

### Service Page Optimizations
- Adding comparison tables
- Rewriting H1/byline
- Adding trust signal sections
- Expanding FAQ sections
- Adding AI differentiation paragraphs

### Location Page Creation
- New suburb-specific service pages
- Measure: local keyword rankings, location-specific traffic

### Blog Post Publishing
- New informational content
- Template/download posts
- Provider comparison posts
- Measure: organic clicks, keyword coverage expansion

### Provider Comparison Additions
- New comparison tables on existing pages
- New "vs" blog posts
- Measure: comparison keyword rankings, AI referral traffic

### Trust Signal Enhancements
- Adding registration numbers
- Adding testimonials
- Adding clinical governance sections
- Measure: overall page authority signals, position changes

### FAQ Additions
- New FAQ sections
- Expanding existing FAQs with PAA questions
- Measure: featured snippet captures, PAA appearances

---

## Weekly Routine

Every week:

1. Run git scan (Step 1)
2. For changes past their evaluation window, measure results (Step 3)
3. Make keep/iterate/revert decisions (Step 4)
4. Log results to PLAYBOOK.md (Step 5)
5. Capture baselines for new changes (Step 2)

---

## Usage

```
/experiment-loop
```

Runs the full weekly cycle: scan, measure, decide, log.

```
/experiment-loop --check "/services/sil-services"
```

Check status of a specific page experiment.
