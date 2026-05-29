---
name: search-system
description: Stream-first search framework for TMNL. Invoke when implementing search, QueryDSL operators, progressive results, multi-source indices, or FlexSearch integration. Covers Effect.Stream patterns, fiber cancellation, and benchmark duels.
model_invoked: true
triggers:
  - "search"
  - "QueryDSL"
  - "FlexSearch"
  - "progressive search"
  - "search stream"
  - "field operator"
  - "regex search"
  - "indices builder"
  - "multi-source search"
  - "search benchmark"
  - "fiber cancellation"
  - "withMinScore"
---

# Search System for TMNL

## Overview

A Stream-first search framework with:
- **QueryDSL** — Google-style operators (field:value, regex:pattern, "phrases", -exclude)
- **Progressive emission** — Results cascade as Stream chunks
- **Fiber cancellation** — Interrupt searches mid-flight
- **Multi-source composition** — Emacs Consult-inspired indices builder
- **Dual drivers** — FlexSearch (fast) vs Linear (simple)

## Canonical Sources

### TMNL Implementations

| File | Purpose | Pattern |
|------|---------|---------|
| `src/lib/search/index.ts` | Barrel export, public API | Stream-first architecture |
| `src/lib/search/types.ts` | Core interfaces (SearchServiceImpl, SearchResult) | Stream.Stream return types |
| `src/lib/search/query/schemas.ts` | QueryDSL Schema definitions | Effect Schema for operators |
| `src/lib/search/query/parser.ts` | Query string → ParsedQuery | Regex extraction pipeline |
| `src/lib/search/query/executor.ts` | ParsedQuery → results | Hybrid: driver + post-filter |
| `src/lib/search/query/operators.ts` | Stream operators (withFieldMatch, withRegexFilter) | Stream.filter composition |
| `src/lib/search/drivers/flexsearch.ts` | FlexSearch Document driver | Ref-based state + Stream chunks |
| `src/lib/search/drivers/linear.ts` | Fallback linear search | Simple .includes() + Stream |
| `src/lib/indices/builder.ts` | Multi-source stream composition | Stream.mergeAll pattern |
| `src/lib/indices/types.ts` | SearchSource interface | Consult-inspired sources |

### Testbeds

- **SearchTestbed**: `/testbed/search` — 36K Wikipedia movies, benchmark duel
- **IndicesTestbed**: `/testbed/indices` — Multi-source narrowing demonstration

---

## Pattern 1: SearchServiceImpl Interface — STREAM-FIRST API

**When:** Defining a search driver or service implementation.

The search service interface separates queries (Stream) from mutations (Effect):

```typescript
import { Effect, Stream } from 'effect'
import type { SearchServiceImpl, SearchResult, SearchError, Indexable } from '@/lib/search'

interface SearchServiceImpl<T extends Indexable> {
  // ───────────────────────────────────────────────────────────────────────────
  // Mutations (Effect - one-shot, transactional)
  // ───────────────────────────────────────────────────────────────────────────

  /** Index a collection of items */
  index: (items: readonly T[], config: IndexConfig<T>) => Effect.Effect<void, SearchError>

  /** Add a single item */
  add: (item: T) => Effect.Effect<void, SearchError>

  /** Update an existing item */
  update: (item: T) => Effect.Effect<void, SearchError>

  /** Remove an item by ID */
  remove: (id: string | number) => Effect.Effect<void, SearchError>

  // ───────────────────────────────────────────────────────────────────────────
  // Queries (Stream - progressive, cancellable)
  // ───────────────────────────────────────────────────────────────────────────

  /** Search (auto-detect strategy) */
  search: (query: string, options?: SearchOptions) => Stream.Stream<SearchResult<T>, SearchError>

  /** Prefix search (autocomplete) */
  prefix: (query: string, options?: Omit<SearchOptions, 'strategy'>) => Stream.Stream<SearchResult<T>, SearchError>

  /** Fuzzy search (typo-tolerant) */
  fuzzy: (query: string, options?: Omit<SearchOptions, 'strategy'>) => Stream.Stream<SearchResult<T>, SearchError>

  // ───────────────────────────────────────────────────────────────────────────
  // Admin (Effect - one-shot)
  // ───────────────────────────────────────────────────────────────────────────

  /** Get index stats */
  stats: () => Effect.Effect<SearchStats, SearchError>

  /** Clear the entire index */
  clear: () => Effect.Effect<void, SearchError>
}
```

