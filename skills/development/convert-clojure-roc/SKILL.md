---
name: convert-clojure-roc
description: Convert Clojure code to idiomatic Roc. Use when migrating Clojure applications to Roc's platform model, translating dynamic functional code to static functional style, or refactoring REPL-driven code to compile-time verified patterns. Extends meta-convert-dev with Clojure-to-Roc specific patterns.
---

# Convert Clojure to Roc

Convert Clojure code to idiomatic Roc. This skill extends `meta-convert-dev` with Clojure-to-Roc specific type mappings, idiom translations, and tooling for translating from dynamically-typed REPL-driven development to statically-typed platform-based architecture.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Clojure's dynamic types → Roc's static types
- **Idiom translations**: REPL-driven patterns → compile-time verified code
- **Error handling**: Exception-based → Result type with pattern matching
- **Concurrency patterns**: Atoms/refs/agents → platform-managed tasks
- **Platform architecture**: JVM-based → platform/application separation
- **Paradigm shift**: Dynamic functional → static functional with structural types

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Clojure language fundamentals - see `lang-clojure-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → Clojure) - see `convert-roc-clojure`
- ClojureScript frontend patterns - focus is on Clojure backend to Roc applications

---

## Quick Reference

| Clojure | Roc | Notes |
|---------|-----|-------|
| `(defn f [x] ...)` | `f = \x -> ...` | Function definition |
| `String` | `Str` | String type |
| `Long` / `Integer` | `I64` / `U64` | Integer types (specify signedness) |
| `Double` | `F64` | Floating point |
| `Boolean` | `Bool` | Boolean type |
| `nil` | Tag union with empty variant | No null; use `[Some a, None]` |
| `[1 2 3]` (vector) | `List I64` | Lists (immutable sequences) |
| `{:a 1 :b 2}` | `{ a: 1, b: 2 }` | Maps → Records (must have known shape) |
| `#{1 2 3}` | `Set I64` | Sets |
| `(try ... (catch ...))` | `Result a err` | Exception → Result type |
| `(atom x)` | Platform state | Atoms → platform-managed state |
| `(fn [x] (* x x))` | `\x -> x * x` | Anonymous functions |
| `(map f coll)` | `List.map f coll` | Map over collections |

---

## When Converting Code

1. **Analyze source thoroughly** before writing target - understand dynamic behavior
2. **Map types first** - convert dynamic runtime checks to static types
3. **Preserve semantics** over syntax similarity - embrace Roc's type system
4. **Adopt target idioms** - don't write "Clojure code in Roc syntax"
5. **Handle edge cases** - nil → explicit Maybe, exceptions → Result
6. **Leverage platform model** - separate pure logic from I/O
7. **Test equivalence** - same inputs → same outputs
8. **Add compile-time validation** - use Roc's type system to replace runtime checks

---

## Type System Mapping

### Primitive Types

| Clojure | Roc | Notes |
|---------|-----|-------|
| `String` | `Str` | Direct mapping |
| `Long` (default) | `I64` | 64-bit signed integer |
| `Integer` | `I32` | 32-bit signed integer |
| `Double` | `F64` | 64-bit floating point |
| `Float` | `F32` | 32-bit floating point |
| `Boolean` (true/false) | `Bool` | Direct mapping |
| `Character` | `U32` | Unicode code point |
| `nil` | `[None]` or `Result` | No null; use tag unions |
| `Keyword` | Tag or `Str` | `:keyword` → tag or string |

**Important numeric differences:**
- Clojure: Arbitrary precision integers (BigInt) available, automatic promotion
- Roc: Fixed-size integers, explicit overflow behavior (wrapping vs saturating vs checking)
- Clojure: `(/ 1 3)` returns exact ratio; `(/ 1.0 3)` returns float
- Roc: Must choose F64 or Dec (decimal) for division

### Collection Types

