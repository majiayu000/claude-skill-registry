---
name: clojure-programmer
description: Clojure-specific philosophy, idioms, and judgment frameworks. Use when working with Clojure code. Emphasizes data-oriented design, runtime validation with spec, REPL-driven development, and the philosophy of simplicity over ease.
---

# Clojure Programmer Skill

**Target Clojure 1.12.3+** (current stable as of September 2025). Version history at https://github.com/clojure/clojure/blob/master/changes.md.

This skill provides judgment frameworks and philosophical grounding for expert-level Clojure development. It assumes you understand functional programming and Lisp basics from training, focusing instead on Clojure-specific philosophy, when/why guidance, and retrieval triggers for avoiding common mistakes.

<core_philosophy>
## Core Philosophy: Simple Made Easy

**For foundational software engineering principles, see the software-engineer skill. For general FP principles, see the functional-programmer skill—this skill provides Clojure-specific guidance that supersedes those general patterns.**

**Rich Hickey's foundational distinction:** "Simple" means one thing, one concept, one task. "Easy" means familiar, near at hand. **Always choose simple over easy.**

This philosophy permeates every Clojure decision:
- Maps over classes (simple: just data vs easy: familiar OOP)
- Data orientation over objects (simple: transformations vs easy: encapsulation)
- Immutability by default (simple: values don't change vs easy: mutation in place)
- Runtime contracts over types (simple: validate what you need vs easy: compile-time guarantees)

**The critical insight:** Simplicity enables change. Easy rots into complexity. When facing a choice between "this feels familiar from Java/Python/JavaScript" and "this is the Clojure way," choose the Clojure way. The unfamiliarity is temporary; the simplicity compounds.

**"Programs must be written for people to read, and only incidentally for machines to execute."** — Hal Abelson, SICP

## Code as Ontology: The Open-World Assumption

**From Rich Hickey's Spec-ulation:** Clojure's design was inspired by RDF's open-world assumption. **Code is an ontology of a solution.** Names create enduring semantic commitments.

### Open Systems Enable Growth

**"If I put on a hat, it does not change what my family is."** — Rich Hickey

Maps are collections of keys, not the stuff inside the keys. Extra keys don't change identity:

```clojure
;; These are the same entity with different knowledge
{:user/id 123 :user/name "Alice"}
{:user/id 123 :user/name "Alice" :user/email "alice@example.com"}

;; Identity preserved, knowledge accreted
```

**This is RDF's open-world assumption:**
- You don't know everything about an entity upfront
- New facts can always be added
- Systems should tolerate unknown information
- Prohibition ("no other keys allowed") turns growth into breakage

### Spec Embodies Open-World Reasoning

**"Spec is about what you CAN do, not about what you CAN'T."** — Rich Hickey

Why spec doesn't allow closed maps:

```clojure
;; If you could say "only these keys"
(s/def ::user (s/closed-keys :req [::id ::name]))

;; Then adding ::email later would BREAK everything
;; Every consumer would need updating
;; Growth becomes breakage
;; Cascading changes up the dependency tree
```

**The open-world discipline:**
- Always presume you might receive more than you know about
- Select the keys you need: `(select-keys user [::id ::name])`
- Don't blindly display everything (might expose sensitive data)
- Ignore what you don't understand
- **Never prohibit growth**

### Levels and Scopes: Don't Conflate

**Each level is a collection with two operations: add or remove.**

- **Functions** — require args, provide return
- **Namespaces** — collections of vars (adding vars = growth, removing = breakage)
- **Artifacts** — collections of namespaces (adding namespaces = growth, removing = breakage)

**"My family doesn't change when I put on a hat."** A function changing (putting on a hat) doesn't change the namespace (the family). Don't version the namespace because a function changed. Don't version the artifact because a namespace changed.

### Accretion Over Breakage

**Growth happens through accretion:**
- Provide more (return additional keys)
- Require less (make parameters optional)
- Add new functions alongside old ones (foo and foo-2 coexist)

**Breakage happens through:**
- Requiring more (mandatory parameters)
- Providing less (removing return keys)
- Removing functions
- **Changing semantics under the same name**

**The discipline:** Turn breakage into accretion. Don't remove `foo`, add `foo-2`. Don't require new parameters, make them optional. Don't remove keys from returns, add new ones.

### Knowledge Representation Connection

**For knowledge engineers:** This is why Clojure feels natural for ontology work. The language's data model mirrors RDF's assumptions:

- **Open-world reasoning** — Unknown facts might exist
- **Monotonic knowledge growth** — Add facts, don't retract (in public APIs)
- **Identity vs. information** — Entity identity (qualified keywords) separate from information (map values)
- **Schema evolution** — Adding predicates doesn't break existing queries
- **Namespace = vocabulary** — Like RDF namespaces, prevents collisions

**Write Clojure code the way you'd design an ontology:** Open to extension, explicit about semantics, preserving meaning over time.
</core_philosophy>

<repl_driven>
## REPL-Driven Development: Living in Your Program

**The REPL isn't just a tool—it's how you think about Clojure development.** Stuart Halloway: "You're living in your program invoking your tools, instead of living in your tools invoking your program."

### The Fundamental Shift

Traditional development: Write code → Compile → Run → Debug → Repeat
REPL-driven development: Start program → Develop features while running → Test immediately → Never restart

**What this means practically:**
- Launch your application once and keep it running for days
- Develop features by evaluating forms directly in namespaces
- Test functions as you write them with real data
- Debug production by connecting a REPL to running systems
- Explore APIs interactively rather than reading docs
- Build features incrementally without compile/restart cycles

### The Comment Block Pattern

Standard practice for preserving REPL experiments:

```clojure
(comment
  ;; REPL-driven development workflow
  (def test-user {:user/id 123 :user/name "Alice"})
  (create-user test-user)
  (db/query {:user/id 123})

  ;; These forms don't execute in production
  ;; But preserve your development process
  ;; And serve as executable documentation
  )
```

**Why this matters:** The `comment` block captures your development thinking. Future you (or other developers) can see how you explored the problem space. This is executable documentation of the design process.

### My Limitations with REPLs

**I cannot use IDE-integrated REPLs** (CIDER, Calva). Terminal-based REPL invocation hangs the bash tool. I work differently:
- Evaluate individual forms via command-line tools
- Write code that's immediately testable without REPL state
- Design for composability and pure functions
- Test interactively when you run the REPL

**This is actually good discipline:** Code that works without complex REPL state is more robust, testable, and maintainable.
</repl_driven>

<data_oriented>
## Data-Oriented Design: Just Use Maps

**Rich Hickey's guidance: "Just use maps."** This isn't laziness—it's profound design insight.

### The Philosophy

**Separate code from data:**
- Data is generic, code is specific
- Systems transform data, they don't encapsulate it
- Open systems beat closed abstractions
- Information wants to be discoverable

**Why maps are the default:**
- Flexible: add/remove keys freely without schema changes
- Composable: generic functions (assoc, dissoc, update, select-keys) work everywhere
- Discoverable: You can see what's there (keys, vals)
- Open: Consumers take what they need, ignore the rest
- Evolution-friendly: Adding data doesn't break existing code

### Qualified Keywords Prevent Collisions

```clojure
;; Good: namespaced keywords
{:user/id 123
 :user/name "Alice"
 :user/email "alice@example.com"
 :account/id 456
 :account/balance 1000.0
 :account/currency :USD}

;; Bad: unqualified keys risk collisions
{:id 123        ; Which id? User or account?
 :name "Alice"
 :balance 1000.0}
```

**Auto-resolved keywords in the namespace:**

```clojure
(ns myapp.users)

;; ::name resolves to :myapp.users/name
{::id 123
 ::name "Alice"
 ::email "alice@example.com"}
```

### When to Use Records vs Maps

**Maps should be 95% of your data structures.** Records exist for specific cases:

**Use records when:**
- Java interop requires specific types
- Performance-critical code with known fields (measure first!)
- Protocol implementation needs type dispatch
- You want a named type for clarity (rare)

**Use maps when:**
- Exploring the domain (always start here)
- Flexibility matters more than performance
- You don't know all fields upfront
- Different consumers need different subsets
- You want loose coupling

**Don't create records prematurely.** Start with maps. Only extract records when you have evidence they're needed. The flexibility of maps compounds over time.

### EDN: Clojure's Data Format

**EDN (Extensible Data Notation):** Subset of Clojure syntax for data serialization.
- Human-readable and machine-parseable
- Richer types than JSON (keywords, symbols, sets, tagged literals)
- Extensible through tagged elements

**Use EDN for:**
- Configuration files
- Data exchange between Clojure systems
- Persisting application state
- When consumers understand EDN

**Use JSON when:**
- Interfacing with non-Clojure systems
- Web APIs for JavaScript consumers
- External requirements dictate it
</data_oriented>

<spec>
## Spec: Runtime Validation, Not a Type System

**Critical positioning:** Spec provides runtime validation with detailed error messages. It is NOT compile-time type checking. The namespace `clojure.spec.alpha` is production-ready despite "alpha" (indicates potential API evolution, not quality).

### When Spec is Mandatory

**At system boundaries:**
- External API inputs (HTTP, queue messages, file uploads)
- Public function contracts at service boundaries
- Configuration validation on startup
- Data contracts between services

**Where spec shines:**
- Detailed error messages for debugging
- Generative testing with random data
- Development-time instrumentation
- Executable documentation of data shapes

### When NOT to Use Spec

**Don't over-specify:**
- Internal function arguments (adds overhead, little benefit)
- Performance-critical hot paths (validation cost matters)
- During initial development exploration
- Where the cost exceeds the value

**The judgment call:** Spec at boundaries where bad data enters. Don't spec internal implementation details. Trust your code within the boundary.

### Basic Spec Patterns

**Register specs with namespaced keywords:**

```clojure
(require '[clojure.spec.alpha :as s])

;; Predicate-based specs
(s/def ::id pos-int?)
(s/def ::email (s/and string? #(re-matches #".+@.+\..+" %)))
(s/def ::role #{:admin :user :guest})

;; Map specs - note: maps are OPEN by default
(s/def ::user
  (s/keys :req [::id ::email]
          :opt [::role ::created-at]))
```

**Co-locate specs with code:**

```clojure
(ns myapp.users
  (:require [clojure.spec.alpha :as s]))

(s/def ::id pos-int?)
(s/def ::email string?)
(s/def ::user (s/keys :req [::id ::email]))

(defn create-user
  "Creates a new user account."
  [user-data]
  (let [validated (s/conform ::user user-data)]
    (if (s/invalid? validated)
      (throw (ex-info "Invalid user data"
                      (s/explain-data ::user user-data)))
      (db/insert! :users validated))))
```

### Function Specs

```clojure
(s/fdef create-user
  :args (s/cat :user-data ::user)
  :ret ::user
  :fn (s/and #(= (-> % :args :user-data ::email)
                 (-> % :ret ::email))))
```

**Instrument in development only:**

```clojure
(require '[clojure.spec.test.alpha :as stest])

;; Development/test: validates :args at call time
(stest/instrument `create-user)

