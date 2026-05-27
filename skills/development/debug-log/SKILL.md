---
name: debug-log
description: Printf-style debug logging for development-time visibility
---

# Debug Log

Printf-style logging for development and debugging. Compiles away completely in release builds.

## Purpose

- Development-time visibility into program state
- Add arbitrary trace points during debugging
- Zero overhead in release builds

## Usage

```c
#include "debug_log.h"

DEBUG_LOG("value=%d state=%s", x, state_name);
DEBUG_LOG("=== Entering function ===");
DEBUG_LOG("buffer contents: %.*s", (int)len, buf);
```

## Build Configuration

| Build | DEBUG defined | Behavior |
|-------|---------------|----------|
| Debug | Yes | Writes to `IKIGAI_DEBUG.LOG` |
| Release | No | Compiles to `((void)0)` - removed entirely |

## Initialization

In debug builds, call once early in `main()`:

```c
#ifdef DEBUG
ik_debug_log_init();
#endif
```

Or simply use the macro form (safe in any build):

```c
ik_debug_log_init();  // No-op if DEBUG not defined
```

## Output Format

```
[2025-01-15 10:30:00] src/client.c:34:main: === Session starting, PID=12345 ===
```

Format: `[timestamp] file:line:function: message`

## Log Location

- File: `IKIGAI_DEBUG.LOG` in working directory
- Truncated on each run (via `ik_debug_log_init`)

## Inspecting Logs

```bash
tail -f IKIGAI_DEBUG.LOG
```

## Alternate Buffer Note

ikigai runs in terminal alternate buffer mode. `printf()` and `fprintf(stderr, ...)` are not visible during execution. Use `DEBUG_LOG` instead.

## Source Files

- `src/debug_log.h` - Macro definition
- `src/debug_log.c` - Implementation (excluded from coverage)
