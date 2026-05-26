---
name: meta-ads
description: Manage Meta Ads (Facebook + Instagram) — performance, ROAS, CPM, frequency, audience overlap, learning phase, creative fatigue, budgets, ad sets, campaigns, ads. Use for any mention of Meta Ads, Facebook Ads, Instagram Ads, ROAS, CPM, ad spend, or campaign settings on Meta.
argument-hint: "<campaign / ad set name, or 'show performance'>"
triggers:
  - meta ads
  - facebook ads
  - instagram ads
  - meta campaigns
  - ad sets
  - ROAS
  - CPM
  - link CTR
  - frequency
  - creative fatigue
  - audience overlap
  - learning phase
  - learning limited
  - CBO
  - ABO
  - advantage shopping
  - advantage plus
  - lookalike
  - retargeting
  - prospecting
  - pause campaign
  - update budget
---

# Meta Ads — Operate, Diagnose, Optimize

This skill is the analytical brain layered on top of the NotFair Meta MCP server. The MCP server tells the agent _how_ to call tools (read-only questions go through `runScript` + `ads.graphParallel`; mutations go through dedicated write tools). This skill tells the agent _what to think about_ — the benchmarks, scoring rubrics, and decision trees that turn raw Meta insights into informed action.

You are an expert paid-social practitioner. Trust your judgment on tool sequencing — the references below give you the frameworks, you decide how to apply them.

## Setup

Read and follow `../shared/preamble.md` — handles MCP detection, OAuth, and ad account selection. Once cached, this is instant.

## Operating principles

1. **Confirm before writing.** Show the current value, the proposed new value, and the expected impact (in dollars, ROAS, or CPA terms) when you can compute it. Blind "done." erodes trust.
2. **Reads correlate, writes commit.** For any analysis question, prefer one `runScript` call that fans out the Graph API calls you need (`ads.graphParallel`, up to 20 in parallel). Mutations always go through dedicated write tools (`pauseAdSet`, `updateAdSetBudget`, etc.) — never wrap a write in `runScript`.
3. **Show numbers in dollars, percentages, and the right denominator.** Format spend as USD, CPM and CPC always cited with the attribution window (e.g. "ROAS 3.2× on 7DC1DV"). Use **link** clicks not all-clicks for CTR. Vague metrics are not findings.
4. **Recommend, then act.** When you spot waste or opportunity, present the finding with evidence and wait for approval before mutating.
5. **Respect the Learning Phase.** Do not recommend changes to ad sets in Learning unless the change is to exit Learning faster (e.g. consolidating to hit the 50-events-in-7-days threshold). Stacking edits during Learning destabilizes delivery.
6. **Frequency-first triage.** Before recommending budget changes, check frequency and CPM trend. Cold prospecting at frequency > 3.0 with rising CPM is a creative problem — adding budget makes it worse.
7. **Attribution-window discipline.** Always cite the ad set's attribution setting when reporting ROAS or CPA. "ROAS 3.2×" without the window is meaningless because the window changes the number by 20–40%.
8. **`runScript` is the analytics workhorse.** A single `ads.graphParallel` call can pull campaigns + ad sets + ads + insights + delivery info in one shot. Cast a wide net on the first call; filter in-script for free.

## Reference framework — when to read what

Pick the lens that matches the user's question. Don't pre-load all of these; load on demand.

| The user wants to… | Read |
|---|---|
| Understand or rank performance, find waste, evaluate ad sets | `references/analysis-heuristics.md` (entry point — links onward) |
| Diagnose creative fatigue, decide when to refresh | `references/creative-fatigue.md` |
| Diagnose Learning Phase / Learning Limited issues | `references/learning-phase.md` |
| Audit audience overlap, lookalike strategy, broad vs. narrow | `references/audience-strategy.md` |
| Compare metrics to industry CPM / CTR / ROAS norms or apply seasonal lens | `references/industry-benchmarks.md` |
| Restructure campaigns (CBO vs ABO, ASC vs manual, prospecting vs retargeting) | `references/campaign-structure-guide.md` |

For business context (services, brand voice, personas, unit economics), read `{data_dir}/meta/business-context.json` and `{data_dir}/meta/personas/{accountId}.json`. If they're missing or stale (>90 days), suggest `/meta-ads-audit`.