**Key Design**:
- **Queries return Stream** → progressive UI, natural cancellation
- **Mutations return Effect** → one-shot, transactional
- **Indexable base type** → requires `id` field

**TMNL Location**: `src/lib/search/types.ts:147`

---

## Pattern 2: FlexSearch Driver — REF-BASED STATE + STREAM CHUNKS

**When:** Implementing a search driver backed by FlexSearch.

Use `Effect.Ref` to manage driver state, emit results as Stream chunks:

```typescript
import { Effect, Ref, Stream, Chunk } from 'effect'
import { Document } from 'flexsearch'
import type { SearchServiceImpl, SearchResult, Indexable } from '@/lib/search'

interface FlexSearchState<T extends Indexable> {
  index: Document<T> | null
  config: IndexConfig<T> | null
  items: Map<string | number, T>
  itemCount: number
  lastUpdated: number
}

export const createFlexSearchDriver = <T extends Indexable>(): Effect.Effect<
  SearchServiceImpl<T>
> =>
  Effect.gen(function* () {
    // Internal state via Ref
    const stateRef = yield* Ref.make<FlexSearchState<T>>({
      index: null,
      config: null,
      items: new Map(),
      itemCount: 0,
      lastUpdated: 0,
    })

    // Index mutation
    const index = (items: readonly T[], config: IndexConfig<T>) =>
      Effect.gen(function* () {
        const flexIndex = new Document<T>({
          charset: 'latin:extra',
          tokenize: 'forward',
          document: {
            id: (config.idField as string) ?? 'id',
            index: config.fields.map(normalizeFieldConfig),
            store: config.store ?? true,
          },
        })

        // Add all items
        for (const item of items) {
          flexIndex.add(item)
        }

        // Store state
        yield* Ref.set(stateRef, {
          index: flexIndex,
          config,
          items: new Map(items.map((item) => [item.id, item])),
          itemCount: items.length,
          lastUpdated: Date.now(),
        })
      })

    // Search query → Stream
    const search = (query: string, options?: SearchOptions) =>
      Stream.async<SearchResult<T>, SearchError>((emit) => {
        Effect.runPromise(
          Effect.gen(function* () {
            const idx = yield* getIndex()
            const itemsMap = yield* getItems()

            // Execute search (sync FlexSearch call)
            const results = idx.search(query, {
              limit: options?.limit ?? 100,
            })

            // Map to SearchResult format
            const mapped = mapFlexSearchResults(results, itemsMap)

            // Emit in chunks
            const chunkSize = options?.chunkSize ?? 10
            for (let i = 0; i < mapped.length; i += chunkSize) {
              const chunk = mapped.slice(i, i + chunkSize)
              emit.chunk(Chunk.fromIterable(chunk))
            }

            emit.end()
          })
        )
      })

    return { index, search, /* ... other methods */ }
  })
```

**Key Pattern**: `Stream.async` + chunk emission for progressive results.

**TMNL Location**: `src/lib/search/drivers/flexsearch.ts:40`

---

## Pattern 3: QueryDSL Schemas — EFFECT SCHEMA FOR OPERATORS

**When:** Defining structured query operators with runtime validation.

Use Effect Schema to define query operator types:

