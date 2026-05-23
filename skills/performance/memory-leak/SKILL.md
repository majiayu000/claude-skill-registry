---
name: memory-leak
description: Memory leak detection and analysis for Node.js, Python, and browsers
disable-model-invocation: false
---

# Memory Leak Detection & Analysis

I'll help you detect, analyze, and fix memory leaks across your application stack.

Arguments: `$ARGUMENTS` - runtime environment (node/python/browser) or specific files

---

## Token Optimization

This skill uses efficient patterns to minimize token consumption during memory leak detection and analysis.

### Optimization Strategies

#### 1. Runtime Detection Caching (Saves 700 tokens per invocation)

Cache detected runtime environment and profiling tools:

```bash
CACHE_FILE=".claude/cache/memory-leak/runtime.json"
CACHE_TTL=86400  # 24 hours

mkdir -p .claude/cache/memory-leak

if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null)))

    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        # Use cached runtime info
        RUNTIME=$(jq -r '.runtime' "$CACHE_FILE")
        VERSION=$(jq -r '.version' "$CACHE_FILE")
        PROFILING_TOOLS=$(jq -r '.profiling_tools' "$CACHE_FILE")

        echo "Using cached runtime: $RUNTIME $VERSION"
        echo "Profiling tools: $PROFILING_TOOLS"

        SKIP_DETECTION="true"
    fi
fi
```

**Savings:** 700 tokens (no repeated package.json reads, no npm list checks)

#### 2. Early Exit for No Leak Pattern (Saves 90%)

Quick memory pattern check before full profiling:

```bash
# Quick check: Is memory growing abnormally?
if [ -f "memory-leak/state.json" ]; then
    LAST_RSS=$(jq -r '.last_snapshot.rss_mb' memory-leak/state.json)
    CURRENT_RSS=$(ps -o rss= -p $APP_PID | awk '{print $1/1024}')

    GROWTH_PERCENT=$(echo "scale=2; ($CURRENT_RSS - $LAST_RSS) / $LAST_RSS * 100" | bc)

    # Early exit if growth < 10%
    if (( $(echo "$GROWTH_PERCENT < 10" | bc -l) )); then
        echo "✓ Memory usage stable (${GROWTH_PERCENT}% growth)"
        echo "  Last: ${LAST_RSS}MB, Current: ${CURRENT_RSS}MB"
        echo ""
        echo "No significant memory leak detected"
        echo "Use --force for full profiling"
        exit 0
    fi
fi
```

**Savings:** 90% when memory stable (skip profiling: 3,000 → 300 tokens)

#### 3. Sample-Based Snapshot Analysis (Saves 85%)

Analyze only key metrics from heap snapshots, not full dump:

```bash
# Efficient: Extract summary from heap snapshot (not full analysis)
analyze_heap_snapshot() {
    local snapshot_file="$1"

    # Parse JSON for key metrics only (efficient)
    SNAPSHOT_SIZE=$(jq '.snapshot.meta.total_size' "$snapshot_file")
    NODE_COUNT=$(jq '.snapshot.node_count' "$snapshot_file")
    EDGE_COUNT=$(jq '.snapshot.edge_count' "$snapshot_file")

    # Find top 5 largest object types (not all types)
    TOP_TYPES=$(jq -r '.nodes | group_by(.type) |
        map({type: .[0].type, total: map(.self_size) | add}) |
        sort_by(.total) | reverse | .[0:5] |
        .[] | "\(.type): \(.total)"' "$snapshot_file")

    echo "Heap Snapshot Summary:"
    echo "  Size: $(numfmt --to=iec $SNAPSHOT_SIZE)"
    echo "  Nodes: $NODE_COUNT"
    echo "  Edges: $EDGE_COUNT"
    echo ""
    echo "Top 5 Object Types:"
    echo "$TOP_TYPES"

    echo ""
    echo "Use --detailed for full heap analysis"
}
```

**Savings:** 85% (summary metrics vs full heap dump: 5,000 → 750 tokens)

