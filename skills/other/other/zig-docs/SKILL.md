---
name: zig-docs
description: Fetches Zig language and standard library documentation via CLI. Activates when needing Zig API details, std lib function signatures, or language reference content that isn't covered in zig-best-practices.
---

# Zig Documentation Fetching

## Instructions

- Use raw GitHub sources for std lib documentation (most reliable)
- Use pandoc for language reference from ziglang.org (works for prose content)
- The std lib HTML docs at ziglang.org are JavaScript-rendered and return empty content; avoid them
- Zig source files contain doc comments (`//!` for module docs, `///` for item docs) that serve as authoritative documentation

## Quick Reference

### Fetch Standard Library Source (Recommended)

Standard library modules are self-documenting. Fetch source directly:

```bash
# Module source with doc comments
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/<module>.zig"

# Common modules:
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/log.zig"
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/mem.zig"
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/fs.zig"
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/heap.zig"
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/debug.zig"
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/testing.zig"
```

### Fetch Allocator Interface

```bash
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/mem/Allocator.zig"
```

### Fetch Language Reference (Prose)

```bash
# Full language reference (large, ~500KB of text)
pandoc -f html -t plain "https://ziglang.org/documentation/master/"

# Pipe to head for specific sections
pandoc -f html -t plain "https://ziglang.org/documentation/master/" | head -200
```

### List Standard Library Contents

```bash
# List all std lib modules via GitHub API
curl -sL "https://api.github.com/repos/ziglang/zig/contents/lib/std" | jq -r '.[].name'

# List subdirectory contents
curl -sL "https://api.github.com/repos/ziglang/zig/contents/lib/std/mem" | jq -r '.[].name'
```

### Fetch zig.guide Content

```bash
# Landing page and navigation
pandoc -f html -t plain "https://zig.guide/"
```

## Documentation Sources

| Source | URL Pattern | Notes |
|--------|-------------|-------|
| Std lib source | `raw.githubusercontent.com/ziglang/zig/master/lib/std/<path>` | Most reliable; includes doc comments |
| Language reference | `ziglang.org/documentation/master/` | Use pandoc; prose content |
| zig.guide | `zig.guide/` | Beginner-friendly; use pandoc |
| GitHub API | `api.github.com/repos/ziglang/zig/contents/lib/std` | List directory contents |

## Common Module Paths

| Module | Path |
|--------|------|
| Allocator | `lib/std/mem/Allocator.zig` |
| ArrayList | `lib/std/array_list.zig` |
| HashMap | `lib/std/hash_map.zig` |
| StringHashMap | `lib/std/hash/map.zig` |
| File System | `lib/std/fs.zig` |
| File | `lib/std/fs/File.zig` |
| IO | `lib/std/Io.zig` |
| Logging | `lib/std/log.zig` |
| Testing | `lib/std/testing.zig` |
| Debug | `lib/std/debug.zig` |
| Heap | `lib/std/heap.zig` |
| Build System | `lib/std/Build.zig` |
| JSON | `lib/std/json.zig` |
| HTTP | `lib/std/http.zig` |
| Thread | `lib/std/Thread.zig` |
| Process | `lib/std/process.zig` |

## Version-Specific Documentation

Replace `master` with version tag for stable releases:

```bash
# 0.14.0 release
curl -sL "https://raw.githubusercontent.com/ziglang/zig/0.14.0/lib/std/log.zig"

# Language reference for specific version
pandoc -f html -t plain "https://ziglang.org/documentation/0.14.0/"
```

## Searching Documentation

### Search for specific function/type in std lib

```bash
# Search for function name across std lib
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/<module>.zig" | grep -A5 "pub fn <name>"

# Example: find allocator.create
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/mem/Allocator.zig" | grep -A10 "pub fn create"
```

### Extract doc comments

```bash
# Module-level docs (//!)
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/log.zig" | grep "^//!"

# Function/type docs (///)
curl -sL "https://raw.githubusercontent.com/ziglang/zig/master/lib/std/mem/Allocator.zig" | grep -B1 "pub fn" | grep "///"
```

## Troubleshooting

**Empty content from ziglang.org/documentation/master/std/:**
- The std lib HTML docs are JavaScript-rendered; use raw GitHub instead

**pandoc fails:**
- Some pages require JavaScript; fall back to curl + raw GitHub
- Check URL is correct (no trailing slash issues)

**Rate limiting on GitHub API:**
- Use raw.githubusercontent.com URLs directly instead of API
- Cache frequently accessed content locally

## References

- Language Reference: https://ziglang.org/documentation/master/
- Standard Library Source: https://github.com/ziglang/zig/tree/master/lib/std
- Zig Guide: https://zig.guide/
- Release Tags: https://github.com/ziglang/zig/tags