;; Production: turn off (performance overhead)
(stest/unstrument `create-user)
```

### Generative Testing

**Specs automatically generate test data:**

```clojure
(require '[clojure.spec.gen.alpha :as gen])

(gen/sample (s/gen ::user))
;; Generates random valid users

(stest/check `create-user)
;; Property-based testing with generated inputs
```

### Spec Guidelines from Production Use

**Maps are open by default:** Extra keys allowed. This is intentional—enables evolution. Use `s/keys` not `s/strict-keys` unless you have a specific reason.

**The spec IS the function:** It defines correctness. Design specs carefully.

**Don't fight the alpha status:** `clojure.spec.alpha` is stable and widely used. The "alpha" means "we might make a new namespace for breaking changes" not "this is experimental."

**spec2/spec-alpha2:** Work in progress with no timeline. Stick with spec.alpha for all production code.
</spec>

<state_management>
## State Management: Atoms, Refs, Agents, and Vars

**Clojure provides different reference types for different coordination needs.** Understanding when to use each is critical.

### Decision Tree

**Atoms (90% of state):**
- Uncoordinated, synchronous, independent state
- Your default choice for application state
- Use for: caches, counters, configuration, UI state
- Operations: `swap!`, `reset!`, `compare-and-set!`

```clojure
(def app-state (atom {:users {} :sessions {}}))

