---
name: clojure-sente
description: Realtime bidirectional communications between Clojure server and ClojureScript client. Use when building apps where BOTH client and server use sente - NOT for connecting to third-party WebSocket APIs. Provides server push, realtime updates, and reliable async messaging with automatic WebSocket/Ajax fallback.
---

# Sente

Realtime web communications library for Clojure/Script using WebSockets with automatic Ajax fallback.

Sente provides bidirectional async communications between a Clojure server and ClojureScript browser client, with automatic protocol selection (WebSocket or long-polling), reconnection handling, and event batching. Send arbitrary Clojure values between client and server with efficient serialization.

NOTE: Sente is for communication between your own Clojure server and ClojureScript client - both sides must use sente. It is NOT a generic WebSocket client for connecting to third-party WebSocket APIs. For connecting to external WebSocket servers, use hato, http-kit client, or gniazdo instead.

## Setup

deps.edn:
```clojure
com.taoensso/sente {:mvn/version "1.21.0"}
```

Leiningen:
```clojure
[com.taoensso/sente "1.21.0"]
```

See https://clojars.org/com.taoensso/sente for the latest version.

## Quick Start

Server (Clojure):
```clojure
(ns my-app.server
  (:require
    [taoensso.sente :as sente]
    [taoensso.sente.server-adapters.http-kit :refer [get-sch-adapter]]
    [ring.middleware.anti-forgery :refer [wrap-anti-forgery]]
    [compojure.core :refer [defroutes GET POST]]))

;; Create channel socket server
(let [{:keys [ch-recv send-fn connected-uids
              ajax-post-fn ajax-get-or-ws-handshake-fn]}
      (sente/make-channel-socket-server! (get-sch-adapter) {})]

  (def ring-ajax-post                ajax-post-fn)
  (def ring-ajax-get-or-ws-handshake ajax-get-or-ws-handshake-fn)
  (def ch-chsk                       ch-recv) ; Receive channel
  (def chsk-send!                    send-fn) ; Send function
  (def connected-uids                connected-uids)) ; Atom of connected users

;; Add routes for channel socket
(defroutes my-routes
  (GET  "/chsk" req (ring-ajax-get-or-ws-handshake req))
  (POST "/chsk" req (ring-ajax-post                req)))

;; Wrap with necessary middleware
(def app
  (-> my-routes
      wrap-keyword-params
      wrap-params
      wrap-anti-forgery  ; Important for security
      wrap-session))
```

Client (ClojureScript):
```clojure
(ns my-app.client
  (:require
    [taoensso.sente :as sente :refer [cb-success?]]))

;; Get CSRF token from page
(def ?csrf-token
  (when-let [el (.getElementById js/document "sente-csrf-token")]
    (.getAttribute el "data-csrf-token")))

;; Create channel socket client
(let [{:keys [chsk ch-recv send-fn state]}
      (sente/make-channel-socket-client!
        "/chsk"        ; Must match server route
        ?csrf-token
        {:type :auto})] ; :auto, :ws, or :ajax

  (def chsk       chsk)
  (def ch-chsk    ch-recv) ; Receive channel
  (def chsk-send! send-fn) ; Send function
  (def chsk-state state))  ; Watchable state atom
```

HTML (include CSRF token):
```clojure
;; In your Hiccup/HTML template
(let [csrf-token (force ring.middleware.anti-forgery/*anti-forgery-token*)]
  [:div#sente-csrf-token {:data-csrf-token csrf-token}])
```

## Core Concepts

Event - Messages have the form `[event-id event-data]`:
```clojure
[:my-app/some-event {:data "value"}]
```

Event-msg - Events arrive wrapped in maps with metadata:
```clojure
;; Server event-msg
{:event [:my-app/some-event {:data "value"}]
 :id    :my-app/some-event
 :?data {:data "value"}
 :ring-req {...}           ; Ring request map
 :?reply-fn (fn [reply])   ; Present when client requested reply
 :uid "user-123"           ; User ID
 :client-id "..."}         ; Specific client/tab

;; Client event-msg
{:event [:my-app/some-event {:data "value"}]
 :id    :my-app/some-event
 :?data {:data "value"}
 :send-fn chsk-send!}
```

