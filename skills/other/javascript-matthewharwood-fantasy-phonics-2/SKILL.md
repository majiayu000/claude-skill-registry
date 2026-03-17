---
name: javascript-pragmatic-rules
description: 30 pragmatic rules for production JavaScript covering async operations, V8 optimization, memory management, testing, error handling, and performance. Use when writing JavaScript, optimizing performance, handling promises, or building production-grade applications. Includes promise rejection handling, V8 hidden classes, memory leak prevention, and structured testing patterns.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch
---

# JavaScript Pragmatic Rules

30 battle-tested principles for production JavaScript.

## Relationship with Web Components

This skill provides best practices for **all JavaScript code**, including web components. When building interactive UI components with the Custom Elements API, combine this skill with `web-components-architecture`:

- **This skill (`javascript-pragmatic-rules`)**: HOW to write JavaScript correctly
  - Async patterns (Rules 1-4)
  - Error handling (Rules 7-10)
  - Performance optimization (Rules 16-22)
  - Testing strategies (Rules 12-15)

- **`web-components-architecture` skill**: WHAT pattern to use for components
  - Component lifecycle (connectedCallback, disconnectedCallback)
  - Shadow DOM and encapsulation
  - Attribute-driven state
  - HandleEvent pattern

**Example:** A custom `<data-table>` component should:
- Use `web-components-architecture` for structure (extends HTMLElement, uses Shadow DOM)
- Use `javascript-pragmatic-rules` Rule 4 for cleanup (disconnectedCallback removes listeners)
- Use `javascript-pragmatic-rules` Rule 17 for memory leak prevention
- Use `javascript-pragmatic-rules` Rule 2 for timeout on async data fetching

See `web-components-architecture` skill for component-specific patterns.

## Related Skills

- **`js-micro-utilities`**: Zero-dependency utility functions (debounce, throttle, deep clone, pick/omit). Use for production code when you need tested utilities.
- **`web-components-architecture`**: Component structure and lifecycle patterns

---

## Async Operations & Promises

### Rule 1: Handle Promise Rejections

Unhandled rejections corrupt state and make debugging impossible.

```javascript
// ✅ Explicit error handling with context
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return { success: true, data: await response.json() };
  } catch (error) {
    throw new Error(`User fetch failed for ${userId}`, { cause: error });
  }
}

// Global safety net
window.addEventListener('unhandledrejection', (e) => {
  console.error('Unhandled promise rejection:', e.reason);
  if (window.errorTracker) {
    window.errorTracker.captureException(e.reason);
  }
  e.preventDefault();
});

// Result type pattern
async function safeUserFetch(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) return { ok: false, error: `HTTP ${response.status}` };
    return { ok: true, value: await response.json() };
  } catch (error) {
    return { ok: false, error: error.message };
  }
}
```

### Rule 2: Time-Bound Async Operations

Network requests can hang indefinitely. Timeouts prevent resource exhaustion.

```javascript
// ✅ AbortController for cancellable fetch
async function fetchWithTimeout(url, timeoutMs = 5_000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error(`Request to ${url} timed out after ${timeoutMs}ms`);
    }
    throw error;
  }
}

// Advanced: timeout with exponential backoff retry
async function fetchWithRetry(url, options = {}) {
  const timeout = options.timeout ?? 5_000;
  const maxRetries = options.maxRetries ?? 3;
  const retryDelay = options.retryDelay ?? 1_000;
  const retryOn = options.retryOn ?? [408, 429, 500, 502, 503, 504];

  let lastError;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, { signal: controller.signal });
      clearTimeout(timeoutId);
      if (response.ok) return await response.json();

      if (!retryOn.includes(response.status)) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      lastError = new Error(`HTTP ${response.status}`);
    } catch (error) {
      clearTimeout(timeoutId);
      lastError = error.name === 'AbortError' ? new Error(`Timeout after ${timeout}ms`) : error;
    }

    if (attempt < maxRetries) {
      await new Promise(resolve => setTimeout(resolve, retryDelay * (2 ** attempt)));
    }
  }
  throw new Error(`Failed after ${maxRetries} retries`, { cause: lastError });
}
```

### Rule 3: Limit Concurrent Operations

Unbounded concurrency exhausts resources. Controlled concurrency prevents cascading failures.