```typescript
import { Schema } from 'effect'

/**
 * Valid field names for dorking operators.
 */
export const FieldName = Schema.Literal("category", "scope", "name", "desc", "keys")
export type FieldName = typeof FieldName.Type

/**
 * Field operator: `field:value` or `-field:value` (exclusion)
 */
export const FieldOperator = Schema.Struct({
  _tag: Schema.Literal("FieldOperator"),
  field: FieldName,
  value: Schema.String,
  exclude: Schema.Boolean,
})
export type FieldOperator = typeof FieldOperator.Type

/**
 * Regex operator: `regex:pattern`
 */
export const RegexOperator = Schema.Struct({
  _tag: Schema.Literal("RegexOperator"),
  pattern: Schema.String,
})
export type RegexOperator = typeof RegexOperator.Type

/**
 * Phrase operator: `"exact phrase"`
 */
export const PhraseOperator = Schema.Struct({
  _tag: Schema.Literal("PhraseOperator"),
  phrase: Schema.String,
})
export type PhraseOperator = typeof PhraseOperator.Type

/**
 * Union of all operator types.
 */
export const QueryOperator = Schema.Union(FieldOperator, RegexOperator, PhraseOperator)
export type QueryOperator = typeof QueryOperator.Type

/**
 * Fully parsed query structure.
 */
export const ParsedQuery = Schema.Struct({
  /** Free-form search text after operator extraction */
  text: Schema.String,

  /** Field operators: category:, scope:, name:, desc:, keys: */
  fieldOperators: Schema.Array(FieldOperator),

  /** Regex operators: regex:pattern */
  regexOperators: Schema.Array(RegexOperator),

  /** Quoted phrase operators: "exact phrase" */
  phraseOperators: Schema.Array(PhraseOperator),

  /** Match mode: exact, prefix, fuzzy (default: fuzzy) */
  matchMode: Schema.optional(Schema.Literal("exact", "prefix", "fuzzy")),

  /** Case sensitivity (default: insensitive) */
  caseSensitive: Schema.optional(Schema.Boolean),

  /** Result limit */
  limit: Schema.optional(Schema.Number),

  /** Sort order */
  sort: Schema.optional(Schema.Literal("score", "name")),
})
export type ParsedQuery = typeof ParsedQuery.Type
```

**Key Pattern**: TaggedStruct with discriminator `_tag` for pattern matching.

**TMNL Location**: `src/lib/search/query/schemas.ts:15`

---

## Pattern 4: Query Parser — REGEX EXTRACTION PIPELINE

**When:** Parsing raw query strings into structured ParsedQuery.

Extraction order matters to handle quoted phrases correctly:

```typescript
import { Effect } from 'effect'
import type { ParsedQuery } from './schemas'

/** Quoted phrases: "exact phrase" */
const QUOTED_PATTERN = /"([^"]+)"/g

/** Regex operator: regex:pattern */
const REGEX_PATTERN = /regex:(\S+)/g

/** Field operators: field:value or -field:value */
const FIELD_PATTERN = /(-?)(category|scope|name|desc|keys):(\S+)/g

/** Case sensitivity: case:sensitive or case:insensitive */
const CASE_PATTERN = /case:(sensitive|insensitive)/g

/** Match mode: exact:, prefix:, fuzzy: followed by optional text */
const MATCH_MODE_PATTERN = /(exact|prefix|fuzzy):(\S*)/g

/** Limit: limit:N */
const LIMIT_PATTERN = /limit:(\d+)/g

/** Sort: sort:score or sort:name */
const SORT_PATTERN = /sort:(score|name)/g

/**
 * Parse a raw query string into a structured ParsedQuery.
 *
 * Extraction order:
 * 1. Quoted phrases (preserve spaces inside quotes)
 * 2. Regex patterns
 * 3. Field operators
 * 4. Search params (case, match mode, limit, sort)
 * 5. Remaining text is free-form search
 */
export const parseQuery = (input: string): Effect.Effect<ParsedQuery> =>
  Effect.sync(() => {
    let text = input
    const fieldOps: FieldOperator[] = []
    const regexOps: RegexOperator[] = []
    const phraseOps: PhraseOperator[] = []
    let matchMode: MatchMode | undefined
    let caseSensitive: boolean | undefined
    let limit: number | undefined
    let sort: SortField | undefined

    // 1. Extract quoted phrases FIRST (preserve spaces inside quotes)
    for (const match of input.matchAll(QUOTED_PATTERN)) {
      phraseOps.push({
        _tag: "PhraseOperator",
        phrase: match[1],
      })
      text = text.replace(match[0], " ")
    }

    // 2. Extract regex operators
    for (const match of text.matchAll(REGEX_PATTERN)) {
      regexOps.push({
        _tag: "RegexOperator",
        pattern: match[1],
      })
      text = text.replace(match[0], " ")
    }

    // 3. Extract field operators (including exclusions with -)
    for (const match of text.matchAll(FIELD_PATTERN)) {
      const [full, exclude, field, value] = match
      if (isValidField(field)) {
        fieldOps.push({
          _tag: "FieldOperator",
          field,
          value,
          exclude: exclude === "-",
        })
        text = text.replace(full, " ")
      }
    }

    // 4-7. Extract params...

    // 8. Clean up remaining text
    text = text.replace(/\s+/g, " ").trim()

    return {
      text,
      fieldOperators: fieldOps,
      regexOperators: regexOps,
      phraseOperators: phraseOps,
      matchMode,
      caseSensitive,
      limit,
      sort,
    }
  })
```

