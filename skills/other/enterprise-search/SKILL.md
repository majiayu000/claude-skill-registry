---
name: enterprise-search
description: Enterprise search engineering — relevance tuning, query understanding, index management, search quality measurement, ranking optimization, schema design. Use when building search features, debugging relevance, tuning ranking, designing indices, or measuring search quality.
agent: opensearch-elasticsearch-engineer
routing:
  triggers:
    - "enterprise search"
    - "search relevance"
    - "ranking"
    - "inverted index"
    - "query understanding"
    - "BM25"
    - "nDCG"
    - "search quality"
    - "OpenSearch"
    - "Elasticsearch"
    - "vector search"
    - "hybrid search"
    - "Solr"
    - "Vespa"
    - "Typesense"
    - "analyzer chain"
    - "search tuning"
    - "learned ranking"
    - "LTR"
    - "query DSL"
  category: engineering
  force_route: false
  pairs_with: []
user-invocable: true  # justification: user works in enterprise search; direct invocation for domain-specific work
---

# Enterprise Search Engineering

Search infrastructure design, relevance tuning, query understanding, index management, quality measurement, and performance optimization. Each mode loads its own reference files on demand.

---

## Mode Detection

Classify into one mode before proceeding.

| Mode | Signal Phrases | Reference |
|------|---------------|-----------|
| **RELEVANCE** | tune relevance, BM25, boost, function score, field weight, LTR, learned ranking, ranking model | `references/relevance-tuning.md` |
| **QUERY** | query understanding, intent classification, entity extraction, query expansion, synonyms, spell correction, query rewriting | `references/query-understanding.md` |
| **INDEX** | schema design, mapping, analyzer chain, reindex, alias, ILM, index template, field type | `references/index-management.md` |
| **QUALITY** | nDCG, MRR, precision, recall, search quality, judgment, A/B test, evaluation, search funnel | `references/search-quality.md` |
| **PERFORMANCE** | slow query, shard, cache, circuit breaker, scroll, search_after, query optimization, latency | `references/performance-optimization.md` |
| **ARCHITECTURE** | search architecture, hybrid search, vector search, pipeline design, platform selection, migration | (cross-reference: load relevant references based on sub-topic) |

If the request spans modes, pick the primary and note the secondary. ARCHITECTURE mode loads references from whichever sub-topics apply.

---

## Workflow by Mode

### RELEVANCE Mode

**Load**: `references/relevance-tuning.md`, `references/llm-search-failure-modes.md`

1. **Diagnose** — Identify the relevance problem before tuning.

| Problem Class | Symptoms | Starting Point |
|--------------|----------|----------------|
| Poor precision | Good results buried under noise | Field boosting, minimum_should_match |
| Poor recall | Known-good results missing | Analyzer tuning, query expansion, synonym filters |
| Wrong ordering | Right results, wrong rank | BM25 parameter tuning, function scoring |
| Domain mismatch | Generic scoring fails domain | Learned ranking (LTR), custom similarity |
| Freshness | Stale results ranked too high | Decay functions, recency boosts |

2. **Baseline** — Capture current relevance metrics before making changes. Minimum: nDCG@10, P@5, MRR on a representative judgment set. No tuning without a baseline.

3. **Tune** — Apply changes from the reference. One variable at a time. Measure after each change.

| Tuning Layer | Tools | When to Use |
|-------------|-------|-------------|
| Analyzer chain | Tokenizers, filters, char_filters | Recall problems, morphological mismatch |
| Field boosting | Multi-match boosts, cross_fields | Some fields matter more than others |
| BM25 parameters | k1, b per field | Content-type-specific term saturation |
| Function scoring | Decay, field_value_factor, script_score | Non-textual relevance signals (popularity, freshness, authority) |
| Rescoring | rescore query with window_size | Expensive scoring on top-N candidates |
| Learned ranking (LTR) | Feature engineering, model training, SLTR plugin | BM25 + hand-tuned boosts plateau |

4. **Validate** — Compare against baseline. Accept only statistically significant improvements. Check for regression on other query classes.

**Gate**: Baseline metrics captured. Each tuning change measured independently. No "tuned several things and it got better" — isolate the effect.

### QUERY Mode

**Load**: `references/query-understanding.md`, `references/llm-search-failure-modes.md`

1. **Classify query intent** — Determine what the user wants before constructing the query.

| Intent | Example | Query Strategy |
|--------|---------|---------------|
| Navigational | "OpenSearch documentation" | Exact match, title boost, URL matching |
| Informational | "how to configure sharding" | Full-text across body fields, snippet extraction |
| Transactional | "buy enterprise license" | Product/SKU fields, availability filters |
| Faceted | "red shoes size 10" | Structured filters + text scoring |
| Exploratory | "machine learning applications" | Broad match, diversified results, related terms |

2. **Extract entities** — People, products, dates, categories, attributes from the query string.

3. **Transform** — Apply query expansion, spelling correction, synonym injection, and relaxation strategies from the reference.

