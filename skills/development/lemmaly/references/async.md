# Async reference

## Sequential vs parallel

```js
// Bad — sequential, total = sum of latencies
const user = await fetchUser(id);
const posts = await fetchPosts(id);
const friends = await fetchFriends(id);

// Good — parallel, total = max of latencies
const [user, posts, friends] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
  fetchFriends(id),
]);
```

Apply this every time the awaits don't depend on each other. The model often writes the sequential form by reflex.

## When parallel is wrong

- Each call mutates shared state (race).
- Each call needs the previous result.
- Each call counts against a strict rate limit and you'd burst over it.
- Each call holds an exclusive lock or DB transaction.

In those cases, write the sequential form and leave a one-line comment.

## Concurrency limit ("don't fan out to infinity")

`Promise.all(thousand_things.map(fetch))` will hit the server with 1000 simultaneous connections. Cap it:

```js
// p-limit (npm)
import pLimit from 'p-limit';
const limit = pLimit(10);   // ten in flight
const results = await Promise.all(items.map(i => limit(() => fetchOne(i))));
```

Pick the concurrency to fit the downstream's capacity, not the network's.

## `forEach` is async-hostile

```js
// Bad — forEach ignores the returned promises; "load()" returns before any await resolves
items.forEach(async i => {
  await save(i);
});
console.log('done');     // lies

// Good
for (const i of items) await save(i);                              // sequential
await Promise.all(items.map(i => save(i)));                        // parallel
```

If you see `async` inside `.forEach(`, it's almost always wrong.

## Cancellation: `AbortController`

User clicks away, tab hidden, debounced search supersedes the prior request — all should cancel:

```js
const ctrl = new AbortController();
const res = await fetch(url, { signal: ctrl.signal });
// later
ctrl.abort();
```

In React: cancel in the cleanup of `useEffect`. In a search box: cancel the prior controller before issuing the next request.

## Debounce vs throttle vs request coalescing

| Pattern | What it does | When |
|---------|--------------|------|
| Debounce | Run after user pauses for X ms | Search-as-you-type, autosave |
| Throttle | Run at most once per X ms | Scroll/resize handlers, drag |
| Coalesce | Multiple identical concurrent requests → one in-flight request, all callers wait | Same-key fetches inside a tick |

Coalesce example:

```js
const inflight = new Map();
function getCached(key) {
  if (inflight.has(key)) return inflight.get(key);
  const p = fetchOne(key).finally(() => inflight.delete(key));
  inflight.set(key, p);
  return p;
}
```

## Streaming over buffering

If you'll process items one-by-one anyway, don't materialize the whole list first:

```js
// Bad
const all = await fetchAll();
for (const item of all) await process(item);

// Good — async iterator / cursor
for await (const item of fetchPaged()) await process(item);
```

Saves memory and lets you start processing before the source has finished producing.

## Retries: do them right or not at all

A naive `for (let i = 0; i < 3; i++) try { ... }` retry storm during an outage is how minor incidents become major ones.

- Only retry on transient errors (timeouts, 502/503, network reset). Not 4xx.
- Exponential backoff with jitter: `delay = base * 2^attempt + random()`.
- Cap total retry time, not just attempt count.
- Apply at the edge, not at every layer (or you get retry^layers).

## Timeouts

Every external call has a timeout. Default Node `fetch` has none. Always:

```js
const ctrl = new AbortController();
const t = setTimeout(() => ctrl.abort(), 5000);
try {
  return await fetch(url, { signal: ctrl.signal });
} finally {
  clearTimeout(t);
}
```

## Promise.all vs Promise.allSettled

- `Promise.all` rejects on the first failure — good when partial result is useless.
- `Promise.allSettled` always resolves with per-item status — good when partial is fine and you want to report failures.

Choose deliberately. The default reflex (`all`) is often wrong for "fetch user's widgets from N services where one being down is tolerable".
