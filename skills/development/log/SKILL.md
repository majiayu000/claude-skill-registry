---
name: log
description: Logging skill for the ikigai project
---

# Logging

## Critical: Alternate Buffer Mode

ikigai runs in terminal alternate buffer mode. **stdout/stderr are not visible during execution.** Do not use `printf()` or `fprintf(stderr, ...)` for debugging.

Use the logger instead - it writes to a file you can inspect.

## Usage

```c
#include "logger.h"

// Legacy printf-style (being deprecated)
ik_log_debug("value=%d", x);
ik_log_info("started processing");
ik_log_warn("unexpected state");
ik_log_error("operation failed: %s", reason);

// New JSONL API (preferred)
yyjson_mut_doc *doc = ik_log_create();
yyjson_mut_val *root = yyjson_mut_doc_get_root(doc);
yyjson_mut_obj_add_str(doc, root, "event", "chunk_received");
yyjson_mut_obj_add_int(doc, root, "bytes", len);
ik_log_debug_json(doc);  // Takes ownership, frees doc
```

## Inspecting Logs

```bash
# Tail logs during development
tail -f $PWD/.ikigai/logs/current/log 

```

## Levels

- `debug` - Development tracing
- `info` - Normal operations
- `warn` - Recoverable issues
- `error` - Failures
- `fatal` - Calls `exit(1)` after logging
