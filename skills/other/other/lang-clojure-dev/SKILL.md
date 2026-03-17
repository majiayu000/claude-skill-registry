---
name: lang-clojure-dev
description: Foundational Clojure patterns covering functional programming, REPL-driven development, immutable data structures, and idiomatic code. Use when writing Clojure code, working with sequences and lazy evaluation, understanding macros, or needing guidance on functional programming patterns. This is the entry point for Clojure development.
---

# Clojure Fundamentals

Foundational Clojure patterns and core language features. This skill serves as a reference for idiomatic Clojure development and functional programming practices.

## Overview

**This skill covers:**
- Core syntax (functions, data structures, special forms)
- Functional programming patterns
- REPL-driven development workflow
- Immutable data structures and persistent collections
- Sequence operations and lazy evaluation
- Destructuring and pattern matching
- Macros and metaprogramming basics
- Concurrency primitives (atoms, refs, agents)
- Java interop fundamentals
- Serialization (EDN, JSON, Transit, clojure.spec)
- Build/dependencies (Leiningen, deps.edn, tools.build)
- Testing (clojure.test, test.check, Midje)

**This skill does NOT cover:**
- ClojureScript and web development - see `lang-clojurescript-dev`
- Specific frameworks (Ring, Compojure, etc.) - see framework-specific skills
- Advanced spec patterns and generative testing - see dedicated testing skills

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Define function | `(defn name [args] body)` |
| Anonymous function | `(fn [x] (* x x))` or `#(* % %)` |
| Create vector | `[1 2 3]` or `(vector 1 2 3)` |
| Create map | `{:key "value"}` or `(hash-map :key "value")` |
| Create set | `#{1 2 3}` or `(hash-set 1 2 3)` |
| Thread-first | `(-> x (f) (g))` = `(g (f x))` |
| Thread-last | `(->> coll (map f) (filter pred))` |
| Conditional | `(if test then else)` |
| Pattern match | `(case x 1 :one 2 :two :default)` |
| List comprehension | `(for [x coll] (transform x))` |

---

## Core Data Structures

### Lists

```clojure
;; Lists - linked lists, evaluated as function calls
'(1 2 3)          ; Quoted list (not evaluated)
(list 1 2 3)      ; Create list
(cons 0 '(1 2 3)) ; => (0 1 2 3)
(first '(1 2 3))  ; => 1
(rest '(1 2 3))   ; => (2 3)
(nth '(1 2 3) 1)  ; => 2
```

### Vectors

```clojure
;; Vectors - indexed access, grow at the end
[1 2 3]           ; Vector literal
(vector 1 2 3)    ; Create vector
(conj [1 2] 3)    ; => [1 2 3] (add to end)
(get [1 2 3] 1)   ; => 2
([1 2 3] 1)       ; => 2 (vectors are functions)
(assoc [1 2 3] 1 42) ; => [1 42 3]
(subvec [1 2 3 4 5] 1 4) ; => [2 3 4]
```

### Maps

```clojure
;; Maps - key-value pairs
{:name "Alice" :age 30}  ; Map literal
(hash-map :a 1 :b 2)     ; Create map
(get {:a 1} :a)          ; => 1
({:a 1} :a)              ; => 1 (maps are functions)
(:a {:a 1})              ; => 1 (keywords are functions)
(assoc {:a 1} :b 2)      ; => {:a 1 :b 2}
(dissoc {:a 1 :b 2} :b)  ; => {:a 1}
(update {:a 1} :a inc)   ; => {:a 2}
(merge {:a 1} {:b 2})    ; => {:a 1 :b 2}

;; Nested updates
(assoc-in {:user {:name "Alice"}} [:user :age] 30)
;; => {:user {:name "Alice" :age 30}}

(update-in {:user {:count 0}} [:user :count] inc)
;; => {:user {:count 1}}
```

### Sets