User vs Client - Sente distinguishes between users and clients:
- User ID: Persistent identity (can survive across sessions/devices)
- Client ID: Specific browser tab/connection
- One user can have multiple connected clients
- Server push targets user IDs, not individual clients

## Sending Events

Client to Server (with optional reply):
```clojure
;; Fire and forget
(chsk-send! [:my-app/request {:user-input "data"}])

;; With callback for reply
(chsk-send!
  [:my-app/request {:user-input "data"}]
  5000  ; Timeout in ms
  (fn [reply]
    (if (sente/cb-success? reply)  ; Check for :chsk/closed, :chsk/timeout, :chsk/error
      (println "Success:" reply)
      (println "Failed"))))
```

Server to User (push):
```clojure
;; Send to all clients of a specific user
(chsk-send! "user-id" [:my-app/notification {:msg "New update!"}])

;; Send returns true if at least one client received the message
(when-not (chsk-send! user-id event)
  (println "User not connected"))
```

Server Reply to Client Request:
```clojure
;; In your event handler on server
(defn handle-request [{:keys [?reply-fn ?data]}]
  (when ?reply-fn
    (?reply-fn {:status :ok :result "processed"})))
```

## Event Routing

Use a multimethod to dispatch events by ID:

Client:
```clojure
(defmulti -event-msg-handler :id)

(defmethod -event-msg-handler :default
  [{:keys [event]}]
  (println "Unhandled event:" event))

(defmethod -event-msg-handler :chsk/state
  [{:keys [?data]}]
  (let [[old-state new-state] ?data]
    (if (:first-open? new-state)
      (println "Channel socket successfully established!")
      (println "Channel socket state change:" new-state))))

(defmethod -event-msg-handler :my-app/notification
  [{:keys [?data]}]
  (println "Received notification:" ?data))

;; Start event router
(defonce router
  (sente/start-client-chsk-router! ch-chsk -event-msg-handler))
```

Server:
```clojure
(defmulti -event-msg-handler :id)

(defmethod -event-msg-handler :default
  [{:keys [event]}]
  (println "Unhandled event:" event))

(defmethod -event-msg-handler :my-app/request
  [{:keys [?data ?reply-fn uid ring-req]}]
  (println "Request from user" uid ":" ?data)
  (when ?reply-fn
    (?reply-fn {:status :ok})))

;; Start event router
(defonce router
  (sente/start-server-chsk-router! ch-chsk -event-msg-handler))
```

## User Identity

Set user ID in one of two ways:

1. Via Ring session (most common):
```clojure
;; In your login handler
{:status 200
 :session (assoc session :uid "user-123")}
```

2. Via custom user-id-fn:
```clojure
(sente/make-channel-socket-server!
  (get-sch-adapter)
  {:user-id-fn (fn [ring-req]
                 (get-in ring-req [:params :user-id]))})
```

For anonymous/per-session users, use a random UUID:
```clojure
{:session (assoc session :uid (str (java.util.UUID/randomUUID)))}
```

## Connected Users

Watch the connected-uids atom to track who's online:

```clojure
;; Server-side
(add-watch connected-uids :watcher
  (fn [_ _ old-state new-state]
    (when (not= old-state new-state)
      (println "Connected users changed:")
      (println "  WebSocket:" (:ws   new-state)) ; Set of user IDs
      (println "  Ajax:"      (:ajax new-state)) ; Set of user IDs
      (println "  All:"       (:any  new-state))))) ; Set of all user IDs
```

## Channel Socket State

Client-side state changes trigger `:chsk/state` events:

```clojure
;; Client receives [:chsk/state [old-state new-state]] events
(defmethod -event-msg-handler :chsk/state
  [{:keys [?data]}]
  (let [[old new] ?data]
    (if (:first-open? new)
      (println "Connected!")
      (when (not= (:open? old) (:open? new))
        (if (:open? new)
          (println "Reconnected")
          (println "Disconnected"))))))
```

State map keys:
- `:open?` - Is connection currently open?
- `:first-open?` - First successful connection?
- `:ever-opened?` - Has ever connected successfully?
- `:type` - Current protocol (`:ws` or `:ajax`)
- `:uid` - User ID from server
- `:csrf-token` - CSRF token from server

