---
name: clojure-ring-jetty-adapter
description: |
  Ring Jetty adapter for running ring-compatible web servers in Clojure. Use when you are working with ring and jetty starting and need to know to configure or interact with a ring jetty
---

# Ring Jetty Adapter

The Ring Jetty adapter runs Ring handlers on an embedded Jetty 12 server. It's Ring-compatible and supports HTTP, HTTPS, WebSockets, and Unix domain sockets.

## Setup

deps.edn:
```clojure
ring/ring-jetty-adapter {:mvn/version "1.15.3"}
```

Leiningen:
```clojure
[ring/ring-jetty-adapter "1.15.3"]
```

See https://clojars.org/ring/ring-jetty-adapter for the latest version.

## Quick Start

Basic synchronous handler:
```clojure
(require '[ring.adapter.jetty :refer [run-jetty]])

(defn handler [request]
  {:status 200
   :headers {"Content-Type" "text/html"}
   :body "Hello World"})

(run-jetty handler {:port 3000})
```

Non-blocking server for REPL:
```clojure
;; Set :join? false to return control to REPL
(def server (run-jetty handler {:port 3000 :join? false}))
```

# Server Lifecycle

## Starting a Server

`run-jetty` returns a `org.eclipse.jetty.server.Server` instance:
```clojure
(def server (run-jetty handler {:port 3000 :join? false}))
```

With `:join? true` (default), the function blocks until the server stops. With `:join? false`, it returns immediately.

## Stopping a Server

Call `.stop` on the server instance:
```clojure
(.stop server)
```

Or use it in a component lifecycle library:
```clojure
;; Component/Integrant/Mount pattern
(defn start-server [handler config]
  (run-jetty handler (merge config {:join? false})))

(defn stop-server [server]
  (.stop server))
```

## Graceful Shutdown

The server stops gracefully by default, completing in-flight requests:
```clojure
(.stop server)  ; Waits for current requests to complete
```

# Basic Configuration

## Port and Host

```clojure
(run-jetty handler
  {:port 3000          ; Listen port (default 80)
   :host "localhost"}) ; Listen host (default all interfaces)
```

## Thread Pool

Control worker threads:
```clojure
(run-jetty handler
  {:min-threads 8       ; Minimum threads (default 8)
   :max-threads 50      ; Maximum threads (default 50)
   :thread-idle-timeout 60000  ; Thread idle timeout in ms (default 60000)
   :max-queued-requests 100})  ; Max queued requests (default Integer/MAX_VALUE)
```

Use daemon threads (useful for testing):
```clojure
(run-jetty handler {:daemon? true})
```

Custom thread pool:
```clojure
(import '[java.util.concurrent Executors])

(run-jetty handler
  {:thread-pool (Executors/newVirtualThreadPerTaskExecutor)}) ; Java 19+
```

## Connection Configuration

```clojure
(run-jetty handler
  {:max-idle-time 200000        ; Connection idle timeout in ms (default 200000)
   :acceptor-threads 2          ; Number of acceptor threads (default -1, auto)
   :selector-threads 4})        ; Number of selector threads (default -1, auto)
```

## HTTP Configuration

```clojure
(run-jetty handler
  {:output-buffer-size 32768     ; Response buffer size (default 32768)
   :request-header-size 8192     ; Max request header size (default 8192)
   :response-header-size 8192    ; Max response header size (default 8192)
   :send-date-header? true       ; Include Date header (default true)
   :send-server-version? true})  ; Include Server header (default true)
```

# SSL/HTTPS Configuration

## Basic SSL

```clojure
(run-jetty handler
  {:ssl? true                    ; Enable SSL
   :ssl-port 443                 ; SSL port (default 443, implies :ssl? true)
   :keystore "path/to/keystore.jks"
   :key-password "password"})
```

## Advanced SSL Options

```clojure
(run-jetty handler
  {:ssl-port 8443
   :keystore "keystore.jks"       ; Path to keystore or KeyStore instance
   :keystore-type "jks"           ; Keystore type (default "jks")
   :key-password "secret"
   :truststore "truststore.jks"   ; Optional truststore
   :trust-password "secret"
   :client-auth :need})           ; :need, :want, or :none (default :none)
```

Using an SSLContext directly:
```clojure
(import '[javax.net.ssl SSLContext])

(run-jetty handler
  {:ssl-port 8443
   :ssl-context (SSLContext/getInstance "TLS")})
```

## SSL Cipher and Protocol Control

