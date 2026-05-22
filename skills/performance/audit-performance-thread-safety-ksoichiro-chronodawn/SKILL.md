---
name: audit-performance-thread-safety
description: Audit codebase for performance bottlenecks and thread-safety issues
---

# Performance and Thread Safety Audit Guide

**Purpose**: Systematically audit Minecraft mod codebase for performance bottlenecks, thread-safety issues, and dimension isolation problems.

**When to use**:
- Before major releases
- After implementing new structure generation systems
- After adding new boss spawning systems
- When investigating multiplayer crashes or lag
- When profiling shows unexpected CPU usage

**Output**: Generates comprehensive audit report with findings, risk assessment, and fix recommendations.

---

## Audit Process

### Phase 1: Identify Critical Code Paths

**What to look for**:
1. **Event handlers** registered with `TickEvent.SERVER_POST` or `TickEvent.SERVER_LEVEL_POST`
2. **Structure generation code** in `worldgen/` packages
3. **Boss spawning systems** in `worldgen/spawning/`
4. **Dimension-specific handlers** that process multiple dimensions
5. **Mixin classes** that modify structure placement

**Commands**:
```bash
# Find all event registrations
grep -r "TickEvent\\.SERVER" common/src/main/java --include="*.java"

# Find boss room placers and spawners
find common/src/main/java -name "*BossRoom*.java" -o -name "*Spawner*.java"

# Find structure-related mixins
find common/src/main/java/*/mixin -name "*Structure*.java"
```

---

### Phase 2: Performance Analysis (T428)

#### 2.1 Main Thread Blocking Detection

**Critical patterns to find**:

1. **Large block scans on main thread**:
   ```java
   // BAD: Scanning millions of blocks synchronously
   for (int x = minX; x <= maxX; x++) {
       for (int y = minY; y <= maxY; y++) {
           for (int z = minZ; z <= maxZ; z++) {
               BlockPos pos = new BlockPos(x, y, z);
               BlockState state = level.getBlockState(pos);
               // ... processing ...
           }
       }
   }
   ```
   **Red flags**:
   - Scan range > 50 blocks in any dimension
   - No chunking or pagination
   - Called every tick or frequently

2. **Repeated full-area scans**:
   ```java
   // BAD: Scanning same area multiple times
   removeWater();          // Scan 1
   placeTemplate();
   finalizeWaterlogging(); // Scan 2
   scheduledFinalize();    // Scan 3 (later)
   ```
   **Red flags**:
   - Same area scanned 3+ times
   - Delayed/scheduled rescans
   - No caching of positions

3. **Single-tick batch operations**:
   ```java
   // BAD: Processing all candidates in one tick
   for (PlacementCandidate candidate : allCandidates) {
       evaluateCandidate(candidate); // Heavy computation
   }
   ```
   **Red flags**:
   - Loop over large collection (10+ items)
   - Heavy computation per iteration
   - No async processing or spreading across ticks

#### 2.2 Performance Impact Assessment

For each issue found, estimate:

| Metric | Measurement | Severity |
|--------|-------------|----------|
| Blocks scanned | Count triple-nested loops | > 100K = CRITICAL |
| Scan frequency | Ticks between scans | < 600 = HIGH |
| Pause duration | Estimated ms (1M blocks ≈ 50-100ms) | > 200ms = CRITICAL |
| Affected players | How many players trigger | All nearby = CRITICAL |

**Document findings**:
```markdown
### Issue: [Description]
**File**: `path/to/File.java` (lines X-Y)
**Pattern**: [Large block scan / Repeated scan / Batch operation]
**Impact**:
- Blocks scanned: [count]
- Estimated pause: [ms]
- Frequency: Every [ticks]
**Severity**: [CRITICAL / HIGH / MEDIUM]
```

---

### Phase 3: Thread Safety Analysis (T429)

#### 3.1 Non-Thread-Safe Collection Detection

**Critical patterns to find**:

1. **Static HashMap/HashSet in multi-threaded context**:
   ```java
   // BAD: HashMap is NOT thread-safe
   private static final Map<ResourceLocation, Set<BlockPos>> map = new HashMap<>();
   ```
   **Where to check**:
   - Boss room placers
   - Entity spawners
   - Event handlers that process all dimensions
   - Mixin classes with instance variables

2. **Non-atomic map operations**:
   ```java
   // BAD: putIfAbsent + get is NOT atomic as two operations
   map.putIfAbsent(key, new HashSet<>());
   Set<BlockPos> set = map.get(key);  // Race condition here

   // BAD: get + increment + put is NOT atomic
   int count = map.get(key);
   count++;
   map.put(key, count);  // Lost updates possible
   ```

