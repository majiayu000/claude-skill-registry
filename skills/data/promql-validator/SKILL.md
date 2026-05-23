---
name: promql-validator
depth: extended
description: >-
    Validates existing PromQL query syntax, detects anti-patterns, checks best practices, and optimizes performance. Use when validating/auditing/reviewing queries, NOT creating new ones (use promql-generator instead).
---

# [H1][PROMQL_VALIDATOR]
>**Dictum:** *Validation catches errors that generation misses.*

<br>

Validate PromQL for Prometheus 3.8-3.10 (native histograms stable, feature flag no-op since 3.9). Cross-references: **promql-generator** for query creation, **observability-stack** for alert rule deployment.

**Tasks:**
1. **Syntax**: `python3 .claude/skills/promql-validator/scripts/validate_syntax.py validate "<query>"`.
2. **Best Practices**: `python3 .claude/skills/promql-validator/scripts/check_best_practices.py check "<query>"`.
3. **Explain**: Parse and describe -- metrics, types, functions, output labels, result structure.
4. **Clarify Intent (STOP AND WAIT)**: Ask user -- goal, metric type, time window, aggregation, use case.
5. **Compare**: Highlight mismatches between intent and implementation.
6. **Optimize**: Suggest recording rules, better matchers, appropriate ranges.
7. **Refine**: Offer alternatives, explain trade-offs, iterate.

---
## [1][VERSION_MATRIX]
>**Dictum:** *Version awareness prevents false positives.*

<br>

| [INDEX] | [VERSION]   | [KEY_CHANGES]                                                                     |
| :-----: | ----------- | --------------------------------------------------------------------------------- |
|   [1]   | **3.0**     | UTF-8 `{"my.metric"}`, `info()` experimental, `holt_winters` renamed.             |
|   [2]   | **3.5 LTS** | `mad_over_time`, `ts_of_min/max/last_over_time` experimental.                     |
|   [3]   | **3.6**     | `step()`, duration expressions (`promql-duration-expr` flag).                     |
|   [4]   | **3.7**     | `first_over_time`, anchored+smoothed rate.                                        |
|   [5]   | **3.8**     | Native histograms **stable** (`scrape_native_histograms: true` in scrape config). |
|   [6]   | **3.9**     | Native histogram flag is **no-op**; `/api/v1/features` endpoint.                  |
|   [7]   | **3.10**    | Maintenance release (Feb 2026); stability fixes only.                             |

---
## [2][VALIDATION_RULES]
>**Dictum:** *Rules detect errors before Prometheus does.*

<br>

| [INDEX] | [CATEGORY]   | [RULE]                                                                   | [SEVERITY] |
| :-----: | ------------ | ------------------------------------------------------------------------ | ---------- |
|   [1]   | **Syntax**   | Metric names: `[a-zA-Z_:][a-zA-Z0-9_:]*` or UTF-8 `{"metric"}`.          | error.     |
|   [2]   | **Syntax**   | Label matchers: `=`, `!=`, `=~`, `!~` only.                              | error.     |
|   [3]   | **Syntax**   | Durations: `[0-9]+(ms\|s\|m\|h\|d\|w\|y)`.                               | error.     |
|   [4]   | **Semantic** | `rate()`/`irate()` only on counters (`_total`, `_count`, `_bucket`).     | warning.   |
|   [5]   | **Semantic** | Never `rate()` on gauges -- use `avg_over_time()` or direct.             | warning.   |
|   [6]   | **Semantic** | `histogram_quantile()` needs `rate()` on `_bucket` + `le` in `by()`.     | warning.   |
|   [7]   | **Semantic** | Never average summary quantiles -- use histogram buckets.                | error.     |
|   [8]   | **Semantic** | `holt_winters()` deprecated 3.0 -- use `double_exponential_smoothing()`. | warning.   |
|   [9]   | **Perf**     | Always use specific label matchers to reduce cardinality.                | warning.   |
|  [10]   | **Perf**     | `=` over `=~` for exact matches (5-10x faster index lookup).             | info.      |
|  [11]   | **Perf**     | `rate()` range >= 4x scrape interval (typically `[2m]` minimum).         | warning.   |
|  [12]   | **Perf**     | `irate()` range <= 5m (only uses last 2 samples).                        | warning.   |
|  [13]   | **Perf**     | Subquery ranges < 7d; recording rules for longer.                        | warning.   |
|  [14]   | **Native**   | Native histogram queries omit `le` from `by()` clause.                   | info.      |
|  [15]   | **Native**   | `histogram_avg(rate(m[5m]))` replaces `_sum/_count` division (3.8+).     | info.      |
|  [16]   | **Native**   | `histogram_fraction(0, t, rate(m[5m]))` for latency SLOs (3.8+).         | info.      |

