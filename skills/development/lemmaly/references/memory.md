# Memory reference

Memory bugs are quiet. They don't break tests. They get noticed when a process OOMs in production at 3am.

## The big classes of leak

### 1. Unbounded cache
```js
// Bad — grows forever
const cache = new Map();
function get(key) {
  if (!cache.has(key)) cache.set(key, expensive(key));
  return cache.get(key);
}

// Good — bounded
import { LRUCache } from 'lru-cache';
const cache = new LRUCache({ max: 1000, ttl: 1000 * 60 * 5 });
```
Any `Map` / `dict` keyed by user input is a candidate leak.

### 2. Event listeners not removed
```js
// Bad — every component instance adds a listener; unmount doesn't remove it
useEffect(() => {
  window.addEventListener('resize', handler);
}, []);

// Good
useEffect(() => {
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
}, []);
```
Same for: `setInterval`, `setTimeout` (for long timers), `IntersectionObserver`, `MutationObserver`, EventEmitter `.on`, Postgres / Redis client subscriptions, WebSocket.

### 3. Closures retaining large parents
```js
// Bad — handler closes over `largeData` even though it only uses `id`
function makeHandler(largeData) {
  const id = largeData.id;
  return () => doStuff(id, largeData);   // largeData stays alive as long as handler exists
}

// Better — destructure what you need
function makeHandler({ id }) {
  return () => doStuff(id);
}
```
Watch for: handlers attached to long-lived emitters, cached partial applications, React `useCallback` deps that include big objects.

### 4. Detached DOM
```js
// Bad — node removed from DOM, but JS still references it
const cache = { lastTooltip: tooltipEl };
tooltipEl.remove();   // removed from DOM but cache still holds → not GC'd
```
Null out references when you're done.

### 5. Streams not consumed / not closed
```js
// Bad — leaks file handle if `process` throws
const stream = fs.createReadStream(path);
await process(stream);

// Good
const stream = fs.createReadStream(path);
try { await process(stream); } finally { stream.destroy(); }
```
Same for: DB cursors, HTTP responses (in Node, `res.on('data')` without consuming), child processes.

### 6. Globals and module-level state
A module-level `Map`, `Array`, or counter that's appended to from request handlers but never trimmed is a leak.

## Buffer vs stream

If the input can be unbounded (user upload, log file, ML response), **stream** it:

```js
// Bad — loads full body into memory
const body = await req.text();
const data = JSON.parse(body);

// Good — streaming JSON parser, or process line-by-line
import readline from 'readline';
const rl = readline.createInterface({ input: req });
for await (const line of rl) handle(JSON.parse(line));
```

In Python: read `chunk = f.read(64 * 1024)` in a loop, or use generators. Don't `f.read()` an arbitrary file.

## Large objects in request scope

Holding a 50 MB result set in memory per concurrent request → 50 reqs = 2.5 GB. Patterns:

- Paginate. Don't return "all".
- Project (`SELECT id, name`) — don't `SELECT *`.
- Stream the response. In Node, write chunks to `res`. In Python/Django, `StreamingHttpResponse`.

## "Deep clone to be safe" anti-pattern

```js
const copy = JSON.parse(JSON.stringify(huge));   // O(n) time + O(n) memory + breaks Dates, Maps, etc.
```
Almost always wrong. Either you need a true clone (use `structuredClone`) or you don't (just spread the keys you need).

## Observable signs in prod

- RSS / heap grows monotonically over hours and doesn't drop after low traffic → cache or listener leak.
- Pods OOM-killed during long-running migrations → buffer instead of stream.
- Latency P99 climbs slowly during a deploy's lifetime, drops at restart → GC pressure from leak.

## Tools

- Node: `node --inspect`, Chrome DevTools "Memory" → take heap snapshots over time, diff them.
- Browser: same DevTools panel, "Detached elements" view for DOM leaks.
- Python: `tracemalloc`, `objgraph` for retention paths.
- Production: track RSS over time; alert on monotonic growth.
