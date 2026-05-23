---
name: caching-strategy
description: Cache expensive operations to avoid redundant work across workflow phases. Caches project docs (15min TTL), npm info (60min), grep results (30min), token counts (until file modified), web searches (15min). Auto-triggers when detecting repeated reads of same files or repeated API calls. Saves 20-40% execution time.
---

<objective>
The caching-strategy skill eliminates redundant work by intelligently caching expensive operations across workflow phases, reducing execution time by 20-40%.

Repeated work wastes time and resources:
- Reading docs/project/api-strategy.md 5 times in /plan phase (5× file I/O)
- Searching codebase for "user" pattern 3 times (3× grep execution)
- Fetching npm package info for same package repeatedly (3× network calls)
- Counting tokens in spec.md every phase (5× token calculation)
- Web searching "React hooks best practices" multiple times (3× API calls)

This skill implements smart caching with:
1. **File read cache**: Cache file contents until file modified (mtime check)
2. **Search result cache**: Cache grep/glob results for 30 minutes
3. **Network request cache**: Cache npm/web API calls for 15-60 minutes
4. **Computed value cache**: Cache expensive calculations until inputs change
5. **Automatic invalidation**: TTL expiration + file modification detection

The result: 20-40% faster workflow execution with zero behavior changes (transparent caching).
</objective>

<quick_start>
<cacheable_operations>
**High-value caching targets** (biggest time savings):

1. **Project documentation reads** (15min TTL):
   - `docs/project/api-strategy.md`
   - `docs/project/system-architecture.md`
   - `docs/project/tech-stack.md`
   - Read once per phase, not 5× per phase

2. **Codebase searches** (30min TTL):
   - Grep: `"user"` in `**/*.ts` → Cache results
   - Glob: `**/components/**/*.tsx` → Cache file list
   - Repeated in anti-duplication, implementation, review

3. **Package registry queries** (60min TTL):
   - npm info for package versions
   - Dependency metadata
   - Rarely changes during single workflow

4. **Web searches** (15min TTL):
   - Documentation lookups
   - Error message searches
   - Best practice research

5. **Token counts** (until file modified):
   - spec.md token count
   - plan.md token count
   - Recompute only when file changes
</cacheable_operations>

<basic_workflow>
**Before caching**:
```
Phase 1 (/plan):
  - Read api-strategy.md (250ms)
  - Read tech-stack.md (200ms)
  - Read api-strategy.md again (250ms) ← Redundant
  - Grep "user" in codebase (3s)
Total: 3.7s
```

**After caching**:
```
Phase 1 (/plan):
  - Read api-strategy.md (250ms) → Cache
  - Read tech-stack.md (200ms) → Cache
  - Read api-strategy.md (from cache: 5ms) ← Cached!
  - Grep "user" (3s) → Cache
Total: 3.45s saved 250ms (6.7%)
```

**Across multiple phases**:
```
/plan:   Read api-strategy.md (250ms) → Cache
/tasks:  Read api-strategy.md (from cache: 5ms) ← Saved 245ms
/impl:   Read api-strategy.md (from cache: 5ms) ← Saved 245ms
/opt:    Read api-strategy.md (from cache: 5ms) ← Saved 245ms

Total saved: 735ms on single file across 4 phases
```
</basic_workflow>

<immediate_value>
**Typical /feature workflow** (7 phases):

**Without caching**:
```
Phase reads:
- api-strategy.md: 7 reads × 250ms = 1.75s
- tech-stack.md: 5 reads × 200ms = 1s
- spec.md: 10 reads × 150ms = 1.5s
- Grep "user": 3 searches × 3s = 9s
- npm info react: 2 calls × 500ms = 1s
Total redundant work: 14.25s
```

**With caching**:
```
Phase reads:
- api-strategy.md: 1 read (250ms) + 6 cache hits (30ms) = 280ms
- tech-stack.md: 1 read (200ms) + 4 cache hits (20ms) = 220ms
- spec.md: 1 read (150ms) + 9 cache hits (45ms) = 195ms
- Grep "user": 1 search (3s) + 2 cache hits (10ms) = 3.01s
- npm info react: 1 call (500ms) + 1 cache hit (5ms) = 505ms
Total with caching: 4.21s

Time saved: 14.25s - 4.21s = 10.04s (70% reduction)
```

