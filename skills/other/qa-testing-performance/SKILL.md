---
name: qa-testing-performance
description: "Designs performance and load testing for web, API, and backend systems. Use when setting budgets, profiling bottlenecks, or adding performance regression gates."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# QA Testing (Performance)

Performance engineering guidance for validating throughput, latency, resource consumption, and scalability. Use this skill to design load tests, set CI performance budgets, profile bottlenecks, and plan capacity.

Core sources are curated in `data/sources.json`. Prefer primary docs and re-check volatile external facts before recommending versions, pricing, or tool features.

## Quick Start

If key context is missing, ask for: SLOs/SLAs, critical user journeys, infrastructure topology, current baselines, traffic patterns (peak/sustained), database query hotspots, and frontend performance targets (Core Web Vitals).

1. **Baseline** — measure current latency (p50/p95/p99), throughput, error rate, and resource utilization under realistic traffic.
2. **Design scenarios** — model critical user journeys as scripted load test scenarios with realistic think times, data parameterization, and ramp profiles.
3. **Execute** — run load, stress, soak, or spike tests against a representative environment with monitoring active.
4. **Analyze** — compare results against baselines and budgets using percentiles, throughput curves, and error rate correlation. Identify bottlenecks with profiling.
5. **Set CI budgets** — define performance gates (latency thresholds, throughput minimums, error rate caps, Core Web Vitals budgets) and integrate into the pipeline.

## Workflow

1. Establish realistic baselines, traffic models, and budgets.
2. Choose the right performance test type and toolchain for the risk.
3. Run the scenarios against representative environments with monitoring active.
4. Analyze bottlenecks, then convert findings into budgets, profiles, and CI gates.

## Inputs to Gather

- SLOs/SLAs for latency, availability, throughput
- Critical user journeys and their expected traffic volumes
- Infrastructure topology (services, databases, caches, queues, CDN)
- Current performance baselines (if any)
- Traffic patterns: peak hours, seasonal spikes, growth projections
- Database query hotspots and slow query logs
- Frontend targets: Core Web Vitals (LCP, INP, CLS), bundle size limits
- Environment parity: how close is the test environment to production?

## Test Types

| Type | Purpose | When to Run |
|------|---------|-------------|
| Load | Validate behavior under expected traffic | Pre-release, nightly |
| Stress | Find the breaking point beyond expected capacity | Pre-release, capacity planning |
| Soak / Endurance | Detect memory leaks, connection pool exhaustion, GC degradation over hours | Weekly, pre-release |
| Spike | Validate behavior under sudden traffic bursts | Pre-release, after autoscaling changes |
| Capacity | Find the ceiling — max throughput before SLO violation | Quarterly, before major launches |

## When NOT to Load Test

Load testing has a real cost (build time, environment risk, engineer attention). Skip or downscope it when:

- **No SLO exists yet and traffic is trivial.** An internal tool with 5 users and no growth path doesn't need a load-testing harness — define the SLO first, or skip until one exists.
- **Production telemetry already answers the question.** If RUM/APM already shows the system holding p95/p99 comfortably under real peak traffic, a synthetic load test adds little; spend the budget on a soak test (leak/GC drift) instead, which telemetry alone won't catch as reliably.
- **The bottleneck is already known and reproducible.** Don't stand up a load-testing campaign to "confirm" a bug you can already reproduce with a single request under a profiler. Profile, fix, then run one confirmation load test — not a full suite.
- **Pre-product-market-fit.** Traffic shape, critical journeys, and even the API surface are still changing weekly. A load test built now models a system that won't exist in a month; capacity math (Little's Law, back-of-envelope RPS) is cheaper and nearly as informative at this stage.
- **Third-party or partner APIs without an agreement to test.** Load testing a vendor's production endpoint without permission risks rate-limit bans or ToS violations. Use their sandbox/staging tier, or model the dependency's expected latency into your own capacity math instead of hitting it directly.
- **A one-off batch job with no user-facing latency SLO.** Throughput/capacity math (rows/sec needed vs. measured single-run rate) is usually sufficient; a full VU-ramp load test is overkill for a job that runs once a night with no concurrent users.

When in doubt, the cheapest sanity check is Little's Law arithmetic (see [references/capacity-planning.md](references/capacity-planning.md#littles-law-sizing-concurrency-from-rate-and-latency)) — if the back-of-envelope math shows huge headroom, a full load-testing campaign may not be worth the cost yet.

