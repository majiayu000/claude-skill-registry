---
name: pm-feedback
description: Классифицирует пользовательский фидбек (Excel/CSV/текст) по 6 категориям, делает sentiment-анализ, кластеризацию тем, анализ трендов, триангуляцию по источникам, расчёт NPS и извлечение персон. На выходе — Top-10 болей с рекомендациями к действию. User-invoked only — do NOT auto-trigger. Triggers on /pm-feedback, "анализ обратной связи", "разбор отзывов", "анализ NPS", "analyze user feedback", "VOC analysis", "NPS analysis", "review analysis".
---

# pm-feedback — User feedback analysis


Part of the Personal Corp framework — running a one-person business through AI agents.
Structure raw feedback into a decision-driving insight report. Built-in classification, sentiment, theme clustering, NPS, trend analysis, source triangulation, and persona extraction.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Feedback data | yes | Excel / CSV / pasted text / review screenshots |
| Purpose | no | Product improvement / satisfaction / topic-specific (e.g. post-launch reaction); default product improvement |
| Time range | no | For freshness tagging and trend analysis |
| Source channels | no | Multiple channels enable triangulation |

**Mode:** ≤ 20 items → close-read mode (item-by-item with detailed reading); > 20 → statistical mode (auto-classify + aggregated report).

## Step 1 — Pre-process data

- Drop exact duplicates
- Merge near-duplicates (similarity > 90%), record merge count
- Ultra-short items (< 5 chars, no substance like "good"/"bad") → counted separately, not in deep analysis
- If a rating column exists (1-10 or 1-5 stars) → extract for NPS
- Identify source channel (in-app feedback, app store, support ticket, social media, etc.)

## Step 2 — Classification

**Six-category taxonomy:**

| Category | Criterion | Example |
|---|---|---|
| **Feature request** | User wants something not yet built | "I'd like batch export" |
| **Bug report** | Existing feature behaves incorrectly | "Save button loses my data" |
| **Usage question** | User can't find or doesn't know how | "How do I change my password?" |
| **UX complaint** | Feature exists but experience is poor | "Loading is too slow" / "UI too cluttered" |
| **Positive review** | Satisfaction, praise, recommendation | "Love this feature!" |
| **Other** | Unclassifiable or off-topic | Spam, ads, noise |

When ambiguous (one item spans multiple), tag primary + secondary.

## Step 3 — Sentiment analysis

| Sentiment | Signals | Calibration |
|---|---|---|
| **Positive** | Likes, praise, recommends, thanks | Pure factual praise ("works") = neutral, not positive |
| **Neutral** | Statement of fact, question, calm suggestion | Feature requests = neutral by default unless angry |
| **Negative** | Complaint, anger, disappointment, threats | "I wish you supported X" = neutral; "Why don't you support X yet?" = negative |

**Negative-intensity grading:**
- **Mild:** calm dissatisfaction ("not very convenient")
- **Medium:** explicit disappointment ("very disappointed", "bad experience")
- **Severe:** threats ("I'll uninstall if not fixed", "I'll file a complaint") → high-priority handling

## Step 4 — Theme clustering

Apply two methods to extract core themes.

**Method A — Affinity mapping:**

1. **Split observations:** decompose each feedback item into independent observation cards
2. **Natural cluster:** group by similarity without preset labels — let themes emerge
3. **Name themes:** label each cluster ("payment flow friction", "search results irrelevant")
4. **Identify hierarchy:** group small clusters under larger themes (e.g. "payment friction" + "long refund cycle" → "transaction experience")
5. **Flag outliers:** items that fit no cluster — possible early signals

**Method B — Thematic coding:**

1. **Open coding:** tag each item with descriptive labels ("slow load", "crash", "hidden entry point")
2. **Axial coding:** group descriptive labels into abstract themes ("slow load" + "crash" → "performance issues")
3. **Selective coding:** identify core themes and their relationships
4. **Quantify frequency:** count mentions and share per theme

**Cluster output:**

| Theme | Sub-theme | Mentions | Share | Representative quote |
|---|---|---|---|---|
| {theme 1} | {sub-a} | {N} | {X%} | "verbatim quote" |

## Step 5 — NPS analysis (if rating data exists)

- **NPS = % Promoters (9-10) − % Detractors (0-6)**
- Industry benchmarks: SaaS avg 30-40, consumer apps avg 20-30
- 5-star → 10-pt mapping: 5★=10, 4★=8, 3★=6, 2★=4, 1★=2

## Step 6 — Trend analysis (if time data exists)

**MoM (or WoW) change calculation:**
- Aggregate by week or month per category
- Growth rate = (current − previous) / previous × 100%
- Watch for > 30% changes — flag as "needs attention"

**Inflection-point detection:**
- 3+ consecutive periods in one direction → established trend
- Sudden direction reversal → trigger investigation
- Correlate with external events: releases, campaigns, competitor moves

**Trend output:**
- Time-series description per category
- Mark significant changes + likely cause
- Early-warning: which metrics are deteriorating, which improving

## Step 7 — Triangulation

When data spans multiple channels, cross-validate to lift confidence.

