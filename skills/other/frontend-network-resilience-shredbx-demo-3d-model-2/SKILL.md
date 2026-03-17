---
description: Network resilience patterns for frontend - retry logic, exponential backoff, error handling, offline detection
tags: [frontend, network, resilience, retry, error-handling, UX]
related_skills: [frontend-svelte, dev-philosophy, dev-code-quality]
applies_to: [Plan, dev-frontend-svelte]
---

# Frontend Network Resilience Patterns

Comprehensive patterns for building robust network operations in frontend applications.

---

## Core Principles

1. **Never trust the network** - Always plan for failure
2. **Fail gracefully** - Degrade functionality, don't break completely
3. **Provide feedback** - User should know what's happening
4. **Auto-recover** - Retry transient failures automatically
5. **Differentiate errors** - Different errors need different messages

---

## Pattern 1: Exponential Backoff Retry

**When to Use:**
- Loading external SDKs (Clerk, Stripe, Google Maps)
- API calls to backend services
- Third-party API integrations
- CDN resource loading

**When NOT to Use:**
- User-initiated actions (use immediate retry with button instead)
- Real-time operations (WebSocket - use reconnection logic instead)
- Operations that must succeed exactly once (payments - use idempotency)

**Implementation Pattern:**

```typescript
/**
 * Retry an operation with exponential backoff
 *
 * @param operation - Async function to retry
 * @param maxAttempts - Maximum number of attempts (default: 4)
 * @param initialDelay - Initial delay in ms (default: 2000)
 * @param maxDelay - Maximum delay in ms (default: 30000)
 * @returns Result of operation or throws after all attempts exhausted
 */
async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  maxAttempts = 4,
  initialDelay = 2000,
  maxDelay = 30000
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      // Last attempt - rethrow error
      if (attempt === maxAttempts) {
        throw error;
      }

      // Calculate delay with exponential backoff
      const delay = Math.min(
        initialDelay * Math.pow(2, attempt - 1),
        maxDelay
      );

      console.log(`Attempt ${attempt}/${maxAttempts} failed, retrying in ${delay}ms...`);

      // Wait before next attempt
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('All retry attempts exhausted');
}
```

**Usage Example:**

```typescript
// Loading external SDK with retry
const sdkLoaded = await retryWithBackoff(
  async () => {
    if (!sdk.loaded) {
      throw new Error('SDK not ready');
    }
    return true;
  },
  4,      // 4 attempts
  2000,   // Start with 2s delay
  30000   // Max 30s delay
);
```

**Backoff Schedule Examples:**

```
4 attempts, 2s initial:
  Attempt 1 → wait 2s → Attempt 2 → wait 4s → Attempt 3 → wait 8s → Attempt 4
  Total: ~14s

4 attempts, 3s initial:
  Attempt 1 → wait 3s → Attempt 2 → wait 6s → Attempt 3 → wait 12s → Attempt 4
  Total: ~21s

5 attempts, 2s initial:
  Attempt 1 → wait 2s → Attempt 2 → wait 4s → Attempt 3 → wait 8s →
  Attempt 4 → wait 16s → Attempt 5
  Total: ~30s
```

---

## Pattern 2: Error Type Differentiation

**Error Taxonomy:**

```typescript
type NetworkErrorType =
  | 'offline'           // No internet connection
  | 'timeout'           // Request/load took too long
  | 'blocked'           // Blocked by browser/extension/firewall
  | 'not_found'         // Resource doesn't exist (404)
  | 'server_error'      // Server returned 5xx
  | 'unauthorized'      // Auth failed (401/403)
  | 'rate_limited'      // Too many requests (429)
  | 'network_error'     // Generic network failure
  | 'unknown';          // Unclassified error

interface NetworkError {
  type: NetworkErrorType;
  message: string;
  userMessage: string;  // User-friendly message
  canRetry: boolean;    // Should we offer retry?
  autoRetry: boolean;   // Should we auto-retry?
}
```

**Error Detection:**

