---
name: clojure
description: Develop Clojure applications using deps.edn, tools.deps, and functional patterns. Activate when working with .clj/.cljc/.cljs files, deps.edn, or user mentions Clojure, REPL, spec, transducers, reducers, or functional programming.
---

# Clojure Development

Functional-first Clojure with **deps.edn**, **tools.deps**, and **immutability**.

## Workflow

```
1. MODEL    -> Define data with maps, records, specs
2. COMPOSE  -> Build with pure functions, ->> threading
3. TEST     -> Write tests first (clojure.test or Kaocha)
4. VALIDATE -> clojure -M:test/run && clj-kondo --lint src
5. ITERATE  -> Refactor in REPL, keep functions pure
```

## CLI

```bash
# Project setup
clojure -Tnew app :name myuser/myapp    # New app project
clojure -Tnew lib :name myuser/mylib    # New library

# Run
clojure -M -m myapp.core                # Run -main
clojure -M:run                          # Via alias
clojure -X:run                          # Exec function

# REPL
clj                                     # Basic REPL
clojure -M:repl/rebel                   # Rebel readline

# Test
clojure -X:test/run                     # Run tests (Kaocha)
clojure -M:test -m kaocha.runner        # Alternative

# Build
clojure -T:build uber                   # Uberjar
clojure -T:build jar                    # Library jar

# Dependencies
clojure -X:deps tree                    # Dependency tree
clojure -X:deps find-versions :lib clojure.java-time/clojure.java-time
clojure -M:search/outdated              # Find outdated deps
```

## Notes

Project layout, deps.edn templates, core patterns, naming conventions, and anti-patterns live in `reference.md`.

## Research Tools

```
# gh search code for real-world Clojure patterns
gh search code "(go-loop [" --language=clojure
gh search code "(comp (map" --language=clojure
gh search code "(s/def ::" --language=clojure
```

## References

- [reference.md](reference.md) - Data structures, best practices, idioms, error handling
- [patterns.md](cookbook/patterns.md) - Functional patterns, sequences, transducers
- [concurrency.md](cookbook/concurrency.md) - Atoms, refs, agents, core.async
- [spec.md](cookbook/spec.md) - clojure.spec validation & generative testing
- [testing.md](cookbook/testing.md) - clojure.test, Kaocha configuration
- [macros.md](cookbook/macros.md) - Metaprogramming patterns
