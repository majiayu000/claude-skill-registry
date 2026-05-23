---
name: hammer-memory-profiler
description: Simplified memory profiling and leak detection for SDL3 HammerEngine using valgrind memcheck, AddressSanitizer, and massif. Identifies memory leaks, allocation hotspots, buffer reuse violations, and provides system-by-system memory breakdown with optimization suggestions. Use after performance-critical changes or when investigating memory issues.
allowed-tools: [Bash, Read, Write, Grep, Glob]
---

# HammerEngine Memory Profiler

Comprehensive memory profiling and leak detection for SDL3 HammerEngine. Identifies memory leaks, per-frame allocation hotspots, buffer reuse violations, and provides actionable optimization recommendations following CLAUDE.md patterns.

## Available Scripts

This skill includes utility scripts in `.claude/skills/hammer-memory-profiler/scripts/`:

- **`run_leak_check.sh`** - Quick memory leak detection with valgrind memcheck
- **`run_massif_all_tests.sh`** - Run valgrind massif on all test executables
- **`parse_massif.py`** - Parse massif reports and generate comprehensive analysis

Use these scripts directly or let the skill invoke them automatically.

## Purpose

Memory management is critical for HammerEngine's performance targets (10K+ entities @ 60 FPS). This Skill automates:

1. **Leak Detection** - Find memory leaks before production
2. **Allocation Profiling** - Identify per-frame allocation hotspots (frame spikes)
3. **Buffer Reuse Verification** - Ensure CLAUDE.md buffer patterns followed
4. **System Breakdown** - Track memory usage per manager (AI, Collision, etc.)
5. **Baseline Comparison** - Monitor memory usage trends over time
6. **Optimization Suggestions** - Provide specific fixes based on project patterns

## Profiling Modes

### Mode 1: Quick Leak Check (2-5 minutes)
- Run core tests with valgrind memcheck
- Detect definite leaks and invalid access
- Generate summary report
- **Use when:** Daily development, before commits

### Mode 2: Allocation Profiling (5-10 minutes)
- Build with AddressSanitizer
- Run targeted tests (AI, Collision, Pathfinding)
- Identify per-frame allocation patterns
- **Use when:** Investigating frame spikes, performance issues

**Note:** For thread safety validation (data races, deadlocks), use ThreadSanitizer instead of AddressSanitizer. See TSAN section below.

### Mode 3: Full Memory Profile (15-30 minutes)
- Run valgrind massif (heap profiler)
- Detailed memory usage over time
- Peak memory identification
- System-by-system breakdown
- **Use when:** Release preparation, major optimizations

### Mode 4: Buffer Reuse Audit (10-15 minutes)
- Scan code for buffer reuse patterns
- Verify member variables for hot-path buffers
- Check for `clear()` vs reconstruction
- Identify missing `reserve()` calls
- **Use when:** After adding new managers, performance optimization

## Step 1: Gather User Input

Use AskUserQuestion to determine profiling scope:

**Question 1: Profiling Mode**
- Header: "Mode"
- Question: "What type of memory profiling do you want?"
- Options:
  - "Quick Leak Check" (2-5 min, daily use)
  - "Allocation Profiling" (5-10 min, frame spike investigation)
  - "Full Memory Profile" (15-30 min, comprehensive analysis)
  - "Buffer Reuse Audit" (10-15 min, pattern verification)
- multiSelect: false

**Question 2: Test Scope**
- Header: "Scope"
- Question: "Which systems should be profiled?"
- Options:
  - "Core Tests Only" (Thread, Buffer, Event tests)
  - "AI System" (AI optimization, behavior tests)
  - "Collision/Pathfinding" (Collision, pathfinding tests)
  - "All Systems" (Full test suite)
- multiSelect: false

**Question 3: Baseline Comparison**
- Header: "Baseline"
- Question: "Compare against baseline memory metrics?"
- Options:
  - "Yes - Compare" (shows trends)
  - "No - Just current analysis"
  - "Create new baseline" (save current as baseline)
- multiSelect: false

## Step 2: Execute Profiling Based on Mode

### Mode 1: Quick Leak Check

**2a. Ensure Debug Build Exists**
```bash
# Check if debug build exists
if [ ! -f "./bin/debug/thread_system_tests" ]; then
    echo "Debug build not found. Building..."
    cmake -B build/ -G Ninja -DCMAKE_BUILD_TYPE=Debug && ninja -C build
fi
```

**2b. Run Valgrind Memcheck**

**Test Selection Based on Scope:**
- **Core Tests Only:**
  ```bash
  TEST_EXECUTABLES=(
      "./bin/debug/thread_system_tests"
      "./bin/debug/buffer_utilization_tests"
      "./bin/debug/event_manager_tests"
  )
  ```

- **AI System:**
  ```bash
  TEST_EXECUTABLES=(
      "./bin/debug/thread_safe_ai_manager_tests"
      "./bin/debug/ai_optimization_tests"
      "./bin/debug/behavior_functionality_tests"
  )
  ```

- **Collision/Pathfinding:**
  ```bash
  TEST_EXECUTABLES=(
      "./bin/debug/collision_system_tests"
      "./bin/debug/pathfinder_manager_tests"
      "./bin/debug/collision_pathfinding_integration_tests"
  )
  ```

