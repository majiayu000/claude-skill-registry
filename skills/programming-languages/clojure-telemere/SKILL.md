---
name: clojure-telemere
description: Structured telemetry library for Clojure/Script. Use when working with logging, tracing, structured logging, events, signal handling, observability, or replacing Timbre/tools.logging.
---

# Telemere

Telemere is a next-generation structured telemetry library for Clojure/Script. It provides one unified API for traditional logging, structured logging, tracing, and basic performance monitoring.

## Setup

deps.edn:
```clojure
com.taoensso/telemere {:mvn/version "1.2.1"}
```

Leiningen:
```clojure
[com.taoensso/telemere "1.2.1"]
```

See https://clojars.org/com.taoensso/telemere for the latest version.

Namespace setup:
```clojure
(ns my-app
  (:require [taoensso.telemere :as tel]))
```

## Quick Start

Telemere works out-of-the-box with no config needed. Signals print to console by default:

```clojure
(require '[taoensso.telemere :as tel])

;; Traditional logging (string messages)
(tel/log! {:level :info, :msg "User logged in!"})

;; Structured logging (explicit id and data)
(tel/log! {:level :info, :id :auth/login, :data {:user-id 1234}})

;; Mixed style (id, data, and message)
(tel/log! {:level :info
           :id :auth/login
           :data {:user-id 1234}
           :msg "User logged in!"})

;; Trace execution with runtime tracking
(tel/trace! {:id ::my-id :data {:step "processing"}}
  (do-some-work))

;; Check signal content for debugging
(tel/with-signal (tel/log! {...})) ; => {:keys [ns level id data msg_ ...]}
```

## Core Signal Creators

Telemere provides multiple signal creators optimized for different use cases. All accept an opts map:

| Function | Quick Args | Returns | Use Case |
|----------|-----------|---------|----------|
| `log!` | `[?level msg]` | nil | Traditional log messages |
| `event!` | `[id ?level]` | nil | Structured events |
| `trace!` | `[?id form]` | form result | Trace execution + timing |
| `spy!` | `[?level form]` | form result | Debug form values |
| `error!` | `[?id error]` | error | Log errors |
| `catch->error!` | `[?id form]` | value or fallback | Catch & log errors |
| `signal!` | `[opts]` | depends | Low-level, full control |

Examples:
```clojure
;; log! - for messages
(tel/log! "Simple message")
(tel/log! :warn "Warning message")
(tel/log! {:level :info, :data {:x 1}} "Message with data")

;; event! - for structured events
(tel/event! ::user-login)
(tel/event! ::user-login :info)
(tel/event! ::user-login {:level :info, :data {:user-id 42}})

;; trace! - tracks runtime and return value
(tel/trace! (expensive-operation))
(tel/trace! ::complex-op (multi-step-process))

;; spy! - debug form values
(tel/spy! (+ 1 2)) ; => 3, logs the value

;; error! - log errors
(try
  (risky-operation)
  (catch Exception e
    (tel/error! e)))

;; catch->error! - automatic error handling
(tel/catch->error! ::my-op
  (risky-operation)) ; returns value or nil on error
```

## Signal Options

All signal creators accept a map of options:

```clojure
(tel/log!
  {:level :debug
   :id    ::my-id

   ;; Filtering
   :sample 0.75          ; 75% sampling (noop 25% of time)
   :when   (enabled?)    ; conditional execution
   :limit  {"1/sec" [1 1000]
            "5/min" [5 60000]}

   ;; Data and execution
   :let    [x (expensive-calc)]  ; lazy bindings
   :data   {:result x}           ; structured data
   :do     (inc-metric!)         ; side effects

   ;; Context
   :ctx    {:user-id 123}        ; arbitrary context
   :parent trace-parent}         ; tracing parent

  "Message using bindings")
```

Key options:
- `:level` - `:trace`, `:debug`, `:info` (default), `:warn`, `:error`, `:fatal`, or integer
- `:id` - qualified keyword for identifying this signal type
- `:data` - structured data map (preserved as data)
- `:msg` - message string or vector to join
- `:let` - bindings available to `:data` and `:msg`
- `:sample` - random sampling rate (0.0 to 1.0)
- `:when` - conditional execution
- `:limit` - rate limiting map
- `:do` - side effects to execute when signal is created

## Filtering

Filtering happens at multiple stages for efficiency:

```clojure
;; Set minimum level globally
(tel/set-min-level! :warn)  ; All signals
(tel/set-min-level! :log :debug)  ; Just log! signals

;; Filter by namespace patterns
(tel/set-ns-filter! {:disallow "taoensso.*" :allow "taoensso.sente.*"})

;; Filter by ID patterns
(tel/set-id-filter! {:allow #{::my-id "my-app/*"}})

;; Set level per namespace pattern
(tel/set-min-level! :log "taoensso.sente.*" :warn)

;; Transform signals (can modify or filter)
(tel/set-xfn!
  (fn [signal]
    (if (-> signal :data :skip-me?)
      nil  ; Filter out
      (assoc signal :enriched true))))

;; Dynamic context overrides
(tel/with-min-level :trace
  (tel/log! {:level :debug} "This will log"))
```

Filtering is O(1) except for rate limits (O(n-windows)). Compile-time filtering can completely elide signal calls for zero overhead.

## Signal Handlers

Handlers process created signals (write to console, file, DB, etc.):

