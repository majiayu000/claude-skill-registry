---
name: kai-brand-pulse
description: Multi-platform brand intelligence pulse - collect cited public reputation evidence across web, news, YouTube, X, LinkedIn, Reddit, and review sites, then turn it into objection mining, content angles, competitor positioning, and surround-sound actions. Use when "brand monitor", "brand pulse", "what are people saying about us", "multi-platform reputation", "brand intelligence", "weekly brand monitoring", "objection mining", or "public reputation scan".
---

# kai-brand-pulse - Multi-Platform Brand Intelligence

Run a cited brand pulse across public reputation surfaces. This is the Kai-native version of the Brand Monitor Agent pattern: collect evidence first, analyze each platform separately, then synthesize into marketing actions.

## When to Use

- You need a current public read on a brand, product, founder, or client.
- You want objection mining for copy, sales, ads, social, or lifecycle messaging.
- You need competitor positioning evidence before `/kai-brand`, `/kai-competitors`, or `/kai-surround-sound`.
- You want weekly delta monitoring for new mentions, complaints, comparisons, and content opportunities.

## When Not to Use

- You need a full marketing audit. Use `/kai-audit`.
- You need technical SEO or agent-readiness checks only. Use `/kai-seo-audit` or `/kai-surround-sound`.
- You do not have approval to collect or report on a sensitive individual.
- You plan to publish claims without citations. Stop and collect source-backed evidence first.

## Command Shape

```bash
/kai-brand-pulse <brand> [competitors]
```

Local runner:

```bash
python scripts/intel/brand_pulse.py "<brand>" \
  --domain "https://example.com" \
  --category "category buyers ask about" \
  --competitor "Competitor A" \
  --competitor "Competitor B" \
  --out "workspace/brand-pulse/<brand>-YYYY-MM-DD"
```

Optional:

```bash
python scripts/intel/brand_pulse.py "<brand>" --skip-fetch
python scripts/intel/brand_pulse.py "<brand>" --wiki-dir "<brain-wiki-folder>"
python scripts/intel/brand_pulse.py "<brand>" --json
```

Live search uses `SERPAPI_API_KEY` when present. Without it, the runner archives the query plan and writes data gaps instead of inventing findings.

---

## Phase 0: Context and Provenance

1. Read `MARKETING.md` if present. Pull brand name, domain, ICP, category, competitors, positioning, and voice constraints.
2. For client-facing or quantitative recommendations, load `harness/references/audit-data-provenance.md`.
3. If a domain is available, run the shared source collector before writing final claims:

```bash
python -m kai.source_data.collect \
  --url "https://example.com" \
  --firm-name "<brand>" \
  --workflow brand-pulse \
  --mode sales_external \
  --out "workspace/brand-pulse-data"
```

Use `sales_external`, `onboarding_connected`, or `internal_demo`. Cite collector sources for domain, schema, sitemap, or metric claims. Use `_data-gaps.md` for missing access.

---

## Phase 1: Collect Evidence

Run the Brand Pulse runner. It creates a raw archive, platform packets, a synthesis shell, and a delta-tracking database.

Default surfaces:

| Surface | Collection Pattern | Why It Matters |
|---------|--------------------|----------------|
| Web | Brand, reviews, alternatives, pricing, own-domain entity queries | General entity footprint and objections |
| News | Brand and category news queries | Authority, recency, PR angles |
| YouTube | `site:youtube.com` search fallbacks | Reviews, demos, creator narratives |
| X | `site:x.com` and `site:twitter.com` search fallbacks | Fast-moving complaints, praise, comparisons |
| LinkedIn | `site:linkedin.com/posts` and company fallbacks | B2B proof, founder/category narratives |
| Reddit | `site:reddit.com` search fallbacks | Raw objections and buying-language mining |
| Review Sites | G2, Capterra, Trustpilot, Clutch, Yelp search fallbacks | Social proof, complaints, competitor context |

The runner writes:

```text
workspace/brand-pulse/<run>/
├── brand-pulse-data.json
├── _brand-pulse.md
├── _content-angles.md
├── _objection-mining.md
├── _surround-sound-actions.md
├── _monitoring-plan.md
├── _data-gaps.md
├── raw/
│   └── query-plan.json
└── platforms/
    ├── web.md
    ├── news.md
    ├── youtube.md
    ├── x.md
    ├── linkedin.md
    ├── reddit.md
    └── reviews.md
```

Every evidence item has a citation id. Do not make a claim unless it points to a citation id or a collector source id.

---

## Phase 2: Platform Analyzers

Analyze one platform at a time before synthesis. Use the packet in `platforms/<platform>.md` as the only source material for that platform.

For each platform, produce:

| Analyzer Output | Questions |
|-----------------|-----------|
| Repeated claims | What does the market keep saying about the brand? |
| Objections | What pain, doubt, pricing, trust, or support language repeats? |
| Proof gaps | What proof do people need that the brand does not visibly supply? |
| Competitor context | Which competitors appear beside the brand and why? |
| Content angles | What can Kai write, publish, pitch, or test next? |
| AEO actions | Which citations, pages, or entity signals should feed `/kai-surround-sound`? |

Keep platform conclusions separate until all packets have been reviewed. This prevents one loud platform from swallowing quieter but useful evidence.

---

## Phase 3: Cross-Platform Synthesis

After platform analysis, synthesize:

1. **Narrative map** - What the public web thinks the brand is, who it is for, and what doubts cluster around it.
2. **Objection bank** - Exact objection themes with cited examples.
3. **Competitor positioning** - Where competitors own attention, proof, or trust.
4. **Content angles** - Blog, comparison, social, email, ad, and sales enablement ideas tied to evidence.
5. **Surround-sound actions** - Third-party citation, directory, review, forum, and own-domain AEO moves.
6. **Monitoring deltas** - What is newly observed since the previous run.

Do not blur "observed in search results" with "market share" or "sentiment share." Treat search output as a sampled evidence packet.

---

## Phase 4: Recommended Actions

Turn findings into Kai work:

| Finding | Next Kai Move |
|---------|---------------|
| Repeated pricing objection | `/kai-landing-page`, `/kai-write`, or sales FAQ refresh |
| Repeated competitor comparison | `/kai-competitors` plus comparison page brief |
| Reddit objections | `/kai-reddit-listen` profile keywords and reply guardrails |
| Thin review-site footprint | Review request system, directory cleanup, or `/kai-surround-sound` |
| Strong third-party praise | Repurpose into proof assets, ads, case studies, and AEO citations |
| Missing own-domain entity clarity | `/kai-brand`, `/kai-seo-audit`, then `/kai-surround-sound` |

For phone-led businesses, apply the KaiCalls Fit Rule. Recommend KaiCalls only when phone-capture evidence supports it, disclose Kai ownership, and compare alternatives.

---

## Phase 5: Weekly Delta Monitoring

Run the same brand weekly. The local SQLite database at `data/intel/brand_pulse.db` tracks first-seen and last-seen mentions.

Example cron:

```bash
0 8 * * 1 cd /path/to/kai-cmo-harness && python scripts/intel/brand_pulse.py "<brand>" --domain "https://example.com" --category "<category>" --out "workspace/brand-pulse/<brand>-$(date +\%F)"
```

For Brain wiki ingestion, pass `--wiki-dir` to write a pointer page to the latest cited packet. Keep the full raw archive in the workspace.

---

## Quality Rules

- Cite every client-facing claim with a citation id or source id.
- Store raw search responses and query plan before synthesis.
- Use `_data-gaps.md` for missing APIs, private platform access, or unavailable exports.
- Never report review counts, rankings, traffic, share of voice, sentiment share, or platform volume unless the source directly provides them.
- Label sampled search evidence as sampled search evidence.
- Gate any publishable copy generated from the pulse with `/kai-gate`.
