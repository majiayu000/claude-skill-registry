---
name: clojure-core-async-flow
description: core.async.flow provides a declarative framework for building process flows with strict separation of application logic from topology, execution, and lifecycle management. Use when building multi-process systems, data pipelines, or when you need coordinated lifecycle management and error handling across communicating processes.
---

# core.async.flow

A framework for building robust process flows with strict separation of application logic from topology, execution, communication, lifecycle, monitoring and error handling.

core.async.flow provides concrete implementations of processes (threads of activity) and flows (directed graphs of processes communicating via channels). You define pure data->data functions and a declarative flow topology, and the framework handles all channel I/O, thread lifecycle, error handling, and coordination.

## Setup

deps.edn:
```clojure
org.clojure/core.async {:mvn/version "1.7.733"}
```

Leiningen:
```clojure
[org.clojure/core.async "1.7.733"]
```

See https://mvnrepository.com/artifact/org.clojure/core.async for the latest version.

## Quick Start

```clojure
(require '[clojure.core.async.flow :as flow])

;; 1. Define a step function (pure data->data logic)
(defn process-step
  ([] {:params {:multiplier "Multiply factor"}
       :ins {:in "Input channel"}
       :outs {:out "Output channel"}})
  ([{:keys [multiplier]}]
   {:multiplier multiplier})
  ([state transition]
   state)
  ([state input msg]
   [state {:out [(* msg (:multiplier state))]}]))

;; 2. Define the flow topology
(def flow-def
  {:procs {:processor {:proc (flow/process #'process-step)
                       :args {:multiplier 10}}}
   :conns []})

;; 3. Create and start the flow
(def my-flow (flow/create-flow flow-def))
(def {:keys [report-chan error-chan]} (flow/start my-flow))

;; Inject messages and monitor
(flow/inject my-flow [:processor :in] [5])
;; => Outputs 50 on :out channel
```

## Core Concepts

### Step Functions

Step functions are ordinary, pure data->data functions with four arities:

1. describe `()` - Returns static description of params, inputs, outputs
2. init `(arg-map)` - Takes args, returns initial state
3. transition `(state transition)` - Handles lifecycle transitions (start/stop/pause/resume)
4. transform `(state input msg)` - Core processing loop, returns `[state' {out-id [msgs]}]`

```clojure
(defn my-step
  ;; Describe - what this step needs and provides
  ([]
   {:params {:size "Max size"}
    :ins {:in "Input channel"}
    :outs {:out "Output channel"}})

  ;; Init - setup initial state
  ([{:keys [size]}]
   {:size size
    :count 0})

  ;; Transition - handle lifecycle events
  ([state transition]
   (case transition
     ::flow/start (assoc state :active true)
     ::flow/stop (assoc state :active false)
     state))

  ;; Transform - process messages
  ([state input msg]
   (let [new-state (update state :count inc)]
     [new-state {:out [(str "Processed: " msg)]}])))
```

### Process Launchers

Create process launchers with `process`:

```clojure
(flow/process #'my-step)  ; Use var for hot-reloading

;; With workload specification
(flow/process #'my-step {::flow/workload :io})
(flow/process #'my-step {::flow/workload :compute})
(flow/process #'my-step {::flow/workload :mixed})  ; default
```

