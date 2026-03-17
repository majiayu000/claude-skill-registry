---
name: watermelondb
description: WatermelonDB models, observation patterns, and React integration. Use when writing or debugging model code, observers (findAndObserve, query.observe), or screens that display live-updating DB data.
---

# WatermelonDB Model & Observation

## Overview

This skill covers WatermelonDB models (`database/models/`), observation
(reactive queries), and **ensuring React re-renders when observed data
changes**. Use it when working with `findAndObserve`, `query.observe()`,
`withObservables`, or any screen that subscribes to DB changes.

---

## Observation & React Re-rendering

### `findAndObserve` and same-reference emission

- **`findAndObserve(id)`** (on a collection): Fetches a record by ID, returns an
  Observable that emits **immediately** on subscribe and **whenever the record
  is updated or deleted**.
- When a model is updated (e.g. via `model.update()` or `@writer` methods), the
  observable **emits the same object reference** with updated properties — it
  does **not** emit a new model instance.

### React `useState` bailout

- `useState` uses `Object.is` to decide whether to re-render. Passing the **same
  reference** (e.g. `setPhrase(model)`) after an update means **no re-render**.
- Result: DB updates (text, note, language, etc.) **don’t appear** until the
  user navigates away and back, when a new subscription yields a fresh
  reference.

### Fix: store a wrapper so each emit is a new reference

When subscribing to a **single model** (e.g. `findAndObserve`) and storing it in
React state, **don’t** store the raw model. Store a wrapper so every emission
updates state with a **new object**:

```ts
const [phraseState, setPhraseState] = useState<
  { phrase: Phrase; _key: number } | null
>(null);

useEffect(() => {
  if (!id) return;
  const sub = db.collections
    .get<Phrase>(PHRASE_TABLE)
    .findAndObserve(id)
    .subscribe((result) => {
      setPhraseState({ phrase: result, _key: result.updatedAt });
    });
  return () => sub.unsubscribe();
}, [id, db]);

const phrase = phraseState?.phrase ?? null;
```

- Use `phrase` (derived) everywhere in the component. Updates persisted to the
  DB will re-emit, update `phraseState` with a new wrapper, and trigger a
  re-render.

### Query `observe()` and arrays

- **`query.observe()`** emits **arrays** of models. When the query result set
  changes, WatermelonDB typically emits a **new array** reference, so
  `setState(results)` usually triggers re-renders.
- If you **build derived data** (e.g. `linked.filter(...)`, `assignments`) in
  the subscribe callback and `setState` that, you’re already passing new
  references — no extra wrapper needed.

---

## `withObservables` (HOC)

- **`withObservables(triggerProps, getObservables)`** injects observable values
  as props and **always** passes a **new state object** into `setState` (e.g.
  `{ values, isFetching }`), so React re-renders on each emission even when
  model references are unchanged.
- Use it when you can **observe a model (or query) passed as a prop**: e.g.
  `withObservables(['attempt'], ({ attempt }) => ({ attempt: attempt.observe(), ... }))`.
  See `AttemptCard` in `features/lesson/components/AttemptCard.tsx`.
- For **route params** (e.g. `id`) you typically **subscribe manually** in
  `useEffect` (e.g. `findAndObserve(id)`). In that case, use the **wrapper
  pattern** above instead of storing the raw model.

---

## Model patterns in this project

- **Models**: `database/models/` (e.g. `Phrase`, `Lesson`, `Attempt`,
  `Translation`, `Deck`). Use `@field`, `@writer`, and static helpers (e.g.
  `Phrase.findOrCreatePhrase`, `Lesson.addLesson`).
- **Observation**: `useDatabase()` from `@nozbe/watermelondb/react`; then
  `collection.findAndObserve(id)` or `query.observe().subscribe(...)`.
- **Schema/tables**: `database/schema.ts`; collection access via
  `db.collections.get<Model>(TABLE)`.

---

## Quick reference

| Scenario                                  | Pattern                                                                   | Re-render guarantee            |
| ----------------------------------------- | ------------------------------------------------------------------------- | ------------------------------ |
| Single model by `id` (e.g. detail screen) | `findAndObserve` + **wrapper state** `{ model, _key }`                    | Yes                            |
| Query results (list)                      | `query.observe()` + `setState(results)` or derived structures             | Yes (new array/refs)           |
| Model passed as prop                      | `withObservables(['model'], ({ model }) => ({ model: model.observe() }))` | Yes (HOC uses new state shape) |

---

## Resources

- **DeepWiki**: [Nozbe/WatermelonDB](https://github.com/Nozbe/WatermelonDB) —
  `findAndObserve`, `observe()`, `withObservables`, model updates.
- **Project**: `PhraseDetailScreen`, `LessonDetailScreen`, `SetDetailScreen`
  (findAndObserve + wrapper); `AttemptCard` (withObservables).
