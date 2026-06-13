---
name: news-collection
description: "Collect, filter, and freshness-qualify news items."
user-invocable: false
routing:
  triggers:
    - "news collection"
    - "collect news"
    - "qualify news items"
    - "news triage"
    - "filter news feed"
    - "check news freshness"
  not_for: "general research reports — that is research-pipeline. Pick this when the input is a stream of news items to qualify for a content pipeline."
  pairs_with:
    - fact-check
  complexity: Medium
  category: research
---

# News Collection

Gather news items on a topic, filter junk cheaply, verify freshness, and emit
qualified items under an evidence contract. Pipeline-shaped: four phases, a
gate between each. Content pipelines consume the JSON artifact; pair with
fact-check to verify what this skill qualifies.

## Instructions

### Phase 1: COLLECT

**Goal**: gather candidate items from available sources (feeds, search
results, provided fixtures). Every item carries the five-fact evidence
contract: **title, url, outlet, author, published_at**.

Rule (verbatim from the design): publish times are extracted (article
metadata), never guessed; missing timestamp → recorded as unknown, confidence
lowered and disclosed. A guessed timestamp poisons every downstream freshness
verdict; an honest `"published_at": null` keeps the item usable with known
uncertainty.

Record each item as one JSON object per the schema in
`references/evidence-contract.md`. Fill `evidence_notes` with where each fact
came from (meta tag, byline, JSON-LD, sitemap).

Distinguish outcomes: zero items because sources were unreachable is a
collection failure (report it, stop); zero items from reachable sources is a
valid empty feed (deliver an empty artifact with counts of zero).

Gate: every collected item has all five fields present — value or explicit
`null` with a `confidence` downgrade and a disclosure note. Items with silent
gaps stay in COLLECT until the gap is recorded.

### Phase 2: COARSE FILTER

**Goal**: cheap, high-recall pass over collected items. Three verdicts:
`keep` / `monitor_only` / `reject`, each with a reason code from
`references/coarse-filter.md`.

Rule (verbatim from the design): high-magnitude stories are downgraded to
monitor_only at most, never rejected — a false keep is cheap, a silent drop is
expensive. A keep costs one extra freshness check; a wrongly dropped major
story costs the whole pipeline its value.

This phase runs on a cheap model when dispatched — it needs recall, not
judgment depth. See the dispatch note in `references/coarse-filter.md`.

Gate: every item has exactly one verdict and one reason code. `reject`
verdicts on items that look high-magnitude get re-checked once before the
phase closes.

### Phase 3: FRESHNESS CHECK

**Goal**: for each `keep` and `monitor_only` item, establish when the story
first became public and whether this page is the original coverage. Methods in
`references/freshness-forensics.md`:

- First-public time vs page date — a page can carry today's date on old news.
- Syndication and aggregator reposts detected; select the canonical coverage.
- Same-story vs new-development rubric — consolidate duplicates, keep genuine
  developments.

Rule (verbatim from the design): two independent sources or verdict "unclear".
Conservative default: unclear over guessed. An "unclear" verdict is
recoverable downstream; a confidently wrong "fresh" verdict ships stale news.

Gate: every surviving item carries `freshness: fresh | stale | unclear`, a
`first_public_estimate` (or `null`), and the count of sources backing the
verdict. Duplicate clusters are consolidated to one canonical item with
`duplicates_of` links.

### Phase 4: DELIVER

**Goal**: emit qualified items as a structured JSON artifact (schema:
`references/evidence-contract.md`) plus a summary table. Every verdict state
appears in the artifact — `monitor_only`, `unclear`, and `reject` items ship
with their verdicts rather than vanishing, so consumers see the full triage.

Gate (deterministic phase checkpoint — emit this table before delivering the
artifact; delivery without it is incomplete):

| Verdict | Count |
|---------|-------|
| keep | n |
| monitor_only | n |
| reject | n |
| unclear (freshness) | n |
| duplicates consolidated | n |

The counts make silent drops visible: collected total must equal
keep + monitor_only + reject. If it does not, return to the phase that lost
items.

## Error Handling

**No items collected**
- Cause: sources unreachable, or feed genuinely empty.
- Solution: unreachable sources → report collection failure and stop;
  reachable but empty → deliver an empty artifact with zero counts. The two
  outcomes stay distinct so an outage is not read as a quiet news day.

**No timestamp found anywhere for an item**
- Cause: page has no metadata, byline date, or sitemap entry.
- Solution: set `published_at: null`, `confidence: low`, disclose in
  `evidence_notes`; freshness verdict for that item is `unclear`.

**Two sources disagree on first-public time**
- Cause: syndication chain or republished update.
- Solution: apply canonical-coverage selection
  (`references/freshness-forensics.md`); if still split, verdict `unclear`.

**Item count mismatch at DELIVER**
- Cause: an item was dropped without a verdict.
- Solution: diff item ids against the COLLECT record; assign the missing item
  a verdict with reason code.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Recording items, JSON artifact schema, confidence fields | `evidence-contract.md` | Five-fact contract and artifact schema |
| Assigning verdicts, reason codes, cheap-model dispatch | `coarse-filter.md` | Verdict definitions and dispatch note |
| Dating a story, syndication, duplicates, canonical pick | `freshness-forensics.md` | Forensic methods and rubrics |
