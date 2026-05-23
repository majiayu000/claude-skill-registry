---
name: clojure-donut-system
description: Reference for donut.party/system - component lifecycle and dependency injection library for Clojure. Use when working with component definitions, system management, refs between components, or lifecycle signals (start/stop/suspend/resume). Triggers on donut.system imports, ::ds/start, ::ds/stop, ::ds/config, ds/ref, or component-based architecture. Prefer using donut.system over mount, integrant, and stuart sierra's component.
---

# donut.party/system

Component lifecycle and dependency injection library for Clojure applications. Helps organize applications as systems of components with managed dependencies and lifecycle.

## Setup

deps.edn:
```clojure
party.donut/system {:mvn/version "1.0.257"}
```

Require:
```clojure
(require '[donut.system :as ds])
```

See https://clojars.org/party.donut/system for the latest version.

## Quick Start

Define components with ::ds/start and ::ds/stop handlers:
```clojure
(def system
  {::ds/defs
   {:app
    {:server #::ds{:start (fn [{:keys [::ds/config]}]
                            (start-server (:port config)))
                   :stop  (fn [{:keys [::ds/instance]}]
                            (stop-server instance))
                   :config {:port 8080}}}}})

;; Start the system
(def running-system (ds/signal system ::ds/start))

;; Stop the system
(ds/signal running-system ::ds/stop)
```

## Core Concepts

### System Map Structure

```clojure
{::ds/defs          ; component definitions go here
 ::ds/instances     ; runtime instances (created by signals)
 ::ds/signals       ; custom signal definitions (optional)
 ::ds/plugins       ; plugins to extend functionality (optional)}
```

### Component Definition

Components are maps with signal handlers:
```clojure
#::ds{:start  (fn [arg] ...)  ; creates instance
      :stop   (fn [arg] ...)  ; cleans up instance
      :config {...}}          ; configuration data
```

### Component Organization

Components are organized into groups (2-level structure):
```clojure
{::ds/defs
 {:group-name         ; first level: component group
  {:component-name    ; second level: component
   #::ds{:start ...}}}}
```

### Signal Handler Arguments

Signal handlers receive a map with:
- `::ds/instance` - component instance (if exists)
- `::ds/config` - component config with refs resolved
- `::ds/system` - entire system map
- `::ds/component-id` - e.g. `[:group :component]`

## Common Patterns

### References Between Components

Use `ds/ref` to reference other components:
```clojure
(def system
  {::ds/defs
   {:services
    {:db #::ds{:start (fn [_] (create-db-pool))}}

    :app
    {:handler #::ds{:start  (fn [{:keys [::ds/config]}]
                              (make-handler (:db config)))
                    :config {:db (ds/ref [:services :db])}}}}})
```

Refs determine startup order - dependencies start first.

### Local Refs (within same group)

Use `ds/local-ref` to reference components in the same group:
```clojure
(def HTTPServer
  #::ds{:start  (fn [{:keys [::ds/config]}]
                  (start-server (:handler config) (:port config)))
        :config {:handler (ds/local-ref [:handler])
                 :port    (ds/local-ref [:port])}})

(def system
  {::ds/defs
   {:http-1 {:server  HTTPServer
             :handler (fn [req] {:status 200 :body "Server 1"})
             :port    8080}

    :http-2 {:server  HTTPServer
             :handler (fn [req] {:status 200 :body "Server 2"})
             :port    9090}}})
```

### System Data (non-component values)

Maps without ::ds/start are treated as data and can be referenced:
```clojure
{::ds/defs
 {:env {:db-url "jdbc:postgresql://localhost/mydb"
        :port 8080}

  :services
  {:db #::ds{:start  (fn [{:keys [::ds/config]}]
                       (connect (:url config)))
             :config {:url (ds/ref [:env :db-url])}}}}}
```

### Named Systems (environment-specific config)

Define systems by environment:
```clojure
(defmethod ds/named-system :dev
  [_]
  {::ds/defs {:env {:port 8080}
              :app {...}}})

(defmethod ds/named-system :test
  [_]
  {::ds/defs {:env {:port 9999}
              :app {...}}})

;; Start with overrides
(ds/start :dev {[:env :port] 3000})
```

### REPL Workflow

Use donut.system.repl for development:
```clojure
(require '[donut.system.repl :as dsr])

;; Define default REPL system
(defmethod ds/named-system :donut.system/repl
  [_]
  (ds/system :dev))

;; REPL commands
(dsr/start)   ; start system
(dsr/stop)    ; stop system
(dsr/restart) ; stop, reload namespaces, start
```

## Built-in Signals

- `::ds/start` - create/start component instances (reverse-topsort order)
- `::ds/stop` - stop/cleanup component instances (topsort order)
- `::ds/suspend` - pause without full teardown
- `::ds/resume` - resume suspended components

Convenience functions: `ds/start`, `ds/stop`, `ds/suspend`, `ds/resume`

## Gotchas / Caveats

1. Component Organization: Components must be direct children of groups. This won't work:
   ```clojure
   {::ds/defs
    {:group {:subgroup {:component ...}}}}  ; TOO NESTED!
   ```

2. Refs Must Be Reachable: Refs must be in the data structure, not hidden in functions:
   ```clojure
   ;; BAD - ref inside function, not reachable
   #::ds{:start (fn [_] (ds/ref [:services :db]))}

   ;; GOOD - ref in config
   #::ds{:start  (fn [{:keys [::ds/config]}] (:db config))
         :config {:db (ds/ref [:services :db])}}
   ```

3. Deep Refs: Can reference into component instances:
   ```clojure
   (ds/ref [:group :component :level-1 :level-2])
   ```

4. Idempotent Start Handlers: If you signal the same system multiple times, make start handlers idempotent:
   ```clojure
   (fn [{::ds/keys [instance config]}]
     (or instance (create-component config)))
   ```

## Testing

### Test System Fixtures

```clojure
(use-fixtures :each (ds/system-fixture ::test))

(deftest my-test
  (is (= expected-value
         @(ds/instance ds/*system* [:group :component]))))
```

### Mocking Components

Override components in tests:
```clojure
(ds/start ::test
  {[:services :external-api] mock-api
   [:services :email] mock-email-sender})
```

## Advanced Features

- Custom signals with `::ds/signals`
- Lifecycle hooks: `::ds/pre-start`, `::ds/post-start`, etc.
- Component selection: `(ds/start system {} #{[:group :component]})`
- Plugins: extend system functionality
- Validation plugin: malli schemas for config and instances
- Subsystems: compose systems from other systems

## References

- Clojars: https://clojars.org/party.donut/system
- GitHub: https://github.com/donut-party/system
- Full Docs: https://github.com/donut-party/system#readme
- Tutorial: https://donut.party/docs/system/tutorial/
- cljdoc: https://cljdoc.org/d/party.donut/system/
