---
name: clojure-guardrails
description: Reference for Guardrails library with Malli in Clojure. Use when working with `>defn`, `>defn-`, `>def`, `>fdef` macros, gspec syntax, or function validation. Triggers on guardrails imports, `com.fulcrologic.guardrails.malli`, function specs with `=>` operator, or questions about runtime validation in Clojure.
---

# Clojure Guardrails (Malli)

## Detection

Check if guardrails is in use:
```bash
grep -r "guardrails.enabled" deps.edn shadow-cljs.edn 2>/dev/null
```

## Setup

**deps.edn:**
```clojure
{:deps {com.fulcrologic/guardrails {:mvn/version "1.2.16"}
        metosin/malli             {:mvn/version "0.20.0"}}
 :aliases {:dev {:jvm-opts ["-Dguardrails.enabled=true"]}}}
```

See https://clojars.org/com.fulcrologic/guardrails for the latest version.

**Enable at runtime:** `-Dguardrails.enabled=true`

## Import

```clojure
(require '[com.fulcrologic.guardrails.malli.core :refer [>defn >defn- >def >fdef | ? =>]])
```

## Core Macros

| Macro | Purpose |
|-------|---------|
| `>defn` | Define function with inline spec |
| `>defn-` | Private function with spec |
| `>def` | Register malli schema |
| `>fdef` | Declare spec without body |
| `?` | Nilable shorthand `[:maybe schema]` |
| `\|` | "Such that" constraints |
| `=>` | Separates args from return |

## Gspec Syntax

```
[arg-specs* (| arg-preds+)? => ret-spec (| ret-preds+)?]
```

**Basic:**
```clojure
(>defn add [a b]
  [:int :int => :int]
  (+ a b))
```

**With constraints:**
```clojure
(>defn ranged-rand [start end]
  [:int :int | #(< start end)
   => :int | #(>= % start) #(< % end)]
  (+ start (long (rand (- end start)))))
```

**Nilable:**
```clojure
(>defn find-user [id]
  [:int => (? :map)]
  (get users id))
```

**Multi-arity:**
```clojure
(>defn greet
  ([name]
   [:string => :string]
   (str "Hello, " name))
  ([greeting name]
   [:string :string => :string]
   (str greeting ", " name)))
```

**Variadic:**
```clojure
(>defn sum [x & more]
  [:int [:* :int] => :int]
  (apply + x more))
```

**Map schemas:**
```clojure
(>defn process-user [user]
  [[:map [:name :string] [:age :int]] => :string]
  (str (:name user) " is " (:age user)))
```

## Schema Registry

This is an optional feature.

```clojure
(require '[com.fulcrologic.guardrails.malli.registry :as gr.reg])

;; Register schemas
(>def :user/name :string)
(>def :user/age :int)
(>def :user/record [:map :user/name :user/age])

;; Use in functions
(>defn get-user [id]
  [:int => (? :user/record)]
  (lookup id))
```

## Detailed Reference

See [gspec-syntax.md](references/gspec-syntax.md) for complete syntax documentation.