```clojure
;; Sets - unique elements
#{1 2 3}              ; Set literal
(hash-set 1 2 3)      ; Create set
(conj #{1 2} 3)       ; => #{1 2 3}
(disj #{1 2 3} 2)     ; => #{1 3}
(contains? #{1 2 3} 2) ; => true
(#{1 2 3} 2)          ; => 2 (sets are functions)

;; Set operations
(clojure.set/union #{1 2} #{2 3})        ; => #{1 2 3}
(clojure.set/intersection #{1 2} #{2 3}) ; => #{2}
(clojure.set/difference #{1 2} #{2 3})   ; => #{1}
```

---

## Functions

### Defining Functions

```clojure
;; Named function
(defn greet
  "Returns a greeting for the given name."
  [name]
  (str "Hello, " name "!"))

;; Multi-arity function
(defn greet
  ([] (greet "World"))
  ([name] (str "Hello, " name "!"))
  ([greeting name] (str greeting ", " name "!")))

;; Variadic function (variable arguments)
(defn sum [& numbers]
  (reduce + numbers))

(sum 1 2 3 4) ; => 10

;; Pre and post conditions
(defn divide [numerator denominator]
  {:pre [(not= denominator 0)]
   :post [(number? %)]}
  (/ numerator denominator))
```

### Anonymous Functions

```clojure
;; Full form
(fn [x] (* x x))

;; Short form
#(* % %)

;; Multiple arguments
#(+ %1 %2)

;; Using in higher-order functions
(map #(* % 2) [1 2 3]) ; => (2 4 6)
(filter #(> % 5) [3 7 2 8]) ; => (7 8)
```

### Function Composition

```clojure
;; comp - right to left composition
(def process (comp str inc))
(process 5) ; => "6"

;; partial - partial application
(def add5 (partial + 5))
(add5 10) ; => 15

;; complement - logical negation
(def not-empty? (complement empty?))
(not-empty? [1 2 3]) ; => true
```

---

## Sequence Operations

### Core Sequence Functions

```clojure
;; map - transform each element
(map inc [1 2 3]) ; => (2 3 4)
(map + [1 2 3] [10 20 30]) ; => (11 22 33)

;; filter - keep matching elements
(filter even? [1 2 3 4]) ; => (2 4)

;; remove - inverse of filter
(remove even? [1 2 3 4]) ; => (1 3)

;; reduce - accumulate
(reduce + [1 2 3 4]) ; => 10
(reduce + 100 [1 2 3]) ; => 106 (with initial value)

;; take / drop
(take 3 [1 2 3 4 5]) ; => (1 2 3)
(drop 2 [1 2 3 4 5]) ; => (3 4 5)

;; take-while / drop-while
(take-while #(< % 5) [1 2 6 7 3]) ; => (1 2)
(drop-while #(< % 5) [1 2 6 7 3]) ; => (6 7 3)
```

### Lazy Sequences

```clojure
;; Infinite sequences
(def naturals (iterate inc 0))
(take 5 naturals) ; => (0 1 2 3 4)

;; Lazy evaluation
(def evens (filter even? naturals))
(take 3 evens) ; => (0 2 4)

;; repeat
(take 3 (repeat "hi")) ; => ("hi" "hi" "hi")

;; cycle
(take 5 (cycle [1 2])) ; => (1 2 1 2 1)

;; range
(range 5)      ; => (0 1 2 3 4)
(range 2 7)    ; => (2 3 4 5 6)
(range 0 10 2) ; => (0 2 4 6 8)
```

### List Comprehension

```clojure
;; for - list comprehension
(for [x [1 2 3]]
  (* x x))
;; => (1 4 9)

;; Multiple bindings (cartesian product)
(for [x [1 2]
      y [3 4]]
  [x y])
;; => ([1 3] [1 4] [2 3] [2 4])

;; With :when (filter)
(for [x (range 10)
      :when (even? x)]
  x)
;; => (0 2 4 6 8)

;; With :let (local binding)
(for [x [1 2 3]
      :let [y (* x x)]]
  [x y])
;; => ([1 1] [2 4] [3 9])
```

---

## Destructuring

### Sequential Destructuring