#### 4. Bash-Based Memory Monitoring (Saves 75%)

Use `ps` and `top` for memory tracking instead of full profilers:

```bash
# Quick memory check (no profiler needed)
quick_memory_check() {
    local pid="$1"

    # Current memory usage (instant)
    RSS=$(ps -o rss=,vsz= -p $pid | awk '{print $1/1024, $2/1024}')
    RSS_MB=$(echo "$RSS" | cut -d' ' -f1)
    VSZ_MB=$(echo "$RSS" | cut -d' ' -f2)

    # Memory trend (from previous runs)
    if [ -f "memory-leak/trend.log" ]; then
        INITIAL_RSS=$(head -1 memory-leak/trend.log | cut -d',' -f2)
        GROWTH=$(echo "scale=2; $RSS_MB - $INITIAL_RSS" | bc)
        GROWTH_PCT=$(echo "scale=2; $GROWTH / $INITIAL_RSS * 100" | bc)

        echo "Memory Status:"
        echo "  Current: ${RSS_MB}MB RSS, ${VSZ_MB}MB VSZ"
        echo "  Initial: ${INITIAL_RSS}MB"
        echo "  Growth: +${GROWTH}MB (${GROWTH_PCT}%)"
    else
        echo "Memory Status: ${RSS_MB}MB RSS, ${VSZ_MB}MB VSZ"
        echo "  (First measurement - baseline established)"
    fi

    # Append to trend log
    echo "$(date +%s),$RSS_MB,$VSZ_MB" >> memory-leak/trend.log
}
```

**Savings:** 75% vs full profiler (ps/top vs heap snapshot: 2,000 → 500 tokens)

#### 5. Grep-Based Code Scanning (Saves 90%)

Scan for common leak patterns without reading files:

```bash
# Efficient: Grep for leak patterns
scan_leak_patterns() {
    echo "Scanning for common memory leak patterns..."

    local issues=0

    # Event listeners without cleanup
    if grep -q -r "addEventListener\|on(" --include="*.{js,ts}" src/ 2>/dev/null; then
        if ! grep -q "removeEventListener\|off(" --include="*.{js,ts}" src/ 2>/dev/null; then
            echo "⚠️  Event listeners detected without cleanup"
            issues=$((issues + 1))
        fi
    fi

    # Timers without clearInterval/clearTimeout
    if grep -q -r "setInterval\|setTimeout" --include="*.{js,ts}" src/ 2>/dev/null; then
        CLEAR_COUNT=$(grep -c "clearInterval\|clearTimeout" --include="*.{js,ts}" src/ 2>/dev/null)
        if [ "$CLEAR_COUNT" -lt 2 ]; then
            echo "⚠️  Timers without cleanup detected"
            issues=$((issues + 1))
        fi
    fi

    # Global caches without limits
    if grep -q -r "new Map()\|new Set()\|\[\].*cache" --include="*.{js,ts}" src/ 2>/dev/null; then
        echo "💡 Caches detected - verify size limits and TTL"
        issues=$((issues + 1))
    fi

    echo ""
    echo "Potential leak patterns: $issues"
}
```

**Savings:** 90% vs reading all source files (Grep returns matches only)

#### 6. Snapshot Comparison (Only When Needed) (Saves 80%)

Compare snapshots only if multiple exist:

```bash
if [ $(ls memory-leak/snapshots/*.heapsnapshot 2>/dev/null | wc -l) -ge 2 ]; then
    echo "Multiple snapshots available for comparison"

    # Compare only latest 2 (not all)
    LATEST=$(ls -t memory-leak/snapshots/*.heapsnapshot | head -1)
    PREVIOUS=$(ls -t memory-leak/snapshots/*.heapsnapshot | head -2 | tail -1)

    # Extract key metrics only (not full diff)
    LATEST_SIZE=$(jq '.snapshot.meta.total_size' "$LATEST")
    PREV_SIZE=$(jq '.snapshot.meta.total_size' "$PREVIOUS")
    GROWTH=$((LATEST_SIZE - PREV_SIZE))

    echo "Snapshot comparison:"
    echo "  Previous: $(numfmt --to=iec $PREV_SIZE)"
    echo "  Latest: $(numfmt --to=iec $LATEST_SIZE)"
    echo "  Growth: $(numfmt --to=iec $GROWTH)"

else
    echo "Single snapshot - take another for comparison"
    echo "  Run app for 5-10 minutes, then run skill again"
fi
```