## Tool Selection

| Tool | Language | Strengths | Best For |
|------|----------|-----------|----------|
| k6 | JavaScript | CLI-first, built-in thresholds, extensions; **k6 2.0** (GA 2026-05-11) adds a Playwright-compatible browser module, `expect()` assertion API, and AI commands (`k6 x agent`, `k6 x mcp`, `k6 x docs`, `k6 x explore`); the k6 Operator reached 1.0 (stable Kubernetes distributed execution). Latest patch as of this writing is **v2.1.0** (2026-06-30, opt-in feature flags, no breaking changes) — re-check `github.com/grafana/k6/releases` before pinning a version in CI. | API + browser load testing, CI gates, agent-assisted scripting |
| Locust | Python | Distributed, flexible, real Python scripts | Complex scenarios, Python teams |
| Artillery | YAML + JS | Declarative, good for APIs, scenario chaining | API load testing, quick setup |
| Gatling | Java/Kotlin/Scala/JS/TS | Strong reporting, enterprise support; polyglot since 3.12 (GraalVM) | JVM teams, enterprise |
| JMeter | Java/GUI | Widely adopted, protocol support | Legacy, protocol-heavy testing |
| Playwright | JavaScript | Real browser, network interception | Frontend performance, E2E perf |
| Lighthouse CI | JavaScript | Core Web Vitals, accessibility, SEO | Frontend budgets, PR gates |

## SLO-Driven Test Design

Design the test from the SLO, not the other way around. Working backward from "let's load test and see what we get" produces budgets that are either too loose (numbers the system already hits) or arbitrary (nobody can say why 500ms and not 600ms).

1. **Start from the availability/latency SLO.** Example: 99.9% of requests must complete under 300ms, measured over a rolling 30-day window.
2. **Derive the error budget.** Using a 30.44-day average month (365.25 / 12 days ≈ 43,830 minutes): a 99.9% SLO permits `0.001 × 43,830 ≈ 43.8 minutes` (≈ 43m 50s) of budget-consuming behavior per month — whether that's downtime or requests breaching the 300ms latency target. This is the standard "three nines" figure; re-derive it for your own SLO percentage and window rather than reusing someone else's number.
3. **Set the load test's arrival rate at expected peak, not average.** If peak is 500 rps, test at 500 rps (open-loop/arrival-rate — see [references/load-testing-patterns.md](references/load-testing-patterns.md#workload-model-open-vs-closed-loop)), not at a comfortable average that never stresses the tail.
4. **The pass/fail gate is the SLO minus margin, not the SLO itself.** If the SLO is p99 < 300ms, set the CI budget at p99 < 240ms (20% margin) so degradation is caught before it burns the production error budget.
5. **Goodput, not just percentiles, for SLO-gated systems.** Track the fraction of requests meeting the SLO at the tested concurrency (goodput) alongside p50/p95/p99 — a system can have a "fine" p99 while goodput is dropping because the failure mode is errors, not just slow responses (percentiles only describe successful requests unless you explicitly fold errors in as effectively-infinite latency).

## CI Integration Patterns

**Performance budgets** — define explicit thresholds:
- API latency: p95 < target, p99 < ceiling
- Throughput: requests/sec >= minimum under load
- Error rate: < threshold (typically 0.1-1%)
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 (official thresholds per Google, verified 2026-07-11; verify at developers.google.com/search/docs/appearance/core-web-vitals before citing since thresholds are assessed at the 75th percentile over a rolling 28-day window and are subject to change)
- Bundle size: < budget per entry point
- LLM endpoints: TTFT < 500ms (chat), tokens/sec >= target, goodput >= SLO at peak concurrency

**When to run each tier:**
- PR gate (lightweight): Lighthouse CI, bundle size check, smoke load test (30s, low VUs)
- Nightly (full): Full load test suite, soak test (1-2 hours), baseline comparison
- Pre-release (capacity): Stress test, spike test, capacity test with production-like data

**Artifact collection:** test results JSON, flamegraphs, comparison reports, Grafana snapshots, Lighthouse HTML reports.

## Frontend Performance

- **Core Web Vitals** — LCP (loading), INP (interactivity), CLS (visual stability) as primary metrics.
- **Lighthouse CI** — automate audits in CI, set score budgets, compare against baselines.
- **Bundle size** — track with bundlesize, size-limit, or bundlemon; fail PR on regression.
- **Synthetic monitoring** — scheduled Lighthouse runs or WebPageTest for trend tracking.
- **RUM vs synthetic** — use synthetic for CI gates, RUM for real-user production signals.