```clojure
;; Vector destructuring
(let [[a b c] [1 2 3]]
  (+ a b c)) ; => 6

;; Rest binding
(let [[first & rest] [1 2 3 4]]
  rest) ; => (2 3 4)

;; Named arguments + rest
(let [[a b & more :as all] [1 2 3 4 5]]
  {:a a :b b :more more :all all})
;; => {:a 1 :b 2 :more (3 4 5) :all [1 2 3 4 5]}
```

### Associative Destructuring

```clojure
;; Map destructuring
(let [{name :name age :age} {:name "Alice" :age 30}]
  (str name " is " age)) ; => "Alice is 30"

;; Shorthand with :keys
(let [{:keys [name age]} {:name "Alice" :age 30}]
  (str name " is " age))

;; With defaults
(let [{:keys [name age] :or {age 0}} {:name "Bob"}]
  age) ; => 0

;; Nested destructuring
(let [{{{city :city} :address} :user}
      {:user {:address {:city "NYC"}}}]
  city) ; => "NYC"

;; Function arguments
(defn greet-person [{:keys [name age]}]
  (str "Hello " name ", you are " age))

(greet-person {:name "Alice" :age 30})
```

---

## Control Flow

### Conditionals

```clojure
;; if
(if (even? 4)
  "even"
  "odd") ; => "even"

;; if-not
(if-not (empty? [1 2 3])
  "has items"
  "empty") ; => "has items"

;; when (no else branch)
(when (pos? 5)
  (println "positive")
  "result") ; => "result"

;; when-not
(when-not (empty? [])
  "not empty") ; => nil

;; cond (multiple conditions)
(cond
  (< x 0) "negative"
  (> x 0) "positive"
  :else "zero")

;; condp (compare with predicate)
(condp = x
  1 "one"
  2 "two"
  3 "three"
  "other")

;; case (compile-time dispatch)
(case x
  1 "one"
  2 "two"
  "default")
```

### Nil Handling

```clojure
;; if-let (bind only if truthy)
(if-let [result (get {:a 1} :a)]
  (str "found: " result)
  "not found") ; => "found: 1"

;; when-let
(when-let [x (seq [1 2 3])]
  (first x)) ; => 1

;; some-> (thread-first, stop on nil)
(some-> {:a {:b 1}}
        :a
        :b
        inc) ; => 2

;; some->> (thread-last, stop on nil)
(some->> [1 2 3]
         (map inc)
         (filter even?)
         first) ; => 2

;; or (return first truthy value)
(or nil false 0 "result") ; => 0
```

---

## Threading Macros

```clojure
;; -> (thread-first)
(-> 5
    (+ 3)
    (* 2)
    (- 1)) ; => 15
;; Equivalent to: (- (* (+ 5 3) 2) 1)

;; ->> (thread-last)
(->> [1 2 3 4 5]
     (map inc)
     (filter even?)
     (reduce +)) ; => 12

;; as-> (thread with named argument)
(as-> 0 $
  (inc $)
  (+ 3 $)
  (* 2 $)) ; => 8

;; cond-> (conditional threading)
(cond-> []
  true (conj 1)
  (even? 2) (conj 2)
  false (conj 3)) ; => [1 2]

;; cond->> (conditional thread-last)
(cond->> [1 2 3]
  true (map inc)
  false (filter even?)) ; => (2 3 4)
```

---

## Namespaces and Requires

```clojure
;; Define namespace
(ns myapp.core
  "Application core namespace."
  (:require [clojure.string :as str]
            [clojure.set :as set]
            [myapp.util :refer [helper]]
            [myapp.config :refer :all]))

;; Refer specific functions
(:require [clojure.string :refer [upper-case lower-case]])

;; Import Java classes
(:import [java.util Date Calendar]
         [java.io File])

;; Using functions from required namespaces
(str/upper-case "hello") ; => "HELLO"
(set/union #{1 2} #{2 3}) ; => #{1 2 3}
```

---

## State Management

### Atoms

```clojure
;; Create atom
(def counter (atom 0))

;; Read value
@counter ; => 0

;; Update with swap!
(swap! counter inc) ; => 1
(swap! counter + 5) ; => 6

;; Set value with reset!
(reset! counter 0) ; => 0

;; Conditional update with compare-and-set!
(compare-and-set! counter 0 10) ; => true if current value is 0
```

