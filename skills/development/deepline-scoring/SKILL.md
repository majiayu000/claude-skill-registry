---
name: deepline-scoring
disable-model-invocation: false
description: 'Use when discovering niche signals, auditing ICP or won/lost evidence, rescoring accounts, or building account and lead scoring Plays. Triggers on fit scoring, engagement scoring, external proxies, and scoring leakage. Skip pure outreach copy or contributor skill installation tasks.'
---

# Deepline Scoring

## Quick Start

```bash
npm install -g deepline
# Fallback for secure sandboxes: mkdir -p "$HOME/.local" && npm config set prefix "$HOME/.local" && export PATH="$HOME/.local/bin:$PATH" && npm install -g deepline --registry https://code.deepline.com/api/v2/npm/
deepline auth register --wait auto
deepline auth wait --timeout 120 # completes Cowork/browser approval; no-op if already connected
deepline auth status
deepline -h
```

Find evidence for the customer's decision. Use approved rules or a separately evaluated model for scoring. Phrase matches and prevalence ratios alone cannot supply scoring weights.

| Task                            | Read                                                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Find phrases and buyer language | [Keyword catalog](references/keyword-catalog.md), [buyer-language research](references/buyer-language-research.md) |
| Build or audit a score          | [Scoring delivery](references/scoring-delivery.md)                                                                 |
| Test rules or evaluate outcomes | [Testing and evaluation](references/testing-and-evaluation.md)                                                     |
| Create an artifact-backed scorecard | [Scorecard creation pattern](references/scorecard-creation.md) |
| Debug disputed features or routing | [Scoring diagnostics](references/scoring-diagnostics.md) |
| Verify technology               | [Technology evidence](references/technology-evidence.md)                                                           |
| Estimate staffing or demand     | [Capacity evidence](references/capacity-evidence.md)                                                               |

Read `deepline-gtm` before collection and `deepline-plays` before authoring. Verify the workspace, current provider schema and price. Pilot one or two rows and pass the [quality gate](references/quality-gate.md) on the generated outputs before scaling within the approved budget. Keep exports and receipts in a persistent project directory. Reuse collected evidence when rescoring.

## Workflow

1. Define the product, decision date, prediction horizon, population, analysis unit and requested outputs. Before paid collection, identify the executable model and independent expected scores for parity, or historical evidence and untouched labels for predictive evaluation. Missing prerequisites leave that test blocked; an authorized research run can still proceed. Keep fit, engagement, capacity and coverage separate. Use only requested dimensions: `account_fit`, `account_engagement`, `lead_fit`, `lead_engagement`. A combined priority policy must preserve its components.
2. Resolve identities, parent groups and conflicting outcomes. Split discovery and validation by time and parent before selecting features. Preserve the full requested population. Open accounts and random alternatives have unknown outcomes; lookalikes are not wins. Separate acquisition, renewal and expansion.
3. Research workflows, problems, roles, systems and counterexamples across relevant public sources. Follow observed buyer phrases and source URLs. Mine discovery documents without labels, then review concepts and aliases against their evidence. Keep rare and inconclusive candidates. Exclude report prose and outcome summaries from the corpus.
4. Check collection with the [quality gate](references/quality-gate.md). Report coverage by source and outcome before citing lift. Compare a coverage-only model and evaluate features where both outcomes have adequate observed data. Imputation or dropping missingness flags can still encode collection bias. Keep failed, partial and empty results distinct.
5. Check what each feature measures. Reviews are not calls, openings are not hires, and software mentions or portal links do not prove installation. Keep Google reviews, Yelp, traffic estimates and sitemap counts separate. Validate proxies against actual measurements. Exclude AE discovery, opportunity and outcome fields from pre-contact fit. Require evidence that every input was available at the decision date; current enrichment cannot validate past predictions.
6. Freeze extraction rules, aliases, model and reference artifacts before validation. Fit selection, imputation and tuning within training folds. Follow [scoring pitfalls](references/scoring-pitfalls.md) and [signal interpretation](references/signal-interpretation.md). Record every attempted model and failed comparison. Reusing a holdout to refine rules consumes it.
7. For scoring, deliver a checked Play that resolves the identifier, enriches the row and returns the requested outputs. Follow [scoring delivery](references/scoring-delivery.md) and finish with [testing and evaluation](references/testing-and-evaluation.md). Prove existing-output parity separately from predictive usefulness. Keep missing rows unscored with reasons. A cached replay is partial delivery for a live-enrichment request.
8. Deliver one readable report per workspace using the [report template](references/report-template.md). Combine targeting findings, ranked accounts, scoring rules, the runnable Play and evaluation results in that report; link complete tables and raw evidence at the end. Name the supported state: `research_only`, `replay_only`, `exploratory_end_to_end` or `validated_for_named_use_case`. Promotion requires untouched evaluation against the existing rules and a simple baseline, uncertainty estimates and a stated business acceptance threshold. Selected wins or percentile quotas cannot establish usefulness.

