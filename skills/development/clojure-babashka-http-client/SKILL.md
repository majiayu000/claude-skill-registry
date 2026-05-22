---
name: clojure-babashka-http-client
description: HTTP client for Clojure and Babashka built on java.net.http. Use when making HTTP requests, working with REST APIs, downloading files, or needing WebSocket support in Babashka or Clojure.
---

# babashka.http-client

An HTTP client for Clojure and Babashka built on java.net.http. Drop-in replacement for babashka.curl with better streaming support and no external dependencies.

Built-in to Babashka as of version 1.1.171. Supports Clojure 1.10+.

## Setup

deps.edn:
```clojure
org.babashka/http-client {:mvn/version "0.4.22"}
```

bb.edn:
```clojure
org.babashka/http-client {:mvn/version "0.4.22"}
```

See https://clojars.org/org.babashka/http-client for the latest version.

Note: Built-in to Babashka 1.1.171+, no dependency needed.

## Quick Start

```clojure
(require '[babashka.http-client :as http])

;; Simple GET
(http/get "https://httpstat.us/200")
;; => {:status 200, :body "200 OK", :headers {...}}

;; With headers and query params
(http/get "https://postman-echo.com/get"
  {:headers {"Accept" "application/json"}
   :query-params {"q" "clojure"}})

;; POST with JSON body
(http/post "https://postman-echo.com/post"
  {:headers {:content-type "application/json"}
   :body (json/encode {:a 1 :b "2"})})
```

## Core Usage Patterns

### GET Requests

Simple GET:
```clojure
(http/get "https://api.example.com/users")
```

With headers:
```clojure
(http/get "https://api.example.com/users"
  {:headers {"Authorization" "Bearer token"
             :accept "application/json"}})
```

Query parameters:
```clojure
(http/get "https://api.example.com/search"
  {:query-params {:q "clojure" :limit 10}})

;; Multiple values for same key
(http/get "https://api.example.com/filter"
  {:query-params {:tags ["clojure" "http"]}})
```

### POST Requests

JSON body:
```clojure
(http/post "https://api.example.com/users"
  {:headers {:content-type "application/json"}
   :body (json/encode {:name "Alice" :email "alice@example.com"})})
```

Form parameters:
```clojure
(http/post "https://api.example.com/login"
  {:form-params {"username" "alice" "password" "secret"}})
```

File upload:
```clojure
(require '[clojure.java.io :as io])

(http/post "https://api.example.com/upload"
  {:body (io/file "README.md")})

;; Or stream
(http/post "https://api.example.com/upload"
  {:body (io/input-stream "README.md")})
```

### Authentication

Basic auth:
```clojure
(http/get "https://api.example.com/private"
  {:basic-auth ["username" "password"]})
```

Bearer token:
```clojure
(http/get "https://api.example.com/private"
  {:oauth-token "your-token-here"})
```

### Response Handling

String body (default):
```clojure
(:body (http/get "https://example.com"))
```

Stream for large files:
```clojure
(io/copy
  (:body (http/get "https://example.com/large-file.zip" {:as :stream}))
  (io/file "downloaded.zip"))
```

Binary data:
```clojure
(http/get "https://example.com/image.png" {:as :bytes})
```

### Error Handling

By default, throws on non-2xx/3xx status codes:
```clojure
(try
  (http/get "https://httpstat.us/404")
  (catch Exception e
    (let [data (ex-data e)]
      (println "Status:" (:status data)))))
```

Opt out of throwing:
```clojure
(let [resp (http/get "https://httpstat.us/404" {:throw false})]
  (if (= 404 (:status resp))
    (println "Not found")
    (println "Success")))
```

### Multipart Uploads

```clojure
(http/post "https://api.example.com/upload"
  {:multipart
   [{:name "title" :content "My Document"}
    {:name "file"
     :content (io/file "document.pdf")
     :file-name "doc.pdf"
     :content-type "application/pdf"}]})
```

### Custom Client

For advanced configuration (SSL, timeouts, redirects):
```clojure
;; Start with defaults
(def client
  (http/client
    (assoc-in http/default-client-opts
              [:ssl-context :insecure] true)))

;; Use custom client
(http/get "https://untrusted-cert.example.com" {:client client})
```