4. **Construct** — Build the platform-specific query DSL. Include:
   - `bool` query structure (must/should/filter/must_not)
   - Field selection and boosting
   - Filters vs scoring clauses (filters for hard constraints, scoring for ranking signals)
   - Aggregations for facets

5. **Test** — Validate against known queries. Check that transformations improve recall without destroying precision.

**Gate**: Query pipeline handles the 5 intent types. Entity extraction covers the domain vocabulary. Expansion and relaxation strategies are measurable.

### INDEX Mode

**Load**: `references/index-management.md`, `references/llm-search-failure-modes.md`

1. **Requirements** — Gather before designing.

| Question | Why It Matters |
|----------|---------------|
| Document count and growth rate | Shard count, ILM policy |
| Average document size | Shard sizing, bulk indexing batch size |
| Query patterns | Which fields need text analysis vs keyword vs numeric |
| Update frequency | Near-real-time vs batch, refresh interval |
| Retention policy | ILM phases, rollover triggers |
| Access patterns | Hot/warm/cold architecture, read vs write ratio |

2. **Design schema** — Map fields with appropriate types. Use the reference for type selection guidance.

3. **Configure analyzers** — Build analyzer chains for each text field. Standard analyzer is a starting point, not a solution.

4. **Template and alias** — Set up index templates for consistent creation. Use aliases for zero-downtime operations.

5. **Reindex strategy** — Plan for schema evolution. Reindexing is inevitable; design for it.

**Gate**: Schema covers all query-time field requirements. Analyzer chains tested against representative content. Alias strategy supports zero-downtime reindexing.

### QUALITY Mode

**Load**: `references/search-quality.md`, `references/llm-search-failure-modes.md`

1. **Define metrics** — Select metrics appropriate to the use case.

| Metric | Measures | Best For |
|--------|----------|----------|
| nDCG@k | Graded relevance at rank k | Rankings with multiple relevance levels |
| MRR | Position of first relevant result | Navigational queries, single-answer |
| P@k | Fraction relevant in top k | Precision-critical applications |
| Recall@k | Fraction of relevant docs found in top k | Recall-critical applications (legal, compliance) |
| MAP | Average precision across recall levels | Balanced precision/recall |

2. **Collect judgments** — Build the ground truth dataset.

| Method | Scale | Quality | Cost |
|--------|-------|---------|------|
| Expert annotation | Small (100s) | Highest | High |
| Click logs | Large (10K+) | Moderate (position bias) | Low |
| Crowdsourcing | Medium (1K+) | Variable | Medium |
| LLM-assisted | Medium-Large | Good for initial pass, needs validation | Low |

3. **Evaluate** — Run offline evaluation. Compare configurations. Report metrics with confidence intervals.

4. **Online testing** — A/B test or interleave changes against production. Measure engagement metrics alongside relevance metrics.

5. **Monitor** — Continuous quality dashboards. Alerting on metric degradation. Search funnel analysis (query -> click -> conversion).

**Gate**: Judgment set exists with documented guidelines. Offline metrics computed with confidence intervals. Online test plan specifies primary metric, minimum detectable effect, and sample size.

### PERFORMANCE Mode

**Load**: `references/performance-optimization.md`, `references/llm-search-failure-modes.md`

1. **Profile** — Identify the bottleneck before optimizing.

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|------------|
| High p99 latency | Slow queries, GC pauses, shard imbalance | Slow query log, node stats, hot threads |
| Throughput ceiling | Undersized thread pools, too many shards | Thread pool stats, shard count per node |
| Memory pressure | Field data, too many aggregations, deep pagination | Node stats, circuit breaker trips |
| Indexing lag | Merge throttling, refresh overhead, slow pipelines | Index stats, merge stats |
| Cluster instability | Split brain, disk watermarks, master storms | Cluster health, allocation explain |

2. **Diagnose** — Use platform diagnostics to confirm the cause. Measure before changing.

3. **Optimize** — Apply targeted fixes from the reference. One change at a time, measure the effect.

4. **Validate** — Load test the change. Check that optimization does not degrade other metrics (latency vs throughput tradeoff, cache hit rate vs memory).

**Gate**: Bottleneck identified with evidence. Fix targeted at root cause. Load test confirms improvement without regression.

### ARCHITECTURE Mode

Cross-cutting mode. Load references based on the specific question.

1. **Platform evaluation** — When selecting or migrating between platforms.

| Platform | Strengths | Consider When |
|----------|-----------|--------------|
| Elasticsearch/OpenSearch | Mature ecosystem, Lucene-based, strong text search | General-purpose search, log analytics |
| Vespa | Built-in ML serving, tensor computation, real-time updates | ML-heavy ranking, large-scale recommendations |
| Typesense | Simple API, typo tolerance, easy setup | Developer-facing search, smaller datasets |
| Solr | Configurable, NRT, strong faceting | Legacy integration, specific Solr features |
| Meilisearch | Instant search, typo-tolerant, developer-friendly | Frontend search, prototyping |
| Custom (Lucene/Tantivy) | Full control, embedded | Specialized needs, tight integration |

