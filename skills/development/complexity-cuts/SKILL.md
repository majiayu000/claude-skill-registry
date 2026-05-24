---
name: complexity-cuts
description: Use when refactoring existing code that has poor Big-O — nested loops, O(n^2)+ scans, repeated work, redundant allocations, blown memory, or stated symptoms like "this is slow on large inputs", "times out", "OOM", "too much memory", "reduce complexity", "optimize this algorithm". Targets time and space complexity of code that already exists. For preventing bad complexity before code is written, use lemmaly. For math-level optimizations (Bloom, HLL, FFT, JL projection), escalate to mathguard.
metadata:
  priority: 2
  role: corrective
  pathPatterns:
    - '**/*.{js,jsx,ts,tsx,mjs,cjs}'
    - '**/*.py'
    - '**/*.sql'
    - '**/*.java'
    - '**/*.cs'
    - '**/*.go'
    - '**/*.rs'
    - '**/*.{cpp,cc,cxx,hpp,hh,hxx}'
    - '**/*.php'
    - '**/*.rb'
  bashPatterns:
    - 'slow'
    - 'timeout'
    - 'oom'
    - 'optimize'
  chainTo:
    - skill: lemmaly
      when: 'about to write new code instead of fixing existing'
    - skill: invariant-guard
      when: '3+ transformations have failed tests — likely a missing contract, not a missing optimization'
    - skill: mathguard
      when: 'classical floor reached and approximate/probabilistic structure could help'
  retrieval:
    aliases:
      - optimize-bigo
      - fix-n-squared
      - lower-complexity
    intents:
      - optimize slow code
      - reduce big-o
      - fix n+1 query
      - lower memory usage
---

# complexity-cuts — Lower Big-O on Existing Code

lemmaly prevents bad complexity before code is written. complexity-cuts fixes it after the fact: code already exists, it works, but its time or space complexity is worse than necessary.

**Violating the letter of these rules is violating the spirit of the skill.** Adapting "just a little" is how a faster-but-wrong rewrite ships.

## The Iron Law

```text
NO TRANSFORMATION WITHOUT EXISTING TESTS GREEN BEFORE AND AFTER
```

If the code has no tests, you write a characterization test first (golden input → current output). Then transform. Then verify the test still passes. If you skip this, the optimization can silently break callers — and faster-but-wrong is worse than slow-and-right.

## Non-negotiable rules

1. **State current and target Big-O before touching code.** In one line:
   - Current: `time = O(?)`, `space = O(?)`
   - Target: `time = O(?)`, `space = O(?)`
   - Dominant input dimension (n = what, how large in practice)

   If you cannot state current Big-O, you do not yet understand the code. Read more.

2. **Identify the bottleneck, do not guess.** Point to the exact line(s) responsible for the dominant term. Nested loop? Repeated linear scan? Recomputation? Allocation inside a hot loop? The fix lives there, not elsewhere.

3. **One transformation at a time, with a verify-revert-stop loop.** The loop is:

   1. Apply exactly one transformation from the playbook.
   2. Run the existing test suite (or the characterization test you wrote per the Iron Law).
   3. If any test breaks: **revert immediately.** Do not patch the test. Do not patch around the failure. Revert.
   4. Count reverts on this piece of code. If **3 reverts in a row**, STOP optimizing. The bottleneck is wrong, the transformation is wrong, or the code has invariants you have not modeled. Escalate to `invariant-guard` and write the missing contract — do not try a fourth transformation.
   5. Only after a transformation lands green: pick the next one.

   Stacked changes hide regressions. Patched tests hide regressions louder.

4. **Preserve semantics exactly.** Lower complexity must not change outputs, ordering guarantees, stability, or error behavior. If the optimization requires a semantic change (e.g. unordered output), call it out explicitly and confirm it is acceptable.

5. **No invented numbers.** Never write "10x faster" or "saves 200MB" without measuring. Write `<measured: TBD>` and move on, or actually measure with a representative input.

## The transformation playbook

The vast majority of real-world Big-O wins come from a small set of moves. Try them in this order:

### Time-complexity reductions