### Refs (Coordinated, Synchronous)

```clojure
;; Create refs
(def account-a (ref 100))
(def account-b (ref 200))

;; Transaction with dosync
(dosync
  (alter account-a - 50)
  (alter account-b + 50))

;; Read consistent values
(dosync
  [@account-a @account-b]) ; => [50 250]

;; commute (optimistic update)
(dosync
  (commute account-a + 10))
```

### Agents (Asynchronous)

```clojure
;; Create agent
(def logger (agent []))

;; Send asynchronous update
(send logger conj "log entry 1")
(send logger conj "log entry 2")

;; Read value (may not be updated yet)
@logger

;; Wait for all actions to complete
(await logger)

;; send-off for blocking operations
(send-off logger
  (fn [logs]
    (Thread/sleep 1000)
    (conj logs "delayed entry")))
```

---

## Macros

### Using Macros

```clojure
;; Macros expand at compile time
;; Quote to prevent evaluation
'(+ 1 2) ; => (+ 1 2) (unevaluated list)

;; Common built-in macros
(when condition
  (do-thing-1)
  (do-thing-2))

(defn name [args] body) ; defn is a macro

(-> x f g h) ; threading macros are macros
```

### Defining Macros

```clojure
;; Simple macro
(defmacro unless [condition & body]
  `(if (not ~condition)
     (do ~@body)))

(unless false
  (println "This runs")
  "result") ; => "result"

