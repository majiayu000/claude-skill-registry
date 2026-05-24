---
name: clojure-test-check
description: Property-based testing with clojure.test.check. Use when writing generative tests, creating custom generators, or debugging shrinking behavior. Triggers on test.check imports, prop/for-all, gen/* usage, or questions about property-based testing in Clojure.
---

# test.check

Property-based testing generates random test data to verify properties hold across many inputs. Instead of specific test cases, define universal properties.

## Core Pattern

```clojure
(require '[clojure.test.check :as tc]
         '[clojure.test.check.generators :as gen]
         '[clojure.test.check.properties :as prop])

(def my-property
  (prop/for-all [v (gen/vector gen/small-integer)]
    (= (count v) (count (reverse v)))))

(tc/quick-check 100 my-property)
;; => {:result true, :pass? true, :num-tests 100, ...}
```

## clojure.test Integration

```clojure
(require '[clojure.test.check.clojure-test :refer [defspec]])

(defspec sort-is-idempotent ;; 100 optional  iterations value here
  (prop/for-all [v (gen/vector gen/small-integer)]
    (= (sort v) (sort (sort v)))))
```

Important! Prefer NOT to supply an iterations, prefer the framework defaults

## Essential Generators

| Generator | Produces |
|-----------|----------|
| `gen/small-integer` | Integers bounded by size |
| `gen/large-integer` | Full range integers |
| `gen/nat` | Non-negative integers |
| `gen/boolean` | true/false |
| `gen/string` | Strings |
| `gen/keyword` | Keywords |
| `(gen/vector g)` | Vectors of g |
| `(gen/tuple g1 g2)` | Fixed heterogeneous vectors |
| `(gen/elements coll)` | Random element from coll |
| `(gen/one-of [g1 g2])` | Choose generator randomly |

See [references/cheatsheet.md](references/cheatsheet.md) for complete generator reference.

## Generator Combinators

**fmap** - Transform generated values:
```clojure
(gen/fmap sort (gen/vector gen/small-integer))  ; sorted vectors
(gen/fmap set (gen/vector gen/nat))             ; sets from vectors
```

**such-that** - Filter values (use sparingly, only for likely predicates):
```clojure
(gen/such-that not-empty (gen/vector gen/boolean))
```

**bind** - Chain generators (value from first determines second):
```clojure
(gen/bind (gen/not-empty (gen/vector gen/small-integer))
          #(gen/tuple (gen/return %) (gen/elements %)))
```

**let** - Macro combining fmap/bind:
```clojure
(gen/let [a gen/nat
          b gen/nat]
  {:sum (+ a b) :a a :b b})
```

## Custom Record Generators

```clojure
(defrecord User [name id email])

(def user-gen
  (gen/fmap (partial apply ->User)
            (gen/tuple gen/string-alphanumeric
                       gen/nat
                       (gen/fmap #(str % "@example.com") gen/string-alphanumeric))))
```

## Recursive Generators

```clojure
(def json-like
  (gen/recursive-gen
    (fn [inner] (gen/one-of [(gen/list inner)
                             (gen/map gen/keyword inner)]))
    (gen/one-of [gen/small-integer gen/boolean gen/string])))
```

## Shrinking Failures

When a test fails, test.check automatically shrinks to minimal failing case:

```clojure
;; Fails on vectors containing 42
(tc/quick-check 100
  (prop/for-all [v (gen/vector gen/small-integer)]
    (not-any? #{42} v)))
;; :fail [[-35 -9 42 8 31 ...]]  <- original failure
;; :shrunk {:smallest [[42]]}    <- minimal case
```

## Critical Pitfalls

**Avoid gen/bind when gen/fmap suffices** - bind hampers shrinking:
```clojure
;; Bad: shrinks poorly
(gen/let [n (gen/fmap #(* 2 %) gen/nat)]
  (gen/vector gen/large-integer n))

;; Good: shrinks well
(gen/fmap #(cond-> % (odd? (count %)) pop)
          (gen/vector gen/large-integer))
```

**Use gen/large-integer for real integer testing** - small-integer/nat cap at ~200.

**Run at least 100 tests** - Size cycles through 0-199, fewer tests means poor coverage.

**Don't use such-that for unlikely predicates** - Will timeout. Use fmap to construct valid values instead.

See [references/advanced.md](references/advanced.md) for sizing/shrinking details.

## Common Property Patterns

**Roundtrip**: `(= x (decode (encode x)))`
**Idempotence**: `(= (f x) (f (f x)))`
**Invariant preservation**: `(= (count v) (count (sort v)))`
**Commutativity**: `(= (f a b) (f b a))`
**Model comparison**: `(= (my-impl x) (reference-impl x))`

See [references/examples.md](references/examples.md) for generator recipes.
