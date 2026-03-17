---
name: fx-registry
description: Create new Sandestin effect registries following project conventions. Use when adding effects, actions, or placeholders. Keywords: registry, effect, action, placeholder, handler, create, new.
---

# Sandestin Registry Author

Create effect registries for Sandestin projects.

## About Sandestin

Sandestin is a Clojure effect dispatch library with schema-driven discoverability. Registries define effects, actions, and placeholders that can be composed and dispatched.

**GitHub:** https://github.com/brianium/sandestin

### Check if Installed

Look for the dependency in `deps.edn`:

```clojure
io.github.brianium/sandestin {:git/tag "v0.3.0" :git/sha "2be6acc"}
```

### Install if Missing

Add to `deps.edn` under `:deps`:

```clojure
{:deps
 {io.github.brianium/sandestin {:git/tag "v0.3.0" :git/sha "2be6acc"}}}
```

## Workflow

### 1. Check for Existing Patterns

```bash
# Find existing registries
find src -name "*.clj" | xargs grep -l "::s/effects" 2>/dev/null

# Check naming conventions
grep -r "defn registry" src/
```

### 2. Create the Registry

#### Simple Registry (no config)

```clojure
(ns mylib.fx.logging
  "Logging effects."
  (:require [ascolais.sandestin :as s]))

(def registry
  {::s/effects
   {:mylib.log/info
    {::s/description "Log an info message"
     ::s/schema [:tuple [:= :mylib.log/info] :string]
     ::s/handler (fn [_ctx _system msg]
                   (println "[INFO]" msg))}}})
```

#### Configurable Registry (with dependencies)

```clojure
(ns mylib.fx.database
  "Database effects."
  (:require [ascolais.sandestin :as s]))

(defn registry
  "Database effects registry.

   Requires a datasource."
  [datasource]
  {::s/effects
   {:mylib.db/query
    {::s/description "Execute a SQL query"
     ::s/schema [:tuple [:= :mylib.db/query] :string [:* :any]]
     ::s/system-keys [:datasource]
     ::s/handler (fn [_ctx system sql & params]
                   (jdbc/execute! (:datasource system) (into [sql] params)))}}

   ::s/system-schema
   {:datasource [:fn some?]}})
```

### 3. Registration Patterns

**Effect** (side-effecting):

```clojure
{:<ns>/<verb>
 {::s/description "What this effect does"
  ::s/schema [:tuple [:= :<ns>/<verb>] <arg-schemas>]
  ::s/system-keys [:key1 :key2]
  ::s/handler (fn [{:keys [dispatch dispatch-data system]} system & args]
                ;; Do side effect, optionally dispatch continuation
                )}}
```

**Continuation dispatch arities:**

The `dispatch` function in handler context supports three arities:

| Arity | Purpose |
|-------|---------|
| `(dispatch fx)` | Dispatch with current system and dispatch-data |
| `(dispatch extra-data fx)` | Merge `extra-data` into dispatch-data |
| `(dispatch system-override extra-data fx)` | Merge into both system and dispatch-data |

```clojure
;; Add data for placeholders in continuation
(dispatch {:result result} continuation-fx)

;; Override system for nested effects (e.g., route to different connection)
(dispatch {:sse alt-connection}  ;; merged into system
          {:request-id id}       ;; merged into dispatch-data
          continuation-fx)
```

**Action** (pure, returns effect vectors):

```clojure
{:<ns>/<action>
 {::s/description "What this action does"
  ::s/schema [:tuple [:= :<ns>/<action>] <arg-schema>]
  ::s/handler (fn [state & args]
                [[:<ns>/effect1 arg]
                 [:<ns>/effect2 (:val state)]])}}

;; If actions need state from system:
::s/system->state (fn [system] @(:app-state system))
```

**Placeholder** (resolves from dispatch-data):

```clojure
{:<ns>/<placeholder>
 {::s/description "What value this provides"
  ::s/schema [:tuple [:= :<ns>/<placeholder>]]
  ::s/handler (fn [dispatch-data]
                (:some-key dispatch-data))}}

;; Placeholder with arguments
{:<ns>/<placeholder>
 {::s/description "What value this provides"
  ::s/schema [:tuple [:= :<ns>/<placeholder>] <arg-schema>]
  ::s/handler (fn [dispatch-data arg]
                (get-in dispatch-data [:results arg]))}}
```

**Self-Preserving Placeholder** (for async continuations):

When an effect dispatches continuation effects with new data, placeholders in those continuations must "self-preserve" — return themselves when the data isn't available yet, then resolve when re-interpolated with the actual data.

