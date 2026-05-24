---
name: Writing Clojure Docstrings
description: Guidelines for writing effective Clojure docstrings with markdown formatting, wikilinks, code examples, and tables. Always use this skill when writing or reviewing docstrings in Clojure code, or when asked about docstring formatting and style. Triggers on (1) writing new functions/vars/namespaces with docstrings, (2) updating existing docstrings, (3) questions about docstring best practices, (4) reviewing code with docstrings.

---

# Clojure Docstring Guidelines

Write clear, scannable docstrings using markdown formatting. All docstrings are interpreted as Markdown on cljdoc and Codox.

## Core Principles

### 1. Backtick-Quote Arguments and Keywords

Use backticks around function arguments and special keywords to improve readability:

```clojure
(defn conj!
  [coll x]
  "Adds `x` to the transient collection, and return `coll`. The 'addition'
   may happen at different 'places' depending on the concrete type."
  ,,,)
```

### 2. Link with [[Wikilinks]]

Cross-reference functions, namespaces, and Java classes using double-bracket syntax. Works in both Codex and cljdoc:

```clojure
(defn unlisten!
  "Removes registered listener from connection. See also [[listen!]]."
  [conn key]
  (swap! (:listeners (meta conn)) dissoc key))
```

For cross-namespace links, fully qualify:

```clojure
(defn my-func
  "Does something. See [[datascript.core/listen!]] for the underlying mechanism."
  [conn]
  ,,,)

(defn query
  "Executes query. See [[datascript.query]] namespace for details."
  [db q]
  ,,,)

(defn parse-instant
  "Parses timestamp string. Uses [[java.time.Instant]] internally."
  [s]
  ,,,)
```

### 3. Include Small Usage Examples

Show the function in context with code blocks:

```clojure
(defn register
  "Registers a dataloader controller with the application.

  Usage:

  ```clojure
  (def app
    (-> (app-state/constructor)
        (dataloader/register :current-user
          {:target [:user]
           :loader (fn [req]
                     (api/get-current-user))
           :params (fn [prev route]
                     true)})))
  ```

  The dataloader will automatically fetch data when params change."
  [app key config]
  ,,,)
```

### 4. Document Options Maps with Tables

Use markdown tables when a function accepts an options map with multiple keys:

```clojure
(defn router
  "Creates a router from raw route data and optionally options map.

  Options:

  | key              | description
  | -----------------|-------------
  | `:path`          | Base-path for routes
  | `:routes`        | Initial resolved routes (default `[]`)
  | `:data`          | Initial route data (default `{}`)
  | `:spec`          | Spec to validate route data (default `nil`)
  | `:syntax`        | Path parameter syntax (default `:bracket`)
  | `:expand`        | Function to expand route data (default `identity`)
  | `:coerce`        | Function to coerce parameters (default `nil`)
  | `:compile`       | Function to compile routes (default `identity`)
  | `:conflicts`     | Function to handle route conflicts (default `nil`)

  Example:

  ```clojure
  (router
    [[\"api\" {:middleware [wrap-api]}]
     [\"admin\" {:middleware [wrap-admin]}]]
    {:path \"/v1\"})
  ```"
  ([data]
   (router data nil))
  ([data opts]
   ,,,))
```

## Docstring Structure

For public functions, docstrings should contain these fields in order:

1. Complete sentence description (required)
2. Paragraphs/prose/explanation with markdown sections if needed (optional, best for namespaces)
3. Options enumeration using tables (required for public functions with options maps)
4. Examples (optional, only when necessary—skip for obvious things)

```clojure
(defn process-data
  "Processes incoming data and applies transformations.

  The processor validates input, applies filters based on `opts`, and
  returns transformed results. Invalid data is logged and skipped.

  Options:

  | key         | description
  |-------------|-------------
  | `:filters`  | Vector of filter functions to apply
  | `:validate` | Enable validation (default `true`)

  Example:

  ```clojure
  (process-data items {:filters [remove-nil remove-empty]
                       :validate true})
  ```"
  [items opts]
  ,,,)
```

For namespaces, use markdown sections with an optional "## Related Namespaces" section at the end:

```clojure
(ns myapp.data.query
  "Query execution and optimization.

  ## Query Processing

  Queries are parsed, optimized, and executed against the database.
  Use [[prepare-query]] to parse and validate before execution.

  ## Performance

  Query results are cached by default. See `:cache` option to disable.

  ## Related Namespaces

  - [[myapp.data.schema]] - Schema definitions
  - [[myapp.data.index]] - Index management")
```

For private functions, docstrings are optional. Add them only for complex/complicated functions, especially when defining input/output constraints:

```clojure
(defn- validate-config
  "Validates configuration map.

  Input: Map with required keys `:host`, `:port`, `:timeout`.
  Output: Validated config map or throws ExceptionInfo."
  [config]
  ,,,)
```

## Style Guidelines

- Start docstrings with complete sentence
- Be matter of fact and just-long-enough, not overly terse
- Skip markdown bold formatting (`**text**`) entirely
- Dry, sardonic humor is acceptable when it actually clarifies something (rarely)
- Focus on what the function does, not obvious implementation details

## Notable Examples

Projects with exemplary docstring work:

- [Rum](https://cljdoc.org/d/rum/rum/0.11.3/api/rum.core)
- [Datascript](https://cljdoc.org/d/datascript/datascript/0.17.1/api/datascript.core)

Credit: Content adapted from [4 Small Steps Towards Awesome Clojure Docstrings](https://www.martinklepsch.org/posts/writing-awesome-docstrings) by Martin Klepsch.
