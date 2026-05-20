---
name: convert-roc-clojure
description: Convert Roc code to idiomatic Clojure. Use when migrating Roc projects to Clojure, translating Roc patterns to idiomatic Clojure, or refactoring Roc codebases into Clojure. Extends meta-convert-dev with Roc-to-Clojure specific patterns.
---

# Convert Roc to Clojure

Convert Roc code to idiomatic Clojure. This skill extends `meta-convert-dev` with Roc-to-Clojure specific type mappings, idiom translations, and tooling.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Roc types → Clojure data structures
- **Idiom translations**: Roc patterns → idiomatic Clojure
- **Error handling**: Roc Result → Clojure error patterns
- **Platform model**: Roc platform/app → Clojure architecture
- **Evaluation**: Roc eager → Clojure lazy sequences
- **REPL workflow**: Static compilation → REPL-driven development

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Clojure language fundamentals - see `lang-clojure-dev`
- Reverse conversion (Clojure → Roc) - see `convert-clojure-roc`

---

## Quick Reference

| Roc | Clojure | Notes |
|-----|---------|-------|
| `{ name : Str }` | `{:name "..."}` | Records → maps with keyword keys |
| `[Ok a, Err e]` | `try/catch` or custom | Result → exceptions or Either pattern |
| `when x is` | `case` or `cond` | Pattern matching → conditionals |
| `List.map` | `map` | Direct mapping |
| `Task a err` | Function returning data | Effects → imperative code |
| `U32`, `I64` | `long`, `int` | Explicit types → dynamic typing |
| `Str` | `String` | Direct mapping |
| Abilities | Protocols/Multimethods | Trait-like → polymorphism |

---

## When Converting Code

1. **Analyze platform boundaries** - Identify pure logic vs I/O
2. **Map types to data** - Roc's static types become runtime data
3. **Embrace dynamism** - Remove type annotations, trust runtime
4. **Adopt REPL workflow** - Replace test-driven with REPL-driven
5. **Handle nullability** - Roc's Option → nil or explicit checks
6. **Rethink concurrency** - Tasks → core.async or JVM threads

---

## Type System Mapping

### Primitive Types

| Roc | Clojure | Notes |
|-----|---------|-------|
| `U8`, `U16`, `U32`, `U64` | `Long` | All integers unify to JVM types |
| `I8`, `I16`, `I32`, `I64` | `Long` | Signed/unsigned distinction lost |
| `F32`, `F64` | `Double` | Floats become doubles |
| `Str` | `String` | Direct mapping |
| `Bool` | `Boolean` | `true`/`false` (lowercase) |
| `()` (unit) | `nil` | Unit type → nil |

**Key differences:**
- Roc has sized integers, Clojure uses JVM's `Long` (64-bit)
- Overflow behavior: Roc panics, Clojure promotes to BigInt
- Use `unchecked-*` operations if performance critical

### Collection Types

| Roc | Clojure | Notes |
|-----|---------|-------|
| `List a` | `(list ...)` or `[...]` | Lists or vectors |
| `[a, b, c]` (tuple) | `[a b c]` | Tuples → vectors |
| `Dict k v` | `{k v ...}` | Maps with any key type |
| `Set a` | `#{...}` | Direct mapping |
| Array types | `(vector ...)` | Mutable → persistent vectors |

**Considerations:**
- Roc Lists are singly-linked, Clojure lists are too
- Prefer Clojure vectors `[...]` for indexed access
- Roc Dicts require `Hash + Eq`, Clojure maps use `hash` + `=`

### Record Types

| Roc | Clojure | Notes |
|-----|---------|-------|
| `{ name : Str, age : U32 }` | `{:name "..." :age 30}` | Records → maps with keyword keys |
| `{ user & age : 31 }` | `(assoc user :age 31)` | Record update → `assoc` |
| Field access | `(:field map)` or `(get map :field)` | Keyword or `get` function |
| Optional fields | `nil` or explicit check | No built-in Option type |

**Pattern:**

