# Complexity reference

## The only chart that matters for shipping

| n        | O(1)  | O(log n) | O(n)   | O(n log n) | O(n^2)     | O(2^n)     |
|----------|-------|----------|--------|------------|------------|------------|
| 10       | inst. | inst.    | inst.  | inst.      | inst.      | ms         |
| 1,000    | inst. | inst.    | inst.  | inst.      | ms         | impossible |
| 10,000   | inst. | inst.    | ms     | ms         | seconds    | —          |
| 100,000  | inst. | inst.    | tens ms| ~100 ms    | minutes    | —          |
| 1,000,000| inst. | inst.    | ~100 ms| ~seconds   | hours      | —          |

Read as: "if my hot path runs at this `n`, what's my budget?"

Rule of thumb in JS/Python: a `for`-loop body of moderate work does ~10^7 ops/sec. Cross-check before shipping.

## Picking a data structure

| Need                          | Pick                | Why                                      |
|-------------------------------|---------------------|------------------------------------------|
| "Have I seen this value?"     | `Set` / `dict` / `frozenset` | O(1) `has` vs O(n) `includes`/`in list` |
| "Lookup by key"               | `Map` / `dict`      | O(1) — `Object` works but slower for non-string keys |
| "Ordered, frequent insertion at head" | `Deque` / linked list | Array `unshift` is O(n) |
| "Distinct sorted set"         | sorted array + bisect, or `SortedSet` | O(log n) ops |
| "Stack/queue"                 | array `push`/`pop`, or deque | `shift` on array is O(n) |
| "Range query"                 | sorted array + binary search, or interval tree | Avoid linear scan |
| "Top-k of stream"             | heap (priority queue), size k | O(n log k) vs O(n log n) for full sort |
| "Approximate membership at scale" | Bloom filter | When set itself doesn't fit memory |

## Algorithm shortcuts

- **Sort once, query many** — pre-sort if you'll do many lookups/range scans.
- **Two pointers / sliding window** — most "find pair/subarray that satisfies X" problems collapse from O(n^2) to O(n).
- **Hash and intersect** — to find common elements between two arrays, put one in a `Set` first. O(n+m) vs O(n*m).
- **Memoize pure recursion** — DP via memo turns 2^n into n^2 or n.
- **Batch I/O** — `IN (...)` query, `Promise.all([...])`, bulk insert/update. Never one-at-a-time inside a loop.
- **Lazy / streaming** — when n is huge but each consumer only reads a slice (generators, async iterators, cursor-based pagination).

## Amortized vs worst-case

Watch for cases the model usually misses:

- `array.push` — amortized O(1), worst-case O(n) on resize. Fine for batches.
- Hash table resize — amortized O(1), occasional O(n) pause. Matters in real-time.
- `string += s` in Python / JS — repeated copy → O(n^2). Use `''.join(list)` / `arr.join('')`.
- Recursive memoization — first call O(n), subsequent O(1). Cold-start cost.

State amortized AND worst-case when it matters to the caller (e.g. interactive UI, request handler).

## Space matters too

Always state space, not just time. Cases that bite:
- Materializing a full list when you could stream.
- Deep-cloning a large object to "be safe" — pay O(n) memory + O(n) time on every call.
- Caching everything forever — unbounded cache is a memory leak.
- Closures retaining large parents — see `memory.md`.

## "What's n?" — always ask

Never optimize without knowing `n` and growth rate. Ask the user, or read the schema/data shape:

- Per-request `n`? Per-tenant `n`? Per-user lifetime `n`?
- Is it bounded (`<= 100` always), or does it grow linearly with users / time / data ingest?
- Does it appear in a hot path (every request) or a cold path (admin script, once a day)?

A nested loop at n=20 is fine forever. The same code at n=50,000 is an outage.
