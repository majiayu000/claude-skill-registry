---
name: promql-generator
depth: full
description: >-
    Generates PromQL queries with RED/USE/SLO patterns, native histograms, recording rules, and alerting expressions. Use when creating new queries from requirements; excludes validation (use promql-validator).
---

# [H1][PROMQL-GENERATOR]
>**Dictum:** *Query generation follows metric type, then pattern, then optimization.*

<br>

Generate PromQL for Prometheus 3.8-3.10 (native histograms stable, feature flag no-op since 3.9). Cross-references: **promql-validator** for validation, **observability-stack** for deployment.

**Tasks:**
1. Gather goal, use case, metric context via **AskUserQuestion** (skip if provided).
2. Identify metric names, types, labels -- confirm with user.
3. Read relevant reference: `references/promql_functions.md`, `references/promql_patterns.md`, `references/best_practices.md`.
4. Present plain-English plan; confirm via **AskUserQuestion**.
5. Generate query citing applicable pattern.
6. Invoke **promql-validator** skill; fix and re-validate until all checks pass.
7. Deliver: final query + explanation + usage context + customization notes.

---
## [1][METRIC_IDENTIFICATION]
>**Dictum:** *Metric type determines function selection.*

<br>

| [INDEX] | [SUFFIX]                        | [TYPE]             | [FUNCTIONS]                                                  |
| :-----: | ------------------------------- | ------------------ | ------------------------------------------------------------ |
|   [1]   | **`_total`**                    | Counter.           | `rate()`, `irate()`, `increase()`.                           |
|   [2]   | **`_bucket`, `_sum`, `_count`** | Classic Histogram. | `histogram_quantile()`, `rate()`.                            |
|   [3]   | **(none, opaque)**              | Native Histogram.  | `histogram_quantile/count/sum/avg/fraction/stddev/stdvar()`. |
|   [4]   | **(unit suffix)**               | Gauge.             | direct, `*_over_time()`.                                     |

**Guidance:**
- Range >= 4x scrape interval. Label filters: exact `=`, negative `!=`, regex `=~`.
- Aggregation: `sum by (labels)` to keep, `sum without (labels)` to drop.
- Native histograms eliminate `le` label and `_bucket` suffix -- single opaque series per histogram.

---
## [2][VERSION_MATRIX]
>**Dictum:** *Version awareness prevents deprecated patterns.*

<br>

| [INDEX] | [VERSION]   | [RELEASE] | [KEY_CHANGES]                                                                    |
| :-----: | ----------- | --------- | -------------------------------------------------------------------------------- |
|   [1]   | **3.0**     | Nov 2024  | UTF-8 names, `holt_winters` renamed to `double_exponential_smoothing`, `info()`. |
|   [2]   | **3.5 LTS** | Jul 2025  | `mad_over_time`, `ts_of_min/max/last_over_time`, `sort_by_label` (experimental). |
|   [3]   | **3.6**     | Sep 2025  | `step()`, duration expressions (`promql-duration-expr` flag).                    |
|   [4]   | **3.7**     | Oct 2025  | `first_over_time`, anchored+smoothed rate (`promql-extended-range-selectors`).   |
|   [5]   | **3.8**     | Nov 2025  | Native histograms **stable** (`scrape_native_histograms` config).                |
|   [6]   | **3.9**     | Jan 2026  | `native-histogram` flag is **no-op**; `/api/v1/features` endpoint.               |
|   [7]   | **3.10**    | Feb 2026  | Maintenance release; stability fixes only.                                       |

**Guidance:**
- Activate native histograms: `scrape_native_histograms: true` in scrape config (not a feature flag).
- Three experimental gates remain: `promql-experimental-functions`, `promql-duration-expr`, `promql-extended-range-selectors`.

---
## [3][NATIVE_HISTOGRAMS]
>**Dictum:** *Native histograms replace classic for all new instrumentation.*

<br>

No `_bucket` suffix or `le` label. Reduces series cardinality 10-100x. NHCB (3.4+): classic-to-native conversion via `convert_classic_histograms_to_nhcb: true`.