**Savings:** 80% (compare 2 snapshots vs all historical data)

#### 7. Progressive Disclosure for Reports (Saves 70%)

Default to summary, provide detailed analysis on demand:

```bash
DETAIL_LEVEL="${DETAIL_LEVEL:-summary}"

case "$DETAIL_LEVEL" in
    summary)
        # Quick summary (400 tokens)
        echo "Memory: ${RSS_MB}MB, Growth: ${GROWTH_PCT}%"
        echo "Potential issues: $ISSUE_COUNT"
        echo ""
        echo "Use --detailed for full analysis"
        ;;

    detailed)
        # Medium detail (1,500 tokens)
        show_memory_trend
        show_leak_patterns
        show_top_allocations
        ;;

    full)
        # Complete analysis (3,000 tokens)
        show_full_heap_analysis
        show_all_leak_patterns
        show_fix_recommendations
        ;;
esac
```

**Savings:** 70% for default runs (400 vs 1,500-3,000 tokens)

### Cache Invalidation

Caches are invalidated when:
- Runtime environment changes (new Node/Python version)
- 24 hours elapsed (time-based for tool detection)
- User runs `--clear-cache` flag
- New profiling tools installed

### Real-World Token Usage

**Typical memory leak workflow:**

1. **Initial detection:** 1,200-2,000 tokens
   - Runtime detection: 400 tokens
   - Quick memory check: 200 tokens
   - Code pattern scan: 400 tokens
   - Recommendations: 400 tokens

2. **Cached environment:** 400-800 tokens
   - Cached runtime: 100 tokens (85% savings)
   - Quick memory check: 200 tokens
   - Trend analysis: 300 tokens

3. **Stable memory (no leak):** 200-400 tokens
   - Early exit: 200 tokens (90% savings)
   - Summary only: 100 tokens

4. **Heap snapshot analysis:** 800-1,500 tokens
   - Snapshot summary: 400 tokens
   - Top 5 object types: 300 tokens
   - Comparison (if available): 400 tokens

5. **Full leak analysis:** 2,000-3,000 tokens
   - Only when explicitly requested with --full flag

**Average usage distribution:**
- 50% of runs: Stable memory, early exit (200-400 tokens) ✅ Most common
- 30% of runs: Cached quick check (400-800 tokens)
- 15% of runs: Snapshot analysis (800-1,500 tokens)
- 5% of runs: Full leak investigation (2,000-3,000 tokens)

**Expected token range:** 200-2,000 tokens (50% reduction from 400-4,000 baseline)

### Progressive Disclosure

Three levels of detail:

1. **Default (summary):** Memory status + quick scan
   ```bash
   claude "/memory-leak"
   # Shows: current memory, growth %, potential issues
   # Tokens: 400-800
   ```

2. **Detailed (medium):** Trend + pattern analysis
   ```bash
   claude "/memory-leak --detailed"
   # Shows: memory trend, leak patterns, top allocations
   # Tokens: 1,200-1,500
   ```

3. **Full (exhaustive):** Complete heap analysis
   ```bash
   claude "/memory-leak --full"
   # Shows: full heap dump analysis, all patterns, comprehensive fixes
   # Tokens: 2,000-3,000
   ```

### Implementation Notes

**Key patterns applied:**
- ✅ Runtime detection caching (700 token savings)
- ✅ Early exit for stable memory (90% reduction)
- ✅ Sample-based snapshot analysis (85% savings)
- ✅ Bash-based memory monitoring (75% savings)
- ✅ Grep-based code scanning (90% savings)
- ✅ Minimal snapshot comparison (80% savings)
- ✅ Progressive disclosure (70% savings on default)

