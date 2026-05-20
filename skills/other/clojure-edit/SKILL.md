---
name: clojure-edit
description: ALWAYS use this skill when reading or editing Clojure, ClojureScript, CLJC, EDN, Babashka (.bb), or ClojureDart (.cljd) files. Clojure code is structurally sensitive — unbalanced parentheses, brackets, or braces produce broken files. This skill provides form-aware editing scripts, automatic syntax validation via a PostToolUse hook, and structural editing patterns that prevent the most common class of errors. Trigger for any operation on .clj, .cljs, .cljc, .edn, .bb, or .cljd files.
hooks:
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "~/.claude/skills/clojure-edit/scripts/validate_clojure_syntax.clj"
---

# Clojure Edit

Guidance for reading and editing Clojure code with attention to structural correctness, idiomatic patterns, and proper handling of s-expressions.

## Clojure LSP Integration

The **clojure-lsp plugin** provides real-time diagnostics for Clojure files. Use `mcp__ide__getDiagnostics` to check for syntax errors, unresolved symbols, and other issues after editing.

**Supported file types:** `.clj`, `.cljs`, `.cljc`, `.edn`, `.bb`, `.cljd`

**Workflow:**
1. Make edits using the patterns in this skill
2. Call `mcp__ide__getDiagnostics` to verify no errors were introduced
3. Fix any issues before proceeding

**Devbox note:** For projects using devbox, prefix Babashka commands with `devbox run --` (e.g., `devbox run -- bb scripts/...`).

## Reading Clojure Files

### Pattern-Based Reading Strategy

When reading Clojure files, use focused exploration rather than reading entire files:

1. **Read by namespace pattern**: Target specific namespaces or symbols
2. **Read by content pattern**: Search for specific forms or expressions
3. **Read strategically**: Focus on relevant sections to minimize context usage

### Using the read_clojure_file Script

This skill includes a Babashka script for pattern-based, structure-aware file reading. The script requires `bb` (Babashka) to be installed globally on your system:

```bash
# Find all defn forms, showing only signatures (collapsed view)
scripts/read_clojure_file.clj src/my/namespace.clj --form-type defn --collapsed

# Find functions by name pattern
scripts/read_clojure_file.clj src/my/namespace.clj --name-pattern "^process-"

# Search for content within forms
scripts/read_clojure_file.clj src/my/namespace.clj --content-pattern "http-request"

# Combine filters
scripts/read_clojure_file.clj src/my/namespace.clj --form-type defn --name-pattern "user" --collapsed
```

**Benefits:**
- Shows only function signatures when using `--collapsed`, not full bodies
- Filters by form type (defn, defmethod, def, etc.)
- Pattern matching on names and content
- Reduces context usage by focusing on relevant code

### Before Editing

Always read the file before editing IF:
- You haven't read it yet in this session
- External modifications might have occurred
- You need current context about the code structure

Skip reading ONLY if:
- You just wrote the file in the previous tool call
- You have current context from earlier in the session

## Editing Clojure Code Correctly

### Core Principle: Respect the Structure

Clojure code is built from s-expressions (forms). Always edit at the form level, not the character level.

### Editing Strategy

**1. Read First** (if needed)
```
Use Read tool to understand current structure
```

**2. Identify the Form to Edit**
- Locate the specific `defn`, `def`, `let`, or other form
- Understand its boundaries (opening and closing parens)
- Note indentation and surrounding context

**3. Use Edit Tool with Complete Forms**
- Provide complete, balanced s-expressions
- Match exact indentation from the source
- Include ALL parens in both old_string and new_string

**4. Verify Syntax**
- Ensure all opening parens have closing parens
- Check that brackets `[]` and braces `{}` are balanced
- Verify string quotes are closed

### Using the edit_clojure_form Script

This skill includes a Babashka script for form-aware editing that targets functions by name rather than text matching. The script requires `bb` (Babashka) to be installed globally on your system and resolves file paths relative to your current working directory.

#### Basic Usage

```bash
# Replace an entire function by name
scripts/edit_clojure_form.clj --file src/my/namespace.clj \
  --name my-function \
  --operation replace \
  --new-form "(defn my-function [x y]\n  (+ x y 10))"

# Insert a new function before an existing one
scripts/edit_clojure_form.clj --file src/my/namespace.clj \
  --name existing-function \
  --operation insert-before \
  --new-form "(defn helper [x]\n  (* x 2))"

# Insert after a function
scripts/edit_clojure_form.clj --file src/my/namespace.clj \
  --name my-function \
  --operation insert-after \
  --new-form "(defn related-function [x]\n  (my-function x x))"

# Target specific form types (useful for defmethod, etc.)
scripts/edit_clojure_form.clj --file src/my/namespace.clj \
  --name area \
  --form-type defmethod \
  --operation replace \
  --new-form "(defmethod area :circle [shape]\n  (* Math/PI (:radius shape) (:radius shape)))"
```

#### Working with Complex Multi-line Forms

For large or complex forms, use a heredoc with command substitution to avoid shell escaping issues:

```bash
# Use heredoc directly - no temp file needed!
scripts/edit_clojure_form.clj --file src/my/file.clj \
  --name old-function \
  --operation replace \
  --new-form "$(cat <<'EOF'
(defn my-complex-function
  "A complex function with lots of lines"
  {:malli/schema [:=> [:catn
                       [:name :string]
                       [:count :int]]
                  :string]}
  [name count]
  (let [result (complex-calculation name)]
    (process-with count result)))
EOF
)"
```

**Key points:**
- Use `$(cat <<'EOF' ... EOF)` - heredoc wrapped in command substitution
- Single quotes around `'EOF'` prevent variable expansion inside the heredoc
- No temp files needed - everything is inline and self-contained

**Alternative: Temp files** (if heredocs don't work in your shell)
```bash
cat > /tmp/my-form.clj << 'FORM_EOF'
(defn my-complex-function ...)
FORM_EOF

scripts/edit_clojure_form.clj --file src/my/file.clj \
  --name old-function \
  --operation replace \
  --new-form "$(cat /tmp/my-form.clj)"
```

#### Handling Function Names with Special Characters

Function names containing arrows (`->`, `->>`) or other shell-special characters must be quoted:

```bash
# CORRECT - quotes protect the arrow from shell interpretation
scripts/edit_clojure_form.clj --file src/my/file.clj \
  --name 'uri->endpoint-fn' \
  --operation replace \
  --new-form "..."

# WRONG - shell will interpret -> as redirection
scripts/edit_clojure_form.clj --file src/my/file.clj \
  --name uri->endpoint-fn \
  --operation replace \
  --new-form "..."
```

#### Preview Changes with Dry Run

Always preview complex edits before applying them:

```bash
scripts/edit_clojure_form.clj --file src/my/file.clj \
  --name my-function \
  --operation replace \
  --new-form "$(cat /tmp/new-form.clj)" \
  --dry-run | head -50
```

#### Understanding Error Messages

- **"Form not found: `<name>`"** - The target form doesn't exist, or the name is misspelled.
- **"Exception during edit: `<details>`"** - A parsing or manipulation error. Common causes: unbalanced parentheses, invalid syntax, file path issues.

#### Self-Editing Precautions

When editing the script itself:
1. Always use `--dry-run` first
2. Keep a backup or rely on git to restore if needed
3. Test the script immediately after editing

### Common Editing Patterns

#### Adding a New Function

```clojure
;; Use Edit to add after existing function
;; old_string: (end of previous function)
;; new_string: (end of previous function)\n\n(defn new-function [...] ...whole form...)

;; OR use the form-editing script:
;; scripts/edit_clojure_form.clj --file <file> --name <existing-fn> --operation insert-after --new-form "<new-defn>"
```

#### Modifying Function Body

```clojure
;; Replace entire defn form
;; old_string: (defn old-impl [args]\n  old-body)
;; new_string: (defn old-impl [args]\n  new-body)

;; OR use the form-editing script:
;; scripts/edit_clojure_form.clj --file <file> --name old-impl --operation replace --new-form "<new-defn>"
```

#### Adding to Let Bindings

```clojure
;; Replace entire let form
;; old_string: (let [existing bindings]\n  body)
;; new_string: (let [existing bindings\n        new-binding value]\n  body)
```

## Clojure Best Practices

For idiomatic Clojure patterns (conditionals, destructuring, control flow, function design, library usage), see `references/clojure_best_practices.md`.

For documentation practices (docstrings, Codox setup, cross-cutting concerns), see `references/documentation-practices.md`.

## Parenthesis Management

### Golden Rules

1. **Never edit partial forms** - Always include complete s-expressions
2. **Count your parens** - Opening parens must equal closing parens
3. **Match indentation** - Preserve the source's indentation style
4. **Edit structurally** - Think in forms, not lines

### Common Paren Errors to Avoid

```clojure
;; Missing closing paren:
(defn foo [x]
  (+ x 1)  ;; Missing closing paren for defn!

;; Correct:
(defn foo [x]
  (+ x 1))  ;; All parens balanced

;; Mismatched brackets:
(defn foo [x}  ;; [ paired with }
  (+ x 1))

;; Correct:
(defn foo [x]  ;; [ paired with ]
  (+ x 1))
```

### Self-Checking Strategy

Before submitting an edit:
1. Count opening parens in new_string
2. Count closing parens in new_string
3. Verify they match
4. Check bracket [] and brace {} pairs
5. Verify string quotes are paired

## Editing Decision Tree

```
Need to modify Clojure file?
│
├─ Adding new top-level form (defn, def, etc.)?
│  └─ Use Edit: old_string = end of file or previous form
│                new_string = previous context + new complete form
│
├─ Modifying existing function?
│  ├─ Small change (rename, add param)?
│  │  └─ Use Edit: Replace entire defn form
│  │
│  └─ Complete rewrite?
│     └─ Use Edit: Replace entire defn form
│
├─ Adding to existing form (let, cond, etc.)?
│  └─ Use Edit: Replace entire parent form
│
└─ Renaming symbol across file?
   └─ Use Edit with replace_all: true
      (Be careful with common names!)
```

## Reference Materials

- `references/clojure_best_practices.md` - Comprehensive coding guidelines
- `references/documentation-practices.md` - Docstrings, Codox, and documentation conventions
