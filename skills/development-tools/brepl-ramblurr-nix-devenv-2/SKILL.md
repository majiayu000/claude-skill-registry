---
name: brepl
description: Load this skill BEFORE using brepl in any way (mandatory). Teaches the heredoc pattern for reliable code evaluation.
---

# brepl - Evaluating Clojure Code

## CRITICAL: Load This Skill First

**You MUST load this skill before using brepl.** Do NOT attempt to use brepl without loading this skill first, or you will use incorrect syntax.

## Overview

brepl is a REPL client for evaluating Clojure expressions. This skill teaches the heredoc pattern for reliable code evaluation.

**Always load this skill before using brepl. Always use the heredoc pattern for all Clojure code evaluation.**

## The Heredoc Pattern - Default Approach

**Always use heredoc for brepl evaluation.** This eliminates quoting issues, works for all cases, and provides a consistent, reliable pattern.

### Syntax (Stdin - Recommended)

```bash
brepl <<'EOF'
(your clojure code here)
EOF
```

This is the simplest heredoc syntax - stdin feeds directly to brepl.

### Alternative Syntax (Positional Argument)

For simple one-liners, you can use positional arguments:

```bash
brepl '(+ 1 2 3)'
```

Heredoc is preferred for anything with quotes or multiple lines.

**Note**: The `-e` flag is optional - brepl automatically treats stdin and positional arguments as code to evaluate.

**Important**: Use `<<'EOF'` (with quotes) not `<<EOF` to prevent shell variable expansion.

### Examples

**Multi-line expressions**:

```bash
brepl <<'EOF'
(require '[clojure.string :as str])
(str/join ", " ["a" "b" "c"])
EOF
```

**Code with quotes**:

```bash
brepl <<'EOF'
(println "String with 'single' and \"double\" quotes")
EOF
```

**Reloading and testing**:

```bash
brepl <<'EOF'
(require '[myapp.core] :reload)
(myapp.core/some-function "test" 123)
EOF
```

**Complex data structures**:

```bash
brepl <<'EOF'
(def config
  {:database {:host "localhost"
              :port 5432
              :name "mydb"}
   :api {:key "secret-key"
         :endpoint "https://api.example.com"}})
(println (:database config))
EOF
```

**Running tests**:

```bash
brepl <<'EOF'
(require '[clojure.test :refer [run-tests]])
(require '[myapp.core-test] :reload)
(run-tests 'myapp.core-test)
EOF
```

## Alternative: Simple Expressions

For very simple expressions, you can use direct positional arguments:

```bash
# Simple expression
brepl '(inc 1)'

# Same with heredoc (consistent approach)
brepl <<'EOF'
(inc 1)
EOF
```

**Why prefer heredoc:** No mental overhead deciding which pattern to use, no risk of quoting issues, easy to extend.

## Loading Files

To load an entire file into the REPL:

```bash
brepl -f src/myapp/core.clj
```

After loading, you can evaluate functions from that namespace using either pattern.

## Fixing Unbalanced Brackets

Use `brepl balance` to fix unbalanced brackets in Clojure files using parmezan:

```bash
# Fix file in place (default)
brepl balance src/myapp/core.clj

# Preview fix to stdout
brepl balance src/myapp/core.clj --dry-run
```

This is useful for recovering files with bracket errors.

## Common Patterns

### Namespace reloading

```bash
brepl <<'EOF'
(require '[myapp.core] :reload-all)
EOF
```

### Documentation lookup

```bash
brepl <<'EOF'
(require '[clojure.repl :refer [doc source]])
(doc map)
(source filter)
EOF
```

### Error inspection

```bash
brepl <<'EOF'
*e
(require '[clojure.repl :refer [pst]])
(pst)
EOF
```

## Critical Rules

1. **Always use heredoc** - Use the heredoc pattern for all brepl evaluations
2. **Quote the delimiter** - Always use `<<'EOF'` not `<<EOF` to prevent shell expansion
3. **No escaping needed** - Inside heredoc, write Clojure code naturally
4. **Multi-step operations** - Combine multiple forms in one heredoc block
5. **Write correct Clojure** - Ensure proper bracket balancing and valid syntax

## Why Always Use Heredoc

**Consistency over optimization.** While simple positional arguments work for basic cases, using heredoc everywhere means:

1. **No decision fatigue** - One pattern for everything
2. **No quoting errors** - Everything between `<<'EOF'` and `EOF` is literal
3. **Easy to extend** - Add more lines without changing syntax
4. **Readable** - Clear where the code starts and ends
5. **Safe** - No shell interpretation of Clojure code

Shell quoting with Clojure is error-prone: Clojure uses both single and double quotes, nested quotes require escaping, and reader macros can confuse the shell. Heredoc eliminates all these issues.

## Resources

brepl documentation: https://github.com/licht1stein/brepl