**Cache locations:**
- `.claude/cache/memory-leak/runtime.json` - Runtime environment and tools
- `memory-leak/trend.log` - Memory usage timeline (project-specific)
- `memory-leak/state.json` - Last profiling state (project-specific)

**Flags:**
- `--force` - Force full profiling even if memory stable
- `--detailed` - Medium detail level (trend + patterns)
- `--full` - Complete heap analysis
- `--clear-cache` - Force cache invalidation
- `--snapshot` - Take new heap snapshot

**Runtime-specific:**
- Node.js: V8 heap snapshots, process.memoryUsage()
- Python: tracemalloc, memory_profiler
- Browser: Chrome DevTools memory profiler

---

## Session Intelligence

I'll maintain memory profiling sessions for tracking leaks over time:

**Session Files (in current project directory):**
- `memory-leak/profile.md` - Memory analysis and findings
- `memory-leak/state.json` - Profiling data and progress
- `memory-leak/snapshots/` - Heap snapshots and memory dumps

**IMPORTANT:** Session files are stored in a `memory-leak` folder in your current project root

**Auto-Detection:**
- If session exists: Compare with previous profiles
- If no session: Perform initial memory analysis
- Commands: `resume`, `analyze`, `compare`, `new`

## Phase 1: Runtime Detection & Setup

### Extended Thinking for Memory Analysis

For complex memory leak scenarios, I'll use extended thinking to understand patterns:

<think>
When analyzing memory leaks:
- Closure scopes that unintentionally retain references
- Event listener accumulation without cleanup
- Cache implementations without size limits or TTL
- Circular references preventing garbage collection
- Large object graphs held in memory
- Module-level state accumulation
- Timer/interval leaks from abandoned subscriptions
- DOM node retention in Single Page Applications
</think>

**Triggers for Extended Analysis:**
- Long-running server applications
- Real-time data processing systems
- Browser applications with complex state
- Applications with significant memory growth over time

I'll automatically detect your runtime environment:

**Node.js Detection:**
```bash
# Check for Node.js project
if [ -f "package.json" ]; then
    echo "Node.js project detected"
    node_version=$(node --version 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "Node.js $node_version available"
        # Check for profiling tools
        npm list --depth=0 | grep -E "(heapdump|clinic|memwatch|node-inspect)"
    fi
fi
```

**Python Detection:**
```bash
# Check for Python project
if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    echo "Python project detected"
    python_version=$(python3 --version 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$python_version available"
        # Check for profiling modules
        python3 -c "import tracemalloc, memory_profiler" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Memory profiling modules available"
        fi
    fi
fi
```

**Browser Detection:**
```bash
# Check for frontend project
if [ -f "package.json" ]; then
    if grep -qE "(react|vue|angular|svelte)" package.json; then
        echo "Frontend framework detected"
        echo "Browser memory profiling available via Chrome DevTools"
    fi
fi
```

## Phase 2: Memory Profiling Setup

Based on detected environment, I'll configure appropriate profiling:

### Node.js Memory Profiling

**Built-in Inspector:**
```javascript
// Enable heap profiling
node --inspect --expose-gc your-app.js

// Programmatic heap snapshot
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(filename) {
    const snapshotStream = v8.writeHeapSnapshot();
    console.log(`Heap snapshot written to ${snapshotStream}`);
    return snapshotStream;
}

// Take snapshots at intervals
setInterval(() => {
    takeHeapSnapshot(`memory-leak/snapshots/heap-${Date.now()}.heapsnapshot`);
}, 60000);
```

**Heapdump Integration:**
```javascript
const heapdump = require('heapdump');
const path = require('path');

// Trigger on signal
process.on('SIGUSR2', () => {
    const filename = path.join(
        'memory-leak/snapshots',
        `heap-${Date.now()}.heapsnapshot`
    );
    heapdump.writeSnapshot(filename, (err, filepath) => {
        if (err) console.error(err);
        else console.log(`Heap snapshot written to ${filepath}`);
    });
});
```