| Clojure | Roc | Notes |
|---------|-----|-------|
| `[a]` (vector) | `List a` | Immutable lists |
| `'(a)` (list) | `List a` | Both map to List in Roc |
| `{:k v}` (map with keyword keys) | `{ k : V }` (record) | If keys are known at compile time |
| `{k v}` (map with arbitrary keys) | `Dict k v` | For dynamic key sets |
| `#{a}` (set) | `Set a` | Unique values |
| `[a b]` (2-tuple as vector) | `(a, b)` | Explicit tuple type |
| `[a b c]` (3-tuple as vector) | `(a, b, c)` | Roc has native tuples |

**Key difference:**
- Clojure: Maps are the primary composite data structure, keys can be anything
- Roc: Records are typed with known fields at compile time; Dict is for dynamic keys

### Composite Types

| Clojure | Roc | Notes |
|---------|-----|-------|
| `{:name "Alice" :age 30}` | `{ name: "Alice", age: 30 }` | Map → Record (if shape is known) |
| `(defrecord User [name age])` | `User : { name : Str, age : U32 }` | Record type alias |
| `:keyword` / `:another` | `[Keyword, Another]` (tags) | Union types for discriminated values |
| `{:type :user :name "x"}` | `User { name: "x" }` (tag with payload) | Tagged unions |
| `(Either :ok val :error err)` | `Result val err` or `[Ok val, Err err]` | Result type pattern |

### Function Types

| Clojure | Roc | Notes |
|---------|-----|-------|
| `(fn [a] b)` | `a -> b` | Function type signature |
| `(fn [a b] c)` | `a, b -> c` | Multi-argument function |
| `(fn [& args] ...)` | `List a -> ...` | Variadic → list parameter |
| Higher-order function | `(a -> b) -> c` | Functions as values |

---

## Idiom Translation

### Pattern: nil Handling → Tag Unions

Clojure uses nil idiomatically. Roc requires explicit handling through tag unions.

**Clojure:**
```clojure
(defn find-user [id]
  (when (= id 1)
    {:name "Alice" :age 30}))

(defn display-name [user]
  (if user
    (:name user)
    "Anonymous"))

;; Using some->
(def name
  (some-> (find-user 1)
          :name
          (or "Anonymous")))
```

**Roc:**
```roc
# Explicit Maybe pattern
findUser : I64 -> [Some { name : Str, age : U32 }, None]
findUser = \id ->
    if id == 1 then
        Some({ name: "Alice", age: 30 })
    else
        None

displayName : [Some { name : Str, age : U32 }, None] -> Str
displayName = \maybeUser ->
    when maybeUser is
        Some(user) -> user.name
        None -> "Anonymous"

# Using Result for error context
name =
    when findUser(1) is
        Some(user) -> user.name
        None -> "Anonymous"
```

**Why this translation:**
- Roc eliminates null pointer errors at compile time
- Pattern matching on tag unions is exhaustive (compiler checks all cases)
- More explicit but prevents entire classes of runtime errors
- `[Some a, None]` or `Result a err` replace nil idioms

---

### Pattern: Keywords and Maps → Records and Tags

Clojure uses keywords and maps for both data and discriminated unions. Roc uses records for data and tags for unions.

**Clojure:**
```clojure
;; Data with keyword keys
(def user {:name "Alice" :email "alice@example.com" :age 30})

;; Accessing fields
(:name user) ; => "Alice"
(get user :name) ; => "Alice"

;; Discriminated unions with keywords
(defn handle-message [msg]
  (case (:type msg)
    :increment (update-in model [:count] inc)
    :decrement (update-in model [:count] dec)
    :set-count (assoc model :count (:value msg))))

;; Usage
(handle-message {:type :increment})
(handle-message {:type :set-count :value 42})
```

