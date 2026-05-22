---
name: clojure-babashka-cli
description: Turn Clojure functions into CLIs with babashka.cli. Use when working with command-line argument parsing, building CLIs, subcommand dispatching, option validation, or creating tools with babashka/clojure.
---

# babashka.cli

Turn Clojure functions into CLIs with minimal effort. Supports both `:foo value` and `--foo value` style arguments, automatic type coercion, validation, subcommands, and help generation.

## Setup

deps.edn:
```clojure
org.babashka/cli {:mvn/version "0.8.60"}
```

Leiningen:
```clojure
[org.babashka/cli "0.8.60"]
```

Built into babashka - no dependency needed in bb.edn.

See https://clojars.org/org.babashka/cli for the latest version.

## Quick Start

```clojure
#!/usr/bin/env bb
(require '[babashka.cli :as cli])

(defn greet [{:keys [name verbose]}]
  (when verbose (println "Greeting..."))
  (println "Hello" name))

;; Simple parsing
(cli/parse-opts ["--name" "Alice" "--verbose"] {:coerce {:verbose :boolean}})
;;=> {:name "Alice", :verbose true}

;; Call function directly with parsed args
(greet (cli/parse-opts *command-line-args* {:coerce {:verbose :boolean}}))
```

# Core Patterns

## Parse Options

`parse-opts` - returns a map, leaves extra args in metadata:
```clojure
(cli/parse-opts ["--port" "8080" "--host" "0.0.0.0"]
                {:coerce {:port :long}})
;;=> {:port 8080, :host "0.0.0.0"}
```

`parse-args` - separates options from positional arguments:
```clojure
(cli/parse-args ["--force" "file.txt"]
                {:coerce {:force :boolean}})
;;=> {:opts {:force true}, :args ["file.txt"]}
```

## Type Coercion

```clojure
;; Keyword coercion types
{:coerce {:port :long           ; parse-long
          :ratio :double        ; parse-double
          :flag :boolean        ; true/false
          :name :string         ; stays string
          :kw :keyword          ; keyword
          :sym :symbol}}        ; symbol

;; Auto-coercion (enabled by default since v0.3.35)
(cli/parse-opts ["--port" "8080"])        ;;=> {:port 8080}
(cli/parse-opts ["--flag"])               ;;=> {:flag true}
(cli/parse-opts ["--key" ":value"])       ;;=> {:key :value}

;; Collection coercion
{:coerce {:paths []}}                     ; collect into vector
(cli/parse-opts ["--paths" "src" "--paths" "test"] {:coerce {:paths []}})
;;=> {:paths ["src" "test"]}

{:coerce {:tags [:keyword]}}              ; vector of keywords
(cli/parse-opts ["--tags" "foo" "bar"] {:coerce {:tags [:keyword]}})
;;=> {:tags [:foo :bar]}
```

## Aliases (Short Options)

```clojure
(cli/parse-opts ["-p" "8080" "-v"]
                {:alias {:p :port, :v :verbose}
                 :coerce {:port :long, :verbose :boolean}})
;;=> {:port 8080, :verbose true}

;; Combined short flags (since v0.7.51)
(cli/parse-opts ["-abc"])
;;=> {:a true, :b true, :c true}
```

## Positional Arguments

Use `:args->opts` to map positional arguments to option names:
```clojure
;; Fixed number of args
(cli/parse-opts ["alice" "30"]
                {:args->opts [:name :age]
                 :coerce {:age :long}})
;;=> {:name "alice", :age 30}

;; Variable args - first goes to :user, rest to :files
(cli/parse-opts ["alice" "a.txt" "b.txt"]
                {:args->opts (cons :user (repeat :files))
                 :coerce {:files []}})
;;=> {:user "alice", :files ["a.txt" "b.txt"]}
```

## Validation and Requirements

```clojure
(def spec
  {:port {:coerce :long
          :validate pos?
          :require true
          :desc "Server port"}
   :dir {:validate #(fs/directory? %)
         :desc "Working directory"}})

;; Validate with custom message
{:host {:validate {:pred #(re-matches #"[a-z0-9.-]+" %)
                   :ex-msg (fn [m] (str "Invalid host: " (:value m)))}}}

;; Require specific options
(cli/parse-opts [] {:require [:port]})
;;=> Throws: Required option: :port

;; Restrict to known options only
(cli/parse-opts ["--port" "8080" "--unknown" "x"]
                {:spec {:port {}} :restrict true})
;;=> Throws: Unknown option: :unknown
```

## Default Values

```clojure
(cli/parse-opts ["--name" "Alice"]
                {:exec-args {:port 8080, :host "localhost"}})
;;=> {:name "Alice", :port 8080, :host "localhost"}

;; Command-line args override defaults
(cli/parse-opts ["--port" "9000"]
                {:exec-args {:port 8080}})
;;=> {:port 9000}
```

## Subcommands