**Method triangulation:** same problem confirmed by different methods
- e.g. theme cluster says "slow load = top pain" → check if NPS detractors' open-ended answers also concentrate on performance

**Source triangulation:** same finding across channels
- App-store complaints + support tickets + community chatter all cite "crash" → high confidence
- Single-channel finding → tag "single-source, needs validation"

**Time triangulation:** persistence of the same problem
- > 3 weeks consistent → systemic
- One-off → likely transient or already fixed

**Confidence tiers:**

| Tier | Conditions | Tag |
|---|---|---|
| **High** | Multi-source + multi-method + persistent | Decision-ready |
| **Medium** | 2 of the 3 dimensions support | Recommend more data before deciding |
| **Low** | Single source or single method | Reference only, validate further |

## Step 8 — Persona extraction

Identify typical user types from the feedback corpus.

**Method:**
1. **Behavior cluster:** infer user types (newbie / veteran / power user / occasional)
2. **Need cluster:** which users care about efficiency, which about experience, which about price
3. **Sentiment cluster:** loyal advocates / silent users / vocal complainers / churn-edge

**Persona template:**
```
[Persona name]: {one-sentence description}
- Typical traits: {usage frequency, focus, behavior pattern}
- Core need: {primary concern}
- Main pain: {recurring problem}
- Feedback style: {how they express}
- Estimated share: {% of feedback corpus}
- Quote: "{verbatim}"
```

Cap at 3-5 personas — more loses actionability.

## Step 9 — Pain-point ranking

**Pain priority = Frequency × Severity × User weight × Confidence**

| Dimension | Scoring |
|---|---|
| **Frequency** | High (> 10) = 3, Medium (3-10) = 2, Low (< 3) = 1 |
| **Severity** | Critical (feature broken) = 3, Severe (blocks core flow) = 2, Mild (annoying but usable) = 1 |
| **User weight** | Paying = 1.5, Free = 1.0 (or 1.0 if no segmentation data) |
| **Confidence** | High (triangulated) = 1.2, Medium = 1.0, Low (single source) = 0.8 |

Sort descending; output Top 10.

## Step 10 — Generate report

```markdown
# User Feedback Analysis Report

**Period:** {date range}
**Total feedback:** {N} (after dedup: {M})
**Sources:** {channel list}

## 1. Classification
| Category | Count | Share | MoM change (if available) |
|---|---|---|---|

## 2. Sentiment
**Positive:** {X}% | **Neutral:** {Y}% | **Negative:** {Z}%
(Negative breakdown: mild {a} / medium {b} / severe {c})

## 3. Themes
| Theme | Sub-theme | Mentions | Share | Confidence |
|---|---|---|---|---|

## 4. NPS (if rating data)
**Score:** {n} (Promoters {X}% − Detractors {Y}%)
**Benchmark:** {above/below} industry by {Δ}

## 5. Trends (if time data)
- Significant rises: {category}, +{X}% MoM
- Significant drops: {category}, −{X}% MoM
- Inflection events: {description}

## 6. Top 10 Pain Points
| Rank | Pain | Freq | Severity | Confidence | Score | Quote | Recommendation |
|---|---|---|---|---|---|---|---|

## 7. Personas
<!-- 3-5 personas -->

## 8. Key Insights
<!-- Each insight: finding + data + confidence + meaning -->
1. {insight 1}
2. {insight 2}
3. {insight 3}

## 9. Improvement Recommendations
| Priority | Recommendation | Linked pain | Expected impact | Validation method |
|---|---|---|---|---|

## 10. Statistical Notes
- Classification confidence: {high/medium} (sample {N})
- Ambiguous classifications: {count}
- Triangulation coverage: {X%} of findings multi-source verified
- Validity: {sufficient sample / limited sample, results reference-only}
```

## Quality bar

1. Classifications grounded; ambiguous items tag confidence
2. Insights backed by numbers; every insight cites a count
3. Recommendations actionable to feature level
4. Sample < 50 → tag "limited sample, results reference-only"
5. Stats computed via code for accuracy
6. Sentiment runs through calibration rules
7. Theme clusters MECE (mutually exclusive, collectively exhaustive)
8. Triangulation tier explicit per finding

## Red lines

1. **No over-extrapolation** — 3 of 20 items mention X ≠ "many users say X"
2. **Preserve verbatim** — every pain point includes a representative quote for traceability
3. **No fabricated trends** — no MoM analysis without history
4. **No invented personas** — personas grounded in cluster results, not imagined

## When input is incomplete

- **< 10 items** → close-read each; skip statistics (sample too small)
- **No source/time info** → analyze, but tag "missing source/time, recommend supplementing"; skip trend + triangulation
- **Mixed languages** → group by language, analyze separately
- **Single-source** → analyze, but tag "single source, recommend cross-channel validation"

## Related skills

- `/pm-prioritize` — feature requests from feedback → RICE-rank
- `/pm-prd` — high-frequency requests → PRDs
- `/pm-competitive` — competitor mentions in feedback → enrich competitor study
- `/pm-metrics` — cross-validate feedback trends with product metrics

