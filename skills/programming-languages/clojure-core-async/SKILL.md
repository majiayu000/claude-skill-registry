---
name: clojure-core-async
description: Async programming with channels, go blocks, and CSP in Clojure. Use when working with async operations, channel communication, pub/sub patterns, concurrent pipelines, or CSP-style coordination.
---

# core.async

A Clojure library for async programming and communication using CSP (Communicating Sequential Processes) with channels.

core.async enables writing asynchronous code that looks synchronous, avoiding callback hell through channels and lightweight processes (go blocks).

## Setup

deps.edn:
```clojure
org.clojure/core.async {:mvn/version "1.8.741"}
```

Leiningen:
```clojure
[org.clojure/core.async "1.8.741"]
```

See https://search.maven.org (search: org.clojure/core.async) for latest version.

## Quick Start

```clojure
(require '[clojure.core.async :as a :refer [<! >! <!! >!! chan go]])

;; Create a buffered channel
(def c (chan 10))

;; Put and take from ordinary threads (blocking)
(>!! c "hello")
(<!! c)  ; => "hello"

;; Use go blocks for lightweight async processes
(let [c (chan)]
  (go (>! c "world"))
  (println (<!! (go (<! c)))))  ; => "world"

;; Timeout after 100ms
(a/alts!! [(chan) (a/timeout 100)])
```

## Core Concepts

### Channels

Channels are queues that carry values between processes.

```clojure
(chan)                            ; unbuffered (rendezvous)
(chan 10)                         ; fixed buffer
(chan (a/dropping-buffer 10))    ; drops newest when full
(chan (a/sliding-buffer 10))     ; drops oldest when full
(chan 10 (map inc))               ; with transducer (must be buffered)
(a/close! c)                      ; close channel
```

Important: Channels cannot carry `nil` - `nil` from a take means channel is closed and drained.

### Put and Take Operations

```clojure
;; BLOCKING (>!!, <!!) - use in ordinary threads, NOT in go blocks
(>!! c "msg")    ; blocks until accepted
(<!! c)          ; blocks until available

;; PARKING (>!, <!) - ONLY inside go blocks
(go
  (>! c "msg")   ; parks go block, doesn't block thread
  (<! c))        ; parks until available

;; ASYNC (put!, take!) - callbacks, works anywhere
(a/put! c "msg" #(println "put completed"))
(a/take! c #(println "got:" %))

;; NON-BLOCKING (offer!, poll!) - immediate or fail
(a/offer! c "msg")  ; returns true if succeeded
(a/poll! c)         ; returns value if available, nil otherwise
```

Mnemonic: `>` points into channel (put), `<` points out (take).

### Go Blocks and Thread

```clojure
;; go block - lightweight process (parking ops only)
(go
  (let [v (<! some-chan)]
    (>! result-chan (inc v))))

;; go-loop - infinite processing
(go-loop []
  (when-let [v (<! c)]
    (println v)
    (recur)))

;; thread - for blocking I/O
(a/thread
  (Thread/sleep 1000)  ; blocking OK here
  (<!! some-chan)
  "result")
```

CRITICAL: NEVER use blocking ops (`<!!`, `>!!`, `Thread/sleep`, blocking I/O) inside go blocks!

### alts - Waiting on Multiple Channels

```clojure
;; alts! in go block (parking)
(go
  (let [[v ch] (a/alts! [c1 c2 c3])]
    (println "Got" v "from" ch)))

;; alts!! outside go blocks (blocking)
(a/alts!! [c1 c2 (a/timeout 1000)])

;; With default (non-blocking)
(a/alts!! [c1 c2] :default :nothing)

;; Include puts
(a/alts! [[out-c "value"] in-c])

;; alt - alts with pattern matching
(go
  (a/alt!
    c1 ([v] (println "c1:" v))
    c2 ([v] (println "c2:" v))
    (a/timeout 1000) ([_] (println "timeout"))))
```

## Common Patterns

### Pipeline Processing

```clojure
;; pipeline - computational work (non-blocking)
(a/pipeline 4 out (map #(* % %)) in)

;; pipeline-blocking - I/O work
(a/pipeline-blocking 4 out
  (map (fn [url]
         (Thread/sleep 100)  ; blocking OK here
         (fetch url)))
  in)

;; pipeline-async - async callbacks
(defn async-fetch [url result-chan]
  (http/get url (fn [response]
                  (a/put! result-chan response)
                  (a/close! result-chan))))

(a/pipeline-async 10 out async-fetch in)
```

