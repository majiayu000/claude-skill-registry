---
name: clojure-repl
description: Use this skill whenever you need to evaluate Clojure expressions in a REPL — for iterative development, debugging, API exploration, or validating code before saving to files. Covers nREPL connection, incremental prototyping workflow, and REPL-based testing. Prefer this skill over writing untested Clojure code directly to files. Also invoke when the user asks to "try something in the REPL," "test this function," or "debug this interactively."
---

# Clojure REPL

Guide REPL-driven development workflow for Clojure projects. The foundational approach is "tiny steps with high quality rich feedback" — rapid iteration with immediate validation before committing code to files.

**Devbox note:** For projects using devbox, prefix all shell commands with `devbox run --` (e.g., `devbox run -- clojure -M:dev`, `devbox run -- bb nrepl`).

## Connecting to a Running nREPL

Connect to an existing nREPL session rather than starting a new one when a development server is already running. This allows testing code in the actual runtime environment with live application state.

### Finding and Connecting to nREPL

Check for a `.nrepl-port` file in the project directory:

```bash
# Check if nREPL is running
cat .nrepl-port
# => 54321 (the port number)
```

If the file exists, send expressions to the running nREPL:

```bash
# Using Babashka as nREPL client
echo '(+ 1 2)' | bb nrepl-client localhost:$(cat .nrepl-port)

# Or evaluate a file
bb nrepl-client localhost:$(cat .nrepl-port) --file src/my/namespace.clj
```

### Detecting Stale `.nrepl-port`

If `.nrepl-port` exists but connection fails, the REPL process likely died without cleanup:

```bash
# Test if the port is actually open
nc -z localhost $(cat .nrepl-port) 2>/dev/null && echo "REPL running" || echo "Stale port file"

# If stale, clean up and start fresh
rm .nrepl-port
```

### Starting an nREPL Server

If no `.nrepl-port` file exists:

**1. Check for Babashka tasks** (`bb.edn`)

```bash
bb tasks
# Common REPL task names: repl, nrepl, dev
bb nrepl
```

**2. Check for Clojure aliases** (`deps.edn`)

```bash
# Common REPL aliases: :repl, :nrepl, :dev
clojure -M:dev
```

**3. Start a basic nREPL server**

```bash
# Babashka nREPL
bb nrepl-server

# Clojure nREPL
clojure -Sdeps '{:deps {nrepl/nrepl {:mvn/version "1.1.0"}}}' -M -m nrepl.cmdline
```

After starting, the `.nrepl-port` file will be created containing the port number.

### When to Connect vs. Start Fresh

**Connect to running nREPL when:**
- A development server is already running
- Testing code against live application state
- Debugging runtime issues in the actual environment

**Start fresh REPL when:**
- No development server is running
- Working on standalone functions or utilities
- Prototyping new features in isolation

## Core Philosophy: Incremental Verification

**Small steps beat big leaps.** The REPL excels at providing immediate feedback on small, focused code snippets:

1. **Test before committing** - Validate code in REPL first
2. **Build incrementally** - Add one piece at a time
3. **Verify continuously** - Check each step works before proceeding
4. **Save only what works** - Move validated code to files

**The form and maintainability of ephemeral code DOES NOT MATTER** — only the final saved code needs to be clean.

## REPL-Driven Development Workflow

### Phase 1: Problem Definition

Clearly articulate what you're solving:
- What is the goal?
- What inputs and outputs are expected?
- What constraints or requirements exist?

### Phase 2: REPL Prototyping

Work through solutions incrementally in the REPL:

```clojure
;; Start with data
(def sample-data {:name "Alice" :age 30})

;; Test individual operations
(:name sample-data)
;; => "Alice"

;; Build up logic piece by piece
(defn format-name [person]
  (str "Name: " (:name person)))

(format-name sample-data)
;; => "Name: Alice"

;; Add complexity incrementally
(defn format-person [person]
  (str (format-name person)
       ", Age: " (:age person)))

(format-person sample-data)
;; => "Name: Alice, Age: 30"
```

### Phase 3: Step-by-Step Validation