**Savings scale with workflow length**:
- Single phase: 5-10% faster
- Full /feature (7 phases): 20-30% faster
- /epic (20+ phases): 30-40% faster
</immediate_value>
</quick_start>

<workflow>
<step number="1">
**Detect cacheable operation**

Identify operations that are:
- **Idempotent**: Same input → Same output
- **Expensive**: Takes >100ms
- **Repeated**: Called 2+ times
- **Predictable**: Output doesn't change rapidly

**Cacheable**:
- File reads (same file, unchanged content)
- Codebase searches (same pattern, unchanged code)
- API calls (package info, docs, rarely changes)
- Expensive computations (token counts, parsing)

**Not cacheable**:
- User input (unpredictable)
- Current time/date (changes constantly)
- Random values
- System state (memory, CPU)
- Database queries (data changes frequently)
</step>

<step number="2">
**Generate cache key**

Create unique key for each cacheable operation:

**File reads**:
```
Cache key: `file:${absolutePath}`
Example: "file:/project/docs/api-strategy.md"
```

**Grep searches**:
```
Cache key: `grep:${pattern}:${path}:${options}`
Example: "grep:user:**/*.ts:case-insensitive"
```

**Glob patterns**:
```
Cache key: `glob:${pattern}:${cwd}`
Example: "glob:**/components/**/*.tsx:/project"
```

**npm queries**:
```
Cache key: `npm:${operation}:${package}`
Example: "npm:info:react"
```

**Web searches**:
```
Cache key: `web:${query}:${engine}`
Example: "web:React hooks best practices:google"
```

**Token counts**:
```
Cache key: `tokens:${filePath}:${mtime}`
Example: "tokens:/project/spec.md:1704067200"
```

See [references/cache-key-strategies.md](references/cache-key-strategies.md) for comprehensive patterns.
</step>

<step number="3">
**Check cache before executing**

Before expensive operation:

```typescript
function readFile(path: string): string {
  const cacheKey = `file:${path}`;

  // Check cache
  const cached = cache.get(cacheKey);
  if (cached && !isExpired(cached) && !isFileModified(path, cached.mtime)) {
    logger.debug('Cache HIT', { key: cacheKey });
    return cached.value;
  }

  // Cache MISS - execute operation
  logger.debug('Cache MISS', { key: cacheKey });
  const content = fs.readFileSync(path, 'utf-8');
  const mtime = fs.statSync(path).mtimeMs;

  // Store in cache
  cache.set(cacheKey, {
    value: content,
    mtime: mtime,
    cachedAt: Date.now(),
    ttl: 15 * 60 * 1000  // 15 minutes
  });

  return content;
}
```

**Cache check logic**:
1. Generate cache key
2. Look up in cache
3. If found AND not expired AND input unchanged → Return cached value
4. If not found OR expired OR input changed → Execute operation, cache result
</step>

<step number="4">
**Set appropriate TTL**

Different operations have different freshness requirements:

**Immutable** (cache indefinitely):
- npm package versions (once published, never changes)
- Historical git commits
- Published documentation versions

**Stable** (60min TTL):
- npm package metadata (latest version)
- Project documentation (rarely changes during workflow)
- Codebase structure (files/directories)

**Dynamic** (15min TTL):
- Web search results
- API documentation (may update)
- Error message searches

**File-based** (cache until modified):
- File reads → Check mtime
- Token counts → Recompute if file changed
- Parsed AST → Recompute if source changed

**Session-based** (cache for entire workflow):
- User preferences
- Environment variables
- Project configuration

TTL guidelines:
- **Too short**: Cache miss overhead negates benefits
- **Too long**: Stale data causes incorrect results
- **Sweet spot**: Long enough to avoid repeated work, short enough to stay fresh
</step>

<step number="5">
**Invalidate on changes**

Automatically invalidate cache when inputs change:

**File modification**:
```typescript
function isCacheValid(cacheEntry, filePath) {
  const currentMtime = fs.statSync(filePath).mtimeMs;
  return cacheEntry.mtime === currentMtime;
}

// Before returning cached file content
if (!isCacheValid(cached, filePath)) {
  // File modified - invalidate cache
  cache.delete(cacheKey);
  // Re-read file
}
```

**TTL expiration**:
```typescript
function isExpired(cacheEntry) {
  const age = Date.now() - cacheEntry.cachedAt;
  return age > cacheEntry.ttl;
}
```

