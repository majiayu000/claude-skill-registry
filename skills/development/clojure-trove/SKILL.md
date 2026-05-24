---
name: clojure-trove
description: Trove is a minimal logging facade for Clojure/Script supporting both traditional and structured logging. Use when writing libraries that need logging without forcing a backend choice, or when you need rich data-oriented logging with flexible filtering.
---

# Trove

A minimal, modern logging facade for Clojure/Script. It's a lightweight alternative to tools.logging, designed for library authors who want rich logging without forcing users to adopt a specific backend.

Trove supports both traditional string-based logging and structured data-oriented logging, with rich filtering capabilities (by namespace, id, level, data, etc.). It's tiny (1 macro, 0 deps, ~100 loc) and works with Clojure, ClojureScript, GraalVM, and Babashka.

## Setup

deps.edn:
```clojure
com.taoensso/trove {:mvn/version "1.1.0"}
```

Leiningen:
```clojure
[com.taoensso/trove "1.1.0"]
```

See https://clojars.org/com.taoensso/trove for the latest version.

## Quick Start

Library author usage (emitting logs):
```clojure
(ns my-library.core
  (:require [taoensso.trove :as trove]))

;; Traditional logging (string messages)
(trove/log! {:level :info, :msg "User logged in"})
(trove/log! {:level :warn, :msg "Connection retry attempt"})

;; Structured logging (data-oriented)
(trove/log! {:level :info
             :id :auth/login
             :data {:user-id 1234, :session-id "abc123"}
             :msg "User authenticated"})
```

Application user setup (choosing backend):
```clojure
(ns my-app.core
  (:require
   [taoensso.trove :as trove]
   [taoensso.trove.console] ; or .telemere, .timbre, .mulog, .tools-logging, .slf4j
   ))

;; Use default console backend (prints to *out* or js/console)
;; Default is already set, no action needed

;; Or switch to a different backend
(trove/set-log-fn! (taoensso.trove.telemere/get-log-fn))

;; Or disable all logging
(trove/set-log-fn! nil)
```

## Core Concepts

Trove is a facade - it provides a single logging API (`trove/log!`) that library authors use. Application users choose which backend handles those logs by setting `trove/*log-fn*`.

Key design features:
- Map-based API (same as Telemere)
- Automatic lazy evaluation of expensive data
- Backend-agnostic filtering
- Rich structured data support
- Zero runtime dependencies

## Logging API

### Basic Usage

The `log!` macro accepts a map of options:

```clojure
(trove/log!
  {:level :info        ; Required: :trace :debug :info :warn :error :fatal :report
   :id    :user/login  ; Optional: keyword identifier for this event
   :msg   "User login" ; Optional: human-readable message
   :data  {:user-id 42} ; Optional: structured data map
   :error ex})          ; Optional: exception/throwable
```

### Log Levels

Standard levels from least to most severe:
- `:trace` - Very detailed diagnostic info
- `:debug` - Debugging information
- `:info` - Informational messages (default)
- `:warn` - Warning messages
- `:error` - Error conditions
- `:fatal` - Critical failures
- `:report` - Special high-priority reports

### Traditional vs Structured Logging

Traditional (message-focused):
```clojure
(trove/log! {:level :info, :msg "Processing order #1234"})
(trove/log! {:level :error, :msg "Database connection failed", :error ex})
```

Structured (data-focused):
```clojure
(trove/log! {:level :info
             :id :order/process
             :data {:order-id 1234, :user-id 567, :total 99.99}})

(trove/log! {:level :error
             :id :db/connection-failed
             :data {:host "db.example.com", :port 5432}
             :error ex})
```

Structured logging is preferred because:
- Retains rich data types throughout pipeline
- Easier filtering and analysis
- Faster (avoid premature serialization)
- Better suited for databases and analytics tools

### Event IDs

Use keyword IDs to categorize events:
```clojure
;; Namespace-qualified keywords recommended
(trove/log! {:id :auth/login, :data {...}})
(trove/log! {:id :payment/success, :data {...}})
(trove/log! {:id ::order-complete, :data {...}}) ; Auto-namespaced

;; IDs enable powerful filtering
;; - Filter by ID prefix: :auth/*
;; - Track specific events
;; - Build metrics and dashboards
```

## Lazy Evaluation

Trove automatically delays expensive data, so backends can filter before paying computation costs:

```clojure
;; This expensive call only runs if the log passes filtering
(trove/log! {:level :debug
             :data (expensive-computation)})

;; Use :let for shared bindings across lazy args
(trove/log! {:level :info
             :let [result (expensive-call)]
             :msg (format-result result)
             :data (transform-result result)})
```

The `:let` bindings are only evaluated if the log passes filtering.

## Backend Configuration

### Available Backends

Trove includes adapters for common backends:

```clojure
;; Console (default) - prints to *out* or js/console
(require '[taoensso.trove.console])
(trove/set-log-fn! (taoensso.trove.console/get-log-fn))

;; Telemere - modern structured logging
(require '[taoensso.trove.telemere])
(trove/set-log-fn! (taoensso.trove.telemere/get-log-fn))

;; Timbre - popular Clojure logging
(require '[taoensso.trove.timbre])
(trove/set-log-fn! (taoensso.trove.timbre/get-log-fn))

;; μ/log - structured events
(require '[taoensso.trove.mulog])
(trove/set-log-fn! (taoensso.trove.mulog/get-log-fn))

;; tools.logging - Java interop
(require '[taoensso.trove.tools-logging])
(trove/set-log-fn! (taoensso.trove.tools-logging/get-log-fn))

;; SLF4J - Java interop
(require '[taoensso.trove.slf4j])
(trove/set-log-fn! (taoensso.trove.slf4j/get-log-fn))
```

