---
name: logql-generator
depth: extended
description: >-
  Generates LogQL queries for Grafana Loki 3.0-3.6 log aggregation and metric extraction. Use when building Loki queries, dashboards, alerts, or optimizing pipeline performance with bloom filters, structured metadata, pattern matching, and approx_topk aggregations.
---

# [H1][LOGQL-GENERATOR]
>**Dictum:** *Pipeline order determines query performance.*

<br>

Generate LogQL for Loki 3.0-3.6 (bloom filters, structured metadata, `approx_topk`). Cross-references: **observability-stack** for Loki deployment, **promql-generator** for PromQL metric queries.

**Tasks:**
1. **Goal** -- Error analysis, performance, security, debugging? Dashboard, alert, ad-hoc?
2. **Sources** -- Labels (`job`, `namespace`, `app`), log format (JSON/logfmt/plain), time range.
3. **Query type** -- Log query (return lines) or metric query (calculate values)?
4. **Plan** -- Plain-English plan, confirm with user before generating.
5. **Generate** -- Apply patterns below; consult `references/best_practices.md`.
6. **Deliver** -- Final query + explanation + usage context (Grafana panel, alert rule, logcli, HTTP API).

---
## [1][VERSION_MATRIX]
>**Dictum:** *Version awareness prevents deprecated patterns.*

<br>

| [INDEX] | [VERSION] | [KEY_CHANGES]                                                                     |
| :-----: | --------- | --------------------------------------------------------------------------------- |
|   [1]   | **3.0**   | Bloom filters, structured metadata, pattern match `\|>` / `!>`.                   |
|   [2]   | **3.3**   | Bloom acceleration for structured metadata filters.                               |
|   [3]   | **3.5**   | Promtail deprecated (EOL March 2, 2026 -- use Alloy), SSD mode deprecated.        |
|   [4]   | **3.6**   | `approx_topk` on querier, reduced JSON/logfmt parser allocations, Loki UI plugin. |

**Guidance:**
- Promtail EOL March 2, 2026 -- migrate to Alloy.
- BoltDB deprecated -- use TSDB with v13 schema.

---
## [2][PIPELINE_ORDER]
>**Dictum:** *Each stage filters BEFORE the next -- moving expensive operations earlier wastes resources.*

<br>

```
{stream} -> line filter -> decolorize -> struct metadata -> parser -> label filter -> keep/drop -> format -> aggregate
 cheapest                                                                                              most expensive
```

**Guidance:**
- Structured metadata filters BEFORE parsers enables bloom filter acceleration (3.3+).
- Line filters (`|=`, `!=`) are O(1) substring checks -- place before parsers.
- Pattern match `|>` / `!>` uses `<_>` wildcards, 10x faster than regex (3.0+).

**Best-Practices:**
- Extract only needed JSON fields: `| json level, status` not `| json` -- reduces allocations (3.6).
- `| decolorize` before `| logfmt` -- ANSI codes break key=value parsing.
- `| drop instance, pod` before aggregation -- reduces series cardinality.

---
## [3][STREAM_AND_FILTERS]
>**Dictum:** *Specific stream selectors minimize chunk scanning.*

<br>

| [INDEX] | [OPERATOR] | [MEANING]          | [EXAMPLE]                               |
| :-----: | ---------- | ------------------ | --------------------------------------- |
|   [1]   | **`\|=`**  | Contains.          | `{job="app"} \|= "error"`               |
|   [2]   | **`!=`**   | Not contains.      | `{job="app"} != "debug"`                |
|   [3]   | **`\|~`**  | Regex match.       | `{job="app"} \|~ "error\|fatal"`        |
|   [4]   | **`!~`**   | Regex not match.   | `{job="app"} !~ "health\|metrics"`      |
|   [5]   | **`\|>`**  | Pattern match.     | `{app="api"} \|> "<_> level=error <_>"` |
|   [6]   | **`!>`**   | Pattern not match. | `{app="api"} !> "<_> level=debug <_>"`  |

---
## [4][PARSERS]
>**Dictum:** *Parser selection affects per-line cost.*

<br>

| [INDEX] | [PARSER]      | [SYNTAX]                                      | [USE_WHEN]                       |
| :-----: | ------------- | --------------------------------------------- | -------------------------------- |
|   [1]   | **`pattern`** | `\| pattern "<ip> - <_> <status>"`            | Fixed-delimiter structured text. |
|   [2]   | **`logfmt`**  | `\| logfmt [--strict] [--keep-empty]`         | `key=value` pairs.               |
|   [3]   | **`json`**    | `\| json` or `\| json status="response.code"` | JSON (specify fields for perf).  |
|   [4]   | **`regexp`**  | `\| regexp "(?P<field>\\w+)"`                 | Complex extraction, last resort. |
|   [5]   | **`unpack`**  | `\| unpack`                                   | Packed JSON from Alloy/Promtail. |

---
## [5][AGGREGATIONS]
>**Dictum:** *Metric queries aggregate log entries into time series.*

<br>

### [5.1][LOG_RANGE]

