---
name: hammer-benchmark-regression
description: Runs performance benchmarks for SDL3 HammerEngine and detects regressions by comparing metrics against baseline. Use when testing performance-sensitive changes to AI, collision, pathfinding, particle systems, or before merging features to ensure no performance degradation.
allowed-tools: [Bash, Read, Write, Grep]
---

# HammerEngine Performance Regression Detection

This Skill is **critical** for SDL3 HammerEngine's performance requirements. The engine must maintain 10,000+ entity support at 60+ FPS with minimal CPU usage. This Skill detects performance regressions before they reach production.

## Performance Requirements (from CLAUDE.md)

- **AI System:** 10,000+ entities at 60+ FPS with <6% CPU
- **Collision System:** Spatial hash with efficient AABB detection
- **Pathfinding:** A* pathfinding with dynamic weights
- **Event System:** 1K-10K event throughput
- **Particle System:** Camera-aware batched rendering

## Workflow Overview

**⚠️ CRITICAL: AI Scaling Benchmark is MANDATORY**
The AI System is the most performance-critical component. Always run `./tests/test_scripts/run_ai_benchmark.sh` as part of the regression check. DO NOT proceed to report generation without AI benchmark results.

1. **Identify or Create Baseline** - Store previous metrics
2. **Run Benchmark Suite** - Execute ALL 6 performance tests (including AI)
3. **Extract Metrics** - Parse results from test outputs
4. **Compare vs Baseline** - Calculate percentage changes
5. **Flag Regressions** - Alert on performance degradation
6. **Generate Report** - Detailed analysis with recommendations

**Checklist before generating report:**
- [ ] AI Scaling Benchmark completed
- [ ] Collision System Benchmark completed
- [ ] **Pathfinder Benchmark completed** ← CRITICAL: Always verify metrics extracted!
- [ ] Event Manager Scaling completed
- [ ] Particle Manager Benchmark completed
- [ ] UI Stress Tests completed

**Metrics Extraction Verification (MANDATORY):**
- [ ] AI: Entity scaling metrics and updates/sec extracted
- [ ] **Pathfinding: Async throughput metrics extracted (NOT immediate timing)** ← PRODUCTION METRIC ONLY!
- [ ] Collision: SOA timing and efficiency extracted
- [ ] **Trigger Detection: Detector count, overlaps, method (spatial/sweep) extracted**
- [ ] Event: Throughput and latency extracted
- [ ] Particle: Update time extracted
- [ ] UI: Processing throughput extracted

## Benchmark Test Suites

### Available Benchmarks (ALL REQUIRED)

**Working Directory:** Use absolute path to project root or set `$PROJECT_ROOT` environment variable.
All paths below are relative to project root.

**IMPORTANT: All 6 benchmarks MUST be run for complete regression analysis.**

1. **AI Scaling Benchmark** (`./bin/debug/ai_scaling_benchmark`) **[REQUIRED - CRITICAL]**
   - Script: `./tests/test_scripts/run_ai_benchmark.sh`
   - Tests: Entity scaling (100-10000), threading comparison, behavior mix
   - Metrics: Entity updates/sec, time per update, threading speedup
   - Target: 100K+ updates/sec at 10000 entities
   - Duration: ~3 minutes
   - **Status: CRITICAL - Engine core performance benchmark**

2. **Collision Scaling Benchmark** (`./bin/debug/collision_scaling_benchmark`) **[REQUIRED]**
   - Script: `./tests/test_scripts/run_collision_scaling_benchmark.sh`
   - Tests: SAP (Sweep-and-Prune) for MM, Spatial Hash for MS, Trigger Detection scaling
   - Metrics: MM/MS time, throughput, pair counts, trigger detection overlaps, sub-quadratic scaling
   - **Trigger Detection:** Tests spatial query (<50 entities) and sweep-and-prune (>=50 entities) paths
   - Duration: ~2 minutes

3. **Pathfinder Benchmark** (`./bin/debug/pathfinder_benchmark`) **[REQUIRED]**
   - Script: `./tests/test_scripts/run_pathfinder_benchmark.sh`
   - Tests: Async pathfinding throughput at scale
   - Metrics: **Async throughput (paths/sec), batch processing performance, success rate**
   - **Note:** Immediate pathfinding deprecated - only track async metrics
   - Duration: ~5 minutes