```javascript
// ✅ Batch processing with concurrency limit
async function processInBatches(items, batchSize, processor) {
  const results = [];
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(batch.map(processor));
    results.push(...batchResults);
  }
  return results;
}

// ✅ Promise pool with semaphore
class PromisePool {
  #concurrency;
  #running = 0;
  #queue = [];

  constructor(concurrency) {
    this.#concurrency = concurrency;
  }

  async run(fn) {
    while (this.#running >= this.#concurrency) {
      await new Promise(resolve => this.#queue.push(resolve));
    }
    this.#running++;
    try {
      return await fn();
    } finally {
      this.#running--;
      const resolve = this.#queue.shift();
      if (resolve) resolve();
    }
  }
}

// Advanced: rate limiter with token bucket
class RateLimiter {
  #tokensPerSecond;
  #tokens;
  #maxTokens;
  #lastRefill;

  constructor(tokensPerSecond, burstSize = tokensPerSecond) {
    this.#tokensPerSecond = tokensPerSecond;
    this.#tokens = burstSize;
    this.#maxTokens = burstSize;
    this.#lastRefill = Date.now();
  }

  #refill() {
    const now = Date.now();
    const elapsed = (now - this.#lastRefill) / 1_000;
    this.#tokens = Math.min(this.#maxTokens, this.#tokens + elapsed * this.#tokensPerSecond);
    this.#lastRefill = now;
  }

  async acquire() {
    this.#refill();
    if (this.#tokens >= 1) {
      this.#tokens -= 1;
      return;
    }
    const timeToWait = ((1 - this.#tokens) / this.#tokensPerSecond) * 1_000;
    await new Promise(resolve => setTimeout(resolve, timeToWait));
    this.#refill();
    this.#tokens -= 1;
  }

  async run(fn) {
    await this.acquire();
    return fn();
  }
}
```

### Rule 4: Clean Up Resources

Orphaned timers/listeners cause memory leaks. Proper cleanup is essential.

```javascript
// ✅ Web Component cleanup
class TimerComponent extends HTMLElement {
  #intervalId = null;

  connectedCallback() {
    this.#intervalId = setInterval(() => {
      this.textContent = Date.now();
    }, 1_000);
  }

  disconnectedCallback() {
    if (this.#intervalId) {
      clearInterval(this.#intervalId);
      this.#intervalId = null;
    }
  }
}

// ✅ Cleanup registry pattern
class CleanupRegistry {
  #cleanups = [];

  registerTimeout(callback, delay) {
    const id = setTimeout(callback, delay);
    this.#cleanups.push(() => clearTimeout(id));
    return id;
  }

  registerInterval(callback, delay) {
    const id = setInterval(callback, delay);
    this.#cleanups.push(() => clearInterval(id));
    return id;
  }

  registerListener(element, event, handler, options) {
    element.addEventListener(event, handler, options);
    this.#cleanups.push(() => element.removeEventListener(event, handler, options));
  }

  registerCleanup(fn) {
    this.#cleanups.push(fn);
  }

  cleanup() {
    for (const fn of this.#cleanups) fn();
    this.#cleanups = [];
  }
}

// Usage in Web Component
class MyComponent extends HTMLElement {
  #cleanup = new CleanupRegistry();

  connectedCallback() {
    this.#cleanup.registerTimeout(() => console.log('Delayed'), 1_000);
    this.#cleanup.registerListener(window, 'resize', this.#handleResize.bind(this));
  }

  disconnectedCallback() {
    this.#cleanup.cleanup();
  }

  #handleResize() {
    // Handle resize
  }
}

// Advanced: cancellable polling
class Poller {
  #fn;
  #interval;
  #timeoutId = null;
  #isActive = false;

  constructor(fn, interval) {
    this.#fn = fn;
    this.#interval = interval;
  }

  async #poll() {
    if (!this.#isActive) return;
    try {
      await this.#fn();
    } catch (error) {
      console.error(error);
    }
    if (this.#isActive) {
      this.#timeoutId = setTimeout(() => queueMicrotask(() => this.#poll()), this.#interval);
    }
  }

  start() {
    if (this.#isActive) return;
    this.#isActive = true;
    queueMicrotask(() => this.#poll());
  }

  stop() {
    this.#isActive = false;
    if (this.#timeoutId) {
      clearTimeout(this.#timeoutId);
      this.#timeoutId = null;
    }
  }
}
```

## Object Design & Immutability

### Rule 4a: Initialize All Properties

V8 creates hidden classes for objects. Adding properties dynamically causes shape transitions, deoptimizing property access.

```javascript
// ✅ Initialize all properties upfront
class User {
  #name;
  #email;
  #age;

  constructor(name, email = null, age = null) {
    this.#name = name;
    this.#email = email;
    this.#age = age;
  }

  setEmail(email) {
    this.#email = email; // No shape transition, just value change
  }

  setAge(age) {
    this.#age = age;
  }

  getName() {
    return this.#name;
  }

  getEmail() {
    return this.#email;
  }

  getAge() {
    return this.#age;
  }
}

// Factory ensures consistent shapes
function createPoint(x = 0, y = 0, z = 0) {
  return { x, y, z };
}

// All points have identical shape
const points = Array.from({ length: 1_000 }, (_, i) => createPoint(i, i * 2, i * 3));

// Optimized loop - V8 knows exact shape
let sum = 0;
for (const point of points) {
  sum += point.x + point.y + point.z; // Fast property access
}
```

