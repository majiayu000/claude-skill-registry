---
name: joker-lint
description: Joker Lint Skill
version: 1.0.0
---


# joker-lint Skill


> *"Fast Clojure linting in Go. No JVM. Instant feedback."*

## Overview

**Joker Lint** uses the Joker interpreter (Clojure in Go) for fast static analysis and linting. Sub-second startup, no JVM required.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | -1 (MINUS) |
| Role | VALIDATOR |
| Function | Validates Clojure code style and correctness |

## Installation

```bash
# macOS
brew install candid82/brew/joker

# From source
go install github.com/candid82/joker@latest
```

## Core Commands

```bash
# Lint a file
joker --lint src/core.clj

# Lint with specific rules
joker --lint --working-dir . src/**/*.clj

# Format check
joker --format src/core.clj

# REPL mode
joker
```

## Lint Rules

```clojure
;; .joker configuration
{:rules {:no-unused-fn true
         :no-unused-bindings true
         :no-private-access true
         :no-redeclare true
         :if-without-else :warning}}
```

## Integration with clj-kondo

```clojure
;; Use both for comprehensive linting
(defn lint-project []
  (let [joker-results (joker-lint "src/")
        kondo-results (clj-kondo-lint "src/")]
    {:joker joker-results
     :kondo kondo-results
     :total-issues (+ (count joker-results)
                      (count kondo-results))}))
```

## GF(3) Lint Triads

```clojure
;; Linting as validation (-1)
;; Code generation as (+1)
;; Formatting as coordination (0)

(def lint-triad
  {:generator  {:tool "cursive-gen" :trit +1}
   :coordinator {:tool "cljfmt" :trit 0}
   :validator   {:tool "joker-lint" :trit -1}})

(defn balanced-code-flow [code]
  (-> code
      (generate)      ; +1
      (format-code)   ; 0
      (lint)))        ; -1
;; Σ = +1 + 0 + (-1) = 0 ✓
```

## Babashka Integration

```clojure
#!/usr/bin/env bb

(require '[babashka.process :refer [shell]])

(defn joker-lint [path]
  (let [result (shell {:out :string :err :string :continue true}
                      "joker" "--lint" path)]
    {:exit (:exit result)
     :issues (parse-lint-output (:out result))
     :trit -1}))  ; Validation role

(defn lint-and-report [paths]
  (->> paths
       (map joker-lint)
       (mapcat :issues)
       (group-by :severity)))
```

## Performance

| Tool | Startup | 1000 lines |
|------|---------|------------|
| Joker | 10ms | 50ms |
| clj-kondo | 100ms | 200ms |
| Eastwood | 5s | 10s |

## GF(3) Triads

```
joker-lint (-1) ⊗ cljfmt (0) ⊗ cursive-gen (+1) = 0 ✓
joker-lint (-1) ⊗ babashka-clj (0) ⊗ clojure (+1) = 0 ✓
joker-lint (-1) ⊗ clj-kondo-3color (0) ⊗ squint-runtime (+1) = 0 ✓
```

---

**Skill Name**: joker-lint
**Type**: Static Analysis / Linting
**Trit**: -1 (MINUS - VALIDATOR)
**GF(3)**: Validates Clojure code correctness


## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to Cat# = Comod(P) as a bicomodule in the Prof home:

```
Trit: 0 (ERGODIC)
Home: Prof (profunctors/bimodules)
Poly Op: ⊗ (parallel composition)
Kan Role: Adj (adjunction bridge)
```

### GF(3) Naturality

The skill participates in triads where:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.