(swap! app-state update-in [:users user-id] assoc :last-seen (Instant/now))
```

**Refs (coordinated transactions):**
- Coordinated, synchronous, transactional state (STM)
- Multiple identities must change together atomically
- Use for: account transfers, inventory management, ACID-like guarantees
- More overhead than atoms—only use when coordination required

```clojure
(def account-a (ref 1000))
(def account-b (ref 500))

(dosync
  (alter account-a - 100)
  (alter account-b + 100))
```

**Agents (asynchronous updates):**
- Uncoordinated, asynchronous, queued state changes
- Background tasks and controlled side effects
- Use `send` for CPU-bound, `send-off` for blocking I/O

```clojure
(def background-processor (agent {}))

(send background-processor process-batch data)
```

**Vars with dynamic scope:**
- Thread-local bindings for configuration
- Use for: `*out*`, `*print-length*`, context propagation
- **Never use vars for application state**

### The Atom Anti-Pattern

**Don't use atoms for everything just because they're simple:**

```clojure
;; Anti-pattern: global mutable state everywhere
(defonce web-server (atom nil))
(defonce db-connection (atom nil))
(defonce cache (atom {}))

(defn start! []
  (reset! web-server (create-server))
  (reset! db-connection (connect-db)))
```

**Better: Component/Mount/Integrant for lifecycle:**

```clojure
(defn create-system []
  {:web-server (create-server)
   :database (connect-db)
   :cache {}})