Workload types:
- `:mixed` - General purpose (default)
- `:io` - I/O-bound work (don't do extensive computation in transform)
- `:compute` - CPU-bound work (transform runs in separate thread, must not block!)

### Flow Definition

A flow definition is a map with `:procs` and `:conns`:

```clojure
{:procs {:source {:proc (flow/process #'source-step)
                  :args {:source-chan in-chan}
                  :chan-opts {:buffer-size 100}}
         :processor {:proc (flow/process #'process-step)
                     :args {:multiplier 10}}
         :sink {:proc (flow/process #'sink-step)
                :args {:sink-chan out-chan}}}

 :conns [[[:source :out] [:processor :in]]
         [[:processor :out] [:sink :in]]]}
```

Connections format: `[[from-pid outid] [to-pid inid]]`

### Source and Sink Processes

Connect flows to external channels using `::flow/in-ports` and `::flow/out-ports`:

```clojure
(defn source-step
  ([]
   {:params {:source-chan "External input channel"}
    :ins {}
    :outs {:out "Flow output"}})

  ([{:keys [source-chan]}]
   {::flow/in-ports {:external source-chan}})

  ([state transition] state)

  ([state input msg]
   ;; Read from :external, output to :out
   [state {:out [msg]}]))

(defn sink-step
  ([]
   {:params {:sink-chan "External output channel"}
    :ins {:in "Flow input"}
    :outs {}})

  ([{:keys [sink-chan]}]
   {::flow/out-ports {:external sink-chan}})

  ([state transition] state)

  ([state input msg]
   ;; Receive on :in, send to :external
   [state {:external [msg]}]))
```

## Flow Lifecycle

```clojure
;; Create flow
(def my-flow (flow/create-flow flow-def))

;; Start all processes
(def {:keys [report-chan error-chan]} (flow/start my-flow))

;; Control the flow
(flow/pause my-flow)        ; Pause all processes
(flow/resume my-flow)       ; Resume all processes
(flow/pause-proc my-flow :processor)   ; Pause single process
(flow/resume-proc my-flow :processor)  ; Resume single process

;; Inspect state
(flow/ping my-flow)         ; Get all process states
(flow/ping-proc my-flow :processor)  ; Get single process state

;; Inject messages at any point
(flow/inject my-flow [:processor :in] [1 2 3])

;; Stop the flow
(flow/stop my-flow)
```

## Transform Return Values

The transform arity returns `[state' output-map]` where output-map is `{out-id [msgs]}`:

```clojure
([state input msg]
  (let [result (process-message msg)]
    ;; Send to single output
    [state {:out [result]}]

    ;; Send to multiple outputs
    [state {:out1 [result]
            :out2 [(transform result)]}]

    ;; Send to report channel (monitoring/logging)
    [state {::flow/report [{:type :info :msg "Processed"}]}]

    ;; Reply to sender (if msg has return address)
    [state {[:sender-pid :reply] [result]}]

    ;; No output
    [state {}]))
```

Never return nil as a message value (core.async channels don't support nil).

## Helper Functions

Lift ordinary functions into step functions:

```clojure
;; Lift function returning collection
(def multi-step
  (flow/lift*->step
    (fn [x] [(inc x) (dec x)])))

;; Lift function returning single value
(def single-step
  (flow/lift1->step
    (fn [x] (inc x))))

;; Create step from map of arities
(def map-step
  (flow/map->step
    {:describe (fn [] {...})
     :init (fn [args] {...})
     :transition (fn [state t] {...})
     :transform (fn [state input msg] [...])}))
```

## Common Patterns

### Data Pipeline

```clojure
(def pipeline-def
  {:procs {:reader {:proc (flow/process #'read-step)}
           :validator {:proc (flow/process #'validate-step)}
           :transformer {:proc (flow/process #'transform-step)}
           :writer {:proc (flow/process #'write-step)}}
   :conns [[[:reader :out] [:validator :in]]
           [[:validator :out] [:transformer :in]]
           [[:transformer :out] [:writer :in]]]})
```

### Fan-out/Fan-in

```clojure
;; Fan-out: One process sends to multiple
{:conns [[[:source :out] [:worker1 :in]]
         [[:source :out] [:worker2 :in]]
         [[:source :out] [:worker3 :in]]]}

;; Fan-in: Multiple processes send to one
{:conns [[[:worker1 :out] [:aggregator :in]]
         [[:worker2 :out] [:aggregator :in]]
         [[:worker3 :out] [:aggregator :in]]]}
```

### Conditional Input Filtering

Use `::flow/input-filter` to dynamically control which inputs to read:

```clojure
([state input msg]
  (if (ready-for-more? state)
    [state {:out [msg]}]
    ;; Pause input temporarily
    [(assoc state ::flow/input-filter
            (fn [cid] false))
     {}]))
```

### Error Handling

Step functions can throw exceptions - flow handles them:

```clojure
([state input msg]
  (when (invalid? msg)
    (throw (ex-info "Invalid message" {:msg msg})))
  [state {:out [(process msg)]}])

;; Errors appear on error-chan
(def {:keys [error-chan]} (flow/start my-flow))
(go-loop []
  (when-let [error (<! error-chan)]
    (log/error error)
    (recur)))
```

### Monitoring and Reporting

Send monitoring data to the report channel:

```clojure
([state input msg]
  [state {::flow/report [{:type :metric
                          :name "messages-processed"
                          :value 1}]
          :out [result]}])

;; Consume reports
(def {:keys [report-chan]} (flow/start my-flow))
(go-loop []
  (when-let [report (<! report-chan)]
    (metrics/record report)
    (recur)))
```

## Key Gotchas

1. Use vars for step functions: Pass `#'my-step` not `my-step` to enable hot-reloading during development.

2. Transform must be pure: No side effects, no channel operations. Throw exceptions for errors - don't try to handle them in the step function.

3. No nil messages: core.async channels don't support nil. Return empty output map `{}` instead of `{:out [nil]}`.

4. Compute workload must not block: When using `:workload :compute`, the transform arity runs in a separate thread with timeout. Don't call blocking operations.

5. External channels are not managed: Channels in `::flow/in-ports` and `::flow/out-ports` must be created by you and their lifecycle is not managed by flow.

6. Connection topology is static: You cannot dynamically add/remove connections while the flow is running. Create a new flow for topology changes.

7. Process state is isolated: State is per-process. To share data between processes, send messages or use external state management.

## Advanced Features

For these features, consult the full documentation:

- Custom executors for workload management
- Channel buffer configuration and backpressure
- Using `datafy` to inspect flow topology
- flow-monitor tool for visualization
- Implementing custom `ProcLauncher` protocol
- Multi-arity output (sending to computed output channels)

## References

- API Docs: https://clojure.github.io/core.async/flow.html
- Flow Guide: https://github.com/clojure/core.async/blob/master/doc/flow-guide.md
- Rationale: https://github.com/clojure/core.async/blob/master/doc/flow.md
- flow-monitor: https://github.com/clojure/core.async.flow-monitor/
- GitHub: https://github.com/clojure/core.async