| [INDEX] | [FUNCTION]                        | [USE_WHEN]             |
| :-----: | --------------------------------- | ---------------------- |
|   [1]   | **`rate(log-range)`**             | Dashboard rate panels. |
|   [2]   | **`count_over_time(log-range)`**  | Counting occurrences.  |
|   [3]   | **`bytes_rate(log-range)`**       | Bandwidth monitoring.  |
|   [4]   | **`absent_over_time(log-range)`** | Dead service alerting. |

---
### [5.2][UNWRAPPED_RANGE]

| [INDEX] | [FUNCTION]                           | [USE_WHEN]                     |
| :-----: | ------------------------------------ | ------------------------------ |
|   [1]   | **`sum/avg/max/min_over_time`**      | Aggregate numeric values.      |
|   [2]   | **`quantile_over_time(phi, range)`** | Latency percentiles from logs. |
|   [3]   | **`first/last_over_time`**           | Boundary values.               |
|   [4]   | **`rate_counter(range)`**            | Counter-like log values.       |

Operators: `sum`, `avg`, `min`, `max`, `count`, `stddev`, `topk`, `bottomk`, `approx_topk`, `sort`, `sort_desc`.
Grouping: `sum by (label1, label2) (...)` or `sum without (label1) (...)`.

---
### [5.3][APPROX_TOPK]

`approx_topk(k, expr)` -- probabilistic top-K via count-min sketch, instant queries only. Requires `limits_config.shard_aggregations: [approx_topk]` on querier.

---
## [6][STRUCTURED_METADATA]
>**Dictum:** *Structured metadata enables high-cardinality filtering without index impact.*

<br>

Filter AFTER stream selector, BEFORE parsers for bloom acceleration. NOT indexed -- no cardinality impact.

```logql
{app="api"} | trace_id="abc123" | json | level="error"     # CORRECT -- bloom accelerated
# WRONG: {app="api", trace_id="abc123"}                     # trace_id is NOT an indexed label
```

**Guidance:**
- Bloom filters (3.3+) provide O(1) chunk skipping for string equality and OR filters placed before parsers.
- Automatic labels: `service_name` (from container/OTel), `detected_level` (when `discover_log_levels: true`).
- `vector(0)` fallback in alerting prevents "no data" flapping on sparse logs.

---
## [7][METRIC_PATTERNS]
>**Dictum:** *Metric queries are pre-aggregated -- prefer for dashboards and alerts.*

<br>

| [INDEX] | [PATTERN]            | [QUERY]                                                                                   |
| :-----: | -------------------- | ----------------------------------------------------------------------------------------- |
|   [1]   | **Rate**             | `rate({job="app"} \|= "error" [5m])`                                                      |
|   [2]   | **Count by label**   | `sum by (app) (count_over_time({ns="prod"} \| json [5m]))`                                |
|   [3]   | **Error percentage** | `sum(rate({app="api"} \| json \| level="error" [5m])) / sum(rate({app="api"}[5m])) * 100` |
|   [4]   | **Latency P95**      | `quantile_over_time(0.95, {app="api"} \| json \| unwrap duration [5m])`                   |
|   [5]   | **Approx Top 10**    | `approx_topk(10, sum by (endpoint) (rate({app="api"}[5m])))`                              |
|   [6]   | **Dead service**     | `absent_over_time({app="api"}[5m])`                                                       |
|   [7]   | **Offset compare**   | `sum(rate(...[5m])) - sum(rate(...[5m] offset 1d))`                                       |

---
## [8][NON-EXISTENT_FEATURES]
>**Dictum:** *Generating non-existent operators wastes user time.*

<br>

| [INDEX] | [FEATURE]         | [REALITY]                                                       |
| :-----: | ----------------- | --------------------------------------------------------------- |
|   [1]   | **`\| dedup`**    | UI-level in Grafana Explore. Use `sum by (field)` for dedup.    |
|   [2]   | **`\| distinct`** | Reverted PR #8662. Use `count(count by (field) (...))`.         |
|   [3]   | **`\| limit N`**  | API param `&limit=100`, Grafana "Line limit", logcli `--limit`. |

---
## [9][ALLOY_PIPELINE_STAGES]
>**Dictum:** *Alloy pipeline stages shape labels and metadata arriving in Loki.*

<br>

| [INDEX] | [STAGE]                      | [PURPOSE]                                  |
| :-----: | ---------------------------- | ------------------------------------------ |
|   [1]   | **`loki.relabel`**           | Map K8s labels to Loki labels.             |
|   [2]   | **`loki.process/multiline`** | Aggregate multi-line logs (stack traces).  |
|   [3]   | **`loki.process/sampling`**  | Reduce high-volume streams (cost control). |

[REFERENCE] `infrastructure/src/deploy.ts` lines 29-36.

---
## [10][RESOURCES]
>**Dictum:** *Reference files provide copy-paste patterns and performance guidance.*

<br>

- `examples/log_queries.logql` -- log parsing, filtering, structured metadata, template functions.
- `examples/metric_queries.logql` -- aggregation, alerting, rate/counter functions, label operations.
- `references/best_practices.md` -- performance, anti-patterns, recording rules.
- context7 MCP (`grafana loki`) -- authoritative docs for unclear syntax.