**Key Pattern**: Sequential regex extraction with text replacement.

**TMNL Location**: `src/lib/search/query/parser.ts:83`

---

## Pattern 5: Query Executor — HYBRID DRIVER + POST-FILTER

**When:** Executing a ParsedQuery against a search driver.

Use driver for fuzzy/prefix/exact, post-filter for regex/exclusions:

```typescript
import { Effect, Stream, Chunk } from 'effect'
import type { SearchServiceImpl, SearchResult, ParsedQuery } from '@/lib/search'

/**
 * Execute a ParsedQuery against a search driver.
 *
 * Hybrid approach:
 * 1. Driver handles: fuzzy/prefix/exact search, field boosting
 * 2. Post-filter handles: regex, exclusions, phrases, case sensitivity
 * 3. Post-sort handles: sort:score, sort:name (collects all results)
 */
export const executeQuery = <T extends SearchableItem>(
  driver: SearchServiceImpl<T>,
  query: ParsedQuery
): Effect.Effect<readonly SearchResult<T>[], SearchError> =>
  Effect.gen(function* () {
    // Handle empty query
    if (isEmpty(query)) {
      return []
    }

    // Build SearchOptions from query params
    const options: SearchOptions = {
      limit: query.sort ? undefined : query.limit, // Don't limit if sorting (need all)
      strategy: query.matchMode ?? "fuzzy",
    }

    // Execute base search via driver
    let results: readonly SearchResult<T>[]

    if (!query.text.trim() && hasOperators(query)) {
      // Operators-only query → get all items then filter
      const stats = yield* driver.stats()
      results = yield* driver.search("", { ...options, limit: stats.itemCount + 100 }).pipe(
        Stream.runCollect,
        Effect.map(Chunk.toReadonlyArray)
      )
    } else {
      // Normal search with text
      results = yield* driver.search(query.text, options).pipe(
        Stream.runCollect,
        Effect.map(Chunk.toReadonlyArray)
      )
    }

    // Post-filter: Field operators (include)
    const includes = query.fieldOperators.filter((op) => !op.exclude)
    for (const op of includes) {
      const prop = fieldToProperty(op.field)
      const lowerValue = op.value.toLowerCase()
      results = results.filter((r) => {
        const fieldValue = (r.item as Record<string, unknown>)[prop]
        if (typeof fieldValue !== "string") return false
        return fieldValue.toLowerCase().includes(lowerValue)
      })
    }

    // Post-filter: Field operators (exclude)
    const excludes = query.fieldOperators.filter((op) => op.exclude)
    for (const op of excludes) {
      const prop = fieldToProperty(op.field)
      const lowerValue = op.value.toLowerCase()
      results = results.filter((r) => {
        const fieldValue = (r.item as Record<string, unknown>)[prop]
        if (typeof fieldValue !== "string") return true // Keep if field doesn't exist
        return !fieldValue.toLowerCase().includes(lowerValue)
      })
    }

    // Post-filter: Regex operators
    for (const op of query.regexOperators) {
      const flags = query.caseSensitive ? "" : "i"
      let regex: RegExp
      try {
        regex = new RegExp(op.pattern, flags)
      } catch {
        continue // Invalid regex - skip
      }
      results = results.filter((r) => {
        const item = r.item
        return regex.test(item.name) || regex.test(item.description ?? "")
      })
    }

    // Post-filter: Phrase operators
    for (const op of query.phraseOperators) {
      const phrase = query.caseSensitive ? op.phrase : op.phrase.toLowerCase()
      results = results.filter((r) => {
        const item = r.item
        const name = query.caseSensitive ? item.name : item.name.toLowerCase()
        const desc = query.caseSensitive
          ? (item.description ?? "")
          : (item.description ?? "").toLowerCase()
        return name.includes(phrase) || desc.includes(phrase)
      })
    }

    // Sort if requested (breaks streaming, but acceptable)
    if (query.sort === "score") {
      results = [...results].sort((a, b) => b.score - a.score)
    } else if (query.sort === "name") {
      results = [...results].sort((a, b) => a.item.name.localeCompare(b.item.name))
    }

    // Apply final limit (after sorting)
    if (query.limit !== undefined) {
      results = results.slice(0, query.limit)
    }

    return results
  })
```

