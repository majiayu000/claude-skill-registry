---
name: systematic-debugger
description: This skill should be used when the user mentions "debugging", "troubleshooting", "bug", "error", "issue", "not working", "broken", discusses investigating problems, asks about debugging techniques, DevTools usage, or mentions they need to fix something. Addresses methodical problem-solving approach for software issues.
version: 1.0.0
---

# Systematic Debugging

Methodical approach to identifying and fixing software issues. Emphasizes reproducibility, isolation, and verification over trial-and-error debugging. Covers browser DevTools, Node debugging, logging strategies, and Svelte-specific debugging techniques.

---

## When This Skill Applies

Use this skill when:
- User reports something "not working"
- Investigating errors or unexpected behaviour
- Performance issues need diagnosis
- Setting up debugging infrastructure
- Explaining debugging approaches
- Teaching debugging techniques
- Questions about DevTools or debugging tools

---

## The Debugging Methodology

**Four-step process**: Reproduce → Isolate → Fix → Verify

### 1. Reproduce

**Make the bug happen reliably**

Can't fix what you can't reproduce. First priority is finding reliable steps to trigger the issue.

**Questions to ask**:
- What exact steps produce the error?
- Does it happen every time or intermittently?
- What's the expected vs actual behaviour?
- What's the minimal reproduction case?

**Document reproduction steps**:
````markdown
## To Reproduce

1. Navigate to `/dashboard`
2. Click "Load More" button
3. Scroll to bottom of page
4. Click "Load More" again

**Expected**: More items load
**Actual**: Page freezes, console shows error
**Frequency**: Happens every time on 2nd click
````

**If intermittent**:
- Look for race conditions
- Check network timing issues
- Consider state-dependent bugs
- Try multiple environments

### 2. Isolate (Root-Cause Depth)

**Narrow down the cause — then go deeper.**

Once reproducible, determine exactly where the problem originates. But don't stop at the first explanation. The first "cause" is often a symptom. Ask **why** repeatedly until you reach the structural root.

**The Five Whys**:
```
Bug: Users see stale data after updating their profile.

Why? → The cache isn't invalidated after the update.
Why? → The update function doesn't call cache.invalidate().
Why? → The caching layer was added after the update function was written.
Why? → There's no pattern ensuring new writes invalidate related caches.
Root: Missing cache invalidation convention. Fix the convention, not just this instance.
```

**Depth vs speed**: Not every bug warrants five whys. Use your judgment:
- **Shallow fix appropriate**: Typo, wrong variable name, missing null check
- **Deep investigation warranted**: Bug that could recur, affects multiple users, or reveals a pattern gap

**Isolation techniques**:

**Binary search approach**:
````typescript
// Working at line 50?
console.log('Check 1:', data); // ✓ Data good here

// Working at line 75?
console.log('Check 2:', result); // ✗ Result undefined here

// Problem is between lines 50-75
````

**Comment out code**:
````typescript
// Does removing this fix it?
// await someAsyncFunction();

// If yes, problem is in someAsyncFunction
````

**Minimal reproduction**:
````typescript
// Strip away everything non-essential
// Original: 300 lines, complex state, multiple API calls
// Minimal: 20 lines that show the exact issue

async function minimalRepro() {
  const data = await fetch('/api/items');
  console.log(data); // undefined when expected array
}
````

**Check assumptions**:
````typescript
// Assumption: API returns array
console.log(typeof data); // "object" - it's null!

// Assumption: User is logged in
console.log(user); // undefined - not logged in!
````

### 3. Fix

**Implement targeted solution**

Now that you know the cause, fix it specifically.

**Fix patterns**:

**Null/undefined checks**:
````typescript
// Before (crashes)
const count = items.length;

// After
const count = items?.length ?? 0;
````

**Async timing**:
````typescript
// Before (race condition)
fetch('/api/data');
renderUI(); // Renders before data arrives

// After
const data = await fetch('/api/data');
renderUI(data);
````

**State initialization**:
````typescript
// Before (undefined on first render)
let items;

