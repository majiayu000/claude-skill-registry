---
name: scope-capture
description: |
  REPL debugging tool for capturing and inspecting local scope at runtime.
  Use when debugging functions, investigating test failures, understanding intermediate values,
  or when you need to recreate the runtime context of code without manually fabricating values.
---

# scope-capture

Capture local scope at runtime and recreate it in the REPL for debugging.

## Quick Start

```clojure
(require 'sc.api)

;; 1. Add spy to capture scope
(defn my-fn [x y]
  (let [result (+ x y)]
    (sc.api/spy result)))  ; Captures x, y, result

;; 2. Call the function - spy logs EP id
(my-fn 3 4)
; SPY [1 -1] ... saved scope with locals [x y result]
; => 7

;; 3. Recreate scope with defsc (defs all locals as vars)
(sc.api/defsc 1)
; => [#'user/x #'user/y #'user/result]

;; 4. Now evaluate expressions using captured values
x        ; => 3
y        ; => 4
result   ; => 7
(* x y)  ; => 12

;; 5. Clean up when done
(sc.api/dispose! 1)
```

## Core Concepts

**Code Site (CS)** - A location in code where `spy` or `brk` is placed. Has a negative ID like `-1`, `-2`.

**Execution Point (EP)** - A specific execution of a Code Site. Has a positive ID like `1`, `2`, `3`.

**Log format:** `SPY [EP CS]` e.g., `SPY [7 -3]` means Execution Point 7 at Code Site -3.

## Recording Scope

### spy - Capture and continue

```clojure
;; Wrap an expression - captures scope AND the expression value
(sc.api/spy (some-expression))

;; Without expression - just capture scope at this point
(sc.api/spy)

;; With options
(sc.api/spy {:sc/dynamic-vars [*out* *my-var*]}
  (some-expression))
```

### brk - Capture and block (breakpoint)

```clojure
(defn process [data]
  (let [transformed (transform data)]
    (sc.api/brk transformed)))  ; Blocks here until released

;; In another thread, call the function
(future (process my-data))
; BRK [2 -1] ... saved scope, use sc.api/loose to resume

;; Release the breakpoint
(sc.api/loose 2)              ; Continue normally
(sc.api/loose-with 2 value)   ; Continue with replacement value
(sc.api/loose-with-err 2 ex)  ; Continue by throwing exception
```

## Recreating Scope

### defsc - Define vars (preferred for editor eval)

```clojure
(sc.api/defsc 1)
; Defines vars for all captured locals in current namespace
; Now you can evaluate sub-expressions directly in your editor

x        ; works
(+ x y)  ; works
```

### letsc - Let bindings

```clojure
(sc.api/letsc 1
  (+ x y))  ; x and y bound from captured scope
; => 7

;; Useful for one-off evaluations without polluting namespace
```

### ep-repl - Sub-REPL (JVM only)

```clojure
(sc.repl/ep-repl 1)
; SC[1 -1]=> x
; => 3
; SC[1 -1]=> :repl/quit
```

## Common Patterns

### Spy without wrapping expression

```clojure
(let [x (foo)
      y (bar x)]
  (sc.api/spy)  ; Just capture x and y here
  (something x y))
```

### Spy only on errors

```clojure
(try
  (my-fallible-code)
  (catch Throwable err
    (sc.api/spy err)  ; Capture scope when error occurs
    (throw err)))
```

### Disable in loops

```clojure
;; If spy/brk is in a loop, disable after first capture
(sc.api/disable! -1)  ; Use the Code Site ID (negative)
```

### Combine multiple scopes

```clojure
;; Capture from different places, then combine
(sc.api/defsc 1)  ; Defines a, b from first spy
(sc.api/defsc 2)  ; Defines x, y from second spy
;; Now all four vars available
```

### Restore last execution point

```clojure
(eval `(sc.api/defsc ~(sc.api/last-ep-id)))
```

## Utility Functions

```clojure
;; Get info about execution point
(sc.api/ep-info 1)
; => {:sc.ep/id 1
;     :sc.ep/local-bindings {x 3, y 4, ...}
;     :sc.ep/value 7
;     :sc.ep/code-site {...}}

;; Get info about code site
(sc.api/cs-info -1)

;; Get last execution point ID
(sc.api/last-ep-id)

;; Quiet versions (only log types, not values)
(sc.api/spyqt expr)
(sc.api/brkqt expr)

;; Clean up vars created by defsc
(sc.api/undefsc 1)

;; Free memory from execution point
(sc.api/dispose! 1)
```

## Caveats

**Memory leak warning:** Remove `spy`/`brk` before production - they accumulate captured data.

**Dynamic vars:** Must be explicitly declared:
```clojure
(sc.api/spy {:sc/dynamic-vars [*out* *my-var*]} expr)
```

**defsc overwrites vars:** If a var with same name exists (especially `defonce`), `defsc` will fail or overwrite it.

**ClojureScript:** Must use `[ep-id cs-id]` vector syntax:
```clojure
;; ClojureScript requires both IDs
(sc.api/defsc [1 -1])
(sc.api/letsc [1 -1] expr)
```

## Workflow Summary

1. **Add spy** where you want to capture: `(sc.api/spy expr)` or just `(sc.api/spy)`
2. **Execute** the code path (call the function, run the test, etc.)
3. **Note the EP ID** from the log: `SPY [1 -1]`
4. **Recreate scope:** `(sc.api/defsc 1)`
5. **Debug** by evaluating sub-expressions in your editor
6. **Clean up:** `(sc.api/dispose! 1)` and remove the spy call

## Quick Reference

| Function | Purpose |
|----------|---------|
| `(spy expr)` | Capture scope + evaluate expr |
| `(spy)` | Capture scope only |
| `(brk expr)` | Capture scope + block execution |
| `(defsc ep)` | Def vars from captured scope |
| `(letsc ep body)` | Let-bind captured scope |
| `(loose ep)` | Resume blocked brk |
| `(loose-with ep val)` | Resume with replacement value |
| `(dispose! ep)` | Free captured data |
| `(disable! cs)` | Disable a code site |
| `(ep-info ep)` | Get execution point info |
| `(last-ep-id)` | Get most recent EP id |
