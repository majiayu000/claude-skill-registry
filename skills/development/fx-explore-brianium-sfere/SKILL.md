---
name: fx-explore
description: Discover available effects, actions, and placeholders in a Sandestin project. Use when asking what effects exist, searching for functionality, or needing example invocations. Keywords: effects, actions, dispatch, describe, grep, sample.
---

# Sandestin Effect Explorer

Discover and understand available effects, actions, and placeholders.

**Important:** All discoverability functions operate on the **dispatch function**, not registries. You must first create a dispatch via `(s/create-dispatch [registries...])` before using these functions.

## About Sandestin

Sandestin is a Clojure effect dispatch library with schema-driven discoverability. Effects are dispatched as vectors like `[:myapp/save-user {:name "Alice"}]`.

**GitHub:** https://github.com/brianium/sandestin

### Check if Installed

Look for the dependency in `deps.edn`:

```clojure
io.github.brianium/sandestin {:git/tag "v0.3.0" :git/sha "2be6acc"}
```

### Install if Missing

Add to `deps.edn` under `:deps`:

```clojure
{:deps
 {io.github.brianium/sandestin {:git/tag "v0.3.0" :git/sha "2be6acc"}}}
```

## Workflow

### 1. Find the Dispatch

Search for `create-dispatch` to locate the project's dispatch namespace.

### 2. Explore via REPL

```clojure
(require '[ascolais.sandestin :as s])
(require '[<dispatch-ns> :refer [dispatch]])

;; List everything
(s/describe dispatch)

;; Filter by type
(s/describe dispatch :effects)
(s/describe dispatch :actions)
(s/describe dispatch :placeholders)

;; Search by keyword
(s/grep dispatch "user")
(s/grep dispatch #"save|create")

;; Get details on specific item
(s/describe dispatch :some.ns/effect-name)

;; Generate sample invocation
(s/sample dispatch :some.ns/effect-name)

;; See system requirements
(s/system-schema dispatch)
```

## Output Format

Summarize findings:

```
### Effects

**:myapp.db/query** - Execute a SQL query
  Requires: [:datasource]
  Example: [:myapp.db/query "SELECT * FROM users" 42]

### Actions

**:myapp.user/create** - Create user and send welcome email
  Expands to: db insert + email send
```

## Key Functions

| Function | Purpose |
|----------|---------|
| `(s/describe dispatch)` | List all items |
| `(s/describe dispatch :key)` | Details for specific item |
| `(s/grep dispatch "pattern")` | Search by string/regex |
| `(s/sample dispatch :key)` | Generate sample data |
| `(s/system-schema dispatch)` | System requirements |