// After
let items = [];
````

**Error boundaries**:
````typescript
// Before (crashes entire app)
const result = riskyOperation();

// After
try {
  const result = riskyOperation();
} catch (error) {
  console.error('Operation failed:', error);
  showErrorToUser('Something went wrong');
}
````

### 4. Verify

**Confirm the fix works**

Don't assume it's fixed. Test thoroughly.

**Verification checklist**:
- ✓ Original reproduction steps no longer produce error
- ✓ Expected behaviour now occurs
- ✓ No new errors introduced
- ✓ Edge cases still work
- ✓ Performance not degraded

**Test edge cases**:
````typescript
// Fixed for normal case, but what about:
- Empty array
- Null values
- Very large datasets
- Network failures
- Simultaneous requests
````

**Write regression test** (see Testing Foundations skill):
````typescript
it('should handle second "Load More" click', async () => {
  render(ItemList);

  await clickLoadMore();
  await clickLoadMore(); // This used to crash

  expect(screen.getAllByRole('listitem').length).toBeGreaterThan(10);
});
````

---

## Browser DevTools

### Console

**Strategic logging**:
````typescript
// ✗ Bad: Non-informative
console.log(data);

// ✓ Good: Labeled and contextual
console.log('API Response:', data);
console.log('User state before update:', user);

// ✓ Better: Grouped related logs
console.group('Data Processing');
console.log('Input:', rawData);
console.log('Processed:', processedData);
console.log('Output:', finalResult);
console.groupEnd();

// ✓ Advanced: Conditional logging
const DEBUG = true;
DEBUG && console.log('Debug info:', state);

// ✓ Tables for arrays of objects
console.table(users);
````

**Console methods**:
````typescript
console.log('Normal message');
console.info('Informational');
console.warn('Warning - check this');
console.error('Error occurred');
console.debug('Debug details');

// Timing
console.time('operation');
// ... code to measure
console.timeEnd('operation'); // operation: 45.2ms

// Assertions
console.assert(value > 0, 'Value must be positive:', value);

// Count occurrences
console.count('API call'); // API call: 1
console.count('API call'); // API call: 2
````

### Network Tab

**Inspect API requests**:
- Check request URL and method
- Verify headers (Authorization, Content-Type)
- Inspect request payload
- Check response status and body
- Look for failed requests (red)
- Check timing (slow responses)

**Common issues**:
````
404 Not Found → Check URL spelling, route exists
401 Unauthorized → Check auth token present and valid
500 Server Error → Check server logs, API issue
CORS Error → Check server allows origin
Timeout → API too slow or not responding
````

### Elements Tab

**Inspect DOM**:
- Check element exists
- Verify classes applied
- Check computed styles
- Inspect event listeners
- Modify styles live

**Common CSS issues**:
````css
/* Check computed styles for: */
- Display: none (hidden element)
- Z-index conflicts
- Overflow: hidden (content clipped)
- Position issues
- Flexbox/Grid properties
````

### Sources Tab (Debugger)

**Breakpoints**:
````typescript
function processData(data) {
  // Set breakpoint on this line
  const result = transform(data);

  // Execution pauses, inspect:
  // - data value
  // - Scope variables
  // - Call stack

  return result;
}
````

**Breakpoint types**:
- **Line breakpoints** - Pause at specific line
- **Conditional breakpoints** - Pause only when condition true
- **Logpoints** - Log without stopping execution
- **Exception breakpoints** - Pause on errors

**Debugger controls**:
- **Continue** (F8) - Resume execution
- **Step over** (F10) - Execute current line, don't go into functions
- **Step into** (F11) - Go into function calls
- **Step out** (Shift+F11) - Exit current function

### Application Tab

**Inspect storage**:
- **Local Storage** - Persistent key-value storage
- **Session Storage** - Session-only storage
- **Cookies** - Check authentication cookies
- **IndexedDB** - Client-side database
- **Cache Storage** - Service worker cache