### Rule 5: Prefer Immutability

Immutability prevents bugs from shared mutable state, enables time-travel debugging, and makes code predictable.

```javascript
// ✅ Create new objects
function addItemToCart(cart, item) {
  return {
    ...cart,
    items: [...cart.items, item],
    total: cart.total + item.price
  };
}

// ✅ Immutable deep update
function updateUserAddress(user, newAddress) {
  return {
    ...user,
    profile: {
      ...user.profile,
      address: {
        ...user.profile.address,
        ...newAddress
      }
    }
  };
}

// ES2023 immutable array operations
const numbers = [5, 2, 8, 1, 9];
const sorted = numbers.toSorted((a, b) => a - b); // numbers unchanged
const reversed = numbers.toReversed(); // numbers unchanged
const spliced = numbers.toSpliced(1, 2, 99, 100); // numbers unchanged
const updated = numbers.with(2, 999); // numbers unchanged

// Deep cloning with structuredClone
const copy = structuredClone(original); // Handles dates, maps, sets, etc.
```

### Rule 6: Design for Cancellation

Users navigate away, components unmount. Cancellation prevents wasted work and race conditions.

```javascript
// ✅ Cancellable fetch in Web Component
class SearchComponent extends HTMLElement {
  #query = '';
  #results = [];
  #abortController = null;

  async #search() {
    if (this.#abortController) this.#abortController.abort();

    this.#abortController = new AbortController();
    const signal = this.#abortController.signal;

    try {
      const response = await fetch(`/api/search?q=${this.#query}`, { signal });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      this.#results = await response.json();
      this.render();
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('Search cancelled');
        return;
      }
      console.error('Search failed:', error);
    }
  }

  disconnectedCallback() {
    if (this.#abortController) this.#abortController.abort();
  }

  render() {
    // Render results
  }
}

// Generic cancellable async function
function makeCancellable(asyncFn) {
  let isCancelled = false;
  const controller = new AbortController();

  const promise = (async () => {
    try {
      const result = await asyncFn(controller.signal);
      if (isCancelled) throw new Error('Cancelled');
      return result;
    } catch (error) {
      if (isCancelled || error.name === 'AbortError') throw new Error('Cancelled');
      throw error;
    }
  })();

  return {
    promise,
    cancel: () => {
      isCancelled = true;
      controller.abort();
    }
  };
}
```

### Rule 7: Graceful Error Boundaries

Unhandled errors crash entire component trees. Error boundaries contain failures and preserve working UI.

```javascript
// ✅ Web Component error boundary
class ErrorBoundary extends HTMLElement {
  #hasError = false;
  #error = null;

  connectedCallback() {
    window.addEventListener('error', this.#handleError.bind(this));
    window.addEventListener('unhandledrejection', this.#handleRejection.bind(this));
  }

  disconnectedCallback() {
    window.removeEventListener('error', this.#handleError.bind(this));
    window.removeEventListener('unhandledrejection', this.#handleRejection.bind(this));
  }

  #handleError(event) {
    this.#hasError = true;
    this.#error = event.error;
    this.#render();
    if (window.errorTracker) {
      window.errorTracker.captureException(event.error);
    }
    event.preventDefault();
  }

  #handleRejection(event) {
    this.#hasError = true;
    this.#error = event.reason;
    this.#render();
    event.preventDefault();
  }

  #resetError() {
    this.#hasError = false;
    this.#error = null;
    this.#render();
  }

  #render() {
    if (this.#hasError) {
      this.innerHTML = `
        <div role="alert">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error Details</summary>
            <pre>${this.#error?.toString() ?? 'Unknown error'}</pre>
          </details>
          <button>Try again</button>
        </div>
      `;
      const button = this.querySelector('button');
      if (button) button.addEventListener('click', () => this.#resetError());
    }
  }
}

customElements.define('error-boundary', ErrorBoundary);
```

## Error Handling & Resilience

### Rule 8: Zero Uncaught Exceptions

Uncaught exceptions crash applications and corrupt state. Global handlers ensure all errors are logged.

```javascript
// ✅ Comprehensive error handling setup
class GlobalErrorHandler {
  #logger;

  constructor(options = {}) {
    this.#logger = options.logger ?? console;
    this.#setupHandlers();
  }