### Pub/Sub

```clojure
;; Create publication with topic function
(def publication (a/pub in-chan :msg-type))

;; Subscribe channels to topics
(a/sub publication :greeting greeting-chan)
(a/sub publication :farewell farewell-chan)

;; Publish messages (to original in-chan)
(>!! in-chan {:msg-type :greeting :text "Hi"})

;; With topic-specific buffers
(a/pub in-chan :type
  (fn [topic]
    (case topic
      :critical (a/dropping-buffer 1000)
      :normal (a/sliding-buffer 10)
      1)))
```

### Mult/Tap - Broadcasting

```clojure
;; Create mult from source (copies to ALL taps)
(def m (a/mult source-chan))
(a/tap m listener1)
(a/tap m listener2)
(>!! source-chan "broadcast")  ; all listeners receive
```

### Collection Helpers

```clojure
(a/onto-chan! c [1 2 3])        ; put coll onto channel
(<!! (a/into [] c))              ; take into vector
(<!! (a/reduce + 0 c))           ; reduce over channel
(a/merge [c1 c2 c3])             ; merge channels
(a/pipe in-chan out-chan)        ; pipe one to another
```

## Key Gotchas

### 1. Blocking in Go Blocks

NEVER do blocking operations in go blocks - they will block the entire thread pool:

```clojure
;; BAD
(go
  (<!! some-chan)           ; WRONG - use <! instead
  (Thread/sleep 1000)       ; WRONG - use (<! (timeout 1000))
  (.read socket))           ; WRONG - use thread instead

;; GOOD
(a/thread
  (<!! some-chan)           ; OK
  (Thread/sleep 1000)       ; OK
  (.read socket))           ; OK
```

Enable go checking in development: `-Dclojure.core.async.go-checking=true`

### 2. Function Boundaries in Go Blocks

Parking ops don't work across function boundaries:

```clojure
;; BAD: <! inside fn created by map/for
(go (map <! channels))
(go (for [c cs] (<! c)))

;; GOOD: doseq/loop don't create closures
(go (doseq [c cs] (println (<! c))))
(go-loop [cs channels]
  (when-let [c (first cs)] (println (<! c)) (recur (rest cs))))
```

### 3. Buffering and Deadlocks

```clojure
;; BAD: unbuffered channel deadlocks
(let [c (chan)] (>!! c "msg") (<!! c))  ; blocks forever

;; GOOD: use buffer or separate process
(let [c (chan 1)] (>!! c "msg") (<!! c))
(let [c (chan)] (go (>! c "msg")) (<!! c))
```

### 4. nil Values and Closing

```clojure
;; Never put nil - it's the "closed channel" signal
(>!! c nil)      ; BAD - throws
(>!! c ::none)   ; GOOD - sentinel value

;; Close from producer, check on consumer
(a/close! c)
(go-loop []
  (when-let [v (<! c)]  ; nil when closed
    (process v)
    (recur)))
```

### 5. Pub/Sub Blocking

If ANY subscriber can't accept, WHOLE publication blocks - always buffer subscribers:

```clojure
(a/sub pub :topic (chan 100))  ; GOOD - buffered
```

### 6. Prefer put! over (go (>! ...))

```clojure
(a/put! c val (fn [_] nil))  ; efficient
(go (>! c val))               ; wasteful
```

## Advanced

```clojure
;; Promise channel - single-value (like futures)
(def p (a/promise-chan))
(>!! p "first")
(<!! p)  ; => "first" (cached, all readers get same value)

;; Fan-out: one -> many workers
(dotimes [_ 5] (go-loop [] (when-let [v (<! in)] (process v) (recur))))

;; Fan-in: many -> one (use merge)
(a/merge [producer1 producer2 producer3])
```

## References

- API Docs: https://clojure.github.io/core.async/
- GitHub: https://github.com/clojure/core.async
- Rationale: https://clojure.github.io/core.async/rationale.html
- Rich Hickey Talk: https://www.youtube.com/watch?v=yJxFPoxqzWE
- Code Walkthrough: https://github.com/clojure/core.async/blob/master/examples/walkthrough.clj