Use `dispatch` for subcommand routing:
```clojure
(defn copy-cmd [{:keys [opts]}]
  (println "Copying" (:file opts)))

(defn delete-cmd [{:keys [opts]}]
  (println "Deleting" (:file opts) "depth:" (:depth opts)))

(def table
  [{:cmds ["copy"]   :fn copy-cmd   :args->opts [:file]}
   {:cmds ["delete"] :fn delete-cmd :args->opts [:file]
                                    :coerce {:depth :long}}
   {:cmds [] :fn (fn [_] (println "Unknown command"))}])

(cli/dispatch table ["copy" "foo.txt"])
;;=> Copying foo.txt

(cli/dispatch table ["delete" "bar.txt" "--depth" "3"])
;;=> Deleting bar.txt depth: 3
```

Shared options across subcommands (since v0.8.54):
```clojure
(def table
  [{:cmds [] :spec {:verbose {:coerce :boolean}}}  ; global option
   {:cmds ["build"] :fn build-cmd :spec {:target {:coerce :keyword}}}
   {:cmds ["test"] :fn test-cmd}])

(cli/dispatch table ["--verbose" "build" "--target" "prod"])
;;=> {:dispatch ["build"], :opts {:verbose true, :target :prod}}
```

## Help Generation

Use `format-opts` to generate help text:
```clojure
(def spec
  {:port {:desc "Server port"
          :ref "<port>"
          :default 8080
          :coerce :long
          :alias :p}
   :host {:desc "Server host"
          :ref "<host>"
          :default-desc "localhost"
          :alias :h}
   :verbose {:desc "Enable verbose logging"
             :alias :v}})

(println (cli/format-opts {:spec spec :order [:port :host :verbose]}))
;; Prints:
;;   -p, --port    <port> 8080      Server port
;;   -h, --host    <host> localhost Server host
;;   -v, --verbose                   Enable verbose logging
```

## Error Handling

Custom error handler:
```clojure
(cli/parse-opts []
  {:spec {:port {:require true :desc "Server port"}}
   :error-fn
   (fn [{:keys [type cause msg option]}]
     (when (= :org.babashka/cli type)
       (case cause
         :require (println "Missing required:" option)
         :validate (println "Invalid value:" msg)
         :coerce (println "Cannot parse:" msg)
         :restrict (println "Unknown option:" option))
       (System/exit 1)))})
```

# Common CLI Patterns

## Complete CLI with Help

```clojure
(def cli-spec
  {:spec
   {:port {:coerce :long
           :desc "Server port"
           :default 8080
           :alias :p}
    :verbose {:coerce :boolean
              :desc "Verbose output"
              :alias :v}
    :help {:coerce :boolean
           :desc "Show help"
           :alias :h}}})

(defn show-help []
  (println "Usage: server [options]")
  (println (cli/format-opts cli-spec)))

(defn -main [& args]
  (let [opts (cli/parse-opts args cli-spec)]
    (if (:help opts)
      (show-help)
      (start-server opts))))
```

## Building Tasks for Babashka

In bb.edn:
```clojure
{:tasks
 {build {:doc "Build the project"
         :task (let [opts (cli/parse-opts *command-line-args*
                           {:coerce {:clean :boolean}})]
                 (when (:clean opts) (clean))
                 (compile-project opts))}}}
```

Usage: `bb build --clean`

## Clojure CLI Integration

Call any function as a CLI without wrapper code. In deps.edn:
```clojure
{:aliases
 {:exec {:extra-deps {org.babashka/cli {:mvn/version "0.8.60"}}
         :main-opts ["-m" "babashka.cli.exec"]}}}
```

Usage:
```clojure
;; Call any function with map arg
clojure -M:exec my-ns/my-fn --port 8080 --verbose

;; Add metadata to function for coercion
(defn my-fn
  {:org.babashka/cli {:coerce {:port :long}}}
  [{:keys [port verbose]}]
  ...)
```

# Key Gotchas

1. Options are open by default - extra options don't cause errors. Use `:restrict true` to enforce known options only.

2. Without `:coerce` info, ambiguous args default to strings:
```clojure
(cli/parse-args ["--port" "8080"])  ;;=> {:port "8080"} (string!)
```

3. Boolean flags need no value - just their presence:
```clojure
(cli/parse-opts ["--verbose"])      ;;=> {:verbose true}
```

4. Negative flags work automatically (since v0.7.51):
```clojure
(cli/parse-opts ["--no-colors"])    ;;=> {:colors false}
```

5. Use `--` to separate options from arguments when ambiguous:
```clojure
(cli/parse-args ["--paths" "src" "test" "--" "file.txt"]
                {:coerce {:paths []}})
;;=> {:opts {:paths ["src" "test"]}, :args ["file.txt"]}
```

6. The library is still evolving - check CHANGELOG for breaking changes before upgrading.

# References

- [Full API Reference](references/API.md) - Complete function signatures and documentation
- [GitHub README](https://github.com/babashka/cli) - Comprehensive examples and guides
- [Babashka Book CLI Chapter](https://book.babashka.org/#cli) - Integration with babashka tasks