### Console Backend Options

The default console backend supports filtering:

```clojure
;; Only log :warn and above
(trove/set-log-fn!
  (taoensso.trove.console/get-log-fn
    {:min-level :warn}))
```

### Dynamic Backend Switching

Use `binding` for temporary backend changes:

```clojure
;; Disable logging in tests
(binding [trove/*log-fn* nil]
  (run-tests))

;; Use custom backend in specific context
(binding [trove/*log-fn* my-custom-log-fn]
  (perform-operation))
```

## Writing Custom Backends

Implement a function matching the `*log-fn*` signature:

```clojure
(defn my-log-fn
  [ns coords level id lazy_]
  ;; ns     - String namespace, e.g. "my-app.utils"
  ;; coords - [line column] or nil
  ;; level  - Keyword: :trace :debug :info :warn :error :fatal :report
  ;; id     - Keyword or nil, e.g. :auth/login
  ;; lazy_  - Map or delayed map: {:keys [msg data error kvs]}

  ;; Force lazy_ to get the actual values
  (let [{:keys [msg data error kvs]} (force lazy_)]
    ;; Implement filtering
    (when (should-log? level id)
      ;; Perform logging side effects
      (send-to-backend {:level level :id id :msg msg :data data}))))

;; Configure it
(trove/set-log-fn! my-log-fn)
```

Key implementation notes:
- Force `lazy_` to access `:msg`, `:data`, `:error`, `:kvs`
- Implement filtering before forcing to avoid expensive computation
- The log-fn is called synchronously - use async/threading for expensive work
- Return value is ignored

## Advanced Options

### Custom Namespace and Coordinates

Override the defaults:

```clojure
(trove/log! {:level :info
             :ns "custom.namespace"
             :coords [100 50]
             :msg "Override defaults"})
```

### Custom Log Function Per Call

Use a different backend for specific logs:

```clojure
(trove/log! {:level :info
             :log-fn my-special-log-fn
             :msg "Uses custom backend"})
```

### Custom Key-Value Pairs

Pass additional data to your custom log-fn:

```clojure
(trove/log! {:level :info
             :msg "Custom event"
             :my-custom-key "value"
             :another-key 123})

;; Your log-fn receives these in the :kvs key
(defn my-log-fn [ns coords level id lazy_]
  (let [{:keys [kvs]} (force lazy_)]
    (println "Custom keys:" (:my-custom-key kvs))))
```

## Common Patterns

### Library Usage Pattern

As a library author, just use `trove/log!`:

```clojure
(ns my-library.api
  (:require [taoensso.trove :as trove]))

(defn process-data [data]
  (trove/log! {:level :debug
               :id ::process-start
               :data {:count (count data)}})
  (try
    (let [result (do-processing data)]
      (trove/log! {:level :info
                   :id ::process-complete
                   :data {:processed (count result)}})
      result)
    (catch Exception ex
      (trove/log! {:level :error
                   :id ::process-failed
                   :error ex
                   :data {:count (count data)}})
      (throw ex))))
```

Your users control the backend without changing your code.

### Application Setup Pattern

In your application entry point:

```clojure
(ns my-app.main
  (:require
   [taoensso.trove :as trove]
   [taoensso.trove.telemere]
   [my-library.api :as lib]))

(defn -main []
  ;; Configure logging backend once
  (trove/set-log-fn! (taoensso.trove.telemere/get-log-fn))

  ;; All libraries using Trove now log to Telemere
  (lib/process-data [...]))
```

### Conditional Logging

Use when expressions for conditional logic:

```clojure
(when (dev-mode?)
  (trove/log! {:level :debug
               :data (expensive-debug-info)}))

;; Or use level filtering in the backend
(trove/set-log-fn!
  (taoensso.trove.console/get-log-fn {:min-level :info}))
```

## Key Gotchas

1. Log-fn is synchronous: The `*log-fn*` runs on the calling thread. Implement async/backpressure for expensive operations in your log-fn.

2. Lazy evaluation: Values like `:data` and `:msg` may be wrapped in `delay`. Always `force` the `lazy_` argument in custom log-fns.

3. Backend setup timing: Set `*log-fn*` before any logging occurs. Do this early in application startup.

4. Nil log-fn: When `*log-fn*` is `nil`, all logging noops. This is intentional - useful for disabling logs.

5. Map required: The `log!` macro requires a compile-time map. Variables won't work:
   ```clojure
   ;; This works
   (trove/log! {:level :info, :msg "ok"})

   ;; This fails
   (let [opts {:level :info}]
     (trove/log! opts)) ; Compile error!
   ```

6. ClojureScript console: In ClojureScript, the console backend checks for `js/console` existence before logging.

## When to Use Trove

Use Trove when:
- Writing libraries that need logging
- You want structured logging without committing to a backend
- You need rich filtering capabilities
- You want ClojureScript compatibility
- You prefer a data-oriented logging API

Don't use Trove when:
- Writing an application (use Telemere, Timbre, etc. directly)
- You need advanced features like log appenders, formatting, rotation (use a full backend)
- You have no logging needs (obviously)

Trove is specifically designed for library authors. Application developers should typically use a full-featured backend directly.

## References

- GitHub: https://github.com/taoensso/trove
- API Docs: https://cljdoc.org/d/com.taoensso/trove/
- Clojars: https://clojars.org/com.taoensso/trove
- Slack: #trove on Clojurians Slack
- Related: [Telemere](https://www.taoensso.com/telemere) (full-featured backend using same API)
