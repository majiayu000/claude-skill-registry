---
name: research-arxiv-scout
description: "Discovers and triages recent arXiv papers for AI/ML, agents, and software/QA. Use when scouting categories, arXiv IDs, or source lists."
compatibility: Portable core. arXiv API attribution required in any output that uses arXiv data.
version: "1.1"
last_validated: 2026-07-11
---

# research-arxiv-scout

Use arXiv as a discovery layer for recent research, then produce repo-friendly outputs (ranked recommendations and `02_sources-*.json`-style entries) without fabricating metrics.

## Required attribution (arXiv API terms of use)

Include the following line in any output that uses arXiv data:

Thank you to arXiv for use of its open access interoperability.

Source: this exact sentence is arXiv's requested attribution statement, published on the **arXiv API Documentation** page (`info.arxiv.org/help/api/index.html`, linked from `data/sources.json`) — not on the Terms of Use page (`tou.html`), which covers rate limits and permitted use but does not itself contain an attribution clause. Checked 2026-07-11.

## Quick Reference

| Task | Inputs | Deliverable | Use these files |
| --- | --- | --- | --- |
| Scout for a known skill | Skill name | Ranked list + actions | `config.yaml`, `assets/recommendation-output-template.md` |
| Scout for a topic | Topic + categories | Ranked list + actions | `references/category-taxonomy.md` |
| Summarize one paper | arXiv ID | Single-paper summary | `references/arxiv-api-guide.md` |
| Propose sources updates | Target path | `02_sources-*.json` entries | `assets/sources-json-template.md` |
| Mine HCI/CSCW retention papers (killer-feature bundle handoff) | Commercial product / candidate feature_id | Rows on shared bundle ledger | `references/product-retention-categories.md`, `config.yaml` key `killer-feature-retention` |

## Workflow

### ASCII Flow

```text
arXiv scout request
  -> Map target to arXiv categories and keywords
  -> Query arXiv metadata with date-aware parameters
  -> Triage candidates for relevance, practicality, and evidence
  -> Verify abstract URLs, IDs, titles, authors, and any code links
  -> Produce ranked recommendations or sources-json entries
  -> Include required arXiv attribution and final checklist
```

### 1) Map target to categories and keywords

- If the target matches a key in `config.yaml`, use its categories, keywords, and time window.
- Otherwise, pick 1-4 arXiv categories and 3-8 keywords using `references/category-taxonomy.md`.

### 2) Query arXiv (metadata only)

- Use `references/arxiv-api-guide.md` to build queries for `export.arxiv.org/api/query`.
- Prefer `sortBy=submittedDate` and `sortOrder=descending` when scouting recent work.
- Start with `max_results=50`; paginate if needed.

Minimal query skeleton:

```text
search_query=cat:cs.AI AND (agents OR "tool use")
sortBy=submittedDate&sortOrder=descending&start=0&max_results=50
```

### 2b) Pre-triage: social-signal cross-reference

Before scoring API results, cross-reference candidate arXiv IDs against:

- **HF Papers** (`huggingface.co/papers`) — daily community highlights and upvotes.
- **alphaXiv** (`alphaxiv.org`) — social layer on arXiv with comments and trending signals.

Flag any paper that appears on either platform — community attention is a fast quality gate that reduces triage effort. Also check each candidate's abstract for a GitHub or project-page link; verified code links upgrade the Practicality score (low implementation lift).

### 3) Triage and score

For each candidate paper, extract:

- Title, authors, arXiv ID, submitted date, categories
- Abstract-based relevance to the target
- Implementation signals (only if verified): code repository, dataset, benchmark, reproducibility notes

Do not include citation counts, GitHub stars, conference acceptance, or affiliations unless you can verify them.

**Signal-vs-noise judgment calls (apply before scoring):**

