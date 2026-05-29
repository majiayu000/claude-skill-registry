---
name: fx-bootstrap
description: Set up Sandestin in a new project. Use when integrating sandestin into an application or library, creating dispatch namespaces, or wiring registries together. Keywords: setup, bootstrap, create-dispatch, wire, integrate, project.
---

# Sandestin Project Bootstrap

Set up Sandestin effect dispatch in a new project or library.

## About Sandestin

Sandestin is a Clojure effect dispatch library with schema-driven discoverability. This skill helps you integrate sandestin into your project by creating the dispatch wiring.

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

## Key Concept: Dispatch vs Registry

| Concept | What It Is | Created By |
|---------|-----------|------------|
| **Registry** | Map of effects/actions/placeholders | Your code (see fx-registry skill) |
| **Dispatch** | Callable function combining registries | `s/create-dispatch` |

**Discoverability functions (`describe`, `grep`, `sample`) operate on dispatch, not registries.**

## Common Mistake

```clojure
;; WRONG - create-dispatch takes a vector, not a single registry
(def dispatch (s/create-dispatch my-registry))

;; CORRECT - wrap in a vector
(def dispatch (s/create-dispatch [my-registry]))
```

## Workflow

### 1. Identify Your Registries

Find or create registries for your project's effects:

```bash
# Find existing registries in the project
grep -r "::s/effects" src/
```

### 2. Create a Dispatch Namespace

Create a namespace that wires registries into a dispatch function:

```clojure
(ns myapp.dispatch
  "Effect dispatch for myapp."
  (:require [ascolais.sandestin :as s]
            [myapp.fx.db :as db]
            [myapp.fx.email :as email]
            [myapp.fx.logging :as logging]))

(defn create-dispatch
  "Create the application dispatch function.

   Options:
   - :datasource - database connection pool
   - :email-client - email service client"
  [{:keys [datasource email-client]}]
  (s/create-dispatch
    [[db/registry datasource]       ;; configurable registry
     [email/registry email-client]  ;; configurable registry
     logging/registry]))            ;; simple registry (no config)
```

### 3. Registry Specification Formats

`create-dispatch` accepts a vector of registry specs. Each spec can be:

| Format | Use Case | Example |
|--------|----------|---------|
| `registry-map` | Simple registry, no config | `logging/registry` |
| `[registry-fn arg1 arg2]` | Configurable registry | `[db/registry datasource]` |
| `zero-arity-fn` | Lazy/deferred registry | `my-registry-fn` |

```clojure
(s/create-dispatch
  [;; Simple map registry
   logging/registry

   ;; Configurable - calls (db/registry datasource)
   [db/registry datasource]

   ;; Zero-arity function - calls (cache/registry)
   cache/registry])
```

### 4. Export a Convenience Constructor

For libraries, export a function that creates dispatch with sensible defaults:

```clojure
(ns mylib.core
  "Public API for mylib."
  (:require [ascolais.sandestin :as s]
            [mylib.dispatch :as dispatch]))

(defn create-dispatch
  "Create a mylib dispatch function.

   Required options:
   - :datasource - JDBC datasource

   Optional:
   - :logger - custom logger (default: println)"
  [opts]
  (dispatch/create-dispatch opts))

;; Re-export discoverability for convenience
(def describe s/describe)
(def grep s/grep)
(def sample s/sample)
```

### 5. Document in CLAUDE.md (for downstream projects)

When your library uses sandestin, add usage docs to help Claude:

```markdown
## Effect Dispatch

This project uses Sandestin for effect dispatch.

### Creating Dispatch

```clojure
(require '[mylib.core :as mylib])

;; Create dispatch - note the options map
(def dispatch (mylib/create-dispatch {:datasource ds}))
```

### Discovering Effects

```clojure
(require '[ascolais.sandestin :as s])

(s/describe dispatch)           ;; List all
(s/describe dispatch :effects)  ;; Filter by type
(s/grep dispatch "user")        ;; Search
(s/sample dispatch ::mylib/save) ;; Generate sample
```
```

## Invoking Dispatch

The dispatch function signature is:

```clojure
(dispatch system dispatch-data effects)
```

| Argument | Purpose |
|----------|---------|
| `system` | Map of runtime dependencies (datasource, clients, etc.) |
| `dispatch-data` | Data for placeholder resolution |
| `effects` | Vector of effect vectors to execute |

```clojure
;; Execute effects
(dispatch
  {:datasource ds}                          ;; system
  {:current-user user}                      ;; dispatch-data (for placeholders)
  [[:myapp.db/query "SELECT * FROM users"]  ;; effects
   [:myapp.log/info "Query executed"]])
```

## Related Skills

- **fx-registry**: Create effect registries (the building blocks)
- **fx-explore**: Discover effects with describe/grep/sample
