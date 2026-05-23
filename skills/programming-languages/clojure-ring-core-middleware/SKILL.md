---
name: clojure-ring-core-middleware
description: |
  Ring core middleware for Clojure. Use when working with parameter parsing, sessions, cookies, flash messages, static files, or composing middleware stacks. Triggers on ring.middleware, wrap-params, wrap-session, wrap-cookies, or middleware composition questions.
---

# Ring Core Middleware

Ring middleware are higher-order functions that wrap handlers to add functionality. Middleware compose via function wrapping - outermost middleware executes first.

## Quick Start

Common middleware stack:
```clojure
(require '[ring.middleware.params :refer [wrap-params]]
         '[ring.middleware.keyword-params :refer [wrap-keyword-params]]
         '[ring.middleware.session :refer [wrap-session]]
         '[ring.middleware.flash :refer [wrap-flash]])

(def app
  (-> handler
      wrap-keyword-params
      wrap-params
      wrap-flash
      wrap-session))
```

Order matters: innermost (handler) to outermost (first to execute).

# Parameter Processing

## wrap-params

Parses URL-encoded parameters from query string and form body. Adds `:query-params`, `:form-params`, `:params` to request.

```clojure
(wrap-params handler {:encoding "UTF-8"})
;; URL: /search?q=clojure -> {:params {"q" "clojure"}}
```

## wrap-keyword-params

Converts parameter string keys to keywords. Must come after wrap-params.

```clojure
(-> handler wrap-keyword-params wrap-params)
;; {"q" "clojure"} -> {:q "clojure"}
```

## wrap-nested-params

Converts flat params to nested structures using bracket notation.

```clojure
(-> handler wrap-nested-params wrap-keyword-params wrap-params)
;; {"user[name]" "Alice"} -> {:user {:name "Alice"}}
```

## wrap-multipart-params

Handles file uploads. Adds `:multipart-params` with file metadata.

```clojure
(wrap-multipart-params handler {:store (temp-file-store)})
;; Uploaded file structure:
;; {"file" {:filename "doc.pdf" :content-type "application/pdf"
;;          :tempfile #object[java.io.File ...] :size 51200}}
```

Options: `:encoding`, `:store` (temp-file-store or byte-array-store). Temp files deleted after 1 hour.

# Session & State

## wrap-cookies

Parses cookies from headers. Adds `:cookies` to request, reads from `:cookies` in response.

```clojure
(wrap-cookies handler)
;; Request: {:cookies {"session_id" {:value "abc123"}}}
;; Response: {:cookies {"session_id" {:value "abc123" :max-age 3600
;;                                     :secure true :http-only true}}}
```

Attributes: `:domain`, `:path`, `:secure`, `:http-only`, `:max-age`, `:expires`, `:same-site`

## wrap-session

Manages browser sessions via cookies. Read from `:session` in request, write to `:session` in response.

```clojure
(wrap-session handler {:store (cookie-store {:key "16-byte-secret"})
                       :cookie-attrs {:max-age 3600 :secure true}})

;; Read: (get-in request [:session :username])
;; Update: (assoc response :session (assoc session :count 1))
;; Delete: (assoc response :session nil)
;; Recreate ID: (assoc response :session (vary-meta session assoc :recreate true))
```

Options: `:store` (memory-store default, cookie-store), `:cookie-name`, `:cookie-attrs`

Stores: memory-store (not multi-server), cookie-store (needs 16-byte key)

## wrap-flash

Session-based flash messages persisting across one redirect. Must wrap around wrap-session.

```clojure
(-> handler wrap-flash wrap-session)
;; Set: (assoc response :flash "Success!")
;; Read: (:flash request)
```

Messages auto-expire after being read once.

# HTTP Protocol

## wrap-head
Converts HEAD requests to GET and strips body. Usually innermost wrapper.

## wrap-not-modified
Returns 304 responses via ETag/Last-Modified. Checks `If-Modified-Since` and `If-None-Match` headers.