```roc
// Roc
user = { name: "Alice", age: 30 }
older = { user & age: 31 }
```

```clojure
;; Clojure
(def user {:name "Alice" :age 30})
(def older (assoc user :age 31))
```

### Tag Unions (Sum Types)

Roc's tag unions have no direct Clojure equivalent. Use tagged maps or protocols.

| Roc Pattern | Clojure Approach | Notes |
|-------------|------------------|-------|
| `[Red, Green, Blue]` | `#{:red :green :blue}` (keywords) | Simple enums → keyword sets |
| `[Ok a, Err e]` | `try/catch` or `{:type :ok :value a}` | Result → exceptions or tagged maps |
| `[Some a, None]` | `nil` or explicit value | Option → nil convention |
| Nested tags | Protocols or multimethod | Complex sum types need abstraction |

**Example - Result Type:**

```roc
// Roc
divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

when divide(10, 2) is
    Ok(result) -> Num.toStr(result)
    Err(DivByZero) -> "Cannot divide by zero"
```

**Option 1: Exceptions (idiomatic for errors)**

```clojure
;; Clojure - exception style
(defn divide [a b]
  (if (zero? b)
    (throw (ex-info "Division by zero" {:a a :b b}))
    (quot a b)))

(try
  (str (divide 10 2))
  (catch clojure.lang.ExceptionInfo e
    "Cannot divide by zero"))
```

**Option 2: Tagged maps (functional style)**

```clojure
;; Clojure - Either pattern
(defn divide [a b]
  (if (zero? b)
    {:type :error :reason :div-by-zero}
    {:type :ok :value (quot a b)}))

(let [result (divide 10 2)]
  (case (:type result)
    :ok (str (:value result))
    :error "Cannot divide by zero"))
```

### Abilities → Protocols

| Roc | Clojure | Notes |
|-----|---------|-------|
| `where a implements Eq` | No equivalent | Dynamic typing, everything comparable |
| `where a implements Hash` | Automatic via `hash` | Built-in hashing |
| `where a implements Inspect` | `pr-str`, `prn` | Built-in printing |
| Custom abilities | `defprotocol` + `extend-type` | Protocol-oriented design |

**Example:**

```roc
// Roc
toString : a -> Str where a implements Inspect
toString = \value -> Inspect.toStr(value)
```

```clojure
;; Clojure
(defn to-string [value]
  (pr-str value))  ; Works for any value
```

For custom behavior:

```clojure
;; Define protocol
(defprotocol Stringable
  (to-string [this]))

;; Implement for types
(extend-type User
  Stringable
  (to-string [user]
    (format "%s <%s>" (:name user) (:email user))))
```

---

## Idiom Translation

### Pattern: Functional Pipelines

**Roc:**
```roc
numbers = [1, 2, 3, 4, 5]
result = numbers
    |> List.map(\n -> n * 2)
    |> List.keepIf(\n -> n > 5)
    |> List.walk(0, Num.add)
```

**Clojure:**
```clojure
(def numbers [1 2 3 4 5])
(def result
  (->> numbers
       (map #(* % 2))
       (filter #(> % 5))
       (reduce +)))
```

**Why this translation:**
- Roc's `|>` → Clojure's `->>` (thread-last macro)
- `List.keepIf` → `filter`
- `List.walk` → `reduce`
- Anonymous functions: `\n ->` → `#(...)` or `(fn [n] ...)`

### Pattern: Record Updates

**Roc:**
```roc
user = { name: "Alice", age: 30, email: "alice@example.com" }

updated = { user &
    age: 31,
    email: "alice@newdomain.com"
}

nested = {
    user: { name: "Alice", address: { city: "NYC" } }
}

movedUser = { nested &
    user: { nested.user & address: { city: "SF" } }
}
```

**Clojure:**
```clojure
(def user {:name "Alice" :age 30 :email "alice@example.com"})

(def updated
  (assoc user
         :age 31
         :email "alice@newdomain.com"))

(def nested
  {:user {:name "Alice" :address {:city "NYC"}}})

(def moved-user
  (assoc-in nested [:user :address :city] "SF"))
```