3. **Mixin instance variables**:
   ```java
   @Mixin(SomeClass.class)
   public class SomeMixin {
       // BAD: Instance variable in mixin (shared across threads)
       private final Set<BlockPos> positions = new HashSet<>();
   }
   ```

#### 3.2 Thread Safety Verification

For each collection found, check:

**Questions**:
1. Is it accessed from multiple dimension threads? (Check event handler type)
2. Is it static? (Static = shared across all threads)
3. Is the collection type thread-safe? (HashMap/HashSet = NO, ConcurrentHashMap = YES)
4. Are operations atomic? (get+put = NO, compute() = YES)

**Thread-safe patterns**:
```java
// GOOD: ConcurrentHashMap for maps
private static final Map<K, V> map = new ConcurrentHashMap<>();

// GOOD: ConcurrentHashMap.newKeySet() for sets
private static final Set<BlockPos> set = ConcurrentHashMap.newKeySet();

// GOOD: Collections.newSetFromMap for sets
private static final Set<BlockPos> set = Collections.newSetFromMap(new ConcurrentHashMap<>());

// GOOD: Collections.synchronizedSet for sets
private final Set<BlockPos> set = Collections.synchronizedSet(new HashSet<>());

// GOOD: Atomic increment
map.compute(key, (k, v) -> (v == null ? 0 : v) + 1);

// GOOD: Atomic putIfAbsent for sets
map.computeIfAbsent(key, k -> ConcurrentHashMap.newKeySet());
```

**Document findings**:
```markdown
### Issue: Non-thread-safe [HashMap/HashSet/ArrayList]
**File**: `path/to/File.java` (lines X-Y)
**Pattern**:
```java
private static final Map<K, V> map = new HashMap<>();
```
**Risk**: [ConcurrentModificationException / Data corruption / Lost updates]
**Fix**: Replace with `ConcurrentHashMap`
**Severity**: [CRITICAL / HIGH / MEDIUM]
```

---

### Phase 4: Dimension Isolation Analysis (T430)

#### 4.1 Cross-Dimension Processing Detection

**Critical patterns to find**:

1. **Processing all dimensions without filtering**:
   ```java
   // BAD: Processes ALL dimensions
   TickEvent.SERVER_POST.register(server -> {
       for (ServerLevel level : server.getAllLevels()) {
           processLevel(level); // No dimension check!
       }
   });
   ```

2. **Missing dimension filter in handlers**:
   ```java
   // BAD: No early exit for wrong dimension
   public static void checkAndProcess(ServerLevel level) {
       // Immediately starts processing without dimension check
       for (...) { ... }
   }
   ```

**GOOD patterns**:
```java
// GOOD: Filter to specific dimension
TickEvent.SERVER_LEVEL_POST.register(level -> {
    if (!level.dimension().equals(ModDimensions.CHRONO_DAWN_DIMENSION)) {
        return; // Early exit
    }
    // ... process only Chrono Dawn
});
```

#### 4.2 Dimension Context Verification

For each handler found, check:

**Questions**:
1. Which dimension(s) should this handler process?
2. Does it have a dimension filter?
3. Is it using `SERVER_POST` (global) or `SERVER_LEVEL_POST` (per-dimension)?
4. Does the structure/entity only spawn in one dimension?

**Expected behavior**:
- Boss room placers: Only Chrono Dawn dimension
- Boss spawners: Only Chrono Dawn dimension
- Time distortion: Only Chrono Dawn dimension (already has filter)
- Portal handlers: Multiple dimensions (OK to process all)

**Document findings**:
```markdown
### Issue: No dimension filtering
**File**: `path/to/File.java` (lines X-Y)
**Pattern**: Processes all dimensions without filter
**Impact**: Wasted CPU cycles in [Overworld/Nether/End]
**Expected**: Only process [Chrono Dawn] dimension
**Fix**: Add early-exit dimension filter
**Severity**: MEDIUM
```

---

### Phase 5: Generate Audit Report

#### 5.1 Report Structure

```markdown
# Performance and Thread Safety Audit Report

**Date**: [YYYY-MM-DD]
**Branch**: [branch-name]
**Tasks**: T428 (Performance), T429 (Thread Safety), T430 (Dimension Isolation)

---

## Executive Summary

[Brief overview of findings, priority, risk]

---

## T428: Main Thread Blocking in Structure Generation

### Findings

[Detailed findings from Phase 2]

### Root Cause Analysis

[Why these issues exist]

### Recommended Fixes

[Prioritized fix recommendations]

---

## T429: Non-Thread-Safe Collection Usage

### Findings

[Detailed findings from Phase 3]

### Root Cause Analysis

[Why these issues exist]

### Recommended Fixes

[Prioritized fix recommendations]

---

## T430: Dimension Filtering in Chunk Processing

### Findings

[Detailed findings from Phase 4]

### Root Cause Analysis

[Why these issues exist]

### Recommended Fixes

[Prioritized fix recommendations]

---

## Summary of Issues Found

[Table of all issues with severity, files, priority]

---

## Next Steps

[Recommended actions in priority order]

---

## Estimated Effort

[Time estimates for fixes]

---

## Risk Assessment

[What happens without fixes vs with fixes]
```