```clojure
(run-jetty handler
  {:ssl? true
   :keystore "keystore.jks"
   :key-password "secret"
   :exclude-ciphers ["SSL_RSA_WITH_DES_CBC_SHA"]
   :exclude-protocols ["SSLv3" "TLSv1"]
   :replace-exclude-ciphers? false    ; false = add to defaults (default)
   :replace-exclude-protocols? false  ; true = replace defaults
   :sni-host-check? true})            ; SNI hostname check (default true)
```

## Keystore Auto-Reload

Automatically reload keystore when it changes:
```clojure
(run-jetty handler
  {:ssl? true
   :keystore "keystore.jks"
   :key-password "secret"
   :keystore-scan-interval 60})  ; Check every 60 seconds
```

# HTTP and HTTPS Together

Run both HTTP and HTTPS:
```clojure
(run-jetty handler
  {:port 8080        ; HTTP port
   :ssl-port 8443    ; HTTPS port
   :keystore "keystore.jks"
   :key-password "secret"})
```

Disable HTTP (HTTPS only):
```clojure
(run-jetty handler
  {:http? false      ; Disable HTTP
   :ssl-port 8443
   :keystore "keystore.jks"
   :key-password "secret"})
```

# WebSockets

Ring 1.11+ supports WebSockets through the `ring.websocket` namespace.

Basic WebSocket handler:
```clojure
(require '[ring.websocket :as ws])

(defn ws-handler [request]
  (if (ws/upgrade-request? request)
    {::ws/listener
     {:on-open
      (fn [socket]
        (ws/send socket "Welcome!"))
      :on-message
      (fn [socket message]
        (ws/send socket (str "Echo: " message)))
      :on-close
      (fn [socket code reason]
        (println "Closed:" code reason))}}
    {:status 426
     :body "WebSocket upgrade required"}))

(run-jetty ws-handler {:port 3000 :join? false})
```

## WebSocket Listener Events

All available events:
```clojure
{::ws/listener
 {:on-open    (fn [socket] ...)                    ; WebSocket opened
  :on-message (fn [socket message] ...)            ; Message received (String or ByteBuffer)
  :on-ping    (fn [socket buffer] ...)             ; PING received (optional)
  :on-pong    (fn [socket buffer] ...)             ; PONG received
  :on-error   (fn [socket throwable] ...)          ; Error occurred
  :on-close   (fn [socket code reason] ...)}}      ; WebSocket closed
```

## WebSocket Socket Operations

Send messages:
```clojure
;; Synchronous send
(ws/send socket "text message")
(ws/send socket byte-array)
(ws/send socket byte-buffer)

;; Asynchronous send with callbacks
(ws/send socket "message"
  (fn [] (println "Success"))
  (fn [ex] (println "Failed:" ex)))
```

Ping/pong:
```clojure
(ws/ping socket)              ; Send PING
(ws/ping socket byte-buffer)  ; PING with data
(ws/pong socket)              ; Send unsolicited PONG
(ws/pong socket byte-buffer)  ; PONG with data
```

Close connection:
```clojure
(ws/close socket)                    ; Normal close
(ws/close socket 1000 "Goodbye")     ; Close with code and reason
(ws/open? socket)                    ; Check if open
```

## WebSocket Configuration

Configure WebSocket limits:
```clojure
(run-jetty ws-handler
  {:port 3000
   :ws-idle-timeout 30000      ; Idle timeout in ms (default 30000)
   :ws-max-text-size 65536     ; Max text message size in bytes (default 65536)
   :ws-max-binary-size 65536}) ; Max binary message size in bytes (default 65536)
```

## WebSocket Subprotocols

Specify accepted subprotocol:
```clojure
(defn ws-handler [request]
  (if (ws/upgrade-request? request)
    {::ws/listener {...}
     ::ws/protocol "my-protocol"}  ; Accepted subprotocol
    {:status 426 :body "WebSocket upgrade required"}))
```

# Async Handlers

For async/streaming handlers, use `:async? true`:
```clojure
(defn async-handler [request respond raise]
  (future
    (try
      (respond {:status 200 :body "Async response"})
      (catch Exception e
        (raise e)))))

(run-jetty async-handler
  {:async? true
   :async-timeout 30000          ; Timeout in ms (default 0, no timeout)
   :async-timeout-handler         ; Optional timeout handler
   (fn [request respond raise]
     (respond {:status 408 :body "Request timeout"}))})
```

The async handler receives three arguments:
- `request` - the Ring request map
- `respond` - function to call with response map
- `raise` - function to call with exception