**Memory Usage Monitoring:**
```javascript
function monitorMemory() {
    const usage = process.memoryUsage();
    return {
        timestamp: new Date().toISOString(),
        rss: Math.round(usage.rss / 1024 / 1024) + ' MB',
        heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + ' MB',
        heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + ' MB',
        external: Math.round(usage.external / 1024 / 1024) + ' MB',
        arrayBuffers: Math.round(usage.arrayBuffers / 1024 / 1024) + ' MB'
    };
}

// Log memory every minute
setInterval(() => {
    console.log('Memory usage:', JSON.stringify(monitorMemory()));
}, 60000);
```

### Python Memory Profiling

**tracemalloc (Built-in):**
```python
import tracemalloc
import linecache

def start_memory_tracking():
    tracemalloc.start()

def take_memory_snapshot():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 memory consuming lines ]")
    for stat in top_stats[:10]:
        print(stat)

    return snapshot

def compare_snapshots(snapshot1, snapshot2):
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("[ Top 10 memory growth areas ]")
    for stat in top_stats[:10]:
        print(stat)
```

**memory_profiler:**
```python
from memory_profiler import profile

@profile
def potentially_leaky_function():
    # Function to analyze
    pass

# Run with: python -m memory_profiler your_script.py
```

**objgraph for Reference Tracking:**
```python
import objgraph
import gc

def analyze_object_growth():
    # Show most common types
    objgraph.show_most_common_types()

    # Track object growth
    objgraph.show_growth()

    # Find reference chains keeping objects alive
    roots = objgraph.get_leaking_objects()
    print(f"Found {len(roots)} potentially leaked objects")
```

### Browser Memory Profiling

**Chrome DevTools Integration:**
I'll guide you through browser memory analysis:

1. **Heap Snapshot Workflow:**
   - Take snapshot before action
   - Perform suspected leaky operation
   - Take snapshot after action
   - Compare snapshots for retained objects

2. **Allocation Timeline:**
   - Record allocation timeline
   - Perform operations
   - Identify object allocations that weren't freed

3. **Memory Panel Analysis:**
   - Monitor memory usage in real-time
   - Identify memory spikes and growth trends
   - Track garbage collection effectiveness

**Common Browser Leak Patterns:**
```javascript
// Pattern 1: Event listener leaks
class LeakyComponent {
    constructor() {
        // BAD: Never removed
        window.addEventListener('resize', this.handleResize);
    }

    // FIX: Cleanup in destroy
    destroy() {
        window.removeEventListener('resize', this.handleResize);
    }
}

// Pattern 2: Timer leaks
function leakyFunction() {
    // BAD: Interval never cleared
    setInterval(() => {
        console.log('Running...');
    }, 1000);
}

// Pattern 3: Detached DOM nodes
let cache = [];
function cacheElement() {
    // BAD: Keeps DOM nodes in memory after removal
    cache.push(document.getElementById('temp'));
}
```

## Phase 3: Leak Detection Analysis

I'll analyze memory patterns to identify leaks:

**Detection Strategies:**

1. **Heap Growth Analysis:**
   - Monitor heap size over time
   - Identify continuous growth without GC recovery
   - Compare heap snapshots

2. **Retained Object Analysis:**
   - Find objects that should be garbage collected
   - Trace retention paths
   - Identify unexpected references

3. **Circular Reference Detection:**
   - Scan for circular reference patterns
   - Check for manual cleanup requirements
   - Suggest WeakMap/WeakRef solutions

4. **Event Listener Auditing:**
   - Count active event listeners
   - Match add/remove pairs
   - Find orphaned listeners