4. **Event Manager Scaling** (`./bin/debug/event_manager_scaling_benchmark`) **[REQUIRED]**
   - Script: `./tests/test_scripts/run_event_scaling_benchmark.sh`
   - Tests: Event throughput 10-4000 events, concurrency
   - Metrics: Events/sec, dispatch latency, queue depth
   - Duration: ~2 minutes

5. **Particle Manager Benchmark** (`./bin/debug/particle_manager_benchmark`) **[REQUIRED]**
   - Script: `./tests/test_scripts/run_particle_manager_benchmark.sh`
   - Tests: Batch rendering performance, particle updates
   - Metrics: Particles/frame, update time, batch count
   - Duration: ~2 minutes

6. **UI Stress Tests** (`./bin/debug/ui_stress_test`) **[REQUIRED]**
   - Script: `./tests/test_scripts/run_ui_stress_tests.sh`
   - Tests: UI component performance, layout, collision checks
   - Metrics: Processing throughput, iteration time, layout calc/sec
   - Duration: ~1 minute

### Total Benchmark Duration: ~15 minutes

## Execution Steps

### Step 1: Identify Baseline

**Baseline Storage Location:**
```
$PROJECT_ROOT/test_results/baseline/
├── thread_safe_ai_baseline.txt         (AI system baseline)
├── collision_benchmark_baseline.txt
├── pathfinder_benchmark_baseline.txt
├── event_benchmark_baseline.txt
├── particle_manager_baseline.txt
├── buffer_utilization_baseline.txt
├── resource_tests_baseline.txt
├── serialization_baseline.txt
└── baseline_metadata.txt
```

**Baseline Creation Logic:**
```bash
# Check if baseline exists (requires PROJECT_ROOT to be set)
if [ ! -d "$PROJECT_ROOT/test_results/baseline/" ]; then
    echo "No baseline found. Creating baseline from current run..."
    mkdir -p "$PROJECT_ROOT/test_results/baseline/"
    CREATING_BASELINE=true
fi
```

**When to Create New Baseline:**
- No baseline exists (first run)
- User explicitly requests baseline refresh
- Major optimization work completed (intentional performance change)
- After validating improvements (new baseline for future comparisons)

### Step 2: Run Benchmark Suite

**CRITICAL: ALL 6 benchmarks must be run. DO NOT skip the AI benchmark.**

**Run individually (RECOMMENDED - allows better progress tracking):**
```bash
# IMPORTANT: Set PROJECT_ROOT and run from project directory
# Example: cd /path/to/SDL3_HammerEngine_Template && export PROJECT_ROOT=$(pwd)

# 1. AI Scaling Benchmark (REQUIRED - 3 minutes)
./tests/test_scripts/run_ai_benchmark.sh

# 2. Collision Scaling Benchmark (REQUIRED - 2 minutes)
./tests/test_scripts/run_collision_scaling_benchmark.sh

# 3. Pathfinder Benchmark (REQUIRED - 5 minutes)
./tests/test_scripts/run_pathfinder_benchmark.sh

# 4. Event Manager Scaling (REQUIRED - 2 minutes)
./tests/test_scripts/run_event_scaling_benchmark.sh

# 5. Particle Manager Benchmark (REQUIRED - 2 minutes)
./tests/test_scripts/run_particle_manager_benchmark.sh

# 6. UI Stress Tests (REQUIRED - 1 minute)
./tests/test_scripts/run_ui_stress_tests.sh
```

**Timeout Protection:**
Each benchmark has timeout protection:
- AI Scaling: 600 seconds (10 minutes)
- Others: 300 seconds (5 minutes)

If timeout occurs, flag as potential infinite loop or performance catastrophe.

**Progress Tracking:**
```
Running benchmarks (this will take ~15 minutes)...
[1/6] AI Scaling Benchmark... ✓ (3m 00s) - CRITICAL
[2/6] Collision Scaling Benchmark... ✓ (2m 05s)
[3/6] Pathfinder Benchmark... ✓ (5m 05s)
[4/6] Event Manager Scaling... ✓ (2m 10s)
[5/6] Particle Manager Benchmark... ✓ (2m 05s)
[6/6] UI Stress Tests... ✓ (1m 02s)
Total: 33m 49s
```

**Execution Order:**
Run benchmarks in the order listed above. AI benchmark should always be run first as it's the most critical system and longest-running test.

### Step 3: Extract Metrics

