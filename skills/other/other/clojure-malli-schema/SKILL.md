---
name: clojure-malli-schema
description: ALWAYS use when writing or modifying Clojure functions or data structures. Defines how to add Malli schemas as :malli/schema metadata, enforces :catn over :cat for self-documenting parameter names, and covers schema registries, test fixtures with dev-mode instrumentation, and common schema patterns. Triggers on new functions, function signature changes, data structure definitions, Malli setup, schema validation issues.
---

# Malli Schema

## Why Schemas Matter

- **Validation**: Catch errors early with runtime validation (in dev/test)
- **Documentation**: Schemas serve as executable, always-up-to-date documentation — they reduce the need for type descriptions in docstrings
- **Generative Testing**: Enable property-based testing with generated test data
- **Zero Runtime Cost**: Store schemas as metadata — no production dependency on Malli
- **Better Error Messages**: Clear validation errors show exactly what's wrong

## Schema Organization

### Function Schemas
- Add as `:malli/schema` metadata on the function itself
- Keep Malli as dev-only dependency (no runtime impact)
- Metadata travels with the function definition

### Data Structure Schemas
- Define in separate schema namespace (e.g., `my-app.schema`)
- Group related schemas in registry functions
- Register in test fixtures for validation

### Schema Location Pattern
```
src/
  my_app/
    core.clj           # Functions with :malli/schema metadata
    schema.clj         # Data structure schemas + registries
test/
  my_app/
    core_test.clj      # Registers schemas in fixtures
```

## Adding Function Schemas

### Critical Rule: Always Use `:catn`

**ALWAYS use `:catn` (not `:cat`) for function parameters** to provide descriptive names. This makes schemas self-documenting — `:cat` leaves parameters unnamed, producing unclear error messages and unreadable schemas.

### Template

```clojure
(defn my-function
  "Function docstring explaining what it does"
  {:malli/schema [:=> [:catn
                       [:param-name :param-type]
                       [:other-param :other-type]]
                  :return-type]}
  [param-name other-param]
  ;; implementation
  )
```

### Why `:catn` vs `:cat`

Bad — Using `:cat`:
```clojure
{:malli/schema [:=> [:cat :string :string] :string]}
```
- Unclear which parameter is which
- No self-documentation
- Harder to debug validation errors

Good — Using `:catn`:
```clojure
{:malli/schema [:=> [:catn
                     [:uri :string]
                     [:root-path :string]]
                :string]}
```
- Immediately clear what each parameter represents
- Self-documenting
- Better error messages

### Examples

**Simple function:**
```clojure
(defn add
  "Adds two numbers"
  {:malli/schema [:=> [:catn
                       [:x :int]
                       [:y :int]]
                  :int]}
  [x y]
  (+ x y))
```

**Function with optional parameters:**
```clojure
(defn fetch-user
  "Fetches user with optional timeout"
  {:malli/schema [:=> [:catn
                       [:user-id :string]
                       [:options [:map
                                  [:timeout {:optional true} :int]]]]
                  [:maybe :map]]}
  [user-id options]
  ;; implementation
  )
```

**Function returning maybe/optional:**
```clojure
(defn find-by-id
  "Finds entity by ID, returns nil if not found"
  {:malli/schema [:=> [:catn [:id :int]]
                  [:maybe :map]]}
  [id]
  ;; implementation
  )
```

**Higher-order function (returns function):**
```clojure
(defn make-adder
  "Creates a function that adds n to its input"
  {:malli/schema [:=> [:catn [:n :int]]
                  [:fn #(fn? %)]]}
  [n]
  (fn [x] (+ x n)))
```

**Multi-arity function:**
```clojure
(defn greet
  "Greets a person, optionally with title"
  {:malli/schema [:function
                  [:=> [:catn [:name :string]] :string]
                  [:=> [:catn [:title :string] [:name :string]] :string]]}
  ([name]
   (str "Hello, " name))
  ([title name]
   (str "Hello, " title " " name)))
```

**Single-argument function (still use `:catn` for consistency):**
```clojure
(defn square
  "Squares a number"
  {:malli/schema [:=> [:catn [:n :int]]
                  :int]}
  [n]
  (* n n))
```

## Adding Data Structure Schemas

### 1. Define the Schema

In your schema namespace (e.g., `my_app/schema.clj`):

```clojure
(ns my-app.schema
  (:require [malli.core :as m]))

(def user?
  "Schema for user data structure"
  [:map
   [:id :int]
   [:name :string]
   [:email [:string {:min 5}]]
   [:age {:optional true} :int]
   [:roles [:set :keyword]]])

(def http-request?
  "Schema for HTTP request"
  [:map
   [:method [:enum :get :post :put :delete]]
   [:uri :string]
   [:headers {:optional true} [:map-of :string :string]]
   [:body {:optional true} :any]])
```