**Manual invalidation**:
```typescript
// When user saves file
onFileSave((filePath) => {
  cache.invalidatePattern(`file:${filePath}*`);
  cache.invalidatePattern(`grep:*`);  // File change may affect search results
});

// When switching git branch
onBranchChange(() => {
  cache.clear();  // Full invalidation
});
```

**Dependency invalidation**:
```typescript
// If spec.md changes, invalidate token count
onFileChange('spec.md', () => {
  cache.delete('tokens:spec.md');
});
```
</step>

<step number="6">
**Monitor cache effectiveness**

Track metrics to optimize caching strategy:

**Hit rate**:
```
Hit rate = Cache hits / (Cache hits + Cache misses)

Good: >60% hit rate
Great: >80% hit rate
Excellent: >90% hit rate
```

**Time savings**:
```
Time saved = Σ(Cache hit time - Original operation time)

Example:
- 10 file reads from cache (50ms) vs disk (250ms)
- Saved: 10 × (250ms - 50ms) = 2000ms (2 seconds)
```

**Cache size**:
```
Monitor memory usage
- Target: <50MB cache size
- Evict oldest entries if exceeds limit (LRU eviction)
```

**Metrics to log**:
```typescript
{
  cacheHits: 145,
  cacheMisses: 23,
  hitRate: 0.863,  // 86.3%
  timeSaved: 12450,  // 12.45 seconds
  cacheSize: 34.2,  // MB
  topKeys: [
    { key: 'file:api-strategy.md', hits: 24 },
    { key: 'grep:user:**/*.ts', hits: 12 }
  ]
}
```

See [references/cache-monitoring.md](references/cache-monitoring.md) for dashboard setup.
</step>
</workflow>

<cache_types>
<file_read_cache>
**When to use**: Reading same file multiple times in workflow

**Implementation**:
```typescript
const fileCache = new Map();

function readFileCached(path: string): string {
  const cacheKey = `file:${path}`;
  const stat = fs.statSync(path);
  const currentMtime = stat.mtimeMs;

  const cached = fileCache.get(cacheKey);
  if (cached && cached.mtime === currentMtime) {
    return cached.content;  // Cache HIT
  }

  // Cache MISS
  const content = fs.readFileSync(path, 'utf-8');
  fileCache.set(cacheKey, {
    content,
    mtime: currentMtime,
    size: stat.size
  });

  return content;
}
```

**Use cases**:
- Project docs (api-strategy.md, tech-stack.md)
- Spec files (spec.md, plan.md, tasks.md)
- Configuration files (package.json, tsconfig.json)

**Invalidation**: File mtime changes

**Expected hit rate**: 70-90% (files read multiple times per phase)
</file_read_cache>

<search_result_cache>
**When to use**: Repeated grep/glob searches

**Implementation**:
```typescript
const searchCache = new Map();
const SEARCH_TTL = 30 * 60 * 1000;  // 30 minutes

function grepCached(pattern: string, path: string, options: any): string[] {
  const cacheKey = `grep:${pattern}:${path}:${JSON.stringify(options)}`;

  const cached = searchCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < SEARCH_TTL) {
    return cached.results;  // Cache HIT
  }

  // Cache MISS
  const results = execGrep(pattern, path, options);
  searchCache.set(cacheKey, {
    results,
    timestamp: Date.now()
  });

  return results;
}
```

**Use cases**:
- Anti-duplication searches (same pattern multiple times)
- Dependency analysis (finding imports/exports)
- Code review (finding patterns across codebase)

**Invalidation**: 30min TTL or file modifications in search path

**Expected hit rate**: 40-60% (searches often repeated in same phase)
</search_result_cache>

<network_request_cache>
**When to use**: API calls with stable results

**Implementation**:
```typescript
const networkCache = new Map();

async function npmInfoCached(packageName: string): Promise<any> {
  const cacheKey = `npm:info:${packageName}`;
  const NPM_TTL = 60 * 60 * 1000;  // 60 minutes

  const cached = networkCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < NPM_TTL) {
    return cached.data;  // Cache HIT
  }

  // Cache MISS
  const data = await execCommand(`npm info ${packageName} --json`);
  networkCache.set(cacheKey, {
    data,
    timestamp: Date.now()
  });

  return data;
}
```

