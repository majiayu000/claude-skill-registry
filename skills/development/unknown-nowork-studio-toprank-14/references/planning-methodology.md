# Content Planning Methodology

Reference for `/content-planner`. The skill applies these rules; this file is
the load-bearing logic, kept out of the SKILL.md so the prompt stays focused on
workflow.

---

## CTR-by-position curve (informational intent)

Use as the baseline for "expected CTR at position P". Numbers reflect ~2024–2026
median informational CTR; transactional and brand queries skew higher.

| Position | Expected CTR |
|---|---|
| 1  | 0.275 |
| 2  | 0.160 |
| 3  | 0.110 |
| 4  | 0.080 |
| 5  | 0.062 |
| 6  | 0.050 |
| 7  | 0.040 |
| 8  | 0.033 |
| 9  | 0.028 |
| 10 | 0.024 |
| 11–20 | 0.010 |
| 21+   | < 0.005 |

A query whose actual CTR is < 50% of the expected CTR at its average position
is a **CTR underperformer** — title/meta rewrite candidate, not new content.

---

## Opportunity buckets — full rubric

### Bucket A: Striking-distance queries
Condition: average position in **[5.0, 20.0]**, impressions/90d ≥ 100, intent
is informational (the query has "how", "what", "why", "best", "vs", "guide",
or is a noun phrase Google answers with content).

Action: schedule a new post or substantial refresh that targets the exact
query intent.

### Bucket B: Unanswered intent (gaps)
Condition: query appears in GSC at position > 20 with impressions ≥ 50/90d,
and no page on the site ranks for it in the top 20 (the query×page report
shows only one weak page or none).

Action: schedule a new post. Verify it fits the site's topical area against
`business-context.json` if available — don't plan a gardening post for a SaaS
analytics site just because GSC saw 200 impressions for "compost ratios".

### Bucket C: CTR underperformers (refresh)
Condition: position in **[1.0, 10.0]**, impressions/90d ≥ 500, actual CTR <
0.5 × expected CTR at that position.

Action: emit a **refresh** entry — type = "refresh", `refreshTarget` set to
the URL. The writerPrompt should point at `/meta-tags-optimizer` first, then
`/content-writer` for body refresh if needed.

### Bucket D: Related-keyword expansions
Not its own calendar entry. For each Bucket A/B parent, identify 2–4 related
queries from the same `query × page` cluster — synonyms, long-tails, question
forms, "[parent] vs X", "[parent] for [audience]". They become **secondary
keywords** on the parent's calendar entry → become H2s in the eventual post.

### Bucket E: Cannibalization warning
Condition: same query appears at position < 20 for **two or more pages on the
same site**, each with ≥ 20 impressions.

Action: write a warning into `warnings[]`, do NOT schedule new content for
this query. Route the user to `/seo-analysis` for the canonical-page fix.

---

## Click potential formula

For each candidate topic that survives bucket classification:

```
projectedImpressions   = impressions90d × seasonalityFactor
targetCtrAtPosition3   = 0.110   # from CTR curve, informational baseline
currentExpectedClicks  = impressions90d × currentCtr
projectedClicks        = projectedImpressions × targetCtrAtPosition3
clickPotential         = projectedClicks − currentExpectedClicks
```

`seasonalityFactor` defaults to 1.0. If the query is clearly seasonal (e.g.
"black friday", "tax filing", "summer camp"), adjust the next 90 days:

| Pattern | factor (next 90d) |
|---|---|
| Peak season ahead | 2.0 |
| Mid-season | 1.0 |
| Off-season trailing | 0.4 |

Tie-breakers when click potential is within 10%:
1. Lower content-production cost (refresh > new post)
2. Higher intent-to-revenue alignment (commercial > pure informational)
3. Closer to topical authority the site already has

---

## Scheduling rules

- **One post per week** by default. The agent should not pack 12 posts into 4
  weeks just because the data supports it — production capacity is the real
  bottleneck, and SEO compounds over months.
- **P0 first** — the top 4 by click potential are P0, the next 4 are P1, the
  rest P2. Schedule P0s in weeks 1–4.
- **Refresh entries can run in parallel** with new posts (they're cheaper to
  ship) — schedule them as same-week siblings, not consuming a weekly slot.
- **Skip weeks** where the user has external deadlines if they tell you about
  them — don't fight the user's actual calendar.

---

## Click-potential output (what the JSON has to carry)

For every topic in `content-calendar.json`:

```json
"gsc": {
  "currentPosition": 9.4,
  "impressions90d": 2480,
  "currentCtr": 0.018,
  "clickPotential": 228
}
```

`clickPotential` is the **estimated additional monthly clicks** if the topic
hits position 3. It's an upper-bound estimate, not a guarantee — communicate
that clearly in the rationale field.

---

## Title-hook reuse

Every planned title goes through the four `/content-writer` hook patterns:
number + specificity, audience-named guide, contrarian myth-break, outcome
promise + proof. Reject bare-keyword titles ("Facebook SEO Optimization") at
the planning stage — fixing it post-write costs more.

---

## Failure modes to avoid

- **Padding the calendar** with low-clickPotential topics to hit a count.
  Better to ship 6 strong topics than 12 mediocre ones.
- **Ignoring intent mismatch** between bucket A queries and the site's actual
  business. If GSC sees a query but the site can't credibly answer it,
  skip it.
- **Treating impressions as volume** for brand-new queries. GSC impressions
  reflect what *you* served — a query with 12 impressions could be a 12k/mo
  query you barely show for. When third-party volume isn't available, note
  the uncertainty in the rationale.
- **Scheduling refreshes for pages that are already strong** (position < 3,
  CTR within 80% of expected). Don't break what works.
