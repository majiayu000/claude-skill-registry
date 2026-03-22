---
description: Fetch the exact source code of a named symbol (function, class, method, type) from the codebase using the codemunch index. Reads only the lines for that symbol — not the whole file. Uses LSP for hover docs and type info when available. This is the core token-saving operation.
---

# Fetch Skill

Retrieve the exact source of a named symbol. Read 20 lines instead of 800.

## Usage

Called with a symbol name, e.g.: `validateToken`, `AuthService`, `getUserById`, `Invoice`

## Step 1 — Look up in index

```bash
# Read the index
cat .claude/codemunch/index.json | python3 -c "
import json, sys
idx = json.load(sys.stdin)
name = '$SYMBOL_NAME'
matches = [s for s in idx['symbols'] if s['name'].lower() == name.lower()]
print(json.dumps(matches, indent=2))
" 2>/dev/null

# Or with jq if available
jq --arg n "$SYMBOL_NAME" '[.symbols[] | select(.name | ascii_downcase == ($n | ascii_downcase))]' \
  .claude/codemunch/index.json 2>/dev/null
```

If no index exists: the staleness-gate skill will have already built it before this skill runs.

If multiple matches (e.g. overloaded methods or same name in different files), show a disambiguation list and ask which one.

## Step 2 — Extract the symbol source

Use the `start_line` and `end_line` from the index entry to read only those lines:

```bash
FILE="src/auth/tokens.ts"
START=142
END=163

# Add a few lines of context before (for decorators, comments, annotations)
CONTEXT_BEFORE=3
ACTUAL_START=$((START - CONTEXT_BEFORE))
[ $ACTUAL_START -lt 1 ] && ACTUAL_START=1

sed -n "${ACTUAL_START},${END}p" "$FILE"
```

**Token count for this operation: ~20-40 tokens**
**Token count for reading the full file: ~5,000-15,000 tokens**

## Step 3 — Enrich with LSP (when available)

If LSP is configured for this language, additionally fetch:

**Hover information** — type signature, documentation:
```
Use Claude Code's /lsp tool:
  textDocument/hover
  position: { line: START_LINE, character: 0 }
```

**Type signature** — already in index if built with LSP, but refresh if stale

**Find references count** — how many places call this symbol:
```
Use /lsp:
  textDocument/references (just count, don't fetch all)
```

## Step 4 — Display

Show the symbol in this format:

```
📍 validateToken  [function]  src/auth/tokens.ts:142-163
   Engine: LSP  |  Signature: validateToken(token: string): Promise<User | null>
   Container: AuthService  |  References: 14
   ─────────────────────────────────────────
   [source code lines 139-163]
   ─────────────────────────────────────────
   Tokens used: ~35  (vs ~8,400 to read full file — 99.6% savings)
```

## Step 5 — Update usage stats

Append to `.claude/codemunch/session.log`:
```
fetch|validateToken|src/auth/tokens.ts:142-163|35 tokens|lsp
```

## Fallback for missing end_line (rg-indexed symbols)

If `end_line` is null (rg fallback didn't have it), use a smart heuristic:

```bash
# Read from start_line until we find the closing brace at the same indent level
# or until the next function/class declaration
# Max 60 lines to avoid reading too much
awk -v start=$START_LINE -v max=60 '
  NR==start { depth=0; capture=1 }
  capture {
    print
    # Count opening and closing braces/blocks
    for(i=1;i<=length($0);i++) {
      c=substr($0,i,1)
      if(c=="{" || c=="(" || c=="[") depth++
      if(c=="}" || c==")" || c=="]") depth--
    }
    if(NR>start && depth<=0) exit
    if(NR>start+max) exit
  }
' "$FILE"
```