See [references/frontend-performance.md](references/frontend-performance.md) for detailed guidance.

## Backend and Database Performance

- **API latency profiling** — instrument endpoints with tracing, identify slow spans.
- **Database** — benchmark critical queries, test connection pool under load, detect N+1 patterns, validate index effectiveness.
- **Memory leak detection** — soak tests with heap snapshot comparison at intervals.
- **GC pressure** — monitor GC pause times and frequency under sustained load.

See [references/database-performance-testing.md](references/database-performance-testing.md) for database-specific patterns.

## Profiling and Analysis

- **CPU profiling** — flamegraphs to identify hot code paths. Language-specific: Node.js `--prof`, Python `py-spy`, Go `pprof`, Java async-profiler.
- **Memory profiling** — heap snapshots and allocation tracking to find leaks and excessive allocation.
- **Statistical rigor** — discard warm-up period, use percentiles (not averages), run sufficient duration for stable results, compare distributions not single numbers.

See [references/profiling-optimization.md](references/profiling-optimization.md) for language-specific profiling guidance.

## Capacity Planning

- **From load tests to sizing** — use stress test results to determine max throughput per instance, then calculate instance count for target traffic with headroom.
- **Cost modeling** — map instance counts to cloud costs, compare against traffic growth projections.
- **Auto-scaling validation** — load test with ramp patterns that trigger scaling, measure scale-up latency and cold-start impact.

See [references/capacity-planning.md](references/capacity-planning.md) for the full framework.

## Quick Reference

| Task | Approach | Key Metric |
|------|----------|------------|
| API latency regression | k6 with baseline comparison | p95 delta |
| Frontend speed regression | Lighthouse CI budget | LCP, INP, CLS |
| Memory leak detection | Soak test + heap snapshots | Heap growth over time |
| Capacity ceiling | Stress test with ramp-up | Max RPS before SLO breach |
| Database bottleneck | Query benchmark + connection pool test | Query p95, pool wait time |
| Bundle size regression | size-limit or bundlemon in CI | Bundle size delta |
| Auto-scaling validation | Spike test with monitoring | Scale-up latency, error rate during scale |
| LLM/AI API latency | Separate TTFT and generation throughput; test with realistic prompt distributions | TTFT p95, tokens/sec, goodput |
| Continuous profiling | Pyroscope 2.0 (Grafana) for always-on production profiling | Regression detection at deploy time |

## Decision Tree

```text
Performance concern: [Symptom]
    │
    ├─ Slow API responses?
    │   ├─ Under normal load? → Profile backend (flamegraph + trace spans)
    │   └─ Only under load? → Load test → find bottleneck (CPU, DB, pool, GC)
    │
    ├─ Slow page load?
    │   ├─ Large bundle? → Bundle analysis + code splitting
    │   └─ Slow server response? → API profiling + caching
    │   └─ Layout shift? → CLS debugging (font, image, dynamic content)
    │
    ├─ Unknown capacity?
    │   └─ Stress test → find ceiling → capacity plan with headroom
    │
    ├─ Memory growth over time?
    │   └─ Soak test + heap snapshots at intervals → compare retained objects
    │
    ├─ Latency spikes under traffic bursts?
    │   └─ Spike test → check auto-scaling, connection pools, queue depth
    │
    ├─ LLM/AI endpoint?
    │   ├─ TTFT too high? → prefill optimization (prompt length, batching)
    │   ├─ Throughput degrading? → tokens/sec sweep + concurrency step test
    │   └─ Inconsistent under load? → warm vs cold cache scenario; mock for CI
    │
    └─ Need CI performance gate?
        ├─ API? → k6 thresholds in pipeline
        ├─ Frontend? → Lighthouse CI budgets
        └─ Bundle? → size-limit or bundlemon
```

## Do / Avoid

**Do:**
- Baseline before optimizing — measure first, then improve
- Use percentiles (p50, p95, p99) — never averages for latency
- Test with realistic data volumes and parameterized test data
- Profile before guessing — flamegraphs over intuition
- Run sustained soak tests to find memory leaks and GC issues
- Discard warm-up period from results (JIT, cache priming, connection pool fill)
- Test against a representative environment, not an empty staging instance