**Metrics Extraction Patterns:**

#### AI System Metrics

**Extract scaling performance:**
```bash
# Parse tabular output from AIEntityScaling test
grep -A 20 "AI Entity Scaling" test_results/ai_scaling_benchmark_*.txt | \
  grep -E "^\s+[0-9]+\s+[0-9.]+"

# Extract summary metrics (primary regression detection)
grep -E "Entity updates per second:|Threading mode:|Threading threshold" \
  test_results/ai_scaling_benchmark_*.txt

# Or use the current run file
cat test_results/ai_scaling_current.txt | grep -A 5 "SCALABILITY SUMMARY"
```

**Example Output:**
```
--- AI Entity Scaling ---
  Entities   Time (ms)   Updates/sec   Threading     Status
       100        0.85        117647       single          OK
       500        1.23        406504       multi           OK
      1000        1.89        529100       multi           OK
      2000        3.21        623053       multi           OK
      5000        7.12        702247       multi           OK
     10000       13.45        743494       multi           OK

SCALABILITY SUMMARY:
Entity updates per second: 743494 (at 10000 entities)
Threading mode: WorkerBudget Multi-threaded
```

**Baseline Key Format:** `Entity_<count>_UpdatesPerSec`

**Key Metrics:**
- **Updates/sec:** Primary performance metric (higher is better)
- **Threading threshold:** Currently 500 entities (single-threaded below, multi above)
- **Scaling efficiency:** Updates/sec should increase sub-linearly with entity count

#### Collision Scaling Metrics
```bash
# Extract metrics from collision scaling benchmark
grep -E "Movables|Statics|Time \(ms\)|Throughput|Scenario" test_results/collision_scaling_current.txt
```

**Example Output:**
```
--- MM Scaling (SAP) ---
  Movables   Time (ms)    MM Pairs    Throughput
       100        0.02           5        5151/ms
       500        0.14          31        3559/ms
      1000        0.22          59        4596/ms
      2000        0.41          97        4893/ms
      5000        1.11         282        4509/ms
     10000        2.26         527        4434/ms

--- MS Scaling (Spatial Hash) ---
   Statics    Movables   Time (ms)    MS Pairs          Mode
       100         200        0.15         155          hash
       500         200        0.14          93          hash
      2000         200        0.15          83          hash
      5000         200        0.15          79          hash
     10000         200        0.15          70          hash
     20000         200        0.15          72          hash

--- Combined Scaling ---
       Scenario   Time (ms)        MM        MS      Total
    Small (500)        0.11        14        15          29
  Medium (1500)        0.19        35        36          71
   Large (3000)        0.34        64        65         129
      XL (6000)        0.65       164       164         328
    XXL (12000)        1.31       305       305         610
```

**Key Metrics:**
- MM SAP: O(n log n) - time grows sub-quadratically with movable count
- MS Hash: O(n) - time stays FLAT as static count increases (spatial hash effectiveness)
- Combined: Sub-quadratic scaling verified up to 12K entities

#### Trigger Detection Metrics
```bash
# Extract trigger detection scaling from collision benchmark
grep -E "Detectors|Triggers|Overlaps|Method" test_results/collision_scaling_current.txt | \
  grep -v "^--"
```

**Example Output:**
```
--- Trigger Detection Scaling ---
   Detectors    Triggers   Time (ms)    Overlaps        Method
           1         100       0.143           0        spatial
           1         400       0.138           0        spatial
          10         200       0.145           1        spatial
          25         200       0.148           4        spatial
          50         200       0.228           3          sweep
         100         200       0.255           9          sweep
         200         400       0.433          44          sweep
```

**Key Metrics:**
- **Detectors:** Entities with NEEDS_TRIGGER_DETECTION flag (Player + enabled NPCs)
- **Triggers:** EventOnly triggers in the world (water, area markers, etc.)
- **Method:** Spatial query (<50 entities) or sweep-and-prune (>=50 entities)
- **Performance Target:** <0.5ms for typical scenarios (1-50 detectors, 100-400 triggers)

**Adaptive Strategy Thresholds:**
- < 50 entities: Spatial queries O(N × ~k nearby triggers)
- ≥ 50 entities: Sweep-and-prune O((N+T) log (N+T))

#### Pathfinder Metrics **[ASYNC THROUGHPUT ONLY]**