---
## [3][ANTI_PATTERNS]
>**Dictum:** *Anti-patterns waste resources or produce incorrect results.*

<br>

| [INDEX] | [ANTI_PATTERN]                | [BAD]                                    | [GOOD]                                                      |
| :-----: | ----------------------------- | ---------------------------------------- | ----------------------------------------------------------- |
|   [1]   | **No filters**                | `http_requests_total{}`.                 | `http_requests_total{job="api"}`.                           |
|   [2]   | **Regex for exact**           | `{status=~"200"}`.                       | `{status="200"}`.                                           |
|   [3]   | **Raw counter**               | `http_requests_total`.                   | `rate(http_requests_total[5m])`.                            |
|   [4]   | **Rate on gauge**             | `rate(memory_usage_bytes[5m])`.          | `avg_over_time(memory_usage_bytes[5m])`.                    |
|   [5]   | **Avg quantiles**             | `avg(metric{quantile="0.95"})`.          | `histogram_quantile(0.95, sum by (le) (rate(bucket[5m])))`. |
|   [6]   | **Long irate**                | `irate(metric[1h])`.                     | `rate(metric[1h])` or `irate(metric[2m])`.                  |
|   [7]   | **Deprecated fn**             | `holt_winters(m[5m], 0.5, 0.5)`.         | `double_exponential_smoothing(m[5m], 0.5, 0.5)`.            |
|   [8]   | **Classic when native avail** | `sum by (job, le) (rate(m_bucket[5m]))`. | `sum by (job) (rate(m[5m]))`.                               |
|   [9]   | **Missing group_left**        | `metric * on(l) info_metric`.            | `metric * on(l) group_left(labels) info_metric`.            |
|  [10]   | **Unquoted UTF-8 (3.0+)**     | `http.server.request.duration`.          | `{"http.server.request.duration"}`.                         |

---
## [4][OUTPUT_FORMAT]
>**Dictum:** *Structured output enables actionable remediation.*

<br>

```
## PromQL Validation Results

### Syntax Check
- Status: VALID / WARNING / ERROR
- Issues: [list with severity and WHY]

### Semantic Check
- Status: VALID / WARNING / ERROR
- Issues: [list with severity and WHY]

### Performance Analysis
- Status: OPTIMIZED / CAN BE IMPROVED / INEFFICIENT
- Suggestions: [list with estimated improvement]

### Query Explanation
- Metrics: [names and types]
- Functions: [what each does]
- Output Labels: [labels in result, or "None (fully aggregated)"]
- Expected Result Structure: [instant/range vector, scalar] with [series count]

### Intent Verification
1. What are you measuring?
2. Counter/gauge/histogram/summary?
3. Time window?
4. Aggregation labels?
5. Alerting, dashboarding, or analysis?
```

---
## [5][KNOWN_LIMITATIONS]
>**Dictum:** *Known boundaries set realistic expectations.*

<br>

- **Metric type detection**: Heuristic from naming conventions; custom names may misclassify.
- **Native histogram detection**: Cannot distinguish classic from native without runtime context.
- **No runtime context**: Cannot verify metric existence or label validity -- test against Prometheus.

---
## [6][CITATION_SOURCES]
>**Dictum:** *Source attribution enables verification.*

<br>

- `scripts/_common.py` -- shared constants, CheckSpec dataclass, parsing utilities.
- `scripts/validate_syntax.py` -- data-driven syntax validation via CheckSpec tuples.
- `scripts/check_best_practices.py` -- data-driven semantic/performance checks.
- `docs/best_practices.md` -- rules reference with native histogram patterns.
- `docs/anti_patterns.md` -- 33 anti-patterns with WHY column.
