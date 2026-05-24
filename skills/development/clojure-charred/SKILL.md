---
name: clojure-charred
description: High-performance JSON and CSV parsing library for Clojure. Use when working with JSON or CSV data and need fast in Clojure, efficient parsing/writing with a clojure.data.json/clojure.data.csv compatible API.
---

# charred

Efficient character-based file parsing for CSV and JSON formats. Zero dependencies, as fast as univocity or jackson, with drop-in compatible APIs for clojure.data.csv and clojure.data.json.

## Setup

deps.edn:
```clojure
com.cnuernber/charred {:mvn/version "1.037"}
```

Require:
```clojure
(require '[charred.api :as charred])
```

See https://clojars.org/com.cnuernber/charred for the latest version.

## Quick Start

JSON:
```clojure
;; Read JSON from string
(charred/read-json "{\"a\": 1, \"b\": 2}")
; => {"a" 1, "b" 2}

;; Transform keys while reading
(charred/read-json "{\"a\": 1, \"b\": 2}" :key-fn keyword)
; => {:a 1, :b 2}

;; Write JSON to string
(charred/write-json-str {:a 1, :b 2})
; => "{\"a\":1,\"b\":2}"

;; Pretty-print JSON
(println (charred/write-json-str {:a 1, :b 2}))
; {
;   "a": 1,
;   "b": 2
; }
```

CSV:
```clojure
;; Read CSV from string or file
(charred/read-csv "Year,Make,Model\n1997,Ford,E350\n2000,Mercury,Cougar")
; => [["Year" "Make" "Model"] ["1997" "Ford" "E350"] ["2000" "Mercury" "Cougar"]]

;; Read from file
(charred/read-csv (java.io.File. "data.csv"))

;; Write CSV to string
(charred/write-csv-str [["Year" "Make" "Model"]
                        ["1997" "Ford" "E350"]])
; => "Year,Make,Model\n1997,Ford,E350\n"
```

## Core Concepts

Performance characteristics:
- Tuned for large files (>1MB)
- For small files/streams, use `:async? false` and smaller `:bufsize` (e.g., 8192)
- Character array-based parsing optimized by HotSpot
- Zero dependencies

Input types accepted:
- Strings
- java.io.Reader
- java.io.File
- Anything clojure.java.io/reader accepts

## JSON API

### Reading JSON

```clojure
;; Basic reading
(charred/read-json "{\"x\":42}")  ; => {"x" 42}

;; Key transformation
(charred/read-json "{\"first_name\":\"John\"}" :key-fn keyword)
; => {:first-name "John"}

;; Read from reader/file
(charred/read-json (java.io.StringReader. "{\"x\":42}"))
(charred/read-json (java.io.File. "data.json") :key-fn keyword)

;; BigDecimal for all floating point
(charred/read-json "3.14159" :bigdec true)  ; => 3.14159M
```

### Writing JSON

```clojure
;; Write to string
(charred/write-json-str {:name "Alice" :age 30})
; => "{\"name\":\"Alice\",\"age\":30}"

;; Write to writer
(with-open [w (java.io.FileWriter. "output.json")]
  (charred/write-json {:name "Alice"} w))

;; Value transformation
(charred/write-json-str {:created (java.time.Instant/now)}
                        :value-fn (fn [k v]
                                   (if (instance? java.time.Instant v)
                                     (.toString v)
                                     v)))
```

### High-Performance JSON for Small Objects

For parsing many small JSON objects, create specialized parse functions:

```clojure
;; Create optimized parser with fixed options
(def parse-fn (charred/parse-json-fn :key-fn keyword))

;; Use in tight loop - much faster than repeated read-json calls
(doseq [json-str json-strings]
  (let [data (parse-fn json-str)]
    (process data)))

;; Similar pathway for writing
(def write-fn (charred/write-json-fn))
(doseq [obj objects]
  (write-fn obj))
```

These specialized functions are thread-safe and significantly faster for repeated operations on small objects.

## CSV API

### Reading CSV

```clojure
;; Basic reading - returns seq of string vectors
(charred/read-csv "a,b,c\n1,2,3")
; => [["a" "b" "c"] ["1" "2" "3"]]

;; From file
(charred/read-csv (java.io.File. "data.csv"))

;; Custom separator
(charred/read-csv "a;b;c\n1;2;3" :separator \;)

;; Skip comments and trim whitespace
(charred/read-csv data :comment-char \# :trim-leading-whitespace? true)

;; Column filtering
(charred/read-csv data :column-whitelist ["name" "age"])
```

### Writing CSV

```clojure
;; Write to string
(charred/write-csv-str [["name" "age"]
                        ["Alice" "30"]
                        ["Bob" "25"]])
; => "name,age\nAlice,30\nBob,25\n"

;; Write to writer
(with-open [w (java.io.FileWriter. "output.csv")]
  (charred/write-csv [["name" "age"] ["Alice" "30"]] w))

;; Custom separator
(charred/write-csv data writer :separator \;)
```

## Common Patterns

### Processing Large CSV Files

```clojure
;; read-csv returns a lazy sequence - process incrementally
(with-open [rdr (io/reader "large-file.csv")]
  (let [rows (charred/read-csv rdr)]
    (doseq [row rows]
      (process-row row))))
```

### Nested JSON Structures

```clojure
;; Deeply nested structures work seamlessly
(charred/read-json "{\"a\":[1,2,{\"b\":[3,\"four\"]},5.5]}" :key-fn keyword)
; => {:a [1 2 {:b [3 "four"]} 5.5]}
```

### CSV with Headers as Maps

```clojure
(let [rows (charred/read-csv "name,age\nAlice,30\nBob,25")
      [header & data] rows]
  (->> data
       (map #(zipmap (map keyword header) %))))
; => ({:name "Alice", :age "30"} {:name "Bob", :age "25"})
```

## Performance Tuning

For large files (>1MB):
```clojure
;; Use defaults - async reading with larger buffers
(charred/read-json large-file)
```

For small files or streams (<1MB):
```clojure
;; Disable async, use smaller buffer
(charred/read-json small-file :async? false :bufsize 8192)
```

For repeated small object parsing:
```clojure
;; Create specialized parser once, reuse many times
(def parser (charred/parse-json-fn :key-fn keyword))
(parser json-string)  ; Much faster than read-json in loops
```

## Gotchas / Caveats

1. Tuned for large files: Default settings optimize for files >1MB. For smaller data, disable async and reduce buffer size.

2. JSON keys must be strings: `{26:"z"}` is invalid JSON and will throw an exception.

3. CSV quoted fields: Multiline values in CSV must be properly quoted. Unclosed quotes will throw EOFException.

4. Memory usage: The `read-csv` function returns a lazy sequence, so large files won't load entirely into memory unless you realize the sequence (e.g., with `vec` or `doall`).

5. Performance of small objects: If parsing many small JSON objects, always create a specialized parser with `parse-json-fn` instead of calling `read-json` repeatedly.

## References

- API Documentation: https://cnuernber.github.io/charred/
- GitHub Repository: https://github.com/cnuernber/charred
- cljdoc: https://cljdoc.org/d/com.cnuernber/charred/
- Benchmarks: https://github.com/cnuernber/fast-json
- Large CSV Support: https://cnuernber.github.io/charred/charred.bulk.html