Test each expression before advancing:

```clojure
;; Test edge cases
(format-person {:name "Bob"})
;; Error! Missing :age

;; Fix and retest
(defn format-person [person]
  (str (format-name person)
       (when-let [age (:age person)]
         (str ", Age: " age))))

(format-person {:name "Bob"})
;; => "Name: Bob"

(format-person sample-data)
;; => "Name: Alice, Age: 30"
```

### Phase 4: File Integration

Save working solutions to source files using the clojure-edit skill.

### Phase 5: Verification

Reload and confirm saved code functions correctly:

```clojure
;; Reload namespace
(require '[my.namespace :as ns] :reload)

;; Test from namespace
(ns/format-person sample-data)
;; => "Name: Alice, Age: 30"

;; Run tests
(clojure.test/run-tests 'my.namespace-test)
```

## REPL Commands and Techniques

For namespace management, code exploration, data inspection, and other REPL commands, see `references/repl_workflows.md`.

### Using the inspect_namespace Script

This skill includes a Babashka script for quickly exploring namespace contents without loading them in the REPL:

```bash
# Inspect a namespace file, showing all public functions
scripts/inspect_namespace.clj src/my/namespace.clj

# Include private functions
scripts/inspect_namespace.clj src/my/namespace.clj --with-private

# Show only function names (useful for quick reference)
scripts/inspect_namespace.clj src/my/namespace.clj --names-only

# Show summary statistics
scripts/inspect_namespace.clj src/my/namespace.clj --summary
```

## Workflow Decision Tree

```
Starting new feature or debugging?
│
├─ New feature development
│  ├─ 1. Define sample data in REPL
│  ├─ 2. Build functions incrementally
│  ├─ 3. Test each piece as you go
│  ├─ 4. Refine based on edge cases
│  ├─ 5. Save working code to file (clojure-edit skill)
│  └─ 6. Reload namespace and verify
│
├─ Debugging existing code
│  ├─ 1. Reload namespace with problem
│  ├─ 2. Reproduce issue in REPL
│  ├─ 3. Isolate problematic expression
│  ├─ 4. Test fixes incrementally
│  ├─ 5. Apply fix to file (clojure-edit skill)
│  └─ 6. Verify with tests
│
├─ Exploring unfamiliar code
│  ├─ 1. Load namespace in REPL
│  ├─ 2. Use (dir ns) to see functions
│  ├─ 3. Use (doc fn) and (source fn)
│  ├─ 4. Test functions with sample data
│  └─ 5. Build understanding incrementally
│
└─ Refactoring
   ├─ 1. Load current implementation
   ├─ 2. Create test data that covers cases
   ├─ 3. Verify current behavior
   ├─ 4. Build new implementation in REPL
   ├─ 5. Test against same data
   ├─ 6. Save when behavior matches
   └─ 7. Run test suite to verify
```

## Best Practices

### Do:
- **Make tiny steps** - Build complexity gradually
- **Test continuously** - Verify each step works
- **Use real data** - Test with actual inputs you'll encounter
- **Explore freely** - Try different approaches in REPL
- **Fail fast** - Find errors quickly in REPL rather than after saving
- **Reload often** - Keep REPL state fresh with `:reload`

### Don't:
- **Skip testing** - Don't assume code works without trying it
- **Write big blocks** - Don't build complex functions all at once
- **Ignore errors** - Don't move forward when something fails
- **Save untested code** - Don't commit to files before REPL validation
- **Trust stale state** - Don't forget to reload after file changes

## Integration with Testing

### Running Tests from REPL

```clojure
;; Run all tests in namespace
(require '[clojure.test :refer [run-tests]])
(run-tests 'my.namespace-test)

;; Run specific test
(require '[clojure.test :refer [test-var]])
(test-var #'my.namespace-test/my-test-name)
```

## Running Tests via CLI

```bash
# Run all tests
clojure -X:test

# Run specific namespace
clojure -X:test :namespace 'my.namespace.test'
```

## Reference Materials

For REPL commands, development patterns, debugging techniques, and session patterns, see `references/repl_workflows.md`.