**Roc:**
```roc
# Records for data (compile-time known fields)
user = { name: "Alice", email: "alice@example.com", age: 30 }

# Accessing fields
user.name # "Alice"

# Type alias for clarity
User : { name : Str, email : Str, age : U32 }

# Discriminated unions with tags
Message : [
    Increment,
    Decrement,
    SetCount(I64),
]

handleMessage : Message, Model -> Model
handleMessage = \msg, model ->
    when msg is
        Increment -> { model & count: model.count + 1 }
        Decrement -> { model & count: model.count - 1 }
        SetCount(value) -> { model & count: value }

# Usage
handleMessage(Increment, model)
handleMessage(SetCount(42), model)
```

**Why this translation:**
- Records provide compile-time field checking (no typos in field names)
- Tags are lightweight and type-safe for discriminated unions
- Pattern matching ensures all message types are handled
- More rigid but catches errors at compile time instead of runtime

---

### Pattern: Dynamic Sequences → Typed Lists

Clojure's sequences are lazily evaluated and dynamically typed. Roc's lists are strictly typed.

**Clojure:**
```clojure
;; Lazy sequence operations
(defn process-items [items]
  (->> items
       (map #(* % 2))
       (filter even?)
       (take 10)
       (reduce + 0)))

;; Infinite sequences
(def naturals (iterate inc 0))
(take 5 naturals) ; => (0 1 2 3 4)

;; Mixed type handling (not recommended but possible)
(map str [1 :two "three"]) ; => ("1" ":two" "three")
```

**Roc:**
```roc
# Strict typed list operations
processItems : List I64 -> I64
processItems = \items ->
    items
    |> List.map(\x -> x * 2)
    |> List.keepIf(\x -> x % 2 == 0)
    |> List.takeFirst(10)
    |> List.sum

# No lazy evaluation - compute eagerly
# For large data, use platform streaming

# Type safety - all elements must be same type
# This won't compile:
# mixedList = [1, "two", :three] # Error!

# Must use tag unions for heterogeneous data
Item : [Num I64, Text Str, Symbol Str]
mixedList : List Item
mixedList = [Num(1), Text("two"), Symbol("three")]
```

**Why this translation:**
- Roc evaluates strictly, avoiding lazy evaluation pitfalls
- Type safety prevents runtime type errors
- Explicit tag unions for heterogeneous data
- Performance is more predictable (no hidden thunks)

---

### Pattern: Exception Handling → Result Type

Clojure uses exceptions for error handling (Java interop). Roc uses the Result type.

**Clojure:**
```clojure
(defn parse-age [s]
  (try
    (let [age (Long/parseLong s)]
      (cond
        (neg? age) (throw (ex-info "Age must be non-negative" {:age age}))
        (>= age 150) (throw (ex-info "Age must be less than 150" {:age age}))
        :else age))
    (catch NumberFormatException e
      (throw (ex-info "Not a valid number" {:input s})))))

;; Calling code
(try
  (let [age (parse-age input)]
    (str "Age: " age))
  (catch Exception e
    (str "Error: " (.getMessage e))))
```

**Roc:**
```roc
# Result type for errors
parseAge : Str -> Result U32 Str
parseAge = \s ->
    when Str.toU32(s) is
        Ok(age) ->
            if age < 0 then
                Err("Age must be non-negative")
            else if age >= 150 then
                Err("Age must be less than 150")
            else
                Ok(age)
        Err(_) ->
            Err("Not a valid number")

# Calling code with pattern matching
result = parseAge(input)
message = when result is
    Ok(age) -> "Age: \(Num.toStr(age))"
    Err(error) -> "Error: \(error)"

# Chaining Results with try
validateAndDouble : Str -> Result U32 Str
validateAndDouble = \s ->
    age = try parseAge(s)
    if age > 50 then
        Ok(age * 2)
    else
        Err("Age must be greater than 50")
```

