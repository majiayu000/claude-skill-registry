---
name: clojure-aero
description: Aero is an EDN configuration library with reader tag extensions for profiles, environment variables, and references. Use when working with configuration files, environment-specific settings, or when you need explicit, intentful config management in Clojure.
---

# Aero

A small library for explicit, intentful configuration using EDN with powerful reader tag extensions.

## Setup

deps.edn:
```clojure
aero/aero {:mvn/version "1.1.6"}
```

Leiningen:
```clojure
[aero "1.1.6"]
```

See https://clojars.org/aero for the latest version.

## Quick Start

```clojure
(require '[aero.core :refer [read-config]])

;; Create config.edn:
;; {:greeting "World!"
;;  :port #profile {:default 8000
;;                  :dev 8001
;;                  :prod 80}}

;; Read from classpath (recommended)
(read-config (clojure.java.io/resource "config.edn"))
;; => {:greeting "World!", :port 8000}

;; Read with profile
(read-config (clojure.java.io/resource "config.edn") {:profile :dev})
;; => {:greeting "World!", :port 8001}
```

## Core Concepts

Aero reads EDN configuration files with special reader tags that allow:
- Profile-based configuration (dev/test/prod)
- Environment variable injection
- References to other config values
- File inclusion for modular configs
- Type coercion (string to long/double/keyword/boolean)
- Conditional logic based on hostname, user, etc.

Always use `io/resource` to read from classpath - works in both REPL and JAR files. Direct file paths like `(read-config "config.edn")` fail in JARs.

## Reader Tags

### #profile - Environment-specific values

```clojure
{:webserver
  {:port #profile {:default 8000
                   :dev 8001
                   :test 8002
                   :prod 80}}}

;; Usage:
(read-config "config.edn" {:profile :dev})
;; => {:webserver {:port 8001}}
```

### #env - Environment variables

```clojure
{:database-uri #env DATABASE_URI}

;; Reads from (System/getenv "DATABASE_URI")
```

### #envf - Format with environment variables

```clojure
{:database #envf ["protocol://%s:%s" DATABASE_HOST DATABASE_NAME]}

;; Builds string from multiple env vars
```

### #or - Provide defaults

```clojure
{:port #or [#env PORT 8080]
 :debug #boolean #or [#env DEBUG "true"]}

;; First available value wins, uses 8080 if PORT not set
```

### #ref - Reference other config values

```clojure
{:db-connection "datomic:dynamo://dynamodb"
 :webserver {:db #ref [:db-connection]}
 :analytics {:db #ref [:db-connection]}}

;; Both :webserver and :analytics get same db-connection value
;; References use get-in vector paths
```

### #include - Modular configs

```clojure
{:webserver #include "webserver.edn"
 :analytics #include "analytics.edn"}
```

By default resolves relative to parent config. Use custom resolver:

```clojure
(require '[aero.core :refer [resource-resolver root-resolver]])

;; Always resolve from classpath
(read-config "config.edn" {:resolver resource-resolver})

;; Or provide a map
(read-config "config.edn"
  {:resolver {"webserver.edn" "resources/webserver/config.edn"}})
```

### #join - String concatenation

```clojure
{:url #join ["jdbc:postgresql://psq-prod/prod?user="
             #env PROD_USER
             "&password="
             #env PROD_PASSWD]}
```

### #merge - Merge maps

```clojure
{:config #merge [{:foo :bar} {:foo :baz :qux 123}]}
;; => {:config {:foo :baz :qux 123}}
```

### Type coercion tags

```clojure
{:port #long #or [#env PORT "8080"]           ; Parse string to Long
 :factor #double #env FACTOR                   ; Parse to Double
 :mode #keyword #env MODE                      ; Parse to keyword
 :debug #boolean #or [#env DEBUG "true"]}      ; Parse to boolean
```

### #hostname - Host-specific config

```clojure
{:webserver
  {:port #hostname {"stone" 8080
                    #{"emerald" "diamond"} 8081
                    :default 8082}}}
```

### #user - User-specific config

Like #hostname but switches on the current user.

## Common Patterns

### Hide passwords in local files

Don't put secrets in version control or env vars. Use private files:

```clojure
{:secrets #include #join [#env HOME "/.secrets.edn"]

 :aws-secret-access-key
  #profile {:test #ref [:secrets :aws-test-key]
            :prod #ref [:secrets :aws-prod-key]}}
```

### Wrap config access in functions

```clojure
(ns myproj.config
  (:require [aero.core :as aero]
            [clojure.java.io :as io]))

(defn config [profile]
  (aero/read-config (io/resource "config.edn") {:profile profile}))

(defn webserver-port [config]
  (get-in config [:webserver :port]))

;; Usage in app:
(let [cfg (config :prod)]
  (start-server :port (webserver-port cfg)))
```

This insulates your code from config structure changes.

### Feature toggles

```clojure
{:features
  {:new-ui #profile {:default false
                     :dev true
                     :staging true
                     :prod false}}}
```

### Component integration

Pass config to components without boilerplate:

```clojure
(defn configure [system profile]
  (let [config (aero/read-config (io/resource "config.edn")
                                 {:profile profile})]
    (merge-with merge system config)))

(defn new-system [profile]
  (-> (new-system-map)
      (configure profile)
      (system-using (new-dependency-map))))
```

## Custom Reader Tags

Extend the reader multimethod for custom tags:

```clojure
(require '[aero.core :refer [reader]])

(defmethod reader 'mytag
  [{:keys [profile] :as opts} tag value]
  (if (= value :favorite)
    :chocolate
    :vanilla))

;; In config.edn:
;; {:flavor #mytag :favorite}
```

## Gotchas

1. File paths vs resources: Use `(io/resource "config.edn")` not `"config.edn"` to avoid JAR deployment failures

2. Environment variables for secrets: Don't use #env for passwords - they leak via `ps` and monitoring. Use #include with private files instead

3. Single config file: Keep one config file when possible - easier to manage and less duplication

4. #or evaluation order: Tags evaluate left to right, first non-nil wins

5. References are recursive: #ref works across #include boundaries

6. Profile is just a key: Can be any keyword - :dev, :prod, :staging, :local, etc.

## Advanced: Macro Tag Literals (Alpha)

For custom conditional constructs, use the alpha API:

```clojure
(ns myns
  (:require [aero.alpha.core :as aero.alpha]))

(defmethod aero.alpha/eval-tagged-literal 'myprofile
  [tagged-literal opts env ks]
  (aero.alpha/expand-case (:profile opts) tagged-literal opts env ks))
```

See README for #or implementation example.

## References

- GitHub: https://github.com/juxt/aero
- Clojars: https://clojars.org/aero
- API Docs: https://cljdoc.org/d/aero/aero/
- Community: #juxt channel on Clojurians Slack
- Extensions: https://github.com/monkey-projects/aero-ext