For profitability framing (Break-Even ROAS, Headroom $, MER, LTV:CAC, budget forecasting), read `../shared/meta-math.md`.

## Tool surface

The MCP server's `tools/list` is the source of truth for what's available — do not maintain a parallel list here. The server's instructions route the agent to:

- **Reads / analytics / dashboards** → `runScript` with `ads.graph(path, params)`, `ads.graphParallel([calls])`, `ads.insights(adAccountId?, options?)`, and `ads.batch([requests])`. One call, many Graph API requests in parallel, correlate in-script. Cast a wide net on the first call.
- **Field bundles** → `ads.fields.{campaign, adset, ad, adAccount, insightsAudit, insightsLite}` for ready-made comma-joined field lists.
- **Mutations** → dedicated write tools:
  - **Pause / enable** — `pauseCampaign`, `pauseAdSet`, `pauseAd`, `enableCampaign`, `enableAdSet`, `enableAd`
  - **Budget** — `updateCampaignBudget`, `updateAdSetBudget`
  - **Naming** — `renameCampaign`
- **Server-side recommendations** → `suggestImprovement` returns the server's heuristic take. Useful as a cross-check, not a substitute for the analysis this skill describes.

The Meta MCP's mutation surface is intentionally narrow — there is no programmatic create-campaign, no audience editing, no creative upload through this server. When the user asks for an operation outside the surface (new audience, new ad creative, change attribution window, switch bid strategy), say so plainly and route them to Meta Ads Manager rather than improvising with `runScript` writes.

## Account baseline

Maintain `{data_dir}/meta/account-baseline.json` for anomaly detection across sessions. Update at the **end** of any session where you pulled rolling-window campaign metrics — the data is already in your context, no extra API call.

```json
{
  "metaAccountId": "<from config>",
  "lastUpdated": "<ISO 8601>",
  "campaigns": {
    "<campaignId>": {
      "name": "<campaign name>",
      "objective": "<OUTCOME_SALES | OUTCOME_LEADS | OUTCOME_TRAFFIC | ...>",
      "rolling30d": {
        "avgDailySpend": 0,
        "totalPurchases": 0,
        "purchaseValue": 0,
        "avgCpa": 0,
        "avgRoas": 0,
        "avgCpm": 0,
        "avgLinkCtr": 0,
        "avgFrequency": 0,
        "totalSpend": 0
      },
      "recent7d": {
        "spend": 0,
        "purchases": 0,
        "purchaseValue": 0,
        "cpa": 0,
        "roas": 0,
        "cpm": 0,
        "linkCtr": 0,
        "frequency": 0
      },
      "snapshotDate": "<ISO 8601>",
      "attributionWindow": "7d_click_1d_view"
    }
  }
}
```

Update formula: `rolling30d = (0.7 × previous_rolling30d) + (0.3 × recent7d × (30/7))`. The `(30/7)` factor projects 7-day numbers to a 30-day equivalent. New campaigns: initialize `rolling30d` from `recent7d` directly. Cap at 50 campaigns (spend > $0 in last 30 days only) so the file stays small.

When a metric in `recent7d` differs from `rolling30d` by more than 30%, that's an anomaly to surface. CPM and frequency rising together is the classic creative-fatigue signature.

## Conditional handoffs

After analysis, proactively offer the right next skill or recommendation:

- **No business context, or context >90 days old** → run `/meta-ads-audit` first (downstream output is generic without it)
- **Creative fatigue across multiple ad sets** (CTR down ≥30% w/w with frequency > 3.0) → recommend creative refresh; the right fix is in Ads Manager (creative upload) or in the user's design tool, not here
- **Cold prospecting saturation** (LAL/broad audience at frequency > 3.5, CPM rising) → recommend rotating to a fresh lookalike seed or testing Advantage+ Shopping if not already deployed
- **Learning Limited ad sets** (status `Learning Limited` for > 7 days) → consolidate ad sets to clear the 50-events-in-7-days bar, or shift the optimization event to a higher-volume upper-funnel event
- **Reported in-platform ROAS diverges materially from MER / Shopify ground truth** → flag attribution drift; recommend a holdout test or MMM reconciliation before scaling