**⚠️ IMPORTANT:** PathfinderManager uses **async-only pathfinding** in production. Immediate (synchronous) pathfinding is deprecated and should NOT be tracked in regression analysis.

**Production Metrics Extraction:**
```bash
# Extract async pathfinding throughput - PRIMARY METRIC
grep -E "Async.*Throughput|paths/sec" test_results/pathfinder_benchmark_results.txt | \
  grep -E "Throughput:"

# Example output format:
#   Throughput: 3e+02 paths/sec
#   Throughput: 4e+02 paths/sec
#   Throughput: 4e+02 paths/sec
```

**REQUIRED Metrics to Extract:**
1. **Async throughput** (paths/second) - Production metric
2. **Success rate** (must be 100%)
3. **Batch processing performance** (if high-volume scenarios tested)

**DEPRECATED Metrics (DO NOT TRACK):**
- ❌ Immediate pathfinding timing (deprecated, not used in production)
- ❌ Path calculation time by distance (legacy synchronous metric)
- ❌ Per-path latency measurements (not relevant for async architecture)

**Baseline Comparison Keys:**
- `Pathfinding_Async_Throughput_PathsPerSec`
- `Pathfinding_Batch_Processing_Enabled`
- `Pathfinding_SuccessRate`

**Example Baseline Comparison:**
```
| Metric | Baseline | Current | Change | Status |
|--------|----------|---------|--------|--------|
| Async Throughput | 300-400 paths/sec | 300-400 paths/sec | 0% | ⚪ Stable |
| Batch Processing | 50K paths/sec | 100K paths/sec | +100% | 🟢 Major Improvement |
| Success Rate | 100% | 100% | 0% | ✓ Maintained |
```

**What to Report:**
- Always include a dedicated "Pathfinding System" section in regression reports
- Focus on async throughput as primary metric
- Highlight batch processing performance for high-volume scenarios
- Note success rate (failures are critical regressions)
- Exclude deprecated immediate pathfinding metrics from analysis

#### Event Manager Metrics
```bash
grep -E "Events/sec:|Dispatch Latency:|Queue Depth:" test_results/event_manager_scaling/performance_metrics.txt
```

**Example Output:**
```
Events/sec: 8500
Dispatch Latency: 0.12ms
Queue Depth: 128
Peak Throughput: 10000 events/sec
```

#### Particle Manager Metrics
```bash
grep -E "Particles/frame:|Render Time:|Batch Count:" test_results/particle_benchmark/performance_metrics.txt
```

**Example Output:**
```
Particles/frame: 5000
Render Time: 3.2ms
Batch Count: 12
Culling Efficiency: 88%
```

#### UI Metrics
```bash
grep -E "Render Time:|Event Handling:|Components:" test_results/ui_stress/performance_metrics.txt
```

**Example Output:**
```
Components: 1000
Render Time: 4.5ms
Event Handling: 0.3ms
DPI Scaling: 60 FPS
```

### Step 4: Compare Against Baseline

**Comparison Algorithm:**

For each metric:
1. Read baseline value
2. Read current value
3. Calculate percentage change: `((current - baseline) / baseline) * 100`
4. Determine status:
   - **Regression:** Slower/worse performance
   - **Improvement:** Faster/better performance
   - **Stable:** Within noise threshold (±5%)

**Example Comparison:**

| System | Metric | Baseline | Current | Change | Status |
|--------|--------|----------|---------|--------|--------|
| AI | FPS | 62.3 | 56.8 | -8.8% | 🔴 Regression |
| AI | CPU% | 5.8% | 6.4% | +10.3% | 🔴 Regression |
| Collision | Checks/sec | 125000 | 134000 | +7.2% | 🟢 Improvement |
| Pathfinder | Calc Time | 8.5ms | 8.7ms | +2.4% | ⚪ Stable |

### Step 5: Flag Regressions

**Regression Severity Levels:**

#### 🔴 CRITICAL (Block Merge)
- AI System FPS drops below 60
- AI System CPU usage exceeds 8%
- Any performance metric degrades >15%
- Benchmark timeouts (infinite loops)

#### 🟠 WARNING (Review Required)
- Performance degradation 10-15%
- AI System FPS 60-65 (near threshold)
- Collision/Pathfinding >10% slower

#### 🟡 MINOR (Monitor)
- Performance degradation 5-10%
- Within acceptable variance but trending down

#### ⚪ STABLE (Acceptable)
- Performance change <5% (measurement noise)