**Key Pattern**: Driver for base search, post-filter for QueryDSL operators.

**TMNL Location**: `src/lib/search/query/executor.ts:64`

---

## Pattern 6: Stream Operators — COMPOSABLE FILTERS

**When:** Building reusable Stream filters for search results.

Create operators that compose via `Stream.pipe`:

```typescript
import { Stream } from 'effect'
import type { SearchResult, SearchError, FieldOperator } from '@/lib/search'

/**
 * Filter results by field value match (include or exclude).
 */
export const withFieldMatch = <T extends SearchableItem>(
  field: FieldOperator["field"],
  value: string,
  exclude = false
) =>
  Stream.filter<SearchResult<T>, SearchError>((r) => {
    const prop = fieldToProperty(field)
    const fieldValue = (r.item as Record<string, unknown>)[prop]
    if (typeof fieldValue !== "string") return exclude
    const matches = fieldValue.toLowerCase().includes(value.toLowerCase())
    return exclude ? !matches : matches
  })

/**
 * Filter results by regex pattern.
 *
 * Matches against name and description fields.
 * Invalid patterns are silently ignored (pass-through).
 */
export const withRegexFilter = <T extends SearchableItem>(
  pattern: string,
  caseSensitive = false
) => {
  let regex: RegExp | null = null
  try {
    regex = new RegExp(pattern, caseSensitive ? "" : "i")
  } catch {
    // Invalid regex - will pass through all results
  }

  return Stream.filter<SearchResult<T>, SearchError>((r) => {
    if (!regex) return true // Pass through if invalid
    const item = r.item
    return regex.test(item.name) || regex.test(item.description ?? "")
  })
}

/**
 * Filter results by exact phrase match.
 */
export const withPhraseMatch = <T extends SearchableItem>(
  phrase: string,
  caseSensitive = false
) =>
  Stream.filter<SearchResult<T>, SearchError>((r) => {
    const item = r.item
    const p = caseSensitive ? phrase : phrase.toLowerCase()
    const name = caseSensitive ? item.name : item.name.toLowerCase()
    const desc = caseSensitive ? (item.description ?? "") : (item.description ?? "").toLowerCase()
    return name.includes(p) || desc.includes(p)
  })

/**
 * Filter by minimum score.
 */
export const withMinScore = <T, E>(minScore: number) =>
  Stream.filter<SearchResult<T>, E>((r) => r.score >= minScore)

/**
 * Collect all results and sort by field.
 *
 * Note: This breaks streaming - all results are collected before emission.
 */
export const sortedBy = <T extends SearchableItem>(
  field: "score" | "name"
): (<E>(stream: Stream.Stream<SearchResult<T>, E>) => Stream.Stream<SearchResult<T>, E>) =>
  <E>(stream: Stream.Stream<SearchResult<T>, E>) =>
    stream.pipe(
      Stream.runCollect,
      Effect.map((chunk) => {
        const arr = Chunk.toReadonlyArray(chunk)
        const sorted =
          field === "score"
            ? [...arr].sort((a, b) => b.score - a.score)
            : [...arr].sort((a, b) => a.item.name.localeCompare(b.item.name))
        return sorted
      }),
      Stream.fromEffect,
      Stream.flatMap(Stream.fromIterable)
    )
```

**Usage**:

```typescript
const results = await Effect.runPromise(
  driver.search('godfather').pipe(
    withMinScore(0.3),
    withFieldMatch('category', 'film'),
    withRegexFilter('^The'),
    sortedBy('score'),
    Stream.take(10),
    Stream.runCollect
  )
)
```

**TMNL Location**: `src/lib/search/query/operators.ts:44`

---

## Pattern 7: Fiber Cancellation — INTERRUPT MID-SEARCH

**When:** Building search UI with cancel button.

Use `Effect.runFork` + `Fiber.interrupt` for cancellable searches:

