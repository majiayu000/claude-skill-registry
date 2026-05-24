# Hot paths reference

A "hot path" is code that runs many times per second, per request, or per render. Small constants matter here; nowhere else.

## How to identify one

A path is hot if any of:
- Runs inside React `render` / function-component body / `useEffect` with frequent deps.
- Runs per item in a list of `n > 100`.
- Runs per request on a server (especially middleware, auth checks).
- Runs per frame (animation, scroll, drag, resize handlers).
- Runs per keystroke (search, validation).
- Runs in a polling/interval loop.

If you can't say which of these applies, you don't know if it's hot. Ask the user.

## React: the common re-render causes

1. **New referential identity every render.**
   ```jsx
   // Bad — new array every render, breaks memo
   <Child items={[a, b, c]} options={{ sort: true }} />

   // Bad — new function every render
   <Child onClick={() => doThing(id)} />

   // Good
   const items = useMemo(() => [a, b, c], [a, b, c]);
   const onClick = useCallback(() => doThing(id), [id]);
   ```
   But only if `Child` is `React.memo` and the cost of re-rendering it actually matters. Don't blanket-memo.

2. **Context that changes too often.** Any consumer of a Context re-renders when its value reference changes. Split contexts; memoize the value object.

3. **Anonymous components in render.**
   ```jsx
   // Bad — new component type every render, full subtree remounts
   function Parent() {
     function Item({ x }) { return <li>{x}</li>; }
     return items.map(x => <Item x={x} />);
   }
   ```
   Hoist `Item` outside.

4. **Inline object/array props to a memoized child.** Same problem as (1). Hoist or `useMemo`.

5. **Effects with object/array deps.** `useEffect(fn, [{ a, b }])` — that object is new every render → infinite loop or constant re-run. Memoize the dep, or list scalars.

6. **`key={index}` on a reorderable list.** Forces unnecessary unmounts/remounts and breaks input state.

## Big lists

- **Virtualize at ~200+ items rendered at once.** `react-virtuoso`, `@tanstack/react-virtual`, or native CSS `content-visibility: auto`.
- **Move heavy work off the main thread.** `Web Worker` for parsing/diffing/searching large data.
- **Defer non-critical work.** `startTransition` / `useDeferredValue` for filtering. `requestIdleCallback` for analytics.

## Event-loop blocking

In JS, a single tick over ~50ms is felt as a jank. Over ~200ms, the user thinks the app is frozen.

Common offenders to never run synchronously on the main thread:
- JSON.parse / JSON.stringify on payloads > a few hundred KB.
- Sort / dedupe / aggregation over > ~50k items.
- Regex with catastrophic backtracking on untrusted input (ReDoS).
- Image / video / PDF processing.
- Sync crypto.

Fix: chunk with `setTimeout(_, 0)` / `MessageChannel`, move to a Worker, or stream.

## Render budgets (rules of thumb)

| Surface | Budget |
|---------|--------|
| First paint (LCP) | < 2.5s |
| Interaction (INP) | < 200ms |
| Per-frame work | < 16ms (60fps) or < 8ms (120fps) |
| Server response (TTFB) | < 200ms warm |

State a budget when shipping new UI work. Then measure.

## Server hot paths

- Auth/identity middleware runs on every request — must be O(1) or cached.
- N+1 queries in list endpoints — see `n-plus-one.md`.
- JSON serialization on huge payloads — paginate or stream.
- Synchronous bcrypt/argon2 in a request handler — fine if rare, costly under load. Tune cost factor.
- Cold start: minimize module-load work, lazy-import heavy deps.