**Analysis Output:**
```markdown
# Memory Leak Analysis Report

## Executive Summary
- **Environment**: Node.js 20.10.0
- **Analysis Duration**: 30 minutes
- **Leak Detected**: YES
- **Severity**: HIGH
- **Memory Growth**: 45 MB/hour

## Leak Sources Identified

### 1. Event Listener Accumulation
- **Location**: `src/services/WebSocketService.js:45`
- **Issue**: Socket event listeners not removed on disconnect
- **Impact**: ~2 MB per connection
- **Retention Path**: `EventEmitter -> handler -> closure -> largeDataBuffer`

### 2. Cache Without Limits
- **Location**: `src/cache/ResponseCache.js:23`
- **Issue**: Unbounded in-memory cache
- **Impact**: ~15 MB/hour growth
- **Retention Path**: `Map -> CacheEntry -> responseBody`

### 3. Circular References
- **Location**: `src/models/User.js:67`
- **Issue**: Parent-child circular references
- **Impact**: Prevents GC, accumulates 5 MB/hour
- **Retention Path**: `User -> friends[] -> User`

## Recommendations
[Detailed fix recommendations...]
```

## Phase 4: Integration with Performance Profiling

**Cross-Skill Integration:**
```bash
# When memory leaks impact performance
/memory-leak analyze    # Detect memory issues
/performance-profile    # Check CPU/runtime impact
```

I'll coordinate analysis across both dimensions:
- Memory leaks causing GC pressure
- Performance degradation from memory churn
- Optimization opportunities from profiling data

## Phase 5: Leak Remediation

I'll help fix identified leaks systematically:

**Fix Pattern 1: Proper Cleanup**
```javascript
// BEFORE: Leak
class Component {
    constructor() {
        this.timer = setInterval(this.update, 1000);
        window.addEventListener('resize', this.handleResize);
    }
}

// AFTER: Fixed
class Component {
    constructor() {
        this.timer = setInterval(this.update, 1000);
        this.handleResize = this.handleResize.bind(this);
        window.addEventListener('resize', this.handleResize);
    }

    destroy() {
        clearInterval(this.timer);
        window.removeEventListener('resize', this.handleResize);
        this.timer = null;
    }
}
```

**Fix Pattern 2: Bounded Caches**
```javascript
// BEFORE: Unbounded
const cache = new Map();

function cacheResponse(key, data) {
    cache.set(key, data);
}

// AFTER: LRU Cache with limits
class LRUCache {
    constructor(maxSize = 100) {
        this.cache = new Map();
        this.maxSize = maxSize;
    }

    set(key, value) {
        if (this.cache.size >= this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        this.cache.set(key, value);
    }
}
```

**Fix Pattern 3: WeakRef for Circular References**
```javascript
// BEFORE: Strong circular reference
class User {
    constructor(name) {
        this.name = name;
        this.friends = [];
    }

    addFriend(user) {
        this.friends.push(user);
        user.friends.push(this); // Circular reference
    }
}

// AFTER: WeakRef to break cycle
class User {
    constructor(name) {
        this.name = name;
        this.friends = [];
    }

    addFriend(user) {
        this.friends.push(new WeakRef(user));
        user.friends.push(new WeakRef(this));
    }

    getFriends() {
        return this.friends
            .map(ref => ref.deref())
            .filter(friend => friend !== undefined);
    }
}
```

**Fix Pattern 4: Cleanup in Python**
```python
# BEFORE: Leak
class DataProcessor:
    def __init__(self):
        self.cache = {}
        self.connections = []

    def process(self, data):
        self.cache[data.id] = data  # Never cleaned

# AFTER: Context manager and cleanup
class DataProcessor:
    def __init__(self, max_cache_size=1000):
        self.cache = {}
        self.connections = []
        self.max_cache_size = max_cache_size

    def process(self, data):
        if len(self.cache) >= self.max_cache_size:
            # Remove oldest
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[data.id] = data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        self.cache.clear()
        for conn in self.connections:
            conn.close()
        self.connections.clear()
```

## Phase 6: Verification & Monitoring

After applying fixes, I'll verify the leak is resolved:

