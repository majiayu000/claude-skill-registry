---
name: clojure-hato
description: Modern HTTP client for Clojure wrapping JDK 11+ java.net.http. Use when working with HTTP requests, REST APIs, async HTTP calls, WebSockets, or needing HTTP/2 support.
---

# hato

Modern HTTP client for Clojure wrapping JDK 11's HttpClient with support for HTTP/1.1, HTTP/2, sync/async requests, and WebSockets.

Requires JDK 11 or above.

## Setup

deps.edn:
```clojure
hato/hato {:mvn/version "1.0.0"}
```

Leiningen:
```clojure
[hato/hato "1.0.0"]
```

Require:
```clojure
(require '[hato.client :as hc])
```

See https://clojars.org/hato/hato for the latest version.

## Quick Start

```clojure
;; Simple GET request
(hc/get "https://httpbin.org/get")
; => {:status 200, :body "{...}", :headers {...}, :request-time 112, ...}

;; POST with JSON
(hc/post "https://httpbin.org/post"
  {:form-params {:a 1 :b 2}
   :content-type :json})

;; GET with query params
(hc/get "https://httpbin.org/get"
  {:query-params {:q "search term" :page 1}})

;; Async request (returns CompletableFuture)
@(hc/get "https://httpbin.org/get" {:async? true})
```

## Core Concepts

Built-in client vs reusable client:
- Without `:http-client` option: creates single-use client per request
- With reusable client: connection pooling, persistent connections, better performance

Creating a reusable client:
```clojure
(def client (hc/build-http-client
              {:connect-timeout 10000
               :redirect-policy :normal}))

(hc/get "https://example.com" {:http-client client})
```

Response coercion with `:as`:
- `:string` (default) - returns body as string
- `:json` / `:json-string-keys` - parses JSON (requires cheshire)
- `:byte-array` - returns raw bytes
- `:stream` - returns java.io.InputStream
- `:auto` - auto-detects based on content-type

## Common Patterns

### Building a Reusable Client

```clojure
(def http-client
  (hc/build-http-client
    {:connect-timeout 10000        ; connection timeout (ms)
     :redirect-policy :normal       ; :never :normal :always
     :cookie-policy :all            ; :none :all :original-server
     :version :http-2}))            ; :http-1.1 :http-2

;; Use for all requests
(hc/get url {:http-client http-client})
```

### Sync vs Async Requests

```clojure
;; Synchronous - blocks until response
(hc/get "https://example.com")

;; Async - returns CompletableFuture
(let [future (hc/get "https://example.com" {:async? true})]
  @future)  ; deref to block for result

;; Async with callbacks
(hc/get "https://example.com"
  {:async? true}
  (fn [resp] (println "Success:" (:status resp)))  ; respond callback
  (fn [error] (println "Error:" error)))           ; raise callback
```

### Request with Headers and Auth

```clojure
;; Custom headers
(hc/get "https://api.example.com"
  {:headers {"x-api-key" "secret"
             "accept" "application/json"}})

;; Basic auth (preemptive)
(hc/get "https://api.example.com"
  {:basic-auth {:user "username" :pass "password"}})

;; OAuth bearer token
(hc/get "https://api.example.com"
  {:oauth-token "your-token-here"})
```

### Query Params and Form Data

```clojure
;; Query params (GET)
(hc/get "https://api.example.com/search"
  {:query-params {:q "clojure" :limit 10}})
; => GET /search?q=clojure&limit=10

;; Form-encoded POST
(hc/post "https://example.com/login"
  {:form-params {:username "user" :password "pass"}})
; => Content-Type: application/x-www-form-urlencoded

;; JSON POST
(hc/post "https://api.example.com/users"
  {:form-params {:name "Alice" :email "alice@example.com"}
   :content-type :json})
; => Content-Type: application/json
; => Body: {"name":"Alice","email":"alice@example.com"}
```

### Response Coercion

```clojure
;; Auto-parse JSON response (requires cheshire)
(hc/get "https://api.example.com/data" {:as :json})
; => {:status 200, :body {:key "value"}, ...}

;; Stream large responses
(with-open [stream (:body (hc/get url {:as :stream}))]
  (io/copy stream (io/file "output.bin")))

;; Get raw bytes
(hc/get "https://example.com/image.png" {:as :byte-array})
```

### Multipart File Upload

```clojure
(hc/post "https://example.com/upload"
  {:multipart [{:name "title" :content "My File"}
               {:name "file"
                :content (io/file "path/to/file.pdf")
                :filename "document.pdf"
                :content-type "application/pdf"}]})
```

### Error Handling

```clojure
;; By default, throws on 4xx/5xx status
(try
  (hc/get "https://example.com/notfound")
  (catch clojure.lang.ExceptionInfo e
    (let [{:keys [status body]} (ex-data e)]
      (println "Error" status body))))

;; Disable exception throwing
(let [{:keys [status body]} (hc/get url {:throw-exceptions? false})]
  (if (< status 400)
    (println "Success:" body)
    (println "Failed:" status)))
```

### WebSockets

```clojure
(require '[hato.websocket :as ws])

;; Create WebSocket connection (returns CompletableFuture)
(let [socket @(ws/websocket "ws://echo.websocket.events"
                {:on-message (fn [ws msg last?]
                               (println "Received:" msg))
                 :on-close (fn [ws status reason]
                             (println "Closed:" status reason))
                 :on-error (fn [ws error]
                             (println "Error:" error))})]
  ;; Send message
  @(ws/send! socket "Hello World!")

  ;; Close connection
  (ws/close! socket))
```

## Gotchas / Caveats

JDK 11+ Required: hato requires Java 11 or above. For older Java, use clj-http instead.

JSON/Transit Dependencies: Response coercion with `:as :json` or `:as :transit+json` requires optional dependencies:
- cheshire 5.9.0+ for JSON
- com.cognitect/transit-clj for Transit

Connection Pooling: Always create a reusable client with `build-http-client` for production use. Single-use clients (without `:http-client` option) don't pool connections.

Redirect Limit: Default max redirects is 5. Change with `-Djdk.httpclient.redirects.retrylimit=10`. Client returns 30x response with empty body when limit exceeded (no exception thrown).

Nested Query Params: Nested maps in `:query-params` are flattened by default:
```clojure
{:query-params {:a {:b {:c 5}}}}  ; => "a[b][c]=5"
```
Disable with `:ignore-nested-query-string true`.

Form Params: Nested maps in `:form-params` are NOT flattened by default. Enable with `:flatten-nested-form-params true`.

Default Timeout: Connection timeout is unlimited by default. Always set `:connect-timeout` for production:
```clojure
(hc/build-http-client {:connect-timeout 10000})  ; 10 seconds
```

Request Timeout: Per-request timeout with `:timeout` option (separate from connect-timeout):
```clojure
(hc/get url {:timeout 5000})  ; 5 second timeout for response
```

## Advanced Topics

For advanced features, see the GitHub repo and cljdoc:
- Custom middleware and request interceptors
- Client SSL/TLS certificate authentication
- Custom cookie handlers
- HTTP/2 server push
- Proxy configuration
- Custom thread executors

## References

- GitHub: https://github.com/gnarroway/hato
- API Docs: https://cljdoc.org/d/hato/hato/
- JavaDoc HttpClient: https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html