  #setupHandlers() {
    window.addEventListener('error', (event) => {
      this.#handleError({
        type: 'error',
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        error: event.error,
        timestamp: Date.now()
      });
      event.preventDefault();
    });

    window.addEventListener('unhandledrejection', (event) => {
      this.#handleError({
        type: 'unhandledRejection',
        reason: event.reason,
        timestamp: Date.now()
      });
      event.preventDefault();
    });
  }

  #handleError(errorInfo) {
    this.#logger.error('Global error:', errorInfo);

    // Send to error tracking service
    if (window.errorTracker) {
      window.errorTracker.captureException(errorInfo.error ?? errorInfo.reason, {
        extra: errorInfo
      });
    }

    // Use keepalive to ensure delivery
    if (navigator.sendBeacon) {
      navigator.sendBeacon('/api/errors', JSON.stringify(errorInfo));
    }
  }
}
```

### Rule 9: Small Module Interfaces

Large interfaces couple consumers to implementation details. Small, focused modules are easier to test and maintain.

```javascript
// ✅ Focused modules (1-3 exports)

// user_repository.js - Data access (1 export)
export class UserRepository {
  async findById(id) { /* ... */ }
  async save(user) { /* ... */ }
  async delete(id) { /* ... */ }
}

// user_validator.js - Validation (1 export)
export function validateUser(user) {
  const errors = [];
  if (!user.email || !isValidEmail(user.email)) errors.push('Invalid email');
  if (!user.password || user.password.length < 8) errors.push('Password must be 8+ characters');
  return { isValid: errors.length === 0, errors };
}

// Facade pattern for clean interface
export class OrderService {
  #payment;
  #inventory;
  #shipping;

  constructor() {
    this.#payment = new PaymentProcessor();
    this.#inventory = new InventoryManager();
    this.#shipping = new ShippingCalculator();
  }

  async createOrder(orderData) {
    const inventoryCheck = await this.#inventory.reserve(orderData.items);
    if (!inventoryCheck.success) throw new Error('Items not available');

    const shippingCost = await this.#shipping.calculate(orderData.address);
    const payment = await this.#payment.charge(orderData.paymentMethod, orderData.total + shippingCost);

    return { orderId: payment.orderId, total: orderData.total + shippingCost };
  }
}
```

### Rule 10: Map Errors to User Messages

Technical error messages confuse users. User-friendly messages improve UX.

```javascript
// ✅ Error mapping
class ErrorMapper {
  #errorMap = new Map([
    ['NETWORK_ERROR', { title: 'Connection Problem', message: 'Check your internet.', action: 'Retry' }],
    ['TIMEOUT', { title: 'Request Timeout', message: 'Request took too long. Try again.', action: 'Retry' }],
    ['UNAUTHORIZED', { title: 'Sign In Required', message: 'Session expired. Sign in again.', action: 'Sign In' }],
    ['FORBIDDEN', { title: 'Access Denied', message: 'No permission for this action.', action: null }],
    ['VALIDATION_ERROR', { title: 'Invalid Input', message: 'Check your input and try again.', action: 'Edit' }],
    ['SERVER_ERROR', { title: 'Server Error', message: 'Something went wrong. Team notified.', action: 'Contact Support' }],
    ['NOT_FOUND', { title: 'Not Found', message: 'Resource not found.', action: 'Go Back' }]
  ]);

  mapError(errorCode, context = {}) {
    const mapped = this.#errorMap.get(errorCode);
    if (!mapped) return { title: 'Unexpected Error', message: 'An error occurred. Try again.', action: 'Retry' };

    let message = mapped.message;
    for (const key of Object.keys(context)) {
      message = message.replaceAll(`{${key}}`, context[key]);
    }
    return { ...mapped, message };
  }

  fromHTTPStatus(status) {
    const statusMap = {
      400: 'VALIDATION_ERROR', 401: 'UNAUTHORIZED', 403: 'FORBIDDEN', 404: 'NOT_FOUND',
      408: 'TIMEOUT', 429: 'RATE_LIMITED', 500: 'SERVER_ERROR', 502: 'SERVER_ERROR',
      503: 'SERVER_ERROR', 504: 'TIMEOUT'
    };
    return this.mapError(statusMap[status] ?? 'SERVER_ERROR');
  }
}
```

## Logging & Observability

### Rule 11: Structured Logging

Plain text logs are hard to query. Structured logs enable powerful filtering and debugging.

```javascript
// ✅ Structured logging with context
class Logger {
  #serviceName;
  #environment;
  #minimumLevel;
  #levels = { debug: 0, info: 1, warn: 2, error: 3 };

  constructor(options = {}) {
    this.#serviceName = options.serviceName ?? 'app';
    this.#environment = options.environment ?? 'development';
    this.#minimumLevel = options.minimumLevel ?? 'info';
  }