- **All Systems:**
  ```bash
  TEST_EXECUTABLES=(
      # Run all test executables in bin/debug/
  )
  ```

**Valgrind Command Template:**
```bash
OUTPUT_DIR="test_results/memory_profiles"
mkdir -p "$OUTPUT_DIR"

for TEST_EXEC in "${TEST_EXECUTABLES[@]}"; do
    TEST_NAME=$(basename "$TEST_EXEC")
    echo "Running valgrind on $TEST_NAME..."

    valgrind \
        --leak-check=full \
        --show-leak-kinds=all \
        --track-origins=yes \
        --verbose \
        --log-file="$OUTPUT_DIR/${TEST_NAME}_memcheck.log" \
        "$TEST_EXEC" --log_level=test_suite \
        2>&1 | tee "$OUTPUT_DIR/${TEST_NAME}_output.txt"
done
```

**Valgrind Flags Explained:**
- `--leak-check=full`: Detailed leak information
- `--show-leak-kinds=all`: Show all leak types (definite, indirect, possible, reachable)
- `--track-origins=yes`: Track origin of uninitialized values
- `--verbose`: Detailed output
- `--log-file`: Save valgrind output to file

**2c. Parse Valgrind Output**

**Extract Key Metrics:**
```bash
# Parse all memcheck logs
for LOG in "$OUTPUT_DIR"/*_memcheck.log; do
    TEST_NAME=$(basename "$LOG" _memcheck.log)

    echo "=== $TEST_NAME ==="

    # Definite leaks (CRITICAL)
    DEFINITE_LEAKS=$(grep "definitely lost:" "$LOG" | tail -1 | awk '{print $4, $5}')
    echo "Definite leaks: $DEFINITE_LEAKS"

    # Indirect leaks
    INDIRECT_LEAKS=$(grep "indirectly lost:" "$LOG" | tail -1 | awk '{print $4, $5}')
    echo "Indirect leaks: $INDIRECT_LEAKS"

    # Possible leaks
    POSSIBLE_LEAKS=$(grep "possibly lost:" "$LOG" | tail -1 | awk '{print $4, $5}')
    echo "Possible leaks: $POSSIBLE_LEAKS"

    # Still reachable (not critical)
    REACHABLE=$(grep "still reachable:" "$LOG" | tail -1 | awk '{print $4, $5}')
    echo "Still reachable: $REACHABLE"

    # Total heap usage
    TOTAL_HEAP=$(grep "total heap usage:" "$LOG" | tail -1)
    echo "Heap usage: $TOTAL_HEAP"

    # Invalid reads/writes (CRITICAL)
    INVALID_READ=$(grep -c "Invalid read" "$LOG")
    INVALID_WRITE=$(grep -c "Invalid write" "$LOG")
    echo "Invalid reads: $INVALID_READ"
    echo "Invalid writes: $INVALID_WRITE"

    echo ""
done
```

**Severity Classification:**
- **CRITICAL (Block merge):**
  - Definite leaks > 0 bytes
  - Invalid reads/writes > 0
  - Use after free

- **WARNING (Review required):**
  - Indirect leaks > 100 bytes
  - Possible leaks > 1 KB
  - Uninitialized value usage

- **INFO (Monitor):**
  - Still reachable < 10 KB (static globals, SDL resources)

---

### Mode 2: Allocation Profiling

**2a. Build with AddressSanitizer**

```bash
echo "Building with AddressSanitizer..."

# Clean build
rm -rf build/

# Configure with ASan
cmake -B build/ -G Ninja \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_CXX_FLAGS="-D_GLIBCXX_DEBUG -fsanitize=address -fno-omit-frame-pointer -g" \
    -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address" \
    -DUSE_MOLD_LINKER=OFF

# Build
ninja -C build
```

**Why AddressSanitizer for Allocation Profiling:**
- Tracks every allocation with stack traces
- Detects heap-buffer-overflow (buffer overruns)
- Catches use-after-free
- Identifies double-free
- ~2x slowdown (acceptable for profiling)

**2b. Run Tests with ASan**

```bash
OUTPUT_DIR="test_results/memory_profiles"
mkdir -p "$OUTPUT_DIR"

# Set ASan options
export ASAN_OPTIONS="detect_leaks=1:symbolize=1:log_path=$OUTPUT_DIR/asan"

for TEST_EXEC in "${TEST_EXECUTABLES[@]}"; do
    TEST_NAME=$(basename "$TEST_EXEC")
    echo "Running ASan on $TEST_NAME..."

    "$TEST_EXEC" --log_level=test_suite 2>&1 | tee "$OUTPUT_DIR/${TEST_NAME}_asan_output.txt"
done

unset ASAN_OPTIONS
```

**2c. Parse ASan Output**

