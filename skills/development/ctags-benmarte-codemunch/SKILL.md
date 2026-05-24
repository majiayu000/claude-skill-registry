---
description: Index the codebase using Universal ctags when LSP is unavailable for a language. Generates a JSON symbol table with name, kind, file, line, and end line for all detected symbols. Supports 40+ languages natively.
---

# ctags Indexing Skill

Use Universal ctags to build a symbol index when LSP is not available.

## Check ctags version

```bash
# Universal ctags has --output-format=json — we need this
ctags --version 2>&1 | grep -i universal
# If not universal ctags, basic ctags won't have JSON output
# Fall back to parsing classic ctags format instead
```

## Run ctags

```bash
universal-ctags \
  --recurse=yes \
  --output-format=json \
  --fields=+n+e+K+S+Z \
  --extras=+q+r \
  --exclude=node_modules \
  --exclude=.git \
  --exclude=target \
  --exclude=__pycache__ \
  --exclude=.claude/codemunch \
  --exclude=dist \
  --exclude=build \
  --exclude=vendor \
  -f - \
  . 2>/dev/null
```

## Field reference

- `n` — line number
- `e` — end line
- `K` — kind (long form: "function", "class", etc.)
- `S` — signature
- `Z` — scope (container class/module)

## Parse output into codemunch format

ctags JSON output per line:
```json
{"_type":"tag","name":"validateToken","path":"src/auth/tokens.ts","pattern":"/^async function validateToken/","kind":"function","line":142,"end":163,"signature":"(token: string): Promise<User | null>","scope":"AuthService","scopeKind":"class"}
```

**Filter noise kinds**: Skip noise kinds: constant, property, variable, enumerator. These inflate the index 15x without adding useful navigation value. Only keep symbols where kind is one of: function, method, class, interface, type, enum, namespace.

Map each kept symbol to codemunch format:
```json
{
  "name": "validateToken",
  "kind": "function",
  "file": "src/auth/tokens.ts",
  "start_line": 142,
  "end_line": 163,
  "signature": "(token: string): Promise<User | null>",
  "container": "AuthService",
  "engine": "ctags"
}
```

## Classic ctags fallback (non-universal)

If only basic/exuberant ctags is available (no JSON support):

```bash
ctags -R --fields=+iaS --extra=+q -f .claude/codemunch/tags .
```

Parse the tab-separated `.claude/codemunch/tags` file:
```
# format: name TAB file TAB pattern TAB kind TAB extensions...
validateToken  src/auth/tokens.ts  /^async function validateToken/  f  line:142
```

End line is not available in classic ctags — use the rg-fallback skill's brace-counting heuristic.
