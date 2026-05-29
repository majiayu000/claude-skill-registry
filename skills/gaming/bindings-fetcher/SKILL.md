---
name: FFI Bindings Fetcher
description: This skill should be used when the user asks to "fetch FFI bindings", "update zx.rs", "update zx.h", "update zx.zig", "get latest bindings", "download FFI", "refresh bindings", "update FFI module", or mentions updating, fetching, or downloading Nethercore ZX FFI bindings for their game project.
version: 1.0.0
---

# FFI Bindings Fetcher

## Overview

Nethercore ZX FFI bindings are auto-generated at build time and hosted publicly on GitHub. Always fetch the complete bindings file - never copy individual functions inline.

## Bindings URLs

| Language | GitHub URL |
|----------|------------|
| Rust | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs` |
| C | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h` |
| Zig | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig` |

## Fetch Commands

### Rust Projects

```bash
# Fetch to src/zx.rs
curl -o src/zx.rs https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs
```

**Usage in code:**
```rust
// src/lib.rs
mod zx;
use zx::*;

// src/player.rs (or any other module)
use crate::zx::*;
```

### C Projects

```bash
# Fetch to project root
curl -o zx.h https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h
```

**Usage in code:**
```c
#include "zx.h"
```

### Zig Projects

```bash
# Fetch to src/zx.zig
curl -o src/zx.zig https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig
```

**Usage in code:**
```zig
const zx = @import("zx.zig");
```

## Fetching via WebFetch

When using Claude Code's WebFetch tool to retrieve bindings:

**Prompt:** "Return the complete file contents exactly as-is. This is FFI bindings code."

Save the fetched content to the appropriate location:
- Rust: `src/zx.rs`
- C: `zx.h` (project root)
- Zig: `src/zx.zig`

## When to Update Bindings

Update bindings when:
1. Starting a new project
2. After a Nethercore console update
3. When encountering FFI function signature errors
4. When needing newly added FFI functions

## Critical Rules

1. **Never edit bindings files** - They are auto-generated and will be overwritten
2. **Never copy functions inline** - Always use the complete bindings file
3. **Use module imports** - Access FFI through proper module system
4. **Keep lib.rs minimal** - Only mod declarations and entry points (~50 lines)

## Project File Limits

When generating game code, follow these limits:

| File | Max Lines | Purpose |
|------|-----------|---------|
| lib.rs/main.zig/game.c | 50 | Entry points + mod declarations only |
| System files | 300 | Individual game systems |
| Feature directories | 300/file | Complex features split into modules |

## Bindings Contents

The bindings files contain (~1700 lines for Rust):
- FFI function declarations
- Type definitions (handles, enums, structs)
- Helper functions and macros
- Complete documentation comments

All 250+ FFI functions are included - no need to add anything manually.