#### 🟢 IMPROVEMENT
- Performance improvement >5%
- Successful optimization

**Regression Detection Logic:**

```python
def classify_change(metric_name, baseline, current, is_lower_better=False):
    change_pct = ((current - baseline) / baseline) * 100

    # Invert for metrics where lower is better (e.g., CPU%, time)
    if is_lower_better:
        change_pct = -change_pct

    # Critical thresholds for AI system (most important)
    if "AI" in metric_name or "FPS" in metric_name:
        if metric_name == "FPS" and current < 60:
            return "CRITICAL", "FPS below 60 threshold"
        if metric_name == "CPU" and current > 8:
            return "CRITICAL", "CPU exceeds 8% threshold"

    # General thresholds
    if change_pct < -15:
        return "CRITICAL", f"{abs(change_pct):.1f}% regression"
    elif change_pct < -10:
        return "WARNING", f"{abs(change_pct):.1f}% regression"
    elif change_pct < -5:
        return "MINOR", f"{abs(change_pct):.1f}% regression"
    elif change_pct > 5:
        return "IMPROVEMENT", f"{change_pct:.1f}% improvement"
    else:
        return "STABLE", f"{abs(change_pct):.1f}% variance (acceptable)"
```

**AI Benchmark Regression Detection Strategy:**

1. **Scaling Regression (Low Entity Counts):**
   - 100-500 entity performance regresses more than larger counts
   - **Root Cause:** Single-threaded path overhead, behavior initialization
   - **Action:** Profile single-threaded update path, check behavior creation costs
   - **Impact:** Small-world performance degraded

2. **Scaling Regression (High Entity Counts):**
   - 5000-10000 entity performance regresses
   - **Root Cause:** Threading overhead, batch processing, WorkerBudget tuning
   - **Action:** Profile ThreadSystem, check batch sizes, validate WorkerBudget
   - **Impact:** Large-world performance degraded

3. **Threading Speedup Degraded:**
   - Single-threaded time stable but multi-threaded time increases
   - **Root Cause:** Thread contention, lock overhead, false sharing
   - **Action:** Profile thread synchronization, check mutex usage
   - **Impact:** Threading efficiency degraded

4. **Uniform Regression:**
   - All entity counts regress proportionally
   - **Root Cause:** Core update loop changes, behavior execution overhead
   - **Action:** Profile behavior update(), check per-entity costs
   - **Impact:** System-wide performance degradation

### Step 6: Generate Report

**Report Structure:**

