---
name: clojure-babashka-json
description: babashka.json is a cross-platform JSON abstraction for Clojure/babashka. Use when working with JSON parsing, serialization, or writing portable code that runs on both JVM and babashka.
---

# babashka.json

A minimal abstraction over multiple JSON implementations, providing a unified API that works seamlessly in both JVM Clojure and babashka.

The library automatically selects the best available JSON implementation on your classpath without requiring conditional reader macros or platform-specific code.

## Setup

deps.edn:
```clojure
org.babashka/json {:mvn/version "0.1.7"}
```

Leiningen:
```clojure
[org.babashka/json "0.1.7"]
```

See https://clojars.org/org.babashka/json for the latest version.

## Quick Start

```clojure
(require '[babashka.json :as json])

;; Parse JSON string to Clojure data
(json/read-str "{\"name\": \"Alice\", \"age\": 30}")
;; => {:name "Alice", :age 30}

;; Serialize Clojure data to JSON
(json/write-str {:name "Bob" :age 25})
;; => "{\"name\":\"Bob\",\"age\":25}"

;; Round-trip
(-> {:users [{:id 1} {:id 2}]}
    json/write-str
    json/read-str)
;; => {:users [{:id 1} {:id 2}]}
```

## Core Functions

### read-str - Parse JSON string

```clojure
;; Basic parsing - keys become keywords by default
(json/read-str "{\"a\": 1, \"b\": 2}")
;; => {:a 1, :b 2}

;; Arrays
(json/read-str "[1, 2, 3]")
;; => [1 2 3]

;; Keep string keys
(json/read-str "{\"a\": 1}" {:key-fn str})
;; => {"a" 1}

;; Custom key transformation
(json/read-str "{\"user_id\": 123}" {:key-fn #(-> % keyword str/upper-case keyword)})
;; => {:USER_ID 123}
```

Options:
- `:key-fn` - Function to transform JSON object keys. Defaults to `keyword`.

### write-str - Serialize to JSON

```clojure
;; Maps
(json/write-str {:name "Alice" :active true})
;; => "{\"name\":\"Alice\",\"active\":true}"

;; Vectors
(json/write-str [1 2 3])
;; => "[1,2,3]"

;; Nested structures
(json/write-str {:users [{:id 1 :name "Alice"}
                         {:id 2 :name "Bob"}]})
;; => "{\"users\":[{\"id\":1,\"name\":\"Alice\"},{\"id\":2,\"name\":\"Bob\"}]}"

;; Keywords become strings
(json/write-str {:status :active})
;; => "{\"status\":\"active\"}"
```

### read - Parse from reader

```clojure
(require '[clojure.java.io :as io])

;; Read from file
(with-open [rdr (io/reader "data.json")]
  (json/read (json/->json-reader rdr)))

;; Read from string reader
(let [rdr (json/->json-reader (java.io.StringReader. "{\"a\": 1}"))]
  (json/read rdr))
;; => {:a 1}

;; With custom key function
(let [rdr (json/->json-reader (java.io.StringReader. "{\"a\": 1}")
                               {:key-fn str})]
  (json/read rdr {:key-fn str}))
;; => {"a" 1}
```

### get-provider - Check current implementation

```clojure
(json/get-provider)
;; => cheshire/cheshire (in babashka)
;; => org.clojure/data.json (on JVM without other deps)
```

## Provider Selection

On the JVM, babashka.json automatically uses the first available library in this order:

1. cheshire/cheshire (babashka default)
2. com.cnuernber/charred
3. metosin/jsonista
4. org.clojure/data.json (bundled fallback)

Force a specific provider via JVM property BEFORE loading the library:

```clojure
;; In deps.edn :jvm-opts
:jvm-opts ["-Dbabashka.json.provider=com.cnuernber/charred"]

;; Or programmatically (must be before requiring babashka.json)
(System/setProperty "babashka.json.provider" "metosin/jsonista")
(require '[babashka.json :as json])
```

Valid provider values:
- `cheshire/cheshire`
- `com.cnuernber/charred`
- `metosin/jsonista`
- `org.clojure/data.json`

## Common Patterns

### API Response Handling

```clojure
(require '[babashka.json :as json])

(defn fetch-user [id]
  (-> (http/get (str "https://api.example.com/users/" id))
      :body
      (json/read-str)))

;; Use the data
(let [user (fetch-user 123)]
  (println "User:" (:name user)))
```

### File I/O

```clojure
(require '[clojure.java.io :as io]
         '[babashka.json :as json])

;; Write JSON to file
(defn save-config [config path]
  (spit path (json/write-str config)))

;; Read JSON from file
(defn load-config [path]
  (json/read-str (slurp path)))

;; Streaming large files
(defn read-large-json [path]
  (with-open [rdr (io/reader path)]
    (json/read (json/->json-reader rdr))))
```

### babashka Scripts

```clojure
#!/usr/bin/env bb

(require '[babashka.json :as json])

;; Read from stdin
(let [data (json/read-str (slurp *in*))]
  (println "Processing" (count data) "records"))

;; Write to stdout
(println (json/write-str {:status "ok" :timestamp (System/currentTimeMillis)}))
```

### Portable JVM/babashka Code

Instead of this:
```clojure
#?(:bb (cheshire.core/parse-string s keyword)
   :clj (clojure.data.json/read-str s :key-fn keyword))
```

Write this:
```clojure
(require '[babashka.json :as json])
(json/read-str s)
```

Works identically on both platforms.

## Key Gotchas

1. Keywords vs Strings: By default, JSON object keys become keywords. Use `:key-fn str` if you need string keys.

2. Provider must be set early: The `babashka.json.provider` system property must be set BEFORE the library is loaded. Setting it after has no effect.

3. Excluding the bundled dependency: If you don't want `org.clojure/data.json` on your classpath:
   ```clojure
   org.babashka/json {:mvn/version "0.1.7"
                      :exclusions [org.clojure/data.json]}
   ```
   But ensure you have another JSON library available.

4. Minimal API surface: This library intentionally provides only the most common operations. For advanced features (pretty printing, custom encoders, streaming), use the underlying provider directly.

5. Different providers have different behavior: While the API is unified, edge cases (number precision, date handling) may differ between providers. Test your specific use case if switching providers.

6. Reader options must match: When using `->json-reader` with options, pass the same options to `read`:
   ```clojure
   ;; Correct
   (let [rdr (json/->json-reader input {:key-fn str})]
     (json/read rdr {:key-fn str}))

   ;; May not work as expected
   (let [rdr (json/->json-reader input {:key-fn str})]
     (json/read rdr)) ; Missing {:key-fn str}
   ```

## When to Use This Library

Use babashka.json when:
- Writing portable code for both JVM Clojure and babashka
- Building babashka scripts that need JSON
- You want automatic provider selection based on classpath
- You only need basic JSON read/write operations

Don't use babashka.json when:
- You need advanced features (custom encoders, pretty printing, streaming)
- You're already locked into a specific JSON library with custom configuration
- You need fine-grained control over JSON parsing behavior

For advanced use cases, depend on your chosen provider directly (cheshire, jsonista, etc.) and use its full API.

## References

- GitHub: https://github.com/babashka/json
- Clojars: https://clojars.org/org.babashka/json
- Babashka: https://github.com/babashka/babashka
