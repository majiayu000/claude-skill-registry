---
name: kernel-basics
description: Essential Zephyr RTOS kernel services. Covers thread lifecycle and priority, the logging subsystem for diagnostics, and the interactive shell for real-time hardware inspection and debugging. Trigger when writing application flows, adding logging to modules, or creating interactive CLI commands.
---

# Zephyr Kernel Basics

Master the essential services that bring your Zephyr application to life.

## Core Workflows

### 1. Threads & Scheduling
Create and manage multi-threaded application flows.
- **Reference**: **[threads.md](references/threads.md)**
- **Key Tools**: `K_THREAD_DEFINE`, `k_sleep`, `k_yield`, Priorities.

### 2. Logging & Diagnostics
Implement layered logging for better observability and troubleshooting.
- **Reference**: **[logging.md](references/logging.md)**
- **Key Tools**: `LOG_MODULE_REGISTER`, `LOG_INF`, `LOG_ERR`, Dynamic Filtering.

### 3. Interactive Shell (CLI)
Build powerful command-line interfaces for hardware and software inspection.
- **Reference**: **[shell.md](references/shell.md)**
- **Key Tools**: `SHELL_CMD_REGISTER`, `SHELL_STATIC_SUBCMD_SET_CREATE`.

## Quick Start (Logging)
```c
#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(my_app, CONFIG_APP_LOG_LEVEL);

void my_fn(void) {
    LOG_INF("Hello from Zephyr!");
}
```

## Quick Start (Threads)
```c
K_THREAD_DEFINE(worker_tid, 1024, worker_fn, NULL, NULL, NULL, 5, 0, 0);
```

## Resources

- **[References](references/)**:
  - `threads.md`: Configuration and creation of kernel threads.
  - `logging.md`: Log levels, modules, and backends.
  - `shell.md`: Interactive command registration and subcommands.
