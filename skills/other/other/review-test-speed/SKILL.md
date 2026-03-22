---
name: review-test-speed
description: Optimize AHK test suite speed without sacrificing reliability
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Analyze AHK test suite performance and find speed optimizations. Use parallelism where possible.

**Scope**: AHK tests only — unit tests, GUI tests, live tests, lifecycle tests. NOT static analysis checks (`review-static-speed` covers those) and NOT query tools (`review-tool-speed` covers those).

## Step 1 — Baseline

Run `.\tests\test.ps1 --live --timing` to get the hierarchical timing report. This is the ground truth for where time is spent.

## What to Look For

### Phase-level bottlenecks

The test suite is heavily parallelized into phases. Within a parallel phase, the slowest test determines the phase duration. Look for:
- A single test file much longer than its siblings in the same phase — suggests splitting it
- A phase with only one test — could it run in parallel with an adjacent phase?
- Phases that could overlap but don't (e.g., a phase 2 test that has no dependency on phase 1 results)

### Store/process reuse

Launching AHK processes and compiled exes is expensive (~1–2s each). Look for:
- Tests that launch their own store/process when they could share one from a prior test in the same file
- Multiple test files that each launch the same subprocess independently — could they share a single launch?
- But respect test isolation: shared state between unrelated tests causes flakiness. Only reuse when tests are logically sequential.

### Sleep vs polling

The test suite uses `WaitForFlag(&flag)` for adaptive polling (see `testing.md`). Look for:
- Fixed `Sleep()` calls that could be converted to polling with `WaitForFlag` or similar
- But **do NOT shorten existing Sleep values blindly** — past attempts at aggressive sleep reduction caused flakiness. Any sleep that exists likely survived because shorter values were tried and failed.

### Compilation overhead

Live tests depend on compilation. Check:
- Is smart-skip working correctly? (Should skip Ahk2Exe when exe is newer than all sources)
- Is compilation running in parallel with pre-gate? (It should be — see `testing.md` pipeline model)

### Test splitting candidates

For any test file that is a phase bottleneck, check whether it can be logically split:
- Independent test groups with no shared state → safe to split into parallel files
- Tests sharing a launched process or store → must stay together (splitting would add launch overhead that exceeds the parallelism gain)
- Use `tests/bench_unit_split.ps1` to measure AHK startup overhead vs per-file test time

## Constraints

This suite is designed for **automated agentic execution** — no user interaction, no prompts, cursor suppression, icon suppression. Any new or modified tests MUST follow existing patterns in `test_utils.ahk`:
- `_Test_RunSilent(cmdLine)` for process launching
- `WaitForFlag(&flag)` for adaptive polling
- Proper cleanup on all exit paths

## Validation

After explore agents report back, **validate every finding yourself**.

For each candidate optimization:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with actual code quoted. Include the `--timing` numbers that make this a bottleneck.
2. **Trace dependencies**: Does this test depend on state from a prior test? Does splitting it require duplicating setup?
3. **Counter-argument**: "What would make this optimization counterproductive?" — Would splitting add more launch overhead than it saves in parallelism? Would removing a sleep cause timing-dependent flakiness?
4. **Observed vs inferred**: Did you measure the bottleneck in `--timing` output, or infer it from code structure?

## CRITICAL — Stability Validation

**Every optimization MUST pass a stability gate before inclusion in the plan.** After implementing a change, run the full test suite 5 times consecutively:

```powershell
.\tests\test.ps1 --live
.\tests\test.ps1 --live
.\tests\test.ps1 --live
.\tests\test.ps1 --live
.\tests\test.ps1 --live
```

All 5 runs must pass. A single failure means the optimization introduced flakiness and must be reverted or reworked. We are optimizing speed AND stability, not speed at the cost of reliability.

## Plan Format

**Section 1 — Phase bottlenecks** (timing data from `--timing`):

| Phase | Bottleneck Test | Duration | Next Slowest | Gap | Splittable? |
|-------|----------------|----------|-------------|-----|-------------|
| Phase 2 | `test_live_core.ahk` | 8.2s | `test_live_features.ahk` 3.1s | 5.1s | Yes — groups A and B are independent |

**Section 2 — Process reuse opportunities**:

| File | Lines | Current | Optimization | Estimated Savings |
|------|-------|---------|-------------|-------------------|
| `test_foo.ahk` | 42–60 | Launches own store | Reuse store from test_bar | ~1.5s |

**Section 3 — Sleep-to-polling conversions**:

| File | Line | Current | Replacement | Risk |
|------|------|---------|-------------|------|
| `test_foo.ahk` | 88 | `Sleep(500)` | `WaitForFlag(&ready)` | Low — flag already exists |

Order by estimated time savings (largest first). Note cumulative impact on total suite duration.

Ignore any existing plans — create a fresh one.