```markdown
# HammerEngine Performance Regression Report
**Date:** YYYY-MM-DD HH:MM:SS
**Branch:** <current-branch>
**Baseline:** <baseline-date or "New Baseline Created">
**Total Benchmark Time:** <duration>

---

## 🎯 Overall Status: <PASSED/FAILED/WARNING>

<summary-of-regressions>

---

## 📊 Performance Summary

### AI System - Entity Scaling

**Purpose:** Tests AIManager performance with production behaviors

| Entities | Baseline | Current | Change | Threading | Status |
|----------|----------|---------|--------|-----------|--------|
| 100 | 120K/s | 117K/s | -2.5% | single | ⚪ Stable |
| 500 | 410K/s | 406K/s | -1.0% | multi | ⚪ Stable |
| 1000 | 535K/s | 529K/s | -1.1% | multi | ⚪ Stable |
| 2000 | 630K/s | 623K/s | -1.1% | multi | ⚪ Stable |
| 5000 | 710K/s | 702K/s | -1.1% | multi | ⚪ Stable |
| 10000 | 750K/s | 743K/s | -0.9% | multi | ⚪ Stable |

**Status:** ⚪ **STABLE**
- All metrics within acceptable variance (<6%)
- Scaling efficiency maintained across entity counts
- Threading speedup consistent above threshold

**Threading Mode Comparison:**
| Entities | Single (ms) | Multi (ms) | Speedup |
|----------|-------------|------------|---------|
| 500 | 2.45 | 1.23 | 1.99x |
| 1000 | 4.12 | 1.89 | 2.18x |
| 2000 | 7.85 | 3.21 | 2.44x |
| 5000 | 18.50 | 7.12 | 2.60x |

---

### Collision Scaling System

| Scenario | Baseline (ms) | Current (ms) | Change | Throughput | Status |
|----------|---------------|--------------|--------|------------|--------|
| MM 1000 movables | 0.25 | 0.22 | -12% | 4596/ms | 🟢 Improvement |
| MM 5000 movables | 1.20 | 1.11 | -8% | 4509/ms | 🟢 Improvement |
| MM 10000 movables | 2.50 | 2.26 | -10% | 4434/ms | 🟢 Improvement |
| MS 10K statics | 0.16 | 0.15 | -6% | FLAT | ⚪ Stable |
| MS 20K statics | 0.16 | 0.15 | -6% | FLAT | ⚪ Stable |
| Combined XL (6K) | 0.70 | 0.65 | -7% | N/A | 🟢 Improvement |
| Combined XXL (12K) | 1.40 | 1.31 | -6% | N/A | 🟢 Improvement |

**Status:** 🟢 **IMPROVEMENT**
- SAP (Sweep-and-Prune) for MM: O(n log n) scaling confirmed up to 10K movables
- Spatial Hash for MS: O(n) scaling confirmed - time stays FLAT from 100 to 20K statics
- Combined: Sub-quadratic scaling verified up to 12K entities

---

### Trigger Detection System (EventOnly Triggers)

**Purpose:** Tests detection of EventOnly triggers (water, area markers, etc.) by entities with NEEDS_TRIGGER_DETECTION flag.

| Detectors | Triggers | Baseline (ms) | Current (ms) | Change | Method | Status |
|-----------|----------|---------------|--------------|--------|--------|--------|
| 1 (Player) | 100 | 0.15 | 0.14 | -7% | spatial | ⚪ Stable |
| 1 (Player) | 400 | 0.15 | 0.14 | -7% | spatial | ⚪ Stable |
| 10 (NPCs) | 200 | 0.16 | 0.15 | -6% | spatial | ⚪ Stable |
| 25 (NPCs) | 200 | 0.16 | 0.15 | -6% | spatial | ⚪ Stable |
| 50 (threshold) | 200 | 0.25 | 0.23 | -8% | sweep | ⚪ Stable |
| 100 (NPCs) | 200 | 0.28 | 0.26 | -7% | sweep | ⚪ Stable |
| 200 (NPCs) | 400 | 0.45 | 0.43 | -4% | sweep | ⚪ Stable |

**Status:** ⚪ **STABLE**
- Adaptive strategy working correctly (spatial <50, sweep >=50)
- Performance within targets (<0.5ms for typical scenarios)
- Flag-based filtering eliminates unnecessary AABB tests

**Notes:**
- Only entities with NEEDS_TRIGGER_DETECTION flag are processed
- Player has flag by default; NPCs can opt-in via setTriggerDetection(true)
- Replaced O(movables × triggers) brute-force with adaptive O(N × k) or O((N+T) log (N+T))

---

### Pathfinding System **[ALWAYS INCLUDE - CRITICAL]**

**⚠️ IMPORTANT:** This section is MANDATORY in all regression reports. Pathfinding performance directly impacts integrated AI benchmarks.

| Distance (units) | Baseline Time | Current Time | Change | Path Nodes | Success Rate | Status |
|------------------|---------------|--------------|--------|------------|--------------|--------|
| 50 (Short) | 0.048 ms | 0.024 ms | -50.0% | 1 | 100% | 🟢 Major Improvement |
| 400 (Medium) | 0.259 ms | 0.049 ms | -81.1% | 3 | 100% | 🟢 Major Improvement |
| 2000 (Long) | 0.502 ms | 0.052 ms | -89.6% | 6 | 100% | 🟢 Major Improvement |
| 4000 (Very Long) | 0.756 ms | 0.128 ms | -83.1% | 10 | 100% | 🟢 Major Improvement |
| 8000 (Extreme) | N/A | 0.349 ms | N/A | 20 | 100% | 🟢 Excellent |

**Status:** [Determine based on actual results]
- Path calculation performance across all distance ranges
- Success rate (must be 100% - failures are critical regressions)
- Path quality (nodes explored should be reasonable)
- A* algorithm and cache effectiveness

**Template Notes:**
- Always show ALL distance ranges (50, 400, 2000, 4000, 8000 units)
- Include success rate for each distance (failures = critical regression)
- Note path quality (average nodes should be optimal)
- Highlight major improvements or regressions
- Cross-reference with integrated AI benchmark if pathfinding impacts it

---

### Event Manager

| Metric | Baseline | Current | Change | Status |
|--------|----------|---------|--------|--------|
| Events/sec | 8500 | 8200 | -3.5% | ⚪ Stable |
| Dispatch Latency | 0.12ms | 0.13ms | +8.3% | 🟡 MINOR |
| Queue Depth | 128 | 128 | 0.0% | ⚪ Stable |
| Peak Throughput | 10000 | 9800 | -2.0% | ⚪ Stable |

**Status:** 🟡 **MINOR REGRESSION**
- Slight increase in dispatch latency
- Monitor for further degradation

---

### Particle Manager

| Metric | Baseline | Current | Change | Status |
|--------|----------|---------|--------|--------|
| Particles/frame | 5000 | 5000 | 0.0% | ⚪ Stable |
| Render Time | 3.2ms | 3.1ms | -3.1% | ⚪ Stable |
| Batch Count | 12 | 11 | -8.3% | 🟢 Improvement |
| Culling Efficiency | 88% | 90% | +2.3% | 🟢 Improvement |

**Status:** 🟢 **IMPROVEMENT**
- Better batching efficiency
- Improved culling

---

### UI System

| Metric | Baseline | Current | Change | Status |
|--------|----------|---------|--------|--------|
| Components | 1000 | 1000 | 0.0% | ⚪ Stable |
| Render Time | 4.5ms | 4.4ms | -2.2% | ⚪ Stable |
| Event Handling | 0.3ms | 0.3ms | 0.0% | ⚪ Stable |
| DPI Scaling FPS | 60 | 60 | 0.0% | ⚪ Stable |

**Status:** ⚪ **STABLE**

---

## 🚨 Critical Issues (BLOCKING)

1. **AI System FPS Below Threshold**
   - Current: 56.8 FPS (Target: 60+)
   - Regression: -8.8%
   - **Action Required:** Must fix before merge

---

## ⚠️ Warnings (Review Required)

1. **AI System CPU Usage Increase**
   - Current: 6.4% (Target: <6%)
   - Regression: +10.3%

2. **AI Update Time Increase**
   - Current: 13.9ms (Baseline: 12.4ms)
   - Regression: +12.1%

---

## 📈 Improvements

1. **Collision System Performance**
   - Query time improved 12.5%
   - Collision checks/sec improved 7.2%

2. **Particle Manager Batching**
   - Batch count reduced 8.3% (better efficiency)
   - Culling efficiency improved 2.3%

---

## 🔍 Detailed Analysis

### Performance Hotspots (if callgrind data available)

<parse callgrind reports from test_results/valgrind/callgrind/>

Top Functions by Time:
1. AIManager::updateBehaviors - 45% (up from 38% - REGRESSION)
2. CollisionManager::detectCollisions - 18% (down from 22% - IMPROVEMENT)
3. PathfinderManager::calculatePath - 12% (stable)

---

## 📋 Recommendations

### Immediate Actions (Critical)
1. Investigate AI System performance regression
2. Profile AIManager::updateBehaviors with valgrind/callgrind
3. Review commits since baseline for AI changes
4. Do not merge until FPS ≥60 restored

### Short-term Actions (Warnings)
1. Monitor Event Manager dispatch latency
2. Consider AI batch size optimization
3. Review recent AI behavior changes

### Long-term Actions (Optimization)
1. Apply collision system improvements to other managers
2. Document particle manager batching technique
3. Consider updating baseline after AI fixes validated

---

## 📁 Files

**Baseline:** `$PROJECT_ROOT/test_results/baseline/*.txt`
**Current Results:** `$PROJECT_ROOT/test_results/*/performance_metrics.txt`
**Callgrind Reports:** `$PROJECT_ROOT/test_results/valgrind/callgrind/` (if available)
**Full Report:** `$PROJECT_ROOT/test_results/regression_reports/regression_YYYY-MM-DD.md`

---

## ✅ Next Steps

- [ ] Fix AI System FPS regression (BLOCKING)
- [ ] Verify fixes with re-run: `claude run benchmark regression check`
- [ ] Update baseline after validation: `claude update performance baseline`
- [ ] Document optimization techniques from collision improvements

---

**Generated by:** hammer-benchmark-regression Skill
**Report saved to:** $PROJECT_ROOT/test_results/regression_reports/regression_YYYY-MM-DD.md
```

