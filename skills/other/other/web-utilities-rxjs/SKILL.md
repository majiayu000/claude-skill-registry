---
name: web-utilities-rxjs
description: Reactive programming with RxJS - Observables, operators, Subjects, error handling, and memory leak prevention
---

# RxJS Reactive Programming Patterns

> **Quick Guide:** Use RxJS for complex async flows involving event streams, composed async operations, and reactive data pipelines. Create Observables with `of`, `from`, `fromEvent`, or `defer`. Transform with pipeable operators (`map`, `filter`, `switchMap`). Always unsubscribe to prevent memory leaks -- use the `takeUntil` pattern with a destroy Subject, or store subscriptions and call `unsubscribe()` in cleanup. Suffix observable variables with `$`. Choose the right flattening operator: `switchMap` to cancel previous, `mergeMap` for parallel, `concatMap` for sequential, `exhaustMap` to ignore while busy.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST unsubscribe from every long-lived Observable -- use `takeUntil`, `take`, `first`, or explicit `unsubscribe()` to prevent memory leaks)**

**(You MUST choose the correct flattening operator -- `switchMap` for cancellation, `mergeMap` for parallel, `concatMap` for sequential, `exhaustMap` to ignore while busy)**

**(You MUST place `takeUntil` LAST in the pipe chain -- placing it before higher-order operators like `switchMap` leaves inner subscriptions alive)**

**(You MUST handle errors with `catchError` inside the pipe -- an unhandled error terminates the entire Observable chain permanently)**

</critical_requirements>

---

**Auto-detection:** RxJS, rxjs, Observable, Subject, BehaviorSubject, ReplaySubject, AsyncSubject, subscribe, pipe, switchMap, mergeMap, concatMap, exhaustMap, combineLatest, forkJoin, fromEvent, of, from, interval, timer, defer, catchError, retry, debounceTime, throttleTime, distinctUntilChanged, takeUntil, map, filter, tap, shareReplay

**When to use:**

- Complex async flows composing multiple HTTP requests, WebSockets, or event streams
- Event stream processing with debounce, throttle, or buffer logic
- Real-time data pipelines (stock tickers, chat, live updates)
- Cancellable HTTP requests (type-ahead search, route changes)
- Coordinating multiple async sources (race, combine, fork-join)

**When NOT to use:**

- Simple one-shot HTTP requests (use `fetch` or your data-fetching solution)
- Simple component state (use `useState`, `ref`, or signals)
- State management (use a dedicated state management solution)
- Single async operation with no stream composition (use `async`/`await`)

**Key patterns covered:**

- Observable creation (`of`, `from`, `fromEvent`, `interval`, `timer`, `defer`)
- Pipeable operators (transformation, filtering, combination)
- Higher-order mapping (`switchMap`, `mergeMap`, `concatMap`, `exhaustMap`)
- Subjects (`Subject`, `BehaviorSubject`, `ReplaySubject`, `AsyncSubject`)
- Error handling (`catchError`, `retry` with config, `retryWhen` deprecated)
- Memory leak prevention (`takeUntil` pattern, subscription management)
- Combination operators (`combineLatest`, `forkJoin`, `merge`, `concat`)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Observable creation, subscription, basic operators, error handling
- [examples/higher-order.md](examples/higher-order.md) - switchMap, mergeMap, concatMap, exhaustMap patterns
- [examples/subjects.md](examples/subjects.md) - Subject types, multicasting, state sharing
- [examples/combination.md](examples/combination.md) - combineLatest, forkJoin, merge, concat, race
- [examples/memory-leaks.md](examples/memory-leaks.md) - takeUntil pattern, subscription cleanup strategies
- [reference.md](reference.md) - Operator decision tree, flattening operator cheat sheet, gotchas

---

<philosophy>

## Philosophy

RxJS implements the **Observable pattern** for composing asynchronous and event-based programs using observable sequences. The core idea: treat everything as a stream -- clicks, HTTP responses, timers, WebSocket messages -- and compose them declaratively with operators.

**Key principle:** Observables are lazy. Nothing happens until you `subscribe()`. Operators in a `pipe()` build a processing pipeline that transforms values as they flow through.

```typescript
import { fromEvent, map, filter, debounceTime } from "rxjs";

const DEBOUNCE_MS = 300;
const MIN_QUERY_LENGTH = 3;

// Declarative stream: input events -> debounced search queries
const search$ = fromEvent<InputEvent>(searchInput, "input").pipe(
  map((event) => (event.target as HTMLInputElement).value),
  debounceTime(DEBOUNCE_MS),
  filter((query) => query.length >= MIN_QUERY_LENGTH),
);
```

