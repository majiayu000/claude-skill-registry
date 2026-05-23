---
name: clojure-ring-spec
description: |
  Ring specification for HTTP server applications in Clojure. Use when working with: (1) Ring handlers (sync or async), (2) Ring request maps and their keys, (3) Ring response maps and their keys, (4) Ring middleware, (5) Ring adapters, (6) WebSocket responses and listeners, or when questions mention Ring spec, handler signatures, request/response map structure, or Ring protocols.
---

# Ring Spec (1.5.1)

Ring is an abstraction layer for building HTTP server applications in Clojure. Defines synchronous and asynchronous APIs.

## Handlers

Synchronous handler (1 arg):
```clojure
(fn [request] response)
```

Asynchronous handler (3 args):
```clojure
(fn [request respond raise]
  (respond response))  ; or (raise exception)
```

Dual-arity handler:
```clojure
(fn
  ([request] response)
  ([request respond raise] (respond response)))
```

## Middleware

Higher-order functions that augment handlers:
```clojure
(fn [handler & config-options] enhanced-handler)
```

## Adapters

Start HTTP server with handler and options:
```clojure
(run-adapter handler options)
(run-adapter handler {:async? true})  ; for async handlers
```

## Request Maps

| Key                 | Type                               | Required | Notes |
| ------------------- | ---------------------------------- | -------- | ----- |
|`:body`              |`java.io.InputStream`               |          | Request body |
|`:character-encoding`|`String`                            |          | DEPRECATED |
|`:content-length`    |`String`                            |          | DEPRECATED |
|`:content-type`      |`String`                            |          | DEPRECATED |
|`:headers`           |`{String String}`                   | Yes      | Lowercase keys; multi-value concat with `,`; `cookie` uses `;` |
|`:protocol`          |`String`                            | Yes      | e.g. "HTTP/1.1" |
|`:query-string`      |`String`                            |          | After `?`, excludes `?` |
|`:remote-addr`       |`String`                            | Yes      | Client or last proxy IP |
|`:request-method`    |`Keyword`                           | Yes      | `:get`, `:post`, etc. |
|`:scheme`            |`Keyword`                           | Yes      | `:http`, `:https`, `:ws`, `:wss` |
|`:server-name`       |`String`                            | Yes      | Server name or IP |
|`:server-port`       |`Integer`                           | Yes      | Port |
|`:ssl-client-cert`   |`java.security.cert.X509Certificate`|          | SSL cert if provided |
|`:uri`               |`String`                            | Yes      | Absolute path, starts with `/` |

## Response Maps

| Key      | Type                                       | Required |
| -------- | ------------------------------------------ | -------- |
|`:body`   |`ring.core.protocols/StreamableResponseBody`|          |
|`:headers`|`{String String}` or `{String [String]}`    | Yes      |
|`:status` |`Integer`                                   | Yes      |

Response body satisfies `StreamableResponseBody` protocol:
```clojure
(defprotocol StreamableResponseBody
  (write-body-to-stream [body response output-stream]))
```

Default implementations: `byte[]`, `String`, `clojure.lang.ISeq`, `java.io.InputStream`, `java.io.File`, `nil`

## WebSockets

WebSocket response (returned from handler):
```clojure
(fn [request]
  #:ring.websocket{:listener websocket-listener
                   :protocol "optional-subprotocol"})
```

Or from async handler:
```clojure
(fn [request respond raise]
  (respond #:ring.websocket{:listener websocket-listener}))
```

### WebSocket Listener Protocol

```clojure
(defprotocol Listener
  (on-open    [listener socket])
  (on-message [listener socket message])      ; message: CharSequence or ByteBuffer
  (on-pong    [listener socket data])         ; data: ByteBuffer
  (on-error   [listener socket throwable])
  (on-close   [listener socket code reason])) ; code: int, reason: String
```

Optional ping handler:
```clojure
(defprotocol PingListener
  (on-ping [listener socket data]))  ; If not implemented, adapter auto-responds to pings
```

### WebSocket Socket Protocol

```clojure
(defprotocol Socket
  (-open? [socket])                           ; Returns truthy if connected
  (-send  [socket message])                   ; message: CharSequence or ByteBuffer
  (-ping  [socket data])                      ; data: ByteBuffer
  (-pong  [socket data])                      ; data: ByteBuffer (unsolicited)
  (-close [socket code reason]))              ; code: int, reason: String
```

Optional async send:
```clojure
(defprotocol AsyncSocket
  (-send-async [socket message succeed fail]))  ; succeed: (fn []), fail: (fn [throwable])
```
