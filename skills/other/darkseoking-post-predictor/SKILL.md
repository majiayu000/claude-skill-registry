---
name: darkseoking-post-predictor
description: Use when predicting Threads post performance, analyzing post history patterns, estimating engagement ceiling for a draft, or deciding what content type to write next. Works with or without personal data — uses darkseoking benchmark as fallback.
---

# Threads Post Predictor

Analyzes historical Threads post data using algorithm knowledge from `darkseoking-mindset` to predict post performance and recommend optimal content strategy.

## How to Use

### With personal profile (most precise)

1. Load [personal-profile.md](references/personal-profile.md) — pre-built account baselines, quadrant data, persona tags
2. Load [prediction-model.md](references/prediction-model.md) — run V2 dual-stage prediction using personal data
3. Present findings: quadrant diagnosis, Views/ER ranges, optimization path

### With post history CSV but no profile (build one)

1. User provides post history — see **Data Format** below
2. Load [historical-analysis.md](references/historical-analysis.md) — build personal baseline and patterns
3. Save output as `references/personal-profile.md` for future use
4. Load [prediction-model.md](references/prediction-model.md) — predict using freshly built profile

### Without any personal data (benchmark only)

1. Skip historical-analysis.md and personal-profile.md
2. Load [prediction-model.md](references/prediction-model.md) — use darkseoking benchmark patterns directly
3. Predict based on content type hierarchy, thread structure, and algorithm rules
4. Note: predictions are directional (which content type has higher ceiling) rather than numeric. Cannot distinguish distribution-driven vs conversion-driven success without views data.

## Data Format

**Minimum useful data per post:** content (or topic summary) + at least one engagement metric (likes, comments, or reposts).

**For V2 dual-stage prediction (strongly recommended):** views + likes per post. Without views, prediction falls back to V1 single-stage and cannot distinguish distribution-driven vs conversion-driven success.

**Ideal CSV columns:** content, likes, views, replies, reposts, shares, engagement_rate, media_type, is_quote, created_at

**Minimum posts:** 15+ for meaningful baseline. 30+ for pattern extraction. Under 15 — use darkseoking benchmark with caveats.

**Accepted formats:** CSV, pasted list, verbal description of recent 5-10 posts with approximate engagement numbers.

**Personal profile:** If `references/personal-profile.md` exists, load it to skip re-running full historical analysis. If it doesn't exist and user provides CSV, run historical-analysis.md and save the output as `references/personal-profile.md`. Profiles should be refreshed when new data is available (e.g. monthly).

## Scenes

| Scenario | Action |
|----------|--------|
| User provides full post history | Run complete analysis + prediction |
| User asks "what should I write next?" with data context | Run content-type recommendation |
| User wants to know ceiling before posting | Run prediction on draft + historical context |
| User wants to understand why a post underperformed | Run gap analysis against historical patterns |
| User has no data, just wants general guidance | Use darkseoking benchmark patterns from prediction-model.md |

## References

- [historical-analysis.md](references/historical-analysis.md) — how to extract patterns from post data
- [prediction-model.md](references/prediction-model.md) — how to predict ceiling and recommend strategy (V2: dual-stage Views × ER)
- [personal-profile.md](references/personal-profile.md) — personal baseline, quadrant profile, persona tags (gitignored; built from user's post data)
- Benchmark data → `darkseoking-mindset/references/darkseoking-all-posts.csv`
- Algorithm knowledge → `darkseoking-mindset` skill