**Look for allocation patterns:**
```bash
for OUTPUT in "$OUTPUT_DIR"/*_asan_output.txt; do
    TEST_NAME=$(basename "$OUTPUT" _asan_output.txt)

    echo "=== $TEST_NAME ASan Analysis ==="

    # Heap buffer overflow
    BUFFER_OVERFLOW=$(grep -c "heap-buffer-overflow" "$OUTPUT")
    if [ "$BUFFER_OVERFLOW" -gt 0 ]; then
        echo "🔴 CRITICAL: $BUFFER_OVERFLOW heap buffer overflows detected"
        grep -A 10 "heap-buffer-overflow" "$OUTPUT"
    fi

    # Use after free
    USE_AFTER_FREE=$(grep -c "heap-use-after-free" "$OUTPUT")
    if [ "$USE_AFTER_FREE" -gt 0 ]; then
        echo "🔴 CRITICAL: $USE_AFTER_FREE use-after-free detected"
        grep -A 10 "heap-use-after-free" "$OUTPUT"
    fi

    # Double free
    DOUBLE_FREE=$(grep -c "attempting double-free" "$OUTPUT")
    if [ "$DOUBLE_FREE" -gt 0 ]; then
        echo "🔴 CRITICAL: $DOUBLE_FREE double-free detected"
        grep -A 10 "attempting double-free" "$OUTPUT"
    fi

    # Allocation summary
    grep "alloc-dealloc-mismatch" "$OUTPUT" || echo "✅ No alloc-dealloc mismatches"

    echo ""
done
```

**2d. Identify Per-Frame Allocation Hotspots**

**Search for hot-path allocations in code:**
```bash
echo "=== Per-Frame Allocation Hotspot Analysis ==="

# Check for allocations in update loops
echo "Searching for potential per-frame allocations..."

# AIManager update loop
grep -n "std::vector" src/managers/AIManager.cpp | grep -i "update\|process" || echo "✅ AIManager: No obvious vector allocations in update"

# CollisionManager
grep -n "std::vector" src/managers/CollisionManager.cpp | grep -i "update\|detect" || echo "✅ CollisionManager: No obvious vector allocations in update"

# ParticleManager
grep -n "std::vector" src/managers/ParticleManager.cpp | grep -i "update\|render" || echo "✅ ParticleManager: No obvious vector allocations in update"

# Look for allocations inside loops
echo ""
echo "Checking for allocations inside loops (MAJOR ISSUE)..."
grep -A 5 "for\|while" src/managers/*.cpp | grep "std::vector\|std::make" | head -20
```

**Per-Frame Allocation Patterns to Flag:**
```cpp
// 🔴 BAD: Allocates every frame
void update() {
    std::vector<Data> buffer;  // Fresh allocation
    buffer.reserve(entityCount);
    // ... use buffer
}  // Deallocation

// 🔴 BAD: Allocation in loop
for (size_t i = 0; i < count; ++i) {
    std::vector<Item> items;  // Allocation per iteration!
    // ...
}

// 🔴 BAD: No reserve before push_back loop
std::vector<Entity> entities;
for (...) {
    entities.push_back(entity);  // Incremental reallocations
}
```

---

### Mode 2b: Thread Safety Validation (ThreadSanitizer)

**Use ThreadSanitizer (TSAN) for:**
- Data race detection in multi-threaded code
- Deadlock detection
- Thread synchronization issues
- **Use when:** Testing threading systems (AIManager, EventManager, ParticleManager threading tests)

**Important:** ThreadSanitizer and AddressSanitizer are **mutually exclusive** - use one or the other, not both.

**2a. Build with ThreadSanitizer**

```bash
echo "Building with ThreadSanitizer..."

# Clean build
rm -rf build/

# Configure with TSan
cmake -B build/ -G Ninja \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_CXX_FLAGS="-D_GLIBCXX_DEBUG -fsanitize=thread -fno-omit-frame-pointer -g" \
    -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=thread" \
    -DUSE_MOLD_LINKER=OFF

# Build
ninja -C build
```

**Why ThreadSanitizer:**
- Detects data races at runtime (reads/writes without synchronization)
- Finds deadlocks and lock order violations
- Validates thread-safe container usage
- ~5-15x slowdown (acceptable for thread safety validation)

**2b. Run Threading Tests with TSan**

```bash
OUTPUT_DIR="test_results/memory_profiles"
mkdir -p "$OUTPUT_DIR"

# Threading-focused tests
THREAD_TESTS=(
    "./bin/debug/thread_system_tests"
    "./bin/debug/thread_safe_ai_manager_tests"
    "./bin/debug/thread_safe_ai_integration_tests"
    "./bin/debug/particle_manager_threading_tests"
    "./bin/debug/event_coordination_integration_tests"
)

for TEST_EXEC in "${THREAD_TESTS[@]}"; do
    TEST_NAME=$(basename "$TEST_EXEC")
    echo "Running TSan on $TEST_NAME..."

    "$TEST_EXEC" --log_level=test_suite 2>&1 | tee "$OUTPUT_DIR/${TEST_NAME}_tsan_output.txt"
done
```

**2c. Parse TSan Output**