**Use cases**:
- npm package info
- Web documentation fetches
- GitHub API calls (repo info, release data)

**Invalidation**: 15-60min TTL (depends on data volatility)

**Expected hit rate**: 50-70% (packages queried multiple times)
</network_request_cache>

<computed_value_cache>
**When to use**: Expensive calculations with same inputs

**Implementation**:
```typescript
const computeCache = new Map();

function countTokensCached(filePath: string): number {
  const stat = fs.statSync(filePath);
  const cacheKey = `tokens:${filePath}:${stat.mtimeMs}`;

  const cached = computeCache.get(cacheKey);
  if (cached) {
    return cached.count;  // Cache HIT
  }

  // Cache MISS
  const content = fs.readFileSync(filePath, 'utf-8');
  const count = tokenizer.count(content);  // Expensive operation

  computeCache.set(cacheKey, { count });
  return count;
}
```

**Use cases**:
- Token counting
- Code parsing/AST generation
- Complexity analysis
- Checksum calculation

**Invalidation**: Input file mtime changes

**Expected hit rate**: 60-80% (same files analyzed repeatedly)
</computed_value_cache>

<web_search_cache>
**When to use**: Web searches for documentation/errors

**Implementation**:
```typescript
const webCache = new Map();
const WEB_TTL = 15 * 60 * 1000;  // 15 minutes

async function webSearchCached(query: string): Promise<any> {
  const cacheKey = `web:${query}`;

  const cached = webCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < WEB_TTL) {
    return cached.results;  // Cache HIT
  }

  // Cache MISS
  const results = await performWebSearch(query);
  webCache.set(cacheKey, {
    results,
    timestamp: Date.now()
  });

  return results;
}
```

**Use cases**:
- Documentation lookups
- Error message searches
- Best practice research
- Library usage examples

**Invalidation**: 15min TTL

**Expected hit rate**: 30-50% (searches often unique, but some repeated)
</web_search_cache>
</cache_types>

<auto_trigger_conditions>
<when_to_cache>
**Operation characteristics**:
- Takes >100ms to execute
- Called 2+ times with same inputs
- Idempotent (same input → same output)
- Results don't change rapidly

**Detection patterns**:

**Repeated file reads**:
```
Phase activity log:
- Read api-strategy.md
- Read tech-stack.md
- Read api-strategy.md  ← DUPLICATE (trigger caching)
```

**Repeated searches**:
```
Search history:
- Grep "user" in **/*.ts
- ... (other work)
- Grep "user" in **/*.ts  ← DUPLICATE (trigger caching)
```

**Repeated API calls**:
```
Network calls:
- npm info react
- ... (other work)
- npm info react  ← DUPLICATE (trigger caching)
```

**Expensive computations**:
```
Computation log:
- Count tokens in spec.md (took 350ms)
- ... (other work)
- Count tokens in spec.md  ← EXPENSIVE + DUPLICATE (trigger caching)
```
</when_to_cache>

<when_not_to_cache>
**Operation characteristics**:
- Non-idempotent (random, time-based, stateful)
- Fast (<50ms execution time)
- Called once (no repetition)
- Results change frequently

**Examples**:

**Don't cache**:
- User input (unpredictable)
- `Date.now()` (always changes)
- Random values (`Math.random()`)
- Database queries (data changes)
- File writes (side effects)
- Environment variables modified by user

**Don't cache** (too fast):
- Simple string operations
- Array lookups
- Map/Set operations
- Variable assignments
</when_not_to_cache>

<proactive_caching>
**Pre-cache common operations**:

At workflow start (/feature):
```typescript
async function precacheCommonDocs() {
  // Pre-load project docs (will be needed in /plan, /tasks, /implement)
  await Promise.all([
    readFileCached('docs/project/api-strategy.md'),
    readFileCached('docs/project/tech-stack.md'),
    readFileCached('docs/project/system-architecture.md')
  ]);
  // Now cached for all phases
}
```

**Prefetch based on workflow phase**:

```typescript
// When entering /plan phase
async function prefetchForPlanPhase() {
  // Plan phase always needs these
  await Promise.all([
    readFileCached('docs/project/api-strategy.md'),
    readFileCached('docs/project/data-architecture.md'),
    grepCached('interface.*Props', '**/*.tsx', {})  // Common search
  ]);
}
```

