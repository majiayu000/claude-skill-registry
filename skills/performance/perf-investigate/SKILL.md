---
name: perf-investigate
description: Self-contained multi-phase performance investigation workflow for establishing baselines, locating hot paths, profiling, testing one-change optimizations, and making evidence-gated keep/stop decisions. Use when performance investigation, why is this slow, perf regression, profile and optimize, establish a performance baseline, investigate latency.
metadata:
  short-description: Perf investigation workflow
---

Performance work is an extend op-cell: add measured capability without guessing, stacking changes, or laundering anecdotes into evidence. The invariant is: every hypothesis cites source evidence, every optimization has a baseline delta, and every decision is recorded in `.outline/perf/`.

## When to Apply / NOT

Apply: performance investigation; unexplained latency; throughput or memory regression; profiling a named scenario; creating a versioned baseline; deciding whether an optimization is worth keeping.

NOT: wrong-output bugs; speculative micro-optimizations; no reproducible command; no success metric; user only wants a quick code review; workloads too short to measure without variance control.

## Workflow

Use artifacts only under `.outline/perf/`:

- Ledger: `.outline/perf/investigations/<id>.md`
- Baselines: `.outline/perf/baselines/<version>.json`
- Profiles: `.outline/perf/profiles/<id>/`
- Experiments: `.outline/perf/experiments/<id>/`

### 1. Setup — scenario, command, version, quote

Require all three before measuring:

- scenario: the exact workload or user journey
- command: executable benchmark or repro command
- version: baseline label, commit label, release label, or user-provided slug

Record the user's problem statement verbatim. Do not paraphrase it. Create the ledger immediately with the phase order and empty evidence slots.

```sh
mkdir -p .outline/perf/investigations .outline/perf/baselines .outline/perf/profiles .outline/perf/experiments
```

Ledger id: short stable slug such as `2026-06-05-checkout-latency` or `<version>-<scenario-slug>`.

### 2. Baseline — repeated >=60s series

Run sequentially. No parallel benchmarks. Minimum measured duration is 60 seconds per baseline series. Prefer `hyperfine`; if the command emits structured metrics, preserve both `hyperfine` output and command metrics.

```sh
hyperfine --warmup 3 --min-runs 10 --export-json .outline/perf/baselines/<version>.hyperfine.json '<command>'
```

Then write exactly one consolidated baseline file:

```text
.outline/perf/baselines/<version>.json
```

The JSON must contain version, scenario, command, duration/run policy, environment, samples, summary metrics, source artifacts, and the verbatim quote. Overwrite the same version only when intentionally refreshing that version's baseline.

### 3. Hypotheses — <=5, evidence first

Generate at most five hypotheses. Each MUST cite at least one concrete evidence item before the claim is allowed:

- git history: recent change, churn, bug-fix cluster, ownership gap
- file:line: code path, allocation, loop, query, serialization, cache, I/O, locking, parsing
- baseline signal: p95 delta, throughput drop, RSS/alloc growth, variance spike

Git-history recipes:

```sh
git --no-pager log --since='90 days ago' --format='%h%x09%ad%x09%an%x09%s' --date=short -- <path>
git --no-pager log --format='%h%x09%ad%x09%s' --date=short --all --grep='fix\|perf\|slow\|latency\|timeout\|regress' -- <path>
git shortlog -sn -- <path>
```

Hypothesis shape:

```yaml
- id: H1
  claim: <one falsifiable sentence>
  evidence:
    - git:<commit-or-log-command-summary>
    - file:<path:line> <observed mechanism>
  confidence: low|med|high
  predicted_delta: <metric and direction>
  test: <single experiment or profiler check>
```

Certainty: HIGH = direct profile/baseline evidence plus code mechanism; MEDIUM = code mechanism plus correlated git or benchmark signal; LOW = plausible path with weak evidence. LOW can guide profiling, never justify code changes.

### 4. Code-paths — entry points and hot files

Locate entry points and candidate hot files before profiling.

When the repo is indexed, use codegraph first:

```text
codegraph_explore "<scenario terms> entry points hot path handlers"
codegraph_search "<symbol-or-route>"
codegraph_callers "<suspect symbol>"
codegraph_callees "<entry symbol>"
codegraph_impact "<symbol or file>"
```

Fallback commands:

```sh
git grep -nE '<route|handler|command|scenario-keyword|metric-name>' -- ':!node_modules' ':!dist' ':!build'
ast-grep -p 'function $NAME($$$ARGS) { $$$BODY }' <path>
ast-grep -p 'async function $NAME($$$ARGS) { $$$BODY }' <path>
ast-grep -p '$OBJ.$METHOD($$$ARGS)' <path>
```