**Look for thread safety violations:**
```bash
for OUTPUT in "$OUTPUT_DIR"/*_tsan_output.txt; do
    TEST_NAME=$(basename "$OUTPUT" _tsan_output.txt)

    echo "=== $TEST_NAME TSan Analysis ==="

    # Data races
    DATA_RACES=$(grep -c "WARNING: ThreadSanitizer: data race" "$OUTPUT")
    if [ "$DATA_RACES" -gt 0 ]; then
        echo "🔴 CRITICAL: $DATA_RACES data race(s) detected"
        grep -A 15 "WARNING: ThreadSanitizer: data race" "$OUTPUT"
    fi

    # Deadlocks
    DEADLOCKS=$(grep -c "WARNING: ThreadSanitizer: lock-order-inversion" "$OUTPUT")
    if [ "$DEADLOCKS" -gt 0 ]; then
        echo "🔴 CRITICAL: $DEADLOCKS potential deadlock(s) detected"
        grep -A 15 "WARNING: ThreadSanitizer: lock-order-inversion" "$OUTPUT"
    fi

    # Thread leaks
    THREAD_LEAKS=$(grep -c "WARNING: ThreadSanitizer: thread leak" "$OUTPUT")
    if [ "$THREAD_LEAKS" -gt 0 ]; then
        echo "⚠️  WARNING: $THREAD_LEAKS thread leak(s) detected"
    fi

    if [ "$DATA_RACES" -eq 0 ] && [ "$DEADLOCKS" -eq 0 ] && [ "$THREAD_LEAKS" -eq 0 ]; then
        echo "✅ No thread safety issues detected"
    fi

    echo ""
done
```

**Severity Classification:**
- **CRITICAL (Block merge):**
  - Data races (concurrent reads/writes without synchronization)
  - Deadlocks or lock-order inversions

- **WARNING (Review required):**
  - Thread leaks (threads not properly joined)
  - Signal-unsafe function calls

---

### Mode 3: Full Memory Profile (Massif)

**3a. Run Valgrind Massif**

```bash
OUTPUT_DIR="test_results/memory_profiles"
mkdir -p "$OUTPUT_DIR"

for TEST_EXEC in "${TEST_EXECUTABLES[@]}"; do
    TEST_NAME=$(basename "$TEST_EXEC")
    echo "Running massif on $TEST_NAME..."

    valgrind \
        --tool=massif \
        --massif-out-file="$OUTPUT_DIR/${TEST_NAME}_massif.out" \
        --time-unit=ms \
        --detailed-freq=1 \
        --max-snapshots=100 \
        --threshold=0.1 \
        "$TEST_EXEC" --log_level=test_suite
done
```

**Massif Flags:**
- `--tool=massif`: Heap profiler
- `--time-unit=ms`: Time in milliseconds
- `--detailed-freq=1`: Detailed snapshot frequency
- `--max-snapshots=100`: Store up to 100 snapshots
- `--threshold=0.1`: Capture 0.1% heap changes

**3b. Parse Massif Output**

```bash
for MASSIF in "$OUTPUT_DIR"/*_massif.out; do
    TEST_NAME=$(basename "$MASSIF" _massif.out)

    echo "=== $TEST_NAME Massif Analysis ==="

    # Generate text report
    ms_print "$MASSIF" > "$OUTPUT_DIR/${TEST_NAME}_massif_report.txt"

    # Extract peak memory
    PEAK_MEM=$(grep "peak" "$MASSIF" | head -1)
    echo "Peak memory: $PEAK_MEM"

    # Extract allocation sites (top 10)
    echo ""
    echo "Top 10 allocation sites:"
    ms_print "$MASSIF" | grep -A 1 "->.*%" | head -20

    echo ""
done
```

**3c. System-by-System Breakdown**

**Extract memory usage by manager:**
```bash
echo "=== Memory Usage by System ==="

# Parse massif reports for specific managers
for REPORT in "$OUTPUT_DIR"/*_massif_report.txt; do
    echo ""
    echo "Report: $(basename "$REPORT")"

    # AIManager allocations
    AI_ALLOCS=$(grep -c "AIManager" "$REPORT")
    echo "  AIManager allocations: $AI_ALLOCS"

    # CollisionManager allocations
    COLLISION_ALLOCS=$(grep -c "CollisionManager" "$REPORT")
    echo "  CollisionManager allocations: $COLLISION_ALLOCS"

    # PathfinderManager allocations
    PATHFINDER_ALLOCS=$(grep -c "PathfinderManager" "$REPORT")
    echo "  PathfinderManager allocations: $PATHFINDER_ALLOCS"

    # EventManager allocations
    EVENT_ALLOCS=$(grep -c "EventManager" "$REPORT")
    echo "  EventManager allocations: $EVENT_ALLOCS"

    # ParticleManager allocations
    PARTICLE_ALLOCS=$(grep -c "ParticleManager" "$REPORT")
    echo "  ParticleManager allocations: $PARTICLE_ALLOCS"
done
```

---

### Mode 4: Buffer Reuse Audit

**4a. Scan for Buffer Reuse Patterns**

