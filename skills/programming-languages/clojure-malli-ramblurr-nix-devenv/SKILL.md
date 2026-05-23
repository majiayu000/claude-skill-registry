---
name: clojure-malli
description: |
  Data validation with Malli schemas in Clojure. Use when working with: (0)
  malli, (1) data validation or coercion, (2) defining schemas for maps,
  collections, or domain models, (3) API request/response validation, (4) form
  validation, (5) runtime type checking, or when the user mentions malli,
  schemas, validation, data contracts, or data integrity.

---

# Malli Data Validation

Malli validates data against schemas. Schemas are Clojure data structures.

## Quick Validation

```clojure
(require '[malli.core :as m])
(require '[malli.error :as me])

;; Validate
(m/validate [:map [:name :string] [:age :int]]
            {:name "Alice" :age 30})
;; => true

;; Get errors
(-> [:map [:name :string] [:age :int]]
    (m/explain {:name "Alice" :age "thirty"})
    (me/humanize))
;; => {:age ["should be an integer"]}
```

## Quick Coercion

```clojure
(require '[malli.transform :as mt])

;; Decode string input to proper types
(m/decode [:map [:port :int] [:active :boolean]]
          {:port "8080" :active "true"}
          (mt/string-transformer))
;; => {:port 8080, :active true}

;; Coerce = decode + validate (throws on error)
(m/coerce [:map [:id :int]] {:id "42"} (mt/string-transformer))
;; => {:id 42}
```

## Common Schema Patterns

### Maps with Required/Optional Keys

```clojure
[:map
 [:id :uuid]                              ;; required
 [:name :string]                          ;; required
 [:email {:optional true} :string]        ;; optional
 [:role {:default "user"} :string]]       ;; optional with default
```

### Constrained Values

```clojure
[:string {:min 1 :max 100}]    ;; string length 1-100
[:int {:min 0 :max 150}]       ;; integer range
[:enum "draft" "published"]    ;; one of these values
[:re #".+@.+\..+"]             ;; regex match
```

### Collections

```clojure
[:vector :int]                 ;; vector of ints
[:set :keyword]                ;; set of keywords
[:map-of :keyword :string]     ;; map with keyword keys, string values
[:tuple :double :double]       ;; fixed [x, y] pair
```

### Unions and Conditionals

```clojure
;; Simple union
[:or :string :int]

;; Nilable
[:maybe :string]               ;; string or nil

;; Tagged union with dispatch
[:multi {:dispatch :type}
 [:user [:map [:type [:= :user]] [:name :string]]]
 [:admin [:map [:type [:= :admin]] [:role :string]]]]
```

### Nested Structures

```clojure
[:map
 [:user [:map
         [:name :string]
         [:address [:map
                    [:city :string]
                    [:zip :string]]]]]]
```

## Performance: Cache Validators

```clojure
;; BAD - creates validator every call
(defn process [data]
  (when (m/validate schema data) ...))

;; GOOD - cached validator
(def valid? (m/validator schema))
(defn process [data]
  (when (valid? data) ...))

;; Same for decoders
(def decode-request (m/decoder schema (mt/string-transformer)))
(def coerce-request (m/coercer schema (mt/string-transformer)))
```

## Key Gotchas

1. **decode doesn't validate** - returns invalid data as-is. Use `coerce` for safety.
2. **Maps are open by default** - extra keys allowed. Use `{:closed true}` to reject them.
3. **Keys are required by default** - use `{:optional true}` for optional keys.

## Detailed References

- **[Schema Syntax](references/schema-syntax.md)** - All builtin types, properties, operators
- **[API Reference](references/api-reference.md)** - Core functions with signatures
- **[Registries](references/registries.md)** - Reusable schema patterns
