---
name: uroot
description: u-root utility implementation patterns (streaming I/O, error format, symlinks)
disable-model-invocation: false
---

# u-root Utils Integration

This skill covers implementing u-root utility commands in Invowk.

Use this skill when working on:
- `internal/uroot/` - u-root utility implementations
- Adding new built-in shell utilities
- Modifying u-root command behavior

---

## Terminology

**Standardized naming conventions:**

- **Project name**: "u-root" (lowercase with hyphen) — use in prose, documentation, and comments
- **Go identifiers**: "uroot" (lowercase, no hyphen) — use for package names, types, and variables
- **Config option**: `enable_uroot_utils` — existing schema, follows Go/CUE convention

**Examples:**
- Prose: "The u-root integration provides built-in utilities..."
- Package: `internal/uroot/`
- Type: `UrootCommand`, `UrootHandler`
- Function: `tryUrootBuiltin()`
- Config: `virtual_shell.enable_uroot_utils: true`

**Rationale:** Consistent terminology reduces confusion. The hyphenated form matches the upstream project name (`github.com/u-root/u-root`), while the unhyphenated form follows Go naming conventions (hyphens are not allowed in identifiers).

---

## Streaming I/O Requirement

**CRITICAL: All u-root utility implementations MUST use streaming I/O for file operations.**

Never buffer entire file contents into memory, regardless of file size. This rule ensures:
- Predictable memory usage independent of input size
- No OOM conditions when processing large files
- Consistent behavior across all file sizes

### Required Pattern

```go
// CORRECT: Streaming copy with proper close handling
func copyFile(src, dst string) (err error) {
    srcFile, err := os.Open(src)
    if err != nil {
        return err
    }
    defer func() { _ = srcFile.Close() }() // Read-only source; close error non-critical

    dstFile, err := os.Create(dst)
    if err != nil {
        return err
    }
    defer func() {
        if closeErr := dstFile.Close(); closeErr != nil && err == nil {
            err = closeErr
        }
    }()

    _, err = io.Copy(dstFile, srcFile)  // Streams in chunks
    return err
}
```

### Anti-Patterns to Avoid

```go
// WRONG: Loads entire file into memory
data, err := os.ReadFile(src)
if err != nil {
    return err
}
err = os.WriteFile(dst, data, 0644)

// WRONG: Buffering entire content
content, _ := io.ReadAll(reader)
writer.Write(content)
```

### Applies To

All u-root utility implementations that handle file content:
- `cp` - File copying
- `mv` - File moving (when cross-filesystem)
- `cat` - File concatenation
- `head` / `tail` - File viewing
- `grep` - Pattern matching (line-by-line streaming)
- `sort` - Sorting (may require temp files for large inputs)
- `wc` - Word/line counting (streaming counters)

### Exception: Sorting Large Files

`sort` may need to use temporary files for inputs that exceed available memory. This is acceptable as it's the standard approach used by GNU sort (`-T` tempdir). The key constraint remains: never hold unbounded data in heap memory.

---

## Symlink Handling

**Default behavior: Follow symlinks (copy target content, not the link).**

This matches standard POSIX `cp` behavior and prevents symlink-based path traversal attacks.

- `cp source dest` where `source` is a symlink → copies the target file content
- `cp -r dir/ dest/` where `dir/` contains symlinks → copies target contents, not links
- Symlink preservation requires explicit `-P` flag (when supported)

### Security Rationale

Following symlinks by default prevents:
- Symlink attacks where a malicious link points outside the intended directory
- Accidental exposure of sensitive files via symlink indirection
- Unexpected behavior when copying between filesystems

---

## Unsupported Flag Handling

When a u-root utility receives flags it doesn't support (e.g., GNU-specific extensions like `--color`):

- **Silently ignore** the unsupported flag
- Execute the command with supported flags only
- Do NOT emit warnings or errors for unknown flags

This matches common cross-platform behavior where BSD utilities ignore GNU-specific flags.

---

## Error Reporting Format

**All errors from u-root utilities MUST be prefixed with `[uroot]`.**

This prefix clearly identifies the error source, distinguishing u-root implementation errors from system utility errors and aiding debugging.

### Required Format

```
[uroot] <command>: <error message>
```

### Examples

```
[uroot] cp: cannot stat 'missing': No such file or directory
[uroot] mv: cannot move 'src' to 'dst': Permission denied
[uroot] cat: /path/to/file: Is a directory
[uroot] mkdir: cannot create directory 'existing': File exists
```

### Implementation Pattern

```go
// CORRECT: Prefix errors with [uroot]
func (h *CpHandler) Run(ctx context.Context, args []string) error {
    // ... implementation ...
    if err != nil {
        return fmt.Errorf("[uroot] cp: %w", err)
    }
    return nil
}

// WRONG: Raw error without prefix
func (h *CpHandler) Run(ctx context.Context, args []string) error {
    if err != nil {
        return fmt.Errorf("cp: %w", err)  // Missing [uroot] prefix!
    }
    return nil
}
```

### Rationale

- Users can immediately identify whether an error comes from u-root or system utilities
- Simplifies debugging when both u-root and system utilities are used in the same script
- Enables targeted troubleshooting of u-root implementations vs environment issues

---

## Common Pitfalls

- **Buffering file contents** - Always use `io.Copy()` or similar streaming patterns. Never use `os.ReadFile()` or `io.ReadAll()` for arbitrary user files.
- **Missing error prefix** - All u-root errors must include the `[uroot]` prefix for source identification.
- **Naked defer Close()** - Never use `defer f.Close()`. For read-only files, use `defer func() { _ = f.Close() }()` with comment. For write operations, use named returns to capture close errors.