### Naming Convention

Suffix observable variables with `$` to distinguish them from plain values:

```typescript
const users$ = userService.getUsers(); // Observable
const users = []; // plain array
```

### Current Version

RxJS **7.8.x** is the current stable release. v7 introduced smaller bundle sizes (~50% smaller via tree-shaking), pipeable-only operators, and improved TypeScript types. v8 is in development.

### When to Use RxJS

- Event streams that need composition (debounce + filter + switchMap)
- Multiple concurrent async operations needing coordination
- Real-time data that arrives over time (WebSockets, SSE, polling)
- Complex cancellation logic (cancel previous request on new input)

### When NOT to Use RxJS

- Simple fetch calls -- `async`/`await` or your data-fetching solution is simpler
- One-off async operations without stream semantics
- State management -- use a dedicated state solution
- When the team lacks RxJS experience and the problem is simple

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Observable Creation

Use the right creation function for the data source.

```typescript
import {
  of,
  from,
  fromEvent,
  interval,
  timer,
  defer,
  EMPTY,
  NEVER,
  throwError,
} from "rxjs";

// ✅ Good Example - Matching creation function to data source

// Static values
const static$ = of(1, 2, 3); // emits 1, 2, 3, then completes

// From iterable/Promise/array
const fromArray$ = from([1, 2, 3]); // emits 1, 2, 3, then completes
const fromPromise$ = from(fetch("/api/users")); // emits response, completes

// DOM events (infinite stream -- must unsubscribe)
const clicks$ = fromEvent(document, "click");

// Timed emissions
const POLL_INTERVAL_MS = 1000;
const interval$ = interval(POLL_INTERVAL_MS); // emits 0, 1, 2... every second

const INITIAL_DELAY_MS = 2000;
const timer$ = timer(INITIAL_DELAY_MS); // emits 0 after 2s, then completes

// Deferred creation -- new Observable per subscriber
const deferred$ = defer(() => from(fetch("/api/data")));

// Sentinel observables
const empty$ = EMPTY; // completes immediately, emits nothing
const error$ = throwError(() => new Error("Something failed"));
```

**Why good:** each creation function matches the data source semantics, `defer` ensures fresh execution per subscriber, named constants for durations

```typescript
// ❌ Bad Example - Wrapping a promise without defer
const bad$ = from(fetch("/api/users")); // fetch fires immediately, shared across subscribers!
```

**Why bad:** without `defer`, the fetch executes once when the Observable is created, not when subscribed -- all subscribers share the same stale response

---

### Pattern 2: Pipeable Operators

All operators are used inside `.pipe()`. Import from `"rxjs/operators"` or `"rxjs"` (v7.2+).

```typescript
import { map, filter, tap, take, skip, distinctUntilChanged } from "rxjs";

const MIN_AGE = 18;

// ✅ Good Example - Operator pipeline
const adults$ = users$.pipe(
  filter((user) => user.age >= MIN_AGE),
  map((user) => user.name),
  distinctUntilChanged(), // skip consecutive duplicates
  tap((name) => console.log("Processing:", name)), // side effects (logging)
);
```

**Why good:** clear transformation pipeline, each operator has a single purpose, `tap` for side effects keeps the pipeline pure otherwise

```typescript
// ❌ Bad Example - Nesting subscribes instead of using operators
users$.subscribe((user) => {
  if (user.age >= MIN_AGE) {
    names$.subscribe((name) => {
      console.log(name); // nested subscription = memory leak risk
    });
  }
});
```

**Why bad:** nested subscriptions are impossible to clean up properly, create exponential subscription count, lose back-pressure control

---

### Pattern 3: Error Handling with catchError

Errors terminate the Observable chain. Use `catchError` to recover or provide fallback values.

```typescript
import { catchError, retry, of, from, timer, switchMap } from "rxjs";

const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 1000;

// ✅ Good Example - Error recovery with fallback
const data$ = source$.pipe(
  switchMap(() =>
    from(fetch("/api/data")).pipe(
      retry(MAX_RETRIES), // retry up to 3 times on failure
      catchError((error) => {
        console.error("Fetch failed:", error);
        return of([]); // fallback: emit empty array, stream continues
      }),
    ),
  ),
);

// ✅ Good Example - Delayed retry with backoff
const resilient$ = source$.pipe(
  switchMap(() =>
    from(fetch("/api/data")).pipe(
      retry({
        count: MAX_RETRIES,
        delay: (error, retryCount) => timer(RETRY_DELAY_MS * retryCount),
      }),
      catchError(() => of({ data: null, error: true })),
    ),
  ),
);
```