For each candidate path, record `file:line`, symbol, why it is on the path, and which hypothesis it supports or refutes. Keep the set to the 10-15 files most tied to the scenario.

### 5. Profiling — pick the profiler and produce a flamegraph

Use the profiler that matches the workload. Capture the profile under `.outline/perf/profiles/<id>/`. A text summary alone is not enough; produce a flamegraph or flamegraph-compatible artifact and record path(s).

Node.js:

```sh
node --cpu-prof --cpu-prof-dir .outline/perf/profiles/<id> --cpu-prof-name cpu.cpuprofile <script-or-command-args>
npx -y speedscope .outline/perf/profiles/<id>/cpu.cpuprofile
```

Python:

```sh
py-spy record --duration 60 --rate 100 --output .outline/perf/profiles/<id>/flame.svg -- <command>
```

Go:

```sh
go test -run '^$' -bench '<bench>' -cpuprofile .outline/perf/profiles/<id>/cpu.pprof ./<pkg>
go tool pprof -svg <binary-or-test-binary> .outline/perf/profiles/<id>/cpu.pprof > .outline/perf/profiles/<id>/flame.svg
```

Java/JVM:

```sh
asprof -d 60 -f .outline/perf/profiles/<id>/flame.html <pid-or-java-command>
```

Native/Rust/C/C++ on Linux:

```sh
perf record -F 99 -g -o .outline/perf/profiles/<id>/perf.data -- <command>
perf script -i .outline/perf/profiles/<id>/perf.data > .outline/perf/profiles/<id>/perf.stacks
```

If frame pointers or symbols are missing, rebuild in the closest production-equivalent release mode with symbols enabled. Record the profiler command, artifact path, top frames, and file:line mappings.

### 6. Optimization — one change, >=2 runs, revert between experiments

Test exactly one change per experiment. No bundled optimizations. No follow-up tweak before measurement.

Discipline:

1. Start from the baseline code state.
2. Apply one change tied to one hypothesis.
3. Run at least two `hyperfine` comparisons.
4. Record raw samples, aggregate, variance, delta, and confidence.
5. Revert the change before the next experiment.
6. If keeping a change, re-apply only after the verdict says keep.

Comparison command:

```sh
hyperfine --warmup 3 --min-runs 10 --export-json .outline/perf/experiments/<id>/<experiment>.json '<baseline-command>' '<experiment-command>'
```

Revert discipline:

```sh
git restore -- <changed-files>
git diff --exit-code -- <changed-files>
```

Verdicts:

- keep: meaningful delta, stable variance, no correctness regression
- reject: no improvement, worse tail, higher resource cost, or complexity exceeds gain
- inconclusive: conflicting runs or profiler does not support the hypothesis

### 7. Decision — verdict and rationale required

Do not end with raw data. Write a decision:

```yaml
verdict: continue|keep|reject|stop|rerun
rationale: <why the evidence supports this>
evidence:
  - baseline:<path>
  - profile:<path>
  - experiment:<path>
next: <exact next action or stop condition>
```

Stop is valid when evidence says the bottleneck is elsewhere, the optimization is not worth complexity, variance is too high, or the measured budget is already met.

### 8. Consolidation — preserve the useful state

Finalize the ledger. Ensure there is one baseline JSON for the version, profile artifacts are named, experiments are linked, and rejected hypotheses are not left ambiguous. If a change is kept, add or update the smallest durable regression guard available for the project; if no guard is feasible, record why.

## Anti-patterns

- **Benchmark theater**: single run, short run, or hand-timed output.
- **Hypothesis laundering**: claim first, evidence later.
- **Stacked changes**: multiple edits measured as one.
- **Profiler cosplay**: profile artifact exists but no flamegraph, frame interpretation, or file:line mapping.
- **Metric drift**: comparing p50 to p95, debug to release, cold-start to warm path, or different inputs.
- **Invisible quote**: user problem paraphrased instead of preserved.
- **State sprawl**: caches, version vectors, editor shims, or run-state ceremony.

## Validation Gates

Before yielding an investigation result:

1. Ledger exists at `.outline/perf/investigations/<id>.md` with the verbatim quote.
2. Baseline exists at `.outline/perf/baselines/<version>.json` and records a >=60s repeated series.
3. Hypotheses are <=5 and every hypothesis has evidence plus confidence.
4. Code paths include entry points or hot files with `file:line` evidence.
5. Profiling produced a flamegraph or flamegraph-compatible artifact.
6. Each optimization experiment is one change, measured with >=2 runs, and reverted before the next.
7. Decision has verdict, rationale, and evidence links.
8. Consolidation leaves no orphan state or ambiguous rejected hypothesis.

Reference contract: `references/investigation.md` carries the exact phase contract, hypothesis rules, ledger template, and baseline schema for this skill.