**Why this translation:**
- `assoc` for shallow updates
- `assoc-in` for nested path updates
- Immutability preserved in both

### Pattern: Pattern Matching

**Roc:**
```roc
when expr is
    Num(n) -> n
    Add(left, right) -> eval(left) + eval(right)
    Multiply(left, right) -> eval(left) * eval(right)
```

**Clojure:**
```clojure
;; Option 1: case with keywords
(case (:type expr)
  :num (:value expr)
  :add (+ (eval-expr (:left expr)) (eval-expr (:right expr)))
  :multiply (* (eval-expr (:left expr)) (eval-expr (:right expr))))

;; Option 2: multimethods (more flexible)
(defmulti eval-expr :type)

(defmethod eval-expr :num [expr]
  (:value expr))

(defmethod eval-expr :add [expr]
  (+ (eval-expr (:left expr)) (eval-expr (:right expr))))

(defmethod eval-expr :multiply [expr]
  (* (eval-expr (:left expr)) (eval-expr (:right expr))))

;; Option 3: core.match (library)
(require '[clojure.core.match :refer [match]])

(match expr
  {:type :num :value n} n
  {:type :add :left l :right r} (+ (eval-expr l) (eval-expr r))
  {:type :multiply :left l :right r} (* (eval-expr l) (eval-expr r)))
```

**Why this translation:**
- Roc's exhaustive pattern matching → Clojure dispatch mechanisms
- Use `case` for simple discriminators
- Use multimethods for extensible polymorphism
- Use `core.match` library for rich pattern matching

### Pattern: Option/Maybe Type

**Roc:**
```roc
findUser : U64 -> [Some User, None]
findUser = \id ->
    if found then
        Some(user)
    else
        None

when findUser(1) is
    Some(user) -> "Found: \(user.name)"
    None -> "Not found"
```

**Clojure:**
```clojure
(defn find-user [id]
  (if-let [user (get-user-from-db id)]
    user
    nil))

;; Using result
(if-let [user (find-user 1)]
  (str "Found: " (:name user))
  "Not found")

;; Or with explicit checks
(let [user (find-user 1)]
  (if (some? user)
    (str "Found: " (:name user))
    "Not found"))
```

**Why this translation:**
- Roc's `None` → Clojure's `nil`
- Use `if-let` for nil checks with binding
- Use `some?` and `nil?` predicates
- Clojure embraces nil as "no value"

### Pattern: Opaque Types

**Roc:**
```roc
UserId := U64

fromU64 : U64 -> UserId
fromU64 = \id -> @UserId(id)

toU64 : UserId -> U64
toU64 = \@UserId(id) -> id
```

**Clojure:**
```clojure
;; Option 1: No wrapping (rely on discipline)
(defn user-id [id] id)

;; Option 2: Tagged map
(defn user-id [id]
  {:type ::user-id :value id})

(defn user-id-value [user-id]
  (:value user-id))

;; Option 3: deftype (Java interop)
(deftype UserId [id]
  Object
  (toString [_] (str "UserId(" id ")")))

(defn user-id [id]
  (->UserId id))

(defn user-id-value [^UserId user-id]
  (.id user-id))

;; Option 4: clojure.spec for validation
(require '[clojure.spec.alpha :as s])

(s/def ::user-id (s/and int? pos?))

(defn user-id [id]
  {:pre [(s/valid? ::user-id id)]}
  id)
```

**Why this translation:**
- Roc enforces opacity at compile time
- Clojure relies on conventions or runtime checks
- Choose based on strictness needs
- Spec adds runtime validation without wrapper types

---

## Error Handling

### Roc Result → Clojure Exceptions

Roc uses `Result a e` for recoverable errors. Clojure typically uses exceptions.

**Roc:**
```roc
parseConfig : Str -> Result Config [ParseError Str, FileNotFound]
parseConfig = \path ->
    content = File.readUtf8!(path) |> Result.mapErr(\_ -> FileNotFound)
    Str.toJson!(content) |> Result.mapErr(\e -> ParseError(e))
```