- **Versioned re-announcements.** A paper with `v2`/`v3` in its history and an `updated` date inside your window but a `published` (first-submission) date months or years older is a *revision*, not new work — see `references/arxiv-api-guide.md#version-deduplication`. Sorting by `lastUpdatedDate` will surface these; always cross-check `published` before treating a hit as fresh.
- **Citation-count traps on fresh papers.** Even where citation counts are verifiable (Semantic Scholar/OpenAlex), a paper submitted in the last 1-3 months will have a near-zero count almost regardless of quality — citation lag, not merit, dominates at that age. Do not use "0 citations" as a negative signal on anything younger than ~6 months, and do not present a low count as meaningful evidence either way; state the paper's age instead.
- **Preprint vs. peer-reviewed.** arXiv is a preprint server: most results are *not yet peer-reviewed*, and some are rejected-and-resubmitted or duplicate-with-different-framing work. Absent a verified acceptance note (author's own "accepted at ..." line, checked against the actual venue), treat every candidate as unreviewed and say so in the report — do not imply venue prestige you have not confirmed.
- **Hype-paper tells.** Down-weight (do not auto-reject, but flag) candidates that combine: (a) marketing-register title/abstract language ("revolutionary", "unprecedented", state-of-the-art claims with no named baseline), (b) benchmarks limited to the authors' own curated dataset with no third-party eval, and (c) heavy same-day cross-posting to HF Papers / alphaXiv / X with upvote counts but no substantive technical discussion in the comments. Community attention (step 2b) is a *volume* signal, not a *quality* signal — read the abstract and, where available, the actual discussion thread before letting upvotes raise a score.
- **Author/lab self-citation and PR-driven timing.** A paper timed to a product launch or funding announcement from the same lab is not disqualifying, but note the coincidence in "Limits/risks" rather than silently treating it as independent validation.

Suggested scoring (0-10):

| Dimension | 0-3 | 4-7 | 8-10 |
| --- | --- | --- | --- |
| Relevance | Weak match | Partial match | Direct match |
| Practicality | High lift | Moderate lift | Low lift |
| Evidence | Unclear | Some evaluation | Clear evaluation |

### 4) Produce deliverables

- Recommendation report: use `assets/recommendation-output-template.md`
- `02_sources-*.json` entries: use `assets/sources-json-template.md`

### 5) Final checks (before handoff)

- [ ] Attribution line included (above)
- [ ] Time window stated (and matches what you searched)
- [ ] Categories and keywords listed (or referenced via `config.yaml`)
- [ ] All URLs point to abstract pages (`https://arxiv.org/abs/...`)
- [ ] arXiv IDs are exact (no typos, correct year/format)
- [ ] No duplicates in the final shortlist
- [ ] Paper titles/authors match the abstract page
- [ ] Any code links included were verified
- [ ] Any datasets/benchmarks referenced were verified
- [ ] Any conference/venue claims were verified (or omitted)
- [ ] Any impact metrics (citations/stars) were verified (or omitted)
- [ ] No unverified metrics or claims
- [ ] Suggested actions are concrete and repo-specific
- [ ] Target `02_sources-*.json` schema preserved (no reshaping)

## Killer-Feature Mode (HCI Retention Papers)

Specialized mode that contributes the **`hci_retention_paper`** signal to the bundle's [Killer-Feature Convergence Protocol](../startup-review-mining/references/killer-feature-convergence.md) owned by `startup-review-mining`.

**Premise.** HCI/CSCW/UIST work periodically publishes long-term studies that empirically tie a specific feature or interaction pattern to retention, freemium conversion, or willingness-to-pay. arXiv's `cs.HC` (plus `cs.CY`, `cs.SI`, `cs.IR`) indexes most of this work — though only ~50-70% of CHI/CSCW is on arXiv, so the ACM-only fraction stays with `research-scout`'s conference query generator.

**When to use:** bundle handoff from `startup-review-mining` Killer-Feature Mode KF3 asks for the HCI signal; OR you have a candidate `feature_id` and want a rigorous attribution study.

**Workflow delta:**

```text
KF-ARX-1. Map target to the config.yaml key `killer-feature-retention`
          (categories: cs.HC, cs.CY, cs.SI, cs.IR;
           keywords: long-term retention, feature adoption, freemium conversion, ...)
KF-ARX-2. Query arXiv per templates in references/product-retention-categories.md
KF-ARX-3. Triage with the standard 0-10 dimensions PLUS the
          "Attribution rigor" dimension defined in that reference
KF-ARX-4. Only papers with rigor>=7 graduate to a row on
          ../startup-review-mining/assets/pay-trigger-ledger.tsv
          (signal_type=hci_retention_paper; wtp_strength=strong if causal,
           implicit if correlational only)
KF-ARX-5. Run ../startup-review-mining/scripts/converge_killer_features.py
```

Expect 0-2 strong rows per scan — sparse but high credibility per hit. Zero rows is normal and does not downgrade other signals in the Convergence Rule.

**References:**
- [references/product-retention-categories.md](references/product-retention-categories.md) — categories, keyword groups, query templates, attribution-rigor scoring, anti-patterns
- [../startup-review-mining/references/killer-feature-convergence.md](../startup-review-mining/references/killer-feature-convergence.md) — bundle Convergence Rule
- [config.yaml](config.yaml) — `killer-feature-retention` key

## Navigation

Resources:

- [data/sources.json](data/sources.json) — Official arXiv sources and complementary discovery tools
- [references/arxiv-api-guide.md](references/arxiv-api-guide.md) — API query patterns for `export.arxiv.org/api/query`
- [references/category-taxonomy.md](references/category-taxonomy.md) — Category selection and examples
- [references/product-retention-categories.md](references/product-retention-categories.md) — Killer-feature mode (HCI retention papers) categories + scoring
- [config.yaml](config.yaml) — Project mappings (skill → categories/keywords/time windows)
- [assets/recommendation-output-template.md](assets/recommendation-output-template.md) — Recommendation report template
- [assets/sources-json-template.md](assets/sources-json-template.md) — `02_sources-*.json` entry template

Related skills:

- [`../research-scout/SKILL.md`](../research-scout/SKILL.md) — multi-source research idea mining (arXiv + HF Papers + Semantic Scholar + Papers with Code + conferences + industry blogs + curator newsletters). Use it when you want cross-source corroboration; use this skill when arXiv depth and category taxonomy are the priority.
- [`../research-git/SKILL.md`](../research-git/SKILL.md) — git-history research for repo-internal evidence.

## Fact-Checking

- Verify all arXiv IDs and abstract URLs (`https://arxiv.org/abs/<id>`) before output. Hallucinated IDs are the most common failure mode.
- Do not fabricate citation counts, GitHub stars, conference acceptance, or affiliations. Omit if not directly verified on the source page.
- Code links must be checked against the abstract page or repository, not assumed from the title.
- arXiv's API Documentation page asks every API consumer to include the attribution line "Thank you to arXiv for use of its open access interoperability." in any output that uses arXiv data (see "Required attribution" above for the precise source).
- For runtime-specific or volatile claims (dataset size, benchmark numbers, version-specific footguns), label them with the date pulled and prefer primary sources.
- If web access is unavailable, mark all paper-specific claims as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
