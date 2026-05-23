---
name: squint-runtime
description: Squint ClojureScript runtime for minimal JS output compilation
---

# Squint Runtime Skill

**Status**: ✅ Production Ready
**Author**: Michiel Borkent (borkdude)
**Trit**: 0 (ERGODIC - neutral transport)
**Stars**: 1.2k+

---

## Overview

Squint is a **light-weight ClojureScript dialect** that compiles to JavaScript with minimal runtime overhead. It's the "minimal" alternative in borkdude's browser runtime spectrum.

## When to Use Squint vs Cherry

| Aspect | Squint | Cherry 🍒 |
|--------|--------|-----------|
| **Runtime size** | Minimal (~10KB) | Full cljs.core (~100KB) |
| **Semantics** | JS-like | Full CLJS |
| **Data structures** | JS objects/arrays | Persistent immutable |
| **Keywords** | Strings | CLJS keywords |
| **Interop** | Seamless | Requires macros |
| **JSX** | ❌ | ✅ |
| **Use case** | Small scripts, interop | Full applications |

## Installation

```bash
npm install squint-cljs@latest
```

## Usage

```clojure
;; example.cljs
(ns example)

;; Functions compile to regular JS functions
(defn greet [name]
  (str "Hello, " name "!"))

;; JS interop is seamless
(js/console.log (greet "World"))

;; Object destructuring works naturally
(defn process [{:keys [a b c]}]
  (+ a b c))

(process #js {:a 1 :b 2 :c 3})  ; => 6
```

### Compile and Run

```bash
# Compile to JS
npx squint compile example.cljs

# Run directly
npx squint run example.cljs
```

## Key Differences from CLJS

1. **Data structures are JS native**:
   ```clojure
   {:a 1}  ; => {a: 1} in JS (plain object)
   [1 2 3] ; => [1, 2, 3] in JS (array)
   ```

2. **Keywords become strings**:
   ```clojure
   :foo ; => "foo" in JS
   ```

3. **No persistent data structures** (use JS mutation)

4. **Faster interop** (no conversion needed)

## Integration with Gay.jl Colors

```clojure
(ns squint.gay-colors)

;; SplitMix64 constants
(def GOLDEN 0x9E3779B97F4A7C15)
(def MASK64 0xFFFFFFFFFFFFFFFF)

(defn splitmix64 [state]
  (let [s (bit-and (+ state GOLDEN) MASK64)
        z (-> s
              (bit-xor (unsigned-bit-shift-right s 30))
              (* 0xBF58476D1CE4E5B9)
              (bit-and MASK64))
        z (-> z
              (bit-xor (unsigned-bit-shift-right z 27))
              (* 0x94D049BB133111EB)
              (bit-and MASK64))]
    (bit-xor z (unsigned-bit-shift-right z 31))))

(defn color-at [seed idx]
  (loop [state seed i idx]
    (if (zero? i)
      (let [v (splitmix64 state)
            l (+ 10 (* 85 (/ (bit-and v 0xFF) 255)))
            c (* 100 (/ (bit-and (unsigned-bit-shift-right v 8) 0xFF) 255))
            h (* 360 (/ (bit-and (unsigned-bit-shift-right v 16) 0xFFFF) 65535))]
        {:L l :C c :H h})
      (recur (splitmix64 state) (dec i)))))
```

## Commands

```bash
just squint-compile file.cljs  # Compile CLJS to JS
just squint-run file.cljs      # Run CLJS file
just squint-watch              # Watch mode compilation
```

---

**Skill Name**: squint-runtime
**Type**: ClojureScript Compiler
**Trit**: 0 (ERGODIC)
**Invariant**: ✅ Deterministic compilation
