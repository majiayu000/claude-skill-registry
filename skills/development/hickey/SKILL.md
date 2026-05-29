---
name: hickey-simple-made-easy
description: Write functional code in the style of Rich Hickey, creator of Clojure. Emphasizes simplicity over easiness, immutability, data-oriented programming, and managing state explicitly. Use when designing systems that need to be understood and maintained.
---

# Rich Hickey Style Guide

## Overview

Rich Hickey is the creator of Clojure and Datomic. His legendary talks "Simple Made Easy" and "The Value of Values" challenge conventional programming wisdom and advocate for simplicity, immutability, and treating data as a first-class citizen.

## Core Philosophy

> "Simple is not easy. Easy is familiar. Simple is about lack of interleaving."

> "State. You're doing it wrong."

> "It is better to have 100 functions operate on one data structure than 10 functions on 10 data structures."

Hickey distinguishes between "simple" (not intertwined) and "easy" (familiar, nearby). He argues we should pursue simplicity even when it's not easy.

## Design Principles

1. **Simple ≠ Easy**: Simple means not complected (intertwined). Pursue it.

2. **Values Over State**: Immutable values simplify everything.

3. **Data > Objects**: Plain data with generic functions beats object hierarchies.

4. **Explicit State**: When state is needed, manage it explicitly.

## When Writing Code

### Always

- Prefer immutable data structures
- Use maps, vectors, sets—plain data
- Separate data from functions
- Make state changes explicit and controlled
- Design with time in mind (values don't change)
- Question complexity—is this complected?

### Never

- Conflate simple with easy
- Hide state in objects
- Create unnecessary abstractions
- Reach for classes when data suffices
- Ignore the cost of complexity
- Complect things that could be separate

### Prefer

- Maps over objects
- Pure functions over methods
- Composition over inheritance
- Declarative over imperative
- Data literals over constructors
- Namespaced keywords over types

## Code Patterns

### Data Orientation

```clojure
;; BAD: Object-oriented thinking
(defrecord Person [name age email])
(defn person-greet [person]
  (str "Hello, " (:name person)))

;; GOOD: Just use maps—they're data
(def person {:name "Alice" :age 30 :email "alice@example.com"})

;; Generic functions work on all maps
(defn greet [entity]
  (str "Hello, " (:name entity)))

;; Works for any map with :name
(greet {:name "Bob" :type :user})
(greet {:name "Acme" :type :company})


;; 100 functions on 1 data structure
;; All of these work on your map:
(get person :name)
(assoc person :age 31)
(update person :age inc)
(select-keys person [:name :email])
(keys person)
(vals person)
(merge person {:title "Dr."})
```

### Immutability

```clojure
;; Data doesn't change—you create new data
(def v1 [1 2 3])
(def v2 (conj v1 4))

v1  ;; Still [1 2 3]
v2  ;; [1 2 3 4]

;; Structural sharing makes this efficient
;; v1 and v2 share structure in memory


;; Update nested structures with assoc-in, update-in
(def user {:name "Alice" 
           :address {:city "Portland" 
                     :zip "97201"}})

(def updated (assoc-in user [:address :city] "Seattle"))
;; user is unchanged, updated has new city


;; No defensive copying needed
(defn process [data]
  ;; data cannot be mutated, safe to pass around
  (transform data))
```

### Explicit State with Atoms

```clojure
;; When you need state, make it explicit
(def counter (atom 0))

;; Read state
@counter  ;; 0

;; Update state (pure function applied atomically)
(swap! counter inc)  ;; 1
(swap! counter + 10) ;; 11

;; State is in ONE place, not scattered through objects
;; Updates are explicit, not hidden in setters


;; For complex state, use a single atom with a map
(def app-state 
  (atom {:users {}
         :sessions {}
         :config {:debug false}}))

;; Update specific parts
(swap! app-state assoc-in [:config :debug] true)
(swap! app-state update-in [:users] assoc "alice" {:name "Alice"})
```

### Simple vs Easy

```clojure
;; EASY but COMPLEX: Object with intertwined concerns
;; - State + identity + behavior all mixed
;; - Hard to test, hard to reason about
(defprotocol OrderProcessor
  (add-item [this item])
  (remove-item [this item-id])
  (calculate-total [this])
  (submit [this]))

;; SIMPLE: Separate concerns
;; Data (just values)
(def order {:items [] :status :draft})

;; Pure functions (no state)
(defn add-item [order item]
  (update order :items conj item))

(defn calculate-total [order]
  (reduce + (map :price (:items order))))

;; Side effects isolated
(defn submit-order! [order]
  (db/save! order)
  (email/send-confirmation! order))

;; Each piece is:
;; - Testable in isolation
;; - Understandable alone
;; - Recombinable
```

### Spec for Data Validation

```clojure
(require '[clojure.spec.alpha :as s])

;; Describe your data
(s/def ::name string?)
(s/def ::age pos-int?)
(s/def ::email (s/and string? #(re-matches #".+@.+" %)))

(s/def ::person
  (s/keys :req-un [::name ::age ::email]))

;; Validate
(s/valid? ::person {:name "Alice" :age 30 :email "alice@example.com"})
;; true

;; Explain failures
(s/explain ::person {:name "Alice" :age -5 :email "bad"})
;; :age - failed: pos-int?
;; :email - failed: regex match

;; Generate test data
(require '[clojure.spec.gen.alpha :as gen])
(gen/sample (s/gen ::person))
```

### Transducers for Composition

```clojure
;; Problem: each step creates intermediate collections
(->> data
     (map transform)      ;; new collection
     (filter valid?)      ;; new collection
     (take 10))           ;; new collection

;; Solution: transducers compose without intermediate collections
(def xform
  (comp
    (map transform)
    (filter valid?)
    (take 10)))

;; Apply to any collection type
(into [] xform data)        ;; vector
(into #{} xform data)       ;; set
(transduce xform + 0 data)  ;; reduce

;; Same transformation, different contexts
;; No intermediate collections created
```

### Managing Time

```clojure
;; Values are immutable—they represent a point in time
;; This enables powerful patterns:

;; 1. History (undo/redo)
(def history (atom []))
(def current (atom {:count 0}))

(defn update-with-history! [f & args]
  (swap! history conj @current)
  (swap! current #(apply f % args)))

(defn undo! []
  (when (seq @history)
    (reset! current (peek @history))
    (swap! history pop)))


;; 2. Snapshotting
(defn snapshot []
  @app-state)  ;; Returns immutable value

(def before (snapshot))
;; ... make changes ...
(def after (snapshot))

;; Compare states directly
(= before after)
(clojure.data/diff before after)
```

## The Complectedness Test

Ask these questions:

1. **Is state complected with identity?** Separate them with values + refs.
2. **Is behavior complected with data?** Use data + functions, not objects.
3. **Is order complected with logic?** Use declarative over imperative.
4. **Is specificity complected with generality?** Use generic data structures.

## Mental Model

Hickey approaches design by asking:

1. **Is this simple or just easy?** Familiar ≠ simple
2. **What is this complected with?** Find the intertwining
3. **Is this data or process?** Separate them
4. **Where does state live?** Make it explicit
5. **What happens over time?** Values + references

## Signature Hickey Moves

- Maps for everything
- Pure functions on immutable data
- Atoms for explicit state
- Transducers for composable transforms
- Spec for data validation
- Separating complected concerns