**Console Summary:**
```
=== Performance Regression Check ===

Status: 🔴 REGRESSION DETECTED (BLOCKING)

Critical Issues:
  🔴 AI System FPS: 56.8 (target: 60+) - 8.8% regression

Warnings:
  🟠 AI CPU Usage: 6.4% (target: <6%) - 10.3% increase
  🟡 Event Dispatch Latency: +8.3%

Improvements:
  🟢 Collision Query Time: -12.5%
  🟢 Particle Batching: -8.3%

Total Benchmark Time: 21m 15s

❌ DO NOT MERGE - Fix AI regression first

Full Report: $PROJECT_ROOT/test_results/regression_reports/regression_2025-01-15.md
```

## Storage & Baseline Management

### Baseline Update Command
```bash
# After validating improvements, update baseline (requires PROJECT_ROOT)
cp "$PROJECT_ROOT/test_results/"*/performance_metrics.txt "$PROJECT_ROOT/test_results/baseline/"
echo "Baseline updated: $(date)" > "$PROJECT_ROOT/test_results/baseline/baseline_date.txt"
```

### Baseline History
Keep historical baselines for long-term tracking:
```
$PROJECT_ROOT/test_results/baseline_history/
├── 2025-01-01_baseline/
├── 2025-01-15_baseline/
└── 2025-02-01_baseline/
```