**Search for reusable buffers (member variables):**
```bash
echo "=== Buffer Reuse Pattern Audit ==="

# Find all manager classes
MANAGERS=$(find include/managers -name "*.hpp" -type f)

for MANAGER in $MANAGERS; do
    MANAGER_NAME=$(basename "$MANAGER" .hpp)
    echo ""
    echo "=== $MANAGER_NAME ==="

    # Check for member vector variables (potential reuse buffers)
    echo "Member vectors (should be reused):"
    grep "std::vector" "$MANAGER" | grep "m_" | head -10

    # Check implementation for clear() usage
    CPP_FILE="src/managers/${MANAGER_NAME}.cpp"
    if [ -f "$CPP_FILE" ]; then
        CLEAR_COUNT=$(grep -c "\.clear()" "$CPP_FILE")
        echo "clear() calls: $CLEAR_COUNT (good - reuses capacity)"

        # Flag missing reserve() calls
        RESERVE_COUNT=$(grep -c "\.reserve(" "$CPP_FILE")
        echo "reserve() calls: $RESERVE_COUNT"

        if [ "$RESERVE_COUNT" -eq 0 ]; then
            echo "⚠️  WARNING: No reserve() calls found - check for incremental reallocations"
        fi
    fi
done
```

**4b. Check for Buffer Reuse Anti-Patterns**

**Common anti-patterns:**
```bash
echo ""
echo "=== Checking for Anti-Patterns ==="

# Anti-pattern 1: Local vectors in update functions
echo "1. Local vectors in update functions (should be members):"
grep -n "void.*update\|void.*process" src/managers/*.cpp | while read -r line; do
    FILE=$(echo "$line" | cut -d: -f1)
    LINE_NUM=$(echo "$line" | cut -d: -f2)

    # Check 20 lines after function definition for std::vector
    sed -n "${LINE_NUM},$((LINE_NUM+20))p" "$FILE" | grep -n "std::vector" | while read -r vec_line; do
        echo "  $FILE:$((LINE_NUM + $(echo "$vec_line" | cut -d: -f1))) - Local vector in update"
    done
done

# Anti-pattern 2: Vector reconstruction instead of clear()
echo ""
echo "2. Vector reconstruction (use clear() instead):"
for CPP in src/managers/*.cpp; do
    # Look for pattern: vectorName = std::vector<Type>();
    grep -n "= std::vector<" "$CPP" | head -5
done

# Anti-pattern 3: Push_back without reserve
echo ""
echo "3. push_back loops without prior reserve():"
for CPP in src/managers/*.cpp; do
    echo "  Checking $CPP..."
    # This is approximate - look for push_back in loops
    grep -B 5 "push_back" "$CPP" | grep "for\|while" | head -3
done
```

**4c. Verify CLAUDE.md Buffer Patterns**

**Good patterns from CLAUDE.md:**
```bash
echo ""
echo "=== Verifying CLAUDE.md Buffer Patterns ==="

# Pattern 1: Member variables for hot-path buffers
echo "1. Checking for member buffer variables..."
for MANAGER in include/managers/*.hpp; do
    MANAGER_NAME=$(basename "$MANAGER" .hpp)
    MEMBER_BUFFERS=$(grep "m_.*Buffer\|m_.*Cache\|m_.*Results" "$MANAGER" | wc -l)
    echo "  $MANAGER_NAME: $MEMBER_BUFFERS reusable buffers"
done

# Pattern 2: clear() over reconstruction
echo ""
echo "2. Checking clear() usage (capacity preservation)..."
for CPP in src/managers/*.cpp; do
    CLEAR_COUNT=$(grep -c "\.clear()" "$CPP")
    RECONSTRUCT_COUNT=$(grep -c "= std::vector" "$CPP")
    echo "  $(basename "$CPP"): clear() = $CLEAR_COUNT, reconstruct = $RECONSTRUCT_COUNT"

    if [ "$RECONSTRUCT_COUNT" -gt "$CLEAR_COUNT" ]; then
        echo "    ⚠️  More reconstructions than clears - check for capacity loss"
    fi
done

# Pattern 3: reserve() before loops
echo ""
echo "3. Checking reserve() before insertion loops..."
for CPP in src/managers/*.cpp; do
    echo "  $(basename "$CPP"):"
    grep -B 3 "for.*push_back\|while.*push_back" "$CPP" | grep "reserve(" || echo "    ⚠️  No reserve() found before push_back loops"
done
```

---

## Step 3: Baseline Comparison (if requested)

**3a. Load Baseline Metrics**

