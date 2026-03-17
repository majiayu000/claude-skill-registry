---
name: adding-benchmarks
description: Add new benchmarks to the CI pipeline. Guides through creating benchmark JSON files, integrating with bootstrap.sh, and ensuring proper CI upload via ci3.yml workflow.
---

# Adding Benchmarks

## When to Use

Use this skill when:
- Adding new performance benchmarks to a package
- Creating benchmark tests that should be tracked over time
- Integrating existing benchmarks into the CI pipeline

## Benchmark System Overview

Benchmarks flow through the system as follows:
1. **Generation**: Each package produces `bench-out/*.bench.json` files
2. **Aggregation**: `bench_merge` in root `bootstrap.sh` combines all files, prefixing names with the package path
3. **Upload**: CI caches the merged JSON and GitHub Action uploads to the benchmark dashboard
4. **Display**: Results appear at the dashboard with historical tracking

**Live dashboard:** https://aztecprotocol.github.io/benchmark-page-data/bench/?branch=next

## How Benchmark Names Work

### Name Construction

The **final benchmark name** combines two parts:

1. **Package prefix** (added automatically by `bench_merge`): Based on where the file lives
2. **Local name** (what you write in JSON): Your metric identifier

### Dashboard Grouping

The dashboard splits names by `/` to create a collapsible tree. The **last segment** becomes the chart name, everything before it becomes the group hierarchy.

| Full Name | Group Path | Chart Name |
|-----------|------------|------------|
| `yarn-project/stdlib/Tx/private/getTxHash/avg` | `yarn-project/stdlib/Tx/private/getTxHash` | `avg` |
| `yarn-project/kv-store/Map/Individual insertion` | `yarn-project/kv-store/Map` | `Individual insertion` |
| `barretenberg/sol/Add2HonkVerifier` | `barretenberg/sol` | `Add2HonkVerifier` |

### Naming Best Practices

**Use `/` to create logical groupings:**
```json
[
  {"name": "Tx/private/getTxHash/avg", "value": 1.2, "unit": "ms"},
  {"name": "Tx/private/getTxHash/p50", "value": 1.1, "unit": "ms"},
  {"name": "Tx/public/getTxHash/avg", "value": 2.3, "unit": "ms"}
]
```

**Avoid flat names** - they create no hierarchy and are hard to navigate:
```json
[
  {"name": "tx_private_gettxhash_avg", "value": 1.2, "unit": "ms"}
]
```

**Common suffixes:**
- Timing: `avg`, `p50`, `p95`, `p99`, `min`, `max`, `total`
- Size: `_opcodes`, `_gates`, `memory`
- Rate: `gasPerSecond`, `jobs_per_sec`

## Required JSON Format

All benchmark files must be arrays using the `customSmallerIsBetter` format:

```json
[
  {"name": "category/metric_name", "value": 12345, "unit": "gas"},
  {"name": "category/another_metric", "value": 100.5, "unit": "ms"}
]
```

**Rules:**
- Must be a JSON array `[...]`, not an object
- Each entry needs `name`, `value`, `unit`
- `value` must be numeric (lower is better)
- File must end with `.bench.json`

**Optional fields** (preserved by benchmark-action):
- `range` (string): Variance info (e.g., `"± 5%"`)
- `extra` (string): Metadata — used for stacked chart grouping (see below)

## Stacked Charts

To render multiple metrics as a **single stacked area chart** (e.g., component breakdowns), add an `extra` field with a `stacked:GROUP_NAME` value. Entries sharing the same GROUP_NAME are overlaid on one chart.

```json
[
  {"name": "proving/cpus-8/total_ms", "value": 31663, "unit": "ms"},
  {"name": "proving/cpus-8/oink_prove_ms", "value": 4992, "unit": "ms", "extra": "stacked:proving/cpus-8/components"},
  {"name": "proving/cpus-8/sumcheck_ms", "value": 3318, "unit": "ms", "extra": "stacked:proving/cpus-8/components"},
  {"name": "proving/cpus-8/circuit_ms", "value": 4642, "unit": "ms", "extra": "stacked:proving/cpus-8/components"}
]
```

**How it works:**
- `extra: "stacked:GROUP_NAME"` → entries with the same GROUP_NAME are rendered as one stacked chart
- No `extra` field → individual line chart (default behavior)
- Stacked entries still appear as individual charts on the main benchmark-action dashboard; the stacked view is rendered by a custom dashboard page
- The GROUP_NAME becomes the chart title (after `bench_merge` prefixing, same as `name`)
- The `extra` field is one of the 5 fields preserved by the benchmark-action Zod schema (`name`, `value`, `unit`, `range`, `extra`); any other custom fields will be stripped