## Integration with Development Workflow

**Use this Skill:**
- Before merging feature branches
- After performance optimizations (verify improvement)
- Weekly during active development
- Before releases (ensure no regressions)
- When modifying AI, collision, pathfinding, or particle systems

## Final Report Validation Checklist

**⚠️ MANDATORY: Verify BEFORE submitting report to user**

Before finalizing any regression report, confirm ALL of the following:

### Benchmark Execution
- [ ] All 6 benchmarks completed successfully (no timeouts/crashes)
- [ ] AI Scaling: Entity scaling results present with updates/sec metrics
- [ ] **Pathfinding: Path length scaling data extracted** ← CRITICAL!
- [ ] Collision: SOA timing data extracted
- [ ] Event Manager: Throughput data extracted
- [ ] Particle Manager: Update timing data extracted
- [ ] UI Stress: Processing metrics extracted

### Report Completeness
- [ ] **Pathfinding System section included in report** ← DO NOT SKIP!
- [ ] AI System: Entity scaling and threading comparison sections present
- [ ] Collision System: Performance table present
- [ ] Event Manager: Metrics table present
- [ ] Particle Manager: Performance data present
- [ ] UI System: Throughput data present
- [ ] Overall status determined (PASSED/WARNING/FAILED)
- [ ] Regression/improvement analysis complete

### Critical Pathfinding Verification
- [ ] Pathfinding metrics extracted from `test_results/pathfinder_benchmark_current.txt`
- [ ] All 5 distance ranges present (50, 400, 2000, 4000, 8000 units)
- [ ] Success rates reported (must be 100%)
- [ ] Performance comparison against baseline completed
- [ ] Pathfinding section visible in final report

**If ANY checklist item is unchecked, DO NOT submit the report. Extract missing data first.**

## Exit Codes

- **0:** All benchmarks passed, no regressions
- **1:** Critical regressions detected (BLOCKING)
- **2:** Warnings detected (review required)
- **3:** Benchmark failed to run (timeout/crash)
- **4:** Baseline creation mode (informational)

## Usage Examples

When the user says:
- "check for performance regressions"
- "run benchmarks"
- "test performance"
- "verify no performance degradation"
- "compare against baseline"

Activate this Skill automatically.

## Performance Expectations

- **Full benchmark suite:** ~31 minutes
  - AI Scaling: ~18 minutes
  - Collision: ~3 minutes
  - Pathfinder: ~5 minutes
  - Event Manager: ~2 minutes
  - Particle Manager: ~2 minutes
  - UI Stress: ~1 minute
- **Report generation:** 2-3 minutes
- **Total:** ~33-35 minutes for complete analysis

## Troubleshooting

**Benchmark timeouts:**
- Possible infinite loop or catastrophic performance regression
- Run individual benchmark with debugging: `gdb ./bin/debug/ai_system_benchmark`

**Inconsistent results:**
- System load affecting benchmarks
- Re-run benchmarks in clean environment
- Close other applications
- Check for thermal throttling

**No baseline found:**
- Skill will create baseline from current run
- Subsequent runs will compare against this baseline
- Update baseline after validating improvements