```

**Why:** Global atoms create hidden dependencies, make testing hard, and obscure system boundaries. Use lifecycle libraries for managing stateful resources.
</state_management>

<common_mistakes>
## Common Mistakes from Other Language Backgrounds

These patterns are retrieval triggers—seeing them should activate knowledge about the Clojure alternative.

<from_java>
### From Java: Fighting Data Orientation

**Overusing class hierarchies where maps suffice:**

```clojure
;; Java thinking: types for everything
(defrecord User [id name email])
(defrecord Admin [id name email permissions])
(defrecord Guest [id name])

;; Clojure thinking: just data
{:user/id 123 :user/name "Alice" :user/role :admin :user/permissions #{:read :write}}
{:user/id 456 :user/name "Guest" :user/role :guest}
```

**Creating unnecessary mutable state:**

```clojure
;; Java thinking: everything needs state management
(defonce users (atom {}))

(defn create-user! [user-data]
  (let [id (generate-id)
        user (assoc user-data :user/id id)]
    (swap! users assoc id user)
    user))

;; Clojure thinking: pass data through
(defn create-user [db user-data]
  (let [user (assoc user-data :user/id (generate-id))]
    (db/insert! db :users user)))
```

**The `contains?` confusion:**

```clojure
;; Java: Collection#contains checks for VALUE
;; Clojure: contains? checks for KEY/INDEX

(contains? {:a 1 :b 2} :a)  ; true (key exists)
(contains? {:a 1 :b 2} 1)   ; false (1 is not a key)
(contains? [0 1 2] 1)       ; true (index 1 exists)

;; For value membership, use:
(some #{1} (vals {:a 1 :b 2}))  ; 1 (truthy)
```

**Not enabling reflection warnings:**

```clojure
;; Add to dev/user.clj
(set! *warn-on-reflection* true)

;; Causes compiler warnings for reflection
;; Fix with type hints in hot paths only
```

**Making everything private:**

Clojure trusts developers. Use `*.impl.*` namespaces for internal details rather than making everything `defn-`.
</from_java>

<from_python>
### From Python: Lazy Evaluation Surprises

**Expecting eager evaluation:**

```clojure
;; Lazy sequences don't realize until needed
(def results (map expensive-operation data))
;; Nothing has run yet!

;; Force realization when you need it
(doall (map expensive-operation data))  ; Realizes and returns seq
(dorun (map expensive-operation data))  ; Realizes for side effects, returns nil
(into [] (map expensive-operation data)) ; Realizes into vector
```

**Printing infinite sequences hangs:**

```clojure
;; Don't do this
(println (range))  ; Hangs trying to realize infinity

;; Do this
(println (take 10 (range)))  ; Finite!
```

**Holding sequence heads causes space leaks:**

```clojure
;; Bad: holds entire sequence in memory
(let [data (range 1000000)]
  (println (first data))
  (println (last data)))  ; Entire sequence retained!

;; Good: don't hold the head
(println (first (range 1000000)))
(println (last (range 1000000)))  ; Separate realization
```
</from_python>

<from_javascript>
### From JavaScript: Async and Binding Differences

**Trying to use async/await directly:**

```clojure
;; JavaScript async/await doesn't exist in Clojure
;; Use core.async for coordination (not all async operations!)

(require '[clojure.core.async :as async])

(defn fetch-user [id]
  (async/go
    (let [response (async/<! (http/get (str "/users/" id)))]
      (:body response))))
```

**Over-using core.async:**

```clojure
;; Don't over-complicate
;; Simple callbacks are fine!

;; Overkill
(async/go
  (let [result (async/<! (simple-async-op))]
    (process result)))

;; Better: just use a callback
(simple-async-op #(process %))
```

**Expecting 'this' binding:**

Clojure has no implicit `this`. Pass data explicitly.
</from_javascript>

<from_haskell>
### From Haskell: Over-Abstraction

**Creating type-level abstractions with macros:**

Don't recreate Haskell's type system. Embrace dynamic runtime validation with spec.

**Assuming purity enforcement:**

```clojure
;; Clojure: pragmatic impurity
;; Just do side effects where needed
(defn get-user-name []
  (println "Name: ")
  (read-line))

;; Isolate at boundaries, but don't fight them
```

**Avoiding necessary runtime validation:**

```clojure
;; Haskell thinking: types ensure correctness
;; Clojure thinking: validate at boundaries

(defn create-user [user-data]
  (let [validated (s/conform ::user user-data)]
    (when (s/invalid? validated)
      (throw (ex-info "Invalid user"
                      (s/explain-data ::user user-data))))
    (db/insert! :users validated)))
```
</from_haskell>

<from_imperative>
### General Imperative/OO Anti-Patterns

**Not using `recur` for tail recursion:**

```clojure
;; Stack overflow: JVM has no TCO
(defn factorial [n]
  (if (zero? n)
    1
    (* n (factorial (dec n)))))

;; Correct: use recur
(defn factorial
  ([n] (factorial n 1))
  ([n acc]
   (if (zero? n)
     acc
     (recur (dec n) (* acc n)))))
```

**Misusing equality:**

```clojure
;; Use = by default for structural equality
(= 1 1.0)   ; false (different types)
(== 1 1.0)  ; true (numeric equality only)

;; = for collections
(= [1 2 3] [1 2 3])  ; true
```
</from_imperative>
</common_mistakes>

<advanced_topics>
## Advanced Topics: Judgment Frameworks

### When to Use Macros

**Rich Hickey: "Don't use macros unless you absolutely need to."**

**Use macros when you need to:**
- Control evaluation order (delay/prevent evaluation)
- Generate repetitive boilerplate that can't be abstracted with HOFs
- Perform compile-time code generation
- Create domain-specific syntax (sparingly!)
- Manipulate code as data

**Use functions for everything else.** Functions are the default.

**Anti-patterns:**
- Using macros when higher-order functions suffice
- Creating unreadable DSLs
- Premature abstraction
- Making debugging harder for no benefit

```clojure
;; Don't write a macro for this
(defmacro double [x]
  `(* 2 ~x))

;; Write a function
(defn double [x]
  (* 2 x))
```

**When you do write macros:** Create usage examples first. Break complex macros into helper functions. Prefer syntax-quote forms.

### When to Use Transducers

**Transducers provide composable, context-independent transformations.**

**Use transducers when:**
- Avoiding intermediate collections improves performance (measure!)
- Same transformation applies across contexts (collections, channels, streams)
- Building reusable transformation pipelines
- Performance-critical data processing

**Don't use when:**
- Simple threading macros are clearer
- Small collections where intermediate collections don't matter
- Team unfamiliarity outweighs benefits
- You haven't measured performance

```clojure
;; Without transducers
(->> data
     (map parse)
     (filter valid?)
     (map transform))  ; Three intermediate seqs

;; With transducers (single pass)
(def xf (comp (map parse)
              (filter valid?)
              (map transform)))

(into [] xf data)
(transduce xf conj [] data)
```

### When to Use core.async

**core.async serves specific coordination needs, not all async operations.**

**Use core.async for:**
- ClojureScript: avoiding callback hell
- Producer-consumer architectures
- Coordinating multiple async operations
- Event-driven systems with complex flow
- Pipeline processing

**Avoid core.async for:**
- Simple callbacks (just use callbacks!)
- No coordination between operations
- Blocking I/O (use `thread` not `go`)
- Team unfamiliar with CSP concepts

**Key patterns:**
- `go` for parking (lightweight, many thousands possible)
- `thread` for blocking operations
- Dynamic bindings DON'T persist across go block boundaries
- Prefix channel-returning functions with `<`

### Performance Optimization Workflow

**Always measure before optimizing.**

1. **Profile first:**
   - criterium for microbenchmarks
   - clj-async-profiler for flame graphs
   - tufte for application metrics
   - VisualVM/YourKit for comprehensive JVM profiling

2. **High-level optimization (do first):**
   - Fix algorithmic complexity
   - Choose appropriate data structures
   - Use transducers for transformation pipelines

3. **Type hints (only if reflection is the problem):**
   - `(set! *warn-on-reflection* true)` in development
   - Add hints to hot paths only
   - Trust JVM JIT for most code

4. **Primitive optimization (measure first!):**
   - Unchecked math for hot paths
   - Primitive arrays with proper type hints
   - Primitive locals in tight loops

5. **Verify improvements:**
   - Measure before and after
   - Watch for regressions
   - Document why optimizations exist

**Anti-patterns:**
- Premature optimization
- Ignoring algorithmic complexity
- Optimizing cold paths
- Not measuring improvements
- Type hinting everything

**The 90/10 rule:** 90% of time spent in 10% of code. Find that 10% first.
</advanced_topics>

<tooling>
## Mandatory Tooling Stack

### clj-kondo: Mandatory Static Analysis

**clj-kondo must fail builds on errors in CI.** Fast, comprehensive static analyzer:
- Arity errors across namespaces
- Unused vars and bindings
- Unresolved symbols
- Type mismatches
- Deprecated var usage
- Reflection warnings
- And much more

**CI configuration:**

```bash
# Run first in CI (fastest feedback)
clj-kondo --lint src test --fail-level error --parallel
```

**Local `.clj-kondo/config.edn`:**

```clojure
{:linters {:unresolved-symbol {:level :error}
           :unused-binding {:level :warning}
           :unused-private-var {:level :warning}
           :deprecated-var {:level :warning}}
 :lint-as {my.macro/defroute clojure.core/def}}
```

**Integration:**
- Editor integration (real-time feedback)
- CI enforcement (fails builds)
- Pre-commit hooks (optional)

### Spec: Mandatory at API Boundaries

Already covered extensively above. Key: mandatory for external inputs, optional for internal code.

### zprint: Opinionated Code Formatting

**zprint reformats code from scratch** like `gofmt` or Spotless. Aggressive, opinionated, maximum consistency.

**Philosophy:** Surrender control of formatting for consistency. Let the tool handle it.

**Configuration in `deps.edn`:**

```clojure
:format {:deps {zprint/zprint {:mvn/version "1.2.9"}}
         :main-opts ["-m" "zprint.main"]}
```

**CI check:**

```bash
# Check formatting (don't auto-fix in CI)
clojure -M:format "{:search-config? true}" check src test

# Format locally
clojure -M:format "{:search-config? true}" -w src test
```

**`.zprintrc` options:**

```clojure
{:style :community
 :width 80
 :map {:comma? false}}
```

**Why zprint over cljfmt:** Complete reformatting ensures absolute consistency. cljfmt preserves your line breaks; zprint doesn't trust you to get them right.

## Optional/Recommended Tooling

### Kibit: Idiomatic Code Suggestions

**"There's a function for that!"** Suggests more idiomatic Clojure patterns.

Uses core.logic to find code that could be more idiomatic:

```clojure
;; Kibit suggests
(if (not x) y z) → (if-not x y z)
(apply concat x) → (mapcat identity x)
```

**Use for:**
- Learning Clojure idioms
- Code reviews
- Improving existing code

**Don't enforce in CI** (too opinionated, some suggestions debatable).

### Eastwood: Deep Static Analysis

**Slower but more thorough than clj-kondo.** Best for CI where speed isn't critical.

Complements clj-kondo with different checks. Use both if you want comprehensive coverage.

<testing>
### Testing: clojure.test + test.check

**For general testing philosophy and TDD principles, see the test-driven-development skill.** This section covers Clojure-specific testing practices.

**Core testing principle (from test-driven-development skill):** Mock at architectural boundaries (external systems, injected dependencies), not internal implementation details.

**clojure.test dominates (~85% adoption):**
- Built-in
- Universal tooling support
- Battle-tested

```clojure
(ns myapp.users-test
  (:require [clojure.test :refer [deftest is testing]]
            [myapp.users :as users]))

(deftest create-user-test
  (testing "creates user with valid data"
    (let [user-data {:user/email "alice@example.com"}
          result (users/create-user user-data)]
      (is (pos-int? (:user/id result))
          "Generated user ID should be positive")))

  (testing "throws on invalid data"
    (is (thrown? clojure.lang.ExceptionInfo
                 (users/create-user {:invalid :data})))))
```

**Add test.check for property-based testing:**

Leverage spec for generative testing via `clojure.spec.test.alpha/check`.
</testing>
</tooling>

<build_tools>
## Build Tool Selection: deps.edn for New Projects

**deps.edn has won the build tool debate (70%+ adoption and growing).** Leiningen still fine for existing projects.

### deps.edn: Recommended for New Projects

**Why:**
- Officially recommended by Clojure core team
- Focused philosophy: dependency resolution and classpath
- Compose tools as needed
- Git dependencies without Maven
- Growing ecosystem momentum

**Basic structure:**

```clojure
{:deps {org.clojure/clojure {:mvn/version "1.12.3"}}

 :paths ["src" "resources"]

 :aliases
 {:test {:extra-paths ["test"]
         :extra-deps {io.github.cognitect-labs/test-runner
                      {:git/tag "v0.5.1" :git/sha "dfb30dd"}}}

  :dev {:extra-deps {org.clojure/tools.namespace {:mvn/version "1.4.4"}}}

  :lint {:deps {clj-kondo/clj-kondo {:mvn/version "2025.01.24"}}
         :main-opts ["-m" "clj-kondo.main" "--lint" "src" "test"]}

  :format {:deps {zprint/zprint {:mvn/version "1.2.9"}}
           :main-opts ["-m" "zprint.main"]}}}
```

**Compose aliases:**

```bash
clj -M:dev:test  # Development + testing
clj -M:format "{:search-config? true}" -w src test
```

### Leiningen: Still Valid for Existing Projects

Don't migrate unless you have a reason. Leiningen is stable, batteries-included, and well-supported.

**Use Leiningen when:**
- Existing project already uses it
- Team expertise is there
- Plugin ecosystem provides needed functionality
</build_tools>

<project_structure>
## Project Structure and Namespace Organization

### Standard Layout

```
my-project/
├── deps.edn
├── README.md
├── .gitignore
├── .clj-kondo/config.edn
├── .zprintrc
├── src/
│   └── myapp/
│       ├── core.clj
│       ├── users.clj
│       └── db.clj
├── test/
│   └── myapp/
│       ├── core_test.clj
│       └── users_test.clj
├── resources/
│   └── config.edn
├── dev/
│   └── user.clj
└── target/  (gitignored)
```

### Namespace Organization Principles

**Large namespaces are acceptable.** Clojure core has 500+ symbols in one namespace. Don't over-fragment.

**Hard rule: No circular dependencies.** If A requires B, B cannot require A.

**Naming pattern:** `[organization].[project].[module]`

```clojure
(ns myapp.users
  "User management functionality."
  (:require [clojure.spec.alpha :as s]
            [clojure.string :as str]
            [myapp.db :as db])
  (:import [java.time Instant]
           [java.util UUID]))
```

**Standard library aliases (use these):**
- `[clojure.string :as str]`
- `[clojure.set :as set]`
- `[clojure.java.io :as io]`

### dev/user.clj Pattern

```clojure
(ns user
  "Development namespace loaded automatically."
  (:require [clojure.tools.namespace.repl :refer [refresh]]))

(defn start []
  (start-system))

(defn stop []
  (stop-system))

(defn reset []
  (stop)
  (refresh :after 'user/start))

(comment
  (start)
  (stop)
  (reset))
```
</project_structure>

<documentation>
## Documentation Standards

**Public API functions require docstrings.** Production code expectations.

### Docstring Format

```clojure
(defn create-user
  "Creates a new user account with the provided data.

  Validates `user-data` against the ::user spec and persists
  to the database. Returns the created user with generated :user/id.

  Arguments:
  - `user-data`: Map with :user/email (required), :user/role (optional)

  Returns:
  - Created user map with :user/id, :user/email, :user/created-at

  Throws:
  - `ex-info` with spec explanation if validation fails
  - `SQLException` if database insert fails"
  [user-data]
  ...)
```

**Rules:**
- First line: complete sentence summarizing function
- Format for ~80 characters
- Use Markdown (compatible with Codox/cljdoc)
- Wrap identifiers in backticks
- Link related vars: `[[related-fn]]`

**Metadata:**

```clojure
(defn ^:no-doc internal-helper ...)  ; Exclude from docs

(defn ^{:deprecated "1.2.0"} old-fn
  "Legacy. Use [[new-fn]] instead."
  ...)
```
</documentation>

## Version Targeting and Upgrade Philosophy

**Clojure 1.12.3 (September 2025) is current.** Version history: https://github.com/clojure/clojure/blob/master/changes.md

### Aggressive Adoption is Safe

**The community upgrades rapidly** thanks to exceptional backward compatibility.

**Rich Hickey's "Spec-ulation" philosophy:**
- Growth through accretion (adding), not breakage (removing)
- Breaking changes warrant new namespaces, not version bumps
- "Dependency hell becomes mutability hell"

**Practical guidelines:**
- Upgrade to stable releases within 6-12 months
- Specify exact versions in deps.edn
- Test thoroughly despite strong compatibility
- Monitor https://clojure.org/releases/devchangelog

**Clojure 1.12 highlights:**
- Method values (Java methods as first-class functions)
- Functional interface adaptation (IFns auto-convert)
- Array class syntax
- Virtual thread support

**Compatibility:** Java 8 minimum, Java 21 LTS recommended, supports through Java 25.

## Respecting Third-Party Codebases

**Aggressive adoption applies ONLY to codebases you own.**

When contributing to open source:
- Respect existing style and tooling choices
- Follow their Clojure version targeting
- Don't force modern features on older codebases
- Propose improvements through proper channels
- "You're a guest—respect the house rules"

<related_skills>
## Related Skills

- **software-engineer** — Core engineering philosophy, system design principles
- **functional-programmer** — General FP principles (this skill provides Clojure-specific guidance)
- **test-driven-development** — Testing philosophy and TDD principles
</related_skills>

<resources>
## Resources

**Official:**
- https://clojure.org - Official site
- https://github.com/clojure/clojure/blob/master/changes.md - Changelog
- https://clojure.org/guides/spec - Spec guide
- https://clojure.org/reference/java_interop - Java interop

**Rich Hickey's Essential Talks (transcripts—machine-readable):**
- Transcripts: https://github.com/matthiasn/talk-transcripts/tree/master/Hickey_Rich
- Key talks: "Simple Made Easy", "Value of Values", "Spec-ulation" (read transcripts, not video)

**Community:**
- https://guide.clojure.style - Authoritative style guide
- https://clojuredocs.org - API reference with examples
- https://clojureverse.org - Discussion forum
- https://corfield.org - Sean Corfield's production experience

**Tooling:**
- https://github.com/clj-kondo/clj-kondo - Static analyzer
- https://github.com/kkinnear/zprint - Code formatter
- https://github.com/clj-commons/kibit - Idiomatic suggestions
- https://github.com/jonase/eastwood - Deep static analysis

**Books (online):**
- "Clojure for the Brave and True" - https://www.braveclojure.com

**Performance:**
- https://clojure-goes-fast.com/blog/performance-nemesis-reflection
- https://codescene.com/engineering-blog/performance-optimization-workflow-clojure
</resources>
