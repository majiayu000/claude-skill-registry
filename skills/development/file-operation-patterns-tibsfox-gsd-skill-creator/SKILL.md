---
name: file-operation-patterns
description: Safe file operation patterns. Use when performing bulk file operations or writing deployment scripts.
---

# File Operation Patterns

## Safe Patterns

```bash
# Create directory tree (idempotent)
mkdir -p path/to/nested/dir

# Copy preserving permissions
cp -rp src/ dst/

# Atomic write (prevents partial reads)
tmpfile=$(mktemp "${target}.XXXXXX")
echo "$content" > "$tmpfile"
mv "$tmpfile" "$target"

# Safe deletion (guard variables)
[ -n "$DIR" ] && [ "$DIR" != "/" ] && rm -rf "$DIR"

# Incremental sync
rsync -av src/ dst/
```

## Anti-Patterns

| Don't | Do |
|-------|------|
| `rm -rf $DIR` unguarded | Guard with `[ -n "$DIR" ]` |
| Write directly to target | Write to temp, then `mv` |
| Assume dir exists | `mkdir -p` first |
| Ignore permissions | `cp -p` or explicit `chmod` |