**Clojure (exception-based):**
```clojure
(defn parse-config [path]
  (try
    (-> path
        slurp
        json/parse-string)
    (catch java.io.FileNotFoundException e
      (throw (ex-info "Config file not found" {:path path} e)))
    (catch Exception e
      (throw (ex-info "Failed to parse config" {:path path} e)))))

;; Usage
(try
  (parse-config "config.json")
  (catch clojure.lang.ExceptionInfo e
    (case (:type (ex-data e))
      :file-not-found (println "File not found")
      :parse-error (println "Parse failed"))))
```

**Clojure (functional Either pattern):**
```clojure
(defn parse-config [path]
  (try
    {:type :ok :value (-> path slurp json/parse-string)}
    (catch java.io.FileNotFoundException e
      {:type :error :reason :file-not-found :path path})
    (catch Exception e
      {:type :error :reason :parse-error :message (.getMessage e)})))

;; Usage
(let [result (parse-config "config.json")]
  (case (:type result)
    :ok (:value result)
    :error (println "Error:" (:reason result))))
```

**Decision tree:**

```
Is the error expected/recoverable?
├─ YES, common case → Either pattern (tagged maps)
└─ NO, exceptional → throw exceptions

Is error handling central to the API?
├─ YES → Either pattern for composability
└─ NO → Exceptions for simplicity
```

### Roc Try Operator → Clojure Chaining

**Roc:**
```roc
calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)  # Early return on Err
    y = divide!(x, c)  # Early return on Err
    Ok(y)
```

**Clojure (exception chaining):**
```clojure
(defn calculate [a b c]
  (let [x (divide a b)
        y (divide x c)]
    y))
;; Exceptions propagate automatically
```