;; Macro with syntax quote
(defmacro debug [expr]
  `(let [result# ~expr]
     (println '~expr "=>" result#)
     result#))

(debug (+ 1 2))
;; Prints: (+ 1 2) => 3
;; Returns: 3

;; Auto-gensym with #
(defmacro with-logging [& body]
  `(let [start# (System/currentTimeMillis)]
     (let [result# (do ~@body)]
       (println "Took" (- (System/currentTimeMillis) start#) "ms")
       result#)))
```

---

## Java Interop

```clojure
;; Create Java object
(new java.util.Date)
(java.util.Date.) ; Shorthand

;; Call instance method
(.toUpperCase "hello") ; => "HELLO"
(.substring "hello" 1 3) ; => "el"

;; Call static method
(Math/abs -5) ; => 5
(System/getProperty "java.version")

;; Access field
(.length "hello") ; => 5

;; Chain calls with ..
(.. "hello"
    (toUpperCase)
    (substring 0 3)) ; => "HEL"

;; doto (call multiple methods on same object)
(doto (java.util.HashMap.)
  (.put "a" 1)
  (.put "b" 2))
```

---

## REPL-Driven Development

### Workflow

```clojure
;; 1. Start REPL
;; lein repl or clj

;; 2. Load namespace
(require '[myapp.core :as core] :reload)

;; 3. Test function interactively
(core/my-function "test input")

;; 4. Inspect data
(pprint complex-data-structure)

;; 5. Check documentation
(doc map)
(source map)

;; 6. Find functions
(apropos "str")
(find-doc "sequence")

;; 7. Examine namespace
(dir clojure.string)
(ns-publics 'clojure.string)
```

### Common REPL Utilities

```clojure
;; Pretty print
(require '[clojure.pprint :refer [pprint]])
(pprint {:a 1 :b 2 :c {:d 3}})

;; Inspect Java classes
(require '[clojure.reflect :as r])
(r/reflect String)

;; Test assertions
(assert (= 4 (+ 2 2)))

;; Time execution
(time (reduce + (range 1000000)))
```

---

## Common Idioms

### Pipeline Processing

```clojure
;; Transform data through pipeline
(->> data
     (map parse-record)
     (filter valid?)
     (map transform)
     (group-by :category)
     (into (sorted-map)))
```

### Error Handling

```clojure
;; try/catch
(try
  (/ 1 0)
  (catch ArithmeticException e
    (println "Error:" (.getMessage e))
    nil)
  (finally
    (println "Cleanup")))

;; With custom exceptions
(try
  (when (invalid? data)
    (throw (ex-info "Invalid data"
                    {:data data :reason :validation})))
  (process data)
  (catch clojure.lang.ExceptionInfo e
    (let [{:keys [data reason]} (ex-data e)]
      (log/error "Failed:" reason))))
```

### Memoization

```clojure
;; Cache function results
(def fib
  (memoize
    (fn [n]
      (if (<= n 1)
        n
        (+ (fib (- n 1))
           (fib (- n 2)))))))

(fib 40) ; Fast after first call
```

### Transducers

```clojure
;; Composable algorithmic transformations
(def xf
  (comp
    (map inc)
    (filter even?)
    (take 5)))

;; Apply to different contexts
(sequence xf (range)) ; => (2 4 6 8 10)
(into [] xf (range))  ; => [2 4 6 8 10]
(transduce xf + (range)) ; => 30
```

---

## Troubleshooting

### Nil Pointer Exceptions

**Problem:** `NullPointerException` when calling methods

```clojure
(.toUpperCase nil) ; NullPointerException
```

**Fix:** Use nil-safe operations
```clojure
(some-> nil .toUpperCase) ; => nil
(when-let [s "hello"]
  (.toUpperCase s))
```

### Stack Overflow

**Problem:** Recursion without tail call optimization

```clojure
(defn sum [n]
  (if (zero? n)
    0
    (+ n (sum (dec n))))) ; Not tail recursive

(sum 10000) ; StackOverflowError
```

**Fix:** Use `recur` for tail recursion
```clojure
(defn sum [n]
  (loop [n n acc 0]
    (if (zero? n)
      acc
      (recur (dec n) (+ acc n)))))

;; Or use reduce
(defn sum [n]
  (reduce + (range (inc n))))
```

### Lazy Sequence Realization

**Problem:** Unexpected performance due to lazy evaluation

```clojure
;; This realizes the entire sequence multiple times
(let [nums (map expensive-fn (range 1000))]
  (+ (count nums) (first nums) (last nums)))
```

**Fix:** Force realization once with `doall` or `vec`
```clojure
(let [nums (vec (map expensive-fn (range 1000)))]
  (+ (count nums) (first nums) (last nums)))
```

### Keyword vs String Keys

**Problem:** Map lookup returns nil

```clojure
(get {"name" "Alice"} :name) ; => nil
```

**Fix:** Use consistent key types
```clojure
(get {:name "Alice"} :name) ; => "Alice"
;; Or convert
(keyword "name") ; => :name
```

---

## Serialization

Clojure provides multiple serialization options, from the native EDN format to JSON and Transit for interoperability. Validation is handled through `clojure.spec` and schema libraries.

### EDN (Extensible Data Notation)

```clojure
;; EDN is Clojure's native data format
(require '[clojure.edn :as edn])

;; Read EDN string
(edn/read-string "{:name \"Alice\" :age 30}")
;; => {:name "Alice" :age 30}

;; Read with custom readers
(edn/read-string {:readers {'inst #(java.time.Instant/parse %)}}
                 "#inst \"2024-01-15T10:30:00Z\"")

;; Write EDN
(pr-str {:name "Alice" :age 30})
;; => "{:name \"Alice\", :age 30}"

;; Read from file
(edn/read-string (slurp "config.edn"))
```

### JSON with Cheshire

```clojure
;; deps.edn: {:deps {cheshire/cheshire {:mvn/version "5.12.0"}}}
(require '[cheshire.core :as json])

;; Parse JSON
(json/parse-string "{\"name\": \"Alice\", \"age\": 30}" true)
;; => {:name "Alice" :age 30} (true = keywordize keys)

;; Generate JSON
(json/generate-string {:name "Alice" :age 30})
;; => "{\"name\":\"Alice\",\"age\":30}"

;; Pretty print
(json/generate-string {:name "Alice" :items [1 2 3]} {:pretty true})

;; Custom encoders
(json/generate-string
  {:timestamp (java.time.Instant/now)}
  {:encoders {java.time.Instant (fn [v gen] (.writeString gen (str v)))}})

;; Streaming for large files
(json/parse-stream (io/reader "large.json") true)
```

### Transit (High-Performance)

```clojure
;; deps.edn: {:deps {com.cognitect/transit-clj {:mvn/version "1.0.333"}}}
(require '[cognitect.transit :as transit])
(import '[java.io ByteArrayOutputStream ByteArrayInputStream])

;; Write Transit
(defn to-transit [data]
  (let [out (ByteArrayOutputStream.)]
    (transit/write (transit/writer out :json) data)
    (.toString out)))

(to-transit {:name "Alice" :keywords #{:a :b}})
;; Preserves Clojure types including keywords and sets

;; Read Transit
(defn from-transit [s]
  (transit/read (transit/reader (ByteArrayInputStream. (.getBytes s)) :json)))

;; Custom handlers for domain types
(defrecord User [id name])

(def write-handlers
  {User (transit/write-handler
          (constantly "user")
          (fn [u] [(:id u) (:name u)]))})
```

### Validation with clojure.spec

```clojure
(require '[clojure.spec.alpha :as s])

;; Define specs
(s/def ::name (s/and string? #(< 0 (count %) 100)))
(s/def ::email (s/and string? #(re-matches #".+@.+\..+" %)))
(s/def ::age (s/and int? #(< 0 % 150)))
(s/def ::user (s/keys :req-un [::name ::email]
                      :opt-un [::age]))

;; Validate
(s/valid? ::user {:name "Alice" :email "alice@example.com"})
;; => true

;; Explain failures
(s/explain ::user {:name "" :email "invalid"})
;; Prints detailed validation errors

;; Conform (parse + validate)
(s/def ::id-or-name (s/or :id int? :name string?))
(s/conform ::id-or-name 42) ; => [:id 42]

;; Validate function arguments
(defn create-user [{:keys [name email] :as user}]
  {:pre [(s/valid? ::user user)]}
  (assoc user :id (java.util.UUID/randomUUID)))

;; Generate test data
(require '[clojure.spec.gen.alpha :as gen])
(gen/sample (s/gen ::name) 5)
```

### See Also

- `patterns-serialization-dev` - Cross-language serialization patterns

---

## Build and Dependencies

Clojure has two primary build ecosystems: Leiningen (the traditional choice) and tools.deps/CLI (the modern Clojure CLI).

### Leiningen (project.clj)

```clojure
;; project.clj
(defproject myapp "0.1.0-SNAPSHOT"
  :description "My Clojure application"
  :url "https://github.com/user/myapp"
  :license {:name "EPL-2.0"}

  ;; Dependencies
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [cheshire "5.12.0"]
                 [ring/ring-core "1.10.0"]]

  ;; Development dependencies
  :profiles {:dev {:dependencies [[midje "1.10.9"]]
                   :plugins [[lein-midje "3.2.1"]]}}

  ;; Entry point
  :main myapp.core
  :aot [myapp.core]

  ;; Resources
  :resource-paths ["resources"]
  :source-paths ["src"]
  :test-paths ["test"]

  ;; REPL configuration
  :repl-options {:init-ns myapp.core})
```

```bash
# Common Leiningen commands
lein new app myapp          # Create new project
lein deps                   # Download dependencies
lein repl                   # Start REPL
lein run                    # Run main function
lein test                   # Run tests
lein uberjar                # Build standalone JAR
lein install                # Install to local Maven repo
lein deploy clojars         # Publish to Clojars
```

### tools.deps (deps.edn)

```clojure
;; deps.edn
{:paths ["src" "resources"]

 :deps {org.clojure/clojure {:mvn/version "1.11.1"}
        cheshire/cheshire {:mvn/version "5.12.0"}
        ring/ring-core {:mvn/version "1.10.0"}}

 :aliases
 {:dev {:extra-paths ["dev"]
        :extra-deps {nrepl/nrepl {:mvn/version "1.0.0"}}}

  :test {:extra-paths ["test"]
         :extra-deps {io.github.cognitect-labs/test-runner
                      {:git/tag "v0.5.1" :git/sha "dfb30dd"}}}

  :build {:deps {io.github.clojure/tools.build {:mvn/version "0.9.4"}}
          :ns-default build}

  :outdated {:deps {com.github.liquidz/antq {:mvn/version "2.5.1109"}}
             :main-opts ["-m" "antq.core"]}}}
```

```bash
# Common CLI commands
clj                         # Start REPL
clj -X:test                 # Run tests
clj -M:dev -m myapp.core    # Run with alias
clj -A:dev:test             # Combine aliases
clj -Sdeps '{:deps {...}}'  # Add deps inline
clj -T:build uber           # Build uberjar
```

### Dependency Sources

```clojure
;; Maven (Clojars, Maven Central)
{:deps {ring/ring-core {:mvn/version "1.10.0"}}}

;; Git dependency
{:deps {io.github.user/lib {:git/tag "v1.0.0" :git/sha "abc123"}}}

;; Local project
{:deps {mylib {:local/root "../mylib"}}}

;; Git with specific path
{:deps {lib {:git/url "https://github.com/user/monorepo"
             :git/sha "abc123"
             :deps/root "libs/mylib"}}}
```

### Build Script (tools.build)

```clojure
;; build.clj
(ns build
  (:require [clojure.tools.build.api :as b]))

(def lib 'myapp/myapp)
(def version "0.1.0")
(def class-dir "target/classes")
(def basis (b/create-basis {:project "deps.edn"}))
(def jar-file (format "target/%s-%s.jar" (name lib) version))
(def uber-file (format "target/%s-%s-standalone.jar" (name lib) version))

(defn clean [_]
  (b/delete {:path "target"}))

(defn jar [_]
  (b/write-pom {:class-dir class-dir :lib lib :version version :basis basis})
  (b/copy-dir {:src-dirs ["src" "resources"] :target-dir class-dir})
  (b/jar {:class-dir class-dir :jar-file jar-file}))

(defn uber [_]
  (clean nil)
  (b/copy-dir {:src-dirs ["src" "resources"] :target-dir class-dir})
  (b/compile-clj {:basis basis :src-dirs ["src"] :class-dir class-dir})
  (b/uber {:class-dir class-dir :uber-file uber-file :basis basis
           :main 'myapp.core}))
```

### Publishing to Clojars

```clojure
;; deps.edn alias for deployment
{:aliases
 {:deploy {:deps {slipset/deps-deploy {:mvn/version "0.2.1"}}
           :exec-fn deps-deploy.deps-deploy/deploy
           :exec-args {:installer :remote :artifact "target/myapp.jar"}}}}

;; Or in project.clj
{:deploy-repositories [["clojars" {:url "https://repo.clojars.org"
                                   :username :env/CLOJARS_USERNAME
                                   :password :env/CLOJARS_TOKEN}]]}
```

---

## Testing

Clojure's testing ecosystem includes the built-in `clojure.test`, property-based testing with `test.check`, and BDD-style testing with Midje.

### clojure.test (Built-in)

```clojure
(ns myapp.core-test
  (:require [clojure.test :refer [deftest testing is are]]
            [myapp.core :as core]))

;; Basic test
(deftest add-test
  (is (= 4 (core/add 2 2)))
  (is (= 0 (core/add -1 1))))

;; Grouped assertions with testing
(deftest user-validation-test
  (testing "valid users"
    (is (core/valid-user? {:name "Alice" :email "a@b.com"}))
    (is (core/valid-user? {:name "Bob" :email "b@c.org"})))

  (testing "invalid users"
    (is (not (core/valid-user? {:name "" :email "a@b.com"})))
    (is (not (core/valid-user? {:name "Alice" :email "invalid"})))))

;; Table-driven tests with are
(deftest arithmetic-test
  (are [x y expected] (= expected (core/add x y))
    1 1 2
    2 3 5
    -1 1 0
    0 0 0))

;; Testing exceptions
(deftest divide-test
  (is (thrown? ArithmeticException (core/divide 1 0)))
  (is (thrown-with-msg? Exception #"cannot be zero"
        (core/safe-divide 1 0))))

;; Fixtures for setup/teardown
(use-fixtures :once
  (fn [f]
    (println "Starting test suite")
    (f)
    (println "Test suite complete")))

(use-fixtures :each
  (fn [f]
    (reset! core/db {})  ; Clean state
    (f)))
```

### test.check (Property-Based)

```clojure
;; deps.edn: {:deps {org.clojure/test.check {:mvn/version "1.1.1"}}}
(ns myapp.props-test
  (:require [clojure.test :refer [deftest is]]
            [clojure.test.check :as tc]
            [clojure.test.check.generators :as gen]
            [clojure.test.check.properties :as prop]
            [clojure.test.check.clojure-test :refer [defspec]]))

;; Property: reverse is its own inverse
(defspec reverse-involutive 100
  (prop/for-all [v (gen/vector gen/small-integer)]
    (= v (vec (reverse (reverse v))))))

;; Property: sorted output
(defspec sort-produces-sorted 100
  (prop/for-all [v (gen/vector gen/small-integer)]
    (let [sorted (sort v)]
      (every? (fn [[a b]] (<= a b))
              (partition 2 1 sorted)))))

;; Custom generator
(def user-gen
  (gen/hash-map
    :id gen/uuid
    :name (gen/not-empty gen/string-alphanumeric)
    :age (gen/choose 18 100)
    :email (gen/fmap #(str % "@example.com")
                     gen/string-alphanumeric)))

(defspec user-roundtrip 50
  (prop/for-all [user user-gen]
    (= user (core/parse-user (core/serialize-user user)))))

;; Manual property check
(tc/quick-check 100
  (prop/for-all [n gen/nat]
    (= n (core/identity-fn n))))
```

### Midje (BDD-Style)

```clojure
;; deps.edn: {:deps {midje/midje {:mvn/version "1.10.9"}}}
(ns myapp.core-test
  (:require [midje.sweet :refer :all]
            [myapp.core :as core]))

;; Facts with arrows
(fact "addition works correctly"
  (core/add 2 2) => 4
  (core/add -1 1) => 0)

;; Tabular facts
(tabular
  (fact "multiplication table"
    (core/multiply ?x ?y) => ?result)
  ?x ?y ?result
  1  1  1
  2  3  6
  0  5  0)

;; Checking predicates
(fact "string processing"
  (core/process "hello") => string?
  (core/process "hello") => #(> (count %) 0))

;; Mocking/stubbing
(fact "external API calls"
  (core/fetch-user 123) => {:id 123 :name "Alice"}
  (provided
    (core/http-get "https://api.example.com/users/123")
      => {:status 200 :body "{\"id\":123,\"name\":\"Alice\"}"}))

;; Checking exceptions
(fact "division by zero throws"
  (core/divide 1 0) => (throws ArithmeticException))

;; Prerequisites
(against-background
  [(core/get-config) => {:db-url "test://db"}]
  (fact "uses test config"
    (core/db-url) => "test://db"))
```

### Running Tests

```bash
# Leiningen
lein test                   # Run all tests
lein test myapp.core-test   # Run specific namespace
lein test :only myapp.core-test/add-test  # Run single test
lein midje                  # Run Midje tests

# tools.deps with test-runner
clj -X:test                 # Run all tests
clj -X:test :nses '[myapp.core-test]'  # Specific namespace

# REPL
(require '[clojure.test :refer [run-tests]])
(run-tests 'myapp.core-test)
```

### Test Organization

```
myapp/
├── src/
│   └── myapp/
│       └── core.clj
├── test/
│   └── myapp/
│       ├── core_test.clj       ; Unit tests
│       ├── integration_test.clj ; Integration tests
│       └── props_test.clj      ; Property tests
├── dev/
│   └── user.clj                ; REPL utilities
└── deps.edn
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Async/await, channels, threads
- `patterns-serialization-dev` - JSON, validation, struct tags
- `patterns-metaprogramming-dev` - Decorators, macros, annotations

---

## References

- [Clojure Documentation](https://clojure.org/reference/documentation)
- [ClojureDocs](https://clojuredocs.org/)
- [Clojure Style Guide](https://guide.clojure.style/)
- [Clojure Koans](http://clojurekoans.com/)
- [4Clojure Problems](http://www.4clojure.com/)
