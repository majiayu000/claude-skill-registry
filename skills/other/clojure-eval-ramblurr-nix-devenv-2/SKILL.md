---
name: clojure-eval
description: Use this skill BEFORE using writing any Clojure code. It teaches how to use the Clojure REPL (via brepl) so you can test code, check if edited files compile, verify function behavior, or interact with a running REPL session.
---

# Clojure REPL Evaluation

**You MUST load this skill before using brepl.** Do NOT attempt to use brepl without loading this skill first, or you will use incorrect syntax.


## When to Use This Skill

Use this skill when you need to:
- Verify that edited Clojure files compile and load correctly
- Test function behavior interactively
- Check the current state of the REPL
- Debug code by evaluating expressions
- Require or load namespaces for testing
- Validate that code changes work before committing

## How It Works

`brepl` is a REPL client for evaluating Clojure expressions. This skill teaches the heredoc pattern for reliable code evaluation.

The `brepl` command evaluates Clojure code against an nREPL server. It auto-detects the port from the `.nrepl-port` file in your project directory, so explicit port configuration is usually unnecessary.

## The Heredoc Pattern

Always use the heredoc pattern for brepl evaluation. This eliminates quoting issues, works for all cases, and provides a consistent approach.

### Syntax

```bash
brepl "$(cat <<'EOF'
(your clojure code here)
EOF
)"
```

Note: Use `<<'EOF'` (with single quotes) to prevent shell variable expansion.

### Why Use Heredoc

- No quoting issues: Everything between `<<'EOF'` and `EOF` is literal
- Consistent pattern: One approach for all evaluations
- Multi-line friendly: Natural formatting for readable code
- Easy to extend: Add more forms without changing syntax
- Safe: No shell interpretation of Clojure code

## Examples

### Simple Expression (alternative for trivial cases)

```bash
brepl '(+ 1 2 3)'
```

### Multi-line Expressions

```bash
brepl "$(cat <<'EOF'
(require '[clojure.string :as str])
(str/join ", " ["a" "b" "c"])
EOF
)"
```

### Code with Quotes

```bash
brepl "$(cat <<'EOF'
(println "String with 'single' and \"double\" quotes")
EOF
)"
```

### Require a Namespace (always use :reload to pick up changes)

```bash
brepl "$(cat <<'EOF'
(require '[my.namespace :as ns] :reload)
EOF
)"
```

### Full Namespace Reload (including dependencies)

```bash
brepl "$(cat <<'EOF'
(require '[myapp.core] :reload-all)
EOF
)"
```

### Namespace Reloading and Testing

```bash
brepl "$(cat <<'EOF'
(require '[myapp.core] :reload)
(myapp.core/some-function "test" 123)
EOF
)"
```

### Complex Data Structures

```bash
brepl "$(cat <<'EOF'
(def config
  {:database {:host "localhost"
              :port 5432}
   :api {:key "secret-key"}})
(println (:database config))
EOF
)"
```

### Running Tests

```bash
brepl "$(cat <<'EOF'
(require '[clojure.test :refer [run-tests]])
(require '[myapp.core-test] :reload)
(run-tests 'myapp.core-test)
EOF
)"
```

### Documentation Lookup

```bash
brepl "$(cat <<'EOF'
(require '[clojure.repl :refer [doc source]])
(doc map)
(source filter)
EOF
)"
```

### Error Inspection

```bash
brepl "$(cat <<'EOF'
*e
(require '[clojure.repl :refer [pst]])
(pst)
EOF
)"
```

### Loading Files

To load an entire file into the REPL:

```bash
brepl -f src/myapp/core.clj
```

## Available Options

- `-e, --e <expr>` - Expression to evaluate
- `-f, --f <file>` - File to load and execute
- `-p, --p <port>` - nREPL port (auto-detects from .nrepl-port if not specified)
- `-h, --h <host>` - nREPL host (default: localhost or BREPL_HOST)
- `--verbose` - Show raw nREPL messages instead of parsed output
- `--help` - Show help message

## Port Configuration

The port is resolved in this order:

1. Command line: `-p 7888`
2. Auto-detect: `.nrepl-port` file in project directory
3. Environment: `BREPL_PORT=7888`

```bash
# Auto-detect from .nrepl-port (most common)
brepl -e '(+ 1 2)'

# Explicit port
brepl -p 7888 -e '(+ 1 2)'

# Using environment variable
BREPL_PORT=7888 brepl -e '(+ 1 2)'
```

## Critical Rules

1. Always use heredoc: Use the heredoc pattern for all brepl evaluations
2. Quote the delimiter: Always use `<<'EOF'` not `<<EOF` to prevent shell expansion
3. No escaping needed: Inside heredoc, write Clojure code naturally
4. Multi-step operations: Combine multiple forms in one heredoc block
5. Write correct Clojure: Ensure proper bracket balancing and valid syntax

## Important Notes

- Prefer heredoc pattern: Use heredoc for all but the simplest expressions to avoid quoting issues
- Always use :reload: When requiring namespaces, use `:reload` to pick up recent changes
- Auto-detection handles ports: No explicit port discovery needed in most cases
- The `-e` flag is optional: `brepl '(+ 1 2)'` works the same as `brepl -e '(+ 1 2)'`

## Typical Workflow

1. Ensure nREPL is running (creates .nrepl-port file)
2. Require namespace:
   ```bash
   brepl "$(cat <<'EOF'
   (require '[my.ns :as ns] :reload)
   EOF
   )"
   ```
3. Test function:
   ```bash
   brepl "$(cat <<'EOF'
   (ns/my-fn ...)
   EOF
   )"
   ```
4. Iterate: Make changes, re-require with `:reload`, test again

## Resources

brepl documentation: https://github.com/licht1stein/brepl (check extra/)