## Inputs and commands

CSV columns: `domain,status,website,jobs`; optional `account_id,parent_id,split,known_at,scored_at`. Status: `won|lost|lookalike|unlabeled`. Merge repeated observations while retaining their sources. Resolve conflicting labels through an explicit cohort rule; never discard every duplicate domain.

Use the opt-in `*_v2.py` helpers for new work. Unversioned scripts retain their existing interfaces. Update consumers explicitly before switching versions.

```bash
python3 scripts/analyze_signals_v2.py --input accounts.csv --discover-phrases \
  --max-phrases 500 --min-phrase-accounts 2 --output candidates.json

python3 scripts/analyze_signals_v2.py --input accounts.csv \
  --keywords keywords.json --tools tools.json --job-roles roles.json \
  --partition discovery --evidence-limit 12 --output discovery.json
```

The miner uses 2–5-word n-grams from discovery accounts, with source and phrase-length diversity. It ignores labels and validation documents. It does not understand negation or generate synonyms. Review matches, nonmatches, buyer/seller context and wrong-company text. Use `--min-phrase-accounts 1` for a labeled rare-phrase pass. Report truncation and increase the cap when needed.

Configs map categories to lists of strings or `{"name":"concept","aliases":["phrase","explicit stem*"]}`. Strings match exact phrase boundaries. Roles match job titles; use keyword concepts for duties.

Validation requires `--partition validation --manifest frozen.json`. The manifest contains `analyzer_sha256`, timezone-aware `frozen_at`, and `config_sha256` hashes for `keywords,tools,job_roles`. Freeze before scoring. Each row requires `known_at <= scored_at`, with `known_at` reflecting the latest availability of all included sources. The script cannot verify timestamp provenance. Scoring before contact uses the stricter cutoff in the delivery contract.

V2 returns `signals[]`, `statistics`, `method`, `config_sha256` and `scoring_eligible:false`. Its metric is Jeffreys-smoothed P(feature|won)/P(feature|lost), not win-rate lift. Wilson intervals describe prevalence; Fisher p-values and BH/BY q-values cover the configured tests in that invocation. They assume independent accounts and do not correct for parent clustering, selection bias or undisclosed repeated experiments. Outputs remain exploratory, including validation-partition runs.

## Source adapters

- Websites: `{"data":{"results":[{"url":"...","title":"...","text":"..."}]}}`, `pages`, direct text/markdown records and known `toolResponse.rawV2/raw` wrappers.
- Jobs: `{"result":{"listings":[{"title":"...","description":"...","url":"..."}]}}`, `jobs[].job_details`, `job_listings` and JSON:API `data[].attributes`.
- Preserve source IDs and dates. Add a fixture and adapter for each new shape. Unsupported or malformed payloads fail.
- An empty jobs array means no returned records for that query; retain its filters and limits. An empty website scrape means unknown coverage. Neither establishes staffing, current vacancies or business-trait absence.
- Named `website/jobs` headers auto-detect. Legacy positional columns require explicit indices. Duplicate headers, invalid labels and unresolved mixed outcomes fail.

## Verification

Follow [testing and evaluation](references/testing-and-evaluation.md) for the acceptance contract. The executable evaluation suite is delivered separately from this skill change. Keep implementation replay, live enrichment and predictive validation distinct, and report missing prerequisites.

Keep customer rules, cases and receipts outside published skills. Treat [proven signals](references/proven-signals.md) as hypotheses. For optional contacts, use the current GTM workflow and [dedupe](references/dedupe.md)/[prospecting](references/step-7-prospects.md) guidance; the local contact helper only exports a shortlist. Do not infer names from LinkedIn slugs or treat domain matching as email verification.