# Unix Domain Sockets

Listen on a Unix domain socket:
```clojure
(run-jetty handler
  {:unix-socket "/tmp/my-app.sock"})
```

The socket file is automatically deleted on JVM exit.

# Advanced Configuration

## Custom Server Configuration

Use `:configurator` for direct server access:
```clojure
(run-jetty handler
  {:port 3000
   :configurator
   (fn [^org.eclipse.jetty.server.Server server]
     ;; Direct Jetty configuration
     (.setStopAtShutdown server true)
     (.setStopTimeout server 5000))})
```

## Example: Production Configuration

```clojure
(defn start-production-server [handler]
  (run-jetty handler
    {:port 8080
     :host "0.0.0.0"
     :join? false
     :min-threads 10
     :max-threads 100
     :max-queued-requests 1000
     :max-idle-time 300000
     :send-server-version? false  ; Don't leak server version
     :configurator
     (fn [server]
       (.setStopAtShutdown server true)
       (.setStopTimeout server 30000))}))
```

# Common Patterns

## Component Lifecycle

Using with component libraries:
```clojure
;; Stuart Sierra's Component
(defrecord WebServer [handler port server]
  component/Lifecycle
  (start [this]
    (if server
      this
      (assoc this :server
        (run-jetty handler {:port port :join? false}))))
  (stop [this]
    (when server
      (.stop server))
    (assoc this :server nil)))

;; Integrant
(defmethod ig/init-key :adapter/jetty [_ {:keys [handler options]}]
  (run-jetty handler (merge options {:join? false})))

(defmethod ig/halt-key! :adapter/jetty [_ server]
  (.stop server))
```

## REPL Development

For interactive development:
```clojure
(defonce server (atom nil))

(defn start! []
  (reset! server
    (run-jetty #'app {:port 3000 :join? false})))

(defn stop! []
  (when @server
    (.stop @server)
    (reset! server nil)))

(defn restart! []
  (stop!)
  (start!))
```

Using `#'app` (var instead of function) allows reloading handler without restart.

## Production Deployment

For production as an uberjar:
```clojure
(ns myapp.main
  (:require [ring.adapter.jetty :refer [run-jetty]])
  (:gen-class))

(defn -main [& args]
  (let [port (Integer/parseInt (or (System/getenv "PORT") "8080"))]
    (run-jetty handler {:port port})))
```

In project.clj:
```clojure
{:profiles
 {:uberjar
  {:aot :all
   :main myapp.main}}}
```

Build and run:
```bash
lein uberjar
PORT=8080 java -jar target/myapp-standalone.jar
```

# Key Gotchas

## Join Behavior

By default `:join? true` blocks forever. Always use `:join? false` in:
- REPL sessions
- Component lifecycle systems
- Tests
- Any context where you need control flow to continue

## Thread Pool Sizing

Default thread pool (8-50 threads) is conservative. For high-concurrency apps:
```clojure
{:min-threads 50
 :max-threads 200
 :max-queued-requests 5000}
```

For async handlers or virtual threads (Java 19+), fewer threads needed.

## WebSocket Upgrade Check

Always check `ws/upgrade-request?` before returning WebSocket response:
```clojure
(defn handler [request]
  (if (ws/upgrade-request? request)
    {::ws/listener {...}}
    {:status 426 :body "WebSocket upgrade required"}))
```

## SSL Client Authentication

`:client-auth` options:
- `:none` (default) - no client cert required
- `:want` - request client cert, optional
- `:need` - require client cert, connection fails without it

## Server Version Header

Set `:send-server-version? false` in production to avoid leaking Jetty version.

# Comparison with http-kit

vs http-kit server:
- Jetty: Mature, battle-tested, feature-rich, heavier (~10MB with deps)
- http-kit: Lightweight (~90KB), fast, zero dependencies, simpler API
- Jetty: Better SSL/TLS configurability
- http-kit: Built-in HTTP client (Jetty is server-only)
- Both: Ring-compatible, WebSocket support, production-ready

Choose Jetty for:
- Complex SSL requirements
- Need servlet features
- Already using Jetty infrastructure

Choose http-kit for:
- Minimal dependencies
- High concurrency with low memory
- Need both client and server
- Simpler deployment

# References

- Ring Wiki: https://github.com/ring-clojure/ring/wiki
- API Docs: https://cljdoc.org/d/ring/ring-jetty-adapter/
- Jetty Documentation: https://www.eclipse.org/jetty/documentation/