  log(level, message, context = {}) {
    if (this.#levels[level] < this.#levels[this.#minimumLevel]) return;

    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      service: this.#serviceName,
      environment: this.#environment,
      message,
      ...context
    };

    if (this.#environment === 'production' && navigator.sendBeacon) {
      navigator.sendBeacon('/api/logs', JSON.stringify(logEntry));
    }

    console[level](JSON.stringify(logEntry));
  }

  info(message, context) { this.log('info', message, context); }
  warn(message, context) { this.log('warn', message, context); }
  error(message, error, context = {}) {
    this.log('error', message, {
      ...context,
      error: { message: error.message, stack: error.stack, name: error.name }
    });
  }
}

// Performance logging
class PerformanceLogger extends Logger {
  startTimer(operation) {
    const timerId = `${operation}_${Date.now()}`;
    performance.mark(`${timerId}_start`);
    return timerId;
  }

  endTimer(timerId, operation, context = {}) {
    performance.mark(`${timerId}_end`);
    try {
      performance.measure(timerId, `${timerId}_start`, `${timerId}_end`);
      const measure = performance.getEntriesByName(timerId)[0];
      if (measure) {
        this.info('Operation completed', { operation, duration: measure.duration, ...context });
      }
      performance.clearMarks(`${timerId}_start`);
      performance.clearMarks(`${timerId}_end`);
      performance.clearMeasures(timerId);
      return measure ? measure.duration : null;
    } catch (error) {
      this.error('Failed to measure performance', error);
      return null;
    }
  }
}
```

### Rule 12: Table-Driven Tests

Repetitive test code is error-prone. Table-driven tests make it easy to add cases and see patterns.

```javascript
// ✅ Table-driven tests
describe('calculateDiscount', () => {
  const testCases = [
    [100, 1, 0, 'No discount for single item'],
    [100, 5, 10, '10% discount for 5 items'],
    [100, 10, 20, '20% discount for 10 items'],
    [100, 20, 30, '30% discount for 20+ items'],
    [0, 10, 0, 'Zero price returns zero'],
    [100, 0, 0, 'Zero quantity returns zero']
  ];

  for (const [price, quantity, expected, description] of testCases) {
    test(`${description}: calculateDiscount(${price}, ${quantity}) = ${expected}`, () => {
      expect(calculateDiscount(price, quantity)).toBe(expected);
    });
  }
});

// Complex test cases
describe('validateEmail', () => {
  const testCases = [
    ['user@example.com', true],
    ['user.name@example.com', true],
    ['user+tag@example.co.uk', true],
    ['', false],
    ['invalid', false],
    ['@example.com', false],
    ['user@', false]
  ];

  for (const [email, expected] of testCases) {
    test(`validateEmail("${email}") should return ${expected}`, () => {
      expect(validateEmail(email)).toBe(expected);
    });
  }
});
```

## Testing Strategy

### Rule 13: Realistic API Testing

Unit tests with mocks don't catch integration issues. Realistic API tests provide confidence.

```javascript
// ✅ Browser-based fetch mocking
const originalFetch = window.fetch;