```typescript
function classifyNetworkError(error: any): NetworkError {
  // Offline detection
  if (!navigator.onLine) {
    return {
      type: 'offline',
      message: 'Network offline',
      userMessage: 'No internet connection. Please check your network.',
      canRetry: true,
      autoRetry: false  // Don't auto-retry if offline
    };
  }

  // Timeout
  if (error.name === 'TimeoutError' || error.message?.includes('timeout')) {
    return {
      type: 'timeout',
      message: error.message,
      userMessage: 'Connection is very slow. Please check your internet.',
      canRetry: true,
      autoRetry: true  // Auto-retry timeouts
    };
  }

  // Blocked (CSP, ad blocker, CORS)
  if (error.message?.includes('blocked') ||
      error.message?.includes('CSP') ||
      error.name === 'SecurityError') {
    return {
      type: 'blocked',
      message: error.message,
      userMessage: 'Resource blocked. Please disable ad blockers.',
      canRetry: true,
      autoRetry: false  // User must fix blocker first
    };
  }

  // HTTP status codes
  if (error.status === 404) {
    return {
      type: 'not_found',
      message: error.message,
      userMessage: 'Resource not found.',
      canRetry: false,
      autoRetry: false
    };
  }

  if (error.status >= 500) {
    return {
      type: 'server_error',
      message: error.message,
      userMessage: 'Server error. Please try again later.',
      canRetry: true,
      autoRetry: true  // Server errors are often transient
    };
  }

  if (error.status === 401 || error.status === 403) {
    return {
      type: 'unauthorized',
      message: error.message,
      userMessage: 'Please sign in again.',
      canRetry: false,
      autoRetry: false
    };
  }

  if (error.status === 429) {
    return {
      type: 'rate_limited',
      message: error.message,
      userMessage: 'Too many requests. Please wait a moment.',
      canRetry: true,
      autoRetry: true  // With longer backoff
    };
  }

  // Generic network error
  return {
    type: 'network_error',
    message: error.message || 'Unknown error',
    userMessage: 'Network error. Please try again.',
    canRetry: true,
    autoRetry: true
  };
}
```

---

## Pattern 3: Offline Detection

**Implementation:**

```typescript
import { onMount } from 'svelte';

let isOnline = $state(true);

onMount(() => {
  // Initial check
  isOnline = navigator.onLine;

  // Listen for online/offline events
  const handleOnline = () => { isOnline = true; };
  const handleOffline = () => { isOnline = false; };

  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);

  return () => {
    window.removeEventListener('online', handleOnline);
    window.removeEventListener('offline', handleOffline);
  };
});
```

**Usage in Components:**

```svelte
{#if !isOnline}
  <div class="offline-banner">
    ⚠️ No internet connection. Some features may not work.
  </div>
{/if}

<button
  onclick={handleAction}
  disabled={!isOnline}
>
  Submit
</button>
```

---

## Pattern 4: Progressive Loading with Feedback

**For External SDK Loading:**

```svelte
<script lang="ts">
  let loadingState = $state<'idle' | 'loading' | 'ready' | 'error'>('idle');
  let loadingTime = $state(0);
  let attemptNumber = $state(0);
  let error = $state<NetworkError | null>(null);

  // Show progress message after 3s
  let showProgress = $derived(loadingTime > 3);

  async function loadSDK() {
    loadingState = 'loading';
    loadingTime = 0;

    // Update loading time every second
    const interval = setInterval(() => {
      loadingTime++;
    }, 1000);

    try {
      await retryWithBackoff(
        async () => {
          attemptNumber++;
          // SDK load logic
          if (!sdk.loaded) throw new Error('Not ready');
          return true;
        },
        4,
        2000
      );

      clearInterval(interval);
      loadingState = 'ready';
    } catch (err) {
      clearInterval(interval);
      loadingState = 'error';
      error = classifyNetworkError(err);
    }
  }
</script>

{#if loadingState === 'loading'}
  <div class="loading-container">
    <Spinner />

    {#if attemptNumber > 1}
      <p>Connecting... (attempt {attemptNumber}/4)</p>
    {:else if showProgress}
      <p>This is taking longer than expected ({loadingTime}s)...</p>
    {:else}
      <p>Loading...</p>
    {/if}
  </div>
{:else if loadingState === 'error'}
  <ErrorMessage
    error={error}
    onRetry={error.canRetry ? loadSDK : undefined}
  />
{/if}
```

---

## Pattern 5: SSR-Friendly Network Operations

**Guidelines:**

1. **Never call network operations during SSR**
   ```typescript
   // ❌ BAD - Will fail during SSR
   const data = await fetch('/api/data');

   // ✅ GOOD - Only runs client-side
   onMount(async () => {
     const data = await fetch('/api/data');
   });
   ```

2. **Provide initial loading state in SSR HTML**
   ```svelte
   <!-- This renders during SSR -->
   <div class="content">
     {#if data}
       <DataDisplay {data} />
     {:else}
       <!-- This spinner is in SSR HTML -->
       <Spinner />
       <p>Loading content...</p>
     {/if}
   </div>
   ```