| Smell | Fix | Typical win |
|---|---|---|
| `for x in A: if x in B` where B is list/array | Convert B to `Set`/`Map` once | O(n·m) → O(n+m) |
| Nested loop computing pairs/joins | Hash-join on the key; index by lookup field | O(n·m) → O(n+m) |
| Repeated `.find` / `.indexOf` / `.includes` inside a loop | Precompute index `Map<key, item>` outside loop | O(n^2) → O(n) |
| Repeated recomputation of same value | Memoize / cache by input key | O(n·f(n)) → O(n + f(n)) |
| Sort inside a loop | Sort once outside | O(n^2 log n) → O(n log n) |
| Linear scan for min/max/median repeatedly | Heap / sorted structure | O(n·k) → O(n log k) |
| Recursive recomputation (naive Fibonacci shape) | Memoize, or convert to iterative DP | exponential → O(n) |
| String concatenation in a loop (some langs) | Use builder / `join` / `array.push` then join | O(n^2) → O(n) |
| Repeated regex compile in loop | Compile once outside | constant-factor, large |
| Counting / grouping via nested loop | Single pass with `Counter` / `Map<k, count>` | O(n^2) → O(n) |
| Sliding-window written as nested loop | Two-pointer / windowed sum | O(n^2) → O(n) |
| Repeated prefix sums | Precompute prefix array, O(1) range queries | O(n·q) → O(n+q) |
| Pairwise distance / containment checks on intervals | Sort + sweep line | O(n^2) → O(n log n) |
| Top-K via full sort | Heap of size K | O(n log n) → O(n log k) |
| Repeated set membership in loop body | `Set` once, reuse | O(n·m) → O(n) |
| `await` inside a `for` over independent items | `Promise.all` / batched concurrency | wall-clock O(n·latency) → O(latency) |
| ORM query inside a loop (N+1) | `IN (...)` / `select_related` / bulk fetch | O(n) round-trips → O(1) |

### Space-complexity reductions

| Smell | Fix | Typical win |
|---|---|---|
| Materializing whole list/array just to iterate | Generator / iterator / stream | O(n) → O(1) |
| Building intermediate arrays via chained `.map().filter().map()` on huge data | Single-pass loop or lazy pipeline | k·O(n) → O(n) (often O(1) extra) |
| Caching every intermediate result of a recursion | Rolling window (keep last k states) | O(n) → O(k) |
| Storing parents/visited for graph traversal when only count needed | Bitset / counter only | O(n) → O(1) |
| Copying input to mutate | In-place mutation when caller allows | O(n) → O(1) |
| Reading entire file before processing | Stream line-by-line / chunked | O(file) → O(chunk) |
| Deep-clone for safety in a loop | Clone once, or use structural sharing / immutables | O(n·m) → O(n+m) |
| Holding references that prevent GC (closures, listeners, caches) | Bound the cache (LRU), remove listeners, scope closures tightly | unbounded → bounded |
| Loading full result set from DB | Cursor / pagination / streaming query | O(rows) → O(page) |
| `JSON.parse(JSON.stringify(x))` for cloning | `structuredClone` or targeted copy | O(n) work and allocation removed |

### When you cannot lower asymptotic Big-O

Sometimes O(n log n) really is the floor. Then move to constant-factor wins:
- Replace pointer-chasing structures with contiguous arrays (cache locality).
- Hoist invariants out of loops.
- Avoid allocation in the hot loop (reuse buffers).
- Prefer typed arrays / native containers over boxed objects for numeric work.
- Batch syscalls / I/O.

State explicitly: "Asymptotic floor is O(n log n); applying constant-factor optimizations only."

## Required workflow

For each piece of code you optimize:

1. **Measure or estimate current Big-O.** Write it down.
2. **Identify the bottleneck line(s).** Point at them.
3. **Pick one transformation from the playbook.** Name it.
4. **Apply it.** One change.
5. **Verify behavior.** Tests pass, or outputs match on a representative input.
6. **State new Big-O.** Time and space.
7. **Repeat if more wins exist and are worth the complexity cost.**

## Canonical example — workflow vs no-workflow

The same optimization with and without the verify-revert-stop loop.

**Bottleneck.** `getOrdersWithUsers()` runs 10s on 10k orders. Cause: `users.find(u => u.id === o.userId)` inside the map → O(n·m).

<Bad>

```ts
// No workflow: change semantics + the optimization in one go
export function getOrdersWithUsers(orders, users) {
  const userById = Object.fromEntries(users.map(u => [u.id, u]));
  return orders
    .map(o => ({ ...o, user: userById[o.userId] }))
    .filter(o => o.user); // silently drops orders whose user was deleted
}
```

