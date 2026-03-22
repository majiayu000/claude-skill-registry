---
name: ce-performance-tuning
description: >
  Configure CE caching, parallel execution, batch-size tuning, and FAST feature
  filtering per ADR-003 and ADR-004 for faster explanations on large datasets.
---

# CE Performance Tuning

You are optimizing calibrated-explanations performance for a user's workload.

## Required references

- `docs/improvement/adrs/ADR-003-caching-key-and-eviction.md`
- `docs/improvement/adrs/ADR-004-parallel-backend-abstraction.md`
- `src/calibrated_explanations/cache/` (caching implementation)
- `src/calibrated_explanations/perf/` (performance utilities)
- `src/calibrated_explanations/parallel/` (parallel execution)

## Use this skill when

- CE explanations are slow on a user's dataset.
- Configuring caching for repeated calibrator calls.
- Enabling or tuning parallel execution.
- Diagnosing performance bottlenecks in CE pipelines.

## Performance levers

### 1. Caching (ADR-003)

CE provides an opt-in in-process LRU cache for calibrator results:

- **Enable**: `cache=True` or configure via `CE_CACHE=1` env var.
- **Eviction**: LRU with configurable `max_items`.
- **Flush**: Call `explainer.flush_cache()` when input data changes.
- **Deterministic keys**: Cache keys use namespace + version_tag + payload hash.

Key source files:
- `src/calibrated_explanations/cache/cache.py` (core cache)
- `src/calibrated_explanations/cache/explanation_cache.py` (explanation-level)

### 2. Parallel execution (ADR-004)

CE supports parallel feature-level and instance-level explanation:

- **Auto strategy**: `ParallelExecutor` chooses serial vs. parallel based on
  workload hints (n_instances, n_features, task_size_hint_bytes).
- **Force parallel**: `CE_PARALLEL=thread` or `CE_PARALLEL=process`.
- **Force serial**: `CE_PARALLEL=serial` (useful for debugging).
- **Configuration**: `ParallelConfig` with `min_instances_for_parallel`,
  `min_features_for_parallel`, `instance_chunk_size`, `feature_chunk_size`.

Key source files:
- `src/calibrated_explanations/parallel/parallel.py`
- `src/calibrated_explanations/perf/parallel.py`

### 3. Batch size and chunking

For large datasets:
- Chunk explanations into batches to control memory usage.
- Use `instance_chunk_size` to limit per-batch instance count.
- Monitor memory with `task_size_hint_bytes` for the auto strategy.

### 4. FAST feature filtering

Uses FAST explanation weights to filter out low-importance features *before*
running the expensive factual/alternative explanation pass. This reduces the
per-instance feature space and can significantly speed up large-feature datasets.

- **Source**: `src/calibrated_explanations/core/explain/_feature_filter.py`
- **Config object**: `FeatureFilterConfig(enabled, per_instance_top_k=8, strict_observability)`
- **Enable via env var**: `CE_FEATURE_FILTER=on` (or `1`, `true`)
- **Disable**: `CE_FEATURE_FILTER=off` (default)
- **Tune top-k**: `CE_FEATURE_FILTER=on,top_k=12` (comma-separated tokens)
- **Strict observability**: `CE_STRICT_OBSERVABILITY=1` — promotes debug-level
  filter events to WARNING and emits structured governance log entries.

How it works:
1. A FAST explanation pass runs first (cheap, approximate).
2. Per instance, the top-k features by absolute FAST weight are kept.
3. Features not in any instance's top-k are added to the global ignore set.
4. The expensive explanation pass runs on the reduced feature set.

**Trade-off**: Lower `top_k` = faster but may drop marginally relevant features.
Higher `top_k` = closer to unfiltered behaviour but less speedup.

When to use:
- Datasets with many features (50+) where most features are irrelevant per instance.
- Batch explanations where per-instance filtering provides cumulative savings.

## Diagnostic workflow

1. **Baseline**: Time `explainer.explain_factual(X)` on a representative sample.
2. **Profile**: Check if bottleneck is calibration, perturbation, or collection.
3. **Apply**: Enable caching (if repeated calibrator calls), then parallel
   execution (if many instances/features), then FAST feature filtering
   (if many features per instance are irrelevant).
4. **Measure**: Compare timing after each change.

## Constraints

- Caching is opt-in; it does not change calibration semantics.
- Parallel execution may increase memory usage.
- FAST feature filtering may drop marginally relevant features at low `top_k`.
- Always verify that explanations remain correct after tuning.