**When to use stacked charts:**
- Component-level timing breakdowns (e.g., sumcheck, PCS, circuit construction)
- Resource allocation views (e.g., memory by subsystem)
- Any case where you want to see how a total decomposes into parts over time

## Adding a New Benchmark

### Step 1: Create the Benchmark

**TypeScript** (most common):
```typescript
// my_bench.test.ts
import { Timer } from '@aztec/foundation/timer';
import { writeFile, mkdir } from 'fs/promises';

describe('MyComponent benchmarks', () => {
  const results: { name: string; value: number; unit: string }[] = [];

  afterAll(async () => {
    if (process.env.BENCH_OUTPUT) {
      await mkdir(path.dirname(process.env.BENCH_OUTPUT), { recursive: true });
      await writeFile(process.env.BENCH_OUTPUT, JSON.stringify(results));
    }
  });

  it('benchmark operation', async () => {
    const timer = new Timer();
    // ... operation to benchmark ...
    results.push({ name: 'MyComponent/operation/avg', value: timer.ms(), unit: 'ms' });
  });
});
```

**Shell** (jq-based):
```bash
mkdir -p bench-out
jq -n '[
  {name: "metric1", value: '$VALUE1', unit: "ms"},
  {name: "metric2", value: '$VALUE2', unit: "gas"}
]' > bench-out/my-component.bench.json
```

**Python**:
```python
import json
benchmark_list = [{"name": "category/metric", "value": 12345, "unit": "gas"}]
with open("bench-out/my-component.bench.json", "w") as f:
    json.dump(benchmark_list, f)
```

### Step 2: Register in bootstrap.sh

Add to the package's `bench_cmds` function:

```bash
function bench_cmds {
  local hash=$(hash)
  echo "$hash BENCH_OUTPUT=bench-out/my_component.bench.json yarn-project/scripts/run_test.sh <package>/src/my_bench.test.ts"
}
```

**Options:** `:ISOLATE=1`, `:CPUS=8`, `:MEM=16g`, `:TIMEOUT=7200`

**CPUS Suggestion:** For long running or compute-heavy benchmarks allocate CPUs (`:CPUS=N`). Benchmarks have strict scheduling, so if you request X CPUs, you'll have them available for consistent results.

**ISOLATE Suggestion:** Use `:ISOLATE=1` when your benchmark needs a clean, isolated environment with no network access and pinned resources. This runs the test in a Docker container, ensuring reproducible results without interference from other processes.

**MEM Suggestion:** Use `:MEM=Xg` (e.g., `:MEM=16g`) for memory-intensive benchmarks that may exceed the default allocation (CPUS × 4GB). Pair with `:ISOLATE=1` since memory limits are enforced via Docker.

**TIMEOUT Suggestion:** Use `:TIMEOUT=N` (in seconds) for benchmarks that take longer than the default timeout. For example, `:TIMEOUT=1800` for 30 minutes, `:TIMEOUT=7200` for 2 hours.

**Important naming gotcha:** Benchmark test files must use `.bench.test.ts` (with a dot before `bench`), NOT `_bench.test.ts`. The test discovery pattern `[[ "$test" =~ \.bench\.test\.ts$ ]]` specifically looks for `.bench.test.ts`.

### Step 3: Verify

```bash
# Run locally
BENCH_OUTPUT=bench-out/test.bench.json yarn test src/my_bench.test.ts

# Validate JSON
jq . bench-out/test.bench.json
jq 'all(has("name") and has("value") and has("unit"))' bench-out/test.bench.json
```

## CI Details

**Benchmarks upload when:**
- PR has label: `ci-merge-queue`, `ci-full`, or `ci-full-no-test-cache` (publishes to target branch, i.e. `next` or a merge-train branch)
- Running on merge queue (publishes with `next`)

**10-commit visibility window:** The dashboard only shows benchmarks that ran in the last 10 commits. If a benchmark stops running, it disappears after ~10 merges.

## Reference Implementations

- **TypeScript**: `yarn-project/stdlib/src/tx/tx_bench.test.ts`
- **Python**: `l1-contracts/scripts/generate_benchmark_json.py`
- **Shell**: `yarn-project/p2p/testbench/consolidate_benchmarks.sh`
- **Circuits**: `noir-projects/noir-protocol-circuits/scripts/run_bench.sh`