**Why good:** `catchError` returns a fallback Observable keeping the outer stream alive, `retry` with delay config prevents hammering the server, error is scoped to inner Observable

```typescript
// ❌ Bad Example - catchError in wrong position
const bad$ = source$.pipe(
  catchError(() => of([])), // catches errors from source$, NOT from switchMap
  switchMap(() => from(fetch("/api/data"))), // errors here kill the stream!
);
```

**Why bad:** `catchError` must be inside the inner Observable pipe to catch inner errors; placing it before `switchMap` only catches source errors

---

### Pattern 4: Rate Limiting (debounceTime, throttleTime)

Control emission frequency for performance.

```typescript
import {
  debounceTime,
  throttleTime,
  distinctUntilChanged,
  auditTime,
} from "rxjs";

const DEBOUNCE_MS = 300;
const THROTTLE_MS = 200;

// ✅ Good Example - Search input with debounce
const searchQuery$ = fromEvent<InputEvent>(searchInput, "input").pipe(
  map((e) => (e.target as HTMLInputElement).value.trim()),
  debounceTime(DEBOUNCE_MS), // wait 300ms of silence before emitting
  distinctUntilChanged(), // skip if value unchanged
);

// ✅ Good Example - Scroll position with throttle
const scrollPosition$ = fromEvent(window, "scroll").pipe(
  throttleTime(THROTTLE_MS), // emit at most every 200ms
  map(() => window.scrollY),
);
```

**Why good:** `debounceTime` waits for pause in emissions (ideal for user input), `throttleTime` limits rate (ideal for continuous events like scroll/resize), `distinctUntilChanged` prevents redundant processing

---

### Pattern 5: Higher-Order Mapping Operators

The most critical decision in RxJS: choosing the right flattening operator.

```
New outer value arrives while inner Observable is still running:
├── Cancel previous inner, switch to new? → switchMap
├── Run new inner in parallel with previous? → mergeMap
├── Queue new inner, wait for previous to finish? → concatMap
└── Ignore new outer value until current inner finishes? → exhaustMap
```

```typescript
import { switchMap, mergeMap, concatMap, exhaustMap } from "rxjs";

// ✅ switchMap - Type-ahead search (cancel previous request)
const searchResults$ = searchQuery$.pipe(
  switchMap((query) => from(fetch(`/api/search?q=${query}`))),
);

// ✅ mergeMap - Bulk file upload (process all in parallel)
const uploads$ = files$.pipe(
  mergeMap((file) => uploadFile(file), 3), // concurrent limit of 3
);

// ✅ concatMap - Sequential form submissions (preserve order)
const saves$ = saveActions$.pipe(
  concatMap((data) =>
    from(fetch("/api/save", { method: "POST", body: JSON.stringify(data) })),
  ),
);

// ✅ exhaustMap - Login button (ignore clicks while request pending)
const login$ = loginClick$.pipe(
  exhaustMap(() => from(authService.login(credentials))),
);
```

**Why good:** each operator matches the exact concurrency semantics needed, `mergeMap` with concurrent limit prevents resource exhaustion

See [examples/higher-order.md](examples/higher-order.md) for detailed patterns.

---

### Pattern 6: Subjects

Subjects are both Observable and Observer -- they can multicast values to multiple subscribers.

```typescript
import { Subject, BehaviorSubject, ReplaySubject, AsyncSubject } from "rxjs";

// ✅ Subject - No initial value, no replay
const event$ = new Subject<string>();
event$.subscribe((v) => console.log("A:", v));
event$.next("hello"); // A: hello
event$.subscribe((v) => console.log("B:", v));
event$.next("world"); // A: world, B: world (B missed "hello")

// ✅ BehaviorSubject - Has current value, replays latest to new subscribers
const currentUser$ = new BehaviorSubject<User | null>(null);
currentUser$.subscribe((u) => console.log("User:", u)); // immediately: User: null
currentUser$.next({ name: "Alice" }); // User: { name: "Alice" }
currentUser$.getValue(); // synchronous access: { name: "Alice" }

// ✅ ReplaySubject - Replays N previous values to new subscribers
const REPLAY_BUFFER_SIZE = 3;
const messages$ = new ReplaySubject<string>(REPLAY_BUFFER_SIZE);
messages$.next("msg1");
messages$.next("msg2");
messages$.next("msg3");
messages$.subscribe((m) => console.log(m)); // replays: msg1, msg2, msg3

// ✅ AsyncSubject - Emits only the LAST value, only on complete()
const result$ = new AsyncSubject<number>();
result$.next(1);
result$.next(2);
result$.next(3);
result$.complete(); // subscribers receive: 3 (only last value, only after complete)
```