```typescript
import { useCallback, useRef } from 'react'
import { Effect, Stream, Fiber } from 'effect'
import type { SearchServiceImpl, SearchResult, SearchError } from '@/lib/search'

const useSearchStream = (driver: SearchServiceImpl<MovieItem> | null) => {
  const fiberRef = useRef<Fiber.RuntimeFiber<void, SearchError> | null>(null)
  const [results, setResults] = useState<SearchResult<MovieItem>[]>([])
  const [status, setStatus] = useState<'idle' | 'streaming' | 'complete' | 'cancelled'>('idle')

  const search = useCallback(
    (query: string) => {
      if (!driver || !query.trim()) {
        setResults([])
        setStatus('idle')
        return
      }

      // Cancel previous fiber if running
      if (fiberRef.current) {
        Effect.runFork(Fiber.interrupt(fiberRef.current))
        setStatus('cancelled')
      }

      setResults([])
      setStatus('streaming')

      const program = driver.search(query, { limit: 100, chunkSize: 5 }).pipe(
        Stream.runForEach((result) =>
          Effect.sync(() => {
            setResults((prev) => [...prev, result])
          })
        ),
        Effect.ensuring(
          Effect.sync(() => {
            setStatus('complete')
          })
        )
      )

      fiberRef.current = Effect.runFork(program)
    },
    [driver]
  )

  const cancel = useCallback(() => {
    if (fiberRef.current) {
      Effect.runFork(Fiber.interrupt(fiberRef.current))
      setStatus('cancelled')
      fiberRef.current = null
    }
  }, [])

  return { results, status, search, cancel }
}
```

**Key Pattern**: Store fiber in ref, interrupt on cancel or new search.

**TMNL Location**: `src/components/testbed/SearchTestbed.tsx:127`

---

## Pattern 8: Benchmark Duel — FLEXSEARCH VS LINEAR

**When:** Comparing driver performance.

Race two drivers against the same query:

```typescript
import { useCallback, useState } from 'react'
import { Effect, Stream } from 'effect'
import type { SearchServiceImpl } from '@/lib/search'

interface DuelResult {
  time: number
  count: number
}

const useBenchmarkDuel = (
  flexDriver: SearchServiceImpl<MovieItem> | null,
  linearDriver: SearchServiceImpl<MovieItem> | null
) => {
  const [flexResult, setFlexResult] = useState<DuelResult | null>(null)
  const [linearResult, setLinearResult] = useState<DuelResult | null>(null)
  const [isRunning, setIsRunning] = useState(false)

  const runDuel = useCallback(
    async (query: string) => {
      if (!flexDriver || !linearDriver || !query.trim()) return

      setIsRunning(true)
      setFlexResult(null)
      setLinearResult(null)

      // Race FlexSearch
      const flexStart = performance.now()
      const flexResults = await Effect.runPromise(
        flexDriver.search(query, { limit: 50 }).pipe(Stream.runCollect)
      )
      const flexTime = performance.now() - flexStart
      setFlexResult({ time: Math.round(flexTime * 100) / 100, count: flexResults.length })

      // Race Linear
      const linearStart = performance.now()
      const linearResults = await Effect.runPromise(
        linearDriver.search(query, { limit: 50 }).pipe(Stream.runCollect)
      )
      const linearTime = performance.now() - linearStart
      setLinearResult({ time: Math.round(linearTime * 100) / 100, count: linearResults.length })

      setIsRunning(false)
    },
    [flexDriver, linearDriver]
  )

  const winner =
    flexResult && linearResult
      ? flexResult.time < linearResult.time
        ? 'flex'
        : 'linear'
      : null

  return { flexResult, linearResult, winner, isRunning, runDuel }
}
```

**Key Pattern**: Sequential execution with timing, visual winner comparison.

**TMNL Location**: `src/components/testbed/SearchTestbed.tsx:213`

---

## Pattern 9: Indices Builder — MULTI-SOURCE STREAM COMPOSITION

**When:** Composing multiple search sources (Emacs Consult pattern).

Use `Stream.mergeAll` to combine sources with metadata injection:

```typescript
import { Effect, Stream, Ref } from 'effect'
import type { SearchSource, SearchItem, MergedItem } from '@/lib/indices'

/**
 * Convert a source's items to a stream with metadata injection
 */
const sourceToStream = <T extends SearchItem>(
  source: SearchSource<T>
): Stream.Stream<MergedItem<T>> => {
  const result = source.items()

  // Check if it's already a stream
  const isStream = (x: unknown): x is Stream.Stream<T> =>
    typeof x === "object" && x !== null && "_tag" in (x as object)

  const baseStream: Stream.Stream<T> = isStream(result)
    ? result
    : pipe(
        result as Effect.Effect<readonly T[]>,
        Effect.map((items) => Stream.fromIterable(items)),
        Stream.unwrap
      )

  // Inject source metadata into each item
  return pipe(
    baseStream,
    Stream.map(
      (item): MergedItem<T> => ({
        ...item,
        _source: source.id,
        _sourceName: source.name,
        _sourceIcon: source.icon,
        _sourceAccent: source.accent,
      })
    ),
    // Source isolation - failures don't crash the whole search
    Stream.catchAll((error) => {
      console.warn(`[indices] Source "${source.id}" failed:`, error)
      return Stream.empty
    })
  )
}

/**
 * Create indices builder from sources
 */
export const createIndicesBuilder = <T extends SearchItem>(
  sources: readonly SearchSource<T>[],
  config: IndicesConfig = {}
): Effect.Effect<IndicesResult<T>> =>
  Effect.gen(function* () {
    const cfg = { ...DEFAULT_CONFIG, ...config }

    // Filter to enabled sources
    const enabledSources = sources.filter((s) => {
      if (s.hidden && !cfg.includeHidden) return false
      if (s.enabled && !s.enabled()) return false
      return true
    })

    // Create individual source streams
    const sourceStreams = enabledSources.map((source) => sourceToStream(source))

    // Merge all streams (unordered for speed)
    const mergedStream = Stream.mergeAll(sourceStreams, {
      concurrency: cfg.concurrency,
    })

    // Create narrow state ref
    const narrowStateRef = yield* Ref.make<NarrowState>({
      activeKey: null,
      keyToSource: buildKeyToSourceMap(enabledSources),
    })

    return {
      stream: mergedStream,
      narrow: (key: string) =>
        Ref.update(narrowStateRef, (state) => ({ ...state, activeKey: key })),
      widen: () =>
        Ref.update(narrowStateRef, (state) => ({ ...state, activeKey: null })),
      narrowState: Ref.get(narrowStateRef),
      sources: enabledSources,
      getSourceByKey: (key: string) => enabledSources.find((s) => s.narrowKey === key),
    }
  })
```

**Key Pattern**: `Stream.mergeAll` + metadata injection + narrowing via Ref.

**TMNL Location**: `src/lib/indices/builder.ts:140`

---

## Pattern 10: SearchSource Definition — CONSULT-INSPIRED

**When:** Defining a search source for the indices builder.

Inspired by Emacs Consult's source plist pattern:

```typescript
import { Effect } from 'effect'
import type { SearchSource } from '@/lib/indices'

interface TestbedIndexItem {
  readonly id: string
  readonly name: string
  readonly route: string
  readonly category: 'data' | 'ui' | 'animation'
  readonly description?: string
}

const testbedSource: SearchSource<TestbedIndexItem> = {
  id: 'testbeds',
  name: 'Testbeds',
  narrowKey: 't',
  category: 'navigation',
  icon: '◈',
  accent: 'cyan',
  hidden: false,
  enabled: () => true,

  // Sync items
  items: () => Effect.succeed(getSearchableTestbeds()),

  // Action on selection
  action: (item) =>
    Effect.sync(() => {
      navigate(item.route)
    }),

  // Optional preview
  preview: (item) =>
    Effect.succeed({
      type: 'route' as const,
      route: item.route,
    }),
}
```

**Key Fields**:
- `narrowKey` — Press key + space to filter to this source only
- `items` — Sync (Effect) or async (Stream) candidate generator
- `action` — Execute on selection
- `preview` — Optional live preview during selection

**TMNL Location**: `src/lib/indices/sources.ts` (conceptual)

---

## Decision Tree: Which Pattern?

