---
name: deep-research
description: Deep multi-round web research with query decomposition, iterative refinement, source triangulation, and structured synthesis. Use when the user asks to research a topic in depth, investigate a complex question, compare multiple options, produce a research report, or needs comprehensive information from multiple sources.
license: MIT
allowed-tools: web_search web_fetch user_message
---

# Deep Research Methodology

You are conducting deep research — not a quick lookup. Your goal is to produce a thorough, well-sourced analysis that the user can trust and act on.

## Phase 1: Decompose the Question

Before searching, break the user's question into 3–6 **sub-questions** that together cover the full scope. Write them out explicitly.

Example — user asks "Should we migrate from REST to GraphQL?":
1. What are the current technical limitations of REST for our use case?
2. What performance and developer-experience benefits does GraphQL offer?
3. What are the known operational costs and pitfalls of GraphQL at scale?
4. What do teams who migrated back from GraphQL report?
5. What is the current industry adoption trend and tooling maturity?

This decomposition guides all subsequent searches.

## Phase 2: Broad Search (Round 1)

For **each sub-question**, run a targeted `web_search` query. Use diverse query formulations:

- **Factual query** — direct question phrased for search engines
- **Authoritative query** — target official docs, research papers, `.gov`, `.edu`, `.org`
- **Contrarian query** — "problems with X", "X criticism", "X vs Y disadvantages"
- **Recent query** — append current year or "2025" / "2026" for fast-moving topics

Request 5 results per query. Track all URLs seen — discard duplicates across queries.

After completing all broad searches, use `user_message` to send the user a brief progress update (e.g., "Completed broad search across 5 sub-questions. Found 18 unique results. Moving to deep dive on top 5 sources.").

## Phase 3: Deep Dive (Round 2)

From Round 1 results, select the **top 3–5 most promising URLs** and fetch their full content with `web_fetch`. Prioritize:

1. Primary sources (official documentation, research papers, data sets)
2. In-depth technical posts with benchmarks or case studies
3. Sources that represent opposing viewpoints

When reading fetched content:
- Extract **specific data points**: numbers, dates, benchmarks, quotes
- Note the **publication date** and **author credentials**
- If a page fails to load or is paywalled, note it and search for an alternative

## Phase 4: Gap Analysis & Iterative Refinement (Round 3+)

After Round 2, review what you have and identify gaps:

- Are any sub-questions still poorly answered?
- Did new information reveal sub-questions you hadn't considered?
- Are there conflicting claims that need a tiebreaker source?

Run additional targeted searches to fill gaps. Repeat until each sub-question has at least 2 independent, credible sources — or you've exhausted reasonable search avenues.

Use `user_message` to update the user on gap analysis progress (e.g., "Gap analysis: 2 sub-questions need more evidence. Running targeted follow-up searches.").

**Stop condition**: You have converging evidence for each sub-question, OR you have clearly identified where evidence is lacking.

## Phase 5: Source Evaluation

Before including any source in your report, assess it:

| Criterion | Strong | Weak |
|---|---|---|
| **Type** | Primary source, peer-reviewed, official docs | Aggregator, opinion blog, anonymous forum |
| **Recency** | Published within 1–2 years (for tech/policy topics) | Older than 3 years on a fast-moving topic |
| **Independence** | No financial stake in the claim | Vendor marketing, sponsored content |
| **Consensus** | 3+ independent sources agree | Single source, no corroboration |
| **Specificity** | Concrete data, benchmarks, examples | Vague claims, no supporting evidence |

Discard sources that score "Weak" on 3+ criteria unless they provide a unique perspective worth noting.

## Phase 6: Synthesize & Report

Structure your final output as:

```
## Summary
[3–5 sentence executive summary answering the user's core question]

## Key Findings

### [Sub-question 1]
- [Finding with specific data and source attribution]
- [Finding with specific data and source attribution]

### [Sub-question 2]
- ...

(repeat for each sub-question)

## Conflicting Information
- [Source A claims X (reason/evidence), while Source B claims Y (reason/evidence)]
- [Your assessment of which is more credible and why]

## Gaps & Limitations
- [What couldn't be reliably determined]
- [Areas where evidence is thin or outdated]

## Confidence Assessment
[High / Medium / Low] — with a 1-sentence justification

## Sources
1. [Title] — [URL] — [Date] — [Used for: which finding]
2. ...
```

## Rules

- **Minimum 3 search rounds** before producing a report (broad → deep → gap-fill)
- **Never cite a source you haven't fetched and read** — search snippets are unreliable
- **Never omit contradictory evidence** — report disagreements honestly
- **Never present a single source as definitive** — triangulate
- **Always distinguish facts from opinions** — "According to [source]..." vs stating as fact
- **Flag uncertainty explicitly** — "Evidence is limited" is more useful than false confidence
- **Cite every claim** — no unsourced assertions in the findings