**Common storage issues**:
````typescript
// Check if data stored correctly
localStorage.getItem('user'); // "undefined" as string? null?

// Check cookie domain/path
// Check expiration
// Check HttpOnly/Secure flags
````

### Performance Tab

**Profile performance**:
1. Click record
2. Perform slow action
3. Stop recording
4. Analyze flame chart

**Look for**:
- Long tasks (>50ms)
- Excessive re-renders
- Slow API calls
- Memory leaks (increasing usage)

---

## Node.js Debugging

### Built-in Debugger

**Start with inspect**:
````bash
node --inspect server.js
# or
node --inspect-brk server.js  # Break on first line
````

**Chrome DevTools**:
1. Open chrome://inspect
2. Click "Open dedicated DevTools for Node"
3. Same interface as browser debugging

### Console Debugging
````typescript
// Strategic placement
async function fetchUserData(userId) {
  console.log('Fetching user:', userId);

  const user = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
  console.log('Query result:', user);

  if (!user) {
    console.log('User not found');
    return null;
  }

  console.log('Returning user:', user);
  return user;
}
````

### Debug Module
````typescript
import debug from 'debug';

const log = debug('app:users');

log('Fetching user %s', userId); // Only shows if DEBUG=app:* enabled

// Enable specific namespaces
// DEBUG=app:users node server.js
// DEBUG=app:* node server.js
// DEBUG=* node server.js
````

---

## Svelte-Specific Debugging

### Reactive Statements

**Log reactive changes**:
````svelte
<script>
  let count = 0;

  // Debug reactive statement
  $: console.log('Count changed:', count);

  // Debug derived value
  $: doubled = count * 2;
  $: console.log('Doubled:', doubled);

  // Debug with condition
  $: if (count > 10) {
    console.log('Count exceeded threshold');
  }
</script>
````

### Component Lifecycle
````svelte
<script>
  import { onMount, onDestroy, beforeUpdate, afterUpdate } from 'svelte';

  onMount(() => {
    console.log('Component mounted');
    return () => console.log('Component cleanup');
  });

  onDestroy(() => {
    console.log('Component destroyed');
  });

  beforeUpdate(() => {
    console.log('Before DOM update');
  });

  afterUpdate(() => {
    console.log('After DOM update');
  });
</script>
````

### Store Debugging
````typescript
import { writable } from 'svelte/store';

function createDebugStore(name, initial) {
  const store = writable(initial);

  // Log all updates
  const { subscribe, set, update } = store;

  return {
    subscribe,
    set: (value) => {
      console.log(`${name} set to:`, value);
      set(value);
    },
    update: (fn) => {
      console.log(`${name} updated`);
      update((val) => {
        const newVal = fn(val);
        console.log(`  Old:`, val, `New:`, newVal);
        return newVal;
      });
    }
  };
}

export const userStore = createDebugStore('user', null);
````

### Svelte DevTools

**Browser extension** - Install Svelte DevTools

Features:
- Component tree inspection
- Props and state values
- Store contents
- Event listeners
- Performance profiling

---

## Logging Strategies

### Log Levels
````typescript
const LOG_LEVELS = {
  ERROR: 0,
  WARN: 1,
  INFO: 2,
  DEBUG: 3
};

const currentLevel = LOG_LEVELS.INFO;

function log(level, message, ...args) {
  if (level <= currentLevel) {
    const prefix = ['ERROR', 'WARN', 'INFO', 'DEBUG'][level];
    console.log(`[${prefix}]`, message, ...args);
  }
}

// Usage
log(LOG_LEVELS.ERROR, 'Failed to load user');
log(LOG_LEVELS.DEBUG, 'Cache hit for key:', key); // Only shows if DEBUG level
````

### Contextual Logging
````typescript
function createLogger(context) {
  return {
    info: (msg, ...args) => console.log(`[${context}]`, msg, ...args),
    error: (msg, ...args) => console.error(`[${context}]`, msg, ...args),
    debug: (msg, ...args) => console.debug(`[${context}]`, msg, ...args)
  };
}