### 2. Create Registry Function

Group related schemas:

```clojure
(defn user-schemas []
  {:user user?
   :http-request http-request?})

(defn validation-schemas []
  {:email-regex #"^[^@]+@[^@]+\.[^@]+$"
   :phone-regex #"^\d{3}-\d{3}-\d{4}$"})
```

### 3. Register in Tests

In your test file, register schemas in fixtures:

```clojure
(ns my-app.core-test
  (:require [clojure.test :refer [deftest is testing use-fixtures]]
            [my-app.schema :as app-schema]
            [malli.core :as m]
            [malli.dev :as mdev]
            [malli.registry :as mr]))

(use-fixtures :once
  (fn [f]
    (mr/set-default-registry!
     (merge
      (m/comparator-schemas)
      (m/type-schemas)
      (m/sequence-schemas)
      (m/base-schemas)
      (app-schema/user-schemas)
      (app-schema/validation-schemas)))
    (mdev/start!)  ;; Enable dev-mode instrumentation
    (f)
    (mdev/stop!)
    (mr/set-default-registry! m/default-registry)))
```

## Schema Checklist for New Code

When adding or modifying code, ensure:

- [ ] All public functions have `:malli/schema` metadata
- [ ] Function schemas use `:catn` (not `:cat`) with descriptive parameter names
- [ ] All data structures passed between functions are defined in schema namespace
- [ ] New schemas are added to appropriate registry function
- [ ] Test registries are updated to include new schema groups
- [ ] Tests pass (validates schemas work correctly)
- [ ] Schemas use custom types from registry (not just primitives) when applicable

## Verification Workflow

Before committing code:

1. **Run tests** — schemas are validated automatically when dev-mode is active
   ```bash
   # For devbox projects: devbox run -- bb test
   ```

2. **Check Malli dev-mode output** — look for:
   - "instrumented N function vars" message
   - No schema-related errors or warnings
   - All expected functions instrumented

3. **Verify schema errors are helpful** — if validation fails:
   - Error message should clearly indicate which parameter failed
   - Should show expected vs actual types
   - `:catn` names should appear in error messages

## Project Setup

### Initial Malli Setup

Add Malli as a dev dependency (use the latest stable version from [Malli releases](https://github.com/metosin/malli/releases)):

**deps.edn:**
```clojure
{:deps {}
 :aliases
 {:dev {:extra-deps {metosin/malli {:mvn/version "LATEST"}}}
  :test {:extra-deps {metosin/malli {:mvn/version "LATEST"}}}}}
```

### Create Schema Namespace

```clojure
(ns my-app.schema
  "Malli schemas for data validation"
  (:require [malli.core :as m]))

;; Define your schemas here

(defn all-schemas []
  "Registry of all application schemas"
  {})
```

## Best Practices

1. **Add schemas as you write code** — don't retrofit later
2. **Use `:catn` always** — even for single-arg functions
3. **Keep schemas close to data** — define in schema namespace, use in code
4. **Use descriptive parameter names** — `[:uri :string]` not `[:s :string]`
5. **Prefer custom types over primitives** — create `:user-id` type instead of using `:int` everywhere
6. **Test schema validation** — write tests that intentionally violate schemas
7. **Update schemas with code changes** — keep them in sync
8. **Use dev-mode in tests** — catches schema violations early

## Common Pitfalls to Avoid

Using `:cat` instead of `:catn`:
```clojure
{:malli/schema [:=> [:cat :string :int] :string]}  ;; Bad!
```

Forgetting to register custom schemas:
```clojure
;; Defined :user-id in schema.clj but forgot to add to registry
{:malli/schema [:=> [:catn [:id :user-id]] :map]}  ;; Will fail!
```

Missing metadata key:
```clojure
(defn foo [x]
  [:=> [:catn [:x :int]] :int]  ;; Wrong! Not in metadata
  (+ x 1))
```

Not using dev-mode in tests:
```clojure
;; Missing (mdev/start!) in test fixture
;; Schemas defined but never validated!
```

## Troubleshooting

### "Schema not found: :my-type"
- Check that the schema is defined in your schema namespace
- Verify the registry function includes the schema
- Ensure test fixtures register your schemas

### "Unable to resolve symbol: mdev"
- Add Malli to dev/test dependencies
- Require `[malli.dev :as mdev]` in test namespace

### Functions not being instrumented
- Verify `(mdev/start!)` is called in test fixture
- Check that registry is set before dev-mode starts
- Ensure function has `:malli/schema` metadata (not just a schema)

### Validation errors are unclear
- Switch from `:cat` to `:catn` for better error messages
- Add `:title` or `:description` to schemas for clarity
- Use specific custom types instead of generic primitives

For common schema patterns and a quick reference card, read `references/malli-patterns.md`.
