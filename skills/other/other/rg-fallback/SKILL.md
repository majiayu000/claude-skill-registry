---
description: Index symbols using ripgrep regex patterns when neither LSP nor ctags is available. Covers TypeScript, JavaScript, Python, Go, Rust, Ruby, Java, Kotlin, C, C++, PHP, and can be extended with custom patterns for any language via .claude/codemunch/config.json.
---

# Ripgrep Pattern Indexing Skill

Last-resort indexing using language-aware regex patterns. Works on any language — if rg is installed, codemunch works.

## Built-in patterns per language

Run the appropriate pattern for each detected language:

```bash
# --- TypeScript / JavaScript ---
rg --json --pcre2 \
  "^(export\s+)?(default\s+)?(async\s+)?function\s+(\w+)|^\s{0,2}(async\s+)?(\w+)\s*[=:]\s*(async\s+)?\(|^(export\s+)?(abstract\s+)?class\s+(\w+)|^(export\s+)?interface\s+(\w+)|^(export\s+)?type\s+(\w+)\s*=" \
  --type ts --type js \
  --glob "!node_modules" --glob "!dist" --glob "!.next" \
  2>/dev/null

# --- Python ---
rg --json \
  "^(async\s+)?def\s+(\w+)|^class\s+(\w+)" \
  --type py \
  --glob "!__pycache__" \
  2>/dev/null

# --- Go ---
rg --json \
  "^func\s+(\([\w\s\*]+\)\s+)?(\w+)|^type\s+(\w+)\s+(struct|interface|func)" \
  --type go \
  2>/dev/null

# --- Rust ---
rg --json \
  "^(pub(\([\w:]+\))?\s+)?(async\s+)?fn\s+(\w+)|^(pub(\([\w:]+\))?\s+)?(struct|enum|trait|type)\s+(\w+)|^impl(\s*<[^>]+>)?\s+(\w+)" \
  --type rust \
  2>/dev/null

# --- Ruby ---
rg --json \
  "^\s*(def\s+(self\.)?(\w+)|class\s+(\w+)|module\s+(\w+))" \
  --type ruby \
  2>/dev/null

# --- Java ---
rg --json \
  "(public|private|protected|package)(\s+static)?(\s+\w+)+\s+(\w+)\s*\(|^(public|private|protected)?\s*(abstract\s+)?class\s+(\w+)|^(public\s+)?interface\s+(\w+)" \
  --type java \
  2>/dev/null

# --- Kotlin ---
rg --json \
  "^(fun\s+(\w+)|class\s+(\w+)|object\s+(\w+)|interface\s+(\w+)|data\s+class\s+(\w+))" \
  --type kotlin \
  2>/dev/null

# --- C ---
rg --json \
  "^[\w\s\*]+\s+(\w+)\s*\([^;{]*\)\s*\{|^(struct|enum|union)\s+(\w+)\s*\{" \
  --type c \
  2>/dev/null

# --- C++ ---
rg --json \
  "^[\w\s\*:<>]+\s+(\w+)\s*\([^;]*\)\s*(const\s*)?\{|^(class|struct|enum)\s+(\w+)" \
  --type cpp \
  2>/dev/null

# --- PHP ---
rg --json \
  "^(public|private|protected|static|\s)*(function\s+(\w+))|^(abstract\s+)?class\s+(\w+)|^interface\s+(\w+)" \
  --type php \
  2>/dev/null

# --- Swift ---
rg --json \
  "^(public|private|internal|open|fileprivate)?\s*(static\s+)?(func\s+(\w+)|class\s+(\w+)|struct\s+(\w+)|enum\s+(\w+)|protocol\s+(\w+))" \
  --type swift \
  2>/dev/null

# --- Shell / Bash ---
rg --json \
  "^(function\s+)?(\w+)\s*\(\s*\)\s*\{" \
  --type sh \
  2>/dev/null

# --- Lua ---
rg --json \
  "^(local\s+)?function\s+(\w[\w\.]*)|^(\w[\w\.]*)\s*=\s*function" \
  --type lua \
  2>/dev/null

# --- Zig ---
rg --json \
  "^(pub\s+)?fn\s+(\w+)|^(pub\s+)?const\s+(\w+)\s*=\s*(struct|enum|union)" \
  --type zig \
  2>/dev/null
```

## Noise filtering

Skip noise kinds: constant, property, variable, enumerator. These inflate the index 15x without adding useful navigation value. The rg patterns above should only match function/class/interface/type declarations, not `const`/`let`/`var` assignments unless they are arrow functions (e.g. `const foo = async (`). If a matched line is a plain variable assignment (no arrow function or class expression), discard it.

Only keep symbols whose kind resolves to: function, method, class, interface, type, enum, namespace.

## Parse ripgrep JSONL output

Each match looks like:
```json
{"type":"match","data":{"path":{"text":"src/auth/tokens.ts"},"lines":{"text":"async function validateToken(token: string): Promise<User | null> {\n"},"line_number":142,"absolute_offset":4821,"submatches":[...]}}
```

Extract:
- `file` = `data.path.text`
- `start_line` = `data.line_number`
- `name` = parse from `data.lines.text` using the matched group
- `end_line` = use brace-counting heuristic (see fetch skill)
- `signature` = the full match line, trimmed

## Custom patterns via config

Users can add patterns for any language in `.claude/codemunch/config.json`:

```json
{
  "custom_patterns": {
    "solidity": {
      "function": "^\\s*(function|modifier|event|error)\\s+(\\w+)",
      "class": "^(contract|library|interface)\\s+(\\w+)"
    },
    "hcl": {
      "function": "^(resource|data|module|variable|output)\\s+\"(\\w+)\"\\s+\"(\\w+)\""
    },
    "prisma": {
      "class": "^(model|enum)\\s+(\\w+)\\s+\\{"
    }
  }
}
```
