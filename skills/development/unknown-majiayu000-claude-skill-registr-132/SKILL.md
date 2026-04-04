---
name: http-kit
description: http-kit is a HTTP client and server for Clojure with Ring compatibility. Use when working with http-kit client or server
---

# http-kit

Simple, high-performance event-driven HTTP client+server for Clojure.

http-kit uses an event-driven, non-blocking I/O model. It's Ring-compatible, has zero dependencies, and is ~90kB with ~3k lines of code.

## Setup

deps.edn:
```clojure
http-kit/http-kit {:mvn/version "2.8.1"}
```

Leiningen:
```clojure
[http-kit/http-kit "2.8.1"]
```

See https://clojars.org/http-kit/http-kit for the latest version.

## Quick Start

Server:
```clojure
(require '[org.httpkit.server :as hk-server])

(defn app [req]
  {:status 200
   :headers {"Content-Type" "text/html"}
   :body "hello HTTP!"})

(def server (hk-server/run-server app {:port 8080}))

;; Stop server
(server) ; immediate shutdown
(server :timeout 100) ; graceful shutdown
```

Client:
```clojure
(require '[org.httpkit.client :as hk-client])

;; Promise-based (async)
(def resp-promise (hk-client/get "http://example.com"))
@resp-promise ; block for result

;; Callback-based (async)
(hk-client/get "http://example.com"
  (fn [{:keys [status headers body error]}]
    (if error
      (println "Failed:" error)
      (println "Success:" status))))
```

# Server

## Basic Handler

Ring-compatible handler:
```clojure
(defn app [req]
  {:status 200
   :headers {"Content-Type" "application/json"}
   :body "{\"message\": \"Hello\"}"})
```

## Server Options

```clojure
(hk-server/run-server app
  {:port 8080
   :ip "0.0.0.0"
   :thread 4                           ; worker threads
   :queue-size 20480                   ; request queue size
   :max-body 8388608                   ; max request body size (bytes)
   :max-line 4096                      ; max HTTP line size
   :legacy-unsafe-remote-addr? false   ; secure remote-addr (see below)
   :legacy-content-length? false})     ; respect handler Content-Length
```

## WebSockets

Two APIs available: http-kit's unified API (works for both WebSocket and long-polling) and Ring's WebSocket API.

Using http-kit's unified API:
```clojure
(def channels (atom #{}))

(defn on-open    [ch]             (swap! channels conj ch))
(defn on-close   [ch status-code] (swap! channels disj ch))
(defn on-receive [ch message]
  (doseq [ch @channels]
    (hk-server/send! ch (str "Broadcasting: " message))))

(defn ws-handler [ring-req]
  (if-not (:websocket? ring-req)
    {:status 200 :body "WebSocket endpoint"}
    (hk-server/as-channel ring-req
      {:on-open    on-open
       :on-receive on-receive
       :on-close   on-close})))
```

Using Ring's WebSocket API:
```clojure
(require '[ring.websocket :as ws])

(def sockets (atom #{}))

(defn on-open    [ch]                    (swap! sockets conj ch))
(defn on-close   [ch status-code reason] (swap! sockets disj ch))
(defn on-message [ch message]
  (doseq [ch @sockets]
    (ws/send ch (str "Broadcasting: " message))))

(defn ws-handler [ring-req]
  (if-not (:websocket? ring-req)
    {:status 200 :body "WebSocket endpoint"}
    {::ws/listener
     {:on-open    on-open
      :on-message on-message
      :on-close   on-close}}))
```

Sending to WebSocket (unified API):
```clojure
(hk-server/send! channel "message")        ; returns true on success
(hk-server/send! channel "message" false)  ; false = don't close after send
(hk-server/close channel)                  ; explicitly close connection
```

Key differences between APIs:
- Unified API works with both WebSockets and HTTP long-polling
- Unified API: detect send success via return value
- Ring API: detect send success via callbacks
- Ring API provides close reason (though often empty in practice)

## Streaming Responses

Use `as-channel` for HTTP streaming:
```clojure
(defn streaming-handler [req]
  (hk-server/as-channel req
    {:on-open (fn [ch]
                (hk-server/send! ch {:status 200
                                    :headers {"Content-Type" "text/plain"}
                                    :body ""} false)
                (future
                  (dotimes [i 10]
                    (Thread/sleep 1000)
                    (hk-server/send! ch (str "Chunk " i "\n") false))
                  (hk-server/close ch)))}))
```

# Client

## Promise-Based Requests

Returns immediately with a promise (after DNS lookup):
```clojure
;; GET request
(def resp (hk-client/get "http://example.com"))
@resp  ; block for result
(deref resp 5000 :timeout) ; timeout after 5s

;; Concurrent requests
(let [r1 (hk-client/get "http://example.com")
      r2 (hk-client/get "http://other.com")]
  (println (:status @r1))
  (println (:status @r2)))
```

## Callback-Based Requests

```clojure
(hk-client/get "http://example.com"
  {:timeout 200
   :basic-auth ["user" "pass"]
   :headers {"X-Custom" "value"}}
  (fn [{:keys [status headers body error opts]}]
    (if error
      (println "Failed:" error)
      (println "Success:" status))))
```

## Request Options

