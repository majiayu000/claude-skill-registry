---
name: clojure-coffi
description: |
  Coffi FFI library for calling native C code from Clojure via Panama FFM API (JDK 22+). Use when: wrapping native C libraries, calling native functions, working with off-heap memory and arenas, etc.
---

# Coffi FFI Library

Coffi wraps the Panama Foreign Function & Memory API for calling native C code from Clojure.


## Setup

Add to deps.edn:
```clojure
;; use gh cli to check latest commit with `gh browse  -c -n IGJoshua/coffi`
io.github.IGJoshua/coffi                  {:git/sha "ae3e38a449c88b998db98b0d4bffa9908dea1c79"}
```

JVM argument required:
```
--enable-native-access=ALL-UNNAMED
```

Or in deps.edn alias:
```clojure
{:aliases {:dev {:jvm-opts ["--enable-native-access=ALL-UNNAMED"]}}}
```

Prep deps

```
clojure -Xdeps prep :aliases '[:dev :test]'
```


## Quick Start

```clojure
(require '[coffi.ffi :as ffi :refer [defcfn]]
         '[coffi.mem :as mem])

;; Wrap a native function
(defcfn strlen
  strlen [::mem/c-string] ::mem/long)

(strlen "hello") ;; => 5

;; Load a library
(ffi/load-system-library "z")        ;; System library
(ffi/load-library "path/to/lib.so")  ;; From path
```


## Core Pattern: defcfn

```clojure
(defcfn var-name
  "docstring"
  native_symbol_name [arg-types...] return-type)

;; With wrapper logic
(defcfn var-name
  "native_symbol" [arg-types...] return-type
  native-fn        ;; Binds the raw native function
  [clj-args...]    ;; Clojure argument list
  (body...))       ;; Wrapper body that calls native-fn
```


## Type Quick Reference

| Coffi Type | C Type | Notes |
|------------|--------|-------|
| `::mem/byte` | `int8_t` | |
| `::mem/short` | `int16_t` | |
| `::mem/int` | `int32_t` | |
| `::mem/long` | `int64_t` | |
| `::mem/float` | `float` | |
| `::mem/double` | `double` | |
| `::mem/pointer` | `void*` | |
| `::mem/c-string` | `char*` | Null-terminated |
| `::mem/void` | `void` | Return only |
| `[::mem/struct [...]]` | struct | See below |
| `[::mem/array type n]` | `type[n]` | Fixed size |
| `[::ffi/fn [args] ret]` | function ptr | Callbacks |

For complete type reference: [references/types.md](references/types.md)


## Struct Definition

```clojure
(require '[coffi.layout :as layout])

;; Always use layout/with-c-layout for FFI structs
(mem/defalias ::my-struct
  (layout/with-c-layout
    [::mem/struct
     [[:name ::mem/c-string]
      [:count ::mem/int]
      [:value ::mem/double]]]))

;; Use in function
(defcfn process-data
  process_data [::my-struct] ::mem/int)

(process-data {:name "test" :count 5 :value 3.14})
```


## Memory Arenas

Always use `confined-arena` with `with-open` for temporary allocations:

```clojure
(with-open [arena (mem/confined-arena)]
  (let [ptr (mem/serialize data type arena)]
    (native-fn ptr)))
;; Memory freed automatically
```

Arena types:
- `confined-arena` - Thread-local, freed on close (most common)
- `shared-arena` - Multi-thread, freed on close
- `auto-arena` - GC-managed
- `global-arena` - Never freed

For details: [references/memory.md](references/memory.md)


## Common Patterns

### Output pointer parameter

```clojure
(defcfn open-resource
  "open_resource" [::mem/c-string ::mem/pointer] ::mem/int
  native-open
  [name]
  (with-open [arena (mem/confined-arena)]
    (let [out-ptr (mem/alloc-instance ::mem/pointer arena)
          code (native-open name out-ptr)]
      (if (zero? code)
        (mem/deserialize-from out-ptr ::mem/pointer)
        (throw (ex-info "Failed" {:code code}))))))
```

### String with explicit length

```clojure
(defcfn bind-text
  "bind_text" [::mem/pointer ::mem/c-string ::mem/int] ::mem/int
  native-bind
  [handle text]
  (let [bytes (.getBytes text "UTF-8")]
    (native-bind handle text (count bytes))))
```

### Array serialization

```clojure
;; Serialize array
(mem/serialize [1 2 3 4] [::mem/array ::mem/int 4] arena)

;; For raw Java arrays (better performance)
(mem/serialize (int-array [1 2 3 4]) [::mem/array ::mem/int 4 :raw? true] arena)
```

### Callback to native code

```clojure
(defcfn set-callback
  set_callback [[::ffi/fn [::mem/int] ::mem/int]] ::mem/void)

(set-callback (fn [x] (* x 2)))
```

For more examples: [references/examples.md](references/examples.md)


## Reference Files

Read these references depending on what you are doing. You should read at least one of the now, if not all of them

- [types.md](references/types.md) - Complete type system (primitives, structs, arrays, enums, unions, custom types)
- [memory.md](references/memory.md) - Memory management (arenas, allocation, serialization, pointer ops)
- [examples.md](references/examples.md) - Real-world patterns from sqlite4clj and coffi tests