```clojure
{:<ns>/<result>
 {::s/description "Result from async operation, self-preserving"
  ::s/schema [:tuple [:= :<ns>/<result>]]
  ::s/handler (fn [dispatch-data]
                ;; Return self if data not yet available
                (or (:<ns>/<result> dispatch-data)
                    [:<ns>/<result>]))}}
```

Usage pattern:

```clojure
;; Effect that dispatches continuation with result
{:<ns>/fetch
 {::s/handler
  (fn [{:keys [dispatch]} system url continuation-fx]
    (let [result (http/get url)]
      ;; Dispatch continuation with result in dispatch-data
      (dispatch {:<ns>/result result} continuation-fx))
    :fetch-started)}}

;; Calling code - placeholder resolves in continuation dispatch
(dispatch {} {}
  [[:<ns>/fetch "http://api.example.com"
    [[:<ns>/process [:<ns>/result]]]]])
```

Flow:
1. Initial dispatch interpolates `[:<ns>/result]` → returns itself (no data yet)
2. Effect runs, calls `dispatch` with `{:<ns>/result actual-data}`
3. Continuation dispatch interpolates `[:<ns>/result]` → returns `actual-data`

### 4. Wire Registries to Dispatch

**Important:** `create-dispatch` takes a **vector of registries**, not a single registry.

```clojure
;; Correct - vector of registries
(def dispatch (s/create-dispatch [my-registry]))

;; Wrong - will fail
(def dispatch (s/create-dispatch my-registry))
```

#### Combining Multiple Registries

Registries can be simple maps or `[registry-fn & args]` vectors for configurable registries:

```clojure
(ns myapp.dispatch
  (:require [ascolais.sandestin :as s]
            [myapp.fx.db :as db]
            [myapp.fx.logging :as logging]
            [myapp.fx.http :as http]))

(defn create-dispatch
  "Create dispatch with all application registries."
  [{:keys [datasource http-client]}]
  (s/create-dispatch
    [[db/registry datasource]      ;; configurable - passes datasource arg
     logging/registry              ;; simple - no config needed
     [http/registry http-client]])) ;; configurable - passes client arg
```

#### Registry Merge Behavior

When registries have overlapping keys:
- **Effects, actions, placeholders**: Later registry wins (with warning via tap>)
- **Interceptors**: Concatenated in order
- **system-schema**: Merged (later wins per key)

### 5. Test via REPL

```clojure
(require '[ascolais.sandestin :as s])
(require '[mylib.fx.logging :as logging])

;; Create a test dispatch
(def dispatch (s/create-dispatch [logging/registry]))

;; Verify registration
(s/describe dispatch :mylib.log/info)
(s/sample dispatch :mylib.log/info)

;; Test it
(dispatch {} {} [[:mylib.log/info "hello"]])
```

## Required Fields

| Field | Purpose |
|-------|---------|
| `::s/description` | Human-readable description |
| `::s/schema` | Malli schema for how the effect is **called** |
| `::s/handler` | Implementation function |

### Schema Format

**Schemas describe invocation shape, NOT return types.** The schema specifies how to call the effect — the effect key and its arguments:

```clojure
[:tuple [:= :qualified/keyword] <arg-schemas...>]
```

Examples:

```clojure
;; Effect taking a string argument
::s/schema [:tuple [:= :mylib.log/info] :string]
;; Called as: [:mylib.log/info "hello"]

;; Effect taking a set of symbols
::s/schema [:tuple [:= :mylib.stock/analyze] [:set :string]]
;; Called as: [:mylib.stock/analyze #{"AAPL" "GOOG"}]

;; Effect taking a map argument
::s/schema [:tuple [:= :mylib.report/render] [:map {:description "Report data"}]]
;; Called as: [:mylib.report/render {:title "Q4" :data [...]}]
```

**Do NOT** document return types in schemas. Schemas are for discoverability of how to invoke effects, not for validating outputs.

## Optional Fields

| Field | Purpose |
|-------|---------|
| `::s/system-keys` | Declare system map dependencies |
| `::s/system-schema` | Malli schemas for system keys |
| `::s/system->state` | Extract immutable state for actions |

## Placeholder Patterns

| Pattern | When to Use |
|---------|-------------|
| Simple | Value available at dispatch time (e.g., DOM event data) |
| Self-preserving | Value available later via continuation dispatch (e.g., async results) |
| Transforming | Wraps another placeholder to transform its value |

**Transforming placeholder example:**

```clojure
;; Extract field from async result
{:<ns>/result-name
 {::s/description "Extract name from async result"
  ::s/schema [:tuple [:= :<ns>/result-name]]
  ::s/handler
  (fn [dispatch-data]
    ;; Check if result is available before transforming
    (if-let [result (:<ns>/result dispatch-data)]
      (:name result)
      [:<ns>/result-name]))}}

;; Usage: [:<ns>/result-name] instead of nesting
```