function mockFetch(handlers) {
  window.fetch = async (url, options = {}) => {
    for (const handler of handlers) {
      const match = url.match(handler.pattern);
      if (match && options.method === handler.method) {
        const response = await handler.handler(match, options.body);
        return new Response(JSON.stringify(response.body), {
          status: response.status,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    return originalFetch(url, options);
  };
}

function restoreFetch() {
  window.fetch = originalFetch;
}

// Usage
const handlers = [
  {
    method: 'GET',
    pattern: /\/api\/users\/(\d+)/,
    handler: async (match) => {
      const id = match[1];
      if (id === '999') return { status: 404, body: { error: 'User not found' } };
      return { status: 200, body: { id, name: 'Test User', email: 'test@example.com' } };
    }
  }
];

mockFetch(handlers);
// Run tests
restoreFetch();
```

### Rule 14: Property-Based Tests

Example-based tests only cover known cases. Property-based tests generate random inputs, finding edge cases.

```javascript
// ✅ Property-based testing
describe('Array sorting', () => {
  // Property: sorted array should be in ascending order
  test('sort produces ascending order', () => {
    for (let i = 0; i < 100; i++) {
      const arr = generateRandomArray();
      const sorted = arr.toSorted((a, b) => a - b);
      for (let j = 1; j < sorted.length; j++) {
        expect(sorted[j]).toBeGreaterThanOrEqual(sorted[j - 1]);
      }
    }
  });

  // Property: sorted array contains same elements
  test('sort preserves all elements', () => {
    for (let i = 0; i < 100; i++) {
      const arr = generateRandomArray();
      const sorted = arr.toSorted((a, b) => a - b);
      expect(sorted).toHaveLength(arr.length);
      for (const item of sorted) expect(arr.includes(item)).toBe(true);
    }
  });

  // Property: sorting twice gives same result (idempotence)
  test('sort is idempotent', () => {
    for (let i = 0; i < 100; i++) {
      const arr = generateRandomArray();
      const sorted1 = arr.toSorted((a, b) => a - b);
      const sorted2 = sorted1.toSorted((a, b) => a - b);
      expect(sorted1).toEqual(sorted2);
    }
  });
});

function generateRandomArray() {
  const length = Math.floor(Math.random() * 100);
  return Array.from({ length }, () => Math.floor(Math.random() * 1_000) - 500);
}
```

### Rule 15: Debounce/Throttle UI Events

High-frequency events can fire hundreds of times per second, causing performance issues.

> **Production tip:** For tested implementations with edge case handling, use `just-debounce-it` and `just-throttle` from the `js-micro-utilities` skill. The implementations below show how these patterns work.

```javascript
// ✅ Debounce implementation
function debounce(fn, delay) {
  let timeoutId = null;
  return (...args) => {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      fn(...args);
      timeoutId = null;
    }, delay);
  };
}

// Usage
const searchInput = document.getElementById('search');
const debouncedSearch = debounce(async (query) => {
  const response = await fetch(`/api/search?q=${query}`);
  const results = await response.json();
  displayResults(results);
}, 300);

searchInput.addEventListener('input', (e) => debouncedSearch(e.target.value));

// ✅ Throttle implementation
function throttle(fn, limit) {
  let inThrottle = false;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Usage
const throttledScroll = throttle(() => {
  const scrollY = window.scrollY;
  document.getElementById('back-to-top').style.display = scrollY > 500 ? 'block' : 'none';
}, 100);

window.addEventListener('scroll', throttledScroll);
```

## Performance Optimization

### Rule 16: Profile Before Optimizing

Premature optimization wastes time. Profiling identifies actual bottlenecks.

```javascript
// ✅ Performance API
const start = performance.now();
expensiveOperation();
console.log(`Took ${performance.now() - start}ms`);

// Comprehensive performance monitoring
class PerformanceMonitor {
  #name;

  constructor(name) {
    this.#name = name;
  }

  start(label = 'default') {
    performance.mark(`${this.#name}_${label}_start`);
  }

  end(label = 'default') {
    const startMark = `${this.#name}_${label}_start`;
    const endMark = `${this.#name}_${label}_end`;
    performance.mark(endMark);
    performance.measure(`${this.#name}_${label}`, startMark, endMark);
    const measure = performance.getEntriesByName(`${this.#name}_${label}`)[0];
    const duration = measure.duration;
    if (duration > 100) console.warn(`Slow: ${this.#name}_${label} took ${duration.toFixed(2)}ms`);
    performance.clearMarks(startMark);
    performance.clearMarks(endMark);
    performance.clearMeasures(`${this.#name}_${label}`);
    return duration;
  }
}
```

### Rule 17: Avoid Memory Leaks

Memory leaks degrade performance over time. Proper cleanup is essential.

```javascript
// ✅ Web Component comprehensive cleanup
class DataTable extends HTMLElement {
  #cleanup = [];
  #intervalId = null;
  #observer = null;

  connectedCallback() {
    const handleResize = () => this.#updateLayout();
    window.addEventListener('resize', handleResize);
    this.#cleanup.push(() => window.removeEventListener('resize', handleResize));

    this.#observer = new IntersectionObserver((entries) => this.#handleIntersection(entries));
    this.#observer.observe(this);
    this.#cleanup.push(() => this.#observer.disconnect());

    this.#intervalId = setInterval(() => this.#fetchUpdates(), 5_000);
    this.#cleanup.push(() => clearInterval(this.#intervalId));
  }

  disconnectedCallback() {
    for (const fn of this.#cleanup) fn();
    this.#cleanup = [];
  }

  #updateLayout() {}
  #handleIntersection(entries) {}
  #fetchUpdates() {}
}
```

### Rule 18: Use Web Workers for CPU Work

Heavy computation blocks the main thread. Web Workers enable true parallelism.

```javascript
// ✅ Offload computation to worker

// worker.js
self.onmessage = (event) => {
  const { type, data } = event.data;
  if (type === 'PROCESS_DATA') {
    const result = processLargeDataset(data);
    self.postMessage({ type: 'RESULT', result });
  }
};

function processLargeDataset(data) {
  return data.map(item => {
    let result = item;
    for (let i = 0; i < 1_000; i++) result = transform(result);
    return result;
  });
}

function transform(value) {
  return value * 2 + 1;
}

// main.js
class WorkerPool {
  #workers = [];
  #queue = [];
  #activeJobs = new Map();

  constructor(workerPath, poolSize = navigator.hardwareConcurrency ?? 4) {
    for (let i = 0; i < poolSize; i++) {
      const worker = new Worker(workerPath);
      worker.onmessage = (event) => this.#handleMessage(worker, event);
      worker.onerror = (error) => this.#handleError(worker, error);
      this.#workers.push({ worker, isBusy: false });
    }
  }

  async execute(type, data) {
    return new Promise((resolve, reject) => {
      const job = { type, data, resolve, reject };
      this.#queue.push(job);
      this.#processQueue();
    });
  }

  #processQueue() {
    if (this.#queue.length === 0) return;
    const availableWorker = this.#workers.find(w => !w.isBusy);
    if (!availableWorker) return;

    const job = this.#queue.shift();
    availableWorker.isBusy = true;
    this.#activeJobs.set(availableWorker.worker, job);
    availableWorker.worker.postMessage({ type: job.type, data: job.data });
  }

  #handleMessage(worker, event) {
    const job = this.#activeJobs.get(worker);
    if (!job) return;

    const workerInfo = this.#workers.find(w => w.worker === worker);
    if (workerInfo) workerInfo.isBusy = false;

    this.#activeJobs.delete(worker);
    job.resolve(event.data);
    this.#processQueue();
  }

  #handleError(worker, error) {
    const job = this.#activeJobs.get(worker);
    if (job) {
      job.reject(error);
      this.#activeJobs.delete(worker);
    }
    const workerInfo = this.#workers.find(w => w.worker === worker);
    if (workerInfo) workerInfo.isBusy = false;
    this.#processQueue();
  }
}
```

### Rule 19: Avoid Deoptimization Triggers

V8 optimizes hot functions with TurboFan JIT. Certain patterns trigger deoptimization.

```javascript
// ❌ Triggers deoptimization
delete obj.property;
function bad() { console.log(arguments); }
eval(code);
try { return x * 2; } catch (error) { return 0; }

// ✅ Optimization-friendly
obj.property = undefined; // Set to undefined instead of delete
const good = (...args) => args.reduce((a, b) => a + b, 0); // Rest params instead of arguments
new Function(code)(); // Function constructor instead of eval

// Move try-catch out of hot path
function goodTryCatch(x) {
  return calculate(x); // Hot path is optimizable
}

function calculate(x) {
  return x * 2; // Can be inlined and optimized
}

// Wrap in try-catch at call site only if needed
try {
  const result = goodTryCatch(value);
} catch (error) {
  // Handle error
}

// Keep call sites monomorphic (single type)
function numberToString(num) {
  return String(num); // Always called with numbers
}

function processNumbers(numbers) {
  return numbers.map(n => numberToString(n)); // Monomorphic
}
```

### Rule 20: Prefer requestAnimationFrame

setTimeout/setInterval aren't synchronized with display refresh, causing jank. requestAnimationFrame ensures smooth 60fps animations.

```javascript
// ✅ Smooth animation
class Animator {
  #rafId = null;
  #isRunning = false;

  animate(callback) {
    if (this.#isRunning) return;
    this.#isRunning = true;
    let lastTime = performance.now();

    const loop = (currentTime) => {
      if (!this.#isRunning) return;
      const deltaTime = currentTime - lastTime;
      lastTime = currentTime;
      callback(deltaTime, currentTime);
      this.#rafId = requestAnimationFrame(loop);
    };

    this.#rafId = requestAnimationFrame(loop);
  }

  stop() {
    this.#isRunning = false;
    if (this.#rafId) {
      cancelAnimationFrame(this.#rafId);
      this.#rafId = null;
    }
  }
}

// Usage: smooth scroll animation
function smoothScroll(targetY, duration = 1_000) {
  const startY = window.scrollY;
  const distance = targetY - startY;
  const startTime = performance.now();
  const animator = new Animator();

  animator.animate((delta, currentTime) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeInOutCubic(progress);
    window.scrollTo(0, startY + distance * eased);
    if (progress >= 1) animator.stop();
  });
}

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - ((-2 * t + 2) ** 3) / 2;
}
```

### Rule 21: Keep Array Types Consistent

V8 uses specialized array representations. Mixing types downgrades arrays to slower generic mode.

```javascript
// ✅ PACKED_SMI_ELEMENTS (Fastest)
const integers = [1, 2, 3, 4, 5]; // All small integers (31-bit), no holes

// ✅ PACKED_DOUBLE_ELEMENTS (Fast)
const doubles = [1.5, 2.7, 3.14, 4.2]; // All doubles, no holes

// ⚠️ PACKED_ELEMENTS (Slower)
const mixed = [1, 'string', {}, null]; // Mixed types

// ❌ HOLEY_SMI_ELEMENTS (Slow)
const holey = [1, 2, , 4, 5]; // Has holes (empty slots)

// ❌ HOLEY_ELEMENTS (Slowest)
const worst = [1, , 'string', , {}]; // Mixed types AND holes

// ✅ Avoid holes
const array1 = new Array(100).fill(0); // PACKED_SMI
const array2 = [];
for (let i = 0; i < 100; i++) array2.push(i); // PACKED_SMI

// ❌ Delete creates holes
const arr = [1, 2, 3, 4, 5];
delete arr[2]; // Now HOLEY

// ✅ Splice to remove
const arr2 = [1, 2, 3, 4, 5];
arr2.splice(2, 1); // Still PACKED
```

### Rule 22: Use Typed Arrays for Numerics

Typed arrays provide native memory layout, enabling SIMD operations and cache-friendly access. 10-100x faster than regular arrays for numeric computation.

```javascript
// ✅ Image processing
class ImageProcessor {
  #width;
  #height;
  #data;

  constructor(width, height) {
    this.#width = width;
    this.#height = height;
    this.#data = new Uint8ClampedArray(width * height * 4); // RGBA: 4 bytes per pixel
  }

  getPixel(x, y) {
    const index = (y * this.#width + x) * 4;
    return {
      r: this.#data[index],
      g: this.#data[index + 1],
      b: this.#data[index + 2],
      a: this.#data[index + 3]
    };
  }

  setPixel(x, y, r, g, b, a = 255) {
    const index = (y * this.#width + x) * 4;
    this.#data[index] = r;
    this.#data[index + 1] = g;
    this.#data[index + 2] = b;
    this.#data[index + 3] = a;
  }

  toGrayscale() {
    for (let i = 0; i < this.#data.length; i += 4) {
      const gray = this.#data[i] * 0.299 + this.#data[i + 1] * 0.587 + this.#data[i + 2] * 0.114;
      this.#data[i] = this.#data[i + 1] = this.#data[i + 2] = gray;
    }
  }
}

// Physics simulation
class ParticleSystem {
  #positions; // x, y, z
  #velocities;
  #count;

  constructor(count) {
    // Structure of Arrays (SoA) for cache efficiency
    this.#positions = new Float64Array(count * 3);
    this.#velocities = new Float64Array(count * 3);
    this.#count = count;
  }

  update(deltaTime) {
    for (let i = 0; i < this.#count; i++) {
      const idx = i * 3;
      this.#positions[idx] += this.#velocities[idx] * deltaTime;
      this.#positions[idx + 1] += this.#velocities[idx + 1] * deltaTime;
      this.#positions[idx + 2] += this.#velocities[idx + 2] * deltaTime;
      this.#velocities[idx + 1] -= 9.8 * deltaTime; // Gravity
    }
  }
}
```

## Quick Reference

### Async
```javascript
// Timeout: await fetchWithTimeout(url, 5_000)
// Pool: const pool = new PromisePool(10); await pool.run(fn)
// Cleanup: disconnectedCallback() { clearInterval(this.intervalId); }
```

### Objects
```javascript
// Init all: constructor() { this.#prop1 = val1; this.#prop2 = val2; }
// Immutable: const next = { ...state, updated: true }
// Cancel: const controller = new AbortController(); () => controller.abort()
```

### Performance
```javascript
// Profile: const start = performance.now(); work(); console.log(performance.now() - start)
// Typed array: const buffer = new Float64Array(1_000)
// Monomorphic: Keep single type at each call site
```

### Common Gotchas
```javascript
// ❌ Don't
delete obj.prop; // Use obj.prop = undefined
function f() { arguments } // Use rest params
eval(code); // Use Function()
with (obj) {} // Use destructuring
const arr = [1, , 3]; // No holes
const mixed = [1, 'two']; // Keep types consistent

// ✅ Do
obj.prop = undefined;
const f = (...args) => {};
new Function(code)();
const { value } = obj;
const arr = [1, 0, 3];
const numbers = [1, 2, 3];
```

### Priority Matrix

**Always Apply:**
- Handle rejections (Rule 1)
- Timeout async (Rule 2)
- Clean up resources (Rule 4)
- Init properties (Rule 4a)
- Global errors (Rule 8)

**Hot Paths Only (>10k ops/sec):**
- V8 optimization (Rules 19-22)
- Web Workers (Rule 18)
- Array optimization (Rule 21-22)

**As Needed:**
- Concurrency limits (Rule 3)
- Immutability (Rule 5)
- Cancellation (Rule 6)
- Error boundaries (Rule 7)

---

For V8 optimization deep dive (Rules 22a-27), see V8_OPTIMIZATION.md.