#### 5.2 Severity Classification

**CRITICAL**:
- Main thread freeze > 500ms
- HashMap in multi-threaded context
- Race conditions causing data corruption

**HIGH**:
- Main thread freeze 200-500ms
- Non-atomic operations with high frequency
- Missing thread synchronization

**MEDIUM**:
- Main thread freeze 50-200ms
- Missing dimension filters (CPU waste)
- Inefficient algorithms

**LOW**:
- Main thread freeze < 50ms
- Minor optimization opportunities

---

## Common Issues and Solutions

### Issue 1: Large Block Scanning

**Problem**: Scanning millions of blocks on main thread
**Solution**:
1. **Chunk-based scanning**: Process 1 chunk per tick
2. **Marker caching**: Cache marker positions after first scan
3. **Pre-calculation**: Calculate positions during structure generation

**Example fix**:
```java
// Before: Scan all at once
for (BlockPos pos : BlockPos.betweenClosed(min, max)) { ... }

// After: Process 1 chunk per tick
private static ChunkPos currentChunk = null;
private static Iterator<BlockPos> scanIterator = null;

public static void onTick(ServerLevel level) {
    if (scanIterator == null) {
        // Start new scan
        currentChunk = ...;
        scanIterator = BlockPos.betweenClosed(...).iterator();
    }

    int processed = 0;
    while (scanIterator.hasNext() && processed < 256) { // Limit per tick
        BlockPos pos = scanIterator.next();
        // ... process ...
        processed++;
    }

    if (!scanIterator.hasNext()) {
        scanIterator = null; // Done
    }
}
```

### Issue 2: Thread-Unsafe Collections

**Problem**: HashMap/HashSet accessed from multiple threads
**Solution**: Replace with ConcurrentHashMap

**Example fix**:
```java
// Before:
private static final Map<ResourceLocation, Set<BlockPos>> map = new HashMap<>();

// After:
private static final Map<ResourceLocation, Set<BlockPos>> map = new ConcurrentHashMap<>();

// Before (non-atomic):
map.putIfAbsent(key, new HashSet<>());
Set<BlockPos> set = map.get(key);

// After (atomic):
Set<BlockPos> set = map.computeIfAbsent(key, k -> ConcurrentHashMap.newKeySet());

// Before (non-atomic increment):
int count = map.get(key);
count++;
map.put(key, count);

// After (atomic increment):
int count = map.compute(key, (k, v) -> (v == null ? 0 : v) + 1);
```

### Issue 3: Missing Dimension Filter

**Problem**: Processing all dimensions when structure only spawns in one
**Solution**: Add early-exit dimension filter

**Example fix**:
```java
// Before:
public static void checkAndProcess(ServerLevel level) {
    ResourceLocation dimensionId = level.dimension().location();
    // ... process ...
}

// After:
public static void checkAndProcess(ServerLevel level) {
    // Only process Chrono Dawn dimension
    if (!level.dimension().equals(ModDimensions.CHRONO_DAWN_DIMENSION)) {
        return;
    }

    ResourceLocation dimensionId = level.dimension().location();
    // ... process ...
}
```

---

## Verification Checklist

After applying fixes:

- [ ] All modules compile successfully (`:common:compileJava`, `:fabric:compileJava`, `:neoforge:compileJava`)
- [ ] No new warnings introduced
- [ ] Thread-safe collections used everywhere
- [ ] Atomic operations for all shared state modifications
- [ ] Dimension filters added where appropriate
- [ ] Documentation updated (comments added explaining thread-safety)
- [ ] Performance logging added for slow operations
- [ ] Build test passes
- [ ] Manual testing in single-player (no freezes)
- [ ] Manual testing in multiplayer (no crashes)

---

## References

**Related Documentation**:
- `CLAUDE.md` → "Structure Worldgen Guidelines" (for structure generation best practices)
- `.claude/skills/structure-worldgen/SKILL.md` (for waterlogging prevention patterns)

**Related Tasks**:
- T428: Performance audit and optimization
- T429: Thread-safety audit and fixes
- T430: Dimension filtering audit

**Example Audit Reports**:
- See project root for `audit_report_performance_thread_safety.md` (example report)
- See project root for `FIXES_APPLIED.md` (example fixes summary)

---

**Last Updated**: 2026-01-02
**Author**: Claude Sonnet 4.5