2. **Hybrid search design** — When combining keyword and vector retrieval.

| Strategy | How | Tradeoff |
|----------|-----|----------|
| Score fusion (RRF) | Reciprocal rank fusion of BM25 + vector results | Simple, no training needed. Weights are heuristic. |
| Linear combination | Weighted sum of normalized BM25 + vector scores | Tunable. Requires score normalization. |
| Re-ranking | BM25 retrieval -> vector re-rank top N | Efficient. Vector search only on candidates. |
| Two-stage | Coarse retrieval (either) -> fine-grained re-rank (LTR) | Best quality. Most complex. |

3. **Pipeline design** — Ingestion, enrichment, indexing, query, ranking pipelines.

4. **Migration planning** — Version upgrades, platform changes, zero-downtime strategies.

---

## LLM Failure Modes in Search Engineering

**Load `references/llm-search-failure-modes.md` for all modes.** These are the specific ways LLMs fail at search tasks:

| Failure Mode | What Happens | Defense |
|-------------|-------------|---------|
| Hallucinated query DSL | LLM invents plausible-looking query syntax that does not exist | Validate every query against the specific platform version's API docs |
| Version confusion | Mixing Elasticsearch 7.x and 8.x APIs, or ES and OpenSearch syntax | State the exact platform and version upfront. Reference version-specific docs. |
| Generic relevance advice | "Improve your relevance by boosting important fields" without specifics | Require concrete field names, boost values, and expected metric impact |
| Vector search as default | Recommending embeddings when BM25 with good analyzers solves the problem | Start with BM25 tuning. Vector search adds complexity; justify the added value. |
| Ignoring measurement | Suggesting changes without a quality measurement framework | Require baseline metrics before any tuning recommendation |
| Deprecated feature suggestions | Recommending removed or deprecated APIs (type mappings, indices.optimize) | Check the deprecation/migration guide for the target version |
| Over-engineered schemas | Adding 50 fields with sub-fields when 10 fields cover the queries | Schema complexity should match query requirements, not data model completeness |
| Cargo-cult configuration | Copying cluster settings from blog posts without understanding the workload | Every configuration value should have a justification tied to the specific workload |

---

## Platform-Specific Conventions

When generating configuration or queries, always specify the target platform and version.

| Platform | Query Language | Config Format | Key Differences |
|----------|---------------|--------------|-----------------|
| Elasticsearch 8.x | Query DSL (JSON) | elasticsearch.yml | Security on by default, no type mappings |
| OpenSearch 2.x | Query DSL (JSON) | opensearch.yml | Fork divergence from ES 7.10, alerting built-in |
| Solr 9.x | SolrQL / JSON Request API | solrconfig.xml + schema.xml | Config-driven, ZooKeeper coordination |
| Vespa | YQL | services.xml + schemas | Custom ranking expressions, tensors native |
| Typesense | REST params | Command-line / JSON | Simpler model, automatic typo tolerance |

**Cross-platform traps**:
- OpenSearch `_search` API is largely ES 7.10-compatible, but diverges on security, ML, and alerting APIs
- Elasticsearch `_field_caps` behavior changed between 7.x and 8.x
- Solr `edismax` and ES `multi_match` are similar in concept but differ in syntax, defaults, and tie-breaking
- Vespa ranking expressions are not Lucene scoring — different mental model entirely

---

## Output Conventions

- Markdown with clear headers. Scannable by engineers.
- All query DSL in fenced code blocks with platform and version annotation: ````json // OpenSearch 2.x```
- Tables for parameter comparisons, metric results, configuration options.
- Every recommendation includes: what to change, why, expected effect, how to measure.
- Configuration snippets are copy-pasteable with comments explaining each value.

---

## Reference Loading Table

| Reference | Contents | Load When |
|-----------|----------|-----------|
| `references/relevance-tuning.md` | BM25 parameters, LTR features, boost strategies, function scoring, field weighting | RELEVANCE mode, or relevance sub-questions in other modes |
| `references/query-understanding.md` | Intent classification, entity extraction, query expansion, spell correction, query relaxation | QUERY mode, or query pipeline questions |
| `references/index-management.md` | Schema design, analyzer chains, mapping optimization, reindex strategies, ILM | INDEX mode, or schema/mapping questions |
| `references/search-quality.md` | nDCG, MRR, P@k, judgment collection, A/B testing, evaluation methodology | QUALITY mode, or measurement questions |
| `references/performance-optimization.md` | Query optimization, caching, sharding, pagination, circuit breakers, slow query diagnosis | All modes — always load as guardrail |
| `references/llm-search-failure-modes.md` | How LLMs fail at search tasks: hallucinated DSL, version confusion, generic advice, measurement avoidance | All modes — always load as guardrail |