**Why this translation:**
- Result type makes errors explicit in function signatures
- Compiler enforces error handling (can't ignore Err case)
- No hidden control flow (exceptions can jump anywhere)
- `try` keyword unwraps Result or early-returns Err
- More verbose but impossible to forget error handling

---

### Pattern: Atoms and State → Platform State Management

Clojure uses atoms for shared mutable state. Roc pushes state to the platform layer.

**Clojure:**
```clojure
;; Atom for application state
(def app-state (atom {:count 0 :users #{}}))

;; Pure update function
(defn increment-count [state]
  (update state :count inc))

;; Apply update
(swap! app-state increment-count)

;; Read state
@app-state

;; Watch state changes
(add-watch app-state :logger
  (fn [key atom old-state new-state]
    (println "State changed:" old-state "->" new-state)))
```

**Roc:**
```roc
# Application code is pure - no mutable state
# State is managed by the platform

# Define state type
Model : { count : I64, users : Set Str }

# Pure update functions
incrementCount : Model -> Model
incrementCount = \model ->
    { model & count: model.count + 1 }

# Platform integration (example with basic-cli)
app =
    { init: { count: 0, users: Set.empty() }
    , update: update
    , subscriptions: subscriptions
    }

update : Msg, Model -> Model
update = \msg, model ->
    when msg is
        Increment -> incrementCount(model)
        # ...other messages

# Platform handles state persistence, not application code
```

**Why this translation:**
- Roc applications are pure functions of (state, message) → new state
- Platform layer handles actual state mutation and effects
- Clearer separation between pure logic and side effects
- Makes testing trivial (just test pure functions)
- State changes are tracked by platform, not manual watching

---

## Paradigm Translation

### Mental Model Shift: Dynamic REPL-Driven → Static Platform-Based

| Clojure Approach | Roc Approach | Key Insight |
|------------------|--------------|-------------|
| REPL-driven development | Compile-time verification | Catch errors before running |
| Runtime type checking | Static type inference | Types are inferred, not annotated everywhere |
| Flexible data (maps with any keys) | Structured data (records with known fields) | Trade flexibility for safety |
| Atoms for state | Platform-managed state | Separate pure logic from effects |
| Exceptions for errors | Result type | Errors are values, must be handled |
| Lazy sequences | Strict evaluation | Predictable performance |
| Macros for abstraction | Functions + abilities | Less metaprogramming, more composition |

### Architectural Shift: JVM Application → Platform/Application

| Clojure Architecture | Roc Architecture | Translation Strategy |
|---------------------|------------------|---------------------|
| JVM process with main function | Application on platform | Main → platform definition |
| Ring/HTTP server | Platform provides HTTP | Use http-server platform |
| File I/O anywhere | Platform exposes I/O tasks | Collect I/O at boundaries |
| Database access in functions | Platform provides DB tasks | Task-based database access |
| Manual dependency management | Platform provides dependencies | Platform includes needed capabilities |

---

## Error Handling

### Clojure Error Model → Roc Error Model

**Clojure's approach:**
- Exceptions (from Java) for error conditions
- `try/catch/finally` blocks
- Custom exception types with `ex-info`
- Error data attached to exceptions

**Roc's approach:**
- `Result a err` type for operations that can fail
- Pattern matching on `Ok` and `Err` variants
- `try` keyword for early returns from Result
- Errors are just values (typically strings or custom tags)

### Common Error Patterns

| Clojure Pattern | Roc Pattern | Example |
|----------------|-------------|---------|
| `(throw (ex-info ...))` | `Err("...")` | `Err("Invalid input")` |
| `(try ... (catch ...))` | `when result is Ok(...) -> ... Err(...) -> ...` | Pattern match on Result |
| Error propagation with `(when-let ...)` | `try` keyword | `x = try parseNum(s)` |
| Multiple error types | Tag union for errors | `[ValidationErr, ParseErr, DbErr]` |
| Error data | Record in Err variant | `Err({ code: 404, msg: "Not found" })` |

### Example: Error Propagation

**Clojure:**
```clojure
(defn process-user [user-id]
  (try
    (let [user (fetch-user user-id)
          validated (validate-user user)
          updated (update-permissions validated)]
      {:success updated})
    (catch Exception e
      {:error (.getMessage e)})))
```

**Roc:**
```roc
processUser : I64 -> Result User Str
processUser = \userId ->
    user = try fetchUser(userId)
    validated = try validateUser(user)
    updated = try updatePermissions(validated)
    Ok(updated)

# The 'try' keyword automatically propagates Err
# If any step returns Err, the whole function returns that Err
```

---

## Concurrency Patterns

### Clojure Concurrency → Roc Platform Tasks

**Clojure's approach:**
- Atoms, Refs, Agents for coordinated state
- `core.async` for CSP-style channels
- Java threads and futures
- STM (Software Transactional Memory) with refs

**Roc's approach:**
- Platform provides Task type for async operations
- Tasks are descriptions of work (not running computations)
- Platform handles scheduling and execution
- No shared mutable state in application code

### Task Model Translation

| Clojure Pattern | Roc Pattern | Notes |
|----------------|-------------|-------|
| `(future ...)` | `Task.async ...` | Async computation |
| `@(future ...)` (deref) | `Task.await task` | Wait for result |
| `(go (<! chan))` | Platform-specific subscriptions | Channel → subscription |
| `(swap! atom f)` | `Task.map model f` | State update via task |
| Blocking I/O | `Task.await (Http.get url)` | I/O as tasks |

### Example: HTTP Request

**Clojure:**
```clojure
(require '[clj-http.client :as http])

(defn fetch-data [url]
  (try
    (let [response (http/get url {:as :json})]
      (:body response))
    (catch Exception e
      (println "Error:" (.getMessage e))
      nil)))

;; Async version
(require '[clojure.core.async :refer [go <!]])

(defn fetch-data-async [url]
  (go
    (try
      (let [response (<! (http/get url {:as :json :async? true}))]
        (:body response))
      (catch Exception e
        (println "Error:" e)
        nil))))
```

**Roc:**
```roc
# Tasks are values describing work to be done
fetchData : Str -> Task (List User) [HttpErr Str]
fetchData = \url ->
    response = try Http.get(url) |> Task.mapErr(\_ -> HttpErr("Request failed"))
    bytes = response.body
    decoded = try Decode.fromBytes(bytes) |> Task.mapErr(\_ -> HttpErr("Decode failed"))
    Ok(decoded)

# Platform executes tasks, not application code
# Composing tasks
processUsers : Task (List Str) [HttpErr Str]
processUsers =
    users = try fetchData("https://api.example.com/users")
    names = List.map(users, \u -> u.name)
    Task.ok(names)
```

**Why this translation:**
- Tasks are descriptions, not running code (referentially transparent)
- Platform handles actual I/O execution
- Error handling is explicit in the type signature
- Easier to test (tasks are just data until executed by platform)

---

## Platform Architecture

### JVM Process → Platform/Application Separation

**Key conceptual shift:**

In Clojure, your application is a JVM process that directly performs I/O. In Roc, your application is a pure module that describes transformations, and the platform handles I/O.

```
Clojure:                    Roc:
┌─────────────────┐         ┌─────────────────┐
│   Application   │         │   Application   │
│   (impure)      │         │   (pure Roc)    │
│  ┌───────────┐  │         │                 │
│  │ Database  │  │         │  Pure functions │
│  │ HTTP      │  │         │  Type defs      │
│  │ File I/O  │  │         │  Logic only     │
│  └───────────┘  │         └────────┬────────┘
└─────────────────┘                  │ Pure interface
      JVM                            ▼
                              ┌─────────────────┐
                              │    Platform     │
                              │  (Roc + host)   │
                              │  ┌───────────┐  │
                              │  │ Database  │  │
                              │  │ HTTP      │  │
                              │  │ File I/O  │  │
                              │  └───────────┘  │
                              └─────────────────┘
```

### Platform Selection

When converting a Clojure application, choose the appropriate Roc platform:

| Clojure Application Type | Roc Platform | Notes |
|--------------------------|--------------|-------|
| CLI tool | `basic-cli` | Task-based CLI apps |
| Web server | `basic-webserver` | HTTP server apps |
| Script | `basic-cli` | File processing, automation |
| Library | No platform | Pure Roc module, consumed by platform apps |

---

## Common Pitfalls

1. **Trying to use nil directly**: Roc has no null. Use tag unions like `[Some a, None]` or `Result a err`.
   - Bad: Expecting nil to work as in Clojure
   - Good: `when maybeValue is Some(v) -> ... None -> ...`

2. **Using maps for everything**: In Roc, use records when fields are known at compile time.
   - Bad: `{ "dynamicKey": value }` (dynamic string keys)
   - Good: `{ knownField: value }` (compile-time known) or `Dict.fromList([("key", value)])` for truly dynamic keys

3. **Forgetting to handle errors**: Result forces you to handle both Ok and Err.
   - Bad: Only pattern matching on Ok case
   - Good: `when result is Ok(v) -> ... Err(e) -> ...` (exhaustive)

4. **Mixing pure logic with effects**: Keep application code pure.
   - Bad: Calling I/O functions directly in application logic
   - Good: Return Task values, let platform execute them

5. **Over-using type annotations**: Roc infers most types.
   - Bad: Annotating every single function when types are obvious
   - Good: Annotate public API boundaries and complex functions only

6. **Expecting lazy evaluation**: Roc evaluates strictly.
   - Bad: Assuming `List.map` won't compute until needed
   - Good: Use platform streaming for large data

7. **Not leveraging pattern matching**: Use `when` exhaustively instead of `if/else` chains.
   - Bad: `if x == A then ... else if x == B then ...`
   - Good: `when x is A -> ... B -> ... C -> ...`

8. **Ignoring numeric overflow**: Roc has explicit overflow behavior.
   - Bad: Assuming automatic BigInt promotion like Clojure
   - Good: Choose appropriate integer size (I64, I32) and handle overflow explicitly

---

## Limitations

### Coverage Gaps

| Pillar | lang-clojure-dev | lang-roc-dev | Mitigation |
|--------|------------------|--------------|------------|
| Module | ✓ | ✓ | Both skills have good coverage |
| Error | ~ | ✓ | Clojure uses exceptions contextually; Roc has dedicated section |
| Concurrency | ~ | ✓ | Clojure has state mgmt; Roc has tasks - this skill bridges gap |
| Metaprogramming | ✓ | ✓ | Both covered (macros vs abilities) |
| Zero/Default | ~ | ~ | Both mention in context; this skill provides explicit nil → Maybe translation |
| Serialization | ✓ | ✗ | Clojure covered; reference `patterns-serialization-dev` for Roc |
| Build | ✓ | ✗ | Clojure covered; consult Roc platform documentation |
| Testing | ✓ | ✓ | Both covered |
| REPL/Workflow | ✓ | ~ | Clojure REPL-centric; Roc compile-time focused |

**Combined Score:** 14/17 (Good with noted gaps)

**Gaps:**
- Roc serialization patterns not fully covered in lang-roc-dev
- Roc build tooling not covered in lang-roc-dev
- REPL workflow differences require paradigm shift

**Mitigation:**
- Reference `patterns-serialization-dev` for encoding/decoding patterns
- Consult official Roc platform documentation for build process
- This skill documents REPL → compile-time workflow shift

### Known Limitations

1. **Serialization**: This skill has limited guidance on Roc's serialization patterns (Encode/Decode) because lang-roc-dev lacks comprehensive serialization coverage. For production serialization, consult `patterns-serialization-dev` and Roc platform documentation.

2. **Build tooling**: Conversion patterns for build scripts (Leiningen/deps.edn → Roc platform config) may be incomplete. Refer to specific platform documentation.

3. **Advanced macros**: Some complex Clojure macros may not have direct Roc equivalents. Consider whether the macro is solving a problem that Roc's type system already addresses.

### External Resources Used

| Resource | What It Provided | Reliability |
|----------|------------------|-------------|
| lang-clojure-dev | Clojure patterns (REPL, macros, sequences) | High (internal skill) |
| lang-roc-dev | Roc patterns (records, tags, platform model) | High (internal skill) |
| meta-convert-dev | APTV workflow and general conversion methodology | High (internal skill) |
| Roc tutorial | Platform/application architecture | High (official) |

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| Roc compiler | Type checking and compilation | Provides detailed error messages |
| `roc check` | Type check without building | Fast feedback loop |
| `roc test` | Run expect tests | Inline testing with `expect` |
| `roc repl` | Interactive exploration | Limited compared to Clojure REPL |
| `roc format` | Code formatting | Standard formatter |
| `roc docs` | Generate documentation | From type signatures |

**No direct Clojure → Roc transpiler exists.** Conversion is manual but type-guided.

---

## Examples

### Example 1: Simple - Function with Optional Return

**Before (Clojure):**
```clojure
(defn find-first-even [numbers]
  (first (filter even? numbers)))

;; Usage
(find-first-even [1 3 5 6 7]) ; => 6
(find-first-even [1 3 5])     ; => nil
```

**After (Roc):**
```roc
# Explicit Maybe return type
findFirstEven : List I64 -> [Some I64, None]
findFirstEven = \numbers ->
    when List.findFirst(numbers, \n -> n % 2 == 0) is
        Ok(n) -> Some(n)
        Err(_) -> None

# Usage
result1 = findFirstEven([1, 3, 5, 6, 7]) # Some(6)
result2 = findFirstEven([1, 3, 5])       # None

# Pattern match on result
message = when result1 is
    Some(n) -> "Found: \(Num.toStr(n))"
    None -> "No even number found"
```

**Key changes:**
- nil → explicit `[Some a, None]` tag union
- Return type documents possibility of no result
- Compiler enforces handling both cases

---

### Example 2: Medium - Error Handling and Validation

**Before (Clojure):**
```clojure
(require '[clojure.spec.alpha :as s])

(s/def ::email (s/and string? #(re-matches #".+@.+\..+" %)))
(s/def ::age (s/and int? #(< 0 % 150)))
(s/def ::user (s/keys :req-un [::email ::age]))

(defn create-user [email age]
  (let [user {:email email :age age}]
    (if (s/valid? ::user user)
      {:ok user}
      {:error (s/explain-str ::user user)})))

;; Usage
(create-user "alice@example.com" 30)
;; => {:ok {:email "alice@example.com", :age 30}}

(create-user "invalid" 200)
;; => {:error "Spec validation failed..."}
```

**After (Roc):**
```roc
# Type-safe user record
User : { email : Str, age : U32 }

# Validation errors as tag union
ValidationErr : [InvalidEmail, AgeOutOfRange]

# Validation functions
validateEmail : Str -> Result Str ValidationErr
validateEmail = \email ->
    if Str.contains(email, "@") && Str.contains(email, ".") then
        Ok(email)
    else
        Err(InvalidEmail)

validateAge : U32 -> Result U32 ValidationErr
validateAge = \age ->
    if age > 0 && age < 150 then
        Ok(age)
    else
        Err(AgeOutOfRange)

# Create user with validation
createUser : Str, U32 -> Result User ValidationErr
createUser = \email, age ->
    validEmail = try validateEmail(email)
    validAge = try validateAge(age)
    Ok({ email: validEmail, age: validAge })

# Usage
result1 = createUser("alice@example.com", 30)
# Ok({ email: "alice@example.com", age: 30 })

result2 = createUser("invalid", 200)
# Err(InvalidEmail)

# Pattern match on result
message = when result1 is
    Ok(user) -> "Created user: \(user.email)"
    Err(InvalidEmail) -> "Invalid email format"
    Err(AgeOutOfRange) -> "Age must be between 0 and 150"
```

**Key changes:**
- Runtime spec validation → compile-time types + Result validation
- Error strings → typed error variants
- `try` keyword chains validations, short-circuits on first error
- Pattern matching provides exhaustive error handling

---

### Example 3: Complex - State Management and Updates

**Before (Clojure):**
```clojure
(defrecord TodoItem [id text completed])

(def app-state
  (atom {:todos []
         :next-id 0
         :filter :all}))

(defn add-todo [state text]
  (let [id (:next-id state)
        todo (->TodoItem id text false)]
    (-> state
        (update :todos conj todo)
        (update :next-id inc))))

(defn toggle-todo [state id]
  (update state :todos
    (fn [todos]
      (mapv #(if (= (:id %) id)
              (update % :completed not)
              %)
            todos))))

(defn set-filter [state filter]
  (assoc state :filter filter))

(defn visible-todos [state]
  (let [todos (:todos state)
        filter (:filter state)]
    (case filter
      :all todos
      :active (filterv (complement :completed) todos)
      :completed (filterv :completed todos))))

;; Usage with atom
(swap! app-state add-todo "Learn Roc")
(swap! app-state toggle-todo 0)
(swap! app-state set-filter :completed)
(visible-todos @app-state)
```

**After (Roc):**
```roc
# Types
TodoItem : { id : U64, text : Str, completed : Bool }

Filter : [All, Active, Completed]

Model : {
    todos : List TodoItem,
    nextId : U64,
    filter : Filter,
}

# Messages for updates
Msg : [
    AddTodo Str,
    ToggleTodo U64,
    SetFilter Filter,
]

# Pure update functions
addTodo : Model, Str -> Model
addTodo = \model, text ->
    newTodo = { id: model.nextId, text: text, completed: Bool.false }
    { model &
        todos: List.append(model.todos, newTodo),
        nextId: model.nextId + 1,
    }

toggleTodo : Model, U64 -> Model
toggleTodo = \model, id ->
    updatedTodos = List.map(model.todos, \todo ->
        if todo.id == id then
            { todo & completed: !todo.completed }
        else
            todo
    )
    { model & todos: updatedTodos }

setFilter : Model, Filter -> Model
setFilter = \model, filter ->
    { model & filter: filter }

# Query function
visibleTodos : Model -> List TodoItem
visibleTodos = \model ->
    when model.filter is
        All -> model.todos
        Active -> List.keepIf(model.todos, \t -> !t.completed)
        Completed -> List.keepIf(model.todos, \t -> t.completed)

# Main update dispatcher
update : Msg, Model -> Model
update = \msg, model ->
    when msg is
        AddTodo(text) -> addTodo(model, text)
        ToggleTodo(id) -> toggleTodo(model, id)
        SetFilter(filter) -> setFilter(model, filter)

# Initial model
init : Model
init = {
    todos: [],
    nextId: 0,
    filter: All,
}

# Usage (in platform context, not shown)
# model1 = update(AddTodo("Learn Roc"), init)
# model2 = update(ToggleTodo(0), model1)
# model3 = update(SetFilter(Completed), model2)
# visible = visibleTodos(model3)
```

**Key changes:**
- Atom with mutable state → immutable Model type
- Keywords for actions → typed Msg tag union
- `swap!` updates → pure `update` function
- State managed by platform, not application
- All updates are pure functions: (Msg, Model) → Model
- Easier to test (no atoms, just pure functions)
- Type system prevents invalid messages or state shapes

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-clojure-dev` - Clojure development patterns (REPL, macros, sequences)
- `lang-roc-dev` - Roc development patterns (platform model, records, abilities)
- `convert-elm-roc` - Similar functional to functional conversion (Elm → Roc)
- `convert-haskell-roc` - Another ML-family language conversion

Cross-cutting pattern skills (for areas not fully covered by lang-*-dev):
- `patterns-serialization-dev` - Encode/Decode patterns across languages
- `patterns-concurrency-dev` - Async, tasks, channels across languages