All HTTP methods support these options:
```clojure
(hk-client/request
  {:url "http://example.com/api"
   :method :post  ; :get :post :put :delete :head :patch
   :headers {"X-Api-Key" "secret"}
   :query-params {"q" "search term"}
   :form-params {"key" "value"}        ; form-encoded body
   :body (json/encode {:key "value"})  ; raw body (e.g., JSON)

   :basic-auth ["user" "pass"]
   :oauth-token "token"
   :user-agent "MyApp/1.0"

   :timeout 1000     ; connection + read timeout (ms)
   :keepalive 30000  ; keep-alive duration (ms), -1 to disable

   :follow-redirects true  ; follow 301/302 (default true)
   :max-redirects 10       ; max redirects to follow

   :insecure? false  ; accept untrusted SSL certs
   :as :auto})       ; output coercion (see below)
```

Convenience methods: `get`, `post`, `put`, `delete`, `head`, `patch`, `options`

## Keep-Alive Connections

http-kit client uses HTTP keep-alive by default (120s):
```clojure
;; Custom keep-alive duration
@(hk-client/get "http://example.com" {:keepalive 30000}) ; 30s

;; This reuses the TCP connection
@(hk-client/get "http://example.com" {:keepalive 30000})

;; Disable keep-alive
@(hk-client/get "http://example.com" {:keepalive -1})
```

## Output Coercion

Control response body format with `:as`:
```clojure
;; Stream (java.io.InputStream) - for large responses
{:as :stream}

;; Byte array - for binary data
{:as :byte-array}

;; String - for text responses
{:as :text}

;; Auto-detect from Content-Type (default)
{:as :auto}
```

Example:
```clojure
(hk-client/get "http://example.com/image.png"
  {:as :stream}
  (fn [{:keys [body]}]
    ;; body is java.io.InputStream
    (io/copy body (io/file "downloaded.png"))))
```

## Multipart File Upload

```clojure
(hk-client/post "http://example.com/upload"
  {:multipart
   [{:name "comment" :content "Uploading my file"}
    {:name "file"
     :content (io/file "path/to/file.txt")
     :filename "file.txt"}]})
```

Content can be String, File, or InputStream. All content is read before sending, so keep files small (few MB).

# Common Patterns

## Passing State in Callbacks

Options map is passed to callback:
```clojure
(let [start-time (System/currentTimeMillis)]
  (hk-client/get "http://example.com"
    {:my-start-time start-time}
    (fn [{:keys [status opts]}]
      (let [{:keys [method url my-start-time]} opts]
        (println method url "took"
          (- (System/currentTimeMillis) my-start-time) "ms")))))
```

## Custom Thread Pool (Server)

Control worker threads:
```clojure
(require '[org.httpkit.utils :as utils])

;; Easy way - use utils/new-worker
(hk-server/run-server app
  {:port 8080
   :worker-pool (utils/new-worker "my-worker-" 8)})

;; Java 19+ virtual threads
(hk-server/run-server app
  {:port 8080
   :worker-pool (java.util.concurrent.Executors/newVirtualThreadPerTaskExecutor)})
```

## Request Body Size Limiting (Client)

```clojure
(hk-client/get "http://example.com"
  {:filter (hk-client/max-body-filter (* 1024 100))}) ; reject if >100KB
```

# Key Gotchas

## Server Security

1. Remote address spoofing: By default `:remote-addr` is populated from `X-Forwarded-For` header, which clients can spoof. Set `:legacy-unsafe-remote-addr? false` to use actual socket address (usually your proxy's IP).

2. Getting real client IP: Parse `X-Forwarded-For` at application level with knowledge of trusted proxies. Never trust the leftmost IP blindly. Consider using the [client-ip](https://github.com/outskirtslabs/client-ip) library.

3. Production deployment: Always run behind a reverse proxy (nginx, Caddy, HAProxy) for HTTPS support, load balancing, and security.

## Nested Query Params

http-kit supports nested params but encoding is fragile:
```clojure
;; This works but is not robust
{:query-params {:a {:b {:c 5}}}} ; => "a[b][c]=5"

;; Better: encode explicitly
(require '[clojure.data.json :as json])
{:query-params {:a (json/write-str {:b {:c 5}})}}
```

## Content-Length Control

By default http-kit calculates Content-Length from body and overrides handler headers. Set `:legacy-content-length? false` to respect handler's Content-Length (useful for RFC-compliant HEAD responses).

## WebSocket Compatibility

Check `:websocket?` in request before calling `as-channel`:
```clojure
(defn handler [req]
  (if (:websocket? req)
    (hk-server/as-channel req {...})
    {:status 200 :body "Not a WebSocket request"}))
```

# Advanced Topics

For these advanced features, consult the [full documentation](http://http-kit.github.io/http-kit/):

- Unix Domain Sockets (UDS) - Java 16+
- Server Name Indication (SNI) - auto-enabled in 2.7+
- Custom client instances with `make-client`
- Testing with http-kit-fake for mocking requests
- Custom request queues and monitoring

## References

- API Docs: https://cljdoc.org/d/http-kit/http-kit/
- Wiki: https://github.com/http-kit/http-kit/wiki
- Benchmarks: https://github.com/http-kit/http-kit/wiki/4-Benchmarking