**Avoid:**
- Optimizing without profiling evidence
- Using averages for latency metrics (they hide tail latency)
- Testing only the happy path with trivial data
- Testing against production without safeguards and stakeholder approval
- Ignoring warm-up period in results
- Treating a single run as conclusive — run multiple iterations
- Comparing results across different environments or data sets

## Resources

| Resource | Purpose |
|----------|---------|
| [references/load-testing-patterns.md](references/load-testing-patterns.md) | Load test design: scenarios, ramp-up, data, analysis; open/closed loop; LLM/AI API testing |
| [references/performance-budgets-ci.md](references/performance-budgets-ci.md) | CI performance gates and baseline management |
| [references/profiling-optimization.md](references/profiling-optimization.md) | CPU, memory, I/O profiling by language; continuous profiling with Pyroscope 2.0 |
| [references/frontend-performance.md](references/frontend-performance.md) | Core Web Vitals, Lighthouse CI, bundle tracking |
| [references/database-performance-testing.md](references/database-performance-testing.md) | Query benchmarks, connection pools, N+1 detection |
| [references/capacity-planning.md](references/capacity-planning.md) | Load results to infrastructure sizing |

### Data

| File | Purpose |
|------|---------|
| [data/sample-perf-results.json](data/sample-perf-results.json) | Realistic B2B SaaS performance test results: budgets, measured values, and test scenarios |

## Templates

| Template | Purpose |
|----------|---------|
| [assets/template-performance-test-plan.md](assets/template-performance-test-plan.md) | Performance test scope, scenarios, and acceptance criteria |
| [assets/template-k6-load-test.js](assets/template-k6-load-test.js) | Starter k6 script with stages, thresholds, and custom metrics |
| [assets/template-performance-budget.md](assets/template-performance-budget.md) | Budget definition for latency, throughput, and Core Web Vitals |

## Scripts

Stdlib-only Python CLI — no external dependencies, runs with Python 3.9+.

| Script | Purpose |
|--------|---------|
| [scripts/perf_budget_checker.py](scripts/perf_budget_checker.py) | Budget validation, CI tier planning, and full Markdown report generation |

Run from the `qa-testing-performance/` directory:

```bash
# Budget check — PASS/WARN/FAIL per metric, overall CI gate verdict
python scripts/perf_budget_checker.py check --input data/sample-perf-results.json

# CI test tier assignment (PR_gate / nightly / pre_release) for all scenarios
python scripts/perf_budget_checker.py plan --input data/sample-perf-results.json

# Full Markdown performance test report to stdout
python scripts/perf_budget_checker.py report --input data/sample-perf-results.json

# Write report to file
python scripts/perf_budget_checker.py report \
  --input data/sample-perf-results.json \
  --output report.md
```

The `check` subcommand exits `1` on any FAIL metric (CI-gate-friendly). See [scripts/README.md](scripts/README.md) for full format details and threshold reference.

## ASCII Flow

```text
Performance testing request
  -> Gather SLOs, traffic shape, topology, budgets, and critical journeys
  -> Baseline latency, throughput, errors, resources, and frontend vitals
  -> Design load, stress, spike, soak, or profiling scenario
  -> Execute against representative environment with monitoring active
  -> Analyze bottlenecks with percentiles, saturation, traces, and profiles
  -> Add CI or release budgets only after repeatable evidence exists
```

## Navigation

- `## Workflow`, `## Test Types`, and `## Decision Tree` for the baseline sequence
- `## When NOT to Load Test` and `## SLO-Driven Test Design` before committing to a full test campaign
- `## Resources`, `## Templates`, and `## Scripts` for deeper materials and automation
- `## Related Skills` for observability, resilience, backend, and database handoffs

## Related Skills

| Skill | Purpose |
|-------|---------|
| [qa-observability](../qa-observability/SKILL.md) | Metrics, tracing, and performance monitoring |
| [qa-resilience](../qa-resilience/SKILL.md) | Failure mode testing under load |
| [qa-testing-strategy](../qa-testing-strategy/SKILL.md) | Risk-based test strategy |
| [qa-debugging](../qa-debugging/SKILL.md) | Performance debugging and profiling |
| [ops-devops-platform](../ops-devops-platform/SKILL.md) | CI/CD and infrastructure |
| [software-backend](../software-backend/SKILL.md) | Backend API optimization |
| [data-sql-optimization](../data-sql-optimization/SKILL.md) | Database query tuning |

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search or web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