```bash
BASELINE_DIR="test_results/memory_profiles/baseline"

if [ -d "$BASELINE_DIR" ] && [ "$COMPARE_BASELINE" = "Yes" ]; then
    echo "=== Baseline Comparison ==="

    # Compare leak counts
    for LOG in "$OUTPUT_DIR"/*_memcheck.log; do
        TEST_NAME=$(basename "$LOG" _memcheck.log)
        BASELINE_LOG="$BASELINE_DIR/${TEST_NAME}_memcheck.log"

        if [ -f "$BASELINE_LOG" ]; then
            echo ""
            echo "Test: $TEST_NAME"

            # Current leaks
            CURRENT_LEAKS=$(grep "definitely lost:" "$LOG" | tail -1 | awk '{print $4}')
            CURRENT_LEAKS=${CURRENT_LEAKS:-0}

            # Baseline leaks
            BASELINE_LEAKS=$(grep "definitely lost:" "$BASELINE_LOG" | tail -1 | awk '{print $4}')
            BASELINE_LEAKS=${BASELINE_LEAKS:-0}

            # Compare
            if [ "$CURRENT_LEAKS" -gt "$BASELINE_LEAKS" ]; then
                DELTA=$((CURRENT_LEAKS - BASELINE_LEAKS))
                echo "  🔴 REGRESSION: +$DELTA bytes leaked (was $BASELINE_LEAKS, now $CURRENT_LEAKS)"
            elif [ "$CURRENT_LEAKS" -lt "$BASELINE_LEAKS" ]; then
                DELTA=$((BASELINE_LEAKS - CURRENT_LEAKS))
                echo "  🟢 IMPROVEMENT: -$DELTA bytes leaked (was $BASELINE_LEAKS, now $CURRENT_LEAKS)"
            else
                echo "  ⚪ STABLE: $CURRENT_LEAKS bytes leaked (unchanged)"
            fi

            # Compare heap usage
            CURRENT_HEAP=$(grep "total heap usage:" "$LOG" | tail -1 | awk '{print $5}')
            BASELINE_HEAP=$(grep "total heap usage:" "$BASELINE_LOG" | tail -1 | awk '{print $5}')

            if [ ! -z "$CURRENT_HEAP" ] && [ ! -z "$BASELINE_HEAP" ]; then
                HEAP_DELTA=$((CURRENT_HEAP - BASELINE_HEAP))
                echo "  Total allocs: $CURRENT_HEAP (baseline: $BASELINE_HEAP, delta: $HEAP_DELTA)"
            fi
        fi
    done
fi
```

**3b. Save as New Baseline (if requested)**

```bash
if [ "$BASELINE_MODE" = "Create new baseline" ]; then
    echo ""
    echo "=== Saving New Baseline ==="

    mkdir -p "$BASELINE_DIR"

    # Copy current results to baseline
    cp "$OUTPUT_DIR"/*_memcheck.log "$BASELINE_DIR/" 2>/dev/null || true
    cp "$OUTPUT_DIR"/*_massif.out "$BASELINE_DIR/" 2>/dev/null || true

    # Save metadata
    cat > "$BASELINE_DIR/baseline_metadata.txt" <<EOF
Baseline created: $(date)
Branch: $(git rev-parse --abbrev-ref HEAD)
Commit: $(git rev-parse HEAD)
Tests included: $(ls "$OUTPUT_DIR"/*_memcheck.log | wc -l)
EOF

    echo "✅ Baseline saved to $BASELINE_DIR"
fi
```

---

## Step 4: Generate Memory Profile Report

**Report Structure:**