const log = createLogger('UserService');
log.info('Fetching user', userId);
log.error('Failed to fetch', error);
````

### Production Logging

**Don't ship debug logs**:
````typescript
// ✗ Bad: Logs in production
console.log('User clicked button');

// ✓ Good: Conditional logging
if (import.meta.env.DEV) {
  console.log('User clicked button');
}

// ✓ Better: Logging service
logger.info('User action', { action: 'button_click', userId });
````

**Production-safe logging**:
````typescript
// Errors only in production
if (import.meta.env.PROD) {
  window.addEventListener('error', (event) => {
    logToService({
      message: event.message,
      stack: event.error?.stack,
      timestamp: new Date().toISOString()
    });
  });
}
````

---

## Common Bug Patterns

### Race Conditions

**Problem**:
````typescript
// Race: Which finishes first?
fetchUserData(userId);
fetchUserPosts(userId);
render(); // Might render before data arrives
````

**Solution**:
````typescript
const [userData, userPosts] = await Promise.all([
  fetchUserData(userId),
  fetchUserPosts(userId)
]);
render(userData, userPosts);
````

### Stale Closures

**Problem**:
````svelte
<script>
  let count = 0;

  function startTimer() {
    setInterval(() => {
      console.log(count); // Always logs 0 (stale closure)
      count++;
    }, 1000);
  }
</script>
````

**Solution**:
````svelte
<script>
  let count = 0;

  function startTimer() {
    setInterval(() => {
      count = count + 1; // Access current value via update
    }, 1000);
  }

  // Or use reactive statement
  $: if (timerActive) {
    const interval = setInterval(() => count++, 1000);
    return () => clearInterval(interval);
  }
</script>
````

### Undefined Reference Errors

**Problem**:
````typescript
const name = user.profile.name; // Cannot read property 'name' of undefined
````

**Solution**:
````typescript
// Optional chaining
const name = user?.profile?.name;

// With default
const name = user?.profile?.name ?? 'Unknown';

// Defensive check
if (user?.profile?.name) {
  const name = user.profile.name;
}
````

### Memory Leaks

**Problem**:
````svelte
<script>
  import { onMount } from 'svelte';

  onMount(() => {
    const interval = setInterval(() => {
      // Do work
    }, 1000);
    // Never cleaned up! Memory leak
  });
</script>
````

**Solution**:
````svelte
<script>
  import { onMount } from 'svelte';

  onMount(() => {
    const interval = setInterval(() => {
      // Do work
    }, 1000);

    return () => clearInterval(interval); // Cleanup
  });
</script>
````

### Async State Updates

**Problem**:
````typescript
async function loadData() {
  loading = true;
  const data = await fetchData();
  items = data; // If component unmounted, this updates destroyed component
  loading = false;
}
````

**Solution**:
````typescript
async function loadData() {
  loading = true;
  let cancelled = false;

  onDestroy(() => {
    cancelled = true;
  });

  const data = await fetchData();

  if (!cancelled) {
    items = data;
    loading = false;
  }
}
````

---

## Performance Debugging

### Identify Slow Operations
````typescript
function measurePerformance(label, fn) {
  const start = performance.now();
  const result = fn();
  const end = performance.now();
  console.log(`${label}: ${(end - start).toFixed(2)}ms`);
  return result;
}

const result = measurePerformance('Data processing', () => {
  return processLargeDataset(data);
});
````

### Profile Re-renders
````svelte
<script>
  import { afterUpdate } from 'svelte';

  let updateCount = 0;

  afterUpdate(() => {
    updateCount++;
    console.log('Component re-rendered', updateCount, 'times');
  });
</script>
````

### Find Memory Leaks

**Chrome DevTools Memory Tab**:
1. Take heap snapshot
2. Perform action
3. Take another snapshot
4. Compare snapshots
5. Look for growing objects

---

## TypeScript Debugging

### Type Errors as Debugging Aid
````typescript
// TypeScript catches bugs at compile time
function getUser(id: string): User {
  return fetchUser(id); // Error: fetchUser expects number
  // Bug found before runtime!
}
````