**Warm cache from previous phase**:

```typescript
// /tasks phase uses output from /plan phase
function warmCacheForTasks() {
  // spec.md and plan.md already read in /plan - should be cached
  readFileCached('specs/NNN-slug/spec.md');
  readFileCached('specs/NNN-slug/plan.md');
}
```
</proactive_caching>
</auto_trigger_conditions>

<examples>
<example name="file-read-optimization">
**Scenario**: /plan phase reads api-strategy.md 5 times

**Without caching**:
```typescript
// /plan phase workflow
const apiStrategy1 = readFile('docs/project/api-strategy.md');  // 250ms (disk read)
// ... analyze versioning strategy

const apiStrategy2 = readFile('docs/project/api-strategy.md');  // 250ms (disk read again)
// ... check deprecation policy

const apiStrategy3 = readFile('docs/project/api-strategy.md');  // 250ms (disk read again)
// ... validate breaking change rules

const apiStrategy4 = readFile('docs/project/api-strategy.md');  // 250ms (disk read again)
// ... generate plan section

const apiStrategy5 = readFile('docs/project/api-strategy.md');  // 250ms (disk read again)
// ... final validation

Total time: 1250ms (1.25 seconds)
```

**With caching**:
```typescript
// First read: Cache MISS (read from disk)
const apiStrategy1 = readFileCached('docs/project/api-strategy.md');  // 250ms
// Store in cache with mtime

// Subsequent reads: Cache HIT (read from memory)
const apiStrategy2 = readFileCached('docs/project/api-strategy.md');  // 5ms
const apiStrategy3 = readFileCached('docs/project/api-strategy.md');  // 5ms
const apiStrategy4 = readFileCached('docs/project/api-strategy.md');  // 5ms
const apiStrategy5 = readFileCached('docs/project/api-strategy.md');  // 5ms

Total time: 270ms
Time saved: 980ms (78% reduction)
```

**Cache invalidation**:
```typescript
// If user edits api-strategy.md during /plan phase
fs.writeFileSync('docs/project/api-strategy.md', newContent);

// Next read detects mtime change
const apiStrategy6 = readFileCached('docs/project/api-strategy.md');
// mtime changed → Cache MISS → Re-read from disk (250ms)
// Update cache with new content
```
</example>

<example name="grep-search-optimization">
**Scenario**: Anti-duplication searches for "user" pattern 3 times

**Without caching**:
```typescript
// Task 1: Create user endpoint
const results1 = grep('"user"', '**/*.ts');  // 3000ms (scan entire codebase)

// Task 2: Create user service
const results2 = grep('"user"', '**/*.ts');  // 3000ms (scan again)

// Task 3: Create user model
const results3 = grep('"user"', '**/*.ts');  // 3000ms (scan again)

Total time: 9000ms (9 seconds)
```

**With caching**:
```typescript
// Task 1: Cache MISS (execute grep)
const results1 = grepCached('"user"', '**/*.ts');  // 3000ms
// Store results in cache (30min TTL)

// Task 2: Cache HIT (return cached results)
const results2 = grepCached('"user"', '**/*.ts');  // 10ms

// Task 3: Cache HIT (return cached results)
const results3 = grepCached('"user"', '**/*.ts');  // 10ms

Total time: 3020ms
Time saved: 5980ms (66% reduction)
```

**Cache invalidation**:
```typescript
// If new file created with "user" in it
fs.writeFileSync('src/services/UserService.ts', content);

// Search cache invalidated (codebase changed)
cache.invalidatePattern('grep:*');

// Next grep: Cache MISS (re-execute)
const results4 = grepCached('"user"', '**/*.ts');  // 3000ms
// Picks up new UserService.ts file
```
</example>

<example name="npm-info-optimization">
**Scenario**: Dependency curator checks react package 3 times

**Without caching**:
```typescript
// Check current version
const info1 = await execCommand('npm info react --json');  // 500ms (network call)

// Check for vulnerabilities
const info2 = await execCommand('npm info react --json');  // 500ms (network call again)

// Check peer dependencies
const info3 = await execCommand('npm info react --json');  // 500ms (network call again)

Total time: 1500ms
```

