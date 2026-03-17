---
name: libsupervision
description: >
  libsupervision - Process supervision system. Supervisor manages process tree
  inspired by s6-svscan. LongRunner handles persistent processes with restart.
  OneShot handles single-execution tasks. ProcessState tracks process lifecycle.
  LogWriter manages process logging. Use for service management, process
  control, and graceful shutdown handling.
---

# libsupervision Skill

## When to Use

- Managing long-running service processes
- Implementing process supervision with restart
- Running one-shot initialization tasks
- Handling graceful shutdown across processes

## Key Concepts

**Supervisor**: Manages a tree of processes, handling startup order and
shutdown.

**LongRunner**: Process that restarts automatically on exit (for services).

**OneShot**: Process that runs once (for migrations, initialization).

**ProcessState**: Tracks process state transitions (starting, running, stopped).

## Usage Patterns

### Pattern 1: Create supervision tree

```javascript
import { Supervisor, LongRunner, OneShot } from "@copilot-ld/libsupervision";

const supervisor = new Supervisor();
supervisor.add(new OneShot("migrate", "npm run migrate"));
supervisor.add(new LongRunner("web", "npm start"));
await supervisor.start();
```

### Pattern 2: Handle signals

```javascript
process.on("SIGTERM", async () => {
  await supervisor.stop(); // Graceful shutdown
});
```

## Integration

Powers the service supervision system. Used by librc for service management.