```markdown
# HammerEngine Memory Profile Report

**Generated:** YYYY-MM-DD HH:MM:SS
**Branch:** <current-branch>
**Commit:** <commit-hash>
**Profiling Mode:** <mode>
**Test Scope:** <scope>

---

## Executive Summary

**Overall Status:** ✅ CLEAN / ⚠️ WARNINGS / 🔴 CRITICAL ISSUES

**Key Findings:**
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Memory Health:** [Excellent/Good/Fair/Poor]

---

## Leak Detection Results

### Critical Leaks (BLOCKING)

| Test | Definite Leaks | Invalid Access | Status |
|------|----------------|----------------|--------|
| [Test 1] | [X bytes] | [N violations] | 🔴/✅ |
| [Test 2] | [X bytes] | [N violations] | 🔴/✅ |

**Total Definite Leaks:** [X bytes] (Target: 0 bytes)

### Leak Details

[For each test with leaks, include:]

**Test:** [test_name]
**Leak Location:** [file:line]
**Stack Trace:**
```
[valgrind stack trace]
```

**Likely Cause:** [Analysis]
**Suggested Fix:** [Specific code change]

---

## Allocation Profiling (if Mode 2)

### Per-Frame Allocation Hotspots

| System | Allocations/Frame | Impact | Status |
|--------|-------------------|--------|--------|
| AIManager | [N] | [Frame spike: Xms] | ⚠️/✅ |
| CollisionManager | [N] | [Frame spike: Xms] | ⚠️/✅ |
| ParticleManager | [N] | [Frame spike: Xms] | ⚠️/✅ |

**Total Per-Frame Allocations:** [N] (Target: 0 in hot paths)

### Anti-Pattern Violations

**1. Local Vectors in Update Functions:**
- `AIManager.cpp:123` - `std::vector<Data> localBuffer;` in `processBatch()`
  - **Fix:** Make `m_processingBuffer` member variable, use `clear()` per frame

**2. Push_back Without Reserve:**
- `CollisionManager.cpp:456` - Loop with `results.push_back()` without `reserve()`
  - **Fix:** Add `results.reserve(expectedCount);` before loop

**3. Vector Reconstruction:**
- `PathfinderManager.cpp:789` - `m_pathCache = std::vector<Path>();`
  - **Fix:** Replace with `m_pathCache.clear();` to preserve capacity

---

## Memory Usage by System (if Mode 3)

### Peak Memory

| System | Peak Allocation | % of Total | Trend |
|--------|----------------|------------|-------|
| AIManager | [X MB] | [%] | 📈/📉/➡️ |
| CollisionManager | [X MB] | [%] | 📈/📉/➡️ |
| PathfinderManager | [X MB] | [%] | 📈/📉/➡️ |
| EventManager | [X MB] | [%] | 📈/📉/➡️ |
| ParticleManager | [X MB] | [%] | 📈/📉/➡️ |
| **Total** | **[X MB]** | **100%** | - |

### Top Allocation Sites

1. **AIManager::processBatch()** - [X MB] ([%] of total)
   - [N] allocations
   - Stack trace: [abbreviated]

2. **CollisionManager::detectCollisions()** - [X MB] ([%] of total)
   - [N] allocations
   - Stack trace: [abbreviated]

---

## Buffer Reuse Audit (if Mode 4)

### Pattern Compliance

| Manager | Member Buffers | clear() Usage | reserve() Usage | Grade |
|---------|----------------|---------------|-----------------|-------|
| AIManager | ✅ Yes | ✅ Correct | ✅ Present | A |
| CollisionManager | ✅ Yes | ⚠️ Partial | ❌ Missing | C |
| ParticleManager | ❌ No | ❌ Local vars | ❌ Missing | F |

**Overall Compliance:** [%] (Target: 100%)

### Recommendations

**AIManager:**
- ✅ Excellent buffer reuse pattern
- Document as reference implementation

**CollisionManager:**
- ⚠️ Add `reserve()` calls in `detectCollisions()` before `results.push_back()` loop
- Estimated improvement: -50 allocs/frame

**ParticleManager:**
- 🔴 Critical: Replace local `std::vector<Particle> activeParticles;` with member `m_activeParticles`
- 🔴 Add `m_activeParticles.clear()` at start of `update()`
- 🔴 Add `reserve(maxParticles)` in constructor
- Estimated improvement: -200 allocs/frame

---

## Baseline Comparison (if applicable)

### Leak Trend

| Test | Baseline | Current | Change | Status |
|------|----------|---------|--------|--------|
| [Test 1] | [X bytes] | [X bytes] | [+/-] | 🔴/🟢/⚪ |

### Memory Usage Trend

[Chart or table showing memory usage over time]

**Overall Trend:** [Improving/Stable/Degrading]

---

## Optimization Opportunities

### High Priority (Immediate Fix)

1. **ParticleManager: Eliminate per-frame allocations**
   - **Current:** 200 allocs/frame (~128 KB/frame)
   - **Impact:** Frame spikes of 5-10ms
   - **Fix:** [Specific code changes]
   - **Expected Improvement:** -5ms frame time

2. **CollisionManager: Add reserve() calls**
   - **Current:** Incremental reallocations in query results
   - **Impact:** 1-2ms overhead
   - **Fix:** [Specific code changes]
   - **Expected Improvement:** -1ms query time

### Medium Priority

3. **AIManager: Increase batch buffer size**
   - **Current:** 1024 entities, reallocs when exceeded
   - **Fix:** Increase to 2048 or make dynamic
   - **Expected Improvement:** Eliminate rare reallocs

### Low Priority

4. **EventManager: Consider event pool**
   - **Current:** Event objects allocated per dispatch
   - **Fix:** Implement object pool for event reuse
   - **Expected Improvement:** -10% event dispatch time

---

## Specific Code Fixes

### Fix 1: ParticleManager Buffer Reuse

**File:** `include/managers/ParticleManager.hpp:45`

**Before:**
```cpp
class ParticleManager
{
    // ... no reusable buffer
};
```

**After:**
```cpp
class ParticleManager
{
    std::vector<Particle> m_activeParticles;  // Reusable buffer
    // ... reserve in constructor
};
```

**File:** `src/managers/ParticleManager.cpp:123`

**Before:**
```cpp
void ParticleManager::update(float deltaTime)
{
    std::vector<Particle> activeParticles;  // Allocation every frame!
    // ... use activeParticles
}
```

**After:**
```cpp
void ParticleManager::update(float deltaTime)
{
    m_activeParticles.clear();  // Reuse capacity
    // ... use m_activeParticles
}
```

**File:** `src/managers/ParticleManager.cpp:34` (constructor)

**Add:**
```cpp
ParticleManager::ParticleManager()
{
    m_activeParticles.reserve(MAX_PARTICLES);  // Pre-allocate
}
```

---

## Test Results Summary

**Tests Run:** [N]
**Tests Passed:** [N]
**Critical Issues:** [N]
**Warnings:** [N]

**Status:** [✅ CLEAN / ⚠️ NEEDS REVIEW / 🔴 FIX REQUIRED]

---

## Action Items

### Critical (Fix Before Commit)
- [ ] [Critical issue 1]
- [ ] [Critical issue 2]

### Important (Fix Soon)
- [ ] [Important issue 1]
- [ ] [Important issue 2]

### Optional (Consider)
- [ ] [Optional improvement 1]
- [ ] [Optional improvement 2]

---

## Files Modified (Recommended)

Based on findings, these files should be modified:

```
include/managers/ParticleManager.hpp      (add member buffer)
src/managers/ParticleManager.cpp          (use buffer, add clear/reserve)
src/managers/CollisionManager.cpp         (add reserve calls)
```

---

## Next Steps

1. **If critical issues:** Fix immediately, re-run profile to verify
2. **If warnings:** Review and plan fixes
3. **If clean:** Update baseline (save as reference)
4. **Consider:** Run full benchmark suite to measure performance impact

**Re-run Profile:**
```bash
# After fixes, re-run to verify
[Command to re-invoke this skill]
```

---

**Report Generated By:** hammer-memory-profiler Skill
**Report Saved To:** `test_results/memory_profiles/memory_profile_YYYY-MM-DD.md`
```