**Verification Process:**
1. Take baseline memory snapshot
2. Run application under load
3. Monitor memory growth over time
4. Compare with pre-fix behavior
5. Validate no new leaks introduced

**Long-term Monitoring Setup:**
```javascript
// Production memory monitoring
const monitoring = {
    interval: 300000, // 5 minutes
    threshold: 500 * 1024 * 1024, // 500 MB

    start() {
        setInterval(() => {
            const usage = process.memoryUsage();

            if (usage.heapUsed > this.threshold) {
                console.warn('Memory threshold exceeded', {
                    heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + ' MB',
                    timestamp: new Date().toISOString()
                });

                // Optional: trigger alert or heap dump
            }
        }, this.interval);
    }
};
```

## Context Continuity

**Session Resume:**
When you return and run `/memory-leak` or `/memory-leak resume`:
- Load previous analysis and snapshots
- Compare current memory with baseline
- Show trend analysis
- Continue from last checkpoint

**Progress Example:**
```
RESUMING MEMORY LEAK ANALYSIS
├── Initial heap size: 125 MB
├── Current heap size: 180 MB
├── Growth rate: 9 MB/hour
├── Leaks fixed: 2 of 4
├── Next: Circular reference in User model

Comparing heap snapshots...
```

## Practical Examples

**Start Analysis:**
```
/memory-leak                    # Auto-detect runtime
/memory-leak node               # Node.js specific
/memory-leak python             # Python specific
/memory-leak browser            # Browser guidance
/memory-leak src/services/      # Analyze specific path
```

**Session Control:**
```
/memory-leak resume      # Continue analysis
/memory-leak analyze     # Run new profiling
/memory-leak compare     # Compare snapshots
/memory-leak status      # Check current state
```

## Safety Guarantees

**Protection Measures:**
- Git checkpoint before fixes
- Non-invasive profiling
- No production impact from analysis
- Snapshot data stays local

**Important:** I will NEVER:
- Profile production without permission
- Modify profiling in way that impacts performance
- Expose sensitive data in snapshots
- Add AI attribution to commits

## Skill Integration

When appropriate for memory issues:
- `/performance-profile` - Cross-reference with CPU usage
- `/test` - Verify fixes don't break functionality
- `/review` - Code review for leak patterns
- `/commit` - Safe commit of memory fixes

## Profiling Tools Reference

**Node.js:**
- Built-in: `--inspect`, `--expose-gc`, `v8.writeHeapSnapshot()`
- heapdump: Heap snapshot on demand
- clinic: Comprehensive profiling suite
- memwatch-next: Memory leak detection
- node-inspect: Interactive debugging

**Python:**
- Built-in: `tracemalloc`, `gc` module
- memory_profiler: Line-by-line profiling
- objgraph: Object reference tracking
- pympler: Advanced memory analysis
- guppy3: Heap analysis

**Browser:**
- Chrome DevTools Memory Panel
- Firefox Developer Tools Memory Tool
- Heap snapshots
- Allocation timeline
- Performance monitor

## Token Budget Optimization

To stay within 3,500-5,500 token budget:
- **Focus analysis on detected issues only**
- **Use compact reporting format**
- **Defer detailed profiling to manual review**
- **Provide actionable fixes over theory**
- **Batch similar leak patterns**

## What I'll Actually Do

1. **Detect runtime** - Auto-identify Node.js/Python/Browser
2. **Profile systematically** - Use appropriate tools for platform
3. **Identify leaks** - Extended thinking for complex patterns
4. **Provide fixes** - Concrete code changes
5. **Verify resolution** - Confirm leaks eliminated
6. **Monitor ongoing** - Setup long-term tracking

I'll help you eliminate memory leaks and establish monitoring to prevent future issues.

---

**Credits:**
- Inspired by Node.js profiling best practices
- Chrome DevTools Memory Profiling Guide
- Python memory_profiler documentation
- obra/superpowers debugging methodology
- Production memory leak patterns from real-world applications
