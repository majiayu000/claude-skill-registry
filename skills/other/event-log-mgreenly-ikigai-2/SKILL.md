---
name: event-log
description: JSONL event stream for external integrations and hooks
---

# Event Log

JSONL-based event logging for external program integration. Events mirror database event creation and enable hooks similar to Claude Code's event system.

## Purpose

- Emit structured events for external consumers
- Enable hook-based integrations
- Mirror the database event stream

## Log Location

- Default: `.ikigai/logs/current.log`
- Override: `$IKIGAI_LOG_DIR/current.log`

## APIs

### DI-Based (Preferred)

```c
#include "logger.h"

// Create logger with explicit context
ik_logger_t *logger = ik_logger_create(ctx, working_dir);

// Create and emit event
yyjson_mut_doc *doc = ik_log_create();
yyjson_mut_val *root = yyjson_mut_doc_get_root(doc);
yyjson_mut_obj_add_str(doc, root, "event", "chunk_received");
yyjson_mut_obj_add_int(doc, root, "bytes", len);
ik_logger_debug_json(logger, doc);  // Takes ownership, frees doc
```

### Legacy Global (Migration)

```c
// Initialize once
ik_log_init(working_dir);

// Emit events
yyjson_mut_doc *doc = ik_log_create();
// ... populate doc ...
ik_log_debug_json(doc);  // Takes ownership

// Shutdown
ik_log_shutdown();
```

## Log Levels

| Level | Function | Purpose |
|-------|----------|---------|
| debug | `ik_logger_debug_json()` | Verbose event tracing |
| info | `ik_logger_info_json()` | Normal operations |
| warn | `ik_logger_warn_json()` | Recoverable issues |
| error | `ik_logger_error_json()` | Failures |
| fatal | `ik_logger_fatal_json()` | Calls `exit(1)` after logging |

## Output Format

Each line is a JSON object:

```json
{"level":"debug","timestamp":"2025-01-15T10:30:00.123-05:00","logline":{"event":"chunk_received","bytes":1024}}
```

## Inspecting Events

```bash
tail -f .ikigai/logs/current.log
```

## Source Files

- `src/logger.h` - API declarations
- `src/logger.c` - Implementation