**Why good:** each Subject type matches a specific multicast pattern, `BehaviorSubject` for current state, `ReplaySubject` for message history, `AsyncSubject` for final results

See [examples/subjects.md](examples/subjects.md) for detailed patterns.

---

### Pattern 7: Memory Leak Prevention

The `takeUntil` pattern is the standard approach for cleanup.

```typescript
import { Subject, takeUntil } from "rxjs";

// ✅ Good Example - takeUntil with destroy Subject
class DataService {
  private readonly destroy$ = new Subject<void>();

  initialize(): void {
    this.longLivedStream$
      .pipe(
        switchMap((id) => this.fetchData(id)),
        takeUntil(this.destroy$), // MUST be LAST in the pipe
      )
      .subscribe((data) => this.handleData(data));
  }

  cleanup(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

**Why good:** `takeUntil` as last operator ensures all inner subscriptions are cleaned up, single destroy Subject handles all subscriptions

```typescript
// ❌ Bad Example - takeUntil before switchMap
this.source$
  .pipe(
    takeUntil(this.destroy$), // BAD: inner Observable from switchMap survives!
    switchMap((id) => this.longRunningRequest(id)),
  )
  .subscribe();
```

**Why bad:** `takeUntil` before `switchMap` unsubscribes from the outer source but the inner Observable created by `switchMap` continues running -- a silent memory leak

See [examples/memory-leaks.md](examples/memory-leaks.md) for all cleanup strategies.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Nested `.subscribe()` calls inside `.subscribe()` -- use flattening operators (`switchMap`, `mergeMap`, etc.) instead
- Missing `takeUntil` or `unsubscribe()` on long-lived Observables -- causes memory leaks
- `takeUntil` placed before higher-order operators in the pipe -- inner subscriptions survive cleanup
- Unhandled errors in Observable chains -- one error kills the entire stream permanently
- Using `mergeMap` when `switchMap` is appropriate -- causes race conditions and stale data

**Medium Priority:**

- Using `.subscribe()` just to get a value and assign it -- consider `async` pipe, `firstValueFrom()`, or `lastValueFrom()` for one-shot usage
- Not using `shareReplay` when multiple subscribers need the same HTTP response -- causes duplicate requests
- Forgetting `distinctUntilChanged()` after `debounceTime` -- processes unchanged values
- Using `new Observable()` when a creation function exists -- `fromEvent`, `from`, `timer` are cleaner

**Gotchas & Edge Cases:**

- `from(promise)` executes the promise immediately at creation time, not at subscription time -- use `defer(() => from(promise))` for lazy execution
- `BehaviorSubject.getValue()` returns the current value synchronously but doesn't trigger subscriptions -- use `.pipe()` for reactive updates
- `catchError` must return an Observable -- returning a plain value is a type error
- `forkJoin` only emits when ALL source Observables complete -- one incomplete source blocks everything
- `combineLatest` requires all sources to emit at least once before producing any output
- `interval(0)` does NOT emit synchronously -- it uses `setInterval` and is always async
- HTTP Observables (single-emission, auto-complete) generally don't need unsubscription, but `fromEvent`, `interval`, and Subject-based streams always do
- `retry` re-subscribes to the source Observable from scratch -- ensure the source is idempotent
- `shareReplay({ bufferSize: 1, refCount: true })` -- without `refCount: true`, the source is never unsubscribed even when all subscribers leave

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST unsubscribe from every long-lived Observable -- use `takeUntil`, `take`, `first`, or explicit `unsubscribe()` to prevent memory leaks)**

**(You MUST choose the correct flattening operator -- `switchMap` for cancellation, `mergeMap` for parallel, `concatMap` for sequential, `exhaustMap` to ignore while busy)**

**(You MUST place `takeUntil` LAST in the pipe chain -- placing it before higher-order operators like `switchMap` leaves inner subscriptions alive)**

**(You MUST handle errors with `catchError` inside the pipe -- an unhandled error terminates the entire Observable chain permanently)**

**Failure to follow these rules will cause memory leaks, stale data, and silently broken Observable chains.**

</critical_reminders>