Disable redirects:
```clojure
(def no-redirect-client
  (http/client {:follow-redirects :never}))

(http/get "https://httpstat.us/302" {:client no-redirect-client})
```

### Compression

Request compressed responses:
```clojure
(http/get "https://api.stackexchange.com/2.2/sites"
  {:headers {"Accept-Encoding" ["gzip" "deflate"]}})
```

Response is automatically decompressed.

### Async Requests

Returns CompletableFuture:
```clojure
(def resp-future (http/get "https://example.com" {:async true}))

;; Block for result
@resp-future

;; With timeout
(deref resp-future 5000 ::timeout)

;; Callbacks
(http/get "https://example.com"
  {:async true
   :async-then (fn [resp] (println "Success:" (:status resp)))
   :async-catch (fn [e] (println "Error:" (.getMessage e)))})
```

### Timeouts

Connection timeout (on client):
```clojure
(def client (http/client {:connect-timeout 5000})) ; 5 seconds
(http/get "https://example.com" {:client client})
```

Request timeout:
```clojure
(http/get "https://example.com" {:timeout 10000}) ; 10 seconds
```

### URI Construction

Safe URI building from components:
```clojure
(http/request
  {:uri {:scheme "https"
         :host "api.example.com"
         :port 443
         :path "/v1/users"
         :query "active=true&limit=10"}})
```

### WebSockets

```clojure
(require '[babashka.http-client.websocket :as ws])

(def socket
  (ws/websocket
    {:uri "wss://echo.websocket.org"
     :on-open (fn [ws] (ws/send! ws "Hello"))
     :on-message (fn [ws data last] (println "Received:" data))
     :on-close (fn [ws status reason] (println "Closed"))
     :on-error (fn [ws err] (println "Error:" err))}))

;; Send message
(ws/send! socket "Hello WebSocket")

;; Close
(ws/close! socket)
```

## Key Gotchas

1. Throws on non-2xx/3xx by default - Use {:throw false} if you want to handle errors manually.

2. Streaming vs buffering - Default response body is a string (buffered in memory). Use {:as :stream} for large files to avoid OOM.

3. Built-in to Babashka - Don't add as dependency in bb.edn if using Babashka 1.1.171+.

4. Headers can be strings or keywords - Both work: {"Content-Type" "..."} and {:content-type "..."}.

5. CompletableFuture with :async - Use deref/@, not blocking waits. Add timeout to deref to avoid hanging.

6. Custom client is reusable - Create once, reuse for many requests. Don't create new client per request.

7. DNS lookup is synchronous - Even with :async true, initial DNS lookup blocks. Cache results for repeated requests to same host.

## Advanced: Interceptors

Interceptors transform requests/responses. Similar to Ring middleware.

Custom JSON interceptor:
```clojure
(require '[babashka.http-client.interceptors :as interceptors])

(def json-interceptor
  {:name ::json
   :request (fn [req]
              (if (= :json (:as req))
                (-> req
                    (assoc-in [:headers :accept] "application/json")
                    (assoc :as :string ::json true))
                req))
   :response (fn [resp]
               (if (get-in resp [:request ::json])
                 (update resp :body json/parse-string)
                 resp))})

(def my-interceptors
  (cons json-interceptor interceptors/default-interceptors))

(http/get "https://api.example.com/data"
  {:interceptors my-interceptors
   :as :json})
```

Modify existing interceptor:
```clojure
;; Don't throw on 404
(def unexceptional-statuses
  (conj #{200 201 202 203 204 205 206 207 300 301 302 303 304 307} 404))

(def my-throw-interceptor
  {:name ::throw-on-exceptional-status-code
   :response (fn [resp]
               (if (or (false? (some-> resp :request :throw))
                       (contains? unexceptional-statuses (:status resp)))
                 resp
                 (throw (ex-info (str "Exceptional status: " (:status resp)) resp))))})

(def my-interceptors
  (mapv #(if (= ::interceptors/throw-on-exceptional-status-code (:name %))
           my-throw-interceptor
           %)
        interceptors/default-interceptors))
```

## References

- [API Reference](references/API.md) - Complete API documentation
- [GitHub](https://github.com/babashka/http-client)
- [Babashka Book](https://book.babashka.org/#babashkahttp_client)
