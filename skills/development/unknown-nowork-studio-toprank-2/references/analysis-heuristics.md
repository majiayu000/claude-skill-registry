# Meta Ads Analysis Heuristics

Entry point for any "how is my account doing", "find waste", "rank ad sets", or "why is X happening" question. These are the rules a paid-social analyst applies in their head — encoded so the agent doesn't drift into generic dashboard summaries.

## The Four-Pass Framework

For any account-level analysis, run four passes in order. Skip a pass only if it's empirically irrelevant to the question.

### Pass 1 — Stop the bleeding

Find spend that is structurally negative and recommend pausing or restructuring before doing anything else.

| Signal | Threshold | Action |
|---|---|---|
| Ad set spent ≥ $50 in last 7 days, 0 purchases (Sales objective) | Hard | Pause; investigate optimization event firing first |
| Ad set ROAS < 0.5 × Break-Even ROAS over rolling 14 days | Hard | Pause unless deliberate top-of-funnel push with downstream LTV justification |
| Ad set frequency > 5.0 with link CTR declining | Saturation | Rotate creative or audience; do not raise budget |
| Ad set in Learning Limited > 14 days, no improvement | Stuck | Consolidate or shift optimization event to higher-volume upstream event |
| Campaign spending on broken Pixel (EMQ < 5.0) | Tracking | Stop until Pixel + CAPI is fixed; downstream optimization is unreliable |

### Pass 2 — Capture more (scale what's working)

Identify ad sets and creative that are clearing Break-Even ROAS with headroom, and recommend scaling within the **20% rule** to avoid Learning Phase reset.

| Signal | Action |
|---|---|
| Ad set ROAS ≥ 1.3 × Break-Even, frequency ≤ 2.0, audience saturation < 30% | Increase budget +20% / week, monitor CPA drift after each step |
| Top creative concept by ROAS, declining frequency or steady CTR | Duplicate into a fresh ad set with broader audience to extend reach |
| Country / placement split shows a clear winner the campaign isn't capturing | Suggest a placement-isolated ad set for testing (acknowledge it limits Meta's optimization) |
| ASC (Advantage+ Shopping) outperforming manual prospecting on ROAS | Shift more budget to ASC; preserve a small manual cell as a control |

**Always check audience saturation before recommending scale.** A small custom audience already at 60% reach has nowhere to go.

### Pass 3 — Fix fundamentals

The structural issues that throttle the whole account, regardless of campaign-level performance.

| Issue | Symptom | Fix |
|---|---|---|
| Pixel + CAPI not deduplicated | Events Manager EMQ < 7.0, ROAS swings wildly between Meta vs Shopify | Server-side CAPI integration with event_id deduplication |
| Default attribution mismatched to sales cycle | High-consideration ecom on 1-day click | Move to 7DC1DV (the default) and re-baseline |
| Single ad set carries the whole campaign | Top ad set = > 70% of campaign spend | Diversify — single-ad-set dependency is fragile to fatigue |
| No retargeting layer | All spend on prospecting | Add a retargeting ad set on warm site visitors / engagers / cart abandoners |
| All creative on one concept / format | One UGC video, no static or other concepts | Build 3+ concept lanes; Meta needs creative diversity to optimize |
| Special Ad Category misclassified | Credit / employment / housing vertical running standard targeting | Reclassify in Ads Manager — risk of takedown otherwise |

### Pass 4 — Test next

After the account is clean and scaled, what's the next experiment? Frame this as a prioritized backlog, not a deployment:

- New audience (lookalike from a different seed, broad with creative-led targeting)
- New creative concept (UGC vs studio, problem-solution vs aspirational, founder-led vs polished)
- New attribution window experiment (does 1-day click match the data better than 7DC1DV?)
- New objective (move from Traffic to Conversions, or test Lead → Conversion event)

## Encoded Heuristics — apply these, they aren't obvious

- **Rank by spend × (Break-Even ROAS – Current ROAS), not by ROAS.** A 0.8× ROAS ad set spending $5,000/mo loses more than a 0.3× ROAS ad set spending $300/mo — the dollar gap is what matters.
- **Link CTR is a creative diagnostic, not a goal.** A 2.5% link CTR with 1.2× ROAS is worse than 0.8% link CTR with 4.5× ROAS. CTR rewards clickbait; ROAS rewards customers.
- **Frequency without a CPM trend is incomplete.** Frequency 4.0 with stable CPM and stable CTR is fine for warm retargeting. Frequency 4.0 with CPM up 30% week-over-week is fatigue.
- **Hook rate (3-sec views / impressions) leads link CTR by ~5 days on video creative.** Watch hook rate drop first; the CTR drop confirms it later.
- **CPM rising with no creative or audience change usually means competitive pressure or seasonality.** Cross-check with Q4 inflation, Black Friday, vertical-specific spikes (e.g. Valentine's for floral / jewelry, fitness in January).
- **Reported ROAS overestimates true ROAS post-iOS 14.** Modeled conversions inflate the in-platform number. Ground-truth against Shopify / GA4 / internal MMM before any major scaling decision.
- **A "Learning Limited" status persisting > 7 days means the ad set will never exit Learning at current volume.** It needs consolidation, a higher-volume optimization event, or more budget to clear 50 events / week.
- **Three ad sets with > 50% audience overlap to one another are not three ad sets — they're one fragmented ad set.** Consolidate.
- **Branded campaigns are rare on Meta** (unlike Search). If the user is running search-style "brand defense", that's usually wasted spend on Meta — Meta's discovery-led format means brand searchers are already converting elsewhere.

## How to structure the analysis output

For any audit-style question:

1. **Headline finding (one sentence).** "Account is profitable at MER 4.1× but Meta-reported ROAS overstates by ~25% vs. Shopify."
2. **Top 3 actions (with dollar impact).** "Pause ad sets X, Y, Z — saves $1,420/mo. Refresh creative on ad set A — projected lift $800/mo."
3. **Evidence.** Specific campaign / ad set names, dollar amounts, percentage deltas, attribution windows.
4. **What you didn't check (and why).** Honest. "Skipped placement breakdowns because the question was about budget pacing."

Avoid the dashboard-summary trap: long tables of numbers without verdicts. Every number should be paired with a "so what" — otherwise it's noise.
