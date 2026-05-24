---
name: search
description: Use when searching codebases with sg (ast-grep) or rg (ripgrep). Triggers on "find pattern", "search for", "ast-grep", "sg", "rg", code search tasks.
---

# Code Search Reference

## When to Use sg vs rg

| Need | Tool | Why |
|------|------|-----|
| Structural code pattern (functions, classes, imports) | `sg` | AST-aware, ignores formatting |
| Text/string/comment search | `rg` | Faster, no parse needed |
| Cross-language refactor | `sg --rewrite` | Safe structural replacement |
| Regex across files | `rg` | Full PCRE2 regex support |
| Find + replace respecting syntax | `sg --interactive` | Won't break code structure |

## sg Metavariables

| Syntax | Matches | Example |
|--------|---------|---------|
| `$NAME` | Exactly one AST node | `$FUNC(x)` matches `foo(x)` |
| `$$VAR` | Exactly one unnamed/anonymous node | Rarely needed directly |
| `$$$LIST` | Zero or more nodes (variadic) | `$FUNC($$$ARGS)` matches `foo()`, `foo(a)`, `foo(a, b, c)` |

`$$$` is the multi-node wildcard. Use it for argument lists, statement bodies, and anywhere the count varies.

## sg Patterns by Language

### Python

```bash
sg -p 'def $FUNC($$$ARGS)' -l py
sg -p 'async def $NAME($$$ARGS)' -l py
sg -p 'class $CLASS' -l py
sg -p 'except:' -l py
sg -p 'Optional[$T]' --rewrite '$T | None' -l py --interactive
sg -p 'assert $COND' -l py
sg -p '@$DECORATOR
def $FUNC($$$ARGS):
    $$$BODY' -l py
```

### TypeScript / TSX

```bash
sg -p 'import $X from $Y' -l ts
sg -p 'import { $$$NAMES } from $SOURCE' -l ts
sg -p 'function $NAME($$$ARGS): JSX.Element { $$$BODY }' -l tsx
sg -p 'console.log($$$ARGS)' -l ts
sg -p 'const $NAME = ($$$ARGS) => $$$BODY' -l ts
sg -p '$EXPR as $TYPE' -l ts
```

**React hooks — can't use `use$HOOK()` pattern.** ast-grep parses `use$HOOK` as a single identifier, not prefix + metavariable. Use rule YAML instead:

```yaml
# find-hooks.yml
id: find-react-hooks
language: tsx
rule:
  kind: call_expression
  regex: "^use[A-Z]"
```

```bash
sg scan --rule find-hooks.yml
```

### Go

Go often needs **pattern objects** because bare patterns are ambiguous without file-level context.

```yaml
# find-go-func.yml
id: find-functions
language: go
rule:
  kind: function_declaration
  has:
    kind: identifier
    regex: "^Handle"
```

```bash
sg -p 'fmt.Println($$$ARGS)' -l go
sg -p 'if err != nil { $$$BODY }' -l go
sg scan --rule find-go-func.yml
```

### Rust

```bash
sg -p 'fn $NAME($$$ARGS) -> $RET { $$$BODY }' -l rs
sg -p 'impl $TRAIT for $TYPE { $$$BODY }' -l rs
sg -p 'unwrap()' -l rs
sg -p '#[derive($$$ATTRS)]' -l rs
sg -p 'println!($$$ARGS)' -l rs
```

## sg Refactoring

```bash
sg -p 'console.log($$$ARGS)' --rewrite '' -l ts --interactive
sg -p 'require($MOD)' --rewrite 'import $MOD from $MOD' -l js
sg -p 'assert.equal($A, $B)' --rewrite 'expect($A).toBe($B)' -l ts
```

## sg Gotchas

- **Patterns must be valid parseable code** in the target language. `$FOO(` alone won't work.
- **Can't mix prefix text with metavariables** in identifiers. `use$Hook`, `get$Name` — none work. Use `kind:` + `regex:` rule instead.
- **Go needs pattern objects** for most structural matches. Bare patterns lack the package-level context Go's parser requires.
- **`$$$` is NOT `...`** — ast-grep uses `$$$` for variadic matching, not Semgrep's `...` syntax.
- **Rule ordering matters** — in compound rules, the first matched rule binds metavariables. Later rules see those bindings.

## rg Patterns

```bash
rg 'TODO|FIXME|HACK' --type-add 'code:*.{ts,py,rs,go}' -t code
rg '(def |fn |func |function )\w+' -t py -t rust -t go -t js
rg '^(import |from .+ import |require\()' -t py -t js -t ts
rg -l 'pattern'
rg -c 'pattern'
rg -C3 'pattern'
rg -F 'exact.match()'
rg -U 'struct \w+\s*\{[^}]*\}'
rg -v 'pattern'
rg -o '\b\w+Error\b'
rg --files-without-match 'test'
rg 'old' -r 'new'
```

## rg Essential Flags

| Flag | Purpose |
|------|---------|
| `-t type` | Filter by file type (`-t py`, `-t js`, `-t rust`) |
| `-g 'glob'` | Filter by glob (`-g '*.test.ts'`, `-g '!node_modules'`) |
| `-l` | List matching files only |
| `-c` | Count matches per file |
| `-C N` | Show N lines of context |
| `-F` | Fixed string, no regex |
| `-U` | Multiline mode |
| `-i` | Case insensitive |
| `-w` | Match whole words only |
| `-v` | Invert match |
| `-o` | Show only matched text |
| `-r 'text'` | Replace matched text in output |
| `--json` | Machine-readable JSON output |
| `-S` | Smart case (case-insensitive unless uppercase present) |
