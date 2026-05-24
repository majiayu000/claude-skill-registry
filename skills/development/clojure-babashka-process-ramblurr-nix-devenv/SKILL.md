---
name: clojure-babashka-process
description: Clojure library for shelling out and spawning sub-processes. Use when working with external programs, command execution, piping between processes, or handling process I/O streams.
---

# babashka.process

babashka.process is a Clojure library for shelling out and spawning sub-processes. It provides a simple, high-level API with support for piping, streaming I/O, and async execution.

## Setup

Built into babashka since v0.2.3. For JVM projects:

deps.edn:
```clojure
babashka/process {:mvn/version "0.5.22"}
```

Leiningen:
```clojure
[babashka/process "0.5.22"]
```

See https://clojars.org/babashka/process for the latest version.

## Quick Start

Most common: use `shell` for quick command execution:

```clojure
(require '[babashka.process :refer [shell]])

;; Execute and stream output (throws on non-zero exit)
(shell "ls" "-la")

;; Capture output as string
(-> (shell {:out :string} "ls" "-la") :out)
;; => "total 144\ndrwxr-xr-x ..."

;; Don't throw on error, handle exit code
(-> (shell {:continue true} "ls nothing") :exit)
;; => 1
```

For async/streaming needs, use `process`:

```clojure
(require '[babashka.process :refer [process check]])

;; Launch process, don't wait
(def proc (process {:out :string} "ls"))

;; Wait for completion and check exit
(-> proc check :out)
```

## Core Functions

### shell - High-level execution

The recommended function for most use cases:

```clojure
;; Inherits I/O, throws on error, kills subprocesses on shutdown
(shell "ls" "-la")

;; First arg is auto-tokenized
(shell "ls -la")  ; same as above

;; Capture output
(shell {:out :string} "git status")

;; Change directory
(shell {:dir "src"} "ls")

;; Add environment variables
(shell {:extra-env {"FOO" "BAR"}} "env")

;; Don't throw on error
(shell {:continue true} "false")
```

### process - Low-level control

Use when you need async processing or custom I/O handling:

```clojure
;; Launch async, returns immediately
(def p (process "long-running-command"))

;; Check if running
(alive? p)  ; => true

;; Wait for completion
@p  ; blocks until done, adds :exit

;; Or check and throw on error
(check p)
```

### sh - Like clojure.java.shell/sh

Convenience wrapper that captures output and blocks:

```clojure
(require '[babashka.process :refer [sh]])

(-> (sh "ls") :out)
;; => "file1.txt\nfile2.txt\n"

;; Similar to clojure.java.shell/sh but doesn't throw
(-> (sh "false") :exit)
;; => 1
```

## Piping Processes

Thread output from one process to another:

```clojure
;; Using shell (need {:out :string} for next process)
(let [ls-result (shell {:out :string} "ls")]
  (shell {:in (:out ls-result)} "grep" "md"))

;; Using process (stream-based, more efficient)
(-> (process "ls")
    (process {:out :string} "grep" "md")
    deref
    :out)
;; => "README.md\n"

;; Multiple pipes
(-> (process "cat" "file.txt")
    (process "grep" "error")
    (process {:out :string} "wc" "-l")
    check
    :out)
```

## I/O Options

### Output Capture

```clojure
;; As string
{:out :string}

;; As byte array
{:out :bytes}

;; Inherit (print to console)
{:out :inherit}

;; Write to file
{:out :write :out-file (io/file "output.txt")}
{:out "/tmp/output.txt"}  ; shorthand

;; Append to file
{:out :append :out-file (io/file "log.txt")}

;; Discard output
{:out :discard}

;; Redirect stderr to stdout
{:err :out}
```

### Input Sources

```clojure
;; String input
{:in "hello world"}

;; From file
{:in (io/file "input.txt")}

;; From stream
{:in (io/input-stream "data")}

;; From previous process (piping)
{:prev some-process}
```

## Streaming I/O

```clojure
(require '[clojure.java.io :as io])

;; Feed input while running
(def cat-proc (process "cat"))
(def stdin (io/writer (:in cat-proc)))
(binding [*out* stdin]
  (println "hello"))
(.close stdin)
(slurp (:out cat-proc))  ; => "hello\n"

;; Read output line by line
(def proc (process {:err :inherit} "tail" "-f" "log.txt"))
(with-open [rdr (io/reader (:out proc))]
  (binding [*in* rdr]
    (when-let [line (read-line)]
      (println "Got:" line))))
(destroy-tree proc)
```

## Process Management

```clojure
;; Check if running
(alive? proc)

;; Destroy process
(destroy proc)

;; Destroy process and all descendants (JDK9+)
(destroy-tree proc)

;; Shutdown hook
(process {:shutdown destroy-tree} "long-running")
```

## Pipelines

Use `pipeline` with `pb` for JDK9+ native pipelines:

```clojure
(require '[babashka.process :refer [pipeline pb]])

;; Create pipeline
(def pipes (pipeline (pb "ls") (pb "grep" "txt") (pb "wc" "-l")))

;; Get result from last process
(-> pipes last :out slurp)

;; Check all processes in pipeline
(run! check pipes)
```

## Common Patterns

```clojure
;; Auto-tokenization (shell only)
(shell "ls -la")  ; => ["ls" "-la"]
(shell "git commit -m" "msg")  ; => ["git" "commit" "-m" "msg"]

;; Error handling
(try
  (shell "false")
  (catch Exception e
    (println "Failed")))

;; Or handle exit yourself
(let [result (shell {:continue true} "false")]
  (when (not= 0 (:exit result))
    (println "Exit:" (:exit result))))

;; Directory and environment
(shell {:dir "src/main"} "ls")
(shell {:extra-env {"API_KEY" "secret"}} "node" "script.js")

;; Debug commands
(shell {:pre-start-fn #(println "Running:" (:cmd %))} "ls")
```

## Key Gotchas

1. **Output buffering deadlock**: Always provide `:out` option for large output:
   ```clojure
   ;; BAD - deadlocks
   (-> (process {:in large-string} "cat") check)
   ;; GOOD
   (-> (process {:out :string :in large-string} "cat") check)
   ```

2. **Deref before reading output**: Must deref process before accessing `:out :string` or `:out :bytes`.

3. **shell vs process defaults**: `shell` defaults to `:inherit` (console I/O), `process` uses buffered streams.

4. **Windows quirks**: `.ps1` scripts need `powershell.exe -File`, env vars are case-sensitive in `:extra-env`.

5. **:continue only for exit codes**: Program-not-found errors still throw even with `{:continue true}`.

## Advanced Features

For these features, see the [API reference](references/API.md):

- `$` macro - convenience macro with interpolation
- `exec` - replace current process (Unix exec call, GraalVM only)
- Custom process builders with `pb` and `start`
- Exit callbacks with `:exit-fn` (JDK11+)
- Custom program resolvers
- Integration with promesa for promises

## References

- [Full API documentation](references/API.md)
- GitHub: https://github.com/babashka/process
- README: https://github.com/babashka/process/blob/master/README.md