```
What are you building?
│
├─ Search UI with progressive results?
│  └─ Pattern 2: FlexSearch Driver + Stream chunks + Pattern 7: Fiber cancellation
│
├─ QueryDSL parser?
│  └─ Pattern 3: Effect Schema operators + Pattern 4: Regex extraction
│
├─ QueryDSL executor?
│  └─ Pattern 5: Hybrid driver + post-filter
│
├─ Composable search filters?
│  └─ Pattern 6: Stream operators (withMinScore, withFieldMatch, etc.)
│
├─ Performance comparison?
│  └─ Pattern 8: Benchmark duel (FlexSearch vs Linear)
│
├─ Multi-source search (Emacs Consult)?
│  └─ Pattern 9: Indices builder + Pattern 10: SearchSource definition
│
└─ Custom search driver?
   └─ Pattern 1: SearchServiceImpl interface (Stream for queries, Effect for mutations)
```

---

## Anti-Patterns

### Don't: Return Effect from search queries

```typescript
// BANNED - queries should return Stream, not Effect
search: (query: string) => Effect.Effect<SearchResult<T>[]>

// CORRECT - Stream for progressive emission
search: (query: string) => Stream.Stream<SearchResult<T>, SearchError>
```

### Don't: Extract operators in wrong order

```typescript
// BANNED - field operators extracted before quotes
for (const match of input.matchAll(FIELD_PATTERN)) { ... }
for (const match of input.matchAll(QUOTED_PATTERN)) { ... }

// CORRECT - quotes FIRST to preserve spaces inside phrases
for (const match of input.matchAll(QUOTED_PATTERN)) { ... }
for (const match of input.matchAll(FIELD_PATTERN)) { ... }
```

### Don't: Forget to handle empty queries in executor

```typescript
// BANNED - empty query returns nothing from FlexSearch
const results = yield* driver.search("", options)

// CORRECT - detect operators-only queries and get all items first
if (!query.text.trim() && hasOperators(query)) {
  const stats = yield* driver.stats()
  results = yield* driver.search("", { limit: stats.itemCount + 100 })
}
```

### Don't: Ignore invalid regex patterns

```typescript
// BANNED - throws on invalid pattern
const regex = new RegExp(op.pattern, flags)

// CORRECT - catch and skip invalid patterns
let regex: RegExp
try {
  regex = new RegExp(op.pattern, flags)
} catch {
  continue // Skip this filter
}
```

### Don't: Forget to interrupt previous fiber

```typescript
// BANNED - new search leaves old fiber running
const program = driver.search(query)
fiberRef.current = Effect.runFork(program)

// CORRECT - interrupt previous fiber first
if (fiberRef.current) {
  Effect.runFork(Fiber.interrupt(fiberRef.current))
}
fiberRef.current = Effect.runFork(program)
```

---

## Integration Points

**Depends on:**
- `effect-patterns` — Effect.gen, Stream.Stream, Ref.make
- `effect-schema-mastery` — Schema.Struct, Schema.Literal, TaggedStruct
- `effect-stream-patterns` — Stream.async, Stream.mergeAll, Stream.runCollect

**Used by:**
- Command palette (search commands with QueryDSL)
- File search (multi-field search with regex)
- Testbed navigation (indices builder with narrowing)

---

## Quick Reference

| Task | Pattern | File |
|------|---------|------|
| Create FlexSearch driver | `createFlexSearchDriver<T>()` | drivers/flexsearch.ts:40 |
| Create Linear driver | `createLinearDriver<T>()` | drivers/linear.ts |
| Parse QueryDSL | `parseQuery(input)` | query/parser.ts:83 |
| Execute QueryDSL | `executeQuery(driver, query)` | query/executor.ts:64 |
| Filter by min score | `withMinScore(0.3)` | operators.ts |
| Filter by field | `withFieldMatch('category', 'grid')` | query/operators.ts:44 |
| Filter by regex | `withRegexFilter('^nav.*')` | query/operators.ts:79 |
| Filter by phrase | `withPhraseMatch('add row')` | query/operators.ts:133 |
| Sort results | `sortedBy('score')` | query/operators.ts:173 |
| Cancel search | `Fiber.interrupt(fiberRef.current)` | SearchTestbed.tsx:143 |
| Benchmark duel | `useBenchmarkDuel(flex, linear)` | SearchTestbed.tsx:213 |
| Build indices | `createIndicesBuilder(sources)` | indices/builder.ts:140 |
| Define source | `SearchSource<T>` interface | indices/types.ts:63 |
| Narrow to source | `indices.narrow('t')` | indices/builder.ts:182 |
| Widen all sources | `indices.widen()` | indices/builder.ts:187 |