**With caching**:
```typescript
// First call: Cache MISS (network call)
const info1 = await npmInfoCached('react');  // 500ms
// Store in cache (60min TTL)

// Subsequent calls: Cache HIT (return cached data)
const info2 = await npmInfoCached('react');  // 5ms
const info3 = await npmInfoCached('react');  // 5ms

Total time: 510ms
Time saved: 990ms (66% reduction)
```

**TTL expiration**:
```typescript
// After 60 minutes (TTL expired)
const info4 = await npmInfoCached('react');  // 500ms (re-fetch)
// Update cache with latest package info
```
</example>

<example name="token-count-optimization">
**Scenario**: Token budget checks across 4 phases

**Without caching**:
```typescript
// /plan phase: Check token budget
const tokens1 = countTokens('specs/001/spec.md');  // 350ms (tokenize entire file)

// /tasks phase: Check token budget
const tokens2 = countTokens('specs/001/spec.md');  // 350ms (tokenize again)

// /implement phase: Check token budget
const tokens3 = countTokens('specs/001/spec.md');  // 350ms (tokenize again)

// /optimize phase: Check token budget
const tokens4 = countTokens('specs/001/spec.md');  // 350ms (tokenize again)

Total time: 1400ms (1.4 seconds)
```

**With caching**:
```typescript
// /plan phase: Cache MISS (compute tokens)
const tokens1 = countTokensCached('specs/001/spec.md');  // 350ms
// Cache key includes mtime: "tokens:spec.md:1704067200"

// /tasks phase: Cache HIT (spec.md unchanged)
const tokens2 = countTokensCached('specs/001/spec.md');  // 5ms

// /implement phase: Cache HIT (spec.md unchanged)
const tokens3 = countTokensCached('specs/001/spec.md');  // 5ms

// /optimize phase: Cache HIT (spec.md unchanged)
const tokens4 = countTokensCached('specs/001/spec.md');  // 5ms

Total time: 365ms
Time saved: 1035ms (74% reduction)
```

**Cache invalidation on file modification**:
```typescript
// User updates spec.md during /implement
fs.writeFileSync('specs/001/spec.md', updatedContent);

// mtime changes: 1704067200 → 1704067500

// Next token count: Cache key mismatch
const tokens5 = countTokensCached('specs/001/spec.md');
// New key: "tokens:spec.md:1704067500" (not in cache)
// Cache MISS → Recompute (350ms)
```
</example>
</examples>

<anti_patterns>
<anti_pattern name="caching-non-idempotent-operations">
**Problem**: Caching operations that change on each call

**Bad approach**:
```typescript
// Caching timestamp (always changes)
const timestamp = cacheable(() => Date.now());  // WRONG
```

**Correct approach**:
```typescript
// Don't cache non-idempotent operations
const timestamp = Date.now();  // No caching
```

**Rule**: Only cache idempotent operations (same input → same output).
</anti_pattern>

<anti_pattern name="overly-aggressive-caching">
**Problem**: Caching everything, including fast operations

**Bad approach**:
```typescript
// Caching simple string operations
const uppercased = cacheable((str) => str.toUpperCase());  // WRONG (too fast)
```

**Correct approach**:
```typescript
// Don't cache operations faster than cache overhead
const uppercased = str.toUpperCase();  // Direct call
```

**Rule**: Only cache operations taking >100ms.
</anti_pattern>

<anti_pattern name="stale-cache-serving">
**Problem**: Serving stale data because TTL too long

**Bad approach**:
```typescript
// Caching file content for 24 hours
const FILE_TTL = 24 * 60 * 60 * 1000;  // WRONG (file may change)
```

**Correct approach**:
```typescript
// Check file mtime instead of long TTL
function isCacheValid(cached, filePath) {
  const currentMtime = fs.statSync(filePath).mtimeMs;
  return cached.mtime === currentMtime;
}
```

**Rule**: For file-based caching, check mtime. For network caching, use appropriate TTL (15-60min).
</anti_pattern>

<anti_pattern name="unbounded-cache-growth">
**Problem**: Cache grows without limit, exhausts memory

**Bad approach**:
```typescript
// No size limit or eviction policy
cache.set(key, value);  // Keeps growing forever
```

**Correct approach**:
```typescript
// LRU cache with size limit
const cache = new LRU({ max: 500, maxSize: 50 * 1024 * 1024 });  // 500 entries, 50MB max
```