```clojure
;; Add custom handler
(tel/add-handler! :my-handler
  (fn [signal] (println "Got signal:" (:id signal))))

;; Add handler with filtering and async dispatch
(tel/add-handler! :my-handler
  (fn
    ([signal] (save-to-db signal))
    ([] (close-db-connection)))  ; Called on shutdown

  {:async {:mode :dropping
           :buffer-size 1024
           :n-threads 1}
   :priority 100
   :min-level :info
   :sample 0.5
   :ns-filter {:disallow "noisy.namespace.*"}
   :limit {"1/sec" [1 1000]}})

;; View current handlers
(tel/get-handlers)

;; Handler statistics
(tel/get-handlers-stats)

;; Remove handler
(tel/remove-handler! :my-handler)

;; Stop all handlers (IMPORTANT: call on shutdown!)
(tel/stop-handlers!)
```

### Included Handlers

Console handlers (output as formatted text, edn, or JSON):
```clojure
;; Human-readable text (default)
(tel/add-handler! :console
  (tel/handler:console
    {:output-fn (tel/format-signal-fn {})}))

;; EDN output
(tel/add-handler! :console-edn
  (tel/handler:console
    {:output-fn (tel/pr-signal-fn {:pr-fn :edn})}))

;; JSON output (Clj needs JSON library)
(require '[jsonista.core :as json])
(tel/add-handler! :console-json
  (tel/handler:console
    {:output-fn (tel/pr-signal-fn
                  {:pr-fn json/write-value-as-string})}))
```

Other included handlers:
- `handler:file` - Write to files (Clj only)
- `handler:postal` - Email via Postal (Clj only)
- `handler:slack` - Slack notifications (Clj only)
- `handler:tcp-socket` / `handler:udp-socket` - Network sockets (Clj only)
- `handler:open-telemetry` - OpenTelemetry integration (Clj only)

## Interop

### SLF4J (Java Logging)

1. Add dependencies:
   - `org.slf4j/slf4j-api` (v2+)
   - `com.taoensso/telemere-slf4j`

2. SLF4J calls automatically become Telemere signals

Verify: `(tel/check-interop)` => `{:slf4j {:telemere-receiving? true}}`

### tools.logging

1. Add `org.clojure/tools.logging` dependency
2. Call `(tel/tools-logging->telemere!)` or set env config

Verify: `(tel/check-interop)` => `{:tools-logging {:telemere-receiving? true}}`

### System Streams

Redirect `System/out` and `System/err` to Telemere:
```clojure
(tel/streams->telemere!)
```

### OpenTelemetry

See [references/config.md](references/config.md#opentelemetry) for OpenTelemetry integration.

## Common Patterns

### Message Building

```clojure
;; Fixed message
(tel/log! "User logged in")

;; Joined message vector
(tel/log! ["User" user-id "logged in"])

;; With preprocessing
(tel/log!
  {:let [username (str/upper-case raw-name)
         balance  (parse-double raw-balance)]
   :data {:username username
          :balance balance}}
  ["User" username "balance:" (format "$%.2f" balance)])
```

### Tracing Nested Operations

```clojure
(defn process-order [order-id]
  (tel/trace! {:id ::process-order :data {:order-id order-id}}
    (let [order (fetch-order order-id)
          _     (tel/trace! {:id ::validate-order}
                  (validate-order order))
          _     (tel/trace! {:id ::charge-payment}
                  (charge-payment order))]
      (ship-order order))))
```

### Dynamic Context

```clojure
;; Set context for all signals in scope
(tel/with-ctx {:request-id request-id
               :user-id user-id}
  (tel/log! {:id ::processing} "Started")
  (process-request)
  (tel/log! {:id ::complete} "Done"))
```

### Error Handling

```clojure
;; Simple error logging
(try
  (risky-op)
  (catch Exception e
    (tel/error! ::operation-failed e)))

;; Automatic error catching with fallback
(tel/catch->error! ::fetch-user
  {:catch-val {:id nil :name "Guest"}}
  (fetch-user-from-db user-id))
```

## Key Gotchas

1. **Always call `stop-handlers!`** on shutdown to flush buffers and close resources. Use `tel/call-on-shutdown!` for JVM shutdown hooks.

2. **Signals are filtered before creation** - data in `:let`, `:data`, `:msg`, `:do` is only evaluated if the signal passes filters.

3. **Handler filters are additive** - handlers can be MORE restrictive than call filters, not less.

4. **Messages are lazy** - message building only happens if the signal is created and handled.

5. **`:error` value != `:error` level** - signals can have error values at any level, and vice versa.

6. **Cache validators** - use `tel/validator`, `tel/decoder`, etc. once, not per signal.

## Performance

Telemere is highly optimized:
- Filtered signals: ~350 nsecs/call
- Compile-time elision: 0 nsecs (completely removed)
- Handler dispatch is typically async with backpressure control

Tips for performance:
- Use compile-time filtering for hot paths
- Use sampling for high-volume signals
- Use rate limiting for expensive operations
- Cache validators/transformers outside signal calls

## Detailed References

- [Getting Started](references/getting-started.md) - Setup, usage, default config
- [Architecture](references/architecture.md) - How signal flow works
- [Config](references/config.md) - Filtering, handlers, interop configuration
- [Handlers](references/handlers.md) - Writing and configuring handlers
- [FAQ](references/faq.md) - Common questions (vs Timbre, vs μ/log, etc.)
- [Tips](references/tips.md) - Best practices for observable systems

## External References

- GitHub: https://github.com/taoensso/telemere
- Wiki: https://github.com/taoensso/telemere/wiki
- API Docs: https://cljdoc.org/d/com.taoensso/telemere/
- Slack: https://www.taoensso.com/telemere/slack

## Internal Help

Telemere includes extensive docstrings accessible from your REPL:
- `tel/help:signal-creators` - Creating signals
- `tel/help:signal-options` - All signal options
- `tel/help:signal-content` - Signal map content
- `tel/help:filters` - Filtering and transformations
- `tel/help:handlers` - Handler management
- `tel/help:handler-dispatch-options` - Handler dispatch configuration
- `tel/help:environmental-config` - JVM/env/classpath configuration