3. **Handle hydration gracefully**
   ```typescript
   let data = $state(null);
   let isLoading = $state(true); // true during SSR and hydration

   onMount(async () => {
     // This runs after hydration
     data = await loadData();
     isLoading = false;
   });
   ```

---

## Planning Checklist

When planning any feature with network operations, ensure:

### Network Operation Requirements
- [ ] Retry logic with exponential backoff specified
- [ ] Number of attempts and timing justified (e.g., 4 attempts, 2s initial)
- [ ] Error types are differentiated with appropriate messages
- [ ] Offline state is detected and handled
- [ ] Timeout values are specified and justified
- [ ] Manual retry option provided (button)
- [ ] Loading states defined for all durations (0-3s, 3-10s, 10s+)

### SSR/Hydration Requirements
- [ ] Network operations only in onMount or client-side code
- [ ] Initial loading state present in SSR HTML
- [ ] No flash of incorrect content (FOUC) during hydration
- [ ] Progressive enhancement considered

### UX Requirements
- [ ] User sees feedback within 1s (spinner, progress indicator)
- [ ] Progress message shown if loading > 3s
- [ ] Error messages are user-friendly and actionable
- [ ] User can retry without full page refresh
- [ ] Graceful degradation if JS disabled (where possible)

---

## Testing Requirements

All network operations must include tests for:

1. **Success scenario** - Normal network conditions
2. **Slow network** - Simulated 3G (3-5s response time)
3. **Very slow network** - Extreme latency (8-10s)
4. **Offline** - No internet connection
5. **Timeout** - No response within timeout period
6. **Intermittent failure** - Fails first 2 attempts, succeeds on 3rd
7. **Persistent failure** - Fails all retry attempts
8. **Error types** - 401, 403, 404, 429, 500, 503

**Playwright Example:**

```typescript
test('SDK loads with retry on slow network', async ({ page, context }) => {
  // Simulate slow 3G
  await context.route('**/clerk.sdk.js', async (route) => {
    await new Promise(resolve => setTimeout(resolve, 4000));
    await route.continue();
  });

  await page.goto('/login');

  // Should show loading state
  await expect(page.locator('.spinner')).toBeVisible();

  // Should show progress message after 3s
  await expect(page.locator('text=Taking longer')).toBeVisible({ timeout: 4000 });

  // Should eventually load
  await expect(page.locator('.clerk-sign-in')).toBeVisible({ timeout: 10000 });
});
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Single Timeout Without Retry

```typescript
// BAD - Gives up after one timeout
const loaded = await waitForSDK(10000);
if (!loaded) {
  showError('Failed to load');
}
```

```typescript
// GOOD - Retries with backoff
const loaded = await retryWithBackoff(
  () => waitForSDK(5000),
  4,
  2000
);
```

### ❌ Mistake 2: Generic Error Messages

```typescript
// BAD - Same message for all errors
catch (error) {
  showError('Something went wrong. Please try again.');
}
```

```typescript
// GOOD - Differentiated messages
catch (error) {
  const networkError = classifyNetworkError(error);
  showError(networkError.userMessage);

  if (networkError.canRetry) {
    showRetryButton();
  }
}
```

### ❌ Mistake 3: Ignoring Offline State

```typescript
// BAD - Attempts network call while offline
async function loadData() {
  return await fetch('/api/data');
}
```

```typescript
// GOOD - Checks offline state first
async function loadData() {
  if (!navigator.onLine) {
    throw new Error('offline');
  }
  return await fetch('/api/data');
}
```

### ❌ Mistake 4: Network Calls During SSR

```typescript
// BAD - Will fail during SSR
const data = await fetch('/api/data');
```

```typescript
// GOOD - Only client-side
let data = $state(null);

onMount(async () => {
  data = await fetch('/api/data');
});
```

---

## References

- [MDN: Exponential Backoff](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB#using_experimental_features)
- [Google Cloud: Retry Strategy](https://cloud.google.com/iot/docs/how-tos/exponential-backoff)
- [AWS: Error Retries and Exponential Backoff](https://docs.aws.amazon.com/general/latest/gr/api-retries.html)
- [SvelteKit: Load Functions](https://kit.svelte.dev/docs/load)

---

**Last Updated:** 2025-11-06
**Applies To:** All frontend network operations
**Mandatory:** YES - Plan agents must reference this during planning