| [INDEX] | [FUNCTION]                                        | [PURPOSE]                     |
| :-----: | ------------------------------------------------- | ----------------------------- |
|   [1]   | **`histogram_quantile(phi, v)`**                  | Percentile (no `le` needed).  |
|   [2]   | **`histogram_avg(v)`**                            | Average (replaces sum/count). |
|   [3]   | **`histogram_fraction(lo, hi, v)`**               | Fraction between bounds.      |
|   [4]   | **`histogram_stddev(v)` / `histogram_stdvar(v)`** | Estimated stddev / variance.  |
|   [5]   | **`histogram_count(v)` / `histogram_sum(v)`**     | Observation count / sum.      |

```promql
# Classic: histogram_quantile(0.95, sum by (job, le) (rate(metric_bucket[5m])))
# Native:  histogram_quantile(0.95, sum by (job) (rate(metric[5m])))
```

**Best-Practices:**
- Prefer `histogram_avg()` over manual `_sum/_count` division -- single function, single series.
- Use `histogram_fraction(0, 0.2, rate(m[5m]))` for latency SLOs -- precise without bucket interpolation.
- `rate()`, `increase()`, `delta()` on native histograms produce gauge histograms (3.9+).

---
## [4][EXPERIMENTAL_FUNCTIONS]
>**Dictum:** *Experimental functions expand analysis under explicit feature flags.*

<br>

| [INDEX] | [FUNCTION]                                     | [FLAG]                          | [SINCE] | [PURPOSE]                               |
| :-----: | ---------------------------------------------- | ------------------------------- | ------- | --------------------------------------- |
|   [1]   | **`info(v [, selector])`**                     | `promql-experimental-functions` | 3.0+    | Automatic metadata enrichment.          |
|   [2]   | **`double_exponential_smoothing(v[r],sf,tf)`** | `promql-experimental-functions` | 3.0+    | Smoothed gauge (replaced holt_winters). |
|   [3]   | **`mad_over_time(v[r])`**                      | `promql-experimental-functions` | 3.5+    | MAD-based anomaly detection.            |
|   [4]   | **`first_over_time(v[r])`**                    | `promql-experimental-functions` | 3.7+    | First (oldest) value in range.          |
|   [5]   | **`limitk(k,v)` / `limit_ratio(r,v)`**         | `promql-experimental-functions` | 3.0+    | Deterministic series sampling.          |
|   [6]   | **`step()`**                                   | `promql-duration-expr`          | 3.6+    | Current evaluation step size.           |

**Guidance:**
- `info()` replaces manual `* on (...) group_left (...)` for metadata joins.
- `mad_over_time` enables z-score anomaly detection: `m > avg_over_time(m[1h]) + 3 * mad_over_time(m[1h])`.
- `limitk`/`limit_ratio` use deterministic hash-based sampling -- same series across evaluations.

---
## [5][LOOKUP_STRATEGY]
>**Dictum:** *Lookup strategy prioritizes authoritative sources.*

<br>

**context7 MCP** (preferred): resolve "prometheus" -> get-library-docs with topic.
**WebSearch** fallback: `"Prometheus PromQL [topic] documentation examples"`.

---
## [6][RESOURCES]
>**Dictum:** *Reference files provide detailed function, pattern, and optimization guidance.*

<br>

| [INDEX] | [FILE]                               | [WHEN_TO_READ]                                         |
| :-----: | ------------------------------------ | ------------------------------------------------------ |
|   [1]   | **`references/promql_functions.md`** | Function behavior, metric types, decision tree.        |
|   [2]   | **`references/promql_patterns.md`**  | RED/USE/SLO/alerting/join/efficiency patterns.         |
|   [3]   | **`references/best_practices.md`**   | Optimization, anti-patterns, pre-deploy checklist.     |
|   [4]   | **`examples/alerting_rules.yaml`**   | Production alerting rule templates.                    |
|   [5]   | **`examples/recording_rules.yaml`**  | Pre-computed metric rule templates (classic + native). |