**Save report to:**
```bash
REPORT_FILE="test_results/memory_profiles/memory_profile_$(date +%Y-%m-%d_%H-%M-%S).md"
cat > "$REPORT_FILE" <<'EOF'
[Generated markdown report]
EOF

echo "✅ Memory profile report saved to: $REPORT_FILE"
```

---

## Step 5: Console Summary

**Output to user:**

```
=== HammerEngine Memory Profile ===

Mode: [Mode Name]
Scope: [Test Scope]
Duration: [Time taken]

Overall Status: [✅ CLEAN / ⚠️ WARNINGS / 🔴 CRITICAL]

Critical Issues: [N]
Warnings: [N]

[If critical:]
🔴 CRITICAL ISSUES FOUND - DO NOT COMMIT
  - [Issue 1]
  - [Issue 2]

[If warnings:]
⚠️  WARNINGS DETECTED - REVIEW RECOMMENDED
  - [Warning 1]
  - [Warning 2]

[If clean:]
✅ NO MEMORY ISSUES DETECTED
  - 0 bytes leaked
  - 0 invalid access violations
  - Buffer reuse patterns correct

Memory Usage:
  - Peak: [X MB]
  - Total allocations: [N]
  - Per-frame allocations: [N] (Target: 0)

Top Allocation Sites:
  1. [System] - [X MB]
  2. [System] - [X MB]
  3. [System] - [X MB]

Baseline Comparison: [If applicable]
  - Leaks: [+/-X bytes]
  - Allocations: [+/-N]
  - Trend: [Improving/Stable/Degrading]

Full Report: test_results/memory_profiles/memory_profile_YYYY-MM-DD.md

Next Steps:
  [If critical] - Fix issues and re-run profile
  [If clean] - Update baseline: "update memory baseline"
```

---

## Usage Examples

When the user says:
- "profile memory usage"
- "check for memory leaks"
- "analyze memory allocations"
- "audit buffer reuse patterns"
- "find allocation hotspots"
- "check per-frame allocations"
- "memory profile AI system"

Activate this Skill automatically.

---

## Integration with Development Workflow

**Use this Skill:**

### Daily Development
- Quick leak check before commits
- Catches leaks early (cheaper to fix)

### Performance Investigation
- Allocation profiling when diagnosing frame spikes
- Identifies per-frame allocation culprits

### Major Changes
- Full profile after adding new managers
- Verify memory usage within budget

### Release Preparation
- Comprehensive profile before releases
- Ensure no regressions since last baseline

### Periodic Audits
- Monthly buffer reuse audit
- Maintain code quality over time

---

## Common Memory Issues in HammerEngine

### Issue 1: Per-Frame Allocations (Frame Spikes)

**Symptom:** Periodic frame drops every 1-2 seconds
**Cause:** Heap allocations in update loop triggering OS paging
**Solution:** Member buffer + clear() pattern from CLAUDE.md

### Issue 2: Missing reserve() Calls

**Symptom:** Gradual frame time increase with entity count
**Cause:** Incremental vector reallocations (2x growth pattern)
**Solution:** Pre-calculate size, call reserve() before loop

### Issue 3: SDL Resource Leaks

**Symptom:** "Still reachable" leaks from SDL
**Cause:** Missing SDL_Destroy calls in destructors
**Solution:** Ensure proper cleanup in manager destructors

### Issue 4: Thread-Safe Container Allocations

**Symptom:** Allocation contention visible in profiler
**Cause:** Multiple threads allocating from same heap
**Solution:** Thread-local buffers or per-thread allocators

### Issue 5: Smart Pointer Overhead

**Symptom:** High allocation rate despite buffer reuse
**Cause:** Unnecessary shared_ptr copies (atomic ref-count ops)
**Solution:** Use raw pointers in hot paths (see CLAUDE.md)

---

## Performance Expectations

- **Quick Leak Check:** 2-5 minutes (3-5 core tests)
- **Allocation Profiling:** 5-10 minutes (rebuild + targeted tests)
- **Full Memory Profile:** 15-30 minutes (massif + all systems)
- **Buffer Reuse Audit:** 10-15 minutes (code scanning)

**Manual Equivalent:** 45-90 minutes per profiling session

---

## Exit Codes

- **0:** No memory issues detected
- **1:** Critical leaks detected (BLOCKING)
- **2:** Warnings detected (review required)
- **3:** Buffer reuse violations (performance impact)
- **4:** Baseline comparison shows regression

---

## Important Notes

1. **Always profile in Debug mode** - Release optimizations hide issues
2. **Run on quiet system** - Background processes affect results
3. **Compare against baseline** - Trends matter more than absolutes
4. **Fix critical issues immediately** - Don't accumulate memory debt
5. **Document patterns** - Share good buffer reuse examples

---

**Ready to profile HammerEngine memory usage. Ask user for profiling mode and scope.**