Faster, *and* changes the result set. Existing tests catch it — but the diff also "fixes" a flaky test by removing the assertion that checked the old behavior. Ships green. Breaks the billing report two weeks later.

</Bad>

<Good>

```ts
// Workflow applied:
//   Bottleneck: orders.map → users.find  (line 14)
//   Current: time = O(n·m), space = O(1)
//   Target:  time = O(n+m), space = O(m)
//   Transformation: precompute index Map<userId, User> outside the loop
//   Semantic risk: None — orders with missing users still emit `user: undefined` exactly as before
//   Reverts so far: 0

export function getOrdersWithUsers(orders, users) {
  const userById = new Map(users.map(u => [u.id, u]));
  return orders.map(o => ({ ...o, user: userById.get(o.userId) }));
}
```

One transformation. Existing tests stay untouched. Run them. If green, ship. If red, revert (don't patch). After 3 reverts, stop and load `invariant-guard` — the bottleneck is wrong, or the function has a contract no one wrote down.

</Good>

## Output discipline

When proposing or applying an optimization, your message must contain — in this order:

1. **Bottleneck** — file:line and one-sentence reason.
2. **Current complexity** — `time = O(?)`, `space = O(?)`.
3. **Transformation** — name from the playbook (or describe it if novel).
4. **New complexity** — `time = O(?)`, `space = O(?)`.
5. **Semantic risk** — anything callers might notice (ordering, stability, error timing). "None" is a valid answer if true.
6. **The diff.**

If any of 1–5 is missing, the optimization is not ready to apply.

## Stop conditions — do not optimize further when

- Asymptotic Big-O already matches a known lower bound for the problem.
- The input is provably small and bounded (n < ~100 and not on a hot path).
- The optimization would obscure correctness or harm readability without a measured win.
- The bottleneck is I/O or external service latency, not CPU/memory — go fix that instead.

Premature optimization past these points adds risk without payoff.

## Rationalizations to watch for

These are real verbatim thoughts captured from a controlled test where the model produced a correct optimization but skipped the workflow that would document it for reviewers:

| Excuse | Reality |
| --- | --- |
| "I already solved this in my head — just paste the diff and add labels after." | Retrofitted labels lie about the reasoning order. Write bottleneck → complexity → transformation → diff in that order, or you are writing fiction. |
| "Stating the current Big-O is busywork — everyone can see the nested loop." | If everyone can see it, writing one line costs nothing. If only you can see it, you just saved the reviewer's time. |
| "Semantic risk is None, skip that step." | "None" is a valid answer — but write it. The next reader does not know which guarantees you considered. |
| "I'll do all three transformations in one diff." | Stacked transformations hide regressions. One transformation, verify, repeat. |
| "It's just a small refactor, the workflow is overkill." | Then it takes 30 seconds. The cases where you skip the workflow are the ones where you miss the optimization next to the obvious one. |
| "I'll measure later." | Later is `<measured: TBD>` forever. Either measure now or accept the asymptotic argument as the only claim. |

If any of these sound familiar mid-edit: stop, restart the seven-step output discipline.

## Red flags — STOP

- Optimizing without stating current Big-O.
- "This should be faster" without identifying a specific bottleneck line.
- Stacking multiple transformations before verifying any one of them.
- Claiming a speedup without measuring or without an asymptotic argument.
- Lowering complexity by silently changing output semantics.
- Rewriting code that runs once at startup with n = 12.

All of these mean: back up, restate the rules, start the workflow over.

## Verification checklist

Before claiming an optimization is complete:

- [ ] Existing tests (or a written characterization test) were green BEFORE the transformation.
- [ ] Exactly one transformation was applied.
- [ ] Tests are green AFTER the transformation.
- [ ] No test was modified, weakened, or skipped to make it pass.
- [ ] Current Big-O and target Big-O are stated in the diff or PR description.
- [ ] Semantic risk is written down ("None" is valid if true).
- [ ] If a measured claim was made (e.g. "3x faster"), the measurement command is included.
- [ ] Revert count on this code is < 3.

Cannot check every box? The optimization is not done. Either revert or finish the gap — do not ship a half-verified speedup.