## Common Patterns

Broadcast to all connected users:
```clojure
;; Server
(doseq [uid (:any @connected-uids)]
  (chsk-send! uid [:my-app/broadcast {:msg "System announcement"}]))
```

Request/response with timeout:
```clojure
;; Client
(chsk-send!
  [:my-app/fetch-data {:id 123}]
  3000
  (fn [reply]
    (if (sente/cb-success? reply)
      (update-ui! reply)
      (show-error! "Request timed out"))))
```

Wait for connection before sending:
```clojure
;; Client - wait for first connection
(defonce connected? (atom false))

(defmethod -event-msg-handler :chsk/state
  [{:keys [?data]}]
  (when (:first-open? (second ?data))
    (reset! connected? true)
    (chsk-send! [:my-app/init {}])))
```

Lifecycle management with component:
```clojure
;; Both start-client-chsk-router! and start-server-chsk-router!
;; return a (fn stop []) for cleanup
(defonce router
  (sente/start-server-chsk-router! ch-chsk event-msg-handler))

;; Later, on shutdown:
(router) ; Stops the router
```

## Server Adapters

Sente supports multiple web servers via adapters:

```clojure
;; http-kit
[taoensso.sente.server-adapters.http-kit :refer [get-sch-adapter]]

;; Immutant
[taoensso.sente.server-adapters.immutant :refer [get-sch-adapter]]

;; Aleph
[taoensso.sente.server-adapters.aleph :refer [get-sch-adapter]]

;; nginx-clojure
[taoensso.sente.server-adapters.nginx-clojure :refer [get-sch-adapter]]

;; Jetty 9+
[taoensso.sente.server-adapters.jetty9 :refer [get-sch-adapter]]
```

All use the same `(get-sch-adapter)` function.

## Serialization (Packers)

Sente uses "packers" for serialization. Default is edn:

```clojure
;; Using Transit (recommended for performance + binary data)
(require '[taoensso.sente.packers.transit :as sente-transit])

(sente/make-channel-socket-server!
  (get-sch-adapter)
  {:packer (sente-transit/get-packer :json)}) ; or :msgpack

;; Custom Transit handlers (e.g., for Joda Time)
(def packer
  (sente-transit/->TransitPacker
    :json
    {:handlers {org.joda.time.DateTime my-write-handler}}
    {:handlers {"m" my-read-handler}}))
```

Client and server must use the same packer.

## Gotchas / Caveats

Event ordering - Sente does NOT guarantee event ordering. Events may arrive out of order due to buffering, async serialization, etc. Don't depend on ordering.

Large payloads - Do NOT use Sente for payloads > 1MB:
- WebSocket connections will bottleneck
- Large transfers can cause client disconnects
- Instead: Use Sente for signaling, make large transfers via Ajax
  - Client->Server: Client requests large data via Ajax
  - Server->Client: Server signals client to fetch data via Ajax

Security requirements:
- ALWAYS use CSRF protection (ring-anti-forgery or ring-defaults)
- ALWAYS protect the POST endpoint (ajax-post-fn)
- Use HTTPS in production (automatic for WebSockets = WSS)

User ID for push - Server push requires a user ID. Client->server requests don't need one, but server->client push does. Set via Ring session `:uid` key or custom `:user-id-fn`.

Session modification - WebSocket events use the INITIAL handshake request's session. To modify sessions (login/logout), use regular HTTP Ajax, not WebSocket events.

Router lifecycle - The router functions return a `stop` function. Call it on shutdown to clean up (though the cost of not doing so is minimal - just a parked go thread).

## Advanced Topics

For these features, consult the official documentation:

- Custom event batching and buffering
- Debugging connections at protocol level
- Testing strategies
- Performance tuning
- Alternative server adapters
- Component/lifecycle integration libraries

## References

- API Docs: https://cljdoc.org/d/com.taoensso/sente/
- GitHub: https://github.com/taoensso/sente
- Wiki: https://github.com/taoensso/sente/wiki
- Example Projects: https://github.com/taoensso/sente/wiki/3-Example-projects
- Getting Started: https://github.com/taoensso/sente/wiki/1-Getting-started
- FAQ: https://github.com/taoensso/sente/wiki/3-FAQ