## wrap-content-type
Auto-adds Content-Type from file extension. Falls back to `application/octet-stream`.
```clojure
(wrap-content-type handler {:mime-types {"txt" "text/plain"}})
```

## wrap-content-length
Auto-calculates Content-Length. Uses SizableResponseBody protocol.

# Static Content

## wrap-file
Serves files from filesystem. Checks filesystem before handler.
```clojure
(wrap-file handler "/var/www/public" {:index-files? true :allow-symlinks? false})
```

## wrap-resource
Serves resources from classpath (JAR/WAR compatible). Path relative to `resources/`.
```clojure
(wrap-resource handler "public")  ; serves resources/public/*
```

## Static Pattern
Combine with content-type and not-modified. These must wrap outside resource/file.
```clojure
(-> handler (wrap-resource "public") wrap-content-type wrap-not-modified)
```

# Middleware Patterns

```clojure
;; Basic pattern
(defn wrap-custom [handler]
  (fn [request]
    (let [response (handler request)]
      response)))

;; Add request keys
(defn wrap-user [handler]
  (fn [request]
    (if-let [user-id (-> request :session :user-id)]
      (handler (assoc request :user (get-user-by-id user-id)))
      (handler request))))

;; Conditional execution
(defn wrap-auth [handler]
  (fn [request]
    (if (authorized? request)
      (handler request)
      {:status 403 :body "Access Denied"})))
```

# Common Stacks

## Development Stack

```clojure
(def app
  (-> handler
      wrap-keyword-params
      wrap-nested-params
      wrap-params
      wrap-flash
      wrap-session))
```

## Production with Static Files

```clojure
(def app
  (-> handler
      wrap-keyword-params
      wrap-nested-params
      wrap-params
      wrap-flash
      wrap-session
      (wrap-resource "public")
      wrap-content-type
      wrap-not-modified))
```

# Key Gotchas

1. Middleware order matters:
   - wrap-params before wrap-keyword-params before wrap-nested-params
   - wrap-session before wrap-flash
   - wrap-resource/wrap-file outermost
   - wrap-content-type and wrap-not-modified outside static middleware

2. wrap-multipart-params doesn't include basic params - use both wrap-params and wrap-multipart-params

3. Session stores:
   - memory-store: not suitable for multi-server deployments
   - cookie-store: requires 16-byte secret key, sessions stored in browser

4. wrap-file-info is DEPRECATED - use wrap-content-type + wrap-not-modified instead

5. Flash messages require wrap-session

6. Cookie security: use `:secure true` for HTTPS, `:http-only true` to prevent JavaScript access, `:same-site :strict` for CSRF protection

7. File uploads: temp-file-store auto-deletes after 1 hour - save files permanently if needed

## Session Store Protocol

Custom session stores implement SessionStore:
```clojure
(require '[ring.middleware.session.store :as store])

(defrecord CustomStore []
  store/SessionStore
  (read-session [_ key]
    (read-data-from-backend key))
  (write-session [_ key data]
    (let [key (or key (generate-secure-random-key))]
      (save-data-to-backend key data)
      key))
  (delete-session [_ key]
    (delete-data-from-backend key)
    nil))
```

CRITICAL: Generate cryptographically secure random keys for new sessions to prevent session hijacking.

# References

- Source: https://github.com/ring-clojure/ring/tree/master/ring-core/src/ring/middleware
- API Docs: https://cljdoc.org/d/ring/ring-core/
- Wiki: https://github.com/ring-clojure/ring/wiki
- Specific guides:
  - Parameters: https://github.com/ring-clojure/ring/wiki/Parameters
  - Sessions: https://github.com/ring-clojure/ring/wiki/Sessions
  - Cookies: https://github.com/ring-clojure/ring/wiki/Cookies
  - File Uploads: https://github.com/ring-clojure/ring/wiki/File-Uploads
  - Static Resources: https://github.com/ring-clojure/ring/wiki/Static-Resources
  - Middleware Patterns: https://github.com/ring-clojure/ring/wiki/Middleware-Patterns