### Type Narrowing
````typescript
function processValue(value: string | number) {
  // TypeScript knows value could be either

  if (typeof value === 'string') {
    // TypeScript knows value is string here
    console.log(value.toUpperCase());
  } else {
    // TypeScript knows value is number here
    console.log(value.toFixed(2));
  }
}
````

### Any Type as Red Flag
````typescript
// ✗ Bad: Loses type safety
function process(data: any) {
  return data.value; // No error checking
}

// ✓ Good: Proper typing
function process(data: { value: string }) {
  return data.value; // TypeScript verifies structure
}
````

---

## Debugging Checklist

When stuck, systematically check:

**Environment**:
- [ ] Correct Node version?
- [ ] Dependencies installed? (`npm install`)
- [ ] Environment variables set?
- [ ] Correct database/API URL?

**Code**:
- [ ] Can you reproduce reliably?
- [ ] What's the exact error message?
- [ ] What line throws the error?
- [ ] What are variable values at that point?

**Data**:
- [ ] Is data in expected format?
- [ ] Are fields null/undefined?
- [ ] Is array empty when expected full?
- [ ] Are types correct (string vs number)?

**Network**:
- [ ] API request succeeding?
- [ ] Correct URL and method?
- [ ] Auth headers present?
- [ ] Response status 200?
- [ ] Response body as expected?

**State**:
- [ ] Component mounted?
- [ ] Store initialized?
- [ ] User authenticated?
- [ ] Data loaded before access?

---

## Portfolio Evidence

**KSBs Demonstrated**:
- **S10**: Analyse Problem Reports (systematic debugging approach)
- **S11**: Apply Appropriate Recovery Techniques (bug fixes)
- **S13**: Follow Testing Procedures (verification steps)

**How to Document**:
- Document bug investigation process
- Show before/after code
- Explain root cause analysis
- Include reproduction steps
- Show verification tests
- Screenshot DevTools usage

**Evidence Example**:
````markdown
## Bug Investigation: Infinite Scroll Crash

**Problem**: Clicking "Load More" twice caused page freeze

**Reproduction Steps**:
1. Navigate to /feed
2. Click "Load More"
3. Click "Load More" again
4. Page freezes

**Investigation**:
- Console showed "Maximum call stack exceeded"
- Debugger breakpoint revealed offset not incrementing
- Isolated to `loadMoreItems()` function

**Root Cause**:
Offset state not updating correctly, causing same API call repeatedly

**Fix**:
```typescript
// Before
function loadMore() {
  fetchItems(offset); // offset never changes
}

// After
function loadMore() {
  fetchItems(offset);
  offset += PAGE_SIZE; // Increment after fetch
}
```

**Verification**:
- Manual testing: ✓ Can click multiple times
- Added regression test
- No performance degradation
````

---

## Root-Cause vs Symptom Fixes

**Symptom fix**: Fixes the immediate problem but doesn't prevent recurrence.
**Root-cause fix**: Addresses the structural issue that allowed the bug to exist.

```typescript
// Symptom fix: Add null check where the crash happens
const name = user?.profile?.name ?? 'Unknown';

// Root-cause fix: Ensure profile is always populated at creation
async function createUser(data: CreateUserRequest): Promise<User> {
	return await db.users.create({
		...data,
		profile: { name: data.name } // Profile guaranteed at creation
	});
}
```

**When to ship a symptom fix**: When the root cause is expensive to fix and the symptom fix is safe. But always log the root cause as a follow-up task.

**When to insist on root-cause fix**: When the bug pattern could recur in other places, when data integrity is at risk, or when the symptom fix introduces its own complexity.

---

## Success Criteria

Debugging is effective when:
- Bugs reproduce reliably
- Root causes identified (not just symptoms)
- Fixes targeted and minimal
- No regressions introduced
- Process documented for learning
- Prevention strategies considered
- Structural patterns that enabled the bug are addressed or logged