**Rule**: Set cache size limits and use LRU eviction.
</anti_pattern>

<anti_pattern name="ignoring-cache-invalidation">
**Problem**: Not invalidating cache when inputs change

**Bad approach**:
```typescript
// File changes but cache not invalidated
fs.writeFileSync('api-strategy.md', newContent);
const cached = readFileCached('api-strategy.md');  // Returns old content!
```

**Correct approach**:
```typescript
// Invalidate on file write
fs.writeFileSync('api-strategy.md', newContent);
cache.invalidate('file:api-strategy.md');
const fresh = readFileCached('api-strategy.md');  // Re-reads new content
```

**Rule**: Invalidate cache when inputs change (file mtime, TTL expiration, manual invalidation).
</anti_pattern>
</anti_patterns>

<validation>
<success_indicators>
Caching strategy successfully applied when:

1. **Hit rate**: >60% cache hit rate (most operations served from cache)
2. **Time savings**: 20-40% reduction in workflow execution time
3. **Zero staleness**: No stale data served (proper invalidation)
4. **Memory usage**: Cache size <50MB (efficient memory use)
5. **Transparent**: Behavior identical to non-cached version (correctness maintained)
6. **Measurable**: Cache metrics logged (hits, misses, time saved)
</success_indicators>

<metrics>
Track caching effectiveness:

**Hit rate metrics**:
```typescript
{
  totalRequests: 200,
  cacheHits: 145,
  cacheMisses: 55,
  hitRate: 0.725  // 72.5%
}
```

**Time savings**:
```typescript
{
  totalTimeWithCache: 12.3,  // seconds
  totalTimeWithoutCache: 18.7,  // seconds (estimated)
  timeSaved: 6.4,  // seconds (34% reduction)
  timeSavedPercent: 34.2
}
```

**Cache size**:
```typescript
{
  entries: 347,
  sizeBytes: 42_534_912,  // 42MB
  sizeMB: 40.6
}
```

**Top cached operations**:
```typescript
{
  topKeys: [
    { key: 'file:api-strategy.md', hits: 24, timeSaved: 5800 },
    { key: 'grep:user:**/*.ts', hits: 12, timeSaved: 35800 },
    { key: 'npm:info:react', hits: 8, timeSaved: 3960 }
  ]
}
```
</metrics>

<validation_checklist>
Before deploying caching:

- [ ] Operations are idempotent (same input → same output)
- [ ] TTLs appropriate for data volatility
- [ ] Invalidation triggers configured (file mtime, manual)
- [ ] Cache size limits set (prevent memory exhaustion)
- [ ] Metrics collection enabled (hit rate, time saved)
- [ ] Behavior identical to non-cached (correctness verified)
- [ ] Hit rate >60% (confirms caching is effective)
- [ ] Time savings >20% (confirms performance benefit)
</validation_checklist>
</validation>

<reference_guides>
For deeper topics, see reference files:

**Cache key strategies**: [references/cache-key-strategies.md](references/cache-key-strategies.md)
- Generating unique cache keys
- Handling complex inputs
- Collision avoidance

**Cache monitoring**: [references/cache-monitoring.md](references/cache-monitoring.md)
- Setting up metrics dashboard
- Analyzing cache effectiveness
- Optimizing hit rates

**Implementation patterns**: [references/implementation-patterns.md](references/implementation-patterns.md)
- In-memory cache (Map, LRU)
- Persistent cache (Redis, file-based)
- Distributed cache (multi-process)
</reference_guides>

<success_criteria>
The caching-strategy skill is successfully applied when:

1. **Auto-detection**: Repeated operations automatically trigger caching
2. **Appropriate caching**: Only expensive (>100ms), idempotent, repeated operations cached
3. **Correct TTLs**: File-based (mtime check), network (15-60min), computed (until input changes)
4. **Proper invalidation**: Cache invalidated when inputs change (file mtime, TTL, manual)
5. **High hit rate**: >60% of cacheable operations served from cache
6. **Significant savings**: 20-40% reduction in workflow execution time
7. **Memory efficient**: Cache size <50MB, LRU eviction when needed
8. **Transparent behavior**: Cached operations produce identical results to non-cached
9. **Measurable impact**: Metrics show time saved, hit rates, cache effectiveness
10. **Zero staleness**: No stale data served (all invalidation triggers working)
</success_criteria>
