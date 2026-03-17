---
name: paren-debug
description: Debug parenthesis balance issues in Scheme files. Invoke when encountering "unexpected end-of-file reading list" or "unexpected close parenthesis" errors, or when manually counting parens.
allowed-tools: Bash(scheme:*, ./fold:*), Read, Grep
---

# Paren Debug Skill

## When to Use

Invoke this skill when you encounter:
- `Exception in read: unexpected end-of-file reading list at line N`
- `Exception in read: unexpected close parenthesis at line N`
- Any situation where you're manually counting parentheses
- After editing Scheme code and getting parse errors

## Tools Available

### `paren-locate` - Primary Tool (Stack-Based)

The most useful tool. Shows **exact locations** of paren errors:

```bash
scheme -q <<'EOF'
(load "boundary/tools/paren-check.ss")
(paren-locate "path/to/file.ss")
EOF
```

Output format is compiler-friendly (file:line:col):
```
path/to/file.ss:46:1: error: unclosed '(' - never closed
path/to/file.ss:61:19: error: mismatched brackets: opened '[' at line 61 col 12, closed with ')'
```

### `paren-ok?` - Quick Check

Returns `#t` if file is balanced, `#f` otherwise:

```bash
scheme -q <<'EOF'
(load "boundary/tools/paren-check.ss")
(paren-ok? "path/to/file.ss")
EOF
```

### `paren-errors` - Programmatic Access

Returns list of error structs for further processing:

```bash
scheme -q <<'EOF'
(load "boundary/tools/paren-check.ss")
(paren-errors "path/to/file.ss")
EOF
```

### `paren-check` - Legacy Balance Report

Line-by-line balance report (less precise but shows running totals):

```bash
scheme -q <<'EOF'
(load "boundary/tools/paren-check.ss")
(paren-check "path/to/file.ss")
EOF
```

### `./fold -c` / `./fold --check-syntax` - Quick CLI Check

Fast paren check from command line (no daemon needed):

```bash
./fold -c path/to/file.ss
./fold --check-syntax path/to/file.ss
```

Output:
```
# Success:
path/to/file.ss: ✓ All parentheses balanced

# Error:
path/to/file.ss:46:1: error: unclosed '(' - never closed
```

Exit codes: 0 = balanced, 1 = errors found.

## Workflow

1. **When you see a paren error**: Run `paren-locate` first
2. **Read the error location**: The output tells you exactly which opener was never closed
3. **Fix at the source**: Go to the reported line/column and add the missing closer
4. **Verify**: Run `paren-ok?` to confirm the fix

## Example Session

```bash
# 1. You edited exports.ss and get:
#    Exception in read: unexpected end-of-file reading list at line 46

# 2. Run paren-locate
scheme -q <<'EOF'
(load "boundary/tools/paren-check.ss")
(paren-locate "boundary/introspect/exports.ss")
EOF

# Output:
# boundary/introspect/exports.ss:46:1: error: unclosed '(' - never closed

# 3. The error is at line 46, column 1 - that's where the unclosed ( is!
#    NOT at the end of the file where Scheme complained.

# 4. Fix and verify:
scheme -q <<'EOF'
(load "boundary/tools/paren-check.ss")
(paren-ok? "boundary/introspect/exports.ss")
EOF
# Output: #t
```

## Error Types Detected

| Type | Message Pattern | Meaning |
|------|----------------|---------|
| `unclosed` | `unclosed '(' - never closed` | Opener at this location has no matching closer |
| `extra-close` | `unexpected ')' - no matching opener` | Closer with no corresponding opener |
| `mismatch` | `opened '[' at line X, closed with ')'` | Wrong bracket type used to close |

## Tips

- **Don't count parens manually** - always use `paren-locate`
- **The error location is where to fix** - unlike Scheme's error which points to where the list started
- **Check after every significant edit** - catch errors early
- **Mismatch detection** - the tool catches `(foo]` style errors that pure counting misses

## File Location

`boundary/tools/paren-check.ss` - Load this to access all paren-checking functions.
