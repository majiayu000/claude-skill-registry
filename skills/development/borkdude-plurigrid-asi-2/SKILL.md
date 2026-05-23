<!-- Propagated to cursor | Trit: -1 | Source: .ruler/skills/borkdude -->

# Borkdude Skill: ClojureScript Runtime Selection

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - runtime neutral)
**Principle**: Right tool for context
**Author**: Michiel Borkent (@borkdude)

---

## Overview

**Borkdude** provides guidance for selecting the appropriate ClojureScript runtime based on execution context. Named after Michiel Borkent, creator of Babashka, SCI, Cherry, Squint, and other Clojure tools.

## Runtime Matrix

| Runtime | Context | JVM | Node | Browser | REPL |
|---------|---------|-----|------|---------|------|
| **Babashka** | Scripting | ✗ | ✗ | ✗ | ✓ |
| **SCI** | Embedded | ✓ | ✓ | ✓ | ✓ |
| **Cherry** | Compiler | ✗ | ✓ | ✓ | ✓ |
| **Squint** | Compiler | ✗ | ✓ | ✓ | ✓ |
| **Scittle** | Browser | ✗ | ✗ | ✓ | ✓ |
| **nbb** | Node | ✗ | ✓ | ✗ | ✓ |

## Decision Tree

```
Start
  │
  ├── Need fast startup? ─────────► Babashka (bb)
  │
  ├── Browser target?
  │     ├── Minimal bundle? ──────► Squint
  │     ├── Full ClojureScript? ──► Cherry  
  │     └── Script tag? ──────────► Scittle
  │
  ├── Node scripting? ────────────► nbb
  │
  └── Embedded interpreter? ──────► SCI
```

## Commands

```bash
# Babashka (scripting)
bb script.clj

# nbb (Node)
npx nbb script.cljs

# Squint (compile to JS)
npx squint compile src/main.cljs

# Cherry (compile with macros)
npx cherry compile src/main.cljs

# Scittle (browser)
# <script src="https://cdn.jsdelivr.net/npm/scittle@0.6.15/dist/scittle.js"></script>
```

## SCI (Small Clojure Interpreter)

Embedded interpreter for sandboxed evaluation:

```clojure
(require '[sci.core :as sci])

(def ctx (sci/init {:namespaces {'user {'foo (fn [] "bar")}}}))

(sci/eval-string* ctx "(user/foo)")
;; => "bar"
```

## Cherry vs Squint

| Feature | Cherry | Squint |
|---------|--------|--------|
| ClojureScript compat | High | Medium |
| Bundle size | Larger | Smaller |
| Macros | Full support | Limited |
| Interop | CLJS-style | JS-native |
| Target audience | CLJS developers | JS developers |

## Babashka Pods

Extend Babashka with pods:

```clojure
(require '[babashka.pods :as pods])

(pods/load-pod 'org.babashka/go-sqlite3 "0.1.0")
(require '[pod.babashka.go-sqlite3 :as sqlite])

(sqlite/execute! "test.db" ["CREATE TABLE users (id INTEGER PRIMARY KEY)"])
```

## Integration with Music Topos

```clojure
;; Use Babashka for scripts
(ns ruler.propagate
  (:require [babashka.fs :as fs]))

;; Use SCI for embedded color evaluation
(def color-ctx
  (sci/init {:namespaces 
             {'gay {'color-at (fn [idx] (gay/color-at idx))}}}))
```

## When to Use Each

### Babashka
- Shell scripts
- Build automation
- CLI tools
- Data processing

### SCI
- Sandboxed evaluation
- Plugin systems
- Configuration DSLs
- Interactive REPLs

### Cherry
- Full CLJS features in browser
- Macro-heavy code
- CLJS library compat

### Squint
- Minimal JS output
- JS-first interop
- Small bundles

### Scittle
- Browser scripting
- No build step
- Quick prototypes

### nbb
- Node.js scripting
- npm library access
- Server scripts

## Example: Skill Propagation

```clojure
#!/usr/bin/env bb
;; .ruler/propagate.clj

(require '[babashka.fs :as fs]
         '[clojure.string :as str])

(defn propagate-skill! [skill-name]
  (let [source (str ".ruler/skills/" skill-name "/SKILL.md")
        content (slurp source)]
    (doseq [agent ["codex" "claude" "cursor"]]
      (let [target (str "." agent "/skills/" skill-name "/SKILL.md")]
        (fs/create-dirs (fs/parent target))
        (spit target content)))))

(propagate-skill! "unworld")
```

---

**Skill Name**: borkdude
**Type**: Runtime Selection / ClojureScript Tooling
**Trit**: 0 (ERGODIC)
**Runtimes**: Babashka, SCI, Cherry, Squint, Scittle, nbb