**Clojure (Either pattern with threading):**
```clojure
(defn bind-either [result f]
  (if (= :ok (:type result))
    (f (:value result))
    result))

(defn calculate [a b c]
  (bind-either (divide a b)
    (fn [x]
      (bind-either (divide x c)
        (fn [y]
          {:type :ok :value y})))))

;; Or with a macro for cleaner syntax
(defmacro either-> [value & forms]
  (reduce (fn [v form]
            `(bind-either ~v (fn [~'%] ~form)))
          value forms))

(defn calculate [a b c]
  (either-> (divide a b)
    (divide % c)))
```

---

## Platform Model Translation

### Roc Platform/Application → Clojure Architecture

Roc strictly separates pure application code from effectful platform code. Clojure doesn't enforce this separation.

**Roc architecture:**
```
┌─────────────────────────────┐
│     Application (Pure)      │
│   • Business logic          │
│   • Data transformations    │
│   • No direct I/O           │
└─────────────┬───────────────┘
              │ Task interface
┌─────────────▼───────────────┐
│    Platform (Effects)       │
│   • File I/O                │
│   • Network                 │
│   • Console                 │
└─────────────────────────────┘
```

**Roc:**
```roc
app [main] { pf: platform "..." }

import pf.Stdout
import pf.File
import pf.Task exposing [Task]

main : Task {} []
main =
    content = File.readUtf8!("input.txt")
    processed = String.toUpper(content)  # Pure
    File.writeUtf8!("output.txt", processed)
    Stdout.line!("Done!")
```

**Clojure equivalent (no separation enforced):**
```clojure
(ns myapp.core
  (:require [clojure.java.io :as io]
            [clojure.string :as str]))

(defn -main [& args]
  (let [content (slurp "input.txt")
        processed (str/upper-case content)]  ; Pure
    (spit "output.txt" processed)
    (println "Done!")))
```

**Best practice - manual separation:**

```clojure
;; Pure core logic
(ns myapp.core)

(defn process-content [content]
  (str/upper-case content))

;; Effects layer
(ns myapp.main
  (:require [myapp.core :as core]
            [clojure.java.io :as io]))

(defn read-file [path]
  (slurp path))

(defn write-file [path content]
  (spit path content))

(defn -main [& args]
  (let [content (read-file "input.txt")
        processed (core/process-content content)]
    (write-file "output.txt" processed)
    (println "Done!")))
```

**Why this pattern:**
- Separates testable pure code from I/O
- Makes dependencies explicit
- Easier to test and reason about
- Mimics Roc's architecture voluntarily

### Task-Based Effects → Imperative Code

**Roc:**
```roc
fetchAndProcess : Str -> Task Result [HttpErr]
fetchAndProcess = \url ->
    response = Http.get!(url)
    parsed = Json.decode!(response.body)
    processed = transform(parsed)  # Pure
    Task.ok(processed)
```

**Clojure:**
```clojure
(defn fetch-and-process [url]
  (let [response (http/get url)
        parsed (json/parse-string (:body response) true)
        processed (transform parsed)]
    processed))
```

**With error handling:**
```clojure
(defn fetch-and-process [url]
  (try
    (let [response (http/get url)
          parsed (json/parse-string (:body response) true)
          processed (transform parsed)]
      {:type :ok :value processed})
    (catch Exception e
      {:type :error :reason :http-error :message (.getMessage e)})))
```

---

## Evaluation Strategy Translation

### Roc Eager → Clojure Lazy Sequences

Roc evaluates eagerly by default. Clojure sequence operations are often lazy.

**Roc:**
```roc
# All evaluated immediately
numbers = List.range(0, 1000000)
doubled = List.map(numbers, \n -> n * 2)
filtered = List.keepIf(doubled, \n -> n > 100)
```

**Clojure (lazy by default):**
```clojure
;; Lazy - only realized when consumed
(def numbers (range 1000000))
(def doubled (map #(* % 2) numbers))
(def filtered (filter #(> % 100) doubled))

;; Force evaluation
(def realized (vec filtered))  ; Realizes entire sequence

;; Or realize partially
(take 10 filtered)  ; Only realizes first 10
```

**Key differences:**

| Aspect | Roc | Clojure |
|--------|-----|---------|
| Default | Eager | Lazy (sequences) |
| Infinite sequences | Not possible | Common pattern |
| Memory | Predictable | Can cause space leaks if not careful |
| Side effects in map | Execute immediately | Deferred! |

**Watch out for:**

```clojure
;; BAD - side effects in lazy sequence
(map #(println %) (range 10))  ; Doesn't print!

;; GOOD - realize with doall or doseq
(doall (map #(println %) (range 10)))
(doseq [x (range 10)] (println x))

;; BAD - holding head of lazy sequence
(let [nums (map expensive-fn (range 1000000))]
  (+ (first nums) (last nums)))  ; Entire seq in memory!

;; GOOD - realize once
(let [nums (vec (map expensive-fn (range 1000000)))]
  (+ (first nums) (last nums)))
```

---

## REPL-Driven Development

### Compilation → Interactive Development

Roc is compiled (fast iteration with `roc dev`). Clojure is REPL-driven (instant feedback).

**Roc workflow:**
```bash
# 1. Write code
# 2. Compile and run
roc dev main.roc

# 3. See output
# 4. Edit code
# 5. Recompile (fast)
```

**Clojure workflow:**
```bash
# 1. Start REPL
clj

# 2. Load namespace
(require '[myapp.core :as core] :reload)

# 3. Test function interactively
(core/my-function "test")

# 4. Inspect results
(def result (core/process data))
(clojure.pprint/pprint result)

# 5. Modify function in editor
# 6. Reload namespace (instant)
(require '[myapp.core :as core] :reload)

# 7. Test again (no compilation step)
(core/my-function "test")
```

**Migration strategy:**

```
Roc's test-driven → Clojure's REPL-driven

1. Instead of writing tests first:
   - Load code in REPL
   - Try functions with sample data
   - Iterate rapidly

2. After exploration:
   - Codify behavior as tests
   - Use property-based testing

3. Development loop:
   - Edit code
   - Reload in REPL (instant)
   - Test manually
   - Write tests
   - Repeat
```

**Example - exploring data:**

```clojure
;; REPL session
user=> (def data (slurp "data.json"))
user=> (def parsed (json/parse-string data true))
user=> (keys parsed)
(:users :posts :comments)

user=> (count (:users parsed))
42

user=> (take 2 (:users parsed))
({:name "Alice" :id 1} {:name "Bob" :id 2})

;; Now write the function based on exploration
(defn get-user-names [data]
  (->> (json/parse-string data true)
       :users
       (map :name)))
```

---

## Concurrency Patterns

### Roc Tasks → Clojure Concurrency

Roc's concurrency is platform-specific (Tasks). Clojure has multiple models.

**Roc (platform-provided):**
```roc
# Platform may provide parallel execution
fetchMultiple : List Str -> Task (List Str) [HttpErr]
fetchMultiple = \urls ->
    urls
    |> List.map(Http.get)
    |> Task.sequence  # Platform decides parallelism
```

**Clojure options:**

**1. JVM Threads (simple parallelism):**
```clojure
(defn fetch-multiple [urls]
  (->> urls
       (pmap http/get)  ; Parallel map (uses thread pool)
       (map :body)))
```

**2. core.async (CSP-style):**
```clojure
(require '[clojure.core.async :as async])

(defn fetch-multiple [urls]
  (let [ch (async/chan)
        results (atom [])]
    (doseq [url urls]
      (async/go
        (let [response (async/<! (http/async-get url))]
          (async/>! ch (:body response)))))
    (async/<!! (async/into [] (async/take (count urls) ch)))))
```

**3. Agents (asynchronous updates):**
```clojure
(def results (agent []))

(defn fetch-and-collect [url]
  (send results conj (:body (http/get url))))

(doseq [url urls]
  (fetch-and-collect url))

(await results)
@results
```

**4. Futures (simple async):**
```clojure
(defn fetch-multiple [urls]
  (let [futures (mapv #(future (http/get %)) urls)]
    (mapv #(:body (deref %)) futures)))
```

**Choose based on:**
- `pmap` - Simple data parallelism
- `future` - Fire-and-forget async tasks
- Agents - Asynchronous state updates
- core.async - Complex coordination, CSP patterns

---

## Common Gotchas

### 1. Nil vs None

**Roc:**
```roc
# Explicit Option type
maybeUser : [Some User, None]
maybeUser = None

# Compiler forces handling
when maybeUser is
    Some(user) -> use(user)
    None -> default
```

**Clojure:**
```clojure
;; nil is used for "no value"
(def maybe-user nil)

;; Easy to forget nil checks
(str/upper-case (:name maybe-user))  ; NullPointerException!

;; Must check explicitly
(when maybe-user
  (str/upper-case (:name maybe-user)))

;; Or use safe navigation
(some-> maybe-user :name str/upper-case)
```

**Mitigation:** Use `some?`, `nil?`, `if-let`, `when-let`, and `some->` liberally.

### 2. Lazy Evaluation Side Effects

**Roc:**
```roc
# Eager - side effects happen immediately
List.map(users, \user -> log(user.name))
```

**Clojure:**
```clojure
;; Lazy - side effects might not happen!
(map #(println (:name %)) users)  ; Returns lazy seq, doesn't print

;; Force realization
(doall (map #(println (:name %)) users))

;; Better: use doseq for side effects
(doseq [user users]
  (println (:name user)))
```

### 3. Integer Overflow

**Roc:**
```roc
# Overflow panics
x : I32
x = 2147483647 + 1  # Runtime error
```

**Clojure:**
```clojure
;; Auto-promotes to BigInt
(def x (+ 2147483647 1))  ; => 2147483648N

;; Unchecked operations for performance
(unchecked-add 2147483647 1)  ; Wraps around

;; Explicit overflow checking
(defn safe-add [a b]
  (try
    (Math/addExact a b)
    (catch ArithmeticException e
      {:type :error :reason :overflow})))
```

### 4. Keyword vs String Keys

**Roc:**
```roc
# Type enforces consistency
user : { name : Str }
user = { name: "Alice" }
```

**Clojure:**
```clojure
;; Both possible, easy to mix
(def user-keywords {:name "Alice"})
(def user-strings {"name" "Alice"})

(get user-keywords :name)   ; => "Alice"
(get user-strings :name)    ; => nil (wrong key type!)

;; Be consistent
;; Prefer keywords for internal keys
;; Use strings only for external data (JSON keys)
```

### 5. Destructuring Nil

**Roc:**
```roc
# Compiler prevents this
when maybeUser is
    Some({ name, age }) -> process(name, age)
    None -> default
```

**Clojure:**
```clojure
;; Destructuring nil throws
(let [{:keys [name age]} nil]  ; NullPointerException
  (str name))

;; Check first
(when-let [{:keys [name age]} maybe-user]
  (str name))

;; Or provide defaults
(let [{:keys [name age] :or {name "Unknown" age 0}} maybe-user]
  (str name))
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| Leiningen | Build tool, dependency management | Traditional choice |
| Clojure CLI | Modern build, deps.edn | Official tooling |
| REPL | Interactive development | Core workflow |
| CIDER | Emacs integration | Industry standard |
| Cursive | IntelliJ plugin | Full IDE support |
| Calva | VS Code plugin | Modern editor support |
| clj-kondo | Linter | Catches common errors |
| clojure.test | Testing framework | Built-in |
| test.check | Property-based testing | QuickCheck-style |
| Midje | BDD testing | Alternative to clojure.test |

---

## Examples

### Example 1: Simple - Data Transformation

**Before (Roc):**
```roc
# Transform user data
processUser : { name : Str, age : U32 } -> { name : Str, ageGroup : Str }
processUser = \user ->
    ageGroup = if user.age < 18 then "minor" else "adult"
    { name: user.name, ageGroup }

users = [
    { name: "Alice", age: 30 },
    { name: "Bob", age: 15 },
]

processed = List.map(users, processUser)
```

**After (Clojure):**
```clojure
;; Transform user data
(defn process-user [user]
  (let [age-group (if (< (:age user) 18) "minor" "adult")]
    {:name (:name user) :age-group age-group}))

(def users
  [{:name "Alice" :age 30}
   {:name "Bob" :age 15}])

(def processed
  (map process-user users))
```

### Example 2: Medium - Error Handling

**Before (Roc):**
```roc
# Parse and validate JSON config
parseConfig : Str -> Result Config [FileErr, ParseErr, ValidationErr]
parseConfig = \path ->
    content = File.readUtf8!(path)
        |> Result.mapErr(\_ -> FileErr("Could not read file"))

    parsed = Json.decode!(content)
        |> Result.mapErr(\e -> ParseErr(e))

    validated = validate!(parsed)
        |> Result.mapErr(\e -> ValidationErr(e))

    Ok(validated)

# Usage
when parseConfig("config.json") is
    Ok(config) ->
        Stdout.line!("Loaded: \(config.name)")
    Err(FileErr(msg)) ->
        Stderr.line!("File error: \(msg)")
    Err(ParseErr(msg)) ->
        Stderr.line!("Parse error: \(msg)")
    Err(ValidationErr(msg)) ->
        Stderr.line!("Validation error: \(msg)")
```

**After (Clojure):**
```clojure
;; Parse and validate JSON config
(defn parse-config [path]
  (try
    (let [content (slurp path)
          parsed (json/parse-string content true)
          validated (validate parsed)]
      {:type :ok :value validated})
    (catch java.io.IOException e
      {:type :error :kind :file-error :message (.getMessage e)})
    (catch Exception e
      (if (= :parse-error (:type (ex-data e)))
        {:type :error :kind :parse-error :message (.getMessage e)}
        {:type :error :kind :validation-error :message (.getMessage e)}))))

;; Usage
(let [result (parse-config "config.json")]
  (case (:type result)
    :ok (println "Loaded:" (-> result :value :name))
    :error (case (:kind result)
             :file-error (println "File error:" (:message result))
             :parse-error (println "Parse error:" (:message result))
             :validation-error (println "Validation error:" (:message result)))))
```

### Example 3: Complex - HTTP Server with Business Logic

**Before (Roc):**
```roc
app [main] { pf: platform "basic-webserver" }

import pf.Http exposing [Request, Response]
import pf.Task exposing [Task]

# Pure business logic
type User = { id : U64, name : Str, email : Str }

findUser : U64, List User -> [Some User, None]
findUser = \id, users ->
    List.findFirst(users, \user -> user.id == id)

validateUser : User -> Result User [InvalidName, InvalidEmail]
validateUser = \user ->
    if Str.isEmpty(user.name) then
        Err(InvalidName)
    else if !(Str.contains(user.email, "@")) then
        Err(InvalidEmail)
    else
        Ok(user)

# HTTP layer
handleRequest : Request, List User -> Task Response []
handleRequest = \request, users ->
    when request.path is
        "/users/:id" ->
            id = parseId!(request.params.id)
            when findUser(id, users) is
                Some(user) ->
                    Http.jsonResponse(200, user)
                None ->
                    Http.jsonResponse(404, { error: "Not found" })

        "/users" when request.method == Post ->
            user = Http.parseJson!(request.body)
            when validateUser(user) is
                Ok(validated) ->
                    saved = saveUser!(validated, users)
                    Http.jsonResponse(201, saved)
                Err(InvalidName) ->
                    Http.jsonResponse(400, { error: "Invalid name" })
                Err(InvalidEmail) ->
                    Http.jsonResponse(400, { error: "Invalid email" })

        _ ->
            Http.jsonResponse(404, { error: "Not found" })

main : Task {} []
main =
    users = loadUsers!()
    Http.serve!(8080, \req -> handleRequest(req, users))
```

**After (Clojure):**
```clojure
(ns myapp.server
  (:require [ring.adapter.jetty :refer [run-jetty]]
            [ring.util.response :refer [response status]]
            [ring.middleware.json :refer [wrap-json-body wrap-json-response]]
            [cheshire.core :as json]))

;; Pure business logic
(defn find-user [id users]
  (first (filter #(= id (:id %)) users)))

(defn validate-user [user]
  (cond
    (empty? (:name user))
    {:type :error :reason :invalid-name}

    (not (re-find #"@" (:email user)))
    {:type :error :reason :invalid-email}

    :else
    {:type :ok :value user}))

;; HTTP layer
(defn json-response [status-code body]
  (-> (response body)
      (status status-code)))

(defn handle-get-user [id users]
  (if-let [user (find-user (parse-long id) users)]
    (json-response 200 user)
    (json-response 404 {:error "Not found"})))

(defn handle-create-user [user users]
  (let [validation (validate-user user)]
    (case (:type validation)
      :ok (let [saved (save-user (:value validation) users)]
            (json-response 201 saved))
      :error (json-response 400 {:error (name (:reason validation))}))))

(defn handler [users]
  (fn [request]
    (let [{:keys [uri request-method params body]} request]
      (cond
        (and (= uri "/users/:id") (= request-method :get))
        (handle-get-user (:id params) users)

        (and (= uri "/users") (= request-method :post))
        (handle-create-user body users)

        :else
        (json-response 404 {:error "Not found"})))))

(defn -main [& args]
  (let [users (load-users)]
    (run-jetty (-> (handler users)
                   wrap-json-body
                   wrap-json-response)
               {:port 8080 :join? false})))
```

**Key translations:**
- Roc's platform effects → Ring middleware pattern
- Roc's Result type → Tagged maps for validation
- Roc's pattern matching → `cond` and `case`
- Roc's Task composition → Direct function calls
- Type safety → Runtime validation with spec (optional)

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-clojure-roc` - Reverse conversion (Clojure → Roc)
- `lang-roc-dev` - Roc development patterns
- `lang-clojure-dev` - Clojure development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async, channels, threads across languages
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Limited in Roc, extensive in Clojure
